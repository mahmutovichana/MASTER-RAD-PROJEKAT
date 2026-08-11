# DocGuard Project Evolution Evaluation 2026-08

This is a synthetic project-evolution live demo. It simulates multiple PR-like changes across invented projects and runs `docguard_hybrid.predict()` with sanitized input only: code-side changed files, code diff, docs-before excerpt, project id, and case id.

- Patch backend: `llm-mock`

## Summary Metrics

| Metric | Value |
| --- | ---: |
| `total_cases` | 24 |
| `binary_accuracy` | 95.83% |
| `precision` | 94.44% |
| `recall` | 100.00% |
| `f1` | 97.14% |
| `category_accuracy` | 95.83% |
| `target_file_accuracy` | 95.83% |
| `scenario_accuracy` | 95.83% |
| `patch_non_empty_rate_for_positive_cases` | 100.00% |
| `false_positives` | 1 |
| `false_negatives` | 0 |
| `unknown_scenarios` | 0 |

## By Project

| Name | Total | Binary | Category | Target | Scenario |
| --- | ---: | ---: | ---: | ---: | ---: |
| `atlas_review_api` | 8 | 87.50% | 87.50% | 87.50% | 87.50% |
| `beacon_billing_service` | 8 | 100.00% | 100.00% | 100.00% | 100.00% |
| `nova_task_platform` | 8 | 100.00% | 100.00% | 100.00% | 100.00% |

## By Category

| Name | Total | Binary | Category | Target | Scenario |
| --- | ---: | ---: | ---: | ---: | ---: |
| `api_reference` | 4 | 100.00% | 100.00% | 100.00% | 100.00% |
| `architecture_flow` | 2 | 100.00% | 100.00% | 100.00% | 100.00% |
| `changelog` | 1 | 100.00% | 100.00% | 100.00% | 100.00% |
| `configuration` | 3 | 100.00% | 100.00% | 100.00% | 100.00% |
| `developer_setup` | 1 | 100.00% | 100.00% | 100.00% | 100.00% |
| `model_contract` | 3 | 100.00% | 100.00% | 100.00% | 100.00% |
| `no_update` | 7 | 85.71% | 85.71% | 85.71% | 85.71% |
| `testing_instructions` | 1 | 100.00% | 100.00% | 100.00% | 100.00% |
| `workflow_documentation` | 2 | 100.00% | 100.00% | 100.00% | 100.00% |

## By Difficulty

| Name | Total | Binary | Category | Target | Scenario |
| --- | ---: | ---: | ---: | ---: | ---: |
| `easy` | 13 | 100.00% | 100.00% | 100.00% | 100.00% |
| `hard` | 2 | 50.00% | 50.00% | 50.00% | 50.00% |
| `medium` | 9 | 100.00% | 100.00% | 100.00% | 100.00% |

## Per-Case Walkthrough Table

| Case | Project | Difficulty | Binary | Category | Target | Scenario | Gold target | Pred target | Signals |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `ATLAS-REVIEW-API-PR-01` | `atlas_review_api` | `easy` | `True` | `True` | `True` | `True` | `docs/api.md` | `docs/api.md` | `route_added` |
| `ATLAS-REVIEW-API-PR-02` | `atlas_review_api` | `medium` | `True` | `True` | `True` | `True` | `docs/api.md` | `docs/api.md` | `validation_min_change, validation_max_change, zod_validation_change, comments_only` |
| `ATLAS-REVIEW-API-PR-03` | `atlas_review_api` | `easy` | `True` | `True` | `True` | `True` | `docs/models.md` | `docs/models.md` | `dto_model_change, dto_field_added` |
| `ATLAS-REVIEW-API-PR-04` | `atlas_review_api` | `easy` | `True` | `True` | `True` | `True` | `docs/configuration.md` | `docs/configuration.md` | `added_env_var` |
| `ATLAS-REVIEW-API-PR-05` | `atlas_review_api` | `medium` | `True` | `True` | `True` | `True` | `docs/workflows.md` | `docs/workflows.md` | `schedule_job_change, changed_background_job_schedule` |
| `ATLAS-REVIEW-API-PR-06` | `atlas_review_api` | `easy` | `True` | `True` | `True` | `True` | `` | `` | `internal_variable_rename, source_only_refactor` |
| `ATLAS-REVIEW-API-PR-07` | `atlas_review_api` | `easy` | `True` | `True` | `True` | `True` | `docs/testing.md` | `docs/testing.md` | `test_command_change` |
| `ATLAS-REVIEW-API-PR-08` | `atlas_review_api` | `hard` | `False` | `False` | `False` | `False` | `` | `docs/api.md` | `route_added, docs_already_updated` |
| `BEACON-BILLING-SERVICE-PR-01` | `beacon_billing_service` | `medium` | `True` | `True` | `True` | `True` | `docs/api.md` | `docs/api.md` | `route_added, changed_status_code` |
| `BEACON-BILLING-SERVICE-PR-02` | `beacon_billing_service` | `easy` | `True` | `True` | `True` | `True` | `docs/models.md` | `docs/models.md` | `dto_model_change, dto_field_added` |
| `BEACON-BILLING-SERVICE-PR-03` | `beacon_billing_service` | `medium` | `True` | `True` | `True` | `True` | `docs/configuration.md` | `docs/configuration.md` | `config_default_change` |
| `BEACON-BILLING-SERVICE-PR-04` | `beacon_billing_service` | `medium` | `True` | `True` | `True` | `True` | `docs/architecture.md` | `docs/architecture.md` | `route_added, auth_middleware_change` |
| `BEACON-BILLING-SERVICE-PR-05` | `beacon_billing_service` | `easy` | `True` | `True` | `True` | `True` | `docs/developer-setup.md` | `docs/developer-setup.md` | `package_script_change, local_seed_or_dev_flow, log_message_change_no_user_visible_behavior` |
| `BEACON-BILLING-SERVICE-PR-06` | `beacon_billing_service` | `medium` | `True` | `True` | `True` | `True` | `` | `` | `private_helper_refactor, source_only_refactor` |
| `BEACON-BILLING-SERVICE-PR-07` | `beacon_billing_service` | `medium` | `True` | `True` | `True` | `True` | `CHANGELOG.md` | `CHANGELOG.md` | `changelog_worthy_change` |
| `BEACON-BILLING-SERVICE-PR-08` | `beacon_billing_service` | `easy` | `True` | `True` | `True` | `True` | `` | `` | `log_message_change_no_user_visible_behavior, source_only_refactor` |
| `NOVA-TASK-PLATFORM-PR-01` | `nova_task_platform` | `easy` | `True` | `True` | `True` | `True` | `docs/api.md` | `docs/api.md` | `route_added, changed_status_code` |
| `NOVA-TASK-PLATFORM-PR-02` | `nova_task_platform` | `easy` | `True` | `True` | `True` | `True` | `docs/models.md` | `docs/models.md` | `dto_model_change, dto_field_added` |
| `NOVA-TASK-PLATFORM-PR-03` | `nova_task_platform` | `easy` | `True` | `True` | `True` | `True` | `docs/configuration.md` | `docs/configuration.md` | `added_env_var` |
| `NOVA-TASK-PLATFORM-PR-04` | `nova_task_platform` | `hard` | `True` | `True` | `True` | `True` | `docs/workflows.md` | `docs/workflows.md` | `service_orchestration_change` |
| `NOVA-TASK-PLATFORM-PR-05` | `nova_task_platform` | `medium` | `True` | `True` | `True` | `True` | `docs/architecture.md` | `docs/architecture.md` | `route_added, auth_middleware_change, rate_limit_or_cache_change` |
| `NOVA-TASK-PLATFORM-PR-06` | `nova_task_platform` | `easy` | `True` | `True` | `True` | `True` | `` | `` | `dto_model_change, comments_only` |
| `NOVA-TASK-PLATFORM-PR-07` | `nova_task_platform` | `easy` | `True` | `True` | `True` | `True` | `` | `` | `test_only_no_behavior_change, source_only_refactor` |
| `NOVA-TASK-PLATFORM-PR-08` | `nova_task_platform` | `medium` | `True` | `True` | `True` | `True` | `` | `` | `formatting_only, source_only_refactor` |

## Case Details

### `ATLAS-REVIEW-API-PR-01` Add review creation endpoint

- Project: `atlas_review_api`
- Difficulty: `easy`
- Gold/pred docs update: `True` / `True`
- Gold/pred category: `api_reference` / `api_reference`
- Gold/pred scenario: `new_endpoint` / `new_endpoint`
- Gold/pred target: `docs/api.md` / `docs/api.md`
- Expected patch summary: Document new POST /reviews endpoint.
- Router reason: Matched positive signal `route_added` from: route_added
- Signals: `route_added`
- Patch backend/verifier: `llm-mock` / `pass`
- Grounded tokens found: `/reviews`
- Patch verifier warnings: ``
- Interpretation: DocGuard matched the intended route.

Code diff:

```diff
+router.post('/reviews', createReview);
+res.status(201).json({ id: saved.id, reviewStatus: saved.status });
```

Docs before:

```md
# API Reference

Existing endpoints are documented here.
```

Generated patch:

```diff
@@ docs/api.md
+Mock LLM patch: document `/reviews` based on the supplied code diff.
```

### `ATLAS-REVIEW-API-PR-02` Tighten review comment validation

- Project: `atlas_review_api`
- Difficulty: `medium`
- Gold/pred docs update: `True` / `True`
- Gold/pred category: `api_reference` / `api_reference`
- Gold/pred scenario: `changed_validation_min` / `changed_validation_min`
- Gold/pred target: `docs/api.md` / `docs/api.md`
- Expected patch summary: Update documented review comment validation.
- Router reason: Matched positive signal `validation_min_change` from: validation_min_change, validation_max_change, zod_validation_change, comments_only
- Signals: `validation_min_change, validation_max_change, zod_validation_change, comments_only`
- Patch backend/verifier: `llm-mock` / `pass`
- Grounded tokens found: ``
- Patch verifier warnings: ``
- Interpretation: DocGuard matched the intended route.

Code diff:

```diff
-comment: z.string().min(3).max(500)
+comment: z.string().min(10).max(280)
```

Docs before:

```md
# API Reference

Existing endpoints are documented here.
```

Generated patch:

```diff
@@ docs/api.md
+Mock LLM patch: document `/api` based on the supplied code diff.
```

### `ATLAS-REVIEW-API-PR-03` Expose reviewer id in review DTO

- Project: `atlas_review_api`
- Difficulty: `easy`
- Gold/pred docs update: `True` / `True`
- Gold/pred category: `model_contract` / `model_contract`
- Gold/pred scenario: `added_dto_model_field` / `added_dto_model_field`
- Gold/pred target: `docs/models.md` / `docs/models.md`
- Expected patch summary: Document reviewerId in model contract.
- Router reason: Matched positive signal `dto_field_added` from: dto_model_change, dto_field_added
- Signals: `dto_model_change, dto_field_added`
- Patch backend/verifier: `llm-mock` / `pass`
- Grounded tokens found: `reviewerId`
- Patch verifier warnings: ``
- Interpretation: DocGuard matched the intended route.

Code diff:

```diff
export interface ReviewDto {
   id: string;
+reviewerId: string;
   status: string;
 }
```

Docs before:

```md
# Models

Core DTOs and response contracts are documented here.
```

Generated patch:

```diff
@@ docs/models.md
+Mock LLM patch: document `reviewerId` based on the supplied code diff.
```

### `ATLAS-REVIEW-API-PR-04` Add review feature flag

- Project: `atlas_review_api`
- Difficulty: `easy`
- Gold/pred docs update: `True` / `True`
- Gold/pred category: `configuration` / `configuration`
- Gold/pred scenario: `added_environment_variable` / `added_environment_variable`
- Gold/pred target: `docs/configuration.md` / `docs/configuration.md`
- Expected patch summary: Document REVIEW_FEATURE_FLAG.
- Router reason: Matched positive signal `added_env_var` from: added_env_var
- Signals: `added_env_var`
- Patch backend/verifier: `llm-mock` / `pass`
- Grounded tokens found: `REVIEW_FEATURE_FLAG`
- Patch verifier warnings: ``
- Interpretation: DocGuard matched the intended route.

Code diff:

```diff
+export const REVIEW_FEATURE_FLAG = process.env.REVIEW_FEATURE_FLAG === 'enabled';
```

Docs before:

```md
# Configuration

DATABASE_URL and service-specific queue names are required.
```

Generated patch:

```diff
@@ docs/configuration.md
+Mock LLM patch: document `REVIEW_FEATURE_FLAG` based on the supplied code diff.
```

### `ATLAS-REVIEW-API-PR-05` Run review scheduler every fifteen minutes

- Project: `atlas_review_api`
- Difficulty: `medium`
- Gold/pred docs update: `True` / `True`
- Gold/pred category: `workflow_documentation` / `workflow_documentation`
- Gold/pred scenario: `changed_background_job_schedule` / `changed_background_job_schedule`
- Gold/pred target: `docs/workflows.md` / `docs/workflows.md`
- Expected patch summary: Update scheduler workflow frequency.
- Router reason: Matched positive signal `changed_background_job_schedule` from: schedule_job_change, changed_background_job_schedule
- Signals: `schedule_job_change, changed_background_job_schedule`
- Patch backend/verifier: `llm-mock` / `pass`
- Grounded tokens found: `*/15 * * * *`
- Patch verifier warnings: ``
- Interpretation: DocGuard matched the intended route.

Code diff:

```diff
-scheduleJob('0 * * * *', runReviewScheduler);
+scheduleJob('*/15 * * * *', runReviewScheduler);
```

Docs before:

```md
# Workflows

Background jobs run on the default hourly schedule.
```

Generated patch:

```diff
@@ docs/workflows.md
+Mock LLM patch: document `*/15 * * * *` based on the supplied code diff.
```

### `ATLAS-REVIEW-API-PR-06` Rename local accumulator

- Project: `atlas_review_api`
- Difficulty: `easy`
- Gold/pred docs update: `False` / `False`
- Gold/pred category: `no_update` / `no_update`
- Gold/pred scenario: `internal_variable_rename_no_behavior_change` / `internal_variable_rename_no_behavior_change`
- Gold/pred target: `` / ``
- Expected patch summary: Internal variable rename only.
- Router reason: Matched no-update signal `internal_variable_rename` from: internal_variable_rename, source_only_refactor
- Signals: `internal_variable_rename, source_only_refactor`
- Patch backend/verifier: `llm-mock` / `pass`
- Grounded tokens found: ``
- Patch verifier warnings: ``
- Interpretation: DocGuard matched the intended route.

Code diff:

```diff
-const totalReviews = reviews.length;
+const renamedInternalTotal = reviews.length;
```

Docs before:

```md
# API Reference

Existing endpoints are documented here.
```

Generated patch:

```diff
not_applicable
```

### `ATLAS-REVIEW-API-PR-07` Switch tests to Vitest

- Project: `atlas_review_api`
- Difficulty: `easy`
- Gold/pred docs update: `True` / `True`
- Gold/pred category: `testing_instructions` / `testing_instructions`
- Gold/pred scenario: `changed_test_command` / `changed_test_command`
- Gold/pred target: `docs/testing.md` / `docs/testing.md`
- Expected patch summary: Update test command documentation.
- Router reason: Matched positive signal `test_command_change` from: test_command_change
- Signals: `test_command_change`
- Patch backend/verifier: `llm-mock` / `pass`
- Grounded tokens found: ``
- Patch verifier warnings: ``
- Interpretation: DocGuard matched the intended route.

Code diff:

```diff
-  "test": "jest"
+  "test": "vitest run"
+  "test:watch": "vitest"
```

Docs before:

```md
# Testing

Run `npm test` for the default test suite.
```

Generated patch:

```diff
@@ docs/testing.md
+Mock LLM patch: document `/testing` based on the supplied code diff.
```

### `ATLAS-REVIEW-API-PR-08` Documented endpoint already updated

- Project: `atlas_review_api`
- Difficulty: `hard`
- Gold/pred docs update: `False` / `True`
- Gold/pred category: `no_update` / `api_reference`
- Gold/pred scenario: `docs_already_updated` / `new_endpoint`
- Gold/pred target: `` / `docs/api.md`
- Expected patch summary: Docs already aligned for the endpoint change.
- Router reason: Matched positive signal `route_added` from: route_added, docs_already_updated
- Signals: `route_added, docs_already_updated`
- Patch backend/verifier: `llm-mock` / `pass`
- Grounded tokens found: `/reviews`
- Patch verifier warnings: ``
- Interpretation: DocGuard missed at least one expected dimension; inspect router reason and signals.

Code diff:

```diff
+router.post('/reviews', createReview);
+// docs/api.md already contains POST /reviews in this PR context
```

Docs before:

```md
POST /reviews is already documented with request and response examples.
```

Generated patch:

```diff
@@ docs/api.md
+Mock LLM patch: document `/reviews` based on the supplied code diff.
```

### `BEACON-BILLING-SERVICE-PR-01` Add invoice payment endpoint

- Project: `beacon_billing_service`
- Difficulty: `medium`
- Gold/pred docs update: `True` / `True`
- Gold/pred category: `api_reference` / `api_reference`
- Gold/pred scenario: `new_endpoint` / `new_endpoint`
- Gold/pred target: `docs/api.md` / `docs/api.md`
- Expected patch summary: Document invoice payment endpoint.
- Router reason: Matched positive signal `route_added` from: route_added, changed_status_code
- Signals: `route_added, changed_status_code`
- Patch backend/verifier: `llm-mock` / `pass`
- Grounded tokens found: `/invoices/:id/payments`
- Patch verifier warnings: ``
- Interpretation: DocGuard matched the intended route.

Code diff:

```diff
+router.post('/invoices/:id/payments', createInvoicePayment);
+res.status(202).json({ paymentId, reviewStatus: 'queued' });
```

Docs before:

```md
# API Reference

Existing endpoints are documented here.
```

Generated patch:

```diff
@@ docs/api.md
+Mock LLM patch: document `/invoices/:id/payments` based on the supplied code diff.
```

### `BEACON-BILLING-SERVICE-PR-02` Add invoice reviewer field

- Project: `beacon_billing_service`
- Difficulty: `easy`
- Gold/pred docs update: `True` / `True`
- Gold/pred category: `model_contract` / `model_contract`
- Gold/pred scenario: `added_dto_model_field` / `added_dto_model_field`
- Gold/pred target: `docs/models.md` / `docs/models.md`
- Expected patch summary: Document invoice reviewerId.
- Router reason: Matched positive signal `dto_field_added` from: dto_model_change, dto_field_added
- Signals: `dto_model_change, dto_field_added`
- Patch backend/verifier: `llm-mock` / `pass`
- Grounded tokens found: `reviewerId`
- Patch verifier warnings: ``
- Interpretation: DocGuard matched the intended route.

Code diff:

```diff
export interface InvoiceDto {
   id: string;
+reviewerId: string;
   totalCents: number;
 }
```

Docs before:

```md
# Models

Core DTOs and response contracts are documented here.
```

Generated patch:

```diff
@@ docs/models.md
+Mock LLM patch: document `reviewerId` based on the supplied code diff.
```

### `BEACON-BILLING-SERVICE-PR-03` Change billing page size default

- Project: `beacon_billing_service`
- Difficulty: `medium`
- Gold/pred docs update: `True` / `True`
- Gold/pred category: `configuration` / `configuration`
- Gold/pred scenario: `changed_default_config_value` / `changed_default_config_value`
- Gold/pred target: `docs/configuration.md` / `docs/configuration.md`
- Expected patch summary: Update default page size docs.
- Router reason: Matched positive signal `config_default_change` from: config_default_change
- Signals: `config_default_change`
- Patch backend/verifier: `llm-mock` / `pass`
- Grounded tokens found: ``
- Patch verifier warnings: ``
- Interpretation: DocGuard matched the intended route.

Code diff:

```diff
-export const default_page_size = 50;
+export const default_page_size = 100;
```

Docs before:

```md
# Configuration

DATABASE_URL and service-specific queue names are required.
```

Generated patch:

```diff
@@ docs/configuration.md
+Mock LLM patch: document `/configuration` based on the supplied code diff.
```

### `BEACON-BILLING-SERVICE-PR-04` Require billing role on invoice routes

- Project: `beacon_billing_service`
- Difficulty: `medium`
- Gold/pred docs update: `True` / `True`
- Gold/pred category: `architecture_flow` / `architecture_flow`
- Gold/pred scenario: `changed_middleware_auth_flow` / `changed_middleware_auth_flow`
- Gold/pred target: `docs/architecture.md` / `docs/architecture.md`
- Expected patch summary: Document billing role middleware behavior.
- Router reason: Matched positive signal `auth_middleware_change` from: route_added, auth_middleware_change
- Signals: `route_added, auth_middleware_change`
- Patch backend/verifier: `llm-mock` / `pass`
- Grounded tokens found: `/invoices/:id/payments`
- Patch verifier warnings: ``
- Interpretation: DocGuard matched the intended route.

Code diff:

```diff
+router.post('/invoices/:id/payments', requireRole('billing'), createInvoicePayment);
+const guard = requireRole('billing');
```

Docs before:

```md
# Architecture

Requests pass through auth middleware and service-level rate limits.
```

Generated patch:

```diff
@@ docs/architecture.md
+Mock LLM patch: document `/invoices/:id/payments` based on the supplied code diff.
```

### `BEACON-BILLING-SERVICE-PR-05` Add invoice export seed command

- Project: `beacon_billing_service`
- Difficulty: `easy`
- Gold/pred docs update: `True` / `True`
- Gold/pred category: `developer_setup` / `developer_setup`
- Gold/pred scenario: `changed_local_development_flow` / `changed_local_development_flow`
- Gold/pred target: `docs/developer-setup.md` / `docs/developer-setup.md`
- Expected patch summary: Document invoice seed flow.
- Router reason: Matched positive signal `local_seed_or_dev_flow` from: package_script_change, local_seed_or_dev_flow, log_message_change_no_user_visible_behavior
- Signals: `package_script_change, local_seed_or_dev_flow, log_message_change_no_user_visible_behavior`
- Patch backend/verifier: `llm-mock` / `pass`
- Grounded tokens found: `npm run seed`
- Patch verifier warnings: ``
- Interpretation: DocGuard matched the intended route.

Code diff:

```diff
+  "seed:invoices": "npm run seed -- invoices"
+console.log("npm run seed prepares invoice demo data");
```

Docs before:

```md
# Developer Setup

Run `npm install`, then `npm run dev`.
```

Generated patch:

```diff
@@ docs/developer-setup.md
+Mock LLM patch: document `npm run seed` based on the supplied code diff.
```

### `BEACON-BILLING-SERVICE-PR-06` Refactor invoice formatting helper

- Project: `beacon_billing_service`
- Difficulty: `medium`
- Gold/pred docs update: `False` / `False`
- Gold/pred category: `no_update` / `no_update`
- Gold/pred scenario: `private_helper_refactor_no_flow_change` / `private_helper_refactor_no_flow_change`
- Gold/pred target: `` / ``
- Expected patch summary: Private helper extraction only.
- Router reason: Matched no-update signal `private_helper_refactor` from: private_helper_refactor, source_only_refactor
- Signals: `private_helper_refactor, source_only_refactor`
- Patch backend/verifier: `llm-mock` / `pass`
- Grounded tokens found: ``
- Patch verifier warnings: ``
- Interpretation: DocGuard matched the intended route.

Code diff:

```diff
+function privateFormatInvoiceTotal(totalCents: number) { return totalCents.toString(); }
 const label = privateFormatInvoiceTotal(totalCents);
```

Docs before:

```md
# API Reference

Existing endpoints are documented here.
```

Generated patch:

```diff
not_applicable
```

### `BEACON-BILLING-SERVICE-PR-07` Notify customers about invoice review window

- Project: `beacon_billing_service`
- Difficulty: `medium`
- Gold/pred docs update: `True` / `True`
- Gold/pred category: `changelog` / `changelog`
- Gold/pred scenario: `changelog_worthy_behavior_change` / `changelog_worthy_behavior_change`
- Gold/pred target: `CHANGELOG.md` / `CHANGELOG.md`
- Expected patch summary: Mention customer notification behavior in changelog.
- Router reason: Matched positive signal `changelog_worthy_change` from: changelog_worthy_change
- Signals: `changelog_worthy_change`
- Patch backend/verifier: `llm-mock` / `pass`
- Grounded tokens found: ``
- Patch verifier warnings: ``
- Interpretation: DocGuard matched the intended route.

Code diff:

```diff
+export function notifyCustomersAboutReviewWindow() {
+  return sendInvoiceReviewWindowNotifications();
+}
```

Docs before:

```md
# Changelog

## Unreleased

- Baseline service scaffold.
```

Generated patch:

```diff
@@ CHANGELOG.md
+Mock LLM patch: document `CHANGELOG` based on the supplied code diff.
```

### `BEACON-BILLING-SERVICE-PR-08` Clean up log message

- Project: `beacon_billing_service`
- Difficulty: `easy`
- Gold/pred docs update: `False` / `False`
- Gold/pred category: `no_update` / `no_update`
- Gold/pred scenario: `log_message_change_no_user_visible_behavior` / `log_message_change_no_user_visible_behavior`
- Gold/pred target: `` / ``
- Expected patch summary: Logging message wording only.
- Router reason: Matched no-update signal `log_message_change_no_user_visible_behavior` from: log_message_change_no_user_visible_behavior, source_only_refactor
- Signals: `log_message_change_no_user_visible_behavior, source_only_refactor`
- Patch backend/verifier: `llm-mock` / `pass`
- Grounded tokens found: ``
- Patch verifier warnings: ``
- Interpretation: DocGuard matched the intended route.

Code diff:

```diff
-logger.info('invoice paid')
+logger.info('invoice payment accepted')
```

Docs before:

```md
# API Reference

Existing endpoints are documented here.
```

Generated patch:

```diff
not_applicable
```

### `NOVA-TASK-PLATFORM-PR-01` Add task archive endpoint

- Project: `nova_task_platform`
- Difficulty: `easy`
- Gold/pred docs update: `True` / `True`
- Gold/pred category: `api_reference` / `api_reference`
- Gold/pred scenario: `new_endpoint` / `new_endpoint`
- Gold/pred target: `docs/api.md` / `docs/api.md`
- Expected patch summary: Document task archive endpoint.
- Router reason: Matched positive signal `route_added` from: route_added, changed_status_code
- Signals: `route_added, changed_status_code`
- Patch backend/verifier: `llm-mock` / `pass`
- Grounded tokens found: `/tasks/:id/archive`
- Patch verifier warnings: ``
- Interpretation: DocGuard matched the intended route.

Code diff:

```diff
+router.post('/tasks/:id/archive', archiveTask);
+res.status(202).json({ reviewStatus: 'archived' });
```

Docs before:

```md
# API Reference

Existing endpoints are documented here.
```

Generated patch:

```diff
@@ docs/api.md
+Mock LLM patch: document `/tasks/:id/archive` based on the supplied code diff.
```

### `NOVA-TASK-PLATFORM-PR-02` Add task reviewer field

- Project: `nova_task_platform`
- Difficulty: `easy`
- Gold/pred docs update: `True` / `True`
- Gold/pred category: `model_contract` / `model_contract`
- Gold/pred scenario: `added_dto_model_field` / `added_dto_model_field`
- Gold/pred target: `docs/models.md` / `docs/models.md`
- Expected patch summary: Document reviewerId on task model.
- Router reason: Matched positive signal `dto_field_added` from: dto_model_change, dto_field_added
- Signals: `dto_model_change, dto_field_added`
- Patch backend/verifier: `llm-mock` / `pass`
- Grounded tokens found: `reviewerId`
- Patch verifier warnings: ``
- Interpretation: DocGuard matched the intended route.

Code diff:

```diff
export interface TaskDto {
   id: string;
+reviewerId: string;
   state: string;
 }
```

Docs before:

```md
# Models

Core DTOs and response contracts are documented here.
```

Generated patch:

```diff
@@ docs/models.md
+Mock LLM patch: document `reviewerId` based on the supplied code diff.
```

### `NOVA-TASK-PLATFORM-PR-03` Add task queue env var

- Project: `nova_task_platform`
- Difficulty: `easy`
- Gold/pred docs update: `True` / `True`
- Gold/pred category: `configuration` / `configuration`
- Gold/pred scenario: `added_environment_variable` / `added_environment_variable`
- Gold/pred target: `docs/configuration.md` / `docs/configuration.md`
- Expected patch summary: Document task review feature flag.
- Router reason: Matched positive signal `added_env_var` from: added_env_var
- Signals: `added_env_var`
- Patch backend/verifier: `llm-mock` / `pass`
- Grounded tokens found: `REVIEW_FEATURE_FLAG`
- Patch verifier warnings: ``
- Interpretation: DocGuard matched the intended route.

Code diff:

```diff
+export const REVIEW_FEATURE_FLAG = process.env.REVIEW_FEATURE_FLAG || 'task-review-v2';
```

Docs before:

```md
# Configuration

DATABASE_URL and service-specific queue names are required.
```

Generated patch:

```diff
@@ docs/configuration.md
+Mock LLM patch: document `REVIEW_FEATURE_FLAG` based on the supplied code diff.
```

### `NOVA-TASK-PLATFORM-PR-04` Add workflow orchestration step

- Project: `nova_task_platform`
- Difficulty: `hard`
- Gold/pred docs update: `True` / `True`
- Gold/pred category: `workflow_documentation` / `workflow_documentation`
- Gold/pred scenario: `added_service_orchestration_flow` / `added_service_orchestration_flow`
- Gold/pred target: `docs/workflows.md` / `docs/workflows.md`
- Expected patch summary: Document new workflow orchestration step.
- Router reason: Matched positive signal `service_orchestration_change` from: service_orchestration_change
- Signals: `service_orchestration_change`
- Patch backend/verifier: `llm-mock` / `pass`
- Grounded tokens found: ``
- Patch verifier warnings: ``
- Interpretation: DocGuard matched the intended route.

Code diff:

```diff
+await reserveReview(task.id);
+await notifyReviewer(task.assigneeId);
```

Docs before:

```md
# Workflows

Background jobs run on the default hourly schedule.
```

Generated patch:

```diff
@@ docs/workflows.md
+Mock LLM patch: document `/workflows` based on the supplied code diff.
```

### `NOVA-TASK-PLATFORM-PR-05` Add route rate limit

- Project: `nova_task_platform`
- Difficulty: `medium`
- Gold/pred docs update: `True` / `True`
- Gold/pred category: `architecture_flow` / `architecture_flow`
- Gold/pred scenario: `changed_caching_or_rate_limit_flow` / `changed_caching_or_rate_limit_flow`
- Gold/pred target: `docs/architecture.md` / `docs/architecture.md`
- Expected patch summary: Document task archive rate limit.
- Router reason: Matched positive signal `rate_limit_or_cache_change` from: route_added, auth_middleware_change, rate_limit_or_cache_change
- Signals: `route_added, auth_middleware_change, rate_limit_or_cache_change`
- Patch backend/verifier: `llm-mock` / `pass`
- Grounded tokens found: `/tasks/:id/archive`
- Patch verifier warnings: ``
- Interpretation: DocGuard matched the intended route.

Code diff:

```diff
+const taskArchiveRateLimit = rateLimit({ windowMs: 60000, max: 20 });
+router.post('/tasks/:id/archive', taskArchiveRateLimit, archiveTask);
```

Docs before:

```md
# Architecture

Requests pass through auth middleware and service-level rate limits.
```

Generated patch:

```diff
@@ docs/architecture.md
+Mock LLM patch: document `/tasks/:id/archive` based on the supplied code diff.
```

### `NOVA-TASK-PLATFORM-PR-06` Reword internal comments

- Project: `nova_task_platform`
- Difficulty: `easy`
- Gold/pred docs update: `False` / `False`
- Gold/pred category: `no_update` / `no_update`
- Gold/pred scenario: `comments_reworded_no_contract_change` / `comments_reworded_no_contract_change`
- Gold/pred target: `` / ``
- Expected patch summary: Comment rewording only.
- Router reason: Matched no-update signal `comments_only` from: dto_model_change, comments_only
- Signals: `dto_model_change, comments_only`
- Patch backend/verifier: `llm-mock` / `pass`
- Grounded tokens found: ``
- Patch verifier warnings: ``
- Interpretation: DocGuard matched the intended route.

Code diff:

```diff
-// Calculates task score.
+// Computes task score for internal ranking.
```

Docs before:

```md
# Models

Core DTOs and response contracts are documented here.
```

Generated patch:

```diff
not_applicable
```

### `NOVA-TASK-PLATFORM-PR-07` Refactor test assertion

- Project: `nova_task_platform`
- Difficulty: `easy`
- Gold/pred docs update: `False` / `False`
- Gold/pred category: `no_update` / `no_update`
- Gold/pred scenario: `test_assertion_refactor_no_behavior_change` / `test_assertion_refactor_no_behavior_change`
- Gold/pred target: `` / ``
- Expected patch summary: Test assertion refactor only.
- Router reason: Matched no-update signal `test_only_no_behavior_change` from: test_only_no_behavior_change, source_only_refactor
- Signals: `test_only_no_behavior_change, source_only_refactor`
- Patch backend/verifier: `llm-mock` / `pass`
- Grounded tokens found: ``
- Patch verifier warnings: ``
- Interpretation: DocGuard matched the intended route.

Code diff:

```diff
-expect(response.body.id).toBeTruthy();
+expect(response.body).toHaveProperty('id');
```

Docs before:

```md
# Testing

Run `npm test` for the default test suite.
```

Generated patch:

```diff
not_applicable
```

### `NOVA-TASK-PLATFORM-PR-08` Format task env file

- Project: `nova_task_platform`
- Difficulty: `medium`
- Gold/pred docs update: `False` / `False`
- Gold/pred category: `no_update` / `no_update`
- Gold/pred scenario: `formatting_only_in_docs_or_code` / `formatting_only_in_docs_or_code`
- Gold/pred target: `` / ``
- Expected patch summary: Formatting-only config file change.
- Router reason: Matched no-update signal `formatting_only` from: formatting_only, source_only_refactor
- Signals: `formatting_only, source_only_refactor`
- Patch backend/verifier: `llm-mock` / `pass`
- Grounded tokens found: ``
- Patch verifier warnings: ``
- Interpretation: DocGuard matched the intended route.

Code diff:

```diff
+// formatting
 export const TASK_QUEUE = 'tasks';
```

Docs before:

```md
# Configuration

DATABASE_URL and service-specific queue names are required.
```

Generated patch:

```diff
not_applicable
```

