from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import pytest

from scripts.prepare_category_architecture_challenge_v2 import (
    FORBIDDEN_EXPORT_FIELDS,
    FROZEN_VALIDATION_CASE_IDS_SHA256,
    LABELS,
    MODEL_NAME,
    NOTEBOOK_PATH,
    SAFE_EXPORT_FIELDS,
    TRAIN_PATH,
    VALIDATION_PATH,
    build_balanced_pair_inputs,
    build_code_text,
    build_docs_text,
    choose_max_length,
    read_jsonl,
    reject_confirmation_path,
    reject_forbidden_row,
    stable_json_hash,
    validate_export_row,
    validate_training_row,
    validate_v1_exports,
)


ROOT = Path(__file__).resolve().parents[1]


class DummyTokenizer:
    pad_token_id = 0

    def encode(self, text: str, add_special_tokens: bool = False) -> list[int]:
        del add_special_tokens
        tokens = []
        for index, token in enumerate(str(text).replace("\n", " ").split(), 1):
            tokens.append((hash(token) + index) % 30000 + 10)
        return tokens

    def build_inputs_with_special_tokens(self, token_ids_0, token_ids_1=None):
        token_ids_1 = token_ids_1 or []
        return [101] + list(token_ids_0) + [102] + list(token_ids_1) + [102]


def safe_row(*, partition: str = "development_train") -> dict:
    return {
        "case_id": "DGPR-safe",
        "repository": "mahmutovichana/private-service",
        "language": "python",
        "code_changed_files": ["src/api/users.py", "https://github.com/mahmutovichana/private-service/blob/main/src/api/users.py"],
        "code_diff_excerpt": "\n".join(f"+ changed public behavior line {i}" for i in range(500)),
        "docs_before_excerpt": "\n".join(f"documented behavior line {i}" for i in range(500)),
        "gold_doc_category": "api_reference",
        "partition": partition,
    }


def test_confirmation_paths_are_rejected() -> None:
    with pytest.raises(ValueError, match="Confirmation path"):
        reject_confirmation_path(Path("data/final_v2/confirmation/frozen.jsonl"))


def test_confirmation_and_controlled_rows_are_rejected() -> None:
    with pytest.raises(ValueError, match="confirmation"):
        reject_forbidden_row({**safe_row(partition="confirmation")}, source="train")
    with pytest.raises(ValueError, match="controlled"):
        reject_forbidden_row({**safe_row(), "controlled_design_supervision": True}, source="train")
    with pytest.raises(ValueError, match="controlled/synthetic"):
        reject_forbidden_row({**safe_row(), "label_source": "controlled_positive"}, source="train")
    with pytest.raises(ValueError, match="controlled/synthetic"):
        reject_forbidden_row({**safe_row(), "supervision_source": "synthetic_generation"}, source="train")


def test_validation_partitions_are_excluded_from_training() -> None:
    with pytest.raises(ValueError, match="development_train|validation row is forbidden"):
        validate_training_row(safe_row(partition="development_validation"))
    with pytest.raises(ValueError, match="development_train|validation row is forbidden"):
        validate_training_row(safe_row(partition="refresh_validation"))


@pytest.mark.parametrize(
    "field",
    [
        "provenance_tier",
        "docs_after",
        "docs_after_excerpt",
        "docs_diff",
        "docs_diff_excerpt",
        "suggested_docs_update_required",
        "suggested_doc_category",
        "suggested_notes",
    ],
)
def test_forbidden_fields_are_excluded(field: str) -> None:
    row = {**safe_row(), field: "forbidden"}
    with pytest.raises(ValueError, match="unexpected export fields|controlled/synthetic"):
        validate_export_row(row, source="train")


def test_repository_identity_is_excluded_from_model_text() -> None:
    row = safe_row()
    text = build_code_text(row) + "\n" + build_docs_text(row)
    lowered = text.lower()
    assert "mahmutovichana/private-service" not in lowered
    assert "github.com/mahmutovichana/private-service" not in lowered
    assert "[REPOSITORY]" in text


def test_frozen_v1_exports_remain_unchanged_and_disjoint() -> None:
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
    assert all(set(row) == SAFE_EXPORT_FIELDS for row in train + validation)
    assert not any(set(row) & FORBIDDEN_EXPORT_FIELDS for row in train + validation)
    assert set(row["gold_doc_category"] for row in train + validation) == set(LABELS)


def test_long_context_hardware_policy() -> None:
    assert choose_max_length(16.0) == (2048, "gpu_memory_lt_20gb")
    assert choose_max_length(20.0) == (3072, "gpu_memory_ge_20gb")
    assert choose_max_length(35.0) == (4096, "gpu_memory_ge_35gb")


def test_nonempty_diff_and_docs_cannot_be_truncated_to_zero() -> None:
    encoded, stats = build_balanced_pair_inputs(DummyTokenizer(), safe_row(), max_length=128)

    assert len(encoded["input_ids"]) <= 128
    assert len(encoded["attention_mask"]) == len(encoded["input_ids"])
    assert stats["original_diff_tokens"] > 0
    assert stats["retained_diff_tokens"] > 0
    assert stats["original_docs_tokens"] > 0
    assert stats["retained_docs_tokens"] > 0
    assert stats["retained_diff_tokens"] > stats["retained_prefix_tokens"]


def test_notebook_uses_modernbert_long_context_and_no_class_balancing() -> None:
    if not NOTEBOOK_PATH.exists():
        pytest.skip("ModernBERT V2 notebook is not materialized yet")
    notebook = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))
    source = "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])

    assert f'MODEL_NAME = "{MODEL_NAME}"' in source
    assert "answerdotai/ModernBERT-base" in source
    assert 'MODEL_NAME = "microsoft/codebert-base"' not in source
    assert 'AutoTokenizer.from_pretrained("microsoft/codebert-base"' not in source
    assert "codebert_joint_512" in source
    assert "MiniLM" not in source
    assert "SentenceTransformer" not in source
    assert "UniXcoder" not in source
    assert "AutoModelForSequenceClassification" in source
    assert "attn_implementation=\"sdpa\"" in source
    assert "choose_max_length" in source
    assert "MAX_LENGTH = 2048" not in source
    assert "DataCollatorWithPadding" in source
    assert "pad_to_multiple_of=8" in source
    assert "rows_with_zero_retained_diff" in source
    assert "rows_with_zero_retained_docs" in source
    assert "gradient_accumulation_steps=GRADIENT_ACCUMULATION_STEPS" in source
    assert "eval_strategy=\"epoch\"" in source
    assert "processing_class=tokenizer" in source
    assert "class_weight" not in source
    assert "WeightedRandomSampler" not in source
    assert "SMOTE" not in source
    assert "oversampling" not in source
    assert "undersampling" not in source
    assert "focal loss" not in source.lower()
    assert "controlled/synthetic rows" in source
    assert "confirmation" in source.lower()
