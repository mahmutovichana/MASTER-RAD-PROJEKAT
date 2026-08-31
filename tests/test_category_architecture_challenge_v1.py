from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import pytest

from scripts.export_category_architecture_challenge_v1 import (
    FORBIDDEN_EXPORT_FIELDS,
    FROZEN_VALIDATION_CASE_IDS_SHA256,
    LABELS,
    SAFE_EXPORT_FIELDS,
    audit_export_rows,
    build_code_text,
    build_docs_text,
    export_row,
    reject_confirmation_path,
    stable_json_hash,
)


ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIR = ROOT / "data" / "final_v2" / "architecture_challenge_v1"
NOTEBOOK = ROOT / "notebooks" / "category_codebert_architecture_challenge_v1.ipynb"


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def safe_row(case_id: str = "case-1", *, partition: str = "development_train") -> dict:
    return {
        "case_id": case_id,
        "repository": "org/private-repo",
        "pr_number": 1,
        "partition": partition,
        "language": "python",
        "code_changed_files": ["src/app.py"],
        "code_diff_excerpt": "+ changed behavior in https://github.com/org/private-repo",
        "docs_before_excerpt": "Existing docs mention org/private-repo before the change.",
        "gold_docs_update_required": True,
        "gold_doc_category": "api_reference",
        "independent_human_reviewed": True,
    }


def test_confirmation_paths_are_forbidden() -> None:
    with pytest.raises(ValueError, match="Confirmation path"):
        reject_confirmation_path(Path("experiments/gold/confirmation.jsonl"))


def test_export_row_rejects_refresh_as_training_source() -> None:
    with pytest.raises(ValueError, match="refresh validation"):
        export_row(safe_row(partition="refresh_validation"), partition="refresh_validation")


def test_repository_identity_is_masked_from_model_text() -> None:
    row = export_row(safe_row(), partition="development_train")
    combined = build_code_text(row) + "\n" + build_docs_text(row)
    assert "org/private-repo" not in combined.lower()
    assert "github.com/org/private-repo" not in combined.lower()
    assert "[REPOSITORY]" in combined


def test_audit_rejects_forbidden_export_field() -> None:
    validation = [export_row(safe_row("v", partition="development_validation"), partition="development_validation")]
    train = [export_row(safe_row("t"), partition="development_train")]
    train[0]["docs_after_excerpt"] = "post-change documentation"

    audit = audit_export_rows(train, validation)

    assert audit["status"] == "failed"
    assert any("forbidden export keys" in error for error in audit["errors"])


def test_materialized_architecture_export_matches_frozen_contract() -> None:
    manifest_path = EXPORT_DIR / "export_manifest.json"
    if not manifest_path.exists():
        pytest.skip("architecture challenge export artifacts are not materialized")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    train = read_jsonl(EXPORT_DIR / "natural_train_primary_four.jsonl")
    validation = read_jsonl(EXPORT_DIR / "natural_validation_primary_four.jsonl")

    assert manifest["audit"]["status"] == "passed"
    assert manifest["confirmation_accessed"] is False
    assert manifest["controlled_or_synthetic_rows_used"] is False
    assert manifest["refresh_validation_used_for_training"] is False
    assert manifest["audit"]["train_validation_repository_overlap"] == []
    assert len(train) == 1038
    assert len(validation) == 322
    assert Counter(row["gold_doc_category"] for row in train) == {
        "api_reference": 412,
        "configuration": 277,
        "developer_setup": 88,
        "model_contract": 261,
    }
    assert Counter(row["gold_doc_category"] for row in validation) == {
        "api_reference": 85,
        "configuration": 154,
        "developer_setup": 19,
        "model_contract": 64,
    }
    assert stable_json_hash([row["case_id"] for row in validation]) == FROZEN_VALIDATION_CASE_IDS_SHA256
    assert all(set(row) == set(SAFE_EXPORT_FIELDS) for row in train + validation)
    assert not any(set(row) & FORBIDDEN_EXPORT_FIELDS for row in train + validation)
    assert set(row["gold_doc_category"] for row in train + validation) == set(LABELS)


def test_notebook_is_codebert_joint_experiment_not_old_semantic_pipeline() -> None:
    if not NOTEBOOK.exists():
        pytest.skip("CodeBERT architecture challenge notebook is not materialized")
    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    source = "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])

    assert 'MODEL_NAME = "microsoft/codebert-base"' in source
    assert "prepare_for_model" in source
    assert "kept_code" in source
    assert "kept_docs" in source
    assert "SentenceTransformer" not in source
    assert "MiniLM" not in source
    assert "ModernBERT" not in source
    assert "UniXcoder" not in source
    assert "Jina" not in source
