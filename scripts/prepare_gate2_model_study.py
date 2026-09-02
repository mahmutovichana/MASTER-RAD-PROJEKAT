from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from docguard_ml_v2.data_contract import category_eligible_rows
from docguard_ml_v2.gate2_study import load_config, load_development_rows, make_outer_folds, sha256_file, write_csv


def run(config_path: Path, report_dir: Path) -> dict:
    config = load_config(config_path)
    rows, view = load_development_rows(config_path=config_path)
    binary_records, binary_splits = make_outer_folds(rows, task="binary", config=config)
    category_records, category_splits = make_outer_folds(rows, task="category", config=config)
    binary_path = report_dir / "outer_fold_assignments_binary.csv"
    category_path = report_dir / "outer_fold_assignments_category.csv"
    write_csv(binary_path, binary_records)
    write_csv(category_path, category_records)
    category_rows = category_eligible_rows(rows, allowed_partitions={"development_train", "development_validation"})
    manifest = {
        "status": "PREREGISTERED",
        **view,
        "binary_eligible_rows": len(rows),
        "binary_class_counts": dict(sorted(Counter(str(bool(row["gold_docs_update_required"])) for row in rows).items())),
        "category_eligible_rows": len(category_rows),
        "category_class_counts": dict(sorted(Counter(str(row["gold_doc_category"]) for row in category_rows).items())),
        "binary_outer_folds": binary_splits,
        "category_outer_folds": category_splits,
        "binary_repository_count": len(binary_records),
        "category_repository_count": len(category_records),
        "fold_artifacts": {
            "binary": {"path": str(binary_path).replace("\\", "/"), "sha256": sha256_file(binary_path)},
            "category": {"path": str(category_path).replace("\\", "/"), "sha256": sha256_file(category_path)},
        },
        "config_path": str(config_path).replace("\\", "/"),
        "config_sha256": sha256_file(config_path),
        "confirmation_sealed": True,
        "confirmation_accessed": False,
    }
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "development_view_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/final_v2/gate2_model_study.json")
    parser.add_argument("--report-dir", default="reports/final_v2/gate2")
    args = parser.parse_args()
    print(json.dumps(run(Path(args.config), Path(args.report_dir)), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
