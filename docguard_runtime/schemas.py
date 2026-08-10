from __future__ import annotations

from typing import Any


DOC_FILES = {
    "configuration": "docs/configuration.md",
    "api_reference": "docs/api.md",
    "developer_setup": "docs/developer-setup.md",
    "workflow_documentation": "docs/workflows.md",
    "architecture_flow": "docs/architecture.md",
    "model_contract": "docs/models.md",
    "testing_instructions": "docs/testing.md",
    "changelog": "CHANGELOG.md",
}

SECTIONS = {
    "docs/configuration.md": "Environment Variables",
    "docs/api.md": "API Reference",
    "docs/developer-setup.md": "Local Development",
    "docs/workflows.md": "Workflows",
    "docs/architecture.md": "Architecture",
    "docs/models.md": "Data Models",
    "docs/testing.md": "Testing",
    "CHANGELOG.md": "Unreleased",
}


def ok_response(
    docs_update_required: bool,
    doc_category: str,
    target_doc_file: str | None,
    scenario_type: str,
    confidence: float,
    reason: str,
    patch: dict[str, Any] | None,
    diagnostics: dict[str, Any],
    target_section: str | None = None,
) -> dict[str, Any]:
    target = target_doc_file or None
    return {
        "status": "ok",
        "docs_update_required": docs_update_required,
        "doc_category": doc_category,
        "target_doc_file": target,
        "target_section": target_section or (SECTIONS.get(target or "", "Documentation")),
        "scenario_type": scenario_type,
        "confidence": confidence,
        "reason": reason,
        "patch": patch,
        "diagnostics": diagnostics,
        "error_message": None,
    }


def error_response(message: str, diagnostics: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "status": "error",
        "docs_update_required": False,
        "doc_category": "no_update",
        "target_doc_file": None,
        "target_section": "Documentation",
        "scenario_type": "runtime_error",
        "confidence": 0.0,
        "reason": "DocGuard runtime failed.",
        "patch": None,
        "diagnostics": diagnostics or {},
        "error_message": message,
    }

