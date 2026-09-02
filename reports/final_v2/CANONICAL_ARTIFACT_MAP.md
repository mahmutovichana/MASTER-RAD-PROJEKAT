# Final V2 Canonical Artifact Map

This map removes ambiguity between the current Final V2 thesis pipeline and older development artifacts. Later gates may use only the artifacts marked as canonical unless a new gate explicitly supersedes them with a new manifest.

## CANONICAL FINAL V2

These artifacts define the current Final V2 experiment state.

| Component | Canonical path | Role |
| --- | --- | --- |
| Consolidated reviewed dataset | `data/final_v2/human_review/consolidated_enriched_training_v2/consolidated_human_review.jsonl` | Full reviewed corpus used to create the current Final V2 gold dataset. |
| Consolidated review manifest | `data/final_v2/human_review/consolidated_enriched_training_v2/manifest.json` | Dataset integrity, row counts, source counts, duplicate checks and hashes. |
| Positive training pool | `data/final_v2/human_review/consolidated_enriched_training_v2/positive_training_pool.jsonl` | Auditable pool of approved positive rows included in the consolidated corpus. |
| Final V2 gold dataset | `experiments/consolidated_enriched_training_v2/gold/final_human_gold.jsonl` | Canonical machine-learning gold dataset for Final V2. |
| Development train split | `experiments/consolidated_enriched_training_v2/gold/train.jsonl` | Development-only training split. |
| Development validation split | `experiments/consolidated_enriched_training_v2/gold/validation.jsonl` | Development-only model-selection split. |
| Sealed confirmation split | `experiments/consolidated_enriched_training_v2/gold/confirmation.jsonl` | Held-out confirmation split. Must not be used for model selection or tuning. |
| Final V2 gold manifest | `experiments/consolidated_enriched_training_v2/gold/human_gold_manifest.json` | Canonical split sizes, hashes, repository overlap check and sealed-confirmation preservation. |
| Canonical repository partition manifest | `data/final_v2/partitions/canonical_repository_partitions/repository_partition_manifest.json` | Repository-level partition assignments and `confirmation_sealed=true`. |
| Binary classifier config | `configs/binary_classifier_v4.json` | Final V2 binary classifier configuration. |
| Category classifier config | `configs/category_classifier_v8.json` | Final V2 category classifier configuration. |
| Stage 3 semantic generation config | `configs/stage3_semantic_generation_v2.json` | Final V2 Stage 3 retrieval/generation configuration. |
| Gate 1 gold freeze manifest | `reports/final_v2/GOLD_FREEZE_MANIFEST.json` | Immutable machine-checkable identity for the frozen Final V2 human-gold dataset. |
| Gate 1 empty-doc disposition audit | `reports/final_v2/gate1_empty_docs_disposition_audit.json` | Resolution record for rows with empty stored `docs_before_excerpt`. |
| Gate 1 model-visible collision audit | `reports/final_v2/gate1_model_visible_collision_audit.json` | Resolution record for identical safe-input groups and confirmation-boundary safety. |
| Binary development model artifact | `experiments/consolidated_enriched_training_v2/binary_v4/binary_v4.joblib` | Development-selected binary model. Not a confirmation result. |
| Binary development summary | `experiments/consolidated_enriched_training_v2/binary_v4/training_summary.json` | Development-only training/model-selection summary. |
| Category development model artifact | `experiments/consolidated_enriched_training_v2/category_v8/category_v8.joblib` | Development-selected category model. Not a confirmation result. |
| Category development summary | `experiments/consolidated_enriched_training_v2/category_v8/training_summary.json` | Development-only training/model-selection summary. |
| Development figures | `experiments/consolidated_enriched_training_v2/figures/` | Development-only figures generated before final confirmation. |
| Pre-experiment audit | `reports/final_v2/pre_experiment_audit.json` | Existing machine-checkable Final V2 safety audit. |

## HISTORICAL / DEPRECATED

These may remain as development evidence, but must not feed the Final V2 experiment unless a later gate explicitly reclassifies them through a new manifest.

| Path family | Reason |
| --- | --- |
| `experiments/consolidated_enriched_training_v1/` | Prior consolidated experiment family. Historical only. |
| `data/final_v2/human_review/consolidated_enriched_training_v1/` | Prior reviewed consolidation source. It is only upstream historical evidence for the current v2 consolidation. |
| `data/final_v2/human_review/historical_4k_merged/` | Migrated historical data source, not a standalone final dataset. |
| `data/final_v2/human_review/historical_4k_migrated/` | Migrated historical data source, not a standalone final dataset. |
| `data/final_v2/controlled_synthetic_positive_v1/` | Earlier controlled synthetic pilot. Not canonical Final V2 gold. |
| `data/final_v2/controlled_real_project_positive_v1/` | Controlled positive augmentation source already represented through the v2 consolidated manifest. |
| `data/final_v2/controlled_real_project_positive_v2_imbalanced/` | Controlled positive augmentation source already represented through the v2 consolidated manifest. |
| `data/final_v2/expansion/targeted_positive_enrichment_v1/` | Earlier targeted enrichment pilot/source. Not a standalone final dataset. |
| `data/final_v2/expansion/targeted_positive_enrichment_v1_remaining_4800/` | Partial external candidate source. Only the independently accepted 54 positive rows are represented through the v2 consolidated manifest. |
| `data/final_v2/natural_diversity_expansion_v1/` | Natural Diversity source family. Its 779 completed approved reviewed rows are represented in the frozen Final V2 gold through the v2 consolidated manifest; the source folder remains historical/provenance evidence, not a standalone final dataset. |
| `models/real_gold_classifier_*` | Older classifier artifacts. Historical only. |
| `models/real_doc_category_classifier_*` | Older category classifier artifacts. Historical only. |
| `models/external_deep_jit*` | Older external/deep JIT experiments. Historical only. |
| `models/hf_v0_4/` and `models/v0_4/` | Older model families. Historical only. |
| Any `cascade_confirmation*` outputs under old experiment folders | Historical confirmation/evaluation artifacts for old dataset identities. They do not define the current Final V2 confirmation result. |

## GENERATED / REPRODUCIBLE

These outputs are reproducible from canonical inputs and scripts. They may be regenerated only within the appropriate gate.

| Component | Path |
| --- | --- |
| Development predictions | `experiments/consolidated_enriched_training_v2/binary_v4/development_predictions.jsonl` |
| Development predictions | `experiments/consolidated_enriched_training_v2/category_v8/development_predictions.jsonl` |
| Development model comparisons | `experiments/consolidated_enriched_training_v2/binary_v4/model_comparison.json` |
| Development model comparisons | `experiments/consolidated_enriched_training_v2/category_v8/model_comparison.json` |
| Development comparison report | `experiments/consolidated_enriched_training_v2/comparison_metrics.json` |
| Development result summary | `experiments/consolidated_enriched_training_v2/RESULTS_SUMMARY.md` |
| Figure manifest | `experiments/consolidated_enriched_training_v2/figures/figures_manifest.json` |

## IMMUTABLE AFTER FREEZE

These artifacts must not change after their corresponding gate passes.

| Gate | Immutable artifacts after PASS |
| --- | --- |
| Gate 1 — Human-gold dataset freeze | `experiments/consolidated_enriched_training_v2/gold/*`, `data/final_v2/human_review/consolidated_enriched_training_v2/manifest.json`, and the canonical partition manifest. |
| Gate 3 — Final classifier selection and freeze | Frozen binary/category model files, freeze manifests, configs and development-selection summaries. |
| Gate 4 — Stage 3 retrieval/generation study and freeze | Frozen Stage 3 config, prompt/template source hashes and freeze manifest. |
| Gate 5 — One-shot confirmation | Confirmation metrics, predictions, generation outputs and one-shot receipts. |
| Gate 7 — Thesis evidence freeze | Final tables, figures, reports, manifests and thesis-facing reproducibility evidence. |
