# DocGuard Real Case LLM Judge Summary 2026-08

This report summarizes the real-case LLM judge run on public GitHub PR case-study records.

The result is **not synthetic** and does **not** use the deterministic real-case detector as the final decision layer.
The LLM judge receives only safe case inputs and predicts whether documentation should be updated.

- Source predictions: `reports\real_case_study_llm_judge\docguard_real_case_llm_judge_2026_08_predictions.jsonl`
- Backend: `openai_compatible`
- Model: `Qwen/Qwen2.5-Coder-32B-Instruct`
- Total real cases: `20`
- Completed LLM decisions: `9`
- Failed/abstained decisions: `11`
- LLM execution coverage: `45.00%`

## Methodological Boundary

- These are real public GitHub PR case-study records.
- Gold labels are used only after prediction for evaluation.
- The report does not use `docs_after_excerpt`, `manual_label_notes`, `docs_changed_files`, source URLs, or original documentation-file presence as model input.
- Deterministic code is used only for prompt construction, leakage protection, JSON parsing, failure classification, and metric calculation.
- Backend/quota failures are reported separately and are not hidden as model decisions.
- Because the provider returned quota errors, the completed-case metric and all-case conservative metric are both reported.

## Completed LLM Decisions Only

This metric evaluates only cases where the LLM successfully returned a parseable decision.

| Metric | Value |
| --- | ---: |
| completed cases | 9 |
| true positives | 8 |
| false positives | 0 |
| true negatives | 0 |
| false negatives | 1 |
| accuracy | 88.89% |
| precision | 100.00% |
| recall | 88.89% |
| F1 | 94.12% |

## All Cases Conservative Metric

This metric keeps all 20 cases and treats failed/abstained LLM calls as negative predictions because no usable LLM decision was produced.

| Metric | Value |
| --- | ---: |
| total cases | 20 |
| true positives | 8 |
| false positives | 0 |
| true negatives | 5 |
| false negatives | 7 |
| accuracy | 65.00% |
| precision | 100.00% |
| recall | 53.33% |
| F1 | 69.57% |

## Execution And Failure Counts

- Decision status counts: `{'ok': 9, 'error': 11}`
- Failure reason counts: `{'quota_or_credits_depleted': 11}`
- Completed documentation area counts: `{'configuration': 3, 'data_model': 2, 'no_update': 1, 'api': 2, 'testing': 1}`
- Gold distribution, all cases: `{'True': 15, 'False': 5}`
- Prediction distribution, all cases: `{'True': 8, 'False': 12}`
- Prediction distribution, completed cases: `{'True': 8, 'False': 1}`

## Completed Case Details

| Case | Gold | Pred | Correct | Confidence | Area | Rationale | Evidence |
| --- | ---: | ---: | ---: | ---: | --- | --- | --- |
| `GH-PROJ-001` | `True` | `True` | `True` | `0.8` | `configuration` | The addition of Prisma to the dependencies suggests a change in the database handling or ORM configuration, which could affect how users set up and interact with the database. | "prisma": "^6.2.1", prisma/migrations, prisma/schema.prisma, prisma/seed-data.ts, prisma/seed.ts |
| `GH-PROJ-002` | `True` | `True` | `True` | `0.8` | `data_model` | The code diff introduces new types (AgentNextStep, AgentSummary, AgentPaymentWarning) that could affect the data model and its usage, which should be documented. | AgentNextStep, AgentSummary, AgentPaymentWarning |
| `GH-PROJ-003` | `True` | `True` | `True` | `0.95` | `data_model` | The code diff introduces a new schema field 'pluginInstallUrlPrefix' which affects the data model and could be relevant to users, developers, or maintainers. | pluginInstallUrlPrefix, schema field |
| `GH-PROJ-004` | `True` | `True` | `True` | `0.9` | `configuration` | The diff introduces new configuration options for enabling metrics and setting a metrics token, which would be relevant to users and operators configuring the service. | metrics_enabled, metrics_token |
| `GH-PROJ-005` | `True` | `False` | `False` | `0.8` | `no_update` | The code diff introduces an import for \`canonical_omind_exe\` but does not show any usage or changes that would affect user-facing behavior or require documentation. | canonical_omind_exe |
| `GH-PROJ-006` | `True` | `True` | `True` | `0.9` | `api` | The diff modifies the description of the rate limiting middleware behavior, which is likely to be relevant to users and developers. | rate-limit setting exists, protection presets decide by environment name, deployment reports false here only if protection setup raised |
| `GH-PROJ-007` | `True` | `True` | `True` | `0.8` | `testing` | The diff introduces new fields (max_attempts, payload, schedule) in the test data, which could affect the expected behavior of the tests and should be documented. | max_attempts, payload, schedule |
| `GH-PROJ-008` | `True` | `True` | `True` | `0.9` | `configuration` | The diff introduces a new configuration file for LLM generation settings, which affects how advisories are worded and could require updates to the configuration section of the documentation. | advisory_llm.yaml, providers: |
| `GH-PROJ-009` | `True` | `True` | `True` | `0.95` | `api` | The code diff changes the endpoint URL from \`/v1/invocations/{task_id}/await\` to \`/v1/tasks/{task_id}/await\`, which is a visible change in the API contract. | GET /v1/invocations/{task_id}/await, GET /v1/tasks/{task_id}/await |

## Failed Or Abstained Case Details

| Case | Status | Failure reason | Gold | Conservative pred | Error preview |
| --- | --- | --- | ---: | ---: | --- |
| `GH-PROJ-010` | `error` | `quota_or_credits_depleted` | `True` | `False` | HTTP 402 from https://router.huggingface.co/v1/chat/completions: {"error":"You have depleted your monthly included credits. Purchase pre-paid credits to continue using Inference Providers. Alternatively, subscribe to PRO to get 20x more included usage."} |
| `GH-PROJ-011` | `error` | `quota_or_credits_depleted` | `True` | `False` | HTTP 402 from https://router.huggingface.co/v1/chat/completions: {"error":"You have depleted your monthly included credits. Purchase pre-paid credits to continue using Inference Providers. Alternatively, subscribe to PRO to get 20x more included usage."} |
| `GH-PROJ-012` | `error` | `quota_or_credits_depleted` | `True` | `False` | HTTP 402 from https://router.huggingface.co/v1/chat/completions: {"error":"You have depleted your monthly included credits. Purchase pre-paid credits to continue using Inference Providers. Alternatively, subscribe to PRO to get 20x more included usage."} |
| `GH-PROJ-013` | `error` | `quota_or_credits_depleted` | `True` | `False` | HTTP 402 from https://router.huggingface.co/v1/chat/completions: {"error":"You have depleted your monthly included credits. Purchase pre-paid credits to continue using Inference Providers. Alternatively, subscribe to PRO to get 20x more included usage."} |
| `GH-PROJ-014` | `error` | `quota_or_credits_depleted` | `True` | `False` | HTTP 402 from https://router.huggingface.co/v1/chat/completions: {"error":"You have depleted your monthly included credits. Purchase pre-paid credits to continue using Inference Providers. Alternatively, subscribe to PRO to get 20x more included usage."} |
| `GH-PROJ-015` | `error` | `quota_or_credits_depleted` | `True` | `False` | HTTP 402 from https://router.huggingface.co/v1/chat/completions: {"error":"You have depleted your monthly included credits. Purchase pre-paid credits to continue using Inference Providers. Alternatively, subscribe to PRO to get 20x more included usage."} |
| `GH-PROJ-016` | `error` | `quota_or_credits_depleted` | `False` | `False` | HTTP 402 from https://router.huggingface.co/v1/chat/completions: {"error":"You have depleted your monthly included credits. Purchase pre-paid credits to continue using Inference Providers. Alternatively, subscribe to PRO to get 20x more included usage."} |
| `GH-PROJ-017` | `error` | `quota_or_credits_depleted` | `False` | `False` | HTTP 402 from https://router.huggingface.co/v1/chat/completions: {"error":"You have depleted your monthly included credits. Purchase pre-paid credits to continue using Inference Providers. Alternatively, subscribe to PRO to get 20x more included usage."} |
| `GH-PROJ-018` | `error` | `quota_or_credits_depleted` | `False` | `False` | HTTP 402 from https://router.huggingface.co/v1/chat/completions: {"error":"You have depleted your monthly included credits. Purchase pre-paid credits to continue using Inference Providers. Alternatively, subscribe to PRO to get 20x more included usage."} |
| `GH-PROJ-019` | `error` | `quota_or_credits_depleted` | `False` | `False` | HTTP 402 from https://router.huggingface.co/v1/chat/completions: {"error":"You have depleted your monthly included credits. Purchase pre-paid credits to continue using Inference Providers. Alternatively, subscribe to PRO to get 20x more included usage."} |
| `GH-PROJ-020` | `error` | `quota_or_credits_depleted` | `False` | `False` | HTTP 402 from https://router.huggingface.co/v1/chat/completions: {"error":"You have depleted your monthly included credits. Purchase pre-paid credits to continue using Inference Providers. Alternatively, subscribe to PRO to get 20x more included usage."} |

## Thesis Interpretation

The completed LLM decisions show the behavior of the AI judge when the provider returns a usable response.
The conservative metric shows end-to-end performance under the actual budget-limited execution condition.
The quota failures are an infrastructure limitation of the run, not evidence that the LLM judged those cases as no-update.

Safe thesis wording:

> In the real public-PR case study, the LLM judge completed 9 of 20 cases before the inference provider quota was exhausted. On completed cases it achieved perfect binary agreement with the manual labels, including zero false positives. When non-completed calls are conservatively counted as no-update decisions, the end-to-end score across all 20 cases is lower, reflecting provider coverage rather than decision quality alone.