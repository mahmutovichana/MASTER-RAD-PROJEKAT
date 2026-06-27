# Dataset v0.2 Summary

## Purpose

Dataset v0.2 extends DocGuard beyond the regular v0.1 templates. It keeps the same 10 synthetic TypeScript + Express REST API projects and project-level split strategy, but introduces more API-change scenarios so the rule-based baseline no longer has a near-perfect template match.

## New Scenario Types

Positive scenarios added in v0.2:

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

Negative scenarios added in v0.2:

- `docs_already_updated`
- `formatting_only`
- `test_only_change`
- `comment_only_change`
- `dependency_config_change`
- `rename_private_helper`
- `internal_service_logic_no_api_change`

## Difference From v0.1

- v0.1: 1000 records, 5 scenario types, highly regular template-generated diffs.
- v0.2: 1500 records, 22 scenario types, broader positive and negative API-change patterns.

## Why v0.2 Is Harder

- Many scenario types are unsupported by the first rule-based baseline.
- Some positive changes require interpreting removals, path changes, enum changes, status-code changes, and error-response changes.
- Negative examples include code/config/comment/test changes that should not trigger documentation patches.
- The baseline must avoid hallucinating patches for unsupported changes.

## Limitations

- v0.2 is still synthetic and template-generated.
- Generated diffs remain simpler than real-world pull requests.
- Gold patches are minimal and intentionally concise.
- Manual semantic audit is still needed.

## Next Planned Step

Compare the rule-based baseline against an NLP-assisted DocGuard agent that can reason about unsupported v0.2 scenarios and generate more complete documentation patches.
