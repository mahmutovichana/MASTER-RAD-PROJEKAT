# Stage-2 coarse-to-fine hierarchy V1

This is the final train-side Stage-2 architecture experiment. It keeps the
winning frozen MiniLM hybrid representation, replaces the first decision with a
three-way documentation-family classifier, and applies Specialist V2 only
inside `config_setup_family`.

Data:

- `data/final_v2/architecture_challenge_v1/natural_train_primary_four.jsonl`
- rows: 1038
- canonical counts: {'api_reference': 412, 'configuration': 277, 'developer_setup': 88, 'model_contract': 261}
- coarse counts: {'api_reference': 412, 'config_setup_family': 365, 'model_contract': 261}
- SHA256: `9dc1136f1cf695eb69c70b763ad051898aa5fae351fcf028eed97116c8891f99`

Coarse target mapping:

- api_reference -> api_reference
- configuration -> config_setup_family
- developer_setup -> config_setup_family
- model_contract -> model_contract

Frozen representation:

- encoder: `sentence-transformers/all-MiniLM-L6-v2`
- revision: `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`
- semantic chunking: 1000 chars, max 2 chunks per side
- code TF-IDF: char_wb 3–5 grams, min_df=2, max_features=20000
- classifier family: LogisticRegression only

Specialist V2 decision grid:

- class weights: [{'name': 'none', 'value': None, 'rank': 0}, {'name': 'developer_1_5', 'value': {'configuration': 1.0, 'developer_setup': 1.5}, 'rank': 1}, {'name': 'developer_2_0', 'value': {'configuration': 1.0, 'developer_setup': 2.0}, 'rank': 2}, {'name': 'developer_3_0', 'value': {'configuration': 1.0, 'developer_setup': 3.0}, 'rank': 3}, {'name': 'balanced', 'value': 'balanced', 'rank': 4}]
- thresholds: [0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
- precision floor: 0.3

Inference rule:

The specialist runs iff Level 1 predicts `config_setup_family`. Level-1
`api_reference` and `model_contract` predictions finalize directly to those
same canonical labels. There is no post-hoc four-way router and no routing
threshold.

Notebook: `notebooks/category_stage2_coarse_to_fine_hierarchy_v1.ipynb`

The frozen 322-row development validation is not required and must not be
loaded by this train-side pilot.
