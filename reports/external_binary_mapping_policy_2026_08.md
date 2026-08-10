# External Binary Mapping Policy 2026-08

External binary/inconsistency datasets must be kept separate from synthetic labels and from CoDocBench positive-only labels.

## Explicit Inconsistent / Outdated Comment Examples

- `docs_update_required = true`
- `label_source = strong_external_inconsistent_comment`
- `target_kind = comment_or_docstring`
- `scenario_type = external_comment_inconsistency`

These examples mean the code-comment pair is explicitly labeled inconsistent or outdated by the external dataset.

## Explicit Consistent / Up-To-Date Comment Examples

- `docs_update_required = false`
- `label_source = strong_external_consistent_comment`
- `target_kind = comment_or_docstring`
- `scenario_type = external_comment_consistent_no_update`

These examples mean the code-comment pair is explicitly labeled consistent or up to date.

## Reporting Rules

- Do not mix external binary labels with synthetic labels without source-specific reporting.
- Do not promote mined weak negatives to strong negatives.
- Keep `strong_external_*`, `weak_negative_*`, `strong_positive_code_doc_cochange`, and synthetic labels separate in metrics tables.

## Caveat

Code-comment consistency is not identical to project-level Markdown documentation update detection. It is still a defensible external binary proxy for documentation consistency because it directly evaluates whether code and associated natural language documentation/comment text agree.
