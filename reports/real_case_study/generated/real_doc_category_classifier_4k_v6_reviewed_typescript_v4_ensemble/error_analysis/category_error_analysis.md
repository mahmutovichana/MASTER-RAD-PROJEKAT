# Category Classifier Error Analysis

This report analyzes classifier errors only. It does not change predictions, labels, or model selection.

## locked_test

- total: `386`
- accuracy: `0.5285`
- top-2 accuracy: `0.8109`
- errors: `182`

### Gold distribution

```json
{
  "api_reference": 161,
  "configuration": 97,
  "developer_setup": 35,
  "model_contract": 93
}
```

### Predicted distribution

```json
{
  "api_reference": 211,
  "configuration": 51,
  "developer_setup": 53,
  "model_contract": 71
}
```

### Per-class metrics

```json
{
  "api_reference": {
    "f1": 0.6720430107526882,
    "fn": 36,
    "fp": 86,
    "precision": 0.5924170616113744,
    "predicted": 211,
    "recall": 0.7763975155279503,
    "support": 161,
    "tp": 125
  },
  "configuration": {
    "f1": 0.28378378378378377,
    "fn": 76,
    "fp": 30,
    "precision": 0.4117647058823529,
    "predicted": 51,
    "recall": 0.21649484536082475,
    "support": 97,
    "tp": 21
  },
  "developer_setup": {
    "f1": 0.5227272727272727,
    "fn": 12,
    "fp": 30,
    "precision": 0.4339622641509434,
    "predicted": 53,
    "recall": 0.6571428571428571,
    "support": 35,
    "tp": 23
  },
  "model_contract": {
    "f1": 0.4268292682926829,
    "fn": 58,
    "fp": 36,
    "precision": 0.49295774647887325,
    "predicted": 71,
    "recall": 0.3763440860215054,
    "support": 93,
    "tp": 35
  }
}
```

### Most common confusion pairs

```json
{
  "api_reference -> configuration": 17,
  "api_reference -> developer_setup": 10,
  "api_reference -> model_contract": 9,
  "configuration -> api_reference": 44,
  "configuration -> developer_setup": 15,
  "configuration -> model_contract": 17,
  "developer_setup -> api_reference": 1,
  "developer_setup -> configuration": 1,
  "developer_setup -> model_contract": 10,
  "model_contract -> api_reference": 41,
  "model_contract -> configuration": 12,
  "model_contract -> developer_setup": 5
}
```

### Error confidence buckets

```json
{
  "0.00-0.40": 67,
  "0.40-0.50": 74,
  "0.50-0.60": 25,
  "0.60-0.70": 12,
  "0.70-0.80": 3,
  "0.80-1.00": 1,
  "missing": 0
}
```

### High-confidence errors

```json
[
  {
    "case_id": "GH-CAND-6099",
    "code_changed_files": [
      "nx.json"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.8657458907483948,
    "pred_doc_category": "developer_setup",
    "repository": "typescript-eslint/typescript-eslint",
    "source_url": "https://github.com/typescript-eslint/typescript-eslint/pull/12624",
    "top2": [
      "developer_setup",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-0384",
    "code_changed_files": [
      "src/vs/platform/agentHost/common/agentService.ts",
      "src/vs/platform/agentHost/node/agentHostBootstrap.ts",
      "src/vs/platform/agentHost/node/agentHostCommitOperationHandler.ts",
      "src/vs/platform/agentHost/node/agentHostGitStateService.ts",
      "src/vs/platform/agentHost/node/agentHostMain.ts",
      "src/vs/platform/agentHost/node/agentHostPullRequestOperationHandler.ts",
      "src/vs/platform/agentHost/node/agentHostServerMain.ts",
      "src/vs/platform/agentHost/node/agentService.ts",
      "src/vs/platform/agentHost/node/agentServiceComposition.ts",
      "src/vs/platform/agentHost/test/node/agentHostCommitOperationHandler.test.ts",
      "src/vs/platform/agentHost/test/node/agentHostGitStateService.test.ts",
      "src/vs/platform/agentHost/test/node/agentHostPullRequestOperationHandler.test.ts",
      "src/vs/platform/agentHost/test/node/agentService.test.ts",
      "src/vs/platform/agentHost/test/node/agentServiceTestUtils.ts",
      "src/vs/platform/agentHost/test/node/protocolServerHandler.test.ts"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.7861623309622764,
    "pred_doc_category": "api_reference",
    "repository": "microsoft/vscode",
    "source_url": "https://github.com/microsoft/vscode/pull/332035",
    "top2": [
      "api_reference",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-0389",
    "code_changed_files": [
      "src/vs/platform/agentHost/common/agentService.ts",
      "src/vs/platform/agentHost/node/agentHostBootstrap.ts",
      "src/vs/platform/agentHost/node/agentHostCommitOperationHandler.ts",
      "src/vs/platform/agentHost/node/agentHostGitStateService.ts",
      "src/vs/platform/agentHost/node/agentHostMain.ts",
      "src/vs/platform/agentHost/node/agentHostPullRequestOperationHandler.ts",
      "src/vs/platform/agentHost/node/agentHostServerMain.ts",
      "src/vs/platform/agentHost/node/agentService.ts",
      "src/vs/platform/agentHost/node/agentServiceComposition.ts",
      "src/vs/platform/agentHost/test/node/agentHostCommitOperationHandler.test.ts",
      "src/vs/platform/agentHost/test/node/agentHostGitStateService.test.ts",
      "src/vs/platform/agentHost/test/node/agentHostPullRequestOperationHandler.test.ts",
      "src/vs/platform/agentHost/test/node/agentService.test.ts",
      "src/vs/platform/agentHost/test/node/agentServiceTestUtils.ts",
      "src/vs/platform/agentHost/test/node/protocolServerHandler.test.ts"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.7861623309622764,
    "pred_doc_category": "api_reference",
    "repository": "microsoft/vscode",
    "source_url": "https://github.com/microsoft/vscode/pull/332035",
    "top2": [
      "api_reference",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-0346",
    "code_changed_files": [
      "extensions/copilot/src/extension/inlineEdits/node/nextEditProviderTelemetry.ts",
      "extensions/copilot/src/extension/inlineEdits/test/node/nextEditProviderTelemetry.spec.ts",
      "extensions/copilot/src/extension/xtab/common/promptCrafting.ts",
      "extensions/copilot/src/extension/xtab/common/recentFilesForPrompt.ts",
      "extensions/copilot/src/extension/xtab/node/xtabProvider.ts",
      "extensions/copilot/src/extension/xtab/test/common/promptCrafting.spec.ts",
      "extensions/copilot/src/platform/inlineEdits/common/dataTypes/promptSectionTokens.ts",
      "extensions/copilot/src/platform/inlineEdits/common/inlineEditLogContext.ts",
      "extensions/copilot/src/platform/inlineEdits/common/statelessNextEditProvider.ts"
    ],
    "gold_doc_category": "model_contract",
    "language": "typescript",
    "pred_confidence": 0.73595406974366,
    "pred_doc_category": "api_reference",
    "repository": "microsoft/vscode",
    "source_url": "https://github.com/microsoft/vscode/pull/324717",
    "top2": [
      "api_reference",
      "model_contract"
    ]
  },
  {
    "case_id": "GH-CAND-2611",
    "code_changed_files": [
      ".github/workflows/generate-sandboxes.yml",
      "code/lib/cli-storybook/src/sandbox-templates.ts",
      "scripts/sandbox/generate.ts",
      "scripts/sandbox/utils/yarn.test.ts",
      "scripts/sandbox/utils/yarn.ts"
    ],
    "gold_doc_category": "api_reference",
    "language": "typescript",
    "pred_confidence": 0.6984155466297038,
    "pred_doc_category": "configuration",
    "repository": "storybookjs/storybook",
    "source_url": "https://github.com/storybookjs/storybook/pull/35939",
    "top2": [
      "configuration",
      "api_reference"
    ]
  },
  {
    "case_id": "GH-CAND-8575",
    "code_changed_files": [
      "composer.json"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.6965710134385446,
    "pred_doc_category": "developer_setup",
    "repository": "appwrite/appwrite",
    "source_url": "https://github.com/appwrite/appwrite/pull/13307",
    "top2": [
      "developer_setup",
      "api_reference"
    ]
  },
  {
    "case_id": "GH-CAND-5553",
    "code_changed_files": [
      "src/utils/chunkAssignment.ts",
      "test/chunking-form/samples/deoptimized-module-with-dynamic-import/_config.js",
      "test/chunking-form/samples/deoptimized-module-with-dynamic-import/_expected/amd/main.js",
      "test/chunking-form/samples/deoptimized-module-with-dynamic-import/_expected/cjs/main.js",
      "test/chunking-form/samples/deoptimized-module-with-dynamic-import/_expected/es/main.js",
      "test/chunking-form/samples/deoptimized-module-with-dynamic-import/_expected/system/main.js",
      "test/chunking-form/samples/deoptimized-module-with-dynamic-import/a.js",
      "test/chunking-form/samples/deoptimized-module-with-dynamic-import/cjs.js",
      "test/chunking-form/samples/deoptimized-module-with-dynamic-import/lazy-loader.js",
      "test/chunking-form/samples/deoptimized-module-with-dynamic-import/main.js"
    ],
    "gold_doc_category": "developer_setup",
    "language": "typescript",
    "pred_confidence": 0.6737007801401126,
    "pred_doc_category": "configuration",
    "repository": "rollup/rollup",
    "source_url": "https://github.com/rollup/rollup/pull/6306",
    "top2": [
      "configuration",
      "api_reference"
    ]
  },
  {
    "case_id": "GH-CAND-5546",
    "code_changed_files": [
      "src/Module.ts",
      "test/chunking-form/samples/namespace-reexport-side-effect-cache/_config.js",
      "test/chunking-form/samples/namespace-reexport-side-effect-cache/_expected/amd/entry1.js",
      "test/chunking-form/samples/namespace-reexport-side-effect-cache/_expected/amd/entry2.js",
      "test/chunking-form/samples/namespace-reexport-side-effect-cache/_expected/amd/generated-effect.js",
      "test/chunking-form/samples/namespace-reexport-side-effect-cache/_expected/cjs/entry1.js",
      "test/chunking-form/samples/namespace-reexport-side-effect-cache/_expected/cjs/entry2.js",
      "test/chunking-form/samples/namespace-reexport-side-effect-cache/_expected/cjs/generated-effect.js",
      "test/chunking-form/samples/namespace-reexport-side-effect-cache/_expected/es/entry1.js",
      "test/chunking-form/samples/namespace-reexport-side-effect-cache/_expected/es/entry2.js",
      "test/chunking-form/samples/namespace-reexport-side-effect-cache/_expected/es/generated-effect.js",
      "test/chunking-form/samples/namespace-reexport-side-effect-cache/_expected/system/entry1.js",
      "test/chunking-form/samples/namespace-reexport-side-effect-cache/_expected/system/entry2.js",
      "test/chunking-form/samples/namespace-reexport-side-effect-cache/_expected/system/generated-effect.js",
      "test/chunking-form/samples/namespace-reexport-side-effect-cache/entry1.js",
      "test/chunking-form/samples/namespace-reexport-side-effect-cache/entry2.js",
      "test/chunking-form/samples/namespace-reexport-side-effect-cache/lib/effect.js",
      "test/chunking-form/samples/namespace-reexport-side-effect-cache/lib/foo.js",
      "test/chunking-form/samples/namespace-reexport-side-effect-cache/lib/fooImpl.js",
      "test/chunking-form/samples/namespace-reexport-side-effect-cache/lib/index.js",
      "test/function/samples/circular-namespace-reexport-cache/_config.js",
      "test/function/samples/circular-namespace-reexport-cache/entry1.js",
      "test/function/samples/circular-namespace-reexport-cache/entry2.js",
      "test/function/samples/circular-namespace-reexport-cache/lib/effect.js",
      "test/function/samples/circular-namespace-reexport-cache/lib/foo.js",
      "test/function/samples/circular-namespace-reexport-cache/lib/fooImpl.js",
      "test/function/samples/circular-namespace-reexport-cache/lib/index.js",
      "test/function/samples/circular-namespace-reexport-cache/main.js"
    ],
    "gold_doc_category": "model_contract",
    "language": "typescript",
    "pred_confidence": 0.6603375709078162,
    "pred_doc_category": "configuration",
    "repository": "rollup/rollup",
    "source_url": "https://github.com/rollup/rollup/pull/6286",
    "top2": [
      "configuration",
      "api_reference"
    ]
  },
  {
    "case_id": "GH-CAND-1035",
    "code_changed_files": [
      "common/config/azure-pipelines/esrp-publish-rush.yaml",
      "common/config/azure-pipelines/esrp-publish-rushstack.yaml",
      "common/config/azure-pipelines/npm-post-publish.yaml",
      "common/config/azure-pipelines/npm-publish-rush.yaml",
      "common/config/azure-pipelines/npm-publish.yaml",
      "common/config/azure-pipelines/templates/bump-versions-stages.yaml",
      "common/config/azure-pipelines/templates/bump-versions.yaml",
      "common/config/azure-pipelines/templates/configure-git-user.yaml",
      "common/config/azure-pipelines/templates/esrp-publish-stages.yaml",
      "common/config/azure-pipelines/templates/find-bump-pipeline-run.yaml",
      "common/config/azure-pipelines/templates/pack.yaml",
      "common/config/azure-pipelines/templates/prepare-publish-artifacts.yaml",
      "common/config/azure-pipelines/templates/publish.yaml",
      "common/config/azure-pipelines/templates/record-versions.yaml",
      "common/config/azure-pipelines/vscode-extension-publish.yaml"
    ],
    "gold_doc_category": "api_reference",
    "language": "typescript",
    "pred_confidence": 0.6557164394636337,
    "pred_doc_category": "configuration",
    "repository": "microsoft/rushstack",
    "source_url": "https://github.com/microsoft/rushstack/pull/5953",
    "top2": [
      "configuration",
      "api_reference"
    ]
  },
  {
    "case_id": "GH-CAND-6058",
    "code_changed_files": [
      ".github/workflows/ci.yml",
      "nx.json"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.6393511903688742,
    "pred_doc_category": "developer_setup",
    "repository": "typescript-eslint/typescript-eslint",
    "source_url": "https://github.com/typescript-eslint/typescript-eslint/pull/12726",
    "top2": [
      "developer_setup",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-6089",
    "code_changed_files": [
      "knip.ts",
      "nx.json",
      "package.json",
      "packages/ast-spec/package.json",
      "packages/eslint-plugin-internal/package.json",
      "packages/eslint-plugin/package.json",
      "packages/integration-tests/package.json",
      "packages/integration-tests/tools/integration-test-base.ts",
      "packages/parser/package.json",
      "packages/project-service/package.json",
      "packages/rule-schema-to-typescript-types/package.json",
      "packages/rule-tester/package.json",
      "packages/scope-manager/package.json",
      "packages/tsconfig-utils/package.json",
      "packages/type-utils/package.json",
      "packages/types/package.json",
      "packages/typescript-eslint/package.json",
      "packages/typescript-estree/package.json",
      "packages/utils/package.json",
      "packages/visitor-keys/package.json",
      "packages/website-eslint/package.json",
      "packages/website/package.json",
      "pnpm-lock.yaml",
      "pnpm-workspace.yaml"
    ],
    "gold_doc_category": "api_reference",
    "language": "typescript",
    "pred_confidence": 0.6291681896254376,
    "pred_doc_category": "configuration",
    "repository": "typescript-eslint/typescript-eslint",
    "source_url": "https://github.com/typescript-eslint/typescript-eslint/pull/12601",
    "top2": [
      "configuration",
      "api_reference"
    ]
  },
  {
    "case_id": "GH-CAND-0348",
    "code_changed_files": [
      "extensions/copilot/src/extension/tools/node/findTextInFilesTool.tsx"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.6286706603225329,
    "pred_doc_category": "developer_setup",
    "repository": "microsoft/vscode",
    "source_url": "https://github.com/microsoft/vscode/pull/324709",
    "top2": [
      "developer_setup",
      "model_contract"
    ]
  },
  {
    "case_id": "GH-CAND-0341",
    "code_changed_files": [
      "src/vs/sessions/contrib/sessions/browser/blockedSessionsList.ts",
      "src/vs/sessions/contrib/sessions/browser/sessionsTitleBarWidget.ts",
      "src/vs/sessions/contrib/sessions/browser/views/sessionsList.ts",
      "src/vs/workbench/test/browser/componentFixtures/sessions/sessionsTitleBarWidget.fixture.ts"
    ],
    "gold_doc_category": "model_contract",
    "language": "typescript",
    "pred_confidence": 0.6148175115218795,
    "pred_doc_category": "api_reference",
    "repository": "microsoft/vscode",
    "source_url": "https://github.com/microsoft/vscode/pull/324753",
    "top2": [
      "api_reference",
      "model_contract"
    ]
  },
  {
    "case_id": "GH-CAND-1075",
    "code_changed_files": [
      "common/changes/@microsoft/rush/pnpm11-relocate-global-settings_2026-06-18-11-15-37.json",
      "libraries/rush-lib/src/cli/RushPnpmCommandLineParser.ts",
      "libraries/rush-lib/src/cli/test/RushPnpmCommandLineParser.test.ts",
      "libraries/rush-lib/src/logic/installManager/InstallHelpers.ts",
      "libraries/rush-lib/src/logic/installManager/WorkspaceInstallManager.ts",
      "libraries/rush-lib/src/logic/pnpm/PnpmWorkspaceFile.ts",
      "libraries/rush-lib/src/logic/pnpm/test/PnpmWorkspaceFile.test.ts",
      "libraries/rush-lib/src/logic/test/InstallHelpers.test.ts",
      "libraries/rush-lib/src/logic/test/pnpmConfig/common/config/rush/pnpm-config.json",
      "libraries/rush-lib/src/logic/test/pnpmConfigPnpm11/common/config/rush/pnpm-config.json",
      "libraries/rush-lib/src/logic/test/pnpmConfigPnpm11/rush.json"
    ],
    "gold_doc_category": "api_reference",
    "language": "typescript",
    "pred_confidence": 0.6127703300747505,
    "pred_doc_category": "configuration",
    "repository": "microsoft/rushstack",
    "source_url": "https://github.com/microsoft/rushstack/pull/5838",
    "top2": [
      "configuration",
      "api_reference"
    ]
  },
  {
    "case_id": "GH-CAND-0429",
    "code_changed_files": [
      "extensions/copilot/src/extension/tools/node/editFileToolUtils.tsx",
      "extensions/copilot/src/extension/tools/node/readFileTool.tsx",
      "extensions/copilot/src/extension/tools/node/searchSubagentTool.ts",
      "extensions/copilot/src/extension/tools/node/test/searchSubagentTool.spec.ts",
      "extensions/copilot/src/extension/tools/node/test/toolUtils.spec.ts",
      "extensions/copilot/src/extension/tools/node/toolUtils.ts",
      "extensions/copilot/src/extension/tools/node/viewImageTool.tsx"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.6089721685734747,
    "pred_doc_category": "api_reference",
    "repository": "microsoft/vscode",
    "source_url": "https://github.com/microsoft/vscode/pull/331799",
    "top2": [
      "api_reference",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-0428",
    "code_changed_files": [
      "extensions/copilot/src/extension/tools/node/readFileTool.tsx",
      "extensions/copilot/src/extension/tools/node/searchSubagentTool.ts",
      "extensions/copilot/src/extension/tools/node/test/searchSubagentTool.spec.ts",
      "extensions/copilot/src/extension/tools/node/test/toolUtils.spec.ts",
      "extensions/copilot/src/extension/tools/node/toolUtils.ts",
      "extensions/copilot/src/extension/tools/node/viewImageTool.tsx",
      "extensions/copilot/src/platform/chat/common/chatDebugFileLoggerService.ts",
      "extensions/copilot/src/platform/chat/common/sessionTranscriptService.ts"
    ],
    "gold_doc_category": "model_contract",
    "language": "typescript",
    "pred_confidence": 0.6001928659707537,
    "pred_doc_category": "api_reference",
    "repository": "microsoft/vscode",
    "source_url": "https://github.com/microsoft/vscode/pull/331816",
    "top2": [
      "api_reference",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-8691",
    "code_changed_files": [
      "src/Appwrite/Platform/Modules/VCS/Http/GitHub/Deployment.php",
      "src/Appwrite/Vcs/CheckRuns.php",
      "tests/unit/Vcs/CheckRunsTest.php"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.5977543233649739,
    "pred_doc_category": "api_reference",
    "repository": "appwrite/appwrite",
    "source_url": "https://github.com/appwrite/appwrite/pull/13109",
    "top2": [
      "api_reference",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-3075",
    "code_changed_files": [
      "package.json",
      "packages/realtime-js/package-lock.json",
      "packages/realtime-js/package.json",
      "packages/realtime-js/src/Realtime.js",
      "packages/realtime-js/src/index.js",
      "packages/realtime-js/src/mapper.js",
      "packages/realtime-js/test/doctest_spec.js",
      "packages/realtime-js/test/index.js"
    ],
    "gold_doc_category": "model_contract",
    "language": "typescript",
    "pred_confidence": 0.5941948324521678,
    "pred_doc_category": "api_reference",
    "repository": "supabase/supabase",
    "source_url": "https://github.com/supabase/supabase/pull/1",
    "top2": [
      "api_reference",
      "model_contract"
    ]
  },
  {
    "case_id": "GH-CAND-6083",
    "code_changed_files": [
      ".cspell.json",
      "packages/typescript-eslint/package.json",
      "packages/typescript-eslint/src/globs.ts",
      "packages/typescript-eslint/src/index.ts",
      "packages/typescript-eslint/tests/globs.test.ts",
      "pnpm-lock.yaml"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.5890196786351346,
    "pred_doc_category": "api_reference",
    "repository": "typescript-eslint/typescript-eslint",
    "source_url": "https://github.com/typescript-eslint/typescript-eslint/pull/12105",
    "top2": [
      "api_reference",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-0425",
    "code_changed_files": [
      "src/vs/editor/contrib/inlineCompletions/browser/view/inlineEdits/components/gutterIndicatorView.ts",
      "src/vs/platform/hover/browser/hoverWidget.ts",
      "src/vs/sessions/browser/parts/mobile/contributions/mobileMultiDiffView.ts",
      "src/vs/workbench/browser/parts/notifications/notificationsToasts.ts",
      "src/vs/workbench/contrib/mergeEditor/browser/view/editorGutter.ts",
      "src/vs/workbench/contrib/notebook/browser/view/renderers/webviewPreloads.ts",
      "src/vs/workbench/contrib/terminal/browser/xterm/markNavigationAddon.ts"
    ],
    "gold_doc_category": "api_reference",
    "language": "typescript",
    "pred_confidence": 0.5739528133242925,
    "pred_doc_category": "model_contract",
    "repository": "microsoft/vscode",
    "source_url": "https://github.com/microsoft/vscode/pull/331918",
    "top2": [
      "model_contract",
      "api_reference"
    ]
  },
  {
    "case_id": "GH-CAND-0399",
    "code_changed_files": [
      "src/vs/platform/agentHost/common/agent.ts",
      "src/vs/platform/agentHost/common/state/sessionState.ts",
      "src/vs/platform/agentHost/node/agentHostStateManager.ts",
      "src/vs/platform/agentHost/node/agentService.ts",
      "src/vs/platform/agentHost/node/copilot/copilotAgent.ts",
      "src/vs/platform/agentHost/node/shared/worktreeIsolation.ts",
      "src/vs/platform/agentHost/test/node/agentHostStateManager.test.ts",
      "src/vs/platform/agentHost/test/node/agentService.test.ts",
      "src/vs/platform/agentHost/test/node/copilotAgent.test.ts",
      "src/vs/sessions/contrib/providers/agentHost/browser/localAgentHostSessionsProvider.ts",
      "src/vs/workbench/contrib/chat/browser/agentSessions/agentHost/agentHostLegacyMigration.ts",
      "src/vs/workbench/contrib/chat/browser/agentSessions/agentHost/agentHostSessionListStore.ts",
      "src/vs/workbench/contrib/chat/browser/agentSessions/agentSessionsOpener.ts",
      "src/vs/workbench/contrib/chat/browser/widgetHosts/editor/chatEditorInput.ts",
      "src/vs/workbench/contrib/chat/test/browser/agentSessions/agentHostChatContribution.test.ts",
      "src/vs/workbench/contrib/chat/test/browser/agentSessions/agentHostLegacyMigration.test.ts",
      "src/vs/workbench/contrib/chat/test/browser/agentSessions/agentSessionsOpener.test.ts",
      "src/vs/workbench/contrib/chat/test/browser/widgetHosts/editor/chatEditorInput.test.ts"
    ],
    "gold_doc_category": "model_contract",
    "language": "typescript",
    "pred_confidence": 0.5723267747808573,
    "pred_doc_category": "api_reference",
    "repository": "microsoft/vscode",
    "source_url": "https://github.com/microsoft/vscode/pull/331896",
    "top2": [
      "api_reference",
      "model_contract"
    ]
  },
  {
    "case_id": "GH-CAND-6054",
    "code_changed_files": [
      "packages/eslint-plugin/src/rules/no-empty-object-type.ts",
      "packages/eslint-plugin/tests/rules/no-empty-object-type.test.ts"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.5699264586069802,
    "pred_doc_category": "model_contract",
    "repository": "typescript-eslint/typescript-eslint",
    "source_url": "https://github.com/typescript-eslint/typescript-eslint/pull/12739",
    "top2": [
      "model_contract",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-2600",
    "code_changed_files": [
      "code/core/src/server-errors.ts",
      "code/frameworks/angular-vite/src/preset.test.ts",
      "code/frameworks/angular-vite/src/preset.ts"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.5664325462752877,
    "pred_doc_category": "api_reference",
    "repository": "storybookjs/storybook",
    "source_url": "https://github.com/storybookjs/storybook/pull/35998",
    "top2": [
      "api_reference",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-1099",
    "code_changed_files": [
      "common/changes/@microsoft/rush/copilot-pnpm11-allowbuilds-support_2026-06-04-01-00.json",
      "libraries/rush-lib/src/cli/RushPnpmCommandLineParser.ts",
      "libraries/rush-lib/src/logic/installManager/InstallHelpers.ts",
      "libraries/rush-lib/src/logic/installManager/WorkspaceInstallManager.ts",
      "libraries/rush-lib/src/logic/pnpm/PnpmOptionsConfiguration.ts",
      "libraries/rush-lib/src/logic/pnpm/PnpmWorkspaceFile.ts",
      "libraries/rush-lib/src/logic/pnpm/test/PnpmOptionsConfiguration.test.ts",
      "libraries/rush-lib/src/logic/pnpm/test/PnpmWorkspaceFile.test.ts",
      "libraries/rush-lib/src/logic/pnpm/test/jsonFiles/pnpm-config-allowBuilds.json",
      "libraries/rush-lib/src/schemas/pnpm-config.schema.json"
    ],
    "gold_doc_category": "api_reference",
    "language": "typescript",
    "pred_confidence": 0.5647117795718677,
    "pred_doc_category": "configuration",
    "repository": "microsoft/rushstack",
    "source_url": "https://github.com/microsoft/rushstack/pull/5817",
    "top2": [
      "configuration",
      "api_reference"
    ]
  },
  {
    "case_id": "GH-CAND-6062",
    "code_changed_files": [
      "packages/ast-spec/package.json",
      "packages/eslint-plugin/package.json",
      "packages/parser/package.json",
      "packages/project-service/package.json",
      "packages/rule-schema-to-typescript-types/package.json",
      "packages/rule-tester/package.json",
      "packages/scope-manager/package.json",
      "packages/tsconfig-utils/package.json",
      "packages/type-utils/package.json",
      "packages/types/package.json",
      "packages/typescript-eslint/package.json",
      "packages/typescript-estree/package.json",
      "packages/typescript-estree/tsconfig.build.json",
      "packages/utils/package.json",
      "packages/visitor-keys/package.json",
      "packages/website-eslint/package.json",
      "tsconfig.base.json"
    ],
    "gold_doc_category": "model_contract",
    "language": "typescript",
    "pred_confidence": 0.5582028852889379,
    "pred_doc_category": "configuration",
    "repository": "typescript-eslint/typescript-eslint",
    "source_url": "https://github.com/typescript-eslint/typescript-eslint/pull/12677",
    "top2": [
      "configuration",
      "model_contract"
    ]
  }
]
```

## train

- total: `2127`
- accuracy: `0.9690`
- top-2 accuracy: `0.9981`
- errors: `66`

### Gold distribution

```json
{
  "api_reference": 730,
  "configuration": 523,
  "developer_setup": 342,
  "model_contract": 532
}
```

### Predicted distribution

```json
{
  "api_reference": 693,
  "configuration": 505,
  "developer_setup": 387,
  "model_contract": 542
}
```

### Per-class metrics

```json
{
  "api_reference": {
    "f1": 0.9739985945186227,
    "fn": 37,
    "fp": 0,
    "precision": 1.0,
    "predicted": 693,
    "recall": 0.9493150684931507,
    "support": 730,
    "tp": 693
  },
  "configuration": {
    "f1": 0.9708171206225681,
    "fn": 24,
    "fp": 6,
    "precision": 0.9881188118811881,
    "predicted": 505,
    "recall": 0.9541108986615678,
    "support": 523,
    "tp": 499
  },
  "developer_setup": {
    "f1": 0.9382716049382717,
    "fn": 0,
    "fp": 45,
    "precision": 0.8837209302325582,
    "predicted": 387,
    "recall": 1.0,
    "support": 342,
    "tp": 342
  },
  "model_contract": {
    "f1": 0.9813780260707635,
    "fn": 5,
    "fp": 15,
    "precision": 0.9723247232472325,
    "predicted": 542,
    "recall": 0.9906015037593985,
    "support": 532,
    "tp": 527
  }
}
```

### Most common confusion pairs

```json
{
  "api_reference -> configuration": 6,
  "api_reference -> developer_setup": 22,
  "api_reference -> model_contract": 9,
  "configuration -> developer_setup": 18,
  "configuration -> model_contract": 6,
  "model_contract -> developer_setup": 5
}
```

### Error confidence buckets

```json
{
  "0.00-0.40": 6,
  "0.40-0.50": 30,
  "0.50-0.60": 21,
  "0.60-0.70": 5,
  "0.70-0.80": 4,
  "0.80-1.00": 0,
  "missing": 0
}
```

### High-confidence errors

```json
[
  {
    "case_id": "GH-CAND-6030",
    "code_changed_files": [
      "website/package.json"
    ],
    "gold_doc_category": "api_reference",
    "language": "typescript",
    "pred_confidence": 0.792770556452965,
    "pred_doc_category": "developer_setup",
    "repository": "prettier/prettier",
    "source_url": "https://github.com/prettier/prettier/pull/19679",
    "top2": [
      "developer_setup",
      "api_reference"
    ]
  },
  {
    "case_id": "GH-CAND-6007",
    "code_changed_files": [
      "website/package.json"
    ],
    "gold_doc_category": "api_reference",
    "language": "typescript",
    "pred_confidence": 0.7791018229084309,
    "pred_doc_category": "developer_setup",
    "repository": "prettier/prettier",
    "source_url": "https://github.com/prettier/prettier/pull/19715",
    "top2": [
      "developer_setup",
      "api_reference"
    ]
  },
  {
    "case_id": "GH-CAND-4782",
    "code_changed_files": [
      "packages/router/src/router.ts"
    ],
    "gold_doc_category": "api_reference",
    "language": "typescript",
    "pred_confidence": 0.7457181254872405,
    "pred_doc_category": "developer_setup",
    "repository": "vuejs/router",
    "source_url": "https://github.com/vuejs/router/pull/1910",
    "top2": [
      "developer_setup",
      "api_reference"
    ]
  },
  {
    "case_id": "GH-CAND-8474",
    "code_changed_files": [
      "apps/v4/registry/directory.json"
    ],
    "gold_doc_category": "api_reference",
    "language": "typescript",
    "pred_confidence": 0.733761107754517,
    "pred_doc_category": "developer_setup",
    "repository": "shadcn-ui/ui",
    "source_url": "https://github.com/shadcn-ui/ui/pull/10998",
    "top2": [
      "developer_setup",
      "api_reference"
    ]
  },
  {
    "case_id": "GH-CAND-4631",
    "code_changed_files": [
      "pnpm-workspace.yaml"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.6698344350933899,
    "pred_doc_category": "developer_setup",
    "repository": "vuejs/core",
    "source_url": "https://github.com/vuejs/core/pull/15243",
    "top2": [
      "developer_setup",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-6023",
    "code_changed_files": [
      "package.json"
    ],
    "gold_doc_category": "model_contract",
    "language": "typescript",
    "pred_confidence": 0.6609784304420192,
    "pred_doc_category": "developer_setup",
    "repository": "prettier/prettier",
    "source_url": "https://github.com/prettier/prettier/pull/19685",
    "top2": [
      "developer_setup",
      "model_contract"
    ]
  },
  {
    "case_id": "GH-CAND-8487",
    "code_changed_files": [
      "apps/v4/registry/directory.json"
    ],
    "gold_doc_category": "api_reference",
    "language": "typescript",
    "pred_confidence": 0.6468128608233998,
    "pred_doc_category": "developer_setup",
    "repository": "shadcn-ui/ui",
    "source_url": "https://github.com/shadcn-ui/ui/pull/11122",
    "top2": [
      "developer_setup",
      "api_reference"
    ]
  },
  {
    "case_id": "GH-CAND-4811",
    "code_changed_files": [
      "packages/router/__tests__/router.spec.ts",
      "packages/router/src/router.ts"
    ],
    "gold_doc_category": "api_reference",
    "language": "typescript",
    "pred_confidence": 0.643521072205754,
    "pred_doc_category": "developer_setup",
    "repository": "vuejs/router",
    "source_url": "https://github.com/vuejs/router/pull/2157",
    "top2": [
      "developer_setup",
      "api_reference"
    ]
  },
  {
    "case_id": "GH-CAND-8052",
    "code_changed_files": [
      "pnpm-workspace.yaml"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.629716365276014,
    "pred_doc_category": "developer_setup",
    "repository": "TanStack/router",
    "source_url": "https://github.com/TanStack/router/pull/7810",
    "top2": [
      "developer_setup",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-8379",
    "code_changed_files": [
      "package.json"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.5916885420747133,
    "pred_doc_category": "developer_setup",
    "repository": "ant-design/ant-design",
    "source_url": "https://github.com/ant-design/ant-design/pull/58993",
    "top2": [
      "developer_setup",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-8473",
    "code_changed_files": [
      "apps/v4/registry/directory.json"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.581887357064474,
    "pred_doc_category": "developer_setup",
    "repository": "shadcn-ui/ui",
    "source_url": "https://github.com/shadcn-ui/ui/pull/11516",
    "top2": [
      "developer_setup",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-5979",
    "code_changed_files": [
      "package.json"
    ],
    "gold_doc_category": "api_reference",
    "language": "typescript",
    "pred_confidence": 0.5659996445288114,
    "pred_doc_category": "developer_setup",
    "repository": "prettier/prettier",
    "source_url": "https://github.com/prettier/prettier/pull/19773",
    "top2": [
      "developer_setup",
      "model_contract"
    ]
  },
  {
    "case_id": "GH-CAND-8524",
    "code_changed_files": [
      "apps/v4/registry/directory.json"
    ],
    "gold_doc_category": "api_reference",
    "language": "typescript",
    "pred_confidence": 0.5619636826925583,
    "pred_doc_category": "developer_setup",
    "repository": "shadcn-ui/ui",
    "source_url": "https://github.com/shadcn-ui/ui/pull/11299",
    "top2": [
      "developer_setup",
      "api_reference"
    ]
  },
  {
    "case_id": "GH-CAND-4441",
    "code_changed_files": [
      "package.json",
      "renovate.json"
    ],
    "gold_doc_category": "api_reference",
    "language": "typescript",
    "pred_confidence": 0.5607960469238492,
    "pred_doc_category": "model_contract",
    "repository": "angular/angular",
    "source_url": "https://github.com/angular/angular/pull/66420",
    "top2": [
      "model_contract",
      "api_reference"
    ]
  },
  {
    "case_id": "GH-CAND-4980",
    "code_changed_files": [
      "packages/svelte/package.json",
      "packages/svelte/src/version.js"
    ],
    "gold_doc_category": "api_reference",
    "language": "typescript",
    "pred_confidence": 0.5518194991142749,
    "pred_doc_category": "model_contract",
    "repository": "sveltejs/svelte",
    "source_url": "https://github.com/sveltejs/svelte/pull/18640",
    "top2": [
      "model_contract",
      "api_reference"
    ]
  },
  {
    "case_id": "GH-CAND-5960",
    "code_changed_files": [
      "package.json",
      "scripts/build/hacks/build-oxc-wasm-parser.js"
    ],
    "gold_doc_category": "model_contract",
    "language": "typescript",
    "pred_confidence": 0.5505819432070024,
    "pred_doc_category": "developer_setup",
    "repository": "prettier/prettier",
    "source_url": "https://github.com/prettier/prettier/pull/19830",
    "top2": [
      "developer_setup",
      "model_contract"
    ]
  },
  {
    "case_id": "GH-CAND-8546",
    "code_changed_files": [
      "apps/v4/package.json",
      "packages/shadcn/package.json",
      "pnpm-lock.yaml"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.5498643014011754,
    "pred_doc_category": "developer_setup",
    "repository": "shadcn-ui/ui",
    "source_url": "https://github.com/shadcn-ui/ui/pull/11244",
    "top2": [
      "developer_setup",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-5814",
    "code_changed_files": [
      "package.json"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.5459952658584071,
    "pred_doc_category": "developer_setup",
    "repository": "eslint/eslint",
    "source_url": "https://github.com/eslint/eslint/pull/21077",
    "top2": [
      "developer_setup",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-8476",
    "code_changed_files": [
      "apps/v4/package.json",
      "packages/shadcn/package.json",
      "pnpm-lock.yaml"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.5458430372559249,
    "pred_doc_category": "developer_setup",
    "repository": "shadcn-ui/ui",
    "source_url": "https://github.com/shadcn-ui/ui/pull/11286",
    "top2": [
      "developer_setup",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-8529",
    "code_changed_files": [
      "apps/v4/package.json",
      "packages/shadcn/package.json",
      "pnpm-lock.yaml"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.54219481203645,
    "pred_doc_category": "developer_setup",
    "repository": "shadcn-ui/ui",
    "source_url": "https://github.com/shadcn-ui/ui/pull/11306",
    "top2": [
      "developer_setup",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-5893",
    "code_changed_files": [
      "package.json"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.5393600091544853,
    "pred_doc_category": "developer_setup",
    "repository": "eslint/eslint",
    "source_url": "https://github.com/eslint/eslint/pull/21042",
    "top2": [
      "developer_setup",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-8534",
    "code_changed_files": [
      "apps/v4/registry/directory.json"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.5390356606164045,
    "pred_doc_category": "developer_setup",
    "repository": "shadcn-ui/ui",
    "source_url": "https://github.com/shadcn-ui/ui/pull/11290",
    "top2": [
      "developer_setup",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-8491",
    "code_changed_files": [
      "apps/v4/registry/directory.json"
    ],
    "gold_doc_category": "model_contract",
    "language": "typescript",
    "pred_confidence": 0.5321980390533283,
    "pred_doc_category": "developer_setup",
    "repository": "shadcn-ui/ui",
    "source_url": "https://github.com/shadcn-ui/ui/pull/11220",
    "top2": [
      "developer_setup",
      "model_contract"
    ]
  },
  {
    "case_id": "GH-CAND-8525",
    "code_changed_files": [
      "apps/v4/registry/directory.json"
    ],
    "gold_doc_category": "model_contract",
    "language": "typescript",
    "pred_confidence": 0.5309273392275773,
    "pred_doc_category": "developer_setup",
    "repository": "shadcn-ui/ui",
    "source_url": "https://github.com/shadcn-ui/ui/pull/11324",
    "top2": [
      "developer_setup",
      "model_contract"
    ]
  },
  {
    "case_id": "GH-CAND-5869",
    "code_changed_files": [
      "package.json"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.5291532709612714,
    "pred_doc_category": "developer_setup",
    "repository": "eslint/eslint",
    "source_url": "https://github.com/eslint/eslint/pull/21076",
    "top2": [
      "developer_setup",
      "configuration"
    ]
  }
]
```

## validation

- total: `510`
- accuracy: `0.6765`
- top-2 accuracy: `0.8510`
- errors: `165`

### Gold distribution

```json
{
  "api_reference": 163,
  "configuration": 201,
  "developer_setup": 73,
  "model_contract": 73
}
```

### Predicted distribution

```json
{
  "api_reference": 200,
  "configuration": 176,
  "developer_setup": 59,
  "model_contract": 75
}
```

### Per-class metrics

```json
{
  "api_reference": {
    "f1": 0.7217630853994491,
    "fn": 32,
    "fp": 69,
    "precision": 0.655,
    "predicted": 200,
    "recall": 0.803680981595092,
    "support": 163,
    "tp": 131
  },
  "configuration": {
    "f1": 0.7320954907161804,
    "fn": 63,
    "fp": 38,
    "precision": 0.7840909090909091,
    "predicted": 176,
    "recall": 0.6865671641791045,
    "support": 201,
    "tp": 138
  },
  "developer_setup": {
    "f1": 0.5303030303030303,
    "fn": 38,
    "fp": 24,
    "precision": 0.5932203389830508,
    "predicted": 59,
    "recall": 0.4794520547945205,
    "support": 73,
    "tp": 35
  },
  "model_contract": {
    "f1": 0.5540540540540541,
    "fn": 32,
    "fp": 34,
    "precision": 0.5466666666666666,
    "predicted": 75,
    "recall": 0.5616438356164384,
    "support": 73,
    "tp": 41
  }
}
```

### Most common confusion pairs

```json
{
  "api_reference -> configuration": 15,
  "api_reference -> developer_setup": 5,
  "api_reference -> model_contract": 12,
  "configuration -> api_reference": 42,
  "configuration -> developer_setup": 12,
  "configuration -> model_contract": 9,
  "developer_setup -> api_reference": 14,
  "developer_setup -> configuration": 11,
  "developer_setup -> model_contract": 13,
  "model_contract -> api_reference": 13,
  "model_contract -> configuration": 12,
  "model_contract -> developer_setup": 7
}
```

### Error confidence buckets

```json
{
  "0.00-0.40": 69,
  "0.40-0.50": 51,
  "0.50-0.60": 25,
  "0.60-0.70": 14,
  "0.70-0.80": 4,
  "0.80-1.00": 2,
  "missing": 0
}
```

### High-confidence errors

```json
[
  {
    "case_id": "GH-CAND-8875",
    "code_changed_files": [
      "packages/payload/src/uploads/checkFileAccess.spec.ts",
      "packages/payload/src/uploads/checkFileAccess.ts",
      "packages/payload/src/uploads/endpoints/getFile.ts",
      "packages/payload/src/uploads/types.ts",
      "packages/plugin-cloud-storage/src/hooks/afterRead.ts",
      "packages/plugin-cloud-storage/src/types.ts",
      "packages/plugin-cloud-storage/src/utilities/getFilePrefix.spec.ts",
      "packages/plugin-cloud-storage/src/utilities/getFilePrefix.ts",
      "packages/storage-azure/src/staticHandler.ts",
      "packages/storage-gcs/src/staticHandler.ts",
      "packages/storage-r2/src/staticHandler.ts",
      "packages/storage-s3/src/staticHandler.ts",
      "packages/storage-vercel-blob/src/staticHandler.ts",
      "packages/ui/src/elements/EditUpload/index.tsx",
      "packages/ui/src/elements/PreviewSizes/index.tsx",
      "test/plugin-cloud-storage/int.spec.ts",
      "test/storage-azure/int.spec.ts",
      "test/storage-azure/streamingUploads.int.spec.ts",
      "test/storage-s3/int.spec.ts",
      "test/storage-vercel-blob/int.spec.ts",
      "test/uploads/config.ts",
      "test/uploads/int.spec.ts",
      "test/uploads/payload-types.ts",
      "test/uploads/shared.ts"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.8281036455733275,
    "pred_doc_category": "api_reference",
    "repository": "payloadcms/payload",
    "source_url": "https://github.com/payloadcms/payload/pull/15844",
    "top2": [
      "api_reference",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-0124",
    "code_changed_files": [
      "schemas/agent-approval.schema.json",
      "schemas/organization.schema.json",
      "src/agent-source.test.ts",
      "src/agent-source.ts",
      "src/consolidate.test.ts",
      "src/consolidate.ts",
      "src/validate.test.ts",
      "src/validate.ts",
      "vendors.json",
      "website/src/components/AgentDetail.tsx",
      "website/src/components/AgentList.tsx",
      "website/src/components/OrgList.tsx",
      "website/src/filterArtifacts.ts",
      "website/src/hooks/useRegistryData.ts",
      "website/src/pages/AboutPage.tsx",
      "website/src/pages/ApiDocsPage.tsx",
      "website/src/pages/HomePage.tsx",
      "website/src/pages/ToolPage.tsx",
      "website/src/types.ts"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.8251142915042121,
    "pred_doc_category": "api_reference",
    "repository": "eclipsefdn-ai-registry/ai-registry-core",
    "source_url": "https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/78",
    "top2": [
      "api_reference",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-6643",
    "code_changed_files": [
      "ext/node/polyfills/_http_client.js",
      "tests/unit_node/http_test.ts",
      "tests/unit_node/perf_hooks_test.ts"
    ],
    "gold_doc_category": "model_contract",
    "language": "typescript",
    "pred_confidence": 0.7443778852564501,
    "pred_doc_category": "api_reference",
    "repository": "denoland/deno",
    "source_url": "https://github.com/denoland/deno/pull/36557",
    "top2": [
      "api_reference",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-0130",
    "code_changed_files": [
      "schemas/mcp-approval.schema.json",
      "src/consolidate.test.ts",
      "src/consolidate.ts",
      "website/src/components/McpVerificationBadge.tsx",
      "website/src/components/ServerDetail.tsx",
      "website/src/components/ServerList.tsx",
      "website/src/pages/ToolPage.tsx",
      "website/src/types.ts"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.7291962544001208,
    "pred_doc_category": "api_reference",
    "repository": "eclipsefdn-ai-registry/ai-registry-core",
    "source_url": "https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/62",
    "top2": [
      "api_reference",
      "model_contract"
    ]
  },
  {
    "case_id": "GH-CAND-2130",
    "code_changed_files": [
      "Cargo.toml",
      "crates/next-core/src/emit.rs",
      "crates/next-napi-bindings/src/next_api/project.rs",
      "turbopack/crates/turbo-tasks-fs/Cargo.toml",
      "turbopack/crates/turbo-tasks-fs/src/content.rs",
      "turbopack/crates/turbo-tasks-fs/src/disk.rs",
      "turbopack/crates/turbo-tasks-fs/src/embed/fs.rs",
      "turbopack/crates/turbo-tasks-fs/src/lib.rs",
      "turbopack/crates/turbo-tasks-fs/src/null_fs.rs",
      "turbopack/crates/turbo-tasks-fs/src/path.rs",
      "turbopack/crates/turbo-tasks-fs/src/read_glob.rs",
      "turbopack/crates/turbo-tasks-fs/src/virtual_fs.rs",
      "turbopack/crates/turbo-tasks-fs/src/windows.rs",
      "turbopack/crates/turbo-tasks-fuzz/src/fs_watcher.rs",
      "turbopack/crates/turbo-tasks-fuzz/src/symlink_stress.rs",
      "turbopack/crates/turbo-tasks-macros/src/derive/deterministic_hash_macro.rs",
      "turbopack/crates/turbo-unix-path/src/lib.rs",
      "turbopack/crates/turbopack-core/src/asset.rs",
      "turbopack/crates/turbopack-core/src/file_source.rs",
      "turbopack/crates/turbopack-core/src/introspect/utils.rs",
      "turbopack/crates/turbopack-core/src/resolve/pattern.rs",
      "turbopack/crates/turbopack-core/src/server_fs.rs",
      "turbopack/crates/turbopack-core/src/version.rs",
      "turbopack/crates/turbopack-css/src/process.rs",
      "turbopack/crates/turbopack-ecmascript/src/parse.rs",
      "turbopack/crates/turbopack-ecmascript/src/references/external_module.rs",
      "turbopack/crates/turbopack-test-utils/src/snapshot.rs"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.7284915836599412,
    "pred_doc_category": "api_reference",
    "repository": "vercel/next.js",
    "source_url": "https://github.com/vercel/next.js/pull/97395",
    "top2": [
      "api_reference",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-0128",
    "code_changed_files": [
      "src/consolidate.test.ts",
      "src/consolidate.ts",
      "website/src/components/McpVerificationBadge.tsx",
      "website/src/types.ts"
    ],
    "gold_doc_category": "model_contract",
    "language": "typescript",
    "pred_confidence": 0.7149157899817719,
    "pred_doc_category": "api_reference",
    "repository": "eclipsefdn-ai-registry/ai-registry-core",
    "source_url": "https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/63",
    "top2": [
      "api_reference",
      "model_contract"
    ]
  },
  {
    "case_id": "GH-CAND-0121",
    "code_changed_files": [
      "schemas/organization.schema.json",
      "src/consolidate.test.ts",
      "src/consolidate.ts",
      "src/validate.test.ts",
      "website/src/types.ts"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.675373033225946,
    "pred_doc_category": "api_reference",
    "repository": "eclipsefdn-ai-registry/ai-registry-core",
    "source_url": "https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/88",
    "top2": [
      "api_reference",
      "model_contract"
    ]
  },
  {
    "case_id": "GH-CAND-2118",
    "code_changed_files": [
      "Cargo.toml",
      "turbopack/crates/turbo-tasks-backend/src/backend/mod.rs",
      "turbopack/crates/turbo-tasks-backend/src/backend/operation/connect_children.rs",
      "turbopack/crates/turbo-tasks/Cargo.toml",
      "turbopack/crates/turbo-tasks/src/lib.rs",
      "turbopack/crates/turbo-tasks/src/parallel.rs",
      "turbopack/crates/turbo-tasks/src/scope_bounded.rs",
      "turbopack/crates/turbo-tasks/src/scope_unbounded.rs"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.6658510680772364,
    "pred_doc_category": "api_reference",
    "repository": "vercel/next.js",
    "source_url": "https://github.com/vercel/next.js/pull/95974",
    "top2": [
      "api_reference",
      "model_contract"
    ]
  },
  {
    "case_id": "GH-CAND-0146",
    "code_changed_files": [
      "schemas/organization.schema.json",
      "src/consolidate.test.ts",
      "src/consolidate.ts",
      "src/validate.test.ts",
      "website/src/components/OrgList.tsx",
      "website/src/components/ServerDetail.tsx",
      "website/src/components/ServerList.tsx",
      "website/src/components/SkillDetail.tsx",
      "website/src/components/SkillList.tsx",
      "website/src/orgBadge.ts",
      "website/src/pages/ToolPage.tsx",
      "website/src/types.ts"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.6633091049058478,
    "pred_doc_category": "api_reference",
    "repository": "eclipsefdn-ai-registry/ai-registry-core",
    "source_url": "https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/29",
    "top2": [
      "api_reference",
      "model_contract"
    ]
  },
  {
    "case_id": "GH-CAND-0149",
    "code_changed_files": [
      "package-lock.json",
      "package.json",
      "src/skill-source.test.ts",
      "src/skill-source.ts",
      "website/package-lock.json",
      "website/package.json",
      "website/src/components/OrgList.tsx",
      "website/src/components/ServerDetail.tsx",
      "website/src/components/SkillDetail.tsx",
      "website/src/pages/ToolPage.tsx",
      "website/src/sanitize.ts"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.6519767181189816,
    "pred_doc_category": "api_reference",
    "repository": "eclipsefdn-ai-registry/ai-registry-core",
    "source_url": "https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/20",
    "top2": [
      "api_reference",
      "developer_setup"
    ]
  },
  {
    "case_id": "GH-CAND-8238",
    "code_changed_files": [
      "apps/www/components/announcement.tsx",
      "apps/www/components/site/hero.section.tsx"
    ],
    "gold_doc_category": "api_reference",
    "language": "typescript",
    "pred_confidence": 0.6473361178737853,
    "pred_doc_category": "developer_setup",
    "repository": "chakra-ui/chakra-ui",
    "source_url": "https://github.com/chakra-ui/chakra-ui/pull/10849",
    "top2": [
      "developer_setup",
      "model_contract"
    ]
  },
  {
    "case_id": "GH-CAND-8273",
    "code_changed_files": [
      "packages/cli/package.json",
      "pnpm-lock.yaml"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.6392973758537961,
    "pred_doc_category": "developer_setup",
    "repository": "chakra-ui/chakra-ui",
    "source_url": "https://github.com/chakra-ui/chakra-ui/pull/10540",
    "top2": [
      "developer_setup",
      "model_contract"
    ]
  },
  {
    "case_id": "GH-CAND-8302",
    "code_changed_files": [
      "apps/www/package.json",
      "package.json",
      "packages/charts/package.json",
      "packages/react/package.json",
      "pnpm-lock.yaml",
      "sandbox/storybook-ts/package.json"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.6346664210318886,
    "pred_doc_category": "developer_setup",
    "repository": "chakra-ui/chakra-ui",
    "source_url": "https://github.com/chakra-ui/chakra-ui/pull/10614",
    "top2": [
      "developer_setup",
      "model_contract"
    ]
  },
  {
    "case_id": "GH-CAND-8250",
    "code_changed_files": [
      "apps/www/package.json",
      "package.json",
      "packages/charts/package.json",
      "packages/react/package.json",
      "pnpm-lock.yaml",
      "sandbox/storybook-ts/package.json"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.6323072299613494,
    "pred_doc_category": "developer_setup",
    "repository": "chakra-ui/chakra-ui",
    "source_url": "https://github.com/chakra-ui/chakra-ui/pull/10811",
    "top2": [
      "developer_setup",
      "model_contract"
    ]
  },
  {
    "case_id": "GH-CAND-0148",
    "code_changed_files": [
      "schemas/mcp-approval.schema.json",
      "schemas/organization.schema.json",
      "schemas/skill-approval.schema.json",
      "src/consolidate.test.ts",
      "src/consolidate.ts",
      "src/validate.test.ts",
      "src/validate.ts"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.6291512597238256,
    "pred_doc_category": "api_reference",
    "repository": "eclipsefdn-ai-registry/ai-registry-core",
    "source_url": "https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/19",
    "top2": [
      "api_reference",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-8264",
    "code_changed_files": [
      "apps/www/package.json",
      "package.json",
      "packages/charts/package.json",
      "packages/react/package.json",
      "pnpm-lock.yaml",
      "sandbox/storybook-ts/package.json"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.6256201529329296,
    "pred_doc_category": "developer_setup",
    "repository": "chakra-ui/chakra-ui",
    "source_url": "https://github.com/chakra-ui/chakra-ui/pull/10777",
    "top2": [
      "developer_setup",
      "model_contract"
    ]
  },
  {
    "case_id": "GH-CAND-0136",
    "code_changed_files": [
      "src/consolidate.test.ts",
      "src/consolidate.ts",
      "src/validate.test.ts",
      "src/validate.ts"
    ],
    "gold_doc_category": "model_contract",
    "language": "typescript",
    "pred_confidence": 0.6169960418387265,
    "pred_doc_category": "api_reference",
    "repository": "eclipsefdn-ai-registry/ai-registry-core",
    "source_url": "https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/43",
    "top2": [
      "api_reference",
      "model_contract"
    ]
  },
  {
    "case_id": "GH-CAND-0147",
    "code_changed_files": [
      "schemas/skill-approval.schema.json",
      "src/consolidate.test.ts",
      "src/consolidate.ts",
      "src/skill-source.test.ts",
      "src/skill-source.ts",
      "src/validate.test.ts",
      "src/validate.ts"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.6105177930059719,
    "pred_doc_category": "api_reference",
    "repository": "eclipsefdn-ai-registry/ai-registry-core",
    "source_url": "https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/25",
    "top2": [
      "api_reference",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-8319",
    "code_changed_files": [
      "packages/react/src/components/image/image.tsx"
    ],
    "gold_doc_category": "model_contract",
    "language": "typescript",
    "pred_confidence": 0.6100139068858444,
    "pred_doc_category": "developer_setup",
    "repository": "chakra-ui/chakra-ui",
    "source_url": "https://github.com/chakra-ui/chakra-ui/pull/10541",
    "top2": [
      "developer_setup",
      "model_contract"
    ]
  },
  {
    "case_id": "GH-CAND-2115",
    "code_changed_files": [
      "Cargo.toml",
      "turbopack/crates/turbo-tasks-fs/src/watcher/mod.rs"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.6062726927353529,
    "pred_doc_category": "api_reference",
    "repository": "vercel/next.js",
    "source_url": "https://github.com/vercel/next.js/pull/97655",
    "top2": [
      "api_reference",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-0145",
    "code_changed_files": [
      "website/src/components/OrgList.tsx",
      "website/src/pages/HomePage.tsx"
    ],
    "gold_doc_category": "model_contract",
    "language": "typescript",
    "pred_confidence": 0.5927680285180407,
    "pred_doc_category": "api_reference",
    "repository": "eclipsefdn-ai-registry/ai-registry-core",
    "source_url": "https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/30",
    "top2": [
      "api_reference",
      "model_contract"
    ]
  },
  {
    "case_id": "GH-CAND-0809",
    "code_changed_files": [
      "playground/src/samples/basicSample.ts"
    ],
    "gold_doc_category": "developer_setup",
    "language": "typescript",
    "pred_confidence": 0.5889856032340725,
    "pred_doc_category": "model_contract",
    "repository": "microsoft/tsdoc",
    "source_url": "https://github.com/microsoft/tsdoc/pull/441",
    "top2": [
      "model_contract",
      "developer_setup"
    ]
  },
  {
    "case_id": "GH-CAND-8242",
    "code_changed_files": [
      "packages/react/src/components/for/for.tsx"
    ],
    "gold_doc_category": "model_contract",
    "language": "typescript",
    "pred_confidence": 0.5859131657432458,
    "pred_doc_category": "developer_setup",
    "repository": "chakra-ui/chakra-ui",
    "source_url": "https://github.com/chakra-ui/chakra-ui/pull/10842",
    "top2": [
      "developer_setup",
      "model_contract"
    ]
  },
  {
    "case_id": "GH-CAND-0143",
    "code_changed_files": [
      "schemas/organization.schema.json",
      "src/consolidate.test.ts",
      "src/consolidate.ts"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.5795202555472572,
    "pred_doc_category": "api_reference",
    "repository": "eclipsefdn-ai-registry/ai-registry-core",
    "source_url": "https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/31",
    "top2": [
      "api_reference",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-8258",
    "code_changed_files": [
      "apps/www/docs.config.ts"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.5779700730268702,
    "pred_doc_category": "api_reference",
    "repository": "chakra-ui/chakra-ui",
    "source_url": "https://github.com/chakra-ui/chakra-ui/pull/10794",
    "top2": [
      "api_reference",
      "configuration"
    ]
  }
]
```
