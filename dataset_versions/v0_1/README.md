# DocGuard Dataset v0.1 Snapshot

This folder preserves the frozen v0.1 dataset and baseline outputs for thesis traceability.

## Purpose

Dataset v0.1 is a controlled synthetic dataset used for the first baseline evaluation of DocGuard, an agent that analyzes REST API code diffs, detects missing or outdated API documentation, and generates minimal documentation patches.

## Contents

- Projects: 10 synthetic TypeScript + Express REST API projects
- Records: 1000
- Scenario types:
  - `new_endpoint`
  - `changed_validation_min`
  - `changed_auth_requirement`
  - `added_response_field`
  - `internal_refactor`

## Split Strategy

Splits are project-level:

- train: 7 projects, 700 records
- validation: 1 project, 100 records
- test: 2 projects, 200 records

## Baseline Result Summary

The rule-based baseline achieved on v0.1 test:

- docs_update_required precision/recall/F1: 100%
- scenario_type accuracy: 100%
- target_doc_file accuracy: 100%
- patch fact coverage: 80%
- hallucination count: 0

## Known Limitation

The v0.1 diffs are regular and template-generated, which makes the rule-based baseline too strong. This snapshot is preserved as a transparent first baseline, not as a final benchmark.
