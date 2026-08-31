"""Correct provenance on development materializations without opening confirmation data.

This script intentionally accepts only train and validation paths. It preserves
all labels, evidence, case IDs, row order, and partition membership while
separating natural human gold from controlled design supervision.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any

import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from docguard_ml_v2.data_contract import (
    ADDITIONAL_REVIEWED_NATURAL_POSITIVE_LABEL_SOURCE,
    CONTROLLED_DESIGN_LABEL_SOURCE,
    NATURAL_HUMAN_GOLD_LABEL_SOURCE,
)


CONTROLLED_SOURCE_NAMES = {
    "controlled_real_project_positive_v1",
    "controlled_real_project_positive_v2_imbalanced",
}
ADDITIONAL_SOURCE_NAME = "remaining_4800_partial_positive_54"


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if "confirmation" in path.name.lower() or "confirmation" in str(path.parent).lower():
        raise ValueError(f"Confirmation path is forbidden: {path}")
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8-sig") as handle:
        for line_number, line in enumerate(handle, 1):
            if line.strip():
                row = json.loads(line)
                if not isinstance(row, dict):
                    raise ValueError(f"Expected object at {path}:{line_number}")
                if row.get("partition") == "confirmation":
                    raise ValueError(f"Confirmation row is forbidden: {path}:{line_number}")
                rows.append(row)
    return rows


def write_jsonl_atomic(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            for row in rows:
                handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
        os.replace(temporary, path)
    except Exception:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_name(row: dict[str, Any]) -> str:
    return str(row.get("consolidated_source_dataset") or "")


def expected_provenance(row: dict[str, Any]) -> dict[str, Any]:
    source = source_name(row)
    tier = str(row.get("provenance_tier") or "")
    if source in CONTROLLED_SOURCE_NAMES or tier == "controlled_real_project_augmentation":
        return {
            "label_source": CONTROLLED_DESIGN_LABEL_SOURCE,
            "supervision_source": "controlled_synthetic_positive",
            "independent_human_reviewed": False,
            "controlled_design_supervision": True,
            "owner_accepted_for_training": True,
            "train_only": True,
        }
    if source == ADDITIONAL_SOURCE_NAME:
        return {
            "label_source": ADDITIONAL_REVIEWED_NATURAL_POSITIVE_LABEL_SOURCE,
            "supervision_source": "additional_natural_human_review",
            "independent_human_reviewed": True,
            "controlled_design_supervision": False,
            "owner_accepted_for_training": False,
            "train_only": False,
        }
    return {
        "label_source": NATURAL_HUMAN_GOLD_LABEL_SOURCE,
        "supervision_source": "natural_human_gold",
        "independent_human_reviewed": True,
        "controlled_design_supervision": False,
        "owner_accepted_for_training": False,
        "train_only": False,
    }


def correct_rows(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    before = {
        str(row.get("case_id")): (
            row.get("human_docs_update_required"),
            row.get("human_doc_category"),
            row.get("partition"),
        )
        for row in rows
    }
    if len(before) != len(rows):
        raise ValueError("Duplicate or missing case_id in development materialization")
    corrected: list[dict[str, Any]] = []
    for row in rows:
        copied = dict(row)
        old_source = copied.get("label_source")
        provenance = expected_provenance(copied)
        if old_source and old_source != provenance["label_source"]:
            copied["historical_label_source"] = old_source
        copied.update(provenance)
        if copied["label_source"] == CONTROLLED_DESIGN_LABEL_SOURCE and copied.get("partition") != "development_train":
            raise ValueError(f"Controlled row is not in development train: {copied.get('case_id')}")
        corrected.append(copied)
    after = {
        str(row.get("case_id")): (
            row.get("human_docs_update_required"),
            row.get("human_doc_category"),
            row.get("partition"),
        )
        for row in corrected
    }
    if before != after:
        raise ValueError("Provenance correction changed labels, case IDs, or partition membership")
    counts = {
        "row_count": len(corrected),
        "label_source_counts": dict(sorted(Counter(str(row["label_source"]) for row in corrected).items())),
        "supervision_source_counts": dict(sorted(Counter(str(row["supervision_source"]) for row in corrected).items())),
        "independent_human_reviewed_counts": dict(sorted(Counter(str(row["independent_human_reviewed"]) for row in corrected).items())),
        "controlled_design_supervision_counts": dict(sorted(Counter(str(row["controlled_design_supervision"]) for row in corrected).items())),
        "owner_accepted_for_training_counts": dict(sorted(Counter(str(row["owner_accepted_for_training"]) for row in corrected).items())),
        "train_only_counts": dict(sorted(Counter(str(row["train_only"]) for row in corrected).items())),
    }
    return corrected, counts


def run(*, train: Path, validation: Path, output_manifest: Path) -> dict[str, Any]:
    train_rows = load_jsonl(train)
    validation_rows = load_jsonl(validation)
    if any(row.get("partition") != "development_train" for row in train_rows):
        raise ValueError("Train materialization contains a non-development_train row")
    if any(row.get("partition") != "development_validation" for row in validation_rows):
        raise ValueError("Validation materialization contains a non-development_validation row")
    before_hashes = {"train.jsonl": sha256_file(train), "validation.jsonl": sha256_file(validation)}
    corrected_train, train_counts = correct_rows(train_rows)
    corrected_validation, validation_counts = correct_rows(validation_rows)
    write_jsonl_atomic(train, corrected_train)
    write_jsonl_atomic(validation, corrected_validation)
    manifest = {
        "version": "consolidated_enriched_training_v2_development_provenance",
        "confirmation_accessed": False,
        "scope": ["development_train", "development_validation"],
        "labels_or_membership_changed": False,
        "before_sha256": before_hashes,
        "after_sha256": {"train.jsonl": sha256_file(train), "validation.jsonl": sha256_file(validation)},
        "partitions": {"development_train": train_counts, "development_validation": validation_counts},
        "combined_label_source_counts": dict(sorted(Counter(row["label_source"] for row in corrected_train + corrected_validation).items())),
        "combined_supervision_source_counts": dict(sorted(Counter(row["supervision_source"] for row in corrected_train + corrected_validation).items())),
    }
    output_manifest.parent.mkdir(parents=True, exist_ok=True)
    output_manifest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Correct development-only provenance without opening confirmation data.")
    parser.add_argument("--train", type=Path, required=True)
    parser.add_argument("--validation", type=Path, required=True)
    parser.add_argument("--output-manifest", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(train=args.train, validation=args.validation, output_manifest=args.output_manifest), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
