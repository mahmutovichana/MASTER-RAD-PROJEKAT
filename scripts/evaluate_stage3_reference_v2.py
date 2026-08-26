from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from docguard_eval_v2.reference_evaluation import read_jsonl, summarize_reference, write_json


def main() -> int:
    parser = argparse.ArgumentParser(description="Run diagnostic post-hoc reference evaluation for Stage 3 V2 patches.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    summary = summarize_reference(read_jsonl(Path(args.input)))
    write_json(output_dir / "reference_metrics.json", summary)
    (output_dir / "reference_report.md").write_text("# Stage 3 V2 Reference Evaluation\n\nReference metrics are diagnostic/supporting metrics, not automatic semantic truth.\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

