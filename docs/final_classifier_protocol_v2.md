# DocGuard Final Classifier Protocol V2

This protocol defines the final thesis-safe classifier infrastructure for DocGuard.

## Shared Inputs

Binary V4 and Category V8 use the same model-facing serializer from `docguard_ml_v2.data_contract`. The only safe fields are:

- `language`
- `code_changed_files`
- `code_diff_excerpt`
- `docs_before_excerpt`

File paths are allowed only as raw text through `code_changed_files`. The final classifiers do not use gold target files, documentation-after text, PR titles, source URLs, human notes, documentation diffs, or hand-authored path flags.

## Repository Partitions

Both classifiers inherit the Final V2 repository partitions:

- `development_train`
- `development_validation`
- `confirmation`

Model development may use only `development_train` and `development_validation`. Training scripts do not accept confirmation or test arguments. Confirmation evaluation is implemented in separate scripts and requires a model freeze manifest.

## Binary V4

Binary V4 predicts `gold_docs_update_required`. All eligible human-reviewed rows are included unless explicitly marked excluded or invalid. `other_documentation` remains a positive binary example. Natural class imbalance is preserved; no balancing or label-based resampling is used.

Candidate models are frozen before confirmation:

- word TF-IDF + LogisticRegression
- char TF-IDF + LogisticRegression
- word+char TF-IDF + LogisticRegression

Selection uses development validation only. The primary selection metric is MCC, with balanced accuracy, F1, precision, recall, and specificity as secondary metrics. Threshold selection also uses development validation only.

## Category V8

Category V8 is the primary four-class Stage-2 classifier. Eligible rows must be human-positive and have `gold_doc_category` exactly equal to one of:

- `api_reference`
- `configuration`
- `developer_setup`
- `model_contract`

`other_documentation` is valid dataset taxonomy but excluded from primary four-class Stage-2 training. No aliases are used.

The Stage-2 coverage ratio is:

`primary-four positive rows / all positive rows`

The primary Category V8 selection metric is macro-F1 on development validation.

## Freeze And Confirmation

After development selection, `scripts/freeze_final_model_v2.py` creates an immutable freeze manifest with model, config, dataset, split, and partition hashes. The freeze manifest records `confirmation_accessed = false`.

Confirmation evaluation is separate:

- `scripts/evaluate_binary_v4_confirmation.py`
- `scripts/evaluate_category_v8_confirmation.py`

These scripts validate the freeze manifest, refuse inconsistent model hashes, do not tune thresholds or hyperparameters, and can enforce one-shot evaluation receipts.

## Reporting

Training reports include train metrics, validation metrics, train-validation gaps, natural class prevalence, majority baselines, per-language metrics where support is sufficient, config hashes, safe fields, Python/scikit-learn/joblib versions, platform, and seed.

Binary confirmation reports include accuracy, precision, recall, F1, specificity, balanced accuracy, MCC, ROC AUC, average precision, confusion matrix, language-specific metrics, and deterministic bootstrap confidence intervals for major metrics.

Category confirmation reports separate Stage-2 intrinsic evaluation from any later end-to-end conditional evaluation. The intrinsic category score is the primary Category V8 confirmation metric.

## Historical Boundary

Historical V2/V3 binary results and V4-V7 category results remain useful development evidence. Final Binary V4 and Final Category V8 are the final classifier infrastructure for the independent Final V2 confirmation flow.
