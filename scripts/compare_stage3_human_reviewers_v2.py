from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from docguard_eval_v2.reference_evaluation import read_jsonl, reviewer_agreement, write_json


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare two Stage 3 V2 human reviewer files.")
    parser.add_argument("--reviewer-a", required=True)
    parser.add_argument("--reviewer-b", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    result = reviewer_agreement(read_jsonl(Path(args.reviewer_a)), read_jsonl(Path(args.reviewer_b)))
    output_dir = Path(args.output_dir)
    write_json(output_dir / "reviewer_agreement.json", result)
    (output_dir / "reviewer_agreement_report.md").write_text(f"# Stage 3 V2 Reviewer Agreement\n\n- Overlap size: `{result['overlap_size']}`\n- Reliability claim allowed: `{result['reliability_claim_allowed']}`\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

