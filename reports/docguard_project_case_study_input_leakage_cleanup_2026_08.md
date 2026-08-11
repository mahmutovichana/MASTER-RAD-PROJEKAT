# DocGuard Project Case Study Input Leakage Cleanup 2026-08

## Why Cleanup Was Needed

`changed_files` was risky as an automatic model input because positive cases often include documentation paths such as `README.md`, `docs/...`, or `openapi.json`, while negative cases often do not. A runner could learn documentation-file presence instead of code/documentation consistency.

Negative `docs_before_excerpt` values also contained audit text about missing documentation files. That wording is useful for reviewers but leaks label-related evidence if fed to a model.

## Cleanup Performed

- Added `code_changed_files` and `docs_changed_files` to the schema.
- Kept `changed_files` as audit metadata only.
- Moved `docs_changed_files`, `changed_files`, and manually assigned `change_type` to audit-only fields.
- Removed `changed_files` and `change_type` from `allowed_model_input_fields`.
- Cleaned negative-case `docs_before_excerpt` audit text for cases: ``GH-PROJ-016`, `GH-PROJ-017`, `GH-PROJ-018`, `GH-PROJ-019`, `GH-PROJ-020``.

## Final Safe Model Input Fields

- `language`
- `code_changed_files`
- `code_diff_excerpt`
- `docs_before_excerpt`

## Final Audit-Only Fields

- `changed_files`
- `docs_changed_files`
- `change_type`
- `docs_after_excerpt`
- `gold_*`
- `manual_label_notes`
- `label_confidence`

## Validation Result

- Real case file: passed validation on 20 records.
- Template file: passed validation on 4 records.
- Validator now errors if `allowed_model_input_fields` contains `changed_files`, `docs_changed_files`, `change_type`, `docs_after_excerpt`, or `gold_*` fields.
- Validator now errors if `docs_before_excerpt` contains audit phrases about missing documentation files.

## Remaining Limitations

- Positive labels remain stronger than negative labels because positives have visible code+documentation relation.
- Three negative cases remain low confidence and should be replaced or manually confirmed before final quantitative claims.
- Automatic runner remains deferred; no DocGuard case-study score is reported.
- `code_changed_files` may still contain filenames that hint at tests/config/API areas, but it no longer exposes documentation-file presence.
