# Dataset v0.1 Summary

## Purpose

Dataset v0.1 is a controlled synthetic dataset for the first baseline evaluation of DocGuard, an agent that analyzes REST API code diffs, detects missing or outdated API documentation, and generates precise documentation patches.

## Current Scenario Types

- `new_endpoint`
- `changed_validation_min`
- `changed_auth_requirement`
- `added_response_field`
- `internal_refactor`

## Record Counts

- Total records: 1000
- Positive records: 800
- Negative records: 200

## Split Strategy

Splits are project-level to prevent leakage between training and evaluation:

- train: 7 projects, 700 records
- validation: 1 project, 100 records
- test: 2 projects, 200 records

## Known Limitations

- The dataset is synthetic and generated from template-based scenarios.
- Current v0.1 coverage is limited to 5 scenario types.
- Diffs are realistic enough for baseline evaluation, but they do not yet represent all API evolution patterns.
- Gold patches are intentionally minimal and do not model full human documentation style.
- Automatic validation checks consistency, but human audit is still required for quality judgment.

## Next Planned Improvements

- Add the remaining positive and negative scenario types.
- Increase project and module diversity.
- Add deeper grounding checks between `code_diff`, `expected_facts`, and `gold_doc_patch`.
- Run manual audit and correct any low-quality examples.
- Compare the rule-based baseline against an NLP-assisted DocGuard agent.
