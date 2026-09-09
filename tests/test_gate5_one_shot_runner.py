from __future__ import annotations

import json
from pathlib import Path

import pytest

import scripts.run_frozen_stage3_v2_confirmation as stage3_runner
import scripts.run_gate5_one_shot_qwen as gate5_runner
from docguard_llm_v2.hf_backend import (
    InputTokenBudgetExceeded,
)
from scripts.run_gate5_one_shot_qwen import (
    MASTER_RECEIPT,
    ensure_master_receipt_absent,
    require_execute_one_shot,
    validate_partition_manifest_preconfirmation,
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
    tmp_path: Path,
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

    # This test verifies the PRE-confirmation path specifically.
    # The real repository is now legitimately Gate 5 CLOSED,
    # so only the lifecycle-state check is simulated here.
    # The production execution guard itself remains strict.
    monkeypatch.setattr(
        gate5_runner,
        "validate_finalization_state",
        lambda root: {
            "current_gate": 5,
            "gate_statuses": {
                "gate_4_stage3_retrieval_generation_study_and_freeze":
                    "PASS",
                "gate_5_one_shot_confirmation":
                    "NOT_EXECUTED",
            },
            "confirmation_sealed":
                True,
            "confirmation_results_accessed_by_gate_5":
                False,
        },
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
            partition_manifest=
                root
                / "experiments/consolidated_enriched_training_v2/"
                  "gold/human_gold_manifest.json",
            output_root=
                tmp_path
                / "one_shot",
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


def test_classifier_runtime_canary_is_development_only():
    root = Path(
        __file__
    ).resolve().parents[1]

    canary = json.loads(
        (
            root
            / "reports/final_v2/gate5/"
              "GATE5_CLASSIFIER_RUNTIME_PORTABILITY_CANARY.json"
        ).read_text(
            encoding="utf-8"
        )
    )

    assert (
        canary[
            "confirmation_accessed"
        ]
        is False
    )

    assert (
        canary[
            "development_only"
        ]
        is True
    )

    assert (
        canary[
            "gate5_execution_started"
        ]
        is False
    )

    assert (
        canary[
            "source_runtime"
        ][
            "sklearn"
        ]
        == "1.8.0"
    )

    assert (
        canary[
            "target_execution_runtime"
        ]
        == {
            "python": "3.12.13",
            "sklearn": "1.8.0",
            "numpy": "2.4.0",
            "joblib": "1.5.3",
        }
    )


def test_partition_manifest_preflight_is_frozen_metadata() -> None:
    root = Path(
        __file__
    ).resolve().parents[1]

    result = (
        validate_partition_manifest_preconfirmation(
            root
            / "experiments/consolidated_enriched_training_v2/"
              "gold/human_gold_manifest.json"
        )
    )

    assert result["status"] == "PASS"

    assert (
        result[
            "confirmation_accessed"
        ]
        is False
    )

    assert (
        result[
            "confirmation_sealed"
        ]
        is True
    )

    assert (
        result[
            "manifest_mode"
        ]
        == "final_v2_gold_manifest"
    )

    assert (
        result[
            "sha256"
        ]
        ==
        "31745b74192f2711624b30297b5bf5fa210d0a28ef6b6221b26ca2a96272c81e"
    )

    assert (
        result[
            "bytes"
        ]
        == 7710
    )

    assert (
        result[
            "serialization_mode"
        ]
        in {
            "canonical_git_lf",
            "verified_windows_crlf_equivalent",
        }
    )

    assert (
        result[
            "canonical_lf_sha256"
        ]
        ==
        "31745b74192f2711624b30297b5bf5fa210d0a28ef6b6221b26ca2a96272c81e"
    )

    assert (
        result[
            "canonical_lf_bytes"
        ]
        == 7710
    )

    assert (
        result[
            "windows_crlf_equivalent_sha256"
        ]
        ==
        "88bc919675dac77e5ced805e121021dd6fbf43f5bf13b99babf2359625379b93"
    )

    assert (
        result[
            "windows_crlf_equivalent_bytes"
        ]
        == 7976
    )

    assert (
        result[
            "confirmation_rows"
        ]
        == 3747
    )

    assert (
        result[
            "confirmation_repositories"
        ]
        == 52
    )

    assert (
        result[
            "partition_row_counts"
        ]
        == {
            "development_train": 19018,
            "development_validation": 3148,
            "confirmation": 3747,
        }
    )

    assert (
        result[
            "partition_repository_counts"
        ]
        == {
            "development_train": 191,
            "development_validation": 41,
            "confirmation": 52,
        }
    )

    assert (
        result[
            "expected_confirmation_sha256"
        ]
        ==
        "e73caca3b9ef46de284c4755127e3d7cfc0b5db9f3d1c8cd2b85be80b2c6d01b"
    )

    assert (
        result[
            "repository_overlap_count"
        ]
        == 0
    )


def test_missing_partition_manifest_fails_before_confirmation(
    tmp_path: Path,
) -> None:

    with pytest.raises(
        RuntimeError,
        match="Missing frozen Final V2 gold manifest",
    ):
        validate_partition_manifest_preconfirmation(
            tmp_path
            / "repository_partition_manifest.json"
        )


def test_frozen_closed_state_forbids_new_one_shot_execution():
    root = Path(
        __file__
    ).resolve().parents[1]

    with pytest.raises(
        RuntimeError,
        match="not safe for one-shot execution",
    ):
        gate5_runner.validate_finalization_state(
            root
        )
