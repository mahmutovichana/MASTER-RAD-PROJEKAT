from __future__ import annotations

import argparse
import json
import shutil
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORTS_DIR = ROOT / "reports"
PROJECTS_DIR = ROOT / "generated_projects"
SCHEMA_DIR = ROOT / "schema"

DOC_FILES = {
    "api_reference": "docs/api.md",
    "architecture_flow": "docs/architecture.md",
    "model_contract": "docs/models.md",
    "developer_setup": "docs/developer-setup.md",
    "testing_instructions": "docs/testing.md",
    "configuration": "docs/configuration.md",
    "workflow_documentation": "docs/workflows.md",
    "changelog": "CHANGELOG.md",
}
DOC_CATEGORIES = [*DOC_FILES, "no_update"]

POSITIVE_SCENARIOS = [
    "added_environment_variable",
    "removed_environment_variable",
    "changed_default_config_value",
    "changed_local_development_flow",
    "changed_seed_or_setup_flow",
    "added_background_job_flow",
    "changed_background_job_schedule",
    "added_service_orchestration_flow",
    "changed_error_handling_flow",
    "changed_caching_or_rate_limit_flow",
    "changed_middleware_auth_flow",
    "added_dto_model_field",
    "removed_dto_model_field",
    "changed_validation_min",
    "changed_validation_max",
    "changed_enum_values",
    "changed_test_command",
    "changed_testing_framework",
    "changelog_worthy_behavior_change",
    "new_endpoint",
    "removed_endpoint",
    "changed_endpoint_path",
    "changed_http_method",
    "changed_status_code",
    "changed_auth_requirement",
    "added_request_field",
    "removed_request_field",
    "added_response_field",
    "removed_response_field",
]
NEGATIVE_SCENARIOS = [
    "internal_variable_rename_no_behavior_change",
    "private_helper_refactor_no_flow_change",
    "formatting_only_in_docs_or_code",
    "comments_reworded_no_contract_change",
    "test_assertion_refactor_no_behavior_change",
    "dev_dependency_patch_no_command_change",
    "log_message_change_no_user_visible_behavior",
    "internal_performance_refactor_no_documented_behavior_change",
    "docs_already_updated",
    "config_refactor_no_new_env_var",
    "route_implementation_refactor_no_contract_change",
    "helper_extraction_no_behavior_change",
    "type_alias_rename_no_contract_change",
]

POSITIVE_ROUTING = {
    "added_environment_variable": ("configuration", "Environment Variables", ["src/config.ts", ".env.example"], "+REVIEW_FEATURE_FLAG=true"),
    "removed_environment_variable": ("configuration", "Environment Variables", ["src/config.ts", ".env.example"], "-LEGACY_REVIEW_FLAG=true"),
    "changed_default_config_value": ("configuration", "Defaults", ["src/config.ts"], "-DEFAULT_PAGE_SIZE=25\n+DEFAULT_PAGE_SIZE=50"),
    "changed_local_development_flow": ("developer_setup", "Local Development", ["package.json", "README.md"], "+Run npm run seed before npm run dev."),
    "changed_seed_or_setup_flow": ("developer_setup", "Seed Data", ["scripts/seed.ts", "README.md"], "+Seed demo review queues before local startup."),
    "added_background_job_flow": ("workflow_documentation", "Background Jobs", ["src/jobs/review.job.ts"], "+scheduleJob('review-digest', '*/5 * * * *')"),
    "changed_background_job_schedule": ("workflow_documentation", "Background Jobs", ["src/jobs/review.job.ts"], "-0 * * * *\n+*/15 * * * *"),
    "added_service_orchestration_flow": ("workflow_documentation", "Service Orchestration", ["src/modules/tickets/tickets.service.ts"], "+await reserveReview();\n+await notifyReviewer();"),
    "changed_error_handling_flow": ("architecture_flow", "Error Handling", ["src/middleware/error.ts"], "+return res.status(500).json({ code: 'REVIEW_ERROR' })"),
    "changed_caching_or_rate_limit_flow": ("architecture_flow", "Caching And Rate Limits", ["src/middleware/rateLimit.ts"], "+rateLimit({ key: 'review', limit: 100 })"),
    "changed_middleware_auth_flow": ("architecture_flow", "Authentication Flow", ["src/middleware/auth.ts"], "+requireRole(req, 'reviewer')"),
    "added_dto_model_field": ("model_contract", "Ticket DTO", ["src/modules/tickets/tickets.schema.ts"], "+reviewerId: z.string().uuid()"),
    "removed_dto_model_field": ("model_contract", "Ticket DTO", ["src/modules/tickets/tickets.schema.ts"], "-legacyReviewerCode: z.string()"),
    "changed_validation_min": ("api_reference", "Ticket API", ["src/modules/tickets/tickets.schema.ts"], "-title: z.string().min(3)\n+title: z.string().min(10)"),
    "changed_validation_max": ("api_reference", "Ticket API", ["src/modules/tickets/tickets.schema.ts"], "-summary: z.string().max(500)\n+summary: z.string().max(280)"),
    "changed_enum_values": ("api_reference", "Ticket API", ["src/modules/tickets/tickets.schema.ts"], "+status: z.enum(['open','closed','reviewing'])"),
    "changed_test_command": ("testing_instructions", "Test Command", ["package.json"], "-\"test\": \"jest\"\n+\"test\": \"vitest run --coverage\""),
    "changed_testing_framework": ("testing_instructions", "Testing Framework", ["package.json"], "-jest\n+vitest"),
    "changelog_worthy_behavior_change": ("changelog", "Changed", ["src/modules/tickets/tickets.service.ts"], "+notifyCustomersAboutReviewWindow()"),
    "new_endpoint": ("api_reference", "Ticket API", ["src/modules/tickets/tickets.routes.ts"], "+router.post('/reviews', createReview)"),
    "removed_endpoint": ("api_reference", "Ticket API", ["src/modules/tickets/tickets.routes.ts"], "-router.get('/legacy-reviews', listLegacyReviews)"),
    "changed_endpoint_path": ("api_reference", "Ticket API", ["src/modules/tickets/tickets.routes.ts"], "-router.get('/review')\n+router.get('/reviews')"),
    "changed_http_method": ("api_reference", "Ticket API", ["src/modules/tickets/tickets.routes.ts"], "-router.post('/reviews')\n+router.patch('/reviews/:id')"),
    "changed_status_code": ("api_reference", "Ticket API", ["src/modules/tickets/tickets.controller.ts"], "-res.status(201)\n+res.status(202)"),
    "changed_auth_requirement": ("api_reference", "Ticket API", ["src/modules/tickets/tickets.routes.ts"], "+router.post('/reviews', requireReviewer, createReview)"),
    "added_request_field": ("api_reference", "Ticket API", ["src/modules/tickets/tickets.schema.ts"], "+reviewReason: z.string()"),
    "removed_request_field": ("api_reference", "Ticket API", ["src/modules/tickets/tickets.schema.ts"], "-legacyReason: z.string()"),
    "added_response_field": ("api_reference", "Ticket API", ["src/modules/tickets/tickets.controller.ts"], "+reviewStatus: 'queued'"),
    "removed_response_field": ("api_reference", "Ticket API", ["src/modules/tickets/tickets.controller.ts"], "-legacyReviewStatus"),
}


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")


def project_ids() -> list[str]:
    return [f"docguard-v04-project-{i:02d}-api" for i in range(1, 31)]


def create_project(project_id: str) -> None:
    root = PROJECTS_DIR / project_id
    if root.exists():
        shutil.rmtree(root)
    files = {
        "src/config.ts": "export const config = { REVIEW_FEATURE_FLAG: process.env.REVIEW_FEATURE_FLAG === 'true' };",
        ".env.example": "REVIEW_FEATURE_FLAG=true\nDEFAULT_PAGE_SIZE=25",
        "package.json": json.dumps({"scripts": {"dev": "tsx watch src/server.ts", "seed": "tsx scripts/seed.ts", "test": "vitest run"}}, indent=2),
        "README.md": f"# {project_id}\n\nRun npm install and npm run dev.",
        "scripts/seed.ts": "export function seed() { return 'seeded'; }",
        "src/jobs/review.job.ts": "export function scheduleJob() { return 'review'; }",
        "src/middleware/error.ts": "export function errorMiddleware() {}",
        "src/middleware/rateLimit.ts": "export function rateLimit() {}",
        "src/middleware/auth.ts": "export function requireReviewer() {}",
        "src/modules/tickets/tickets.service.ts": "export function reserveReview() {}\nexport function notifyReviewer() {}",
        "src/modules/tickets/tickets.schema.ts": "export const ticketSchema = {};",
        "src/modules/tickets/tickets.routes.ts": "export const router = { get() {}, post() {}, patch() {} };",
        "src/modules/tickets/tickets.controller.ts": "export function createReview(_req, res) { res.status(201).json({}); }",
        "docs/api.md": "# API Reference\n\n## Ticket API",
        "docs/architecture.md": "# Architecture\n\n## Request Flow",
        "docs/models.md": "# Models\n\n## Ticket DTO",
        "docs/developer-setup.md": "# Developer Setup\n\n## Local Development",
        "docs/testing.md": "# Testing\n\n## Test Command",
        "docs/configuration.md": "# Configuration\n\n## Environment Variables",
        "docs/workflows.md": "# Workflows\n\n## Background Jobs",
        "CHANGELOG.md": "# Changelog\n\n## Changed",
    }
    for rel, content in files.items():
        write_text(root / rel, content)


def split_for_project(index: int) -> str:
    if index <= 21:
        return "train"
    if index <= 26:
        return "validation"
    return "test"


def positive_record(project_id: str, split: str, seq: int, scenario: str, variant: int) -> dict:
    category, section, files, diff_body = POSITIVE_ROUTING[scenario]
    target = DOC_FILES[category]
    fact = f"{scenario} affects {section} for review flow variant {variant}"
    return {
        "id": f"{project_id}-{seq:03d}",
        "project_id": project_id,
        "split": split,
        "scenario_type": scenario,
        "docs_update_required": True,
        "change_summary": fact,
        "changed_files": files,
        "code_diff": "\n".join(f"diff --git a/{file} b/{file}" for file in files) + f"\n@@\n{diff_body}\n+// variant {variant}",
        "docs_before_excerpt": f"## {section}\nExisting documentation for {section}.",
        "target_doc_file": target,
        "target_section": section,
        "expected_facts": [fact],
        "gold_doc_patch": f"@@ {section}\n+{fact}.",
        "generated_doc_patch": f"@@ {section}\n+{fact}.",
        "docs_after_gold_excerpt": f"## {section}\nExisting documentation for {section}.\n{fact}.",
        "negative_reason": None,
        "difficulty": "medium",
        "tags": [scenario, category, f"variant_{variant}"],
        "doc_category": category,
        "change_level": "medium",
        "affected_documentation_files": [target],
        "primary_documentation_reason": f"{scenario} changes documented behavior.",
        "change_intent_summary": fact,
    }


def negative_record(project_id: str, split: str, seq: int, scenario: str, variant: int) -> dict:
    changed_file = {
        "dev_dependency_patch_no_command_change": "package.json",
        "test_assertion_refactor_no_behavior_change": "tests/tickets.test.ts",
        "docs_already_updated": "docs/api.md",
        "config_refactor_no_new_env_var": "src/config.ts",
        "route_implementation_refactor_no_contract_change": "src/modules/tickets/tickets.routes.ts",
        "type_alias_rename_no_contract_change": "src/modules/tickets/tickets.schema.ts",
    }.get(scenario, "src/modules/tickets/tickets.service.ts")
    # Ensure changed files exist even for tests.
    write_text(PROJECTS_DIR / project_id / changed_file, f"// {scenario}")
    reason = f"{scenario} does not change documented behavior for variant {variant}."
    return {
        "id": f"{project_id}-{seq:03d}",
        "project_id": project_id,
        "split": split,
        "scenario_type": scenario,
        "docs_update_required": False,
        "change_summary": reason,
        "changed_files": [changed_file],
        "code_diff": f"diff --git a/{changed_file} b/{changed_file}\n@@\n-const internalName{variant} = compute();\n+const renamedInternalName{variant} = compute();",
        "docs_before_excerpt": "No documentation-relevant behavior changed.",
        "target_doc_file": "",
        "target_section": "",
        "expected_facts": [],
        "gold_doc_patch": None,
        "generated_doc_patch": None,
        "docs_after_gold_excerpt": "No documentation-relevant behavior changed.",
        "negative_reason": reason,
        "difficulty": "hard",
        "tags": [scenario, "no_update", f"variant_{variant}"],
        "doc_category": "no_update",
        "change_level": "low",
        "affected_documentation_files": [],
        "primary_documentation_reason": reason,
        "change_intent_summary": reason,
    }


def build_v0_4_records() -> list[dict]:
    records: list[dict] = []
    pos_i = neg_i = 0
    for project_index, project_id in enumerate(project_ids(), start=1):
        split = split_for_project(project_index)
        create_project(project_id)
        for seq in range(1, 201):
            variant = (project_index * 1000) + seq
            if seq % 2:
                scenario = POSITIVE_SCENARIOS[pos_i % len(POSITIVE_SCENARIOS)]
                records.append(positive_record(project_id, split, seq, scenario, variant))
                pos_i += 1
            else:
                scenario = NEGATIVE_SCENARIOS[neg_i % len(NEGATIVE_SCENARIOS)]
                records.append(negative_record(project_id, split, seq, scenario, variant))
                neg_i += 1
    return records


def write_schema() -> None:
    SCHEMA_DIR.mkdir(exist_ok=True)
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "DocGuardRecordV04",
        "type": "object",
        "required": [
            "id", "project_id", "split", "scenario_type", "docs_update_required", "change_summary",
            "changed_files", "code_diff", "docs_before_excerpt", "target_doc_file", "target_section",
            "expected_facts", "gold_doc_patch", "generated_doc_patch", "docs_after_gold_excerpt",
            "negative_reason", "difficulty", "tags", "doc_category", "change_level",
            "affected_documentation_files", "primary_documentation_reason", "change_intent_summary",
        ],
    }
    text = json.dumps(schema, indent=2)
    write_text(DATA_DIR / "schema.json", text)
    write_text(SCHEMA_DIR / "docguard_record.schema.json", text)


def write_v0_4_reports(records: list[dict]) -> None:
    REPORTS_DIR.mkdir(exist_ok=True)
    scenario_counts = Counter(r["scenario_type"] for r in records)
    category_counts = Counter(r["doc_category"] for r in records)
    split_counts = Counter(r["split"] for r in records)
    pos = sum(r["docs_update_required"] for r in records)
    lines = [
        "# Dataset v0.4 Summary",
        "",
        "DocGuard v0.4 is a CPU-first dataset version for hybrid documentation consistency experiments.",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Projects | {len(project_ids())} |",
        f"| Records | {len(records)} |",
        f"| Positive records | {pos} |",
        f"| Negative records | {len(records) - pos} |",
        f"| Train records | {split_counts['train']} |",
        f"| Validation records | {split_counts['validation']} |",
        f"| Test records | {split_counts['test']} |",
        "",
        "## Documentation Categories",
        "",
        *[f"- `{k}`: {v}" for k, v in sorted(category_counts.items())],
        "",
        "## Scenario Types",
        "",
        *[f"- `{k}`: {v}" for k, v in sorted(scenario_counts.items())],
        "",
        "## v0.4 Design Notes",
        "",
        "- Negative records use `doc_category=no_update` and empty target documentation fields.",
        "- Positive fine-grained metrics are evaluated separately from negative binary classification.",
        "- The dataset is balanced 50/50 for binary documentation-update detection.",
        "- The intended baseline path is signal routing plus CPU ML, with small LLMs optional.",
    ]
    write_text(REPORTS_DIR / "dataset_v0_4_summary.md", "\n".join(lines))
    write_text(REPORTS_DIR / "v0_3_to_v0_4_changes.md", "# v0.3 to v0.4 Changes\n\n- Froze v0.3 artifacts.\n- Expanded to 30 projects and 6000 v0.4 records.\n- Added `no_update` category for negatives.\n- Added CPU-first hybrid and ML evaluation path.\n")
    write_text(REPORTS_DIR / "hybrid_methodology.md", "# Hybrid Methodology\n\nDocGuard v0.4 prioritizes CPU-friendly signal extraction, deterministic routing, and classical ML classifiers. The LLM is optional and used only after candidate reduction.\n")
    write_text(REPORTS_DIR / "cpu_real_llm_plan_v0_4.md", "# CPU Real LLM Plan v0.4\n\nNo GPU is available locally. `qwen2_5_coder_0_5b` with `transformers_local` is used only for CPU real pipeline validation. Main v0.4 quality improvements come from signal routing, CPU ML classifiers, and hybrid validation. Optional llama.cpp/GGUF can be configured for better CPU inference without requiring it in default checks.\n")


def write_active_dataset(records: list[dict]) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    write_jsonl(DATA_DIR / "docguard_dataset.jsonl", records)
    for split in ["train", "validation", "test"]:
        write_jsonl(DATA_DIR / f"{split}.jsonl", [r for r in records if r["split"] == split])


def build_v0_4() -> None:
    PROJECTS_DIR.mkdir(exist_ok=True)
    records = build_v0_4_records()
    write_active_dataset(records)
    write_schema()
    write_v0_4_reports(records)
    print(f"Generated v0.4 dataset: {len(project_ids())} projects, {len(records)} records.")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", default="v0_4", choices=["v0_4"])
    args = parser.parse_args()
    if args.version == "v0_4":
        build_v0_4()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
