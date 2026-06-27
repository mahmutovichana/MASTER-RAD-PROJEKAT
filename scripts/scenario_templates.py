from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


Record = dict[str, object]


@dataclass(frozen=True)
class ScenarioContext:
    record_id: str
    project_id: str
    module: str
    section: str
    route_file: str
    controller_file: str
    service_file: str
    repository_file: str
    schema_file: str
    target_doc_file: str = "docs/api.md"


def _base_record(ctx: ScenarioContext, scenario_type: str, docs_update_required: bool) -> Record:
    return {
        "id": ctx.record_id,
        "project_id": ctx.project_id,
        "scenario_type": scenario_type,
        "docs_update_required": docs_update_required,
        "target_doc_file": ctx.target_doc_file,
        "target_section": ctx.section,
        "tags": [ctx.module, scenario_type],
    }


def new_endpoint(
    ctx: ScenarioContext,
    *,
    method: str,
    path: str,
    route_path: str,
    router_name: str,
    handler: str,
    service_method: str,
    repository_name: str,
    collection_name: str,
    service_call: str,
    description: str,
    response_status: str = "200 OK",
) -> Record:
    record = _base_record(ctx, "new_endpoint", True)
    record.update(
        {
            "change_summary": f"Added {method} {path} endpoint.",
            "changed_files": [ctx.route_file, ctx.controller_file, ctx.service_file, ctx.repository_file],
            "code_diff": (
                f"diff --git a/{ctx.route_file} b/{ctx.route_file}\n"
                "@@\n"
                f"+{router_name}.{method.lower()}(\"{route_path}\", {handler});\n"
                f"diff --git a/{ctx.controller_file} b/{ctx.controller_file}\n"
                "@@\n"
                f"+export function {handler}(req: Request, res: Response) {{\n"
                f"+  const result = {service_call};\n"
                f"+  res.status({response_status.split()[0]}).json({{ data: result }});\n"
                "+}\n"
                f"diff --git a/{ctx.service_file} b/{ctx.service_file}\n"
                "@@\n"
                f"+  {service_method}(id: string) {{\n"
                f"+    return {repository_name}.findById(id);\n"
                "+  }\n"
                f"diff --git a/{ctx.repository_file} b/{ctx.repository_file}\n"
                "@@\n"
                "+  findById(id: string) {\n"
                f"+    return {collection_name}.find((item) => item.id === id);\n"
                "+  }"
            ),
            "docs_before_excerpt": f"## {ctx.section}",
            "expected_facts": [
                f"{method} {path} endpoint exists",
                f"Endpoint returns {response_status}",
                description,
            ],
            "gold_doc_patch": (
                f"@@ {ctx.section}\n"
                f"+### {method} {path}\n"
                "+\n"
                f"+{description}.\n"
                "+\n"
                f"+Response: `{response_status}`"
            ),
            "docs_after_gold_excerpt": f"### {method} {path}\n\n{description}.\n\nResponse: `{response_status}`",
            "negative_reason": None,
            "difficulty": "easy",
            "tags": [ctx.module, "endpoint", "documentation-required"],
        }
    )
    return record


def changed_validation_min(
    ctx: ScenarioContext,
    *,
    field: str,
    old_min: int,
    new_min: int,
    zod_prefix: str,
    zod_suffix: str,
    line_suffix: str,
    schema_name: str,
    endpoint: str,
    validation_context: str,
) -> Record:
    record = _base_record(ctx, "changed_validation_min", True)
    record.update(
        {
            "change_summary": (
                f"Changed {field} minimum validation from {old_min} to {new_min} "
                f"for {validation_context}."
            ),
            "changed_files": [ctx.schema_file],
            "code_diff": (
                f"diff --git a/{ctx.schema_file} b/{ctx.schema_file}\n"
                "@@\n"
                f"-  {field}: {zod_prefix}.min({old_min}){zod_suffix}{line_suffix}\n"
                f"+  {field}: {zod_prefix}.min({new_min}){zod_suffix}{line_suffix}"
            ),
            "docs_before_excerpt": f"- `{field}`: integer, minimum {old_min}",
            "expected_facts": [
                f"{endpoint} {field} minimum is {new_min}",
                f"The changed validation is grounded in {schema_name}",
                f"The validation change applies to {validation_context}",
            ],
            "gold_doc_patch": (
                f"@@ {ctx.section}\n"
                f"-- `{field}`: integer, minimum {old_min}\n"
                f"+- `{field}`: integer, minimum {new_min}"
            ),
            "docs_after_gold_excerpt": f"- `{field}`: integer, minimum {new_min}",
            "negative_reason": None,
            "difficulty": "easy",
            "tags": [ctx.module, "validation", "min", "documentation-required"],
        }
    )
    return record


def changed_auth_requirement(
    ctx: ScenarioContext,
    *,
    method: str,
    path: str,
    route_path: str,
    router_name: str,
    handler: str,
    middleware: str,
    auth_description: str,
) -> Record:
    record = _base_record(ctx, "changed_auth_requirement", True)
    record.update(
        {
            "change_summary": f"{method} {path} now requires {auth_description}.",
            "changed_files": [ctx.route_file],
            "code_diff": (
                f"diff --git a/{ctx.route_file} b/{ctx.route_file}\n"
                "@@\n"
                f"-{router_name}.{method.lower()}(\"{route_path}\", {handler});\n"
                f"+{router_name}.{method.lower()}(\"{route_path}\", {middleware}, {handler});"
            ),
            "docs_before_excerpt": f"### {method} {path}\n\nReturns data without authentication details.",
            "expected_facts": [
                f"{method} {path} requires {auth_description}",
                "The authentication requirement is added at route level",
            ],
            "gold_doc_patch": (
                f"@@ {ctx.section}\n"
                f" ### {method} {path}\n"
                " \n"
                "+Authentication: "
                f"{auth_description}."
            ),
            "docs_after_gold_excerpt": f"Authentication: {auth_description}.",
            "negative_reason": None,
            "difficulty": "medium",
            "tags": [ctx.module, "auth", "documentation-required"],
        }
    )
    return record


def added_response_field(
    ctx: ScenarioContext,
    *,
    endpoint: str,
    field: str,
    field_description: str,
    response_fields: list[str],
) -> Record:
    record = _base_record(ctx, "added_response_field", True)
    record.update(
        {
            "change_summary": f"{endpoint} response now includes {field}.",
            "changed_files": [ctx.repository_file, ctx.controller_file],
            "code_diff": (
                f"diff --git a/{ctx.repository_file} b/{ctx.repository_file}\n"
                "@@\n"
                f"+  {field}: string;\n"
                "@@\n"
                f"+    const saved = {{ {field}: \"generated\", ...input }};"
            ),
            "docs_before_excerpt": "Response body omits the new field.",
            "expected_facts": [
                f"{endpoint} response includes {field}",
                field_description,
            ],
            "gold_doc_patch": (
                f"@@ {ctx.section}\n"
                f"+Response body includes {', '.join(f'`{name}`' for name in response_fields)}."
            ),
            "docs_after_gold_excerpt": f"Response body includes {', '.join(f'`{name}`' for name in response_fields)}.",
            "negative_reason": None,
            "difficulty": "medium",
            "tags": [ctx.module, "response", "documentation-required"],
        }
    )
    return record


def internal_refactor(
    ctx: ScenarioContext,
    *,
    symbol_before: str,
    symbol_after: str,
    behavior_summary: str,
) -> Record:
    record = _base_record(ctx, "internal_refactor", False)
    record.update(
        {
            "change_summary": f"Renamed internal symbol {symbol_before} to {symbol_after}.",
            "changed_files": [ctx.service_file],
            "code_diff": (
                f"diff --git a/{ctx.service_file} b/{ctx.service_file}\n"
                "@@\n"
                f"-  const {symbol_before} = {behavior_summary};\n"
                f"+  const {symbol_after} = {behavior_summary};"
            ),
            "docs_before_excerpt": f"## {ctx.section}",
            "expected_facts": [],
            "gold_doc_patch": None,
            "docs_after_gold_excerpt": f"## {ctx.section}",
            "negative_reason": (
                "Only internal implementation naming changed; routes, request schema, "
                "response shape, authentication, and status codes are unchanged."
            ),
            "difficulty": "easy",
            "tags": [ctx.module, "negative", "internal-refactor"],
        }
    )
    return record


SCENARIO_TEMPLATES: dict[str, Callable[..., Record]] = {
    "new_endpoint": new_endpoint,
    "changed_validation_min": changed_validation_min,
    "changed_auth_requirement": changed_auth_requirement,
    "added_response_field": added_response_field,
    "internal_refactor": internal_refactor,
}
