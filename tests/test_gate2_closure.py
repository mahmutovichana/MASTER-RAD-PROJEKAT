from __future__ import annotations

import io
import tarfile
from pathlib import Path

import pytest

from docguard_ml_v2.gate2_closure import choose_winner, repository_bootstrap, safe_archive_members


def _family(mean: float, std: float) -> dict:
    return {"primary_mean": mean, "primary_std": std, "primary_worst": mean - std, "primary_best": mean + std}


def test_winner_rule_uses_std_inside_tolerance_then_simplicity() -> None:
    decision = choose_winner({"M1": _family(.800, .03), "M2": _family(.804, .02), "M3": _family(.804, .02)})
    assert decision["selected_family"] == "M2"
    assert [row["inside_tolerance"] for row in decision["candidates"]] == [True, True, True]


def test_winner_rule_excludes_family_outside_tolerance() -> None:
    decision = choose_winner({"M1": _family(.800, .01), "M2": _family(.806, .10), "M3": _family(.790, .001)})
    assert decision["selected_family"] == "M2"


def test_return_archive_rejects_path_traversal(tmp_path: Path) -> None:
    archive = tmp_path / "unsafe.tar.gz"
    with tarfile.open(archive, "w:gz") as handle:
        content = b"bad"
        member = tarfile.TarInfo("../escape.json"); member.size = len(content)
        handle.addfile(member, io.BytesIO(content))
    with pytest.raises(RuntimeError, match="Unsafe"):
        safe_archive_members(archive)


def test_repository_bootstrap_is_deterministic() -> None:
    records = [
        {"repository": "a", "gold": 0, "prediction": 0}, {"repository": "a", "gold": 1, "prediction": 1},
        {"repository": "b", "gold": 0, "prediction": 1}, {"repository": "b", "gold": 1, "prediction": 1},
    ]
    families = {name: {"records": records} for name in ("M0", "M1", "M2", "M3")}
    first = repository_bootstrap("binary", families, replicates=50, seed=42)
    second = repository_bootstrap("binary", families, replicates=50, seed=42)
    assert first == second
    assert first["unit"] == "repository"


def test_gate2_closure_verifier_passes_without_confirmation_access() -> None:
    from scripts.verify_gate2_closure import verify
    result = verify()
    assert result["status"] == "PASS"
    assert result["confirmation_accessed"] is False
    assert result["gate3_status"] == "NOT_EXECUTED"
