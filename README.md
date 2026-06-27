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
  validate_dataset.py
reports/
  dataset_statistics.md
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

## Current Split

Splits are project-level:

- train: 7 projects
- validation: 1 project
- test: 2 projects
