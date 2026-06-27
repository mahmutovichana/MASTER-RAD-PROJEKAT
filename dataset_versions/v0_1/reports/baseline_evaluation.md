# Baseline Evaluation

- Dataset version used: v0.1
- Split evaluated: test

## Metric Table

| Metric | Value |
| --- | ---: |
| Records | 200 |
| docs_update_required precision | 100.00% |
| docs_update_required recall | 100.00% |
| docs_update_required F1 | 100.00% |
| scenario_type accuracy | 100.00% |
| target_doc_file accuracy | 100.00% |
| patch fact coverage | 80.00% |
| false positives | 0 |
| false negatives | 0 |
| hallucination count | 0 |

## Per-Scenario Performance

| Scenario | Records | Correct | Accuracy |
| --- | ---: | ---: | ---: |
| `added_response_field` | 40 | 40 | 100.00% |
| `changed_auth_requirement` | 40 | 40 | 100.00% |
| `changed_validation_min` | 40 | 40 | 100.00% |
| `internal_refactor` | 40 | 40 | 100.00% |
| `new_endpoint` | 40 | 40 | 100.00% |

## Interpretation

This deterministic baseline performs well on the current template-generated v0.1 scenarios because the diffs contain regular route, schema, repository, and service patterns. Patch fact coverage is intentionally stricter than classification and highlights facts that are not fully recoverable from code diffs alone.

## Limitations

- The baseline relies on regex patterns and generated project conventions.
- Auth descriptions are inferred from middleware names, not business documentation.
- Generated patches are minimal and may not match the gold patch wording exactly.
- The baseline is not expected to generalize to arbitrary real-world projects without additional parsing and NLP support.
