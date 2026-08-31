"""Audit explicit natural-vs-controlled provenance on development rows only."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.correct_development_provenance_v2 import load_jsonl
from docguard_ml_v2.data_contract import (
    ADDITIONAL_REVIEWED_NATURAL_POSITIVE_LABEL_SOURCE,
    CONTROLLED_DESIGN_LABEL_SOURCE,
    NATURAL_HUMAN_GOLD_LABEL_SOURCE,
)


def audit_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    errors: list[str] = []
    for row in rows:
        rid = str(row.get("case_id") or "<missing>")
        source = str(row.get("label_source") or "")
        controlled = source == CONTROLLED_DESIGN_LABEL_SOURCE
        if controlled:
            if row.get("independent_human_reviewed") is not False:
                errors.append(f"{rid}: controlled row marked independently human-reviewed")
            if row.get("controlled_design_supervision") is not True:
                errors.append(f"{rid}: controlled_design_supervision missing")
            if row.get("train_only") is not True or row.get("partition") != "development_train":
                errors.append(f"{rid}: controlled row is not train-only")
            if row.get("label_source") == "human_reviewed_final_v2":
                errors.append(f"{rid}: controlled row uses legacy human label source")
        elif source in {NATURAL_HUMAN_GOLD_LABEL_SOURCE, ADDITIONAL_REVIEWED_NATURAL_POSITIVE_LABEL_SOURCE}:
            if row.get("independent_human_reviewed") is not True:
                errors.append(f"{rid}: natural row missing independent human provenance")
            if row.get("controlled_design_supervision") is not False:
                errors.append(f"{rid}: natural row marked controlled")
        else:
            errors.append(f"{rid}: unsupported label source {source!r}")
        if row.get("partition") == "confirmation":
            errors.append(f"{rid}: confirmation row supplied to development audit")
    return {
        "row_count": len(rows),
        "label_source_counts": dict(sorted(Counter(str(row.get("label_source")) for row in rows).items())),
        "supervision_source_counts": dict(sorted(Counter(str(row.get("supervision_source")) for row in rows).items())),
        "controlled_rows": sum(row.get("label_source") == CONTROLLED_DESIGN_LABEL_SOURCE for row in rows),
        "independent_human_rows": sum(row.get("independent_human_reviewed") is True for row in rows),
        "errors": errors,
        "status": "PASS" if not errors else "FAIL",
    }


def run(train: Path, validation: Path, output: Path) -> dict[str, Any]:
    train_rows = load_jsonl(train)
    validation_rows = load_jsonl(validation)
    report = {
        "version": "development_provenance_audit_v2",
        "confirmation_accessed": False,
        "scopes": {
            "development_train": audit_rows(train_rows),
            "development_validation": audit_rows(validation_rows),
        },
    }
    report["status"] = "PASS" if all(item["status"] == "PASS" for item in report["scopes"].values()) else "FAIL"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit development provenance; confirmation input is forbidden.")
    parser.add_argument("--train", type=Path, required=True)
    parser.add_argument("--validation", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = run(args.train, args.validation, args.output)
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
