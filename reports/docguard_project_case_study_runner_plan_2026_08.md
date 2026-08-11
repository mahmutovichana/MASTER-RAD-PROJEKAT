# DocGuard Project Case Study Runner Plan 2026-08

## Goal

Apply the existing DocGuard runtime/classifier to each manually labeled project-level case and compare predictions against human gold labels.

## Input Construction

For each JSONL case, construct the model input from:

- `code_diff_excerpt`
- `docs_before_excerpt`
- optionally `changed_files`, `language`, and `change_type` as context

Do not use `docs_after_excerpt`, gold labels, manual notes, or patch summaries as model input.

## Proposed Runner Flow

1. Load cases from `data/external/project_case_study/manual_cases.jsonl`.
2. Validate with `validate-project-cases`.
3. Convert each case into the closest existing DocGuard runtime input shape.
4. Run existing DocGuard prediction path.
5. Save one prediction record per case to `reports/docguard_project_case_study_predictions_2026_08.jsonl`.
6. Compare predictions with manual labels.
7. Generate `reports/docguard_project_case_study_evaluation_2026_08.md`.
8. Manually review generated patch suggestions for usefulness.

## Evaluation Fields

Prediction records should include:

- `case_id`
- predicted `docs_update_required`
- predicted category
- predicted target documentation file if available
- generated patch summary or patch text
- confidence if available
- comparison against gold labels
- human patch usefulness rating
- reviewer notes

## Metrics

- Binary accuracy, precision, recall, and F1 for `docs_update_required`.
- Category accuracy on cases where docs update is required.
- Target-file accuracy where a visible target file exists.
- Human patch usefulness counts: acceptable, partially acceptable, not acceptable.

## Implementation Decision

Do not implement the full runner until real cases exist and the exact DocGuard runtime input adapter is chosen. The safe first step is to validate and manually inspect the case-study JSONL format.
