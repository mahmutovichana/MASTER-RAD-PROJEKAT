from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from docguard_eval_v2.reference_evaluation import write_json
from docguard_ml_v2.data_contract import LABEL_SOURCE, PRIMARY_STAGE2_LABELS, SAFE_MODEL_FIELDS


def read(path: str) -> str:
    return (PROJECT_ROOT / path).read_text(encoding="utf-8")


def trainer_help(script: str) -> str:
    result = subprocess.run([sys.executable, script, "--help"], cwd=PROJECT_ROOT, text=True, capture_output=True)
    return result.stdout


def run(extra_source_checks: dict[str, str] | None = None) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def check(name: str, passed: bool, detail: str = "") -> None:
        checks.append({"name": name, "status": "PASS" if passed else "FAIL", "detail": detail})

    builder = read("docguard_external/github_pr_dataset_builder_v2.py")
    ml_contract = read("docguard_ml_v2/data_contract.py")
    stage3 = "\n".join(path.read_text(encoding="utf-8") for path in (PROJECT_ROOT / "docguard_llm_v2").glob("*.py"))
    prefill = read("scripts/prefill_human_label_sheet_v2.py")
    finalizer = read("scripts/finalize_human_gold_v2.py")
    binary_help = trainer_help("scripts/train_binary_classifier_v4.py")
    category_help = trainer_help("scripts/train_category_classifier_v8.py")
    config = json.loads((PROJECT_ROOT / "configs/stage3_semantic_generation_v2.json").read_text(encoding="utf-8"))

    check("candidate_builder_no_gold_emit", "FORBIDDEN_GOLD_FIELDS" in builder and "gold_docs_update_required" in builder)
    check("safe_model_fields_exact", SAFE_MODEL_FIELDS == ["language", "code_changed_files", "code_diff_excerpt", "docs_before_excerpt"])
    check("ml_contract_requires_human_reviewed_final", LABEL_SOURCE in ml_contract and "human_review_complete must be exactly true" in ml_contract)
    check("no_class_balancing_config", '"class_balancing": false' in read("configs/binary_classifier_v4.json").lower() and '"class_balancing": false' in read("configs/category_classifier_v8.json").lower())
    check("category_v8_exact_labels", PRIMARY_STAGE2_LABELS == ["api_reference", "configuration", "developer_setup", "model_contract"])
    check("trainer_cli_no_confirmation", "--confirmation" not in binary_help and "--confirmation" not in category_help and "--test" not in binary_help and "--test" not in category_help)
    check("stage3_no_router_or_grounded_fallback", "router" not in stage3.lower() and "grounded_patch" not in stage3.lower())
    check("stage3_runtime_generation_settings", "generation_options" in stage3 and config.get("max_repair_attempts") <= 1)
    check("human_prefill_safe_only", "docs_diff_excerpt" not in prefill and "docs_after_excerpt" not in prefill and "collector_bucket" not in prefill)
    check("finalizer_requires_completion_audit", "--completion-audit is required" in finalizer)
    check("confirmation_evaluators_require_freeze", "--freeze-manifest" in read("scripts/evaluate_binary_v4_confirmation.py") and "--freeze-manifest" in read("scripts/evaluate_category_v8_confirmation.py"))
    check("stage3_confirmation_runner_exists", (PROJECT_ROOT / "scripts/run_frozen_stage3_v2_confirmation.py").exists())
    check("one_shot_guards_exist", "enforce_one_shot" in read("scripts/run_frozen_stage3_v2_confirmation.py") and "enforce_one_shot" in read("scripts/aggregate_stage3_final_evaluation_v2.py"))
    check("historical_v1_not_dependency", "llm_patch_eval_v1" not in builder + ml_contract + stage3)
    check("operational_pending_downstream_guard_exists", "validate_final_v2_completion_state" in builder and "operational_pending" in builder)
    for name, source in (extra_source_checks or {}).items():
        check(f"extra_source_{name}_no_router", "router" not in source.lower())
        check(f"extra_source_{name}_safe_prefill", "docs_after_excerpt" not in source and "docs_diff_excerpt" not in source)
    status = "PASS" if all(item["status"] == "PASS" for item in checks) else "FAIL"
    return {"status": status, "checks": checks}


def main() -> int:
    parser = argparse.ArgumentParser(description="Static Final V2 pre-experiment audit.")
    parser.add_argument("--output-dir", default="reports/final_v2")
    args = parser.parse_args()
    report = run()
    output_dir = Path(args.output_dir)
    write_json(output_dir / "pre_experiment_audit.json", report)
    lines = ["# Final V2 Pre-Experiment Audit", "", f"- Status: `{report['status']}`", ""]
    for item in report["checks"]:
        lines.append(f"- `{item['status']}` {item['name']}: {item.get('detail', '')}")
    (output_dir / "pre_experiment_audit.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
