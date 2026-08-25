# Category Reviewed Split V2 Protocol

## Purpose

This protocol creates a new documentation-category dataset split after train/validation label review.

The goal is to improve category-label consistency without introducing rule-based routing or manual model steering.

## Leakage boundary

- The previous locked-test split is not used as input.
- The reviewed dataset is built only from the reviewed train and validation files.
- A new locked-test split is created only after labels are fixed.
- The new locked-test split must be used only for final reporting under this V2 category protocol.

## Model-facing fields

- `language`
- `code_changed_files`
- `code_diff_excerpt`
- `docs_before_excerpt`

No gold labels, manual notes, target document files, source URLs, PR titles, docs-after text, or docs diffs are model-facing fields.

## Category schema

- `api_reference`
- `configuration`
- `developer_setup`
- `model_contract`

## Split summary

```json
{
  "combined": {
    "category_counts": {
      "api_reference": 893,
      "configuration": 724,
      "developer_setup": 415,
      "model_contract": 605
    },
    "label_status_counts": {
      "not_reviewed_original_label": 2150,
      "reviewed_category_updated": 63,
      "reviewed_keep": 424
    },
    "repository_counts_top30": {
      "TanStack/router": 103,
      "angular/angular": 102,
      "angular/angular-cli": 97,
      "ant-design/ant-design": 100,
      "appwrite/sdk-for-web": 55,
      "babel/babel": 92,
      "chakra-ui/chakra-ui": 101,
      "d-hinders/Haven-AI": 106,
      "eclipsefdn-ai-registry/ai-registry-core": 25,
      "eslint/eslint": 71,
      "grafana/grafana": 17,
      "microsoft/TypeScript": 86,
      "microsoft/fluentui": 104,
      "microsoft/playwright": 88,
      "microsoft/tsdoc": 112,
      "nodejs/node": 94,
      "npm/cli": 109,
      "nuxt/nuxt": 80,
      "open-telemetry/opentelemetry-js-contrib": 33,
      "pmndrs/zustand": 64,
      "pnpm/pnpm": 115,
      "prettier/prettier": 103,
      "remix-run/remix": 18,
      "shadcn-ui/ui": 114,
      "strapi/strapi": 103,
      "sveltejs/svelte": 67,
      "vuejs/core": 103,
      "vuejs/router": 114,
      "webpack/webpack": 107,
      "yarnpkg/berry": 103
    },
    "rows": 2637,
    "source_split_counts": {
      "reviewed_train": 2127,
      "reviewed_validation": 510
    }
  },
  "language_filter": "typescript",
  "methodology": {
    "category_specific_prediction_rules_added": false,
    "manual_path_flags_added": false,
    "model_facing_fields": [
      "language",
      "code_changed_files",
      "code_diff_excerpt",
      "docs_before_excerpt"
    ],
    "new_locked_test_policy": "final_reporting_only_after_this_split_is_frozen",
    "old_locked_test_excluded": true,
    "target_label_review_used": true
  },
  "outputs": {
    "locked_test": "reports\\real_case_study\\generated\\splits_category_reviewed_v2\\real_pr_category_reviewed_v2_locked_test.jsonl",
    "train": "reports\\real_case_study\\generated\\splits_category_reviewed_v2\\real_pr_category_reviewed_v2_train.jsonl",
    "validation": "reports\\real_case_study\\generated\\splits_category_reviewed_v2\\real_pr_category_reviewed_v2_validation.jsonl"
  },
  "protocol": "category_reviewed_split_v2",
  "ratios": {
    "locked_test": 0.15,
    "train": 0.7,
    "validation": 0.15
  },
  "seed": 20260824,
  "source_inputs": {
    "previous_locked_test_used": false,
    "reviewed_train": "reports\\real_case_study\\generated\\splits_gold_4k_category_review_v2\\real_pr_gold_4k_category_v2_train.jsonl",
    "reviewed_validation": "reports\\real_case_study\\generated\\splits_gold_4k_category_review_v2\\real_pr_gold_4k_category_v2_validation.jsonl"
  },
  "splits": {
    "locked_test": {
      "category_counts": {
        "api_reference": 134,
        "configuration": 108,
        "developer_setup": 63,
        "model_contract": 90
      },
      "label_status_counts": {
        "not_reviewed_original_label": 334,
        "reviewed_category_updated": 8,
        "reviewed_keep": 53
      },
      "repository_counts_top30": {
        "TanStack/router": 14,
        "angular/angular": 15,
        "angular/angular-cli": 17,
        "ant-design/ant-design": 14,
        "appwrite/sdk-for-web": 7,
        "babel/babel": 11,
        "chakra-ui/chakra-ui": 9,
        "d-hinders/Haven-AI": 10,
        "eslint/eslint": 12,
        "grafana/grafana": 3,
        "microsoft/TypeScript": 12,
        "microsoft/fluentui": 21,
        "microsoft/playwright": 16,
        "microsoft/tsdoc": 21,
        "nestjs/nest": 4,
        "nodejs/node": 15,
        "npm/cli": 16,
        "nuxt/nuxt": 14,
        "pmndrs/zustand": 3,
        "pnpm/pnpm": 14,
        "prettier/prettier": 27,
        "remix-run/remix": 3,
        "shadcn-ui/ui": 14,
        "strapi/strapi": 15,
        "sveltejs/svelte": 10,
        "vercel/next.js": 4,
        "vuejs/core": 13,
        "vuejs/router": 15,
        "webpack/webpack": 21,
        "yarnpkg/berry": 20
      },
      "rows": 395,
      "source_split_counts": {
        "reviewed_train": 331,
        "reviewed_validation": 64
      }
    },
    "train": {
      "category_counts": {
        "api_reference": 625,
        "configuration": 507,
        "developer_setup": 290,
        "model_contract": 424
      },
      "label_status_counts": {
        "not_reviewed_original_label": 1495,
        "reviewed_category_updated": 47,
        "reviewed_keep": 304
      },
      "repository_counts_top30": {
        "TanStack/router": 75,
        "angular/angular": 70,
        "angular/angular-cli": 65,
        "ant-design/ant-design": 74,
        "appwrite/sdk-for-web": 38,
        "babel/babel": 71,
        "chakra-ui/chakra-ui": 76,
        "d-hinders/Haven-AI": 77,
        "eclipsefdn-ai-registry/ai-registry-core": 18,
        "eslint/eslint": 46,
        "grafana/grafana": 13,
        "microsoft/TypeScript": 63,
        "microsoft/fluentui": 69,
        "microsoft/playwright": 56,
        "microsoft/tsdoc": 77,
        "nodejs/node": 68,
        "npm/cli": 74,
        "nuxt/nuxt": 55,
        "open-telemetry/opentelemetry-js-contrib": 27,
        "pmndrs/zustand": 46,
        "pnpm/pnpm": 85,
        "prettier/prettier": 57,
        "remix-run/remix": 13,
        "shadcn-ui/ui": 80,
        "strapi/strapi": 68,
        "sveltejs/svelte": 49,
        "vuejs/core": 72,
        "vuejs/router": 88,
        "webpack/webpack": 74,
        "yarnpkg/berry": 65
      },
      "rows": 1846,
      "source_split_counts": {
        "reviewed_train": 1484,
        "reviewed_validation": 362
      }
    },
    "validation": {
      "category_counts": {
        "api_reference": 134,
        "configuration": 109,
        "developer_setup": 62,
        "model_contract": 91
      },
      "label_status_counts": {
        "not_reviewed_original_label": 321,
        "reviewed_category_updated": 8,
        "reviewed_keep": 67
      },
      "repository_counts_top30": {
        "TanStack/router": 14,
        "angular/angular": 17,
        "angular/angular-cli": 15,
        "ant-design/ant-design": 12,
        "appwrite/sdk-for-web": 10,
        "babel/babel": 10,
        "chakra-ui/chakra-ui": 16,
        "d-hinders/Haven-AI": 19,
        "eclipsefdn-ai-registry/ai-registry-core": 6,
        "eslint/eslint": 13,
        "microsoft/TypeScript": 11,
        "microsoft/fluentui": 14,
        "microsoft/playwright": 16,
        "microsoft/tsdoc": 14,
        "nodejs/node": 11,
        "npm/cli": 19,
        "nuxt/nuxt": 11,
        "open-telemetry/opentelemetry-js-contrib": 3,
        "pmndrs/zustand": 15,
        "pnpm/pnpm": 16,
        "prettier/prettier": 19,
        "remix-run/remix": 2,
        "shadcn-ui/ui": 20,
        "strapi/strapi": 20,
        "sveltejs/svelte": 8,
        "vercel/next.js": 1,
        "vuejs/core": 18,
        "vuejs/router": 11,
        "webpack/webpack": 12,
        "yarnpkg/berry": 18
      },
      "rows": 396,
      "source_split_counts": {
        "reviewed_train": 312,
        "reviewed_validation": 84
      }
    }
  },
  "status": "ok"
}
```

## Methodological interpretation

This V2 split may be used as a new frozen category-classification benchmark.
It should not be mixed with the older V1 locked-test result as if both were the same test set.

The correct comparison is within this protocol: validation is used for model selection and V2 locked-test is used only for final reporting.
