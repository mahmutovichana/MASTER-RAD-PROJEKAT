from __future__ import annotations

from scripts.verify_gate4_stage3_freeze import verify


def test_gate4_stage3_freeze_verifier_passes() -> None:
    result = verify()

    assert result["status"] == "PASS"
    assert result["stage3_status"] == "FROZEN"
    assert result["confirmation_accessed"] is False
    assert result["confirmation_sealed"] is True
    assert result["current_gate"] == 5
    assert result["gate5_status"] == "NOT_EXECUTED"
    assert result["processed_rows"] == 200
    assert result["stage3_invocation_count"] == 91
