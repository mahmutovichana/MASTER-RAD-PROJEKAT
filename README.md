# DocGuard Dataset Factory

Synthetic dataset factory for the MSc thesis project:

**Intelligent NLP Agent for Consistency Analysis of Software Projects**

DocGuard analyzes REST API code diffs, detects whether API documentation is missing or outdated, and proposes a precise documentation patch.

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
python -m docguard_llm.cli smoke-test --model qwen2_5_coder_0_5b --backend transformers_local --compact-prompt
```

Run local Transformers inference:

```bash
python -m docguard_llm.cli evaluate --split validation --model qwen2_5_coder_0_5b --backend transformers_local --limit 3 --compact-prompt --continue-on-error
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
python -m docguard_llm.cli smoke-test --model qwen2_5_coder_0_5b --backend transformers_local --compact-prompt --debug
```

```powershell
$env:DOCGUARD_MAX_NEW_TOKENS="120"
python -m docguard_llm.cli evaluate --split validation --model qwen2_5_coder_0_5b --backend transformers_local --limit 3 --compact-prompt --continue-on-error
```

Only after 0.5B works should you try 1.5B sanity-only:

```powershell
$env:DOCGUARD_MAX_NEW_TOKENS="60"
python -m docguard_llm.cli smoke-test --model qwen2_5_coder_1_5b --backend transformers_local --sanity-only --debug
```

The `smoke-test` command writes report checkpoints before generation starts, after prompt build, after generation starts, after generation finishes, and after parsing. Real `evaluate` writes each prediction to JSONL immediately, so partial outputs survive if a later CPU generation fails. The `--timeout-seconds` option is documented for run notes, but no hard Windows timeout is enforced around low-level model generation. Mock results are useful for validating the pipeline, but they are not real Hugging Face model quality.

## Current Split

Splits are project-level:

- train: 7 projects
- validation: 1 project
- test: 2 projects
