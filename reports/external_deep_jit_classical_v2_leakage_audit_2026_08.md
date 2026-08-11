# External Deep-JIT Classical V2 Leakage Audit 2026-08

## Scope

Audited file: `docguard_external/train_binary_classifier_v2.py`

Audited primary result:

- Model: `logreg_balanced`
- Feature set: `word_char_tfidf_plus_manual_features`
- Input mode: `old_comment_plus_code_diff`
- Test result: 75.60% accuracy, 78.84% precision, 69.99% recall, 74.15% F1, 18.79% FPR, 81.21% specificity, MCC 0.5153

## Audit Result

Leakage audit status: passed with one interpretation note.

The v2 primary model can be treated as a methodologically safe Deep-JIT external proxy result, provided it continues to be described as a code-comment consistency proxy rather than the full Markdown DocGuard benchmark.

## Checks

| Check | Result | Evidence |
| --- | --- | --- |
| `old_comment_plus_code_diff` uses only old/current comment and code diff | Passed | `text_for_mode()` builds this mode from `old_comment_raw`/`doc_before` and `code_diff` only. |
| Manual features avoid `new_comment_raw` | Passed | `ManualFeatureExtractor._features()` never reads `new_comment_raw`. |
| Manual features avoid `doc_after` | Passed | `ManualFeatureExtractor._features()` never reads `doc_after`. |
| Manual features avoid `doc_diff` | Passed | `ManualFeatureExtractor._features()` never reads `doc_diff`. |
| Manual features avoid direct labels | Passed | Feature extraction does not read `docs_update_required`, `label`, or `raw_label`. `docs_update_required` is used only by `labels()` to create training/evaluation targets. |
| Manual features avoid source filename leakage | Passed | Feature extraction does not read `metadata.source_file`, `source_file`, `record_id`, repository, or raw filename. |
| Return/Summary subset names are not predictive features | Passed | `subset()` is used only by `evaluate_by_subset()` after prediction. It is not part of `feature_union()` or `ManualFeatureExtractor`. |
| Test is not used for feature/model selection | Passed | `train_and_evaluate_v2()` fits features on train, evaluates candidates on validation, selects by validation MCC/balanced accuracy/F1, and reports test after selection. |
| Best model selected by validation only | Passed | `best = max(trained, key=lambda row: (row["validation"]["mcc"], row["validation"]["balanced_accuracy"], row["validation"]["f1"]))`. |

## Interpretation Note

`ManualFeatureExtractor` can read `new_code_raw` for `old_comment_plus_old_new_code` mode because that input mode explicitly includes old and new code. The primary v2 result uses `old_comment_plus_code_diff`, where manual features expose only old comment and code diff-derived signals. No future documentation fields are used.

## Remaining Caveats

- Deep-JIT label polarity remains `plausible_manual_verification_needed`.
- Deep-JIT remains a code-comment inconsistency proxy, not a project-level Markdown documentation update benchmark.
- Manual features are safe under the audited implementation, but they are still hand-engineered and should be presented as classical feature engineering rather than semantic reasoning.
