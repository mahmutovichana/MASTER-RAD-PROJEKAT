# Category Classifier Error Analysis

This report analyzes classifier errors only. It does not change predictions, labels, or model selection.

## locked_test

- total: `395`
- accuracy: `0.6835`
- top-2 accuracy: `0.8658`
- errors: `125`

### Gold distribution

```json
{
  "api_reference": 134,
  "configuration": 108,
  "developer_setup": 63,
  "model_contract": 90
}
```

### Predicted distribution

```json
{
  "api_reference": 145,
  "configuration": 87,
  "developer_setup": 64,
  "model_contract": 99
}
```

### Per-class metrics

```json
{
  "api_reference": {
    "f1": 0.7670250896057349,
    "fn": 27,
    "fp": 38,
    "precision": 0.7379310344827587,
    "predicted": 145,
    "recall": 0.7985074626865671,
    "support": 134,
    "tp": 107
  },
  "configuration": {
    "f1": 0.6666666666666667,
    "fn": 43,
    "fp": 22,
    "precision": 0.7471264367816092,
    "predicted": 87,
    "recall": 0.6018518518518519,
    "support": 108,
    "tp": 65
  },
  "developer_setup": {
    "f1": 0.5984251968503936,
    "fn": 25,
    "fp": 26,
    "precision": 0.59375,
    "predicted": 64,
    "recall": 0.6031746031746031,
    "support": 63,
    "tp": 38
  },
  "model_contract": {
    "f1": 0.6349206349206349,
    "fn": 30,
    "fp": 39,
    "precision": 0.6060606060606061,
    "predicted": 99,
    "recall": 0.6666666666666666,
    "support": 90,
    "tp": 60
  }
}
```

### Most common confusion pairs

```json
{
  "api_reference -> configuration": 10,
  "api_reference -> developer_setup": 8,
  "api_reference -> model_contract": 9,
  "configuration -> api_reference": 16,
  "configuration -> developer_setup": 9,
  "configuration -> model_contract": 18,
  "developer_setup -> api_reference": 5,
  "developer_setup -> configuration": 8,
  "developer_setup -> model_contract": 12,
  "model_contract -> api_reference": 17,
  "model_contract -> configuration": 4,
  "model_contract -> developer_setup": 9
}
```

### Error confidence buckets

```json
{
  "0.00-0.40": 19,
  "0.40-0.50": 22,
  "0.50-0.60": 26,
  "0.60-0.70": 27,
  "0.70-0.80": 15,
  "0.80-1.00": 16,
  "missing": 0
}
```

### High-confidence errors

```json
[
  {
    "case_id": "GH-CAND-0622",
    "code_changed_files": [
      "src/compiler/checker.ts",
      "src/services/stringCompletions.ts",
      "tests/cases/conformance/es6/yieldExpressions/generatorTypeCheck64.ts",
      "tests/cases/fourslash/stringLiteralCompletionsWithinInferredObjectWhenItsKeysAreUsedOutsideOfIt.ts",
      "tests/cases/fourslash/typeErrorAfterStringCompletionsInNestedCall.ts"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.9097023489472389,
    "pred_doc_category": "model_contract",
    "repository": "microsoft/TypeScript",
    "source_url": "https://github.com/microsoft/TypeScript/pull/56182",
    "top2": [
      "model_contract",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-7985",
    "code_changed_files": [
      "packages/router-core/src/router.ts",
      "packages/router-core/tests/build-location.test.ts"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.9077376173084688,
    "pred_doc_category": "api_reference",
    "repository": "TanStack/router",
    "source_url": "https://github.com/TanStack/router/pull/8110",
    "top2": [
      "api_reference",
      "developer_setup"
    ]
  },
  {
    "case_id": "GH-CAND-1014",
    "code_changed_files": [
      "change/@fluentui-web-components-66ae5150-e0b3-4a9f-a60f-82d4d6fbf79c.json"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.9048681501308115,
    "pred_doc_category": "model_contract",
    "repository": "microsoft/fluentui",
    "source_url": "https://github.com/microsoft/fluentui/pull/36367",
    "top2": [
      "model_contract",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-5585",
    "code_changed_files": [
      "test/CodeSizeTestCases.size.js"
    ],
    "gold_doc_category": "model_contract",
    "language": "typescript",
    "pred_confidence": 0.8973058274213389,
    "pred_doc_category": "api_reference",
    "repository": "webpack/webpack",
    "source_url": "https://github.com/webpack/webpack/pull/21749",
    "top2": [
      "api_reference",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-4843",
    "code_changed_files": [
      "packages/vite/src/plugins/public-dirs.ts",
      "packages/vite/src/plugins/ssr-styles.ts",
      "packages/vite/src/utils/inline-styles.test.ts",
      "packages/vite/src/utils/inline-styles.ts",
      "test/dynamic-paths.test.ts"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.8887849970955982,
    "pred_doc_category": "api_reference",
    "repository": "nuxt/nuxt",
    "source_url": "https://github.com/nuxt/nuxt/pull/36137",
    "top2": [
      "api_reference",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-0983",
    "code_changed_files": [
      ".github/dependabot.yml"
    ],
    "gold_doc_category": "model_contract",
    "language": "typescript",
    "pred_confidence": 0.8753955705604234,
    "pred_doc_category": "configuration",
    "repository": "microsoft/fluentui",
    "source_url": "https://github.com/microsoft/fluentui/pull/36455",
    "top2": [
      "configuration",
      "model_contract"
    ]
  },
  {
    "case_id": "GH-CAND-1031",
    "code_changed_files": [
      "change/@fluentui-web-components-0cc7cb7d-11d6-4f62-ac35-d648276e84e1.json",
      "packages/web-components/package.json"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.8454100285174362,
    "pred_doc_category": "model_contract",
    "repository": "microsoft/fluentui",
    "source_url": "https://github.com/microsoft/fluentui/pull/36329",
    "top2": [
      "model_contract",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-5946",
    "code_changed_files": [
      "src/language-markdown/print/mdast.js"
    ],
    "gold_doc_category": "developer_setup",
    "language": "typescript",
    "pred_confidence": 0.8407198483535622,
    "pred_doc_category": "model_contract",
    "repository": "prettier/prettier",
    "source_url": "https://github.com/prettier/prettier/pull/19482",
    "top2": [
      "model_contract",
      "developer_setup"
    ]
  },
  {
    "case_id": "GH-CAND-4855",
    "code_changed_files": [
      "packages/nitro-server/src/runtime/handlers/error.ts",
      "packages/nitro-server/test/early-404.test.ts",
      "packages/nitro-server/test/error-vary.test.ts"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.8402979201340157,
    "pred_doc_category": "api_reference",
    "repository": "nuxt/nuxt",
    "source_url": "https://github.com/nuxt/nuxt/pull/36121",
    "top2": [
      "api_reference",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-4599",
    "code_changed_files": [
      "packages/runtime-vapor/__tests__/components/Teleport.spec.ts",
      "packages/runtime-vapor/__tests__/for.spec.ts",
      "packages/runtime-vapor/src/apiCreateFor.ts",
      "packages/runtime-vapor/src/block.ts",
      "packages/runtime-vapor/src/directives/vModel.ts",
      "packages/runtime-vapor/src/dom/event.ts",
      "packages/runtime-vapor/src/fragment.ts",
      "packages/runtime-vapor/src/renderEffect.ts"
    ],
    "gold_doc_category": "api_reference",
    "language": "typescript",
    "pred_confidence": 0.8217993486014232,
    "pred_doc_category": "model_contract",
    "repository": "vuejs/core",
    "source_url": "https://github.com/vuejs/core/pull/15329",
    "top2": [
      "model_contract",
      "developer_setup"
    ]
  },
  {
    "case_id": "GH-CAND-4958",
    "code_changed_files": [
      "packages/kit/src/module/define.ts",
      "packages/kit/src/module/install.ts",
      "packages/nuxt/src/app/plugins/dev-server-logs.ts",
      "packages/nuxt/src/core/schema.ts",
      "packages/nuxt/src/pages/module.ts"
    ],
    "gold_doc_category": "model_contract",
    "language": "typescript",
    "pred_confidence": 0.8197974058541655,
    "pred_doc_category": "api_reference",
    "repository": "nuxt/nuxt",
    "source_url": "https://github.com/nuxt/nuxt/pull/35901",
    "top2": [
      "api_reference",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-4953",
    "code_changed_files": [
      "packages/nuxt/src/components/module.ts",
      "packages/nuxt/src/core/app.ts",
      "packages/nuxt/src/core/builder.ts",
      "packages/nuxt/test/app.test.ts"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.816160370754341,
    "pred_doc_category": "api_reference",
    "repository": "nuxt/nuxt",
    "source_url": "https://github.com/nuxt/nuxt/pull/35912",
    "top2": [
      "api_reference",
      "model_contract"
    ]
  },
  {
    "case_id": "GH-CAND-8534",
    "code_changed_files": [
      "apps/v4/registry/directory.json"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.8079652354648035,
    "pred_doc_category": "developer_setup",
    "repository": "shadcn-ui/ui",
    "source_url": "https://github.com/shadcn-ui/ui/pull/11290",
    "top2": [
      "developer_setup",
      "model_contract"
    ]
  },
  {
    "case_id": "GH-CAND-0512",
    "code_changed_files": [
      ".azure-pipelines/publish.yml"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.8077604084565501,
    "pred_doc_category": "developer_setup",
    "repository": "microsoft/playwright",
    "source_url": "https://github.com/microsoft/playwright/pull/42144",
    "top2": [
      "developer_setup",
      "api_reference"
    ]
  },
  {
    "case_id": "GH-CAND-8498",
    "code_changed_files": [
      "apps/v4/registry/directory.json"
    ],
    "gold_doc_category": "model_contract",
    "language": "typescript",
    "pred_confidence": 0.8045691907148763,
    "pred_doc_category": "developer_setup",
    "repository": "shadcn-ui/ui",
    "source_url": "https://github.com/shadcn-ui/ui/pull/11367",
    "top2": [
      "developer_setup",
      "model_contract"
    ]
  },
  {
    "case_id": "GH-CAND-4653",
    "code_changed_files": [
      "packages/runtime-dom/__tests__/customElement.spec.ts",
      "packages/runtime-dom/src/apiCustomElement.ts"
    ],
    "gold_doc_category": "developer_setup",
    "language": "typescript",
    "pred_confidence": 0.8020483440401273,
    "pred_doc_category": "model_contract",
    "repository": "vuejs/core",
    "source_url": "https://github.com/vuejs/core/pull/15154",
    "top2": [
      "model_contract",
      "developer_setup"
    ]
  },
  {
    "case_id": "GH-CAND-6291",
    "code_changed_files": [
      ".yarn/versions/a46c1d8d.yml",
      "packages/acceptance-tests/pkg-tests-fixtures/packages/one-dep-alias-bins-1.0.0/package.json",
      "packages/acceptance-tests/pkg-tests-specs/sources/node-modules.test.ts",
      "packages/plugin-nm/sources/NodeModulesLinker.ts"
    ],
    "gold_doc_category": "developer_setup",
    "language": "typescript",
    "pred_confidence": 0.7957649393924398,
    "pred_doc_category": "configuration",
    "repository": "yarnpkg/berry",
    "source_url": "https://github.com/yarnpkg/berry/pull/7216",
    "top2": [
      "configuration",
      "developer_setup"
    ]
  },
  {
    "case_id": "GH-CAND-4626",
    "code_changed_files": [
      ".vscode/settings.json"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.7850788819681479,
    "pred_doc_category": "developer_setup",
    "repository": "vuejs/core",
    "source_url": "https://github.com/vuejs/core/pull/15250",
    "top2": [
      "developer_setup",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-5563",
    "code_changed_files": [
      "lib/html/syntax.js",
      "test/HtmlSyntax.unittest.js",
      "types.d.ts"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.780283169010247,
    "pred_doc_category": "model_contract",
    "repository": "webpack/webpack",
    "source_url": "https://github.com/webpack/webpack/pull/21787",
    "top2": [
      "model_contract",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-0485",
    "code_changed_files": [
      "packages/playwright-core/src/cli/installActions.ts",
      "packages/playwright-core/src/cli/program.ts",
      "tests/installation/playwright-cli-install-should-work.spec.ts"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.7715781848346267,
    "pred_doc_category": "api_reference",
    "repository": "microsoft/playwright",
    "source_url": "https://github.com/microsoft/playwright/pull/42222",
    "top2": [
      "api_reference",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-6232",
    "code_changed_files": [
      "pnpm11/installing/commands/src/update/index.ts",
      "pnpm11/pnpm/test/update.ts"
    ],
    "gold_doc_category": "developer_setup",
    "language": "typescript",
    "pred_confidence": 0.7702945148262176,
    "pred_doc_category": "configuration",
    "repository": "pnpm/pnpm",
    "source_url": "https://github.com/pnpm/pnpm/pull/13826",
    "top2": [
      "configuration",
      "developer_setup"
    ]
  },
  {
    "case_id": "GH-CAND-0877",
    "code_changed_files": [
      "common/changes/eslint-plugin-tsdoc/octogonz-publish-eslint-plugin-tsdoc_2019-11-05-18-08.json",
      "eslint-plugin/package.json",
      "eslint-plugin/src/index.ts",
      "eslint-plugin/src/tests/index.ts",
      "rush.json"
    ],
    "gold_doc_category": "api_reference",
    "language": "typescript",
    "pred_confidence": 0.7680258808933499,
    "pred_doc_category": "configuration",
    "repository": "microsoft/tsdoc",
    "source_url": "https://github.com/microsoft/tsdoc/pull/192",
    "top2": [
      "configuration",
      "api_reference"
    ]
  },
  {
    "case_id": "GH-CAND-8194",
    "code_changed_files": [
      "src/react.ts",
      "src/vanilla.ts"
    ],
    "gold_doc_category": "model_contract",
    "language": "typescript",
    "pred_confidence": 0.7633928628978346,
    "pred_doc_category": "api_reference",
    "repository": "pmndrs/zustand",
    "source_url": "https://github.com/pmndrs/zustand/pull/2935",
    "top2": [
      "api_reference",
      "model_contract"
    ]
  },
  {
    "case_id": "GH-CAND-0836",
    "code_changed_files": [
      "common/changes/@microsoft/tsdoc-config/master-to-main_2022-04-09-02-15.json",
      "common/changes/@microsoft/tsdoc/master-to-main_2022-04-09-02-15.json",
      "common/changes/eslint-plugin-tsdoc/master-to-main_2022-04-09-02-15.json",
      "common/config/rush/command-line.json",
      "eslint-plugin/package.json",
      "rush.json",
      "tsdoc-config/package.json",
      "tsdoc/package.json"
    ],
    "gold_doc_category": "api_reference",
    "language": "typescript",
    "pred_confidence": 0.7546996945915632,
    "pred_doc_category": "configuration",
    "repository": "microsoft/tsdoc",
    "source_url": "https://github.com/microsoft/tsdoc/pull/319",
    "top2": [
      "configuration",
      "model_contract"
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
    "pred_confidence": 0.745968520524388,
    "pred_doc_category": "developer_setup",
    "repository": "prettier/prettier",
    "source_url": "https://github.com/prettier/prettier/pull/19830",
    "top2": [
      "developer_setup",
      "model_contract"
    ]
  }
]
```

## train

- total: `1846`
- accuracy: `0.9962`
- top-2 accuracy: `1.0000`
- errors: `7`

### Gold distribution

```json
{
  "api_reference": 625,
  "configuration": 507,
  "developer_setup": 290,
  "model_contract": 424
}
```

### Predicted distribution

```json
{
  "api_reference": 625,
  "configuration": 501,
  "developer_setup": 294,
  "model_contract": 426
}
```

### Per-class metrics

```json
{
  "api_reference": {
    "f1": 0.9984,
    "fn": 1,
    "fp": 1,
    "precision": 0.9984,
    "predicted": 625,
    "recall": 0.9984,
    "support": 625,
    "tp": 624
  },
  "configuration": {
    "f1": 0.9940476190476192,
    "fn": 6,
    "fp": 0,
    "precision": 1.0,
    "predicted": 501,
    "recall": 0.9881656804733728,
    "support": 507,
    "tp": 501
  },
  "developer_setup": {
    "f1": 0.9931506849315068,
    "fn": 0,
    "fp": 4,
    "precision": 0.9863945578231292,
    "predicted": 294,
    "recall": 1.0,
    "support": 290,
    "tp": 290
  },
  "model_contract": {
    "f1": 0.9976470588235293,
    "fn": 0,
    "fp": 2,
    "precision": 0.9953051643192489,
    "predicted": 426,
    "recall": 1.0,
    "support": 424,
    "tp": 424
  }
}
```

### Most common confusion pairs

```json
{
  "api_reference -> developer_setup": 1,
  "configuration -> api_reference": 1,
  "configuration -> developer_setup": 3,
  "configuration -> model_contract": 2
}
```

### Error confidence buckets

```json
{
  "0.00-0.40": 1,
  "0.40-0.50": 5,
  "0.50-0.60": 0,
  "0.60-0.70": 1,
  "0.70-0.80": 0,
  "0.80-1.00": 0,
  "missing": 0
}
```

### High-confidence errors

```json
[
  {
    "case_id": "GH-CAND-4631",
    "code_changed_files": [
      "pnpm-workspace.yaml"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.6020481329463792,
    "pred_doc_category": "developer_setup",
    "repository": "vuejs/core",
    "source_url": "https://github.com/vuejs/core/pull/15243",
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
    "pred_confidence": 0.4909835935235882,
    "pred_doc_category": "developer_setup",
    "repository": "shadcn-ui/ui",
    "source_url": "https://github.com/shadcn-ui/ui/pull/11286",
    "top2": [
      "developer_setup",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-5012",
    "code_changed_files": [
      "packages/svelte/package.json",
      "packages/svelte/src/version.js"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.47446012348745603,
    "pred_doc_category": "model_contract",
    "repository": "sveltejs/svelte",
    "source_url": "https://github.com/sveltejs/svelte/pull/18560",
    "top2": [
      "model_contract",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-4782",
    "code_changed_files": [
      "packages/router/src/router.ts"
    ],
    "gold_doc_category": "api_reference",
    "language": "typescript",
    "pred_confidence": 0.46678463257736375,
    "pred_doc_category": "developer_setup",
    "repository": "vuejs/router",
    "source_url": "https://github.com/vuejs/router/pull/1910",
    "top2": [
      "developer_setup",
      "api_reference"
    ]
  },
  {
    "case_id": "GH-CAND-8175",
    "code_changed_files": [
      "src/traditional.ts"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.4414745359753547,
    "pred_doc_category": "model_contract",
    "repository": "pmndrs/zustand",
    "source_url": "https://github.com/pmndrs/zustand/pull/3116",
    "top2": [
      "model_contract",
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
    "pred_confidence": 0.4154077318904431,
    "pred_doc_category": "developer_setup",
    "repository": "shadcn-ui/ui",
    "source_url": "https://github.com/shadcn-ui/ui/pull/11516",
    "top2": [
      "developer_setup",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-8110",
    "code_changed_files": [
      "src/middleware/devtools.ts"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.33384909047370326,
    "pred_doc_category": "api_reference",
    "repository": "pmndrs/zustand",
    "source_url": "https://github.com/pmndrs/zustand/pull/3414",
    "top2": [
      "api_reference",
      "configuration"
    ]
  }
]
```

## validation

- total: `396`
- accuracy: `0.7071`
- top-2 accuracy: `0.8561`
- errors: `116`

### Gold distribution

```json
{
  "api_reference": 134,
  "configuration": 109,
  "developer_setup": 62,
  "model_contract": 91
}
```

### Predicted distribution

```json
{
  "api_reference": 148,
  "configuration": 96,
  "developer_setup": 56,
  "model_contract": 96
}
```

### Per-class metrics

```json
{
  "api_reference": {
    "f1": 0.801418439716312,
    "fn": 21,
    "fp": 35,
    "precision": 0.7635135135135135,
    "predicted": 148,
    "recall": 0.8432835820895522,
    "support": 134,
    "tp": 113
  },
  "configuration": {
    "f1": 0.6926829268292682,
    "fn": 38,
    "fp": 25,
    "precision": 0.7395833333333334,
    "predicted": 96,
    "recall": 0.6513761467889908,
    "support": 109,
    "tp": 71
  },
  "developer_setup": {
    "f1": 0.6101694915254238,
    "fn": 26,
    "fp": 20,
    "precision": 0.6428571428571429,
    "predicted": 56,
    "recall": 0.5806451612903226,
    "support": 62,
    "tp": 36
  },
  "model_contract": {
    "f1": 0.6417112299465241,
    "fn": 31,
    "fp": 36,
    "precision": 0.625,
    "predicted": 96,
    "recall": 0.6593406593406593,
    "support": 91,
    "tp": 60
  }
}
```

### Most common confusion pairs

```json
{
  "api_reference -> configuration": 7,
  "api_reference -> developer_setup": 4,
  "api_reference -> model_contract": 10,
  "configuration -> api_reference": 15,
  "configuration -> developer_setup": 9,
  "configuration -> model_contract": 14,
  "developer_setup -> api_reference": 5,
  "developer_setup -> configuration": 9,
  "developer_setup -> model_contract": 12,
  "model_contract -> api_reference": 15,
  "model_contract -> configuration": 9,
  "model_contract -> developer_setup": 7
}
```

### Error confidence buckets

```json
{
  "0.00-0.40": 16,
  "0.40-0.50": 24,
  "0.50-0.60": 28,
  "0.60-0.70": 21,
  "0.70-0.80": 18,
  "0.80-1.00": 9,
  "missing": 0
}
```

### High-confidence errors

```json
[
  {
    "case_id": "GH-CAND-0625",
    "code_changed_files": [
      "src/compiler/checker.ts",
      "tests/cases/compiler/reverseMappedTypeInferenceWidening1.ts",
      "tests/cases/compiler/reverseMappedTypeInferenceWidening2.ts"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.9434346482223483,
    "pred_doc_category": "model_contract",
    "repository": "microsoft/TypeScript",
    "source_url": "https://github.com/microsoft/TypeScript/pull/62722",
    "top2": [
      "model_contract",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-8009",
    "code_changed_files": [
      "packages/router-core/src/searchParams.ts",
      "packages/router-core/tests/searchParams.bench.ts",
      "packages/router-core/tests/searchParams.test.ts"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.9318072181219045,
    "pred_doc_category": "api_reference",
    "repository": "TanStack/router",
    "source_url": "https://github.com/TanStack/router/pull/8006",
    "top2": [
      "api_reference",
      "model_contract"
    ]
  },
  {
    "case_id": "GH-CAND-2719",
    "code_changed_files": [
      "test/regressions/a11y/axe.test.ts",
      "test/regressions/a11y/axe.ts",
      "test/regressions/demoMeta.ts",
      "test/regressions/index.test.js"
    ],
    "gold_doc_category": "model_contract",
    "language": "typescript",
    "pred_confidence": 0.9276016427753884,
    "pred_doc_category": "api_reference",
    "repository": "mui/material-ui",
    "source_url": "https://github.com/mui/material-ui/pull/48915",
    "top2": [
      "api_reference",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-8328",
    "code_changed_files": [
      "package.json",
      "pnpm-lock.yaml"
    ],
    "gold_doc_category": "model_contract",
    "language": "typescript",
    "pred_confidence": 0.8764619686782972,
    "pred_doc_category": "configuration",
    "repository": "chakra-ui/chakra-ui",
    "source_url": "https://github.com/chakra-ui/chakra-ui/pull/10494",
    "top2": [
      "configuration",
      "model_contract"
    ]
  },
  {
    "case_id": "GH-CAND-8240",
    "code_changed_files": [
      "apps/compositions/src/examples/splitter-css-units.tsx",
      "apps/compositions/src/examples/splitter-resize-behavior.tsx"
    ],
    "gold_doc_category": "developer_setup",
    "language": "typescript",
    "pred_confidence": 0.8723699447268852,
    "pred_doc_category": "api_reference",
    "repository": "chakra-ui/chakra-ui",
    "source_url": "https://github.com/chakra-ui/chakra-ui/pull/10848",
    "top2": [
      "api_reference",
      "developer_setup"
    ]
  },
  {
    "case_id": "GH-CAND-0610",
    "code_changed_files": [
      "src/lib/es2020.string.d.ts"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.8547674542757663,
    "pred_doc_category": "model_contract",
    "repository": "microsoft/TypeScript",
    "source_url": "https://github.com/microsoft/TypeScript/pull/62885",
    "top2": [
      "model_contract",
      "developer_setup"
    ]
  },
  {
    "case_id": "GH-CAND-0611",
    "code_changed_files": [
      "src/lib/es2020.string.d.ts"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.8546160162227309,
    "pred_doc_category": "model_contract",
    "repository": "microsoft/TypeScript",
    "source_url": "https://github.com/microsoft/TypeScript/pull/62873",
    "top2": [
      "model_contract",
      "developer_setup"
    ]
  },
  {
    "case_id": "GH-CAND-8052",
    "code_changed_files": [
      "pnpm-workspace.yaml"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.8431566924290501,
    "pred_doc_category": "developer_setup",
    "repository": "TanStack/router",
    "source_url": "https://github.com/TanStack/router/pull/7810",
    "top2": [
      "developer_setup",
      "api_reference"
    ]
  },
  {
    "case_id": "GH-CAND-6222",
    "code_changed_files": [
      ".github/actions/binstall/action.yml",
      ".github/workflows/docker.yml",
      ".github/workflows/pacquet-cargo-unused.yml",
      ".github/workflows/pacquet-ci.yml",
      ".github/workflows/pacquet-codecov.yml",
      ".github/workflows/pacquet-integrated-benchmark.yml",
      ".github/workflows/pacquet-micro-benchmark.yml",
      ".github/workflows/release.yml",
      "package.json",
      "pnpm-lock.yaml",
      "pnpm-workspace.yaml"
    ],
    "gold_doc_category": "developer_setup",
    "language": "typescript",
    "pred_confidence": 0.8384981157118467,
    "pred_doc_category": "configuration",
    "repository": "pnpm/pnpm",
    "source_url": "https://github.com/pnpm/pnpm/pull/14006",
    "top2": [
      "configuration",
      "developer_setup"
    ]
  },
  {
    "case_id": "GH-CAND-0636",
    "code_changed_files": [
      "src/compiler/binder.ts",
      "tests/cases/fourslash/unreachableCodeAfterEdit.ts",
      "tests/cases/fourslash/unusedLabelAfterEdit.ts"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.7970040887013056,
    "pred_doc_category": "model_contract",
    "repository": "microsoft/TypeScript",
    "source_url": "https://github.com/microsoft/TypeScript/pull/62783",
    "top2": [
      "model_contract",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-5013",
    "code_changed_files": [
      "packages/svelte/src/compiler/print/index.js",
      "packages/svelte/src/compiler/print/types.d.ts",
      "packages/svelte/types/index.d.ts"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.7920213632419034,
    "pred_doc_category": "model_contract",
    "repository": "sveltejs/svelte",
    "source_url": "https://github.com/sveltejs/svelte/pull/18474",
    "top2": [
      "model_contract",
      "api_reference"
    ]
  },
  {
    "case_id": "GH-CAND-4715",
    "code_changed_files": [
      "packages/runtime-dom/__tests__/directives/vModel.spec.ts",
      "packages/runtime-dom/src/directives/vModel.ts"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.7887412932165259,
    "pred_doc_category": "model_contract",
    "repository": "vuejs/core",
    "source_url": "https://github.com/vuejs/core/pull/15010",
    "top2": [
      "model_contract",
      "developer_setup"
    ]
  },
  {
    "case_id": "GH-CAND-0571",
    "code_changed_files": [
      "src/lib/es5.d.ts"
    ],
    "gold_doc_category": "developer_setup",
    "language": "typescript",
    "pred_confidence": 0.78765642325461,
    "pred_doc_category": "model_contract",
    "repository": "microsoft/TypeScript",
    "source_url": "https://github.com/microsoft/TypeScript/pull/62971",
    "top2": [
      "model_contract",
      "developer_setup"
    ]
  },
  {
    "case_id": "GH-CAND-4490",
    "code_changed_files": [
      "packages/angular/build/src/builders/application/inject-debug-ids.ts",
      "packages/angular/build/src/utils/debug-id.ts",
      "packages/angular/build/src/utils/debug-id_spec.ts"
    ],
    "gold_doc_category": "developer_setup",
    "language": "typescript",
    "pred_confidence": 0.7862418751864799,
    "pred_doc_category": "model_contract",
    "repository": "angular/angular-cli",
    "source_url": "https://github.com/angular/angular-cli/pull/33572",
    "top2": [
      "model_contract",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-4606",
    "code_changed_files": [
      "packages/runtime-core/src/apiCreateApp.ts",
      "packages/runtime-core/src/hydration.ts",
      "packages/runtime-core/src/renderer.ts",
      "packages/runtime-core/src/vnode.ts",
      "packages/runtime-vapor/__tests__/hydration.spec.ts",
      "packages/runtime-vapor/__tests__/scopeId.spec.ts",
      "packages/runtime-vapor/src/apiCreateFor.ts",
      "packages/runtime-vapor/src/component.ts",
      "packages/runtime-vapor/src/componentSlots.ts",
      "packages/runtime-vapor/src/dom/hydration.ts",
      "packages/runtime-vapor/src/dom/template.ts",
      "packages/runtime-vapor/src/fragment.ts",
      "packages/runtime-vapor/src/fragmentFlags.ts",
      "packages/runtime-vapor/src/hmr.ts",
      "packages/runtime-vapor/src/scopeId.ts",
      "packages/runtime-vapor/src/slotBoundary.ts",
      "packages/runtime-vapor/src/slotFragment.ts",
      "packages/runtime-vapor/src/vdomInterop.ts"
    ],
    "gold_doc_category": "api_reference",
    "language": "typescript",
    "pred_confidence": 0.7760659080023868,
    "pred_doc_category": "model_contract",
    "repository": "vuejs/core",
    "source_url": "https://github.com/vuejs/core/pull/15311",
    "top2": [
      "model_contract",
      "api_reference"
    ]
  },
  {
    "case_id": "GH-CAND-0498",
    "code_changed_files": [
      "packages/playwright/src/isomorphic/testServerInterface.ts",
      "packages/playwright/src/plugins/index.ts",
      "packages/playwright/src/runner/tasks.ts",
      "packages/playwright/src/runner/testRunner.ts",
      "packages/playwright/src/runner/watchMode.ts",
      "packages/playwright/src/transform/compilationCache.ts"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.772249559428672,
    "pred_doc_category": "api_reference",
    "repository": "microsoft/playwright",
    "source_url": "https://github.com/microsoft/playwright/pull/42200",
    "top2": [
      "api_reference",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-8338",
    "code_changed_files": [
      ".dumi/theme/builtins/ComponentMeta/index.tsx",
      ".dumi/theme/common/styles/Demo.tsx",
      "components/descriptions/Row.tsx",
      "components/descriptions/__tests__/index.test.tsx",
      "components/list/index.tsx"
    ],
    "gold_doc_category": "api_reference",
    "language": "typescript",
    "pred_confidence": 0.7694889142331873,
    "pred_doc_category": "configuration",
    "repository": "ant-design/ant-design",
    "source_url": "https://github.com/ant-design/ant-design/pull/59067",
    "top2": [
      "configuration",
      "api_reference"
    ]
  },
  {
    "case_id": "GH-CAND-0139",
    "code_changed_files": [
      "src/skill-source.test.ts",
      "src/skill-source.ts"
    ],
    "gold_doc_category": "api_reference",
    "language": "typescript",
    "pred_confidence": 0.7650613714899543,
    "pred_doc_category": "configuration",
    "repository": "eclipsefdn-ai-registry/ai-registry-core",
    "source_url": "https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/38",
    "top2": [
      "configuration",
      "api_reference"
    ]
  },
  {
    "case_id": "GH-CAND-4840",
    "code_changed_files": [
      "packages/vite/src/plugins/public-dirs.ts",
      "packages/vite/test/public-dirs.test.ts"
    ],
    "gold_doc_category": "model_contract",
    "language": "typescript",
    "pred_confidence": 0.7566843259431068,
    "pred_doc_category": "api_reference",
    "repository": "nuxt/nuxt",
    "source_url": "https://github.com/nuxt/nuxt/pull/36143",
    "top2": [
      "api_reference",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-6638",
    "code_changed_files": [
      "benchmark/sqlite/sqlite-is-transaction.js"
    ],
    "gold_doc_category": "model_contract",
    "language": "typescript",
    "pred_confidence": 0.743692344727346,
    "pred_doc_category": "developer_setup",
    "repository": "nodejs/node",
    "source_url": "https://github.com/nodejs/node/pull/65218",
    "top2": [
      "developer_setup",
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
    "pred_confidence": 0.7409115239212234,
    "pred_doc_category": "developer_setup",
    "repository": "chakra-ui/chakra-ui",
    "source_url": "https://github.com/chakra-ui/chakra-ui/pull/10541",
    "top2": [
      "developer_setup",
      "model_contract"
    ]
  },
  {
    "case_id": "GH-CAND-0496",
    "code_changed_files": [
      "packages/isomorphic/trace/entries.ts",
      "packages/isomorphic/trace/snapshotRenderer.ts",
      "packages/isomorphic/trace/snapshotServer.ts",
      "packages/isomorphic/trace/traceLoader.ts",
      "packages/isomorphic/trace/traceModernizer.ts",
      "packages/playwright-core/src/server/har/harRecorder.ts",
      "packages/playwright-core/src/server/har/harTracer.ts",
      "packages/playwright-core/src/server/localUtils.ts",
      "packages/playwright-core/src/server/trace/recorder/snapshotter.ts",
      "packages/playwright-core/src/server/trace/recorder/tracing.ts",
      "packages/playwright-core/src/server/trace/viewer/traceViewer.ts",
      "packages/playwright-core/src/tools/trace/traceAttachments.ts",
      "packages/playwright-core/src/tools/trace/traceRequests.ts",
      "packages/playwright-core/src/tools/trace/traceScreenshot.ts",
      "packages/playwright-core/src/tools/trace/traceSnapshot.ts",
      "packages/playwright/src/worker/testTracing.ts",
      "packages/trace-viewer/src/sw/main.ts",
      "packages/trace-viewer/src/third_party/devtools.ts",
      "packages/trace-viewer/src/ui/attachmentsTab.tsx",
      "packages/trace-viewer/src/ui/filmStrip.tsx",
      "packages/trace-viewer/src/ui/networkResourceDetails.tsx",
      "packages/trace-viewer/src/ui/sourceTab.tsx",
      "packages/trace/src/har.ts",
      "packages/trace/src/snapshot.ts",
      "packages/trace/src/trace.ts",
      "tests/library/browsertype-connect.spec.ts",
      "tests/library/har.spec.ts",
      "tests/library/tracing.spec.ts",
      "tests/library/video.spec.ts",
      "tests/mcp/tracing.spec.ts",
      "tests/playwright-test/playwright.trace.spec.ts"
    ],
    "gold_doc_category": "model_contract",
    "language": "typescript",
    "pred_confidence": 0.7323348486539637,
    "pred_doc_category": "api_reference",
    "repository": "microsoft/playwright",
    "source_url": "https://github.com/microsoft/playwright/pull/42192",
    "top2": [
      "api_reference",
      "model_contract"
    ]
  },
  {
    "case_id": "GH-CAND-8554",
    "code_changed_files": [
      "apps/v4/app/(app)/(create)/components/accent-picker.tsx",
      "apps/v4/app/(app)/(create)/components/base-color-picker.tsx",
      "apps/v4/app/(app)/(create)/components/chart-color-picker.tsx",
      "apps/v4/app/(app)/(create)/components/font-picker.tsx",
      "apps/v4/app/(app)/(create)/components/icon-library-picker.tsx",
      "apps/v4/app/(app)/(create)/components/menu-picker.tsx",
      "apps/v4/app/(app)/(create)/components/picker.tsx",
      "apps/v4/app/(app)/(create)/components/preview-override.tsx",
      "apps/v4/app/(app)/(create)/components/preview.tsx",
      "apps/v4/app/(app)/(create)/components/radius-picker.tsx",
      "apps/v4/app/(app)/(create)/components/style-picker.tsx",
      "apps/v4/app/(app)/(create)/components/theme-picker.tsx",
      "apps/v4/app/(app)/(create)/create/page.tsx",
      "apps/v4/app/(app)/(typeset)/components/font-picker.tsx",
      "apps/v4/app/(app)/(typeset)/components/option-picker.tsx",
      "apps/v4/app/(app)/(typeset)/components/picker.tsx",
      "apps/v4/app/(app)/(typeset)/components/preview-override.tsx",
      "apps/v4/app/(app)/(typeset)/components/preview.tsx",
      "apps/v4/app/(app)/(typeset)/typeset/page.tsx"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.7281842212505453,
    "pred_doc_category": "api_reference",
    "repository": "shadcn-ui/ui",
    "source_url": "https://github.com/shadcn-ui/ui/pull/11207",
    "top2": [
      "api_reference",
      "model_contract"
    ]
  },
  {
    "case_id": "GH-CAND-8810",
    "code_changed_files": [
      "packages/plugins/sentry/jest.config.js",
      "packages/plugins/sentry/package.json",
      "packages/plugins/sentry/server/src/services/__tests__/sentry.vitest.test.ts",
      "packages/plugins/sentry/server/tsconfig.json",
      "packages/plugins/sentry/vitest.config.ts"
    ],
    "gold_doc_category": "configuration",
    "language": "typescript",
    "pred_confidence": 0.7179686580868873,
    "pred_doc_category": "api_reference",
    "repository": "strapi/strapi",
    "source_url": "https://github.com/strapi/strapi/pull/27252",
    "top2": [
      "api_reference",
      "configuration"
    ]
  },
  {
    "case_id": "GH-CAND-0627",
    "code_changed_files": [
      "src/compiler/checker.ts"
    ],
    "gold_doc_category": "developer_setup",
    "language": "typescript",
    "pred_confidence": 0.7156153936201339,
    "pred_doc_category": "model_contract",
    "repository": "microsoft/TypeScript",
    "source_url": "https://github.com/microsoft/TypeScript/pull/61560",
    "top2": [
      "model_contract",
      "developer_setup"
    ]
  }
]
```
