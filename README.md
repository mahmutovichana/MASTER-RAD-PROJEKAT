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

The LLM-assisted prototype lives in `docguard_llm/`. It performs inference only; no fine-tuning is done in this phase.

Supported model keys:

- `qwen2_5_coder_7b`: `Qwen/Qwen2.5-Coder-7B-Instruct`
- `deepseek_coder_6_7b`: `deepseek-ai/deepseek-coder-6.7b-instruct`
- `qwen2_5_coder_3b`: `Qwen/Qwen2.5-Coder-3B-Instruct`

List models:

```bash
python -m docguard_llm.cli list-models
```

Run a mock evaluation without downloading models:

```bash
python -m docguard_llm.cli evaluate --split validation --model qwen2_5_coder_7b --backend mock --limit 20
python -m docguard_llm.cli compare --split validation --backend mock --limit 20
```

Run local Transformers inference:

```bash
python -m docguard_llm.cli evaluate --split test --model qwen2_5_coder_7b --backend transformers_local
```

Run against a local vLLM/TGI OpenAI-compatible server:

```bash
$env:DOCGUARD_TGI_BASE_URL="http://localhost:8000/v1"
python -m docguard_llm.cli evaluate --split test --model qwen2_5_coder_7b --backend text_generation_inference
```

The 7B models may require a GPU, quantization, or a local serving setup. Use `qwen2_5_coder_3b` for a smaller local comparison.

## Current Split

Splits are project-level:

- train: 7 projects
- validation: 1 project
- test: 2 projects
