# HF Classifier Methodology v0.4

DocGuard v0.4.2 adds Hugging Face classifier experiments to reduce reliance on hardcoded routing while keeping the deterministic router as an interpretable baseline and guardrail.

The default experiment uses `sentence-transformers/all-MiniLM-L6-v2` as a frozen embedding model. This model is small enough for CPU-first experimentation and produces reusable text embeddings without full transformer fine-tuning. Logistic regression classifiers are then trained for `docs_update_required`, `doc_category`, positive-only `target_doc_file`, and `scenario_type`.

CodeBERT is included as an optional embedding backend through `microsoft/codebert-base`. It is relevant because DocGuard inputs combine code diffs and natural-language documentation context, but it is slower on CPU and is not part of the default checks.

Zero-shot classification is also optional. It can compare DocGuard labels against a ready-made natural language inference model, but it is CPU-slow and may not understand project-specific scenario labels.

Sequence classifier fine-tuning is thesis-relevant because it tests whether supervised pretrained models can learn DocGuard labels directly. It is implemented with Hugging Face `Trainer`, but kept optional because CPU fine-tuning can be slow.

The hybrid `--decision-source hf_embedding` mode lets the HF embedding classifier provide the primary prediction. The router remains as a validator and fallback when classifier confidence is low or when a predicted target file violates documentation-file constraints.

v0.4.3 adds no-leak input modes because the original `full_current` representation can be too informative. `change_summary`, `change_intent_summary`, and extracted signal names may encode scenario semantics close to the gold labels. The recommended thesis result is therefore `raw_diff_plus_docs`, which includes changed files, raw code diff, and the existing documentation excerpt only.

Recommended reporting tiers:

- Primary fair HF result: `raw_diff_plus_docs`
- Assisted HF result: `raw_diff_plus_signals`
- Upper-bound assisted result: `full_current`

The `full_current` result should be treated as an upper bound, not as the main no-leak learned classifier result.

v0.4.3 separates scenario evaluation into overall, positive, and negative subsets. This matters because positive scenario and target-file accuracy drive documentation patch generation, while negative subtype labels are diagnostic explanations for no-update cases. Binary no-update detection is the primary practical requirement for negatives.

Negative no-update subtypes are grouped into thesis-friendly reason groups such as `no_behavior_change_refactor`, `no_contract_change_textual`, and `dependency_or_config_no_doc_impact`. These groups are more interpretable than a large flat confusion matrix and better reflect the fact that many negative subtype confusions still produce the correct operational decision: no documentation update.

Large scenario confusion matrices should not be used as the main thesis figure. Positive scenario, negative scenario, and grouped negative reason matrices are reported separately.
