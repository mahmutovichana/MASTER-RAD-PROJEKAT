# DocGuard LLM Patch Quality Methodology 2026-08

## Role Of The LLM

The LLM remains the documentation patch generator. It receives a routed documentation task, the code diff, current documentation context, and an allowed-facts block extracted from visible evidence. Its role is to draft a concise Markdown patch in documentation style.

## Role Of The Guardrails

The fact extractor, postprocessor, verifier, and patch-quality evaluator are guardrails around generation. They are not presented as the final intelligent generator. Their job is to make LLM output inspectable and safer:

- the fact extractor states what facts are visibly supported by the diff and docs-before context
- the prompt uses those facts to constrain generation
- the postprocessor removes noisy model formatting
- the verifier checks for unsupported claims and grounding failures
- the quality evaluator summarizes groundedness, minimality, readability, usefulness, and hallucination risk

## Why This Is Better Than Raw LLM Generation

Raw LLM generation can produce fluent documentation that looks plausible while adding unsupported details. The first Qwen 1.5B smoke test showed this risk: a patch could mention grounded tokens such as `/reviews` and `201`, but still invent fields or status examples. The guardrail layer makes these errors visible instead of treating fluency as correctness.

## Why This Is Better Than A Pure Rule-Based Generator

The legacy rule-based patch generator is safe but often too generic. It can produce patches such as `+new_endpoint.` or `+added_environment_variable.`, which are easy to verify but not useful developer-facing documentation. The LLM layer can produce richer prose, while the deterministic checks keep that prose tied to observed evidence.

## Human Review Requirement

The patch-quality scores are heuristic and safety-oriented. They are useful for comparing patch backends and identifying risky outputs, but they are not human gold labels. A developer or technical writer should still review generated patches before applying them.

## Evidence Boundary

The project-evolution data is synthetic demo evidence. It supports implementation sanity, explainability, and workflow demonstration. It is not an external benchmark and should not be reported as production performance or final real-world patch quality.
