# Consolidated enriched training corpus v2

- Validation: **PASS**
- Rows: **25,913**
- Positive: **5,948 (22.95%)**
- Negative: **19,965**
- Controlled augmentation rows: **4,000**
- Natural/historical reviewed rows: **21,913**
- Natural Diversity Expansion V1 included rows: **779 / 779**
- Duplicates skipped: **0**

## Categories

- `api_reference`: **1,554**
- `configuration`: **1,467**
- `developer_setup`: **992**
- `model_contract`: **1,122**
- `no_update`: **19,965**
- `other_documentation`: **813**

## Sources

- `consolidated_enriched_training_v1`: **21,080**
- `controlled_real_project_positive_v1`: **2,000**
- `controlled_real_project_positive_v2_imbalanced`: **2,000**
- `natural_diversity_expansion_v1`: **779**
- `remaining_4800_partial_positive_54`: **54**

## Provenance

- `additional_reviewed_natural_positive`: **54**
- `controlled_design_label`: **4,000**
- `natural_human_gold`: **21,859**

Controlled rows use `label_source=controlled_design_label`, `supervision_source=controlled_synthetic_positive`, `independent_human_reviewed=false`, and `train_only=true`. Natural human gold and the 54 additional natural positives use separate provenance values. Controlled rows must remain development-train-only so repository/template leakage cannot inflate validation or sealed-confirmation metrics.
