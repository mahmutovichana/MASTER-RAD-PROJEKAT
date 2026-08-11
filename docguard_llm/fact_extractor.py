from __future__ import annotations

import re
from typing import Any


HTTP_METHODS = {"get", "post", "put", "patch", "delete"}


def _add_unique(items: list[str], value: str | None) -> None:
    if value and value not in items:
        items.append(value)


def _added_removed_lines(code_diff: str) -> list[str]:
    return [
        line
        for line in code_diff.splitlines()
        if line.startswith(("+", "-")) and not line.startswith(("+++", "---"))
    ]


def _extract_object_fields(fragment: str) -> list[str]:
    fields: list[str] = []
    for match in re.finditer(r"([A-Za-z_][A-Za-z0-9_]*)\s*:", fragment):
        _add_unique(fields, match.group(1))
    return fields


def _extract_interface_fields(code_diff: str) -> tuple[list[str], list[str]]:
    fields: list[str] = []
    types: list[str] = []
    for line in _added_removed_lines(code_diff):
        if not line.startswith("+"):
            continue
        match = re.search(r"\+\s*([A-Za-z_][A-Za-z0-9_]*)\??\s*:\s*([A-Za-z_][A-Za-z0-9_<>\[\]| ]*)", line)
        if match:
            _add_unique(fields, match.group(1))
            _add_unique(types, match.group(2).strip())
    return fields, types


def extract_allowed_facts(
    code_diff: str,
    docs_before: str | None = None,
    category: str | None = None,
    scenario: str | None = None,
) -> dict[str, Any]:
    text = f"{code_diff}\n{docs_before or ''}"
    allowed_tokens: list[str] = []
    allowed_facts: dict[str, Any] = {
        "http_methods": [],
        "route_paths": [],
        "status_codes": [],
        "response_fields": [],
        "request_fields": [],
        "auth_roles": [],
        "validation_min_values": [],
        "validation_max_values": [],
        "interface_or_class_names": [],
        "added_fields": [],
        "field_types": [],
        "env_vars": [],
        "config_variables": [],
        "default_values": [],
        "test_commands": [],
        "frameworks": [],
        "cron_expressions": [],
        "job_or_function_names": [],
        "rate_limit_values": [],
        "middleware_names": [],
        "behavior_tokens": [],
    }

    for method, route in re.findall(r"router\.(get|post|put|patch|delete)\(['\"]([^'\"]+)['\"]", code_diff, flags=re.IGNORECASE):
        method_upper = method.upper()
        _add_unique(allowed_facts["http_methods"], method_upper)
        _add_unique(allowed_tokens, method_upper)
        _add_unique(allowed_facts["route_paths"], route)
        _add_unique(allowed_tokens, route)

    for status in re.findall(r"res\.status\((\d{3})\)", code_diff):
        _add_unique(allowed_facts["status_codes"], status)
        _add_unique(allowed_tokens, status)

    for json_match in re.finditer(r"\.json\(\s*\{([^}]*)\}", code_diff, flags=re.DOTALL):
        for field in _extract_object_fields(json_match.group(1)):
            _add_unique(allowed_facts["response_fields"], field)
            _add_unique(allowed_tokens, field)

    for body_match in re.finditer(r"(?:req\.body|body)\.([A-Za-z_][A-Za-z0-9_]*)", code_diff):
        field = body_match.group(1)
        _add_unique(allowed_facts["request_fields"], field)
        _add_unique(allowed_tokens, field)
    for destructured in re.finditer(r"\{([^}]+)\}\s*=\s*(?:req\.body|body)", code_diff):
        for field in re.findall(r"\b([A-Za-z_][A-Za-z0-9_]*)\b", destructured.group(1)):
            _add_unique(allowed_facts["request_fields"], field)
            _add_unique(allowed_tokens, field)

    for role in re.findall(r"requireRole\(['\"]([^'\"]+)['\"]\)", code_diff):
        _add_unique(allowed_facts["auth_roles"], role)
        _add_unique(allowed_tokens, role)

    for value in re.findall(r"\.min\((\d+)\)", code_diff):
        _add_unique(allowed_facts["validation_min_values"], value)
        _add_unique(allowed_tokens, value)
    for value in re.findall(r"\.max\((\d+)\)", code_diff):
        _add_unique(allowed_facts["validation_max_values"], value)
        _add_unique(allowed_tokens, value)

    for name in re.findall(r"(?:interface|class)\s+([A-Za-z_][A-Za-z0-9_]*)", code_diff):
        _add_unique(allowed_facts["interface_or_class_names"], name)
        _add_unique(allowed_tokens, name)
    added_fields, field_types = _extract_interface_fields(code_diff)
    for field in added_fields:
        _add_unique(allowed_facts["added_fields"], field)
        _add_unique(allowed_tokens, field)
    for field_type in field_types:
        _add_unique(allowed_facts["field_types"], field_type)
        _add_unique(allowed_tokens, field_type)

    for env_var in re.findall(r"process\.env\.([A-Z][A-Z0-9_]*)", code_diff):
        _add_unique(allowed_facts["env_vars"], env_var)
        _add_unique(allowed_tokens, env_var)
    for variable in re.findall(r"(?:const|let|var|export const)\s+([A-Za-z_][A-Za-z0-9_]*)\s*=", code_diff):
        _add_unique(allowed_facts["config_variables"], variable)
        _add_unique(allowed_tokens, variable)
    for line in _added_removed_lines(code_diff):
        if "=" in line and re.search(r"\bdefault\b|default_", line, flags=re.IGNORECASE):
            value = line.split("=", 1)[1].strip().rstrip(";")
            _add_unique(allowed_facts["default_values"], value)
            _add_unique(allowed_tokens, value.strip("'\""))

    for command in re.findall(r"npm run [A-Za-z0-9:_-]+|vitest(?: run)?|jest", code_diff):
        _add_unique(allowed_facts["test_commands"], command)
        _add_unique(allowed_tokens, command)
        if "vitest" in command:
            _add_unique(allowed_facts["frameworks"], "vitest")
        if "jest" in command:
            _add_unique(allowed_facts["frameworks"], "jest")

    for cron in re.findall(r"['\"]((?:\*|\*/\d+|\d+) (?:\*|\d+) (?:\*|\d+) (?:\*|\d+) (?:\*|\d+))['\"]", code_diff):
        _add_unique(allowed_facts["cron_expressions"], cron)
        _add_unique(allowed_tokens, cron)
    for name in re.findall(r"\b(?:function|const|await)\s+([A-Za-z_][A-Za-z0-9_]*)\b|\b([A-Za-z_][A-Za-z0-9_]*)\(", code_diff):
        value = next((part for part in name if part), "")
        if value and value not in {"if", "return", "json", "status", "router"}:
            _add_unique(allowed_facts["job_or_function_names"], value)

    for name in re.findall(r"\b([A-Za-z_][A-Za-z0-9_]*RateLimit|rateLimit)\b", code_diff):
        _add_unique(allowed_facts["middleware_names"], name)
        _add_unique(allowed_tokens, name)
    for key, value in re.findall(r"\b(windowMs|max)\s*:\s*(\d+)", code_diff):
        token = f"{key}: {value}"
        _add_unique(allowed_facts["rate_limit_values"], token)
        _add_unique(allowed_tokens, value)

    for token in re.findall(r"\b[A-Za-z_][A-Za-z0-9_]{5,}\b", code_diff):
        if token.lower() not in {"router", "status", "string", "number", "return", "export", "const"}:
            _add_unique(allowed_facts["behavior_tokens"], token)

    blocked_terms_hint = [
        "Do not mention request fields unless listed in allowed_facts.request_fields.",
        "Do not mention response fields unless listed in allowed_facts.response_fields.",
        "Do not mention enum/status values unless listed in allowed_tokens.",
        "Do not mention auth mechanisms, roles, or security behavior unless listed in allowed_facts.auth_roles or visible in docs_before.",
    ]
    missing_context_notes: list[str] = []
    if category == "api_reference" and not allowed_facts["request_fields"]:
        missing_context_notes.append("request fields are not visible")
    if category == "api_reference" and not allowed_facts["response_fields"]:
        missing_context_notes.append("response fields are not visible")
    if scenario and "auth" in scenario and not allowed_facts["auth_roles"]:
        missing_context_notes.append("auth role is not visible")

    return {
        "allowed_tokens": allowed_tokens,
        "allowed_facts": allowed_facts,
        "blocked_terms_hint": blocked_terms_hint,
        "missing_context_notes": missing_context_notes,
    }
