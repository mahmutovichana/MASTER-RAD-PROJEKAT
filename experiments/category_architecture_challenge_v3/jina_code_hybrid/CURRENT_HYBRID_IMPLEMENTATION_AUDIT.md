# Current hybrid implementation audit

This audit documents the frozen Stage-2 hybrid pipeline that V3 must match as closely as possible.

- Current frozen model: `hybrid__natural_only__multinomial_logreg__natural_diversity_expansion_v1`
- Source scripts inspected:
  - `scripts/run_category_semantic_development_v1.py`
  - `scripts/run_natural_diversity_refresh_category_v1.py`
- Frozen V1 train rows reused for V3: 1038
- Frozen V1 validation rows reused for V3: 322
- Validation case-id SHA256: `aac3384de6d482abefb4201091bf828d6d8c1c91c1ddbdad40a4ec7273051e3e`
- Train/validation repository overlap: 0

## Matched lexical channel

- Input: sanitized code side only (`language`, `code_changed_files`, `code_diff_excerpt`).
- Vectorizer: `TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=2, max_features=20000, sublinear_tf=True, dtype=np.float32)`.
- Fit policy: fit only on training rows; transform internal eval/development validation.

## Matched semantic relational channel

- Current encoder being replaced: `sentence-transformers/all-MiniLM-L6-v2` revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`.
- V3 encoder: `jinaai/jina-embeddings-v2-base-code` frozen, resolved to an exact Hugging Face SHA at Colab runtime.
- Separate embeddings: `E_code = encoder(code_side)`, `E_docs = encoder(docs_before)`.
- Relational features: `E_code`, `E_docs`, `abs(E_code - E_docs)`, `E_code * E_docs`, `cosine(E_code, E_docs)`.
- Embeddings are normalized; cosine is therefore dot product.

## Matched scalar features

Seven lexical relational scalars are reused: shared-token log count, shared/union ratio, shared/min-side ratio, identifier overlap ratio, changed-path token overlap ratio, log code length, log docs length.

## Matched classifier

- Classifier: `LogisticRegression(C=1.0, solver="lbfgs", max_iter=2000, random_state=42)`.
- Class weights: none.
- Resampling: none.
- No grid search, no threshold tuning, no class balancing.

## Primary controlled change

Only the frozen semantic encoder changes from MiniLM to Jina code-aware embeddings. The lexical feature family, relational feature construction, sparse/dense concatenation, and Logistic Regression configuration remain matched.
