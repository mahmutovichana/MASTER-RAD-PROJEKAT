from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from docguard_ml_v2.data_contract import write_json
from docguard_ml_v2.model_manifest import sha256_file, utc_now


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def run(*, model_file: Path, training_summary: Path, config: Path, dataset_manifest: Path, repository_partition_manifest: Path, output: Path, train_split: Path | None = None, validation_split: Path | None = None, model_version: str | None = None) -> dict[str, Any]:
    summary = load_json(training_summary)
    manifest = {
        "status": "frozen",
        "model_version": model_version or str(summary.get("model_version") or "final_v2_model"),
        "selected_model": summary.get("selected_model"),
        "selected_threshold": summary.get("selected_threshold"),
        "development_metrics": summary.get("best_metrics"),
        "freeze_timestamp": utc_now(),
        "seed": summary.get("config", {}).get("seed"),
        "confirmation_accessed": False,
        "hashes": {
            "model": sha256_file(model_file),
            "training_summary": sha256_file(training_summary),
            "config": sha256_file(config),
            "dataset_manifest": sha256_file(dataset_manifest),
            "repository_partition_manifest": sha256_file(repository_partition_manifest),
            "train_split": None if train_split is None else sha256_file(train_split),
            "validation_split": None if validation_split is None else sha256_file(validation_split),
        },
        "paths": {
            "model_file": str(model_file),
            "training_summary": str(training_summary),
            "config": str(config),
            "dataset_manifest": str(dataset_manifest),
            "repository_partition_manifest": str(repository_partition_manifest),
        },
    }
    write_json(output, manifest)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Freeze a Final V2 development-selected model before confirmation.")
    parser.add_argument("--model-file", required=True)
    parser.add_argument("--training-summary", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--dataset-manifest", required=True)
    parser.add_argument("--repository-partition-manifest", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--train-split")
    parser.add_argument("--validation-split")
    parser.add_argument("--model-version")
    args = parser.parse_args()
    print(json.dumps(run(model_file=Path(args.model_file), training_summary=Path(args.training_summary), config=Path(args.config), dataset_manifest=Path(args.dataset_manifest), repository_partition_manifest=Path(args.repository_partition_manifest), output=Path(args.output), train_split=Path(args.train_split) if args.train_split else None, validation_split=Path(args.validation_split) if args.validation_split else None, model_version=args.model_version), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

