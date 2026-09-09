from __future__ import annotations

from pathlib import Path

from scripts.verify_gate5_preregistration import (
    verify,
)


ROOT = Path(__file__).resolve().parents[1]


def test_gate5_preregistration_verifier_passes_post_confirmation():
    result = verify(
        ROOT
    )

    assert (
        result["status"]
        == "PASS"
    )

    assert (
        result[
            "lifecycle_state"
        ]
        == "POST_CONFIRMATION_FROZEN_CLOSED"
    )

    assert (
        result[
            "preflight_status"
        ]
        == "PREREGISTRATION_VERIFIED_POST_CONFIRMATION"
    )

    assert (
        result[
            "gate5_execution"
        ]
        == "COMPLETED_ONE_SHOT_CONFIRMATION"
    )

    assert (
        result[
            "current_gate"
        ]
        >= 6
    )

    assert (
        result[
            "confirmation_accessed_by_this_verifier"
        ]
        is False
    )

    assert (
        result[
            "confirmation_results_accessed_by_gate_5"
        ]
        is True
    )

    assert (
        result[
            "execution_artifacts_present"
        ]
        is True
    )

    assert (
        result[
            "confirmation_sealed"
        ]
        is True
    )

    assert (
        result[
            "bootstrap_replicates"
        ]
        == 2000
    )

    assert (
        result[
            "bootstrap_seed"
        ]
        == 42
    )


def test_gate5_preregistration_verifier_never_opens_confirmation(
    monkeypatch,
):
    original_open = Path.open

    def guarded_open(
        self,
        *args,
        **kwargs,
    ):
        normalized = str(
            self
        ).replace(
            "\\",
            "/",
        ).lower()

        if normalized.endswith(
            "/gold/confirmation.jsonl"
        ):
            raise AssertionError(
                "Gate 5 preregistration verifier "
                "attempted to open confirmation."
            )

        return original_open(
            self,
            *args,
            **kwargs,
        )

    monkeypatch.setattr(
        Path,
        "open",
        guarded_open,
    )

    result = verify(
        ROOT
    )

    assert (
        result[
            "confirmation_accessed_by_this_verifier"
        ]
        is False
    )


def test_gate5_preregistration_verifier_preserves_portability_evidence():
    result = verify(
        ROOT
    )

    assert (
        result[
            "gate3_eol_portability_correction"
        ]
        == "PASS"
    )

    assert (
        result[
            "gate3_child_manifest_link_portability"
        ]
        == "PASS"
    )

    assert (
        result[
            "gate4_artifact_eol_portability"
        ]
        == "PASS"
    )

    assert (
        result[
            "classifier_runtime_canary"
        ]
        == "REFERENCE_FROZEN_PRE_CONFIRMATION"
    )


def test_gate5_preregistration_verifier_is_post_confirmation_read_only():
    result = verify(
        ROOT
    )

    assert (
        result[
            "confirmation_results_accessed_by_gate_5"
        ]
        is True
    )

    assert (
        result[
            "confirmation_accessed_by_this_verifier"
        ]
        is False
    )

    assert (
        result[
            "gate5_execution"
        ]
        == "COMPLETED_ONE_SHOT_CONFIRMATION"
    )
