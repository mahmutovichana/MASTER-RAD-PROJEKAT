# Quality Checks

The validation script checks:

- at least 2500 records exist
- required legacy and v0.3 fields are present
- documentation categories and change levels are valid
- duplicate ids and duplicate semantic records do not exist
- labels match positive/negative scenario groups
- positive records include expected facts and gold patches
- negative records include clear reasons and no gold patches
- target and affected documentation files exist
- project-level split leakage is absent
