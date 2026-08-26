from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.human_review_workflow_v2 import label_tuple, read_review_file, validate_integrity, validate_taxonomy, write_json


def audit(rows: list[dict]) -> tuple[list[str], dict]:
    errors: list[str] = []
    seen: dict[str, tuple] = {}
    for index, row in enumerate(rows, start=1):
        cid = str(row.get("case_id") or f"row_{index}")
        ok_hash, hash_reason = validate_integrity(row)
        ok_tax, tax_reason = validate_taxonomy(row)
        if not ok_hash:
            errors.append(f"{cid}: {hash_reason}")
        if not ok_tax:
            errors.append(f"{cid}: {tax_reason}")
        if cid in seen:
            errors.append(f"{cid}: duplicate_case")
            if seen[cid] != label_tuple(row):
                errors.append(f"{cid}: unresolved_conflict")
        seen[cid] = label_tuple(row)
        for key in ["human_docs_update_required", "human_doc_category"]:
            if row.get(key) in {"", None}:
                errors.append(f"{cid}: missing_{key}")
    report = {"status": "fail" if errors else "ok", "row_count": len(rows), "errors": errors, "label_source_can_become_human_reviewed_final_v2": not errors}
    return errors, report


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit that Final V2 human review is complete before gold finalization.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    errors, report = audit(read_review_file(Path(args.input)))
    output_dir = Path(args.output_dir)
    write_json(output_dir / "human_review_completion_audit.json", report)
    (output_dir / "human_review_completion_audit.md").write_text(f"# Human Review Completion Audit\n\n- Status: `{report['status']}`\n- Rows: `{report['row_count']}`\n- Errors: `{len(errors)}`\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
