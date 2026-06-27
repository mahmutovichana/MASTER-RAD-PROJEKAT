from __future__ import annotations

import re


DATASET_SCENARIOS = {
    "added_background_job_flow",
    "added_endpoint_error_response",
    "added_environment_variable",
    "added_request_field",
    "added_response_field",
    "added_service_orchestration_flow",
    "changed_auth_requirement",
    "changed_caching_or_rate_limit_flow",
    "changed_error_handling_flow",
    "changed_local_development_flow",
    "changed_pagination_default",
    "changed_rate_limit_policy",
    "changed_request_field_type",
    "changed_response_status_code",
    "changed_validation_max",
    "changed_validation_min",
    "comments_reworded_no_contract_change",
    "deprecated_endpoint",
    "dev_dependency_patch_no_command_change",
    "formatting_only_in_docs_or_code",
    "internal_performance_refactor_no_documented_behavior_change",
    "internal_refactor",
    "internal_variable_rename_no_behavior_change",
    "log_message_change_no_user_visible_behavior",
    "new_endpoint",
    "private_helper_refactor_no_flow_change",
    "removed_endpoint",
    "renamed_response_field",
    "test_assertion_refactor_no_behavior_change",
    "unknown_change",
}


DOC_CATEGORY_MAP = {
    "api": "api_reference",
    "api_change": "api_reference",
    "api_reference": "api_reference",
    "api_ref": "api_reference",
    "config": "configuration",
    "configuration": "configuration",
    "model": "model_contract",
    "models": "model_contract",
    "dto": "model_contract",
    "model_contract": "model_contract",
    "developer_setup": "developer_setup",
    "local_development": "developer_setup",
    "testing": "testing_instructions",
    "testing_instructions": "testing_instructions",
    "workflow": "workflow_documentation",
    "workflows": "workflow_documentation",
    "background_jobs": "workflow_documentation",
    "workflow_documentation": "workflow_documentation",
    "architecture": "architecture_flow",
    "architecture_flow": "architecture_flow",
    "changelog": "changelog",
}


TARGET_FILE_MAP = {
    "api": "docs/api.md",
    "api.md": "docs/api.md",
    "docs/api.md": "docs/api.md",
    "architecture": "docs/architecture.md",
    "docs/architecture.md": "docs/architecture.md",
    "models": "docs/models.md",
    "model": "docs/models.md",
    "docs/models.md": "docs/models.md",
    "configuration": "docs/configuration.md",
    "config": "docs/configuration.md",
    "docs/configuration.md": "docs/configuration.md",
    "workflow": "docs/workflows.md",
    "workflows": "docs/workflows.md",
    "docs/workflows.md": "docs/workflows.md",
    "testing": "docs/testing.md",
    "tests": "docs/testing.md",
    "docs/testing.md": "docs/testing.md",
    "readme": "README.md",
    "readme.md": "README.md",
    "developer_setup": "docs/developer-setup.md",
    "developer-setup": "docs/developer-setup.md",
    "docs/developer-setup.md": "docs/developer-setup.md",
}


def canonical_label(value: object) -> str:
    text = "" if value is None else str(value)
    text = text.strip().lower().replace("\\", "/")
    text = re.sub(r"[\s\-]+", "_", text)
    text = re.sub(r"[^a-z0-9_./]", "", text)
    return text


def normalize_doc_category(value: object) -> str:
    key = canonical_label(value)
    return DOC_CATEGORY_MAP.get(key, key)


def normalize_target_doc_file(value: object) -> str:
    raw = "" if value is None else str(value).strip()
    if raw in {"README.md", "CHANGELOG.md"}:
        return raw
    key = canonical_label(raw)
    return TARGET_FILE_MAP.get(key, key)


def normalize_target_section(value: object) -> str:
    return "" if value is None else str(value).strip()


def has_env_signal(record: dict) -> bool:
    text = " ".join(record.get("changed_files", [])) + " " + record.get("code_diff", "")
    lowered = text.lower()
    return ".env" in lowered or "config.ts" in lowered or "process.env" in lowered or "feature_flag" in lowered


def has_background_job_signal(record: dict) -> bool:
    text = (record.get("code_diff", "") + " " + " ".join(record.get("changed_files", []))).lower()
    return "schedulejob" in text or "worker" in text or "job" in text


def has_local_development_signal(record: dict) -> bool:
    text = (record.get("code_diff", "") + " " + record.get("target_section", "") + " " + record.get("docs_before_excerpt", "")).lower()
    return "local development" in text or "seed" in text or "dev command" in text or "tsx watch" in text


def normalize_scenario_type(value: object, record: dict | None = None) -> str:
    key = canonical_label(value)
    if key in DATASET_SCENARIOS:
        return key
    record = record or {}
    if key == "configuration" and has_env_signal(record):
        return "added_environment_variable"
    if key == "background_job" and has_background_job_signal(record):
        return "added_background_job_flow"
    if key == "local_development" and has_local_development_signal(record):
        return "changed_local_development_flow"
    if key in {"api_change", "integration", "configuration", "background_job", "local_development"}:
        return "unknown_change"
    return key or "unknown_change"


def add_normalized_fields(prediction: dict, record: dict | None = None) -> dict:
    row = dict(prediction)
    row.setdefault("raw_scenario_type", row.get("scenario_type", ""))
    row.setdefault("raw_doc_category", row.get("doc_category", ""))
    row.setdefault("raw_target_doc_file", row.get("target_doc_file", ""))
    row.setdefault("raw_target_section", row.get("target_section", ""))
    row["normalized_scenario_type"] = normalize_scenario_type(row.get("scenario_type"), record)
    row["normalized_doc_category"] = normalize_doc_category(row.get("doc_category"))
    row["normalized_target_doc_file"] = normalize_target_doc_file(row.get("target_doc_file"))
    row["normalized_target_section"] = normalize_target_section(row.get("target_section"))
    return row
