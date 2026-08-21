from __future__ import annotations

import re
from typing import Any

from docguard_llm.fact_extractor import extract_allowed_facts

UNSUPPORTED_CLAIMS = {"oauth", "jwt", "admin", "bearer", "token"}
COMMON_MARKDOWN_WORDS = {
    "api", "request", "response", "responses", "field", "fields", "status", "code", "codes",
    "creates", "create", "returns", "visible", "implementation", "document", "based", "supplied",
    "diff", "patch", "configuration", "workflow", "model", "testing", "command", "default",
}
NO_UPDATE_PHRASES = {
    "no additional content is required",
    "no documentation update is required",
    "no update is required",
    "nothing needs to be changed",
}


def extract_grounding_tokens(code_diff: str) -> list[str]:
    return list(extract_allowed_facts(code_diff).get("allowed_tokens") or [])


def _allowed_values(facts: dict[str, Any]) -> set[str]:
    allowed = {str(token).lower() for token in facts.get("allowed_tokens", [])}
    allowed_facts = facts.get("allowed_facts", {})
    for values in allowed_facts.values():
        if isinstance(values, list):
            allowed.update(str(value).lower() for value in values)
    return allowed


def _allowed_field_names(facts: dict[str, Any]) -> set[str]:
    allowed_facts = facts.get("allowed_facts", {})
    fields: set[str] = set()
    for key in ["response_fields", "request_fields", "added_fields", "env_vars", "config_variables"]:
        fields.update(str(value).lower() for value in allowed_facts.get(key, []))
    return fields


def _mentioned_code_identifiers(patch_text: str) -> set[str]:
    identifiers = set(re.findall(r"`([A-Za-z_][A-Za-z0-9_]*)`", patch_text))
    for line in patch_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("|") and "|" in stripped.strip("|"):
            for part in stripped.strip("|").split("|"):
                value = part.strip().strip("`")
                if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", value):
                    identifiers.add(value)
        if re.match(r"^\+\s*[-*]\s+`?[A-Za-z_][A-Za-z0-9_]*`?\s*[:.-]", line):
            match = re.search(r"`?([A-Za-z_][A-Za-z0-9_]*)`?", line)
            if match:
                identifiers.add(match.group(1))
    return identifiers


def _quoted_example_values(patch_text: str) -> set[str]:
    return {
        value
        for value in re.findall(r"['\"]([A-Za-z_][A-Za-z0-9_-]+)['\"]", patch_text)
        if not value.startswith("/")
    }


def _required_added_env_vars(code_diff: str, docs_before: str) -> set[str]:
    docs = docs_before.lower()
    required: set[str] = set()
    for line in code_diff.splitlines():
        if not line.startswith("+") or line.startswith("+++"):
            continue
        for env_var in re.findall(r"process\.env\.([A-Z][A-Z0-9_]*)", line):
            if env_var.lower() not in docs:
                required.add(env_var)
    return required


def _required_added_routes(code_diff: str, docs_before: str) -> set[str]:
    docs = docs_before.lower()
    required: set[str] = set()
    for line in code_diff.splitlines():
        if not line.startswith("+") or line.startswith("+++"):
            continue
        for method, route in re.findall(r"(?:router|app)\.(get|post|put|patch|delete)\(['\"]([^'\"]+)", line, flags=re.IGNORECASE):
            token = f"{method.upper()} {route}"
            if method.lower() not in docs or route.lower() not in docs:
                required.add(token)
    return required


def verify_patch(
    patch_text: str | None,
    docs_update_required: bool,
    target_doc_file: str,
    code_diff: str,
    docs_before: str,
    doc_category: str | None = None,
    scenario_type: str | None = None,
    allowed_facts: dict[str, Any] | None = None,
) -> dict[str, Any]:
    warnings: list[str] = []
    facts = allowed_facts or extract_allowed_facts(code_diff, docs_before, doc_category, scenario_type)
    if not docs_update_required:
        if patch_text:
            return {"verifier_status": "fail", "warnings": ["no-update prediction should not include a patch"], "grounded_tokens_found": []}
        return {"verifier_status": "pass", "warnings": [], "grounded_tokens_found": []}
    if not patch_text:
        return {"verifier_status": "fail", "warnings": ["positive prediction has empty patch"], "grounded_tokens_found": []}
    mentioned_files = {match for match in re.findall(r"(?:docs/[A-Za-z0-9_.-]+\.md|CHANGELOG\.md|README\.md)", patch_text)}
    outside = sorted(path for path in mentioned_files if path != target_doc_file)
    if outside:
        warnings.append(f"patch mentions filenames outside target: {', '.join(outside)}")
    context = f"{code_diff}\n{docs_before}".lower()
    patch_lower = patch_text.lower()
    if any(phrase in patch_lower for phrase in NO_UPDATE_PHRASES):
        warnings.append("positive documentation update patch claims no content is required")
    for claim in sorted(UNSUPPORTED_CLAIMS):
        if claim in patch_lower and claim not in context:
            warnings.append(f"unsupported security/role claim: {claim}")
    allowed_values = _allowed_values(facts)
    allowed_fields = _allowed_field_names(facts)
    mentioned_identifiers = _mentioned_code_identifiers(patch_text)
    unsupported_identifiers = []
    for identifier in sorted(mentioned_identifiers):
        lowered = identifier.lower()
        if lowered in COMMON_MARKDOWN_WORDS:
            continue
        if lowered not in allowed_values and lowered not in allowed_fields:
            unsupported_identifiers.append(identifier)
    if unsupported_identifiers:
        warnings.append(f"unsupported field/identifier claims: {', '.join(unsupported_identifiers)}")
    unsupported_examples = []
    for value in sorted(_quoted_example_values(patch_text)):
        lowered = value.lower()
        if lowered in COMMON_MARKDOWN_WORDS:
            continue
        if lowered not in allowed_values and lowered not in allowed_fields:
            unsupported_examples.append(value)
    if unsupported_examples:
        warnings.append(f"unsupported quoted/example values: {', '.join(unsupported_examples)}")
    if "request fields" in patch_lower and not (facts.get("allowed_facts", {}).get("request_fields") or []):
        warnings.append("patch includes request fields although none are visible in allowed facts")
    missing_required = []
    for env_var in sorted(_required_added_env_vars(code_diff, docs_before)):
        if env_var.lower() not in patch_lower:
            missing_required.append(env_var)
    for route in sorted(_required_added_routes(code_diff, docs_before)):
        method, route_path = route.split(" ", 1)
        if method.lower() not in patch_lower or route_path.lower() not in patch_lower:
            missing_required.append(route)
    if missing_required:
        warnings.append(f"patch misses required visible change tokens: {', '.join(missing_required)}")
    if doc_category == "api_reference" or target_doc_file.endswith("api.md"):
        response_fields = {str(value).lower() for value in facts.get("allowed_facts", {}).get("response_fields", [])}
        if response_fields:
            field_like = {item.lower() for item in mentioned_identifiers if item.lower() not in COMMON_MARKDOWN_WORDS}
            invalid = sorted(item for item in field_like if item not in response_fields and item not in allowed_values)
            if invalid:
                warnings.append(f"API patch mentions fields not visible in response/request facts: {', '.join(invalid)}")
    tokens = list(facts.get("allowed_tokens") or extract_grounding_tokens(code_diff))
    found = [token for token in tokens if token.lower() in patch_lower]
    if tokens and not found:
        warnings.append("patch does not include any concrete token extracted from the diff")
    too_large = len([line for line in patch_text.splitlines() if line.startswith("+")]) > 12
    if too_large:
        warnings.append("patch is large for a minimal documentation patch")
    status = "fail" if any(
        "outside target" in item
        or "unsupported" in item
        or "claims no content" in item
        or "misses required" in item
        or "request fields although none" in item
        or "fields not visible" in item
        for item in warnings
    ) else ("warn" if warnings else "pass")
    return {"verifier_status": status, "warnings": warnings, "grounded_tokens_found": found}
