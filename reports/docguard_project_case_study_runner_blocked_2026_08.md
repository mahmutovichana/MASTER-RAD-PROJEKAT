# DocGuard Project Case Study Runner Blocked 2026-08

## Status

Full automatic project-case evaluation runner is deferred.

## Reason

The existing `docguard` runtime is currently shaped around synthetic DocGuard records. It expects fields and patterns such as:

- `id`
- `project_id`
- `code_diff`
- `docs_update_required`
- `scenario_type`
- `doc_category`
- `target_doc_file`
- `expected_facts`
- synthetic TypeScript route patterns under `src/modules/...`

The real case-study schema uses project-level fields such as `case_id`, `code_diff_excerpt`, `docs_before_excerpt`, `gold_doc_category`, and `gold_target_doc_file`. Applying the current runtime directly would require an adapter and would likely mark many real cases as `unknown_change`, producing a misleading evaluation.

## Safe Manual Path

1. Validate the real cases:

```bash
python -m docguard_external.cli validate-project-cases --input data/external/project_case_study/manual_cases.jsonl --report reports/docguard_project_case_study_validation_2026_08.md
```

2. For each case, construct model input only from:

- `language`
- `changed_files`
- `code_diff_excerpt`
- `docs_before_excerpt`

Do not use `changed_files`, `docs_changed_files`, or `change_type` for automatic evaluation. `changed_files` and `docs_changed_files` reveal documentation-file presence, and `change_type` is manually assigned during audit. A future runner may predict change type from the diff, but it must not receive the gold/manual value as input.

3. Run the current DocGuard prediction path only after a real-case adapter exists.
4. Mark unsupported prediction dimensions as `not_evaluated`, not inferred.
5. Save future predictions to `reports/docguard_project_case_study_predictions_2026_08.jsonl`.
6. Save future summary metrics to `reports/docguard_project_case_study_evaluation_2026_08.md`.

## Required Adapter Work

- Map `case_id` to the runtime record id.
- Map `code_diff_excerpt` to `code_diff`.
- Provide a safe project id and `code_changed_files` context.
- Predict or derive change type from `code_diff_excerpt`; do not use manual `change_type`.
- Add project-level category/target mapping beyond the synthetic REST API scenarios.
- Generate patch suggestions without relying on synthetic route-only assumptions.
- Explicitly output `not_evaluated` for category, target-file, or patch usefulness if the adapter cannot support them.

Until that adapter exists, this study should be used as a validated manual case file and evaluation plan, not as an automatic score.
