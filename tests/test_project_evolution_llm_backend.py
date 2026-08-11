from __future__ import annotations

from pathlib import Path

from docguard_demo.run_project_evolution_flow import run


def test_project_evolution_legacy_backend(tmp_path: Path) -> None:
    result = run(tmp_path / "legacy", patch_backend="legacy")
    assert result["status"] == "ok"
    assert result["patch_backend"] == "legacy"
    assert (tmp_path / "legacy" / "docguard_project_evolution_predictions.jsonl").exists()


def test_project_evolution_llm_mock_backend(tmp_path: Path) -> None:
    result = run(tmp_path / "llm_mock", patch_backend="llm-mock")
    assert result["status"] == "ok"
    assert result["patch_backend"] == "llm-mock"
    assert (tmp_path / "llm_mock" / "docguard_llm_mock_patch_generation_report_2026_08.md").exists()
