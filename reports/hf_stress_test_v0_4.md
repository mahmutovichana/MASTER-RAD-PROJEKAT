# HF Stress Test v0.4 raw_diff_plus_docs

| Metric | Value |
| --- | ---: |
| `model_name` | sentence-transformers/all-MiniLM-L6-v2 |
| `input_mode` | raw_diff_plus_docs |
| `classifier_type` | LogisticRegression |
| `total_records` | 800 |
| `docs_update_required_precision` | 1.0000 |
| `docs_update_required_recall` | 1.0000 |
| `docs_update_required_f1` | 1.0000 |
| `false_positive_count` | 0 |
| `false_negative_count` | 0 |
| `positive_doc_category_accuracy` | 0.9025 |
| `positive_target_doc_file_accuracy` | 0.8025 |
| `positive_scenario_type_accuracy` | 0.8375 |
| `negative_classification_accuracy` | 1.0000 |
| `macro_scenario_f1` | 0.7204 |
| `macro_doc_category_f1` | 0.9256 |
| `average_embedding_inference_latency_seconds` | 0.0267 |

## Binary Robustness

The saved stress run shows binary detection remained robust: F1 is `1.0000`, with `0` false positives and `0` false negatives.

## Fine-Grained Robustness

Fine-grained prediction is more sensitive to lexical/template changes: positive doc category accuracy is `0.9025`, target file accuracy is `0.8025`, positive scenario accuracy is `0.8375`, and macro scenario F1 is `0.7204`.

The metrics `negative_scenario_type_accuracy` and `negative_reason_group_accuracy` were added after this saved stress run. Rerun the stress command to refresh this report with those fields:

```bash
python -m docguard_hf_classifier.cli stress-test --version v0_4 --input-mode raw_diff_plus_docs
```
