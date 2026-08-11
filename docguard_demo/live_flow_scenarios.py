from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ID = "atlas_review_api"
PROJECT_DIR = ROOT / "generated_live_demo_projects" / PROJECT_ID
DATA_PATH = ROOT / "data" / "live_flow" / "docguard_live_flow_cases.jsonl"

DOCS = {
    "docs/api.md": "# API\n\n## Reviews\n\nExisting review endpoints are documented here.\n",
    "docs/models.md": "# Models\n\nReview contains id, rating, status, and comment.\n",
    "docs/configuration.md": "# Configuration\n\nSet DATABASE_URL and REVIEW_QUEUE_NAME for local use.\n",
    "docs/testing.md": "# Testing\n\nRun `npm test` to execute the Jest suite.\n",
    "docs/workflows.md": "# Workflows\n\nThe review scheduler checks pending reviews hourly.\n",
    "docs/architecture.md": "# Architecture\n\nRequests pass through auth middleware and standard error handling.\n",
    "docs/developer-setup.md": "# Developer Setup\n\nRun `npm install` and `npm run dev`.\n",
    "CHANGELOG.md": "# Changelog\n\n## Unreleased\n\n- Initial review API scaffold.\n",
}


def write_project() -> None:
    files = {
        "src/routes/reviews.ts": "import { Router } from 'express';\nexport const router = Router();\nrouter.get('/reviews/:id', getReview);\n",
        "src/routes/users.ts": "import { Router } from 'express';\nexport const router = Router();\n",
        "src/middleware/auth.ts": "export function requireRole(role: string) { return role; }\nexport const rateLimit = { windowMs: 60000 };\n",
        "src/config/env.ts": "export const REVIEW_QUEUE_NAME = process.env.REVIEW_QUEUE_NAME || 'reviews';\nexport const default_page_size = 25;\n",
        "src/models/review.ts": "export interface Review { id: string; rating: number; status: string; comment?: string }\n",
        "src/jobs/reviewScheduler.ts": "export const reviewSchedule = '0 * * * *';\nexport function notifyCustomersAboutReviewWindow() { return true; }\n",
        "package.json": json.dumps({"scripts": {"dev": "tsx src/server.ts", "test": "jest", "seed": "tsx scripts/seed.ts"}}, indent=2),
        **DOCS,
    }
    for relative, content in files.items():
        path = PROJECT_DIR / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def record(
    case_id: str,
    changed_files: list[str],
    code_diff: str,
    docs_before: str,
    docs_update_required: bool,
    scenario_type: str,
    doc_category: str,
    target_doc_file: str,
    target_section: str,
    expected_facts: list[str],
    change_summary: str,
) -> dict[str, Any]:
    return {
        "id": case_id,
        "project_id": PROJECT_ID,
        "changed_files": changed_files,
        "code_diff": code_diff.strip() + "\n",
        "docs_before": docs_before,
        "docs_update_required": docs_update_required,
        "scenario_type": scenario_type,
        "doc_category": doc_category,
        "target_doc_file": target_doc_file,
        "target_section": target_section,
        "expected_facts": expected_facts,
        "change_summary": change_summary,
    }


def live_flow_records() -> list[dict[str, Any]]:
    return [
        record(
            "LIVE-API-NEW-ENDPOINT",
            ["src/routes/reviews.ts"],
            "+router.post('/reviews', createReview);\n+res.status(201).json({ id: saved.id });",
            DOCS["docs/api.md"],
            True,
            "new_endpoint",
            "api_reference",
            "docs/api.md",
            "Reviews",
            ["Document POST /reviews endpoint."],
            "New review creation endpoint added.",
        ),
        record(
            "LIVE-API-VALIDATION-MIN",
            ["src/routes/reviews.ts"],
            "-body('comment').isLength({ min: 3 })\n+body('comment').isLength({ min: 10 })\n+const schema = z.string().min(10);",
            DOCS["docs/api.md"],
            True,
            "changed_validation_min",
            "api_reference",
            "docs/api.md",
            "Reviews",
            ["Document minimum comment length of 10."],
            "Review comment minimum length changed.",
        ),
        record(
            "LIVE-MODEL-FIELD-ADDED",
            ["src/models/review.ts"],
            " export interface Review {\n   id: string;\n+  reviewerId: string;\n }",
            DOCS["docs/models.md"],
            True,
            "added_dto_model_field",
            "model_contract",
            "docs/models.md",
            "Review",
            ["Document reviewerId on Review model."],
            "Review model now includes reviewerId.",
        ),
        record(
            "LIVE-CONFIG-ENV-VAR",
            ["src/config/env.ts"],
            "+export const REVIEW_FEATURE_FLAG = process.env.REVIEW_FEATURE_FLAG === 'enabled';",
            DOCS["docs/configuration.md"],
            True,
            "added_environment_variable",
            "configuration",
            "docs/configuration.md",
            "Environment Variables",
            ["Document REVIEW_FEATURE_FLAG."],
            "New review feature flag environment variable added.",
        ),
        record(
            "LIVE-TESTING-COMMAND",
            ["package.json"],
            '-    "test": "jest"\n+    "test": "vitest run"\n+    "test:watch": "vitest"',
            DOCS["docs/testing.md"],
            True,
            "changed_test_command",
            "testing_instructions",
            "docs/testing.md",
            "Testing",
            ["Document vitest test command."],
            "Test command changed from Jest to Vitest.",
        ),
        record(
            "LIVE-WORKFLOW-SCHEDULE",
            ["src/jobs/reviewScheduler.ts"],
            "-export const reviewSchedule = '0 * * * *';\n+export const reviewSchedule = '*/15 * * * *';\n+scheduleJob('*/15 * * * *', processReviewWindow);",
            DOCS["docs/workflows.md"],
            True,
            "changed_background_job_schedule",
            "workflow_documentation",
            "docs/workflows.md",
            "Review Scheduler",
            ["Document 15 minute review scheduler."],
            "Review scheduler now runs every 15 minutes.",
        ),
        record(
            "LIVE-ARCH-RATE-LIMIT",
            ["src/middleware/auth.ts"],
            "+export const reviewRateLimit = rateLimit({ windowMs: 60000, max: 30 });\n+export const requireReviewRole = requireRole('reviewer');",
            DOCS["docs/architecture.md"],
            True,
            "changed_caching_or_rate_limit_flow",
            "architecture_flow",
            "docs/architecture.md",
            "Middleware",
            ["Document reviewer role and rateLimit behavior."],
            "Review routes now use role and rate limit middleware.",
        ),
        record(
            "LIVE-DEVELOPER-SEED",
            ["package.json", "scripts/seedReviews.ts"],
            '+    "seed:reviews": "npm run seed -- reviews"\n+console.log("npm run seed creates review demo data");',
            DOCS["docs/developer-setup.md"],
            True,
            "changed_local_development_flow",
            "developer_setup",
            "docs/developer-setup.md",
            "Seed Data",
            ["Document npm run seed for review demo data."],
            "Local setup now includes review seed data.",
        ),
        record(
            "LIVE-CHANGELOG-WORTHY",
            ["src/jobs/reviewScheduler.ts"],
            "+export function notifyCustomersAboutReviewWindow() {\n+  return sendReviewWindowNotifications();\n+}",
            DOCS["CHANGELOG.md"],
            True,
            "changelog_worthy_behavior_change",
            "changelog",
            "CHANGELOG.md",
            "Unreleased",
            ["Mention customer review-window notifications."],
            "Customers are now notified about review windows.",
        ),
        record(
            "LIVE-NEG-VARIABLE-RENAME",
            ["src/routes/reviews.ts"],
            "-const totalReviews = reviews.length;\n+const renamedInternalTotal = reviews.length;",
            DOCS["docs/api.md"],
            False,
            "internal_variable_rename_no_behavior_change",
            "no_update",
            "",
            "",
            [],
            "Internal variable rename without behavior change.",
        ),
        record(
            "LIVE-NEG-HELPER-REFACTOR",
            ["src/routes/reviews.ts"],
            "+function privateNormalizeReview(input) { return input.trim(); }\n const normalized = privateNormalizeReview(comment);",
            DOCS["docs/api.md"],
            False,
            "private_helper_refactor_no_flow_change",
            "no_update",
            "",
            "",
            [],
            "Private helper extraction without flow change.",
        ),
        record(
            "LIVE-NEG-TEST-ASSERTION",
            ["tests/reviews.test.ts"],
            "-expect(response.body.id).toBeTruthy();\n+expect(response.body).toHaveProperty('id');",
            DOCS["docs/testing.md"],
            False,
            "test_assertion_refactor_no_behavior_change",
            "no_update",
            "",
            "",
            [],
            "Test assertion refactor only.",
        ),
        record(
            "LIVE-NEG-COMMENT-REWORDED",
            ["src/models/review.ts"],
            "-// Calculates review score.\n+// Computes review score for internal ranking.",
            DOCS["docs/models.md"],
            False,
            "comments_reworded_no_contract_change",
            "no_update",
            "",
            "",
            [],
            "Comment wording changed without contract change.",
        ),
        record(
            "LIVE-NEG-FORMATTING",
            ["src/config/env.ts"],
            "+// formatting\n const default_page_size = 25;",
            DOCS["docs/configuration.md"],
            False,
            "formatting_only_in_docs_or_code",
            "no_update",
            "",
            "",
            [],
            "Formatting-only code change.",
        ),
        record(
            "LIVE-NEG-DOCS-ALREADY-UPDATED",
            ["docs/api.md"],
            "diff --git a/docs/api.md b/docs/api.md\n+POST /reviews is already documented in this documentation-only change.",
            DOCS["docs/api.md"],
            False,
            "docs_already_updated",
            "no_update",
            "",
            "",
            [],
            "Documentation already updated; no missing patch remains.",
        ),
    ]


def generate_live_flow_cases(data_path: Path = DATA_PATH) -> list[dict[str, Any]]:
    write_project()
    records = live_flow_records()
    data_path.parent.mkdir(parents=True, exist_ok=True)
    data_path.write_text("\n".join(json.dumps(item, ensure_ascii=False) for item in records) + "\n", encoding="utf-8")
    return records


if __name__ == "__main__":
    generate_live_flow_cases()
