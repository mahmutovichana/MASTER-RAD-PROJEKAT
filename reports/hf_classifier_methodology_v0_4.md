# HF Classifier Methodology v0.4

DocGuard v0.4.2 adds Hugging Face classifier experiments to reduce reliance on hardcoded routing while keeping the deterministic router as an interpretable baseline and guardrail.

The default experiment uses `sentence-transformers/all-MiniLM-L6-v2` as a frozen embedding model. This model is small enough for CPU-first experimentation and produces reusable text embeddings without full transformer fine-tuning. Logistic regression classifiers are then trained for `docs_update_required`, `doc_category`, positive-only `target_doc_file`, and `scenario_type`.

CodeBERT is included as an optional embedding backend through `microsoft/codebert-base`. It is relevant because DocGuard inputs combine code diffs and natural-language documentation context, but it is slower on CPU and is not part of the default checks.

Zero-shot classification is also optional. It can compare DocGuard labels against a ready-made natural language inference model, but it is CPU-slow and may not understand project-specific scenario labels.

Sequence classifier fine-tuning is thesis-relevant because it tests whether supervised pretrained models can learn DocGuard labels directly. It is implemented with Hugging Face `Trainer`, but kept optional because CPU fine-tuning can be slow.

The hybrid `--decision-source hf_embedding` mode lets the HF embedding classifier provide the primary prediction. The router remains as a validator and fallback when classifier confidence is low or when a predicted target file violates documentation-file constraints.
