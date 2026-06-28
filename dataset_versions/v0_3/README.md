# DocGuard Dataset v0.3 Snapshot

This frozen snapshot preserves the active v0.3 dataset, reports, and real CPU-only LLM validation artifacts before the repository moved to v0.4.

v0.3 broadened DocGuard beyond API reference updates into architecture, middleware, DTO/model contracts, developer setup, testing, configuration, workflow, background job, and changelog-style documentation maintenance.

v0.3 also included the first real CPU-only Hugging Face validation using `qwen2_5_coder_0_5b` with the `transformers_local` backend. That run showed the local real inference path works on CPU and can detect binary documentation-update needs on a small validation subset.

## Limitations That Motivate v0.4

- Fine-grained LLM classification was weak for `scenario_type`, `doc_category`, and `target_doc_file`.
- The small LLM sometimes selected source files as target documentation files.
- Negative examples should not be evaluated on documentation category or target file in the same way as positive examples.
- The dataset remains synthetic and uses relatively simple generated diffs.

v0.4 is therefore CPU-first: signal routing, classical ML, and a hybrid deterministic system are the main path, with small LLMs used only as optional verifiers or patch helpers.
