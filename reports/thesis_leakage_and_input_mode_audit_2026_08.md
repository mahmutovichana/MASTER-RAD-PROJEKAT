# Thesis Leakage And Input-Mode Audit 2026-08

## Summary

No active primary evaluation path was found to silently include future documentation text. The main fair/assisted CoDocBench modes are clean, Deep-JIT training inputs exclude future comments, and upper-bound modes are clearly labeled. The remaining risk is conceptual: normalized records store future fields for audit, so thesis text must distinguish stored fields from model input fields.

## Module Audit

| File | Input construction checked | Status | Notes |
| --- | --- | --- | --- |
| `docguard_external/evaluate_existing_docguard.py` | CoDocBench `code_diff_only`, `code_diff_plus_doc_before`, `code_diff_plus_doc_diff_upper_bound` | ok | `code_diff_only` sets docs excerpt to empty. `code_diff_plus_doc_before` uses only `doc_before`. Upper-bound mode uses `doc_diff` and is explicitly labeled `upper_bound_leakage_risk`. |
| `docguard_external/evaluate_existing_docguard.py` | Fallback handling | ok | `code_diff_plus_doc_before` now errors if `doc_before` is missing, preventing fallback to `doc_diff`. |
| `docguard_external/evaluate_binary.py` | Deep-JIT zero-shot bridge | ok with caveat | Uses `doc_before` as current comment and `code_diff`; does not use `doc_after`/`doc_diff` as model input. The report examples display `doc_diff` for audit only. |
| `docguard_external/train_binary_classifier.py` | `old_comment_plus_code_diff` | ok | Uses `old_comment_raw` and generated `code_diff`; excludes `new_comment_raw`, `doc_after`, and `doc_diff`. |
| `docguard_external/train_binary_classifier.py` | `code_diff_only` | ok | Uses generated `code_diff` only. No comment text is included. |
| `docguard_external/train_binary_classifier.py` | `old_comment_plus_old_new_code` | ok | Uses old comment and code before/after; no future updated comment. |
| `docguard_external/train_binary_classifier.py` | `old_comment_plus_new_code` | ok | Uses old comment and new code; no future updated comment. This is a plausible detection input because changed code is known at review time. |
| `docguard_external/codocbench_adapter.py` | Normalized CoDocBench mapping | ok with caveat | Stores `doc_after`/`doc_diff` for labels/audit. Evaluation modes decide whether these fields enter model input. |
| `docguard_external/docchecker_adapter.py` | 500-record binary proxy mapping | ok with caveat | Stores `doc_after` and `doc_diff` for audit. Zero-shot evaluation does not feed them into model input. |
| `docguard_external/deep_jit_binary.py` | Normalized Deep-JIT export | ok | Stores `new_comment_raw`/`doc_after`/`doc_diff` for audit. Export report explicitly says training module input builders do not include them. |

## Direct Checks

- CoDocBench fair mode `code_diff_only`: clean. It includes changed file metadata and code diff, with no documentation text.
- CoDocBench assisted mode `code_diff_plus_doc_before`: clean for primary reporting. It includes current documentation before the update, not future documentation.
- CoDocBench upper-bound mode: leaky by design and correctly labeled as `upper_bound_leakage_risk`.
- Deep-JIT `old_comment_plus_code_diff`: clean. It uses old comment and code diff only.
- Deep-JIT `code_diff_only`: clean.
- Deep-JIT normalized records: contain future comment fields, but those fields are not used by `input_text`.

## Risk Rating

| Risk | Rating | Mitigation |
| --- | --- | --- |
| Silent CoDocBench future-doc fallback | low | Current code blocks missing `doc_before` in assisted mode and labels upper-bound mode. |
| Deep-JIT future-comment leakage in classifier | low | Input builder excludes `new_comment_raw`, `doc_after`, and `doc_diff`. |
| Reader confusion because audit records store future fields | moderate | Thesis should say future fields are retained for audit/label provenance only, not model input. |

## Verdict

No primary thesis result appears invalid due to leakage. The thesis should keep input-mode terminology explicit: strict fair (`code_diff_only`), assisted fair (`doc_before` only), and upper-bound/leakage-risk (`doc_diff`).
