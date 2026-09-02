# Finalization Gate 2 — development-only ML model study protocol

Status: **PREREGISTERED; no model-family results observed at creation**.

## Immutable research boundary

- Gate 1 freeze commit: `c931d0bffcdc4389abea8f5fb67b6e8c476fe8b8`.
- Frozen gold SHA-256: `68ebe23ab4dd8a02ee1ea459e3b6a374a3efa2891afc8d344a533676eb3b5a08`.
- Development universe: the union of frozen `development_train` and `development_validation`, exactly 22,166 rows.
- Sealed confirmation: exactly 3,747 rows; it is forbidden to load into any Gate 2 feature, fitting, threshold, diagnostic, or performance path.
- Safe model fields only: `language`, `code_changed_files`, `code_diff_excerpt`, `docs_before_excerpt`.
- Dataset membership, labels, taxonomy, safe fields, and the development/confirmation repository boundary are immutable.

The fail-closed loader verifies the gold hash before reading rows, validates every row, discards the confirmation partition before returning, and asserts the expected development and excluded-confirmation counts. The derived development identity is recorded in `development_view_manifest.json`; it is a view, not a competing gold dataset.

## Tasks and metrics

Binary uses all 22,166 development rows and the frozen Boolean target. Its primary metric is MCC. Secondary metrics are precision, positive recall, positive F1, macro-F1, balanced accuracy, specificity, accuracy, average precision, ROC-AUC when valid, Brier score, and confusion matrix.

Category uses exactly the existing Category V8 positive-primary eligibility contract: `api_reference`, `configuration`, `developer_setup`, and `model_contract`. `other_documentation` remains outside the primary Category V8 task. Its primary metric is Macro-F1. Secondary metrics are per-class precision/recall/F1, weighted F1, balanced accuracy, accuracy, and confusion matrix.

## Preregistered families

- **M0 Dummy:** deterministic `most_frequent`; lower-bound reporting only and not normally selectable.
- **M1 Lexical:** the existing selected Binary V4 / Category V8 representation: canonical safe serializer, Char-TF-IDF `char_wb`, n-grams 3–5, `min_df=1`, `max_features=80,000`, `sublinear_tf=true`, followed by logistic regression. This preserves the actually selected historical baseline for both tasks.
- **M2 Semantic relation:** frozen `microsoft/unixcoder-base` at model/tokenizer revision `5604afdc964f6c53782a6813140ade5216b99006`. Code/change and docs-before views are encoded separately. The single pooling choice is attention-masked mean pooling of final hidden states. The relation vector is `[code, docs, abs(code-docs), code*docs, cosine]`, followed by logistic regression.
- **M3 Hybrid:** the exact M1 sparse block concatenated with the exact M2 relation block. The only semantic scaling values are `0.25`, `1.0`, and `4.0`.

No other encoder, family, feature, pooling policy, or post-result model addition is allowed. CodeReviewer is future work only. UniXcoder is frozen; no fine-tuning, PEFT, or LoRA occurs.

## Semantic serialization and truncation

Code/change view uses only language, normalized changed-file paths, and code diff. Documentation view is exactly docs-before, including deterministic encoding of an empty string for legitimate empty-doc rows. Each view is tokenized separately to maximum length 512. After reserving tokenizer special tokens, overlength sequences retain a deterministic head/tail split (earlier token receives the odd remainder). Pooling is float32 attention-masked mean pooling. Truncation counts, proportions, token quantiles, and language breakdown are recorded. No alternate truncation or pooling policy will be compared.

## Nested repository-disjoint validation

Outer CV is `StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)`, grouped by canonical lower-case repository. Binary and Category have task-specific frozen assignments. Category was checked in the preregistered order 5→4→3 and five valid folds were feasible. Each repository occurs in exactly one outer validation fold.

Within each outer-training fold, inner CV is three-fold `StratifiedGroupKFold`, grouped by repository, shuffled deterministically with seed `42 + outer_fold`. Inner CV selects only:

- `C ∈ {0.25, 1.0, 4.0}`;
- `class_weight ∈ {None, "balanced"}`;
- for M3 only, `semantic_scale ∈ {0.25, 1.0, 4.0}`.

For Binary, each configuration receives inner out-of-fold probabilities. Threshold is selected only from those probabilities on the fixed 0.05–0.95 grid in 0.05 steps. Ranking is MCC, balanced accuracy, F1, then threshold closest to 0.5, then lower threshold. The outer validation fold never selects its threshold. Category configuration selection uses mean inner Macro-F1 with deterministic config ordering as final tie-break.

## Winner rule and uncertainty

For each task, learned families are ranked by mean outer primary metric. If the best means differ by at most 0.005, lower outer-fold standard deviation wins; if still tied, simplicity order is M1→M2→M3. M0 is baseline only. This rule cannot be changed after results.

Development OOF predictions are resampled in 2,000 deterministic repository-clustered bootstrap replicates. Paired M2−M1, M3−M1, and winner−M1 deltas are reported with 95% intervals. Invalid replicates are skipped and counted. Bootstrap evidence does not alter the winner rule.

## Diagnostics and reproducibility

OOF diagnostics cover fold stability, supported major languages (TypeScript, Python, C#, Go), provenance families including Natural Diversity, and documented model-visible collisions. Provenance is never a feature. Small-support results receive explicit warnings. Identical safe-input conflicts remain retained as an irreducible ambiguity limitation; no collision group may cross development/confirmation.

Every execution appends STARTED/COMPLETED/FAILED records to `GATE2_RUN_REGISTRY.jsonl`, including task, family, fold, config, seed, source commit, gold SHA, encoder revision when relevant, and artifact identity. Failed runs are never erased.

The canonical configuration is `configs/final_v2/gate2_model_study.json`. Colab is compute only: canonical loading, embedding extraction, validation, and study logic live in repository scripts. Model weights and disposable embedding caches are not committed. Confirmation remains sealed throughout Gate 2.

Post-result changes are forbidden except documented, protocol-preserving fixes for genuine implementation bugs.
