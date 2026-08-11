from __future__ import annotations


PATCH_DOC_CATEGORIES = {
    "api_reference",
    "model_contract",
    "configuration",
    "testing_instructions",
    "workflow_documentation",
    "architecture_flow",
    "developer_setup",
    "changelog",
}

PATCH_TARGET_FILES = {
    "docs/api.md",
    "docs/models.md",
    "docs/configuration.md",
    "docs/testing.md",
    "docs/workflows.md",
    "docs/architecture.md",
    "docs/developer-setup.md",
    "CHANGELOG.md",
}

DEFAULT_PATCH_MAX_NEW_TOKENS = 512
DEFAULT_PATCH_TEMPERATURE = 0.2
