# S1 pre-development technical amendment 03

Status: **FROZEN BEFORE FIRST COMPLETED RERANKER DEVELOPMENT ROW**.

The resumed frozen S1 run correctly reused the completed repository corpus (200/200) and completed embedding/retrieval-score checkpoints (200/200), with no embedding recomputation. It then entered the pinned Qwen3 reranker and raised `torch.cuda.OutOfMemoryError` before completing any reranker row. The unchanged implementation had attempted to tokenize and score the complete candidate-document batch together at the 8,192-token maximum. No retrieval metrics, aggregate reranker results, generation rows or development configuration selection had been produced.

## Amendment

Every `QwenReranker.score(query, documents)` call first attempts the complete logical document batch exactly as before. Only `torch.cuda.OutOfMemoryError` triggers release of temporary tensors, `gc.collect()`, `torch.cuda.empty_cache()`, and deterministic left/right bisection. Both halves recurse until they fit; odd sizes use floor division for the left half and retain the remainder on the right. Scores are concatenated left before right, preserving one score per original document in original order. A single query-document OOM fails closed, and unrelated runtime exceptions propagate unchanged.

The reranker model and frozen revision, tokenizer, prompt template, query, document strings, candidate union, `padding=True`, `truncation=True`, maximum length 8,192, dtype, yes/no token logits, softmax probability and final top-3 policy are unchanged. There is no CPU fallback, prompt shortening, candidate dropping or alternate model.

Each score call records candidate and output counts, attempted and effective batch sizes, OOM split count, minimum effective batch size, and single-item OOM state. Each completed row records the ordered candidate indices, their finite bounded scores and diagnostics. The reranker checkpoint is rewritten through a flushed/fsynced temporary file and atomically replaced after each completed row. Valid existing rows are reused; duplicate or unexpected case IDs fail closed; malformed, incomplete, identity/membership/order-mismatched, non-finite or out-of-range rows are ignored and recomputed. Temporary partial content is not a valid checkpoint. Completed repository and embedding checkpoints are preserved unchanged.

## Frozen boundary

- Trigger: reranker CUDA OOM before the first completed reranker development row.
- Repository corpus completed: 200/200.
- Embedding candidate retrieval completed: 200/200.
- Reranker completed rows before amendment: 0/200.
- Generation completed rows: 0.
- Retrieval metrics seen: false.
- Aggregate reranker results seen: false.
- Development configuration selection occurred: false.
- Confirmation accessed: false.
- Gate 6 row-level human data accessed: false.
- Reranker model/revision and 8,192-token maximum: unchanged.
- Query/document content, candidate membership and scoring semantics: unchanged.
- Final reranker top-k: 3, unchanged.
- P1/P2 and thresholds: unchanged.
- Schema-correction retry maximum: 1.
- Semantic documentation repair maximum: 1.
- CPU fallback: false.
- Single-item OOM disposition: `FAIL_CLOSED`.

The original freeze and Amendments 01 and 02 remain preserved in Git history. Allocator hardening remains enabled before CUDA initialization but is not treated as the solution to the observed oversized allocation.
