# Consolidated enriched training v2 — results

## Dataset

- Total rows: **25,134**
- Positive: **5,939 (23.63%)**
- Negative: **19,195**
- Controlled train-only augmentation: **4,000**
- Additional reviewed natural positives: **54**
- Validation: **PASS**

## Leakage-safe split

- Development train: **18,519**
- Development validation: **3,028**
- Sealed confirmation: **3,587**
- Controlled/new augmentation is development-train-only.
- Validation and confirmation case membership is unchanged from v1.
- Repository overlap across splits: **0**

## Binary V4 — unchanged natural validation

- Selected model: `char_tfidf_logreg_c0.25_mindf1`; threshold: **0.25**
- Accuracy: **0.9515**
- Precision: **0.8161**
- Recall: **0.7376**
- F1: **0.7749** (v1 0.7888, delta -0.0139)
- Balanced accuracy: **0.8582**
- MCC: **0.7490** (v1 0.7659, delta -0.0169)
- ROC-AUC: **0.9113** (v1 0.9192, delta -0.0079)
- Confusion matrix: TN **2,628**, FP **57**, FN **90**, TP **253**

## Category V8 — unchanged natural validation

- Selected model: `char_tfidf_logreg_c4.0_mindf1`
- Accuracy: **0.4876**
- Macro-F1: **0.3817** (v1 0.3776, delta +0.0042)
- Weighted-F1: **0.4754**
- Balanced accuracy: **0.4181**

- `api_reference` F1: **0.5019** (v1 0.4941, delta +0.0078)
- `configuration` F1: **0.4979** (v1 0.5082, delta -0.0103)
- `developer_setup` F1: **0.0000** (v1 0.0000, delta +0.0000)
- `model_contract` F1: **0.5271** (v1 0.5079, delta +0.0192)

## Interpretation

The augmentation substantially improves training fit but does not materially improve natural repository-disjoint validation. Binary generalization is slightly worse; category macro-F1 is only marginally better, and developer_setup remains undetected. Controlled template volume should therefore not be treated as a substitute for diverse natural positive repositories.
