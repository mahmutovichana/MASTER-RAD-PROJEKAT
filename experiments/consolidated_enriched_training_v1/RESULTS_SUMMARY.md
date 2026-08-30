# Consolidated enriched training v1 — results

## Dataset and repository split

- Total rows: **21,080**
- Positive rows: **1,885 (8.94%)**
- Development train: **14,465 rows / 153 repositories**
- Development validation: **3,028 rows / 38 repositories**
- Sealed confirmation: **3,587 rows / 48 repositories**
- Repository overlap across partitions: **0**

## Binary V4 — development validation

- Selected model: `char_tfidf_logreg_c0.25_mindf1`
- Selected threshold: **0.25**
- Accuracy: **0.9551**
- Precision: **0.8439**
- Recall: **0.7405**
- F1: **0.7888**
- Specificity: **0.9825**
- Balanced accuracy: **0.8615**
- MCC: **0.7659**
- ROC-AUC: **0.9192**
- Confusion matrix: TN **2,638**, FP **47**, FN **89**, TP **254**

Python remains a severe weakness: the validation split contains only 14 positive
Python rows and the selected threshold predicts none of them as positive.

## Category V8 — development validation

- Selected model: `char_tfidf_logreg_c4.0_mindf2`
- Eligible validation positives: **322**
- Accuracy: **0.4876**
- Macro-F1: **0.3776**
- Weighted-F1: **0.4744**
- Balanced accuracy: **0.4109**
- API reference F1: **0.4941**
- Configuration F1: **0.5082**
- Developer setup F1: **0.0000**
- Model contract F1: **0.5079**

The category model has a large train/validation gap and predicts no
`developer_setup` cases. This class is the highest-priority target for further
positive enrichment. Repository diversity is at least as important as raw row
count because the split is repository-disjoint.

## Full Binary V4 → Category V8 → grounded generation cascade

Evaluated on all **3,587 sealed confirmation rows**:

- Binary accuracy: **0.9161**
- Binary precision: **0.6534**
- Binary recall: **0.5312**
- Binary F1: **0.5860**
- Binary specificity: **0.9645**
- TN **3,073**, FP **113**, FN **188**, TP **213**
- Predicted positives: **326**
- Generated patches: **326/326 (100%)**
- Category accuracy conditioned on correctly detected/evaluable positives: **0.4111**
- Verifier: **3,474 pass**, **16 warn**, **97 fail**
- Quality labels: **3,372 excellent**, **102 usable**, **16 needs_review**, **97 rejected**

The earlier cascade F1 of approximately 0.947 was measured on only 486 heavily
positive-enriched cases and is not directly comparable with this repository-
disjoint, mostly-negative confirmation set.

## Leakage and integrity

- Model input fields: `language`, `code_changed_files`, `code_diff_excerpt`,
  `docs_before_excerpt`
- Gold labels, docs-after, manual notes and source URL were not used for prediction.
- Completion/taxonomy/hash audit: **PASS**, 21,080/21,080 rows.
- Classifier infrastructure tests: **13 passed**.
