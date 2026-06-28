# Dataset v0.4 Summary

DocGuard v0.4 is a CPU-first dataset version for hybrid documentation consistency experiments.

| Metric | Value |
| --- | ---: |
| Projects | 30 |
| Records | 6000 |
| Positive records | 3000 |
| Negative records | 3000 |
| Train records | 4200 |
| Validation records | 1000 |
| Test records | 800 |

## Documentation Categories

- `api_reference`: 1339
- `architecture_flow`: 312
- `changelog`: 103
- `configuration`: 312
- `developer_setup`: 208
- `model_contract`: 208
- `no_update`: 3000
- `testing_instructions`: 206
- `workflow_documentation`: 312

## Scenario Types

- `added_background_job_flow`: 104
- `added_dto_model_field`: 104
- `added_environment_variable`: 104
- `added_request_field`: 103
- `added_response_field`: 103
- `added_service_orchestration_flow`: 104
- `changed_auth_requirement`: 103
- `changed_background_job_schedule`: 104
- `changed_caching_or_rate_limit_flow`: 104
- `changed_default_config_value`: 104
- `changed_endpoint_path`: 103
- `changed_enum_values`: 103
- `changed_error_handling_flow`: 104
- `changed_http_method`: 103
- `changed_local_development_flow`: 104
- `changed_middleware_auth_flow`: 104
- `changed_seed_or_setup_flow`: 104
- `changed_status_code`: 103
- `changed_test_command`: 103
- `changed_testing_framework`: 103
- `changed_validation_max`: 103
- `changed_validation_min`: 103
- `changelog_worthy_behavior_change`: 103
- `comments_reworded_no_contract_change`: 231
- `config_refactor_no_new_env_var`: 231
- `dev_dependency_patch_no_command_change`: 231
- `docs_already_updated`: 231
- `formatting_only_in_docs_or_code`: 231
- `helper_extraction_no_behavior_change`: 230
- `internal_performance_refactor_no_documented_behavior_change`: 231
- `internal_variable_rename_no_behavior_change`: 231
- `log_message_change_no_user_visible_behavior`: 231
- `new_endpoint`: 103
- `private_helper_refactor_no_flow_change`: 231
- `removed_dto_model_field`: 104
- `removed_endpoint`: 103
- `removed_environment_variable`: 104
- `removed_request_field`: 103
- `removed_response_field`: 103
- `route_implementation_refactor_no_contract_change`: 230
- `test_assertion_refactor_no_behavior_change`: 231
- `type_alias_rename_no_contract_change`: 230

## v0.4 Design Notes

- Negative records use `doc_category=no_update` and empty target documentation fields.
- Positive fine-grained metrics are evaluated separately from negative binary classification.
- The dataset is balanced 50/50 for binary documentation-update detection.
- The intended baseline path is signal routing plus CPU ML, with small LLMs optional.
