from __future__ import annotations

import json
import re
import shutil
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from scenario_templates import (
    ScenarioContext,
    added_response_field,
    added_request_field,
    changed_endpoint_path,
    changed_error_response,
    changed_http_method,
    changed_auth_requirement,
    changed_enum_values,
    changed_status_code,
    changed_validation_min,
    changed_validation_max,
    deprecated_endpoint,
    internal_refactor,
    negative_record,
    new_endpoint,
    removed_endpoint,
    removed_request_field,
)


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORTS_DIR = ROOT / "reports"
PROJECTS_DIR = ROOT / "generated_projects"
RECORDS_PER_PROJECT = 150

TRAIN_PROJECTS = {
    "shop-api",
    "auth-api",
    "task-manager-api",
    "library-api",
    "booking-api",
    "inventory-api",
    "billing-api",
}
VALIDATION_PROJECTS = {"support-ticket-api"}
TEST_PROJECTS = {"learning-platform-api", "clinic-api"}
VARIANT_TERMS = [
    "audit",
    "import",
    "mobile",
    "partner",
    "bulk",
    "review",
    "archive",
    "public",
    "admin",
    "scheduled",
]
SCENARIO_SEQUENCE = [
    "new_endpoint",
    "changed_validation_min",
    "changed_auth_requirement",
    "added_response_field",
    "internal_refactor",
    "removed_endpoint",
    "changed_endpoint_path",
    "changed_http_method",
    "added_request_field",
    "removed_request_field",
    "changed_validation_max",
    "changed_enum_values",
    "changed_status_code",
    "changed_error_response",
    "deprecated_endpoint",
    "docs_already_updated",
    "formatting_only",
    "test_only_change",
    "comment_only_change",
    "dependency_config_change",
    "rename_private_helper",
    "internal_service_logic_no_api_change",
]


@dataclass(frozen=True)
class ModuleSpec:
    name: str
    item_name: str
    display_name: str
    sample_name: str
    numeric_field: str
    numeric_label: str
    numeric_min: int
    numeric_max: int
    auth_description: str
    response_field: str
    response_fields: list[str]


@dataclass(frozen=True)
class ProjectSpec:
    project_id: str
    title: str
    modules: list[ModuleSpec]


PROJECTS = [
    ProjectSpec(
        "shop-api",
        "Shop API",
        [
            ModuleSpec("products", "product", "Products", "Desk Lamp", "stock", "stock", 0, 500, "a staff bearer token", "sku", ["id", "sku", "name", "status", "stock"]),
            ModuleSpec("orders", "order", "Orders", "Order", "quantity", "quantity", 1, 25, "a customer bearer token", "trackingCode", ["id", "trackingCode", "name", "status", "quantity"]),
        ],
    ),
    ProjectSpec(
        "auth-api",
        "Auth API",
        [
            ModuleSpec("users", "user", "Users", "Pat User", "loginAttempts", "login attempts", 0, 10, "an admin API key", "profileId", ["id", "profileId", "name", "status", "loginAttempts"]),
            ModuleSpec("sessions", "session", "Sessions", "Session", "durationMinutes", "duration minutes", 5, 480, "a valid session token", "issuedAt", ["id", "issuedAt", "name", "status", "durationMinutes"]),
        ],
    ),
    ProjectSpec(
        "task-manager-api",
        "Task Manager API",
        [
            ModuleSpec("tasks", "task", "Tasks", "Write Brief", "priority", "priority", 1, 5, "a workspace member token", "sequenceCode", ["id", "sequenceCode", "name", "status", "priority"]),
            ModuleSpec("projects", "project", "Projects", "Launch Plan", "memberLimit", "member limit", 1, 50, "a workspace owner token", "workspaceCode", ["id", "workspaceCode", "name", "status", "memberLimit"]),
        ],
    ),
    ProjectSpec(
        "library-api",
        "Library API",
        [
            ModuleSpec("books", "book", "Books", "Clean Architecture", "copyCount", "copy count", 1, 20, "a librarian token", "catalogCode", ["id", "catalogCode", "name", "status", "copyCount"]),
            ModuleSpec("loans", "loan", "Loans", "Loan", "loanDays", "loan days", 1, 60, "a borrower token", "dueCode", ["id", "dueCode", "name", "status", "loanDays"]),
        ],
    ),
    ProjectSpec(
        "booking-api",
        "Booking API",
        [
            ModuleSpec("rooms", "room", "Rooms", "Blue Room", "capacity", "capacity", 1, 200, "a venue manager token", "roomCode", ["id", "roomCode", "name", "status", "capacity"]),
            ModuleSpec("reservations", "reservation", "Reservations", "Morning Booking", "guestCount", "guest count", 1, 12, "a booking token", "confirmationCode", ["id", "confirmationCode", "name", "status", "guestCount"]),
        ],
    ),
    ProjectSpec(
        "inventory-api",
        "Inventory API",
        [
            ModuleSpec("items", "item", "Items", "USB Cable", "reorderPoint", "reorder point", 0, 1000, "a warehouse token", "itemCode", ["id", "itemCode", "name", "status", "reorderPoint"]),
            ModuleSpec("shipments", "shipment", "Shipments", "Inbound Shipment", "packageCount", "package count", 1, 100, "a logistics token", "shipmentCode", ["id", "shipmentCode", "name", "status", "packageCount"]),
        ],
    ),
    ProjectSpec(
        "billing-api",
        "Billing API",
        [
            ModuleSpec("invoices", "invoice", "Invoices", "January Invoice", "lineCount", "line count", 1, 200, "a billing token", "invoiceNumber", ["id", "invoiceNumber", "name", "status", "lineCount"]),
            ModuleSpec("payments", "payment", "Payments", "Card Payment", "amountCents", "amount cents", 100, 100000, "a finance token", "receiptNumber", ["id", "receiptNumber", "name", "status", "amountCents"]),
        ],
    ),
    ProjectSpec(
        "support-ticket-api",
        "Support Ticket API",
        [
            ModuleSpec("tickets", "ticket", "Tickets", "Login Issue", "severity", "severity", 1, 5, "a support agent token", "ticketCode", ["id", "ticketCode", "name", "status", "severity"]),
            ModuleSpec("comments", "comment", "Comments", "Initial Reply", "visibilityLevel", "visibility level", 1, 3, "a ticket participant token", "commentCode", ["id", "commentCode", "name", "status", "visibilityLevel"]),
        ],
    ),
    ProjectSpec(
        "learning-platform-api",
        "Learning Platform API",
        [
            ModuleSpec("courses", "course", "Courses", "Intro to APIs", "lessonCount", "lesson count", 1, 80, "an instructor token", "courseCode", ["id", "courseCode", "name", "status", "lessonCount"]),
            ModuleSpec("enrollments", "enrollment", "Enrollments", "Enrollment", "progressPercent", "progress percent", 0, 100, "a learner token", "certificateCode", ["id", "certificateCode", "name", "status", "progressPercent"]),
        ],
    ),
    ProjectSpec(
        "clinic-api",
        "Clinic API",
        [
            ModuleSpec("patients", "patient", "Patients", "Alex Patient", "riskScore", "risk score", 0, 10, "a clinician token", "patientCode", ["id", "patientCode", "name", "status", "riskScore"]),
            ModuleSpec("appointments", "appointment", "Appointments", "Checkup", "durationMinutes", "duration minutes", 10, 180, "a scheduling token", "appointmentCode", ["id", "appointmentCode", "name", "status", "durationMinutes"]),
        ],
    ),
]


def pascal(value: str) -> str:
    return "".join(part.capitalize() for part in re.split(r"[-_]", value))


def camel(value: str) -> str:
    name = pascal(value)
    return name[0].lower() + name[1:]


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def write_jsonl(path: Path, records: list[dict[str, object]]) -> None:
    path.write_text(
        "\n".join(json.dumps(record, ensure_ascii=False) for record in records) + ("\n" if records else ""),
        encoding="utf-8",
    )


def module_paths(module: ModuleSpec) -> dict[str, str]:
    base = f"src/modules/{module.name}/{module.name}"
    return {
        "routes": f"{base}.routes.ts",
        "controller": f"{base}.controller.ts",
        "service": f"{base}.service.ts",
        "repository": f"{base}.repository.ts",
        "schema": f"{base}.schema.ts",
    }


def generate_project(project: ProjectSpec) -> None:
    project_root = PROJECTS_DIR / project.project_id
    if project_root.exists():
        shutil.rmtree(project_root)

    imports = []
    app_uses = []
    docs_sections = []

    for module in project.modules:
        paths = module_paths(module)
        singular = pascal(module.item_name)
        module_camel = camel(module.name)
        router_name = f"{camel(module.item_name)}Router"
        service_name = f"{camel(module.item_name)}Service"
        repository_name = f"{camel(module.item_name)}Repository"
        type_name = singular
        create_schema = f"create{singular}Schema"

        imports.append(f'import {{ {router_name} }} from "./modules/{module.name}/{module.name}.routes";')
        app_uses.append(f'app.use("/{module.name}", {router_name});')

        write_text(
            project_root / paths["schema"],
            f"""
            import {{ z }} from "zod";

            export const {create_schema} = z.object({{
              name: z.string().min(2),
              status: z.enum(["draft", "active", "archived"]),
              {module.numeric_field}: z.number().int().min({module.numeric_min}).max({module.numeric_max})
            }});
            """,
        )
        write_text(
            project_root / paths["repository"],
            f"""
            export type {type_name} = {{
              id: string;
              name: string;
              status: "draft" | "active" | "archived";
              {module.numeric_field}: number;
            }};

            const {module.name}: {type_name}[] = [
              {{ id: "{module.item_name}_1", name: "{module.sample_name}", status: "active", {module.numeric_field}: {module.numeric_min} }}
            ];

            export const {repository_name} = {{
              list() {{
                return {module.name};
              }},
              create(input: Omit<{type_name}, "id">) {{
                const saved = {{ id: `{module.item_name}_${{{module.name}.length + 1}}`, ...input }};
                {module.name}.push(saved);
                return saved;
              }}
            }};
            """,
        )
        write_text(
            project_root / paths["service"],
            f"""
            import {{ {repository_name} }} from "./{module.name}.repository";

            export const {service_name} = {{
              list{pascal(module.name)}() {{
                return {repository_name}.list();
              }},
              create{singular}(input: {{ name: string; status: "draft" | "active" | "archived"; {module.numeric_field}: number }}) {{
                return {repository_name}.create(input);
              }}
            }};
            """,
        )
        write_text(
            project_root / paths["controller"],
            f"""
            import {{ Request, Response }} from "express";
            import {{ {create_schema} }} from "./{module.name}.schema";
            import {{ {service_name} }} from "./{module.name}.service";

            export function list{pascal(module.name)}(_req: Request, res: Response) {{
              res.status(200).json({{ data: {service_name}.list{pascal(module.name)}() }});
            }}

            export function create{singular}(req: Request, res: Response) {{
              const input = {create_schema}.parse(req.body);
              const result = {service_name}.create{singular}(input);
              res.status(201).json({{ data: result }});
            }}
            """,
        )
        write_text(
            project_root / paths["routes"],
            f"""
            import {{ Router }} from "express";
            import {{ create{singular}, list{pascal(module.name)} }} from "./{module.name}.controller";

            export const {router_name} = Router();

            {router_name}.get("/", list{pascal(module.name)});
            {router_name}.post("/", create{singular});
            """,
        )
        docs_sections.append(
            f"""
            ## {module.display_name}

            ### GET /{module.name}

            Returns all {module.name}.

            Response: `200 OK`

            ### POST /{module.name}

            Creates a {module.item_name}.

            Request fields:

            - `name`: string, minimum length 2
            - `status`: one of `draft`, `active`, `archived`
            - `{module.numeric_field}`: integer, minimum {module.numeric_min}, maximum {module.numeric_max}

            Response: `201 Created`
            """
        )

    write_text(
        project_root / "src/app.ts",
        f"""
        import express from "express";
        {chr(10).join(imports)}

        export const app = express();

        app.use(express.json());
        {chr(10).join(app_uses)}

        app.get("/health", (_req, res) => {{
          res.status(200).json({{ status: "ok" }});
        }});
        """,
    )
    write_text(
        project_root / "package.json",
        json.dumps(
            {
                "name": project.project_id,
                "version": "0.1.0",
                "private": True,
                "type": "module",
                "scripts": {"dev": "tsx src/app.ts", "typecheck": "tsc --noEmit"},
                "dependencies": {"express": "^4.18.3", "zod": "^3.23.8"},
                "devDependencies": {"@types/express": "^4.17.21", "tsx": "^4.7.1", "typescript": "^5.4.5"},
            },
            indent=2,
        ),
    )
    write_text(
        project_root / "README.md",
        f"""
        # {project.title}

        Synthetic REST API project for DocGuard dataset examples.

        Modules:

        {chr(10).join(f"- {module.name}" for module in project.modules)}
        """,
    )
    write_text(project_root / "CHANGELOG.md", "# Changelog\n\n## 0.1.0\n\n- Initial synthetic API surface.")
    write_text(project_root / "docs/api.md", f"# {project.title} Documentation\n\n" + "\n".join(section.strip() for section in docs_sections))


def context_for(project: ProjectSpec, module: ModuleSpec, record_id: str) -> ScenarioContext:
    paths = module_paths(module)
    return ScenarioContext(
        record_id=record_id,
        project_id=project.project_id,
        module=module.name,
        section=module.display_name,
        route_file=paths["routes"],
        controller_file=paths["controller"],
        service_file=paths["service"],
        repository_file=paths["repository"],
        schema_file=paths["schema"],
    )


def record_for(project: ProjectSpec, module: ModuleSpec, index: int, global_index: int) -> dict[str, object]:
    ctx = context_for(project, module, f"{project.project_id}-{index:03d}")
    item_pascal = pascal(module.item_name)
    module_pascal = pascal(module.name)
    router_name = f"{camel(module.item_name)}Router"
    service_name = f"{camel(module.item_name)}Service"
    repository_name = f"{camel(module.item_name)}Repository"
    scenario_type = SCENARIO_SEQUENCE[global_index % len(SCENARIO_SEQUENCE)]
    cycle = global_index // len(SCENARIO_SEQUENCE)
    endpoint = f"POST /{module.name}"
    path = f"/{module.name}"
    handler = f"create{item_pascal}"

    if scenario_type == "new_endpoint":
        endpoint_variants = [
            ("/:id", f"/{module.name}/:id", f"get{item_pascal}", f"get{item_pascal}", f"Returns a single {module.item_name} by id"),
            ("/:id/audit", f"/{module.name}/:id/audit", f"get{item_pascal}Audit", f"get{item_pascal}Audit", f"Returns audit details for a single {module.item_name}"),
            ("/:id/summary", f"/{module.name}/:id/summary", f"get{item_pascal}Summary", f"get{item_pascal}Summary", f"Returns a compact summary for a single {module.item_name}"),
            ("/:id/history", f"/{module.name}/:id/history", f"get{item_pascal}History", f"get{item_pascal}History", f"Returns change history for a single {module.item_name}"),
            ("/:id/status", f"/{module.name}/:id/status", f"get{item_pascal}Status", f"get{item_pascal}Status", f"Returns current status details for a single {module.item_name}"),
            ("/:id/metrics", f"/{module.name}/:id/metrics", f"get{item_pascal}Metrics", f"get{item_pascal}Metrics", f"Returns usage metrics for a single {module.item_name}"),
            ("/:id/owner", f"/{module.name}/:id/owner", f"get{item_pascal}Owner", f"get{item_pascal}Owner", f"Returns owner details for a single {module.item_name}"),
            ("/:id/timeline", f"/{module.name}/:id/timeline", f"get{item_pascal}Timeline", f"get{item_pascal}Timeline", f"Returns timeline events for a single {module.item_name}"),
            ("/:id/attachments", f"/{module.name}/:id/attachments", f"get{item_pascal}Attachments", f"get{item_pascal}Attachments", f"Returns attachments for a single {module.item_name}"),
            ("/:id/eligibility", f"/{module.name}/:id/eligibility", f"get{item_pascal}Eligibility", f"get{item_pascal}Eligibility", f"Returns eligibility checks for a single {module.item_name}"),
        ]
        route_path, path, handler, service_method, description = endpoint_variants[cycle % len(endpoint_variants)]
        return new_endpoint(
            ctx,
            method="GET",
            path=path,
            route_path=route_path,
            router_name=router_name,
            handler=handler,
            service_method=service_method,
            repository_name=repository_name,
            collection_name=module.name,
            service_call=f"{service_name}.{service_method}(req.params.id)",
            description=description,
        )
    if scenario_type == "changed_validation_min":
        old_min = module.numeric_min + cycle
        new_min = old_min + 1
        effective_max = max(module.numeric_max, new_min + 10)
        validation_context = f"{VARIANT_TERMS[cycle % len(VARIANT_TERMS)]} workflows"
        return changed_validation_min(
            ctx,
            field=module.numeric_field,
            old_min=old_min,
            new_min=new_min,
            zod_prefix="z.number().int()",
            zod_suffix=f".max({effective_max})",
            line_suffix="",
            schema_name=f"create{item_pascal}Schema",
            endpoint=f"POST /{module.name}",
            validation_context=validation_context,
        )
    if scenario_type == "changed_auth_requirement":
        auth_variants = [
            (module.auth_description, f"require{item_pascal}Access"),
            (f"elevated {module.auth_description}", f"requireElevated{item_pascal}Access"),
            (f"read-write {module.auth_description}", f"requireWrite{item_pascal}Access"),
            (f"read-only {module.auth_description}", f"requireRead{item_pascal}Access"),
            (f"tenant-scoped {module.auth_description}", f"requireTenant{item_pascal}Access"),
            (f"organization-scoped {module.auth_description}", f"requireOrganization{item_pascal}Access"),
            (f"owner-level {module.auth_description}", f"requireOwner{item_pascal}Access"),
            (f"auditor {module.auth_description}", f"requireAuditor{item_pascal}Access"),
            (f"service-to-service {module.auth_description}", f"requireService{item_pascal}Access"),
            (f"temporary elevated {module.auth_description}", f"requireTemporary{item_pascal}Access"),
        ]
        auth_description, middleware = auth_variants[cycle % len(auth_variants)]
        return changed_auth_requirement(
            ctx,
            method="POST",
            path=f"/{module.name}",
            route_path="/",
            router_name=router_name,
            handler=f"create{item_pascal}",
            middleware=middleware,
            auth_description=auth_description,
        )
    if scenario_type == "added_response_field":
        field = module.response_field if cycle == 0 else f"{module.response_field}{pascal(VARIANT_TERMS[cycle % len(VARIANT_TERMS)])}"
        response_fields = list(module.response_fields)
        if field not in response_fields:
            response_fields = [*response_fields, field]
        return added_response_field(
            ctx,
            endpoint=f"POST /{module.name}",
            field=field,
            field_description=f"{field} is generated when the {module.item_name} is created",
            response_fields=response_fields,
        )
    if scenario_type == "internal_refactor":
        return internal_refactor(
            ctx,
            symbol_before=f"raw{module_pascal}{pascal(VARIANT_TERMS[cycle % len(VARIANT_TERMS)])}",
            symbol_after=f"prepared{module_pascal}{pascal(VARIANT_TERMS[cycle % len(VARIANT_TERMS)])}",
            behavior_summary=f"{repository_name}.list()",
        )
    if scenario_type == "removed_endpoint":
        term = VARIANT_TERMS[cycle % len(VARIANT_TERMS)]
        return removed_endpoint(ctx, method="GET", path=f"/{module.name}/legacy-{term}", route_path=f"/legacy-{term}", router_name=router_name, handler=f"listLegacy{module_pascal}{pascal(term)}")
    if scenario_type == "changed_endpoint_path":
        term = VARIANT_TERMS[cycle % len(VARIANT_TERMS)]
        return changed_endpoint_path(ctx, method="GET", old_path=f"/{module.name}/old-{term}", new_path=f"/{module.name}/active-{term}", old_route_path=f"/old-{term}", new_route_path=f"/active-{term}", router_name=router_name, handler=f"list{module_pascal}")
    if scenario_type == "changed_http_method":
        method_variants = [
            ("POST", "PATCH", f"/method-{VARIANT_TERMS[cycle % len(VARIANT_TERMS)]}", f"/{module.name}/method-{VARIANT_TERMS[cycle % len(VARIANT_TERMS)]}"),
            ("POST", "PUT", f"/replace-{VARIANT_TERMS[cycle % len(VARIANT_TERMS)]}", f"/{module.name}/replace-{VARIANT_TERMS[cycle % len(VARIANT_TERMS)]}"),
            ("GET", "POST", f"/search-{VARIANT_TERMS[cycle % len(VARIANT_TERMS)]}", f"/{module.name}/search-{VARIANT_TERMS[cycle % len(VARIANT_TERMS)]}"),
            ("PATCH", "DELETE", f"/archive-{VARIANT_TERMS[cycle % len(VARIANT_TERMS)]}", f"/{module.name}/archive-{VARIANT_TERMS[cycle % len(VARIANT_TERMS)]}"),
        ]
        old_method, new_method, route_path, public_path = method_variants[cycle % len(method_variants)]
        return changed_http_method(ctx, old_method=old_method, new_method=new_method, path=public_path, route_path=route_path, router_name=router_name, handler=handler)
    if scenario_type == "added_request_field":
        field = f"{VARIANT_TERMS[cycle % len(VARIANT_TERMS)]}Note"
        return added_request_field(ctx, endpoint=endpoint, field=field, zod_type="z.string().min(3).optional()", description=f"optional string used for {VARIANT_TERMS[cycle % len(VARIANT_TERMS)]} workflows")
    if scenario_type == "removed_request_field":
        field = f"legacy{pascal(VARIANT_TERMS[cycle % len(VARIANT_TERMS)])}Code"
        return removed_request_field(ctx, endpoint=endpoint, field=field, description=f"legacy string code for {VARIANT_TERMS[cycle % len(VARIANT_TERMS)]} workflows")
    if scenario_type == "changed_validation_max":
        old_max = module.numeric_max + cycle + 5
        new_max = module.numeric_max + cycle
        field = f"{module.numeric_field}{pascal(VARIANT_TERMS[cycle % len(VARIANT_TERMS)])}Limit"
        return changed_validation_max(ctx, field=field, old_max=old_max, new_max=new_max, endpoint=endpoint)
    if scenario_type == "changed_enum_values":
        old_values = ["draft", "active", "archived"]
        new_values = ["draft", "active", VARIANT_TERMS[cycle % len(VARIANT_TERMS)]]
        return changed_enum_values(ctx, field="status", old_values=old_values, new_values=new_values, endpoint=endpoint)
    if scenario_type == "changed_status_code":
        old_status = 200 + (cycle % 20)
        new_status = old_status + 1
        status_endpoint = f"POST /{module.name}/{VARIANT_TERMS[cycle % len(VARIANT_TERMS)]}-status"
        return changed_status_code(ctx, endpoint=status_endpoint, old_status=old_status, new_status=new_status, handler=handler)
    if scenario_type == "changed_error_response":
        return changed_error_response(ctx, endpoint=endpoint, old_error="Invalid request", new_error=f"{pascal(VARIANT_TERMS[cycle % len(VARIANT_TERMS)])} validation failed", status_code=400)
    if scenario_type == "deprecated_endpoint":
        term = VARIANT_TERMS[cycle % len(VARIANT_TERMS)]
        return deprecated_endpoint(ctx, method="GET", path=f"/{module.name}/legacy-{term}", deprecation_date=f"2027-{(cycle % 9) + 1:02d}-01")

    if scenario_type == "docs_already_updated":
        old_min = module.numeric_min + cycle
        new_min = old_min + 1
        code_diff = f"diff --git a/{ctx.schema_file} b/{ctx.schema_file}\n@@\n-  {module.numeric_field}: z.number().int().min({old_min})\n+  {module.numeric_field}: z.number().int().min({new_min})\ndiff --git a/docs/api.md b/docs/api.md\n@@\n-- `{module.numeric_field}`: integer, minimum {old_min}\n+- `{module.numeric_field}`: integer, minimum {new_min}"
        return negative_record(ctx, scenario_type=scenario_type, summary=f"Updated {module.numeric_field} validation and documentation together for {VARIANT_TERMS[cycle % len(VARIANT_TERMS)]} workflows.", changed_file=ctx.schema_file, code_diff=code_diff, negative_reason="The API contract changed, but the documentation update is already included in the same diff.")
    if scenario_type == "formatting_only":
        spaces = " " * ((cycle % 3) + 2)
        return negative_record(ctx, scenario_type=scenario_type, summary=f"Reformatted route spacing for {VARIANT_TERMS[cycle % len(VARIANT_TERMS)]} readability without changing behavior.", changed_file=ctx.route_file, code_diff=f"diff --git a/{ctx.route_file} b/{ctx.route_file}\n@@\n-{router_name}.get(\"/\", list{module_pascal});\n+{router_name}.get(\"/\",{spaces}list{module_pascal});", negative_reason="Only whitespace changed; the API contract is unchanged.")
    if scenario_type == "test_only_change":
        test_file = f"src/modules/{module.name}/{module.name}.service.ts"
        return negative_record(ctx, scenario_type=scenario_type, summary="Added internal service test coverage notes.", changed_file=test_file, code_diff=f"diff --git a/{test_file} b/{test_file}\n@@\n+// Test coverage added for {VARIANT_TERMS[cycle % len(VARIANT_TERMS)]} branch behavior.", negative_reason="The change affects tests or test coverage notes only and does not alter the API contract.")
    if scenario_type == "comment_only_change":
        term = VARIANT_TERMS[cycle % len(VARIANT_TERMS)]
        return negative_record(ctx, scenario_type=scenario_type, summary=f"Added implementation comment for {term} maintenance context.", changed_file=ctx.controller_file, code_diff=f"diff --git a/{ctx.controller_file} b/{ctx.controller_file}\n@@\n+// Keep {module.name} {term} response handling stable for clients.", negative_reason="Only a source comment changed; routes, schemas, status codes, and response bodies are unchanged.")
    if scenario_type == "dependency_config_change":
        patch_version = (cycle % 9) + 1
        term = VARIANT_TERMS[cycle % len(VARIANT_TERMS)]
        return negative_record(ctx, scenario_type=scenario_type, summary=f"Updated package metadata for {term} tooling without API behavior changes.", changed_file="package.json", code_diff=f"diff --git a/package.json b/package.json\n@@\n-  \"docguard:{term}\": \"check\"\n+  \"docguard:{term}\": \"check --strict\"", negative_reason="Package metadata changed, but the REST API contract did not change.")
    if scenario_type == "rename_private_helper":
        suffix = pascal(VARIANT_TERMS[cycle % len(VARIANT_TERMS)])
        return negative_record(ctx, scenario_type=scenario_type, summary=f"Renamed a private {VARIANT_TERMS[cycle % len(VARIANT_TERMS)]} helper function.", changed_file=ctx.service_file, code_diff=f"diff --git a/{ctx.service_file} b/{ctx.service_file}\n@@\n-function normalize{item_pascal}{suffix}Input(input) {{\n+function prepare{item_pascal}{suffix}Input(input) {{", negative_reason="A private helper was renamed without changing public routes, schemas, or responses.")
    if scenario_type == "internal_service_logic_no_api_change":
        sort_field = "id" if cycle % 2 == 0 else "name"
        return negative_record(ctx, scenario_type=scenario_type, summary=f"Changed internal {VARIANT_TERMS[cycle % len(VARIANT_TERMS)]} sorting logic without API contract changes.", changed_file=ctx.service_file, code_diff=f"diff --git a/{ctx.service_file} b/{ctx.service_file}\n@@\n-    return {repository_name}.list();\n+    return {repository_name}.list().sort((left, right) => left.{sort_field}.localeCompare(right.{sort_field}));", negative_reason="Internal ordering logic changed, but the documented endpoints and fields are unchanged.")

    raise ValueError(f"Unsupported scenario type: {scenario_type}")


def build_records() -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    global_index = 0
    for project in PROJECTS:
        for index in range(1, RECORDS_PER_PROJECT + 1):
            module = project.modules[(index - 1) % len(project.modules)]
            records.append(record_for(project, module, index, global_index))
            global_index += 1
    return records


def split_name(project_id: str) -> str:
    if project_id in TRAIN_PROJECTS:
        return "train"
    if project_id in VALIDATION_PROJECTS:
        return "validation"
    if project_id in TEST_PROJECTS:
        return "test"
    raise ValueError(f"Project {project_id} is not assigned to a split")


def write_splits(records: list[dict[str, object]]) -> None:
    split_records: dict[str, list[dict[str, object]]] = {"train": [], "validation": [], "test": []}
    for record in records:
        split_records[split_name(str(record["project_id"]))].append(record)

    for name, rows in split_records.items():
        write_jsonl(DATA_DIR / f"{name}.jsonl", rows)


def write_reports(records: list[dict[str, object]]) -> None:
    scenario_counts = Counter(str(record["scenario_type"]) for record in records)
    project_counts = Counter(str(record["project_id"]) for record in records)
    split_counts = Counter(split_name(str(record["project_id"])) for record in records)
    positive_count = sum(1 for record in records if record["docs_update_required"])
    negative_count = len(records) - positive_count

    stats_lines = [
        "# Dataset Statistics",
        "",
        "Dataset v0.2 regenerated from reusable scenario templates and variation pools across 10 synthetic REST API projects.",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Projects | {len(PROJECTS)} |",
        f"| Records | {len(records)} |",
        f"| Positive records | {positive_count} |",
        f"| Negative records | {negative_count} |",
        f"| Train records | {split_counts['train']} |",
        f"| Validation records | {split_counts['validation']} |",
        f"| Test records | {split_counts['test']} |",
        f"| Train projects | {len(TRAIN_PROJECTS)} |",
        f"| Validation projects | {len(VALIDATION_PROJECTS)} |",
        f"| Test projects | {len(TEST_PROJECTS)} |",
        "",
        "## Scenario Counts",
        "",
    ]
    stats_lines.extend(f"- `{scenario}`: {count}" for scenario, count in sorted(scenario_counts.items()))
    stats_lines.extend(["", "## Project Counts", ""])
    stats_lines.extend(f"- `{project_id}`: {count}" for project_id, count in sorted(project_counts.items()))
    (REPORTS_DIR / "dataset_statistics.md").write_text("\n".join(stats_lines) + "\n", encoding="utf-8")

    (REPORTS_DIR / "quality_checks.md").write_text(
        "\n".join(
            [
                "# Quality Checks",
                "",
                "The validation script checks:",
                "",
                "- at least 1500 records exist",
                "- required fields are present",
                "- duplicate ids do not exist",
                "- duplicate semantic records do not exist",
                "- normalized near-duplicate records do not exist",
                "- positive and negative labels match scenario types",
                "- expected facts are non-empty, unique, and grounded for positive records",
                "- positive records include expected facts",
                "- positive records include a gold documentation patch",
                "- positive gold patches include a hunk header, target section, and added documentation lines",
                "- positive gold patch additions are reflected in the gold after excerpt",
                "- negative records do not include a gold documentation patch",
                "- negative records include a negative reason",
                "- negative records do not change the gold after excerpt",
                "- changed files and target documentation files exist",
                "- train/validation/test splits do not leak projects",
                "- every split record is present in the full dataset",
                "- split copies match the full dataset records",
                "",
                "Current reusable scenario templates:",
                "",
                *[f"- `{scenario}`" for scenario in SCENARIO_SEQUENCE],
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    DATA_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)
    PROJECTS_DIR.mkdir(exist_ok=True)

    for project in PROJECTS:
        generate_project(project)

    records = build_records()
    write_jsonl(DATA_DIR / "docguard_dataset.jsonl", records)
    write_splits(records)
    write_reports(records)

    print(f"Generated {len(PROJECTS)} projects and {len(records)} records.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
