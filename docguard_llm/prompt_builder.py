from __future__ import annotations

import json
import re
from pathlib import Path

from docguard_llm.config import PATCH_DOC_CATEGORIES, PATCH_TARGET_FILES
from docguard_llm.prompt_templates import get_patch_template


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
    if prompt_mode == "hybrid_compact":
        return build_hybrid_compact_prompt(record)
    raise ValueError(f"Unsupported prompt mode: {prompt_mode}")


def build_hybrid_compact_prompt(record: dict) -> list[dict]:
    from docguard_hybrid.doc_router import route

    routed = route(record)
    system = "You are DocGuard. Return strict JSON only. Use only the provided candidates."
    user_payload = {
        "task": "Verify the routed documentation decision and produce a concise JSON prediction.",
        "changed_files": record["changed_files"],
        "code_diff": record["code_diff"],
        "docs_before_excerpt": record["docs_before_excerpt"],
        "extracted_signals": routed["signals"],
        "router_candidate_doc_categories": routed["candidate_doc_categories"],
        "router_candidate_target_doc_files": routed["candidate_target_doc_files"],
        "router_candidate_scenario_types": routed["candidate_scenario_types"],
        "router_reason": routed["router_reason"],
        "expected_output_json_schema": output_schema_text(),
    }
    return [{"role": "system", "content": system}, {"role": "user", "content": json.dumps(user_payload, indent=2)}]


def build_sanity_prompt() -> list[dict]:
    return [
        {"role": "system", "content": "Return JSON only."},
        {"role": "user", "content": 'Return only this JSON: {"ok": true}'},
    ]


def _extract_prompt_tokens(code_diff: str) -> list[str]:
    tokens: list[str] = []
    patterns = [
        r"['\"](/[A-Za-z0-9_:{}/-]+)['\"]",
        r"\b([A-Z][A-Z0-9_]{3,})\b",
        r"\b(npm run [A-Za-z0-9:_-]+)\b",
        r"^\+\s*([A-Za-z_][A-Za-z0-9_]*Id)\b",
        r"['\"](\*/\d+ \* \* \* \*)['\"]",
        r"res\.status\((\d{3})\)",
        r"requireRole\(['\"]([^'\"]+)['\"]\)",
    ]
    for pattern in patterns:
        for match in re.finditer(pattern, code_diff, flags=re.MULTILINE):
            token = match.group(1)
            if token not in tokens:
                tokens.append(token)
    return tokens


def build_patch_prompt(
    *,
    code_diff: str,
    docs_before: str,
    target_doc_file: str,
    doc_category: str,
    scenario_type: str,
    signals: list[str],
    router_reason: str,
    project_id: str,
    target_section: str | None = None,
) -> tuple[str, dict]:
    if doc_category not in PATCH_DOC_CATEGORIES:
        raise ValueError(f"Unsupported patch doc_category: {doc_category}")
    if target_doc_file not in PATCH_TARGET_FILES:
        raise ValueError(f"Unsupported patch target_doc_file: {target_doc_file}")
    tokens = _extract_prompt_tokens(code_diff)
    metadata = {
        "project_id": project_id,
        "target_doc_file": target_doc_file,
        "doc_category": doc_category,
        "scenario_type": scenario_type,
        "signals": list(signals),
        "router_reason": router_reason,
        "target_section": target_section or "",
        "grounding_tokens": tokens,
        "forbidden_inputs_excluded": [
            "gold labels",
            "expected facts",
            "expected patch summary",
            "docs-after text",
            "manual notes",
        ],
    }
    prompt = "\n".join(
        [
            get_patch_template(doc_category),
            "",
            f"Project id: {project_id}",
            f"Target document: {target_doc_file}",
            f"Target section: {target_section or target_doc_file}",
            f"Documentation category: {doc_category}",
            f"Router scenario hint: {scenario_type}",
            f"Detected signals: {', '.join(signals) or 'none'}",
            f"Router reason: {router_reason}",
            f"Concrete tokens extracted from diff: {', '.join(tokens) or 'none'}",
            "",
            "Current documentation:",
            "```md",
            docs_before.strip(),
            "```",
            "",
            "Code diff:",
            "```diff",
            code_diff.strip(),
            "```",
            "",
            "Return only the Markdown patch.",
        ]
    )
    return prompt, metadata
