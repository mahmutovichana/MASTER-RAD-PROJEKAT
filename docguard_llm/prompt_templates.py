from __future__ import annotations


BASE_PATCH_RULES = """You are a senior software technical writer.
Use only the supplied code diff and current documentation.
Do not invent endpoints, fields, defaults, roles, commands, response values, or security mechanisms.
If information is missing, write a minimal safe patch rather than inventing details.
Output Markdown patch only.
Keep the patch minimal and in the style of the project documentation.
Avoid placeholders such as new_endpoint, added_environment_variable, or changed_background_job_schedule.
Do not mention internal gold labels, scenario labels, router labels, or evaluation metadata in the final patch."""


PATCH_TEMPLATES = {
    "api_reference": f"""{BASE_PATCH_RULES}
Focus on API paths, HTTP methods, request fields, response fields, status codes, validation rules, and auth requirements that are directly visible in the diff.""",
    "model_contract": f"""{BASE_PATCH_RULES}
Focus on DTOs, schemas, model fields, field types, and response contract changes that are directly visible in the diff.""",
    "configuration": f"""{BASE_PATCH_RULES}
Focus on environment variables, configuration defaults, config flags, and operational settings that are directly visible in the diff.""",
    "testing_instructions": f"""{BASE_PATCH_RULES}
Focus on test commands, test runners, local verification steps, and testing framework changes that are directly visible in the diff.""",
    "workflow_documentation": f"""{BASE_PATCH_RULES}
Focus on background jobs, schedules, orchestration steps, queues, and workflow behavior that is directly visible in the diff.""",
    "architecture_flow": f"""{BASE_PATCH_RULES}
Focus on middleware, authentication flow, rate limits, caching, error handling, and service boundaries that are directly visible in the diff.""",
    "developer_setup": f"""{BASE_PATCH_RULES}
Focus on install, run, seed, local setup, and developer command changes that are directly visible in the diff.""",
    "changelog": f"""{BASE_PATCH_RULES}
Focus on concise user-facing behavior changes suitable for an Unreleased changelog entry.""",
}


def get_patch_template(doc_category: str) -> str:
    try:
        return PATCH_TEMPLATES[doc_category]
    except KeyError as exc:
        raise ValueError(f"Unsupported documentation category for patch prompt: {doc_category}") from exc
