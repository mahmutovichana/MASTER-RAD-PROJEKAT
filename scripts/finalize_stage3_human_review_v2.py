from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from docguard_eval_v2.reference_evaluation import read_jsonl, summarize_human_reviews, validate_review, write_json, write_jsonl


def run(input_path: Path, output_dir: Path) -> dict:
    approved = []
    excluded = []
    for row in read_jsonl(input_path):
        ok, reason = validate_review(row)
        if ok:
            approved.append(row)
        else:
            excluded.append({**row, "exclusion_reason": reason})
    output_dir.mkdir(parents=True, exist_ok=True)
    summary = summarize_human_reviews(approved)
    summary["excluded_or_incomplete_reviews"] = len(excluded)
    write_jsonl(output_dir / "approved_reviews.jsonl", approved)
    write_jsonl(output_dir / "excluded_or_incomplete_reviews.jsonl", excluded)
    write_json(output_dir / "human_review_summary.json", summary)
    (output_dir / "human_review_report.md").write_text(f"# Stage 3 V2 Human Review\n\n- Approved reviews: `{len(approved)}`\n- Excluded/incomplete: `{len(excluded)}`\n- Accept-as-is rate: `{summary['accept_as_is_rate']:.4f}`\n", encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Finalize Stage 3 V2 blind human reviews.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    print(json.dumps(run(Path(args.input), Path(args.output_dir)), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

