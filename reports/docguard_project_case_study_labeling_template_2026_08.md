# DocGuard Project Case Study Labeling Template 2026-08

## Purpose

Use this template to manually label a small real-world DocGuard case study. These cases evaluate the DocGuard agent behavior: update-required detection, routing/category, target documentation file, and patch usefulness.

Deep-JIT should not be used as a substitute for this study because Deep-JIT measures code-comment binary consistency, not project-level Markdown documentation maintenance.

## Selecting Commits Or PRs

Choose 15-30 real commits or pull requests from GitHub projects. Prefer backend or REST API repositories with small, inspectable changes involving:

- API endpoint additions/removals/behavior changes
- validation rule changes
- request or response schema changes
- configuration changes
- testing command changes
- workflow or developer process changes
- documentation already updated in the same PR
- internal refactors where documentation should not change

Avoid huge PRs, generated-code-only changes, dependency lockfile-only changes, and cases where the relevant documentation cannot be inspected.

## Deciding `gold_docs_update_required`

Label `true` when a reasonable maintainer should update user-facing, developer-facing, or API documentation because the code diff changes behavior, usage, configuration, commands, schemas, endpoints, or workflow.

Label `false` when the change is internal only, documentation is already accurate, the behavior is unchanged, or no stable documentation target exists.

Use `label_confidence: low` when context is incomplete or the change could reasonably be interpreted both ways.

## Assigning `gold_doc_category`

Use:

- `api_reference` for endpoints, parameters, validation, auth, status codes, and response fields.
- `configuration` for environment variables, feature flags, defaults, deployment config, or runtime settings.
- `developer_setup` for install, local setup, seed data, or development prerequisites.
- `testing` for test commands, coverage, CI commands, or test scope.
- `workflow` for operational or user workflows.
- `architecture` for service boundaries, background jobs, queues, or internal design that is documented.
- `data_model` for entity fields and schema/model documentation.
- `changelog` when the best target is release notes.
- `none` for negative cases.
- `uncertain` for genuinely ambiguous cases.

## Identifying Target Doc File

Set `gold_target_doc_file` to the most likely documentation file visible in the project, such as `README.md`, `docs/api.md`, `docs/configuration.md`, or `docs/testing.md`.

Use `uncertain` when the project has multiple plausible targets. Use `none` for negative cases.

## Judging Patch Usefulness

After DocGuard produces a suggestion, rate usefulness manually:

- Acceptable: correct update need, target/category plausible, and patch summary would help a maintainer.
- Partially acceptable: right update need but wrong target, incomplete patch, or vague wording.
- Not acceptable: wrong update need, unsafe suggestion, hallucinated target, or patch contradicts code.

Save qualitative notes even when computing summary metrics.

## Example Positive Cases

- A new `GET /orders/{id}/events` endpoint is added and `docs/api.md` lacks it.
- Password minimum length changes from 8 to 12 and API docs still say 8.
- `.env` variable `PAYMENTS_WEBHOOK_SECRET` becomes required and setup docs do not mention it.
- Test command changes from unit-only to unit plus integration and README still shows the old command.

## Example Negative Cases

- A variable rename preserves behavior and docs are still accurate.
- A helper function is refactored without changing public behavior.
- Documentation is updated in the same PR and already reflects the code change.
- A generated lockfile changes without user-visible behavior.

## Warnings

- Do not use `docs_after_excerpt` as model input. It is audit-only.
- Do not label from future documentation alone; use the code diff and documentation-before view for the model input.
- Do not force high-confidence labels when the repository context is weak.
- Do not report placeholder records as results.
