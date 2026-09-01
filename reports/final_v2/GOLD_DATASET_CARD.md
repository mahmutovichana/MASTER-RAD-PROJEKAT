# Final V2 Gold Dataset Card

Status: candidate only, not frozen. Gate 1 did not pass.

## Dataset identity

- Candidate canonical path: `experiments/consolidated_enriched_training_v2/gold/final_human_gold.jsonl`
- Candidate SHA-256: `baeaa4e6142b7c8b80f6417aaf09ad71bdc155e6ea4aff7f15d6494d503358c5`
- Candidate row count: `25,134`
- Split-generation script: `scripts/prepare_consolidated_training_v2.py`
- Consolidated review artifact: `data/final_v2/human_review/consolidated_enriched_training_v2/consolidated_human_review.jsonl`
- Consolidated review SHA-256: `6aa3da7a5821e6613bbe4426e56caccc461a6cd0936a87f9328eb47821bc83e4`
- Consolidated review manifest: `data/final_v2/human_review/consolidated_enriched_training_v2/manifest.json`
- Consolidated review manifest SHA-256: `e1fbaea0b6a507cfbc5d62793f464dec945cb9a43e31f2de84b714e0cccd2c10`
- Gold manifest: `experiments/consolidated_enriched_training_v2/gold/human_gold_manifest.json`
- Gold manifest SHA-256 after deterministic Gate 1 rebuild: `c698cadcc3a1b02b0a6b0820d227d22a8e39bfcefccaef8479da63b36cd08ed5`
- Partition manifest: `data/final_v2/partitions/canonical_repository_partitions/repository_partition_manifest.json`
- Partition manifest SHA-256: `ff434af660f52f229ab5d1fbf978fc1268913c2e16ea9711fa863eb44a8f7c89`
- Natural Diversity completion audit: `data/final_v2/natural_diversity_expansion_v1/human_review/finalized/review_completion_audit.json`
- Natural Diversity completion audit SHA-256: `99c4409b6fa6ed893585d09f3da77548c23c8f704043caca351c15ff61fe7d63`

No `GOLD_FREEZE_MANIFEST.json` was created because Gate 1 found unresolved blockers.

## Composition

| Metric | Count |
| --- | ---: |
| Total examples | 25,134 |
| Positive examples | 5,939 |
| Negative examples | 19,195 |
| Positive prevalence | 23.6293% |
| Unique repositories | 264 |

## Category distribution

| Category | Count |
| --- | ---: |
| `no_update` | 19,195 |
| `api_reference` | 1,552 |
| `configuration` | 1,465 |
| `model_contract` | 1,122 |
| `developer_setup` | 989 |
| `other_documentation` | 811 |

## Language distribution

| Language | Count |
| --- | ---: |
| TypeScript | 14,015 |
| Python | 7,942 |
| C# | 1,920 |
| Go | 648 |
| Unknown | 244 |
| Java | 185 |
| Rust | 107 |
| SQL | 54 |
| JavaScript | 15 |
| Kotlin | 4 |

## Split distribution

| Split | Rows | Positive | Negative | Positive rate | Repositories |
| --- | ---: | ---: | ---: | ---: | ---: |
| `development_train` | 18,519 | 5,195 | 13,324 | 28.0523% | 178 |
| `development_validation` | 3,028 | 343 | 2,685 | 11.3276% | 38 |
| `confirmation` | 3,587 | 401 | 3,186 | 11.1793% | 48 |

The outer development/confirmation boundary is repository-disjoint. Future Gate 2 work may create temporary development-only folds inside the frozen development universe, but must not change the frozen case membership or confirmation repository membership.

## Source / provenance composition

| Source dataset | Rows | Positive | Negative | Positive rate |
| --- | ---: | ---: | ---: | ---: |
| `consolidated_enriched_training_v1` | 21,080 | 1,885 | 19,195 | 8.9412% |
| `controlled_real_project_positive_v1` | 2,000 | 2,000 | 0 | 100.0000% |
| `controlled_real_project_positive_v2_imbalanced` | 2,000 | 2,000 | 0 | 100.0000% |
| `remaining_4800_partial_positive_54` | 54 | 54 | 0 | 100.0000% |

The enrichment/controlled sources have materially higher positive prevalence than the natural/historical source. This construction choice must be discussed as a thesis limitation and as training-set enrichment, not as natural corpus prevalence.

## Source × category distribution

| Source dataset | `api_reference` | `configuration` | `developer_setup` | `model_contract` | `other_documentation` | `no_update` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `consolidated_enriched_training_v1` | 539 | 532 | 128 | 415 | 271 | 19,195 |
| `controlled_real_project_positive_v1` | 400 | 400 | 400 | 400 | 400 | 0 |
| `controlled_real_project_positive_v2_imbalanced` | 580 | 520 | 460 | 300 | 140 | 0 |
| `remaining_4800_partial_positive_54` | 33 | 13 | 1 | 7 | 0 | 0 |

## Natural Diversity Expansion trace

Natural Diversity Expansion V1 is complete as its own finalized review family, but it is not represented in the current candidate Final V2 gold.

| Item | Count / status |
| --- | ---: |
| Planned stratified seeds | 780 |
| Accepted candidate cases | 779 |
| Sent to human review | 779 |
| Completed reviewed rows | 779 |
| Approved / excluded | 779 / 0 |
| Positive / negative | 9 / 770 |
| In current candidate gold by `case_id` | 0 |
| In current candidate gold by repo+PR | 0 |
| Repo+PR overlap with current candidate gold | 0 |
| Outside current candidate gold | 779 |

The Natural Diversity manifest marks `refresh_validation_excluded_from_training=true`. However, Gate 1 still treats the 779 completed-but-not-included rows as an unresolved scope decision for freeze: they are either deliberately outside the final thesis gold, or the gold must be rebuilt to include the intended subset. This cannot be inferred silently.

## Label integrity

- Required final label fields are present in the candidate gold.
- `review_status=approved` for all 25,134 candidate rows.
- `human_review_complete=true` for all 25,134 candidate rows.
- Binary/category consistency errors: 0.
- Duplicate `case_id`: 0.
- Duplicate repository+PR identity: 0.
- Conflicting labels for identical model-safe input: 1 group.
- Rows with empty `docs_before_excerpt`: 25.

## Reviewer integrity

- Explicit reviewer-like metadata is present for 4,000 controlled rows as `reviewer = "Codex controlled contract review"`.
- The remaining 21,134 rows do not carry explicit reviewer IDs in the candidate gold.
- Explicit multi-review cases detected: 0.
- Explicit disagreement/conflict fields detected: 0.
- Explicit adjudicated cases detected: 0.
- Explicit unresolved conflicts detected: 0.
- Cohen's kappa is not computed because the repository does not contain sufficient dual-review assignments for a valid agreement estimate.

## Known limitations

- Natural Diversity Expansion V1 has 779 completed reviewed rows outside the current candidate gold.
- Candidate gold includes enrichment/controlled positive sources with 100% positive prevalence, unlike the natural/historical source.
- 25 rows have empty `docs_before_excerpt`, including 13 positive rows.
- One pair of rows has identical model-safe text but conflicting labels.
- Reviewer metadata is incomplete for formal inter-annotator agreement statistics.
- Language and category distributions are intentionally imbalanced.
