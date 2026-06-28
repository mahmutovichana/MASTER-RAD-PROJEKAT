# HF Embedding Error Analysis v0.4

Split: `validation`
Input mode: `raw_diff_plus_docs`
F1: `1.0000`

## Most Confused Scenario Pairs

- `log_message_change_no_user_visible_behavior` -> `helper_extraction_no_behavior_change`: 24
- `internal_performance_refactor_no_documented_behavior_change` -> `helper_extraction_no_behavior_change`: 22
- `comments_reworded_no_contract_change` -> `helper_extraction_no_behavior_change`: 20
- `formatting_only_in_docs_or_code` -> `helper_extraction_no_behavior_change`: 17
- `private_helper_refactor_no_flow_change` -> `helper_extraction_no_behavior_change`: 17
- `internal_variable_rename_no_behavior_change` -> `helper_extraction_no_behavior_change`: 15
- `internal_variable_rename_no_behavior_change` -> `internal_performance_refactor_no_documented_behavior_change`: 9
- `internal_performance_refactor_no_documented_behavior_change` -> `internal_variable_rename_no_behavior_change`: 8
- `helper_extraction_no_behavior_change` -> `comments_reworded_no_contract_change`: 7
- `internal_variable_rename_no_behavior_change` -> `comments_reworded_no_contract_change`: 7
- `private_helper_refactor_no_flow_change` -> `comments_reworded_no_contract_change`: 7
- `formatting_only_in_docs_or_code` -> `internal_performance_refactor_no_documented_behavior_change`: 7
- `log_message_change_no_user_visible_behavior` -> `internal_variable_rename_no_behavior_change`: 7
- `private_helper_refactor_no_flow_change` -> `internal_performance_refactor_no_documented_behavior_change`: 7
- `helper_extraction_no_behavior_change` -> `internal_performance_refactor_no_documented_behavior_change`: 7
- `formatting_only_in_docs_or_code` -> `comments_reworded_no_contract_change`: 6
- `comments_reworded_no_contract_change` -> `internal_variable_rename_no_behavior_change`: 6
- `private_helper_refactor_no_flow_change` -> `internal_variable_rename_no_behavior_change`: 6
- `formatting_only_in_docs_or_code` -> `internal_variable_rename_no_behavior_change`: 6
- `comments_reworded_no_contract_change` -> `internal_performance_refactor_no_documented_behavior_change`: 6

## Most Confused Doc Categories


## HF Disagrees With Router

docguard-v04-project-22-api-004, docguard-v04-project-22-api-006, docguard-v04-project-22-api-008, docguard-v04-project-22-api-010, docguard-v04-project-22-api-012, docguard-v04-project-22-api-014, docguard-v04-project-22-api-016, docguard-v04-project-22-api-018, docguard-v04-project-22-api-022, docguard-v04-project-22-api-024, docguard-v04-project-22-api-026, docguard-v04-project-22-api-030, docguard-v04-project-22-api-032, docguard-v04-project-22-api-034, docguard-v04-project-22-api-038, docguard-v04-project-22-api-040, docguard-v04-project-22-api-042, docguard-v04-project-22-api-043, docguard-v04-project-22-api-044, docguard-v04-project-22-api-046

## HF Correct, Router Wrong

docguard-v04-project-22-api-004, docguard-v04-project-22-api-006, docguard-v04-project-22-api-008, docguard-v04-project-22-api-012, docguard-v04-project-22-api-022, docguard-v04-project-22-api-024, docguard-v04-project-22-api-030, docguard-v04-project-22-api-032, docguard-v04-project-22-api-034, docguard-v04-project-22-api-038, docguard-v04-project-22-api-043, docguard-v04-project-22-api-046, docguard-v04-project-22-api-048, docguard-v04-project-22-api-050, docguard-v04-project-22-api-056, docguard-v04-project-22-api-058, docguard-v04-project-22-api-060, docguard-v04-project-22-api-064, docguard-v04-project-22-api-072, docguard-v04-project-22-api-074

## Router Correct, HF Wrong

docguard-v04-project-22-api-014, docguard-v04-project-22-api-040, docguard-v04-project-22-api-066, docguard-v04-project-22-api-092, docguard-v04-project-22-api-144, docguard-v04-project-22-api-170, docguard-v04-project-22-api-196, docguard-v04-project-23-api-022, docguard-v04-project-23-api-048, docguard-v04-project-23-api-074, docguard-v04-project-23-api-100, docguard-v04-project-23-api-126, docguard-v04-project-23-api-152, docguard-v04-project-23-api-178, docguard-v04-project-24-api-004, docguard-v04-project-24-api-030, docguard-v04-project-24-api-056, docguard-v04-project-24-api-108, docguard-v04-project-24-api-134, docguard-v04-project-24-api-186
