# HF Negative Subtype Error Analysis v0.4

Input mode: `raw_diff_plus_docs`
Split: `test`
Classifier architecture: `staged`

Negative subtype errors are less severe than false positives or false negatives when binary classification is correct, because the system still correctly predicts that no documentation update is required. They are diagnostic labels for analysis, not patch-generation targets.

## Negative Scenario Subtype Accuracy

| Subtype | Support | Correct | Accuracy |
| --- | ---: | ---: | ---: |
| `comments_reworded_no_contract_change` | 31 | 2 | 0.0645 |
| `config_refactor_no_new_env_var` | 31 | 31 | 1.0000 |
| `dev_dependency_patch_no_command_change` | 31 | 31 | 1.0000 |
| `docs_already_updated` | 31 | 31 | 1.0000 |
| `formatting_only_in_docs_or_code` | 31 | 0 | 0.0000 |
| `helper_extraction_no_behavior_change` | 30 | 5 | 0.1667 |
| `internal_performance_refactor_no_documented_behavior_change` | 31 | 8 | 0.2581 |
| `internal_variable_rename_no_behavior_change` | 31 | 8 | 0.2581 |
| `log_message_change_no_user_visible_behavior` | 31 | 2 | 0.0645 |
| `private_helper_refactor_no_flow_change` | 31 | 1 | 0.0323 |
| `route_implementation_refactor_no_contract_change` | 30 | 30 | 1.0000 |
| `test_assertion_refactor_no_behavior_change` | 31 | 31 | 1.0000 |
| `type_alias_rename_no_contract_change` | 30 | 30 | 1.0000 |

## Negative Reason Group Accuracy

| Group | Support | Correct | Accuracy |
| --- | ---: | ---: | ---: |
| `dependency_or_config_no_doc_impact` | 62 | 62 | 1.0000 |
| `docs_already_consistent` | 31 | 31 | 1.0000 |
| `no_behavior_change_refactor` | 153 | 131 | 0.8562 |
| `no_contract_change_textual` | 93 | 12 | 0.1290 |
| `route_internal_no_contract_change` | 30 | 30 | 1.0000 |
| `test_only_no_product_behavior` | 31 | 31 | 1.0000 |

## Top Confused Negative Subtype Pairs

- `formatting_only_in_docs_or_code` -> `internal_performance_refactor_no_documented_behavior_change`: 13 (41.9% of `formatting_only_in_docs_or_code`)
- `comments_reworded_no_contract_change` -> `internal_variable_rename_no_behavior_change`: 11 (35.5% of `comments_reworded_no_contract_change`)
- `helper_extraction_no_behavior_change` -> `internal_performance_refactor_no_documented_behavior_change`: 10 (33.3% of `helper_extraction_no_behavior_change`)
- `private_helper_refactor_no_flow_change` -> `helper_extraction_no_behavior_change`: 10 (32.3% of `private_helper_refactor_no_flow_change`)
- `comments_reworded_no_contract_change` -> `internal_performance_refactor_no_documented_behavior_change`: 10 (32.3% of `comments_reworded_no_contract_change`)
- `log_message_change_no_user_visible_behavior` -> `internal_variable_rename_no_behavior_change`: 10 (32.3% of `log_message_change_no_user_visible_behavior`)
- `internal_variable_rename_no_behavior_change` -> `internal_performance_refactor_no_documented_behavior_change`: 9 (29.0% of `internal_variable_rename_no_behavior_change`)
- `internal_variable_rename_no_behavior_change` -> `helper_extraction_no_behavior_change`: 9 (29.0% of `internal_variable_rename_no_behavior_change`)
- `log_message_change_no_user_visible_behavior` -> `helper_extraction_no_behavior_change`: 9 (29.0% of `log_message_change_no_user_visible_behavior`)
- `internal_performance_refactor_no_documented_behavior_change` -> `internal_variable_rename_no_behavior_change`: 9 (29.0% of `internal_performance_refactor_no_documented_behavior_change`)
- `private_helper_refactor_no_flow_change` -> `internal_variable_rename_no_behavior_change`: 8 (25.8% of `private_helper_refactor_no_flow_change`)
- `formatting_only_in_docs_or_code` -> `internal_variable_rename_no_behavior_change`: 8 (25.8% of `formatting_only_in_docs_or_code`)
- `log_message_change_no_user_visible_behavior` -> `internal_performance_refactor_no_documented_behavior_change`: 8 (25.8% of `log_message_change_no_user_visible_behavior`)
- `private_helper_refactor_no_flow_change` -> `internal_performance_refactor_no_documented_behavior_change`: 8 (25.8% of `private_helper_refactor_no_flow_change`)
- `helper_extraction_no_behavior_change` -> `internal_variable_rename_no_behavior_change`: 8 (26.7% of `helper_extraction_no_behavior_change`)
- `formatting_only_in_docs_or_code` -> `helper_extraction_no_behavior_change`: 7 (22.6% of `formatting_only_in_docs_or_code`)
- `internal_performance_refactor_no_documented_behavior_change` -> `helper_extraction_no_behavior_change`: 7 (22.6% of `internal_performance_refactor_no_documented_behavior_change`)
- `comments_reworded_no_contract_change` -> `helper_extraction_no_behavior_change`: 5 (16.1% of `comments_reworded_no_contract_change`)
- `helper_extraction_no_behavior_change` -> `comments_reworded_no_contract_change`: 5 (16.7% of `helper_extraction_no_behavior_change`)
- `internal_performance_refactor_no_documented_behavior_change` -> `comments_reworded_no_contract_change`: 5 (16.1% of `internal_performance_refactor_no_documented_behavior_change`)

## Binary Correct, Subtype Wrong Examples

| Record | Gold subtype | Predicted subtype | Gold group | Predicted group |
| --- | --- | --- | --- | --- |
| `docguard-v04-project-27-api-004` | `private_helper_refactor_no_flow_change` | `internal_variable_rename_no_behavior_change` | `no_behavior_change_refactor` | `no_behavior_change_refactor` |
| `docguard-v04-project-27-api-006` | `formatting_only_in_docs_or_code` | `internal_variable_rename_no_behavior_change` | `no_contract_change_textual` | `no_behavior_change_refactor` |
| `docguard-v04-project-27-api-008` | `comments_reworded_no_contract_change` | `internal_variable_rename_no_behavior_change` | `no_contract_change_textual` | `no_behavior_change_refactor` |
| `docguard-v04-project-27-api-014` | `log_message_change_no_user_visible_behavior` | `internal_performance_refactor_no_documented_behavior_change` | `no_contract_change_textual` | `no_behavior_change_refactor` |
| `docguard-v04-project-27-api-024` | `helper_extraction_no_behavior_change` | `internal_performance_refactor_no_documented_behavior_change` | `no_behavior_change_refactor` | `no_behavior_change_refactor` |
| `docguard-v04-project-27-api-028` | `internal_variable_rename_no_behavior_change` | `internal_performance_refactor_no_documented_behavior_change` | `no_behavior_change_refactor` | `no_behavior_change_refactor` |
| `docguard-v04-project-27-api-030` | `private_helper_refactor_no_flow_change` | `helper_extraction_no_behavior_change` | `no_behavior_change_refactor` | `no_behavior_change_refactor` |
| `docguard-v04-project-27-api-032` | `formatting_only_in_docs_or_code` | `internal_variable_rename_no_behavior_change` | `no_contract_change_textual` | `no_behavior_change_refactor` |
| `docguard-v04-project-27-api-034` | `comments_reworded_no_contract_change` | `internal_performance_refactor_no_documented_behavior_change` | `no_contract_change_textual` | `no_behavior_change_refactor` |
| `docguard-v04-project-27-api-040` | `log_message_change_no_user_visible_behavior` | `internal_performance_refactor_no_documented_behavior_change` | `no_contract_change_textual` | `no_behavior_change_refactor` |
| `docguard-v04-project-27-api-050` | `helper_extraction_no_behavior_change` | `private_helper_refactor_no_flow_change` | `no_behavior_change_refactor` | `no_behavior_change_refactor` |
| `docguard-v04-project-27-api-054` | `internal_variable_rename_no_behavior_change` | `helper_extraction_no_behavior_change` | `no_behavior_change_refactor` | `no_behavior_change_refactor` |
