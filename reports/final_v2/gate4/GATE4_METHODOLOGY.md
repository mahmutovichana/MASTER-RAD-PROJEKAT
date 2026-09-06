# Gate 4 development-only Stage 3 study

Status: **PASS / FROZEN**.

The frozen Gate 3 Binary classifier scores every `development_validation` row at threshold 0.15. Only predicted-positive rows receive the frozen Gate 3 Category prediction. The primary sample is a seed-42 random sample of up to 100 predicted positives, drawn before retrieval-context availability is inspected and without category, language, repository, gold-label, or human-label balancing.

The supplementary stress sample contains 25 frozen predicted positives per primary predicted category and may use both development partitions. It cannot replace or be pooled with the primary natural-distribution result.

The shared context adapter reads numbered `doc_context_01..12` pairs plus supported direct/nested legacy candidate lists, emits only `{path, excerpt, source_ref}`, removes incomplete candidates and deterministic duplicates, and never invents a target from pathless `docs_before_excerpt`.

Rows without canonical retrieval candidates are system coverage failures, not Qwen or verifier failures. They receive `retrieval_context_unavailable`, zero LLM calls, and no patch. Gold/reference fields are unavailable to sampling and generation and may only enter a later, separate post-generation development evaluation.

Gate 2 nested cross-validation remains the development performance estimate for the classifiers. Gate 4 does not access confirmation. No generation results or Stage 3 freeze are claimed before the external Qwen execution is returned and verified.

Preparation verification passed after the development-only structured-output and memory-safety hardening: 39 focused tests passed, and the complete safe non-confirmation suite passed with 441 tests and 30 warnings. Writer and repair prompts explicitly require a complete JSON object with typed fields, including numeric writer_confidence in [0,1]. Malformed JSON or invalid structured-output types fail closed as human_review_required. The real Qwen backend now enforces a deterministic maximum input size of 4096 tokens before moving the prompt to CUDA. Oversized prompts are not silently truncated; they fail closed as human_review_required with input_token_budget_exceeded. The offending oversized prompt is rejected before CUDA and does not increment the LLM-call counter; if the budget is exceeded during writer or repair, any earlier successful calls for that case remain recorded. Any residual CUDA out-of-memory condition is converted to human_review_required with cuda_out_of_memory so that one case cannot abort the batch. These execution conditions are reported separately from safety/provenance violations. Samples and frozen classifiers were unchanged, and confirmation was not accessed.


Final development execution completed and passed post-run integrity verification. The canonical final analysis and freeze evidence are under `reports/final_v2/gate4/final_results/` and `GATE4_STAGE3_FREEZE_MANIFEST.json`. Confirmation remained sealed throughout Gate 4.
