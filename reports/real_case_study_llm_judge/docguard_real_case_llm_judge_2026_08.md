# DocGuard Real Case LLM Judge Evaluation 2026-08

This report evaluates an LLM decision layer on real public GitHub PR case-study records.
The LLM receives only safe input fields and does not receive gold labels, docs-after text, manual notes, manually assigned change type, source URLs, or documentation-file presence from the original PR.

- Input: `data\external\project_case_study\manual_cases.jsonl`
- Backend: `openai_compatible`
- Model: `Qwen/Qwen2.5-Coder-32B-Instruct`

## Input Leakage Policy

Allowed LLM input fields:

- `case_id`
- `code_changed_files`
- `code_diff_excerpt`
- `docs_before_excerpt`
- `language`

Audit-only fields excluded from LLM input:

- `allowed_model_input_fields`
- `audit_only_fields`
- `change_type`
- `changed_files`
- `commit_or_pr`
- `docs_after_excerpt`
- `docs_changed_files`
- `gold_doc_category`
- `gold_docs_update_required`
- `gold_patch_summary`
- `gold_target_doc_file`
- `gold_target_section`
- `label_confidence`
- `manual_label_notes`
- `source_url`

## Metrics

| Metric | Value |
| --- | ---: |
| total cases | 20 |
| true positives | 8 |
| false positives | 0 |
| true negatives | 5 |
| false negatives | 7 |
| binary accuracy | 65.00% |
| precision | 100.00% |
| recall | 53.33% |
| F1 | 69.57% |
| abstentions | 11 |

## Count Summaries

- Decision status counts: `{'ok': 9, 'error': 11}`
- Documentation area counts: `{'configuration': 3, 'data_model': 2, 'no_update': 1, 'api': 2, 'testing': 1, 'error': 11}`
- Gold distribution: `{'True': 15, 'False': 5}`
- Prediction distribution: `{'True': 8, 'False': 12}`

## Per-Case Table

| Case | Gold | Pred | Correct | Status | Confidence | Area | Rationale | Evidence |
| --- | ---: | ---: | ---: | --- | ---: | --- | --- | --- |
| `GH-PROJ-001` | `True` | `True` | `True` | `ok` | `0.8` | `configuration` | The addition of Prisma to the dependencies suggests a change in the database handling or ORM configuration, which could affect how users set up and interact with the database. | "prisma": "^6.2.1", prisma/migrations, prisma/schema.prisma, prisma/seed-data.ts, prisma/seed.ts |
| `GH-PROJ-002` | `True` | `True` | `True` | `ok` | `0.8` | `data_model` | The code diff introduces new types (AgentNextStep, AgentSummary, AgentPaymentWarning) that could affect the data model and its usage, which should be documented. | AgentNextStep, AgentSummary, AgentPaymentWarning |
| `GH-PROJ-003` | `True` | `True` | `True` | `ok` | `0.95` | `data_model` | The code diff introduces a new schema field 'pluginInstallUrlPrefix' which affects the data model and could be relevant to users, developers, or maintainers. | pluginInstallUrlPrefix, schema field |
| `GH-PROJ-004` | `True` | `True` | `True` | `ok` | `0.9` | `configuration` | The diff introduces new configuration options for enabling metrics and setting a metrics token, which would be relevant to users and operators configuring the service. | metrics_enabled, metrics_token |
| `GH-PROJ-005` | `True` | `False` | `False` | `ok` | `0.8` | `no_update` | The code diff introduces an import for \`canonical_omind_exe\` but does not show any usage or changes that would affect user-facing behavior or require documentation. | canonical_omind_exe |
| `GH-PROJ-006` | `True` | `True` | `True` | `ok` | `0.9` | `api` | The diff modifies the description of the rate limiting middleware behavior, which is likely to be relevant to users and developers. | rate-limit setting exists, protection presets decide by environment name, deployment reports false here only if protection setup raised |
| `GH-PROJ-007` | `True` | `True` | `True` | `ok` | `0.8` | `testing` | The diff introduces new fields (max_attempts, payload, schedule) in the test data, which could affect the expected behavior of the tests and should be documented. | max_attempts, payload, schedule |
| `GH-PROJ-008` | `True` | `True` | `True` | `ok` | `0.9` | `configuration` | The diff introduces a new configuration file for LLM generation settings, which affects how advisories are worded and could require updates to the configuration section of the documentation. | advisory_llm.yaml, providers: |
| `GH-PROJ-009` | `True` | `True` | `True` | `ok` | `0.95` | `api` | The code diff changes the endpoint URL from \`/v1/invocations/{task_id}/await\` to \`/v1/tasks/{task_id}/await\`, which is a visible change in the API contract. | GET /v1/invocations/{task_id}/await, GET /v1/tasks/{task_id}/await |
| `GH-PROJ-010` | `True` | `False` | `False` | `error` | `0.0` | `error` | LLM generation failed. |  |
| `GH-PROJ-011` | `True` | `False` | `False` | `error` | `0.0` | `error` | LLM generation failed. |  |
| `GH-PROJ-012` | `True` | `False` | `False` | `error` | `0.0` | `error` | LLM generation failed. |  |
| `GH-PROJ-013` | `True` | `False` | `False` | `error` | `0.0` | `error` | LLM generation failed. |  |
| `GH-PROJ-014` | `True` | `False` | `False` | `error` | `0.0` | `error` | LLM generation failed. |  |
| `GH-PROJ-015` | `True` | `False` | `False` | `error` | `0.0` | `error` | LLM generation failed. |  |
| `GH-PROJ-016` | `False` | `False` | `True` | `error` | `0.0` | `error` | LLM generation failed. |  |
| `GH-PROJ-017` | `False` | `False` | `True` | `error` | `0.0` | `error` | LLM generation failed. |  |
| `GH-PROJ-018` | `False` | `False` | `True` | `error` | `0.0` | `error` | LLM generation failed. |  |
| `GH-PROJ-019` | `False` | `False` | `True` | `error` | `0.0` | `error` | LLM generation failed. |  |
| `GH-PROJ-020` | `False` | `False` | `True` | `error` | `0.0` | `error` | LLM generation failed. |  |

## Error Details

### `GH-PROJ-005`

- Gold docs update required: `True`
- Predicted docs update required: `False`
- Decision status: `ok`
- Confidence: `0.8`
- Documentation area: `no_update`
- Rationale: The code diff introduces an import for `canonical_omind_exe` but does not show any usage or changes that would affect user-facing behavior or require documentation.
- Evidence: `canonical_omind_exe`

Raw decision:

```json
{
  "docs_update_required": false,
  "confidence": 0.8,
  "documentation_area": "no_update",
  "rationale": "The code diff introduces an import for `canonical_omind_exe` but does not show any usage or changes that would affect user-facing behavior or require documentation.",
  "evidence": ["canonical_omind_exe"]
}
```

### `GH-PROJ-010`

- Gold docs update required: `True`
- Predicted docs update required: `False`
- Decision status: `error`
- Confidence: `0.0`
- Documentation area: `error`
- Rationale: LLM generation failed.
- Evidence: ``

Raw decision:

```json

```

### `GH-PROJ-011`

- Gold docs update required: `True`
- Predicted docs update required: `False`
- Decision status: `error`
- Confidence: `0.0`
- Documentation area: `error`
- Rationale: LLM generation failed.
- Evidence: ``

Raw decision:

```json

```

### `GH-PROJ-012`

- Gold docs update required: `True`
- Predicted docs update required: `False`
- Decision status: `error`
- Confidence: `0.0`
- Documentation area: `error`
- Rationale: LLM generation failed.
- Evidence: ``

Raw decision:

```json

```

### `GH-PROJ-013`

- Gold docs update required: `True`
- Predicted docs update required: `False`
- Decision status: `error`
- Confidence: `0.0`
- Documentation area: `error`
- Rationale: LLM generation failed.
- Evidence: ``

Raw decision:

```json

```

### `GH-PROJ-014`

- Gold docs update required: `True`
- Predicted docs update required: `False`
- Decision status: `error`
- Confidence: `0.0`
- Documentation area: `error`
- Rationale: LLM generation failed.
- Evidence: ``

Raw decision:

```json

```

### `GH-PROJ-015`

- Gold docs update required: `True`
- Predicted docs update required: `False`
- Decision status: `error`
- Confidence: `0.0`
- Documentation area: `error`
- Rationale: LLM generation failed.
- Evidence: ``

Raw decision:

```json

```

## Interpretation Boundary

- This is real public-PR case-study evidence, not synthetic project-evolution evidence.
- The LLM judge is the decision layer; deterministic code here only handles safe input construction, JSON parsing, leakage protection, and metric calculation.
- Gold labels are used only after prediction for evaluation.
- Low-confidence negative cases should be interpreted carefully because absence of a documentation patch in a PR does not always prove that no documentation update was needed.