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

`docguard_llm.llm_generator.generate_documentation_patch()` includes an optional `hf` backend for future HuggingFace causal instruction models such as Qwen, Mistral, or Llama variants. Imports for `torch` and `transformers` are lazy and occur only when `backend="hf"` is explicitly requested with a model name.

No model is downloaded, trained, or executed in this step.

## Current Limitation

The `llm-mock` backend returns clearly marked mock patches. It validates architecture and safety, but it is not a real patch-quality result. A real CPU/GPU HuggingFace experiment should be reported separately once a model is explicitly selected and run.
