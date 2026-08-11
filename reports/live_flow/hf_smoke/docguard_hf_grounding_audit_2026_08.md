# DocGuard HF Grounding Audit 2026-08

## Original Qwen 1.5B Issue

The first real HuggingFace patch-generation smoke run showed that the optional HF backend can produce more natural documentation prose than the legacy patch generator, but it can also add unsupported details.

For this visible code diff:

```diff
+router.post('/reviews', createReview);
+res.status(201).json({ id: saved.id, reviewStatus: saved.status });
```

the model produced a patch that mentioned details not grounded in the diff, including request field `title`, status examples `"pending"` and `"approved"`, and `status` instead of the visible response field `reviewStatus`.

The earlier verifier returned a clean pass because it found grounded tokens such as `/reviews` and `201`. That was too weak: a patch can contain some correct facts and still hallucinate important contract details.

## Added Fact Extractor

`docguard_llm/fact_extractor.py` now extracts allowed facts from only the supplied diff and docs-before text. It supports API methods, route paths, status codes, response JSON fields, request fields when visible, auth roles, validation min/max values, model fields, env vars, config defaults, test commands, cron expressions, workflow function names, and rate-limit settings.

For the `POST /reviews` example, the allowed facts include:

- method: `POST`
- route path: `/reviews`
- status code: `201`
- response fields: `id`, `reviewStatus`

They do not include `title`, `pending`, `approved`, or plain `status` as a response field.

## Prompt Changes

`build_patch_prompt(...)` now includes an "Allowed facts extracted from the diff" block and explicit constraints:

- only write statements supported by allowed facts
- do not add request fields unless they appear in allowed facts
- do not add response fields unless they appear in allowed facts
- do not add enum/status examples unless visible in allowed facts
- do not invent authentication or security behavior
- do not rewrite the whole document
- generate a minimal patch only

For API prompts, the prompt also says not to include a Request Fields section when request fields are not visible, and to include only visible response fields.

## Verifier Changes

`patch_verifier.py` now checks more than token overlap. It warns or fails on unsupported field names, quoted/example values, security/auth claims, filenames outside the target file, request-field sections without visible request fields, and overly large patches.

The old hallucinated `POST /reviews` patch no longer gets a clean pass because `title`, `pending`, `approved`, and `status` are not allowed facts for that diff.

## Thesis Quality Impact

This improves DocGuard's thesis alignment because patch generation is no longer judged only by surface plausibility. The agent now has an explicit grounding boundary between the code/documentation evidence it observed and the documentation text it is allowed to propose.

This is still not a production guarantee. It is a lightweight rule-based guardrail for a zero-shot/few-shot HF patch-generation phase, and human review remains required.

## Recommended Next HF Smoke Command

Use the same 1.5B model with lower generation entropy:

```bash
python scripts/smoke_hf_patch_generation.py --model Qwen/Qwen2.5-1.5B-Instruct --case-limit 5 --max-new-tokens 192 --temperature 0.1
```

Do not run Qwen 3B or 7B locally in this grounding-audit step.
