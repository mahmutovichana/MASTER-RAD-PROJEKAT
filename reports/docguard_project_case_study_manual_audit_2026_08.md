# DocGuard Project Case Study Manual Audit 2026-08

This report summarizes the real project-level DocGuard manual case-study file after methodology hardening. It is a small manually audited sample, not a large benchmark and not a replacement for the synthetic benchmark or Deep-JIT proxy evidence.

## Collection Summary

- Cases collected: `20`
- Positive cases: `15`
- Negative cases: `5`
- Repositories used: `19`

## Repositories

- `Apprentice-doa/YieldSense-Crop-Yield-Forecasting-Carnegie-Mellon-University`
- `CryptoJones/omind`
- `FaultMaven/faultmaven`
- `Jonbj/alembic`
- `Mininglamp-OSS/octo-web`
- `NomadicDaddy/starsync`
- `RedHatInsights/lightspeed-advisor-on-premise-ocp`
- `SiinXu/stock-pulse-ai`
- `aws-solutions-library-samples/sample-voice-agent`
- `d-hinders/Haven-AI`
- `eclipsefdn-ai-registry/ai-registry-core`
- `eumemic/aios`
- `lightning-it/ansible-collection-supplementary`
- `ragpark/controltower`
- `simstudioai/sim`
- `singleton-sd/poc-plattform-kit`
- `srbadni/JobApplicationTracker`
- `torbido-hq/cicerone`
- `vLLM-HUST/vllm-hust-benchmark`

## Distribution By Change Type

| Change type | Count |
| --- | ---: |
| `api_endpoint_change` | 2 |
| `configuration_change` | 2 |
| `internal_refactor_no_docs_needed` | 1 |
| `request_response_schema_change` | 8 |
| `testing_command_change` | 6 |
| `workflow_change` | 1 |

## Label Distribution

| Label | Count |
| --- | ---: |
| `negative` | 5 |
| `positive` | 15 |

## Label Confidence Distribution

| Confidence | Count |
| --- | ---: |
| `high` | 15 |
| `low` | 3 |
| `medium` | 2 |

## Five Strongest Positive Cases

### `GH-PROJ-001` `ragpark/controltower`

- URL: https://github.com/ragpark/controltower/pull/2
- Change type: `request_response_schema_change`
- Target doc: `README.md`
- Category: `data_model`
- Notes: Real public GitHub PR. Positive label based on code patch plus documentation patch in the same PR: Align ingestion to the ActiveHub export schema and fix container/mapping defects

### `GH-PROJ-002` `d-hinders/Haven-AI`

- URL: https://github.com/d-hinders/Haven-AI/pull/1314
- Change type: `request_response_schema_change`
- Target doc: `docs/architecture/07-edge-signer.md`
- Category: `data_model`
- Notes: Real public GitHub PR. Positive label based on code patch plus documentation patch in the same PR: feat(mcp+sdk): structured next_action/agent_summary/warnings contract (#1308)

### `GH-PROJ-003` `eclipsefdn-ai-registry/ai-registry-core`

- URL: https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/79
- Change type: `request_response_schema_change`
- Target doc: `skills/create-plugin-approval/SKILL.md`
- Category: `data_model`
- Notes: Real public GitHub PR. Positive label based on code patch plus documentation patch in the same PR: Add Agent Plugin (agent-plugins.org) as a fourth artifact type

### `GH-PROJ-004` `torbido-hq/cicerone`

- URL: https://github.com/torbido-hq/cicerone/pull/59
- Change type: `api_endpoint_change`
- Target doc: `examples/serve/README.md`
- Category: `data_model`
- Notes: Real public GitHub PR. Positive label based on code patch plus documentation patch in the same PR: Add Prometheus /metrics endpoint for serve mode

### `GH-PROJ-005` `CryptoJones/omind`

- URL: https://github.com/CryptoJones/omind/pull/229
- Change type: `testing_command_change`
- Target doc: `docs/install-verification.md`
- Category: `testing`
- Notes: Real public GitHub PR. Positive label based on code patch plus documentation patch in the same PR: fix(provision,guard,store): pin hooks to a canonical omind, fix title recall


## Negative Cases

### `GH-PROJ-016` `simstudioai/sim`

- URL: https://github.com/simstudioai/sim/pull/6539
- Change type: `testing_command_change`
- Target doc: `none`
- Confidence: `low`
- Notes: Real public GitHub PR selected as negative from code-only file list. Manual confidence is medium because no documentation file changed in the captured PR files: fix(executor): restore delegated workflow execution Hardening audit: label lowered to low because delegated workflow execution may affect documented behavior; requires human reviewer confirmation.

### `GH-PROJ-017` `Mininglamp-OSS/octo-web`

- URL: https://github.com/Mininglamp-OSS/octo-web/pull/1347
- Change type: `testing_command_change`
- Target doc: `none`
- Confidence: `medium`
- Notes: Real public GitHub PR selected as negative from code-only file list. Manual confidence is medium because no documentation file changed in the captured PR files: refactor(docs): share the current-members list between rich and html panels Hardening audit: retained as medium-confidence negative because the captured diff is internal/test-oriented and no documentation file is present, but this remains weaker than positive code+docs evidence.

### `GH-PROJ-018` `Jonbj/alembic`

- URL: https://github.com/Jonbj/alembic/pull/229
- Change type: `testing_command_change`
- Target doc: `none`
- Confidence: `low`
- Notes: Real public GitHub PR selected as negative from code-only file list. Manual confidence is medium because no documentation file changed in the captured PR files: fix(#151): segnali solo-fallback visibili nel Decision Log (SKIP_FALLBACK) Hardening audit: label lowered to low because decision-log visibility could plausibly require user-facing or operations documentation; requires human reviewer confirmation.

### `GH-PROJ-019` `aws-solutions-library-samples/sample-voice-agent`

- URL: https://github.com/aws-solutions-library-samples/sample-voice-agent/pull/26
- Change type: `internal_refactor_no_docs_needed`
- Target doc: `none`
- Confidence: `low`
- Notes: Real public GitHub PR selected as negative from code-only file list. Manual confidence is medium because no documentation file changed in the captured PR files: Fix local browser prototyping (python -m app.local_main) Hardening audit: label lowered to low because local browser prototyping behavior may affect developer setup; requires human reviewer confirmation.

### `GH-PROJ-020` `singleton-sd/poc-plattform-kit`

- URL: https://github.com/singleton-sd/poc-plattform-kit/pull/148
- Change type: `testing_command_change`
- Target doc: `none`
- Confidence: `medium`
- Notes: Real public GitHub PR selected as negative from code-only file list. Manual confidence is medium because no documentation file changed in the captured PR files: Add deterministic Storybook auth fixtures for Chromatic login testing Hardening audit: retained as medium-confidence negative because the captured diff is internal/test-oriented and no documentation file is present, but this remains weaker than positive code+docs evidence.


## Known Limitations

- The sample has 20 cases and is intentionally small.
- Positive labels are stronger because code and documentation patches are visible together.
- Negative labels remain weaker; three were lowered to low confidence and should be human-reviewed or replaced before final quantitative claims.
- GitHub unauthenticated API rate limiting prevented reliable replacement during this pass; no fake cases were added.
- Excerpts are short by design and do not reproduce large copyrighted code or documentation blocks.
- `docs_after_excerpt`, `change_type`, and all `gold_*` fields are audit-only and must not be used as automatic model input.
- This study supports practical DocGuard agent alignment but should be reported as qualitative/semi-quantitative evidence, not a large benchmark.
