# VS Code LLM Patch Runtime 2026-08

This note documents the non-synthetic VS Code runtime path for documentation patch generation.

## Implemented Flow

The VS Code extension can now run two patch-generation modes on the current workspace git diff:

- `deterministic`: fast grounded fallback patch composer.
- `llm-hf`: real Hugging Face patch generation using the current code diff, current docs-before text, router output, allowed facts, postprocessing, verifier checks, and patch-quality labels.
- `llm-openai-compatible`: real chat-completions-compatible generation for stronger hosted or local servers such as vLLM, LM Studio, or compatible provider APIs.
- `llm-ollama`: real local Ollama chat generation for quantized local models.

The runtime does not use gold labels, expected facts, docs-after text, generated project-evolution records, or synthetic case metadata in this path.

## Real Local HF Smoke

Workspace input:

- workspace: `examples/vscode_demo`
- changed file: `src/config.ts`
- visible change: added `process.env.REVIEW_WINDOW || '7d'`
- target document selected by DocGuard: `docs/configuration.md`

Model attempted:

- `Qwen/Qwen2.5-Coder-0.5B-Instruct`

Observed result:

- generation status: `ok`
- verifier status: `fail`
- quality label: `rejected`
- hallucination risk: `high`
- reason: the model copied prompt/current-documentation content or claimed no additional content was required instead of producing a grounded patch for `REVIEW_WINDOW`.

The verifier correctly rejected the unsafe output and exposed a safe fallback patch:

```md
## Environment Variables

- `REVIEW_WINDOW` sets the review window and defaults to `7d`.
```

Larger local CPU attempt:

- `Qwen/Qwen2.5-Coder-1.5B-Instruct` was too slow for a practical live VS Code flow on the local CPU-only setup and was stopped.

## Interpretation

The VS Code tool now supports the intended real LLM patch-generation architecture, but the local CPU-only small-model setup is not yet a reliable quality generator. The correct thesis-safe claim is:

- DocGuard can route real workspace changes to the correct documentation file.
- DocGuard can call a real Hugging Face LLM for patch drafting.
- The verifier catches failed or hallucination-prone LLM patch outputs.
- A safe grounded fallback remains available when the LLM patch is rejected.

Do not claim that the current local 0.5B/1.5B CPU LLM setup is production-ready or consistently writes human-quality documentation.

## Next Practical Requirement

To make the LLM patch layer consistently useful, run the same VS Code/runtime path with a stronger generation backend:

- GPU/Colab/Kaggle with a stronger Qwen Coder/Instruct model, or
- a quantized local GGUF/llama.cpp backend, or
- a remote text-generation endpoint.

The code now supports the latter two options through `llm-openai-compatible` and `llm-ollama`. These are the recommended paths for moving from architecture validation to higher-quality LLM patch generation without adding hardcoded documentation text.
