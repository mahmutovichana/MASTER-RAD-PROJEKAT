# External Deep-JIT Frozen Code Encoder Comparison 2026-08

Status: deferred / locally blocked for a full run.

The frozen code-encoder baseline has been implemented in `docguard_external/train_code_encoder_binary.py` and exposed through `python -m docguard_external.cli train-code-encoder-binary`.

## Local Availability Check

- `torch`: available
- `transformers`: available
- CUDA/GPU: unavailable (`torch.cuda.is_available() == False`)

## Why The Full Run Was Not Executed Here

The combined-validation benchmark contains 23,508 train records, 2,630 validation records, and 2,906 test records. Extracting UniXcoder/CodeBERT/GraphCodeBERT embeddings for this full split on CPU would likely take substantially longer than the current improvement pass and may require large model downloads.

No encoder result is fabricated. The classical v2 baseline was run fully and already exceeds the minimum target result, so the encoder baseline is best treated as the next optional GPU/Colab experiment.

## Implemented Command

```bash
python -m docguard_external.cli train-code-encoder-binary --train data/external/deep_jit_binary_combined_validation/train.jsonl --validation data/external/deep_jit_binary_combined_validation/validation.jsonl --test data/external/deep_jit_binary_combined_validation/test.jsonl --model-output models/external_deep_jit_code_encoder/binary_code_encoder.joblib --report reports/external_deep_jit_frozen_code_encoder_comparison_2026_08.md --cache-dir data/external/embedding_cache --encoder microsoft/unixcoder-base
```

## Evaluation Guardrails

- Use combined validation only for model selection.
- Evaluate once on untouched test.
- Report Return and Summary subset metrics separately.
- Do not use `new_comment_raw`, `doc_after`, or `doc_diff` as input.
