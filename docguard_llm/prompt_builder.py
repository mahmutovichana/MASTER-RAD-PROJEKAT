from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

CANDIDATE_DOC_FILES = [
    "docs/api.md",
    "docs/architecture.md",
    "docs/models.md",
    "docs/developer-setup.md",
    "docs/workflows.md",
    "docs/configuration.md",
    "docs/testing.md",
    "README.md",
    "CHANGELOG.md",
]
DOC_CATEGORIES = [
    "api_reference",
    "architecture_flow",
    "model_contract",
    "developer_setup",
    "testing_instructions",
    "configuration",
    "workflow_documentation",
    "changelog",
]
COMMON_VALIDATION_SCENARIOS = [
    "added_environment_variable",
    "changed_local_development_flow",
    "added_background_job_flow",
    "changed_error_handling_flow",
    "added_service_orchestration_flow",
    "changed_caching_or_rate_limit_flow",
    "internal_variable_rename_no_behavior_change",
    "private_helper_refactor_no_flow_change",
    "formatting_only_in_docs_or_code",
    "dev_dependency_patch_no_command_change",
    "test_assertion_refactor_no_behavior_change",
    "comments_reworded_no_contract_change",
    "log_message_change_no_user_visible_behavior",
    "internal_performance_refactor_no_documented_behavior_change",
]
TARGET_FILE_MAPPING = {
    "environment variables/config flags": "docs/configuration.md",
    "local setup/dev commands/install/run/seed": "docs/developer-setup.md",
    "background jobs/scheduled jobs/service orchestration/workflows": "docs/workflows.md",
    "middleware/error handling/rate limiting/caching/auth flow": "docs/architecture.md",
    "DTO/model/schema/data contract": "docs/models.md",
    "tests/test commands/test behavior": "docs/testing.md",
    "API endpoints/request/response/status/auth/validation": "docs/api.md",
    "release/user-facing change summary": "CHANGELOG.md",
}


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def select_few_shot_examples(limit: int = 7) -> list[dict]:
    wanted_categories = [
        "api_reference",
        "architecture_flow",
        "model_contract",
        "developer_setup",
        "configuration",
        "workflow_documentation",
    ]
    examples: list[dict] = []
    seen = set()
    for record in read_jsonl(DATA_DIR / "train.jsonl"):
        category = record["doc_category"]
        if record["docs_update_required"] and category in wanted_categories and category not in seen:
            examples.append(record)
            seen.add(category)
        if len(examples) == len(wanted_categories):
            break
    for record in read_jsonl(DATA_DIR / "train.jsonl"):
        if not record["docs_update_required"]:
            examples.append(record)
            break
    return examples[:limit]


def output_schema_text() -> str:
    return json.dumps(
        {
            "docs_update_required": "boolean",
            "scenario_type": "string",
            "doc_category": "string",
            "target_doc_file": "string",
            "target_section": "string",
            "generated_doc_patch": "string or null",
            "change_intent_summary": "string",
            "primary_documentation_reason": "string",
            "expected_facts_covered": ["string"],
            "confidence": "number between 0 and 1",
        },
        indent=2,
    )


def compact_example(record: dict) -> dict:
    return {
        "input": {
            "changed_files": record["changed_files"],
            "code_diff": record["code_diff"],
            "docs_before_excerpt": record["docs_before_excerpt"],
            "target_section": record["target_section"],
        },
        "output": {
            "docs_update_required": record["docs_update_required"],
            "scenario_type": record["scenario_type"],
            "doc_category": record["doc_category"],
            "target_doc_file": record["target_doc_file"],
            "target_section": record["target_section"],
            "generated_doc_patch": record["gold_doc_patch"],
            "change_intent_summary": record["change_intent_summary"],
            "primary_documentation_reason": record["primary_documentation_reason"],
            "expected_facts_covered": record["expected_facts"],
            "confidence": 0.9,
        },
    }


def build_prompt(record: dict, few_shot_examples: list[dict] | None = None) -> list[dict]:
    examples = few_shot_examples if few_shot_examples is not None else select_few_shot_examples()
    system = (
        "You are DocGuard, an agent for documentation consistency analysis. "
        "Return strict JSON only. Do not add markdown or explanation outside JSON. "
        "Use only facts grounded in code_diff and docs_before_excerpt."
    )
    user_payload = {
        "task": [
            "understand high-level intent",
            "decide if project documentation must be updated",
            "classify scenario_type and doc_category",
            "choose target_doc_file",
            "generate a minimal documentation patch only when needed",
            "avoid hallucinating ungrounded facts",
        ],
        "candidate_documentation_files": CANDIDATE_DOC_FILES,
        "doc_categories": DOC_CATEGORIES,
        "allowed_scenario_types": "Use dataset scenario types when clear; otherwise use unknown_change.",
        "expected_output_json_schema": output_schema_text(),
        "few_shot_examples_from_train_only": [compact_example(example) for example in examples],
        "record": {
            "id": record["id"],
            "changed_files": record["changed_files"],
            "code_diff": record["code_diff"],
            "docs_before_excerpt": record["docs_before_excerpt"],
            "target_section": record["target_section"],
        },
    }
    return [{"role": "system", "content": system}, {"role": "user", "content": json.dumps(user_payload, indent=2)}]


def build_compact_prompt(record: dict) -> list[dict]:
    system = (
        "You are DocGuard. Return strict JSON only. "
        "Use only facts grounded in code_diff and docs_before_excerpt."
    )
    user_payload = {
        "task": "Decide whether this REST API code change requires documentation updates and return the required JSON schema.",
        "candidate_documentation_files": CANDIDATE_DOC_FILES,
        "expected_output_json_schema": output_schema_text(),
        "record": {
            "id": record["id"],
            "changed_files": record["changed_files"],
            "code_diff": record["code_diff"],
            "docs_before_excerpt": record["docs_before_excerpt"],
        },
    }
    return [{"role": "system", "content": system}, {"role": "user", "content": json.dumps(user_payload, indent=2)}]


def build_compact_prompt_v2(record: dict) -> list[dict]:
    system = (
        "You are DocGuard. Return strict JSON only. "
        "Use only facts grounded in code_diff and docs_before_excerpt. "
        "Return exact enum values. Do not invent broad labels such as API Change, integration, API, Configuration, or Workflow."
    )
    user_payload = {
        "task": "Decide whether this REST API code change requires documentation updates and return the required JSON schema.",
        "strict_label_instruction": "Return exact enum values for scenario_type and doc_category. Choose target_doc_file only from candidate_documentation_files.",
        "candidate_documentation_files": CANDIDATE_DOC_FILES,
        "allowed_doc_categories": DOC_CATEGORIES,
        "target_file_mapping": TARGET_FILE_MAPPING,
        "common_validation_scenario_labels": COMMON_VALIDATION_SCENARIOS,
        "negative_change_guidance": "If the change is internal only, formatting only, comments only, tests only, or has no user-visible documented behavior change, set docs_update_required=false and use the closest no-doc-update scenario label.",
        "expected_output_json_schema": output_schema_text(),
        "record": {
            "id": record["id"],
            "changed_files": record["changed_files"],
            "code_diff": record["code_diff"],
            "docs_before_excerpt": record["docs_before_excerpt"],
            "target_section": record["target_section"],
        },
    }
    return [{"role": "system", "content": system}, {"role": "user", "content": json.dumps(user_payload, indent=2)}]


def build_prompt_for_mode(record: dict, prompt_mode: str, few_shot_examples: list[dict] | None = None) -> list[dict]:
    if prompt_mode == "compact":
        return build_compact_prompt(record)
    if prompt_mode == "compact_v2":
        return build_compact_prompt_v2(record)
    if prompt_mode == "full":
        return build_prompt(record, few_shot_examples)
    raise ValueError(f"Unsupported prompt mode: {prompt_mode}")


def build_sanity_prompt() -> list[dict]:
    return [
        {"role": "system", "content": "Return JSON only."},
        {"role": "user", "content": 'Return only this JSON: {"ok": true}'},
    ]
