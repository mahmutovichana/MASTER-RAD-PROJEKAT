# DocGuard Dataset Factory

Synthetic dataset factory for the MSc thesis project:

**Intelligent NLP Agent for Consistency Analysis of Software Projects**

DocGuard analyzes REST API code diffs, detects whether API documentation is missing or outdated, and proposes a precise documentation patch.

## Project Recovery and Real-Data Validation

As of the August 2026 recovery audit, DocGuard should not be restarted from scratch. The existing synthetic v0.4 dataset, HF embedding classifier, hybrid validator, runtime, and VS Code MVP should be preserved as a controlled prototype and developer workflow demo.

Synthetic v0.4 results should not be treated as final thesis-level evidence by themselves. The next research step is external real-world validation, preferably a small CoDocBench pilot mapped through `docguard_external/`.

Key recovery reports:

- `reports/project_recovery_audit_2026_08.md`
- `reports/synthetic_dataset_risk_assessment_2026_08.md`
- `reports/external_dataset_research_plan_2026_08.md`
- `reports/research_reframing_2026_08.md`
- `reports/synthetic_vs_real_evaluation_design_2026_08.md`

## External Real-World Validation Pilot

Synthetic-only evaluation is not enough for final thesis evidence because the v0.4 dataset is generated inside this project and may contain template/generator bias. CoDocBench is introduced as the first real-world validation pilot for code-documentation or code-docstring co-change behavior.

The pilot intentionally maps only positive code-doc co-change examples first. It does **not** create negative labels automatically from code-only commits.

Install optional external dataset dependencies if needed:

```bash
python -m pip install datasets huggingface_hub pandas pyarrow
```

Inspect, prepare, and validate a small CoDocBench sample:

```bash
python -m docguard_external.cli inspect --dataset codocbench --limit 5
python -m docguard_external.cli prepare --dataset codocbench --limit 100 --output data/external/codocbench_sample.jsonl
python -m docguard_external.cli validate --input data/external/codocbench_sample.jsonl
```

The first 100-record CoDocBench pilot has been completed and validated. To create a stronger stratified positive sample:

```bash
python -m docguard_external.cli prepare --dataset codocbench --limit 500 --output data/external/codocbench_sample_500.jsonl --exclude-whitespace-only --max-per-project 50 --shuffle --seed 42
python -m docguard_external.cli validate --input data/external/codocbench_sample_500.jsonl
```

To evaluate whether existing DocGuard predictors recognize those real external positives:

```bash
python -m docguard_external.cli evaluate-existing --input data/external/codocbench_sample_500.jsonl --output reports/external_codocbench_existing_docguard_positive_recall_2026_08.md
```

This positive-only external evaluation can report positive recall and false negatives. It cannot report precision, F1, false-positive rate, or negative classification quality until a defensible external negative set is added.

The 500-record CoDocBench positive pilot is now leakage-audited. The strict `code_diff_only` mode achieved 100.00% positive recall on 500 positives. The assisted `code_diff_plus_doc_before` mode achieved 99.80% positive recall. Confidence remains low, so this is evidence of high sensitivity to real code-doc co-changes, not complete external generalization. The `code_diff_plus_doc_diff_upper_bound` mode includes future documentation changes and is useful only as an upper-bound diagnostic, not final thesis evidence.

Run fair and upper-bound external input modes explicitly:

```bash
python -m docguard_external.cli evaluate-existing --input data/external/codocbench_sample_500.jsonl --output reports/external_codocbench_positive_recall_code_diff_only_2026_08.md --external-input-mode code_diff_only --diagnostics
python -m docguard_external.cli evaluate-existing --input data/external/codocbench_sample_500.jsonl --output reports/external_codocbench_positive_recall_code_diff_plus_doc_before_2026_08.md --external-input-mode code_diff_plus_doc_before --diagnostics
python -m docguard_external.cli evaluate-existing --input data/external/codocbench_sample_500.jsonl --output reports/external_codocbench_positive_recall_doc_diff_upper_bound_2026_08.md --external-input-mode code_diff_plus_doc_diff_upper_bound --diagnostics
```

External negative labels are still required before reporting precision, F1, false-positive rate, or negative classification quality for the full project-level Markdown documentation task.

Run synthetic negative sanity controls to check for constant-positive behavior:

```bash
python -m docguard_external.cli evaluate-synthetic-negatives --limit 500 --external-input-mode code_diff_only --output reports/synthetic_negative_control_code_diff_only_2026_08.md
python -m docguard_external.cli evaluate-synthetic-negatives --limit 500 --external-input-mode code_diff_plus_doc_before --output reports/synthetic_negative_control_code_diff_plus_doc_before_2026_08.md
```

These controls use synthetic negatives only. They are not a substitute for a real external negative set.

The synthetic negative controls passed with 0/500 false positives in both `code_diff_only` and `code_diff_plus_doc_before` modes, so the model does not appear constant-positive under this control.

Inspect local DocChecker / Deep-JIT data after manually downloading it:

```bash
python -m docguard_external.cli inspect --dataset docchecker --data-dir data/external/raw/docchecker --limit 10
python -m docguard_external.cli inspect --dataset docchecker --data-dir data/external/raw/deep_jit_inconsistency --limit 10
```

The Deep-JIT / DocChecker-style local inspection confirmed explicit binary labels and old/new code/comment fields in the Just-In-Time inconsistency data. A balanced 500-record external binary proxy sample can be prepared, validated, and evaluated with:

```bash
python -m docguard_external.cli prepare --dataset docchecker --data-dir data/external/raw/deep_jit_inconsistency --limit 500 --output data/external/docchecker_binary_sample_500.jsonl
python -m docguard_external.cli validate --input data/external/docchecker_binary_sample_500.jsonl
python -m docguard_external.cli evaluate-existing-binary --input data/external/docchecker_binary_sample_500.jsonl --output reports/external_docchecker_existing_docguard_binary_evaluation_2026_08.md
```

The first 500-record external binary proxy evaluation uses Deep-JIT `test` partition records only, balanced across `Return/test` and `Summary/test`. It produced 50.40% accuracy, 50.20% precision, 100.00% recall, and 66.84% F1, with 248/250 negatives predicted as update-required. This is useful evidence that the current model is highly sensitive on real inconsistent comments, but poorly calibrated for external consistent comments in this proxy setting. It is not deployment-ready and motivates external binary adaptation/calibration. It should be reported as code-comment inconsistency proxy evidence, not final system performance and not full Markdown API documentation update performance.

Run the separate Deep-JIT task-specific adaptation experiment:

```bash
python -m docguard_external.cli deep-jit-split-audit --data-dir data/external/raw/deep_jit_inconsistency
python -m docguard_external.cli export-deep-jit-binary --data-dir data/external/raw/deep_jit_inconsistency --output-dir data/external/deep_jit_binary
python -m docguard_external.cli train-binary --train data/external/deep_jit_binary/train.jsonl --validation data/external/deep_jit_binary/validation.jsonl --test data/external/deep_jit_binary/test.jsonl --model-output models/external_deep_jit/binary_tfidf_logreg.joblib --report reports/external_deep_jit_binary_classifier_evaluation_2026_08.md
```

The normalized Deep-JIT export keeps original split boundaries and excludes `new_comment_raw`, `doc_after`, and `doc_diff` from classifier inputs. With best model selection based on validation F1, the lightweight external classifier run selected `tfidf_logreg` with `old_comment_plus_code_diff` input: 68.72% accuracy, 73.41% precision, 58.71% recall, 65.24% F1, 21.27% FPR, 78.73% specificity, 68.72% balanced accuracy, and MCC 0.3821 on the test split. This greatly improves specificity compared with the zero-shot DocGuard FPR of 99.20% and specificity of 0.80%, but it does not turn Deep-JIT into project-level Markdown documentation evidence. Validation-set threshold tuning selected threshold `0.45`; applied once to test, it produced 67.65% accuracy, 68.03% precision, 66.62% recall, 67.32% F1, and 31.31% FPR. Deep-JIT label polarity remains `plausible_manual_verification_needed` until confirmed from original dataset documentation or preprocessing code.

### Deep-JIT combined-validation robustness experiment

The first Deep-JIT adaptation used the available official Return validation split, while the test set included both Return and Summary. To reduce this Return-only validation bias, a robustness export adds a deterministic balanced Summary validation carve-out from `Summary/train.json` while keeping `Summary/test.json` untouched:

```bash
python -m docguard_external.cli export-deep-jit-combined-validation --data-dir data/external/raw/deep_jit_inconsistency --output-dir data/external/deep_jit_binary_combined_validation --seed 42 --summary-validation-per-label 420
python -m docguard_external.cli train-binary --train data/external/deep_jit_binary_combined_validation/train.jsonl --validation data/external/deep_jit_binary_combined_validation/validation.jsonl --test data/external/deep_jit_binary_combined_validation/test.jsonl --model-output models/external_deep_jit_combined_validation/binary_tfidf_logreg.joblib --report reports/external_deep_jit_combined_validation_classifier_evaluation_2026_08.md
```

The combined-validation split contains 23,508 train records, 2,630 validation records, and the same untouched 2,906-record test split. Validation now includes Return 1,790 + Summary 840 records. This changed model selection to `tfidf_linear_svc` with `old_comment_plus_code_diff`: 66.41% accuracy, 68.82% precision, 60.01% recall, 64.12% F1, 27.19% FPR, 72.81% specificity, 66.41% balanced accuracy, and MCC 0.3310. The conclusion remains the same but more conservative: task-specific adaptation greatly improves specificity over zero-shot, while model selection is somewhat sensitive to validation subset composition. The combined-validation result should be treated as the cleaner thesis result; the Return-only validation result remains a historical baseline. Generated `data/external/deep_jit_binary_combined_validation/` and `models/external_deep_jit_combined_validation/` are ignored and should not be committed.

### Next improvement phase

The current combined-validation Deep-JIT result is not final. It is methodologically cleaner than the earlier Return-only validation run, but its accuracy, F1, and MCC are still modest for the desired thesis evidence package.

The next implementation phase keeps DocGuard as the central thesis artifact and treats Deep-JIT as an external binary proxy benchmark, not as the full Markdown documentation task. Planned improvements:

- stronger classical Deep-JIT baseline with word/char TF-IDF, manual code/comment features, and validation-MCC model selection
- optional frozen pretrained code-encoder baseline using UniXcoder or CodeBERT embeddings if dependencies and hardware allow
- small project-level real-world case study to evaluate DocGuard detection, category/target routing, and documentation patch usefulness

Run the stronger classical baseline:

```bash
python -m docguard_external.cli train-binary-v2 --train data/external/deep_jit_binary_combined_validation/train.jsonl --validation data/external/deep_jit_binary_combined_validation/validation.jsonl --test data/external/deep_jit_binary_combined_validation/test.jsonl --model-output models/external_deep_jit_classical_v2/binary_classical_v2.joblib --report reports/external_deep_jit_classical_v2_model_comparison_2026_08.md
```

The full classical v2 run is the current best Deep-JIT proxy result. It selected `logreg_balanced` with `word_char_tfidf_plus_manual_features` and `old_comment_plus_code_diff`: 75.60% accuracy, 78.84% precision, 69.99% recall, 74.15% F1, 18.79% FPR, 81.21% specificity, 75.60% balanced accuracy, and MCC 0.5153 on the untouched combined-validation Deep-JIT test split. This improves over the previous combined-validation best while remaining an external code-comment proxy result.

The v2 safety and ablation audit confirms that the primary v2 model excludes future documentation fields (`new_comment_raw`, `doc_after`, `doc_diff`) and is selected by validation only. Manual features are useful but not the sole driver: word+char TF-IDF provides the main lift, and manual features add a smaller improvement.

Run the optional frozen code-encoder baseline:

```bash
python -m docguard_external.cli train-code-encoder-binary --train data/external/deep_jit_binary_combined_validation/train.jsonl --validation data/external/deep_jit_binary_combined_validation/validation.jsonl --test data/external/deep_jit_binary_combined_validation/test.jsonl --model-output models/external_deep_jit_code_encoder/binary_code_encoder.joblib --report reports/external_deep_jit_frozen_code_encoder_comparison_2026_08.md --cache-dir data/external/embedding_cache
```

The frozen pretrained encoder baseline is implemented but deferred locally because CUDA is unavailable. It should be treated as an optional GPU/Colab experiment. DocGuard remains the central thesis artifact; Deep-JIT is only an external proxy benchmark for code-comment consistency, not the full Markdown DocGuard benchmark.

### Project-level DocGuard case study

The next required alignment step is a small manually labeled project-level case study. This keeps DocGuard as the central thesis artifact: code diff -> update-required detection -> routing/category -> documentation patch suggestion -> developer workflow.

The case-study framework lives in:

- `docguard_external/project_case_study.py`
- `data/external/project_case_study/manual_cases_template.jsonl`
- `reports/docguard_project_case_study_labeling_template_2026_08.md`
- `reports/docguard_project_level_real_case_study_plan_2026_08.md`
- `reports/docguard_project_case_study_runner_plan_2026_08.md`

Validate the starter template:

```bash
python -m docguard_external.cli validate-project-cases --input data/external/project_case_study/manual_cases_template.jsonl --report reports/docguard_project_case_study_template_validation_2026_08.md
```

The first real case-study file now contains 20 public GitHub PR cases: 15 positive documentation-update cases and 5 negative no-update cases. After methodology hardening, confidence distribution is 15 high, 2 medium, and 3 low. Validation passed:

```bash
python -m docguard_external.cli validate-project-cases --input data/external/project_case_study/manual_cases.jsonl --report reports/docguard_project_case_study_validation_2026_08.md
```

This case study should evaluate binary `docs_update_required`, documentation category, target documentation file, and human patch usefulness. Placeholder records are examples only and must not be reported as results.

The automatic case-study runner is deferred for now because the current DocGuard runtime expects synthetic records and synthetic REST route patterns. A real-case adapter is needed before reporting automatic case-study scores. Safe automatic inputs are limited to `language`, `code_changed_files`, `code_diff_excerpt`, and `docs_before_excerpt`. `changed_files`, `docs_changed_files`, manually assigned `change_type`, `docs_after_excerpt`, and gold/manual fields are audit-only.

### DocGuard live flow playground

The repository includes a small synthetic live-flow playground for final implementation sanity checks. It creates an invented `atlas_review_api` mini project, generates 15 live demo cases, and runs `docguard_hybrid.predict()` across the main documentation classes. This is an on-the-spot demo layer, not a benchmark and not a replacement for the real case study or Deep-JIT proxy evidence.

Run it with:

```bash
python -m docguard_demo.run_live_flow --output-dir reports/live_flow
```

Current live-flow output is in `reports/live_flow/docguard_live_flow_evaluation_2026_08.md`. The demo covers API reference, model contract, configuration, testing instructions, workflow documentation, architecture flow, developer setup, changelog, and no-update cases.

Large raw external downloads should stay under `data/external/raw/`, which is ignored by git.

CoDocBench should be reported as real-world code-doc/comment validation, not as a direct replacement for project-level Markdown documentation update detection.

This repository currently contains a reusable synthetic dataset generator:

- 10 generated TypeScript + Express REST API projects
- 1000 dataset records total
- dataset schema
- validation script
- project-level train/validation/test split files

The full target can later be reached by adding more projects and increasing the generation configuration.

## Current Status

- Dataset v0.1 frozen in `dataset_versions/v0_1`
- Dataset v0.2 frozen in `dataset_versions/v0_2`
- Dataset v0.3 generated with 10 projects, 2500 records, higher-level documentation categories, and expanded scenario diversity
- Rule-based baseline implemented in `docguard/`
- Baseline evaluated on v0.1, v0.2, and v0.3
- Next step: NLP-assisted DocGuard for harder v0.3 scenarios

## Dataset v0.1

Dataset v0.1 is a controlled synthetic dataset for the first baseline evaluation of the DocGuard agent. It is designed to test whether a deterministic or NLP-assisted system can inspect REST API code diffs, decide whether API documentation needs an update, classify the change type, and produce a minimal documentation patch.

Dataset v0.1 contains:

- 10 synthetic TypeScript + Express REST API projects
- 1000 JSONL records
- 5 scenario types: `new_endpoint`, `changed_validation_min`, `changed_auth_requirement`, `added_response_field`, `internal_refactor`
- project-level train/validation/test split
- train: 7 projects
- validation: 1 project
- test: 2 projects
- validation status: passed with `python scripts/validate_dataset.py`

The automatic validator checks schema and consistency constraints, but it does not replace human quality review. Use `reports/manual_audit_sample.jsonl` and `reports/manual_audit_template.md` for manual inspection.

## Structure

```text
generated_projects/
  shop-api/
  auth-api/
  task-manager-api/
  library-api/
  booking-api/
  inventory-api/
  billing-api/
  support-ticket-api/
  learning-platform-api/
  clinic-api/
data/
  docguard_dataset.jsonl
  train.jsonl
  validation.jsonl
  test.jsonl
  schema.json
scripts/
  create_manual_audit_sample.py
  validate_dataset.py
reports/
  dataset_statistics.md
  dataset_v0_1_summary.md
  dataset_v0_2_summary.md
  dataset_v0_3_summary.md
  visual_evaluation_report.md
  figures/
  manual_audit_sample.jsonl
  manual_audit_template.md
  quality_checks.md
```

## Validate The Dataset

Regenerate the current inspection dataset:

```bash
python scripts/build_dataset.py
```

Validate the generated files:

```bash
python scripts/validate_dataset.py
```

The validator checks required fields, positive/negative label consistency, duplicate ids, changed file references, project-level split leakage, and basic schema constraints.

Evaluate the current baseline:

```bash
python -m docguard.cli evaluate --split test --version v0_3
```

Generate visual reports:

```bash
python scripts/generate_figures.py
```

## Hugging Face LLM-Assisted Phase

> Important: This report was generated with the mock backend. Mock results validate the DocGuard LLM pipeline, but they do not represent real Hugging Face model quality. Real model results must be generated with transformers_local or text_generation_inference backends.

The LLM-assisted prototype lives in `docguard_llm/`. It performs inference only; no fine-tuning is done in this phase.

The default repository checks do not download or run large Hugging Face models. Real model evaluation is optional and should be run manually on a small subset first.

Supported model keys:

- `qwen2_5_coder_7b`: `Qwen/Qwen2.5-Coder-7B-Instruct`
- `deepseek_coder_6_7b`: `deepseek-ai/deepseek-coder-6.7b-instruct`
- `qwen2_5_coder_3b`: `Qwen/Qwen2.5-Coder-3B-Instruct`
- `qwen2_5_coder_1_5b`: `Qwen/Qwen2.5-Coder-1.5B-Instruct`
- `qwen2_5_coder_0_5b`: `Qwen/Qwen2.5-Coder-0.5B-Instruct`

The 0.5B and 1.5B models are included only for CPU-friendly real-run validation. The 3B model is the first stronger local option. The 7B model remains the main quality candidate, but it should normally be run on GPU, Colab/Kaggle, or a vLLM/TGI server rather than CPU-only.

List models:

```bash
python -m docguard_llm.cli list-models
```

Run a mock evaluation without downloading models:

```bash
python -m docguard_llm.cli evaluate --split validation --model qwen2_5_coder_7b --backend mock --limit 20
python -m docguard_llm.cli compare --split validation --backend mock --limit 20
```

The official mock output filenames include `_mock`, for example:

- `data/llm_predictions_v0_3_validation_mock_qwen2_5_coder_7b.jsonl`
- `reports/llm_evaluation_v0_3_mock_qwen2_5_coder_7b.md`
- `reports/llm_model_comparison_v0_3_mock.md`

Install optional local inference dependencies:

```bash
pip install transformers accelerate torch sentencepiece
```

Optional quantization packages such as `bitsandbytes` may be useful on compatible GPU setups, but they are not required for default checks.

Smoke-test one small real model on one validation record:

```bash
python -m docguard_llm.cli smoke-test --model qwen2_5_coder_0_5b --backend transformers_local --prompt-mode compact_v2
```

Run local Transformers inference:

```bash
python -m docguard_llm.cli evaluate --split validation --model qwen2_5_coder_0_5b --backend transformers_local --limit 10 --prompt-mode compact_v2 --continue-on-error --retry-on-parse-error
```

Run against a local vLLM/TGI OpenAI-compatible server:

```bash
$env:DOCGUARD_TGI_BASE_URL="http://localhost:8000/v1"
python -m docguard_llm.cli evaluate --split validation --model qwen2_5_coder_3b --backend text_generation_inference --limit 10
```

The 7B models may require a GPU, quantization, or a local serving setup. On CPU-only machines, use `qwen2_5_coder_0_5b` first and treat `qwen2_5_coder_1_5b` as an optional next sanity check. See `reports/real_llm_run_plan.md`, `reports/real_llm_cpu_run_status.md`, and `reports/real_llm_manual_review_template.md` before running larger real-model evaluations.

## CPU-Only Real-Run Troubleshooting

Check CUDA availability:

```bash
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"
```

If CUDA is `False`, do not start with 3B or 7B models. CPU and disk offload can be very slow, and full 3B/7B evaluation should be done on GPU, Colab/Kaggle, or vLLM/TGI. Start with the smallest sanity-only real generation path, then 0.5B compact prompts:

```powershell
$env:DOCGUARD_MAX_NEW_TOKENS="60"
python -m docguard_llm.cli smoke-test --model qwen2_5_coder_0_5b --backend transformers_local --sanity-only --debug
```

```powershell
$env:DOCGUARD_MAX_NEW_TOKENS="120"
python -m docguard_llm.cli smoke-test --model qwen2_5_coder_0_5b --backend transformers_local --prompt-mode compact_v2 --debug
```

```powershell
$env:DOCGUARD_MAX_NEW_TOKENS="180"
python -m docguard_llm.cli evaluate --split validation --model qwen2_5_coder_0_5b --backend transformers_local --limit 10 --prompt-mode compact_v2 --continue-on-error --retry-on-parse-error
```

Only after 0.5B works should you try 1.5B sanity-only:

```powershell
$env:DOCGUARD_MAX_NEW_TOKENS="60"
python -m docguard_llm.cli smoke-test --model qwen2_5_coder_1_5b --backend transformers_local --sanity-only --debug
```

The `smoke-test` command writes report checkpoints before generation starts, after prompt build, after generation starts, after generation finishes, and after parsing. Real `evaluate` writes each prediction to JSONL immediately, so partial outputs survive if a later CPU generation fails. `--compact-prompt` remains supported and is equivalent to `--prompt-mode compact`; use `--prompt-mode compact_v2` for the improved enum-guided prompt. For `qwen2_5_coder_0_5b` compact DocGuard prompts, `120` new tokens may truncate JSON; use `180` or `220` for evaluation and keep `60` only for sanity-only. The `--retry-on-parse-error` option retries likely truncated JSON once with 100 additional tokens. The `--timeout-seconds` option is documented for run notes, but no hard Windows timeout is enforced around low-level model generation. Mock results are useful for validating the pipeline, but they are not real Hugging Face model quality.

## Current Split

Splits are project-level:

- train: 7 projects
- validation: 1 project
- test: 2 projects

## DocGuard v0.4 CPU-First Hybrid Phase

v0.4 moves from LLM-heavy experimentation to a CPU-first hybrid system:

- 30 synthetic REST API projects
- 6000 balanced records
- explicit `no_update` category for negatives
- signal extraction and deterministic document routing
- CPU-friendly ML/fallback classifiers
- hybrid agent with deterministic patch composition
- optional small LLM verifier using `--prompt-mode hybrid_compact`

Build and validate v0.4:

```bash
python scripts/build_dataset.py --version v0_4
python scripts/validate_dataset.py --version v0_4
```

The dataset builder writes positive-only documentation category diagnostics to `reports/dataset_v0_4_summary.md`. To experiment with a more even positive category mix, rebuild with:

```bash
python scripts/build_dataset.py --version v0_4 --rebalance-positive-categories
python scripts/validate_dataset.py --version v0_4
```

Train and evaluate CPU ML:

```bash
python -m docguard_ml.cli train --version v0_4
python -m docguard_ml.cli evaluate --version v0_4 --split validation
python -m docguard_ml.cli evaluate --version v0_4 --split test
```

The ML trainer uses scikit-learn when available and falls back to the repository signal model otherwise. Evaluation reports include `ml_backend` so runs are comparable. On Python versions where scikit-learn wheels are not available, use the fallback path or a Python 3.12 virtual environment:

```bash
python -m pip install scikit-learn joblib
```

Evaluate the hybrid router:

```bash
python -m docguard_hybrid.cli evaluate --split validation --version v0_4
python -m docguard_hybrid.cli evaluate --split test --version v0_4
```

Create the v0.4 ablation and figures:

```bash
python scripts/create_ablation_v0_4.py
python scripts/generate_figures.py
```

## Hugging Face Classifier Experiments

v0.4 also includes a separate HF classifier track. The router remains as an interpretable baseline and guardrail, while the HF embedding classifier is used to reduce hardcoded decision logic.

Install the default classifier dependencies:

```bash
python -m pip install sentence-transformers scikit-learn joblib
```

Export the dataset and train/evaluate the CPU-friendly embedding classifier:

```bash
python -m docguard_hf_classifier.cli export --version v0_4 --input-mode raw_diff_plus_docs
python -m docguard_hf_classifier.cli train-embeddings --version v0_4 --model sentence-transformers/all-MiniLM-L6-v2 --input-mode raw_diff_plus_docs
python -m docguard_hf_classifier.cli evaluate-embeddings --version v0_4 --split validation --input-mode raw_diff_plus_docs
python -m docguard_hf_classifier.cli evaluate-embeddings --version v0_4 --split test --input-mode raw_diff_plus_docs
```

Evaluate the hybrid system with HF embedding predictions as the primary decision source and the router as a guardrail:

```bash
python -m docguard_hybrid.cli evaluate --split validation --version v0_4 --decision-source hf_embedding --hf-input-mode raw_diff_plus_docs
python -m docguard_hybrid.cli evaluate --split test --version v0_4 --decision-source hf_embedding --hf-input-mode raw_diff_plus_docs
```

HF input modes are available for leakage analysis:

- `raw_diff_only`: changed files and code diff only
- `raw_diff_plus_docs`: changed files, code diff, and previous documentation excerpt
- `raw_diff_plus_signals`: raw diff plus docs plus extracted signal names
- `raw_diff_plus_summary`: raw diff plus docs plus generated summaries
- `full_current`: summary, signals, docs, changed files, and code diff

Use `raw_diff_plus_docs` as the primary fair thesis result. Treat `raw_diff_plus_signals` as assisted and `full_current` as an upper-bound setting because summaries and rule-derived signals can leak label semantics.

Scenario evaluation is split into positive and negative subsets. For practical DocGuard behavior, binary no-update detection and positive target/scenario accuracy matter most. Negative subtype labels are diagnostic, so reports also include grouped negative reason accuracy for a cleaner thesis discussion.

Run the input ablation and stress checks:

```bash
python -m docguard_hf_classifier.cli ablate-inputs --version v0_4 --model sentence-transformers/all-MiniLM-L6-v2
python -m docguard_hf_classifier.cli stress-test --version v0_4 --input-mode raw_diff_plus_docs
python -m docguard_hf_classifier.cli leakage-check --version v0_4 --input-mode raw_diff_plus_docs
python -m docguard_hf_classifier.cli analyze-negatives --version v0_4 --split test --input-mode raw_diff_plus_docs
```

Optional slower CPU experiments:

```bash
python -m docguard_hf_classifier.cli train-embeddings --version v0_4 --model microsoft/codebert-base --backend transformers
python -m docguard_hf_classifier.cli evaluate-zero-shot --version v0_4 --split validation --limit 20 --model facebook/bart-large-mnli
python -m docguard_hf_classifier.cli train-sequence --version v0_4 --task docs_update_required --base-model distilroberta-base --epochs 1 --limit-train 200 --limit-eval 100
```

The embedding classifier is preferred for CPU-first thesis experiments. CodeBERT, zero-shot, and full sequence fine-tuning are supported as optional comparison tracks. `qwen2_5_coder_0_5b` remains a real LLM inference proof rather than the main classifier.

## VS Code Extension MVP

DocGuard v0.5 adds a practical VS Code workflow:

- run DocGuard from the Command Palette, editor context menu, explorer context menu, or status bar
- analyze current git changes through the Python runtime
- show a bottom-panel patch preview when documentation should change
- apply documentation patches only after user confirmation
- fall back to the deterministic hybrid router if the HF model is unavailable

Train the recommended local classifier:

```bash
python -m docguard_hf_classifier.cli train-embeddings --version v0_4 --model sentence-transformers/all-MiniLM-L6-v2 --input-mode raw_diff_plus_docs --classifier-architecture staged
```

Run the Python runtime directly:

```bash
python -m docguard_runtime.runtime_cli analyze-workspace --workspace examples/vscode_demo --format json
```

Run the extension:

```bash
cd vscode-docguard
npm install
npm run compile
```

Then open `vscode-docguard` in VS Code and press `F5` to launch an Extension Development Host. For a hands-on demo, open `examples/vscode_demo`, make a small config or API change, and run `DocGuard: Analyze Workspace Changes`.

Use the short hybrid LLM prompt only for small CPU validation runs:

```powershell
$env:DOCGUARD_MAX_NEW_TOKENS="180"
python -m docguard_llm.cli evaluate --split validation --model qwen2_5_coder_0_5b --backend transformers_local --limit 10 --prompt-mode hybrid_compact --continue-on-error --retry-on-parse-error
```

`transformers_local` works on CPU but can be slow. The optional `llama_cpp` backend supports GGUF models through `llama-cpp-python` when installed and configured with `DOCGUARD_LLAMACPP_MODEL_PATH`; it is not required for default checks. The 0.5B model remains the default CPU proof model, while larger 1.5B/3B/7B evaluations are future GPU, Colab/Kaggle, vLLM/TGI, or quantized GGUF work.
