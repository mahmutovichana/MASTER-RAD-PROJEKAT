# DocGuard LLM Mock Patch Generation Report 2026-08

This report exercises the optional LLM patch-generation architecture with the mock backend. No HuggingFace model is downloaded or executed.

- cases evaluated: 5
- patch backend: `llm-mock`
- verifier status counts: `{"pass": 5}`

When a real HuggingFace instruction model is plugged in, the same prompt builder, postprocessor, and verifier remain in place. Only the generation backend changes from `mock` to `hf`.

## Prompt Examples

### `ATLAS-REVIEW-API-PR-01`

Prompt:

```text
You are a senior software technical writer.
Use only the supplied code diff and current documentation.
Do not invent endpoints, fields, defaults, roles, commands, response values, or security mechanisms.
If information is missing, write a minimal safe patch rather than inventing details.
Output Markdown patch only.
Keep the patch minimal and in the style of the project documentation.
Avoid placeholders such as new_endpoint, added_environment_variable, or changed_background_job_schedule.
Do not mention internal gold labels, scenario labels, router labels, or evaluation metadata in the final patch.
Focus on API paths, HTTP methods, request fields, response fields, status codes, validation rules, and auth requirements that are directly visible in the diff.

Allowed facts extracted from the diff:
{
  "allowed_tokens": [
    "POST",
    "/reviews",
    "201",
    "id",
    "reviewStatus"
  ],
  "allowed_facts": {
    "http_methods": [
      "POST"
    ],
    "route_paths": [
      "/reviews"
    ],
    "status_codes": [
      "201"
    ],
    "response_fields": [
      "id",
      "reviewStatus"
    ],
    "request_fields": [],
    "auth_roles": [],
    "validation_min_values": [],
    "validation_max_values": [],
    "interface_or_class_names": [],
    "added_fields": [],
    "field_types": [],
    "env_vars": [],
    "config_variables": [],
    "default_values": [],
    "test_commands": [],
    "frameworks": [],
    "cron_expressions": [],
    "job_or_function_names": [
      "post"
    ],
    "rate_limit_values": [],
    "middleware_names": [],
    "behavior_tokens": [
      "reviews",
      "createReview",
      "reviewStatus"
    ]
  },
  "blocked_terms_hint": [
    "Do not mention request fields unless listed in allowed_facts.request_fields.",
    "Do not mention response fields unless listed in allowed_facts.response_fields.",
    "Do not mention enum/status values unless listed in allowed_tokens.",
    "Do not mention auth mechanisms, roles, or security behavior unless listed in allowed_facts.auth_roles or visible in docs_before."
  ],
  "missing_context_notes": [
    "request fields are not visible"
  ]
}

You may only write documentation statements supported by these allowed facts.
Do not add request fields unless they appear in allowed facts.
Do not add response fields unless they appear in allowed facts.
Do not add example enum/status values unless visible in allowed facts.
Do not invent authentication/security behavior.
Do not rewrite the whole doc
```

Raw mock patch:

```diff
@@ docs/api.md
+Mock LLM patch: document `POST` based on the supplied code diff.
```

Postprocessed patch:

```diff
@@ docs/api.md
+Mock LLM patch: document `POST` based on the supplied code diff.
```

Verifier: `pass`; warnings: `[]`; grounded tokens: `['POST']`

### `ATLAS-REVIEW-API-PR-02`

Prompt:

```text
You are a senior software technical writer.
Use only the supplied code diff and current documentation.
Do not invent endpoints, fields, defaults, roles, commands, response values, or security mechanisms.
If information is missing, write a minimal safe patch rather than inventing details.
Output Markdown patch only.
Keep the patch minimal and in the style of the project documentation.
Avoid placeholders such as new_endpoint, added_environment_variable, or changed_background_job_schedule.
Do not mention internal gold labels, scenario labels, router labels, or evaluation metadata in the final patch.
Focus on API paths, HTTP methods, request fields, response fields, status codes, validation rules, and auth requirements that are directly visible in the diff.

Allowed facts extracted from the diff:
{
  "allowed_tokens": [
    "3",
    "10",
    "500",
    "280",
    "comment",
    "z"
  ],
  "allowed_facts": {
    "http_methods": [],
    "route_paths": [],
    "status_codes": [],
    "response_fields": [],
    "request_fields": [],
    "auth_roles": [],
    "validation_min_values": [
      "3",
      "10"
    ],
    "validation_max_values": [
      "500",
      "280"
    ],
    "interface_or_class_names": [],
    "added_fields": [
      "comment"
    ],
    "field_types": [
      "z"
    ],
    "env_vars": [],
    "config_variables": [],
    "default_values": [],
    "test_commands": [],
    "frameworks": [],
    "cron_expressions": [],
    "job_or_function_names": [
      "string",
      "min",
      "max"
    ],
    "rate_limit_values": [],
    "middleware_names": [],
    "behavior_tokens": [
      "comment"
    ]
  },
  "blocked_terms_hint": [
    "Do not mention request fields unless listed in allowed_facts.request_fields.",
    "Do not mention response fields unless listed in allowed_facts.response_fields.",
    "Do not mention enum/status values unless listed in allowed_tokens.",
    "Do not mention auth mechanisms, roles, or security behavior unless listed in allowed_facts.auth_roles or visible in docs_before."
  ],
  "missing_context_notes": [
    "request fields are not visible",
    "response fields are not visible"
  ]
}

You may only write documentation statements supported by these allowed facts.
Do not add request fields unless they appear in allowed facts.
Do not add response fields unless they appear in allowed facts.
Do not add example enum/status values unless visible in allowed facts.
Do not invent authentication/security behavior.
Do not rewr
```

Raw mock patch:

```diff
@@ docs/api.md
+Mock LLM patch: document `3` based on the supplied code diff.
```

Postprocessed patch:

```diff
@@ docs/api.md
+Mock LLM patch: document `3` based on the supplied code diff.
```

Verifier: `pass`; warnings: `[]`; grounded tokens: `['3']`

### `ATLAS-REVIEW-API-PR-03`

Prompt:

```text
You are a senior software technical writer.
Use only the supplied code diff and current documentation.
Do not invent endpoints, fields, defaults, roles, commands, response values, or security mechanisms.
If information is missing, write a minimal safe patch rather than inventing details.
Output Markdown patch only.
Keep the patch minimal and in the style of the project documentation.
Avoid placeholders such as new_endpoint, added_environment_variable, or changed_background_job_schedule.
Do not mention internal gold labels, scenario labels, router labels, or evaluation metadata in the final patch.
Focus on DTOs, schemas, model fields, field types, and response contract changes that are directly visible in the diff.

Allowed facts extracted from the diff:
{
  "allowed_tokens": [
    "ReviewDto",
    "reviewerId",
    "string"
  ],
  "allowed_facts": {
    "http_methods": [],
    "route_paths": [],
    "status_codes": [],
    "response_fields": [],
    "request_fields": [],
    "auth_roles": [],
    "validation_min_values": [],
    "validation_max_values": [],
    "interface_or_class_names": [
      "ReviewDto"
    ],
    "added_fields": [
      "reviewerId"
    ],
    "field_types": [
      "string"
    ],
    "env_vars": [],
    "config_variables": [],
    "default_values": [],
    "test_commands": [],
    "frameworks": [],
    "cron_expressions": [],
    "job_or_function_names": [],
    "rate_limit_values": [],
    "middleware_names": [],
    "behavior_tokens": [
      "interface",
      "ReviewDto",
      "reviewerId"
    ]
  },
  "blocked_terms_hint": [
    "Do not mention request fields unless listed in allowed_facts.request_fields.",
    "Do not mention response fields unless listed in allowed_facts.response_fields.",
    "Do not mention enum/status values unless listed in allowed_tokens.",
    "Do not mention auth mechanisms, roles, or security behavior unless listed in allowed_facts.auth_roles or visible in docs_before."
  ],
  "missing_context_notes": []
}

You may only write documentation statements supported by these allowed facts.
Do not add request fields unless they appear in allowed facts.
Do not add response fields unless they appear in allowed facts.
Do not add example enum/status values unless visible in allowed facts.
Do not invent authentication/security behavior.
Do not rewrite the whole document.
Generate a minimal patch only.

Project id: atlas_review_api
Target document: docs/models.md
Target section: docs/models.md
Documentation cate
```

Raw mock patch:

```diff
@@ docs/models.md
+Mock LLM patch: document `ReviewDto` based on the supplied code diff.
```

Postprocessed patch:

```diff
@@ docs/models.md
+Mock LLM patch: document `ReviewDto` based on the supplied code diff.
```

Verifier: `pass`; warnings: `[]`; grounded tokens: `['ReviewDto']`

