from __future__ import annotations


SIGNALS = [
    "added_env_var", "removed_env_var", "config_default_change", "package_script_change",
    "local_seed_or_dev_flow", "route_added", "route_removed", "route_path_changed",
    "http_method_changed", "zod_validation_change", "request_field_change", "response_field_change",
    "dto_model_change", "middleware_error_change", "auth_middleware_change", "rate_limit_or_cache_change",
    "schedule_job_change", "service_orchestration_change", "test_command_change", "changelog_worthy_change",
    "docs_already_updated", "formatting_only", "comments_only", "test_only_no_behavior_change",
    "private_helper_refactor", "internal_variable_rename", "source_only_refactor",
]


def extract_signals(record: dict) -> dict[str, bool]:
    files = " ".join(record.get("changed_files", [])).lower()
    diff = record.get("code_diff", "")
    text = f"{files}\n{diff}".lower()
    added = "+" in diff
    removed = "-" in diff
    signals = {name: False for name in SIGNALS}
    signals["added_env_var"] = added and (".env" in files or "process.env" in text or "_flag" in text)
    signals["removed_env_var"] = removed and (".env" in files or "legacy" in text and "flag" in text)
    signals["config_default_change"] = "default_" in text or "default" in text and "config" in files
    signals["package_script_change"] = "package.json" in files and ("dev" in text or "seed" in text or "install" in text)
    signals["local_seed_or_dev_flow"] = "seed" in text or "npm run dev" in text or "local" in text
    signals["route_added"] = "router." in text and added and "post" in text
    signals["route_removed"] = "router." in text and removed and "legacy" in text
    signals["route_path_changed"] = "router." in text and "/reviews" in text and "/review" in text
    signals["http_method_changed"] = "router.patch" in text or ("router.post" in text and "router.patch" in text)
    signals["zod_validation_change"] = "z." in text or ".min(" in text or ".max(" in text or "z.enum" in text
    signals["request_field_change"] = "schema" in files and ("reason" in text or "field" in text)
    signals["response_field_change"] = "controller" in files and ("status" in text or "response" in text)
    signals["dto_model_change"] = "schema" in files or "dto" in text or "model" in text or "interface" in text
    signals["middleware_error_change"] = "middleware/error" in files or "review_error" in text
    signals["auth_middleware_change"] = "middleware/auth" in files or "requirereviewer" in text or "role" in text
    signals["rate_limit_or_cache_change"] = "ratelimit" in text or "cache" in text
    signals["schedule_job_change"] = "schedulejob" in text or "job" in files
    signals["service_orchestration_change"] = "reserve" in text or "notify" in text or "orchestration" in text
    signals["test_command_change"] = "package.json" in files and ("vitest" in text or "jest" in text or "test" in text)
    signals["changelog_worthy_change"] = "notifycustomers" in text or "user-facing" in text
    signals["docs_already_updated"] = "docs/" in files
    signals["formatting_only"] = "formatting" in text
    signals["comments_only"] = "comment" in text
    signals["test_only_no_behavior_change"] = "tests/" in files and not signals["test_command_change"]
    signals["private_helper_refactor"] = "helper" in text
    signals["internal_variable_rename"] = "renamedinternal" in text or "internalname" in text
    positive = any(signals[name] for name in SIGNALS[:20])
    negative = any(signals[name] for name in SIGNALS[20:])
    signals["source_only_refactor"] = negative and not positive
    return signals


def signal_names(signals: dict[str, bool]) -> list[str]:
    return [name for name, enabled in signals.items() if enabled]
