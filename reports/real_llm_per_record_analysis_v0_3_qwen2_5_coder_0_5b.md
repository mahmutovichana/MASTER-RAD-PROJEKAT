# Real LLM Per-Record Analysis v0.3: qwen2_5_coder_0_5b

- prediction_file: `data\llm_predictions_v0_3_validation_transformers_local_qwen2_5_coder_0_5b.jsonl`
- records: 10
- docs_update_required F1: 100.00%
- doc_category accuracy: 10.00%
- target_doc_file accuracy: 10.00%
- scenario_type accuracy: 0.00%
- parse errors: 0
- average latency seconds: 22.17

## 1. support-ticket-api-001

- gold docs_update_required: `True`
- predicted docs_update_required: `True`
- gold scenario_type: `added_environment_variable`
- raw scenario_type: `API Change`
- normalized scenario_type: `unknown_change`
- gold doc_category: `configuration`
- raw doc_category: `Configuration`
- normalized doc_category: `configuration`
- gold target_doc_file: `docs/configuration.md`
- raw target_doc_file: `docs/configuration.md`
- normalized target_doc_file: `docs/configuration.md`
- parse_error: `False`
- latency_seconds: `22.240508499999123`
- interpretation: **semantically close**

Raw output excerpt:

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

## 2. support-ticket-api-002

- gold docs_update_required: `True`
- predicted docs_update_required: `True`
- gold scenario_type: `changed_local_development_flow`
- raw scenario_type: `integration`
- normalized scenario_type: `unknown_change`
- gold doc_category: `developer_setup`
- raw doc_category: `API`
- normalized doc_category: `api_reference`
- gold target_doc_file: `docs/developer-setup.md`
- raw target_doc_file: `README.md`
- normalized target_doc_file: `README.md`
- parse_error: `False`
- latency_seconds: `18.77996390000044`
- interpretation: **wrong category and target file**

Raw output excerpt:

```text
```json
{
  "docs_update_required": true,
  "scenario_type": "integration",
  "doc_category": "API",
  "target_doc_file": "README.md",
  "target_section": "Local Development Flow",
  "generated_doc_patch": null,
  "change_intent_summary": "This change adds a step to the README file to ensure that local data is properly seeded before running the development server.",
  "primary_documentation_reason": "It provides a clear and concise explanation of the purpose of the change.",
  "expected_facts_covered": [],
  "confidence": 0.9
}
```
```

## 3. support-ticket-api-003

- gold docs_update_required: `True`
- predicted docs_update_required: `True`
- gold scenario_type: `added_background_job_flow`
- raw scenario_type: `integration`
- normalized scenario_type: `unknown_change`
- gold doc_category: `workflow_documentation`
- raw doc_category: `API`
- normalized doc_category: `api_reference`
- gold target_doc_file: `docs/workflows.md`
- raw target_doc_file: `docs/api.md`
- normalized target_doc_file: `docs/api.md`
- parse_error: `False`
- latency_seconds: `20.27663240000038`
- interpretation: **wrong category and target file**

Raw output excerpt:

```text
```json
{
  "docs_update_required": true,
  "scenario_type": "integration",
  "doc_category": "API",
  "target_doc_file": "docs/api.md",
  "target_section": "Background Jobs",
  "generated_doc_patch": null,
  "change_intent_summary": "Integrates a scheduled job to review jobs.",
  "primary_documentation_reason": "The scheduled job is added to the background jobs section of the API documentation.",
  "expected_facts_covered": [],
  "confidence": 0.9
}
```
```

## 4. support-ticket-api-004

- gold docs_update_required: `True`
- predicted docs_update_required: `True`
- gold scenario_type: `changed_error_handling_flow`
- raw scenario_type: `integration`
- normalized scenario_type: `unknown_change`
- gold doc_category: `architecture_flow`
- raw doc_category: `middleware`
- normalized doc_category: `middleware`
- gold target_doc_file: `docs/architecture.md`
- raw target_doc_file: `src/middleware/error.ts`
- normalized target_doc_file: `src/middleware/error.ts`
- parse_error: `False`
- latency_seconds: `22.626519299999927`
- interpretation: **wrong category and target file**

Raw output excerpt:

```text
```json
{
  "docs_update_required": true,
  "scenario_type": "integration",
  "doc_category": "middleware",
  "target_doc_file": "src/middleware/error.ts",
  "target_section": "error handling",
  "generated_doc_patch": null,
  "change_intent_summary": "The error handling middleware should return a 500 status code with a custom error message.",
  "primary_documentation_reason": "This change introduces a new error handling mechanism that returns a custom error message.",
  "expected_facts_covered": [],
  "confidence": 0.9
}
```
```

## 5. support-ticket-api-005

- gold docs_update_required: `True`
- predicted docs_update_required: `True`
- gold scenario_type: `added_service_orchestration_flow`
- raw scenario_type: `integration`
- normalized scenario_type: `unknown_change`
- gold doc_category: `workflow_documentation`
- raw doc_category: `API`
- normalized doc_category: `api_reference`
- gold target_doc_file: `docs/workflows.md`
- raw target_doc_file: `src/modules/tickets/tickets.service.ts`
- normalized target_doc_file: `src/modules/tickets/tickets.service.ts`
- parse_error: `False`
- latency_seconds: `23.159321099999943`
- interpretation: **wrong category and target file**

Raw output excerpt:

```text
```json
{
  "docs_update_required": true,
  "scenario_type": "integration",
  "doc_category": "API",
  "target_doc_file": "src/modules/tickets/tickets.service.ts",
  "target_section": "reserveReview and notifyReview methods",
  "generated_doc_patch": null,
  "change_intent_summary": "The `reserveReview` and `notifyReview` methods are responsible for managing review requests, so they need to be documented.",
  "primary_documentation_reason": "These methods are part of the ticket management service and are crucial for handling user requests.",
  "expected_facts_covered": [],
  "confidence": 0.9
}
```
```

## 6. support-ticket-api-006

- gold docs_update_required: `True`
- predicted docs_update_required: `True`
- gold scenario_type: `changed_caching_or_rate_limit_flow`
- raw scenario_type: `integration`
- normalized scenario_type: `unknown_change`
- gold doc_category: `architecture_flow`
- raw doc_category: `API`
- normalized doc_category: `api_reference`
- gold target_doc_file: `docs/architecture.md`
- raw target_doc_file: `src/middleware/rateLimit.ts`
- normalized target_doc_file: `src/middleware/ratelimit.ts`
- parse_error: `False`
- latency_seconds: `21.997801400000753`
- interpretation: **wrong category and target file**

Raw output excerpt:

```text
```json
{
  "docs_update_required": true,
  "scenario_type": "integration",
  "doc_category": "API",
  "target_doc_file": "src/middleware/rateLimit.ts",
  "target_section": "Rate Limiting",
  "generated_doc_patch": null,
  "change_intent_summary": "Added rate limiting middleware to handle requests with high rates.",
  "primary_documentation_reason": "This change enhances the reliability of the API by limiting the number of requests per second.",
  "expected_facts_covered": [],
  "confidence": 0.9
}
```
```

## 7. support-ticket-api-007

- gold docs_update_required: `False`
- predicted docs_update_required: `False`
- gold scenario_type: `internal_variable_rename_no_behavior_change`
- raw scenario_type: `API Change`
- normalized scenario_type: `unknown_change`
- gold doc_category: `workflow_documentation`
- raw doc_category: `API`
- normalized doc_category: `api_reference`
- gold target_doc_file: `docs/workflows.md`
- raw target_doc_file: `src/modules/tickets/tickets.service.ts`
- normalized target_doc_file: `src/modules/tickets/tickets.service.ts`
- parse_error: `False`
- latency_seconds: `22.68247479999991`
- interpretation: **wrong category and target file**

Raw output excerpt:

```text
```json
{
  "docs_update_required": false,
  "scenario_type": "API Change",
  "doc_category": "API",
  "target_doc_file": "src/modules/tickets/tickets.service.ts",
  "target_section": "compute function",
  "generated_doc_patch": null,
  "change_intent_summary": "The `compute` function has been updated to return a `ReviewResult` object instead of a string.",
  "primary_documentation_reason": "This change does not affect the functionality of the `tickets.service.ts` file.",
  "expected_facts_covered": [],
  "confidence": 0.9
}
```
```

## 8. support-ticket-api-008

- gold docs_update_required: `False`
- predicted docs_update_required: `False`
- gold scenario_type: `private_helper_refactor_no_flow_change`
- raw scenario_type: `API Change`
- normalized scenario_type: `unknown_change`
- gold doc_category: `workflow_documentation`
- raw doc_category: `API`
- normalized doc_category: `api_reference`
- gold target_doc_file: `docs/workflows.md`
- raw target_doc_file: `src/modules/comments/comments.service.ts`
- normalized target_doc_file: `src/modules/comments/comments.service.ts`
- parse_error: `False`
- latency_seconds: `23.608732299999247`
- interpretation: **wrong category and target file**

Raw output excerpt:

```text
```json
{
  "docs_update_required": false,
  "scenario_type": "API Change",
  "doc_category": "API",
  "target_doc_file": "src/modules/comments/comments.service.ts",
  "target_section": "compute function",
  "generated_doc_patch": null,
  "change_intent_summary": "The `compute` function in the `comments.service.ts` file has been updated to return a different value.",
  "primary_documentation_reason": "This change does not affect the functionality of the API, so no additional documentation is needed.",
  "expected_facts_covered": [],
  "confidence": 0.9
}
```
```

## 9. support-ticket-api-009

- gold docs_update_required: `False`
- predicted docs_update_required: `False`
- gold scenario_type: `formatting_only_in_docs_or_code`
- raw scenario_type: `API Change`
- normalized scenario_type: `unknown_change`
- gold doc_category: `workflow_documentation`
- raw doc_category: `API`
- normalized doc_category: `api_reference`
- gold target_doc_file: `docs/workflows.md`
- raw target_doc_file: `src/modules/tickets/tickets.controller.ts`
- normalized target_doc_file: `src/modules/tickets/tickets.controller.ts`
- parse_error: `False`
- latency_seconds: `25.2727143000011`
- interpretation: **wrong category and target file**

Raw output excerpt:

```text
```json
{
  "docs_update_required": false,
  "scenario_type": "API Change",
  "doc_category": "API",
  "target_doc_file": "src/modules/tickets/tickets.controller.ts",
  "target_section": "compute function",
  "generated_doc_patch": null,
  "change_intent_summary": "The `compute` function has been updated to return a `reviewResult` instead of `reviewValue`. This change does not require any documentation updates.",
  "primary_documentation_reason": "The `compute` function is used to determine the review result, which is a common operation in ticket management systems.",
  "expected_facts_covered": [],
  "confidence": 0.9
}
```
```

## 10. support-ticket-api-010

- gold docs_update_required: `False`
- predicted docs_update_required: `False`
- gold scenario_type: `dev_dependency_patch_no_command_change`
- raw scenario_type: `API Change`
- normalized scenario_type: `unknown_change`
- gold doc_category: `workflow_documentation`
- raw doc_category: `API Documentation`
- normalized doc_category: `api_documentation`
- gold target_doc_file: `docs/workflows.md`
- raw target_doc_file: `docs/api.md`
- normalized target_doc_file: `docs/api.md`
- parse_error: `False`
- latency_seconds: `21.041251399998146`
- interpretation: **wrong category and target file**

Raw output excerpt:

```text
{
  "docs_update_required": false,
  "scenario_type": "API Change",
  "doc_category": "API Documentation",
  "target_doc_file": "docs/api.md",
  "target_section": "Compute Function",
  "generated_doc_patch": null,
  "change_intent_summary": "The `compute()` function has been updated to return a different value.",
  "primary_documentation_reason": "This change does not affect the functionality of the API.",
  "expected_facts_covered": [],
  "confidence": 0.9
}
```
