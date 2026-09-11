from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from docguard_eval_v2.reference_evaluation import (
    evaluation_reference_view,
    patch_text,
    read_jsonl,
    write_json,
    write_jsonl,
)


def run(*, primary_sample: Path, confirmation: Path, output_dir: Path) -> dict:
    primary_rows = read_jsonl(primary_sample)
    primary_ids = [str(row["case_id"]) for row in primary_rows]
    primary_id_set = set(primary_ids)
    references = {
        str(row["case_id"]): evaluation_reference_view(row)
        for row in read_jsonl(confirmation)
        if str(row.get("case_id") or "") in primary_id_set
    }
    if set(references) != primary_id_set:
        missing = sorted(primary_id_set - set(references))
        raise ValueError(f"Confirmation reference rows missing for primary cases: {missing}")

    output_rows = [row for row in primary_rows if patch_text(row).strip()]
    reference_input = [
        {**row, **references[str(row["case_id"])]}
        for row in output_rows
    ]

    status_counts = Counter(str(row.get("final_status") or "") for row in primary_rows)
    execution_errors: Counter[str] = Counter()
    safety_violations: Counter[str] = Counter()
    for row in primary_rows:
        stage3 = row.get("stage3_result") or {}
        error = stage3.get("execution_error") or {}
        if error:
            execution_errors[str(error.get("code") or "unknown")] += 1
        for verifier_key in ("first_pass_verifier", "repair_verifier"):
            for violation in (stage3.get(verifier_key) or {}).get("violations") or []:
                safety_violations[str(violation.get("code") or "unknown")] += 1

    safety = {
        "schema_version": "gate6_primary_safety_diagnostics_v1",
        "sample_scope": "primary_natural_distribution",
        "diagnostic_only": True,
        "sample_rows": len(primary_rows),
        "generated_output_rows": len(output_rows),
        "stage3_invocation_count": sum(bool(row.get("stage3_invoked")) for row in primary_rows),
        "retrieval_context_available_count": sum(bool(row.get("retrieval_context_available")) for row in primary_rows),
        "final_status_counts": dict(sorted(status_counts.items())),
        "execution_error_counts": dict(sorted(execution_errors.items())),
        "safety_violation_counts": dict(sorted(safety_violations.items())),
        "interpretation": (
            "Frozen verifier and execution diagnostics for the 100-row primary sample; "
            "pipeline safety acceptance is not human accept-as-is and is not a human quality score."
        ),
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    reference_path = output_dir / "primary_output_rows_with_post_hoc_references.jsonl"
    safety_path = output_dir / "primary_safety_diagnostics.json"
    write_jsonl(reference_path, reference_input)
    write_json(safety_path, safety)
    result = {
        "primary_rows": len(primary_rows),
        "reference_evaluation_rows": len(reference_input),
        "reference_scope": "conditional_on_generated_output",
        "safety_path": safety_path.as_posix(),
        "reference_input_path": reference_path.as_posix(),
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare frozen Gate 6 reference and safety inputs.")
    parser.add_argument("--primary-sample", required=True)
    parser.add_argument("--confirmation", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    print(json.dumps(run(
        primary_sample=Path(args.primary_sample),
        confirmation=Path(args.confirmation),
        output_dir=Path(args.output_dir),
    ), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
