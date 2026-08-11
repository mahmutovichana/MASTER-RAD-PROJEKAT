from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE_DIR = ROOT / "generated_live_demo_projects" / "project_evolution"
DATA_PATH = ROOT / "data" / "live_flow" / "docguard_project_evolution_cases.jsonl"

DOCS = {
    "docs/api.md": "# API Reference\n\nExisting endpoints are documented here.\n",
    "docs/models.md": "# Models\n\nCore DTOs and response contracts are documented here.\n",
    "docs/configuration.md": "# Configuration\n\nDATABASE_URL and service-specific queue names are required.\n",
    "docs/testing.md": "# Testing\n\nRun `npm test` for the default test suite.\n",
    "docs/workflows.md": "# Workflows\n\nBackground jobs run on the default hourly schedule.\n",
    "docs/architecture.md": "# Architecture\n\nRequests pass through auth middleware and service-level rate limits.\n",
    "docs/developer-setup.md": "# Developer Setup\n\nRun `npm install`, then `npm run dev`.\n",
    "CHANGELOG.md": "# Changelog\n\n## Unreleased\n\n- Baseline service scaffold.\n",
}

PROJECTS = {
    "atlas_review_api": {
        "description": "TypeScript/Express-like review management API.",
        "files": {
            "src/routes/reviews.ts": "router.get('/reviews/:id', getReview);\n",
            "src/models/review.ts": "export interface Review { id: string; status: string; }\n",
            "src/config/env.ts": "export const default_page_size = 25;\n",
            "src/jobs/reviewScheduler.ts": "export const schedule = '0 * * * *';\n",
            "src/middleware/auth.ts": "export const requireRole = (role: string) => role;\n",
            "package.json": '{"scripts":{"test":"jest","dev":"tsx src/server.ts"}}\n',
            **DOCS,
        },
    },
    "beacon_billing_service": {
        "description": "Billing and invoice service with REST-style routes and background invoice jobs.",
        "files": {
            "src/routes/invoices.ts": "router.get('/invoices/:id', getInvoice);\n",
            "src/models/invoice.ts": "export interface Invoice { id: string; status: string; }\n",
            "src/config/billingEnv.ts": "export const default_page_size = 50;\n",
            "src/jobs/invoiceScheduler.ts": "export const schedule = '0 * * * *';\n",
            "src/middleware/auth.ts": "export const requireRole = (role: string) => role;\n",
            "package.json": '{"scripts":{"test":"jest","dev":"tsx src/server.ts"}}\n',
            **DOCS,
        },
    },
    "nova_task_platform": {
        "description": "Task and workflow automation service.",
        "files": {
            "src/routes/tasks.ts": "router.get('/tasks/:id', getTask);\n",
            "src/models/task.ts": "export interface Task { id: string; state: string; }\n",
            "src/config/taskEnv.ts": "export const default_page_size = 20;\n",
            "src/jobs/taskScheduler.ts": "export const schedule = '0 * * * *';\n",
            "src/middleware/auth.ts": "export const requireRole = (role: string) => role;\n",
            "package.json": '{"scripts":{"test":"jest","dev":"tsx src/server.ts"}}\n',
            **DOCS,
        },
    },
}


def case(
    project_id: str,
    sequence: int,
    pr_title: str,
    code_changed_files: list[str],
    code_diff: str,
    docs_before: str,
    required: bool,
    category: str,
    target: str,
    section: str,
    facts: list[str],
    summary: str,
    scenario: str,
    difficulty: str,
    notes: str,
) -> dict[str, Any]:
    return {
        "case_id": f"{project_id.upper().replace('_', '-')}-PR-{sequence:02d}",
        "project_id": project_id,
        "pr_title": pr_title,
        "sequence_number": sequence,
        "code_changed_files": code_changed_files,
        "code_diff": code_diff.strip() + "\n",
        "docs_before": docs_before,
        "gold_docs_update_required": required,
        "gold_doc_category": category,
        "gold_target_doc_file": target,
        "gold_target_section": section,
        "expected_facts": facts,
        "expected_patch_summary": summary,
        "scenario_type": scenario,
        "change_summary": summary,
        "difficulty": difficulty,
        "realism_notes": notes,
    }


def project_cases() -> list[dict[str, Any]]:
    d = DOCS
    return [
        case("atlas_review_api", 1, "Add review creation endpoint", ["src/routes/reviews.ts", "src/models/review.ts"], "+router.post('/reviews', createReview);\n+res.status(201).json({ id: saved.id, reviewStatus: saved.status });", d["docs/api.md"], True, "api_reference", "docs/api.md", "Reviews", ["POST /reviews creates a review."], "Document new POST /reviews endpoint.", "new_endpoint", "easy", "Route addition plus response status."),
        case("atlas_review_api", 2, "Tighten review comment validation", ["src/routes/reviews.ts"], "-comment: z.string().min(3).max(500)\n+comment: z.string().min(10).max(280)", d["docs/api.md"], True, "api_reference", "docs/api.md", "Reviews", ["Review comment min is 10 and max is 280."], "Update documented review comment validation.", "changed_validation_min", "medium", "Min/max change in request validation."),
        case("atlas_review_api", 3, "Expose reviewer id in review DTO", ["src/models/review.ts"], " export interface ReviewDto {\n   id: string;\n+reviewerId: string;\n   status: string;\n }", d["docs/models.md"], True, "model_contract", "docs/models.md", "ReviewDto", ["ReviewDto includes reviewerId."], "Document reviewerId in model contract.", "added_dto_model_field", "easy", "DTO field added."),
        case("atlas_review_api", 4, "Add review feature flag", ["src/config/env.ts"], "+export const REVIEW_FEATURE_FLAG = process.env.REVIEW_FEATURE_FLAG === 'enabled';", d["docs/configuration.md"], True, "configuration", "docs/configuration.md", "Environment Variables", ["REVIEW_FEATURE_FLAG toggles review rollout."], "Document REVIEW_FEATURE_FLAG.", "added_environment_variable", "easy", "New env var."),
        case("atlas_review_api", 5, "Run review scheduler every fifteen minutes", ["src/jobs/reviewScheduler.ts"], "-scheduleJob('0 * * * *', runReviewScheduler);\n+scheduleJob('*/15 * * * *', runReviewScheduler);", d["docs/workflows.md"], True, "workflow_documentation", "docs/workflows.md", "Review Scheduler", ["Review scheduler runs every 15 minutes."], "Update scheduler workflow frequency.", "changed_background_job_schedule", "medium", "Background job schedule change."),
        case("atlas_review_api", 6, "Rename local accumulator", ["src/routes/reviews.ts"], "-const totalReviews = reviews.length;\n+const renamedInternalTotal = reviews.length;", d["docs/api.md"], False, "no_update", "", "", [], "Internal variable rename only.", "internal_variable_rename_no_behavior_change", "easy", "No behavior or docs contract change."),
        case("atlas_review_api", 7, "Switch tests to Vitest", ["package.json", "vitest.config.ts"], '-  "test": "jest"\n+  "test": "vitest run"\n+  "test:watch": "vitest"', d["docs/testing.md"], True, "testing_instructions", "docs/testing.md", "Testing", ["Tests now run with vitest."], "Update test command documentation.", "changed_test_command", "easy", "Test command changed."),
        case("atlas_review_api", 8, "Documented endpoint already updated", ["src/routes/reviews.ts"], "+router.post('/reviews', createReview);\n+// docs/api.md already contains POST /reviews in this PR context", "POST /reviews is already documented with request and response examples.", False, "no_update", "", "", [], "Docs already aligned for the endpoint change.", "docs_already_updated", "hard", "A realistic no-update case that would fool route keyword matching."),
        case("beacon_billing_service", 1, "Add invoice payment endpoint", ["src/routes/invoices.ts"], "+router.post('/invoices/:id/payments', createInvoicePayment);\n+res.status(202).json({ paymentId, reviewStatus: 'queued' });", d["docs/api.md"], True, "api_reference", "docs/api.md", "Invoices", ["POST /invoices/:id/payments queues payment."], "Document invoice payment endpoint.", "new_endpoint", "medium", "New endpoint and async status."),
        case("beacon_billing_service", 2, "Add invoice reviewer field", ["src/models/invoice.ts"], " export interface InvoiceDto {\n   id: string;\n+reviewerId: string;\n   totalCents: number;\n }", d["docs/models.md"], True, "model_contract", "docs/models.md", "InvoiceDto", ["InvoiceDto includes reviewerId."], "Document invoice reviewerId.", "added_dto_model_field", "easy", "Model contract change."),
        case("beacon_billing_service", 3, "Change billing page size default", ["src/config/billingEnv.ts"], "-export const default_page_size = 50;\n+export const default_page_size = 100;", d["docs/configuration.md"], True, "configuration", "docs/configuration.md", "Defaults", ["Default billing page size is 100."], "Update default page size docs.", "changed_default_config_value", "medium", "Default config value change."),
        case("beacon_billing_service", 4, "Require billing role on invoice routes", ["src/middleware/auth.ts", "src/routes/invoices.ts"], "+router.post('/invoices/:id/payments', requireRole('billing'), createInvoicePayment);\n+const guard = requireRole('billing');", d["docs/architecture.md"], True, "architecture_flow", "docs/architecture.md", "Authorization", ["Invoice payment route requires billing role."], "Document billing role middleware behavior.", "changed_middleware_auth_flow", "medium", "Auth middleware behavior change."),
        case("beacon_billing_service", 5, "Add invoice export seed command", ["package.json", "scripts/seedInvoices.ts"], '+  "seed:invoices": "npm run seed -- invoices"\n+console.log("npm run seed prepares invoice demo data");', d["docs/developer-setup.md"], True, "developer_setup", "docs/developer-setup.md", "Seed Data", ["Invoice demo data uses npm run seed."], "Document invoice seed flow.", "changed_local_development_flow", "easy", "Local setup command changed."),
        case("beacon_billing_service", 6, "Refactor invoice formatting helper", ["src/routes/invoices.ts"], "+function privateFormatInvoiceTotal(totalCents: number) { return totalCents.toString(); }\n const label = privateFormatInvoiceTotal(totalCents);", d["docs/api.md"], False, "no_update", "", "", [], "Private helper extraction only.", "private_helper_refactor_no_flow_change", "medium", "Internal helper extraction."),
        case("beacon_billing_service", 7, "Notify customers about invoice review window", ["src/jobs/invoiceScheduler.ts"], "+export function notifyCustomersAboutReviewWindow() {\n+  return sendInvoiceReviewWindowNotifications();\n+}", d["CHANGELOG.md"], True, "changelog", "CHANGELOG.md", "Unreleased", ["Customers are notified about invoice review windows."], "Mention customer notification behavior in changelog.", "changelog_worthy_behavior_change", "medium", "Behavior change suited to changelog."),
        case("beacon_billing_service", 8, "Clean up log message", ["src/routes/invoices.ts"], "-logger.info('invoice paid')\n+logger.info('invoice payment accepted')", d["docs/api.md"], False, "no_update", "", "", [], "Logging message wording only.", "log_message_change_no_user_visible_behavior", "easy", "Log-only change."),
        case("nova_task_platform", 1, "Add task archive endpoint", ["src/routes/tasks.ts"], "+router.post('/tasks/:id/archive', archiveTask);\n+res.status(202).json({ reviewStatus: 'archived' });", d["docs/api.md"], True, "api_reference", "docs/api.md", "Tasks", ["POST /tasks/:id/archive archives a task."], "Document task archive endpoint.", "new_endpoint", "easy", "New task endpoint."),
        case("nova_task_platform", 2, "Add task reviewer field", ["src/models/task.ts"], " export interface TaskDto {\n   id: string;\n+reviewerId: string;\n   state: string;\n }", d["docs/models.md"], True, "model_contract", "docs/models.md", "TaskDto", ["TaskDto includes reviewerId."], "Document reviewerId on task model.", "added_dto_model_field", "easy", "Model field added."),
        case("nova_task_platform", 3, "Add task queue env var", ["src/config/taskEnv.ts"], "+export const REVIEW_FEATURE_FLAG = process.env.REVIEW_FEATURE_FLAG || 'task-review-v2';", d["docs/configuration.md"], True, "configuration", "docs/configuration.md", "Environment Variables", ["REVIEW_FEATURE_FLAG controls task review workflow."], "Document task review feature flag.", "added_environment_variable", "easy", "Env var added."),
        case("nova_task_platform", 4, "Add workflow orchestration step", ["src/jobs/taskScheduler.ts", "src/routes/tasks.ts"], "+await reserveReview(task.id);\n+await notifyReviewer(task.assigneeId);", d["docs/workflows.md"], True, "workflow_documentation", "docs/workflows.md", "Task Review Workflow", ["Task review reserves capacity and notifies reviewer."], "Document new workflow orchestration step.", "added_service_orchestration_flow", "hard", "Multi-step orchestration."),
        case("nova_task_platform", 5, "Add route rate limit", ["src/middleware/auth.ts", "src/routes/tasks.ts"], "+const taskArchiveRateLimit = rateLimit({ windowMs: 60000, max: 20 });\n+router.post('/tasks/:id/archive', taskArchiveRateLimit, archiveTask);", d["docs/architecture.md"], True, "architecture_flow", "docs/architecture.md", "Rate Limiting", ["Task archive route has rateLimit max 20."], "Document task archive rate limit.", "changed_caching_or_rate_limit_flow", "medium", "Rate limit middleware."),
        case("nova_task_platform", 6, "Reword internal comments", ["src/models/task.ts"], "-// Calculates task score.\n+// Computes task score for internal ranking.", d["docs/models.md"], False, "no_update", "", "", [], "Comment rewording only.", "comments_reworded_no_contract_change", "easy", "Comments only."),
        case("nova_task_platform", 7, "Refactor test assertion", ["tests/tasks.test.ts"], "-expect(response.body.id).toBeTruthy();\n+expect(response.body).toHaveProperty('id');", d["docs/testing.md"], False, "no_update", "", "", [], "Test assertion refactor only.", "test_assertion_refactor_no_behavior_change", "easy", "Test assertion only."),
        case("nova_task_platform", 8, "Format task env file", ["src/config/taskEnv.ts"], "+// formatting\n export const TASK_QUEUE = 'tasks';", d["docs/configuration.md"], False, "no_update", "", "", [], "Formatting-only config file change.", "formatting_only_in_docs_or_code", "medium", "Formatting could fool config keyword matching."),
    ]


def write_projects(records: list[dict[str, Any]]) -> None:
    for project_id, config in PROJECTS.items():
        root = BASE_DIR / project_id
        for relative, content in config["files"].items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        (root / "README.md").write_text(f"# {project_id}\n\n{config['description']}\n", encoding="utf-8")
        project_records = [item for item in records if item["project_id"] == project_id]
        lines = ["# Evolution Log", "", f"Baseline purpose: {config['description']}", "", "## PR Sequence", ""]
        for item in project_records:
            lines.extend(
                [
                    f"### {item['sequence_number']}. {item['pr_title']}",
                    "",
                    f"- Case: `{item['case_id']}`",
                    f"- Difficulty: `{item['difficulty']}`",
                    f"- Docs update required: `{item['gold_docs_update_required']}`",
                    f"- Expected target doc: `{item['gold_target_doc_file'] or 'none'}`",
                    f"- Change: {item['change_summary']}",
                    "- DocGuard prediction: pending runner execution",
                    "",
                ]
            )
        (root / "evolution_log.md").write_text("\n".join(lines), encoding="utf-8")


def generate_project_evolution_cases(data_path: Path = DATA_PATH) -> list[dict[str, Any]]:
    records = project_cases()
    write_projects(records)
    data_path.parent.mkdir(parents=True, exist_ok=True)
    data_path.write_text("\n".join(json.dumps(item, ensure_ascii=False) for item in records) + "\n", encoding="utf-8")
    return records


if __name__ == "__main__":
    generate_project_evolution_cases()
