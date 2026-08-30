from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.human_review_workflow_v2 import label_tuple, normalize_status, progress, read_review_file, validate_integrity, validate_taxonomy, write_json, write_jsonl


def run(paths: list[Path], output_dir: Path) -> dict:
    merged: dict[str, dict] = {}
    conflicts = []
    incomplete = []
    normalization_count = 0
    for path in paths:
        for row in read_review_file(path):
            status, normalized = normalize_status(row.get("review_status"))
            if normalized:
                row = {**row, "review_status": status}
                normalization_count += 1
            cid = str(row.get("case_id") or "")
            ok_hash, hash_reason = validate_integrity(row)
            ok_tax, tax_reason = validate_taxonomy(row)
            if not ok_hash:
                conflicts.append({**row, "conflict_reason": hash_reason, "source_file": str(path)})
                continue
            if not ok_tax:
                incomplete.append({**row, "incomplete_reason": tax_reason, "source_file": str(path)})
                continue
            if cid in merged:
                if label_tuple(merged[cid]) != label_tuple(row):
                    conflicts.append({"case_id": cid, "conflict_reason": "duplicate_case_id_conflicting_human_label", "existing": merged[cid], "incoming": row})
                continue
            merged[cid] = row
    rows = list(merged.values())
    output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(output_dir / "merged_human_review.jsonl", rows)
    write_jsonl(output_dir / "review_conflicts.jsonl", conflicts)
    write_jsonl(output_dir / "incomplete_reviews.jsonl", incomplete)
    report = progress(rows + incomplete)
    report.update({"merged_rows": len(rows), "conflicts": len(conflicts), "incomplete_reviews": len(incomplete), "legacy_exclude_normalized_to_excluded": normalization_count})
    write_json(output_dir / "review_progress.json", report)
    (output_dir / "review_merge_report.md").write_text(f"# Human Review Merge\n\n- Merged approved rows: `{len(rows)}`\n- Conflicts: `{len(conflicts)}`\n- Incomplete/invalid: `{len(incomplete)}`\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Merge reviewed Final V2 CSV/JSONL batches.")
    parser.add_argument("--input", action="append", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    result = run([Path(path) for path in args.input], Path(args.output_dir))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 1 if result["conflicts"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
