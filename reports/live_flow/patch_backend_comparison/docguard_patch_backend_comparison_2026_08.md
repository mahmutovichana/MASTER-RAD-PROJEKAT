# DocGuard Patch Backend Comparison 2026-08

HF backend was not run; pass `--hf-model` to compare a real HuggingFace model.

| Case | Target doc | Legacy patch | LLM mock patch | LLM HF patch | Verifier | Grounded tokens | Observation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ATLAS-REVIEW-API-PR-01` | `docs/api.md` | `@@ Documentation +new_endpoint.` | `@@ docs/api.md +Mock LLM patch: document POST based on the supplied code diff.` | `not run` | `legacy:warn / llm-mock:pass` | `legacy: / llm-mock:POST` | Patch is usable for inspection but has verifier warnings. Patch passed lightweight grounding checks. |
| `ATLAS-REVIEW-API-PR-02` | `docs/api.md` | `@@ Documentation +changed_validation_min.` | `@@ docs/api.md +Mock LLM patch: document 3 based on the supplied code diff.` | `not run` | `legacy:warn / llm-mock:pass` | `legacy: / llm-mock:3` | Patch is usable for inspection but has verifier warnings. Patch passed lightweight grounding checks. |
| `ATLAS-REVIEW-API-PR-03` | `docs/models.md` | `@@ Documentation +added_dto_model_field.` | `@@ docs/models.md +Mock LLM patch: document ReviewDto based on the supplied code diff.` | `not run` | `legacy:warn / llm-mock:pass` | `legacy: / llm-mock:ReviewDto` | Patch is usable for inspection but has verifier warnings. Patch passed lightweight grounding checks. |
| `ATLAS-REVIEW-API-PR-04` | `docs/configuration.md` | `@@ Documentation +added_environment_variable.` | `@@ docs/configuration.md +Mock LLM patch: document REVIEW_FEATURE_FLAG based on the supplied code diff.` | `not run` | `legacy:warn / llm-mock:pass` | `legacy: / llm-mock:REVIEW_FEATURE_FLAG` | Patch is usable for inspection but has verifier warnings. Patch passed lightweight grounding checks. |
| `ATLAS-REVIEW-API-PR-05` | `docs/workflows.md` | `@@ Documentation +changed_background_job_schedule.` | `@@ docs/workflows.md +Mock LLM patch: document 0 * * * * based on the supplied code diff.` | `not run` | `legacy:warn / llm-mock:pass` | `legacy: / llm-mock:0 * * * *` | Patch is usable for inspection but has verifier warnings. Patch passed lightweight grounding checks. |
