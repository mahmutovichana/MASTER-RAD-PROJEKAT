# DocGuard Project Evolution Failure Analysis 2026-08

No current failures were found after the latest project-evolution run.

- Patch backend: `legacy`
- Total cases: 24
- False positives: 0
- False negatives: 0
- Category mismatches: 0
- Target-file mismatches: 0
- Scenario mismatches: 0

Historical note: the previous hard false positive was caused by `route_added` winning over `docs_already_updated`. The router now treats explicit docs-before coverage as a high-confidence no-update signal.
