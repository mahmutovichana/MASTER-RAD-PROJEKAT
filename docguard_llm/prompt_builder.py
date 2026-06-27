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

