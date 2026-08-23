# Real PR Classifier Error Analysis

- Prediction file: `reports\real_case_study\generated\real_gold_classifier_4k_v1\threshold_sweep_mcc_predictions.jsonl`
- Cases file: `data\external\project_case_study\generated\real_pr_gold_4k_v1_protocol_labeled.jsonl`
- Total rows: `4138`

## Error counts

- `TN`: `632`
- `TP`: `2937`
- `FN`: `480`
- `FP`: `89`

## Error counts by split

- `locked_test`: `{'TP': 394, 'FP': 31, 'TN': 94, 'FN': 101}`
- `train`: `{'TN': 479, 'TP': 2081, 'FN': 322, 'FP': 17}`
- `validation`: `{'TP': 462, 'FN': 57, 'TN': 59, 'FP': 41}`

## Error counts by language

- `go`: `{'TP': 113, 'FP': 6, 'FN': 1}`
- `python`: `{'TN': 47, 'TP': 166, 'FN': 83, 'FP': 1}`
- `typescript`: `{'TN': 585, 'TP': 2658, 'FN': 396, 'FP': 82}`

## Error counts by candidate type

- `code_and_docs_changed_needs_manual_validation`: `{'TP': 1088, 'FN': 42}`
- `code_only_needs_manual_validation`: `{'TN': 429, 'TP': 1849, 'FN': 438, 'FP': 39}`
- `code_only_test_or_fixture_candidate_negative_review`: `{'TN': 203, 'FP': 50}`

## Top repositories by false negatives

- `open-telemetry/opentelemetry-python-contrib`: `73`
- `eslint/eslint`: `48`
- `chakra-ui/chakra-ui`: `40`
- `nodejs/node`: `39`
- `ant-design/ant-design`: `34`
- `microsoft/playwright`: `32`
- `babel/babel`: `28`
- `TanStack/router`: `19`
- `microsoft/fluentui`: `18`
- `nuxt/nuxt`: `18`
- `angular/angular-cli`: `17`
- `open-telemetry/opentelemetry-js-contrib`: `14`
- `microsoft/rushstack`: `12`
- `strapi/strapi`: `11`
- `typescript-eslint/typescript-eslint`: `11`
- `microsoft/TypeScript`: `10`
- `microsoft/tsdoc`: `8`
- `pmndrs/zustand`: `8`
- `CryptoJones/omind`: `7`
- `yarnpkg/berry`: `5`

## Top repositories by false positives

- `pmndrs/zustand`: `19`
- `appwrite/appwrite`: `12`
- `typescript-eslint/typescript-eslint`: `11`
- `npm/cli`: `8`
- `microsoft/TypeScript-go`: `6`
- `microsoft/tsdoc`: `5`
- `pnpm/pnpm`: `4`
- `appwrite/sdk-for-web`: `3`
- `eclipsefdn-ai-registry/ai-registry-core`: `3`
- `rollup/rollup`: `3`
- `babel/babel`: `2`
- `sveltejs/svelte`: `2`
- `vercel/next.js`: `2`
- `microsoft/rushstack`: `2`
- `vuejs/core`: `1`
- `prettier/prettier`: `1`
- `grafana/grafana`: `1`
- `remix-run/remix`: `1`
- `microsoft/vscode`: `1`
- `supabase/supabase`: `1`
