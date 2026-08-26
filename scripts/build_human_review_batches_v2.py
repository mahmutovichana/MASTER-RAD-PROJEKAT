from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.human_review_workflow_v2 import deterministic_sample, load_jsonl, make_review_row, progress, write_csv, write_json, write_jsonl


def run(input_path: Path, output_dir: Path, *, batch_size: int = 500, seed: int = 42, reviewer_id: str | None = None, partition_manifest: Path | None = None) -> dict:
    rows = [make_review_row(row) for row in deterministic_sample(load_jsonl(input_path), 10**12, seed)]
    output_dir.mkdir(parents=True, exist_ok=True)
    batches = []
    for index in range(0, len(rows), batch_size):
        batch_number = (index // batch_size) + 1
        batch_rows = rows[index : index + batch_size]
        stem = f"batch_{batch_number:03d}"
        write_jsonl(output_dir / f"{stem}.jsonl", batch_rows)
        write_csv(output_dir / f"{stem}.csv", batch_rows)
        batches.append({"batch_id": stem, "row_count": len(batch_rows), "jsonl": f"{stem}.jsonl", "csv": f"{stem}.csv"})
    manifest = {
        "input": str(input_path),
        "seed": seed,
        "batch_size": batch_size,
        "reviewer_id": reviewer_id,
        "partition_manifest_supplied_for_audit_only": partition_manifest is not None,
        "partition_manifest": None if partition_manifest is None else str(partition_manifest),
        "partition_blinded_in_outputs": True,
        "ordering_strategy": "deterministic_repository_aware_interleaving_no_label_or_partition_inputs",
        "total_rows": len(rows),
        "batches": batches,
    }
    write_json(output_dir / "review_batch_manifest.json", manifest)
    write_json(output_dir / "review_progress_initial.json", progress(rows))
    (output_dir / "review_batch_report.md").write_text(f"# Final V2 Human Review Batches\n\n- Rows: `{len(rows)}`\n- Batch size: `{batch_size}`\n- Batches: `{len(batches)}`\n- Partition blinded in reviewer files: `True`\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Build deterministic Final V2 human review batches.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--batch-size", type=int, default=500)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--reviewer-id")
    parser.add_argument("--partition-manifest")
    args = parser.parse_args()
    print(json.dumps(run(Path(args.input), Path(args.output_dir), batch_size=args.batch_size, seed=args.seed, reviewer_id=args.reviewer_id, partition_manifest=Path(args.partition_manifest) if args.partition_manifest else None), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
