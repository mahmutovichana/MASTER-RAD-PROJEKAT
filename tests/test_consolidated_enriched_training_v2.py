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
    assert manifest["row_count"] == 25_913
    assert manifest["positive_count"] == 5_948
    assert manifest["negative_count"] == 19_965
    assert manifest["natural_diversity_included_rows"] == 779
    assert manifest["natural_diversity_missing_rows"] == 0
    assert manifest["duplicates_skipped"] == 0
    assert manifest["validation_error_count"] == 0
    assert manifest["category_counts"] == {
        "api_reference": 1_554,
        "configuration": 1_467,
        "developer_setup": 992,
        "model_contract": 1_122,
        "no_update": 19_965,
        "other_documentation": 813,
    }


def test_training_v2_split_is_leakage_safe() -> None:
    manifest = read(RUN / "gold/human_gold_manifest.json")
    assert manifest["partition_row_counts"] == {
        "development_train": 19_018,
        "development_validation": 3_148,
        "confirmation": 3_747,
    }
    assert manifest["augmentation_train_only_rows"] == 4_054
    assert manifest["natural_diversity_rows"] == 779
    assert manifest["natural_diversity_partition_row_counts"] == {
        "confirmation": 160,
        "development_train": 499,
        "development_validation": 120,
    }
    assert manifest["repository_overlap_count"] == 0
    assert manifest["confirmation_sealed"] is True
    assert manifest["frozen_validation_case_ids_preserved"] is True
    assert manifest["sealed_confirmation_case_ids_preserved"] is True


def test_gate1_freeze_manifest_matches_new_gold_identity() -> None:
    manifest = read(ROOT / "reports/final_v2/GOLD_FREEZE_MANIFEST.json")
    assert manifest["status"] == "PASS"
    assert manifest["immutable_gold"] is True
    assert manifest["row_count"] == 25_913
    assert manifest["natural_diversity_included_rows"] == 779
    assert manifest["no_training_run_by_gate_1"] is True
    assert manifest["confirmation_accessed_by_gate_1"] is False
    assert manifest["model_visible_collision_audit"]["cross_development_confirmation_groups"] == 0
    assert manifest["empty_docs_audit"]["unresolved_re_review_rows"] == 0
