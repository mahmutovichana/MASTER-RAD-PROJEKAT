from __future__ import annotations

from pathlib import Path

from scripts.verify_gate5_preregistration import (
    verify,
)


ROOT = Path(__file__).resolve().parents[1]


def test_gate5_preregistration_verifier_passes():
    result = verify(
        ROOT
    )

    assert (
        result["status"]
        == "PASS"
    )

    assert (
        result[
            "preflight_status"
        ]
        == "PREPARED_NOT_ACTIVATED"
    )

    assert (
        result[
            "gate5_execution"
        ]
        == "NOT_EXECUTED"
    )

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


def test_gate5_verifier_never_opens_confirmation(
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
            "\\\\",
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
            "confirmation_accessed"
        ]
        is False
    )


def test_gate5_verifier_reports_gate3_eol_portability_correction():
    result = verify(
        ROOT
    )

    assert (
        result[
            "gate3_eol_portability_correction"
        ]
        == "PASS"
    )
