# S1 runtime amendment 05: last-token-only reranker logits

Status: **FROZEN BEFORE GENERATION AND DEVELOPMENT METRICS**.

The trigger was a batch-size-one reranker CUDA OOM on a Tesla T4 after Amendment 03 had correctly bisected candidate batches down to individual query-document pairs. At this boundary the repository corpus and embedding retrieval were complete for 200/200 rows; the global reranker checkpoint contained 18 valid rows, worker 0's durable shard contained 8, and worker 1's durable shard contained 5. Generation contained zero rows. Retrieval metrics, development metrics and prompt selection had not occurred. This amendment is motivated solely by runtime memory, and no reranker score was used to choose it.

## Exact execution optimization

The pinned Transformers 4.51.3 Qwen3 causal-LM forward now receives:

```python
outputs = self.model(
    **batch,
    logits_to_keep=1,
    use_cache=False,
)
```

Scoring remains exactly `outputs.logits[:, -1, [no_id, yes_id]]` followed by `torch.softmax(logits, dim=1)[:, 1]`. The old reference path uses `logits_to_keep=0, use_cache=False`; the canary requires its final-token probabilities to equal the optimized path within `rtol=1e-6, atol=1e-7` on multiple deterministic short pairs. Tokenized tensors must also be identical. `torch.inference_mode()` replaces `torch.no_grad()` only as a non-mutating inference optimization.

The model/revision, tokenizer, dtype, prompt, query/document strings, padding, truncation, 8,192-token maximum, candidate membership, yes/no token IDs, softmax probability, retrieval grid and final reranker top-3 are unchanged. `use_cache=False` is valid because reranking is a single non-generative forward and never consumes `past_key_values`.

## Preserved safeguards

Amendment 03 remains exact: attempt the complete logical candidate batch first; split left/right only on CUDA OOM; recurse to one; preserve order; propagate unrelated runtime failures; fail closed if one pair still OOMs. Amendment 04 remains exact: two spawned workers independently load the frozen reranker on `cuda:0` and `cuda:1`, use separate durable shards and deterministic assignment, and are validated/merged by the parent; the single-worker fallback remains available.

The 18 global, 8 worker-0 and 5 worker-1 valid persisted rows are not deleted or recomputed. Resume validation continues to reject duplicate, missing, unexpected, malformed, non-finite or out-of-range results. New call diagnostics record `logits_to_keep=1`, `use_cache=false`, `LAST_TOKEN_ONLY`, adaptive batch sizes/splits, single-item OOM state, output count, and peak allocated CUDA memory where available. The runtime manifest labels this as an exact execution optimization rather than a scoring-method change.

Confirmation remains inaccessible, Gate 6 row-level human data remains inaccessible, and Amendments 01–04 plus the original freeze remain preserved in Git history.
