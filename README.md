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
