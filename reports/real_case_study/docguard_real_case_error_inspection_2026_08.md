# DocGuard Real Case Error Inspection 2026-08

This diagnostic report inspects real-case prediction errors using only safe case input fields:

- `code_changed_files`
- `language`
- `docs_before_excerpt`
- `code_diff_excerpt`

Audit-only source fields such as `docs_after_excerpt`, `manual_label_notes`, `docs_changed_files`, and gold patch summaries are not shown.

## Error Counts Included

`{'FP': 5}`

## Compact Error Table

| Type | Case | Gold | Pred | Gold category | Pred category | Signals | Verifier | Quality | Risk |
| --- | --- | ---: | ---: | --- | --- | --- | --- | --- | --- |
| `FP` | `GH-PROJ-016` | `False` | `True` | `none` | `model_contract` | `schema_or_model_change, workflow_change` | `pass` | `excellent` | `low` |
| `FP` | `GH-PROJ-017` | `False` | `True` | `none` | `model_contract` | `schema_or_model_change` | `pass` | `usable` | `low` |
| `FP` | `GH-PROJ-018` | `False` | `True` | `none` | `configuration` | `schema_or_model_change, configuration_change, workflow_change` | `pass` | `usable` | `low` |
| `FP` | `GH-PROJ-019` | `False` | `True` | `none` | `api_reference` | `endpoint_change, developer_setup_change, architecture_change` | `pass` | `usable` | `low` |
| `FP` | `GH-PROJ-020` | `False` | `True` | `none` | `model_contract` | `schema_or_model_change` | `fail` | `rejected` | `high` |

## Detailed Cases

### `FP` — `GH-PROJ-016`

- Language: `typescript`
- Code changed files: `['apps/sim/executor/execution/executor.test.ts', 'apps/sim/executor/execution/executor.ts', 'apps/sim/executor/execution/types.ts', 'apps/sim/executor/handlers/agent/agent-handler.test.ts', 'apps/sim/executor/handlers/agent/agent-handler.ts', 'apps/sim/executor/handlers/workflow/custom-block-tool-runner.ts', 'apps/sim/executor/handlers/workflow/workflow-handler.test.ts', 'apps/sim/executor/handlers/workflow/workflow-handler.ts', 'apps/sim/executor/handlers/workflow/workflow-tool-runner.ts', 'apps/sim/executor/types.ts', 'apps/sim/executor/utils/resolved-secret-trace-registry.ts', 'apps/sim/lib/workflows/application/authorization.test.ts']`
- Gold docs update required: `False`
- Predicted docs update required: `True`
- Gold category normalized: `none`
- Predicted category: `model_contract`
- Predicted target: `docs/models.md`
- Predicted scenario: `real_schema_or_model_contract_change`
- Signals: `schema_or_model_change, workflow_change`
- Router reason: Real-case detector used only code_changed_files, code_diff_excerpt, docs_before_excerpt, and language. Signals: schema_or_model_change, workflow_change.
- Verifier: `pass`
- Quality: `excellent`
- Hallucination risk: `low`

Safe code diff excerpt:

```diff
@@ -421,6 +421,7 @@ export class DAGExecutor {
       fileKeys: this.contextExtensions.fileKeys,
       allowLargeValueWorkflowScope: this.contextExtensions.allowLargeValueWorkflowScope,
       userId: this.contextExtensions.userId,
+      executorDelegationOrigin: this.contextExtensions.executorDelegationOrigin,
       isDeployedContext: this.contextExtensions.isDeployedContext,
       enforceCredentialAccess: this.contextExtensions.enforceCredentialAccess,
       piiBlockOutputRedaction: this.contextExtensions.piiBlockOutputRedaction,
```

Safe docs-before excerpt:

```markdown

```

Predicted patch:

```diff
@@ Data Models
+Document the changed public data contract fields: `executorDelegationOrigin`.
```

Warnings / quality reasons:

- patch is grounded, minimal, and readable under lightweight heuristic checks

### `FP` — `GH-PROJ-017`

- Language: `typescript`
- Code changed files: `['unknown-code-file']`
- Gold docs update required: `False`
- Predicted docs update required: `True`
- Gold category normalized: `none`
- Predicted category: `model_contract`
- Predicted target: `docs/models.md`
- Predicted scenario: `real_schema_or_model_contract_change`
- Signals: `schema_or_model_change`
- Router reason: Real-case detector used only code_changed_files, code_diff_excerpt, docs_before_excerpt, and language. Signals: schema_or_model_change.
- Verifier: `pass`
- Quality: `usable`
- Hallucination risk: `low`

Safe code diff excerpt:

```diff
@@ -12,7 +12,7 @@ import {
 } from './api.ts'
 import { useMemberNames } from './useMemberNames.ts'
 import { MemberPicker } from './MemberPicker.tsx'
-import { sortMembersForDisplay, withSyntheticOwner } from './sort.ts'
+import { CurrentMembersList } from './CurrentMembersList.tsx'
 import { settleWithConcurrency } from './batchGrant.ts'
 import { InvitePanel } from '../invite/InvitePanel.tsx'
 import { useAccessRequests, type UseAccessRequestsResult } from '../access-request/useAccessRequests.ts'
@@ -211,51 +211,16 @@ export function MemberPanel({
         displayName={displayName}
       />
```

Safe docs-before excerpt:

```markdown

```

Predicted patch:

```diff
@@ Data Models
+Document the changed public data/schema contract.
```

Warnings / quality reasons:

- patch is grounded, minimal, and readable under lightweight heuristic checks

### `FP` — `GH-PROJ-018`

- Language: `python`
- Code changed files: `['src/portfolio/exit_classification.py', 'src/workers/portfolio_scheduler.py', 'tests/workers/test_fallback_drop_logging.py']`
- Gold docs update required: `False`
- Predicted docs update required: `True`
- Gold category normalized: `none`
- Predicted category: `configuration`
- Predicted target: `docs/configuration.md`
- Predicted scenario: `real_configuration_or_environment_change`
- Signals: `schema_or_model_change, configuration_change, workflow_change`
- Router reason: Real-case detector used only code_changed_files, code_diff_excerpt, docs_before_excerpt, and language. Signals: schema_or_model_change, configuration_change, workflow_change.
- Verifier: `pass`
- Quality: `usable`
- Hallucination risk: `low`

Safe code diff excerpt:

```diff
@@ -40,6 +40,19 @@
 BELOW_ENTRY_GATE = "below_entry_gate"
 """Dropped because |score| was under the active feedback:entry_threshold."""
 
+# ─── Decisions: the value written to execution_decisions.decision for a SKIP ───
+# S4's skip paths persist a row in execution_decisions so a no-trade symbol is
+# distinguishable from NO_NEWS (issue #151). Each drop the ranking applies has a
+# matching decision label; FALLBACK_FILTERED (the in-memory disposition, per cycle)
+# and SKIP_FALLBACK (the persisted decision, cross-cycle) are two names for the same
+# concept at two levels — kept here together so the concept has one source of truth
+# and the scheduler imports the string instead of retyping it.
+DECISION_SKIP_FALLBACK = "SKIP_FALLBACK"
```

Safe docs-before excerpt:

```markdown

```

Predicted patch:

```diff
@@ Configuration
+Document `DECISION_SKIP_FALLBACK` and its visible default value `SKIP_FALLBACK`.
```

Warnings / quality reasons:

- patch is grounded, minimal, and readable under lightweight heuristic checks

### `FP` — `GH-PROJ-019`

- Language: `python`
- Code changed files: `['backend/voice-agent/app/local_main.py', 'backend/voice-agent/requirements.txt']`
- Gold docs update required: `False`
- Predicted docs update required: `True`
- Gold category normalized: `none`
- Predicted category: `api_reference`
- Predicted target: `docs/api.md`
- Predicted scenario: `real_api_or_endpoint_contract_change`
- Signals: `endpoint_change, developer_setup_change, architecture_change`
- Router reason: Real-case detector used only code_changed_files, code_diff_excerpt, docs_before_excerpt, and language. Signals: endpoint_change, developer_setup_change, architecture_change.
- Verifier: `pass`
- Quality: `usable`
- Hallucination risk: `low`

Safe code diff excerpt:

```diff
@@ -38,13 +38,14 @@
 import structlog
 import uvicorn
 from dotenv import load_dotenv
-from fastapi import FastAPI, BackgroundTasks
+from fastapi import FastAPI, BackgroundTasks, Request, Response
 from fastapi.responses import RedirectResponse
 
 from pipecat.pipeline.runner import PipelineRunner
 from pipecat.transports.smallwebrtc.connection import SmallWebRTCConnection
 from pipecat.transports.smallwebrtc.request_handler import (
     ConnectionMode,
```

Safe docs-before excerpt:

```markdown

```

Predicted patch:

```diff
@@ API Reference
+Document the public API contract change detected in the code diff.
```

Warnings / quality reasons:

- patch is grounded, minimal, and readable under lightweight heuristic checks

### `FP` — `GH-PROJ-020`

- Language: `typescript`
- Code changed files: `['apps/web/src/features/auth/login-panel.stories.tsx', 'apps/web/src/testing/fixtures/auth.ts', 'apps/web/src/testing/handlers/auth.ts']`
- Gold docs update required: `False`
- Predicted docs update required: `True`
- Gold category normalized: `none`
- Predicted category: `model_contract`
- Predicted target: `docs/models.md`
- Predicted scenario: `real_schema_or_model_contract_change`
- Signals: `schema_or_model_change`
- Router reason: Real-case detector used only code_changed_files, code_diff_excerpt, docs_before_excerpt, and language. Signals: schema_or_model_change.
- Verifier: `fail`
- Quality: `rejected`
- Hallucination risk: `high`

Safe code diff excerpt:

```diff
@@ -0,0 +1,67 @@
+import type { Me } from '@/features/auth/me';
+
+export const FIXED_NOW = '2026-01-15T10:30:00.000Z';
+
+/**
+ * Mock user: regular tenant user with no elevated roles.
+ * Used for basic sign-in scenarios and permission-restricted features.
+ */
+export const meRegularUser = {
+  id: '00000000-0000-4000-8000-000000000001',
+  email: 'alice@example.com',
```

Safe docs-before excerpt:

```markdown

```

Predicted patch:

```diff
@@ Data Models
+Document the changed public data contract fields: `id`, `email`.
```

Warnings / quality reasons:

- unsupported field/identifier claims: email, id
- patch does not include any concrete token extracted from the diff
- verifier found unsupported claims
