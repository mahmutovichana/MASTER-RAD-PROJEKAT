from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_extension_manifest_contributes_commands_and_view() -> None:
    manifest = json.loads((ROOT / "vscode-docguard" / "package.json").read_text(encoding="utf-8"))
    commands = {item["command"] for item in manifest["contributes"]["commands"]}
    assert "docguard.analyzeWorkspace" in commands
    assert "docguard.applyPatch" in commands
    assert "docguard.panel" in {item["id"] for item in manifest["contributes"]["views"]["docguard"]}

