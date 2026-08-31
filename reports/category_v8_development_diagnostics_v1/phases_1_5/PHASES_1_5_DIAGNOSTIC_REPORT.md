# Category V8 development diagnostics v1 — Phases 1–5

## Scope and confirmation status

This report uses only development train and natural development validation. The diagnostic runner has no confirmation input and rejects confirmation paths/rows. The historical v1 confirmation access is documented in the Phase 0 audit; this phase does not use its examples or metrics.

## Observed facts

- Category validation cases: **322**.
- Category validation macro-F1: **0.3817**; balanced accuracy: **0.4181**.
- developer_setup cases: **19**; configuration→API errors: **79**; model_contract→API errors: **23**.
- Category-eligible controlled development positives: **3460** of 4,000 controlled rows; natural development positives: **1031**.
- Provenance discriminator accuracy: **1.0000**, ROC-AUC: **1.0000** on a repository-grouped development holdout.

## Interpretation

The diagnostic views separate evidence from interpretation. A strong provenance-discriminator score indicates that controlled and natural examples are distinguishable from the same safe representation; it is not itself a DocGuard model-selection result. Structural summaries and nearest neighbors should be read together with the per-case evidence, especially for the 19 developer_setup examples.
The current evidence supports a combination of DATA DOMAIN SHIFT and EVIDENCE/INPUT + REPRESENTATION limitations: controlled rows are shorter, cleaner, concentrated in eight pseudo-repositories and ten documentation paths, while natural cases are longer and more heterogeneous. The ablation results do not support docs_before alone as a sufficient signal. TAXONOMY/ANNOTATION AMBIGUITY remains a review question, not a conclusion, and no labels were changed.

## Input ablations

- `A_code_diff_only` (code_diff_excerpt): validation Macro-F1 **0.3664**, balanced accuracy **0.3857**, model `char_tfidf`.
- `B_docs_before_only` (docs_before_excerpt): validation Macro-F1 **0.2570**, balanced accuracy **0.3278**, model `char_tfidf`.
- `C_changed_files_plus_code_diff` (code_changed_files, code_diff_excerpt): validation Macro-F1 **0.3877**, balanced accuracy **0.4065**, model `char_tfidf`.
- `D_code_diff_plus_docs_before` (code_diff_excerpt, docs_before_excerpt): validation Macro-F1 **0.3610**, balanced accuracy **0.3966**, model `char_tfidf`.
- `E_current_all_safe_fields` (language, code_changed_files, code_diff_excerpt, docs_before_excerpt): validation Macro-F1 **0.3817**, balanced accuracy **0.4181**, model `char_tfidf`.

## Recommendations

1. Do not add more controlled examples solely to increase volume before reviewing the domain-shift and ablation evidence.
2. Treat developer_setup failure as a data/evidence coverage problem until the 19-case review and nearest-neighbor views show otherwise; do not relabel those cases automatically.
3. If the provenance discriminator is easy and controlled structural fingerprints are concentrated, prioritize diverse natural development acquisition and less templated controlled cases.
4. Do not start the semantic embedding experiment until these diagnostics are reviewed and a representation experiment is justified.

## Reproducibility artifacts

- `category_v8_validation_error_analysis.jsonl` and `views/` contain only safe pre-change evidence plus analysis gold/prediction fields.
- `developer_setup_19_case_review.jsonl` and `.md` cover every natural developer_setup case.
- `domain_shift_summary.json` contains structural comparisons and the repository-grouped provenance discriminator.
- `nearest_neighbor_analysis.jsonl` contains separate natural and controlled candidate pools.
- `input_ablation_results.json` contains the fixed-current-Category-V8 char-TF-IDF field comparisons.
