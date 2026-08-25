from __future__ import annotations

from typing import Any

from docguard_llm.fact_extractor import extract_allowed_facts


CATEGORY_TO_TARGET_FILE = {
    "api_reference": "docs/api.md",
    "configuration": "docs/configuration.md",
    "developer_setup": "docs/developer-setup.md",
    "model_contract": "docs/models.md",
    "no_update": "",
}

CATEGORY_TO_SECTION = {
    "api_reference": "API Reference",
    "configuration": "Configuration",
    "developer_setup": "Developer Setup",
    "model_contract": "Data Models",
    "no_update": "Documentation",
}


def _dedupe(values: list[Any]) -> list[str]:
    output: list[str] = []
    for value in values or []:
        text = str(value).strip()
        if text and text not in output:
            output.append(text)
    return output


def _code_items(values: list[str], *, limit: int = 6) -> str:
    items = _dedupe(values)[:limit]
    return ", ".join(f"`{item}`" for item in items)


def _first(values: list[str]) -> str | None:
    values = _dedupe(values)
    return values[0] if values else None


def target_file_for_category(category: str) -> str:
    return CATEGORY_TO_TARGET_FILE.get(category, "docs/implementation-notes.md")


def target_section_for_category(category: str) -> str:
    return CATEGORY_TO_SECTION.get(category, "Documentation")


def _api_patch_lines(allowed_facts: dict[str, Any]) -> list[str]:
    methods = _dedupe(allowed_facts.get("http_methods", []))
    routes = _dedupe(allowed_facts.get("route_paths", []))
    statuses = _dedupe(allowed_facts.get("status_codes", []))
    response_fields = _dedupe(allowed_facts.get("response_fields", []))
    request_fields = _dedupe(allowed_facts.get("request_fields", []))
    auth_roles = _dedupe(allowed_facts.get("auth_roles", []))

    lines: list[str] = []

    if routes:
        method = methods[0] if methods else ""
        endpoint = f"{method} {routes[0]}".strip()
        line = f"+- Document the public API endpoint `{endpoint}`."

        if statuses:
            line = line[:-1] + f" and status code `{statuses[0]}`."

        lines.append(line)

    elif methods:
        lines.append(f"+- Document the public API method `{methods[0]}` visible in the code change.")

    if response_fields:
        lines.append(f"+- Response fields visible in the change: {_code_items(response_fields)}.")

    if request_fields:
        lines.append(f"+- Request fields visible in the change: {_code_items(request_fields)}.")

    if auth_roles:
        lines.append(f"+- Access role visible in the change: {_code_items(auth_roles)}.")

    return lines


def _configuration_patch_lines(allowed_facts: dict[str, Any]) -> list[str]:
    env_vars = _dedupe(allowed_facts.get("env_vars", []))
    config_vars = _dedupe(allowed_facts.get("config_variables", []))
    defaults = _dedupe(allowed_facts.get("default_values", []))

    lines: list[str] = []

    if env_vars and defaults:
        lines.append(
            f"+- Document `{env_vars[0]}` and its visible default value `{defaults[0]}`."
        )
    elif env_vars:
        lines.append(f"+- Document the environment variable `{env_vars[0]}`.")

    if config_vars:
        lines.append(f"+- Document the configuration variable `{config_vars[0]}`.")

    if defaults and not env_vars:
        lines.append(f"+- Document the visible default value `{defaults[0]}`.")

    return lines


def _model_contract_patch_lines(allowed_facts: dict[str, Any]) -> list[str]:
    names = _dedupe(allowed_facts.get("interface_or_class_names", []))
    fields = _dedupe(allowed_facts.get("added_fields", []))
    field_types = _dedupe(allowed_facts.get("field_types", []))
    behavior_tokens = _dedupe(allowed_facts.get("behavior_tokens", []))

    lines: list[str] = []

    if names:
        lines.append(f"+- Document the public contract `{names[0]}`.")

    if fields:
        lines.append(f"+- Contract fields visible in the change: {_code_items(fields)}.")

    if field_types:
        compact_types = _code_items(field_types, limit=4)
        if compact_types:
            lines.append(f"+- Field type information visible in the change: {compact_types}.")

    if not lines and behavior_tokens:
        lines.append(f"+- Document the public model/contract change around `{behavior_tokens[0]}`.")

    return lines


def _developer_setup_patch_lines(allowed_facts: dict[str, Any]) -> list[str]:
    commands = _dedupe(allowed_facts.get("test_commands", []))
    frameworks = _dedupe(allowed_facts.get("frameworks", []))
    behavior_tokens = _dedupe(allowed_facts.get("behavior_tokens", []))

    lines: list[str] = []

    if commands:
        lines.append(f"+- Document the developer command `{commands[0]}`.")

    if frameworks:
        lines.append(f"+- Mention the visible tooling/framework `{frameworks[0]}`.")

    if not lines and behavior_tokens:
        lines.append(f"+- Document the developer setup change around `{behavior_tokens[0]}`.")

    return lines


def _fallback_patch_lines(allowed_facts: dict[str, Any], doc_category: str) -> list[str]:
    tokens = _dedupe(allowed_facts.get("allowed_tokens", []))

    if tokens:
        return [f"+- Document the `{doc_category}` change around `{tokens[0]}`."]

    return [
        "+- Document the visible behavior changed in the code diff.",
    ]


def compose_grounded_patch_text(
    *,
    code_diff: str,
    docs_before: str,
    doc_category: str,
    target_doc_file: str | None = None,
    target_section: str | None = None,
    scenario_type: str | None = None,
) -> dict[str, Any]:
    category = str(doc_category or "no_update").strip() or "no_update"

    if category == "no_update":
        return {
            "patch_text": None,
            "patch_status": "not_applicable",
            "target_doc_file": "",
            "target_section": "Documentation",
            "allowed_facts": {},
            "grounding_tokens": [],
            "generator_warnings": [],
        }

    resolved_target = target_doc_file or target_file_for_category(category)
    resolved_section = target_section or target_section_for_category(category)

    allowed = extract_allowed_facts(
        code_diff,
        docs_before,
        category,
        scenario_type,
    )
    allowed_facts = allowed.get("allowed_facts", {})
    grounding_tokens = _dedupe(allowed.get("allowed_tokens", []))
    warnings: list[str] = []

    if category == "api_reference":
        lines = _api_patch_lines(allowed_facts)
    elif category == "configuration":
        lines = _configuration_patch_lines(allowed_facts)
    elif category == "model_contract":
        lines = _model_contract_patch_lines(allowed_facts)
    elif category == "developer_setup":
        lines = _developer_setup_patch_lines(allowed_facts)
    else:
        lines = []

    if not lines:
        lines = _fallback_patch_lines(allowed, category)
        warnings.append("fallback_patch_used")

    patch_text = "\n".join([f"@@ {resolved_section}", *lines]).strip()

    return {
        "patch_text": patch_text,
        "patch_status": "ok",
        "target_doc_file": resolved_target,
        "target_section": resolved_section,
        "allowed_facts": allowed,
        "grounding_tokens": grounding_tokens,
        "generator_warnings": warnings,
    }


def generate_grounded_patch(
    *,
    docs_update_required: bool,
    code_diff: str,
    docs_before: str,
    doc_category: str,
    target_doc_file: str | None = None,
    target_section: str | None = None,
    scenario_type: str | None = None,
) -> dict[str, Any]:
    if not docs_update_required:
        return {
            "patch_text": None,
            "patch_status": "not_applicable",
            "target_doc_file": "",
            "target_section": "Documentation",
            "allowed_facts": {},
            "grounding_tokens": [],
            "generator_warnings": [],
        }

    return compose_grounded_patch_text(
        code_diff=code_diff,
        docs_before=docs_before,
        doc_category=doc_category,
        target_doc_file=target_doc_file,
        target_section=target_section,
        scenario_type=scenario_type,
    )