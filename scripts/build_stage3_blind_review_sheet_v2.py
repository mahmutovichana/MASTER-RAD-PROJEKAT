from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from docguard_eval_v2.reference_evaluation import build_blind_row, read_jsonl, write_jsonl


def main() -> int:
    parser = argparse.ArgumentParser(description="Build blind human review sheet for Stage 3 V2 generated patches.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    rows = [build_blind_row(row) for row in read_jsonl(Path(args.input))]
    write_jsonl(Path(args.output), rows)
    print(json.dumps({"status": "ok", "rows": len(rows), "output": args.output}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

