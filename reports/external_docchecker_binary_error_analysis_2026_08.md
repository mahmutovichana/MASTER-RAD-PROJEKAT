# External DocChecker Binary Error Analysis 2026-08

## Confusion Matrix

|  | Predicted true | Predicted false |
| --- | ---: | ---: |
| Gold true | 250 | 0 |
| Gold false | 248 | 2 |

## Metrics

| System | TP | FP | TN | FN | Accuracy | Precision | Recall | F1 | FPR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Existing DocGuard | 250 | 248 | 2 | 0 | 50.40% | 50.20% | 100.00% | 66.84% | 99.20% |

## Label Distributions

- Gold labels: `{'True': 250, 'False': 250}`
- Predicted labels: `{'True': 498, 'False': 2}`
- False positives: `248`
- False negatives: `0`
- False positive rate: `99.20%`
- False negative rate: `0.00%`

## Confidence Summary By Outcome

| Outcome | Count | Min | Median | Mean | Max |
| --- | ---: | ---: | ---: | ---: | ---: |
| TP | 250 | 0.0697 | 0.1234 | 0.1396 | 0.3267 |
| FP | 248 | 0.0688 | 0.1203 | 0.1300 | 0.2915 |
| TN | 2 | 0.2261 | 0.2607 | 0.2607 | 0.2953 |
| FN | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## Predicted Doc Category Distribution

### Gold Positive Records

- `workflow_documentation`: 115
- `testing_instructions`: 87
- `model_contract`: 20
- `configuration`: 16
- `architecture_flow`: 5
- `changelog`: 4
- `developer_setup`: 3

### Gold Negative Records

- `workflow_documentation`: 113
- `testing_instructions`: 95
- `architecture_flow`: 14
- `configuration`: 9
- `developer_setup`: 7
- `model_contract`: 6
- `changelog`: 4
- `no_update`: 2

## Predicted Scenario Type Distribution

### Gold Positive Records

- `changed_testing_framework`: 50
- `removed_dto_model_field`: 44
- `changed_test_command`: 42
- `added_service_orchestration_flow`: 28
- `changed_validation_max`: 18
- `changelog_worthy_behavior_change`: 17
- `changed_enum_values`: 8
- `added_environment_variable`: 7
- `changed_seed_or_setup_flow`: 6
- `added_background_job_flow`: 6
- `removed_environment_variable`: 5
- `changed_validation_min`: 4
- `removed_endpoint`: 4
- `changed_middleware_auth_flow`: 4
- `changed_caching_or_rate_limit_flow`: 3
- `changed_local_development_flow`: 2
- `changed_default_config_value`: 1
- `changed_background_job_schedule`: 1

### Gold Negative Records

- `changed_testing_framework`: 103
- `changed_validation_max`: 33
- `added_service_orchestration_flow`: 23
- `changed_validation_min`: 18
- `removed_dto_model_field`: 16
- `changed_test_command`: 11
- `added_background_job_flow`: 8
- `changed_enum_values`: 7
- `changed_caching_or_rate_limit_flow`: 6
- `changelog_worthy_behavior_change`: 6
- `removed_request_field`: 5
- `removed_environment_variable`: 4
- `changed_middleware_auth_flow`: 4
- `removed_endpoint`: 2
- `docs_already_updated`: 2
- `changed_default_config_value`: 1
- `changed_background_job_schedule`: 1

## Target File / Source Distribution

- `data\external\raw\deep_jit_inconsistency\Return\test.json`: 250
- `data\external\raw\deep_jit_inconsistency\Summary\test.json`: 250
