from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from docguard_llm_v2.context_adapter import FORBIDDEN_GENERATION_KEYS
from docguard_llm_v2.gate4_study import (
    BINARY_MODEL_SHA256,
    CATEGORY_MODEL_SHA256,
    GATE3_CLOSURE_COMMIT,
    PRIMARY_SAMPLE_SIZE,
    STAGE3_CONFIG_SHA256,
    primary_sample,
    sha256_file,
)
from docguard_ml_v2.data_contract import PRIMARY_STAGE2_LABELS, load_jsonl
from scripts.verify_gate3_classifier_freeze import verify as verify_gate3


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def verify(root: Path = ROOT) -> dict:
    gate3 = verify_gate3(root)
    if gate3["status"] != "PASS" or gate3["confirmation_accessed"] is not False:
        raise RuntimeError("Gate 3 upstream verification failed")
    output = root / "reports/final_v2/gate4"
    prediction_manifest = load_json(output / "development_prediction_manifest.json")
    predictions = load_jsonl(output / "development_validation_predictions.jsonl")
    primary = load_jsonl(output / "primary_sample.jsonl")
    secondary = load_jsonl(output / "secondary_stress_sample.jsonl")
    samples = load_json(output / "sample_manifest.json")
    coverage = load_json(output / "context_coverage_audit.json")
    external = load_json(output / "external_run_input_manifest.json")
    run_manifest = load_json(output / "external_run_manifest.json")

    if prediction_manifest.get("gate3_closure_commit") != GATE3_CLOSURE_COMMIT:
        raise RuntimeError("Gate 3 closure identity mismatch")
    if prediction_manifest.get("binary_model_sha256") != BINARY_MODEL_SHA256 or prediction_manifest.get("category_model_sha256") != CATEGORY_MODEL_SHA256:
        raise RuntimeError("Frozen model identity mismatch")
    if prediction_manifest.get("output_sha256") != sha256_file(output / "development_validation_predictions.jsonl"):
        raise RuntimeError("Development prediction artifact hash mismatch")
    if len(predictions) != prediction_manifest.get("row_count") or len(predictions) != 3148:
        raise RuntimeError("Development-validation prediction universe mismatch")
    if any(row.get("partition") != "development_validation" for row in predictions):
        raise RuntimeError("Non-validation row in canonical prediction artifact")
    for row in predictions + primary + secondary:
        leaked = FORBIDDEN_GENERATION_KEYS & set(row)
        if leaked:
            raise RuntimeError(f"Forbidden fields in Gate 4 safe artifact: {sorted(leaked)}")
    expected_primary = primary_sample(predictions, target_size=PRIMARY_SAMPLE_SIZE, seed=42)
    if primary != expected_primary or samples["primary"]["sha256"] != sha256_file(output / "primary_sample.jsonl"):
        raise RuntimeError("Primary sample is not reproducible")
    if samples.get("gold_or_human_labels_used_for_selection") is not False or samples.get("context_filtered_before_sampling") is not False:
        raise RuntimeError("Primary sampling safety contract mismatch")
    if len(primary) != min(PRIMARY_SAMPLE_SIZE, prediction_manifest["predicted_positive_count"]):
        raise RuntimeError("Primary sample size mismatch")
    secondary_counts = Counter(str(row.get("frozen_category_prediction")) for row in secondary)
    if secondary_counts != Counter({label: 25 for label in PRIMARY_STAGE2_LABELS}) or len(secondary) != 100:
        raise RuntimeError("Secondary stress sample count mismatch")
    if any(row.get("partition") not in {"development_train", "development_validation"} for row in secondary):
        raise RuntimeError("Non-development row in stress sample")
    for name, rows in (("primary", primary), ("secondary", secondary)):
        available = sum(bool(row.get("retrieval_context_available")) for row in rows)
        audit = coverage[name]
        if audit["sampled_predicted_positives"] != len(rows) or audit["retrieval_context_available"] != available or audit["retrieval_context_unavailable"] != len(rows) - available or audit["planned_stage3_invocation_count"] != available:
            raise RuntimeError(f"{name} context coverage mismatch")
    if external.get("status") != "READY_FOR_EXTERNAL_COMPUTE" or external.get("confirmation_accessed") is not False or external.get("confirmation_paths_allowed") is not False:
        raise RuntimeError("Unsafe external input manifest")
    for relative, expected in external["source_sha256"].items():
        if sha256_file(root / relative) != expected:
            raise RuntimeError(f"External source hash mismatch: {relative}")
    for item in external["inputs"].values():
        if "confirmation" in str(item["path"]).casefold() or sha256_file(root / item["path"]) != item["sha256"]:
            raise RuntimeError("External input path/hash mismatch")
    if external["inputs"]["stage3_config"]["sha256"] != STAGE3_CONFIG_SHA256:
        raise RuntimeError("Stage 3 config identity mismatch")
    run_status = str(run_manifest.get("status") or "")
    prepared_run = (
        run_status == "PREPARED_EXTERNAL_COMPUTE_REQUIRED"
        and run_manifest.get("results_present") is False
        and run_manifest.get("stage3_freeze_manifest_present") is False
    )
    completed_run = (
        run_status == "COMPLETED_DEVELOPMENT_ONLY"
        and run_manifest.get("results_present") is True
        and run_manifest.get("stage3_freeze_manifest_present") is True
    )
    if (
        not (prepared_run or completed_run)
        or run_manifest.get("confirmation_accessed") is not False
        or run_manifest.get("input_manifest_sha256")
        != sha256_file(output / "external_run_input_manifest.json")
    ):
        raise RuntimeError("Gate 4 external-run state mismatch")
    state = load_json(root / "reports/final_v2/finalization_state.json")
    gate4_status = state["gate_statuses"]["gate_4_stage3_retrieval_generation_study_and_freeze"]
    current_gate = int(state["current_gate"])
    freeze_present = state["final_model_freeze_state"]["stage3_freeze_manifest_present"]

    in_progress = (
        gate4_status == "IN_PROGRESS_EXTERNAL_COMPUTE_REQUIRED"
        and current_gate == 4
        and freeze_present is False
        and prepared_run
    )

    frozen = (
        gate4_status == "PASS"
        and current_gate >= 5
        and freeze_present is True
        and completed_run
    )

    if (
        not (in_progress or frozen)
        or state.get("confirmation_results_accessed_by_gate_4") is not False
        or state["confirmation_sealed"] is not True
    ):
        raise RuntimeError("Gate 4 finalization state mismatch")
    return {
        "status": "PASS",
        "gate3_upstream": "PASS",
        "predicted_positive_pool": prediction_manifest["predicted_positive_count"],
        "primary": coverage["primary"],
        "secondary": {**coverage["secondary"], "category_counts": dict(sorted(secondary_counts.items()))},
        "confirmation_accessed": False,
        "gate4_status": gate4_status,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
