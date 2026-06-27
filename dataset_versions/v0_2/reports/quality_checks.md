# Quality Checks

The validation script checks:

- at least 1500 records exist
- required fields are present
- duplicate ids do not exist
- duplicate semantic records do not exist
- normalized near-duplicate records do not exist
- positive and negative labels match scenario types
- expected facts are non-empty, unique, and grounded for positive records
- positive records include expected facts
- positive records include a gold documentation patch
- positive gold patches include a hunk header, target section, and added documentation lines
- positive gold patch additions are reflected in the gold after excerpt
- negative records do not include a gold documentation patch
- negative records include a negative reason
- negative records do not change the gold after excerpt
- changed files and target documentation files exist
- train/validation/test splits do not leak projects
- every split record is present in the full dataset
- split copies match the full dataset records

Current reusable scenario templates:

- `new_endpoint`
- `changed_validation_min`
- `changed_auth_requirement`
- `added_response_field`
- `internal_refactor`
- `removed_endpoint`
- `changed_endpoint_path`
- `changed_http_method`
- `added_request_field`
- `removed_request_field`
- `changed_validation_max`
- `changed_enum_values`
- `changed_status_code`
- `changed_error_response`
- `deprecated_endpoint`
- `docs_already_updated`
- `formatting_only`
- `test_only_change`
- `comment_only_change`
- `dependency_config_change`
- `rename_private_helper`
- `internal_service_logic_no_api_change`
