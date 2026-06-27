# Real Hugging Face LLM Run Plan

Recommended first real model: `Qwen/Qwen2.5-Coder-3B-Instruct` (`qwen2_5_coder_3b`).

Use the 3B model first because it has lower resource requirements than the 7B models, is more practical for local inference checks, and is enough to validate the real `transformers_local` path before spending time on larger runs.

## Suggested Local Transformers Sequence

Start with a tiny validation subset:

```bash
python -m docguard_llm.cli evaluate --split validation --model qwen2_5_coder_3b --backend transformers_local --limit 10
```

If the outputs parse correctly and the documentation patches look grounded, expand slightly:

```bash
python -m docguard_llm.cli evaluate --split validation --model qwen2_5_coder_3b --backend transformers_local --limit 30
```

Then try the primary 7B model on a small subset:

```bash
python -m docguard_llm.cli evaluate --split validation --model qwen2_5_coder_7b --backend transformers_local --limit 10
```

Do not run the full test split until small subset outputs have been manually inspected.

## Server Alternative

If local GPU memory is limited, run a local vLLM, TGI, or other OpenAI-compatible server and point DocGuard at it:

```powershell
$env:DOCGUARD_LLM_BACKEND="text_generation_inference"
$env:DOCGUARD_TGI_BASE_URL="http://localhost:8000/v1"
python -m docguard_llm.cli evaluate --split validation --model qwen2_5_coder_3b --backend text_generation_inference --limit 10
```

## Hardware Notes

7B models may require a GPU, quantization, or a local serving setup. The 3B model is the first practical local test. Optional quantization packages such as `bitsandbytes` can help on compatible systems, but they are not required for the default repository checks.
