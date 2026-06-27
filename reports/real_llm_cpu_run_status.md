# CPU-Only Real LLM Run Status

## Environment

- torch: `2.9.1+cpu`
- CUDA available: `False`
- machine type: CPU-only development setup

## Observed Runs

- `qwen2_5_coder_0_5b` sanity-only generated valid JSON: `{"ok": true}`.
- The first parser version marked that output as failed when the model wrapped JSON inside a markdown code block.
- The sanity-only parser now extracts JSON objects from fenced or surrounding text before checking for `{"ok": true}`.
- `qwen2_5_coder_1_5b` compact prompt downloaded and loaded, reached `generation started`, then returned to PowerShell without a visible completion, latency, raw output, or completed report.

## Conclusion

- `qwen2_5_coder_0_5b` is usable for local real pipeline validation on this CPU-only machine.
- `qwen2_5_coder_1_5b` may be too slow or unstable for DocGuard compact prompts on this CPU-only machine.
- `qwen2_5_coder_3b` and `qwen2_5_coder_7b` should be run on GPU, Colab/Kaggle, or a vLLM/TGI-compatible local server.

## Current Safeguards

- Smoke-test writes reports incrementally before and during generation.
- Real evaluation writes each JSONL prediction immediately after it is generated.
- `--continue-on-error` can save fallback rows and keep processing later records.
- CPU-only generation may still hang or terminate inside lower-level model code; `--timeout-seconds` is documented but no hard Windows timeout is enforced.
