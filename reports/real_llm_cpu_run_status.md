# CPU-Only Real LLM Run Status

## Environment

- torch: `2.9.1+cpu`
- CUDA available: `False`
- machine type: CPU-only development setup

## Observed Runs

- `qwen2_5_coder_0_5b` sanity-only generated valid JSON: `{"ok": true}`.
- The first parser version marked that output as failed when the model wrapped JSON inside a markdown code block.
- The sanity-only parser now extracts JSON objects from fenced or surrounding text before checking for `{"ok": true}`.
- `qwen2_5_coder_0_5b` compact DocGuard smoke test succeeded for `support-ticket-api-001` with usable structured output and about 23.6 seconds latency.
- A tiny 3-record real evaluation with `DOCGUARD_MAX_NEW_TOKENS=120` produced F1 80%, one truncated JSON parse error, and about 20.76 seconds average latency.
- A 10-record real evaluation with `DOCGUARD_MAX_NEW_TOKENS=180` produced 100% precision, 100% recall, 100% F1, zero parse errors, and about 22.17 seconds average latency. Fine-grained scenario, category, and target-file accuracy remained weak.
- `qwen2_5_coder_1_5b` compact prompt downloaded and loaded, reached `generation started`, then returned to PowerShell without a visible completion, latency, raw output, or completed report.

## Conclusion

- `qwen2_5_coder_0_5b` is usable for local real pipeline validation on this CPU-only machine.
- `120` new tokens may truncate compact DocGuard JSON; use `180` or `220` for tiny evaluations and keep `60` only for sanity-only.
- `qwen2_5_coder_1_5b` may be too slow or unstable for DocGuard compact prompts on this CPU-only machine.
- `qwen2_5_coder_3b` and `qwen2_5_coder_7b` should be run on GPU, Colab/Kaggle, or a vLLM/TGI-compatible local server.

## Current Safeguards

- Smoke-test writes reports incrementally before and during generation.
- Real evaluation writes each JSONL prediction immediately after it is generated.
- `--continue-on-error` can save fallback rows and keep processing later records.
- `--retry-on-parse-error` retries likely truncated JSON once with 100 additional generated tokens.
- CPU-only generation may still hang or terminate inside lower-level model code; `--timeout-seconds` is documented but no hard Windows timeout is enforced.

## Recommended Next Commands

```powershell
$env:DOCGUARD_MAX_NEW_TOKENS="180"
python -m docguard_llm.cli evaluate --split validation --model qwen2_5_coder_0_5b --backend transformers_local --limit 10 --prompt-mode compact_v2 --continue-on-error --retry-on-parse-error
```
