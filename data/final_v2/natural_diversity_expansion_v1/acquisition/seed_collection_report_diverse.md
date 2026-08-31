# DocGuard Real PR Seed Collector Report

This report summarizes neutral repo-based sampling of merged public GitHub PRs.

The collector does not assign gold labels and does not decide whether documentation should be updated.
It only creates seed PR URLs for the later candidate builder and manual validation workflow.

- Repositories scanned: `20`
- Seeds accepted: `1100`
- Rejected/skipped PRs: `804`
- Acquisition status: `partial`
- Requirements satisfied: `False`
- Target observed/requested: `1100` / `None`
- Target deficit: `0`
- Minimum language deficits: `{}`
- Collector bucket counts: `{'code_only': 734, 'code_and_docs': 315, 'code_only_tests_or_fixtures': 51}`
- Language hint counts: `{'python': 600, 'typescript': 500}`
- Repository counts per language: `{'python': 10, 'typescript': 9}`
- Candidate bucket counts per language: `{'python': {'code_only': 423, 'code_and_docs': 147, 'code_only_tests_or_fixtures': 30}, 'typescript': {'code_and_docs': 168, 'code_only': 311, 'code_only_tests_or_fixtures': 21}}`
- Reject reason counts: `{'not_merged': 533, 'docs_only_excluded': 181, 'too_many_changed_files': 25, 'other_or_binary_only_excluded': 64, 'too_large_patch': 1}`

## Methodological Boundary

- This is real public GitHub PR sampling.
- No synthetic examples are generated.
- No final labels are assigned here.
- `collector_bucket` is audit metadata for balancing and review planning, not a model label.
- Final evaluation must use only the safe fields produced later by the candidate builder.

## Accepted Seeds

| PR | Repository | Bucket | Language hint | Title |
| --- | --- | --- | --- | --- |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/4040 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | fix: make --use_cache keys hashable for multimodal image/byte requests |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/4068 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | fix(evaluator): report a sample count that does not depend on metric order |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3853 | `eleutherai/lm-evaluation-harness` | `code_and_docs` | `python` | feat(physics_gre): add InflectionAI Physics GRE multiple-choice task |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/4056 | `eleutherai/lm-evaluation-harness` | `code_and_docs` | `python` | Add IndicXNLI Gujarati task (indicxnli_gu) |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3442 | `eleutherai/lm-evaluation-harness` | `code_and_docs` | `python` | Add Uncheatable Eval |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/4059 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | fix(scripts): repair requests_caching.py entrypoint (bad kwargs + helper defined after use) |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/4060 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | chore(pre-commit) |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/4048 | `eleutherai/lm-evaluation-harness` | `code_and_docs` | `python` | fix(ruler): resolve the tokenizer name before the cached lookup |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/4037 | `eleutherai/lm-evaluation-harness` | `code_and_docs` | `python` | fix(minerva_math): stop sqrt shorthand normalization from corrupting indexed roots |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/4039 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | fix(minerva_math): thousands-separator comma strip fuses bare digit tuples ("0,1" -> "01") |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/4034 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | fix(minerva_math): score an answer identical to the gold as correct |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/4045 | `eleutherai/lm-evaluation-harness` | `code_and_docs` | `python` | fix(minerva_math): correct few-shot prompt LaTeX |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3372 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | Fix: Prevent infinite loop when max_seq_lengths < 4096 in prepare_niah.py |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/4054 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | feat(cli): allow key=value to be passed to `--metadata`; linting |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3581 | `eleutherai/lm-evaluation-harness` | `code_and_docs` | `python` | add GreekMMLU (official native-sourced benchmark) task configuration |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/4044 | `eleutherai/lm-evaluation-harness` | `code_and_docs` | `python` | feat(tydiqa): add TyDiQA Gold Passage tasks (9 languages) |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3544 | `eleutherai/lm-evaluation-harness` | `code_and_docs` | `python` | feat(tasks): add LongProc benchmark (6 task types, 16 configs) |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3780 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | feat: add chrf++ aggregation and metric (word_order=2) |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3230 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | Pass dataset_kwargs for Unitxt tasks |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3225 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | Fix the Unitxt init method to set the task name |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/4047 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | Create missing request-cache parent directories |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/2493 | `eleutherai/lm-evaluation-harness` | `code_and_docs` | `python` | kbl-v0.1.1 |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/2093 | `eleutherai/lm-evaluation-harness` | `code_and_docs` | `python` | Add TMLU Benchmark Dataset |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3884 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | Fix MultiChoiceRegexFilter prefix-shadowing of choice text |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3882 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | Fix group stderr to match weight_by_size=False (unweighted) aggregation |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3790 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | Fix ContextSampler crash when few-shot pool contains duplicate eval_doc rows |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/4050 | `eleutherai/lm-evaluation-harness` | `code_only_tests_or_fixtures` | `python` | test(registry): add tests for `higher_is_better` directions |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3993 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | Fix TER metric direction (higher_is_better) and correct chrF docstring |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3885 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | Serialize all numpy scalar types in JSON output, not just int64/int32 |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3984 | `eleutherai/lm-evaluation-harness` | `code_and_docs` | `python` | feat(models): add raw onnxruntime backend for Model Builder ONNX exports |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3670 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | fix: local directory with task name no longer shadows registered task |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/4041 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | fix(med_prescriptions): require both keys before combining complaints and diagnosis |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3657 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | fix: fall back to tokenizer.eos_token when decode returns empty string |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3841 | `eleutherai/lm-evaluation-harness` | `code_and_docs` | `python` | fix(irokobench): repair afrimmlu/afrimgsm/afrixnli task registration and update READMEs |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/4043 | `eleutherai/lm-evaluation-harness` | `code_and_docs` | `python` | Add cieaCOVA task into catalan bench |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3788 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | Add make_table regression coverage |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3784 | `eleutherai/lm-evaluation-harness` | `code_and_docs` | `python` | Add Terretaqa task into Catalanbench |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/4035 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | fix: make delete_cache a no-op when the cache directory is absent |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3887 | `eleutherai/lm-evaluation-harness` | `code_and_docs` | `python` | fix(filters): format_span only normalizes labels, not entity text |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/4003 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | fix: normalize scalar `seed` from a config file the way the CLI does |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/4020 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | fix(config): parse dictionary strings from YAML configs |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3992 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | Enable function resolving for custom tasks |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3960 | `eleutherai/lm-evaluation-harness` | `code_and_docs` | `python` | feat(models): add cross-platform onnxruntime-genai backend + refactor winml |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3991 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | Fix `megatron_lm` backend against Megatron-LM `core_v0.18+`: argument parsing moved out of `initialize_megatron()` |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3959 | `eleutherai/lm-evaluation-harness` | `code_and_docs` | `python` | fix(api): support think_end_token for chat completions |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3995 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | Honor configured timeout for synchronous API requests |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3916 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | fix(huggingface): detect max_length from nested text_config (Gemma3 multimodal) |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/4024 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | chore(megatron): run linter |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/4016 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | fix(hf): pass max_cpu_memory through to accelerate's max_memory |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/4023 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | chore(ci): update pre-commit hooks and workflow packages |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3954 | `eleutherai/lm-evaluation-harness` | `code_and_docs` | `python` | feat(legalbench): add Contract NLI suite (14 NDA entailment tasks) |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3998 | `eleutherai/lm-evaluation-harness` | `code_and_docs` | `python` | Putnam Axiom |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3979 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | fix: resolve fewshot gen_prefix against the fewshot doc, not the eval doc |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3970 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | fix: prevent ValueError when batch_size="auto:N" is passed to API models |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3971 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | fix: prevent ValueError when batch_size="auto" is passed to neuronx model |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3978 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | Exclude eval docs from first-n few-shot samples |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3937 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | Fix fewshot_config.split precedence in TaskConfig |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3923 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | fix(jsonschema_bench): add per-sample validation timeout to prevent eval hangs |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3944 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | fix(afrixnli): use Jinja braces in prompt_1 doc_to_text |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3921 | `eleutherai/lm-evaluation-harness` | `code_and_docs` | `python` | fix(longbench): skip blank leading line in code_sim_score extraction |
| https://github.com/jestjs/jest/pull/16411 | `jestjs/jest` | `code_and_docs` | `typescript` | fix(jest-config): only warn about global-only options where they're actually ignored |
| https://github.com/jestjs/jest/pull/16260 | `jestjs/jest` | `code_and_docs` | `typescript` | feat(jest-resolve): honor `--preserve-symlinks` / `NODE_PRESERVE_SYMLINKS` in the default resolver |
| https://github.com/jestjs/jest/pull/16401 | `jestjs/jest` | `code_only` | `typescript` | chore: migrate `CoverageReporter` test off `mock-fs` |
| https://github.com/jestjs/jest/pull/16404 | `jestjs/jest` | `code_and_docs` | `typescript` | docs: explain `globalsCleanup` and point the JEST-01 warning at it |
| https://github.com/jestjs/jest/pull/16316 | `jestjs/jest` | `code_and_docs` | `typescript` | fix(jest-message-util): print inner errors of AggregateError test failures |
| https://github.com/jestjs/jest/pull/16052 | `jestjs/jest` | `code_and_docs` | `typescript` | Guard missing require.resolve.paths in jest-resolve |
| https://github.com/jestjs/jest/pull/16381 | `jestjs/jest` | `code_and_docs` | `typescript` | fix(jest-util): honor picomatch options when a glob is already cached |
| https://github.com/jestjs/jest/pull/16227 | `jestjs/jest` | `code_and_docs` | `typescript` | fix(reporters): enforce 80 column limit fallback for coverage table i… |
| https://github.com/jestjs/jest/pull/16244 | `jestjs/jest` | `code_and_docs` | `typescript` | fix(jest-runtime, @jest/transform): improve ESM error handling on Node < 24.9 |
| https://github.com/jestjs/jest/pull/16296 | `jestjs/jest` | `code_and_docs` | `typescript` | fix(jest-resolve): isolate virtual mock module IDs |
| https://github.com/jestjs/jest/pull/16226 | `jestjs/jest` | `code_and_docs` | `typescript` | fix(jest-mock): remove leftover own accessor when restoring spyOn of an inherited getter/setter |
| https://github.com/jestjs/jest/pull/16166 | `jestjs/jest` | `code_and_docs` | `typescript` | Make @types/jsdom a peer dependency of jest-environment-jsdom-abstract |
| https://github.com/jestjs/jest/pull/16237 | `jestjs/jest` | `code_and_docs` | `typescript` | fix(jest-mock): walk overloads in ResolveType/RejectType |
| https://github.com/jestjs/jest/pull/16196 | `jestjs/jest` | `code_and_docs` | `typescript` | fix(expect): accept class instances in toMatchObject and objectContaining |
| https://github.com/jestjs/jest/pull/16374 | `jestjs/jest` | `code_and_docs` | `typescript` | feat(jest-snapshot): expose snapshot paths in failure details |
| https://github.com/jestjs/jest/pull/15721 | `jestjs/jest` | `code_and_docs` | `typescript` | chore: bump `unrs-resolver` to 1.12.1, remove `jest-pnp-resolver` and unnecessary checks |
| https://github.com/jestjs/jest/pull/16259 | `jestjs/jest` | `code_and_docs` | `typescript` | feat(collect-tests): expand .each and report accurate per-status counts |
| https://github.com/jestjs/jest/pull/16053 | `jestjs/jest` | `code_and_docs` | `typescript` | feat(jest-mock): add `mock.whenCalledWith(...)` |
| https://github.com/jestjs/jest/pull/16397 | `jestjs/jest` | `code_and_docs` | `typescript` | chore(deps): update glob to v13 |
| https://github.com/jestjs/jest/pull/16399 | `jestjs/jest` | `code_only` | `typescript` | chore(deps): update jayqi/failed-build-issue-action action to v1.3.0 |
| https://github.com/jestjs/jest/pull/16391 | `jestjs/jest` | `code_and_docs` | `typescript` | feat(jest-runtime): automock ESM, sandbox the loader escape hatches, and match Node's graph-error ordering |
| https://github.com/jestjs/jest/pull/16390 | `jestjs/jest` | `code_and_docs` | `typescript` | fix(jest-resolve): apply `moduleNameMapper` to both spellings of core modules |
| https://github.com/jestjs/jest/pull/16389 | `jestjs/jest` | `code_and_docs` | `typescript` | fix(jest-runtime): close ESM mocking, require(esm) and JSON module parity gaps |
| https://github.com/jestjs/jest/pull/16386 | `jestjs/jest` | `code_and_docs` | `typescript` | perf(jest-haste-map): cache the watchman socket path and drop the version probe |
| https://github.com/jestjs/jest/pull/16388 | `jestjs/jest` | `code_and_docs` | `typescript` | fix(jest-resolve): keep the `node:` prefix through async resolution |
| https://github.com/jestjs/jest/pull/16387 | `jestjs/jest` | `code_and_docs` | `typescript` | perf(jest-snapshot): load babel, semver and synckit lazily |
| https://github.com/jestjs/jest/pull/16373 | `jestjs/jest` | `code_and_docs` | `typescript` | perf(jest-resolve): make the warm default-resolver path about 3x cheaper |
| https://github.com/jestjs/jest/pull/16385 | `jestjs/jest` | `code_and_docs` | `typescript` | refactor(jest-runtime): remove dead accessors and collapse duplicated module-loading shapes |
| https://github.com/jestjs/jest/pull/16379 | `jestjs/jest` | `code_and_docs` | `typescript` | fix(jest-core): do not report CustomGC as an open handle |
| https://github.com/jestjs/jest/pull/16377 | `jestjs/jest` | `code_and_docs` | `typescript` | fix(jest-runtime): bind `sandboxInjectedGlobals` to the right values |
| https://github.com/jestjs/jest/pull/16376 | `jestjs/jest` | `code_and_docs` | `typescript` | perf(jest-runtime): cut per-require and per-specifier overhead |
| https://github.com/jestjs/jest/pull/16155 | `jestjs/jest` | `code_and_docs` | `typescript` | fix(jest-console): buffer console output in CustomConsole for reporters |
| https://github.com/jestjs/jest/pull/16375 | `jestjs/jest` | `code_and_docs` | `typescript` | fix(jest-runtime): key ES modules by full URL and share modules between overlapping graphs |
| https://github.com/jestjs/jest/pull/16368 | `jestjs/jest` | `code_and_docs` | `typescript` | fix(jest-runtime): match Node for "type": "commonjs" packages, module.children and data: URIs |
| https://github.com/jestjs/jest/pull/16371 | `jestjs/jest` | `code_and_docs` | `typescript` | perf(jest-resolve): cut repeated work on the resolution hot path |
| https://github.com/jestjs/jest/pull/16370 | `jestjs/jest` | `code_and_docs` | `typescript` | fix(jest-resolve): build and cache `data:` URI module IDs the same way sync and async |
| https://github.com/jestjs/jest/pull/16369 | `jestjs/jest` | `code_and_docs` | `typescript` | fix(jest-resolve): repair the `shouldLoadAsEsm` lookup caches |
| https://github.com/jestjs/jest/pull/16367 | `jestjs/jest` | `code_and_docs` | `typescript` | fix(jest-runtime): mirror Node's ESM/CJS interop and entry-point metadata |
| https://github.com/jestjs/jest/pull/16366 | `jestjs/jest` | `code_and_docs` | `typescript` | fix(jest-runtime): throw ERR_REQUIRE_CYCLE_MODULE on require(esm) re-entry |
| https://github.com/jestjs/jest/pull/16364 | `jestjs/jest` | `code_and_docs` | `typescript` | fix(jest-runtime): gate ESM registry reuse on module status |
| https://github.com/jestjs/jest/pull/16363 | `jestjs/jest` | `code_and_docs` | `typescript` | fix(jest-runtime): terminate CJS export analysis on circular re-exports |
| https://github.com/jestjs/jest/pull/16365 | `jestjs/jest` | `code_and_docs` | `typescript` | fix(jest-runtime): scope module mocks to the isolation block that made them |
| https://github.com/jestjs/jest/pull/16322 | `jestjs/jest` | `code_and_docs` | `typescript` | [jest-circus] Add describe-level retries |
| https://github.com/jestjs/jest/pull/16360 | `jestjs/jest` | `code_and_docs` | `typescript` | fix(jest-haste-map): keep a duplicated mock name alive when its file goes |
| https://github.com/jestjs/jest/pull/16358 | `jestjs/jest` | `code_and_docs` | `typescript` | fix(jest-haste-map): tolerate a locked file while indexing on Windows |
| https://github.com/jestjs/jest/pull/16352 | `jestjs/jest` | `code_and_docs` | `typescript` | fix(jest-haste-map): tighten the cache key and the watched-extension match |
| https://github.com/jestjs/jest/pull/16354 | `jestjs/jest` | `code_and_docs` | `typescript` | fix(jest-haste-map): end the worker farm when the build aborts synchronously |
| https://github.com/jestjs/jest/pull/16355 | `jestjs/jest` | `code_and_docs` | `typescript` | fix(jest-haste-map): attach the watchman client's error listener before use |
| https://github.com/jestjs/jest/pull/16351 | `jestjs/jest` | `code_and_docs` | `typescript` | perf(jest-haste-map): reuse cached metadata for duplicated haste names |
| https://github.com/jestjs/jest/pull/16353 | `jestjs/jest` | `code_and_docs` | `typescript` | fix(jest-haste-map): restore the nested duplicates index in `ModuleMap.fromJSON` |
| https://github.com/jestjs/jest/pull/16348 | `jestjs/jest` | `code_and_docs` | `typescript` | fix: Keep hinted snapshots with their own test |
| https://github.com/jestjs/jest/pull/16347 | `jestjs/jest` | `code_and_docs` | `typescript` | [jest-circus, jest-jasmine2] Fix error-handler restore, `--expand` for assert diffs, and generator test context |
| https://github.com/jestjs/jest/pull/16344 | `jestjs/jest` | `code_and_docs` | `typescript` | [jest-circus, jest-snapshot] Preserve unrelated inline snapshots across test retries |
| https://github.com/jestjs/jest/pull/16346 | `jestjs/jest` | `code_only` | `typescript` | chore: unbreak the TypeScript compatibility job after @tsconfig/node18@18.2.7 |
| https://github.com/jestjs/jest/pull/16343 | `jestjs/jest` | `code_and_docs` | `typescript` | [jest-circus] Isolate done callback state between invocations |
| https://github.com/jestjs/jest/pull/16342 | `jestjs/jest` | `code_and_docs` | `typescript` | [jest-circus] Clear the current test after skipped and todo tests |
| https://github.com/jestjs/jest/pull/16332 | `jestjs/jest` | `code_and_docs` | `typescript` | fix(jest-resolve): load a user resolver written as an ES module |
| https://github.com/jestjs/jest/pull/16341 | `jestjs/jest` | `code_and_docs` | `typescript` | fix(jest-runtime): give `fs` and `node:fs` one ESM namespace |
| https://github.com/jestjs/jest/pull/16338 | `jestjs/jest` | `code_and_docs` | `typescript` | fix(jest-each): serialize bigint values in `%j` titles |
| https://github.com/jestjs/jest/pull/16333 | `jestjs/jest` | `code_and_docs` | `typescript` | fix(pretty-format): move the react-is aliases into the `@jest` scope |
| https://github.com/astral-sh/ty/pull/4426 | `astral-sh/ty` | `code_and_docs` | `python` | Bump version to 0.0.76 |
| https://github.com/astral-sh/ty/pull/4398 | `astral-sh/ty` | `code_only` | `python` | Improve `uv-lock` pre-commit configuration |
| https://github.com/astral-sh/ty/pull/4396 | `astral-sh/ty` | `code_and_docs` | `python` | Bump version to 0.0.75 |
| https://github.com/astral-sh/ty/pull/4392 | `astral-sh/ty` | `code_only` | `python` | Update prek dependencies |
| https://github.com/astral-sh/ty/pull/4351 | `astral-sh/ty` | `code_and_docs` | `python` | Bump version to 0.0.74 |
| https://github.com/astral-sh/ty/pull/4336 | `astral-sh/ty` | `code_only` | `python` | Remove Zulip from the PGO training |
| https://github.com/astral-sh/ty/pull/4333 | `astral-sh/ty` | `code_only` | `python` | Use the versions bot's ruleset bypass when merging |
| https://github.com/astral-sh/ty/pull/4325 | `astral-sh/ty` | `code_only` | `python` | Update prek dependencies |
| https://github.com/astral-sh/ty/pull/4326 | `astral-sh/ty` | `code_only` | `python` | Update dependency python to 3.14 |
| https://github.com/astral-sh/ty/pull/4327 | `astral-sh/ty` | `code_only` | `python` | Update astral-sh/setup-uv action to v10 |
| https://github.com/astral-sh/ty/pull/4322 | `astral-sh/ty` | `code_and_docs` | `python` | Bump version to 0.0.73 |
| https://github.com/astral-sh/ty/pull/4317 | `astral-sh/ty` | `code_only` | `python` | Disable known GitHub cache clients in release workflows |
| https://github.com/astral-sh/ty/pull/4319 | `astral-sh/ty` | `code_only` | `python` | Harden release workflow permissions and shell inputs |
| https://github.com/astral-sh/ty/pull/4321 | `astral-sh/ty` | `code_only` | `python` | Disable cache-aware actions throughout release workflows |
| https://github.com/astral-sh/ty/pull/4313 | `astral-sh/ty` | `code_only` | `python` | Require wheels for Python tooling dependencies |
| https://github.com/astral-sh/ty/pull/4315 | `astral-sh/ty` | `code_and_docs` | `python` | Manage docs build with a dep group |
| https://github.com/astral-sh/ty/pull/4281 | `astral-sh/ty` | `code_only` | `python` | Add dependency cooldowns |
| https://github.com/astral-sh/ty/pull/4268 | `astral-sh/ty` | `code_and_docs` | `python` | Bump version to 0.0.72 |
| https://github.com/astral-sh/ty/pull/4244 | `astral-sh/ty` | `code_and_docs` | `python` | Bump version to 0.0.71 |
| https://github.com/astral-sh/ty/pull/4236 | `astral-sh/ty` | `code_only` | `python` | Validate the PGO pipeline in CI |
| https://github.com/astral-sh/ty/pull/4218 | `astral-sh/ty` | `code_only` | `python` | Enable PGO for Linux ARM64 ty releases |
| https://github.com/astral-sh/ty/pull/4217 | `astral-sh/ty` | `code_only` | `python` | Enable PGO for Windows x86-64 ty releases |
| https://github.com/astral-sh/ty/pull/4216 | `astral-sh/ty` | `code_only` | `python` | Enable PGO for macOS ARM64 ty releases |
| https://github.com/astral-sh/ty/pull/4213 | `astral-sh/ty` | `code_only` | `python` | Enable PGO for Linux x86-64 ty releases |
| https://github.com/astral-sh/ty/pull/4224 | `astral-sh/ty` | `code_only` | `python` | Use Depot runners for release builds |
| https://github.com/astral-sh/ty/pull/4235 | `astral-sh/ty` | `code_only` | `python` | Use an eight-core Ubuntu 24.04 runner for prek CI |
| https://github.com/astral-sh/ty/pull/4228 | `astral-sh/ty` | `code_and_docs` | `python` | Bump version to 0.0.70 |
| https://github.com/astral-sh/ty/pull/4200 | `astral-sh/ty` | `code_only` | `python` | Link to actual docs page rather than README in issue creation menu "Documentation" link |
| https://github.com/astral-sh/ty/pull/4202 | `astral-sh/ty` | `code_and_docs` | `python` | Bump version to 0.0.69 |
| https://github.com/astral-sh/ty/pull/4199 | `astral-sh/ty` | `code_and_docs` | `python` | Bump version to 0.0.68 |
| https://github.com/astral-sh/ty/pull/4192 | `astral-sh/ty` | `code_and_docs` | `python` | Bump version to 0.0.67 |
| https://github.com/astral-sh/ty/pull/4190 | `astral-sh/ty` | `code_only` | `python` | release: use self-repo references |
| https://github.com/astral-sh/ty/pull/4189 | `astral-sh/ty` | `code_only` | `python` | Update bug report issue template |
| https://github.com/astral-sh/ty/pull/4178 | `astral-sh/ty` | `code_only` | `python` | Update prek dependencies |
| https://github.com/astral-sh/ty/pull/4177 | `astral-sh/ty` | `code_only` | `python` | Update dependency prek to v0.4.11 |
| https://github.com/astral-sh/ty/pull/4179 | `astral-sh/ty` | `code_only` | `python` | Update docker/login-action action to v4.5.2 |
| https://github.com/astral-sh/ty/pull/4166 | `astral-sh/ty` | `code_and_docs` | `python` | Bump version to 0.0.66 |
| https://github.com/astral-sh/ty/pull/4113 | `astral-sh/ty` | `code_and_docs` | `python` | Bump version to 0.0.65 |
| https://github.com/astral-sh/ty/pull/4110 | `astral-sh/ty` | `code_only` | `python` | Update actions/setup-python action to v7 |
| https://github.com/astral-sh/ty/pull/4107 | `astral-sh/ty` | `code_only` | `python` | Update actions/checkout action to v7.0.1 |
| https://github.com/astral-sh/ty/pull/4108 | `astral-sh/ty` | `code_only` | `python` | Update dependency prek to v0.4.10 |
| https://github.com/astral-sh/ty/pull/4109 | `astral-sh/ty` | `code_only` | `python` | Update prek dependencies |
| https://github.com/astral-sh/ty/pull/4097 | `astral-sh/ty` | `code_and_docs` | `python` | Bump version to 0.0.64 |
| https://github.com/astral-sh/ty/pull/4071 | `astral-sh/ty` | `code_and_docs` | `python` | Bump version to 0.0.63 |
| https://github.com/astral-sh/ty/pull/4057 | `astral-sh/ty` | `code_and_docs` | `python` | Bump version to 0.0.62 |
| https://github.com/astral-sh/ty/pull/4059 | `astral-sh/ty` | `code_only` | `python` | Update prek dependencies |
| https://github.com/astral-sh/ty/pull/4060 | `astral-sh/ty` | `code_only` | `python` | Update astral-sh/setup-uv action to v9 |
| https://github.com/astral-sh/ty/pull/4058 | `astral-sh/ty` | `code_only` | `python` | Update dependency prek to v0.4.9 |
| https://github.com/astral-sh/ty/pull/4027 | `astral-sh/ty` | `code_and_docs` | `python` | Bump version to 0.0.61 |
| https://github.com/astral-sh/ty/pull/4008 | `astral-sh/ty` | `code_and_docs` | `python` | Bump version to 0.0.60 |
| https://github.com/astral-sh/ty/pull/3997 | `astral-sh/ty` | `code_only` | `python` | Update astral-sh/setup-uv action to v8.3.2 |
| https://github.com/astral-sh/ty/pull/3999 | `astral-sh/ty` | `code_only` | `python` | Update prek dependencies |
| https://github.com/astral-sh/ty/pull/3998 | `astral-sh/ty` | `code_only` | `python` | Update dependency prek to v0.4.8 |
| https://github.com/astral-sh/ty/pull/4000 | `astral-sh/ty` | `code_only` | `python` | Update docker/build-push-action action to v7.3.0 |
| https://github.com/astral-sh/ty/pull/4001 | `astral-sh/ty` | `code_only` | `python` | Update docker/login-action action to v4.4.0 |
| https://github.com/astral-sh/ty/pull/4002 | `astral-sh/ty` | `code_only` | `python` | Update docker/metadata-action action to v6.2.0 |
| https://github.com/astral-sh/ty/pull/4003 | `astral-sh/ty` | `code_only` | `python` | Update docker/setup-buildx-action action to v4.2.0 |
| https://github.com/astral-sh/ty/pull/3979 | `astral-sh/ty` | `code_and_docs` | `python` | Bump version to 0.0.59 |
| https://github.com/astral-sh/ty/pull/3955 | `astral-sh/ty` | `code_and_docs` | `python` | Bump version to 0.0.58 |
| https://github.com/astral-sh/ty/pull/3927 | `astral-sh/ty` | `code_and_docs` | `python` | Bump version to 0.0.57 |
| https://github.com/rossoctl/rossoctl/pull/2484 | `rossoctl/rossoctl` | `code_only` | `python` | fix: Explain when Context Service is disabled |
| https://github.com/rossoctl/rossoctl/pull/2483 | `rossoctl/rossoctl` | `code_and_docs` | `python` | feat: proxy context storage class discovery |
| https://github.com/rossoctl/rossoctl/pull/2494 | `rossoctl/rossoctl` | `code_only` | `python` | build(deps): Bump python from `ce40764` to `cae66f2` in /rossoctl/auth/agent-oauth-secret |
| https://github.com/rossoctl/rossoctl/pull/2495 | `rossoctl/rossoctl` | `code_only` | `python` | build(deps): Bump python from `ce40764` to `cae66f2` in /rossoctl/auth/api-oauth-secret |
| https://github.com/rossoctl/rossoctl/pull/2496 | `rossoctl/rossoctl` | `code_only` | `python` | build(deps): Bump the minor-and-patch group in /rossoctl/ui-v2 with 3 updates |
| https://github.com/rossoctl/rossoctl/pull/2493 | `rossoctl/rossoctl` | `code_only` | `python` | build(deps): Bump python from `ce40764` to `cae66f2` in /rossoctl/backend |
| https://github.com/rossoctl/rossoctl/pull/2492 | `rossoctl/rossoctl` | `code_only` | `python` | build(deps): Bump python from `ce40764` to `cae66f2` in /rossoctl/auth/mlflow-oauth-secret |
| https://github.com/rossoctl/rossoctl/pull/2491 | `rossoctl/rossoctl` | `code_only` | `python` | build(deps): Bump python from `ce40764` to `cae66f2` in /rossoctl/auth/ui-oauth-secret |
| https://github.com/rossoctl/rossoctl/pull/2488 | `rossoctl/rossoctl` | `code_only` | `python` | feat(backend): accept AuthBridge plugin preset and pass onto AgentRuntime.spec |
| https://github.com/rossoctl/rossoctl/pull/2486 | `rossoctl/rossoctl` | `code_only` | `python` | fix(chart): only manage openai-secret when secrets.openaiApiKey is set |
| https://github.com/rossoctl/rossoctl/pull/2497 | `rossoctl/rossoctl` | `code_only` | `python` | build(deps): Bump the minor-and-patch group with 5 updates |
| https://github.com/rossoctl/rossoctl/pull/2478 | `rossoctl/rossoctl` | `code_only` | `python` | build(deps): Bump the minor-and-patch group across 1 directory with 5 updates |
| https://github.com/rossoctl/rossoctl/pull/2458 | `rossoctl/rossoctl` | `code_only` | `python` | build(deps): Bump nginx from `4a73073` to `db35bfc` in /rossoctl/ui-v2 |
| https://github.com/rossoctl/rossoctl/pull/2454 | `rossoctl/rossoctl` | `code_only_tests_or_fixtures` | `python` | fix(e2e): repair SPIFFE trust chain in tx-e2e token-exchange leg |
| https://github.com/rossoctl/rossoctl/pull/2460 | `rossoctl/rossoctl` | `code_only` | `python` | build(deps): Bump the minor-and-patch group across 1 directory with 6 updates |
| https://github.com/rossoctl/rossoctl/pull/2371 | `rossoctl/rossoctl` | `code_and_docs` | `python` | chore: Remove migrated github-pr-review skill |
| https://github.com/rossoctl/rossoctl/pull/2452 | `rossoctl/rossoctl` | `code_only` | `python` | feat: feature-flagged mesh self-heal CronJob |
| https://github.com/rossoctl/rossoctl/pull/2456 | `rossoctl/rossoctl` | `code_only` | `python` | CI: gate floating image tags in rendered subcharts (#2389) |
| https://github.com/rossoctl/rossoctl/pull/2453 | `rossoctl/rossoctl` | `code_only` | `python` | fix: constrain agent route path params to RFC-1123 |
| https://github.com/rossoctl/rossoctl/pull/2403 | `rossoctl/rossoctl` | `code_and_docs` | `python` | Fix: derive pinnable images from values + fix yq write path in pin-release-tags.sh |
| https://github.com/rossoctl/rossoctl/pull/2447 | `rossoctl/rossoctl` | `code_and_docs` | `python` | Feat: report attached contexts in agent detail responses |
| https://github.com/rossoctl/rossoctl/pull/2448 | `rossoctl/rossoctl` | `code_only` | `python` | CI: gate broken relative links in changed docs (#2412) |
| https://github.com/rossoctl/rossoctl/pull/2404 | `rossoctl/rossoctl` | `code_and_docs` | `python` | test(e2e): cover inbound mTLS and the ambient/HBONE path in transparent inbound |
| https://github.com/rossoctl/rossoctl/pull/2399 | `rossoctl/rossoctl` | `code_and_docs` | `python` | chore(release): pin image tags for v0.8.0-alpha.1 |
| https://github.com/rossoctl/rossoctl/pull/2393 | `rossoctl/rossoctl` | `code_and_docs` | `python` | test: Add transparent inbound interception E2E suite |
| https://github.com/rossoctl/rossoctl/pull/2397 | `rossoctl/rossoctl` | `code_only` | `python` | feat: Report backend version from GET /auth/config |
| https://github.com/rossoctl/rossoctl/pull/2240 | `rossoctl/rossoctl` | `code_only` | `python` | build(deps): Bump python from `5b3879b` to `ce40764` in /rossoctl/auth/mlflow-oauth-secret |
| https://github.com/rossoctl/rossoctl/pull/2239 | `rossoctl/rossoctl` | `code_only` | `python` | build(deps): Bump python from `5b3879b` to `ce40764` in /rossoctl/auth/ui-oauth-secret |
| https://github.com/rossoctl/rossoctl/pull/2237 | `rossoctl/rossoctl` | `code_only` | `python` | build(deps): Bump python from `5b3879b` to `ce40764` in /rossoctl/backend |
| https://github.com/rossoctl/rossoctl/pull/2236 | `rossoctl/rossoctl` | `code_only` | `python` | build(deps): Bump python from `5b3879b` to `ce40764` in /rossoctl/auth/api-oauth-secret |
| https://github.com/rossoctl/rossoctl/pull/2235 | `rossoctl/rossoctl` | `code_only` | `python` | build(deps): Bump python from `5b3879b` to `ce40764` in /rossoctl/auth/agent-oauth-secret |
| https://github.com/rossoctl/rossoctl/pull/2388 | `rossoctl/rossoctl` | `code_only` | `python` | Refactor: Split agents.py router into modules under 1000 lines |
| https://github.com/rossoctl/rossoctl/pull/2233 | `rossoctl/rossoctl` | `code_only` | `python` | build(deps): Bump nginx from `8b1e787` to `4a73073` in /rossoctl/ui-v2 |
| https://github.com/rossoctl/rossoctl/pull/2385 | `rossoctl/rossoctl` | `code_only` | `python` | build(deps): Bump hadolint/hadolint-action from 3.3.0 to 3.4.0 in the minor-and-patch group |
| https://github.com/rossoctl/rossoctl/pull/2216 | `rossoctl/rossoctl` | `code_only` | `python` | fix(ui): surface actual backend cause for 409/502 reseed failures in extractReseedError |
| https://github.com/rossoctl/rossoctl/pull/2335 | `rossoctl/rossoctl` | `code_only` | `python` | fix(backend): fall back to legacy agent card endpoint |
| https://github.com/rossoctl/rossoctl/pull/2384 | `rossoctl/rossoctl` | `code_only` | `python` | build(deps): Bump the minor-and-patch group across 1 directory with 8 updates |
| https://github.com/rossoctl/rossoctl/pull/2392 | `rossoctl/rossoctl` | `code_and_docs` | `python` | feat: integrate optional Context Service |
| https://github.com/rossoctl/rossoctl/pull/2386 | `rossoctl/rossoctl` | `code_only` | `python` | build(deps): Bump astral-sh/setup-uv from 9.0.0 to 10.0.1 in the major group across 1 directory |
| https://github.com/rossoctl/rossoctl/pull/2383 | `rossoctl/rossoctl` | `code_only` | `python` | feat: allow k8sResourceLimits/k8sResourceRequests overrides for agents and tools |
| https://github.com/rossoctl/rossoctl/pull/2271 | `rossoctl/rossoctl` | `code_only` | `python` | build(deps): Bump the major group across 1 directory with 3 updates |
| https://github.com/rossoctl/rossoctl/pull/2372 | `rossoctl/rossoctl` | `code_only` | `python` | build(deps): Bump the minor-and-patch group across 1 directory with 9 updates |
| https://github.com/rossoctl/rossoctl/pull/859 | `rossoctl/rossoctl` | `code_only` | `python` | fix: grant stale workflow the permissions it needs |
| https://github.com/rossoctl/rossoctl/pull/749 | `rossoctl/rossoctl` | `code_only` | `python` | CI: Use org-wide reusable stale workflow |
| https://github.com/rossoctl/rossoctl/pull/1607 | `rossoctl/rossoctl` | `code_only` | `python` | fix(charts): Add pinned defaults for utility images in templates |
| https://github.com/rossoctl/rossoctl/pull/1383 | `rossoctl/rossoctl` | `code_only` | `python` | CI: Add PR title verifier workflow |
| https://github.com/rossoctl/rossoctl/pull/2198 | `rossoctl/rossoctl` | `code_only` | `python` | feat(dreaming): trajectory-driven skill optimization via ask-runspace |
| https://github.com/rossoctl/rossoctl/pull/2369 | `rossoctl/rossoctl` | `code_only` | `python` | feat: Add PUT /{namespace}/{name}/identity-config endpoint |
| https://github.com/rossoctl/rossoctl/pull/2245 | `rossoctl/rossoctl` | `code_only` | `python` | Fix: bump operator-chart dependency to 0.3.0-alpha.9 |
| https://github.com/rossoctl/rossoctl/pull/2359 | `rossoctl/rossoctl` | `code_only` | `python` | ci(e2e): make community-KC token-exchange leg non-fatal (#2342) |
| https://github.com/rossoctl/rossoctl/pull/1583 | `rossoctl/rossoctl` | `code_and_docs` | `python` | Adding a Kagenti Demo App |
| https://github.com/rossoctl/rossoctl/pull/2343 | `rossoctl/rossoctl` | `code_only` | `python` | feat(ui): add "Open Data Governance" observability card |
| https://github.com/rossoctl/rossoctl/pull/2212 | `rossoctl/rossoctl` | `code_only` | `python` | fix(autosync): re-sync skill content on change, not just version |
| https://github.com/rossoctl/rossoctl/pull/2338 | `rossoctl/rossoctl` | `code_only` | `python` | fix: 🐛 Publish operator-spiffe-bootstrap image via CI |
| https://github.com/rossoctl/rossoctl/pull/2322 | `rossoctl/rossoctl` | `code_only` | `python` | fix(backend): resolve OpenShift Route targetPort by service port name |
| https://github.com/rossoctl/rossoctl/pull/2313 | `rossoctl/rossoctl` | `code_only` | `python` | fix: :goal_net::white_check_mark: Pin backend MCP and surface MLFlow auth errors |
| https://github.com/rossoctl/rossoctl/pull/2278 | `rossoctl/rossoctl` | `code_only` | `python` | Fix: New icon letter and color (Rename Kagenti to Rossoctl) |
| https://github.com/rossoctl/rossoctl/pull/2251 | `rossoctl/rossoctl` | `code_only` | `python` | fix(simulated-tools): adopt workloads via AgentRuntime instead of self-labeling |
| https://github.com/rossoctl/rossoctl/pull/2246 | `rossoctl/rossoctl` | `code_only` | `python` | chore(release): pin image tags for v0.7.0-alpha.6 |
| https://github.com/rossoctl/rossoctl/pull/2243 | `rossoctl/rossoctl` | `code_and_docs` | `python` | Refactor: Rename rossocortex → cortex; fix cortex webhook-chart name |
| https://github.com/marshmallow-code/marshmallow/pull/3034 | `marshmallow-code/marshmallow` | `code_only` | `python` | Various docstring fixes |
| https://github.com/marshmallow-code/marshmallow/pull/3004 | `marshmallow-code/marshmallow` | `code_only` | `python` | Raise ValidationError (not ValueError) for NaN in TimeDelta |
| https://github.com/marshmallow-code/marshmallow/pull/3024 | `marshmallow-code/marshmallow` | `code_only` | `python` | Simplify `get_value` to match actual usage |
| https://github.com/marshmallow-code/marshmallow/pull/3016 | `marshmallow-code/marshmallow` | `code_and_docs` | `python` | Fix URL validator rejecting a fragment after an empty path |
| https://github.com/marshmallow-code/marshmallow/pull/3015 | `marshmallow-code/marshmallow` | `code_only` | `python` | Pre commit autoupdate |
| https://github.com/marshmallow-code/marshmallow/pull/3011 | `marshmallow-code/marshmallow` | `code_only` | `python` | Update all dependencies |
| https://github.com/marshmallow-code/marshmallow/pull/2994 | `marshmallow-code/marshmallow` | `code_and_docs` | `python` | Enum Allow None Default |
| https://github.com/marshmallow-code/marshmallow/pull/2993 | `marshmallow-code/marshmallow` | `code_only` | `python` | [pre-commit.ci] pre-commit autoupdate |
| https://github.com/marshmallow-code/marshmallow/pull/2990 | `marshmallow-code/marshmallow` | `code_only` | `python` | Update all dependencies |
| https://github.com/marshmallow-code/marshmallow/pull/2988 | `marshmallow-code/marshmallow` | `code_only` | `python` | Simplify use of self.opts.index_errors in _deserialize |
| https://github.com/marshmallow-code/marshmallow/pull/2983 | `marshmallow-code/marshmallow` | `code_only` | `python` | Respect uv.lock in tox envs |
| https://github.com/marshmallow-code/marshmallow/pull/2974 | `marshmallow-code/marshmallow` | `code_and_docs` | `python` | Link to shared CoC and CONTRIBUTING.md |
| https://github.com/marshmallow-code/marshmallow/pull/2973 | `marshmallow-code/marshmallow` | `code_only` | `python` | [pre-commit.ci] pre-commit autoupdate |
| https://github.com/marshmallow-code/marshmallow/pull/2965 | `marshmallow-code/marshmallow` | `code_only` | `python` | [pre-commit.ci] pre-commit autoupdate |
| https://github.com/marshmallow-code/marshmallow/pull/2962 | `marshmallow-code/marshmallow` | `code_only` | `python` | Update astral-sh/setup-uv action to v8 |
| https://github.com/marshmallow-code/marshmallow/pull/2960 | `marshmallow-code/marshmallow` | `code_only` | `python` | chore: set dependency cooldown in uv |
| https://github.com/marshmallow-code/marshmallow/pull/2952 | `marshmallow-code/marshmallow` | `code_only` | `python` | Harden CI; add zizmor |
| https://github.com/marshmallow-code/marshmallow/pull/2950 | `marshmallow-code/marshmallow` | `code_only` | `python` | Pin dependencies |
| https://github.com/marshmallow-code/marshmallow/pull/2947 | `marshmallow-code/marshmallow` | `code_only` | `python` | Switch to renovate |
| https://github.com/marshmallow-code/marshmallow/pull/2948 | `marshmallow-code/marshmallow` | `code_only` | `python` | pre-commit autoupdate |
| https://github.com/marshmallow-code/marshmallow/pull/2799 | `marshmallow-code/marshmallow` | `code_and_docs` | `python` | Add pre/post_load parameters to Field |
| https://github.com/marshmallow-code/marshmallow/pull/2940 | `marshmallow-code/marshmallow` | `code_and_docs` | `python` | Typing improvements to marshmallow.validate |
| https://github.com/marshmallow-code/marshmallow/pull/2939 | `marshmallow-code/marshmallow` | `code_only` | `python` | Remove redundant docs job |
| https://github.com/marshmallow-code/marshmallow/pull/2937 | `marshmallow-code/marshmallow` | `code_and_docs` | `python` | Fix validate.Email to accept IDNs |
| https://github.com/marshmallow-code/marshmallow/pull/2935 | `marshmallow-code/marshmallow` | `code_and_docs` | `python` | Fix Unreachable Warning |
| https://github.com/marshmallow-code/marshmallow/pull/2932 | `marshmallow-code/marshmallow` | `code_only` | `python` | Remove redundant python-version |
| https://github.com/marshmallow-code/marshmallow/pull/2928 | `marshmallow-code/marshmallow` | `code_and_docs` | `python` | Add support for IDNs to validate.URL |
| https://github.com/marshmallow-code/marshmallow/pull/2930 | `marshmallow-code/marshmallow` | `code_and_docs` | `python` | Migrate to uv and use dependency groups |
| https://github.com/marshmallow-code/marshmallow/pull/2929 | `marshmallow-code/marshmallow` | `code_only` | `python` | Bump autodocsumm from 0.2.14 to 0.2.15 |
| https://github.com/marshmallow-code/marshmallow/pull/2906 | `marshmallow-code/marshmallow` | `code_and_docs` | `python` | Add ipaddress types to Schema.TYPE_MAPPING |
| https://github.com/marshmallow-code/marshmallow/pull/2907 | `marshmallow-code/marshmallow` | `code_and_docs` | `python` | Fix Field.error_messages type to allow dict and list values |
| https://github.com/marshmallow-code/marshmallow/pull/2926 | `marshmallow-code/marshmallow` | `code_only` | `python` | Update package metadata to comply with PEP 639 |
| https://github.com/marshmallow-code/marshmallow/pull/2904 | `marshmallow-code/marshmallow` | `code_and_docs` | `python` | Reject booleans in from_timestamp_ms, consistent with from_timestamp |
| https://github.com/marshmallow-code/marshmallow/pull/2902 | `marshmallow-code/marshmallow` | `code_and_docs` | `python` | Fix Enum field by-name lookup to only return actual members |
| https://github.com/marshmallow-code/marshmallow/pull/2903 | `marshmallow-code/marshmallow` | `code_and_docs` | `python` | Fix nested partial to use attr_name instead of data_key for prefix |
| https://github.com/marshmallow-code/marshmallow/pull/2909 | `marshmallow-code/marshmallow` | `code_and_docs` | `python` | Fix OneOf.options() emitting phantom entries when labels outnumber choices |
| https://github.com/marshmallow-code/marshmallow/pull/2901 | `marshmallow-code/marshmallow` | `code_and_docs` | `python` | Fix Constant field with required=True raising ValueError |
| https://github.com/marshmallow-code/marshmallow/pull/2925 | `marshmallow-code/marshmallow` | `code_and_docs` | `python` | Make Number and Mapping abstract base classes |
| https://github.com/marshmallow-code/marshmallow/pull/2919 | `marshmallow-code/marshmallow` | `code_only` | `python` | Bump sphinx-issues from 5.0.1 to 6.0.0 |
| https://github.com/marshmallow-code/marshmallow/pull/2914 | `marshmallow-code/marshmallow` | `code_only` | `python` | [pre-commit.ci] pre-commit autoupdate |
| https://github.com/marshmallow-code/marshmallow/pull/2913 | `marshmallow-code/marshmallow` | `code_only` | `python` | Bump actions/upload-artifact from 6 to 7 |
| https://github.com/marshmallow-code/marshmallow/pull/2912 | `marshmallow-code/marshmallow` | `code_only` | `python` | Bump actions/download-artifact from 7 to 8 |
| https://github.com/marshmallow-code/marshmallow/pull/1220 | `marshmallow-code/marshmallow` | `code_and_docs` | `python` | Pass many and partial to processor methods |
| https://github.com/marshmallow-code/marshmallow/pull/293 | `marshmallow-code/marshmallow` | `code_and_docs` | `python` | Add support for partial loading |
| https://github.com/marshmallow-code/marshmallow/pull/847 | `marshmallow-code/marshmallow` | `code_only` | `python` | Enforce consistent quoting |
| https://github.com/marshmallow-code/marshmallow/pull/94 | `marshmallow-code/marshmallow` | `code_only` | `python` | Class-based validators |
| https://github.com/marshmallow-code/marshmallow/pull/2894 | `marshmallow-code/marshmallow` | `code_and_docs` | `python` | Fix Constant field rejecting None values during load |
| https://github.com/marshmallow-code/marshmallow/pull/2896 | `marshmallow-code/marshmallow` | `code_only` | `python` | [pre-commit.ci] pre-commit autoupdate |
| https://github.com/marshmallow-code/marshmallow/pull/2892 | `marshmallow-code/marshmallow` | `code_only` | `python` | fix: handle uppercase `file` URLs  |
| https://github.com/marshmallow-code/marshmallow/pull/2887 | `marshmallow-code/marshmallow` | `code_only` | `python` | [pre-commit.ci] pre-commit autoupdate |
| https://github.com/marshmallow-code/marshmallow/pull/2854 | `marshmallow-code/marshmallow` | `code_and_docs` | `python` | feat: improve consistency of many arg with nested schema |
| https://github.com/marshmallow-code/marshmallow/pull/2884 | `marshmallow-code/marshmallow` | `code_only` | `python` | Bump actions/upload-artifact from 5 to 6 |
| https://github.com/marshmallow-code/marshmallow/pull/2885 | `marshmallow-code/marshmallow` | `code_only` | `python` | Bump actions/download-artifact from 6 to 7 |
| https://github.com/marshmallow-code/marshmallow/pull/2875 | `marshmallow-code/marshmallow` | `code_only` | `python` | Bump furo from 2025.9.25 to 2025.12.19 |
| https://github.com/marshmallow-code/marshmallow/pull/2883 | `marshmallow-code/marshmallow` | `code_only` | `python` | Remove unused ignore |
| https://github.com/marshmallow-code/marshmallow/pull/2878 | `marshmallow-code/marshmallow` | `code_only` | `python` | 3.x mypy unreachable |
| https://github.com/marshmallow-code/marshmallow/pull/2877 | `marshmallow-code/marshmallow` | `code_only` | `python` | 3.x delint |
| https://github.com/marshmallow-code/marshmallow/pull/2876 | `marshmallow-code/marshmallow` | `code_only` | `python` | Delint |
| https://github.com/marshmallow-code/marshmallow/pull/2874 | `marshmallow-code/marshmallow` | `code_and_docs` | `python` | Fix: Case sensitivity in validator |
| https://github.com/marshmallow-code/marshmallow/pull/2873 | `marshmallow-code/marshmallow` | `code_only` | `python` | Bump actions/checkout from 5 to 6 |
| https://github.com/ansible/ansible-runner/pull/1544 | `ansible/ansible-runner` | `code_only` | `python` | ci: Remove tox Python factors (#1542) |
| https://github.com/ansible/ansible-runner/pull/1542 | `ansible/ansible-runner` | `code_only` | `python` | ci: Remove tox Python factors |
| https://github.com/ansible/ansible-runner/pull/1530 | `ansible/ansible-runner` | `code_and_docs` | `python` | Deprecate bwrap and fact cache APIs |
| https://github.com/ansible/ansible-runner/pull/1540 | `ansible/ansible-runner` | `code_only` | `python` | [PR #1535/0b951b3c backport][release_2.4] 🧪 Cross-integrate coverage and test reports across envs |
| https://github.com/ansible/ansible-runner/pull/1535 | `ansible/ansible-runner` | `code_only` | `python` | 🧪 Cross-integrate coverage and test reports across envs |
| https://github.com/ansible/ansible-runner/pull/1539 | `ansible/ansible-runner` | `code_only` | `python` | [PR #1538/beefc633 backport][release_2.4] 🧪 Bump `reusable-tox.yml` to `1bb9615` |
| https://github.com/ansible/ansible-runner/pull/1538 | `ansible/ansible-runner` | `code_only` | `python` | 🧪 Bump `reusable-tox.yml` to `1bb9615` |
| https://github.com/ansible/ansible-runner/pull/1536 | `ansible/ansible-runner` | `code_only` | `python` | [PR #1534/30e9542f backport][release_2.4] 🧪 Add nightly jobs to the CI |
| https://github.com/ansible/ansible-runner/pull/1534 | `ansible/ansible-runner` | `code_only` | `python` | 🧪 Add nightly jobs to the CI |
| https://github.com/ansible/ansible-runner/pull/1527 | `ansible/ansible-runner` | `code_and_docs` | `python` | [PR #1523/586586de backport][release_2.4] docs: clarify container volume mounts vs bwrap isolation paths |
| https://github.com/ansible/ansible-runner/pull/1523 | `ansible/ansible-runner` | `code_and_docs` | `python` | docs: clarify container volume mounts vs bwrap isolation paths |
| https://github.com/ansible/ansible-runner/pull/1526 | `ansible/ansible-runner` | `code_only_tests_or_fixtures` | `python` | [ci] Remove core integration tests (#1525) |
| https://github.com/ansible/ansible-runner/pull/1525 | `ansible/ansible-runner` | `code_only_tests_or_fixtures` | `python` | [ci] Remove core integration tests |
| https://github.com/ansible/ansible-runner/pull/1524 | `ansible/ansible-runner` | `code_only` | `python` | [ci]: Fix container usage in tests |
| https://github.com/ansible/ansible-runner/pull/1521 | `ansible/ansible-runner` | `code_only_tests_or_fixtures` | `python` | [PR #1513/7c6e15a3 backport][release_2.4] Fix integration tests for Ansible 2.21+ |
| https://github.com/ansible/ansible-runner/pull/1513 | `ansible/ansible-runner` | `code_only_tests_or_fixtures` | `python` | Fix integration tests for Ansible 2.21+ |
| https://github.com/ansible/ansible-runner/pull/1517 | `ansible/ansible-runner` | `code_only` | `python` | CI test fixes: update Python for test container and add image prune retry |
| https://github.com/ansible/ansible-runner/pull/1514 | `ansible/ansible-runner` | `code_only_tests_or_fixtures` | `python` | Bump Ansible versions for test_core_integration tests |
| https://github.com/ansible/ansible-runner/pull/1511 | `ansible/ansible-runner` | `code_only` | `python` | [CI] Remove CodeCov upload from CI (#1357) |
| https://github.com/ansible/ansible-runner/pull/1510 | `ansible/ansible-runner` | `code_only` | `python` | [CI] Updates to CI framework (#1239) |
| https://github.com/ansible/ansible-runner/pull/1504 | `ansible/ansible-runner` | `code_only` | `python` | Short circuit display wrapper in forks (#1414) |
| https://github.com/ansible/ansible-runner/pull/1499 | `ansible/ansible-runner` | `code_only` | `python` | [PR #1498/57438cb5 backport][release_2.4] Update RTD build image |
| https://github.com/ansible/ansible-runner/pull/1498 | `ansible/ansible-runner` | `code_only` | `python` | Update RTD build image |
| https://github.com/ansible/ansible-runner/pull/1489 | `ansible/ansible-runner` | `code_only` | `python` | [PR #1306/27b75ed8 backport][release_2.4] Fix container --tty detection in subprocess mode |
| https://github.com/ansible/ansible-runner/pull/1306 | `ansible/ansible-runner` | `code_only` | `python` | Fix container --tty detection in subprocess mode |
| https://github.com/ansible/ansible-runner/pull/1488 | `ansible/ansible-runner` | `code_only` | `python` | [PR #1142/37f328cd backport][release_2.4] Use `get_option` api from callback plugins |
| https://github.com/ansible/ansible-runner/pull/1142 | `ansible/ansible-runner` | `code_only` | `python` | Use `get_option` api from callback plugins |
| https://github.com/ansible/ansible-runner/pull/1473 | `ansible/ansible-runner` | `code_and_docs` | `python` | Migrate RTD URLs to docs.ansible.com |
| https://github.com/ansible/ansible-runner/pull/1487 | `ansible/ansible-runner` | `code_only` | `python` | [PR #1430/69227d24 backport][release_2.4] Fix runner GH issue templates |
| https://github.com/ansible/ansible-runner/pull/1430 | `ansible/ansible-runner` | `code_only` | `python` | Fix runner GH issue templates |
| https://github.com/ansible/ansible-runner/pull/1486 | `ansible/ansible-runner` | `code_only_tests_or_fixtures` | `python` | [PR #1485/9e7da046 backport][release_2.4] Fix test_invalid_registry_host() integration test |
| https://github.com/ansible/ansible-runner/pull/1485 | `ansible/ansible-runner` | `code_only_tests_or_fixtures` | `python` | Fix test_invalid_registry_host() integration test |
| https://github.com/ansible/ansible-runner/pull/1469 | `ansible/ansible-runner` | `code_only` | `python` | [PR #1454/877b584d backport][release_2.3] feat: improve eof log messages when streaming |
| https://github.com/ansible/ansible-runner/pull/1454 | `ansible/ansible-runner` | `code_only` | `python` | feat: improve eof log messages when streaming |
| https://github.com/ansible/ansible-runner/pull/1467 | `ansible/ansible-runner` | `code_only` | `python` | Fix release_2.3 CI |
| https://github.com/ansible/ansible-runner/pull/1458 | `ansible/ansible-runner` | `code_only` | `python` | [PR #1454/877b584d backport][release_2.4] feat: improve eof log messages when streaming |
| https://github.com/ansible/ansible-runner/pull/1455 | `ansible/ansible-runner` | `code_only` | `python` | Update for Python 3.14 release |
| https://github.com/ansible/ansible-runner/pull/1457 | `ansible/ansible-runner` | `code_and_docs` | `python` | Remove references to Python < 3.10 |
| https://github.com/ansible/ansible-runner/pull/1456 | `ansible/ansible-runner` | `code_only` | `python` | Migrate setup.cfg to pyproject.toml |
| https://github.com/ansible/ansible-runner/pull/1448 | `ansible/ansible-runner` | `code_only_tests_or_fixtures` | `python` | Install pip in container |
| https://github.com/ansible/ansible-runner/pull/1442 | `ansible/ansible-runner` | `code_only` | `python` | Add non-voting tests against ansible-core devel branch |
| https://github.com/ansible/ansible-runner/pull/1450 | `ansible/ansible-runner` | `code_only_tests_or_fixtures` | `python` | [PR #1449/4c918b0a backport][release_2.4] Fix container build cache issue |
| https://github.com/ansible/ansible-runner/pull/1449 | `ansible/ansible-runner` | `code_only_tests_or_fixtures` | `python` | Fix container build cache issue |
| https://github.com/ansible/ansible-runner/pull/1447 | `ansible/ansible-runner` | `code_only_tests_or_fixtures` | `python` | Update core integration tests for 2.19 release |
| https://github.com/ansible/ansible-runner/pull/1446 | `ansible/ansible-runner` | `code_only` | `python` | Move Python minimum from 3.9 to 3.10 |
| https://github.com/ansible/ansible-runner/pull/1445 | `ansible/ansible-runner` | `code_only_tests_or_fixtures` | `python` | Remove wheel building from CI (#1443) |
| https://github.com/ansible/ansible-runner/pull/1443 | `ansible/ansible-runner` | `code_only` | `python` | Remove wheel building from CI |
| https://github.com/ansible/ansible-runner/pull/1439 | `ansible/ansible-runner` | `code_only` | `python` | Backports 2.4 |
| https://github.com/ansible/ansible-runner/pull/1423 | `ansible/ansible-runner` | `code_only_tests_or_fixtures` | `python` | Remove outdated skipif fixtures |
| https://github.com/ansible/ansible-runner/pull/1436 | `ansible/ansible-runner` | `code_only` | `python` | Add Python 3.14 testing |
| https://github.com/ansible/ansible-runner/pull/1434 | `ansible/ansible-runner` | `code_only` | `python` | Python 3.14 compat: replace codecs.open with open |
| https://github.com/ansible/ansible-runner/pull/1435 | `ansible/ansible-runner` | `code_only_tests_or_fixtures` | `python` | Fix CI for core 2.19.0 |
| https://github.com/ansible/ansible-runner/pull/1425 | `ansible/ansible-runner` | `code_only` | `python` | 🧪 Use `reusable-tox.yml` @ `tox-dev/workflow` |
| https://github.com/ansible/ansible-runner/pull/1428 | `ansible/ansible-runner` | `code_only` | `python` | [PR #1425/827f5f65 backport][release_2.4] 🧪 Use `reusable-tox.yml` @ `tox-dev/workflow` |
| https://github.com/ansible/ansible-runner/pull/1052 | `ansible/ansible-runner` | `code_only` | `python` | [release_2.2] Stringify all env vars, not just those from file (#1039) |
| https://github.com/ansible/ansible-runner/pull/1414 | `ansible/ansible-runner` | `code_only` | `python` | Short circuit in forks |
| https://github.com/ansible/ansible-runner/pull/1421 | `ansible/ansible-runner` | `code_and_docs` | `python` | Backport catchup for 2.4 release |
| https://github.com/ansible/ansible-runner/pull/1408 | `ansible/ansible-runner` | `code_only` | `python` | Modify volume mount behavior when source does not exist |
| https://github.com/ansible/ansible-runner/pull/1401 | `ansible/ansible-runner` | `code_only_tests_or_fixtures` | `python` | Bump integration tests for ansible-core 2.18 release |
| https://github.com/ansible/ansible-runner/pull/1394 | `ansible/ansible-runner` | `code_and_docs` | `python` | Upgrade documentation requirements |
| https://github.com/callstack/agent-device/pull/2193 | `callstack/agent-device` | `code_only` | `typescript` | refactor(cli): move process-exit lifecycle to CLI boundary |
| https://github.com/callstack/agent-device/pull/2194 | `callstack/agent-device` | `code_only` | `typescript` | refactor(cli): move update-check policy |
| https://github.com/callstack/agent-device/pull/2187 | `callstack/agent-device` | `code_only_tests_or_fixtures` | `typescript` | test(kernel): move source-value coverage beside kernel owner |
| https://github.com/callstack/agent-device/pull/2185 | `callstack/agent-device` | `code_only` | `typescript` | refactor(app-log): move policy into daemon ownership |
| https://github.com/callstack/agent-device/pull/2186 | `callstack/agent-device` | `code_only` | `typescript` | refactor(recording): move video validation policy |
| https://github.com/callstack/agent-device/pull/2183 | `callstack/agent-device` | `code_only` | `typescript` | refactor: extract daemon session lifecycle inventory facade |
| https://github.com/callstack/agent-device/pull/2184 | `callstack/agent-device` | `code_only` | `typescript` | refactor(snapshot): move Android helper presentation |
| https://github.com/callstack/agent-device/pull/2180 | `callstack/agent-device` | `code_only` | `typescript` | refactor(host-kit): move verified-file ownership |
| https://github.com/callstack/agent-device/pull/2181 | `callstack/agent-device` | `code_only` | `typescript` | refactor(snapshot): move snapshot policy utilities (#2135) |
| https://github.com/callstack/agent-device/pull/2179 | `callstack/agent-device` | `code_only` | `typescript` | refactor(recording): move Swift cache policy to recording ownership |
| https://github.com/callstack/agent-device/pull/2171 | `callstack/agent-device` | `code_only` | `typescript` | fix(daemon): compose stale-claim recovery from the dead owner's state dir |
| https://github.com/callstack/agent-device/pull/2172 | `callstack/agent-device` | `code_only` | `typescript` | fix(apple): switch to manual code signing when a provisioning profile is set |
| https://github.com/callstack/agent-device/pull/2165 | `callstack/agent-device` | `code_and_docs` | `typescript` | docs+ux: make device ownership discoverable end to end |
| https://github.com/callstack/agent-device/pull/2160 | `callstack/agent-device` | `code_only` | `typescript` | feat(apple): reclaim retained runners under device-claim authority |
| https://github.com/callstack/agent-device/pull/2162 | `callstack/agent-device` | `code_and_docs` | `typescript` | feat: add stale device claim release and dead-end recovery guidance |
| https://github.com/callstack/agent-device/pull/2164 | `callstack/agent-device` | `code_only` | `typescript` | fix: keep named sessions visible in scoped inventory |
| https://github.com/callstack/agent-device/pull/2156 | `callstack/agent-device` | `code_only` | `typescript` | fix: reuse canonical Maestro visibility context |
| https://github.com/callstack/agent-device/pull/2155 | `callstack/agent-device` | `code_only` | `typescript` | fix(maestro): measure settle outcomes directly |
| https://github.com/callstack/agent-device/pull/2167 | `callstack/agent-device` | `code_and_docs` | `typescript` | fix: improve ref-based interaction recovery |
| https://github.com/callstack/agent-device/pull/2110 | `callstack/agent-device` | `code_only` | `typescript` | feat: open Limrun uploaded apps |
| https://github.com/callstack/agent-device/pull/2157 | `callstack/agent-device` | `code_and_docs` | `typescript` | feat: add symbol-aware depgraph authority overlay |
| https://github.com/callstack/agent-device/pull/2151 | `callstack/agent-device` | `code_and_docs` | `typescript` | refactor: dissolve caller-side src/replay into command and CLI owners |
| https://github.com/callstack/agent-device/pull/2122 | `callstack/agent-device` | `code_only` | `typescript` | fix: use canonical viewport fallback for rootless touch targeting |
| https://github.com/callstack/agent-device/pull/2152 | `callstack/agent-device` | `code_only` | `typescript` | refactor(snapshot): move text-surface into snapshot presentation |
| https://github.com/callstack/agent-device/pull/2150 | `callstack/agent-device` | `code_only` | `typescript` | refactor(layering): centralize architecture ownership |
| https://github.com/callstack/agent-device/pull/2137 | `callstack/agent-device` | `code_only_tests_or_fixtures` | `typescript` | test: characterize replay application behavior and coordinator ownership |
| https://github.com/callstack/agent-device/pull/2125 | `callstack/agent-device` | `code_and_docs` | `typescript` | refactor: contract Apple platform surface |
| https://github.com/callstack/agent-device/pull/2119 | `callstack/agent-device` | `code_and_docs` | `typescript` | refactor: retire platforms source seam |
| https://github.com/callstack/agent-device/pull/2123 | `callstack/agent-device` | `code_and_docs` | `typescript` | refactor: prune platform split residue |
| https://github.com/callstack/agent-device/pull/2078 | `callstack/agent-device` | `code_and_docs` | `typescript` | feat: add human takeover controls |
| https://github.com/callstack/agent-device/pull/2111 | `callstack/agent-device` | `code_only` | `typescript` | fix(daemon): confine remote HTTP trust boundaries |
| https://github.com/callstack/agent-device/pull/2109 | `callstack/agent-device` | `code_only` | `typescript` | fix(daemon): enforce provider session artifact ownership |
| https://github.com/callstack/agent-device/pull/2104 | `callstack/agent-device` | `code_and_docs` | `typescript` | fix(daemon): fail closed when the auth hook is silent about tenant |
| https://github.com/callstack/agent-device/pull/2059 | `callstack/agent-device` | `code_only` | `typescript` | ci(1874): declare the diagnose lane and stop it misreading its own loop |
| https://github.com/callstack/agent-device/pull/2105 | `callstack/agent-device` | `code_only` | `typescript` | fix(daemon): let a retried open supersede the claim its aborted attempt abandoned |
| https://github.com/callstack/agent-device/pull/2106 | `callstack/agent-device` | `code_and_docs` | `typescript` | refactor: sink package-closed src modules into existing packages |
| https://github.com/callstack/agent-device/pull/2113 | `callstack/agent-device` | `code_only` | `typescript` | fix(wait): surface runner restart timeout evidence |
| https://github.com/callstack/agent-device/pull/2090 | `callstack/agent-device` | `code_only` | `typescript` | refactor(platforms): break the four upward edges out of src/platforms |
| https://github.com/callstack/agent-device/pull/2107 | `callstack/agent-device` | `code_only` | `typescript` | fix(daemon): dispose late durable capture authorities |
| https://github.com/callstack/agent-device/pull/2100 | `callstack/agent-device` | `code_and_docs` | `typescript` | refactor(platforms): sink the shared src/platforms root files into their substrate homes |
| https://github.com/callstack/agent-device/pull/2102 | `callstack/agent-device` | `code_only` | `typescript` | fix(daemon): refuse host path install sources on the HTTP surface |
| https://github.com/callstack/agent-device/pull/2094 | `callstack/agent-device` | `code_and_docs` | `typescript` | refactor: delete capabilities projection shell |
| https://github.com/callstack/agent-device/pull/2083 | `callstack/agent-device` | `code_only` | `typescript` | fix(test): settle the daemon's exit on its own deadline in the web shutdown lane |
| https://github.com/callstack/agent-device/pull/2091 | `callstack/agent-device` | `code_only` | `typescript` | fix(ci): stop ten artifact uploads discarding their hidden paths |
| https://github.com/callstack/agent-device/pull/2092 | `callstack/agent-device` | `code_only` | `typescript` | refactor(layering): remove retired migration scaffolding |
| https://github.com/callstack/agent-device/pull/2093 | `callstack/agent-device` | `code_only_tests_or_fixtures` | `typescript` | refactor(test): derive provider gateway facts from runtime builder |
| https://github.com/callstack/agent-device/pull/2089 | `callstack/agent-device` | `code_only` | `typescript` | refactor: remove retired capability matrix |
| https://github.com/callstack/agent-device/pull/2084 | `callstack/agent-device` | `code_only_tests_or_fixtures` | `typescript` | test: derive unavailable runtime fixtures |
| https://github.com/callstack/agent-device/pull/2081 | `callstack/agent-device` | `code_and_docs` | `typescript` | refactor: retire ADR-0019 cutover scaffolding |
| https://github.com/callstack/agent-device/pull/2074 | `callstack/agent-device` | `code_and_docs` | `typescript` | refactor(commands): one audience table for common input fields |
| https://github.com/callstack/agent-device/pull/2079 | `callstack/agent-device` | `code_only` | `typescript` | ci: run coverage in one job again |
| https://github.com/callstack/agent-device/pull/2072 | `callstack/agent-device` | `code_only` | `typescript` | refactor: close the daemon platform boundary |
| https://github.com/callstack/agent-device/pull/2070 | `callstack/agent-device` | `code_and_docs` | `typescript` | refactor: move platform provider composition out of daemon |
| https://github.com/callstack/agent-device/pull/2071 | `callstack/agent-device` | `code_only` | `typescript` | refactor: move Android system observation out of daemon |
| https://github.com/callstack/agent-device/pull/2067 | `callstack/agent-device` | `code_only` | `typescript` | docs(batch): name the step shape and the accepted commands in `help batch` and in its refusals |
| https://github.com/callstack/agent-device/pull/2076 | `callstack/agent-device` | `code_only` | `typescript` | fix(mcp): admit a batch step's input against the nested command's own schema |
| https://github.com/callstack/agent-device/pull/2077 | `callstack/agent-device` | `code_only` | `typescript` | fix(build): silence TS2883 dts noise in the Apple runner client shim |
| https://github.com/callstack/agent-device/pull/2065 | `callstack/agent-device` | `code_only` | `typescript` | fix(cli): name `--udid` when a device identity is passed to `--device` |
| https://github.com/callstack/agent-device/pull/2068 | `callstack/agent-device` | `code_only` | `typescript` | fix(daemon): address cwd-scoped sessions by their store key, not their public name |
| https://github.com/callstack/agent-device/pull/2066 | `callstack/agent-device` | `code_only` | `typescript` | feat(interaction): accept `fill <target> ""` as the clear-field primitive |
| https://github.com/hynek/structlog/pull/836 | `hynek/structlog` | `code_only` | `python` | [pre-commit.ci] pre-commit autoupdate |
| https://github.com/hynek/structlog/pull/821 | `hynek/structlog` | `code_only` | `python` | Avoid kwargs unpacking in _process_event hot path |
| https://github.com/hynek/structlog/pull/834 | `hynek/structlog` | `code_only` | `python` | Add codspeed benchmarks |
| https://github.com/hynek/structlog/pull/833 | `hynek/structlog` | `code_and_docs` | `python` | update |
| https://github.com/hynek/structlog/pull/831 | `hynek/structlog` | `code_only` | `python` | Enforce 100% type coverage in CI with Pyrefly |
| https://github.com/hynek/structlog/pull/828 | `hynek/structlog` | `code_only` | `python` | 100% type coverage |
| https://github.com/hynek/structlog/pull/830 | `hynek/structlog` | `code_only` | `python` | update actions |
| https://github.com/hynek/structlog/pull/825 | `hynek/structlog` | `code_only` | `python` | Explicit attribute type annotations |
| https://github.com/hynek/structlog/pull/824 | `hynek/structlog` | `code_only` | `python` | [pre-commit.ci] pre-commit autoupdate |
| https://github.com/hynek/structlog/pull/822 | `hynek/structlog` | `code_only` | `python` | build(deps): bump the github-actions group with 3 updates |
| https://github.com/hynek/structlog/pull/820 | `hynek/structlog` | `code_only` | `python` | [pre-commit.ci] pre-commit autoupdate |
| https://github.com/hynek/structlog/pull/818 | `hynek/structlog` | `code_and_docs` | `python` | stdlib: Add snake_case shims for isEnabledFor & getEffectiveLevel |
| https://github.com/hynek/structlog/pull/812 | `hynek/structlog` | `code_and_docs` | `python` | Add CallsiteParameter.QUAL_MODULE |
| https://github.com/hynek/structlog/pull/814 | `hynek/structlog` | `code_only` | `python` | update dev |
| https://github.com/hynek/structlog/pull/813 | `hynek/structlog` | `code_and_docs` | `python` | Add 3.15 to CI |
| https://github.com/hynek/structlog/pull/805 | `hynek/structlog` | `code_and_docs` | `python` | Fix thread name CallsiteParameterAdder in async methods (issue #710) |
| https://github.com/hynek/structlog/pull/811 | `hynek/structlog` | `code_and_docs` | `python` | Correctly unpickle WriteLogger |
| https://github.com/hynek/structlog/pull/786 | `hynek/structlog` | `code_and_docs` | `python` | Add name attribute to BytesLogger |
| https://github.com/hynek/structlog/pull/794 | `hynek/structlog` | `code_and_docs` | `python` | Monochrome Rich traceback rendering w/ ConsoleRenderer(colors=False) |
| https://github.com/hynek/structlog/pull/809 | `hynek/structlog` | `code_only` | `python` | [pre-commit.ci] pre-commit autoupdate |
| https://github.com/hynek/structlog/pull/807 | `hynek/structlog` | `code_and_docs` | `python` | Use WeakKeyDictionary for WRITE_LOCKS to prevent file object leaks |
| https://github.com/hynek/structlog/pull/808 | `hynek/structlog` | `code_only` | `python` | build(deps): bump the github-actions group with 4 updates |
| https://github.com/hynek/structlog/pull/803 | `hynek/structlog` | `code_only` | `python` | [pre-commit.ci] pre-commit autoupdate |
| https://github.com/hynek/structlog/pull/802 | `hynek/structlog` | `code_and_docs` | `python` | Deprecate better-exceptions integration |
| https://github.com/hynek/structlog/pull/801 | `hynek/structlog` | `code_only` | `python` | Build docs on 3.14 |
| https://github.com/hynek/structlog/pull/800 | `hynek/structlog` | `code_and_docs` | `python` | Drop 3.9 |
| https://github.com/hynek/structlog/pull/798 | `hynek/structlog` | `code_only` | `python` | ci: make workflows pass Zizmor in pedantic mode |
| https://github.com/hynek/structlog/pull/796 | `hynek/structlog` | `code_only` | `python` | Update dev |
| https://github.com/hynek/structlog/pull/790 | `hynek/structlog` | `code_and_docs` | `python` | dev: don't raise warning on rendered exceptions |
| https://github.com/hynek/structlog/pull/792 | `hynek/structlog` | `code_only` | `python` | [pre-commit.ci] pre-commit autoupdate |
| https://github.com/hynek/structlog/pull/791 | `hynek/structlog` | `code_only` | `python` | build(deps): bump github/codeql-action from 4.32.3 to 4.32.4 in the github-actions group |
| https://github.com/hynek/structlog/pull/784 | `hynek/structlog` | `code_only` | `python` | build(deps): bump the github-actions group with 2 updates |
| https://github.com/hynek/structlog/pull/785 | `hynek/structlog` | `code_only` | `python` | [pre-commit.ci] pre-commit autoupdate |
| https://github.com/hynek/structlog/pull/781 | `hynek/structlog` | `code_only` | `python` | [pre-commit.ci] pre-commit autoupdate |
| https://github.com/hynek/structlog/pull/780 | `hynek/structlog` | `code_only` | `python` | build(deps): bump the github-actions group with 4 updates |
| https://github.com/hynek/structlog/pull/773 | `hynek/structlog` | `code_only` | `python` | build(deps): bump the github-actions group with 2 updates |
| https://github.com/hynek/structlog/pull/774 | `hynek/structlog` | `code_only` | `python` | [pre-commit.ci] pre-commit autoupdate |
| https://github.com/hynek/structlog/pull/770 | `hynek/structlog` | `code_only` | `python` | [pre-commit.ci] pre-commit autoupdate |
| https://github.com/hynek/structlog/pull/768 | `hynek/structlog` | `code_and_docs` | `python` | Drop Python 3.8 |
| https://github.com/hynek/structlog/pull/767 | `hynek/structlog` | `code_only` | `python` | Make tests order-independent |
| https://github.com/hynek/structlog/pull/766 | `hynek/structlog` | `code_only` | `python` | Drop pretend dependency |
| https://github.com/hynek/structlog/pull/763 | `hynek/structlog` | `code_and_docs` | `python` | stdlib: add support for stacklevel |
| https://github.com/hynek/structlog/pull/765 | `hynek/structlog` | `code_only` | `python` | update dev |
| https://github.com/hynek/structlog/pull/761 | `hynek/structlog` | `code_and_docs` | `python` | Add CallsiteParameter.QUAL_NAME |
| https://github.com/hynek/structlog/pull/760 | `hynek/structlog` | `code_only` | `python` | Expand API type-checking |
| https://github.com/hynek/structlog/pull/759 | `hynek/structlog` | `code_and_docs` | `python` | dev: add colors and force_colors properties |
| https://github.com/hynek/structlog/pull/758 | `hynek/structlog` | `code_and_docs` | `python` | Refactor terminal initialization into separate function |
| https://github.com/hynek/structlog/pull/757 | `hynek/structlog` | `code_and_docs` | `python` | dev: allow columns to be got and set |
| https://github.com/hynek/structlog/pull/756 | `hynek/structlog` | `code_and_docs` | `python` | Allow setting sort_keys on current ConsoleRenderer |
| https://github.com/hynek/structlog/pull/749 | `hynek/structlog` | `code_and_docs` | `python` | Improve ConsoleRenderer ergonomics |
| https://github.com/hynek/structlog/pull/755 | `hynek/structlog` | `code_only` | `python` | Update dev deps |
| https://github.com/hynek/structlog/pull/753 | `hynek/structlog` | `code_only` | `python` | [pre-commit.ci] pre-commit autoupdate |
| https://github.com/hynek/structlog/pull/748 | `hynek/structlog` | `code_and_docs` | `python` | Add support for dict-based interpolation in native loggers |
| https://github.com/hynek/structlog/pull/741 | `hynek/structlog` | `code_and_docs` | `python` | refactor: extract styles configuration to separate method |
| https://github.com/hynek/structlog/pull/747 | `hynek/structlog` | `code_and_docs` | `python` | MaybeTimeStamper: Fix custom keys always being overwritten |
| https://github.com/hynek/structlog/pull/739 | `hynek/structlog` | `code_and_docs` | `python` | Fix unbounded recursion when traceback contains an exception that has a reference to itself in its cause chain |
| https://github.com/hynek/structlog/pull/717 | `hynek/structlog` | `code_and_docs` | `python` | feat(rich): expose `code_width` and delegate full width handling to `rich` |
| https://github.com/hynek/structlog/pull/742 | `hynek/structlog` | `code_only` | `python` | [pre-commit.ci] pre-commit autoupdate |
| https://github.com/hynek/structlog/pull/743 | `hynek/structlog` | `code_only` | `python` | Bump actions/checkout from 4 to 5 |
| https://github.com/hynek/structlog/pull/744 | `hynek/structlog` | `code_only` | `python` | Bump actions/download-artifact from 4 to 5 |
| https://github.com/SonarSource/SonarJS/pull/7840 | `sonarsource/sonarjs` | `code_only` | `typescript` | Update dependency jdx/mise to v2026.8.14 |
| https://github.com/SonarSource/SonarJS/pull/7832 | `sonarsource/sonarjs` | `code_only` | `typescript` | JS-2236 Fix S2004 nested-function depth in the analyze-project unary handler |
| https://github.com/SonarSource/SonarJS/pull/7836 | `sonarsource/sonarjs` | `code_only` | `typescript` | Update dependency jdx/mise to v2026.8.11 |
| https://github.com/SonarSource/SonarJS/pull/7837 | `sonarsource/sonarjs` | `code_only` | `typescript` | Update typescript-eslint/typescript-eslint monorepo to v8.68.0 |
| https://github.com/SonarSource/SonarJS/pull/7838 | `sonarsource/sonarjs` | `code_only` | `typescript` | Update jdx/mise-action action to v4.3.0 |
| https://github.com/SonarSource/SonarJS/pull/7839 | `sonarsource/sonarjs` | `code_only` | `typescript` | Update dependency eslint-doc-generator to v3.7.1 |
| https://github.com/SonarSource/SonarJS/pull/7826 | `sonarsource/sonarjs` | `code_only` | `typescript` | JS-2329 Fix test-file heuristic to preserve source metrics |
| https://github.com/SonarSource/SonarJS/pull/7824 | `sonarsource/sonarjs` | `code_only` | `typescript` | JS-2327 Avoid preloading unrelated generated-source config files |
| https://github.com/SonarSource/SonarJS/pull/7823 | `sonarsource/sonarjs` | `code_and_docs` | `typescript` | JS-2326: Queue concurrent analyze-project requests |
| https://github.com/SonarSource/SonarJS/pull/7822 | `sonarsource/sonarjs` | `code_only` | `typescript` | Update dependency @types/bytes to v3.1.6 |
| https://github.com/SonarSource/SonarJS/pull/7821 | `sonarsource/sonarjs` | `code_only` | `typescript` | JS-2322 Limit S9011 scope to raise only inside forms |
| https://github.com/SonarSource/SonarJS/pull/7816 | `sonarsource/sonarjs` | `code_and_docs` | `typescript` | JS-2312 Decorate rule S8951 |
| https://github.com/SonarSource/SonarJS/pull/7809 | `sonarsource/sonarjs` | `code_and_docs` | `typescript` | Update generated README files and RSPEC JSON |
| https://github.com/SonarSource/SonarJS/pull/7819 | `sonarsource/sonarjs` | `code_only` | `typescript` | Update dependency jdx/mise to v2026.8.10 |
| https://github.com/SonarSource/SonarJS/pull/7813 | `sonarsource/sonarjs` | `code_only` | `typescript` | JS-2313 S2187: False positive on Deno.test declarations |
| https://github.com/SonarSource/SonarJS/pull/7802 | `sonarsource/sonarjs` | `code_only` | `typescript` | JS-2298 Don't raise S2486 when the unused catch clause contains only comments |
| https://github.com/SonarSource/SonarJS/pull/7814 | `sonarsource/sonarjs` | `code_only_tests_or_fixtures` | `typescript` | Update ruling results for PR #7813 |
| https://github.com/SonarSource/SonarJS/pull/7811 | `sonarsource/sonarjs` | `code_only` | `typescript` | Update dependency @inquirer/prompts to v8.6.0 |
| https://github.com/SonarSource/SonarJS/pull/7810 | `sonarsource/sonarjs` | `code_only` | `typescript` | Update dependency jdx/mise to v2026.8.9 |
| https://github.com/SonarSource/SonarJS/pull/7736 | `sonarsource/sonarjs` | `code_only` | `typescript` | JS-2233: Implement S9162: use retryable Cypress assertions |
| https://github.com/SonarSource/SonarJS/pull/7799 | `sonarsource/sonarjs` | `code_only` | `typescript` | JS-2288: Suppress S6757 false positives in class members |
| https://github.com/SonarSource/SonarJS/pull/7752 | `sonarsource/sonarjs` | `code_only` | `typescript` | JS-1014: Implement S9339: Native APIs should be preferred over Axios utility methods |
| https://github.com/SonarSource/SonarJS/pull/7808 | `sonarsource/sonarjs` | `code_only` | `typescript` | Update docker/setup-buildx-action action to v4.3.0 |
| https://github.com/SonarSource/SonarJS/pull/7804 | `sonarsource/sonarjs` | `code_only` | `typescript` | JS-2302 Replace platform threads with virtual threads for blocking operations |
| https://github.com/SonarSource/SonarJS/pull/7806 | `sonarsource/sonarjs` | `code_only` | `typescript` | JS-2303 Replace if-else chains with switch expressions in AnalysisProcessor |
| https://github.com/SonarSource/SonarJS/pull/7805 | `sonarsource/sonarjs` | `code_only` | `typescript` | Update dependency jdx/mise to v2026.8.8 |
| https://github.com/SonarSource/SonarJS/pull/7803 | `sonarsource/sonarjs` | `code_only_tests_or_fixtures` | `typescript` | Update ruling results for PR #7802 |
| https://github.com/SonarSource/SonarJS/pull/7784 | `sonarsource/sonarjs` | `code_only` | `typescript` | JS-2280 Fix S7785 false positive for promise chains stored for later consumption |
| https://github.com/SonarSource/SonarJS/pull/7798 | `sonarsource/sonarjs` | `code_only` | `typescript` | JS-2294 Pin RSPEC for branch-11-X builds |
| https://github.com/SonarSource/SonarJS/pull/7797 | `sonarsource/sonarjs` | `code_and_docs` | `typescript` | JS-2293 Integrate Vortex (SonarQube agentic analysis) protocol |
| https://github.com/SonarSource/SonarJS/pull/7793 | `sonarsource/sonarjs` | `code_only` | `typescript` | BUILD-12287 Move Linux GitHub-hosted jobs to WarpBuild |
| https://github.com/SonarSource/SonarJS/pull/7792 | `sonarsource/sonarjs` | `code_only` | `typescript` | BUILD-12288 Move Windows GitHub-hosted jobs to WarpBuild |
| https://github.com/SonarSource/SonarJS/pull/7796 | `sonarsource/sonarjs` | `code_only` | `typescript` | Update dependency jdx/mise to v2026.8.6 |
| https://github.com/SonarSource/SonarJS/pull/7790 | `sonarsource/sonarjs` | `code_and_docs` | `typescript` | JS-2286 Make RSPEC refresh lifecycle ordering explicit |
| https://github.com/SonarSource/SonarJS/pull/7787 | `sonarsource/sonarjs` | `code_only` | `typescript` | JS-2283 Use consistent generated Java provenance |
| https://github.com/SonarSource/SonarJS/pull/7788 | `sonarsource/sonarjs` | `code_only` | `typescript` | JS-2284 Centralize rule key validation |
| https://github.com/SonarSource/SonarJS/pull/7786 | `sonarsource/sonarjs` | `code_only` | `typescript` | JS-2282 Make Java rule generator safe to import |
| https://github.com/SonarSource/SonarJS/pull/7785 | `sonarsource/sonarjs` | `code_and_docs` | `typescript` | JS-2281 Reuse generated README artifacts in nightly refresh |
| https://github.com/SonarSource/SonarJS/pull/7755 | `sonarsource/sonarjs` | `code_only` | `typescript` | JS-2240 S2819: Avoid false positives for Worker message handlers |
| https://github.com/SonarSource/SonarJS/pull/7777 | `sonarsource/sonarjs` | `code_and_docs` | `typescript` | JS-2211 Load quality profiles from rule metadata |
| https://github.com/SonarSource/SonarJS/pull/7779 | `sonarsource/sonarjs` | `code_only_tests_or_fixtures` | `typescript` | JS-2276 Remove unnecessary String.raw usage in quickfixes test helper |
| https://github.com/SonarSource/SonarJS/pull/7778 | `sonarsource/sonarjs` | `code_and_docs` | `typescript` | JS-2277 Update generated README files and RSPEC JSON |
| https://github.com/SonarSource/SonarJS/pull/7763 | `sonarsource/sonarjs` | `code_and_docs` | `typescript` | JS-2211 Generate per-language quality profiles at build time |
| https://github.com/SonarSource/SonarJS/pull/7771 | `sonarsource/sonarjs` | `code_only` | `typescript` | Narrow css:S4662 to plain CSS |
| https://github.com/SonarSource/SonarJS/pull/7775 | `sonarsource/sonarjs` | `code_only` | `typescript` | Override inherited npm registry for Renovate |
| https://github.com/SonarSource/SonarJS/pull/7660 | `sonarsource/sonarjs` | `code_only` | `typescript` | Update dependency knip to v6.32.2 |
| https://github.com/SonarSource/SonarJS/pull/7715 | `sonarsource/sonarjs` | `code_only` | `typescript` | Update stylelint HTML dependencies to v2 |
| https://github.com/SonarSource/SonarJS/pull/7692 | `sonarsource/sonarjs` | `code_only` | `typescript` | Update SonarSource/sonar-analyzer-commons monorepo |
| https://github.com/SonarSource/SonarJS/pull/7774 | `sonarsource/sonarjs` | `code_only` | `typescript` | Update jdx/mise-action action to v4.2.5 |
| https://github.com/SonarSource/SonarJS/pull/7686 | `sonarsource/sonarjs` | `code_only` | `typescript` | Update dependency jdx/mise to v2026.8.5 |
| https://github.com/SonarSource/SonarJS/pull/7682 | `sonarsource/sonarjs` | `code_only` | `typescript` | Update jdx/mise-action action to v4.2.4 |
| https://github.com/SonarSource/SonarJS/pull/7716 | `sonarsource/sonarjs` | `code_only` | `typescript` | Update dependency @types/semver to v7.8.0 |
| https://github.com/SonarSource/SonarJS/pull/7681 | `sonarsource/sonarjs` | `code_only` | `typescript` | Update docker/login-action action to v4.6.0 |
| https://github.com/SonarSource/SonarJS/pull/7680 | `sonarsource/sonarjs` | `code_only` | `typescript` | Update dependency postcss to v8.5.26 |
| https://github.com/SonarSource/SonarJS/pull/7729 | `sonarsource/sonarjs` | `code_only` | `typescript` | Update typescript-eslint/typescript-eslint monorepo to v8.67.0 |
| https://github.com/SonarSource/SonarJS/pull/7766 | `sonarsource/sonarjs` | `code_only` | `typescript` | Update dependency tsx to v4.23.12 |
| https://github.com/SonarSource/SonarJS/pull/7768 | `sonarsource/sonarjs` | `code_only` | `typescript` | Update dependency memfs to v4.68.1 |
| https://github.com/SonarSource/SonarJS/pull/7767 | `sonarsource/sonarjs` | `code_only` | `typescript` | Update dependency globals to v17.11.0 |
| https://github.com/SonarSource/SonarJS/pull/7770 | `sonarsource/sonarjs` | `code_only` | `typescript` | JS-2261 Skip project analysis when all files are cached |
| https://github.com/SonarSource/SonarJS/pull/7772 | `sonarsource/sonarjs` | `code_only` | `typescript` | JS-2260 Avoid error logs for recoverable parsing failures |
| https://github.com/vllm-project/tpu-inference/pull/3422 | `vllm-project/tpu-inference` | `code_only` | `python` | Enable Prefix Caching for Hybrid Linear-Attention (GDN) Models with DP Support |
| https://github.com/vllm-project/tpu-inference/pull/2064 | `vllm-project/tpu-inference` | `code_and_docs` | `python` | Reorganization of ToC and docs linting |
| https://github.com/vllm-project/tpu-inference/pull/3459 | `vllm-project/tpu-inference` | `code_only` | `python` | [PCP] Remove unnecessary copy op before cache phase |
| https://github.com/vllm-project/tpu-inference/pull/3461 | `vllm-project/tpu-inference` | `code_only` | `python` | feat: RLVllmSampler weight sync via Raiden |
| https://github.com/vllm-project/tpu-inference/pull/3463 | `vllm-project/tpu-inference` | `code_only` | `python` | Bypass continue decode when structured output requests are present |
| https://github.com/vllm-project/tpu-inference/pull/3437 | `vllm-project/tpu-inference` | `code_only` | `python` | Fix compatibility with upstream vLLM AutoWeightsLoader and tied embeddings |
| https://github.com/vllm-project/tpu-inference/pull/3472 | `vllm-project/tpu-inference` | `code_and_docs` | `python` | bench: dual write benchmark results to BigQuery |
| https://github.com/vllm-project/tpu-inference/pull/3465 | `vllm-project/tpu-inference` | `code_only` | `python` | bench: port the bm-infra v6e sonnet workloads to daily Buildkite cases |
| https://github.com/vllm-project/tpu-inference/pull/3411 | `vllm-project/tpu-inference` | `code_only` | `python` | Re-land: bit-pack GDN v3 per-p_id metadata |
| https://github.com/vllm-project/tpu-inference/pull/3054 | `vllm-project/tpu-inference` | `code_only` | `python` | Remove explicit PAT from pipeline now that we have Github App |
| https://github.com/vllm-project/tpu-inference/pull/3450 | `vllm-project/tpu-inference` | `code_only` | `python` | [Bugfix] Compile the Qwen2.5-VL vision tower on the torchax path (mm-encoder JIT padding + ViT pad-segment fixes) |
| https://github.com/vllm-project/tpu-inference/pull/3446 | `vllm-project/tpu-inference` | `code_only` | `python` | [CI] Mark Qwen2.5-VL-7B benchmarks as unverified on the vllm (torchax) nightly variant |
| https://github.com/vllm-project/tpu-inference/pull/3448 | `vllm-project/tpu-inference` | `code_only` | `python` | [CI] Auto-retry DCN P/D disagg steps once on transient TPU session init failure |
| https://github.com/vllm-project/tpu-inference/pull/3433 | `vllm-project/tpu-inference` | `code_only` | `python` | Add warning comment to model loader log |
| https://github.com/vllm-project/tpu-inference/pull/3438 | `vllm-project/tpu-inference` | `code_only` | `python` | [CI] Gate record_verified_commit_hashes step to MODEL_IMPL_TYPE=auto |
| https://github.com/vllm-project/tpu-inference/pull/3451 | `vllm-project/tpu-inference` | `code_only` | `python` | [releases/v0.28.0] Cherry-pick #3446: mark Qwen2.5-VL-7B benchmarks unverified on the vllm (torchax) nightly variant |
| https://github.com/vllm-project/tpu-inference/pull/3242 | `vllm-project/tpu-inference` | `code_only` | `python` | [tpu-inference] Add block-diffusion strategy configuration |
| https://github.com/vllm-project/tpu-inference/pull/3435 | `vllm-project/tpu-inference` | `code_only` | `python` | [Fix] Reduce shared-expert output over in-group TP under attention DP |
| https://github.com/vllm-project/tpu-inference/pull/3406 | `vllm-project/tpu-inference` | `code_only` | `python` | [gemma4] Fix torchax-path E2B/E4B accuracy: inline PLE + skip KV-cache writes for KV-shared layers |
| https://github.com/vllm-project/tpu-inference/pull/3426 | `vllm-project/tpu-inference` | `code_only` | `python` | [DeepSeek-V4] Fix NaN errors in mla_swa unnormalized output buffers |
| https://github.com/vllm-project/tpu-inference/pull/3375 | `vllm-project/tpu-inference` | `code_only` | `python` | Update gmm v2 reference to Tokamax's version. |
| https://github.com/vllm-project/tpu-inference/pull/3431 | `vllm-project/tpu-inference` | `code_only` | `python` | [CI] Remove obsolete transformers>=5.5.0 gate from gemma-4 26B/31B unit tests |
| https://github.com/vllm-project/tpu-inference/pull/3388 | `vllm-project/tpu-inference` | `code_only` | `python` | Fused MoE Kernel integration and optimization |
| https://github.com/vllm-project/tpu-inference/pull/3428 | `vllm-project/tpu-inference` | `code_only` | `python` | [DSv4] Accept backend_cls in VllmDeepseekV4SWACache for vLLM #47808 |
| https://github.com/vllm-project/tpu-inference/pull/3423 | `vllm-project/tpu-inference` | `code_only` | `python` | [Fix] Scope jax.set_mesh context to get_flax_model |
| https://github.com/vllm-project/tpu-inference/pull/3408 | `vllm-project/tpu-inference` | `code_only` | `python` | [gemma4] Make 26B/31B benchmarks pass on the torchax path (HBM headroom, startup timeout, variant bars) |
| https://github.com/vllm-project/tpu-inference/pull/3397 | `vllm-project/tpu-inference` | `code_only` | `python` | [Spec Decode] Guard draft tokens and slice assignments against shape broadcast mismatch |
| https://github.com/vllm-project/tpu-inference/pull/3418 | `vllm-project/tpu-inference` | `code_only` | `python` | [DPScheduler] Add missing ec_connector attribute to DPScheduler |
| https://github.com/vllm-project/tpu-inference/pull/3414 | `vllm-project/tpu-inference` | `code_only` | `python` | [CI] Mark gemma-4 E2B/E4B accuracy as unverified on the vllm (torchax) nightly variant |
| https://github.com/vllm-project/tpu-inference/pull/3407 | `vllm-project/tpu-inference` | `code_only` | `python` | [multimodal] Raise ViT flash-attention scoped-vmem limit to 64MiB |
| https://github.com/vllm-project/tpu-inference/pull/3409 | `vllm-project/tpu-inference` | `code_only` | `python` | [DSv4] Pass attention metadata to jit once per KV-cache group |
| https://github.com/vllm-project/tpu-inference/pull/3257 | `vllm-project/tpu-inference` | `code_only` | `python` | [RL] VllmSampler rollout class |
| https://github.com/vllm-project/tpu-inference/pull/3277 | `vllm-project/tpu-inference` | `code_only` | `python` | PCP + ring attention |
| https://github.com/vllm-project/tpu-inference/pull/3398 | `vllm-project/tpu-inference` | `code_only_tests_or_fixtures` | `python` | [SpecDecode] Remove _disable_shardy_for_qwen35_4b workaround in speculative decoding tests |
| https://github.com/vllm-project/tpu-inference/pull/3362 | `vllm-project/tpu-inference` | `code_only` | `python` | Make pause/resume work on TPU |
| https://github.com/vllm-project/tpu-inference/pull/3404 | `vllm-project/tpu-inference` | `code_only` | `python` | [CI] Mark DFlash as unverified on the vllm (torchax) nightly variant |
| https://github.com/vllm-project/tpu-inference/pull/3402 | `vllm-project/tpu-inference` | `code_only` | `python` | Disable mm_device_do_normalize for JAX-native multimodal models |
| https://github.com/vllm-project/tpu-inference/pull/3403 | `vllm-project/tpu-inference` | `code_only` | `python` | [Fix Test Failure] Make the TP performance threshold platform-aware. |
| https://github.com/vllm-project/tpu-inference/pull/3405 | `vllm-project/tpu-inference` | `code_only` | `python` | Revert "Bit-pack GDN v3 per-p_id metadata to reduce SMEM (#3349)" |
| https://github.com/vllm-project/tpu-inference/pull/3040 | `vllm-project/tpu-inference` | `code_and_docs` | `python` | [kernels][fused_moe] Add another fused EP MoE kernels |
| https://github.com/vllm-project/tpu-inference/pull/3392 | `vllm-project/tpu-inference` | `code_only` | `python` | [DSv4] Port mhc kernels from g3 to tpu-inference  |
| https://github.com/vllm-project/tpu-inference/pull/3391 | `vllm-project/tpu-inference` | `code_only` | `python` | [DSv4] add safe guard to avoid cache being mistakenly copied |
| https://github.com/vllm-project/tpu-inference/pull/3389 | `vllm-project/tpu-inference` | `code_only` | `python` | Honour --group-size when replaying a trace, and read traces from GCS |
| https://github.com/vllm-project/tpu-inference/pull/3383 | `vllm-project/tpu-inference` | `code_only` | `python` | Replay tool-call idle time in the agentic benchmark |
| https://github.com/vllm-project/tpu-inference/pull/3376 | `vllm-project/tpu-inference` | `code_only` | `python` | Separate q,k,v projection in sliding attention layers |
| https://github.com/vllm-project/tpu-inference/pull/3374 | `vllm-project/tpu-inference` | `code_only` | `python` | Fix continue_decode on the flax_nnx path and stop dropping compile options |
| https://github.com/vllm-project/tpu-inference/pull/3341 | `vllm-project/tpu-inference` | `code_only` | `python` | [Multimodal] Update tuned block sizes for flash attention kernel |
| https://github.com/vllm-project/tpu-inference/pull/3290 | `vllm-project/tpu-inference` | `code_and_docs` | `python` | Add Batched RPA Kernel Decode Tuning/Gmm_v2 Kernel Tuner, Update Tuning Infra to Support Error Recovery/Resume |
| https://github.com/vllm-project/tpu-inference/pull/3349 | `vllm-project/tpu-inference` | `code_only` | `python` | Bit-pack GDN v3 per-p_id metadata to reduce SMEM |
| https://github.com/vllm-project/tpu-inference/pull/3365 | `vllm-project/tpu-inference` | `code_and_docs` | `python` | Replay recorded rollout traces in the agentic benchmark |
| https://github.com/vllm-project/tpu-inference/pull/3361 | `vllm-project/tpu-inference` | `code_only` | `python` | [stacked_rpa] Stop over-fetching KV in decode |
| https://github.com/vllm-project/tpu-inference/pull/3366 | `vllm-project/tpu-inference` | `code_only` | `python` | [DSv4] avoid params being copied in fwd pass |
| https://github.com/vllm-project/tpu-inference/pull/3372 | `vllm-project/tpu-inference` | `code_only` | `python` | Advance vLLM LKG to 70b84f0bcb; support transformers 5.15 per-layer Gemma4 configs |
| https://github.com/vllm-project/tpu-inference/pull/3358 | `vllm-project/tpu-inference` | `code_only` | `python` | Advance vLLM LKG to 83ad767eed (latest) with hybrid prefix-caching and MLA compat fixes |
| https://github.com/vllm-project/tpu-inference/pull/3347 | `vllm-project/tpu-inference` | `code_only` | `python` | [Fix] Restrict generation-config downloads for bm-infra |
| https://github.com/vllm-project/tpu-inference/pull/3364 | `vllm-project/tpu-inference` | `code_only` | `python` | fix the daily benchmark timeout issues |
| https://github.com/vllm-project/tpu-inference/pull/3359 | `vllm-project/tpu-inference` | `code_only` | `python` | [DSv4] Add a fused reverse-rope-quant-wo-a kernel |
| https://github.com/vllm-project/tpu-inference/pull/3357 | `vllm-project/tpu-inference` | `code_only` | `python` | Advance vLLM LKG to f5bb701fa (2026-08-03) |
| https://github.com/vllm-project/tpu-inference/pull/3104 | `vllm-project/tpu-inference` | `code_only` | `python` | Thread the attention soft cap through the vLLM attention wrappers |
| https://github.com/vllm-project/tpu-inference/pull/3259 | `vllm-project/tpu-inference` | `code_only` | `python` | compressed tensor nvfp4 support improvement |
| https://github.com/juspay/xyne-spaces/pull/942 | `juspay/xyne-spaces` | `code_only` | `typescript` | feat: XYNE-54938 local CLI harness replayed onto main with prod-readiness hardening |
| https://github.com/juspay/xyne-spaces/pull/994 | `juspay/xyne-spaces` | `code_only` | `typescript` | fix: prevent duplicate agent progress indicator rendering |
| https://github.com/juspay/xyne-spaces/pull/1269 | `juspay/xyne-spaces` | `code_only` | `typescript` | feat: XYNE-55834 read from replica and write to master |
| https://github.com/juspay/xyne-spaces/pull/1268 | `juspay/xyne-spaces` | `code_only` | `typescript` | fix: XYNE-61350 Generate Label action for older recording distinguish based on channel id |
| https://github.com/juspay/xyne-spaces/pull/1261 | `juspay/xyne-spaces` | `code_only` | `typescript` | fix: XYNE-61336 ticket link routing to include channel context |
| https://github.com/juspay/xyne-spaces/pull/1154 | `juspay/xyne-spaces` | `code_only` | `typescript` | fix: XYNE-61353 internal call routing |
| https://github.com/juspay/xyne-spaces/pull/1281 | `juspay/xyne-spaces` | `code_only` | `typescript` | fix: File acl changed for onyx benchmarking |
| https://github.com/juspay/xyne-spaces/pull/1278 | `juspay/xyne-spaces` | `code_only` | `typescript` | fix: XYNE-55716 keep the daily-brief regenerate SSE stream alive |
| https://github.com/juspay/xyne-spaces/pull/1243 | `juspay/xyne-spaces` | `code_only` | `typescript` | fix: XYNE-55716 keep the daily-brief regenerate SSE stream alive |
| https://github.com/juspay/xyne-spaces/pull/1275 | `juspay/xyne-spaces` | `code_only` | `typescript` | fix: XYNE-61381 summary generation fixes |
| https://github.com/juspay/xyne-spaces/pull/1274 | `juspay/xyne-spaces` | `code_only` | `typescript` | fix: XYNE-54658 add chat with agent button in draft agent card |
| https://github.com/juspay/xyne-spaces/pull/1277 | `juspay/xyne-spaces` | `code_and_docs` | `typescript` | fix: XYNE-61187 one app per conversation, not one per generation |
| https://github.com/juspay/xyne-spaces/pull/992 | `juspay/xyne-spaces` | `code_only` | `typescript` | fix: XYNE-56934 use shared date picker for status expiry |
| https://github.com/juspay/xyne-spaces/pull/1276 | `juspay/xyne-spaces` | `code_and_docs` | `typescript` | fix: XYNE-61187 one app per conversation (claw services) |
| https://github.com/juspay/xyne-spaces/pull/1236 | `juspay/xyne-spaces` | `code_only` | `typescript` | feat: XYNE-60735 multi-repo SDLC hubs |
| https://github.com/juspay/xyne-spaces/pull/1245 | `juspay/xyne-spaces` | `code_and_docs` | `typescript` | fix: XYNE-61187 one app per conversation, not one per generation |
| https://github.com/juspay/xyne-spaces/pull/1266 | `juspay/xyne-spaces` | `code_only` | `typescript` | fix: XYNE-61335 revert ordered encryption key rotation (#764) |
| https://github.com/juspay/xyne-spaces/pull/1270 | `juspay/xyne-spaces` | `code_only` | `typescript` | fix: File acl changed for onyx benchmarking |
| https://github.com/juspay/xyne-spaces/pull/1254 | `juspay/xyne-spaces` | `code_only` | `typescript` | fix: XYNE-61320 Allow call participants to admit or decline join requests |
| https://github.com/juspay/xyne-spaces/pull/724 | `juspay/xyne-spaces` | `code_only` | `typescript` | feat: XYNE-56496 add "adding existing ticket as subticket in parent ticket" |
| https://github.com/juspay/xyne-spaces/pull/1145 | `juspay/xyne-spaces` | `code_only` | `typescript` | fix: XYNE-60278 related ticket not coming in desk |
| https://github.com/juspay/xyne-spaces/pull/886 | `juspay/xyne-spaces` | `code_only` | `typescript` | fix: XYNE-54658 add artifacts for agent discovery, mcp suggest |
| https://github.com/juspay/xyne-spaces/pull/1207 | `juspay/xyne-spaces` | `code_only` | `typescript` | fix: XYNE-55539 add in-app browser header indicator for preference education, remove existing toast implementation |
| https://github.com/juspay/xyne-spaces/pull/1249 | `juspay/xyne-spaces` | `code_only` | `typescript` | fix: XYNE-12323 only user key provisioning is gated behind env |
| https://github.com/juspay/xyne-spaces/pull/1101 | `juspay/xyne-spaces` | `code_only` | `typescript` | fix: XYNE-55539 UI feedback |
| https://github.com/juspay/xyne-spaces/pull/1232 | `juspay/xyne-spaces` | `code_only` | `typescript` | feat: XYNE-60825 add PPTX viewer and search-text extraction |
| https://github.com/juspay/xyne-spaces/pull/1191 | `juspay/xyne-spaces` | `code_only` | `typescript` | fix: XYNE-56627 fix empty-result loader flash on cached cmd+K search |
| https://github.com/juspay/xyne-spaces/pull/1244 | `juspay/xyne-spaces` | `code_only` | `typescript` | fix: XYNE-54658 suggest connectors only when actually missing (claw only) |
| https://github.com/juspay/xyne-spaces/pull/1251 | `juspay/xyne-spaces` | `code_only` | `typescript` | fix: XYNE-1315 pass threadMentions as a rank-only term for messages |
| https://github.com/juspay/xyne-spaces/pull/1227 | `juspay/xyne-spaces` | `code_only` | `typescript` | fix: XYNE-60903 canvas notes numbered list and recording summary colors |
| https://github.com/juspay/xyne-spaces/pull/1200 | `juspay/xyne-spaces` | `code_only` | `typescript` | feat: show last updated date in Claw v3 skills |
| https://github.com/juspay/xyne-spaces/pull/1239 | `juspay/xyne-spaces` | `code_only` | `typescript` | fix: XYNE-60846 retry resumed runs before failure |
| https://github.com/juspay/xyne-spaces/pull/1093 | `juspay/xyne-spaces` | `code_only` | `typescript` | Feature/added reassign from usergroup release (#1065) |
| https://github.com/juspay/xyne-spaces/pull/1235 | `juspay/xyne-spaces` | `code_only` | `typescript` | fix: XYNE-60825 revert PPTX viewer, KB UI polish, and workspace toolbar admin control |
| https://github.com/juspay/xyne-spaces/pull/1233 | `juspay/xyne-spaces` | `code_only` | `typescript` | fix: XYNE-60840 use canonical Spaces origin for review links |
| https://github.com/juspay/xyne-spaces/pull/1225 | `juspay/xyne-spaces` | `code_only` | `typescript` | fix: XYNE-60697 canvas links, files, dark mode and keyboard support |
| https://github.com/juspay/xyne-spaces/pull/1214 | `juspay/xyne-spaces` | `code_only` | `typescript` | refactor: XYNE-60840 extract shared null-safe attachment MIME matcher |
| https://github.com/juspay/xyne-spaces/pull/540 | `juspay/xyne-spaces` | `code_only` | `typescript` | fix: XYNE-56053 added copy button in link preview |
| https://github.com/juspay/xyne-spaces/pull/1223 | `juspay/xyne-spaces` | `code_only` | `typescript` | fix: XYNE-60697 canvas links, files, dark mode and keyboard support |
| https://github.com/juspay/xyne-spaces/pull/1224 | `juspay/xyne-spaces` | `code_only` | `typescript` | fix: XYNE-60697 canvas links, files, dark mode and keyboard support |
| https://github.com/juspay/xyne-spaces/pull/1209 | `juspay/xyne-spaces` | `code_only` | `typescript` | feat: XYNE-60825 add PPTX viewer, KB UI polish, and workspace toolbar admin control |
| https://github.com/juspay/xyne-spaces/pull/970 | `juspay/xyne-spaces` | `code_only` | `typescript` | feat: XYNE-56597 : Fix for nav bar when ask ai opens |
| https://github.com/juspay/xyne-spaces/pull/1179 | `juspay/xyne-spaces` | `code_only` | `typescript` | feat: XYNE-55834 fix selection of tickets |
| https://github.com/juspay/xyne-spaces/pull/1222 | `juspay/xyne-spaces` | `code_only` | `typescript` | fix: Onyx Tool change |
| https://github.com/juspay/xyne-spaces/pull/1216 | `juspay/xyne-spaces` | `code_only` | `typescript` | fix: trigger workflow chain for pending responses |
| https://github.com/juspay/xyne-spaces/pull/1217 | `juspay/xyne-spaces` | `code_only` | `typescript` | fix: XYNE-60618 enable jemalloc heap profiling to trace native memory leak |
| https://github.com/juspay/xyne-spaces/pull/1212 | `juspay/xyne-spaces` | `code_only` | `typescript` | feat: XYNE-60697 pop out artifacts from tracks, and expand with the discussion |
| https://github.com/juspay/xyne-spaces/pull/1211 | `juspay/xyne-spaces` | `code_only` | `typescript` | feat: XYNE-60697 pop out artifacts from tracks, and expand with the discussion |
| https://github.com/juspay/xyne-spaces/pull/1210 | `juspay/xyne-spaces` | `code_only` | `typescript` | feat: XYNE-60697 pop out artifacts from tracks, and expand with the discussion |
| https://github.com/juspay/xyne-spaces/pull/1201 | `juspay/xyne-spaces` | `code_only` | `typescript` | feat: XYNE-60774 add humanized cron schedule display in v3 |
| https://github.com/juspay/xyne-spaces/pull/1117 | `juspay/xyne-spaces` | `code_only` | `typescript` | feat: XYNE-57690 radar execution tracking engine |
| https://github.com/juspay/xyne-spaces/pull/1206 | `juspay/xyne-spaces` | `code_only` | `typescript` | feat: XYNE-60697 open SDLC artifacts in a window of their own |
| https://github.com/juspay/xyne-spaces/pull/1195 | `juspay/xyne-spaces` | `code_only` | `typescript` | feat: XYNE-60697 open SDLC artifacts in a window of their own |
| https://github.com/juspay/xyne-spaces/pull/1196 | `juspay/xyne-spaces` | `code_only` | `typescript` | feat: XYNE-60697 open SDLC artifacts in a window of their own |
| https://github.com/juspay/xyne-spaces/pull/1194 | `juspay/xyne-spaces` | `code_only` | `typescript` | feat: XYNE-60697 open SDLC artifacts in a window of their own |
| https://github.com/juspay/xyne-spaces/pull/1198 | `juspay/xyne-spaces` | `code_only` | `typescript` | feat: XYNE-60772 improve webhook payload guidance and draft deletion |
| https://github.com/juspay/xyne-spaces/pull/1197 | `juspay/xyne-spaces` | `code_only` | `typescript` | feat: show last updated date for skills |
| https://github.com/juspay/xyne-spaces/pull/1193 | `juspay/xyne-spaces` | `code_only` | `typescript` | fix: XYNE-60759 external dashboard docker build fix |
| https://github.com/juspay/xyne-spaces/pull/1166 | `juspay/xyne-spaces` | `code_only` | `typescript` | fix: scope ticket reads and writes to reachable tickets, across child tables |
| https://github.com/juspay/xyne-spaces/pull/585 | `juspay/xyne-spaces` | `code_only` | `typescript` | fix: show loaders while Zero queries load on data-backed surfaces |
| https://github.com/cookiecutter/cookiecutter/pull/2029 | `cookiecutter/cookiecutter` | `code_only` | `python` | Convert CLI provided strings to booleans for boolean config variables |
| https://github.com/cookiecutter/cookiecutter/pull/2189 | `cookiecutter/cookiecutter` | `code_and_docs` | `python` | Add Python 3.14 support |
| https://github.com/cookiecutter/cookiecutter/pull/2184 | `cookiecutter/cookiecutter` | `code_only` | `python` | Drop Python 3.9 support |
| https://github.com/cookiecutter/cookiecutter/pull/1981 | `cookiecutter/cookiecutter` | `code_and_docs` | `python` | Implement new style for nested templates config |
| https://github.com/cookiecutter/cookiecutter/pull/2171 | `cookiecutter/cookiecutter` | `code_only` | `python` | fix: empty list causes a crash due to index out of range, explictly raise ValueError now |
| https://github.com/cookiecutter/cookiecutter/pull/2099 | `cookiecutter/cookiecutter` | `code_only` | `python` | Makes order of directory resolving deterministic across different OS |
| https://github.com/cookiecutter/cookiecutter/pull/2147 | `cookiecutter/cookiecutter` | `code_only` | `python` | Close ZipFile with context manager in unzip |
| https://github.com/cookiecutter/cookiecutter/pull/2162 | `cookiecutter/cookiecutter` | `code_and_docs` | `python` | Update CONTRIBUTING.md and dependencies after packaging modernization |
| https://github.com/cookiecutter/cookiecutter/pull/2140 | `cookiecutter/cookiecutter` | `code_and_docs` | `python` | Update README.md to reflect Python 3.7 no longer supported |
| https://github.com/cookiecutter/cookiecutter/pull/2160 | `cookiecutter/cookiecutter` | `code_and_docs` | `python` | Migrate make docs to just docs |
| https://github.com/cookiecutter/cookiecutter/pull/1858 | `cookiecutter/cookiecutter` | `code_and_docs` | `python` | Update base docs, remove tox |
| https://github.com/cookiecutter/cookiecutter/pull/2159 | `cookiecutter/cookiecutter` | `code_only` | `python` | Update Python support to 3.9–3.13 |
| https://github.com/cookiecutter/cookiecutter/pull/2158 | `cookiecutter/cookiecutter` | `code_only` | `python` | Add justfile list recipe |
| https://github.com/cookiecutter/cookiecutter/pull/2157 | `cookiecutter/cookiecutter` | `code_and_docs` | `python` | Modernize packaging and CI/CD workflow |
| https://github.com/cookiecutter/cookiecutter/pull/2156 | `cookiecutter/cookiecutter` | `code_only` | `python` | Update author info |
| https://github.com/cookiecutter/cookiecutter/pull/1991 | `cookiecutter/cookiecutter` | `code_only` | `python` | [1518] Directory Name Render and Create Fix |
| https://github.com/cookiecutter/cookiecutter/pull/2061 | `cookiecutter/cookiecutter` | `code_only` | `python` | add more ruff lints |
| https://github.com/cookiecutter/cookiecutter/pull/2052 | `cookiecutter/cookiecutter` | `code_only` | `python` | Drop support for Python 3.7 |
| https://github.com/cookiecutter/cookiecutter/pull/2084 | `cookiecutter/cookiecutter` | `code_only_tests_or_fixtures` | `python` | Bump paambaati/codeclimate-action from 6.0.0 to 8.0.0 |
| https://github.com/cookiecutter/cookiecutter/pull/2068 | `cookiecutter/cookiecutter` | `code_only_tests_or_fixtures` | `python` | Bump paambaati/codeclimate-action from 5.0.0 to 6.0.0 |
| https://github.com/cookiecutter/cookiecutter/pull/2074 | `cookiecutter/cookiecutter` | `code_only` | `python` | Upgrade to safety v3 |
| https://github.com/cookiecutter/cookiecutter/pull/2063 | `cookiecutter/cookiecutter` | `code_only_tests_or_fixtures` | `python` | don't test old interpreters on macOS and windows |
| https://github.com/cookiecutter/cookiecutter/pull/2062 | `cookiecutter/cookiecutter` | `code_only` | `python` | [pre-commit.ci] pre-commit autoupdate |
| https://github.com/cookiecutter/cookiecutter/pull/2059 | `cookiecutter/cookiecutter` | `code_only` | `python` | run mypy on tests directory |
| https://github.com/cookiecutter/cookiecutter/pull/2060 | `cookiecutter/cookiecutter` | `code_only` | `python` | shrink mypy whitelist for 'main' module |
| https://github.com/cookiecutter/cookiecutter/pull/2055 | `cookiecutter/cookiecutter` | `code_only` | `python` | shrink mypy whitelist for 'extensions' module |
| https://github.com/cookiecutter/cookiecutter/pull/2056 | `cookiecutter/cookiecutter` | `code_only` | `python` | shrink mypy whitelist for 'environment' module |
| https://github.com/cookiecutter/cookiecutter/pull/2054 | `cookiecutter/cookiecutter` | `code_only` | `python` | shrink mypy whitelist for other modules |
| https://github.com/cookiecutter/cookiecutter/pull/2053 | `cookiecutter/cookiecutter` | `code_only` | `python` | shrink mypy whitelist for cookiecutter.utils |
| https://github.com/cookiecutter/cookiecutter/pull/2049 | `cookiecutter/cookiecutter` | `code_only` | `python` | remove some unused args |
| https://github.com/cookiecutter/cookiecutter/pull/2050 | `cookiecutter/cookiecutter` | `code_and_docs` | `python` | Add optional indent parameter to jsonify extension |
| https://github.com/cookiecutter/cookiecutter/pull/2046 | `cookiecutter/cookiecutter` | `code_only` | `python` | [pre-commit.ci] pre-commit autoupdate |
| https://github.com/cookiecutter/cookiecutter/pull/2051 | `cookiecutter/cookiecutter` | `code_and_docs` | `python` | Add type hints for cookiecutter.cli and check it with mypy |
| https://github.com/cookiecutter/cookiecutter/pull/2041 | `cookiecutter/cookiecutter` | `code_only` | `python` | shrink mypy whitelist for cookiecutter.generate |
| https://github.com/cookiecutter/cookiecutter/pull/2044 | `cookiecutter/cookiecutter` | `code_only` | `python` | Use pytest 6.0+ compatible [tool.pytest.ini_options] instead of [tool.pytest] on pyproject.toml |
| https://github.com/cookiecutter/cookiecutter/pull/2007 | `cookiecutter/cookiecutter` | `code_only_tests_or_fixtures` | `python` | Bump codecov/codecov-action from 3 to 4 |
| https://github.com/cookiecutter/cookiecutter/pull/2042 | `cookiecutter/cookiecutter` | `code_only` | `python` | shrink mypy whitelist for cookiecutter.hooks |
| https://github.com/cookiecutter/cookiecutter/pull/2043 | `cookiecutter/cookiecutter` | `code_only` | `python` | [pre-commit.ci] pre-commit autoupdate |
| https://github.com/cookiecutter/cookiecutter/pull/2040 | `cookiecutter/cookiecutter` | `code_only` | `python` | move configuration from setup.cfg to pyproject.toml |
| https://github.com/cookiecutter/cookiecutter/pull/2026 | `cookiecutter/cookiecutter` | `code_only` | `python` | Bump release-drafter/release-drafter from 5 to 6 |
| https://github.com/cookiecutter/cookiecutter/pull/2020 | `cookiecutter/cookiecutter` | `code_only` | `python` | enable lint groups for string formatting |
| https://github.com/cookiecutter/cookiecutter/pull/2016 | `cookiecutter/cookiecutter` | `code_and_docs` | `python` | Add 'pygrep' lints |
| https://github.com/cookiecutter/cookiecutter/pull/2019 | `cookiecutter/cookiecutter` | `code_only` | `python` | add 'perf' lint group |
| https://github.com/cookiecutter/cookiecutter/pull/2014 | `cookiecutter/cookiecutter` | `code_only` | `python` | Add 'pyflakes' lints |
| https://github.com/cookiecutter/cookiecutter/pull/2015 | `cookiecutter/cookiecutter` | `code_only` | `python` | add minimal mypy linting |
| https://github.com/cookiecutter/cookiecutter/pull/2012 | `cookiecutter/cookiecutter` | `code_and_docs` | `python` | Use 'Ruff' for linting and formatting |
| https://github.com/cookiecutter/cookiecutter/pull/1996 | `cookiecutter/cookiecutter` | `code_only` | `python` | [pre-commit.ci] pre-commit autoupdate |
| https://github.com/cookiecutter/cookiecutter/pull/2000 | `cookiecutter/cookiecutter` | `code_only` | `python` | Bump actions/setup-python from 4 to 5 |
| https://github.com/cookiecutter/cookiecutter/pull/1999 | `cookiecutter/cookiecutter` | `code_only_tests_or_fixtures` | `python` | Bump actions/upload-artifact from 3 to 4 |
| https://github.com/cookiecutter/cookiecutter/pull/2010 | `cookiecutter/cookiecutter` | `code_only` | `python` | Fix regression #2009: Adding value to nested dicts broken |
| https://github.com/cookiecutter/cookiecutter/pull/1997 | `cookiecutter/cookiecutter` | `code_and_docs` | `python` | fix: modifying start and end variable strings |
| https://github.com/cookiecutter/cookiecutter/pull/2004 | `cookiecutter/cookiecutter` | `code_only` | `python` | Quick resolution of #2003 |
| https://github.com/cookiecutter/cookiecutter/pull/1995 | `cookiecutter/cookiecutter` | `code_only` | `python` | Fixed errors caused by invalid config files. |
| https://github.com/cookiecutter/cookiecutter/pull/1961 | `cookiecutter/cookiecutter` | `code_only` | `python` | Fix recursive context overwrites |
| https://github.com/cookiecutter/cookiecutter/pull/1920 | `cookiecutter/cookiecutter` | `code_only` | `python` | Fix variables with null default not being required (#1919) |
| https://github.com/cookiecutter/cookiecutter/pull/1923 | `cookiecutter/cookiecutter` | `code_only` | `python` | add checkout details to the context (fixes #1759) |
| https://github.com/cookiecutter/cookiecutter/pull/1989 | `cookiecutter/cookiecutter` | `code_and_docs` | `python` | Support Python 3.12 |
| https://github.com/cookiecutter/cookiecutter/pull/1988 | `cookiecutter/cookiecutter` | `code_only` | `python` | Add isort as a pre-commit hook |
| https://github.com/cookiecutter/cookiecutter/pull/1924 | `cookiecutter/cookiecutter` | `code_only` | `python` | Default values can be passed as a dict |
| https://github.com/cookiecutter/cookiecutter/pull/1977 | `cookiecutter/cookiecutter` | `code_only` | `python` | [pre-commit.ci] pre-commit autoupdate |
| https://github.com/quay/quay/pull/7002 | `quay/quay` | `code_only` | `python` | QUAYIO-2183: fix(logging): downgrade client-caused bearer token errors from ERROR to WARNING |
| https://github.com/quay/quay/pull/7016 | `quay/quay` | `code_only` | `python` | NO-ISSUE: fix(ci): install surge globally in playwright report deploy |
| https://github.com/quay/quay/pull/6781 | `quay/quay` | `code_only` | `python` | [redhat-3.17] NO-ISSUE: build(hermetic): Add Containerfile.art and ART files for Konflux integration |
| https://github.com/quay/quay/pull/7012 | `quay/quay` | `code_only` | `python` | [redhat-3.16] PROJQUAY-11682: fix(autoprune): re-land Cosign tag exclusion with race-safe cascade |
| https://github.com/quay/quay/pull/5876 | `quay/quay` | `code_only` | `python` | [redhat-3.17] PROJQUAY-11441: fix(ui): permission dropdowns navigate away in Firefox |
| https://github.com/quay/quay/pull/6017 | `quay/quay` | `code_only` | `python` | [redhat-3.17] PROJQUAY-11580: fix(ui): move usage logs chart legend outside chart SVG to prevent overlap |
| https://github.com/quay/quay/pull/6265 | `quay/quay` | `code_only` | `python` | [redhat-3.17] PROJQUAY-12102: fix(web): redesign logo selection for dark mode support |
| https://github.com/quay/quay/pull/6456 | `quay/quay` | `code_only` | `python` | [redhat-3.17] PROJQUAY-12199: fix(proxy): serve cached images when upstream registry is unavailable |
| https://github.com/quay/quay/pull/7011 | `quay/quay` | `code_only` | `python` | PROJQUAY-12749: fix(deps): update fast-uri to >=3.1.4 for CVE-2026-16221 |
| https://github.com/quay/quay/pull/6982 | `quay/quay` | `code_only` | `python` | PROJQUAY-12753: fix(deps): update fast-uri to >=3.1.4 for CVE-2026-16221 |
| https://github.com/quay/quay/pull/6990 | `quay/quay` | `code_only` | `python` | [redhat-3.17] PROJQUAY-11682: fix(autoprune): re-land Cosign tag exclusion with race-safe cascade |
| https://github.com/quay/quay/pull/7005 | `quay/quay` | `code_only` | `python` | PROJQUAY-12843: fix: use --nobest flag for microdnf update and clean metadata before install |
| https://github.com/quay/quay/pull/6983 | `quay/quay` | `code_only` | `python` | NO-ISSUE: chore(ci): limit fullsend to master branch |
| https://github.com/quay/quay/pull/6972 | `quay/quay` | `code_only` | `python` | PROJQUAY-12711: fix(mirrorregistry): avoid tag expiration timestamp collisions |
| https://github.com/quay/quay/pull/6979 | `quay/quay` | `code_only_tests_or_fixtures` | `python` | [redhat-3.17] NO-ISSUE: fix(config): map FEATURE_ENABLE_STALE_MPU_CLEANUP as known-unmapped |
| https://github.com/quay/quay/pull/6920 | `quay/quay` | `code_only` | `python` | [redhat-3.18] PROJQUAY-12739: fix(cve): CVE-2026-67320 - bump axios to 1.19.0 |
| https://github.com/quay/quay/pull/6632 | `quay/quay` | `code_only` | `python` | PROJQUAY-12348: fix(ui): default marketplace subscriptions to empty arrays |
| https://github.com/quay/quay/pull/6659 | `quay/quay` | `code_only` | `python` | [redhat-3.17] PROJQUAY-12812: feat(secscan): add retry limiting via metadata_json |
| https://github.com/quay/quay/pull/6922 | `quay/quay` | `code_only` | `python` | [redhat-3.16] PROJQUAY-12737: fix(cve): CVE-2026-67320 - bump axios to 1.19.0 |
| https://github.com/quay/quay/pull/6668 | `quay/quay` | `code_only` | `python` | PROJQUAY-12278: feat(config): add configurable gunicorn worker timeouts |
| https://github.com/quay/quay/pull/6909 | `quay/quay` | `code_only` | `python` | PROJQUAY-12753: fix(deps): update fast-uri to >=3.1.4 for CVE-2026-16221 |
| https://github.com/quay/quay/pull/6969 | `quay/quay` | `code_only` | `python` | [redhat-3.18] NO-ISSUE: fix(cve): CVE-2026-73089 - bump browserslist |
| https://github.com/quay/quay/pull/6959 | `quay/quay` | `code_only` | `python` | [redhat-3.9] PROJQUAY-12581: fix(cve): CVE-2026-73089 - bump browserslist |
| https://github.com/quay/quay/pull/6967 | `quay/quay` | `code_only` | `python` | [redhat-3.14] PROJQUAY-12580: fix(cve): CVE-2026-73089 - bump browserslist |
| https://github.com/quay/quay/pull/6968 | `quay/quay` | `code_only` | `python` | [redhat-3.12] PROJQUAY-12583: fix(cve): CVE-2026-73089 - bump browserslist |
| https://github.com/quay/quay/pull/6962 | `quay/quay` | `code_only` | `python` | [redhat-3.17] NO-ISSUE: fix(cve): CVE-2026-73089 - bump browserslist |
| https://github.com/quay/quay/pull/6966 | `quay/quay` | `code_only` | `python` | [redhat-3.15] PROJQUAY-12584: fix(cve): CVE-2026-73089 - bump browserslist |
| https://github.com/quay/quay/pull/6965 | `quay/quay` | `code_only` | `python` | [redhat-3.16] NO-ISSUE: fix(cve): CVE-2026-73089 - bump browserslist |
| https://github.com/quay/quay/pull/6960 | `quay/quay` | `code_only` | `python` | NO-ISSUE: fix(cve): CVE-2026-73089 - bump browserslist |
| https://github.com/quay/quay/pull/6963 | `quay/quay` | `code_only` | `python` | [redhat-3.10] PROJQUAY-12582: fix(cve): CVE-2026-73089 - bump browserslist |
| https://github.com/quay/quay/pull/6974 | `quay/quay` | `code_only` | `python` | [redhat-3.17] PROJQUAY-12792: fix: Clean up orphaned multipart uploads as part of blob cleanup |
| https://github.com/quay/quay/pull/6976 | `quay/quay` | `code_only` | `python` | [redhat-3.16] PROJQUAY-12801: fix: Clean up orphaned multipart uploads as part of blob cleanup |
| https://github.com/quay/quay/pull/6973 | `quay/quay` | `code_only` | `python` | [redhat-3.18] PROJQUAY-12791: fix: Clean up orphaned multipart uploads as part of blob cleanup |
| https://github.com/quay/quay/pull/6885 | `quay/quay` | `code_only` | `python` | PROJQUAY-12557: fix: Clean up orphaned multipart uploads as part of blob cleanup |
| https://github.com/quay/quay/pull/6941 | `quay/quay` | `code_only` | `python` | [redhat-3.12] PROJQUAY-12465: fix(cve): CVE-2026-69153 - postcss |
| https://github.com/quay/quay/pull/6939 | `quay/quay` | `code_only` | `python` | [redhat-3.17] PROJQUAY-12461: fix(cve): CVE-2026-69153 - postcss |
| https://github.com/quay/quay/pull/6940 | `quay/quay` | `code_only` | `python` | [redhat-3.15] PROJQUAY-12462: fix(cve): CVE-2026-69153 - postcss |
| https://github.com/quay/quay/pull/6943 | `quay/quay` | `code_only` | `python` | [redhat-3.14] PROJQUAY-12460: fix(cve): CVE-2026-69153 - postcss |
| https://github.com/quay/quay/pull/6944 | `quay/quay` | `code_only` | `python` | [redhat-3.9] PROJQUAY-12466: fix(cve): CVE-2026-69153 - postcss |
| https://github.com/quay/quay/pull/6942 | `quay/quay` | `code_only` | `python` | [redhat-3.10] PROJQUAY-12464: fix(cve): CVE-2026-69153 - postcss |
| https://github.com/quay/quay/pull/6928 | `quay/quay` | `code_only` | `python` | [redhat-3.15] PROJQUAY-12571: deps: Bump nanoid to 3.3.12 |
| https://github.com/quay/quay/pull/6925 | `quay/quay` | `code_only` | `python` | [redhat-3.12] PROJQUAY-12735: fix(cve): CVE-2026-67320 - bump axios to 1.19.0 |
| https://github.com/quay/quay/pull/6927 | `quay/quay` | `code_only` | `python` | [redhat-3.9] PROJQUAY-12740: fix(cve): CVE-2026-67320 - bump axios to 1.19.0 |
| https://github.com/quay/quay/pull/6926 | `quay/quay` | `code_only` | `python` | [redhat-3.10] PROJQUAY-12733: fix(cve): CVE-2026-67320 - bump axios to 1.19.0 |
| https://github.com/quay/quay/pull/6924 | `quay/quay` | `code_only` | `python` | [redhat-3.14] PROJQUAY-12734: fix(cve): CVE-2026-67320 - bump axios to 1.19.0 |
| https://github.com/quay/quay/pull/6923 | `quay/quay` | `code_only` | `python` | [redhat-3.15] PROJQUAY-12736: fix(cve): CVE-2026-67320 - bump axios to 1.19.0 |
| https://github.com/quay/quay/pull/6921 | `quay/quay` | `code_only` | `python` | [redhat-3.17] PROJQUAY-12738: fix(cve): CVE-2026-67320 - bump axios to 1.19.0 |
| https://github.com/quay/quay/pull/6805 | `quay/quay` | `code_only` | `python` | QUAYIO-2122: feat(secscan): add thread pool for concurrent V2 manifest indexing |
| https://github.com/quay/quay/pull/6831 | `quay/quay` | `code_only` | `python` | PROJQUAY-12435: feat(migration): migrate OMR PostgreSQL sources |
| https://github.com/quay/quay/pull/6915 | `quay/quay` | `code_and_docs` | `python` | [redhat-3.16] NO-ISSUE: chore(ci): backport workflow consolidation |
| https://github.com/quay/quay/pull/6933 | `quay/quay` | `code_only` | `python` | NO-ISSUE: chore(deps): Update re-actors/alls-green digest to b5b5b37 |
| https://github.com/quay/quay/pull/6717 | `quay/quay` | `code_only` | `python` | QUAYIO-1826: feat(gc): add configurable grace period for namespace deletion |
| https://github.com/quay/quay/pull/6295 | `quay/quay` | `code_and_docs` | `python` | [redhat-3.17] NO-ISSUE: ci: consolidate workflows into sentinel gate |
| https://github.com/quay/quay/pull/6905 | `quay/quay` | `code_only` | `python` | NO-ISSUE: chore(ci): pre-commit autoupdate |
| https://github.com/quay/quay/pull/6901 | `quay/quay` | `code_only` | `python` | NO-ISSUE: chore(deps): Update registry.access.redhat.com/ubi9/python-312-minimal:9.8 Docker digest to 0682a7a |
| https://github.com/quay/quay/pull/6900 | `quay/quay` | `code_only` | `python` | NO-ISSUE: chore(deps): Update registry.access.redhat.com/ubi9/nodejs-22-minimal:9.8 Docker digest to fc8e8eb |
| https://github.com/quay/quay/pull/6803 | `quay/quay` | `code_only` | `python` | [redhat-3.17] QUAYIO-2123: fix: platform KeyError |
| https://github.com/quay/quay/pull/6824 | `quay/quay` | `code_only` | `python` | NO-ISSUE: chore(ci): bump the github-actions group across 1 directory with 8 updates |
| https://github.com/quay/quay/pull/6701 | `quay/quay` | `code_only` | `python` | NO-ISSUE: chore(deps): Update registry.access.redhat.com/ubi9/ubi-minimal:9.8 Docker digest to 8eb2830 |
| https://github.com/quay/quay/pull/5895 | `quay/quay` | `code_only` | `python` | NO-ISSUE: chore(ci): bump agenthunt/conventional-commit-checker-action from 2.0.0 to 2.0.1 |
| https://github.com/pytest-dev/pytest-cov/pull/722 | `pytest-dev/pytest-cov` | `code_only_tests_or_fixtures` | `python` | match coverage 7.10.7 warnings |
| https://github.com/pytest-dev/pytest-cov/pull/727 | `pytest-dev/pytest-cov` | `code_and_docs` | `python` | Improve handling of ResourceWarning from sqlite3. |
| https://github.com/pytest-dev/pytest-cov/pull/717 | `pytest-dev/pytest-cov` | `code_only_tests_or_fixtures` | `python` | Bump the github-actions group with 2 updates |
| https://github.com/pytest-dev/pytest-cov/pull/712 | `pytest-dev/pytest-cov` | `code_and_docs` | `python` | Adding Markdown support as a file_choice |
| https://github.com/pytest-dev/pytest-cov/pull/716 | `pytest-dev/pytest-cov` | `code_and_docs` | `python` | Replace setuptools build backend with hatchling [rebased] |
| https://github.com/pytest-dev/pytest-cov/pull/715 | `pytest-dev/pytest-cov` | `code_and_docs` | `python` | Remove subprocess support |
| https://github.com/pytest-dev/pytest-cov/pull/709 | `pytest-dev/pytest-cov` | `code_only_tests_or_fixtures` | `python` | Bump actions/checkout from 4 to 5 in the github-actions group |
| https://github.com/pytest-dev/pytest-cov/pull/705 | `pytest-dev/pytest-cov` | `code_only` | `python` | Fix typo |
| https://github.com/pytest-dev/pytest-cov/pull/700 | `pytest-dev/pytest-cov` | `code_and_docs` | `python` | Rebase of 695 |
| https://github.com/pytest-dev/pytest-cov/pull/696 | `pytest-dev/pytest-cov` | `code_and_docs` | `python` | Add default filterwarning configuration |
| https://github.com/pytest-dev/pytest-cov/pull/686 | `pytest-dev/pytest-cov` | `code_and_docs` | `python` | Allow the context plugin to check if the controller is running or not. |
| https://github.com/pytest-dev/pytest-cov/pull/547 | `pytest-dev/pytest-cov` | `code_and_docs` | `python` | Remove appveyor |
| https://github.com/pytest-dev/pytest-cov/pull/548 | `pytest-dev/pytest-cov` | `code_only` | `python` | Improve workflow with a collecting status check. |
| https://github.com/pytest-dev/pytest-cov/pull/556 | `pytest-dev/pytest-cov` | `code_only` | `python` | Revert "Enable `pytest-cov[toml]` akin to upstream `coverage[toml]`" |
| https://github.com/pytest-dev/pytest-cov/pull/656 | `pytest-dev/pytest-cov` | `code_and_docs` | `python` | Handle precision for fail-under option |
| https://github.com/pytest-dev/pytest-cov/pull/657 | `pytest-dev/pytest-cov` | `code_only` | `python` | Handle issue 604 |
| https://github.com/pytest-dev/pytest-cov/pull/684 | `pytest-dev/pytest-cov` | `code_only` | `python` | Make sure the CLI precision is used when creating report. Fixes #674. |
| https://github.com/pytest-dev/pytest-cov/pull/683 | `pytest-dev/pytest-cov` | `code_only` | `python` | Remove unnecessary CovFailUnderWarning. Closes #675. |
| https://github.com/pytest-dev/pytest-cov/pull/678 | `pytest-dev/pytest-cov` | `code_only` | `python` | Improve Terminal Output Formatting in pytest-cov |
| https://github.com/pytest-dev/pytest-cov/pull/643 | `pytest-dev/pytest-cov` | `code_only_tests_or_fixtures` | `python` | Support Coverage 7.5's HTML report changes |
| https://github.com/pytest-dev/pytest-cov/pull/645 | `pytest-dev/pytest-cov` | `code_only` | `python` | Use ruff for formatting too |
| https://github.com/pytest-dev/pytest-cov/pull/467 | `pytest-dev/pytest-cov` | `code_only` | `python` | change license in setup.py from BSD to MIT to match LICENSE file |
| https://github.com/pytest-dev/pytest-cov/pull/630 | `pytest-dev/pytest-cov` | `code_only` | `python` | Keep GitHub Actions up to date with GitHub's Dependabot |
| https://github.com/pytest-dev/pytest-cov/pull/632 | `pytest-dev/pytest-cov` | `code_only` | `python` | Remove redundant code for Python 2 |
| https://github.com/pytest-dev/pytest-cov/pull/558 | `pytest-dev/pytest-cov` | `code_only` | `python` | Remove use of rsyncdir |
| https://github.com/pytest-dev/pytest-cov/pull/589 | `pytest-dev/pytest-cov` | `code_and_docs` | `python` | perf: only call summary when the report will be used |
| https://github.com/pytest-dev/pytest-cov/pull/567 | `pytest-dev/pytest-cov` | `code_only` | `python` | Add Python 3.11 and PyPy 3.9 to the testing and drop 3.6 |
| https://github.com/pytest-dev/pytest-cov/pull/563 | `pytest-dev/pytest-cov` | `code_only` | `python` | Update and reorder pre-commit config file |
| https://github.com/pytest-dev/pytest-cov/pull/559 | `pytest-dev/pytest-cov` | `code_only` | `python` | Remove travis integration |
| https://github.com/pytest-dev/pytest-cov/pull/553 | `pytest-dev/pytest-cov` | `code_only` | `python` | Enable `pytest-cov[toml]` akin to upstream `coverage[toml]` |
| https://github.com/pytest-dev/pytest-cov/pull/536 | `pytest-dev/pytest-cov` | `code_and_docs` | `python` | Add support for LCOV output |
| https://github.com/pytest-dev/pytest-cov/pull/549 | `pytest-dev/pytest-cov` | `code_and_docs` | `python` | Use modern approach to specify hook options |
| https://github.com/pytest-dev/pytest-cov/pull/511 | `pytest-dev/pytest-cov` | `code_and_docs` | `python` | `--cov-fail-under` should not cause `pytest --collect-only` to fail |
| https://github.com/pytest-dev/pytest-cov/pull/540 | `pytest-dev/pytest-cov` | `code_only` | `python` | Prevent undesirable new lines to be displayed when report is disabled |
| https://github.com/pytest-dev/pytest-cov/pull/545 | `pytest-dev/pytest-cov` | `code_only` | `python` | migrate build command from distutils to setuptools |
| https://github.com/pytest-dev/pytest-cov/pull/515 | `pytest-dev/pytest-cov` | `code_only` | `python` | [pre-commit.ci] pre-commit autoupdate |
| https://github.com/pytest-dev/pytest-cov/pull/518 | `pytest-dev/pytest-cov` | `code_only_tests_or_fixtures` | `python` | Update test_invalid_coverage_source for coverage-6.2 |
| https://github.com/pytest-dev/pytest-cov/pull/503 | `pytest-dev/pytest-cov` | `code_only` | `python` | [pre-commit.ci] pre-commit autoupdate |
| https://github.com/pytest-dev/pytest-cov/pull/349 | `pytest-dev/pytest-cov` | `code_and_docs` | `python` | Fix regression described in #348 - not all reports returning the total. |
| https://github.com/pytest-dev/pytest-cov/pull/344 | `pytest-dev/pytest-cov` | `code_and_docs` | `python` | Next release |
| https://github.com/pytest-dev/pytest-cov/pull/370 | `pytest-dev/pytest-cov` | `code_only` | `python` | The context tests were failing on newer coverage |
| https://github.com/pytest-dev/pytest-cov/pull/420 | `pytest-dev/pytest-cov` | `code_and_docs` | `python` | Precommit and some dep updates |
| https://github.com/pytest-dev/pytest-cov/pull/382 | `pytest-dev/pytest-cov` | `code_only` | `python` | Silence spurious warnings when xdist is used |
| https://github.com/pytest-dev/pytest-cov/pull/501 | `pytest-dev/pytest-cov` | `code_only` | `python` | [pre-commit.ci] pre-commit autoupdate |
| https://github.com/pytest-dev/pytest-cov/pull/491 | `pytest-dev/pytest-cov` | `code_only` | `python` | [pre-commit.ci] pre-commit autoupdate |
| https://github.com/pytest-dev/pytest-cov/pull/498 | `pytest-dev/pytest-cov` | `code_only` | `python` | Fix spelling error |
| https://github.com/pytest-dev/pytest-cov/pull/500 | `pytest-dev/pytest-cov` | `code_only` | `python` | Add support for Python 3.10 |
| https://github.com/pytest-dev/pytest-cov/pull/494 | `pytest-dev/pytest-cov` | `code_and_docs` | `python` | Test on GitHub Actions |
| https://github.com/pytest-dev/pytest-cov/pull/495 | `pytest-dev/pytest-cov` | `code_only_tests_or_fixtures` | `python` | Hello world to demo GHA |
| https://github.com/pytest-dev/pytest-cov/pull/480 | `pytest-dev/pytest-cov` | `code_only` | `python` | Improve argument validation a bit. |
| https://github.com/pytest-dev/pytest-cov/pull/488 | `pytest-dev/pytest-cov` | `code_and_docs` | `python` | Update .pre-commit-config.yaml |
| https://github.com/pytest-dev/pytest-cov/pull/459 | `pytest-dev/pytest-cov` | `code_and_docs` | `python` | Implement --cov-reset option that resets accumulated --cov directorie… |
| https://github.com/pytest-dev/pytest-cov/pull/481 | `pytest-dev/pytest-cov` | `code_only` | `python` | Add Python 3.9 to trove classifiers |
| https://github.com/pytest-dev/pytest-cov/pull/490 | `pytest-dev/pytest-cov` | `code_only` | `python` | [pre-commit.ci] pre-commit autoupdate |
| https://github.com/pytest-dev/pytest-cov/pull/489 | `pytest-dev/pytest-cov` | `code_and_docs` | `python` | pre-commit autoupdate |
| https://github.com/pytest-dev/pytest-cov/pull/361 | `pytest-dev/pytest-cov` | `code_only` | `python` | warn specific classes |
| https://github.com/pytest-dev/pytest-cov/pull/477 | `pytest-dev/pytest-cov` | `code_only` | `python` | Revert "Avoid using toml as extra (#472)" |
| https://github.com/pytest-dev/pytest-cov/pull/405 | `pytest-dev/pytest-cov` | `code_only` | `python` | Ensure topdir |
| https://github.com/pytest-dev/pytest-cov/pull/472 | `pytest-dev/pytest-cov` | `code_only` | `python` | Avoid using toml as extra |
| https://github.com/pytest-dev/pytest-cov/pull/410 | `pytest-dev/pytest-cov` | `code_and_docs` | `python` | Added toml as extra |
| https://github.com/bluewave-labs/Checkmate/pull/3902 | `bluewave-labs/checkmate` | `code_only` | `typescript` | feat(client): group settings into five tabs |
| https://github.com/bluewave-labs/Checkmate/pull/3905 | `bluewave-labs/checkmate` | `code_only` | `typescript` | feat(maintenance): show monitor tags in maintenance selector |
| https://github.com/bluewave-labs/Checkmate/pull/3901 | `bluewave-labs/checkmate` | `code_and_docs` | `typescript` | feat(client): group sidebar navigation into four labelled sections |
| https://github.com/bluewave-labs/Checkmate/pull/3900 | `bluewave-labs/checkmate` | `code_only` | `typescript` | fix(client): add hover states to tables, cards, stat boxes and icon buttons |
| https://github.com/bluewave-labs/Checkmate/pull/3897 | `bluewave-labs/checkmate` | `code_only` | `typescript` | fix(infrastructure): show the container-namespace notice when it applies |
| https://github.com/bluewave-labs/Checkmate/pull/3896 | `bluewave-labs/checkmate` | `code_only` | `typescript` | fix(infrastructure): clamp gauge arc and fix disk key fallback |
| https://github.com/bluewave-labs/Checkmate/pull/3895 | `bluewave-labs/checkmate` | `code_only` | `typescript` | fix(infrastructure): wrap gauge row so every disk stays reachable |
| https://github.com/bluewave-labs/Checkmate/pull/3899 | `bluewave-labs/checkmate` | `code_only` | `typescript` | feat: first class docker monitoring |
| https://github.com/bluewave-labs/Checkmate/pull/3894 | `bluewave-labs/checkmate` | `code_only` | `typescript` | chore: monitor list refactor |
| https://github.com/bluewave-labs/Checkmate/pull/3889 | `bluewave-labs/checkmate` | `code_only` | `typescript` | develop -> master |
| https://github.com/bluewave-labs/Checkmate/pull/3888 | `bluewave-labs/checkmate` | `code_only` | `typescript` | develop -> demo |
| https://github.com/bluewave-labs/Checkmate/pull/3887 | `bluewave-labs/checkmate` | `code_only` | `typescript` | feat: interpoalte colors for severity of downtime |
| https://github.com/bluewave-labs/Checkmate/pull/3886 | `bluewave-labs/checkmate` | `code_only` | `typescript` | fix: deal with empty strings for proxyId |
| https://github.com/bluewave-labs/Checkmate/pull/3884 | `bluewave-labs/checkmate` | `code_only` | `typescript` | develop -> demo |
| https://github.com/bluewave-labs/Checkmate/pull/3883 | `bluewave-labs/checkmate` | `code_only` | `typescript` | chore: set keep previous data |
| https://github.com/bluewave-labs/Checkmate/pull/3882 | `bluewave-labs/checkmate` | `code_only` | `typescript` | chore: add lockfile check |
| https://github.com/bluewave-labs/Checkmate/pull/3876 | `bluewave-labs/checkmate` | `code_only` | `typescript` | Fix/node version |
| https://github.com/bluewave-labs/Checkmate/pull/3875 | `bluewave-labs/checkmate` | `code_only` | `typescript` | fix package lock sync issue |
| https://github.com/bluewave-labs/Checkmate/pull/3873 | `bluewave-labs/checkmate` | `code_only` | `typescript` | minor version bump |
| https://github.com/bluewave-labs/Checkmate/pull/3872 | `bluewave-labs/checkmate` | `code_only` | `typescript` | fix: logo image preview CSP |
| https://github.com/bluewave-labs/Checkmate/pull/3863 | `bluewave-labs/checkmate` | `code_only` | `typescript` | feat(status-page): show monitor tags in status page selector |
| https://github.com/bluewave-labs/Checkmate/pull/3871 | `bluewave-labs/checkmate` | `code_only` | `typescript` | fix: remove dead workflows |
| https://github.com/bluewave-labs/Checkmate/pull/3870 | `bluewave-labs/checkmate` | `code_only` | `typescript` | fix: regen package lock |
| https://github.com/bluewave-labs/Checkmate/pull/3869 | `bluewave-labs/checkmate` | `code_only` | `typescript` | fix: proxy scoping |
| https://github.com/bluewave-labs/Checkmate/pull/3868 | `bluewave-labs/checkmate` | `code_only` | `typescript` | add global proxy setting config and translation keys |
| https://github.com/bluewave-labs/Checkmate/pull/3867 | `bluewave-labs/checkmate` | `code_only` | `typescript` | feat: proxy frontend |
| https://github.com/bluewave-labs/Checkmate/pull/3860 | `bluewave-labs/checkmate` | `code_only` | `typescript` | feat: proxy resolver |
| https://github.com/bluewave-labs/Checkmate/pull/3859 | `bluewave-labs/checkmate` | `code_only` | `typescript` | feat: outbound proxy server crud |
| https://github.com/bluewave-labs/Checkmate/pull/3858 | `bluewave-labs/checkmate` | `code_only` | `typescript` | feat(client): show uptime percentages with two decimals |
| https://github.com/bluewave-labs/Checkmate/pull/3856 | `bluewave-labs/checkmate` | `code_only` | `typescript` | feat: add theme mode to auth footer menu |
| https://github.com/bluewave-labs/Checkmate/pull/3855 | `bluewave-labs/checkmate` | `code_only` | `typescript` | feat: improve keyboard navigation on create monitor page |
| https://github.com/bluewave-labs/Checkmate/pull/3854 | `bluewave-labs/checkmate` | `code_only` | `typescript` | fix: add recent checks for infra monitors |
| https://github.com/bluewave-labs/Checkmate/pull/3851 | `bluewave-labs/checkmate` | `code_only` | `typescript` | chore: bump server dependencies |
| https://github.com/bluewave-labs/Checkmate/pull/3844 | `bluewave-labs/checkmate` | `code_only` | `typescript` | fix(security): redact sensitive fields from client-side logs |
| https://github.com/bluewave-labs/Checkmate/pull/3837 | `bluewave-labs/checkmate` | `code_only` | `typescript` | fix: propagate SMTP transport errors from EmailService.sendEmail |
| https://github.com/bluewave-labs/Checkmate/pull/3838 | `bluewave-labs/checkmate` | `code_only` | `typescript` | fix: resolve Matrix room aliases and encode room IDs in the send path |
| https://github.com/bluewave-labs/Checkmate/pull/3839 | `bluewave-labs/checkmate` | `code_only` | `typescript` | feat: add authentication support to ntfy notifications |
| https://github.com/bluewave-labs/Checkmate/pull/3847 | `bluewave-labs/checkmate` | `code_only` | `typescript` | fix(status-page): allow DNS monitors to be added to status pages |
| https://github.com/bluewave-labs/Checkmate/pull/3849 | `bluewave-labs/checkmate` | `code_only` | `typescript` | feat: status page ranges client |
| https://github.com/bluewave-labs/Checkmate/pull/3845 | `bluewave-labs/checkmate` | `code_only` | `typescript` | feat: status page ranges server |
| https://github.com/bluewave-labs/Checkmate/pull/3834 | `bluewave-labs/checkmate` | `code_only` | `typescript` | feat: add domain registration expiry monitoring |
| https://github.com/bluewave-labs/Checkmate/pull/3831 | `bluewave-labs/checkmate` | `code_only` | `typescript` | feat: enrich Rocket.Chat notifications |
| https://github.com/bluewave-labs/Checkmate/pull/3829 | `bluewave-labs/checkmate` | `code_only` | `typescript` | chore: form refactor |
| https://github.com/bluewave-labs/Checkmate/pull/3822 | `bluewave-labs/checkmate` | `code_and_docs` | `typescript` | feat: Rocket.Chat notifications |
| https://github.com/bluewave-labs/Checkmate/pull/3825 | `bluewave-labs/checkmate` | `code_only` | `typescript` | fix:  check snapshot |
| https://github.com/bluewave-labs/Checkmate/pull/3820 | `bluewave-labs/checkmate` | `code_only` | `typescript` | chore: ms cleanup |
| https://github.com/bluewave-labs/Checkmate/pull/3819 | `bluewave-labs/checkmate` | `code_only` | `typescript` | feat: client side presentation |
| https://github.com/bluewave-labs/Checkmate/pull/3808 | `bluewave-labs/checkmate` | `code_only_tests_or_fixtures` | `typescript` | test: cover monitor tag filtering |
| https://github.com/bluewave-labs/Checkmate/pull/3818 | `bluewave-labs/checkmate` | `code_only` | `typescript` | feat: chart cleanup |
| https://github.com/bluewave-labs/Checkmate/pull/3797 | `bluewave-labs/checkmate` | `code_only` | `typescript` | Fix monitoring status stuck |
| https://github.com/bluewave-labs/Checkmate/pull/3815 | `bluewave-labs/checkmate` | `code_only` | `typescript` | feat: stacked timing chart |
| https://github.com/bluewave-labs/Checkmate/pull/3801 | `bluewave-labs/checkmate` | `code_only` | `typescript` | chore: cleanup |
| https://github.com/bluewave-labs/Checkmate/pull/3800 | `bluewave-labs/checkmate` | `code_only` | `typescript` | extact monitor children deletion to helper |
| https://github.com/bluewave-labs/Checkmate/pull/3799 | `bluewave-labs/checkmate` | `code_only` | `typescript` | chore: domain refactoring |
| https://github.com/bluewave-labs/Checkmate/pull/3798 | `bluewave-labs/checkmate` | `code_only` | `typescript` | chore: api cleanup |
| https://github.com/bluewave-labs/Checkmate/pull/3796 | `bluewave-labs/checkmate` | `code_only` | `typescript` | Fixes UI bug with German translations |
| https://github.com/bluewave-labs/Checkmate/pull/3795 | `bluewave-labs/checkmate` | `code_only` | `typescript` | fix: remove inline enum definitions |
| https://github.com/bluewave-labs/Checkmate/pull/3794 | `bluewave-labs/checkmate` | `code_only` | `typescript` | fix: positional args |
| https://github.com/bluewave-labs/Checkmate/pull/3793 | `bluewave-labs/checkmate` | `code_only` | `typescript` | chore: convert router classes to exported functions |
| https://github.com/bluewave-labs/Checkmate/pull/3792 | `bluewave-labs/checkmate` | `code_only` | `typescript` | purge unused groups route, update tests |
| https://github.com/ColeMurray/background-agents/pull/1684 | `colemurray/background-agents` | `code_only` | `typescript` | fix: allow bot completion event reads |
| https://github.com/ColeMurray/background-agents/pull/1673 | `colemurray/background-agents` | `code_and_docs` | `typescript` | feat: gate session and automation UI by permission |
| https://github.com/ColeMurray/background-agents/pull/1675 | `colemurray/background-agents` | `code_only` | `typescript` | feat: add workspace access administration |
| https://github.com/ColeMurray/background-agents/pull/1678 | `colemurray/background-agents` | `code_only` | `typescript` | feat: enforce automation ownership and execution authority |
| https://github.com/ColeMurray/background-agents/pull/1674 | `colemurray/background-agents` | `code_and_docs` | `typescript` | feat: enforce session authorization and revoke stale sockets |
| https://github.com/ColeMurray/background-agents/pull/1676 | `colemurray/background-agents` | `code_only` | `typescript` | feat: enforce workspace permissions at the HTTP boundary |
| https://github.com/ColeMurray/background-agents/pull/1677 | `colemurray/background-agents` | `code_only` | `typescript` | feat: add RBAC contracts, persistence, and bootstrap |
| https://github.com/ColeMurray/background-agents/pull/1597 | `colemurray/background-agents` | `code_only` | `typescript` | test: cover managed skill import BFF routes |
| https://github.com/ColeMurray/background-agents/pull/1669 | `colemurray/background-agents` | `code_only` | `typescript` | Refine settings and command composition |
| https://github.com/ColeMurray/background-agents/pull/1668 | `colemurray/background-agents` | `code_only` | `typescript` | feat(web): distinguish open details sidebar icon |
| https://github.com/ColeMurray/background-agents/pull/1667 | `colemurray/background-agents` | `code_only` | `typescript` | perf(control-plane): cache automation instruction prefixes |
| https://github.com/ColeMurray/background-agents/pull/1666 | `colemurray/background-agents` | `code_only` | `typescript` | Fix global command settings search |
| https://github.com/ColeMurray/background-agents/pull/1659 | `colemurray/background-agents` | `code_only` | `typescript` | Refine settings interaction and accessibility patterns |
| https://github.com/ColeMurray/background-agents/pull/1649 | `colemurray/background-agents` | `code_and_docs` | `typescript` | refactor: drop dead modal-infra surface and image-delete round trip |
| https://github.com/ColeMurray/background-agents/pull/1645 | `colemurray/background-agents` | `code_only` | `typescript` | Fix fatal sandbox error reporting endpoint |
| https://github.com/ColeMurray/background-agents/pull/1655 | `colemurray/background-agents` | `code_and_docs` | `typescript` | Add reusable Slack app manifest template |
| https://github.com/ColeMurray/background-agents/pull/1648 | `colemurray/background-agents` | `code_only` | `typescript` | fix(web): suppress expected sandbox access conflicts |
| https://github.com/ColeMurray/background-agents/pull/1656 | `colemurray/background-agents` | `code_only` | `typescript` | Add settings destinations to global command search |
| https://github.com/ColeMurray/background-agents/pull/1654 | `colemurray/background-agents` | `code_only` | `typescript` | Fix PR Autofix attempt limit settings |
| https://github.com/ColeMurray/background-agents/pull/1650 | `colemurray/background-agents` | `code_only` | `typescript` | Rework settings navigation and responsive layout |
| https://github.com/ColeMurray/background-agents/pull/1651 | `colemurray/background-agents` | `code_only` | `typescript` | Autofocus the home page prompt |
| https://github.com/ColeMurray/background-agents/pull/1647 | `colemurray/background-agents` | `code_only` | `typescript` | Fail sandbox pushes immediately on delivery errors |
| https://github.com/ColeMurray/background-agents/pull/1643 | `colemurray/background-agents` | `code_only` | `typescript` | refactor(control-plane): collapse image-build indirection |
| https://github.com/ColeMurray/background-agents/pull/1357 | `colemurray/background-agents` | `code_only` | `typescript` | test: cover media artifact persistence failures |
| https://github.com/ColeMurray/background-agents/pull/1639 | `colemurray/background-agents` | `code_only` | `typescript` | fix(web): surface image-build feed errors and poll while building |
| https://github.com/ColeMurray/background-agents/pull/1614 | `colemurray/background-agents` | `code_only` | `typescript` | Preserve provider preferences with versioned storage |
| https://github.com/ColeMurray/background-agents/pull/1641 | `colemurray/background-agents` | `code_only` | `typescript` | perf(web): virtualize long session timelines |
| https://github.com/ColeMurray/background-agents/pull/1640 | `colemurray/background-agents` | `code_only` | `typescript` | Clarify provider account row actions |
| https://github.com/ColeMurray/background-agents/pull/1635 | `colemurray/background-agents` | `code_only` | `typescript` | refactor(control-plane): kind-parameterize sandbox access artifacts |
| https://github.com/ColeMurray/background-agents/pull/1637 | `colemurray/background-agents` | `code_only` | `typescript` | perf: make timeline grouping linear |
| https://github.com/ColeMurray/background-agents/pull/1634 | `colemurray/background-agents` | `code_and_docs` | `typescript` | Always enable Slack message triggers |
| https://github.com/ColeMurray/background-agents/pull/1636 | `colemurray/background-agents` | `code_only` | `typescript` | Increase GitHub Autofix attempt default to 30 |
| https://github.com/ColeMurray/background-agents/pull/1633 | `colemurray/background-agents` | `code_and_docs` | `typescript` | feat: add completed workflow run automations |
| https://github.com/ColeMurray/background-agents/pull/1632 | `colemurray/background-agents` | `code_only` | `typescript` | refactor(control-plane): split init and child-summary handlers |
| https://github.com/ColeMurray/background-agents/pull/1569 | `colemurray/background-agents` | `code_only` | `typescript` | fix(types): validate unsafe settings request casts |
| https://github.com/ColeMurray/background-agents/pull/1514 | `colemurray/background-agents` | `code_only` | `typescript` | fix(types): validate stored integration settings |
| https://github.com/ColeMurray/background-agents/pull/1605 | `colemurray/background-agents` | `code_only` | `typescript` | fix(types): validate automation request bodies |
| https://github.com/ColeMurray/background-agents/pull/1502 | `colemurray/background-agents` | `code_only` | `typescript` | fix(types): validate boundary casts |
| https://github.com/ColeMurray/background-agents/pull/1544 | `colemurray/background-agents` | `code_only` | `typescript` | fix(types): replace unsafe casts with validated parsing at boundaries |
| https://github.com/ColeMurray/background-agents/pull/1531 | `colemurray/background-agents` | `code_only` | `typescript` | fix(types): validate unsafe boundary casts |
| https://github.com/ColeMurray/background-agents/pull/1419 | `colemurray/background-agents` | `code_only` | `typescript` | fix(types): validate unsafe boundary casts |
| https://github.com/ColeMurray/background-agents/pull/1462 | `colemurray/background-agents` | `code_only` | `typescript` | fix(types): validate unsafe boundary casts |
| https://github.com/ColeMurray/background-agents/pull/1520 | `colemurray/background-agents` | `code_only` | `typescript` | fix(types): replace unsafe persisted-data casts |
| https://github.com/ColeMurray/background-agents/pull/1563 | `colemurray/background-agents` | `code_only` | `typescript` | fix(types): validate unsafe web boundary casts |
| https://github.com/ColeMurray/background-agents/pull/1593 | `colemurray/background-agents` | `code_only` | `typescript` | fix(types): validate sqlite migration rows |
| https://github.com/ColeMurray/background-agents/pull/1610 | `colemurray/background-agents` | `code_only` | `typescript` | fix(types): replace unsafe casts with boundary guards |
| https://github.com/ColeMurray/background-agents/pull/1438 | `colemurray/background-agents` | `code_only` | `typescript` | fix(types): validate unsafe boundary casts |
| https://github.com/ColeMurray/background-agents/pull/1623 | `colemurray/background-agents` | `code_only` | `typescript` | fix(types): replace unsafe casts with validated parsing |
| https://github.com/ColeMurray/background-agents/pull/1408 | `colemurray/background-agents` | `code_and_docs` | `typescript` | feat(bots): let the Slack and Linear classifiers run on OpenAI, and bound the request |
| https://github.com/ColeMurray/background-agents/pull/1631 | `colemurray/background-agents` | `code_only` | `typescript` | fix: type and centralize Modal sandbox HTTP boundaries |
| https://github.com/ColeMurray/background-agents/pull/1629 | `colemurray/background-agents` | `code_only` | `typescript` | refactor(control-plane): split sandbox event processor by family |
| https://github.com/ColeMurray/background-agents/pull/1622 | `colemurray/background-agents` | `code_only` | `typescript` | fix: ignore injected OpenCode files in ESLint |
| https://github.com/ColeMurray/background-agents/pull/1625 | `colemurray/background-agents` | `code_only` | `typescript` | refactor(control-plane): remove Autofix service middle-man |
| https://github.com/ColeMurray/background-agents/pull/1626 | `colemurray/background-agents` | `code_only` | `typescript` | fix: decode image build provenance at API boundary |
| https://github.com/ColeMurray/background-agents/pull/1620 | `colemurray/background-agents` | `code_only` | `typescript` | Refactor Scheduler methods to return typed application results |
| https://github.com/ColeMurray/background-agents/pull/1624 | `colemurray/background-agents` | `code_only` | `typescript` | refactor(control-plane): make Autofix handler a class |
| https://github.com/ColeMurray/background-agents/pull/1618 | `colemurray/background-agents` | `code_only` | `typescript` | Render rich pull request tool events in the timeline |
| https://github.com/ColeMurray/background-agents/pull/1184 | `colemurray/background-agents` | `code_only` | `typescript` | Add Autofix configuration and operations |
| https://github.com/ColeMurray/background-agents/pull/1183 | `colemurray/background-agents` | `code_only` | `typescript` | Accept producer-agnostic Open Inspect reviews |
| https://github.com/ColeMurray/background-agents/pull/1182 | `colemurray/background-agents` | `code_and_docs` | `typescript` | Add human PR feedback Autofix |
| https://github.com/melgarafael/DeskcommCRM/pull/460 | `melgarafael/deskcommcrm` | `code_and_docs` | `typescript` | fix(worker): 'infinity' volta a calar o motor antigo em conversa escalada |
| https://github.com/melgarafael/DeskcommCRM/pull/457 | `melgarafael/deskcommcrm` | `code_and_docs` | `typescript` | fix(ia): o uuid que o modelo inventa deixa de virar filtro |
| https://github.com/melgarafael/DeskcommCRM/pull/449 | `melgarafael/deskcommcrm` | `code_and_docs` | `typescript` | fix(inbox): as abas perguntam quem manda, não o status da conversa |
| https://github.com/melgarafael/DeskcommCRM/pull/446 | `melgarafael/deskcommcrm` | `code_and_docs` | `typescript` | fix(opt-out): "não me mande mais boletos" bloqueava quem estava reclamando |
| https://github.com/melgarafael/DeskcommCRM/pull/430 | `melgarafael/deskcommcrm` | `code_only` | `typescript` | chore(deps): bump the minor-and-patch group with 18 updates |
| https://github.com/melgarafael/DeskcommCRM/pull/429 | `melgarafael/deskcommcrm` | `code_only` | `typescript` | chore(deps): bump actions/create-github-app-token from 2 to 3 |
| https://github.com/melgarafael/DeskcommCRM/pull/451 | `melgarafael/deskcommcrm` | `code_only_tests_or_fixtures` | `typescript` | test(e2e): a janela declarada abre mesmo — a metade que a guarda irmã não vê |
| https://github.com/melgarafael/DeskcommCRM/pull/427 | `melgarafael/deskcommcrm` | `code_only` | `typescript` | chore(deps): bump pnpm/action-setup from 4 to 6 |
| https://github.com/melgarafael/DeskcommCRM/pull/447 | `melgarafael/deskcommcrm` | `code_only_tests_or_fixtures` | `typescript` | test(e2e): a spec de automação drena até esvaziar e diz QUAL falha aconteceu |
| https://github.com/melgarafael/DeskcommCRM/pull/450 | `melgarafael/deskcommcrm` | `code_only` | `typescript` | fix(e2e): a hora do CI deixa de ser entrada escondida das specs de automação |
| https://github.com/melgarafael/DeskcommCRM/pull/444 | `melgarafael/deskcommcrm` | `code_and_docs` | `typescript` | fix(ia): o atendente de IA passa a marcar consulta de verdade |
| https://github.com/melgarafael/DeskcommCRM/pull/417 | `melgarafael/deskcommcrm` | `code_only_tests_or_fixtures` | `typescript` | chore: um .mailmap, para o crédito do contribuidor parar de sair pela metade |
| https://github.com/melgarafael/DeskcommCRM/pull/443 | `melgarafael/deskcommcrm` | `code_only_tests_or_fixtures` | `typescript` | test(e2e): a contagem do painel de segurança passa a ser derivada da lista |
| https://github.com/melgarafael/DeskcommCRM/pull/433 | `melgarafael/deskcommcrm` | `code_only` | `typescript` | fix(dx): os gates passam num clone Windows |
| https://github.com/melgarafael/DeskcommCRM/pull/442 | `melgarafael/deskcommcrm` | `code_and_docs` | `typescript` | fix(queue): o relógio do worker deixa de depender do Postgres 17 |
| https://github.com/melgarafael/DeskcommCRM/pull/440 | `melgarafael/deskcommcrm` | `code_and_docs` | `typescript` | Catraca do #432: variável vazia no .env.example não cai no default com ?? |
| https://github.com/melgarafael/DeskcommCRM/pull/441 | `melgarafael/deskcommcrm` | `code_only_tests_or_fixtures` | `typescript` | Aplica sobre o #420: alinhar o adaptador e vigiar a consulta de produção |
| https://github.com/melgarafael/DeskcommCRM/pull/420 | `melgarafael/deskcommcrm` | `code_and_docs` | `typescript` | fix(agent): agenda nunca confirma sem checar, e handoff avisa o CRM |
| https://github.com/melgarafael/DeskcommCRM/pull/432 | `melgarafael/deskcommcrm` | `code_and_docs` | `typescript` | fix(zernio): base da API vazia cai na produção do provedor |
| https://github.com/melgarafael/DeskcommCRM/pull/416 | `melgarafael/deskcommcrm` | `code_and_docs` | `typescript` | fix(opt-out): espanhol cobria só o vocabulário do #275 — as construções reais não casavam |
| https://github.com/melgarafael/DeskcommCRM/pull/438 | `melgarafael/deskcommcrm` | `code_only` | `typescript` | O escritor real do score produzia linha que o banco recusa (CRMV5W) |
| https://github.com/melgarafael/DeskcommCRM/pull/436 | `melgarafael/deskcommcrm` | `code_and_docs` | `typescript` | fix(ia): quando a IA fica calada, dá para ver por quê |
| https://github.com/melgarafael/DeskcommCRM/pull/409 | `melgarafael/deskcommcrm` | `code_and_docs` | `typescript` | fix(agenda): responsável sem disponibilidade cadastrada não é 'mal configurado' |
| https://github.com/melgarafael/DeskcommCRM/pull/390 | `melgarafael/deskcommcrm` | `code_and_docs` | `typescript` | fix(auth): a organização ativa deixa de ser sorteada |
| https://github.com/melgarafael/DeskcommCRM/pull/401 | `melgarafael/deskcommcrm` | `code_and_docs` | `typescript` | fix(agenda): o compromisso chega ao Google, e o que está lá aparece aqui |
| https://github.com/melgarafael/DeskcommCRM/pull/396 | `melgarafael/deskcommcrm` | `code_only_tests_or_fixtures` | `typescript` | .env.hostgator.example: comentário sai da linha do valor (o parser do kit o engolia) |
| https://github.com/melgarafael/DeskcommCRM/pull/388 | `melgarafael/deskcommcrm` | `code_and_docs` | `typescript` | fix(inbox): desnormaliza assigned_to_user_name, elimina N+1 no GoTrue Admin API |
| https://github.com/melgarafael/DeskcommCRM/pull/386 | `melgarafael/deskcommcrm` | `code_only` | `typescript` | fix(rls): varredura de completude para isolamento multi-tenant |
| https://github.com/melgarafael/DeskcommCRM/pull/380 | `melgarafael/deskcommcrm` | `code_only` | `typescript` | fix(worker): observabilidade de erro via Sentry no worker do agente |
| https://github.com/melgarafael/DeskcommCRM/pull/410 | `melgarafael/deskcommcrm` | `code_only_tests_or_fixtures` | `typescript` | As specs de agenda trabalhavam na semana de hoje, e hoje esvazia |
| https://github.com/melgarafael/DeskcommCRM/pull/408 | `melgarafael/deskcommcrm` | `code_and_docs` | `typescript` | fix(ia): pausar um agente passa a calá-lo em todos os caminhos |
| https://github.com/melgarafael/DeskcommCRM/pull/403 | `melgarafael/deskcommcrm` | `code_only_tests_or_fixtures` | `typescript` | Elegância E proteção: os testes derivam o namespace, e um ponto — um só — o ancora |
| https://github.com/melgarafael/DeskcommCRM/pull/402 | `melgarafael/deskcommcrm` | `code_only_tests_or_fixtures` | `typescript` | O caso de rolagem da agenda escolhia HOJE, e hoje encolhe com o relógio |
| https://github.com/melgarafael/DeskcommCRM/pull/379 | `melgarafael/deskcommcrm` | `code_only` | `typescript` | i18n(es): traduce el módulo de Agenda |
| https://github.com/melgarafael/DeskcommCRM/pull/399 | `melgarafael/deskcommcrm` | `code_and_docs` | `typescript` | Qual grafia do telefone vence deixa de ser decisão do banco (item 3 da #366) |
| https://github.com/melgarafael/DeskcommCRM/pull/385 | `melgarafael/deskcommcrm` | `code_and_docs` | `typescript` | O relógio HTTP provado contra um cron externo de verdade (item 2 da #366) |
| https://github.com/melgarafael/DeskcommCRM/pull/394 | `melgarafael/deskcommcrm` | `code_only_tests_or_fixtures` | `typescript` | A J15 sai da allowlist, porque a colisão dela foi paga |
| https://github.com/melgarafael/DeskcommCRM/pull/391 | `melgarafael/deskcommcrm` | `code_only_tests_or_fixtures` | `typescript` | test: duas jornadas não podem ter o mesmo número |
| https://github.com/melgarafael/DeskcommCRM/pull/381 | `melgarafael/deskcommcrm` | `code_only` | `typescript` | fix(auth): fecha bypass de MFA em 14 rotas administrativas |
| https://github.com/melgarafael/DeskcommCRM/pull/387 | `melgarafael/deskcommcrm` | `code_and_docs` | `typescript` | fix(agenda): a conexão do Google sempre funcionou — ninguém conseguia ver |
| https://github.com/melgarafael/DeskcommCRM/pull/389 | `melgarafael/deskcommcrm` | `code_and_docs` | `typescript` | A troca de organização terminava num beco sem saída |
| https://github.com/melgarafael/DeskcommCRM/pull/384 | `melgarafael/deskcommcrm` | `code_and_docs` | `typescript` | As duas partes do e2e rodam em paralelo, e o teto de 30 min volta a caber |
| https://github.com/melgarafael/DeskcommCRM/pull/373 | `melgarafael/deskcommcrm` | `code_only_tests_or_fixtures` | `typescript` | test(e2e): a troca de organização espera a transição, não o relógio da máquina |
| https://github.com/melgarafael/DeskcommCRM/pull/382 | `melgarafael/deskcommcrm` | `code_and_docs` | `typescript` | fix(agenda): conectar o Google nunca funcionou, o painel era cortado, e a grade virou agenda |
| https://github.com/melgarafael/DeskcommCRM/pull/369 | `melgarafael/deskcommcrm` | `code_and_docs` | `typescript` | fix(agenda): os oito defeitos que a v1.7.0 levou para produção |
| https://github.com/melgarafael/DeskcommCRM/pull/368 | `melgarafael/deskcommcrm` | `code_and_docs` | `typescript` | O interruptor de Push nascia habilitado e se desabilitava sozinho (corrida achada pelo @RagFix) |
| https://github.com/melgarafael/DeskcommCRM/pull/367 | `melgarafael/deskcommcrm` | `code_and_docs` | `typescript` | A tela de Notificações diz o que falta para o aviso chegar com a aba fechada (item 1 da #366) |
| https://github.com/melgarafael/DeskcommCRM/pull/364 | `melgarafael/deskcommcrm` | `code_and_docs` | `typescript` | A triagem só termina quando a versão sai, não no merge |
| https://github.com/melgarafael/DeskcommCRM/pull/363 | `melgarafael/deskcommcrm` | `code_and_docs` | `typescript` | A release do GitHub sai junto com a tag, sem passo manual |
| https://github.com/melgarafael/DeskcommCRM/pull/356 | `melgarafael/deskcommcrm` | `code_and_docs` | `typescript` | test(automation): pontuação nunca bloqueia criação nem encaminhamento do lead |
| https://github.com/melgarafael/DeskcommCRM/pull/359 | `melgarafael/deskcommcrm` | `code_and_docs` | `typescript` | A tag exige a assinatura do corte, não só um número novo no CHANGELOG |
| https://github.com/melgarafael/DeskcommCRM/pull/357 | `melgarafael/deskcommcrm` | `code_and_docs` | `typescript` | A versão deixa de ser escolhida e passa a ser calculada |
| https://github.com/melgarafael/DeskcommCRM/pull/130 | `melgarafael/deskcommcrm` | `code_only_tests_or_fixtures` | `typescript` | test(worker): a linha outbound do ai-response-worker cabe na constraint do banco |
| https://github.com/melgarafael/DeskcommCRM/pull/76 | `melgarafael/deskcommcrm` | `code_and_docs` | `typescript` | fix(audit): chave service role no formato novo do Supabase era lida como ausente |
| https://github.com/melgarafael/DeskcommCRM/pull/53 | `melgarafael/deskcommcrm` | `code_only` | `typescript` | fix(ci): timeline-query nao pode exigir env para ser importado — destrava a main |
| https://github.com/melgarafael/DeskcommCRM/pull/43 | `melgarafael/deskcommcrm` | `code_only` | `typescript` | feat(radar): assumir a demanda direto do Radar (alça de ação) |
| https://github.com/melgarafael/DeskcommCRM/pull/61 | `melgarafael/deskcommcrm` | `code_and_docs` | `typescript` | feat(update): atualizar o CRM pela propria tela, sem SSH |
| https://github.com/melgarafael/DeskcommCRM/pull/88 | `melgarafael/deskcommcrm` | `code_only` | `typescript` | ci(e2e): rodar em série e trazer de volta a reset-password-mfa |
| https://github.com/melgarafael/DeskcommCRM/pull/54 | `melgarafael/deskcommcrm` | `code_only` | `typescript` | build(deps): sobe zod 4, tailwind-merge 3, @hookform/resolvers 5, jest-dom 7 (consolida #47/#48/#49/#50) |
| https://github.com/melgarafael/DeskcommCRM/pull/350 | `melgarafael/deskcommcrm` | `code_and_docs` | `typescript` | fix(handoff): a IA avisa o lead ANTES de sair de campo — nos dois motores de passagem |
| https://github.com/doolijb/serene-pub/pull/116 | `doolijb/serene-pub` | `code_only` | `typescript` | Android file picker impl, drop-zone fix, auto-launch browser fix, cha… |
| https://github.com/doolijb/serene-pub/pull/111 | `doolijb/serene-pub` | `code_only` | `typescript` | Fix mobile sidebar+modal z-index, cloning seeded entries |
| https://github.com/doolijb/serene-pub/pull/110 | `doolijb/serene-pub` | `code_and_docs` | `typescript` | Develop |
| https://github.com/doolijb/serene-pub/pull/109 | `doolijb/serene-pub` | `code_and_docs` | `typescript` | Feature/0.5.1 |
| https://github.com/doolijb/serene-pub/pull/84 | `doolijb/serene-pub` | `code_only` | `typescript` | fixed the initial-start crash by ensuring a default connection is ... |
| https://github.com/doolijb/serene-pub/pull/86 | `doolijb/serene-pub` | `code_only` | `typescript` | PUBLIC_SOCKETS_ENDPOINT sets custom websockets endpoint |
| https://github.com/doolijb/serene-pub/pull/33 | `doolijb/serene-pub` | `code_and_docs` | `typescript` | Feature/fix ws binding |
| https://github.com/doolijb/serene-pub/pull/81 | `doolijb/serene-pub` | `code_and_docs` | `typescript` | build(docker): add dockerfile, along with GH Action to build it and push to ghcr |
| https://github.com/doolijb/serene-pub/pull/46 | `doolijb/serene-pub` | `code_only` | `typescript` | Fix v3, add json support |
| https://github.com/doolijb/serene-pub/pull/34 | `doolijb/serene-pub` | `code_only` | `typescript` | Feature/fix lmstudio |
| https://github.com/doolijb/serene-pub/pull/32 | `doolijb/serene-pub` | `code_only` | `typescript` | Remove current char from stop strings |
| https://github.com/doolijb/serene-pub/pull/14 | `doolijb/serene-pub` | `code_only` | `typescript` | Develop |
| https://github.com/doolijb/serene-pub/pull/13 | `doolijb/serene-pub` | `code_and_docs` | `typescript` | Develop |
| https://github.com/doolijb/serene-pub/pull/12 | `doolijb/serene-pub` | `code_and_docs` | `typescript` | Develop |
| https://github.com/doolijb/serene-pub/pull/7 | `doolijb/serene-pub` | `code_and_docs` | `typescript` | Develop |
| https://github.com/doolijb/serene-pub/pull/6 | `doolijb/serene-pub` | `code_only` | `typescript` | Chat QOL improvements |
| https://github.com/doolijb/serene-pub/pull/5 | `doolijb/serene-pub` | `code_only` | `typescript` | Fixes |
| https://github.com/doolijb/serene-pub/pull/3 | `doolijb/serene-pub` | `code_only` | `typescript` | Merge dev into main |
| https://github.com/doolijb/serene-pub/pull/2 | `doolijb/serene-pub` | `code_and_docs` | `typescript` | Merge dev into main |
| https://github.com/doolijb/serene-pub/pull/1 | `doolijb/serene-pub` | `code_and_docs` | `typescript` | Merge dev into main |
| https://github.com/KeygraphHQ/shannon/pull/431 | `keygraphhq/shannon` | `code_and_docs` | `typescript` | fix(report): emit SARIF by default for exploit runs |
| https://github.com/KeygraphHQ/shannon/pull/432 | `keygraphhq/shannon` | `code_and_docs` | `typescript` | feat: brand the npm page, CLI output, and reports |
| https://github.com/KeygraphHQ/shannon/pull/435 | `keygraphhq/shannon` | `code_only` | `typescript` | feat: bump pi harness to 0.84.2 to enable xAI subscription auth |
| https://github.com/KeygraphHQ/shannon/pull/430 | `keygraphhq/shannon` | `code_only` | `typescript` | ci: authenticate npm publishing via OIDC |
| https://github.com/KeygraphHQ/shannon/pull/429 | `keygraphhq/shannon` | `code_only` | `typescript` | fix: terminate failed scans in Temporal and surface the reason when following |
| https://github.com/KeygraphHQ/shannon/pull/427 | `keygraphhq/shannon` | `code_and_docs` | `typescript` | README update |
| https://github.com/KeygraphHQ/shannon/pull/426 | `keygraphhq/shannon` | `code_only` | `typescript` | fix(cli): align usage command column in help output |
| https://github.com/KeygraphHQ/shannon/pull/425 | `keygraphhq/shannon` | `code_only` | `typescript` | fix(cli): show splash screen on bare invocation and align usage help |
| https://github.com/KeygraphHQ/shannon/pull/424 | `keygraphhq/shannon` | `code_and_docs` | `typescript` | feat(cli): overhaul commands and add live scan status |
| https://github.com/KeygraphHQ/shannon/pull/421 | `keygraphhq/shannon` | `code_and_docs` | `typescript` | feat: generate the final report in PDF format |
| https://github.com/KeygraphHQ/shannon/pull/419 | `keygraphhq/shannon` | `code_and_docs` | `typescript` | feat(cli): reuse host Codex subscription auth for pentest runs |
| https://github.com/KeygraphHQ/shannon/pull/413 | `keygraphhq/shannon` | `code_only` | `typescript` | feat(worker): record severity in analysis mode and fix prompt substitutions |
| https://github.com/KeygraphHQ/shannon/pull/415 | `keygraphhq/shannon` | `code_and_docs` | `typescript` | feat(cli): support any Pi provider via generic SHANNON_AI_API_KEY |
| https://github.com/KeygraphHQ/shannon/pull/377 | `keygraphhq/shannon` | `code_only` | `typescript` | fix: render agent deliverables before the success commit so resume preserves them |
| https://github.com/KeygraphHQ/shannon/pull/402 | `keygraphhq/shannon` | `code_and_docs` | `typescript` | feat: multi-provider model support, SARIF output, and exploit-mode fixes |
| https://github.com/KeygraphHQ/shannon/pull/403 | `keygraphhq/shannon` | `code_and_docs` | `typescript` | docs: sync provider options across bug report, README, and env example |
| https://github.com/KeygraphHQ/shannon/pull/388 | `keygraphhq/shannon` | `code_only` | `typescript` | refactor(worker): converge shared core with shannon-oss |
| https://github.com/KeygraphHQ/shannon/pull/383 | `keygraphhq/shannon` | `code_and_docs` | `typescript` | feat(cli): restructure run folder and improve terminal UX |
| https://github.com/KeygraphHQ/shannon/pull/384 | `keygraphhq/shannon` | `code_and_docs` | `typescript` | feat(cli): restructure run folder and improve terminal UX |
| https://github.com/KeygraphHQ/shannon/pull/371 | `keygraphhq/shannon` | `code_only` | `typescript` | feat(preflight): support multi-repo targets by removing .git check |
| https://github.com/KeygraphHQ/shannon/pull/375 | `keygraphhq/shannon` | `code_and_docs` | `typescript` | docs: rename shn command references to npx @keygraph/shannon |
| https://github.com/KeygraphHQ/shannon/pull/376 | `keygraphhq/shannon` | `code_only` | `typescript` | fix: render agent deliverables before the success commit so resume preserves them |
| https://github.com/KeygraphHQ/shannon/pull/356 | `keygraphhq/shannon` | `code_only` | `typescript` | ci: bump the beta release line to 2.0.0 |
| https://github.com/KeygraphHQ/shannon/pull/354 | `keygraphhq/shannon` | `code_and_docs` | `typescript` | feat(ai): support Claude Fable 5 (upgrade Claude Agent SDK to 0.3.173) |
| https://github.com/KeygraphHQ/shannon/pull/353 | `keygraphhq/shannon` | `code_and_docs` | `typescript` | feat(ai): upgrade to Opus 4.8 and Claude Agent SDK 0.3.163 |
| https://github.com/KeygraphHQ/shannon/pull/350 | `keygraphhq/shannon` | `code_only` | `typescript` | feat(worker): structure intermediate deliverables via MCP collectors |
| https://github.com/KeygraphHQ/shannon/pull/346 | `keygraphhq/shannon` | `code_and_docs` | `typescript` | feat(docker): forward /etc/hosts entries to worker containers |
| https://github.com/KeygraphHQ/shannon/pull/344 | `keygraphhq/shannon` | `code_only` | `typescript` | fix(deps): bump fast-uri to 3.1.2 (CVE-2026-6321) |
| https://github.com/KeygraphHQ/shannon/pull/338 | `keygraphhq/shannon` | `code_only` | `typescript` | fix(docker): pin --ignore-scripts on global npm installs |
| https://github.com/KeygraphHQ/shannon/pull/337 | `keygraphhq/shannon` | `code_only` | `typescript` | feat(preflight): block cloud metadata range in target URL check |
| https://github.com/KeygraphHQ/shannon/pull/335 | `keygraphhq/shannon` | `code_and_docs` | `typescript` | feat(auth): auth-validation preflight + email_login credentials |
| https://github.com/KeygraphHQ/shannon/pull/345 | `keygraphhq/shannon` | `code_and_docs` | `typescript` | feat: share preflight authenticated session across agents |
| https://github.com/KeygraphHQ/shannon/pull/299 | `keygraphhq/shannon` | `code_and_docs` | `typescript` | fix(cli): surface docker errors and add --debug flag for worker logs |
| https://github.com/KeygraphHQ/shannon/pull/329 | `keygraphhq/shannon` | `code_only` | `typescript` | feat(ai): steer notes field for analysis-only mode |
| https://github.com/KeygraphHQ/shannon/pull/328 | `keygraphhq/shannon` | `code_only` | `typescript` | feat(scripts): add --help to save-deliverable and generate-totp |
| https://github.com/KeygraphHQ/shannon/pull/327 | `keygraphhq/shannon` | `code_and_docs` | `typescript` | chore: remove unused scan tools and dead error type |
| https://github.com/KeygraphHQ/shannon/pull/326 | `keygraphhq/shannon` | `code_and_docs` | `typescript` | feat: add config-driven run scoping and report filtering |
| https://github.com/KeygraphHQ/shannon/pull/323 | `keygraphhq/shannon` | `code_only` | `typescript` | feat(cli): block running shannon with sudo or as root |
| https://github.com/KeygraphHQ/shannon/pull/325 | `keygraphhq/shannon` | `code_and_docs` | `typescript` | feat(ai): upgrade to Opus 4.7 with adaptive thinking |
| https://github.com/KeygraphHQ/shannon/pull/314 | `keygraphhq/shannon` | `code_only` | `typescript` | fix(deps): bump protobufjs to 7.5.5 to patch CVE-2026-41242 |
| https://github.com/KeygraphHQ/shannon/pull/295 | `keygraphhq/shannon` | `code_and_docs` | `typescript` | feat: provider extensions and drop claude-code-router mode |
| https://github.com/KeygraphHQ/shannon/pull/282 | `keygraphhq/shannon` | `code_only` | `typescript` | feat: extract pipeline core for library consumption |
| https://github.com/KeygraphHQ/shannon/pull/274 | `keygraphhq/shannon` | `code_only` | `typescript` | fix: pre-recon deliverable filename mismatch |
| https://github.com/KeygraphHQ/shannon/pull/273 | `keygraphhq/shannon` | `code_only` | `typescript` | feat: mount user repo as read-only with writable shannon overlay |
| https://github.com/KeygraphHQ/shannon/pull/267 | `keygraphhq/shannon` | `code_only` | `typescript` | feat: use structured outputs for vuln agent exploitation queues |
| https://github.com/KeygraphHQ/shannon/pull/266 | `keygraphhq/shannon` | `code_and_docs` | `typescript` | chore: enforce pnpm minimum release age and upgrade to v10.33.0 |
| https://github.com/KeygraphHQ/shannon/pull/255 | `keygraphhq/shannon` | `code_only` | `typescript` | fix: harden supply chain security |
| https://github.com/KeygraphHQ/shannon/pull/265 | `keygraphhq/shannon` | `code_only` | `typescript` | chore: update issue templates |
| https://github.com/KeygraphHQ/shannon/pull/254 | `keygraphhq/shannon` | `code_only` | `typescript` | feat: add target URL reachability preflight check |
| https://github.com/KeygraphHQ/shannon/pull/247 | `keygraphhq/shannon` | `code_only` | `typescript` | feat: add beta release and rollback workflows |
| https://github.com/KeygraphHQ/shannon/pull/246 | `keygraphhq/shannon` | `code_and_docs` | `typescript` | feat: add custom base URL support for LiteLLM and compatible proxies |
| https://github.com/KeygraphHQ/shannon/pull/252 | `keygraphhq/shannon` | `code_and_docs` | `typescript` | feat: migrate from MCP tools to CLI based tools |
| https://github.com/KeygraphHQ/shannon/pull/141 | `keygraphhq/shannon` | `code_and_docs` | `typescript` | refactor: decompose activities into services layer with structured error handling |
| https://github.com/KeygraphHQ/shannon/pull/149 | `keygraphhq/shannon` | `code_only` | `typescript` | feat: add preflight validation phase with structured error reporting |
| https://github.com/KeygraphHQ/shannon/pull/177 | `keygraphhq/shannon` | `code_and_docs` | `typescript` | feat: add three-tier model system with Bedrock and Vertex AI support |
| https://github.com/KeygraphHQ/shannon/pull/224 | `keygraphhq/shannon` | `code_and_docs` | `typescript` | Hardening local defaults |
| https://github.com/KeygraphHQ/shannon/pull/161 | `keygraphhq/shannon` | `code_and_docs` | `typescript` | feat: add configurable pipeline retry and concurrency settings |
| https://github.com/KeygraphHQ/shannon/pull/152 | `keygraphhq/shannon` | `code_only` | `typescript` | fix: pass router env vars to SDK subprocess |
| https://github.com/KeygraphHQ/shannon/pull/140 | `keygraphhq/shannon` | `code_and_docs` | `typescript` | feat: add named workspaces with resume support |
| https://github.com/KeygraphHQ/shannon/pull/139 | `keygraphhq/shannon` | `code_and_docs` | `typescript` | feat: add MSYS path fix, Claude Code CLI, and Windows instructions |

## Reject Summary Sample

| Repository | PR | Reason | Bucket |
| --- | ---: | --- | --- |
| `eleutherai/lm-evaluation-harness` | `4061` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `4066` | `docs_only_excluded` | `docs_only` |
| `eleutherai/lm-evaluation-harness` | `359` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `4032` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `2946` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `3836` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `3008` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `3594` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `2977` | `docs_only_excluded` | `docs_only` |
| `eleutherai/lm-evaluation-harness` | `2476` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `3837` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `3660` | `docs_only_excluded` | `docs_only` |
| `eleutherai/lm-evaluation-harness` | `4025` | `docs_only_excluded` | `docs_only` |
| `eleutherai/lm-evaluation-harness` | `3648` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `3760` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `3857` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `4010` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `4026` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `2792` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `3144` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `3792` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `3816` | `too_many_changed_files` | `code_and_docs` |
| `eleutherai/lm-evaluation-harness` | `3932` | `not_merged` | `None` |
| `jestjs/jest` | `15965` | `not_merged` | `None` |
| `jestjs/jest` | `16405` | `not_merged` | `None` |
| `jestjs/jest` | `16339` | `not_merged` | `None` |
| `jestjs/jest` | `16020` | `not_merged` | `None` |
| `jestjs/jest` | `16395` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `jestjs/jest` | `16207` | `not_merged` | `None` |
| `jestjs/jest` | `16154` | `docs_only_excluded` | `docs_only` |
| `jestjs/jest` | `16156` | `not_merged` | `None` |
| `jestjs/jest` | `16335` | `not_merged` | `None` |
| `jestjs/jest` | `16328` | `not_merged` | `None` |
| `jestjs/jest` | `16357` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `jestjs/jest` | `16002` | `not_merged` | `None` |
| `jestjs/jest` | `16283` | `not_merged` | `None` |
| `jestjs/jest` | `16356` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `jestjs/jest` | `16350` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `jestjs/jest` | `16282` | `not_merged` | `None` |
| `jestjs/jest` | `16271` | `not_merged` | `None` |
| `jestjs/jest` | `16337` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `jestjs/jest` | `16292` | `docs_only_excluded` | `docs_only` |
| `astral-sh/ty` | `4384` | `docs_only_excluded` | `docs_only` |
| `astral-sh/ty` | `4382` | `docs_only_excluded` | `docs_only` |
| `astral-sh/ty` | `4165` | `docs_only_excluded` | `docs_only` |
| `astral-sh/ty` | `4316` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `astral-sh/ty` | `4312` | `not_merged` | `None` |
| `astral-sh/ty` | `4282` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `astral-sh/ty` | `4266` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `astral-sh/ty` | `4239` | `docs_only_excluded` | `docs_only` |
| `astral-sh/ty` | `4237` | `not_merged` | `None` |
| `astral-sh/ty` | `4211` | `docs_only_excluded` | `docs_only` |
| `astral-sh/ty` | `4198` | `docs_only_excluded` | `docs_only` |
| `astral-sh/ty` | `4154` | `not_merged` | `None` |
| `astral-sh/ty` | `4112` | `docs_only_excluded` | `docs_only` |
| `astral-sh/ty` | `4038` | `docs_only_excluded` | `docs_only` |
| `astral-sh/ty` | `4028` | `docs_only_excluded` | `docs_only` |
| `rossoctl/rossoctl` | `2481` | `docs_only_excluded` | `docs_only` |
| `rossoctl/rossoctl` | `2480` | `not_merged` | `None` |
| `rossoctl/rossoctl` | `2479` | `docs_only_excluded` | `docs_only` |
| `rossoctl/rossoctl` | `2459` | `not_merged` | `None` |
| `rossoctl/rossoctl` | `2464` | `docs_only_excluded` | `docs_only` |
| `rossoctl/rossoctl` | `2465` | `docs_only_excluded` | `docs_only` |
| `rossoctl/rossoctl` | `2462` | `docs_only_excluded` | `docs_only` |
| `rossoctl/rossoctl` | `2402` | `docs_only_excluded` | `docs_only` |
| `rossoctl/rossoctl` | `2450` | `docs_only_excluded` | `docs_only` |
| `rossoctl/rossoctl` | `2396` | `docs_only_excluded` | `docs_only` |
| `rossoctl/rossoctl` | `2139` | `docs_only_excluded` | `docs_only` |
| `rossoctl/rossoctl` | `2249` | `docs_only_excluded` | `docs_only` |
| `rossoctl/rossoctl` | `2336` | `not_merged` | `None` |
| `rossoctl/rossoctl` | `2355` | `not_merged` | `None` |
| `rossoctl/rossoctl` | `2370` | `not_merged` | `None` |
| `rossoctl/rossoctl` | `2356` | `not_merged` | `None` |
| `rossoctl/rossoctl` | `970` | `docs_only_excluded` | `docs_only` |
| `rossoctl/rossoctl` | `967` | `docs_only_excluded` | `docs_only` |
| `rossoctl/rossoctl` | `2320` | `docs_only_excluded` | `docs_only` |
| `rossoctl/rossoctl` | `2154` | `docs_only_excluded` | `docs_only` |
| `rossoctl/rossoctl` | `2279` | `docs_only_excluded` | `docs_only` |
| `rossoctl/rossoctl` | `2329` | `docs_only_excluded` | `docs_only` |
| `rossoctl/rossoctl` | `2366` | `docs_only_excluded` | `docs_only` |
| `rossoctl/rossoctl` | `2353` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `rossoctl/rossoctl` | `2349` | `docs_only_excluded` | `docs_only` |
| `rossoctl/rossoctl` | `2272` | `not_merged` | `None` |
| `rossoctl/rossoctl` | `2337` | `not_merged` | `None` |
| `rossoctl/rossoctl` | `2351` | `not_merged` | `None` |
| `rossoctl/rossoctl` | `2234` | `not_merged` | `None` |
| `rossoctl/rossoctl` | `2332` | `docs_only_excluded` | `docs_only` |
| `rossoctl/rossoctl` | `2315` | `not_merged` | `None` |
| `rossoctl/rossoctl` | `2341` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `rossoctl/rossoctl` | `2340` | `not_merged` | `None` |
| `rossoctl/rossoctl` | `2270` | `not_merged` | `None` |
| `rossoctl/rossoctl` | `2286` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `rossoctl/rossoctl` | `2324` | `docs_only_excluded` | `docs_only` |
| `rossoctl/rossoctl` | `2299` | `docs_only_excluded` | `docs_only` |
| `rossoctl/rossoctl` | `2328` | `not_merged` | `None` |
| `rossoctl/rossoctl` | `2319` | `docs_only_excluded` | `docs_only` |
| `rossoctl/rossoctl` | `2326` | `docs_only_excluded` | `docs_only` |
| `rossoctl/rossoctl` | `2325` | `docs_only_excluded` | `docs_only` |
| `rossoctl/rossoctl` | `2321` | `docs_only_excluded` | `docs_only` |
| `rossoctl/rossoctl` | `2318` | `docs_only_excluded` | `docs_only` |
| `rossoctl/rossoctl` | `1711` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `rossoctl/rossoctl` | `1303` | `docs_only_excluded` | `docs_only` |
| `rossoctl/rossoctl` | `2193` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `rossoctl/rossoctl` | `2290` | `not_merged` | `None` |
| `rossoctl/rossoctl` | `2311` | `not_merged` | `None` |
| `rossoctl/rossoctl` | `2317` | `docs_only_excluded` | `docs_only` |
| `rossoctl/rossoctl` | `2289` | `docs_only_excluded` | `docs_only` |
| `rossoctl/rossoctl` | `2294` | `docs_only_excluded` | `docs_only` |
| `rossoctl/rossoctl` | `2295` | `docs_only_excluded` | `docs_only` |
| `rossoctl/rossoctl` | `2226` | `not_merged` | `None` |
| `rossoctl/rossoctl` | `2301` | `docs_only_excluded` | `docs_only` |
| `rossoctl/rossoctl` | `2309` | `not_merged` | `None` |
| `rossoctl/rossoctl` | `2314` | `docs_only_excluded` | `docs_only` |
| `rossoctl/rossoctl` | `2310` | `not_merged` | `None` |
| `rossoctl/rossoctl` | `2300` | `docs_only_excluded` | `docs_only` |
| `rossoctl/rossoctl` | `2287` | `docs_only_excluded` | `docs_only` |
| `rossoctl/rossoctl` | `2269` | `docs_only_excluded` | `docs_only` |
| `rossoctl/rossoctl` | `2252` | `docs_only_excluded` | `docs_only` |
| `rossoctl/rossoctl` | `2242` | `not_merged` | `None` |
| `rossoctl/rossoctl` | `2241` | `not_merged` | `None` |
| `rossoctl/rossoctl` | `2238` | `not_merged` | `None` |
| `rossoctl/rossoctl` | `2253` | `too_many_changed_files` | `docs_only` |
| `rossoctl/rossoctl` | `2250` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `rossoctl/rossoctl` | `2248` | `not_merged` | `None` |
| `rossoctl/rossoctl` | `2232` | `docs_only_excluded` | `docs_only` |
| `rossoctl/rossoctl` | `2223` | `docs_only_excluded` | `docs_only` |
| `marshmallow-code/marshmallow` | `3035` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `3033` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `3029` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `3028` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `3020` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `3025` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `3021` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `3023` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `3022` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `3017` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `3007` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `3013` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `3014` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `3012` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `marshmallow-code/marshmallow` | `3010` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `3009` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `3008` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `2992` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `3003` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `3006` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `3002` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `3001` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `2997` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `2996` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `2995` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `2991` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `marshmallow-code/marshmallow` | `2986` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `2984` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `marshmallow-code/marshmallow` | `1003` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `2980` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `marshmallow-code/marshmallow` | `2979` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `2977` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `marshmallow-code/marshmallow` | `2976` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `2975` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `2971` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `2970` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `marshmallow-code/marshmallow` | `2969` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `2968` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `marshmallow-code/marshmallow` | `2967` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `2966` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `marshmallow-code/marshmallow` | `2964` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `marshmallow-code/marshmallow` | `2959` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `marshmallow-code/marshmallow` | `2958` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `2957` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `2956` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `marshmallow-code/marshmallow` | `2955` | `docs_only_excluded` | `docs_only` |
| `marshmallow-code/marshmallow` | `2954` | `docs_only_excluded` | `docs_only` |
| `marshmallow-code/marshmallow` | `2951` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `2943` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `2946` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `2945` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `2944` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `2941` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `2938` | `docs_only_excluded` | `docs_only` |
| `marshmallow-code/marshmallow` | `2934` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `2933` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `2927` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `2931` | `docs_only_excluded` | `docs_only` |
| `marshmallow-code/marshmallow` | `2888` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `2852` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `2910` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `2923` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `2922` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `2920` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `2918` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `2917` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `2916` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `2908` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `2905` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `2898` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `2895` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `2886` | `docs_only_excluded` | `docs_only` |
| `marshmallow-code/marshmallow` | `2882` | `not_merged` | `None` |
| `marshmallow-code/marshmallow` | `2881` | `docs_only_excluded` | `docs_only` |