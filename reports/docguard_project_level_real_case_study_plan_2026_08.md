# DocGuard Project-Level Real Case Study Plan 2026-08

## Goal

Re-align the thesis evidence with the original DocGuard agent goal: software project consistency analysis, not only binary code-comment classification.

## Study Design

Manually audit 10-30 real commits or pull requests from GitHub projects. Prefer REST API or backend projects with changes involving:

- API endpoints
- request validation
- authentication/authorization
- configuration
- response fields
- test commands
- documentation updates

## Labels

For each case, manually record:

- `docs_update_required`
- target documentation category
- target documentation file if visible
- target code area
- whether the DocGuard suggestion is acceptable
- brief human rationale

## Evaluation

Report:

- Binary update-required correctness.
- Category/target routing correctness.
- Target file correctness when a target file is visible.
- Patch usefulness by human review.
- Representative success and failure cases.

## Scope

This is a qualitative or semistructured agent evaluation, not a large ML benchmark. It supports practical applicability and alignment with "software project consistency analysis" while the Deep-JIT classifier remains a proxy evidence stream.
