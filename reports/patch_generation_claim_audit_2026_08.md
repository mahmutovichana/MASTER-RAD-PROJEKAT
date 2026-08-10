# Patch Generation Claim Audit 2026-08

## Summary

Patch generation is currently validated only inside the controlled DocGuard synthetic/prototype setting. External datasets validate detection, positive sensitivity, and code-comment consistency classification; they do not validate real-world Markdown documentation patch generation.

## Evidence Review

| Evidence | What it validates | Patch-generation status |
| --- | --- | --- |
| Synthetic v0.4 hybrid/HF reports | Controlled detection/routing/category/target/patch behavior | Patch fact coverage is synthetic/prototype evidence only. |
| LLM v0.3/v0.4 reports | Prototype patch generation behavior and CPU feasibility | Not final external patch quality evidence. |
| CoDocBench | Real positive code-doc/comment co-change sensitivity | Does not validate generated Markdown patches. It may provide before/after docstrings, but evaluation here is recall-focused. |
| Deep-JIT zero-shot | External binary code-comment consistency proxy | Does not validate patch generation. |
| Deep-JIT task-specific classifier | External binary code-comment consistency adaptation | Does not generate or validate patches. |
| VS Code demo | Developer workflow demonstration | Demo/prototype only, not scientific proof of reliable patches. |

## Safe Claim

Use:

> Patch generation is demonstrated in the controlled DocGuard prototype, while external validation focuses primarily on detection and consistency classification.

## Claims To Avoid

- Do not claim external datasets prove reliable real-world Markdown patch generation.
- Do not claim CoDocBench or Deep-JIT validates `generated_doc_patch`.
- Do not claim production-ready patch application.
- Do not make patch generation the central quantitative external result.

## Future Work

Future work should evaluate patch generation with human review or an external benchmark that contains before/after documentation suitable for patch-level comparison. Metrics should include groundedness, minimality, factual coverage, and developer acceptability.
