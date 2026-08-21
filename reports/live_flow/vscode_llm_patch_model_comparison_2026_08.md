# VS Code LLM Patch Model Comparison

This report compares live DocGuard documentation patch generation on the current VS Code demo workspace.
The deterministic patch composer is used only as a safe fallback and grounding aid; model quality is judged from the LLM patch output.

- Workspace: `examples\vscode_demo`
- Backend: `llm-openai-compatible`
- Recommended model from this run: `Qwen/Qwen2.5-Coder-32B-Instruct`

## Connection Check

| Model | Preflight | Status | Error |
|---|---:|---:|---|
| Qwen/Qwen2.5-Coder-32B-Instruct | ok | 200 |  |
| Qwen/Qwen2.5-Coder-7B-Instruct | ok | 200 |  |
| meta-llama/Llama-3.1-8B-Instruct | ok | 200 |  |

## Summary

| Model | Generation | Verifier | Quality | Hallucination risk | Target | Patch preview | Runtime ms |
|---|---:|---:|---:|---:|---|---|---:|
| Qwen/Qwen2.5-Coder-32B-Instruct | ok | pass | excellent | low | docs/configuration.md#Environment Variables | ## Environment Variables - \`REVIEW_WINDOW\` sets the review window and defaults to \`7d\`. | 1386.45 |
| Qwen/Qwen2.5-Coder-7B-Instruct | ok | pass | excellent | low | docs/configuration.md#Environment Variables | ## Environment Variables ## Environment Variables - \`REVIEW_WINDOW\` sets the review window and defaults to \`7d\`. | 1185.98 |
| meta-llama/Llama-3.1-8B-Instruct | ok | pass | excellent | low | docs/configuration.md#Environment Variables | ## Environment Variables ## Environment Variables - \`REVIEW_WINDOW\` sets the review window and defaults to \`7d\`. - \`REVIEW_MODE\` controls the default ticket review mode. - \`process\` is a field type. - \`env\`... | 9441.66 |

## Detailed Patch Outputs

### Qwen/Qwen2.5-Coder-32B-Instruct

- Generation: `ok`
- Postprocess: `ok`
- Verifier: `pass`
- Quality: `excellent`
- Hallucination risk: `low`
- Grounded tokens: `REVIEW_WINDOW, 7d, env`

Patch preview:

```markdown
## Environment Variables
- `REVIEW_WINDOW` sets the review window and defaults to `7d`.
```

Warnings:

- normalized patch into lightweight diff form
- patch is grounded, minimal, and readable under lightweight heuristic checks

### Qwen/Qwen2.5-Coder-7B-Instruct

- Generation: `ok`
- Postprocess: `ok`
- Verifier: `pass`
- Quality: `excellent`
- Hallucination risk: `low`
- Grounded tokens: `REVIEW_WINDOW, 7d, env`

Patch preview:

```markdown
## Environment Variables
## Environment Variables
- `REVIEW_WINDOW` sets the review window and defaults to `7d`.
```

Warnings:

- normalized patch into lightweight diff form
- patch is grounded, minimal, and readable under lightweight heuristic checks

### meta-llama/Llama-3.1-8B-Instruct

- Generation: `ok`
- Postprocess: `ok`
- Verifier: `pass`
- Quality: `excellent`
- Hallucination risk: `low`
- Grounded tokens: `reviewMode, reviewWindow, process, PORT, REVIEW_MODE, REVIEW_WINDOW, standard, 7d, env`

Patch preview:

```markdown
## Environment Variables
## Environment Variables
- `REVIEW_WINDOW` sets the review window and defaults to `7d`.
- `REVIEW_MODE` controls the default ticket review mode.
- `process` is a field type.
- `env` is a config variable.
- `PORT` is an environment variable.
- `standard` is a default value.
- `7d` is a default value.
- `reviewMode` is an added field.
- `reviewWindow` is an added field.
```

Warnings:

- normalized patch into lightweight diff form
- patch is longer than a minimal documentation update
