# Baseline Evaluation

- Dataset version used: v0.3
- Split evaluated: test

## Metric Table

| Metric | Value |
| --- | ---: |
| Records | 500 |
| docs_update_required precision | 100.00% |
| docs_update_required recall | 54.22% |
| docs_update_required F1 | 70.32% |
| scenario_type accuracy | 7.20% |
| known-scenario accuracy | 60.00% |
| unknown/unsupported scenario count | 464 |
| doc_category accuracy | 7.20% |
| target_doc_file accuracy | 33.60% |
| patch fact coverage | 11.69% |
| false positives | 0 |
| false negatives | 141 |
| hallucination count | 0 |

## v0.1 vs v0.3 Comparison

| Metric | v0.1 value | v0.3 value | Interpretation |
| --- | ---: | ---: | --- |
| docs_update_required precision | 100.00% | 100.00% | Measures how often predicted documentation updates are correct. |
| docs_update_required recall | 100.00% | 54.22% | Drops if unsupported positive changes are missed. |
| docs_update_required F1 | 100.00% | 70.32% | Overall binary update-detection quality. |
| scenario_type accuracy | 100.00% | 7.20% | v0.3 includes unsupported scenario types, so this should be lower. |
| target_doc_file accuracy | 100.00% | 33.60% | All current records still target API docs. |
| patch fact coverage | 80.00% | 11.69% | Lower coverage shows the baseline cannot generate patches for many v0.3 changes. |
| false positives | 0 | 0 | Negative changes incorrectly flagged as doc updates. |
| false negatives | 0 | 141 | Positive changes missed by the baseline. |
| hallucination count | 0 | 0 | Unsupported changes should not trigger invented patches. |

## Per-Scenario Performance

| Scenario | Records | Correct | Accuracy |
| --- | ---: | ---: | ---: |
| `added_background_job_flow` | 12 | 0 | 0.00% |
| `added_dto_model` | 11 | 0 | 0.00% |
| `added_environment_variable` | 12 | 0 | 0.00% |
| `added_middleware_flow` | 11 | 0 | 0.00% |
| `added_request_field` | 12 | 0 | 0.00% |
| `added_response_field` | 12 | 0 | 0.00% |
| `added_service_orchestration_flow` | 12 | 0 | 0.00% |
| `changed_auth_flow` | 11 | 0 | 0.00% |
| `changed_auth_requirement` | 12 | 12 | 100.00% |
| `changed_caching_or_rate_limit_flow` | 12 | 0 | 0.00% |
| `changed_dto_field_semantics` | 11 | 0 | 0.00% |
| `changed_endpoint_path` | 12 | 0 | 0.00% |
| `changed_enum_values` | 12 | 0 | 0.00% |
| `changed_error_handling_flow` | 12 | 0 | 0.00% |
| `changed_error_response` | 12 | 0 | 0.00% |
| `changed_http_method` | 12 | 0 | 0.00% |
| `changed_local_development_flow` | 12 | 0 | 0.00% |
| `changed_run_command` | 12 | 0 | 0.00% |
| `changed_status_code` | 12 | 0 | 0.00% |
| `changed_test_command` | 12 | 0 | 0.00% |
| `changed_validation_max` | 12 | 0 | 0.00% |
| `changed_validation_min` | 12 | 12 | 100.00% |
| `comment_only_change` | 12 | 0 | 0.00% |
| `comments_reworded_no_contract_change` | 12 | 0 | 0.00% |
| `dependency_config_change` | 12 | 0 | 0.00% |
| `deprecated_endpoint` | 12 | 0 | 0.00% |
| `dev_dependency_patch_no_command_change` | 12 | 0 | 0.00% |
| `docs_already_updated` | 12 | 0 | 0.00% |
| `formatting_only` | 12 | 0 | 0.00% |
| `formatting_only_in_docs_or_code` | 12 | 0 | 0.00% |
| `internal_performance_refactor_no_documented_behavior_change` | 12 | 0 | 0.00% |
| `internal_refactor` | 12 | 0 | 0.00% |
| `internal_service_logic_no_api_change` | 12 | 0 | 0.00% |
| `internal_variable_rename_no_behavior_change` | 12 | 0 | 0.00% |
| `log_message_change_no_user_visible_behavior` | 12 | 0 | 0.00% |
| `new_endpoint` | 12 | 12 | 100.00% |
| `private_helper_refactor_no_flow_change` | 12 | 0 | 0.00% |
| `removed_endpoint` | 12 | 0 | 0.00% |
| `removed_request_field` | 12 | 0 | 0.00% |
| `rename_private_helper` | 12 | 0 | 0.00% |
| `test_assertion_refactor_no_behavior_change` | 12 | 0 | 0.00% |
| `test_only_change` | 12 | 0 | 0.00% |

## Per-Doc-Category Performance

| Category | Records | Correct | Accuracy |
| --- | ---: | ---: | ---: |
| `api_reference` | 168 | 36 | 21.43% |
| `architecture_flow` | 46 | 0 | 0.00% |
| `configuration` | 12 | 0 | 0.00% |
| `developer_setup` | 24 | 0 | 0.00% |
| `model_contract` | 22 | 0 | 0.00% |
| `testing_instructions` | 12 | 0 | 0.00% |
| `workflow_documentation` | 216 | 0 | 0.00% |

## Interpretation

The deterministic baseline remains strong on v0.1-style scenarios, but v0.3 introduces many unsupported high-level documentation change types. Those examples are intentionally classified as `unknown_change`, which makes scenario and doc-category accuracy lower and exposes where an NLP-assisted DocGuard agent should improve.

## Limitations

- The baseline relies on regex patterns and generated project conventions.
- Auth descriptions are inferred from middleware names, not business documentation.
- Generated patches are minimal and may not match the gold patch wording exactly.
- The baseline is not expected to generalize to arbitrary real-world projects without additional parsing and NLP support.
