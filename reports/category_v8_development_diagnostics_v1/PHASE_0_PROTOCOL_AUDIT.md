# Category V8 development diagnostics v1 — Phase 0 protocol audit

## Status

**STOP before Phases 1–5.** Two material protocol concerns require an explicit
methodological decision. No dataset row, label, split, model, or historical
experiment artifact was changed during this audit. The sealed confirmation
content was not opened or supplied to any new analysis.

## A. Exact current state (observed facts)

- Repository commit audited: `e8db67fcedcb2c309c2e4ace06d44c1fd8f5bab0` on `main`.
- Consolidated v2 rows: 25,134; positives: 5,939; negatives: 19,195.
- Development train: 18,519 rows; development validation: 3,028 rows.
- The manifest records 3,587 sealed-confirmation rows. Only manifest metadata
  was inspected; the confirmation JSONL was not opened.
- New development-train-only rows: 4,054, comprising 4,000 controlled rows and
  54 additionally reviewed natural positives.
- Direct train/validation repository overlap check: 0.
- `augmentation_train_only=true` rows in train: 4,054; in validation: 0.
- V1 and v2 development-validation case membership is exactly equal: 3,028
  case IDs in each.
- V2 manifest records repository overlap across all partitions as 0 and both
  validation and confirmation membership as preserved.
- Category V8 natural validation contains 322 primary-category positives:
  api_reference 85, configuration 154, developer_setup 19, model_contract 64.
- Category V8 selected model: `char_tfidf_logreg_c4.0_mindf1`.
- Category V8 train accuracy/macro-F1: 0.9813/0.9811.
- Category V8 natural-validation accuracy/macro-F1: 0.4876/0.3817.
- Category V8 developer_setup validation F1: 0.0000.
- Binary V4 v2 natural-validation F1/MCC/ROC-AUC: 0.7749/0.7490/0.9113.
- Binary V4 v1 natural-validation F1/MCC/ROC-AUC: 0.7888/0.7659/0.9192.
- The v2 Binary candidate is therefore not a justified automatic replacement
  for the better v1 development-validation candidate.

Safe model inputs are exactly:

1. `language`
2. `code_changed_files`
3. `code_diff_excerpt`
4. `docs_before_excerpt`

`docs_after_excerpt`, documentation diffs, gold fields, label notes, PR title,
and target-document fields are excluded by the model serializer.

## B. Canonical artifacts and scripts

### Consolidated data and split metadata

- `data/final_v2/human_review/consolidated_enriched_training_v2/consolidated_human_review.jsonl`
- `data/final_v2/human_review/consolidated_enriched_training_v2/manifest.json`
- `data/final_v2/human_review/consolidated_enriched_training_v2/source_provenance.jsonl`
- `experiments/consolidated_enriched_training_v2/gold/train.jsonl`
- `experiments/consolidated_enriched_training_v2/gold/validation.jsonl`
- `experiments/consolidated_enriched_training_v2/gold/human_gold_manifest.json`
- `experiments/consolidated_enriched_training_v1/partitions/repository_partition_manifest.json`
- `experiments/consolidated_enriched_training_v1/partitions/partition_audit.json`

### Models and development outputs

- `experiments/consolidated_enriched_training_v2/category_v8/category_v8.joblib`
- `experiments/consolidated_enriched_training_v2/category_v8/training_summary.json`
- `experiments/consolidated_enriched_training_v2/category_v8/development_predictions.jsonl`
- `experiments/consolidated_enriched_training_v2/binary_v4/binary_v4.joblib`
- `experiments/consolidated_enriched_training_v2/binary_v4/training_summary.json`
- `experiments/consolidated_enriched_training_v2/comparison_metrics.json`
- `experiments/consolidated_enriched_training_v2/RESULTS_SUMMARY.md`

### Controlled and natural additions

- `data/final_v2/controlled_real_project_positive_v1/human_review/reviewed_2000.jsonl`
- `data/final_v2/controlled_real_project_positive_v2_imbalanced/human_review/reviewed_2000.jsonl`
- `data/final_v2/expansion/targeted_positive_enrichment_v1_remaining_4800/raw_candidates_transfer_2323/reviewed_from_scratch_v1/positive_reviewed.jsonl`

### Protocol and training implementation

- `docguard_ml_v2/data_contract.py`
- `docguard_ml_v2/features.py`
- `configs/category_classifier_v8.json`
- `configs/binary_classifier_v4.json`
- `scripts/consolidate_enriched_training_corpus_v2.py`
- `scripts/prepare_consolidated_training_v2.py`
- `scripts/train_category_classifier_v8.py`
- `scripts/train_binary_classifier_v4.py`
- `scripts/build_controlled_real_project_positive_v1.py`
- `tests/test_consolidated_enriched_training_v2.py`
- `tests/test_final_classifier_v2_infrastructure.py`

## C. Confirmation isolation status

- This audit did not open `confirmation.jsonl`, derive predictions from it,
  hash it, or pass it to a model or diagnostic script.
- All proposed diagnostic scripts must reject a confirmation path or a row with
  `partition=confirmation`.
- V2 trainer configuration records `confirmation_access=forbidden` and the v2
  model outputs contain train and development-validation predictions only.
- However, the repository already contains historical v1 directories
  `cascade_confirmation/` and `cascade_confirmation_all_languages/`, and the v1
  results summary explicitly states that the cascade was evaluated on the
  sealed confirmation set. Therefore the thesis must not claim that this set
  was globally untouched. The defensible statement is: **untouched by the new
  development-diagnostics phase**. Historical confirmation results must not be
  used for new model selection.

## D. Controlled-augmentation structure

The 4,000 controlled rows contain:

- 4 underlying projects represented by 8 versioned pseudo-repository IDs;
- 20 mutation templates;
- 2 languages: TypeScript (2,080) and C# (1,920);
- exactly one changed-file extension: `.json` (4,000/4,000);
- exactly one documentation extension: `.md` (4,000/4,000);
- only 10 unique target documentation paths;
- 980 api_reference, 920 configuration, 860 developer_setup,
  700 model_contract, and 540 other_documentation rows.

This is already strong structural evidence that the augmentation domain is far
narrower and cleaner than natural PRs. It is a diagnostic observation, not yet
a causal conclusion about model failure.

## E. Material stop conditions

### E1. Controlled labels are generated and stamped as human gold

`scripts/build_controlled_real_project_positive_v1.py` first creates pending
candidate rows, then in the same generation loop copies every row and assigns:

- `human_docs_update_required = True`
- `human_doc_category = synthetic_category_by_design`
- `review_status = approved`
- `reviewer = "Codex controlled contract review"`

The same builder produced both controlled 2,000-row datasets. All 4,000 rows
have the same review method and reviewer. The later split preparation sets
`label_source=human_reviewed_final_v2` and `human_review_complete=true` on every
row, including controlled rows.

This does not prove the controlled labels are semantically incorrect. It does
mean that their current provenance overstates independent human review. Owner
acceptance of the generated collection is not equivalent to a blind per-row
human review, and the two must not be represented identically in an academic
gold-label field.

### E2. Historical confirmation access exists

Historical v1 confirmation evaluation artifacts exist. They must remain
preserved, but future development selection cannot use them. A final report
must distinguish historical access from the untouched status of this new
phase.

## F. Concrete first implementation batch recommended

Do not begin error analysis or ablations until the provenance decision is made.
The first reviewable implementation batch should:

1. introduce separate, explicit provenance values for natural human gold,
   controlled design labels, and owner acceptance;
2. prevent preparation code from overwriting controlled provenance with
   `human_reviewed_final_v2`;
3. preserve all existing labels and split membership while regenerating only
   development metadata/materializations;
4. add tests that fail when controlled/generated labels are represented as
   independent human gold;
5. add a diagnostic guard that rejects confirmation paths and
   `partition=confirmation` rows;
6. document whether the 4,000 controlled labels will be retained as clearly
   marked train-only weak/controlled supervision or sent through independent
   human review.

After this explicit decision and remediation, Phases 1–5 can proceed on the
unchanged natural development validation set.

## Audited hashes (safe development artifacts)

- v2 train: `51eb370f5636e36034d2e9742c618e831993e0fb28a54ba3a21a11d49548fbe7`
- v2 validation: `6af538c357602367fa6f8ddb796cd7f414591e5f2feff671409917ffdce6a9fc`
- Category V8 model: `8afd9af8ee5f585548464f6fc98e1dd4ce08e0fe7229a19403cdc8cf2798a6e7`
- Category V8 summary: `64dbdcf5b8b7833022c42712246dc89961c9eda26ce449ed57551b256963fda5`

## Phase 0 conclusion

The numerical state and the train/validation leakage invariants match the
request. The requested diagnostic question is scientifically justified, and
the controlled data already shows a strong template/domain fingerprint.
Nevertheless, the provenance inconsistency and historical confirmation access
trigger the supplied stop policy. No modeling or Phase 1–5 output should be
created until the provenance treatment is explicitly approved.
