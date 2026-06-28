# Dataset Split Leakage Check v0.4

Input mode: `raw_diff_plus_docs`

## Project ID Overlap

- `train_validation`: 0 overlap(s)
- `train_test`: 0 overlap(s)
- `validation_test`: 0 overlap(s)

## Near-Duplicate Input Text Hashes Across Splits

None found.

## Repeated Code Diff Template Hashes Across Splits

None found.

## Scenario Distribution Per Split

### train
- `added_background_job_flow`: 73
- `added_dto_model_field`: 73
- `added_environment_variable`: 73
- `added_request_field`: 72
- `added_response_field`: 72
- `added_service_orchestration_flow`: 73
- `changed_auth_requirement`: 72
- `changed_background_job_schedule`: 73
- `changed_caching_or_rate_limit_flow`: 73
- `changed_default_config_value`: 73
- `changed_endpoint_path`: 72
- `changed_enum_values`: 72
- `changed_error_handling_flow`: 73
- `changed_http_method`: 72
- `changed_local_development_flow`: 73
- `changed_middleware_auth_flow`: 73
- `changed_seed_or_setup_flow`: 73
- `changed_status_code`: 72
- `changed_test_command`: 72
- `changed_testing_framework`: 72
- `changed_validation_max`: 72
- `changed_validation_min`: 72
- `changelog_worthy_behavior_change`: 72
- `comments_reworded_no_contract_change`: 162
- `config_refactor_no_new_env_var`: 161
- `dev_dependency_patch_no_command_change`: 162
- `docs_already_updated`: 161
- `formatting_only_in_docs_or_code`: 162
- `helper_extraction_no_behavior_change`: 161
- `internal_performance_refactor_no_documented_behavior_change`: 161
- `internal_variable_rename_no_behavior_change`: 162
- `log_message_change_no_user_visible_behavior`: 162
- `new_endpoint`: 72
- `private_helper_refactor_no_flow_change`: 162
- `removed_dto_model_field`: 72
- `removed_endpoint`: 72
- `removed_environment_variable`: 73
- `removed_request_field`: 72
- `removed_response_field`: 72
- `route_implementation_refactor_no_contract_change`: 161
- `test_assertion_refactor_no_behavior_change`: 162
- `type_alias_rename_no_contract_change`: 161
### validation
- `added_background_job_flow`: 17
- `added_dto_model_field`: 17
- `added_environment_variable`: 17
- `added_request_field`: 17
- `added_response_field`: 17
- `added_service_orchestration_flow`: 17
- `changed_auth_requirement`: 17
- `changed_background_job_schedule`: 17
- `changed_caching_or_rate_limit_flow`: 17
- `changed_default_config_value`: 17
- `changed_endpoint_path`: 17
- `changed_enum_values`: 18
- `changed_error_handling_flow`: 17
- `changed_http_method`: 17
- `changed_local_development_flow`: 17
- `changed_middleware_auth_flow`: 17
- `changed_seed_or_setup_flow`: 17
- `changed_status_code`: 17
- `changed_test_command`: 18
- `changed_testing_framework`: 18
- `changed_validation_max`: 18
- `changed_validation_min`: 18
- `changelog_worthy_behavior_change`: 18
- `comments_reworded_no_contract_change`: 38
- `config_refactor_no_new_env_var`: 39
- `dev_dependency_patch_no_command_change`: 38
- `docs_already_updated`: 39
- `formatting_only_in_docs_or_code`: 38
- `helper_extraction_no_behavior_change`: 39
- `internal_performance_refactor_no_documented_behavior_change`: 39
- `internal_variable_rename_no_behavior_change`: 38
- `log_message_change_no_user_visible_behavior`: 38
- `new_endpoint`: 17
- `private_helper_refactor_no_flow_change`: 38
- `removed_dto_model_field`: 18
- `removed_endpoint`: 17
- `removed_environment_variable`: 17
- `removed_request_field`: 17
- `removed_response_field`: 17
- `route_implementation_refactor_no_contract_change`: 39
- `test_assertion_refactor_no_behavior_change`: 38
- `type_alias_rename_no_contract_change`: 39
### test
- `added_background_job_flow`: 14
- `added_dto_model_field`: 14
- `added_environment_variable`: 14
- `added_request_field`: 14
- `added_response_field`: 14
- `added_service_orchestration_flow`: 14
- `changed_auth_requirement`: 14
- `changed_background_job_schedule`: 14
- `changed_caching_or_rate_limit_flow`: 14
- `changed_default_config_value`: 14
- `changed_endpoint_path`: 14
- `changed_enum_values`: 13
- `changed_error_handling_flow`: 14
- `changed_http_method`: 14
- `changed_local_development_flow`: 14
- `changed_middleware_auth_flow`: 14
- `changed_seed_or_setup_flow`: 14
- `changed_status_code`: 14
- `changed_test_command`: 13
- `changed_testing_framework`: 13
- `changed_validation_max`: 13
- `changed_validation_min`: 13
- `changelog_worthy_behavior_change`: 13
- `comments_reworded_no_contract_change`: 31
- `config_refactor_no_new_env_var`: 31
- `dev_dependency_patch_no_command_change`: 31
- `docs_already_updated`: 31
- `formatting_only_in_docs_or_code`: 31
- `helper_extraction_no_behavior_change`: 30
- `internal_performance_refactor_no_documented_behavior_change`: 31
- `internal_variable_rename_no_behavior_change`: 31
- `log_message_change_no_user_visible_behavior`: 31
- `new_endpoint`: 14
- `private_helper_refactor_no_flow_change`: 31
- `removed_dto_model_field`: 14
- `removed_endpoint`: 14
- `removed_environment_variable`: 14
- `removed_request_field`: 14
- `removed_response_field`: 14
- `route_implementation_refactor_no_contract_change`: 30
- `test_assertion_refactor_no_behavior_change`: 31
- `type_alias_rename_no_contract_change`: 30

## Project Distribution Per Split

### train
- `docguard-v04-project-01-api`: 200
- `docguard-v04-project-02-api`: 200
- `docguard-v04-project-03-api`: 200
- `docguard-v04-project-04-api`: 200
- `docguard-v04-project-05-api`: 200
- `docguard-v04-project-06-api`: 200
- `docguard-v04-project-07-api`: 200
- `docguard-v04-project-08-api`: 200
- `docguard-v04-project-09-api`: 200
- `docguard-v04-project-10-api`: 200
- `docguard-v04-project-11-api`: 200
- `docguard-v04-project-12-api`: 200
- `docguard-v04-project-13-api`: 200
- `docguard-v04-project-14-api`: 200
- `docguard-v04-project-15-api`: 200
- `docguard-v04-project-16-api`: 200
- `docguard-v04-project-17-api`: 200
- `docguard-v04-project-18-api`: 200
- `docguard-v04-project-19-api`: 200
- `docguard-v04-project-20-api`: 200
- `docguard-v04-project-21-api`: 200
### validation
- `docguard-v04-project-22-api`: 200
- `docguard-v04-project-23-api`: 200
- `docguard-v04-project-24-api`: 200
- `docguard-v04-project-25-api`: 200
- `docguard-v04-project-26-api`: 200
### test
- `docguard-v04-project-27-api`: 200
- `docguard-v04-project-28-api`: 200
- `docguard-v04-project-29-api`: 200
- `docguard-v04-project-30-api`: 200
