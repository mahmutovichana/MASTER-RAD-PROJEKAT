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
    changed_auth_requirement,
    changed_validation_min,
    internal_refactor,
    new_endpoint,
)


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORTS_DIR = ROOT / "reports"
PROJECTS_DIR = ROOT / "generated_projects"
RECORDS_PER_PROJECT = 100

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


def record_for(project: ProjectSpec, module: ModuleSpec, index: int) -> dict[str, object]:
    ctx = context_for(project, module, f"{project.project_id}-{index:03d}")
    item_pascal = pascal(module.item_name)
    module_pascal = pascal(module.name)
    router_name = f"{camel(module.item_name)}Router"
    service_name = f"{camel(module.item_name)}Service"
    repository_name = f"{camel(module.item_name)}Repository"
    scenario_slot = (index - 1) % 5
    cycle = (index - 1) // (5 * len(project.modules))

    if scenario_slot == 0:
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
    if scenario_slot == 1:
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
    if scenario_slot == 2:
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
    if scenario_slot == 3:
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
    return internal_refactor(
        ctx,
        symbol_before=f"raw{module_pascal}{pascal(VARIANT_TERMS[cycle % len(VARIANT_TERMS)])}",
        symbol_after=f"prepared{module_pascal}{pascal(VARIANT_TERMS[cycle % len(VARIANT_TERMS)])}",
        behavior_summary=f"{repository_name}.list()",
    )


def build_records() -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for project in PROJECTS:
        for index in range(1, RECORDS_PER_PROJECT + 1):
            module = project.modules[(index - 1) % len(project.modules)]
            records.append(record_for(project, module, index))
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
        "Dataset regenerated from reusable scenario templates and variation pools across 10 synthetic REST API projects.",
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
                "- at least 1000 records exist",
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
                "- `new_endpoint`",
                "- `changed_validation_min`",
                "- `changed_auth_requirement`",
                "- `added_response_field`",
                "- `internal_refactor`",
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
