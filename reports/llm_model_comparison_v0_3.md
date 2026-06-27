# LLM Model Comparison v0.3

> Important: This report was generated with the mock backend. Mock results validate the DocGuard LLM pipeline, but they do not represent real Hugging Face model quality. Real model results must be generated with transformers_local or text_generation_inference backends.

Split: `validation`
Backend: `mock`

| Metric | rule_based_v0_3 | qwen2_5_coder_7b | deepseek_coder_6_7b | qwen2_5_coder_3b | qwen2_5_coder_1_5b | qwen2_5_coder_0_5b | Best model | Interpretation |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| `docs_update_required_precision` | 100.00% | 100.00% | 100.00% | 100.00% | 100.00% | 100.00% | `qwen2_5_coder_7b` | Mock backend validates plumbing; real model runs should replace these values. |
| `docs_update_required_recall` | 54.22% | 72.73% | 72.73% | 72.73% | 72.73% | 72.73% | `qwen2_5_coder_7b` | Mock backend validates plumbing; real model runs should replace these values. |
| `docs_update_required_f1` | 70.32% | 84.21% | 84.21% | 84.21% | 84.21% | 84.21% | `qwen2_5_coder_7b` | Mock backend validates plumbing; real model runs should replace these values. |
| `scenario_type_accuracy` | 7.20% | 20.00% | 20.00% | 20.00% | 20.00% | 20.00% | `qwen2_5_coder_7b` | Mock backend validates plumbing; real model runs should replace these values. |
| `doc_category_accuracy` | 7.20% | 40.00% | 40.00% | 40.00% | 40.00% | 40.00% | `qwen2_5_coder_7b` | Mock backend validates plumbing; real model runs should replace these values. |
| `target_doc_file_accuracy` | 33.60% | 40.00% | 40.00% | 40.00% | 40.00% | 40.00% | `qwen2_5_coder_7b` | Mock backend validates plumbing; real model runs should replace these values. |
| `patch_fact_coverage` | 11.69% | 54.55% | 54.55% | 54.55% | 54.55% | 54.55% | `qwen2_5_coder_7b` | Mock backend validates plumbing; real model runs should replace these values. |
