# Gate 1 Human-Gold Dataset Freeze

Status: **PASS**

## Freeze identity

- Canonical gold path: `experiments/consolidated_enriched_training_v2/gold/final_human_gold.jsonl`
- Canonical gold SHA-256: `68ebe23ab4dd8a02ee1ea459e3b6a374a3efa2891afc8d344a533676eb3b5a08`
- Row count: **25,913**
- Positive / negative: **5,948 / 19,965**
- Positive rate: **22.95%**

## Resolved Gate 1 blockers

- Natural Diversity scope: **resolved**, 779/779 completed approved rows included.
- Source identity duplicates: **0 case-id groups**, **0 repo/PR groups**.
- Model-visible collisions: **7 groups**, **1 conflicting-label group**, **0 crossing confirmation**.
- Empty docs-before rows: **25**, dispositions `{'E1_no_stored_docs_before_context': 23, 'E2_empty_excerpt_with_retrieval_metadata': 2, 'E3_requires_human_adjudication': 0, 'E4_ineligible_integrity_failure': 0}`, re-review required **0**.
- Legacy partition audit: superseded/repaired for frozen V2 split identity; canonical verifier is `scripts/verify_final_v2_gold_freeze.py`.

## Splits

- `development_train`: **19,018 rows**, **5,199 positive**, **13,819 negative**, **191 repositories**
- `development_validation`: **3,148 rows**, **348 positive**, **2,800 negative**, **41 repositories**
- `confirmation`: **3,747 rows**, **401 positive**, **3,346 negative**, **52 repositories**

## Provenance

- `controlled_real_project_augmentation`: **4,000**
- `natural_diversity_expansion_v1_reviewed`: **779**
- `natural_historical_and_targeted_reviewed`: **21,080**
- `natural_targeted_reviewed`: **54**

## Confirmation boundary

- Confirmation split is sealed.
- Gate 1 did not train models.
- Gate 1 did not inspect confirmation predictions, metrics, or results.

## Machine-checkable artifacts

- Freeze manifest: `reports/final_v2/GOLD_FREEZE_MANIFEST.json`
- Completion audit: `reports/final_v2/gate1_human_review_completion_audit/human_review_completion_audit.json`
- Empty-doc audit: `reports/final_v2/gate1_empty_docs_disposition_audit.json`
- Collision audit: `reports/final_v2/gate1_model_visible_collision_audit.json`
- Split manifest: `experiments/consolidated_enriched_training_v2/gold/human_gold_manifest.json`
