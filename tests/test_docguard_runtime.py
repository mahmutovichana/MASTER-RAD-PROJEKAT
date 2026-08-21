from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from docguard_runtime.patch_composer import apply_patch
from docguard_runtime.patch_composer import compose_patch
from docguard_runtime.workspace_analyzer import analyze_workspace


ROOT = Path(__file__).resolve().parents[1]


def test_patch_composer_environment_variable() -> None:
    workspace = ROOT / "generated_live_demo_projects"
    patch = compose_patch(
        workspace,
        "docs/configuration.md",
        "added_environment_variable",
        "configuration",
        "+  reviewWindow: process.env.REVIEW_WINDOW || '7d',",
        "Environment Variables",
    )
    assert patch["file"] == "docs/configuration.md"
    assert "REVIEW_WINDOW" in patch["preview"]
    assert "sets the review window" in patch["preview"]
    assert "defaults to `7d`" in patch["preview"]


def test_patch_composer_ignores_unchanged_env_line_with_added_comma() -> None:
    patch = compose_patch(
        ROOT / "generated_live_demo_projects",
        "docs/configuration.md",
        "added_environment_variable",
        "configuration",
        (
            "-  reviewMode: process.env.REVIEW_MODE || 'standard'\n"
            "+  reviewMode: process.env.REVIEW_MODE || 'standard',\n"
            "+  reviewWindow: process.env.REVIEW_WINDOW || '4d'\n"
        ),
        "Environment Variables",
    )

    assert "REVIEW_WINDOW" in patch["preview"]
    assert "defaults to `4d`" in patch["preview"]
    assert "REVIEW_MODE" not in patch["preview"]


def test_runtime_cli_returns_json() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "docguard_runtime.runtime_cli",
            "analyze-workspace",
            "--workspace",
            str(ROOT / "examples" / "vscode_demo"),
            "--format",
            "json",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=30,
    )
    payload = json.loads(result.stdout)
    assert payload["status"] in {"ok", "error"}
    assert "docs_update_required" in payload


def test_workspace_analysis_stops_after_patch_documents_env_var(tmp_path: Path) -> None:
    workspace = tmp_path / "demo"
    (workspace / "src").mkdir(parents=True)
    (workspace / "docs").mkdir()
    (workspace / "src" / "config.ts").write_text(
        "export const env = {\n"
        "  port: Number(process.env.PORT || 3000),\n"
        "};\n",
        encoding="utf-8",
    )
    (workspace / "docs" / "configuration.md").write_text(
        "# Configuration\n\n"
        "## Environment Variables\n\n"
        "- `PORT` controls the HTTP port.\n",
        encoding="utf-8",
    )
    subprocess.run(["git", "init"], cwd=workspace, check=True, capture_output=True, text=True)
    subprocess.run(["git", "add", "."], cwd=workspace, check=True, capture_output=True, text=True)
    subprocess.run(
        ["git", "-c", "user.email=docguard@example.test", "-c", "user.name=DocGuard", "commit", "-m", "baseline"],
        cwd=workspace,
        check=True,
        capture_output=True,
        text=True,
    )
    (workspace / "src" / "config.ts").write_text(
        "export const env = {\n"
        "  port: Number(process.env.PORT || 3000),\n"
        "  reviewWindow: process.env.REVIEW_WINDOW || '7d',\n"
        "};\n",
        encoding="utf-8",
    )

    first = analyze_workspace(workspace)
    assert first["docs_update_required"] is True
    assert first["target_doc_file"] == "docs/configuration.md"
    assert first["patch"]
    assert "REVIEW_WINDOW" in first["patch"]["preview"]
    assert "sets the review window" in first["patch"]["preview"]
    assert "defaults to `7d`" in first["patch"]["preview"]
    assert "REVIEW_MODE" not in first["patch"]["preview"]

    apply_patch(workspace, first["patch"])
    second = analyze_workspace(workspace)
    assert second["docs_update_required"] is False
    assert second["scenario_type"] == "docs_already_updated"


def test_workspace_analysis_can_use_llm_patch_backend_mock(tmp_path: Path) -> None:
    workspace = tmp_path / "demo"
    (workspace / "src").mkdir(parents=True)
    (workspace / "docs").mkdir()
    (workspace / "src" / "config.ts").write_text(
        "export const env = {\n"
        "  port: Number(process.env.PORT || 3000),\n"
        "};\n",
        encoding="utf-8",
    )
    (workspace / "docs" / "configuration.md").write_text(
        "# Configuration\n\n"
        "## Environment Variables\n\n"
        "- `PORT` controls the HTTP port.\n",
        encoding="utf-8",
    )
    subprocess.run(["git", "init"], cwd=workspace, check=True, capture_output=True, text=True)
    subprocess.run(["git", "add", "."], cwd=workspace, check=True, capture_output=True, text=True)
    subprocess.run(
        ["git", "-c", "user.email=docguard@example.test", "-c", "user.name=DocGuard", "commit", "-m", "baseline"],
        cwd=workspace,
        check=True,
        capture_output=True,
        text=True,
    )
    (workspace / "src" / "config.ts").write_text(
        "export const env = {\n"
        "  port: Number(process.env.PORT || 3000),\n"
        "  reviewWindow: process.env.REVIEW_WINDOW || '7d',\n"
        "};\n",
        encoding="utf-8",
    )

    result = analyze_workspace(workspace, patch_backend="llm-mock")

    assert result["docs_update_required"] is True
    assert result["diagnostics"]["patch_backend"] == "llm-mock"
    assert result["patch"]["backend"] == "llm-mock"
    assert result["patch"]["generation_status"] == "ok"
    assert result["patch"]["verifier_status"] in {"pass", "warn", "fail"}
    assert result["patch"]["preview"]
