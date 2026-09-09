from __future__ import annotations

from scripts.verify_gate4_stage3_freeze import verify


def test_gate4_stage3_freeze_verifier_passes() -> None:
    result = verify()

    assert result["status"] == "PASS"
    assert result["stage3_status"] == "FROZEN"
    assert result["confirmation_accessed"] is False
    assert result["confirmation_sealed"] is True
    assert result["current_gate"] >= 5

    if result["current_gate"] >= 6:
        assert result["gate5_status"] == "PASS"
    else:
        assert result["gate5_status"] == "NOT_EXECUTED"
    assert result["processed_rows"] == 200
    assert result["stage3_invocation_count"] == 91


def test_gate4_artifact_eol_portability_is_frozen_pass() -> None:
    result = verify()

    correction = result[
        "artifact_eol_portability_correction"
    ]

    assert correction["status"] == "PASS"
    assert correction["portable_artifact_count"] == 6
    assert correction["scientific_content_changed"] is False
    assert correction["confirmation_accessed"] is False
