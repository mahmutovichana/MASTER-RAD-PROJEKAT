from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.human_review_workflow_v2 import read_review_file, reviewer_overlap_agreement, write_json, write_jsonl


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare two Final V2 human gold reviewer files.")
    parser.add_argument("--reviewer-a", required=True)
    parser.add_argument("--reviewer-b", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    result = reviewer_overlap_agreement(read_review_file(Path(args.reviewer_a)), read_review_file(Path(args.reviewer_b)))
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(output_dir / "reviewer_agreement.json", {key: value for key, value in result.items() if key != "conflicts"})
    write_jsonl(output_dir / "reviewer_conflicts.jsonl", result["conflicts"])
    (output_dir / "reviewer_agreement_report.md").write_text(f"# Final V2 Reviewer Agreement\n\n- Overlap: `{result['overlap_size']}`\n- Binary agreement: `{result['binary_agreement']:.4f}`\n- Conflicts: `{len(result['conflicts'])}`\n\nDisagreements require explicit adjudication.\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in result.items() if key != "conflicts"}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

