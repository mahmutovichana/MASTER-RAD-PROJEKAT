# Baseline Evaluation

- Dataset version used: v0.2
- Split evaluated: test

## Metric Table

| Metric | Value |
| --- | ---: |
| Records | 300 |
| docs_update_required precision | 93.10% |
| docs_update_required recall | 100.00% |
| docs_update_required F1 | 96.43% |
| scenario_type accuracy | 23.00% |
| known-scenario accuracy | 100.00% |
| unknown/unsupported scenario count | 231 |
| target_doc_file accuracy | 100.00% |
| patch fact coverage | 27.59% |
| false positives | 14 |
| false negatives | 0 |
| hallucination count | 0 |

## v0.1 vs v0.2 Comparison

| Metric | v0.1 value | v0.2 value | Interpretation |
| --- | ---: | ---: | --- |
| docs_update_required precision | 100.00% | 93.10% | Measures how often predicted documentation updates are correct. |
| docs_update_required recall | 100.00% | 100.00% | Drops if unsupported positive changes are missed. |
| docs_update_required F1 | 100.00% | 96.43% | Overall binary update-detection quality. |
| scenario_type accuracy | 100.00% | 23.00% | v0.2 includes unsupported scenario types, so this should be lower. |
| target_doc_file accuracy | 100.00% | 100.00% | All current records still target API docs. |
| patch fact coverage | 80.00% | 27.59% | Lower coverage shows the baseline cannot generate patches for many v0.2 changes. |
| false positives | 0 | 14 | Negative changes incorrectly flagged as doc updates. |
| false negatives | 0 | 0 | Positive changes missed by the baseline. |
| hallucination count | 0 | 0 | Unsupported changes should not trigger invented patches. |

## Per-Scenario Performance

| Scenario | Records | Correct | Accuracy |
| --- | ---: | ---: | ---: |
| `added_request_field` | 13 | 0 | 0.00% |
| `added_response_field` | 14 | 14 | 100.00% |
| `changed_auth_requirement` | 14 | 14 | 100.00% |
| `changed_endpoint_path` | 13 | 0 | 0.00% |
| `changed_enum_values` | 13 | 0 | 0.00% |
| `changed_error_response` | 14 | 0 | 0.00% |
| `changed_http_method` | 13 | 0 | 0.00% |
| `changed_status_code` | 14 | 0 | 0.00% |
| `changed_validation_max` | 13 | 0 | 0.00% |
| `changed_validation_min` | 14 | 14 | 100.00% |
| `comment_only_change` | 14 | 0 | 0.00% |
| `dependency_config_change` | 14 | 0 | 0.00% |
| `deprecated_endpoint` | 14 | 0 | 0.00% |
| `docs_already_updated` | 14 | 0 | 0.00% |
| `formatting_only` | 14 | 0 | 0.00% |
| `internal_refactor` | 13 | 13 | 100.00% |
| `internal_service_logic_no_api_change` | 14 | 0 | 0.00% |
| `new_endpoint` | 14 | 14 | 100.00% |
| `removed_endpoint` | 13 | 0 | 0.00% |
| `removed_request_field` | 13 | 0 | 0.00% |
| `rename_private_helper` | 14 | 0 | 0.00% |
| `test_only_change` | 14 | 0 | 0.00% |

## Interpretation

The deterministic baseline remains strong on v0.1-style scenarios, but v0.2 introduces many unsupported change types. Those examples are intentionally classified as `unknown_change`, which makes scenario accuracy lower and exposes where an NLP-assisted DocGuard agent should improve.

## Limitations

- The baseline relies on regex patterns and generated project conventions.
- Auth descriptions are inferred from middleware names, not business documentation.
- Generated patches are minimal and may not match the gold patch wording exactly.
- The baseline is not expected to generalize to arbitrary real-world projects without additional parsing and NLP support.
