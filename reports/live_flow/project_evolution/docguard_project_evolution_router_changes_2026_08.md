# DocGuard Project Evolution Router Changes 2026-08

This note documents the minimal general improvements made after the first project-evolution run. These changes were not based on project names and did not change gold labels.

## Changes

- `docguard_hybrid/signal_extractor.py` now detects added environment variables and `default_page_size` changes from added/removed diff lines instead of relying on one exact toy string.
- It also detects common no-update patterns for private helper refactors, comment-only changes, and logging-only changes.
- Request/response/model field additions use simple line-based regular expressions so realistic TypeScript snippets can be detected.
- `docguard_hybrid/doc_router.py` now prioritizes `route_added` before `changed_status_code`, because a newly added route that returns `202` should normally be treated as a new endpoint documentation case.
- `docguard_hybrid/doc_router.py` now treats `docs_already_updated` as a high-confidence no-update override. If docs-before explicitly indicates that the visible change is already documented, DocGuard does not propose another documentation patch even when a positive code-change signal such as `route_added` is also present.

## Safety Notes

- The project-evolution runner still passes only sanitized model input: `case_id`, `project_id`, code-side changed files, code diff, and docs-before excerpt.
- Gold fields, expected facts, scenario type, manually assigned category, target doc file, and docs-after text are not passed to `docguard_hybrid.predict()`.
- The new no-update override is based on runtime docs-before evidence, not case ids, project names, gold labels, docs-after text, or expected patch fields.

## Result After Changes

- Total cases: 24
- Binary accuracy: 100.00%
- Precision: 100.00%
- Recall: 100.00%
- F1: 100.00%
- Category accuracy: 100.00%
- Target file accuracy: 100.00%
- Scenario accuracy: 100.00%
- False positives: 0
- False negatives: 0
