# Consolidated enriched training corpus v2

- Validation: **PASS**
- Rows: **25,134**
- Positive: **5,939 (23.63%)**
- Negative: **19,195**
- Controlled augmentation rows: **4,000**
- Natural/historical reviewed rows: **21,134**
- Duplicates skipped: **0**

## Categories

- `api_reference`: **1,552**
- `configuration`: **1,465**
- `developer_setup`: **989**
- `model_contract`: **1,122**
- `no_update`: **19,195**
- `other_documentation`: **811**

## Sources

- `consolidated_enriched_training_v1`: **21,080**
- `controlled_real_project_positive_v1`: **2,000**
- `controlled_real_project_positive_v2_imbalanced`: **2,000**
- `remaining_4800_partial_positive_54`: **54**

Controlled rows are explicitly marked in-row and in source_provenance.jsonl. They must remain development-train-only so repository/template leakage cannot inflate validation or sealed-confirmation metrics.
