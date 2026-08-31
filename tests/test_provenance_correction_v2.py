from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.audit_development_provenance_v2 import audit_rows
from scripts.correct_development_provenance_v2 import correct_rows, expected_provenance, load_jsonl
from scripts.consolidate_enriched_training_corpus_v2 import provenance_for_source
from docguard_ml_v2.data_contract import CONTROLLED_DESIGN_LABEL_SOURCE, validate_final_gold_row


def sample_row(source: str, partition: str = "development_train") -> dict:
    return {
        "case_id": f"case-{source}",
        "consolidated_source_dataset": source,
        "provenance_tier": "controlled_real_project_augmentation" if source.startswith("controlled") else "natural",
        "human_docs_update_required": True,
        "human_doc_category": "api_reference",
        "review_status": "approved",
        "human_review_complete": True,
        "label_source": "human_reviewed_final_v2",
        "partition": partition,
    }


def test_controlled_provenance_is_not_human_gold() -> None:
    expected = expected_provenance(sample_row("controlled_real_project_positive_v1"))
    assert expected["label_source"] == CONTROLLED_DESIGN_LABEL_SOURCE
    assert expected["independent_human_reviewed"] is False
    assert expected["controlled_design_supervision"] is True
    assert expected["train_only"] is True
    assert provenance_for_source("controlled_real_project_positive_v1", "controlled_real_project_augmentation") == expected


def test_correction_preserves_labels_ids_and_partition() -> None:
    rows = [
        sample_row("controlled_real_project_positive_v1"),
        sample_row("remaining_4800_partial_positive_54"),
        sample_row("consolidated_enriched_training_v1", "development_validation"),
    ]
    corrected, counts = correct_rows(rows)
    assert [(r["case_id"], r["human_docs_update_required"], r["human_doc_category"], r["partition"]) for r in corrected] == [
        (r["case_id"], r["human_docs_update_required"], r["human_doc_category"], r["partition"]) for r in rows
    ]
    assert counts["row_count"] == 3
    assert counts["label_source_counts"][CONTROLLED_DESIGN_LABEL_SOURCE] == 1
    assert audit_rows(corrected)["status"] == "PASS"


def test_data_contract_rejects_controlled_validation_row() -> None:
    row = sample_row("controlled_real_project_positive_v1", "development_validation")
    row.update(expected_provenance(row))
    row["gold_docs_update_required"] = True
    row["gold_doc_category"] = "api_reference"
    with pytest.raises(ValueError, match="development-train-only"):
        validate_final_gold_row(row)


def test_development_audit_rejects_confirmation_path(tmp_path: Path) -> None:
    path = tmp_path / "confirmation.jsonl"
    path.write_text(json.dumps(sample_row("consolidated_enriched_training_v1", "confirmation")) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Confirmation path"):
        load_jsonl(path)
