from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.human_review_workflow_v2 import deterministic_sample, load_jsonl, make_review_row, write_csv, write_json, write_jsonl


def run(input_path: Path, output_dir: Path, *, target: int = 400, seed: int = 42) -> dict:
    rows = deterministic_sample(load_jsonl(input_path), target, seed)
    review_rows = [make_review_row(row) for row in rows]
    output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(output_dir / "second_reviewer_subset.jsonl", review_rows)
    write_csv(output_dir / "second_reviewer_subset.csv", review_rows)
    manifest = {"input": str(input_path), "target": target, "seed": seed, "selected_rows": len(review_rows), "sampling_ignores_labels_and_predictions": True}
    write_json(output_dir / "second_reviewer_subset_manifest.json", manifest)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Build blind second-reviewer subset for reliability only.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--target", type=int, default=400)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    print(json.dumps(run(Path(args.input), Path(args.output_dir), target=args.target, seed=args.seed), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
