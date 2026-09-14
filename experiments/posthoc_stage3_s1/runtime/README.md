# S1 runtime

Local CUDA was unavailable during preparation. Repository and Hugging Face caches are runtime-only and ignored. The Kaggle notebook clones the already-pushed frozen scientific commit, verifies its exact SHA, pulls the four required LFS inputs, obtains `HF_TOKEN` from Kaggle Secrets without printing it, and uses a separately attached runtime asset bundle.

The mandatory canary validates CUDA discovery, exact resolved model revisions, sequential embedding/reranker/generator loading and cleanup, 4-bit generator placement, deterministic plan JSON, critic JSON, one repair, VRAM, host RAM and elapsed times. Any failure writes `CANARY_STOP` and prevents the development runner from starting.

The development runner persists repository corpora, embeddings, lexical/dense scores, reranker scores, model-call responses and unique generation results. It checkpoints each completed result and emits a progress receipt every 25 new cases. Prompt selection remains pending a blind development review when objective evidence cannot resolve P1/P2.

Amendment 02 retains logical embedding batches of eight and the 8,192-token limit while bisecting only CUDA-OOM batches deterministically down to one. Valid completed score files are reused; incomplete, corrupt, identity-mismatched or non-finite files are atomically replaced. A single-item OOM and all non-OOM runtime failures remain fail-closed.

Amendment 03 first attempts each reranker call's complete candidate batch, then deterministically bisects only on `torch.cuda.OutOfMemoryError` until the unchanged 8,192-token scoring operation fits or a single pair fails closed. Left-before-right concatenation preserves candidate order. Each completed row is durably and atomically checkpointed; valid rows are reused, duplicate or unexpected identities fail, and malformed, incomplete, membership/order-mismatched or non-finite rows are recomputed without touching completed embedding checkpoints.

Expected 2xT4 wall time is approximately 4–8 hours for 200 development cases, subject to the measured canary. Stop instead of substituting a model if the pinned 14B model is unreliable.
