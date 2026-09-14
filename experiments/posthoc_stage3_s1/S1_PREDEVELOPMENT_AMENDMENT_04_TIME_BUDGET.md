# S1 pre-development amendment 04: time-budget execution

Status: **FROZEN BEFORE GENERATION-RESULT INSPECTION**.

This amendment is motivated only by the bounded compute/time budget. At the freeze boundary, the repository corpus and embedding candidate-retrieval checkpoints were complete for 200/200 rows, reranking was running, no generation results had been viewed or used, and no prompt selection had occurred. Confirmation and Gate 6 row-level human data remained inaccessible. This remains a post-hoc Stage 3 challenger, not a new unbiased confirmation.

## Two-GPU reranker execution

When at least two CUDA devices are visible, the parent uses two spawned process workers—never Python threads. Worker 0 is pinned to `cuda:0`; worker 1 is pinned to `cuda:1`; each independently loads the exact frozen Qwen reranker. Missing cases are assigned by their original frozen row index modulo two. Each worker uses Amendment 03 adaptive CUDA-OOM microbatching and writes only its own flushed, fsynced, atomically replaced shard. The parent validates membership, identities, score counts, ordered candidate indices, finiteness and `[0,1]` bounds, rejects duplicates/missing/unexpected rows, and merges in original frozen case order. Existing valid global and shard checkpoints are reused. With fewer than two visible CUDA devices, the existing single-worker path is retained.

Worker count, device assignments, assigned/reused/new case counts and runtime per worker are recorded without affecting ranking.

## Bounded prompt selection

Phase A starts with exactly 50 cases: 25 from the first frozen 100 primary rows and 25 from the second frozen 100 secondary rows. Within each half, case IDs are ordered by ascending `SHA256("42:" + case_id)` and the first 25 are selected. This selection depends only on frozen membership and case identity, never model output. P1 and P2 run only for this paired subset, for at most 100 initial prompt-case runs. The persistent exact-prompt model-call cache continues to reuse identical target-decision and documentation-plan calls.

Only pairs where both patches exist and differ enter direct preference review. If fewer than 20 such pairs exist, the population extends deterministically to 75 cases using the next 13 primary and 12 secondary cases. If it remains below 20, it extends to the maximum 100 using the next 12 primary and 13 secondary cases. Thus each extension adds exactly 25, balance differs by at most one, all within-half order remains hash-determined, and the paired population never exceeds 100 cases or 200 paired prompt-case runs.

After Phase A, the leakage-safe blind sheet exposes candidates A/B without P1/P2 identity and execution stops as `PROMPT_SELECTION_BLIND_REVIEW_REQUIRED`. Prompt selection uses completed human review only: more direct `reviewer_preference` votes wins; an exact tie is resolved by total human-positive target-fit, grounding, usefulness and style-fit judgments; a remaining exact tie selects P1 deterministically. Self-critic metrics cannot select the prompt.

In Phase B, only the selected prompt is run for development cases missing that selected-variant result. The losing prompt is not required outside the paired subset. The selected prompt ultimately has results for all 200 development cases. Threshold results at 0.35, 0.50 and 0.65 are derived from those same outputs without rerunning generation. The paired results remain available solely for prompt-selection analysis.

The prior design required up to 400 prompt-case runs (two variants × 200 cases). The amended design requires 250 runs without extension and at most 300 runs at the 100-case paired ceiling: `2N + (200 - N) = 200 + N`.

## Unchanged scientific boundary

Models/revisions, retrieval methodology, reranker scoring and Amendment 03, generator prompts P1/P2, thresholds, one schema retry, one semantic repair, frozen membership, confirmation isolation, and Gate 6 human-data isolation are unchanged. The original freeze and Amendments 01–03 remain preserved in Git history.
