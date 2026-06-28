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

## Limit-10 CPU-Only Evaluation

The latest compact real evaluation used 10 validation records with `DOCGUARD_MAX_NEW_TOKENS=180` and `--retry-on-parse-error`.

- records: 10
- true positives: 6
- true negatives: 4
- false positives: 0
- false negatives: 0
- precision: 100%
- recall: 100%
- F1: 100%
- normalized scenario accuracy: 0%
- normalized doc category accuracy: 10%
- normalized target file accuracy: 10%
- raw scenario accuracy: 0%
- raw doc category accuracy: 0%
- raw target file accuracy: 10%
- patch fact coverage: 83.33%
- parse errors: 0
- average latency: about 22.17 seconds

This is a successful CPU-only real inference validation. The 0.5B model is strong enough to validate binary documentation-update detection on a small validation subset, but it is not reliable for final fine-grained scenario classification, documentation category selection, target file selection, or documentation patch quality.

Detailed row-by-row inspection is available in `reports/real_llm_per_record_analysis_v0_3_qwen2_5_coder_0_5b.md`.

## Strict vs Normalized Metrics

The first real model outputs are semantically better than strict string metrics suggest. For example, the model produced `Configuration`, which normalizes to the dataset label `configuration`. The evaluator now reports both strict raw accuracy and normalized accuracy so thesis analysis can distinguish formatting/casing misses from actual semantic misses.

Broad labels such as `API Change` and `integration` are not automatically treated as exact scenario matches. They normalize to `unknown_change` unless there is a clear dataset-specific signal such as environment-variable, background-job, or local-development evidence.

The limit-10 run shows why prompt improvement is needed: binary detection is excellent on this sample, while broad labels such as `API Change`, `integration`, `API`, and `Configuration` still hurt fine-grained metrics. The next local prompt experiment should use `--prompt-mode compact_v2`, which provides exact enum values and target-file routing hints.

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
python -m docguard_llm.cli evaluate --split validation --model qwen2_5_coder_0_5b --backend transformers_local --limit 10 --prompt-mode compact_v2 --continue-on-error --retry-on-parse-error
```

Then move 1.5B/3B/7B evaluation to GPU, Colab/Kaggle, or a vLLM/TGI-compatible server.
