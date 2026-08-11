# LLM Patch Generation Architecture 2026-08

## Why This Layer Was Added

DocGuard already has a working flow for detection, routing, target document selection, and minimal deterministic patch suggestions. The project-evolution demo showed that the remaining weak point is patch quality: legacy patches are safe but generic, for example `+new_endpoint.` or `+added_environment_variable.`.

The new LLM patch-generation layer prepares a model-agnostic architecture for richer documentation patches without changing the validated detection/routing evidence.

## Thesis Alignment

The thesis title focuses on an intelligent NLP agent for software-project consistency analysis. A patch-generation layer makes the agent feel closer to the practical developer workflow:

code diff -> update decision -> documentation category -> target file -> grounded patch draft -> verifier feedback.

## Separation From Detection And Routing

Detection and routing remain owned by `docguard_hybrid`. The LLM patch layer receives only the already routed runtime context and drafts documentation text. This separation keeps binary/category/target metrics comparable with previous reports and avoids mixing patch quality with update detection.

## Fallback Strategy

The old deterministic patch generator remains the default `legacy` backend. The new project-evolution runner supports:

- `--patch-backend legacy`
- `--patch-backend llm-mock`
- `--patch-backend llm-hf --patch-model <model-name>`

The mock backend exercises prompt construction, postprocessing, and verification without loading any model.

## Safe Inputs

The LLM patch prompt uses only:

- project id
- code diff
- current documentation/docs-before excerpt
- predicted target documentation file
- predicted documentation category
- predicted scenario hint
- detected router signals
- router reason
- optional target section when available from runtime context

## Forbidden Inputs

The prompt builder does not accept:

- gold labels
- expected facts
- expected patch summary
- docs-after text
- manual label notes

## HuggingFace Plan

`docguard_llm.llm_generator.generate_documentation_patch()` includes an optional `hf` backend for HuggingFace causal instruction models such as Qwen, Mistral, or Llama variants. Imports for `torch` and `transformers` are lazy and occur only when `backend="hf"` is explicitly requested with a model name.

Recommended grounded smoke command:

```bash
python scripts/smoke_hf_patch_generation.py --model Qwen/Qwen2.5-1.5B-Instruct --case-limit 5 --max-new-tokens 192 --temperature 0.1
```

Recommended first model: `Qwen/Qwen2.5-1.5B-Instruct`.

Optional stronger model: `Qwen/Qwen2.5-3B-Instruct`.

Use 7B models only for cheap GPU/Colab if needed.

No model is downloaded, trained, or executed unless the HF command is explicitly run. This is a zero-shot/few-shot inference phase, not fine-tuning.

After the first Qwen 1.5B smoke test, the patch pipeline was hardened with an allowed-fact extractor and stricter verifier. This prevents a patch from getting a clean pass simply because it includes one grounded token while also inventing unsupported fields or examples.

## Patch Quality Evaluation

`docguard_llm.patch_quality.evaluate_patch_quality(...)` adds a model-agnostic heuristic scoring layer for generated patches. It uses verifier status, verifier warnings, allowed facts, grounded token coverage, patch length, genericness, and readability cues to produce:

- groundedness score
- minimality score
- readability score
- usefulness score
- hallucination risk
- quality label
- quality reasons

These metrics are safety-oriented and comparative. They are not human gold labels and should not be presented as final patch-quality truth. They help show that legacy patches are often safe but generic, while LLM patches can be richer but must remain grounded and reviewed.

## Current Limitation

The `llm-mock` backend returns clearly marked mock patches. It validates architecture and safety, but it is not a real patch-quality result. A real CPU/GPU HuggingFace experiment should be reported separately once a model is explicitly selected and run.

If dependencies are missing, the HF path records a clear error asking for `transformers`, `torch`, and optionally `accelerate` for `--device-map auto`. Legacy and mock runs do not require those packages.
