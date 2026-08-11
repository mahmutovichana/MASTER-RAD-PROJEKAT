# DocGuard Live Flow Evaluation 2026-08

This is an invented synthetic live-flow playground for implementation sanity/demo purposes. It is not a benchmark and does not replace the leakage-hardened real project case study or external Deep-JIT proxy evidence.

## Summary Metrics

| Metric | Value |
| --- | ---: |
| `total_cases` | 15 |
| `binary_accuracy` | 100.00% |
| `category_accuracy` | 100.00% |
| `target_file_accuracy` | 100.00% |
| `scenario_accuracy` | 100.00% |
| `patch_non_empty_rate_for_positive_cases` | 100.00% |
| `false_positives` | 0 |
| `false_negatives` | 0 |
| `unknown_scenario_count` | 0 |

## Per-Case Results

| Case | Binary | Category | Target | Scenario | Gold category | Pred category | Gold target | Pred target | Signals |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `LIVE-API-NEW-ENDPOINT` | `True` | `True` | `True` | `True` | `api_reference` | `api_reference` | `docs/api.md` | `docs/api.md` | `route_added` |
| `LIVE-API-VALIDATION-MIN` | `True` | `True` | `True` | `True` | `api_reference` | `api_reference` | `docs/api.md` | `docs/api.md` | `validation_min_change, zod_validation_change, comments_only` |
| `LIVE-MODEL-FIELD-ADDED` | `True` | `True` | `True` | `True` | `model_contract` | `model_contract` | `docs/models.md` | `docs/models.md` | `dto_model_change, dto_field_added, comments_only` |
| `LIVE-CONFIG-ENV-VAR` | `True` | `True` | `True` | `True` | `configuration` | `configuration` | `docs/configuration.md` | `docs/configuration.md` | `added_env_var` |
| `LIVE-TESTING-COMMAND` | `True` | `True` | `True` | `True` | `testing_instructions` | `testing_instructions` | `docs/testing.md` | `docs/testing.md` | `test_command_change` |
| `LIVE-WORKFLOW-SCHEDULE` | `True` | `True` | `True` | `True` | `workflow_documentation` | `workflow_documentation` | `docs/workflows.md` | `docs/workflows.md` | `schedule_job_change, changed_background_job_schedule` |
| `LIVE-ARCH-RATE-LIMIT` | `True` | `True` | `True` | `True` | `architecture_flow` | `architecture_flow` | `docs/architecture.md` | `docs/architecture.md` | `auth_middleware_change, rate_limit_or_cache_change` |
| `LIVE-DEVELOPER-SEED` | `True` | `True` | `True` | `True` | `developer_setup` | `developer_setup` | `docs/developer-setup.md` | `docs/developer-setup.md` | `package_script_change, local_seed_or_dev_flow, log_message_change_no_user_visible_behavior` |
| `LIVE-CHANGELOG-WORTHY` | `True` | `True` | `True` | `True` | `changelog` | `changelog` | `CHANGELOG.md` | `CHANGELOG.md` | `changelog_worthy_change` |
| `LIVE-NEG-VARIABLE-RENAME` | `True` | `True` | `True` | `True` | `no_update` | `no_update` | `` | `` | `internal_variable_rename, source_only_refactor` |
| `LIVE-NEG-HELPER-REFACTOR` | `True` | `True` | `True` | `True` | `no_update` | `no_update` | `` | `` | `comments_only, private_helper_refactor, source_only_refactor` |
| `LIVE-NEG-TEST-ASSERTION` | `True` | `True` | `True` | `True` | `no_update` | `no_update` | `` | `` | `test_only_no_behavior_change, source_only_refactor` |
| `LIVE-NEG-COMMENT-REWORDED` | `True` | `True` | `True` | `True` | `no_update` | `no_update` | `` | `` | `comments_only, source_only_refactor` |
| `LIVE-NEG-FORMATTING` | `True` | `True` | `True` | `True` | `no_update` | `no_update` | `` | `` | `formatting_only, source_only_refactor` |
| `LIVE-NEG-DOCS-ALREADY-UPDATED` | `True` | `True` | `True` | `True` | `no_update` | `no_update` | `` | `` | `docs_already_updated, source_only_refactor` |

## Generated Patches

### `LIVE-API-NEW-ENDPOINT`

- Router reason: Matched positive signal `route_added` from: route_added
- Generated patch:

```diff
@@ Reviews
+Document POST /reviews endpoint..
```

### `LIVE-API-VALIDATION-MIN`

- Router reason: Matched positive signal `validation_min_change` from: validation_min_change, zod_validation_change, comments_only
- Generated patch:

```diff
@@ Reviews
+Document minimum comment length of 10..
```

### `LIVE-MODEL-FIELD-ADDED`

- Router reason: Matched positive signal `dto_field_added` from: dto_model_change, dto_field_added, comments_only
- Generated patch:

```diff
@@ Review
+Document reviewerId on Review model..
```

### `LIVE-CONFIG-ENV-VAR`

- Router reason: Matched positive signal `added_env_var` from: added_env_var
- Generated patch:

```diff
@@ Environment Variables
+Document REVIEW_FEATURE_FLAG..
```

### `LIVE-TESTING-COMMAND`

- Router reason: Matched positive signal `test_command_change` from: test_command_change
- Generated patch:

```diff
@@ Testing
+Document vitest test command..
```

### `LIVE-WORKFLOW-SCHEDULE`

- Router reason: Matched positive signal `changed_background_job_schedule` from: schedule_job_change, changed_background_job_schedule
- Generated patch:

```diff
@@ Review Scheduler
+Document 15 minute review scheduler..
```

### `LIVE-ARCH-RATE-LIMIT`

- Router reason: Matched positive signal `rate_limit_or_cache_change` from: auth_middleware_change, rate_limit_or_cache_change
- Generated patch:

```diff
@@ Middleware
+Document reviewer role and rateLimit behavior..
```

### `LIVE-DEVELOPER-SEED`

- Router reason: Matched positive signal `local_seed_or_dev_flow` from: package_script_change, local_seed_or_dev_flow, log_message_change_no_user_visible_behavior
- Generated patch:

```diff
@@ Seed Data
+Document npm run seed for review demo data..
```

### `LIVE-CHANGELOG-WORTHY`

- Router reason: Matched positive signal `changelog_worthy_change` from: changelog_worthy_change
- Generated patch:

```diff
@@ Unreleased
+Mention customer review-window notifications..
```

### `LIVE-NEG-VARIABLE-RENAME`

- Router reason: Matched no-update signal `internal_variable_rename` from: internal_variable_rename, source_only_refactor
- Generated patch:

```diff
not_applicable
```

### `LIVE-NEG-HELPER-REFACTOR`

- Router reason: Matched no-update signal `private_helper_refactor` from: comments_only, private_helper_refactor, source_only_refactor
- Generated patch:

```diff
not_applicable
```

### `LIVE-NEG-TEST-ASSERTION`

- Router reason: Matched no-update signal `test_only_no_behavior_change` from: test_only_no_behavior_change, source_only_refactor
- Generated patch:

```diff
not_applicable
```

### `LIVE-NEG-COMMENT-REWORDED`

- Router reason: Matched no-update signal `comments_only` from: comments_only, source_only_refactor
- Generated patch:

```diff
not_applicable
```

### `LIVE-NEG-FORMATTING`

- Router reason: Matched no-update signal `formatting_only` from: formatting_only, source_only_refactor
- Generated patch:

```diff
not_applicable
```

### `LIVE-NEG-DOCS-ALREADY-UPDATED`

- Router reason: Matched no-update signal `docs_already_updated` from: docs_already_updated, source_only_refactor
- Generated patch:

```diff
not_applicable
```

