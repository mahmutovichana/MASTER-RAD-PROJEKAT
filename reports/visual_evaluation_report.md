# Visual Evaluation Report

> Important: This report was generated with the mock backend. Mock results validate the DocGuard LLM pipeline, but they do not represent real Hugging Face model quality. Real model results must be generated with transformers_local or text_generation_inference backends.

These figures summarize dataset v0.3 history, v0.4 CPU-first dataset diagnostics, and the rule-based, ML, and deterministic hybrid evaluation paths. ROC and precision-recall curves use simple baseline scores: 1.0 for confident positive, 0.0 for confident negative, and 0.5 for unknown or unsupported changes.

The all-scenario HF confusion chart with an `other` bucket is diagnostic only and should not be used as the main thesis figure because `other` aggregates unrelated scenario labels. Use the positive scenario, negative scenario, grouped negative reason, and top-confusion figures instead.

Figure generation tries to use matplotlib first. In this local environment matplotlib was unavailable, so the script can fall back to a small built-in PNG renderer while preserving the same output filenames.

## Rule-based baseline figures

### baseline_metrics_v0_1_v0_2_v0_3

![baseline_metrics_v0_1_v0_2_v0_3](figures/baseline_metrics_v0_1_v0_2_v0_3.png)

### baseline_vs_ml_vs_hf_vs_hybrid_metrics_v0_4

![baseline_vs_ml_vs_hf_vs_hybrid_metrics_v0_4](figures/baseline_vs_ml_vs_hf_vs_hybrid_metrics_v0_4.png)

### baseline_vs_ml_vs_hybrid_metrics_v0_4

![baseline_vs_ml_vs_hybrid_metrics_v0_4](figures/baseline_vs_ml_vs_hybrid_metrics_v0_4.png)

### binary_confusion_matrix_v0_3

![binary_confusion_matrix_v0_3](figures/binary_confusion_matrix_v0_3.png)

### cpu_latency_comparison_v0_4

![cpu_latency_comparison_v0_4](figures/cpu_latency_comparison_v0_4.png)

### dataset_version_record_counts

![dataset_version_record_counts](figures/dataset_version_record_counts.png)

### dataset_version_record_counts_v0_3_v0_4

![dataset_version_record_counts_v0_3_v0_4](figures/dataset_version_record_counts_v0_3_v0_4.png)

### doc_category_distribution_v0_3

![doc_category_distribution_v0_3](figures/doc_category_distribution_v0_3.png)

### doc_category_distribution_v0_4

![doc_category_distribution_v0_4](figures/doc_category_distribution_v0_4.png)

### hf_embedding_confusion_scenarios_v0_4

![hf_embedding_confusion_scenarios_v0_4](figures/hf_embedding_confusion_scenarios_v0_4.png)

### hf_embedding_doc_category_accuracy_v0_4

![hf_embedding_doc_category_accuracy_v0_4](figures/hf_embedding_doc_category_accuracy_v0_4.png)

### hf_embedding_scenario_confusion_all_with_other_v0_4

![hf_embedding_scenario_confusion_all_with_other_v0_4](figures/hf_embedding_scenario_confusion_all_with_other_v0_4.png)

### hf_embedding_vs_ml_scenario_accuracy_v0_4

![hf_embedding_vs_ml_scenario_accuracy_v0_4](figures/hf_embedding_vs_ml_scenario_accuracy_v0_4.png)

### hf_full_vs_no_leak_comparison_v0_4

![hf_full_vs_no_leak_comparison_v0_4](figures/hf_full_vs_no_leak_comparison_v0_4.png)

### hf_input_ablation_binary_f1_v0_4

![hf_input_ablation_binary_f1_v0_4](figures/hf_input_ablation_binary_f1_v0_4.png)

### hf_input_ablation_doc_category_accuracy_v0_4

![hf_input_ablation_doc_category_accuracy_v0_4](figures/hf_input_ablation_doc_category_accuracy_v0_4.png)

### hf_input_ablation_scenario_accuracy_v0_4

![hf_input_ablation_scenario_accuracy_v0_4](figures/hf_input_ablation_scenario_accuracy_v0_4.png)

### hf_latency_comparison_v0_4

![hf_latency_comparison_v0_4](figures/hf_latency_comparison_v0_4.png)

### hf_negative_reason_group_accuracy_v0_4

![hf_negative_reason_group_accuracy_v0_4](figures/hf_negative_reason_group_accuracy_v0_4.png)

### hf_negative_reason_group_confusion_v0_4

![hf_negative_reason_group_confusion_v0_4](figures/hf_negative_reason_group_confusion_v0_4.png)

### hf_negative_scenario_confusion_v0_4

![hf_negative_scenario_confusion_v0_4](figures/hf_negative_scenario_confusion_v0_4.png)

### hf_negative_subtype_accuracy_v0_4

![hf_negative_subtype_accuracy_v0_4](figures/hf_negative_subtype_accuracy_v0_4.png)

### hf_positive_scenario_confusion_v0_4

![hf_positive_scenario_confusion_v0_4](figures/hf_positive_scenario_confusion_v0_4.png)

### hf_staged_vs_flat_metrics_v0_4

![hf_staged_vs_flat_metrics_v0_4](figures/hf_staged_vs_flat_metrics_v0_4.png)

### hf_stress_test_metrics_v0_4

![hf_stress_test_metrics_v0_4](figures/hf_stress_test_metrics_v0_4.png)

### hf_top_scenario_confusions_v0_4

![hf_top_scenario_confusions_v0_4](figures/hf_top_scenario_confusions_v0_4.png)

### invalid_source_target_file_count_v0_4

![invalid_source_target_file_count_v0_4](figures/invalid_source_target_file_count_v0_4.png)

### macro_f1_scenario_doc_category_v0_4

![macro_f1_scenario_doc_category_v0_4](figures/macro_f1_scenario_doc_category_v0_4.png)

### negative_classification_accuracy_v0_4

![negative_classification_accuracy_v0_4](figures/negative_classification_accuracy_v0_4.png)

### negative_scenario_distribution_v0_4

![negative_scenario_distribution_v0_4](figures/negative_scenario_distribution_v0_4.png)

### per_doc_category_accuracy_v0_3

![per_doc_category_accuracy_v0_3](figures/per_doc_category_accuracy_v0_3.png)

### per_scenario_accuracy_v0_3

![per_scenario_accuracy_v0_3](figures/per_scenario_accuracy_v0_3.png)

### positive_doc_category_distribution_v0_4

![positive_doc_category_distribution_v0_4](figures/positive_doc_category_distribution_v0_4.png)

### positive_negative_distribution_v0_3

![positive_negative_distribution_v0_3](figures/positive_negative_distribution_v0_3.png)

### positive_negative_distribution_v0_4

![positive_negative_distribution_v0_4](figures/positive_negative_distribution_v0_4.png)

### positive_only_target_file_accuracy_v0_4

![positive_only_target_file_accuracy_v0_4](figures/positive_only_target_file_accuracy_v0_4.png)

### positive_scenario_distribution_v0_4

![positive_scenario_distribution_v0_4](figures/positive_scenario_distribution_v0_4.png)

### precision_recall_curve_v0_3

![precision_recall_curve_v0_3](figures/precision_recall_curve_v0_3.png)

### roc_curve_v0_3

![roc_curve_v0_3](figures/roc_curve_v0_3.png)

### router_vs_hf_agreement_v0_4

![router_vs_hf_agreement_v0_4](figures/router_vs_hf_agreement_v0_4.png)

### scenario_confusion_matrix_v0_3

![scenario_confusion_matrix_v0_3](figures/scenario_confusion_matrix_v0_3.png)

### scenario_distribution_v0_3

![scenario_distribution_v0_3](figures/scenario_distribution_v0_3.png)

### scenario_distribution_v0_4

![scenario_distribution_v0_4](figures/scenario_distribution_v0_4.png)

### split_distribution_v0_3

![split_distribution_v0_3](figures/split_distribution_v0_3.png)

## Mock LLM pipeline figures

### baseline_vs_llm_doc_category_accuracy_v0_3_mock

![baseline_vs_llm_doc_category_accuracy_v0_3_mock](figures/baseline_vs_llm_doc_category_accuracy_v0_3_mock.png)

### baseline_vs_llm_fact_coverage_v0_3_mock

![baseline_vs_llm_fact_coverage_v0_3_mock](figures/baseline_vs_llm_fact_coverage_v0_3_mock.png)

### baseline_vs_llm_metrics_v0_3_mock

![baseline_vs_llm_metrics_v0_3_mock](figures/baseline_vs_llm_metrics_v0_3_mock.png)

### llm_confusion_matrix_best_model_v0_3_mock

![llm_confusion_matrix_best_model_v0_3_mock](figures/llm_confusion_matrix_best_model_v0_3_mock.png)

### llm_latency_comparison_v0_3_mock

![llm_latency_comparison_v0_3_mock](figures/llm_latency_comparison_v0_3_mock.png)

### llm_model_comparison_metrics_v0_3_mock

![llm_model_comparison_metrics_v0_3_mock](figures/llm_model_comparison_metrics_v0_3_mock.png)

### llm_parse_error_counts_v0_3_mock

![llm_parse_error_counts_v0_3_mock](figures/llm_parse_error_counts_v0_3_mock.png)

### llm_per_doc_category_best_model_v0_3_mock

![llm_per_doc_category_best_model_v0_3_mock](figures/llm_per_doc_category_best_model_v0_3_mock.png)

## Real Hugging Face LLM figures

### baseline_vs_real_llm_doc_category_accuracy_v0_3

![baseline_vs_real_llm_doc_category_accuracy_v0_3](figures/baseline_vs_real_llm_doc_category_accuracy_v0_3.png)

### baseline_vs_real_llm_fact_coverage_v0_3

![baseline_vs_real_llm_fact_coverage_v0_3](figures/baseline_vs_real_llm_fact_coverage_v0_3.png)

### baseline_vs_real_llm_metrics_v0_3

![baseline_vs_real_llm_metrics_v0_3](figures/baseline_vs_real_llm_metrics_v0_3.png)

### real_llm_confusion_matrix_best_model_v0_3

![real_llm_confusion_matrix_best_model_v0_3](figures/real_llm_confusion_matrix_best_model_v0_3.png)

### real_llm_latency_v0_3

![real_llm_latency_v0_3](figures/real_llm_latency_v0_3.png)

### real_llm_model_comparison_metrics_v0_3

![real_llm_model_comparison_metrics_v0_3](figures/real_llm_model_comparison_metrics_v0_3.png)

### real_llm_normalized_vs_raw_accuracy_v0_3

![real_llm_normalized_vs_raw_accuracy_v0_3](figures/real_llm_normalized_vs_raw_accuracy_v0_3.png)

### real_llm_parse_errors_v0_3

![real_llm_parse_errors_v0_3](figures/real_llm_parse_errors_v0_3.png)

### real_llm_per_doc_category_best_model_v0_3

![real_llm_per_doc_category_best_model_v0_3](figures/real_llm_per_doc_category_best_model_v0_3.png)
