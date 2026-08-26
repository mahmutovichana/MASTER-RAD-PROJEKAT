from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from docguard_eval_v2.reference_evaluation import read_jsonl, sample_manifest, sample_primary, sample_stress, write_json, write_jsonl


def run(source: Path, output_dir: Path, seed: int = 42, target_size: int = 100, stress_per_category: int = 25) -> dict:
    rows = read_jsonl(source)
    primary = sample_primary(rows, seed=seed, target_size=target_size)
    stress = sample_stress(rows, seed=seed, per_category=stress_per_category)
    output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(output_dir / "primary_natural_sample.jsonl", primary)
    write_jsonl(output_dir / "secondary_category_stress_sample.jsonl", stress)
    manifest = {
        "primary": sample_manifest(source, primary, seed=seed, method="natural_distribution_random_predicted_positive"),
        "secondary": sample_manifest(source, stress, seed=seed, method="supplementary_category_stratified_stress_sample"),
        "secondary_is_supplementary": True,
    }
    write_json(output_dir / "sample_manifest.json", manifest)
    (output_dir / "sample_report.md").write_text("# Stage 3 V2 Confirmation Samples\n\nThe primary sample is natural-distribution random predicted-positive sampling. The category-stratified stress sample is supplementary only.\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Stage 3 V2 confirmation sample files.")
    parser.add_argument("--source", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--target-size", type=int, default=100)
    parser.add_argument("--stress-per-category", type=int, default=25)
    args = parser.parse_args()
    print(json.dumps(run(Path(args.source), Path(args.output_dir), seed=args.seed, target_size=args.target_size, stress_per_category=args.stress_per_category), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

