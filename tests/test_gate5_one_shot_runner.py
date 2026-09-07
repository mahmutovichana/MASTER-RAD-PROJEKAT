from __future__ import annotations

import json
from pathlib import Path

import pytest

import scripts.run_frozen_stage3_v2_confirmation as stage3_runner
from docguard_llm_v2.hf_backend import (
    InputTokenBudgetExceeded,
)
from scripts.run_gate5_one_shot_qwen import (
    MASTER_RECEIPT,
    ensure_master_receipt_absent,
    require_execute_one_shot,
    validate_preconfirmation_frozen_state,
)


def test_execute_one_shot_flag_is_required():
    with pytest.raises(
        RuntimeError,
        match="explicit --execute-one-shot",
    ):
        require_execute_one_shot(
            False
        )

    require_execute_one_shot(
        True
    )


def test_existing_master_receipt_forbids_rerun(
    tmp_path: Path,
):
    output = tmp_path / "one_shot"

    output.mkdir()

    (
        output
        / MASTER_RECEIPT
    ).write_text(
        "{}",
        encoding="utf-8",
    )

    with pytest.raises(
        RuntimeError,
        match="rerun is forbidden",
    ):
        ensure_master_receipt_absent(
            output
        )


def test_preconfirmation_validation_does_not_read_confirmation(
    monkeypatch,
):
    original = Path.read_text

    def guarded_read_text(
        self,
        *args,
        **kwargs,
    ):
        if self.name == "confirmation.jsonl":
            raise AssertionError(
                "Preflight attempted to read confirmation."
            )

        return original(
            self,
            *args,
            **kwargs,
        )

    monkeypatch.setattr(
        Path,
        "read_text",
        guarded_read_text,
    )

    root = Path(__file__).resolve().parents[1]

    result = (
        validate_preconfirmation_frozen_state(
            root=
                root,
            preregistration=
                root
                / "reports/final_v2/gate5/"
                  "GATE5_PREREGISTRATION.json",
            binary_model=
                root
                / "models/final_v2/gate3/"
                  "binary_m1_gate3.joblib",
            binary_freeze=
                root
                / "reports/final_v2/gate3/"
                  "binary_classifier_freeze_manifest.json",
            category_model=
                root
                / "models/final_v2/gate3/"
                  "category_m1_gate3.joblib",
            category_freeze=
                root
                / "reports/final_v2/gate3/"
                  "category_classifier_freeze_manifest.json",
            stage3_config=
                root
                / "configs/"
                  "stage3_semantic_generation_v2.json",
            stage3_freeze=
                root
                / "reports/final_v2/gate4/"
                  "GATE4_STAGE3_FREEZE_MANIFEST.json",
            output_root=
                root
                / "reports/final_v2/gate5/"
                  "one_shot",
        )
    )

    assert (
        result["gate3"]["status"]
        == "PASS"
    )

    assert (
        result["gate4"]["status"]
        == "PASS"
    )


def test_input_budget_failure_is_fail_closed(
    monkeypatch,
):
    class Backend:
        call_count = 0

    def fail_generation(
        **kwargs,
    ):
        raise InputTokenBudgetExceeded(
            input_tokens=5000,
            max_input_tokens=4096,
            purpose="analysis",
        )

    monkeypatch.setattr(
        stage3_runner,
        "generate_semantic_documentation_patch",
        fail_generation,
    )

    row = {
        "case_id":
            "synthetic-budget",
        "repository":
            "org/repo",
        "language":
            "python",
        "code_changed_files":
            ["src/a.py"],
        "code_diff_excerpt":
            "+x",
        "docs_before_excerpt":
            "Existing docs",
        "documentation_context_candidates": [
            {
                "path":
                    "docs/a.md",
                "excerpt":
                    "Existing docs",
                "source_ref":
                    "base",
            }
        ],
    }

    result = (
        stage3_runner.run_stage3_for_positive_row(
            row=
                row,
            category=
                "configuration",
            llm_backend=
                Backend(),
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
    )

    assert (
        result["final_status"]
        == "human_review_required"
    )

    assert (
        result["final_patch"]
        is None
    )

    assert (
        result["execution_error"]["code"]
        == "input_token_budget_exceeded"
    )

    assert (
        result["llm_call_count"]
        == 0
    )
