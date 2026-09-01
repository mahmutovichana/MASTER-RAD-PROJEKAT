# Stage-2 Architecture Challenge V3: Jina code-aware frozen hybrid

Prepared notebook: `notebooks/category_jina_code_hybrid_architecture_challenge_v3.ipynb`

This is the final planned general representation experiment for the Stage-2
four-class category classifier. It tests one change: replace the frozen MiniLM
semantic encoder in the current natural-only hybrid with frozen code-aware
Jina embeddings from `jinaai/jina-embeddings-v2-base-code`.

Frozen data reused exactly from Architecture Challenge V1:

- `data/final_v2/architecture_challenge_v1/natural_train_primary_four.jsonl` (1038 rows)
- `data/final_v2/architecture_challenge_v1/natural_validation_primary_four.jsonl` (322 rows)
- validation case-id SHA256: `aac3384de6d482abefb4201091bf828d6d8c1c91c1ddbdad40a4ec7273051e3e`

The notebook resolves the exact Hugging Face model revision at runtime, keeps
Jina frozen, uses repository only for grouping/audit, and writes lightweight
outputs to this directory. Large embedding caches under `cache/` are
regenerable and ignored by Git.
