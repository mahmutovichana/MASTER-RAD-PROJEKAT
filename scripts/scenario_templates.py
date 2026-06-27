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


def removed_endpoint(ctx: ScenarioContext, *, method: str, path: str, route_path: str, router_name: str, handler: str) -> Record:
    record = _base_record(ctx, "removed_endpoint", True)
    record.update({
        "change_summary": f"Removed {method} {path} endpoint.",
        "changed_files": [ctx.route_file, ctx.controller_file],
        "code_diff": f"diff --git a/{ctx.route_file} b/{ctx.route_file}\n@@\n-{router_name}.{method.lower()}(\"{route_path}\", {handler});\n"
                     f"diff --git a/{ctx.controller_file} b/{ctx.controller_file}\n@@\n-export function {handler}(req: Request, res: Response) {{\n-  res.status(200).json({{ data: [] }});\n-}}",
        "docs_before_excerpt": f"### {method} {path}\n\nReturns resource data.",
        "expected_facts": [f"{method} {path} endpoint was removed", "The route registration was deleted"],
        "gold_doc_patch": f"@@ {ctx.section}\n-### {method} {path}\n-\n-Returns resource data.\n+The `{method} {path}` endpoint is no longer available.",
        "docs_after_gold_excerpt": f"The `{method} {path}` endpoint is no longer available.",
        "negative_reason": None,
        "difficulty": "medium",
        "tags": [ctx.module, "endpoint", "removed", "documentation-required"],
    })
    return record


def changed_endpoint_path(ctx: ScenarioContext, *, method: str, old_path: str, new_path: str, old_route_path: str, new_route_path: str, router_name: str, handler: str) -> Record:
    record = _base_record(ctx, "changed_endpoint_path", True)
    record.update({
        "change_summary": f"Changed {method} endpoint path from {old_path} to {new_path}.",
        "changed_files": [ctx.route_file],
        "code_diff": f"diff --git a/{ctx.route_file} b/{ctx.route_file}\n@@\n-{router_name}.{method.lower()}(\"{old_route_path}\", {handler});\n+{router_name}.{method.lower()}(\"{new_route_path}\", {handler});",
        "docs_before_excerpt": f"### {method} {old_path}",
        "expected_facts": [f"{method} endpoint path changed from {old_path} to {new_path}", f"New documented path is {new_path}"],
        "gold_doc_patch": f"@@ {ctx.section}\n-### {method} {old_path}\n+### {method} {new_path}",
        "docs_after_gold_excerpt": f"### {method} {new_path}",
        "negative_reason": None,
        "difficulty": "medium",
        "tags": [ctx.module, "endpoint", "path", "documentation-required"],
    })
    return record


def changed_http_method(ctx: ScenarioContext, *, old_method: str, new_method: str, path: str, route_path: str, router_name: str, handler: str) -> Record:
    record = _base_record(ctx, "changed_http_method", True)
    record.update({
        "change_summary": f"Changed {path} method from {old_method} to {new_method}.",
        "changed_files": [ctx.route_file],
        "code_diff": f"diff --git a/{ctx.route_file} b/{ctx.route_file}\n@@\n-{router_name}.{old_method.lower()}(\"{route_path}\", {handler});\n+{router_name}.{new_method.lower()}(\"{route_path}\", {handler});",
        "docs_before_excerpt": f"### {old_method} {path}",
        "expected_facts": [f"{path} now uses {new_method}", f"{old_method} was replaced by {new_method}"],
        "gold_doc_patch": f"@@ {ctx.section}\n-### {old_method} {path}\n+### {new_method} {path}",
        "docs_after_gold_excerpt": f"### {new_method} {path}",
        "negative_reason": None,
        "difficulty": "medium",
        "tags": [ctx.module, "endpoint", "method", "documentation-required"],
    })
    return record


def added_request_field(ctx: ScenarioContext, *, endpoint: str, field: str, zod_type: str, description: str) -> Record:
    record = _base_record(ctx, "added_request_field", True)
    record.update({
        "change_summary": f"Added request field {field} to {endpoint}.",
        "changed_files": [ctx.schema_file],
        "code_diff": f"diff --git a/{ctx.schema_file} b/{ctx.schema_file}\n@@\n   status: z.enum([\"draft\", \"active\", \"archived\"]),\n+  {field}: {zod_type}",
        "docs_before_excerpt": "Request fields omit the new field.",
        "expected_facts": [f"{endpoint} accepts {field}", description],
        "gold_doc_patch": f"@@ {ctx.section}\n+- `{field}`: {description}",
        "docs_after_gold_excerpt": f"- `{field}`: {description}",
        "negative_reason": None,
        "difficulty": "medium",
        "tags": [ctx.module, "request", "field", "documentation-required"],
    })
    return record


def removed_request_field(ctx: ScenarioContext, *, endpoint: str, field: str, description: str) -> Record:
    record = _base_record(ctx, "removed_request_field", True)
    record.update({
        "change_summary": f"Removed request field {field} from {endpoint}.",
        "changed_files": [ctx.schema_file],
        "code_diff": f"diff --git a/{ctx.schema_file} b/{ctx.schema_file}\n@@\n-  {field}: z.string().optional(),",
        "docs_before_excerpt": f"- `{field}`: {description}",
        "expected_facts": [f"{endpoint} no longer accepts {field}", f"{field} was removed from the request schema"],
        "gold_doc_patch": f"@@ {ctx.section}\n-`{field}`: {description}\n+The `{field}` request field is no longer supported.",
        "docs_after_gold_excerpt": f"The `{field}` request field is no longer supported.",
        "negative_reason": None,
        "difficulty": "medium",
        "tags": [ctx.module, "request", "field", "documentation-required"],
    })
    return record


def changed_validation_max(ctx: ScenarioContext, *, field: str, old_max: int, new_max: int, endpoint: str) -> Record:
    record = _base_record(ctx, "changed_validation_max", True)
    record.update({
        "change_summary": f"Changed {field} maximum validation from {old_max} to {new_max}.",
        "changed_files": [ctx.schema_file],
        "code_diff": f"diff --git a/{ctx.schema_file} b/{ctx.schema_file}\n@@\n-  {field}: z.number().int().max({old_max})\n+  {field}: z.number().int().max({new_max})",
        "docs_before_excerpt": f"- `{field}`: integer, maximum {old_max}",
        "expected_facts": [f"{endpoint} {field} maximum is {new_max}", f"{field} max changed from {old_max} to {new_max}"],
        "gold_doc_patch": f"@@ {ctx.section}\n-- `{field}`: integer, maximum {old_max}\n+- `{field}`: integer, maximum {new_max}",
        "docs_after_gold_excerpt": f"- `{field}`: integer, maximum {new_max}",
        "negative_reason": None,
        "difficulty": "easy",
        "tags": [ctx.module, "validation", "max", "documentation-required"],
    })
    return record


def changed_enum_values(ctx: ScenarioContext, *, field: str, old_values: list[str], new_values: list[str], endpoint: str) -> Record:
    old_doc = ", ".join(f"`{value}`" for value in old_values)
    new_doc = ", ".join(f"`{value}`" for value in new_values)
    record = _base_record(ctx, "changed_enum_values", True)
    record.update({
        "change_summary": f"Changed allowed {field} enum values for {endpoint}.",
        "changed_files": [ctx.schema_file],
        "code_diff": f"diff --git a/{ctx.schema_file} b/{ctx.schema_file}\n@@\n-  {field}: z.enum({old_values!r})\n+  {field}: z.enum({new_values!r})",
        "docs_before_excerpt": f"- `{field}`: one of {old_doc}",
        "expected_facts": [f"{endpoint} {field} values are {', '.join(new_values)}", f"{field} enum values changed"],
        "gold_doc_patch": f"@@ {ctx.section}\n-- `{field}`: one of {old_doc}\n+- `{field}`: one of {new_doc}",
        "docs_after_gold_excerpt": f"- `{field}`: one of {new_doc}",
        "negative_reason": None,
        "difficulty": "medium",
        "tags": [ctx.module, "enum", "documentation-required"],
    })
    return record


def changed_status_code(ctx: ScenarioContext, *, endpoint: str, old_status: int, new_status: int, handler: str) -> Record:
    record = _base_record(ctx, "changed_status_code", True)
    record.update({
        "change_summary": f"Changed {endpoint} success status from {old_status} to {new_status}.",
        "changed_files": [ctx.controller_file],
        "code_diff": f"diff --git a/{ctx.controller_file} b/{ctx.controller_file}\n@@\n-  res.status({old_status}).json({{ data: result }});\n+  res.status({new_status}).json({{ data: result }});",
        "docs_before_excerpt": f"Response: `{old_status}`",
        "expected_facts": [f"{endpoint} returns {new_status}", f"Controller {handler} changed status to {new_status}"],
        "gold_doc_patch": f"@@ {ctx.section}\n-Response: `{old_status}`\n+Response: `{new_status}`",
        "docs_after_gold_excerpt": f"Response: `{new_status}`",
        "negative_reason": None,
        "difficulty": "easy",
        "tags": [ctx.module, "status-code", "documentation-required"],
    })
    return record


def changed_error_response(ctx: ScenarioContext, *, endpoint: str, old_error: str, new_error: str, status_code: int) -> Record:
    record = _base_record(ctx, "changed_error_response", True)
    record.update({
        "change_summary": f"Changed {endpoint} error response to {new_error}.",
        "changed_files": [ctx.controller_file],
        "code_diff": f"diff --git a/{ctx.controller_file} b/{ctx.controller_file}\n@@\n-  return res.status({status_code}).json({{ error: \"{old_error}\" }});\n+  return res.status({status_code}).json({{ error: \"{new_error}\" }});",
        "docs_before_excerpt": f"Error `{status_code}`: {old_error}",
        "expected_facts": [f"{endpoint} error {status_code} is {new_error}", f"Error response changed from {old_error} to {new_error}"],
        "gold_doc_patch": f"@@ {ctx.section}\n-Error `{status_code}`: {old_error}\n+Error `{status_code}`: {new_error}",
        "docs_after_gold_excerpt": f"Error `{status_code}`: {new_error}",
        "negative_reason": None,
        "difficulty": "hard",
        "tags": [ctx.module, "error-response", "documentation-required"],
    })
    return record


def deprecated_endpoint(ctx: ScenarioContext, *, method: str, path: str, deprecation_date: str) -> Record:
    record = _base_record(ctx, "deprecated_endpoint", True)
    record.update({
        "change_summary": f"Deprecated {method} {path}.",
        "changed_files": [ctx.route_file, ctx.controller_file],
        "code_diff": f"diff --git a/{ctx.route_file} b/{ctx.route_file}\n@@\n+// Deprecated: {method} {path} will be removed on {deprecation_date}",
        "docs_before_excerpt": f"### {method} {path}\n\nEndpoint is documented as active.",
        "expected_facts": [f"{method} {path} is deprecated", f"Deprecation date is {deprecation_date}"],
        "gold_doc_patch": f"@@ {ctx.section}\n+Deprecated: `{method} {path}` will be removed on {deprecation_date}.",
        "docs_after_gold_excerpt": f"Deprecated: `{method} {path}` will be removed on {deprecation_date}.",
        "negative_reason": None,
        "difficulty": "medium",
        "tags": [ctx.module, "deprecated", "documentation-required"],
    })
    return record


def negative_record(ctx: ScenarioContext, *, scenario_type: str, summary: str, changed_file: str, code_diff: str, negative_reason: str) -> Record:
    record = _base_record(ctx, scenario_type, False)
    record.update({
        "change_summary": summary,
        "changed_files": [changed_file],
        "code_diff": code_diff,
        "docs_before_excerpt": f"## {ctx.section}",
        "expected_facts": [],
        "gold_doc_patch": None,
        "docs_after_gold_excerpt": f"## {ctx.section}",
        "negative_reason": negative_reason,
        "difficulty": "easy",
        "tags": [ctx.module, "negative", scenario_type],
    })
    return record


SCENARIO_TEMPLATES.update({
    "removed_endpoint": removed_endpoint,
    "changed_endpoint_path": changed_endpoint_path,
    "changed_http_method": changed_http_method,
    "added_request_field": added_request_field,
    "removed_request_field": removed_request_field,
    "changed_validation_max": changed_validation_max,
    "changed_enum_values": changed_enum_values,
    "changed_status_code": changed_status_code,
    "changed_error_response": changed_error_response,
    "deprecated_endpoint": deprecated_endpoint,
    "negative_record": negative_record,
})
