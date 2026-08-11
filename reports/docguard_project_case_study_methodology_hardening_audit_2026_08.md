# DocGuard Project Case Study Methodology Hardening Audit 2026-08

This audit hardens the 20-record real project-level DocGuard case-study file before it is used as thesis evidence. It intentionally does not report automatic DocGuard accuracy.

## Overall Findings

- All records point to public GitHub PR URLs captured through the GitHub API candidate cache.
- Positive cases are stronger because they include visible code and documentation patches in the same PR.
- Negative cases are weaker because absence of changed documentation is not proof that no documentation update was required.
- `change_type` is manually assigned and has been removed from `allowed_model_input_fields`; it is now audit-only.
- The sample remains skewed toward request/response/schema and testing-command changes.
- No cases were removed or relabeled as positive/negative in this pass; three negative cases were lowered to `low` confidence and marked for human review.

## Record-Level Audit

| Case | Source | Label | Confidence | Change type | Evidence | Suitability | Decision | Why |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `GH-PROJ-001` | `ragpark/controltower` [PR](https://github.com/ragpark/controltower/pull/2) | `True` | `high` | `request_response_schema_change` | `strong` | thesis evidence | remain | Visible code and documentation relation in the same public PR; docs_after remains audit-only. |
| `GH-PROJ-002` | `d-hinders/Haven-AI` [PR](https://github.com/d-hinders/Haven-AI/pull/1314) | `True` | `high` | `request_response_schema_change` | `strong` | thesis evidence | remain | Visible code and documentation relation in the same public PR; docs_after remains audit-only. |
| `GH-PROJ-003` | `eclipsefdn-ai-registry/ai-registry-core` [PR](https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/79) | `True` | `high` | `request_response_schema_change` | `strong` | thesis evidence | remain | Visible code and documentation relation in the same public PR; docs_after remains audit-only. |
| `GH-PROJ-004` | `torbido-hq/cicerone` [PR](https://github.com/torbido-hq/cicerone/pull/59) | `True` | `high` | `api_endpoint_change` | `strong` | thesis evidence | remain | Visible code and documentation relation in the same public PR; docs_after remains audit-only. |
| `GH-PROJ-005` | `CryptoJones/omind` [PR](https://github.com/CryptoJones/omind/pull/229) | `True` | `high` | `testing_command_change` | `strong` | thesis evidence | remain | Visible code and documentation relation in the same public PR; docs_after remains audit-only. |
| `GH-PROJ-006` | `FaultMaven/faultmaven` [PR](https://github.com/FaultMaven/faultmaven/pull/1028) | `True` | `high` | `request_response_schema_change` | `strong` | thesis evidence | remain | Visible code and documentation relation in the same public PR; docs_after remains audit-only. |
| `GH-PROJ-007` | `SiinXu/stock-pulse-ai` [PR](https://github.com/SiinXu/stock-pulse-ai/pull/1045) | `True` | `high` | `request_response_schema_change` | `strong` | thesis evidence | remain | Visible code and documentation relation in the same public PR; docs_after remains audit-only. |
| `GH-PROJ-008` | `Apprentice-doa/YieldSense-Crop-Yield-Forecasting-Carnegie-Mellon-University` [PR](https://github.com/Apprentice-doa/YieldSense-Crop-Yield-Forecasting-Carnegie-Mellon-University/pull/3) | `True` | `high` | `api_endpoint_change` | `strong` | thesis evidence | remain | Visible code and documentation relation in the same public PR; docs_after remains audit-only. |
| `GH-PROJ-009` | `eumemic/aios` [PR](https://github.com/eumemic/aios/pull/1444) | `True` | `high` | `request_response_schema_change` | `strong` | thesis evidence | remain | Visible code and documentation relation in the same public PR; docs_after remains audit-only. |
| `GH-PROJ-010` | `srbadni/JobApplicationTracker` [PR](https://github.com/srbadni/JobApplicationTracker/pull/4) | `True` | `high` | `request_response_schema_change` | `strong` | thesis evidence | remain | Visible code and documentation relation in the same public PR; docs_after remains audit-only. |
| `GH-PROJ-011` | `SiinXu/stock-pulse-ai` [PR](https://github.com/SiinXu/stock-pulse-ai/pull/953) | `True` | `high` | `request_response_schema_change` | `strong` | thesis evidence | remain | Visible code and documentation relation in the same public PR; docs_after remains audit-only. |
| `GH-PROJ-012` | `vLLM-HUST/vllm-hust-benchmark` [PR](https://github.com/vLLM-HUST/vllm-hust-benchmark/pull/167) | `True` | `high` | `testing_command_change` | `strong` | thesis evidence | remain | Visible code and documentation relation in the same public PR; docs_after remains audit-only. |
| `GH-PROJ-013` | `RedHatInsights/lightspeed-advisor-on-premise-ocp` [PR](https://github.com/RedHatInsights/lightspeed-advisor-on-premise-ocp/pull/252) | `True` | `high` | `configuration_change` | `strong` | thesis evidence | remain | Visible code and documentation relation in the same public PR; docs_after remains audit-only. |
| `GH-PROJ-014` | `lightning-it/ansible-collection-supplementary` [PR](https://github.com/lightning-it/ansible-collection-supplementary/pull/673) | `True` | `high` | `configuration_change` | `strong` | thesis evidence | remain | Visible code and documentation relation in the same public PR; docs_after remains audit-only. |
| `GH-PROJ-015` | `NomadicDaddy/starsync` [PR](https://github.com/NomadicDaddy/starsync/pull/10) | `True` | `high` | `workflow_change` | `strong` | thesis evidence | remain | Visible code and documentation relation in the same public PR; docs_after remains audit-only. |
| `GH-PROJ-016` | `simstudioai/sim` [PR](https://github.com/simstudioai/sim/pull/6539) | `False` | `low` | `testing_command_change` | `weak` | qualitative only / needs human review | remain with low confidence or replace if stronger negative is found | Negative evidence is not strong enough because no docs changed is not by itself proof that docs were unnecessary. |
| `GH-PROJ-017` | `Mininglamp-OSS/octo-web` [PR](https://github.com/Mininglamp-OSS/octo-web/pull/1347) | `False` | `medium` | `testing_command_change` | `moderate` | limited thesis evidence | remain as medium-confidence negative | Diff appears internal/test-oriented and no doc file is in captured file list, but negative evidence is still weaker than positives. |
| `GH-PROJ-018` | `Jonbj/alembic` [PR](https://github.com/Jonbj/alembic/pull/229) | `False` | `low` | `testing_command_change` | `weak` | qualitative only / needs human review | remain with low confidence or replace if stronger negative is found | Negative evidence is not strong enough because no docs changed is not by itself proof that docs were unnecessary. |
| `GH-PROJ-019` | `aws-solutions-library-samples/sample-voice-agent` [PR](https://github.com/aws-solutions-library-samples/sample-voice-agent/pull/26) | `False` | `low` | `internal_refactor_no_docs_needed` | `weak` | qualitative only / needs human review | remain with low confidence or replace if stronger negative is found | Negative evidence is not strong enough because no docs changed is not by itself proof that docs were unnecessary. |
| `GH-PROJ-020` | `singleton-sd/poc-plattform-kit` [PR](https://github.com/singleton-sd/poc-plattform-kit/pull/148) | `False` | `medium` | `testing_command_change` | `moderate` | limited thesis evidence | remain as medium-confidence negative | Diff appears internal/test-oriented and no doc file is in captured file list, but negative evidence is still weaker than positives. |

## Negative Case Review

- `GH-PROJ-016` `low`: Real public GitHub PR selected as negative from code-only file list. Manual confidence is medium because no documentation file changed in the captured PR files: fix(executor): restore delegated workflow execution Hardening audit: label lowered to low because delegated workflow execution may affect documented behavior; requires human reviewer confirmation.
- `GH-PROJ-017` `medium`: Real public GitHub PR selected as negative from code-only file list. Manual confidence is medium because no documentation file changed in the captured PR files: refactor(docs): share the current-members list between rich and html panels Hardening audit: retained as medium-confidence negative because the captured diff is internal/test-oriented and no documentation file is present, but this remains weaker than positive code+docs evidence.
- `GH-PROJ-018` `low`: Real public GitHub PR selected as negative from code-only file list. Manual confidence is medium because no documentation file changed in the captured PR files: fix(#151): segnali solo-fallback visibili nel Decision Log (SKIP_FALLBACK) Hardening audit: label lowered to low because decision-log visibility could plausibly require user-facing or operations documentation; requires human reviewer confirmation.
- `GH-PROJ-019` `low`: Real public GitHub PR selected as negative from code-only file list. Manual confidence is medium because no documentation file changed in the captured PR files: Fix local browser prototyping (python -m app.local_main) Hardening audit: label lowered to low because local browser prototyping behavior may affect developer setup; requires human reviewer confirmation.
- `GH-PROJ-020` `medium`: Real public GitHub PR selected as negative from code-only file list. Manual confidence is medium because no documentation file changed in the captured PR files: Add deterministic Storybook auth fixtures for Chromatic login testing Hardening audit: retained as medium-confidence negative because the captured diff is internal/test-oriented and no documentation file is present, but this remains weaker than positive code+docs evidence.

## Distribution Concerns

- Request/response schema changes: `8/20`; this is useful but overrepresented.
- Testing command changes: `6/20`; some are negative/internal-test oriented and should not dominate final claims.
- API endpoint changes: `2/20`; future expansion should add more API endpoint examples.
- Workflow changes: `1/20`; future expansion should add more workflow/configuration examples.

## Replacement Guidance

Prefer replacing low-confidence negatives with stronger examples such as variable renames, import cleanup, logging-only changes, private helper extraction, or test assertion refactors where public API/config/workflow behavior is clearly unchanged. GitHub unauthenticated API rate limiting prevented reliable replacement during this pass, so no invented replacements were added.

## Final Input Leakage Policy

Future automatic runners may use only `language`, `code_changed_files`, `code_diff_excerpt`, and `docs_before_excerpt`. `changed_files`, `docs_changed_files`, manually assigned `change_type`, `docs_after_excerpt`, gold labels, manual notes, and label confidence are audit-only. Documentation-file presence must not be used as a shortcut for binary prediction.
