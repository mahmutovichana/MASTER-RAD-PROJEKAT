from __future__ import annotations

import json
import re
import shutil
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORTS_DIR = ROOT / "reports"
PROJECTS_DIR = ROOT / "generated_projects"
RECORDS_PER_PROJECT = 250

TRAIN_PROJECTS = {"shop-api", "auth-api", "task-manager-api", "library-api", "booking-api", "inventory-api", "billing-api"}
VALIDATION_PROJECTS = {"support-ticket-api"}
TEST_PROJECTS = {"learning-platform-api", "clinic-api"}

DOC_CATEGORIES = {
    "api_reference",
    "architecture_flow",
    "model_contract",
    "developer_setup",
    "testing_instructions",
    "configuration",
    "workflow_documentation",
    "changelog",
}


@dataclass(frozen=True)
class ModuleSpec:
    name: str
    item_name: str
    display_name: str
    sample_name: str
    numeric_field: str
    numeric_min: int
    numeric_max: int
    response_field: str


@dataclass(frozen=True)
class ProjectSpec:
    project_id: str
    title: str
    modules: list[ModuleSpec]


PROJECTS = [
    ProjectSpec("shop-api", "Shop API", [ModuleSpec("products", "product", "Products", "Desk Lamp", "stock", 0, 500, "sku"), ModuleSpec("orders", "order", "Orders", "Order", "quantity", 1, 25, "trackingCode")]),
    ProjectSpec("auth-api", "Auth API", [ModuleSpec("users", "user", "Users", "Pat User", "loginAttempts", 0, 10, "profileId"), ModuleSpec("sessions", "session", "Sessions", "Session", "durationMinutes", 5, 480, "issuedAt")]),
    ProjectSpec("task-manager-api", "Task Manager API", [ModuleSpec("tasks", "task", "Tasks", "Write Brief", "priority", 1, 5, "sequenceCode"), ModuleSpec("projects", "project", "Projects", "Launch Plan", "memberLimit", 1, 50, "workspaceCode")]),
    ProjectSpec("library-api", "Library API", [ModuleSpec("books", "book", "Books", "Clean Architecture", "copyCount", 1, 20, "catalogCode"), ModuleSpec("loans", "loan", "Loans", "Loan", "loanDays", 1, 60, "dueCode")]),
    ProjectSpec("booking-api", "Booking API", [ModuleSpec("rooms", "room", "Rooms", "Blue Room", "capacity", 1, 200, "roomCode"), ModuleSpec("reservations", "reservation", "Reservations", "Morning Booking", "guestCount", 1, 12, "confirmationCode")]),
    ProjectSpec("inventory-api", "Inventory API", [ModuleSpec("items", "item", "Items", "USB Cable", "reorderPoint", 0, 1000, "itemCode"), ModuleSpec("shipments", "shipment", "Shipments", "Inbound Shipment", "packageCount", 1, 100, "shipmentCode")]),
    ProjectSpec("billing-api", "Billing API", [ModuleSpec("invoices", "invoice", "Invoices", "January Invoice", "lineCount", 1, 200, "invoiceNumber"), ModuleSpec("payments", "payment", "Payments", "Card Payment", "amountCents", 100, 100000, "receiptNumber")]),
    ProjectSpec("support-ticket-api", "Support Ticket API", [ModuleSpec("tickets", "ticket", "Tickets", "Login Issue", "severity", 1, 5, "ticketCode"), ModuleSpec("comments", "comment", "Comments", "Initial Reply", "visibilityLevel", 1, 3, "commentCode")]),
    ProjectSpec("learning-platform-api", "Learning Platform API", [ModuleSpec("courses", "course", "Courses", "Intro to APIs", "lessonCount", 1, 80, "courseCode"), ModuleSpec("enrollments", "enrollment", "Enrollments", "Enrollment", "progressPercent", 0, 100, "certificateCode")]),
    ProjectSpec("clinic-api", "Clinic API", [ModuleSpec("patients", "patient", "Patients", "Alex Patient", "riskScore", 0, 10, "patientCode"), ModuleSpec("appointments", "appointment", "Appointments", "Checkup", "durationMinutes", 10, 180, "appointmentCode")]),
]

API_SCENARIOS = [
    "new_endpoint", "changed_validation_min", "changed_auth_requirement", "added_response_field", "internal_refactor",
    "removed_endpoint", "changed_endpoint_path", "changed_http_method", "added_request_field", "removed_request_field",
    "changed_validation_max", "changed_enum_values", "changed_status_code", "changed_error_response", "deprecated_endpoint",
    "docs_already_updated", "formatting_only", "test_only_change", "comment_only_change", "dependency_config_change",
    "rename_private_helper", "internal_service_logic_no_api_change",
]
HIGH_POSITIVE_SCENARIOS = [
    "added_middleware_flow", "changed_auth_flow", "added_dto_model", "changed_dto_field_semantics",
    "changed_run_command", "changed_test_command", "added_environment_variable", "changed_local_development_flow",
    "added_background_job_flow", "changed_error_handling_flow", "added_service_orchestration_flow",
    "changed_caching_or_rate_limit_flow",
]
HIGH_NEGATIVE_SCENARIOS = [
    "internal_variable_rename_no_behavior_change", "private_helper_refactor_no_flow_change",
    "formatting_only_in_docs_or_code", "dev_dependency_patch_no_command_change",
    "test_assertion_refactor_no_behavior_change", "comments_reworded_no_contract_change",
    "log_message_change_no_user_visible_behavior", "internal_performance_refactor_no_documented_behavior_change",
]
SCENARIO_SEQUENCE = API_SCENARIOS + HIGH_POSITIVE_SCENARIOS + HIGH_NEGATIVE_SCENARIOS
POSITIVE_SCENARIOS = set(API_SCENARIOS[:15]) | set(HIGH_POSITIVE_SCENARIOS)
NEGATIVE_SCENARIOS = set(API_SCENARIOS[15:]) | set(HIGH_NEGATIVE_SCENARIOS)
VARIANTS = ["audit", "import", "mobile", "partner", "bulk", "review", "archive", "public", "admin", "scheduled", "tenant", "worker"]


def pascal(value: str) -> str:
    return "".join(part.capitalize() for part in re.split(r"[-_]", value))


def camel(value: str) -> str:
    p = pascal(value)
    return p[0].lower() + p[1:]


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in records) + "\n", encoding="utf-8")


def module_paths(module: ModuleSpec) -> dict[str, str]:
    base = f"src/modules/{module.name}/{module.name}"
    return {name: f"{base}.{name}.ts" for name in ["routes", "controller", "service", "repository", "schema"]}


def generate_project(project: ProjectSpec) -> None:
    root = PROJECTS_DIR / project.project_id
    if root.exists():
        shutil.rmtree(root)
    imports, uses, api_sections, model_sections = [], [], [], []
    for module in project.modules:
        paths = module_paths(module)
        item_pascal = pascal(module.item_name)
        module_pascal = pascal(module.name)
        router = f"{camel(module.item_name)}Router"
        service = f"{camel(module.item_name)}Service"
        repo = f"{camel(module.item_name)}Repository"
        schema = f"create{item_pascal}Schema"
        imports.append(f'import {{ {router} }} from "./modules/{module.name}/{module.name}.routes";')
        uses.append(f'app.use("/{module.name}", auditMiddleware, authMiddleware, {router});')
        write_text(root / paths["schema"], f"""
            import {{ z }} from "zod";
            export const {schema} = z.object({{
              name: z.string().min(2),
              status: z.enum(["draft", "active", "archived"]),
              {module.numeric_field}: z.number().int().min({module.numeric_min}).max({module.numeric_max})
            }});
        """)
        write_text(root / paths["repository"], f"""
            export type {item_pascal} = {{ id: string; name: string; status: "draft" | "active" | "archived"; {module.numeric_field}: number; }};
            const {module.name}: {item_pascal}[] = [{{ id: "{module.item_name}_1", name: "{module.sample_name}", status: "active", {module.numeric_field}: {module.numeric_min} }}];
            export const {repo} = {{
              list() {{ return {module.name}; }},
              create(input: Omit<{item_pascal}, "id">) {{
                const saved = {{ id: `{module.item_name}_${{{module.name}.length + 1}}`, ...input }};
                {module.name}.push(saved);
                return saved;
              }}
            }};
        """)
        write_text(root / paths["service"], f"""
            import {{ {repo} }} from "./{module.name}.repository";
            export const {service} = {{
              list{module_pascal}() {{ return {repo}.list(); }},
              create{item_pascal}(input: {{ name: string; status: "draft" | "active" | "archived"; {module.numeric_field}: number }}) {{
                return {repo}.create(input);
              }}
            }};
        """)
        write_text(root / paths["controller"], f"""
            import {{ Request, Response }} from "express";
            import {{ {schema} }} from "./{module.name}.schema";
            import {{ {service} }} from "./{module.name}.service";
            export function list{module_pascal}(_req: Request, res: Response) {{ res.status(200).json({{ data: {service}.list{module_pascal}() }}); }}
            export function create{item_pascal}(req: Request, res: Response) {{
              const input = {schema}.parse(req.body);
              const result = {service}.create{item_pascal}(input);
              res.status(201).json({{ data: result }});
            }}
        """)
        write_text(root / paths["routes"], f"""
            import {{ Router }} from "express";
            import {{ create{item_pascal}, list{module_pascal} }} from "./{module.name}.controller";
            export const {router} = Router();
            {router}.get("/", list{module_pascal});
            {router}.post("/", create{item_pascal});
        """)
        api_sections.append(f"## {module.display_name}\n\n### GET /{module.name}\n\nReturns all {module.name}.\n\n### POST /{module.name}\n\nCreates a {module.item_name}.\n\n- `{module.numeric_field}`: integer, minimum {module.numeric_min}, maximum {module.numeric_max}\n")
        model_sections.append(f"## {item_pascal} DTO\n\nFields: `id`, `name`, `status`, `{module.numeric_field}`.\n")
    write_text(root / "src/middleware/auth.ts", "export function authMiddleware(_req, _res, next) { next(); }")
    write_text(root / "src/middleware/audit.ts", "export function auditMiddleware(_req, _res, next) { next(); }")
    write_text(root / "src/middleware/error.ts", "export function errorMiddleware(error, _req, res, _next) { res.status(500).json({ error: String(error) }); }")
    write_text(root / "src/middleware/rateLimit.ts", "export function rateLimit(_options) { return (_req, _res, next) => next(); }")
    for term in VARIANTS:
        write_text(root / f"src/jobs/{term}.job.ts", f"export function run{pascal(term)}Job() {{ return '{term}'; }}")
    write_text(root / "src/config.ts", "export const config = { apiTimeoutMs: Number(process.env.API_TIMEOUT_MS ?? 5000), jwtAudience: process.env.JWT_AUDIENCE ?? 'local' };")
    write_text(root / "src/app.ts", f"""
        import express from "express";
        import {{ authMiddleware }} from "./middleware/auth";
        import {{ auditMiddleware }} from "./middleware/audit";
        {chr(10).join(imports)}
        export const app = express();
        app.use(express.json());
        {chr(10).join(uses)}
        app.get("/health", (_req, res) => res.status(200).json({{ status: "ok" }}));
    """)
    write_text(root / ".env.example", "API_TIMEOUT_MS=5000\nJWT_AUDIENCE=docguard-local\nENABLE_AUDIT_LOG=true")
    write_text(root / "package.json", json.dumps({
        "name": project.project_id, "version": "0.3.0", "private": True, "type": "module",
        "scripts": {"dev": "tsx watch src/server.ts", "test": "vitest run", "typecheck": "tsc --noEmit", "lint": "eslint src --ext .ts", "seed": "tsx scripts/seed.ts"},
        "dependencies": {"express": "^4.18.3", "zod": "^3.23.8"},
        "devDependencies": {"@types/express": "^4.17.21", "tsx": "^4.7.1", "typescript": "^5.4.5", "vitest": "^1.5.0", "eslint": "^8.57.0"},
    }, indent=2))
    write_text(root / "README.md", f"""
        # {project.title}

        Synthetic REST API project for DocGuard v0.3 examples.

        ## Install
        `npm install`

        ## Development
        Backend: `npm run dev`

        Local setup uses `.env.example`, in-memory repositories, and synthetic middleware. Some examples mention frontend/backend startup notes for projects that add UI-facing flows.

        ## Test
        `npm test`

        ## Typecheck
        `npm run typecheck`
    """)
    write_text(root / "CHANGELOG.md", "# Changelog\n\n## 0.3.0\n\n- Added richer documentation surfaces for dataset v0.3.")
    write_text(root / "docs/api.md", f"# {project.title} API Reference\n\n" + "\n".join(api_sections))
    write_text(root / "docs/architecture.md", f"# {project.title} Architecture\n\nRequests pass through auth, audit, configuration, route, controller, service, and repository layers.")
    write_text(root / "docs/models.md", f"# {project.title} Models\n\n" + "\n".join(model_sections))
    write_text(root / "docs/developer-setup.md", "# Developer Setup\n\nRun `npm install`, copy `.env.example`, then run `npm run dev`.")
    write_text(root / "docs/workflows.md", "# Workflows\n\nDomain workflows are orchestrated in service modules.")
    write_text(root / "docs/configuration.md", "# Configuration\n\nEnvironment variables: `API_TIMEOUT_MS`, `JWT_AUDIENCE`, `ENABLE_AUDIT_LOG`.")
    write_text(root / "docs/testing.md", "# Testing\n\nRun `npm test` for the synthetic test suite.")


def enrich(record: dict, *, category: str, level: str, files: list[str], reason: str, intent: str) -> dict:
    record["doc_category"] = category
    record["change_level"] = level
    record["affected_documentation_files"] = files
    record["primary_documentation_reason"] = reason
    record["change_intent_summary"] = intent
    return record


def base_record(project: ProjectSpec, module: ModuleSpec, index: int, scenario: str, positive: bool, target: str, section: str) -> dict:
    return {
        "id": f"{project.project_id}-{index:03d}",
        "project_id": project.project_id,
        "scenario_type": scenario,
        "docs_update_required": positive,
        "target_doc_file": target,
        "target_section": section,
        "tags": [module.name, scenario],
    }


def positive_record(project: ProjectSpec, module: ModuleSpec, index: int, scenario: str, category: str, target: str, section: str, changed_files: list[str], diff: str, before: str, facts: list[str], patch: str, after: str, level: str = "medium") -> dict:
    record = base_record(project, module, index, scenario, True, target, section)
    record.update({
        "change_summary": facts[0],
        "changed_files": changed_files,
        "code_diff": diff,
        "docs_before_excerpt": before,
        "expected_facts": facts,
        "gold_doc_patch": patch,
        "docs_after_gold_excerpt": after,
        "negative_reason": None,
        "difficulty": "hard" if level == "high" else "medium",
    })
    return enrich(record, category=category, level=level, files=[target], reason=f"{scenario} changes documented behavior or workflow.", intent="The change modifies project behavior, developer workflow, data contract, or API behavior that readers rely on.")


def negative_record_v3(project: ProjectSpec, module: ModuleSpec, index: int, scenario: str, target: str, changed_file: str, diff: str, reason: str) -> dict:
    record = base_record(project, module, index, scenario, False, target, "Internal Notes")
    record.update({
        "change_summary": reason,
        "changed_files": [changed_file],
        "code_diff": diff,
        "docs_before_excerpt": "No documented behavior changed.",
        "expected_facts": [],
        "gold_doc_patch": None,
        "docs_after_gold_excerpt": "No documented behavior changed.",
        "negative_reason": reason,
        "difficulty": "easy",
    })
    return enrich(record, category="workflow_documentation", level="low", files=[target], reason=reason, intent="The change is internal or cosmetic and does not alter documented behavior.")


def record_for(project: ProjectSpec, module: ModuleSpec, index: int, global_index: int) -> dict:
    scenario = SCENARIO_SEQUENCE[global_index % len(SCENARIO_SEQUENCE)]
    cycle = global_index // len(SCENARIO_SEQUENCE)
    term = VARIANTS[cycle % len(VARIANTS)]
    paths = module_paths(module)
    item = pascal(module.item_name)
    router = f"{camel(module.item_name)}Router"
    service = f"{camel(module.item_name)}Service"
    repo = f"{camel(module.item_name)}Repository"
    endpoint = f"POST /{module.name}"
    api_target = "docs/api.md"

    api_map = {
        "new_endpoint": (f"diff --git a/{paths['routes']} b/{paths['routes']}\n@@\n+{router}.get(\"/{term}/:id\", get{item}{pascal(term)});", f"GET /{module.name}/{term}/:id endpoint exists"),
        "changed_validation_min": (f"diff --git a/{paths['schema']} b/{paths['schema']}\n@@\n-  {module.numeric_field}: z.number().int().min({module.numeric_min})\n+  {module.numeric_field}: z.number().int().min({module.numeric_min + cycle + 1})", f"{endpoint} {module.numeric_field} minimum is {module.numeric_min + cycle + 1}"),
        "changed_auth_requirement": (f"diff --git a/{paths['routes']} b/{paths['routes']}\n@@\n-{router}.post(\"/\", create{item});\n+{router}.post(\"/\", require{item}{pascal(term)}Access, create{item});", f"{endpoint} requires {term} access middleware"),
        "added_response_field": (f"diff --git a/{paths['repository']} b/{paths['repository']}\n@@\n+  {module.response_field}{pascal(term)}: string;", f"{endpoint} response includes {module.response_field}{pascal(term)}"),
        "removed_endpoint": (f"diff --git a/{paths['routes']} b/{paths['routes']}\n@@\n-{router}.get(\"/legacy-{term}\", listLegacy{item});", f"GET /{module.name}/legacy-{term} endpoint was removed"),
        "changed_endpoint_path": (f"diff --git a/{paths['routes']} b/{paths['routes']}\n@@\n-{router}.get(\"/old-{term}\", list{pascal(module.name)});\n+{router}.get(\"/active-{term}\", list{pascal(module.name)});", f"GET path changed from /{module.name}/old-{term} to /{module.name}/active-{term}"),
        "changed_http_method": (f"diff --git a/{paths['routes']} b/{paths['routes']}\n@@\n-{router}.post(\"/{term}\", create{item});\n+{router}.patch(\"/{term}\", create{item});", f"/{module.name}/{term} now uses PATCH"),
        "added_request_field": (f"diff --git a/{paths['schema']} b/{paths['schema']}\n@@\n+  {term}Note: z.string().optional()", f"{endpoint} accepts {term}Note"),
        "removed_request_field": (f"diff --git a/{paths['schema']} b/{paths['schema']}\n@@\n-  legacy{pascal(term)}Code: z.string().optional(),", f"{endpoint} no longer accepts legacy{pascal(term)}Code"),
        "changed_validation_max": (f"diff --git a/{paths['schema']} b/{paths['schema']}\n@@\n-  {module.numeric_field}: z.number().int().max({module.numeric_max + 10})\n+  {module.numeric_field}: z.number().int().max({module.numeric_max})", f"{endpoint} {module.numeric_field} maximum is {module.numeric_max}"),
        "changed_enum_values": (f"diff --git a/{paths['schema']} b/{paths['schema']}\n@@\n-  status: z.enum(['draft','active','archived'])\n+  status: z.enum(['draft','active','{term}'])", f"{endpoint} status enum includes {term}"),
        "changed_status_code": (f"diff --git a/{paths['controller']} b/{paths['controller']}\n@@\n-  res.status(201).json({{ data: result }});\n+  res.status(202).json({{ data: result }});", f"{endpoint} returns 202"),
        "changed_error_response": (f"diff --git a/{paths['controller']} b/{paths['controller']}\n@@\n-  return res.status(400).json({{ error: \"Invalid request\" }});\n+  return res.status(400).json({{ error: \"{pascal(term)} validation failed\" }});", f"{endpoint} error 400 is {pascal(term)} validation failed"),
        "deprecated_endpoint": (f"diff --git a/{paths['routes']} b/{paths['routes']}\n@@\n+// Deprecated: GET /{module.name}/legacy-{term} will be removed on 2027-01-01", f"GET /{module.name}/legacy-{term} is deprecated"),
    }
    if scenario in api_map:
        diff, fact = api_map[scenario]
        if term not in fact:
            fact = f"{fact} for {term} workflow"
        return positive_record(project, module, index, scenario, "api_reference", api_target, module.display_name, [paths["routes"] if "Router" in diff else paths["schema"] if "z." in diff else paths["controller"] if "res.status" in diff else paths["repository"]], diff, f"## {module.display_name}", [fact], f"@@ {module.display_name}\n+{fact}.", f"{fact}.", "medium")

    high_map = {
        "added_middleware_flow": ("architecture_flow", "docs/architecture.md", "Request Flow", [paths["routes"], "src/middleware/audit.ts"], f"+{router}.use(audit{pascal(term)}Middleware);", f"Request flow now includes {term} audit middleware."),
        "changed_auth_flow": ("architecture_flow", "docs/architecture.md", "Authentication Flow", ["src/middleware/auth.ts"], f"-validateBearerToken(req)\n+validateApiKey(req); requireRole(req, \"{term}\")", f"Authentication now uses API key plus {term} role check."),
        "added_dto_model": ("model_contract", "docs/models.md", f"{item}{pascal(term)} DTO", [paths["schema"]], f"+export const {item}{pascal(term)}Dto = z.object({{ id: z.string(), mode: z.literal(\"{term}\") }});", f"{item}{pascal(term)} DTO includes id and mode fields."),
        "changed_dto_field_semantics": ("model_contract", "docs/models.md", f"{item} DTO", [paths["schema"]], f"-  status: z.enum(['draft','active'])\n+  status: z.enum(['draft','active','{term}']) // {term} means externally synchronized", f"`status` semantics now include {term} synchronized state."),
        "changed_run_command": ("developer_setup", "docs/developer-setup.md", "Development Command", ["package.json"], "-\"dev\": \"tsx src/app.ts\"\n+\"dev\": \"tsx watch src/server.ts\"", "Development now uses `tsx watch src/server.ts`."),
        "changed_test_command": ("testing_instructions", "docs/testing.md", "Test Command", ["package.json"], "-\"test\": \"jest\"\n+\"test\": \"vitest run --coverage\"", "Tests now run with `vitest run --coverage`."),
        "added_environment_variable": ("configuration", "docs/configuration.md", "Environment Variables", [".env.example", "src/config.ts"], f"+{term.upper()}_FEATURE_FLAG=true", f"`{term.upper()}_FEATURE_FLAG` configures the {term} feature."),
        "changed_local_development_flow": ("developer_setup", "docs/developer-setup.md", "Local Development Flow", ["README.md"], "+Run `npm run seed` before `npm run dev` for local data.", "Local development now requires seed before dev."),
        "added_background_job_flow": ("workflow_documentation", "docs/workflows.md", "Background Jobs", [f"src/jobs/{term}.job.ts"], f"+scheduleJob(\"{term}\", \"*/5 * * * *\")", f"A scheduled {term} background job runs every five minutes."),
        "changed_error_handling_flow": ("architecture_flow", "docs/architecture.md", "Error Handling", ["src/middleware/error.ts"], f"-return res.status(500).json({{ error }})\n+return res.status(500).json({{ code: \"{term.upper()}_ERROR\", error }})", f"Global errors now include `{term.upper()}_ERROR` codes."),
        "added_service_orchestration_flow": ("workflow_documentation", "docs/workflows.md", "Service Orchestration", [paths["service"]], f"+await {service}.reserve{pascal(term)}();\n+await {service}.notify{pascal(term)}();", f"{module.display_name} workflow now reserves and notifies in sequence."),
        "changed_caching_or_rate_limit_flow": ("architecture_flow", "docs/architecture.md", "Caching And Rate Limits", ["src/middleware/rateLimit.ts", "src/config.ts"], f"+app.use(rateLimit({{ key: \"{term}\", limit: 100 }}));", f"{term} rate limiting is applied in middleware."),
    }
    if scenario in high_map:
        category, target, section, files, diff_body, fact = high_map[scenario]
        if term not in fact.lower():
            fact = f"{fact} This applies to the {term} development context."
        diff = "\n".join(f"diff --git a/{f} b/{f}" for f in files) + f"\n@@\n{diff_body}"
        return positive_record(project, module, index, scenario, category, target, section, files, diff, f"## {section}", [fact], f"@@ {section}\n+{fact}", fact, "high")

    negative_reasons = {
        "internal_refactor": "Internal implementation naming changed without API or workflow behavior changes.",
        "docs_already_updated": "The documentation update is already present in the same diff.",
        "formatting_only": "Only formatting changed; documented behavior is unchanged.",
        "test_only_change": "Only tests changed; runtime behavior and documentation remain valid.",
        "comment_only_change": "Only comments changed; no user-visible behavior changed.",
        "dependency_config_change": "Dependency metadata changed without command or behavior changes.",
        "rename_private_helper": "A private helper was renamed without changing documented flow.",
        "internal_service_logic_no_api_change": "Internal service logic changed without documented behavior changes.",
        "internal_variable_rename_no_behavior_change": "A local variable was renamed without behavior changes.",
        "private_helper_refactor_no_flow_change": "Private helper internals changed but the documented flow is the same.",
        "formatting_only_in_docs_or_code": "Whitespace and formatting changed only.",
        "dev_dependency_patch_no_command_change": "A dev dependency patch did not change setup commands.",
        "test_assertion_refactor_no_behavior_change": "Test assertions were refactored without behavior changes.",
        "comments_reworded_no_contract_change": "Comments were reworded without changing contracts.",
        "log_message_change_no_user_visible_behavior": "Log message text changed but users and developers follow the same docs.",
        "internal_performance_refactor_no_documented_behavior_change": "Performance refactor kept documented behavior unchanged.",
    }
    changed = paths["service"] if "helper" in scenario or "internal" in scenario else "package.json" if "dependency" in scenario else paths["controller"]
    diff = f"diff --git a/{changed} b/{changed}\n@@\n-const {term}Value = compute();\n+const {term}Result = compute();"
    return negative_record_v3(project, module, index, scenario, "docs/workflows.md", changed, diff, negative_reasons[scenario])


def build_records() -> list[dict]:
    records = []
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
    raise ValueError(project_id)


def write_splits(records: list[dict]) -> None:
    buckets = {"train": [], "validation": [], "test": []}
    for record in records:
        buckets[split_name(record["project_id"])].append(record)
    for split, rows in buckets.items():
        write_jsonl(DATA_DIR / f"{split}.jsonl", rows)


def write_schema() -> None:
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "DocGuardDatasetRecord",
        "type": "object",
        "additionalProperties": False,
        "required": [
            "id", "project_id", "scenario_type", "docs_update_required", "change_summary", "changed_files", "code_diff",
            "docs_before_excerpt", "target_doc_file", "target_section", "expected_facts", "gold_doc_patch",
            "docs_after_gold_excerpt", "negative_reason", "difficulty", "tags", "doc_category", "change_level",
            "affected_documentation_files", "primary_documentation_reason", "change_intent_summary",
        ],
        "properties": {field: {"type": "string"} for field in ["id", "project_id", "scenario_type", "change_summary", "code_diff", "docs_before_excerpt", "target_doc_file", "target_section", "docs_after_gold_excerpt", "difficulty", "doc_category", "change_level", "primary_documentation_reason", "change_intent_summary"]},
    }
    schema["properties"].update({
        "docs_update_required": {"type": "boolean"},
        "changed_files": {"type": "array", "items": {"type": "string"}, "minItems": 1},
        "expected_facts": {"type": "array", "items": {"type": "string"}},
        "gold_doc_patch": {"anyOf": [{"type": "string"}, {"type": "null"}]},
        "negative_reason": {"anyOf": [{"type": "string"}, {"type": "null"}]},
        "tags": {"type": "array", "items": {"type": "string"}},
        "affected_documentation_files": {"type": "array", "items": {"type": "string"}, "minItems": 1},
    })
    (DATA_DIR / "schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")


def write_reports(records: list[dict]) -> None:
    scenario_counts = Counter(r["scenario_type"] for r in records)
    category_counts = Counter(r["doc_category"] for r in records)
    split_counts = Counter(split_name(r["project_id"]) for r in records)
    pos = sum(1 for r in records if r["docs_update_required"])
    lines = [
        "# Dataset Statistics", "", "Dataset v0.3 with API, architecture, model, setup, testing, configuration, and workflow documentation targets.", "",
        "| Metric | Value |", "| --- | ---: |", f"| Projects | {len(PROJECTS)} |", f"| Records | {len(records)} |",
        f"| Positive records | {pos} |", f"| Negative records | {len(records)-pos} |", f"| Train records | {split_counts['train']} |",
        f"| Validation records | {split_counts['validation']} |", f"| Test records | {split_counts['test']} |", "", "## Scenario Counts", "",
    ]
    lines += [f"- `{k}`: {v}" for k, v in sorted(scenario_counts.items())]
    lines += ["", "## Documentation Category Counts", ""]
    lines += [f"- `{k}`: {v}" for k, v in sorted(category_counts.items())]
    (REPORTS_DIR / "dataset_statistics.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    checks = [
        "# Quality Checks", "", "The validation script checks:", "", "- at least 2500 records exist",
        "- required legacy and v0.3 fields are present", "- documentation categories and change levels are valid",
        "- duplicate ids and duplicate semantic records do not exist", "- labels match positive/negative scenario groups",
        "- positive records include expected facts and gold patches", "- negative records include clear reasons and no gold patches",
        "- target and affected documentation files exist", "- project-level split leakage is absent",
    ]
    (REPORTS_DIR / "quality_checks.md").write_text("\n".join(checks) + "\n", encoding="utf-8")
    summary = [
        "# Dataset v0.3 Summary", "", "Dataset v0.3 moves beyond endpoint reference updates into broader software project documentation maintenance.",
        "", "## What v0.3 Adds Beyond v0.2", "", "- Architecture and middleware flow scenarios", "- DTO/model contract scenarios",
        "- Developer setup, run command, testing, and configuration scenarios", "- Workflow and background job documentation scenarios",
        "- Higher-level negative examples where code changes should not update docs", "", "## Documentation Categories", "",
        *[f"- `{c}`" for c in sorted(DOC_CATEGORIES)], "", "## Example High-Level Updates", "",
        "- New middleware flow updates `docs/architecture.md`.", "- Added DTO/model updates `docs/models.md`.",
        "- Changed test command updates `docs/testing.md`.", "- Added environment variable updates `docs/configuration.md`.",
        "", "## Why v0.3 Is More Realistic", "", "Real projects require documentation for workflows, setup, configuration, architecture, and data contracts, not only API endpoint references.",
        "", "## Limitations", "", "- Still synthetic and template generated.", "- Generated diffs are simpler than real pull requests.", "- Manual semantic audit remains necessary.",
    ]
    (REPORTS_DIR / "dataset_v0_3_summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")


def main() -> int:
    DATA_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)
    PROJECTS_DIR.mkdir(exist_ok=True)
    for project in PROJECTS:
        generate_project(project)
    records = build_records()
    write_jsonl(DATA_DIR / "docguard_dataset.jsonl", records)
    write_splits(records)
    write_schema()
    write_reports(records)
    print(f"Generated {len(PROJECTS)} projects and {len(records)} records for dataset v0.3.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
