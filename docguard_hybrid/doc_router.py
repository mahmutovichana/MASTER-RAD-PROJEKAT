from __future__ import annotations

from docguard_hybrid.signal_extractor import extract_signals, signal_names


DOC_FILES = {
    "api_reference": "docs/api.md",
    "architecture_flow": "docs/architecture.md",
    "model_contract": "docs/models.md",
    "developer_setup": "docs/developer-setup.md",
    "testing_instructions": "docs/testing.md",
    "configuration": "docs/configuration.md",
    "workflow_documentation": "docs/workflows.md",
    "changelog": "CHANGELOG.md",
    "no_update": "",
}


def route(record: dict) -> dict:
    signals = extract_signals(record)
    names = signal_names(signals)
    negative = any(signals[name] for name in [
        "docs_already_updated", "formatting_only", "comments_only", "test_only_no_behavior_change",
        "private_helper_refactor", "internal_variable_rename", "source_only_refactor",
    ])
    if negative and not any(signals[name] for name in [
        "added_env_var", "removed_env_var", "config_default_change", "package_script_change", "local_seed_or_dev_flow",
        "route_added", "route_removed", "route_path_changed", "http_method_changed", "zod_validation_change",
        "request_field_change", "response_field_change", "dto_model_change", "middleware_error_change",
        "auth_middleware_change", "rate_limit_or_cache_change", "schedule_job_change",
        "service_orchestration_change", "test_command_change", "changelog_worthy_change",
    ]):
        return {
            "docs_update_required": False,
            "candidate_doc_categories": ["no_update"],
            "candidate_target_doc_files": [],
            "candidate_scenario_types": ["unknown_change"],
            "router_confidence": 0.92,
            "router_reason": f"No documented behavior change signals: {', '.join(names)}",
            "signals": names,
        }
    if signals["added_env_var"] or signals["removed_env_var"] or signals["config_default_change"]:
        category, scenario = "configuration", "added_environment_variable"
    elif signals["package_script_change"] or signals["local_seed_or_dev_flow"]:
        category, scenario = "developer_setup", "changed_local_development_flow"
    elif signals["schedule_job_change"] or signals["service_orchestration_change"]:
        category, scenario = "workflow_documentation", "added_background_job_flow" if signals["schedule_job_change"] else "added_service_orchestration_flow"
    elif signals["middleware_error_change"] or signals["auth_middleware_change"] or signals["rate_limit_or_cache_change"]:
        category, scenario = "architecture_flow", "changed_error_handling_flow"
    elif signals["dto_model_change"] and not (signals["zod_validation_change"] or signals["request_field_change"]):
        category, scenario = "model_contract", "added_dto_model_field"
    elif signals["test_command_change"]:
        category, scenario = "testing_instructions", "changed_test_command"
    elif signals["changelog_worthy_change"]:
        category, scenario = "changelog", "changelog_worthy_behavior_change"
    else:
        category, scenario = "api_reference", "new_endpoint"
    return {
        "docs_update_required": True,
        "candidate_doc_categories": [category],
        "candidate_target_doc_files": [DOC_FILES[category]],
        "candidate_scenario_types": [scenario],
        "router_confidence": 0.82,
        "router_reason": f"Matched signals: {', '.join(names) or 'api-like change'}",
        "signals": names,
    }
