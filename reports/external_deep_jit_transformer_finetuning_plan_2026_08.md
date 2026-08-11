# External Deep-JIT Transformer Fine-Tuning Plan 2026-08

## Recommendation

Use UniXcoder or CodeBERT as a sequence classifier for the Deep-JIT / DocChecker-style binary proxy. This should be treated as an optional improvement path, not as the central DocGuard thesis artifact.

## Experiment Ladder

1. Frozen encoder baseline: extract embeddings from `microsoft/unixcoder-base` or `microsoft/codebert-base`, then train LogisticRegression or LinearSVC.
2. Last-2-layer unfreeze: fine-tune only the classification head and the last two transformer layers.
3. Full fine-tuning: fine-tune all layers with early stopping and conservative learning rate.

## Suggested Colab Plan

```bash
pip install transformers torch scikit-learn joblib
python -m docguard_external.cli train-code-encoder-binary \
  --train data/external/deep_jit_binary_combined_validation/train.jsonl \
  --validation data/external/deep_jit_binary_combined_validation/validation.jsonl \
  --test data/external/deep_jit_binary_combined_validation/test.jsonl \
  --model-output models/external_deep_jit_code_encoder/binary_code_encoder.joblib \
  --report reports/external_deep_jit_frozen_code_encoder_comparison_2026_08.md \
  --encoder microsoft/unixcoder-base
```

For full fine-tuning, add a dedicated sequence-classifier script only after the frozen encoder result is known.

## Evaluation Protocol

- Use only `data/external/deep_jit_binary_combined_validation/`.
- Select checkpoints and thresholds on validation only.
- Evaluate once on untouched test.
- Report Return and Summary subset metrics separately.
- Do not use `new_comment_raw`, `doc_after`, or `doc_diff` as input.

## Risks

- Sequence truncation may remove important code context.
- Deep-JIT label polarity remains a caveat until independently confirmed.
- Fine-tuning may overfit to comment style rather than semantic inconsistency.
- GPU runs can be irreproducible unless seeds, package versions, and model revisions are recorded.
