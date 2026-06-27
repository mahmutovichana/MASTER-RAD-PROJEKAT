# DocGuard Dataset v0.2 Snapshot

This folder preserves the frozen v0.2 dataset, reports, manual audit artifacts, and baseline predictions for thesis traceability.

## Purpose

Dataset v0.2 expanded the original API-reference dataset with more endpoint, request, validation, enum, status-code, error-response, deprecation, and negative no-documentation-update scenarios.

## Scenario Types

v0.2 contains 22 scenario types, including the v0.1 scenarios plus API-level additions such as `removed_endpoint`, `changed_endpoint_path`, `changed_http_method`, `added_request_field`, `changed_validation_max`, `changed_enum_values`, `changed_status_code`, `changed_error_response`, and `deprecated_endpoint`.

## Baseline Results

The rule-based baseline on the v0.2 test split produced:

- docs_update_required precision: 93.10%
- docs_update_required recall: 100.00%
- F1: 96.43%
- scenario_type accuracy: 23.00%
- patch fact coverage: 27.59%
- hallucination count: 0

## Known Limitation

v0.2 is harder than v0.1, but it is still mostly API-reference level. It does not yet cover broader project documentation such as architecture flows, developer setup, testing, configuration, model contracts, and operational workflows.
