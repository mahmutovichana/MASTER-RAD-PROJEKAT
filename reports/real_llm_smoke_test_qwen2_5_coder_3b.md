# Real LLM Smoke Test: qwen2_5_coder_3b

> Important: This report was generated with the mock backend. Mock results validate the DocGuard LLM pipeline, but they do not represent real Hugging Face model quality. Real model results must be generated with transformers_local or text_generation_inference backends.

- backend: mock
- status: succeeded
- record_id: support-ticket-api-001

## Structured Prediction

```json
{
  "record_id": "support-ticket-api-001",
  "model_key": "qwen2_5_coder_3b",
  "model_id": "Qwen/Qwen2.5-Coder-3B-Instruct",
  "backend": "mock",
  "docs_update_required": true,
  "scenario_type": "unknown_change",
  "doc_category": "configuration",
  "target_doc_file": "docs/configuration.md",
  "target_section": "Environment Variables",
  "generated_doc_patch": "@@ Environment Variables\n+Update documentation for the changed behavior.",
  "change_intent_summary": "Mock backend inferred the change from deterministic diff signals.",
  "primary_documentation_reason": "Documentation update required.",
  "expected_facts_covered": [
    "documentation update required"
  ],
  "confidence": 0.75,
  "raw_model_output": "{\"docs_update_required\": true, \"scenario_type\": \"unknown_change\", \"doc_category\": \"configuration\", \"target_doc_file\": \"docs/configuration.md\", \"target_section\": \"Environment Variables\", \"generated_doc_patch\": \"@@ Environment Variables\\n+Update documentation for the changed behavior.\", \"change_intent_summary\": \"Mock backend inferred the change from deterministic diff signals.\", \"primary_documentation_reason\": \"Documentation update required.\", \"expected_facts_covered\": [\"documentation update required\"], \"confidence\": 0.75}",
  "parse_error": false,
  "latency_seconds": 8.410000009462237e-05
}
```
