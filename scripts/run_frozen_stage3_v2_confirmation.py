from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import joblib

from docguard_eval_v2.reference_evaluation import generation_view, sha256_file, write_json, write_jsonl
from docguard_ml_v2.data_contract import binary_eligible_rows, load_jsonl, serialize_model_row
from docguard_ml_v2.model_manifest import utc_now
from docguard_llm_v2.pipeline import generate_semantic_documentation_patch, load_config


REFERENCE_FIELDS = {"docs_after", "docs_after_excerpt", "docs_diff_excerpt", "gold_patch_summary", "gold_docs_update_required", "gold_doc_category", "human_label_notes"}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_hash(path: Path, expected: str | None, label: str) -> str:
    actual = sha256_file(path)
    if expected and actual != expected:
        raise ValueError(f"{label} hash mismatch")
    return actual


def validate_inputs(*, confirmation: Path, partition_manifest: Path, binary_model: Path, binary_freeze_manifest: Path, category_model: Path, category_freeze_manifest: Path, stage3_config: Path, stage3_freeze_manifest: Path) -> dict[str, Any]:
    partition = load_json(partition_manifest)
    if partition.get("confirmation_sealed") is not True:
        raise ValueError("Repository partition manifest must have confirmation_sealed=true")
    rows = load_jsonl(confirmation)
    assignments = {str(repo).lower(): part for repo, part in (partition.get("repository_assignments") or {}).items()}
    for row in rows:
        if row.get("partition") != "confirmation" or assignments.get(str(row.get("repository") or "").lower()) != "confirmation":
            raise ValueError(f"Non-confirmation row detected: {row.get('case_id')}")
    binary_freeze = load_json(binary_freeze_manifest)
    category_freeze = load_json(category_freeze_manifest)
    stage3_freeze = load_json(stage3_freeze_manifest)
    hashes = {
        "confirmation_dataset_hash": sha256_file(confirmation),
        "repository_partition_manifest_hash": sha256_file(partition_manifest),
        "binary_model_hash": validate_hash(binary_model, binary_freeze.get("hashes", {}).get("model"), "binary model"),
        "binary_freeze_manifest_hash": sha256_file(binary_freeze_manifest),
        "category_model_hash": validate_hash(category_model, category_freeze.get("hashes", {}).get("model"), "category model"),
        "category_freeze_manifest_hash": sha256_file(category_freeze_manifest),
        "stage3_freeze_manifest_hash": sha256_file(stage3_freeze_manifest),
        "stage3_config_hash": validate_hash(stage3_config, stage3_freeze.get("config_sha256"), "Stage 3 config"),
    }
    for rel_path, expected_hash in (stage3_freeze.get("source_file_sha256") or {}).items():
        current = PROJECT_ROOT / "docguard_llm_v2" / str(rel_path)
        if current.exists() and sha256_file(current) != expected_hash:
            raise ValueError(f"Stage 3 source hash mismatch: {rel_path}")
    return {"rows": rows, "hashes": hashes, "stage3_freeze": stage3_freeze}


def one_shot_guard(output_dir: Path, hashes: dict[str, str], *, enforce: bool, allow_repeat: bool) -> None:
    receipt = output_dir / "stage3_confirmation_generation_receipt.json"
    if not enforce or not receipt.exists():
        return
    old = load_json(receipt)
    same = all(old.get(key) == hashes.get(key) for key in ["confirmation_dataset_hash", "binary_model_hash", "category_model_hash", "stage3_freeze_manifest_hash"])
    if same and not allow_repeat:
        raise ValueError("Frozen Stage 3 confirmation generation already ran for this frozen configuration and dataset.")


def positive_probability(model: Any, row: dict[str, Any]) -> float:
    proba = model.predict_proba([row])[0]
    classes = list(model.named_steps["classifier"].classes_) if hasattr(model, "named_steps") else list(model.classes_)
    return float(proba[classes.index(1)])


def category_prediction(model: Any, row: dict[str, Any]) -> tuple[str, dict[str, float]]:
    label = str(model.predict([row])[0])
    probs: dict[str, float] = {}
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba([row])[0]
        classes = list(model.named_steps["classifier"].classes_) if hasattr(model, "named_steps") else list(model.classes_)
        probs = {str(cls): float(proba[index]) for index, cls in enumerate(classes)}
    return label, probs


def run(*, confirmation: Path, repository_partition_manifest: Path, binary_model: Path, binary_freeze_manifest: Path, category_model: Path, category_freeze_manifest: Path, stage3_config: Path, stage3_freeze_manifest: Path, output_dir: Path, llm_backend: Any, enforce_one_shot: bool = False, allow_repeat_for_reproducibility: bool = False) -> dict[str, Any]:
    validation = validate_inputs(confirmation=confirmation, partition_manifest=repository_partition_manifest, binary_model=binary_model, binary_freeze_manifest=binary_freeze_manifest, category_model=category_model, category_freeze_manifest=category_freeze_manifest, stage3_config=stage3_config, stage3_freeze_manifest=stage3_freeze_manifest)
    rows = binary_eligible_rows(validation["rows"], allowed_partitions={"confirmation"})
    one_shot_guard(output_dir, validation["hashes"], enforce=enforce_one_shot, allow_repeat=allow_repeat_for_reproducibility)
    binary_payload = joblib.load(binary_model)
    category_payload = joblib.load(category_model)
    cfg = load_config(stage3_config)
    output_rows: list[dict[str, Any]] = []
    status_counts: dict[str, int] = {}
    positive_calls = 0
    for row in rows:
        serialize_model_row(row)
        binary_score = positive_probability(binary_payload["model"], row)
        threshold = float(binary_payload["threshold"])
        binary_pred = binary_score >= threshold
        result_row = {
            "case_id": row.get("case_id"),
            "repository": row.get("repository"),
            "language": row.get("language"),
            "code_changed_files": row.get("code_changed_files"),
            "code_diff_excerpt": row.get("code_diff_excerpt"),
            "docs_before_excerpt": row.get("docs_before_excerpt"),
            "frozen_binary_prediction": binary_pred,
            "binary_probability": binary_score,
            "binary_threshold": threshold,
        }
        if binary_pred:
            positive_calls += 1
            category, category_probs = category_prediction(category_payload["model"], row)
            safe_context = generation_view({**row, "pred_doc_category": category})
            stage3 = generate_semantic_documentation_patch(
                docs_update_required=True,
                predicted_category=category,
                code_diff=str(safe_context.get("code_diff_excerpt") or ""),
                docs_before=str(safe_context.get("docs_before_excerpt") or ""),
                documentation_context_candidates=list(row.get("documentation_context_candidates") or row.get("generator_context", {}).get("documentation_context_candidates") or []),
                llm_backend=llm_backend,
                config=cfg,
            )
            result_row.update({"frozen_category_prediction": category, "category_probabilities": category_probs, "stage3_result": stage3, "generated_patch": stage3.get("final_patch"), "selected_retrieved_document": stage3.get("selected_document"), "safety_provenance_result": stage3.get("first_pass_verifier")})
            status_counts[str(stage3.get("final_status"))] = status_counts.get(str(stage3.get("final_status")), 0) + 1
        else:
            status_counts["binary_negative_stage3_not_called"] = status_counts.get("binary_negative_stage3_not_called", 0) + 1
        if REFERENCE_FIELDS & set(result_row):
            raise RuntimeError("Reference fields leaked into generation results")
        output_rows.append(result_row)
    output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(output_dir / "stage3_confirmation_generation_results.jsonl", output_rows)
    receipt = {**validation["hashes"], "source_hashes": validation["stage3_freeze"].get("source_file_sha256"), "run_timestamp": utc_now(), "processed_row_count": len(rows), "positive_stage3_invocation_count": positive_calls, "final_status_counts": status_counts, "repeat_for_reproducibility": bool(allow_repeat_for_reproducibility)}
    write_json(output_dir / "stage3_confirmation_generation_receipt.json", receipt)
    return {"status": "ok", "receipt": receipt}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run frozen Stage 3 V2 confirmation generation. Do not use before final freeze.")
    parser.add_argument("--confirmation", required=True)
    parser.add_argument("--repository-partition-manifest", required=True)
    parser.add_argument("--binary-model", required=True)
    parser.add_argument("--binary-freeze-manifest", required=True)
    parser.add_argument("--category-model", required=True)
    parser.add_argument("--category-freeze-manifest", required=True)
    parser.add_argument("--stage3-config", required=True)
    parser.add_argument("--stage3-freeze-manifest", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--enforce-one-shot", action="store_true")
    parser.add_argument("--allow-repeat-for-reproducibility", action="store_true")
    args = parser.parse_args()
    raise SystemExit("This runner requires an explicit real LLM backend wiring by the caller; it is infrastructure-only from CLI in this hardening pass.")


if __name__ == "__main__":
    main()
