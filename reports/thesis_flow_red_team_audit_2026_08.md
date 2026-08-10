# Thesis Flow Red-Team Audit 2026-08

## Summary

The current thesis flow is broadly coherent and defensible, but it must be written as a hierarchy of evidence rather than as one single benchmark. No result should be described as production-ready. The main methodological risks are: synthetic generator bias, CoDocBench being positive-only, Deep-JIT being a proxy rather than the full Markdown documentation task, Deep-JIT numeric label polarity remaining caveated, and Deep-JIT model selection using a Return-only validation split while the test set combines Return and Summary.

## Evidence Consistency Table

| Claim | Source report/file | Status | Recommended correction |
| --- | --- | --- | --- |
| Synthetic v0.4 contains 30 projects and 6000 records with 3000 positive / 3000 negative examples. | `reports/dataset_v0_4_summary.md`, `reports/project_recovery_audit_2026_08.md`, README summary text | ok | Keep wording as controlled synthetic benchmark. |
| Synthetic v0.4 split is approximately 4200/1000/800 train/validation/test. | `reports/project_recovery_audit_2026_08.md`, v0.4 evaluation reports | ok | If exact split counts are needed in thesis, cite the dataset summary rather than prose. |
| Synthetic v0.4 hybrid/HF path reaches perfect binary test performance. | `reports/hybrid_hf_embedding_evaluation_v0_4_test.md`, `reports/hf_embedding_evaluation_v0_4_raw_diff_plus_docs_test_staged.md` | ok but risky | Must be described as synthetic controlled performance, not real-world generalization. |
| Synthetic patch fact coverage is validated only in synthetic/prototype reports. | `reports/hybrid_hf_embedding_evaluation_v0_4_test.md`, `reports/hybrid_evaluation_v0_4_test.md` | ok but limited | Do not extend patch-generation claims to CoDocBench or Deep-JIT. |
| CoDocBench sample size is 500 positives. | `reports/external_codocbench_sample_500_audit_2026_08.md`, README | ok | State positive-only. |
| CoDocBench `code_diff_only` positive recall is 500/500 = 100.00%. | `reports/external_codocbench_positive_recall_code_diff_only_2026_08.md`, `reports/external_codocbench_input_mode_comparison_2026_08.md` | ok | Do not report precision/F1/FPR from this sample. |
| CoDocBench `code_diff_plus_doc_before` positive recall is 499/500 = 99.80%. | `reports/external_codocbench_positive_recall_code_diff_plus_doc_before_2026_08.md` | ok | Label as assisted but non-leaky because it uses current docs only. |
| CoDocBench leakage audit says the main fair/assisted runs did not use `doc_diff` or `doc_after`. | `reports/external_codocbench_evaluation_leakage_audit_2026_08.md`, `docguard_external/evaluate_existing_docguard.py` | ok | Upper-bound `doc_diff` mode must remain separated and never be primary evidence. |
| Synthetic negative sanity controls had 0/500 false positives in both tested modes. | `reports/synthetic_negative_control_code_diff_only_2026_08.md`, `reports/synthetic_negative_control_code_diff_plus_doc_before_2026_08.md` | ok | Keep as sanity check only; not external negative evidence. |
| Deep-JIT zero-shot binary proxy sample has TP 250, FN 0, FP 248, TN 2. | `reports/external_docchecker_existing_docguard_binary_evaluation_2026_08.md` | ok | Describe as near always-positive behavior. |
| Deep-JIT zero-shot metrics are accuracy 50.40%, precision 50.20%, recall 100.00%, F1 66.84%, FPR 99.20%. | `reports/external_docchecker_existing_docguard_binary_evaluation_2026_08.md`, README | ok | Contextualize F1 as misleading due high FPR. |
| Normalized Deep-JIT benchmark contains train 24348, validation 1790, test 2906 records. | `reports/external_deep_jit_normalized_export_2026_08.md` | ok | Mention validation is Return-only. |
| Deep-JIT trained classifier best model is `tfidf_logreg` with `old_comment_plus_code_diff`, selected by validation F1. | `reports/external_deep_jit_model_comparison_2026_08.md` | ok | Add limitation that validation does not include Summary. |
| Deep-JIT trained classifier test metrics are accuracy 68.72%, precision 73.41%, recall 58.71%, F1 65.24%, FPR 21.27%, specificity 78.73%, balanced accuracy 68.72%, MCC 0.3821. | `reports/external_deep_jit_model_comparison_2026_08.md`, `reports/external_deep_jit_zero_shot_vs_trained_2026_08.md` | ok | Prefer specificity/balanced accuracy/MCC over F1 for interpretation. |
| Validation threshold tuning selected 0.45 and achieved test F1 67.32%, FPR 31.31%. | `reports/external_deep_jit_validation_threshold_tuning_2026_08.md` | ok | Label diagnostic; threshold chosen on Return-only validation. |
| Deep-JIT label polarity is plausible but not fully confirmed. | `reports/external_deep_jit_label_polarity_evidence_2026_08.md` | ok | Keep caveat. Do not upgrade to confirmed without explicit dataset legend. |
| Evidence hierarchy separates synthetic, CoDocBench, synthetic negatives, Deep-JIT zero-shot, and Deep-JIT adaptation. | `reports/thesis_evidence_map_2026_08.md`, `reports/external_validation_evidence_comparison_2026_08.md` | ok | Use this hierarchy in thesis results section. |

## Major Red-Team Findings

1. No current result invalidates the flow, but the Deep-JIT validation-selection setup is weaker than ideal because Summary is missing from validation.
2. Patch generation is not externally validated; it is demonstrated in controlled synthetic/prototype reports only.
3. Deep-JIT label polarity remains a methodological caveat.
4. Zero-shot F1 must not be presented as competitive binary performance because specificity is 0.80% and FPR is 99.20%.

## Overall Verdict

The current flow is thesis-usable if written carefully. The strongest framing is: controlled prototype success, external positive sensitivity, external binary failure mode, and task-specific adaptation improving specificity.
