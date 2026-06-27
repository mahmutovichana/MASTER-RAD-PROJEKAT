# Real LLM Smoke Test: qwen2_5_coder_0_5b

- command: `python -m docguard_llm.cli smoke-test --model qwen2_5_coder_0_5b --backend transformers_local`
- backend: transformers_local
- model_key: qwen2_5_coder_0_5b
- model_id: Qwen/Qwen2.5-Coder-0.5B-Instruct
- selected_record_id: sanity-only
- compact_prompt: False
- sanity_only: True
- prompt_length_characters: 68
- parse_success: False
- latency_seconds: 16.418204500001593
- status: succeeded
- output_usable: False

## Prompt Preview

```text
system: Return JSON only.

user: Return only this JSON: {"ok": true}
```

## Raw Model Output

```text
```json
{
  "ok": true
}
```
```

## Parsed Prediction

```json
{
  "raw_json_parse_error": true
}
```
