# DocGuard Real Project Case Study Evaluation 2026-08

This report evaluates DocGuard on manually validated public GitHub PR cases.
Gold labels are used only after prediction for scoring. They are not passed into the runtime record.

- Input: `data\external\project_case_study\manual_cases.jsonl`
- Prediction mode: `hybrid_router` through the real-case adapter
- Patch backend: `deterministic`

## Leakage Policy

Allowed runtime/model input fields:

- `code_changed_files`
- `code_diff_excerpt`
- `docs_before_excerpt`
- `language`

Audit-only fields excluded from runtime/model input:

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

## Binary Metrics

| Metric | Value |
| --- | ---: |
| total cases | 20 |
| true positives | 15 |
| false positives | 5 |
| true negatives | 0 |
| false negatives | 0 |
| binary accuracy | 75.00% |
| precision | 75.00% |
| recall | 100.00% |
| F1 | 85.71% |

## Category And Target Diagnostics

Category accuracy is reported only for real-case labels that can be normalized to a DocGuard internal category.
Target-file exact accuracy is diagnostic only because real repositories have project-specific documentation paths.

| Metric | Value |
| --- | ---: |
| category supported total | 15 |
| category supported correct | 6 |
| category supported accuracy | 40.00% |
| target exact total diagnostic | 15 |
| target exact correct diagnostic | 0 |
| target exact accuracy diagnostic | 0.00% |

## Quality And Guardrail Counts

- Quality labels: `{'needs_review': 4, 'usable': 11, 'excellent': 3, 'rejected': 2}`
- Hallucination risk: `{'medium': 4, 'low': 14, 'high': 2}`
- Verifier status: `{'warn': 4, 'pass': 14, 'fail': 2}`
- Gold distribution: `{'True': 15, 'False': 5}`
- Prediction distribution: `{'True': 20}`

## Per-Case Results

| Case | Gold | Pred | Binary | Gold category | Pred category | Pred target | Verifier | Quality | Risk | Signals |
| --- | ---: | ---: | ---: | --- | --- | --- | --- | --- | --- | --- |
| `GH-PROJ-001` | `True` | `True` | `True` | `model_contract` | `model_contract` | `docs/models.md` | `warn` | `needs_review` | `medium` | `schema_or_model_change, testing_or_verification_change, workflow_change, developer_setup_change, architecture_change` |
| `GH-PROJ-002` | `True` | `True` | `True` | `model_contract` | `model_contract` | `docs/models.md` | `pass` | `usable` | `low` | `schema_or_model_change, architecture_change` |
| `GH-PROJ-003` | `True` | `True` | `True` | `model_contract` | `model_contract` | `docs/models.md` | `pass` | `usable` | `low` | `schema_or_model_change, testing_or_verification_change` |
| `GH-PROJ-004` | `True` | `True` | `True` | `model_contract` | `configuration` | `docs/configuration.md` | `pass` | `usable` | `low` | `schema_or_model_change, configuration_change, developer_setup_change` |
| `GH-PROJ-005` | `True` | `True` | `True` | `testing_instructions` | `testing_instructions` | `docs/testing.md` | `pass` | `usable` | `low` | `testing_or_verification_change, workflow_change` |
| `GH-PROJ-006` | `True` | `True` | `True` | `api_reference` | `configuration` | `docs/configuration.md` | `warn` | `needs_review` | `medium` | `schema_or_model_change, configuration_change, testing_or_verification_change, architecture_change` |
| `GH-PROJ-007` | `True` | `True` | `True` | `model_contract` | `model_contract` | `docs/models.md` | `pass` | `excellent` | `low` | `schema_or_model_change, workflow_change, tests_only` |
| `GH-PROJ-008` | `True` | `True` | `True` | `model_contract` | `configuration` | `docs/configuration.md` | `pass` | `usable` | `low` | `configuration_change, developer_setup_change` |
| `GH-PROJ-009` | `True` | `True` | `True` | `model_contract` | `api_reference` | `docs/api.md` | `pass` | `usable` | `low` | `schema_or_model_change, endpoint_change` |
| `GH-PROJ-010` | `True` | `True` | `True` | `model_contract` | `configuration` | `docs/configuration.md` | `warn` | `needs_review` | `medium` | `schema_or_model_change, configuration_change` |
| `GH-PROJ-011` | `True` | `True` | `True` | `api_reference` | `model_contract` | `docs/models.md` | `pass` | `usable` | `low` | `schema_or_model_change` |
| `GH-PROJ-012` | `True` | `True` | `True` | `testing_instructions` | `configuration` | `docs/configuration.md` | `pass` | `usable` | `low` | `schema_or_model_change, configuration_change` |
| `GH-PROJ-013` | `True` | `True` | `True` | `configuration` | `configuration` | `docs/configuration.md` | `pass` | `excellent` | `low` | `schema_or_model_change, configuration_change` |
| `GH-PROJ-014` | `True` | `True` | `True` | `configuration` | `api_reference` | `docs/api.md` | `warn` | `needs_review` | `medium` | `schema_or_model_change, endpoint_change, configuration_change` |
| `GH-PROJ-015` | `True` | `True` | `True` | `workflow_documentation` | `model_contract` | `docs/models.md` | `fail` | `rejected` | `high` | `schema_or_model_change, developer_setup_change` |
| `GH-PROJ-016` | `False` | `True` | `False` | `none` | `model_contract` | `docs/models.md` | `pass` | `excellent` | `low` | `schema_or_model_change, workflow_change` |
| `GH-PROJ-017` | `False` | `True` | `False` | `none` | `model_contract` | `docs/models.md` | `pass` | `usable` | `low` | `schema_or_model_change` |
| `GH-PROJ-018` | `False` | `True` | `False` | `none` | `configuration` | `docs/configuration.md` | `pass` | `usable` | `low` | `schema_or_model_change, configuration_change, workflow_change` |
| `GH-PROJ-019` | `False` | `True` | `False` | `none` | `api_reference` | `docs/api.md` | `pass` | `usable` | `low` | `endpoint_change, developer_setup_change, architecture_change` |
| `GH-PROJ-020` | `False` | `True` | `False` | `none` | `model_contract` | `docs/models.md` | `fail` | `rejected` | `high` | `schema_or_model_change` |

## Case Details

### `GH-PROJ-001`

- Gold docs update required: `True`
- Predicted docs update required: `True`
- Predicted category: `model_contract`
- Predicted target: `docs/models.md`
- Predicted scenario: `real_schema_or_model_contract_change`
- Router reason: Real-case detector used only code_changed_files, code_diff_excerpt, docs_before_excerpt, and language. Signals: schema_or_model_change, testing_or_verification_change, workflow_change, developer_setup_change, architecture_change.
- Signals: `schema_or_model_change, testing_or_verification_change, workflow_change, developer_setup_change, architecture_change`
- Verifier: `warn`
- Quality: `needs_review`
- Hallucination risk: `medium`

Generated patch:

```diff
@@ Data Models
+Document the changed public data contract fields: `prisma`.
```

Warnings / quality reasons:

- patch does not include any concrete token extracted from the diff
- patch is grounded, minimal, and readable under lightweight heuristic checks

### `GH-PROJ-002`

- Gold docs update required: `True`
- Predicted docs update required: `True`
- Predicted category: `model_contract`
- Predicted target: `docs/models.md`
- Predicted scenario: `real_schema_or_model_contract_change`
- Router reason: Real-case detector used only code_changed_files, code_diff_excerpt, docs_before_excerpt, and language. Signals: schema_or_model_change, architecture_change.
- Signals: `schema_or_model_change, architecture_change`
- Verifier: `pass`
- Quality: `usable`
- Hallucination risk: `low`

Generated patch:

```diff
@@ Data Models
+Document the changed public data/schema contract.
```

Warnings / quality reasons:

- patch is grounded, minimal, and readable under lightweight heuristic checks

### `GH-PROJ-003`

- Gold docs update required: `True`
- Predicted docs update required: `True`
- Predicted category: `model_contract`
- Predicted target: `docs/models.md`
- Predicted scenario: `real_schema_or_model_contract_change`
- Router reason: Real-case detector used only code_changed_files, code_diff_excerpt, docs_before_excerpt, and language. Signals: schema_or_model_change, testing_or_verification_change.
- Signals: `schema_or_model_change, testing_or_verification_change`
- Verifier: `pass`
- Quality: `usable`
- Hallucination risk: `low`

Generated patch:

```diff
@@ Data Models
+Document the changed public data contract fields: `pluginInstallUrlPrefix`, `description`, `examples`.
```

Warnings / quality reasons:

- patch is grounded, minimal, and readable under lightweight heuristic checks

### `GH-PROJ-004`

- Gold docs update required: `True`
- Predicted docs update required: `True`
- Predicted category: `configuration`
- Predicted target: `docs/configuration.md`
- Predicted scenario: `real_configuration_or_environment_change`
- Router reason: Real-case detector used only code_changed_files, code_diff_excerpt, docs_before_excerpt, and language. Signals: schema_or_model_change, configuration_change, developer_setup_change.
- Signals: `schema_or_model_change, configuration_change, developer_setup_change`
- Verifier: `pass`
- Quality: `usable`
- Hallucination risk: `low`

Generated patch:

```diff
@@ Configuration
+Document the changed configuration setting `metrics_enabled`.
```

Warnings / quality reasons:

- patch is grounded, minimal, and readable under lightweight heuristic checks

### `GH-PROJ-005`

- Gold docs update required: `True`
- Predicted docs update required: `True`
- Predicted category: `testing_instructions`
- Predicted target: `docs/testing.md`
- Predicted scenario: `real_testing_or_verification_change`
- Router reason: Real-case detector used only code_changed_files, code_diff_excerpt, docs_before_excerpt, and language. Signals: testing_or_verification_change, workflow_change.
- Signals: `testing_or_verification_change, workflow_change`
- Verifier: `pass`
- Quality: `usable`
- Hallucination risk: `low`

Generated patch:

```diff
@@ Testing
+Document the changed installation or verification workflow.
```

Warnings / quality reasons:

- patch is grounded, minimal, and readable under lightweight heuristic checks

### `GH-PROJ-006`

- Gold docs update required: `True`
- Predicted docs update required: `True`
- Predicted category: `configuration`
- Predicted target: `docs/configuration.md`
- Predicted scenario: `real_configuration_or_environment_change`
- Router reason: Real-case detector used only code_changed_files, code_diff_excerpt, docs_before_excerpt, and language. Signals: schema_or_model_change, configuration_change, testing_or_verification_change, architecture_change.
- Signals: `schema_or_model_change, configuration_change, testing_or_verification_change, architecture_change`
- Verifier: `warn`
- Quality: `needs_review`
- Hallucination risk: `medium`

Generated patch:

```diff
@@ Configuration
+Document the configuration behavior changed in the code diff.
```

Warnings / quality reasons:

- patch does not include any concrete token extracted from the diff
- patch is grounded, minimal, and readable under lightweight heuristic checks

### `GH-PROJ-007`

- Gold docs update required: `True`
- Predicted docs update required: `True`
- Predicted category: `model_contract`
- Predicted target: `docs/models.md`
- Predicted scenario: `real_schema_or_model_contract_change`
- Router reason: Real-case detector used only code_changed_files, code_diff_excerpt, docs_before_excerpt, and language. Signals: schema_or_model_change, workflow_change, tests_only.
- Signals: `schema_or_model_change, workflow_change, tests_only`
- Verifier: `pass`
- Quality: `excellent`
- Hallucination risk: `low`

Generated patch:

```diff
@@ Data Models
+Document the changed public data contract fields: `max_attempts`, `payload`, `stock_code`, `report_type`, `notify`, `schedule`.
```

Warnings / quality reasons:

- patch is grounded, minimal, and readable under lightweight heuristic checks

### `GH-PROJ-008`

- Gold docs update required: `True`
- Predicted docs update required: `True`
- Predicted category: `configuration`
- Predicted target: `docs/configuration.md`
- Predicted scenario: `real_configuration_or_environment_change`
- Router reason: Real-case detector used only code_changed_files, code_diff_excerpt, docs_before_excerpt, and language. Signals: configuration_change, developer_setup_change.
- Signals: `configuration_change, developer_setup_change`
- Verifier: `pass`
- Quality: `usable`
- Hallucination risk: `low`

Generated patch:

```diff
@@ Configuration
+Document the changed configuration setting `purpose`.
```

Warnings / quality reasons:

- patch is grounded, minimal, and readable under lightweight heuristic checks

### `GH-PROJ-009`

- Gold docs update required: `True`
- Predicted docs update required: `True`
- Predicted category: `api_reference`
- Predicted target: `docs/api.md`
- Predicted scenario: `real_api_or_endpoint_contract_change`
- Router reason: Real-case detector used only code_changed_files, code_diff_excerpt, docs_before_excerpt, and language. Signals: schema_or_model_change, endpoint_change.
- Signals: `schema_or_model_change, endpoint_change`
- Verifier: `pass`
- Quality: `usable`
- Hallucination risk: `low`

Generated patch:

```diff
@@ API Reference
+Document the public API change for `GET /v1/invocations/{task_id}/await`.
```

Warnings / quality reasons:

- patch repeats already documented tokens: GET /v1/invocations/{task_id}/await

### `GH-PROJ-010`

- Gold docs update required: `True`
- Predicted docs update required: `True`
- Predicted category: `configuration`
- Predicted target: `docs/configuration.md`
- Predicted scenario: `real_configuration_or_environment_change`
- Router reason: Real-case detector used only code_changed_files, code_diff_excerpt, docs_before_excerpt, and language. Signals: schema_or_model_change, configuration_change.
- Signals: `schema_or_model_change, configuration_change`
- Verifier: `warn`
- Quality: `needs_review`
- Hallucination risk: `medium`

Generated patch:

```diff
@@ Configuration
+Document the configuration behavior changed in the code diff.
```

Warnings / quality reasons:

- patch does not include any concrete token extracted from the diff
- patch is grounded, minimal, and readable under lightweight heuristic checks

### `GH-PROJ-011`

- Gold docs update required: `True`
- Predicted docs update required: `True`
- Predicted category: `model_contract`
- Predicted target: `docs/models.md`
- Predicted scenario: `real_schema_or_model_contract_change`
- Router reason: Real-case detector used only code_changed_files, code_diff_excerpt, docs_before_excerpt, and language. Signals: schema_or_model_change.
- Signals: `schema_or_model_change`
- Verifier: `pass`
- Quality: `usable`
- Hallucination risk: `low`

Generated patch:

```diff
@@ Data Models
+Document the changed public data/schema contract.
```

Warnings / quality reasons:

- patch is grounded, minimal, and readable under lightweight heuristic checks

### `GH-PROJ-012`

- Gold docs update required: `True`
- Predicted docs update required: `True`
- Predicted category: `configuration`
- Predicted target: `docs/configuration.md`
- Predicted scenario: `real_configuration_or_environment_change`
- Router reason: Real-case detector used only code_changed_files, code_diff_excerpt, docs_before_excerpt, and language. Signals: schema_or_model_change, configuration_change.
- Signals: `schema_or_model_change, configuration_change`
- Verifier: `pass`
- Quality: `usable`
- Hallucination risk: `low`

Generated patch:

```diff
@@ Configuration
+Document the changed configuration setting `exclude`.
```

Warnings / quality reasons:

- patch is grounded, minimal, and readable under lightweight heuristic checks

### `GH-PROJ-013`

- Gold docs update required: `True`
- Predicted docs update required: `True`
- Predicted category: `configuration`
- Predicted target: `docs/configuration.md`
- Predicted scenario: `real_configuration_or_environment_change`
- Router reason: Real-case detector used only code_changed_files, code_diff_excerpt, docs_before_excerpt, and language. Signals: schema_or_model_change, configuration_change.
- Signals: `schema_or_model_change, configuration_change`
- Verifier: `pass`
- Quality: `excellent`
- Hallucination risk: `low`

Generated patch:

```diff
@@ Configuration
+Document the changed configuration setting `NetworkPolicy`.
```

Warnings / quality reasons:

- patch is grounded, minimal, and readable under lightweight heuristic checks

### `GH-PROJ-014`

- Gold docs update required: `True`
- Predicted docs update required: `True`
- Predicted category: `api_reference`
- Predicted target: `docs/api.md`
- Predicted scenario: `real_api_or_endpoint_contract_change`
- Router reason: Real-case detector used only code_changed_files, code_diff_excerpt, docs_before_excerpt, and language. Signals: schema_or_model_change, endpoint_change, configuration_change.
- Signals: `schema_or_model_change, endpoint_change, configuration_change`
- Verifier: `warn`
- Quality: `needs_review`
- Hallucination risk: `medium`

Generated patch:

```diff
@@ API Reference
+Document the public API change for `/var/lib/alloy/data`.
```

Warnings / quality reasons:

- patch does not include any concrete token extracted from the diff
- patch is grounded, minimal, and readable under lightweight heuristic checks

### `GH-PROJ-015`

- Gold docs update required: `True`
- Predicted docs update required: `True`
- Predicted category: `model_contract`
- Predicted target: `docs/models.md`
- Predicted scenario: `real_schema_or_model_contract_change`
- Router reason: Real-case detector used only code_changed_files, code_diff_excerpt, docs_before_excerpt, and language. Signals: schema_or_model_change, developer_setup_change.
- Signals: `schema_or_model_change, developer_setup_change`
- Verifier: `fail`
- Quality: `rejected`
- Hallucination risk: `high`

Generated patch:

```diff
@@ Data Models
+Document the changed public data contract fields: `version`, `repository`, `url`.
```

Warnings / quality reasons:

- unsupported field/identifier claims: url
- verifier found unsupported claims
- patch repeats already documented tokens: url

### `GH-PROJ-016`

- Gold docs update required: `False`
- Predicted docs update required: `True`
- Predicted category: `model_contract`
- Predicted target: `docs/models.md`
- Predicted scenario: `real_schema_or_model_contract_change`
- Router reason: Real-case detector used only code_changed_files, code_diff_excerpt, docs_before_excerpt, and language. Signals: schema_or_model_change, workflow_change.
- Signals: `schema_or_model_change, workflow_change`
- Verifier: `pass`
- Quality: `excellent`
- Hallucination risk: `low`

Generated patch:

```diff
@@ Data Models
+Document the changed public data contract fields: `executorDelegationOrigin`.
```

Warnings / quality reasons:

- patch is grounded, minimal, and readable under lightweight heuristic checks

### `GH-PROJ-017`

- Gold docs update required: `False`
- Predicted docs update required: `True`
- Predicted category: `model_contract`
- Predicted target: `docs/models.md`
- Predicted scenario: `real_schema_or_model_contract_change`
- Router reason: Real-case detector used only code_changed_files, code_diff_excerpt, docs_before_excerpt, and language. Signals: schema_or_model_change.
- Signals: `schema_or_model_change`
- Verifier: `pass`
- Quality: `usable`
- Hallucination risk: `low`

Generated patch:

```diff
@@ Data Models
+Document the changed public data/schema contract.
```

Warnings / quality reasons:

- patch is grounded, minimal, and readable under lightweight heuristic checks

### `GH-PROJ-018`

- Gold docs update required: `False`
- Predicted docs update required: `True`
- Predicted category: `configuration`
- Predicted target: `docs/configuration.md`
- Predicted scenario: `real_configuration_or_environment_change`
- Router reason: Real-case detector used only code_changed_files, code_diff_excerpt, docs_before_excerpt, and language. Signals: schema_or_model_change, configuration_change, workflow_change.
- Signals: `schema_or_model_change, configuration_change, workflow_change`
- Verifier: `pass`
- Quality: `usable`
- Hallucination risk: `low`

Generated patch:

```diff
@@ Configuration
+Document `DECISION_SKIP_FALLBACK` and its visible default value `SKIP_FALLBACK`.
```

Warnings / quality reasons:

- patch is grounded, minimal, and readable under lightweight heuristic checks

### `GH-PROJ-019`

- Gold docs update required: `False`
- Predicted docs update required: `True`
- Predicted category: `api_reference`
- Predicted target: `docs/api.md`
- Predicted scenario: `real_api_or_endpoint_contract_change`
- Router reason: Real-case detector used only code_changed_files, code_diff_excerpt, docs_before_excerpt, and language. Signals: endpoint_change, developer_setup_change, architecture_change.
- Signals: `endpoint_change, developer_setup_change, architecture_change`
- Verifier: `pass`
- Quality: `usable`
- Hallucination risk: `low`

Generated patch:

```diff
@@ API Reference
+Document the public API contract change detected in the code diff.
```

Warnings / quality reasons:

- patch is grounded, minimal, and readable under lightweight heuristic checks

### `GH-PROJ-020`

- Gold docs update required: `False`
- Predicted docs update required: `True`
- Predicted category: `model_contract`
- Predicted target: `docs/models.md`
- Predicted scenario: `real_schema_or_model_contract_change`
- Router reason: Real-case detector used only code_changed_files, code_diff_excerpt, docs_before_excerpt, and language. Signals: schema_or_model_change.
- Signals: `schema_or_model_change`
- Verifier: `fail`
- Quality: `rejected`
- Hallucination risk: `high`

Generated patch:

```diff
@@ Data Models
+Document the changed public data contract fields: `id`, `email`.
```

Warnings / quality reasons:

- unsupported field/identifier claims: email, id
- patch does not include any concrete token extracted from the diff
- verifier found unsupported claims

## Interpretation Boundary

- This is the first automatic real-case adapter run.
- Metrics may be weaker than synthetic project-evolution metrics; that is expected and methodologically useful.
- Synthetic project-evolution remains demo evidence.
- This real-case study is the thesis-critical workflow evidence stream.
- Deterministic patches are fallback-quality suggestions, not final proof of human-quality documentation.