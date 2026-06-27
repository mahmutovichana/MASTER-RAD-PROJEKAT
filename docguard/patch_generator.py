from __future__ import annotations

from docguard.diff_analyzer import DiffFacts


def generate_patch(facts: DiffFacts, scenario_type: str, docs_update_required: bool) -> str | None:
    if not docs_update_required:
        return None

    section = facts.target_section or "API"

    if scenario_type == "new_endpoint" and facts.method and facts.full_path:
        description = facts.endpoint_description or "Returns resource details"
        status = facts.response_status or "200 OK"
        return (
            f"@@ {section}\n"
            f"+### {facts.method} {facts.full_path}\n"
            "+\n"
            f"+{description}.\n"
            "+\n"
            f"+Response: `{status}`"
        )

    if scenario_type == "changed_validation_min" and facts.field and facts.new_min is not None:
        return (
            f"@@ {section}\n"
            f"+- `{facts.field}`: integer, minimum {facts.new_min}"
        )

    if scenario_type == "changed_auth_requirement" and facts.method and facts.full_path and facts.middleware:
        auth_text = facts.auth_description or f"{facts.middleware} middleware"
        return (
            f"@@ {section}\n"
            f" ### {facts.method} {facts.full_path}\n"
            " \n"
            f"+Authentication: {auth_text}."
        )

    if scenario_type == "added_response_field" and facts.field:
        return (
            f"@@ {section}\n"
            f"+Response body includes `{facts.field}`."
        )

    return None
