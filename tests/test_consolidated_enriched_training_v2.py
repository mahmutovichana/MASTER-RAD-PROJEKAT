from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/final_v2/human_review/consolidated_enriched_training_v2"
RUN = ROOT / "experiments/consolidated_enriched_training_v2"


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_consolidated_v2_manifest() -> None:
    manifest = read(DATA / "manifest.json")
    assert manifest["validation"] == "PASS"
    assert manifest["row_count"] == 25_134
    assert manifest["positive_count"] == 5_939
    assert manifest["negative_count"] == 19_195
    assert manifest["duplicates_skipped"] == 0
    assert manifest["validation_error_count"] == 0
    assert manifest["category_counts"] == {
        "api_reference": 1_552,
        "configuration": 1_465,
        "developer_setup": 989,
        "model_contract": 1_122,
        "no_update": 19_195,
        "other_documentation": 811,
    }


def test_training_v2_split_is_leakage_safe() -> None:
    manifest = read(RUN / "gold/human_gold_manifest.json")
    assert manifest["partition_row_counts"] == {
        "development_train": 18_519,
        "development_validation": 3_028,
        "confirmation": 3_587,
    }
    assert manifest["augmentation_train_only_rows"] == 4_054
    assert manifest["repository_overlap_count"] == 0
    assert manifest["frozen_validation_case_ids_preserved"] is True
    assert manifest["sealed_confirmation_case_ids_preserved"] is True


def test_models_and_figures_exist() -> None:
    binary = read(RUN / "binary_v4/training_summary.json")
    category = read(RUN / "category_v8/training_summary.json")
    figures = read(RUN / "figures/figures_manifest.json")
    assert binary["status"] == "ok"
    assert category["status"] == "ok"
    assert binary["row_counts"]["validation_used"] == 3_028
    assert category["scope_counts"]["development_validation"]["primary_stage2_eligible_rows"] == 322
    assert len(figures["figures"]) == 8
    for filename in figures["figures"]:
        path = RUN / "figures" / filename
        assert path.exists()
        assert path.stat().st_size > 10_000
