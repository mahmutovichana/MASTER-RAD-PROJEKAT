from __future__ import annotations

import json
from pathlib import Path

import docguard_demo.run_project_evolution_flow as project_evolution_flow
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


def test_project_evolution_case_limit(tmp_path: Path) -> None:
    result = run(tmp_path / "limited", patch_backend="legacy", case_limit=2)
    assert result["status"] == "ok"
    assert result["total_cases"] == 2


def test_project_evolution_hf_backend_records_dependency_error(tmp_path: Path, monkeypatch) -> None:
    def fake_generate(*_args, **_kwargs):
        return {
            "patch_text": "",
            "backend": "hf",
            "model_name": "fake/model",
            "generation_status": "error",
            "error_message": "backend='hf' requires optional dependencies: torch and transformers.",
            "latency_seconds": 0.0,
        }

    monkeypatch.setattr(project_evolution_flow, "generate_documentation_patch", fake_generate)
    out = tmp_path / "hf"
    result = run(out, patch_backend="llm-hf", patch_model="fake/model", case_limit=1)
    assert result["status"] == "ok"
    assert result["patch_backend"] == "llm-hf"
    row = json.loads((out / "docguard_project_evolution_predictions.jsonl").read_text(encoding="utf-8").splitlines()[0])
    assert row["llm_generation_status"] == "error"
    assert "optional dependencies" in row["llm_error_message"]
