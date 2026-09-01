# Stage-2 configuration vs developer_setup specialist V2

This is the final bounded Stage-2 specialist experiment. It keeps the frozen
winning MiniLM hybrid representation unchanged and varies only the binary
decision layer: developer_setup class weight and decision threshold.

Data: `data/final_v2/configuration_setup_specialist_v1/natural_train_configuration_setup.jsonl`

- rows: 365
- category counts: {'configuration': 277, 'developer_setup': 88}
- SHA256: `bae86d28a07883dc0fac8a0c6919cbd1e3adf9f50b1f2143289c69e0a9a7c495`
- frozen 322 validation accessed: no
- confirmation/refresh validation accessed: no
- controlled/synthetic rows used: no

Representation:

- encoder: `sentence-transformers/all-MiniLM-L6-v2`
- revision: `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`
- chunking: 1000 chars, max 2 chunks per side
- semantic features: code, docs, abs diff, product, cosine
- lexical channel: code-only char_wb TF-IDF 3–5 grams, min_df=2, max_features=20000
- classifier: LogisticRegression(C=1.0, solver='lbfgs', max_iter=2000, random_state=42)

V2 selection:

- outer CV: 5-fold repository-grouped OOF, reusing exact V1 fold membership only if an integrity-usable fold manifest with eval case IDs is supplied
- inner CV: repository-grouped 4-fold, structural fallback to 3-fold
- class weights: [{'name': 'none', 'value': None, 'rank': 0}, {'name': 'developer_1_5', 'value': {'configuration': 1.0, 'developer_setup': 1.5}, 'rank': 1}, {'name': 'developer_2_0', 'value': {'configuration': 1.0, 'developer_setup': 2.0}, 'rank': 2}, {'name': 'developer_3_0', 'value': {'configuration': 1.0, 'developer_setup': 3.0}, 'rank': 3}, {'name': 'balanced', 'value': 'balanced', 'rank': 4}]
- thresholds: [0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
- precision floor: developer_setup precision >= 0.3

Colab notebook: `notebooks/category_configuration_vs_developer_setup_specialist_v2.ipynb`
