# Hybrid Methodology

DocGuard v0.4 prioritizes CPU-friendly signal extraction, deterministic routing, and classical ML classifiers. The LLM is optional and used only after candidate reduction.

The v0.4.1 refinement makes the deterministic layer more explicit. Signal extraction separates endpoint, validation, authentication, response-field, setup, workflow, model-contract, changelog, and no-update refactor cues. The router maps those granular signals to documentation categories and scenario types instead of relying on broad source-file defaults.

The ML layer trains with scikit-learn when it is installed. If scikit-learn is unavailable, the same command falls back to a lightweight signal model and reports `ml_backend = fallback` in the evaluation output.

v0.4.2 adds a Hugging Face classifier track. In `--decision-source hf_embedding` mode, the embedding classifier becomes the primary decision source and the deterministic router becomes a guardrail. This reduces dependence on hardcoded decision logic while preserving interpretable validation rules for invalid target files, no-update records, and low-confidence predictions.

Hybrid evaluation should be reported separately for validation and test splits. The validation split is used for iteration and diagnostics; the test split is reserved for final held-out reporting.

The optional LLM-assisted stage is not part of the default CPU safety check. It remains a small-sample verifier path for compact prompts or future GPU/GGUF runs. The `qwen2_5_coder_0_5b` run remains a real LLM inference proof, not the main classifier path.
