# Real LLM Evaluation Notes v0.3

## CPU-Only Environment

- backend: `transformers_local`
- model: `qwen2_5_coder_0_5b`
- torch: `2.9.1+cpu`
- CUDA available: `False`

## Successful 0.5B Smoke Tests

The sanity-only smoke test generated fenced JSON containing `{"ok": true}` and is now parsed as successful. This confirms that the local Hugging Face Transformers generation path works on the CPU-only machine.

The compact DocGuard smoke test on `support-ticket-api-001` also succeeded:

- parse_success: true
- output_usable: true
- latency: about 23.6 seconds
- predicted `docs_update_required=true`
- selected `docs/configuration.md`
- selected `Environment Variables`
- summarized the added `REVIEW_FEATURE_FLAG`

## Tiny Limit-3 Evaluation

The first compact real evaluation used 3 validation records with `DOCGUARD_MAX_NEW_TOKENS=120`.

- records: 3
- precision: 100%
- recall: 66.67%
- F1: 80%
- normalized scenario accuracy: 0%
- normalized doc category accuracy: 33.33%
- normalized target file accuracy: 33.33%
- raw doc category accuracy: 0%
- patch fact coverage: 66.67%
- parse errors: 1
- average latency: about 20.76 seconds

## Strict vs Normalized Metrics

The first real model outputs are semantically better than strict string metrics suggest. For example, the model produced `Configuration`, which normalizes to the dataset label `configuration`. The evaluator now reports both strict raw accuracy and normalized accuracy so thesis analysis can distinguish formatting/casing misses from actual semantic misses.

Broad labels such as `API Change` and `integration` are not automatically treated as exact scenario matches. They normalize to `unknown_change` unless there is a clear dataset-specific signal such as environment-variable, background-job, or local-development evidence.

## Parse Error Discussion

One output was truncated near the `"confidence` key when `DOCGUARD_MAX_NEW_TOKENS=120`. The parser now marks likely incomplete JSON as `parse_error_type=truncated_json`. Real evaluation can optionally retry such rows once with `--retry-on-parse-error`, increasing the generation budget by 100 tokens for that retry.

## CPU-Only Latency

The 0.5B model takes roughly 20-24 seconds per compact record on this CPU-only setup. That is acceptable for pipeline validation and tiny samples, but not for broad evaluation. The 1.5B compact prompt did not complete visibly on this machine, so 1.5B/3B/7B runs should move to GPU, Colab/Kaggle, or vLLM/TGI.

## Interpretation

`qwen2_5_coder_0_5b` is useful for validating the real local inference pipeline, JSON parsing, normalization, retry behavior, incremental JSONL writing, and report generation. It should not be presented as final model quality. The final quality comparison should use larger models, especially 1.5B/3B/7B, on a more suitable runtime.

## Next Planned Evaluation

Run tiny 0.5B CPU checks with a larger generation budget:

```powershell
$env:DOCGUARD_MAX_NEW_TOKENS="180"
python -m docguard_llm.cli evaluate --split validation --model qwen2_5_coder_0_5b --backend transformers_local --limit 3 --compact-prompt --continue-on-error --retry-on-parse-error
```

Then move 1.5B/3B/7B evaluation to GPU, Colab/Kaggle, or a vLLM/TGI-compatible server.
