from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_extension_manifest_contributes_commands_and_view() -> None:
    manifest = json.loads((ROOT / "vscode-docguard" / "package.json").read_text(encoding="utf-8"))
    commands = {item["command"] for item in manifest["contributes"]["commands"]}
    assert "docguard.analyzeWorkspace" in commands
    assert "docguard.analyzeWorkspaceWithLlm" in commands
    assert "docguard.applyPatch" in commands
    assert "docguard.applyFallbackPatch" in commands
    assert "docguard.panel" in {item["id"] for item in manifest["contributes"]["views"]["docguard"]}
    activation_events = set(manifest["activationEvents"])
    assert "onCommand:docguard.applyPatch" in activation_events
    architecture = manifest["contributes"]["configuration"]["properties"]["docguard.classifierArchitecture"]
    assert architecture["default"] == "hybrid_router"
    assert "hybrid_router" in architecture["enum"]
    patch_backend = manifest["contributes"]["configuration"]["properties"]["docguard.patchBackend"]
    assert patch_backend["default"] == "deterministic"
    assert "llm-hf" in patch_backend["enum"]
    assert "llm-openai-compatible" in patch_backend["enum"]
    assert "llm-ollama" in patch_backend["enum"]
    analysis_backend = manifest["contributes"]["configuration"]["properties"]["docguard.analysisBackend"]
    assert analysis_backend["default"] == "hybrid"
    assert "llm-openai-compatible" in analysis_backend["enum"]
    assert manifest["contributes"]["configuration"]["properties"]["docguard.patchModel"]["default"] == "Qwen/Qwen2.5-1.5B-Instruct"
    assert manifest["contributes"]["configuration"]["properties"]["docguard.llmApiKeyEnvironmentVariable"]["default"] == "DOCGUARD_LLM_API_KEY"
    assert manifest["contributes"]["configuration"]["properties"]["docguard.runtimeTimeoutSeconds"]["default"] == 240
