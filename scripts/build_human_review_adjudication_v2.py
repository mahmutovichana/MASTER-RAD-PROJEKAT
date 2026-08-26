from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.human_review_workflow_v2 import EVIDENCE_FIELDS, load_jsonl, write_jsonl


def build_row(conflict: dict) -> dict:
    a = conflict.get("reviewer_a") or conflict.get("existing") or {}
    b = conflict.get("reviewer_b") or conflict.get("incoming") or {}
    out = {field: a.get(field) for field in EVIDENCE_FIELDS}
    out.update(
        {
            "reviewer_a_docs_update_required": a.get("human_docs_update_required"),
            "reviewer_a_doc_category": a.get("human_doc_category"),
            "reviewer_a_notes": a.get("human_label_notes"),
            "reviewer_b_docs_update_required": b.get("human_docs_update_required"),
            "reviewer_b_doc_category": b.get("human_doc_category"),
            "reviewer_b_notes": b.get("human_label_notes"),
            "adjudicated_docs_update_required": "",
            "adjudicated_doc_category": "",
            "adjudication_notes": "",
            "adjudication_status": "pending",
        }
    )
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Build human-only adjudication sheet for reviewer disagreements.")
    parser.add_argument("--conflicts", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    rows = [build_row(row) for row in load_jsonl(Path(args.conflicts))]
    output_dir = Path(args.output_dir)
    write_jsonl(output_dir / "adjudication_sheet.jsonl", rows)
    output_dir.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else [
        *EVIDENCE_FIELDS,
        "reviewer_a_docs_update_required",
        "reviewer_a_doc_category",
        "reviewer_a_notes",
        "reviewer_b_docs_update_required",
        "reviewer_b_doc_category",
        "reviewer_b_notes",
        "adjudicated_docs_update_required",
        "adjudicated_doc_category",
        "adjudication_notes",
        "adjudication_status",
    ]
    with (output_dir / "adjudication_sheet.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps({"status": "ok", "rows": len(rows), "human_only": True}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
