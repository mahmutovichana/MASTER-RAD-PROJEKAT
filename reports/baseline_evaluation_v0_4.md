# Baseline Evaluation

- Dataset version used: v0.4
- Split evaluated: test

## Metric Table

| Metric | Value |
| --- | ---: |
| Records | 800 |
| docs_update_required precision | 0.00% |
| docs_update_required recall | 0.00% |
| docs_update_required F1 | 0.00% |
| scenario_type accuracy | 0.00% |
| known-scenario accuracy | 0.00% |
| unknown/unsupported scenario count | 800 |
| doc_category accuracy | 0.00% |
| target_doc_file accuracy | 22.38% |
| patch fact coverage | 0.00% |
| false positives | 0 |
| false negatives | 400 |
| hallucination count | 0 |

## v0.1 vs v0.4 Comparison

| Metric | v0.1 value | v0.4 value | Interpretation |
| --- | ---: | ---: | --- |
| docs_update_required precision | 100.00% | 0.00% | Measures how often predicted documentation updates are correct. |
| docs_update_required recall | 100.00% | 0.00% | Drops if unsupported positive changes are missed. |
| docs_update_required F1 | 100.00% | 0.00% | Overall binary update-detection quality. |
| scenario_type accuracy | 100.00% | 0.00% | v0.4 includes unsupported scenario types, so this should be lower. |
| target_doc_file accuracy | 100.00% | 22.38% | All current records still target API docs. |
| patch fact coverage | 80.00% | 0.00% | Lower coverage shows the baseline cannot generate patches for many v0.4 changes. |
| false positives | 0 | 0 | Negative changes incorrectly flagged as doc updates. |
| false negatives | 0 | 400 | Positive changes missed by the baseline. |
| hallucination count | 0 | 0 | Unsupported changes should not trigger invented patches. |

## Per-Scenario Performance

| Scenario | Records | Correct | Accuracy |
| --- | ---: | ---: | ---: |
| `added_background_job_flow` | 14 | 0 | 0.00% |
| `added_dto_model_field` | 14 | 0 | 0.00% |
| `added_environment_variable` | 14 | 0 | 0.00% |
| `added_request_field` | 14 | 0 | 0.00% |
| `added_response_field` | 14 | 0 | 0.00% |
| `added_service_orchestration_flow` | 14 | 0 | 0.00% |
| `changed_auth_requirement` | 14 | 0 | 0.00% |
| `changed_background_job_schedule` | 14 | 0 | 0.00% |
| `changed_caching_or_rate_limit_flow` | 14 | 0 | 0.00% |
| `changed_default_config_value` | 14 | 0 | 0.00% |
| `changed_endpoint_path` | 14 | 0 | 0.00% |
| `changed_enum_values` | 13 | 0 | 0.00% |
| `changed_error_handling_flow` | 14 | 0 | 0.00% |
| `changed_http_method` | 14 | 0 | 0.00% |
| `changed_local_development_flow` | 14 | 0 | 0.00% |
| `changed_middleware_auth_flow` | 14 | 0 | 0.00% |
| `changed_seed_or_setup_flow` | 14 | 0 | 0.00% |
| `changed_status_code` | 14 | 0 | 0.00% |
| `changed_test_command` | 13 | 0 | 0.00% |
| `changed_testing_framework` | 13 | 0 | 0.00% |
| `changed_validation_max` | 13 | 0 | 0.00% |
| `changed_validation_min` | 13 | 0 | 0.00% |
| `changelog_worthy_behavior_change` | 13 | 0 | 0.00% |
| `comments_reworded_no_contract_change` | 31 | 0 | 0.00% |
| `config_refactor_no_new_env_var` | 31 | 0 | 0.00% |
| `dev_dependency_patch_no_command_change` | 31 | 0 | 0.00% |
| `docs_already_updated` | 31 | 0 | 0.00% |
| `formatting_only_in_docs_or_code` | 31 | 0 | 0.00% |
| `helper_extraction_no_behavior_change` | 30 | 0 | 0.00% |
| `internal_performance_refactor_no_documented_behavior_change` | 31 | 0 | 0.00% |
| `internal_variable_rename_no_behavior_change` | 31 | 0 | 0.00% |
| `log_message_change_no_user_visible_behavior` | 31 | 0 | 0.00% |
| `new_endpoint` | 14 | 0 | 0.00% |
| `private_helper_refactor_no_flow_change` | 31 | 0 | 0.00% |
| `removed_dto_model_field` | 14 | 0 | 0.00% |
| `removed_endpoint` | 14 | 0 | 0.00% |
| `removed_environment_variable` | 14 | 0 | 0.00% |
| `removed_request_field` | 14 | 0 | 0.00% |
| `removed_response_field` | 14 | 0 | 0.00% |
| `route_implementation_refactor_no_contract_change` | 30 | 0 | 0.00% |
| `test_assertion_refactor_no_behavior_change` | 31 | 0 | 0.00% |
| `type_alias_rename_no_contract_change` | 30 | 0 | 0.00% |

## Per-Doc-Category Performance

| Category | Records | Correct | Accuracy |
| --- | ---: | ---: | ---: |
| `api_reference` | 179 | 0 | 0.00% |
| `architecture_flow` | 42 | 0 | 0.00% |
| `changelog` | 13 | 0 | 0.00% |
| `configuration` | 42 | 0 | 0.00% |
| `developer_setup` | 28 | 0 | 0.00% |
| `model_contract` | 28 | 0 | 0.00% |
| `no_update` | 400 | 0 | 0.00% |
| `testing_instructions` | 26 | 0 | 0.00% |
| `workflow_documentation` | 42 | 0 | 0.00% |

## Interpretation

The deterministic baseline remains strong on v0.1-style scenarios, but v0.4 introduces many unsupported high-level documentation change types. Those examples are intentionally classified as `unknown_change`, which makes scenario and doc-category accuracy lower and exposes where an NLP-assisted DocGuard agent should improve.

## Limitations

- The baseline relies on regex patterns and generated project conventions.
- Auth descriptions are inferred from middleware names, not business documentation.
- Generated patches are minimal and may not match the gold patch wording exactly.
- The baseline is not expected to generalize to arbitrary real-world projects without additional parsing and NLP support.
