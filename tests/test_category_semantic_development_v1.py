from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from scripts.run_category_semantic_development_v1 import (
    CONTROLLED_DESIGN_LABEL_SOURCE,
    SAFE_INPUT_FIELDS,
    build_code_text,
    build_docs_text,
    deterministic_chunks,
    embedding_cache_key,
    load_development_jsonl,
    reject_confirmation_path,
    reject_confirmation_row,
    relational_semantic_features,
    representation_field_audit,
    select_training_rows,
    stable_json_hash,
)


def row(case_id: str, *, controlled: bool = False, partition: str = "development_train") -> dict:
    return {
        "case_id": case_id,
        "partition": partition,
        "gold_docs_update_required": True,
        "gold_doc_category": "developer_setup",
        "language": "python",
        "code_changed_files": ["pyproject.toml"],
        "code_diff_excerpt": "+requires-python = '>=3.12'",
        "docs_before_excerpt": "Requires Python 3.11.",
        "repository": "secret/repository-identity",
        "docs_after_excerpt": "Requires Python 3.12.",
        "label_source": CONTROLLED_DESIGN_LABEL_SOURCE if controlled else "natural_human_gold",
        "supervision_source": "controlled_synthetic_positive" if controlled else "natural_human_gold",
        "controlled_design_supervision": controlled,
        "independent_human_reviewed": not controlled,
    }


def test_confirmation_path_rejected() -> None:
    with pytest.raises(ValueError, match="Confirmation path"):
        reject_confirmation_path(Path("experiments/gold/confirmation.jsonl"))


def test_confirmation_row_rejected() -> None:
    with pytest.raises(ValueError, match="Confirmation row"):
        reject_confirmation_row(row("c", partition="confirmation"))


def test_loader_rejects_confirmation_row(tmp_path: Path) -> None:
    path = tmp_path / "validation.jsonl"
    path.write_text(json.dumps(row("c", partition="confirmation")) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Confirmation row"):
        load_development_jsonl(path, "development_validation")


def test_controlled_rows_only_enter_controlled_enabled_scenario() -> None:
    rows = [row("natural"), row("controlled", controlled=True)]
    natural = select_training_rows(rows, controlled_enabled=False)
    augmented = select_training_rows(rows, controlled_enabled=True)
    assert [item["case_id"] for item in natural] == ["natural"]
    assert [item["case_id"] for item in augmented] == ["natural", "controlled"]


def test_validation_membership_hash_is_stable() -> None:
    case_ids = ["a", "b", "c"]
    assert stable_json_hash(case_ids) == stable_json_hash(case_ids)
    assert stable_json_hash(case_ids) != stable_json_hash(case_ids[::-1])


def test_safe_input_fields_and_provenance_excluded() -> None:
    audit = representation_field_audit()
    assert audit["repository_identity_excluded"] is True
    assert audit["provenance_excluded"] is True
    assert audit["post_change_docs_excluded"] is True
    used = set(SAFE_INPUT_FIELDS["code"]) | set(SAFE_INPUT_FIELDS["docs"])
    assert "repository" not in used
    assert "label_source" not in used
    assert "docs_after_excerpt" not in used


def test_text_builders_do_not_include_repository_provenance_or_docs_after() -> None:
    example = row("x")
    code = build_code_text(example)
    docs = build_docs_text(example)
    combined = code + docs
    assert "secret/repository-identity" not in combined
    assert "natural_human_gold" not in combined
    assert "Requires Python 3.12" not in combined
    assert "Requires Python 3.11" in docs


def test_semantic_features_are_deterministic() -> None:
    code = np.asarray([[1.0, 0.0], [0.0, 1.0]], dtype=np.float32)
    docs = np.asarray([[0.5, 0.5], [0.0, 1.0]], dtype=np.float32)
    first = relational_semantic_features(code, docs)
    second = relational_semantic_features(code, docs)
    np.testing.assert_array_equal(first, second)
    assert first.shape == (2, 9)


def test_embedding_cache_key_includes_model_revision_and_content() -> None:
    base = embedding_cache_key("model", "rev-a", "code", ["alpha"])
    assert base == embedding_cache_key("model", "rev-a", "code", ["alpha"])
    assert base != embedding_cache_key("model", "rev-b", "code", ["alpha"])
    assert base != embedding_cache_key("model", "rev-a", "code", ["beta"])
    assert base != embedding_cache_key("model", "rev-a", "docs", ["alpha"])


def test_chunking_is_deterministic_and_bounded() -> None:
    text = "abc " * 2_000
    first = deterministic_chunks(text)
    second = deterministic_chunks(text)
    assert first == second
    assert len(first) == 2
    assert all(len(chunk) <= 1_000 for chunk in first)


def test_completed_artifacts_preserve_validation_and_safe_fields() -> None:
    root = Path(__file__).resolve().parents[1] / "experiments" / "category_semantic_development_v1"
    comparison = root / "model_comparison.json"
    if not comparison.exists():
        pytest.skip("semantic experiment artifacts are not materialized")
    payload = json.loads(comparison.read_text(encoding="utf-8"))
    assert payload["validation_membership_identical"] is True
    assert payload["confirmation_accessed"] is False
    predictions = (root / "validation_predictions.jsonl").read_text(encoding="utf-8")
    assert "docs_after_excerpt" not in predictions
    assert "repository" not in predictions
