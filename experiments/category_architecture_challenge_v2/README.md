# Stage-2 Architecture Challenge V2

Prepared notebook: `notebooks/category_modernbert_architecture_challenge_v2.ipynb`

This stage tests one bounded hypothesis: whether a long-context joint Transformer
(`answerdotai/ModernBERT-base`) improves over the frozen natural-only hybrid and the CodeBERT
512-token architecture challenge by retaining substantially more code/document
evidence.

Frozen data reused exactly from V1:

- `data/final_v2/architecture_challenge_v1/natural_train_primary_four.jsonl` (1038 rows)
- `data/final_v2/architecture_challenge_v1/natural_validation_primary_four.jsonl` (322 rows)
- `data/final_v2/architecture_challenge_v1/export_manifest.json` (authoritative manifest)

Guardrails:

- no confirmation access;
- no controlled/synthetic rows;
- no data acquisition;
- no label or membership changes;
- no class balancing;
- repository identity is only used for grouping/audit, not model input.

Colab output target:

- `experiments/category_architecture_challenge_v2/modernbert_long_context/`

Expected normal Colab T4 branch: `MAX_LENGTH=2048`.
