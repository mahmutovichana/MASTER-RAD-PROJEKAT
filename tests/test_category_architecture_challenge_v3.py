from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import pytest

from scripts.prepare_category_architecture_challenge_v3 import (
    CURRENT_HYBRID_IMPLEMENTATION,
    FROZEN_VALIDATION_CASE_IDS_SHA256,
    JINA_MODEL_NAME,
    LABELS,
    NOTEBOOK_PATH,
    PRIMARY_MODEL_ID,
    TRAIN_PATH,
    VALIDATION_PATH,
    build_code_text,
    build_docs_text,
    choose_jina_max_seq_length,
    read_jsonl,
    reject_confirmation_path,
    reject_forbidden_row,
    retained_texts_for_jina,
    stable_json_hash,
    validate_export_row,
    validate_training_row,
    validate_v1_exports,
)


ROOT = Path(__file__).resolve().parents[1]


class DummyTokenizer:
    def encode(self, text: str, add_special_tokens: bool = False) -> list[int]:
        del add_special_tokens
        return [index + 10 for index, _token in enumerate(str(text).replace("\n", " ").split())]

    def decode(self, ids: list[int], skip_special_tokens: bool = True) -> str:
        del skip_special_tokens
        return " ".join(f"tok_{item}" for item in ids)


def safe_row(*, partition: str = "development_train", category: str = "api_reference") -> dict:
    return {
        "case_id": "DGPR-safe-v3",
        "repository": "mahmutovichana/private-service",
        "language": "python",
        "code_changed_files": [
            "src/api/users.py",
            "https://github.com/mahmutovichana/private-service/blob/main/src/api/users.py",
        ],
        "code_diff_excerpt": "\n".join(f"+ public diff line {i}" for i in range(500)),
        "docs_before_excerpt": "\n".join(f"documented behavior line {i}" for i in range(500)),
        "gold_doc_category": category,
        "partition": partition,
    }


def test_exact_frozen_v1_export_used_and_validation_hash_unchanged() -> None:
    audit = validate_v1_exports()
    train = read_jsonl(TRAIN_PATH)
    validation = read_jsonl(VALIDATION_PATH)

    assert audit["validation_case_ids_sha256"] == FROZEN_VALIDATION_CASE_IDS_SHA256
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
    assert not ({row["repository"] for row in train} & {row["repository"] for row in validation})
    assert stable_json_hash([row["case_id"] for row in validation]) == FROZEN_VALIDATION_CASE_IDS_SHA256


def test_confirmation_and_controlled_rows_are_rejected() -> None:
    with pytest.raises(ValueError, match="Confirmation path"):
        reject_confirmation_path(Path("data/final_v2/confirmation/split.jsonl"))
    with pytest.raises(ValueError, match="confirmation"):
        reject_forbidden_row(safe_row(partition="confirmation"), source="train")
    with pytest.raises(ValueError, match="controlled"):
        reject_forbidden_row({**safe_row(), "controlled_design_supervision": True}, source="train")
    with pytest.raises(ValueError, match="controlled"):
        reject_forbidden_row({**safe_row(), "label_source": "controlled_synthetic_positive"}, source="train")
    with pytest.raises(ValueError, match="synthetic"):
        reject_forbidden_row({**safe_row(), "label_source": "synthetic_positive"}, source="train")


def test_non_primary_categories_and_validation_are_excluded_from_training() -> None:
    with pytest.raises(ValueError, match="only development_train"):
        validate_training_row(safe_row(partition="development_validation"))
    with pytest.raises(ValueError, match="only development_train"):
        validate_training_row(safe_row(partition="refresh_validation"))
    with pytest.raises(ValueError, match="primary-four"):
        validate_training_row(safe_row(category="other_documentation"))
    with pytest.raises(ValueError, match="primary-four"):
        validate_training_row(safe_row(category="no_update"))


@pytest.mark.parametrize(
    "field",
    [
        "docs_after",
        "docs_after_excerpt",
        "docs_diff",
        "docs_diff_excerpt",
        "provenance_tier",
        "human_label_notes",
        "suggested_docs_update_required",
        "suggested_doc_category",
        "suggested_notes",
    ],
)
def test_forbidden_fields_are_not_export_or_model_inputs(field: str) -> None:
    with pytest.raises(ValueError, match="unexpected export fields|controlled"):
        validate_export_row({**safe_row(), field: "forbidden"}, source="train")


def test_repository_identity_is_sanitized_from_model_text() -> None:
    row = safe_row()
    text = build_code_text(row) + "\n" + build_docs_text(row)
    lowered = text.lower()
    assert "mahmutovichana/private-service" not in lowered
    assert "github.com/mahmutovichana/private-service" not in lowered
    assert "[REPOSITORY]" in text


def test_deterministic_long_context_policy_and_retention() -> None:
    assert choose_jina_max_seq_length(16.0) == (2048, "gpu_memory_lt_20gb")
    assert choose_jina_max_seq_length(20.0) == (4096, "gpu_memory_ge_20gb")
    assert choose_jina_max_seq_length(35.0) == (8192, "gpu_memory_ge_35gb")

    code_text, docs_text, stats = retained_texts_for_jina(DummyTokenizer(), safe_row(), max_seq_length=128)
    assert code_text
    assert docs_text
    assert stats["original_diff_tokens"] > 0
    assert stats["retained_diff_tokens"] > 0
    assert stats["original_docs_tokens"] > 0
    assert stats["retained_docs_tokens"] > 0
    assert stats["retained_diff_tokens"] > stats["retained_prefix_tokens"]


def test_current_hybrid_configuration_is_documented_and_matched() -> None:
    lexical = CURRENT_HYBRID_IMPLEMENTATION["lexical_channel"]
    classifier = CURRENT_HYBRID_IMPLEMENTATION["classifier"]

    assert lexical["vectorizer"] == "TfidfVectorizer"
    assert lexical["analyzer"] == "char_wb"
    assert lexical["ngram_range"] == [3, 5]
    assert lexical["min_df"] == 2
    assert lexical["max_features"] == 20000
    assert lexical["sublinear_tf"] is True
    assert "training rows only" in lexical["fit_policy"]
    assert classifier["class"] == "sklearn.linear_model.LogisticRegression"
    assert classifier["C"] == 1.0
    assert classifier["solver"] == "lbfgs"
    assert classifier["max_iter"] == 2000
    assert classifier["random_state"] == 42
    assert classifier["class_weight"] is None
    assert classifier["resampling"] is None
    assert CURRENT_HYBRID_IMPLEMENTATION["new_semantic_encoder"] == JINA_MODEL_NAME


def test_embedding_cache_is_ignored_by_git() -> None:
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert "experiments/category_architecture_challenge_v3/jina_code_hybrid/cache/" in gitignore
    assert "experiments/category_architecture_challenge_v3/jina_code_hybrid/**/*.npy" in gitignore


def test_notebook_is_one_frozen_jina_hybrid_experiment() -> None:
    if not NOTEBOOK_PATH.exists():
        pytest.skip("V3 notebook is not materialized yet")
    notebook = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))
    source = "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])

    assert f'JINA_MODEL_NAME = "{JINA_MODEL_NAME}"' in source
    assert f'PRIMARY_MODEL_ID = "{PRIMARY_MODEL_ID}"' in source
    assert "SentenceTransformer(" in source
    assert "trust_remote_code=True" in source
    assert "jina_model.eval()" in source
    assert "parameter.requires_grad_(False)" in source
    assert ".fit(" not in source.split("jina_model = SentenceTransformer", 1)[1].split("tokenizer =", 1)[0]
    assert "jina_model.fit(" not in source
    assert "optimizer" not in source.lower()
    assert "lora" not in source.lower()
    assert "adapter" not in source.lower()
    assert "WeightedRandomSampler" not in source
    assert "SMOTE" not in source
    assert "oversampling" not in source
    assert "undersampling" not in source
    assert "class_weight=\"balanced\"" not in source
    assert "TfidfVectorizer(" in source
    assert "code_vectorizer.fit_transform" in source
    assert "code_vectorizer.transform" in source
    assert "relational_semantic_features" in source
    assert "LogisticRegression(C=1.0, solver=\"lbfgs\", max_iter=2000, random_state=SEED)" in source
    assert "choose_jina_max_seq_length" in source
    assert "return 2048, \"gpu_memory_lt_20gb\"" in source
    assert "rows_with_zero_retained_diff" in source
    assert "rows_with_zero_retained_docs" in source
    assert "No retraining loop" not in source
