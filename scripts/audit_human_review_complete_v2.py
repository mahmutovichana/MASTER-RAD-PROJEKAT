from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from docguard_ml_v2.model_manifest import sha256_file, utc_now
from scripts.human_review_workflow_v2 import label_tuple, parse_bool, read_review_file, validate_integrity, validate_taxonomy, write_json


def audit(rows: list[dict], *, input_path: Path | None = None, conflict_count: int = 0) -> tuple[list[str], dict]:
    errors: list[str] = []
    seen: dict[str, tuple] = {}
    approved = excluded = pending = 0
    taxonomy_ok = True
    integrity_ok = True
    for index, row in enumerate(rows, start=1):
        cid = str(row.get("case_id") or f"row_{index}")
        status = str(row.get("review_status") or "").strip().lower()
        if status == "approved":
            approved += 1
        elif status == "excluded":
            excluded += 1
        else:
            pending += 1
        ok_hash, hash_reason = validate_integrity(row)
        ok_tax, tax_reason = validate_taxonomy(row)
        if not ok_hash:
            integrity_ok = False
            errors.append(f"{cid}: {hash_reason}")
        if not ok_tax:
            taxonomy_ok = False
            errors.append(f"{cid}: {tax_reason}")
        if cid in seen:
            errors.append(f"{cid}: duplicate_case")
            if seen[cid] != label_tuple(row):
                errors.append(f"{cid}: unresolved_conflict")
        seen[cid] = label_tuple(row)
        for key in ["human_docs_update_required", "human_doc_category"]:
            if row.get(key) in {"", None}:
                errors.append(f"{cid}: missing_{key}")
    if conflict_count:
        errors.append(f"unresolved_conflicts: {conflict_count}")
    report = {
        "status": "failed" if errors else "passed",
        "input_sha256": None if input_path is None else sha256_file(input_path),
        "audit_timestamp": utc_now(),
        "row_count": len(rows),
        "approved_count": approved,
        "excluded_count": excluded,
        "pending_count": pending,
        "conflict_count": conflict_count,
        "taxonomy_validation_status": "passed" if taxonomy_ok else "failed",
        "review_integrity_status": "passed" if integrity_ok else "failed",
        "errors": errors,
        "label_source_can_become_human_reviewed_final_v2": not errors,
    }
    return errors, report


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit that Final V2 human review is complete before gold finalization.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--conflicts")
    args = parser.parse_args()
    conflict_count = 0
    if args.conflicts and Path(args.conflicts).exists():
        conflict_count = len([line for line in Path(args.conflicts).read_text(encoding="utf-8").splitlines() if line.strip()])
    errors, report = audit(read_review_file(Path(args.input)), input_path=Path(args.input), conflict_count=conflict_count)
    output_dir = Path(args.output_dir)
    write_json(output_dir / "human_review_completion_audit.json", report)
    (output_dir / "human_review_completion_audit.md").write_text(f"# Human Review Completion Audit\n\n- Status: `{report['status']}`\n- Rows: `{report['row_count']}`\n- Errors: `{len(errors)}`\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
