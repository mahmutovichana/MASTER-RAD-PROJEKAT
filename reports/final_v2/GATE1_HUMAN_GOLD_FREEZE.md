# Gate 1 — Human-Gold Dataset Freeze

## 1. Gate result

Gate 1 status: `FAIL`.

The candidate Final V2 gold dataset is not frozen. I did not create `reports/final_v2/GOLD_FREEZE_MANIFEST.json`.

## 2. Canonical human gold candidate

- Path: `experiments/consolidated_enriched_training_v2/gold/final_human_gold.jsonl`
- SHA-256: `baeaa4e6142b7c8b80f6417aaf09ad71bdc155e6ea4aff7f15d6494d503358c5`
- Rows: 25,134
- Positive: 5,939
- Negative: 19,195
- Positive prevalence: 23.6293%
- Repositories: 264

The deterministic split-preparation script was hardened to reproduce the current Final V2 schema and then rerun. After that rebuild, the split files and `human_gold_manifest.json` hashes matched the actual local bytes.

## 3. Natural Diversity completeness

Natural Diversity Expansion V1 is complete as a standalone review package:

| Item | Count / status |
| --- | ---: |
| Planned stratified seeds | 780 |
| Accepted candidate cases | 779 |
| Sent to human review | 779 |
| Completed reviewed rows | 779 |
| Approved / excluded | 779 / 0 |
| Positive / negative | 9 / 770 |
| Completion audit | `passed` |

However, those 779 completed Natural Diversity rows are not in the current candidate Final V2 gold:

| Inclusion check | Count |
| --- | ---: |
| Included by `case_id` | 0 |
| Included by repository+PR | 0 |
| Missing from current candidate gold by `case_id` | 779 |
| Repository+PR overlap with current candidate gold | 0 |

This is a Gate 1 blocker unless the thesis protocol explicitly declares Natural Diversity Expansion V1 outside the final human-gold dataset. I did not infer that decision silently.

## 4. Dataset composition

| Source dataset | Rows | Positive | Negative | Positive rate |
| --- | ---: | ---: | ---: | ---: |
| `consolidated_enriched_training_v1` | 21,080 | 1,885 | 19,195 | 8.9412% |
| `controlled_real_project_positive_v1` | 2,000 | 2,000 | 0 | 100.0000% |
| `controlled_real_project_positive_v2_imbalanced` | 2,000 | 2,000 | 0 | 100.0000% |
| `remaining_4800_partial_positive_54` | 54 | 54 | 0 | 100.0000% |

The enrichment sources materially change class prevalence. That may be a valid training design, but it must be reported transparently.

## 5. Label integrity

- Required final label fields present: yes.
- `review_status=approved`: 25,134 / 25,134.
- `human_review_complete=true`: 25,134 / 25,134.
- Invalid taxonomy values: 0.
- Binary/category consistency errors: 0.
- Malformed booleans: 0.
- Positive rows with `no_update`: 0.
- Negative rows with positive category: 0.
- Human/gold label mismatches: 0.

Blocking label/evidence issues:

- 25 rows have empty `docs_before_excerpt`.
- 1 identical model-safe input group has conflicting labels:
  - `DGPR-8855c17914e4f995`, `microsoft/promptflow` PR 4005: `false / no_update`
  - `DGPR-ab3191293c61f4fa`, `microsoft/promptflow` PR 4006: `true / developer_setup`

## 6. Reviewer integrity

- Explicit reviewer-like metadata exists for 4,000 controlled rows.
- Explicit reviewer-like metadata is absent for 21,134 rows.
- Multi-review cases detected from stored metadata: 0.
- Reviewer disagreements detected from stored metadata: 0.
- Adjudicated cases detected from stored metadata: 0.
- Unresolved conflict metadata detected: 0.
- Formal Cohen's kappa is not computed because the stored assignments do not provide sufficient dual-review coverage.

No required adjudication protocol with unresolved stored conflicts was found, but the conflicting identical model-safe input group requires human adjudication before freeze.

## 7. Duplicate / identity audit

| Check | Result |
| --- | --- |
| Duplicate `case_id` | 0 groups |
| Duplicate repository+PR identity | 0 groups |
| Duplicate model-safe input | 7 groups, 7 extra rows |
| Conflicting labels among duplicate model-safe inputs | 1 group |
| Duplicate source identity across splits | 0 |
| Duplicate case identity across splits | 0 |

The source identity audit is clean. The model-safe duplicate conflict is not safe to resolve automatically.

## 8. Frozen partition candidate

| Split | Rows | Positive | Negative | Positive rate | Repositories |
| --- | ---: | ---: | ---: | ---: | ---: |
| `development_train` | 18,519 | 5,195 | 13,324 | 28.0523% | 178 |
| `development_validation` | 3,028 | 343 | 2,685 | 11.3276% | 38 |
| `confirmation` | 3,587 | 401 | 3,186 | 11.1793% | 48 |

Overlap checks:

- development_train ↔ development_validation: repositories 0, case IDs 0, repo+PR 0.
- development_train ↔ confirmation: repositories 0, case IDs 0, repo+PR 0.
- development_validation ↔ confirmation: repositories 0, case IDs 0, repo+PR 0.

The outer split boundary is repository-disjoint, but it is not frozen because Gate 1 failed.

## 9. Leakage protection

- Confirmation sealed in canonical repository partition manifest: yes.
- Confirmation results accessed by this task: no.
- Confirmation predictions/metrics inspected: no.
- Training/model selection/Stage 3 run by this task: no.
- Safe model fields remain: `language`, `code_changed_files`, `code_diff_excerpt`, `docs_before_excerpt`.

## 10. Immutable artifacts

No new immutable Gate 1 freeze artifacts were created. The following candidate artifacts were audited but are not frozen by this gate:

- `experiments/consolidated_enriched_training_v2/gold/final_human_gold.jsonl`
- `experiments/consolidated_enriched_training_v2/gold/train.jsonl`
- `experiments/consolidated_enriched_training_v2/gold/validation.jsonl`
- `experiments/consolidated_enriched_training_v2/gold/confirmation.jsonl`
- `experiments/consolidated_enriched_training_v2/gold/human_gold_manifest.json`

## 11. Known limitations / blockers

Gate 1 cannot pass until these are resolved:

1. Decide and document whether the 779 completed Natural Diversity Expansion V1 reviewed rows are intentionally outside the final human-gold dataset, or rebuild the final gold to include the intended subset.
2. Adjudicate the conflicting identical model-safe input pair in `microsoft/promptflow`.
3. Decide whether 25 rows with empty `docs_before_excerpt` remain valid final-gold examples or must be excluded/adjudicated under the existing evidence rules.
4. Replace or supersede the legacy `audit_final_dataset_v2.py` partition recomputation check for consolidated v2, because it recomputes partitions and reports 1,893 mismatches against the frozen v2 split strategy.

## 12. Verification results

- Human review completion audit: `passed`.
- Pre-experiment audit: `PASS`.
- Legacy final dataset audit: `fail`, 1,918 errors:
  - 25 empty `docs_before_excerpt`.
  - 1,893 partition recomputation mismatches from the legacy audit strategy.
- Gate 1 freeze verifier: `FAIL`, because no successful `GOLD_FREEZE_MANIFEST.json` exists and unresolved blockers remain.

## 13. Next allowed action

Do not proceed to Gate 2 yet.

Next action is still Gate 1 remediation/adjudication:

- explicitly exclude or integrate Natural Diversity Expansion V1;
- adjudicate the promptflow duplicate-safe-input conflict;
- resolve the 25 empty-docs-before rows;
- rerun Gate 1 and create `GOLD_FREEZE_MANIFEST.json` only if all freeze conditions pass.
