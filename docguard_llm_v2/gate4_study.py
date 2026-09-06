from __future__ import annotations

import hashlib
import json
import random
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

import joblib

from docguard_llm_v2.context_adapter import FORBIDDEN_GENERATION_KEYS, assert_generation_payload_safe, normalize_documentation_context
from docguard_ml_v2.data_contract import PRIMARY_STAGE2_LABELS, SAFE_MODEL_FIELDS, load_jsonl, serialize_model_row, write_jsonl


GATE3_CLOSURE_COMMIT = "e4b4bed2ca5ddcbc34ad98d5f78fbf88769fa012"
BINARY_MODEL_SHA256 = "7d6a9263e1262c5c54db3d2e100209707c6a7681133fb1505f44125efa954462"
CATEGORY_MODEL_SHA256 = "2d8123ac398568b5c9586b0f8d26d6c4079ddfebd504889b934f77bef65b9f59"
STAGE3_CONFIG_SHA256 = "8e5723a55b8e7ee693bb5a597f0bce87b7ec52cba639d75af77fa7b2e3b25250"
PRIMARY_SAMPLE_SIZE = 100
STRESS_PER_CATEGORY = 25
SEED = 42


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_canonical_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def git_head(root: Path) -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()


def _positive_probability(model: Any, row: dict[str, Any]) -> float:
    probabilities = model.predict_proba([row])[0]
    classes = list(model.named_steps["classifier"].classes_)
    return float(probabilities[classes.index(1)])


def _category_prediction(model: Any, row: dict[str, Any]) -> tuple[str, dict[str, float]]:
    probabilities = model.predict_proba([row])[0]
    classes = [str(item) for item in model.named_steps["classifier"].classes_]
    return str(classes[max(range(len(classes)), key=lambda index: probabilities[index])]), {
        label: float(probabilities[index]) for index, label in enumerate(classes)
    }


def _safe_prediction_row(row: dict[str, Any], *, binary_prediction: bool, binary_probability: float, threshold: float, category_prediction: str | None, category_probabilities: dict[str, float] | None, include_context: bool = True) -> dict[str, Any]:
    candidates = normalize_documentation_context(row) if include_context else []
    result = {
        "case_id": str(row.get("case_id") or ""),
        "repository": str(row.get("repository") or ""),
        "pr_number": row.get("pr_number"),
        "partition": str(row.get("partition") or ""),
        **{field: row.get(field) for field in SAFE_MODEL_FIELDS},
        "documentation_context_candidates": candidates,
        "retrieval_context_available": bool(candidates) if include_context else None,
        "frozen_binary_prediction": bool(binary_prediction),
        "binary_probability": float(binary_probability),
        "binary_threshold": float(threshold),
        "frozen_category_prediction": category_prediction,
        "category_probabilities": category_probabilities,
    }
    if FORBIDDEN_GENERATION_KEYS & set(result):
        raise RuntimeError("Forbidden outcome fields entered development prediction artifact")
    return result


def score_development_rows(rows: list[dict[str, Any]], binary_payload: dict[str, Any], category_payload: dict[str, Any], *, allowed_partitions: set[str], include_context: bool = True) -> list[dict[str, Any]]:
    if not rows or any(row.get("partition") not in allowed_partitions for row in rows):
        raise ValueError("Gate 4 scoring accepts declared development partitions only")
    if "confirmation" in allowed_partitions:
        raise ValueError("Confirmation is forbidden in Gate 4")
    binary_model = binary_payload["model"]
    category_model = category_payload["model"]
    threshold = float(binary_payload["threshold"])
    if threshold != 0.15:
        raise ValueError("Frozen Binary threshold mismatch")
    for row in rows:
        serialize_model_row(row)
    binary_classes = list(binary_model.named_steps["classifier"].classes_)
    binary_probabilities = binary_model.predict_proba(rows)[:, binary_classes.index(1)]
    positive_indexes = [index for index, probability in enumerate(binary_probabilities) if float(probability) >= threshold]
    positive_rows = [rows[index] for index in positive_indexes]
    category_by_index: dict[int, tuple[str, dict[str, float]]] = {}
    if positive_rows:
        category_matrix = category_model.predict_proba(positive_rows)
        category_classes = [str(item) for item in category_model.named_steps["classifier"].classes_]
        for row_index, probabilities in zip(positive_indexes, category_matrix):
            label = category_classes[max(range(len(category_classes)), key=lambda index: probabilities[index])]
            category_by_index[row_index] = (label, {label_name: float(probabilities[index]) for index, label_name in enumerate(category_classes)})
    output: list[dict[str, Any]] = []
    for index, (row, raw_probability) in enumerate(zip(rows, binary_probabilities)):
        probability = float(raw_probability)
        predicted_positive = index in category_by_index
        category, category_probabilities = category_by_index.get(index, (None, None))
        output.append(
            _safe_prediction_row(
                row,
                binary_prediction=predicted_positive,
                binary_probability=probability,
                threshold=threshold,
                category_prediction=category,
                category_probabilities=category_probabilities,
                include_context=include_context,
            )
        )
    return output


def attach_context(rows: list[dict[str, Any]], source_by_case_id: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    for row in rows:
        source = source_by_case_id.get(str(row["case_id"]))
        if source is None:
            raise ValueError(f"Missing source row for {row['case_id']}")
        candidates = normalize_documentation_context(source)
        output.append({**row, "documentation_context_candidates": candidates, "retrieval_context_available": bool(candidates)})
    return output


def primary_sample(predictions: list[dict[str, Any]], *, target_size: int = PRIMARY_SAMPLE_SIZE, seed: int = SEED) -> list[dict[str, Any]]:
    pool = sorted((row for row in predictions if row["frozen_binary_prediction"] is True), key=lambda row: row["case_id"])
    selected = random.Random(seed).sample(pool, min(target_size, len(pool)))
    return [{**row, "sample_name": "primary_natural_distribution", "sample_seed": seed} for row in selected]


def secondary_stress_sample(predictions: list[dict[str, Any]], *, per_category: int = STRESS_PER_CATEGORY, seed: int = SEED, excluded_case_ids: set[str] | None = None) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    rng = random.Random(seed)
    excluded = excluded_case_ids or set()
    for category in PRIMARY_STAGE2_LABELS:
        pool = sorted(
            (row for row in predictions if row["frozen_binary_prediction"] is True and row["frozen_category_prediction"] == category and row["case_id"] not in excluded),
            key=lambda row: row["case_id"],
        )
        if len(pool) < per_category:
            raise ValueError(f"Insufficient predicted-positive rows for {category}: {len(pool)} < {per_category}")
        selected.extend({**row, "sample_name": "secondary_category_stress", "sample_seed": seed} for row in rng.sample(pool, per_category))
    return selected


def sample_coverage(rows: list[dict[str, Any]]) -> dict[str, Any]:
    available = sum(bool(row["retrieval_context_available"]) for row in rows)
    return {
        "sampled_predicted_positives": len(rows),
        "retrieval_context_available": available,
        "retrieval_context_unavailable": len(rows) - available,
        "planned_stage3_invocation_count": available,
        "planned_invocation_rate": (available / len(rows)) if rows else 0.0,
    }


def verify_upstream(root: Path) -> dict[str, str]:
    paths = {
        "validation_input": root / "experiments/consolidated_enriched_training_v2/gold/validation.jsonl",
        "binary_model": root / "models/final_v2/gate3/binary_m1_gate3.joblib",
        "binary_freeze_manifest": root / "reports/final_v2/gate3/binary_classifier_freeze_manifest.json",
        "category_model": root / "models/final_v2/gate3/category_m1_gate3.joblib",
        "category_freeze_manifest": root / "reports/final_v2/gate3/category_classifier_freeze_manifest.json",
        "stage3_config": root / "configs/stage3_semantic_generation_v2.json",
    }
    hashes = {name: sha256_file(path) for name, path in paths.items()}
    if git_head(root) != GATE3_CLOSURE_COMMIT:
        raise ValueError("Gate 4 preparation must start at the canonical Gate 3 closure commit")
    if hashes["binary_model"] != BINARY_MODEL_SHA256 or hashes["category_model"] != CATEGORY_MODEL_SHA256:
        raise ValueError("Frozen Gate 3 model identity mismatch")
    if hashes["stage3_config"] != STAGE3_CONFIG_SHA256:
        raise ValueError("Frozen Stage 3 configuration identity mismatch")
    return hashes


def preparation_paths(root: Path) -> dict[str, Path]:
    output = root / "reports/final_v2/gate4"
    return {
        "output": output,
        "predictions": output / "development_validation_predictions.jsonl",
        "prediction_manifest": output / "development_prediction_manifest.json",
        "primary": output / "primary_sample.jsonl",
        "secondary": output / "secondary_stress_sample.jsonl",
        "sample_manifest": output / "sample_manifest.json",
        "coverage": output / "context_coverage_audit.json",
        "external_input": output / "external_run_input_manifest.json",
        "external_run": output / "external_run_manifest.json",
    }


def prepare_gate4(root: Path, *, source_paths: list[str]) -> dict[str, Any]:
    upstream = verify_upstream(root)
    paths = preparation_paths(root)
    validation_path = root / "experiments/consolidated_enriched_training_v2/gold/validation.jsonl"
    train_path = root / "experiments/consolidated_enriched_training_v2/gold/train.jsonl"
    rows = load_jsonl(validation_path)
    binary_payload = joblib.load(root / "models/final_v2/gate3/binary_m1_gate3.joblib")
    category_payload = joblib.load(root / "models/final_v2/gate3/category_m1_gate3.joblib")
    predictions = score_development_rows(rows, binary_payload, category_payload, allowed_partitions={"development_validation"}, include_context=True)
    primary = primary_sample(predictions)
    train_rows = load_jsonl(train_path)
    train_predictions = score_development_rows(train_rows, binary_payload, category_payload, allowed_partitions={"development_train"}, include_context=False)
    secondary = secondary_stress_sample(predictions + train_predictions)
    source_by_case_id = {str(row["case_id"]): row for row in rows + train_rows}
    secondary = attach_context(secondary, source_by_case_id)
    write_jsonl(paths["predictions"], predictions)
    write_jsonl(paths["primary"], primary)
    write_jsonl(paths["secondary"], secondary)
    prediction_manifest = {
        "schema_version": "gate4_development_predictions_v1",
        "status": "PREPARED",
        "partition": "development_validation",
        "row_count": len(predictions),
        "predicted_positive_count": sum(row["frozen_binary_prediction"] for row in predictions),
        "predicted_category_counts": dict(sorted(Counter(row["frozen_category_prediction"] for row in predictions if row["frozen_binary_prediction"]).items())),
        "binary_threshold": 0.15,
        "input_sha256": upstream["validation_input"],
        "output_sha256": sha256_file(paths["predictions"]),
        "gate3_closure_commit": GATE3_CLOSURE_COMMIT,
        "binary_model_sha256": upstream["binary_model"],
        "binary_freeze_manifest_sha256": upstream["binary_freeze_manifest"],
        "category_model_sha256": upstream["category_model"],
        "category_freeze_manifest_sha256": upstream["category_freeze_manifest"],
        "confirmation_accessed": False,
    }
    write_canonical_json(paths["prediction_manifest"], prediction_manifest)
    coverage = {
        "schema_version": "gate4_context_coverage_v1",
        "selection_order": "sample predicted positives before testing retrieval-context availability",
        "primary": sample_coverage(primary),
        "secondary": sample_coverage(secondary),
        "all_validation": {
            "rows": len(predictions),
            "retrieval_context_available": sum(row["retrieval_context_available"] for row in predictions),
            "retrieval_context_unavailable": sum(not row["retrieval_context_available"] for row in predictions),
        },
        "context_unavailable_disposition": "retrieval_context_unavailable; zero LLM calls; no generated patch; excluded from Qwen/verifier failure counts",
        "confirmation_accessed": False,
    }
    write_canonical_json(paths["coverage"], coverage)
    sample_manifest = {
        "schema_version": "gate4_development_samples_v1",
        "primary": {"method": "natural_distribution_random_predicted_positive", "target_size": 100, "seed": 42, "row_count": len(primary), "sha256": sha256_file(paths["primary"]), **sample_coverage(primary)},
        "secondary": {"method": "predicted_category_stress_from_development_train_and_validation", "eligible_partitions": ["development_train", "development_validation"], "per_category": 25, "seed": 42, "row_count": len(secondary), "sha256": sha256_file(paths["secondary"]), "category_counts": dict(sorted(Counter(row["frozen_category_prediction"] for row in secondary).items())), **sample_coverage(secondary)},
        "sampling_fields": ["frozen_binary_prediction", "frozen_category_prediction", "case_id"],
        "gold_or_human_labels_used_for_selection": False,
        "context_filtered_before_sampling": False,
        "confirmation_accessed": False,
    }
    write_canonical_json(paths["sample_manifest"], sample_manifest)
    source_hashes = {relative: sha256_file(root / relative) for relative in source_paths}
    input_manifest = {
        "schema_version": "gate4_external_input_v1",
        "status": "READY_FOR_EXTERNAL_COMPUTE",
        "gate3_closure_commit": GATE3_CLOSURE_COMMIT,
        "upstream_hashes": upstream,
        "source_sha256": source_hashes,
        "inputs": {
            "primary_sample": {"path": str(paths["primary"].relative_to(root)).replace("\\", "/"), "sha256": sha256_file(paths["primary"])},
            "secondary_stress_sample": {"path": str(paths["secondary"].relative_to(root)).replace("\\", "/"), "sha256": sha256_file(paths["secondary"])},
            "sample_manifest": {"path": str(paths["sample_manifest"].relative_to(root)).replace("\\", "/"), "sha256": sha256_file(paths["sample_manifest"])},
            "stage3_config": {"path": "configs/stage3_semantic_generation_v2.json", "sha256": upstream["stage3_config"]},
        },
        "confirmation_paths_allowed": False,
        "confirmation_accessed": False,
    }
    write_canonical_json(paths["external_input"], input_manifest)
    write_canonical_json(paths["external_run"], {
        "schema_version": "gate4_external_run_v1",
        "status": "PREPARED_EXTERNAL_COMPUTE_REQUIRED",
        "model": "Qwen/Qwen2.5-Coder-7B-Instruct",
        "precision": "float16",
        "quantized": False,
        "input_manifest_sha256": sha256_file(paths["external_input"]),
        "results_present": False,
        "stage3_freeze_manifest_present": False,
        "confirmation_accessed": False,
    })
    return {"prediction_manifest": prediction_manifest, "sample_manifest": sample_manifest, "coverage": coverage}


def generation_payload(row: dict[str, Any]) -> dict[str, Any]:
    if row.get("partition") not in {"development_train", "development_validation"}:
        raise ValueError("External Gate 4 runner accepts development partitions only")
    payload = {
        "case_id": row["case_id"],
        "code_diff_excerpt": str(row.get("code_diff_excerpt") or ""),
        "docs_before_excerpt": str(row.get("docs_before_excerpt") or ""),
        "predicted_category": str(row.get("frozen_category_prediction") or ""),
        "documentation_context_candidates": normalize_documentation_context(row),
    }
    assert_generation_payload_safe(payload)
    return payload
