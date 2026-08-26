from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.human_review_workflow_v2 import progress, read_review_file, write_json


def main() -> int:
    parser = argparse.ArgumentParser(description="Report Final V2 human review progress.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    rows = read_review_file(Path(args.input))
    result = progress(rows)
    output_dir = Path(args.output_dir)
    write_json(output_dir / "human_review_progress.json", result)
    (output_dir / "human_review_progress.md").write_text(f"# Human Review Progress\n\n- Total: `{result['total']}`\n- Approved: `{result['approved']}`\n- Excluded: `{result['excluded']}`\n- Pending: `{result['pending']}`\n- Complete: `{result['percentage_complete']:.2%}`\n\nThis is review progress only, not model evaluation.\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

