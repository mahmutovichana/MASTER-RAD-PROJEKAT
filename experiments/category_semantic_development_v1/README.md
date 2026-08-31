# Category semantic development v1

This development-only experiment compares relational semantic, hybrid, and two-channel lexical representations on the unchanged natural repository-disjoint validation set. Confirmation data was not accessed.

## Best result

- Candidate: `hybrid__natural_plus_controlled__ovr_logreg`
- Natural validation Macro-F1: **0.4542**
- Balanced accuracy: **0.4645**
- developer_setup F1: **0.0741**
- Category V8 baseline Macro-F1: **0.3817**

## Controlled-data utility

- `semantic` Macro-F1 delta (controlled − natural): **-0.0340**
- `hybrid` Macro-F1 delta (controlled − natural): **-0.0174**
- `two_channel_lexical` Macro-F1 delta (controlled − natural): **-0.0176**
- `semantic_code_only` Macro-F1 delta (controlled − natural): **-0.0161**

## Reproduction

```powershell
py scripts/run_category_semantic_development_v1.py --train experiments/consolidated_enriched_training_v2/gold/train.jsonl --validation experiments/consolidated_enriched_training_v2/gold/validation.jsonl --baseline-predictions reports/category_v8_development_diagnostics_v1/phases_1_5/category_v8_validation_error_analysis.jsonl --baseline-config configs/category_classifier_v8.json --baseline-model experiments/consolidated_enriched_training_v2/category_v8/category_v8.joblib --output-dir experiments/category_semantic_development_v1 --embedding-cache-dir data/external/embedding_cache/category_semantic_development_v1 --model-cache-dir data/external/embedding_cache/huggingface_models
```

Downloaded model and embedding matrices are regenerable, gitignored, and not part of the committed experiment artifacts.
