# Final V2 Gold Dataset Card

- Gate 1 status: **PASS**
- Canonical dataset: `experiments/consolidated_enriched_training_v2/gold/final_human_gold.jsonl`
- Canonical SHA-256: `68ebe23ab4dd8a02ee1ea459e3b6a374a3efa2891afc8d344a533676eb3b5a08`
- Rows: **25,913**
- Positive: **5,948 (22.95%)**
- Negative: **19,965**
- Repositories: **284**

## Category distribution

- `api_reference`: **1,554**
- `configuration`: **1,467**
- `developer_setup`: **992**
- `model_contract`: **1,122**
- `no_update`: **19,965**
- `other_documentation`: **813**

## Source distribution

- `consolidated_enriched_training_v1`: **21,080**
- `controlled_real_project_positive_v1`: **2,000**
- `controlled_real_project_positive_v2_imbalanced`: **2,000**
- `natural_diversity_expansion_v1`: **779**
- `remaining_4800_partial_positive_54`: **54**

## Split distribution

- `development_train`: **19,018 rows, 5,199 positive, 13,819 negative, 191 repositories**
- `development_validation`: **3,148 rows, 348 positive, 2,800 negative, 41 repositories**
- `confirmation`: **3,747 rows, 401 positive, 3,346 negative, 52 repositories**

Natural Diversity Expansion V1 is included in this frozen gold dataset: 779/779 completed approved rows.
Controlled positive augmentation remains development-train-only. The confirmation split is sealed and was not used for model selection or Gate 1 evaluation.
