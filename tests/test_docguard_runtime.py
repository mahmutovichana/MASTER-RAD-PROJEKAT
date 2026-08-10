from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from docguard_runtime.patch_composer import compose_patch


ROOT = Path(__file__).resolve().parents[1]


def test_patch_composer_environment_variable() -> None:
    patch = compose_patch(
        ROOT / "examples" / "vscode_demo",
        "docs/configuration.md",
        "added_environment_variable",
        "configuration",
        "+REVIEW_WINDOW=7d",
        "Environment Variables",
    )
    assert patch["file"] == "docs/configuration.md"
    assert "REVIEW_WINDOW" in patch["preview"]


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

