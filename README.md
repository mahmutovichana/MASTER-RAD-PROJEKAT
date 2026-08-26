# DocGuard

DocGuard is an MSc thesis project for detecting when real software changes require documentation updates and for generating guarded documentation patch suggestions.

## Final V2 Status

The canonical thesis architecture is Final V2. It is designed around a real GitHub pull-request corpus, fully human-reviewed gold labels, repository-disjoint development and sealed confirmation partitions, and a semantic LLM documentation-generation stage.

Final V2 has not yet produced final confirmation performance numbers. Do not report Binary V4, Category V8, or Stage 3 V2 final performance until the sealed confirmation flow has been run exactly once after freeze.

## Architecture

```text
GitHub PR candidate
  -> fully human-reviewed Final V2 gold labels
  -> Binary V4 documentation-update classifier
  -> Category V8 primary documentation-category classifier
  -> semantic documentation retrieval at base SHA
  -> LLM change analysis
  -> LLM documentation writer
  -> safety/provenance guard
  -> one LLM repair attempt
  -> accepted patch or human_review_required
```

## Final V2 Principles

- Real GitHub PR corpus, not synthetic-only evidence.
- Fully human-reviewed final labels.
- Repository-disjoint `development_train`, `development_validation`, and sealed `confirmation`.
- Natural class imbalance preserved.
- No class balancing, oversampling, undersampling, or SMOTE in final classifiers.
- Binary V4 uses only `language`, `code_changed_files`, `code_diff_excerpt`, and `docs_before_excerpt`.
- Category V8 uses exact primary labels only: `api_reference`, `configuration`, `developer_setup`, and `model_contract`.
- `other_documentation` is binary positive but excluded from primary four-class Category V8 training.
- Stage 3 V2 has no hardcoded category-to-file router.
- Stage 3 V2 has no deterministic grounded fallback as the final generator.
- Stage 3 quality evaluation is blind-human-first, with reference metrics as supporting diagnostics only.

## Historical Experiments

Earlier work remains useful as development history and regression context:

- synthetic prototype dataset and rule-based baseline
- earlier V1/V2/V3 binary classifiers
- V4-V7 category classifier iterations
- grounded generator prototype
- Qwen100 patch-generation experiments
- hybrid cascade prototype

Historical Qwen100 values are internal V1 verifier acceptance rates:

- grounded acceptable: 76%
- Qwen acceptable: 67%
- hybrid cascade acceptable: 87%

These are not Final V2 accuracy, not human quality, and not final thesis performance.

## Important Protocols

- [Final methodology](docs/final_methodology_v2.md)
- [Final classifier protocol](docs/final_classifier_protocol_v2.md)
- [Final human review protocol](docs/final_human_review_protocol_v2.md)
- [Final Stage 3 evaluation protocol](docs/final_stage3_evaluation_protocol_v2.md)
- [Stage 3 semantic generation protocol](docs/stage3_v2_evaluation_protocol.md)

## Current Safety Boundary

Do not run final candidate construction, model training, model freeze, real LLM generation, or sealed confirmation evaluation until the running acquisition and human-review workflow are complete and the pre-experiment audit passes.
