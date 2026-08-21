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

NEGATIVE_SIGNAL_TO_SCENARIO = [
    ("internal_variable_rename", "internal_variable_rename_no_behavior_change"),
    ("private_helper_refactor", "private_helper_refactor_no_flow_change"),
    ("formatting_only", "formatting_only_in_docs_or_code"),
    ("comments_only", "comments_reworded_no_contract_change"),
    ("test_only_no_behavior_change", "test_assertion_refactor_no_behavior_change"),
    ("dev_dependency_patch_no_command_change", "dev_dependency_patch_no_command_change"),
    ("log_message_change_no_user_visible_behavior", "log_message_change_no_user_visible_behavior"),
    ("internal_performance_refactor_no_documented_behavior_change", "internal_performance_refactor_no_documented_behavior_change"),
    ("docs_already_updated", "docs_already_updated"),
    ("config_refactor_no_new_env_var", "config_refactor_no_new_env_var"),
    ("route_implementation_refactor_no_contract_change", "route_implementation_refactor_no_contract_change"),
    ("helper_extraction_no_behavior_change", "helper_extraction_no_behavior_change"),
    ("type_alias_rename_no_contract_change", "type_alias_rename_no_contract_change"),
]

POSITIVE_SIGNAL_TO_ROUTE = [
    ("config_default_change", "configuration", "changed_default_config_value"),
    ("added_env_var", "configuration", "added_environment_variable"),
    ("removed_env_var", "configuration", "removed_environment_variable"),
    ("local_seed_or_dev_flow", "developer_setup", "changed_local_development_flow"),
    ("package_script_change", "developer_setup", "changed_seed_or_setup_flow"),
    ("changed_background_job_schedule", "workflow_documentation", "changed_background_job_schedule"),
    ("schedule_job_change", "workflow_documentation", "added_background_job_flow"),
    ("service_orchestration_change", "workflow_documentation", "added_service_orchestration_flow"),
    ("middleware_error_change", "architecture_flow", "changed_error_handling_flow"),
    ("rate_limit_or_cache_change", "architecture_flow", "changed_caching_or_rate_limit_flow"),
    ("auth_middleware_change", "architecture_flow", "changed_middleware_auth_flow"),
    ("dto_field_added", "model_contract", "added_dto_model_field"),
    ("dto_field_removed", "model_contract", "removed_dto_model_field"),
    ("changed_testing_framework", "testing_instructions", "changed_testing_framework"),
    ("test_command_change", "testing_instructions", "changed_test_command"),
    ("changelog_worthy_change", "changelog", "changelog_worthy_behavior_change"),
    ("route_removed", "api_reference", "removed_endpoint"),
    ("route_path_changed", "api_reference", "changed_endpoint_path"),
    ("http_method_changed", "api_reference", "changed_http_method"),
    ("route_added", "api_reference", "new_endpoint"),
    ("changed_status_code", "api_reference", "changed_status_code"),
    ("changed_auth_requirement", "api_reference", "changed_auth_requirement"),
    ("request_field_added", "api_reference", "added_request_field"),
    ("request_field_removed", "api_reference", "removed_request_field"),
    ("response_field_added", "api_reference", "added_response_field"),
    ("response_field_removed", "api_reference", "removed_response_field"),
    ("validation_min_change", "api_reference", "changed_validation_min"),
    ("validation_max_change", "api_reference", "changed_validation_max"),
    ("validation_enum_change", "api_reference", "changed_enum_values"),
]


def _no_update_result(signal: str, scenario: str, names: list[str]) -> dict:
    return {
        "docs_update_required": False,
        "candidate_doc_categories": ["no_update"],
        "candidate_target_doc_files": [],
        "candidate_scenario_types": [scenario],
        "router_confidence": 0.94,
        "router_reason": f"Matched no-update signal `{signal}` from: {', '.join(names)}",
        "signals": names,
    }


def route(record: dict) -> dict:
    signals = extract_signals(record)
    names = signal_names(signals)
    if signals.get("docs_already_updated"):
        return _no_update_result("docs_already_updated", "docs_already_updated", names)
    for signal, category, scenario in POSITIVE_SIGNAL_TO_ROUTE:
        if signals.get(signal):
            return {
                "docs_update_required": True,
                "candidate_doc_categories": [category],
                "candidate_target_doc_files": [DOC_FILES[category]],
                "candidate_scenario_types": [scenario],
                "router_confidence": 0.9,
                "router_reason": f"Matched positive signal `{signal}` from: {', '.join(names)}",
                "signals": names,
            }
    for signal, scenario in NEGATIVE_SIGNAL_TO_SCENARIO:
        if signals.get(signal):
            return _no_update_result(signal, scenario, names)
    return {
        "docs_update_required": False,
        "candidate_doc_categories": ["no_update"],
        "candidate_target_doc_files": [],
        "candidate_scenario_types": ["unknown_change"],
        "router_confidence": 0.55,
        "router_reason": f"No high-confidence documentation signal. Signals: {', '.join(names) or 'none'}",
        "signals": names,
    }
