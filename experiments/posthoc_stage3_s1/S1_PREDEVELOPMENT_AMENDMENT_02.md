# S1 pre-development technical amendment 02

Status: **FROZEN BEFORE AGGREGATE S1 NEURAL DEVELOPMENT RESULTS**.

After Amendment 01, the mandatory Kaggle canary passed sufficiently to authorize development execution. The development run reconstructed and checkpointed the repository corpus for all 200 cases, then failed during Qwen3 embedding inference before neural retrieval metrics or configuration selection. A logical batch of eight at the frozen 8,192-token maximum attempted a 9.16 GiB CUDA allocation on a Tesla T4 and raised `torch.cuda.OutOfMemoryError`.

## Amendment

The configured logical embedding batch size remains eight. Each logical batch is attempted unchanged. Only `torch.cuda.OutOfMemoryError` triggers cleanup of temporary tensors, `gc.collect()`, `torch.cuda.empty_cache()`, and deterministic left/right bisection. Recursion permits 8→4→2→1, always concatenating left before right so every input row and its output order are preserved. An OOM at size one fails closed. Unrelated runtime exceptions propagate unchanged.

The model, revision, tokenizer, input text, truncation behavior, maximum length 8,192, dtype, last-token pooling and L2 normalization are unchanged. There is no CPU fallback. Retrieval scores and all downstream scientific semantics are unchanged.

Every encode call records configured maximum batch size, attempted and effective batch sizes, split count, minimum effective batch size and whether a single-item OOM occurred. Score checkpoints persist these diagnostics. Valid completed score files are reused; absent, corrupt, identity-mismatched, dimensionally incomplete or non-finite files are recomputed atomically. `.tmp` files are never treated as complete. Repository corpus checkpoints and ordered case membership are preserved, while duplicate reranker/generation records remain rejected.

## Frozen boundary

- Trigger: development embedding CUDA OOM before neural metrics completed.
- Repository corpus completed: true (200/200).
- Aggregate neural development results seen: false.
- Development configuration selection occurred: false.
- Confirmation accessed: false.
- Gate 6 row-level human data accessed: false.
- Model IDs and revisions: unchanged.
- Embedding maximum length: 8,192, unchanged.
- Configured logical maximum batch size: 8, unchanged.
- Adaptive execution microbatch range: 1–8.
- Retrieval/scoring semantics: unchanged.
- P1/P2 and thresholds: unchanged.
- Semantic repair maximum: 1.
- Schema-correction retry maximum: 1.

The original freeze and Amendment 01 remain preserved in Git history. This amendment supersedes them only for subsequent S1 execution.
