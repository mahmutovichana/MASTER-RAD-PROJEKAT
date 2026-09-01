# Final Stage-2 development evaluation V1

This notebook performs the final Stage-2 development-validation comparison.
It is not final external testing.

Candidates:

1. original four-class MiniLM hybrid baseline
2. approved coarse-to-fine hierarchy with Specialist V2

Train:

- path: `data/final_v2/architecture_challenge_v1/natural_train_primary_four.jsonl`
- rows: 1038
- counts: {'api_reference': 412, 'configuration': 277, 'developer_setup': 88, 'model_contract': 261}
- SHA256: `9dc1136f1cf695eb69c70b763ad051898aa5fae351fcf028eed97116c8891f99`

Frozen development validation:

- path: `data/final_v2/architecture_challenge_v1/natural_validation_primary_four.jsonl`
- rows: 322
- counts: {'api_reference': 85, 'configuration': 154, 'developer_setup': 19, 'model_contract': 64}
- case-ID SHA256: `aac3384de6d482abefb4201091bf828d6d8c1c91c1ddbdad40a4ec7273051e3e`

Frozen representation:

- encoder: `sentence-transformers/all-MiniLM-L6-v2`
- revision: `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`
- semantic chunking: 1000 chars, max 2 chunks per side
- code TF-IDF: char_wb 3–5 grams, min_df=2, max_features=20000

Final specialist policy is selected from train data only before validation
scoring. After `STAGE2_TRAIN_FREEZE_COMPLETE`, the notebook evaluates both
candidates once on the same frozen 322-row development-validation split.
