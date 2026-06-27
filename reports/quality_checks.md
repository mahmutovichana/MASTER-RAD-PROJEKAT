# Quality Checks

The validation script checks:

- at least 1000 records exist
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
