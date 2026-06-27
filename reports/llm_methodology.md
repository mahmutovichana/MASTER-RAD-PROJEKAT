# Hugging Face LLM Methodology

DocGuard uses Hugging Face code-oriented instruction models to test whether zero-shot or few-shot LLM assistance can improve documentation consistency analysis beyond the conservative rule-based baseline.

## Models

- `Qwen/Qwen2.5-Coder-7B-Instruct` is the primary model because it is strong at code reasoning, structured JSON generation, and documentation patch generation.
- `deepseek-ai/deepseek-coder-6.7b-instruct` is included as a comparable open-weight code model.
- `Qwen/Qwen2.5-Coder-3B-Instruct` is included as a smaller option with lower local resource requirements.

## Prompt Structure

Prompts include the code diff, changed files, documentation excerpt before the change, candidate documentation files, documentation categories, allowed scenario types, strict output schema, and few-shot examples selected only from `train.jsonl`.

## Output Contract

The model must return strict JSON with documentation-update label, scenario type, documentation category, target documentation file, minimal patch, grounded facts covered, and confidence.

## Grounding Rules

Generated patches should only mention facts grounded in `code_diff` and `docs_before_excerpt`. Unsupported changes may be classified as `unknown_change` to avoid hallucinated patches.

## Runtime Considerations

The default checks use the deterministic `mock` backend. Real local inference with 7B models may require a GPU, quantization, or a local vLLM/TGI server. The 3B Qwen model is the lightweight comparison option.

## Limitations

This phase performs inference only. It does not fine-tune models, and mock results validate pipeline behavior rather than model quality.
