# Real LLM Smoke Test: qwen2_5_coder_0_5b

- command: `python -m docguard_llm.cli smoke-test --model qwen2_5_coder_0_5b --backend transformers_local`
- backend: transformers_local
- model_key: qwen2_5_coder_0_5b
- model_id: Qwen/Qwen2.5-Coder-0.5B-Instruct
- selected_record_id: support-ticket-api-001
- compact_prompt: True
- sanity_only: False
- prompt_length_characters: 1279
- parse_success: True
- latency_seconds: 23.616968800000905
- last_completed_step: parsed
- generation_started_at: 2026-06-27T15:34:42.388841+00:00
- generation_finished_at: 2026-06-27T15:35:06.006478+00:00
- raw_output_length: 496
- status: succeeded
- output_usable: True

## Prompt Preview

```text
system: You are DocGuard. Return strict JSON only. Use only facts grounded in code_diff and docs_before_excerpt.

user: {
  "task": "Decide whether this REST API code change requires documentation updates and return the required JSON schema.",
  "candidate_documentation_files": [
    "docs/api.md",
    "docs/architecture.md",
    "docs/models.md",
    "docs/developer-setup.md",
    "docs/workflows.md",
    "docs/configuration.md",
    "docs/testing.md",
    "README.md",
    "CHANGELOG.md"
  ],
  "expected_output_json_schema": "{\n  \"docs_update_required\": \"boolean\",\n  \"scenario_type\": \"string\",\n  \"doc_category\": \"string\",\n  \"target_doc_file\": \"string\",\n  \"target_section\": \"string\",\n  \"generated_doc_patch\": \"string or null\",\n  \"change_intent_summary\": \"string\",\n  \"primary_documentation_reason\": \"string\",\n  \"expected_facts_covered\": [\n    \"string\"\n  ],\n  \"confidence\": \"number between 0 and 1\"\n}",
  "record": {
    "id": "support-ticket-api-001",
    "changed_files": [
      ".env.example",
      "src/config.ts"
    ],
    "code_diff": "diff --git a/.env.example b/.env.example\ndiff --git a/src/config.ts b/src/config.ts\n@@\n+REVIEW_FEATURE_FLAG=true",
    "docs_before_excerpt": "## Environment Variables"
  }
}
```

## Raw Model Output

```text
```json
{
  "docs_update_required": true,
  "scenario_type": "API Change",
  "doc_category": "Configuration",
  "target_doc_file": "docs/configuration.md",
  "target_section": "Environment Variables",
  "generated_doc_patch": null,
  "change_intent_summary": "Added a new environment variable `REVIEW_FEATURE_FLAG` to the configuration file.",
  "primary_documentation_reason": "This change affects the configuration of the application.",
  "expected_facts_covered": [],
  "confidence": 0.9
}
```
```

## Parsed Prediction

```json
{
  "docs_update_required": true,
  "scenario_type": "API Change",
  "doc_category": "Configuration",
  "target_doc_file": "docs/configuration.md",
  "target_section": "Environment Variables",
  "generated_doc_patch": null,
  "change_intent_summary": "Added a new environment variable `REVIEW_FEATURE_FLAG` to the configuration file.",
  "primary_documentation_reason": "This change affects the configuration of the application.",
  "expected_facts_covered": [],
  "confidence": 0.9
}
```
