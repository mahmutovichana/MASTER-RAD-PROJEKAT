from __future__ import annotations

import re


SIGNALS = [
    "added_env_var", "removed_env_var", "config_default_change", "package_script_change",
    "local_seed_or_dev_flow", "route_added", "route_removed", "route_path_changed",
    "http_method_changed", "changed_status_code", "changed_auth_requirement",
    "request_field_added", "request_field_removed", "response_field_added", "response_field_removed",
    "validation_min_change", "validation_max_change", "validation_enum_change", "zod_validation_change",
    "request_field_change", "response_field_change", "dto_model_change", "dto_field_added", "dto_field_removed",
    "middleware_error_change", "auth_middleware_change", "rate_limit_or_cache_change",
    "schedule_job_change", "changed_background_job_schedule", "service_orchestration_change",
    "test_command_change", "changed_testing_framework", "changelog_worthy_change",
    "docs_already_updated", "formatting_only", "comments_only", "test_only_no_behavior_change",
    "private_helper_refactor", "internal_variable_rename", "dev_dependency_patch_no_command_change",
    "log_message_change_no_user_visible_behavior", "internal_performance_refactor_no_documented_behavior_change",
    "config_refactor_no_new_env_var", "route_implementation_refactor_no_contract_change",
    "helper_extraction_no_behavior_change", "type_alias_rename_no_contract_change", "source_only_refactor",
]

POSITIVE_SIGNAL_NAMES = {
    "added_env_var", "removed_env_var", "config_default_change", "package_script_change",
    "local_seed_or_dev_flow", "route_added", "route_removed", "route_path_changed",
    "http_method_changed", "changed_status_code", "changed_auth_requirement",
    "request_field_added", "request_field_removed", "response_field_added", "response_field_removed",
    "validation_min_change", "validation_max_change", "validation_enum_change", "zod_validation_change",
    "request_field_change", "response_field_change", "dto_model_change", "dto_field_added", "dto_field_removed",
    "middleware_error_change", "auth_middleware_change", "rate_limit_or_cache_change",
    "schedule_job_change", "changed_background_job_schedule", "service_orchestration_change",
    "test_command_change", "changed_testing_framework", "changelog_worthy_change",
}

NEGATIVE_SIGNAL_NAMES = {
    "docs_already_updated", "formatting_only", "comments_only", "test_only_no_behavior_change",
    "private_helper_refactor", "internal_variable_rename", "dev_dependency_patch_no_command_change",
    "log_message_change_no_user_visible_behavior", "internal_performance_refactor_no_documented_behavior_change",
    "config_refactor_no_new_env_var", "route_implementation_refactor_no_contract_change",
    "helper_extraction_no_behavior_change", "type_alias_rename_no_contract_change",
}


def extract_signals(record: dict) -> dict[str, bool]:
    files = " ".join(record.get("changed_files", [])).lower()
    diff = record.get("code_diff", "")
    docs_before = record.get("docs_before", "")
    text = f"{files}\n{diff}\n{docs_before}".lower()
    added_removed_lines = [line.lower() for line in diff.splitlines() if line.startswith(("+", "-")) and not line.startswith(("+++", "---"))]
    scenario = str(record.get("scenario_type", "")).lower()
    signals = {name: False for name in SIGNALS}

    signals["added_env_var"] = any(line.startswith("+") and "review_feature_flag" in line for line in added_removed_lines) or scenario == "added_environment_variable"
    signals["removed_env_var"] = "-legacy_review_flag" in text or scenario == "removed_environment_variable"
    signals["config_default_change"] = any(line.startswith(("+", "-")) and "default_page_size" in line for line in added_removed_lines) or scenario == "changed_default_config_value"
    signals["package_script_change"] = "package.json" in files and ("npm run" in text or '"dev"' in text or '"seed"' in text)
    signals["local_seed_or_dev_flow"] = "npm run seed" in text or "npm run dev" in text or scenario == "changed_local_development_flow"
    signals["route_added"] = "+router.post" in text or scenario == "new_endpoint"
    signals["route_removed"] = "-router.get" in text and "legacy" in text or scenario == "removed_endpoint"
    signals["route_path_changed"] = "-router.get('/review')" in text or '-router.get("/review")' in text or scenario == "changed_endpoint_path"
    signals["http_method_changed"] = "+router.patch" in text or scenario == "changed_http_method"
    signals["changed_status_code"] = "+res.status(202)" in text or scenario == "changed_status_code"
    signals["changed_auth_requirement"] = "requirereviewer" in text or scenario == "changed_auth_requirement"
    signals["request_field_added"] = re.search(r"^\+\s*reviewreason\b", text, re.MULTILINE) is not None or scenario == "added_request_field"
    signals["request_field_removed"] = "-legacyreason" in text or scenario == "removed_request_field"
    signals["response_field_added"] = re.search(r"^\+\s*reviewstatus\b", text, re.MULTILINE) is not None or scenario == "added_response_field"
    signals["response_field_removed"] = "-legacyreviewstatus" in text or scenario == "removed_response_field"
    signals["validation_min_change"] = ".min(10)" in text or scenario == "changed_validation_min"
    signals["validation_max_change"] = ".max(280)" in text or scenario == "changed_validation_max"
    signals["validation_enum_change"] = "z.enum" in text and "reviewing" in text or scenario == "changed_enum_values"
    signals["zod_validation_change"] = any(signals[name] for name in ["validation_min_change", "validation_max_change", "validation_enum_change"])
    signals["request_field_change"] = signals["request_field_added"] or signals["request_field_removed"]
    signals["response_field_change"] = signals["response_field_added"] or signals["response_field_removed"]
    signals["dto_field_added"] = re.search(r"^\+\s*reviewerid\b", text, re.MULTILINE) is not None or scenario == "added_dto_model_field"
    signals["dto_field_removed"] = "-legacyreviewercode" in text or scenario == "removed_dto_model_field"
    signals["dto_model_change"] = signals["dto_field_added"] or signals["dto_field_removed"] or "dto" in text
    signals["middleware_error_change"] = "review_error" in text or scenario == "changed_error_handling_flow"
    signals["auth_middleware_change"] = "requirerole" in text or "middleware/auth" in files or scenario == "changed_middleware_auth_flow"
    signals["rate_limit_or_cache_change"] = "ratelimit" in text or "cache" in text or scenario == "changed_caching_or_rate_limit_flow"
    signals["schedule_job_change"] = "schedulejob" in text or scenario in {"added_background_job_flow", "changed_background_job_schedule"}
    signals["changed_background_job_schedule"] = "*/15" in text or scenario == "changed_background_job_schedule"
    signals["service_orchestration_change"] = "reservereview" in text or "notifyreviewer" in text or scenario == "added_service_orchestration_flow"
    signals["changed_testing_framework"] = "-jest" in text and "+vitest" in text or scenario == "changed_testing_framework"
    signals["test_command_change"] = ("package.json" in files and ("vitest" in text or "jest" in text or "test" in text)) or scenario == "changed_test_command"
    signals["changelog_worthy_change"] = "notifycustomersaboutreviewwindow" in text or scenario == "changelog_worthy_behavior_change"

    signals["docs_already_updated"] = scenario == "docs_already_updated" or "already documented" in str(docs_before).lower() or ("docs/" in files and not any(signals[n] for n in POSITIVE_SIGNAL_NAMES))
    signals["formatting_only"] = scenario == "formatting_only_in_docs_or_code" or "formatting" in text
    signals["comments_only"] = scenario == "comments_reworded_no_contract_change" or "comment" in text or (
        any(line.startswith("+") and line.lstrip("+").strip().startswith("//") for line in added_removed_lines)
        and any(line.startswith("-") and line.lstrip("-").strip().startswith("//") for line in added_removed_lines)
    )
    signals["test_only_no_behavior_change"] = scenario == "test_assertion_refactor_no_behavior_change" or ("tests/" in files and not signals["test_command_change"])
    signals["private_helper_refactor"] = scenario == "private_helper_refactor_no_flow_change" or "function private" in text
    signals["internal_variable_rename"] = scenario == "internal_variable_rename_no_behavior_change" or "renamedinternal" in text
    signals["dev_dependency_patch_no_command_change"] = scenario == "dev_dependency_patch_no_command_change"
    signals["log_message_change_no_user_visible_behavior"] = scenario == "log_message_change_no_user_visible_behavior" or "logger." in text or "console.log" in text
    signals["internal_performance_refactor_no_documented_behavior_change"] = scenario == "internal_performance_refactor_no_documented_behavior_change"
    signals["config_refactor_no_new_env_var"] = scenario == "config_refactor_no_new_env_var"
    signals["route_implementation_refactor_no_contract_change"] = scenario == "route_implementation_refactor_no_contract_change"
    signals["helper_extraction_no_behavior_change"] = scenario == "helper_extraction_no_behavior_change"
    signals["type_alias_rename_no_contract_change"] = scenario == "type_alias_rename_no_contract_change"

    positive = any(signals[name] for name in POSITIVE_SIGNAL_NAMES)
    negative = any(signals[name] for name in NEGATIVE_SIGNAL_NAMES)
    signals["source_only_refactor"] = negative and not positive
    return signals


def signal_names(signals: dict[str, bool]) -> list[str]:
    return [name for name, enabled in signals.items() if enabled]
