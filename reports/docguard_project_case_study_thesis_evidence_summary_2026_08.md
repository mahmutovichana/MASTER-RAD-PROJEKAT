# DocGuard Project Case Study Thesis Evidence Summary 2026-08

This is a small manually audited project-level case study. It supports practical alignment of DocGuard with software-project documentation consistency, but it is not a large benchmark. No automatic DocGuard score is reported yet because the runner remains deferred pending a real-case adapter.

## Final Counts

- Total cases: `20`
- Positive cases: `15`
- Negative cases: `5`
- High confidence: `15`
- Medium confidence: `2`
- Low confidence: `3`

## Safe Input Policy

- Future automatic runners may use only `language`, `code_changed_files`, `code_diff_excerpt`, and `docs_before_excerpt`.
- `changed_files`, `docs_changed_files`, `change_type`, `docs_after_excerpt`, gold labels, manual notes, and label confidence are audit-only.
- Documentation file presence must not drive binary prediction.

## Distribution By Change Type

| Change type | Count |
| --- | ---: |
| `api_endpoint_change` | 2 |
| `configuration_change` | 2 |
| `internal_refactor_no_docs_needed` | 1 |
| `request_response_schema_change` | 8 |
| `testing_command_change` | 6 |
| `workflow_change` | 1 |

## Strongest Evidence Cases

- `GH-PROJ-001` `ragpark/controltower`: request_response_schema_change -> `README.md`
- `GH-PROJ-002` `d-hinders/Haven-AI`: request_response_schema_change -> `docs/architecture/07-edge-signer.md`
- `GH-PROJ-003` `eclipsefdn-ai-registry/ai-registry-core`: request_response_schema_change -> `skills/create-plugin-approval/SKILL.md`
- `GH-PROJ-004` `torbido-hq/cicerone`: api_endpoint_change -> `examples/serve/README.md`
- `GH-PROJ-005` `CryptoJones/omind`: testing_command_change -> `docs/install-verification.md`
- `GH-PROJ-006` `FaultMaven/faultmaven`: request_response_schema_change -> `docs/reference/api/openapi.json`
- `GH-PROJ-007` `SiinXu/stock-pulse-ai`: request_response_schema_change -> `docs/CHANGELOG.md`
- `GH-PROJ-008` `Apprentice-doa/YieldSense-Crop-Yield-Forecasting-Carnegie-Mellon-University`: api_endpoint_change -> `README.md`

## Qualitative / Review-Needed Cases

- `GH-PROJ-016` `low` `simstudioai/sim`: Real public GitHub PR selected as negative from code-only file list. Manual confidence is medium because no documentation file changed in the captured PR files: fix(executor): restore delegated workflow execution Hardening audit: label lowered to low because delegated workflow execution may affect documented behavior; requires human reviewer confirmation. Leakage cleanup: removed audit text about absent documentation files from docs_before_excerpt; that evidence remains audit-only in manual_label_notes/docs_changed_files.
- `GH-PROJ-017` `medium` `Mininglamp-OSS/octo-web`: Real public GitHub PR selected as negative from code-only file list. Manual confidence is medium because no documentation file changed in the captured PR files: refactor(docs): share the current-members list between rich and html panels Hardening audit: retained as medium-confidence negative because the captured diff is internal/test-oriented and no documentation file is present, but this remains weaker than positive code+docs evidence. Leakage cleanup: removed audit text about absent documentation files from docs_before_excerpt; that evidence remains audit-only in manual_label_notes/docs_changed_files.
- `GH-PROJ-018` `low` `Jonbj/alembic`: Real public GitHub PR selected as negative from code-only file list. Manual confidence is medium because no documentation file changed in the captured PR files: fix(#151): segnali solo-fallback visibili nel Decision Log (SKIP_FALLBACK) Hardening audit: label lowered to low because decision-log visibility could plausibly require user-facing or operations documentation; requires human reviewer confirmation. Leakage cleanup: removed audit text about absent documentation files from docs_before_excerpt; that evidence remains audit-only in manual_label_notes/docs_changed_files.
- `GH-PROJ-019` `low` `aws-solutions-library-samples/sample-voice-agent`: Real public GitHub PR selected as negative from code-only file list. Manual confidence is medium because no documentation file changed in the captured PR files: Fix local browser prototyping (python -m app.local_main) Hardening audit: label lowered to low because local browser prototyping behavior may affect developer setup; requires human reviewer confirmation. Leakage cleanup: removed audit text about absent documentation files from docs_before_excerpt; that evidence remains audit-only in manual_label_notes/docs_changed_files.
- `GH-PROJ-020` `medium` `singleton-sd/poc-plattform-kit`: Real public GitHub PR selected as negative from code-only file list. Manual confidence is medium because no documentation file changed in the captured PR files: Add deterministic Storybook auth fixtures for Chromatic login testing Hardening audit: retained as medium-confidence negative because the captured diff is internal/test-oriented and no documentation file is present, but this remains weaker than positive code+docs evidence. Leakage cleanup: removed audit text about absent documentation files from docs_before_excerpt; that evidence remains audit-only in manual_label_notes/docs_changed_files.

## Thesis-Safe Interpretation

- Use this case study to show that DocGuard is being evaluated against real project-level documentation consistency scenarios.
- Use positive cases as stronger alignment evidence because code and documentation patches are visible together.
- Treat negative cases cautiously; low-confidence negatives should be human-reviewed or replaced before final quantitative claims.
- Do not report automatic DocGuard accuracy until a real-case adapter/runner exists and is validated.
