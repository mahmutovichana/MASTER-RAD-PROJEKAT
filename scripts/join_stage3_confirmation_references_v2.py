from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from docguard_eval_v2.reference_evaluation import evaluation_reference_view, read_jsonl, write_jsonl


def run(generation_results: Path, reference_rows: Path, output: Path) -> list[dict]:
    refs = {str(row.get("case_id")): evaluation_reference_view(row) for row in read_jsonl(reference_rows)}
    joined = []
    for row in read_jsonl(generation_results):
        joined.append({**row, "post_hoc_reference": refs.get(str(row.get("case_id")), {})})
    write_jsonl(output, joined)
    return joined


def main() -> int:
    parser = argparse.ArgumentParser(description="Join Stage 3 generation results to reference-only fields after generation is complete.")
    parser.add_argument("--generation-results", required=True)
    parser.add_argument("--reference-rows", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    rows = run(Path(args.generation_results), Path(args.reference_rows), Path(args.output))
    print(json.dumps({"status": "ok", "rows": len(rows), "output": args.output}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
