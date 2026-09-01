# Stage-2 hierarchical integration pilot V1

This pilot integrates the frozen four-class MiniLM hybrid model with the nested
cost-sensitive configuration/developer_setup Specialist V2. It is a paired
repository-grouped OOF train-side pilot only.

Data:

- `data/final_v2/architecture_challenge_v1/natural_train_primary_four.jsonl`
- rows: 1038
- counts: {'api_reference': 412, 'configuration': 277, 'developer_setup': 88, 'model_contract': 261}
- SHA256: `9dc1136f1cf695eb69c70b763ad051898aa5fae351fcf028eed97116c8891f99`

Frozen representation:

- encoder: `sentence-transformers/all-MiniLM-L6-v2`
- revision: `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`
- semantic chunking: 1000 chars, max 2 chunks per side
- code TF-IDF: char_wb 3–5 grams, min_df=2, max_features=20000
- classifier family: LogisticRegression only

Routing rule:

Route iff the general four-class prediction is `configuration` or
`developer_setup`. API and model-contract general predictions remain unchanged.

Specialist decision grid:

- class weights: [{'name': 'none', 'value': None, 'rank': 0}, {'name': 'developer_1_5', 'value': {'configuration': 1.0, 'developer_setup': 1.5}, 'rank': 1}, {'name': 'developer_2_0', 'value': {'configuration': 1.0, 'developer_setup': 2.0}, 'rank': 2}, {'name': 'developer_3_0', 'value': {'configuration': 1.0, 'developer_setup': 3.0}, 'rank': 3}, {'name': 'balanced', 'value': 'balanced', 'rank': 4}]
- thresholds: [0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
- precision floor: 0.3

Notebook: `notebooks/category_stage2_hierarchical_integration_pilot_v1.ipynb`

The frozen 322-row development validation is not required and must not be
loaded by this pilot.
