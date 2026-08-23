# Methodology Freeze — Real Gold Classifier 4k V2

## Status

This document freezes the current primary experimental setup for the real GitHub PR case study.

Primary model:

- `real_gold_classifier_4k_v2`
- selected model: `path_heavy_word_char_logreg`
- selected threshold: `0.80`
- selection objective: `constrained_f1`
- minimum validation precision: `0.90`
- minimum validation specificity: `0.60`

The selected model and threshold are treated as frozen after this point. Any further experiments must be reported as ablations, robustness checks, calibration experiments, or independent replications.

## Primary locked-test result

Locked-test split:

- total cases: `620`
- true positives: `397`
- true negatives: `106`
- false positives: `19`
- false negatives: `98`

Metrics:

- accuracy: `0.8113`
- precision: `0.9543`
- recall: `0.8020`
- F1: `0.8716`
- specificity: `0.8480`
- false positive rate: `0.1520`
- MCC: `0.5550`
- ROC AUC: `0.8972`
- average precision: `0.9732`

## Leakage policy

The classifier is allowed to use only safe pre-decision input fields:

- `language`
- `code_changed_files`
- `code_diff_excerpt`
- `docs_before_excerpt`

The following fields must not be used as model input:

- `gold_docs_update_required`
- `gold_doc_category`
- `label_confidence`
- `label_source`
- `manual_label_notes`
- `source_url`
- `pr_title`
- `docs_changed_files`
- `docs_after_excerpt`
- `docs_diff_excerpt`
- `candidate_type`
- `swept_binary_correct`
- `pred_docs_update_required`
- `pred_probability`

These fields may be used for evaluation, reporting, audit, error analysis, or label-quality review, but not for model input.

## Model-selection policy

Model selection and threshold selection are performed using the validation split only.

The locked-test split is used only for final reporting and must not be used for:

- choosing model family
- choosing threshold
- choosing feature set
- deciding whether to accept or reject a model variant
- tuning path features or other representation choices

## Labeling statement

The 4k dataset labels are protocol-derived large-scale labels. They are not claimed to be fully human-reviewed labels.

A separate blind manual audit should be performed on a stratified subset to estimate label quality and disagreement patterns.

## Synthetic-data statement

Synthetic examples are not used as the primary final evidence.

Synthetic examples may be used only for:

- controlled demonstrations
- regression tests
- pipeline validation
- qualitative examples

The primary quantitative evidence is based on real public GitHub pull-request cases.

## Known limitations

The strongest performance is observed on TypeScript repositories.

Python remains the main limitation due to low recall. This limitation must be reported explicitly and should be addressed through additional Python data, stratified repository splitting, and independent replication.

The validation split used in the 4k V2 run does not provide enough Python coverage for language-specific threshold calibration.

## Next allowed experiments

The following follow-up experiments are allowed, but they must be reported separately from the frozen V2 primary result:

1. raw-path ablation without manual path flags
2. blind manual label audit
3. repository-group stratified split by language and candidate type
4. additional Python-focused real PR collection
5. GroupKFold / leave-repository-out robustness
6. validation-only probability calibration
7. TF-IDF + embedding late fusion using only safe input fields