from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from docguard_eval_v2.reference_evaluation import (
    frozen_binary_prediction,
    frozen_category_prediction,
    sample_primary,
    sample_stress,
)
from scripts.run_frozen_stage3_v2_confirmation import (
    run_stage3_for_positive_row,
    validate_stage3_freeze,
)


class NoCallLLM:
    def generate(self, *args, **kwargs):
        raise AssertionError(
            "LLM must not be called."
        )


def sha(path: Path) -> str:
    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


def test_sampling_prefers_canonical_frozen_fields():
    row = {
        "case_id": "x",
        "frozen_binary_prediction": False,
        "pred_docs_update_required": True,
        "frozen_category_prediction": "configuration",
        "pred_doc_category": "api_reference",
    }

    assert frozen_binary_prediction(row) is False

    assert (
        frozen_category_prediction(row)
        == "configuration"
    )


def test_historical_sampling_fields_remain_supported():
    row = {
        "case_id": "old",
        "pred_docs_update_required": True,
        "pred_doc_category": "developer_setup",
    }

    assert frozen_binary_prediction(row) is True

    assert (
        frozen_category_prediction(row)
        == "developer_setup"
    )


def test_primary_sampling_uses_frozen_binary_prediction():
    rows = [
        {
            "case_id": "positive",
            "frozen_binary_prediction": True,
            "frozen_category_prediction":
                "configuration",
        },
        {
            "case_id": "negative",
            "frozen_binary_prediction": False,
            "pred_docs_update_required": True,
            "frozen_category_prediction":
                "api_reference",
        },
    ]

    sample = sample_primary(
        rows,
        seed=42,
        target_size=100,
    )

    assert [
        row["case_id"]
        for row in sample
    ] == ["positive"]


def test_stress_sampling_uses_frozen_category_prediction():
    rows = []

    for category in [
        "api_reference",
        "configuration",
        "developer_setup",
        "model_contract",
    ]:
        for index in range(3):
            rows.append(
                {
                    "case_id":
                        f"{category}-{index}",
                    "frozen_binary_prediction":
                        True,
                    "frozen_category_prediction":
                        category,
                    # Deliberately conflicting legacy field.
                    "pred_doc_category":
                        "wrong",
                }
            )

    sample = sample_stress(
        rows,
        seed=42,
        per_category=2,
    )

    assert len(sample) == 8

    counts = {
        category:
            sum(
                frozen_category_prediction(row)
                == category
                for row in sample
            )
        for category in [
            "api_reference",
            "configuration",
            "developer_setup",
            "model_contract",
        ]
    }

    assert counts == {
        "api_reference": 2,
        "configuration": 2,
        "developer_setup": 2,
        "model_contract": 2,
    }


def test_current_gate4_freeze_schema_is_accepted(
    tmp_path: Path,
):
    source = tmp_path / "source.py"
    source.write_text(
        "print('safe')\n",
        encoding="utf-8",
    )

    config = tmp_path / "config.json"

    config_payload = {
        "analysis_model": "model",
        "writer_model": "model",
        "repair_model": "model",
        "pipeline_version": "x",
        "temperature": 0.1,
        "top_k_documents": 3,
        "max_repair_attempts": 1,
        "max_input_tokens": 4096,
        "max_tokens_analysis": 512,
        "max_tokens_writer": 512,
        "max_tokens_repair": 512,
    }

    config.write_text(
        json.dumps(config_payload),
        encoding="utf-8",
    )

    freeze = tmp_path / "freeze.json"

    freeze.write_text(
        json.dumps(
            {
                "schema_version":
                    "gate4_stage3_freeze_v1",
                "gate": 4,
                "status": "PASS",
                "stage3_status": "FROZEN",
                "confirmation_accessed": False,
                "confirmation_sealed": True,
                "stage3_config": {
                    "sha256": sha(config),
                    "settings": config_payload,
                },
                "implementation_source_sha256": {
                    "source.py":
                        sha(source),
                },
            }
        ),
        encoding="utf-8",
    )

    result = validate_stage3_freeze(
        stage3_config=config,
        stage3_freeze_manifest=freeze,
        project_root=tmp_path,
    )

    assert (
        result["stage3_config_sha256"]
        == sha(config)
    )


def test_old_gate4_freeze_schema_is_rejected(
    tmp_path: Path,
):
    config = tmp_path / "config.json"

    config.write_text(
        "{}",
        encoding="utf-8",
    )

    freeze = tmp_path / "freeze.json"

    freeze.write_text(
        json.dumps(
            {
                "config_sha256":
                    sha(config),
                "source_file_sha256":
                    {},
                "confirmation_accessed":
                    False,
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="schema",
    ):
        validate_stage3_freeze(
            stage3_config=config,
            stage3_freeze_manifest=freeze,
            project_root=tmp_path,
        )


def test_no_context_positive_row_has_zero_llm_calls():
    row = {
        "case_id": "no-context",
        "repository": "org/repo",
        "language": "python",
        "code_changed_files": [
            "src/a.py"
        ],
        "code_diff_excerpt": "+x",
        "docs_before_excerpt": "",
    }

    result = run_stage3_for_positive_row(
        row=row,
        category="configuration",
        llm_backend=NoCallLLM(),
        config={
            "analysis_model": "x",
            "writer_model": "x",
            "repair_model": "x",
            "temperature": 0.1,
            "top_k_documents": 3,
            "max_repair_attempts": 1,
            "max_tokens_analysis": 512,
            "max_tokens_writer": 512,
            "max_tokens_repair": 512,
        },
    )

    assert (
        result["final_status"]
        == "retrieval_context_unavailable"
    )

    assert (
        result["llm_call_count"]
        == 0
    )

    assert (
        result["final_patch"]
        is None
    )


def test_reference_fields_do_not_enter_generation_payload():
    row = {
        "case_id": "safe",
        "repository": "org/repo",
        "language": "python",
        "code_changed_files": [
            "src/a.py"
        ],
        "code_diff_excerpt": "+x",
        "docs_before_excerpt": "",
        "docs_after_excerpt":
            "THIS MUST NOT ENTER",
        "gold_docs_update_required":
            True,
        "gold_doc_category":
            "configuration",
    }

    result = run_stage3_for_positive_row(
        row=row,
        category="configuration",
        llm_backend=NoCallLLM(),
        config={
            "analysis_model": "x",
            "writer_model": "x",
            "repair_model": "x",
            "temperature": 0.1,
            "top_k_documents": 3,
            "max_repair_attempts": 1,
            "max_tokens_analysis": 512,
            "max_tokens_writer": 512,
            "max_tokens_repair": 512,
        },
    )

    assert (
        result["final_status"]
        == "retrieval_context_unavailable"
    )
