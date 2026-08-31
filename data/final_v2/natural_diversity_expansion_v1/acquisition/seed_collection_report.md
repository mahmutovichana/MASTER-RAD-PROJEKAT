# DocGuard Real PR Seed Collector Report

This report summarizes neutral repo-based sampling of merged public GitHub PRs.

The collector does not assign gold labels and does not decide whether documentation should be updated.
It only creates seed PR URLs for the later candidate builder and manual validation workflow.

- Repositories scanned: `20`
- Seeds accepted: `1200`
- Rejected/skipped PRs: `815`
- Acquisition status: `complete`
- Requirements satisfied: `True`
- Target observed/requested: `1200` / `1200`
- Target deficit: `0`
- Minimum language deficits: `{}`
- Collector bucket counts: `{'code_and_docs': 429, 'code_only': 713, 'code_only_tests_or_fixtures': 58}`
- Language hint counts: `{'python': 727, 'typescript': 473}`
- Repository counts per language: `{'python': 10, 'typescript': 7}`
- Candidate bucket counts per language: `{'python': {'code_and_docs': 214, 'code_only': 468, 'code_only_tests_or_fixtures': 45}, 'typescript': {'code_and_docs': 215, 'code_only': 245, 'code_only_tests_or_fixtures': 13}}`
- Reject reason counts: `{'docs_only_excluded': 226, 'not_merged': 428, 'other_or_binary_only_excluded': 140, 'too_many_changed_files': 20, 'fetch_pr_files_failed': 1}`

## Methodological Boundary

- This is real public GitHub PR sampling.
- No synthetic examples are generated.
- No final labels are assigned here.
- `collector_bucket` is audit metadata for balancing and review planning, not a model label.
- Final evaluation must use only the safe fields produced later by the candidate builder.

## Accepted Seeds

| PR | Repository | Bucket | Language hint | Title |
| --- | --- | --- | --- | --- |
| https://github.com/schmitech/orbit/pull/288 | `schmitech/orbit` | `code_and_docs` | `python` | feat: add privacy_filter moderation provider for local PII detection |
| https://github.com/schmitech/orbit/pull/271 | `schmitech/orbit` | `code_only` | `python` | Exclude unmatched routes from dashboard latency |
| https://github.com/schmitech/orbit/pull/174 | `schmitech/orbit` | `code_only` | `python` | Add claude GitHub actions 1778072624576 |
| https://github.com/schmitech/orbit/pull/227 | `schmitech/orbit` | `code_only` | `python` | fix: prevent model list truncation when intro is short |
| https://github.com/schmitech/orbit/pull/187 | `schmitech/orbit` | `code_only` | `python` | Add NEAR AI Cloud inference provider |
| https://github.com/schmitech/orbit/pull/148 | `schmitech/orbit` | `code_only` | `python` | Fix #146: audit logs: conversation thread compression |
| https://github.com/schmitech/orbit/pull/72 | `schmitech/orbit` | `code_only` | `python` | renamed background color |
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
| https://github.com/jestjs/jest/pull/16336 | `jestjs/jest` | `code_and_docs` | `typescript` | feat(jest-runtime): resolve the `module-sync` export condition |
| https://github.com/jestjs/jest/pull/16331 | `jestjs/jest` | `code_and_docs` | `typescript` | fix(@jest/transform): key transform caches on the caller support flags |
| https://github.com/jestjs/jest/pull/16330 | `jestjs/jest` | `code_and_docs` | `typescript` | fix: keep source maps past teardown |
| https://github.com/jestjs/jest/pull/16327 | `jestjs/jest` | `code_and_docs` | `typescript` | feat(@jest/source-map): replace `source-map-support` with a Jest-owned implementation |
| https://github.com/jestjs/jest/pull/16326 | `jestjs/jest` | `code_and_docs` | `typescript` | fix: detect Jest's own stack frames without assuming a directory name |
| https://github.com/jestjs/jest/pull/16325 | `jestjs/jest` | `code_only` | `typescript` | chore: handle nightly Node version in test assertion |
| https://github.com/jestjs/jest/pull/16324 | `jestjs/jest` | `code_and_docs` | `typescript` | fix: stop resolving lazy globals when setting up an environment |
| https://github.com/jestjs/jest/pull/16323 | `jestjs/jest` | `code_and_docs` | `typescript` | fix: only warn about a conflicting `globalsCleanup` mode when one was set |
| https://github.com/jestjs/jest/pull/16313 | `jestjs/jest` | `code_only` | `typescript` | chore(deps): update dependency eslint-plugin-jsdoc to v64 |
| https://github.com/jestjs/jest/pull/16321 | `jestjs/jest` | `code_and_docs` | `typescript` | ci: run the test matrix on Node 26 |
| https://github.com/jestjs/jest/pull/16320 | `jestjs/jest` | `code_only` | `typescript` | test: match Node prereleases in version gates |
| https://github.com/jestjs/jest/pull/16319 | `jestjs/jest` | `code_only` | `typescript` | ci: exercise watchman on Node LTS |
| https://github.com/jestjs/jest/pull/16318 | `jestjs/jest` | `code_and_docs` | `typescript` | chore: update react-native example |
| https://github.com/jestjs/jest/pull/16049 | `jestjs/jest` | `code_and_docs` | `typescript` | Update istanbul dependencies |
| https://github.com/jestjs/jest/pull/16273 | `jestjs/jest` | `code_and_docs` | `typescript` | fix: use --config for global config with multiple --projects |
| https://github.com/jestjs/jest/pull/16277 | `jestjs/jest` | `code_and_docs` | `typescript` | fix(cjs-esm-interop): support `module.exports` in ESM |
| https://github.com/jestjs/jest/pull/16295 | `jestjs/jest` | `code_and_docs` | `typescript` | fix(jest-haste-map): tolerate transient EPERM in the watcher lstat |
| https://github.com/jestjs/jest/pull/16224 | `jestjs/jest` | `code_and_docs` | `typescript` | fix(jest-config): add missing options to ValidConfig to prevent spurious warnings |
| https://github.com/jestjs/jest/pull/16314 | `jestjs/jest` | `code_only` | `typescript` | chore: set renovate minimum age |
| https://github.com/jestjs/jest/pull/16211 | `jestjs/jest` | `code_only_tests_or_fixtures` | `typescript` | test: cover asymmetric matcher failures with worker threads |
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
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3847 | `eleutherai/lm-evaluation-harness` | `code_only_tests_or_fixtures` | `python` | Fix broken afrobench group task references (afrisenti/mafand prompt_2) |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3950 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | fix(tmmluplus): use ikala/tmmluplus so the task loads on datasets>=4 |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3943 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | fix(tasks): use script-less parquet mirrors for mathqa, siqa, and moral_stories |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3975 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | fix(scrolls): load SCROLLS without the removed dataset script |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3976 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | fix(arithmetic): load arithmetic tasks without the removed dataset script |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3942 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | fix(tasks): use namespaced dataset paths for webqs, medmcqa, and wmt16 |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3946 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | fix(tasks): use namespaced dataset path for wsc273 |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3980 | `eleutherai/lm-evaluation-harness` | `code_only_tests_or_fixtures` | `python` | fix(tests): pass dataset_kwargs in test_download |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3982 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | fix(spanish_bench): load wnli_es without the removed dataset script |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3977 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | fix(prost): load PROST without the removed dataset script |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3812 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | feat(portuguese_bench): add ASSIN2 RTE and STS tasks |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3826 | `eleutherai/lm-evaluation-harness` | `code_and_docs` | `python` | Add IndicParam: MCQ benchmark for 12 low-resource Indic languages |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3870 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | Fix dataset paths for xnli, xcopa, paws-x, and xquad |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/1961 | `eleutherai/lm-evaluation-harness` | `code_and_docs` | `python` | Mmlu Pro |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3842 | `eleutherai/lm-evaluation-harness` | `code_and_docs` | `python` | fix(kormedmcqa): extract answer choice per paper Appendix B |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3848 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | Fix space in North Macedonian task identifiers (INCLUDE suite) |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3860 | `eleutherai/lm-evaluation-harness` | `code_and_docs` | `python` | feat(legalbench): add HELM-lite LegalBench subset (5 tasks) |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3817 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | fix sglang args |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3803 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | fix(vllm): warn when device argument is ignored |
| https://github.com/EleutherAI/lm-evaluation-harness/pull/3822 | `eleutherai/lm-evaluation-harness` | `code_only` | `python` | fix: keep Anthropic stop sequences nonempty |
| https://github.com/kdeldycke/click-extra/pull/1918 | `kdeldycke/click-extra` | `code_only_tests_or_fixtures` | `python` | Format Python |
| https://github.com/kdeldycke/click-extra/pull/1721 | `kdeldycke/click-extra` | `code_and_docs` | `python` | Release `v7.17.2` |
| https://github.com/kdeldycke/click-extra/pull/1720 | `kdeldycke/click-extra` | `code_and_docs` | `python` | Bump minor version to `v7.18.0` |
| https://github.com/kdeldycke/click-extra/pull/1727 | `kdeldycke/click-extra` | `code_only` | `python` | Sync `uv.lock` |
| https://github.com/kdeldycke/click-extra/pull/1728 | `kdeldycke/click-extra` | `code_only` | `python` | Typo |
| https://github.com/kdeldycke/click-extra/pull/1729 | `kdeldycke/click-extra` | `code_and_docs` | `python` | Typo |
| https://github.com/kdeldycke/click-extra/pull/1724 | `kdeldycke/click-extra` | `code_and_docs` | `python` | Release `v7.18.0` |
| https://github.com/kdeldycke/click-extra/pull/1913 | `kdeldycke/click-extra` | `code_and_docs` | `python` | [changelog] Bump minor version to `v9.1.0` |
| https://github.com/kdeldycke/click-extra/pull/1886 | `kdeldycke/click-extra` | `code_and_docs` | `python` | Release `v9.0.0` |
| https://github.com/kdeldycke/click-extra/pull/1909 | `kdeldycke/click-extra` | `code_only` | `python` | Sync repomatic-managed files |
| https://github.com/kdeldycke/click-extra/pull/1893 | `kdeldycke/click-extra` | `code_only_tests_or_fixtures` | `python` | Typo |
| https://github.com/kdeldycke/click-extra/pull/1906 | `kdeldycke/click-extra` | `code_only` | `python` | Format `pyproject.toml` |
| https://github.com/kdeldycke/click-extra/pull/1899 | `kdeldycke/click-extra` | `code_only_tests_or_fixtures` | `python` | Sync action pins |
| https://github.com/kdeldycke/click-extra/pull/1901 | `kdeldycke/click-extra` | `code_only_tests_or_fixtures` | `python` | Sync workflow pins |
| https://github.com/kdeldycke/click-extra/pull/1706 | `kdeldycke/click-extra` | `code_and_docs` | `python` | Release `v7.17.0` |
| https://github.com/kdeldycke/click-extra/pull/1717 | `kdeldycke/click-extra` | `code_and_docs` | `python` | Release `v7.17.1` |
| https://github.com/kdeldycke/click-extra/pull/1686 | `kdeldycke/click-extra` | `code_and_docs` | `python` | Release `v7.16.0` |
| https://github.com/kdeldycke/click-extra/pull/1703 | `kdeldycke/click-extra` | `code_and_docs` | `python` | Release `v7.16.1` |
| https://github.com/kdeldycke/click-extra/pull/1889 | `kdeldycke/click-extra` | `code_only` | `python` | Typo |
| https://github.com/kdeldycke/click-extra/pull/1775 | `kdeldycke/click-extra` | `code_and_docs` | `python` | [changelog] Bump major version to `v9.0.0` |
| https://github.com/kdeldycke/click-extra/pull/1888 | `kdeldycke/click-extra` | `code_only_tests_or_fixtures` | `python` | Format Python |
| https://github.com/kdeldycke/click-extra/pull/1883 | `kdeldycke/click-extra` | `code_and_docs` | `python` | [changelog] Bump minor version to `v8.10.0` |
| https://github.com/kdeldycke/click-extra/pull/1881 | `kdeldycke/click-extra` | `code_and_docs` | `python` | Release `v8.9.1` |
| https://github.com/kdeldycke/click-extra/pull/1885 | `kdeldycke/click-extra` | `code_only_tests_or_fixtures` | `python` | Sync workflow pins |
| https://github.com/kdeldycke/click-extra/pull/1873 | `kdeldycke/click-extra` | `code_and_docs` | `python` | Release `v8.9.0` |
| https://github.com/kdeldycke/click-extra/pull/1880 | `kdeldycke/click-extra` | `code_only_tests_or_fixtures` | `python` | Sync workflow pins |
| https://github.com/kdeldycke/click-extra/pull/1879 | `kdeldycke/click-extra` | `code_only` | `python` | Format `pyproject.toml` |
| https://github.com/kdeldycke/click-extra/pull/1878 | `kdeldycke/click-extra` | `code_only` | `python` | Format Python |
| https://github.com/kdeldycke/click-extra/pull/1868 | `kdeldycke/click-extra` | `code_and_docs` | `python` | Bump minor version to `v8.9.0` |
| https://github.com/kdeldycke/click-extra/pull/1875 | `kdeldycke/click-extra` | `code_only` | `python` | Sync `uv.lock` |
| https://github.com/kdeldycke/click-extra/pull/1689 | `kdeldycke/click-extra` | `code_and_docs` | `python` | Bump minor version to `v7.16.0` |
| https://github.com/kdeldycke/click-extra/pull/1688 | `kdeldycke/click-extra` | `code_only` | `python` | Format Python |
| https://github.com/kdeldycke/click-extra/pull/1673 | `kdeldycke/click-extra` | `code_and_docs` | `python` | Bump minor version to `v7.15.0` |
| https://github.com/kdeldycke/click-extra/pull/1677 | `kdeldycke/click-extra` | `code_and_docs` | `python` | Format Python |
| https://github.com/kdeldycke/click-extra/pull/1683 | `kdeldycke/click-extra` | `code_only` | `python` | Sync `uv.lock` |
| https://github.com/kdeldycke/click-extra/pull/1680 | `kdeldycke/click-extra` | `code_only` | `python` | Format Python |
| https://github.com/kdeldycke/click-extra/pull/1674 | `kdeldycke/click-extra` | `code_and_docs` | `python` | Release `v7.15.0` |
| https://github.com/kdeldycke/click-extra/pull/1867 | `kdeldycke/click-extra` | `code_and_docs` | `python` | Release `v8.8.1` |
| https://github.com/kdeldycke/click-extra/pull/1870 | `kdeldycke/click-extra` | `code_only` | `python` | Sync `uv.lock` |
| https://github.com/kdeldycke/click-extra/pull/1865 | `kdeldycke/click-extra` | `code_only` | `python` | Typo |
| https://github.com/kdeldycke/click-extra/pull/1871 | `kdeldycke/click-extra` | `code_only_tests_or_fixtures` | `python` | Sync workflow pins |
| https://github.com/kdeldycke/click-extra/pull/1862 | `kdeldycke/click-extra` | `code_and_docs` | `python` | Release `v8.8.0` |
| https://github.com/kdeldycke/click-extra/pull/1864 | `kdeldycke/click-extra` | `code_and_docs` | `python` | Bump minor version to `v8.8.0` |
| https://github.com/kdeldycke/click-extra/pull/1858 | `kdeldycke/click-extra` | `code_and_docs` | `python` | Release `v8.7.0` |
| https://github.com/kdeldycke/click-extra/pull/1861 | `kdeldycke/click-extra` | `code_only` | `python` | Format Python |
| https://github.com/kdeldycke/click-extra/pull/1844 | `kdeldycke/click-extra` | `code_and_docs` | `python` | Bump minor version to `v8.7.0` |
| https://github.com/kdeldycke/click-extra/pull/1852 | `kdeldycke/click-extra` | `code_and_docs` | `python` | Release `v8.6.3` |
| https://github.com/kdeldycke/click-extra/pull/1857 | `kdeldycke/click-extra` | `code_only_tests_or_fixtures` | `python` | Sync workflow pins |
| https://github.com/kdeldycke/click-extra/pull/1855 | `kdeldycke/click-extra` | `code_only_tests_or_fixtures` | `python` | Sync action pins |
| https://github.com/kdeldycke/click-extra/pull/1848 | `kdeldycke/click-extra` | `code_and_docs` | `python` | Release `v8.6.2` |
| https://github.com/kdeldycke/click-extra/pull/1842 | `kdeldycke/click-extra` | `code_and_docs` | `python` | Release `v8.6.1` |
| https://github.com/kdeldycke/click-extra/pull/1847 | `kdeldycke/click-extra` | `code_only_tests_or_fixtures` | `python` | Sync action pins |
| https://github.com/kdeldycke/click-extra/pull/1661 | `kdeldycke/click-extra` | `code_and_docs` | `python` | Bump minor version to `v7.14.0` |
| https://github.com/kdeldycke/click-extra/pull/1664 | `kdeldycke/click-extra` | `code_only` | `python` | Format Python |
| https://github.com/kdeldycke/click-extra/pull/1667 | `kdeldycke/click-extra` | `code_only` | `python` | Format `pyproject.toml` |
| https://github.com/kdeldycke/click-extra/pull/1666 | `kdeldycke/click-extra` | `code_only` | `python` | Format Python |
| https://github.com/kdeldycke/click-extra/pull/1657 | `kdeldycke/click-extra` | `code_and_docs` | `python` | Release `v7.14.0` |
| https://github.com/kdeldycke/click-extra/pull/1669 | `kdeldycke/click-extra` | `code_and_docs` | `python` | Release `v7.14.1` |
| https://github.com/kdeldycke/click-extra/pull/1833 | `kdeldycke/click-extra` | `code_and_docs` | `python` | Release `v8.6.0` |
| https://github.com/kdeldycke/click-extra/pull/1835 | `kdeldycke/click-extra` | `code_and_docs` | `python` | Bump minor version to `v8.6.0` |
| https://github.com/kdeldycke/click-extra/pull/1838 | `kdeldycke/click-extra` | `code_only_tests_or_fixtures` | `python` | Sync workflow pins |
| https://github.com/kdeldycke/click-extra/pull/1836 | `kdeldycke/click-extra` | `code_only` | `python` | Sync `bump-my-version` config |
| https://github.com/kdeldycke/click-extra/pull/1824 | `kdeldycke/click-extra` | `code_and_docs` | `python` | Release `v8.5.0` |
| https://github.com/kdeldycke/click-extra/pull/1629 | `kdeldycke/click-extra` | `code_only` | `python` | Format `pyproject.toml` |
| https://github.com/kdeldycke/click-extra/pull/1624 | `kdeldycke/click-extra` | `code_only_tests_or_fixtures` | `python` | Format Python |
| https://github.com/kdeldycke/click-extra/pull/1632 | `kdeldycke/click-extra` | `code_only` | `python` | Sync `uv.lock` |
| https://github.com/kdeldycke/click-extra/pull/1633 | `kdeldycke/click-extra` | `code_only` | `python` | Format Python |
| https://github.com/kdeldycke/click-extra/pull/1627 | `kdeldycke/click-extra` | `code_and_docs` | `python` | Bump minor version to `v7.12.0` |
| https://github.com/kdeldycke/click-extra/pull/1635 | `kdeldycke/click-extra` | `code_only` | `python` | Format Python |
| https://github.com/kdeldycke/click-extra/pull/1625 | `kdeldycke/click-extra` | `code_and_docs` | `python` | Release `v7.12.0` |
| https://github.com/kdeldycke/click-extra/pull/1645 | `kdeldycke/click-extra` | `code_only` | `python` | Format `pyproject.toml` |
| https://github.com/kdeldycke/click-extra/pull/1638 | `kdeldycke/click-extra` | `code_only` | `python` | Format Python |
| https://github.com/kdeldycke/click-extra/pull/1646 | `kdeldycke/click-extra` | `code_only` | `python` | Format Python |
| https://github.com/kdeldycke/click-extra/pull/1643 | `kdeldycke/click-extra` | `code_and_docs` | `python` | Bump minor version to `v7.13.0` |
| https://github.com/kdeldycke/click-extra/pull/1648 | `kdeldycke/click-extra` | `code_only` | `python` | Format `pyproject.toml` |
| https://github.com/kdeldycke/click-extra/pull/1649 | `kdeldycke/click-extra` | `code_only` | `python` | Sync `bump-my-version` config |
| https://github.com/kdeldycke/click-extra/pull/1652 | `kdeldycke/click-extra` | `code_only` | `python` | Format Python |
| https://github.com/kdeldycke/click-extra/pull/1639 | `kdeldycke/click-extra` | `code_and_docs` | `python` | Release `v7.13.0` |
| https://github.com/kdeldycke/click-extra/pull/1827 | `kdeldycke/click-extra` | `code_and_docs` | `python` | Bump minor version to `v8.5.0` |
| https://github.com/kdeldycke/click-extra/pull/1810 | `kdeldycke/click-extra` | `code_and_docs` | `python` | Release `v8.4.0` |
| https://github.com/mnaoumov/obsidian-codescript-toolkit/pull/7 | `mnaoumov/obsidian-codescript-toolkit` | `code_only` | `typescript` | Apply rebranding |
| https://github.com/locustio/locust/pull/3502 | `locustio/locust` | `code_only` | `python` | Fix Web UI 500 error handler crashing on plain exceptions |
| https://github.com/locustio/locust/pull/3504 | `locustio/locust` | `code_only` | `python` | fix: fix pythonVersion in ruffConfig and fix extend-exclude setting |
| https://github.com/locustio/locust/pull/3487 | `locustio/locust` | `code_only` | `python` | Update uv to 0.12 |
| https://github.com/locustio/locust/pull/3501 | `locustio/locust` | `code_only` | `python` | Fix master stopping test prematurely when a missing worker quits |
| https://github.com/locustio/locust/pull/3498 | `locustio/locust` | `code_only` | `python` | build(deps-dev): bump cryptography from 48.0.1 to 50.0.0 |
| https://github.com/locustio/locust/pull/3494 | `locustio/locust` | `code_only` | `python` | Re-enable tests using Python 3.15. Update uv.lock |
| https://github.com/locustio/locust/pull/3489 | `locustio/locust` | `code_only` | `python` | fix: exclude missing workers from new dispatches |
| https://github.com/locustio/locust/pull/3492 | `locustio/locust` | `code_only` | `python` | Fix FastHttpUser streaming response_length using wrong header key |
| https://github.com/locustio/locust/pull/3483 | `locustio/locust` | `code_only` | `python` | [FEAT] : add active user metric as an observable gauge |
| https://github.com/locustio/locust/pull/3488 | `locustio/locust` | `code_only` | `python` | Fix url possibly unbound in headless non-worker mode |
| https://github.com/locustio/locust/pull/3486 | `locustio/locust` | `code_only` | `python` | Explicitly close csv file handles before exit |
| https://github.com/locustio/locust/pull/3484 | `locustio/locust` | `code_only` | `python` | Fix variable shadowing in _aggregate_dispatched_users |
| https://github.com/locustio/locust/pull/3481 | `locustio/locust` | `code_only` | `python` | build(deps-dev): bump cryptography from 46.0.7 to 48.0.1 |
| https://github.com/locustio/locust/pull/3476 | `locustio/locust` | `code_only` | `python` | Change StatsEntry typing to not allow None for stats |
| https://github.com/locustio/locust/pull/3473 | `locustio/locust` | `code_only` | `python` | Fix response time percentiles being deflated by requests logged with response_time=None |
| https://github.com/locustio/locust/pull/3469 | `locustio/locust` | `code_only` | `python` | Update swarm state with extraOptions |
| https://github.com/locustio/locust/pull/3470 | `locustio/locust` | `code_only` | `python` | Allow new gevent versions |
| https://github.com/locustio/locust/pull/3468 | `locustio/locust` | `code_and_docs` | `python` | Remove support for Python 3.10 |
| https://github.com/locustio/locust/pull/3466 | `locustio/locust` | `code_only` | `python` | skip python3.15 tests |
| https://github.com/locustio/locust/pull/3460 | `locustio/locust` | `code_only` | `python` | chore: add support python3.15 |
| https://github.com/locustio/locust/pull/3464 | `locustio/locust` | `code_only` | `python` | Fix two exception handling bugs |
| https://github.com/locustio/locust/pull/3461 | `locustio/locust` | `code_only` | `python` | Move --csv-full-history validation before process forking |
| https://github.com/locustio/locust/pull/3457 | `locustio/locust` | `code_only` | `python` | minor improvements to type hinting |
| https://github.com/locustio/locust/pull/3431 | `locustio/locust` | `code_only` | `python` | fix: proper_round gives wrong result for integer inputs when digits > 0 |
| https://github.com/locustio/locust/pull/3445 | `locustio/locust` | `code_only` | `python` | build(deps-dev): bump sphinxcontrib-applehelp from 1.0.4 to 2.0.0 |
| https://github.com/locustio/locust/pull/3455 | `locustio/locust` | `code_only` | `python` | Fix rps display issue (caused by inconsistencies in current_rps vs total_rps) |
| https://github.com/locustio/locust/pull/3456 | `locustio/locust` | `code_only` | `python` | Fix Echart Styles |
| https://github.com/locustio/locust/pull/3453 | `locustio/locust` | `code_only` | `python` | Bump Webui Deps |
| https://github.com/locustio/locust/pull/3442 | `locustio/locust` | `code_only_tests_or_fixtures` | `python` | build(deps): bump the all_dependencies group with 6 updates |
| https://github.com/locustio/locust/pull/3440 | `locustio/locust` | `code_only` | `python` | build(deps-dev): bump the eslint group in /locust/webui with 7 updates |
| https://github.com/locustio/locust/pull/3441 | `locustio/locust` | `code_only` | `python` | build(deps): bump the vite group in /locust/webui with 5 updates |
| https://github.com/locustio/locust/pull/3439 | `locustio/locust` | `code_only` | `python` | fix: require host when detecting URLs |
| https://github.com/locustio/locust/pull/3432 | `locustio/locust` | `code_and_docs` | `python` | Add perf ruff rule |
| https://github.com/locustio/locust/pull/3429 | `locustio/locust` | `code_only` | `python` | CLI: remove --csv-full-history for workers with --processes |
| https://github.com/locustio/locust/pull/3425 | `locustio/locust` | `code_only` | `python` | fix: reject partially-matched timespan strings in parse_timespan |
| https://github.com/locustio/locust/pull/3424 | `locustio/locust` | `code_only` | `python` | Add OTEL locust.client.duration histogram for response times |
| https://github.com/locustio/locust/pull/3421 | `locustio/locust` | `code_and_docs` | `python` | Add logging support to for OTEL |
| https://github.com/locustio/locust/pull/3420 | `locustio/locust` | `code_only` | `python` | Add hostname, locustfile and profile to otel Resource |
| https://github.com/locustio/locust/pull/3412 | `locustio/locust` | `code_only` | `python` | up pre-commit 3.xx to 4.xxx |
| https://github.com/locustio/locust/pull/3408 | `locustio/locust` | `code_only_tests_or_fixtures` | `python` | Disable UI lib npm package publication |
| https://github.com/locustio/locust/pull/3409 | `locustio/locust` | `code_and_docs` | `python` | unify ruff in pyproject.toml and pre-commits |
| https://github.com/locustio/locust/pull/3399 | `locustio/locust` | `code_and_docs` | `python` | Add AI-optimized documentation (llms.txt) |
| https://github.com/locustio/locust/pull/3406 | `locustio/locust` | `code_only` | `python` | fix(fasthttp): add 308 to redirect_resonse_codes in LocustUserAgent |
| https://github.com/locustio/locust/pull/3405 | `locustio/locust` | `code_only` | `python` | fix(fasthttp): handle zlib.error for truncated gzip streams under high load |
| https://github.com/locustio/locust/pull/3403 | `locustio/locust` | `code_only` | `python` | Add first seen / last seen timestamps to failure stats |
| https://github.com/locustio/locust/pull/3398 | `locustio/locust` | `code_only` | `python` | Fix FastHttpUser crash on Python 3.13+ due to GC collecting __dict__ reference cycle |
| https://github.com/locustio/locust/pull/3397 | `locustio/locust` | `code_only` | `python` | fix(fasthttp): catch FAILURE_EXCEPTIONS during response body read |
| https://github.com/locustio/locust/pull/3384 | `locustio/locust` | `code_only` | `python` | fix: use total_rps instead of current_rps in HTML report and navbar stats |
| https://github.com/locustio/locust/pull/3382 | `locustio/locust` | `code_only` | `python` | Fix false "--run-time limit reached" log message when shape test completes |
| https://github.com/locustio/locust/pull/3381 | `locustio/locust` | `code_and_docs` | `python` | Fix typos in docs, docstrings, and UI string |
| https://github.com/locustio/locust/pull/3379 | `locustio/locust` | `code_and_docs` | `python` | Add locust-otel Docker image with OpenTelemetry dependencies |
| https://github.com/locustio/locust/pull/3375 | `locustio/locust` | `code_only` | `python` | Bump the vite group across 1 directory with 3 updates |
| https://github.com/locustio/locust/pull/3367 | `locustio/locust` | `code_only` | `python` | Bump typescript from 5.7.2 to 5.9.3 in /locust/webui |
| https://github.com/locustio/locust/pull/3364 | `locustio/locust` | `code_only` | `python` | Bump the vite group in /locust/webui with 2 updates |
| https://github.com/locustio/locust/pull/3363 | `locustio/locust` | `code_only` | `python` | Bump the eslint group in /locust/webui with 8 updates |
| https://github.com/locustio/locust/pull/3374 | `locustio/locust` | `code_only` | `python` | Improve Type Hinting for Wait Time Functions |
| https://github.com/locustio/locust/pull/3373 | `locustio/locust` | `code_and_docs` | `python` | Extract response time bucketing into an overridable function |
| https://github.com/locustio/locust/pull/3356 | `locustio/locust` | `code_only_tests_or_fixtures` | `python` | Bump the all_dependencies group with 2 updates |
| https://github.com/locustio/locust/pull/3358 | `locustio/locust` | `code_only` | `python` | Bump snowballstemmer from 2.2.0 to 3.0.1 |
| https://github.com/locustio/locust/pull/3361 | `locustio/locust` | `code_only` | `python` | Bump sphinxcontrib-serializinghtml from 1.1.10 to 2.0.0 |
| https://github.com/locustio/locust/pull/3359 | `locustio/locust` | `code_only` | `python` | Bump sphinxcontrib-htmlhelp from 2.0.1 to 2.1.0 |
| https://github.com/locustio/locust/pull/3354 | `locustio/locust` | `code_and_docs` | `python` | Add Qdrant support |
| https://github.com/locustio/locust/pull/3353 | `locustio/locust` | `code_only` | `python` | Unset print_stats on workers created by --processes option |
| https://github.com/locustio/locust/pull/3268 | `locustio/locust` | `code_only` | `python` | adding mqtt user feature that works around the paho mqtt 340 connections limit issue |
| https://github.com/locustio/locust/pull/3347 | `locustio/locust` | `code_only` | `python` | Bump cryptography from 43.0.3 to 46.0.5 |
| https://github.com/locustio/locust/pull/3344 | `locustio/locust` | `code_only` | `python` | Add missing event hook parameter documentation |
| https://github.com/locustio/locust/pull/3339 | `locustio/locust` | `code_only` | `python` | Bump sphinx-rtd-theme from 3.0.2 to 3.1.0 |
| https://github.com/locustio/locust/pull/3331 | `locustio/locust` | `code_only` | `python` | Bump packages |
| https://github.com/locustio/locust/pull/3326 | `locustio/locust` | `code_only_tests_or_fixtures` | `python` | Stabilize tests |
| https://github.com/locustio/locust/pull/3325 | `locustio/locust` | `code_only_tests_or_fixtures` | `python` | Stabilize tests |
| https://github.com/locustio/locust/pull/3319 | `locustio/locust` | `code_only` | `python` | Bump the eslint group in /locust/webui with 5 updates |
| https://github.com/locustio/locust/pull/3318 | `locustio/locust` | `code_only_tests_or_fixtures` | `python` | Bump the all_dependencies group with 2 updates |
| https://github.com/locustio/locust/pull/3322 | `locustio/locust` | `code_only` | `python` | Bump @emotion/styled from 11.14.0 to 11.14.1 in /locust/webui in the emotion group |
| https://github.com/locustio/locust/pull/3316 | `locustio/locust` | `code_only` | `python` | Support requests>=2.32.5, reimplement the fix previously there for only loading ssl certificates once |
| https://github.com/locustio/locust/pull/3317 | `locustio/locust` | `code_only` | `python` | Provide a better error message when spawn rate is set to zero |
| https://github.com/locustio/locust/pull/3314 | `locustio/locust` | `code_and_docs` | `python` | Remove references to locust.cloud now that it is shutting down |
| https://github.com/locustio/locust/pull/3313 | `locustio/locust` | `code_only` | `python` | Allow users to stop test run by raising StopTest, use it on missing host in locustfile (and no --host param) |
| https://github.com/locustio/locust/pull/3312 | `locustio/locust` | `code_only` | `python` | Locust Cloud demo tab: update domain from auth.locust.cloud to app.locust.cloud |
| https://github.com/locustio/locust/pull/3311 | `locustio/locust` | `code_only` | `python` | Solving the iter_lines problem |
| https://github.com/locustio/locust/pull/3310 | `locustio/locust` | `code_only` | `python` | Refactor parse_options |
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
| https://github.com/marshmallow-code/marshmallow/pull/2871 | `marshmallow-code/marshmallow` | `code_only` | `python` | [pre-commit.ci] pre-commit autoupdate |
| https://github.com/marshmallow-code/marshmallow/pull/2867 | `marshmallow-code/marshmallow` | `code_only` | `python` | [pre-commit.ci] pre-commit autoupdate |
| https://github.com/marshmallow-code/marshmallow/pull/2865 | `marshmallow-code/marshmallow` | `code_only` | `python` | Bump actions/download-artifact from 5 to 6 |
| https://github.com/marshmallow-code/marshmallow/pull/2866 | `marshmallow-code/marshmallow` | `code_only` | `python` | Bump actions/upload-artifact from 4 to 5 |
| https://github.com/marshmallow-code/marshmallow/pull/2861 | `marshmallow-code/marshmallow` | `code_and_docs` | `python` | (fix) missing constant with len validation |
| https://github.com/marshmallow-code/marshmallow/pull/2864 | `marshmallow-code/marshmallow` | `code_and_docs` | `python` | Test against Python 3.14 |
| https://github.com/marshmallow-code/marshmallow/pull/2863 | `marshmallow-code/marshmallow` | `code_only` | `python` | Drop Python 3.9 |
| https://github.com/marshmallow-code/marshmallow/pull/2856 | `marshmallow-code/marshmallow` | `code_only` | `python` | [pre-commit.ci] pre-commit autoupdate |
| https://github.com/marshmallow-code/marshmallow/pull/2857 | `marshmallow-code/marshmallow` | `code_only` | `python` | Disable RUF043 in tests: allow metacharacters in match patterns |
| https://github.com/marshmallow-code/marshmallow/pull/2855 | `marshmallow-code/marshmallow` | `code_only` | `python` | Bump actions/setup-python from 5 to 6 |
| https://github.com/marshmallow-code/marshmallow/pull/2853 | `marshmallow-code/marshmallow` | `code_only` | `python` | Bump furo from 2025.7.19 to 2025.9.25 |
| https://github.com/marshmallow-code/marshmallow/pull/2849 | `marshmallow-code/marshmallow` | `code_only` | `python` | Bump actions/download-artifact from 4 to 5 |
| https://github.com/marshmallow-code/marshmallow/pull/2850 | `marshmallow-code/marshmallow` | `code_only` | `python` | Bump actions/checkout from 4 to 5 |
| https://github.com/marshmallow-code/marshmallow/pull/2848 | `marshmallow-code/marshmallow` | `code_only` | `python` | [pre-commit.ci] pre-commit autoupdate |
| https://github.com/marshmallow-code/marshmallow/pull/2847 | `marshmallow-code/marshmallow` | `code_only` | `python` | Bump sphinxext-opengraph from 0.12.0 to 0.13.0 |
| https://github.com/marshmallow-code/marshmallow/pull/2846 | `marshmallow-code/marshmallow` | `code_only` | `python` | Remove incorrect documentaion of field_name param |
| https://github.com/marshmallow-code/marshmallow/pull/2844 | `marshmallow-code/marshmallow` | `code_only` | `python` | Bump sphinxext-opengraph from 0.11.0 to 0.12.0 |
| https://github.com/marshmallow-code/marshmallow/pull/2843 | `marshmallow-code/marshmallow` | `code_only` | `python` | Bump sphinxext-opengraph from 0.10.0 to 0.11.0 |
| https://github.com/marshmallow-code/marshmallow/pull/2842 | `marshmallow-code/marshmallow` | `code_only` | `python` | [pre-commit.ci] pre-commit autoupdate |
| https://github.com/marshmallow-code/marshmallow/pull/2837 | `marshmallow-code/marshmallow` | `code_only` | `python` | Bump furo from 2024.8.6 to 2025.7.19 |
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
| https://github.com/SonarSource/SonarJS/pull/7751 | `sonarsource/sonarjs` | `code_only` | `typescript` | JS-2246: Fix S9135 false positive after nested objects are replaced |
| https://github.com/SonarSource/SonarJS/pull/7697 | `sonarsource/sonarjs` | `code_only` | `typescript` | Update dependency globals to v17.8.0 |
| https://github.com/SonarSource/SonarJS/pull/7698 | `sonarsource/sonarjs` | `code_only` | `typescript` | Update dependency minimatch to v10.2.6 |
| https://github.com/SonarSource/SonarJS/pull/7719 | `sonarsource/sonarjs` | `code_only` | `typescript` | Update dependency tsx to v4.23.3 |
| https://github.com/SonarSource/SonarJS/pull/7728 | `sonarsource/sonarjs` | `code_only` | `typescript` | Update dependency memfs to v4.66.0 |
| https://github.com/SonarSource/SonarJS/pull/7747 | `sonarsource/sonarjs` | `code_only` | `typescript` | Update dependency postcss-selector-parser to v7.1.5 |
| https://github.com/SonarSource/SonarJS/pull/7757 | `sonarsource/sonarjs` | `code_only` | `typescript` | Update dependency esbuild to v0.28.2 |
| https://github.com/SonarSource/SonarJS/pull/7758 | `sonarsource/sonarjs` | `code_only` | `typescript` | Update protobufjs/protobuf.js monorepo |
| https://github.com/SonarSource/SonarJS/pull/7761 | `sonarsource/sonarjs` | `code_only` | `typescript` | Update dependency @stylistic/stylelint-plugin to v5.3.0 |
| https://github.com/SonarSource/SonarJS/pull/7762 | `sonarsource/sonarjs` | `code_only` | `typescript` | Update dependency @cyclonedx/cyclonedx-npm to v6.0.1 |
| https://github.com/SonarSource/SonarJS/pull/7760 | `sonarsource/sonarjs` | `code_only` | `typescript` | JS-2250 Fix bump-versions workflow to produce semantic snapshot versions |
| https://github.com/SonarSource/SonarJS/pull/7742 | `sonarsource/sonarjs` | `code_and_docs` | `typescript` | JS-2234 Fix S7649: false positive when an Angular input alias is a JavaScript reserved word |
| https://github.com/SonarSource/SonarJS/pull/7745 | `sonarsource/sonarjs` | `code_only` | `typescript` | JS-2237: Implement S9333: Synchronous Testing Library queries should not be awaited |
| https://github.com/SonarSource/SonarJS/pull/7756 | `sonarsource/sonarjs` | `code_and_docs` | `typescript` | Revert "JS-1610 Replace S1481 with @typescript-eslint/no-unused-vars … |
| https://github.com/SonarSource/SonarJS/pull/7739 | `sonarsource/sonarjs` | `code_only` | `typescript` | JS-2235: Implement S9169: vi.mock should be declared at module scope |
| https://github.com/SonarSource/SonarJS/pull/7743 | `sonarsource/sonarjs` | `code_only` | `typescript` | JS-2236: Implement S9332: disallow Playwright networkidle waits |
| https://github.com/SonarSource/SonarJS/pull/7744 | `sonarsource/sonarjs` | `code_only` | `typescript` | JS-2218 Update S9150 and S9145: Enforce version floor to be 2.7 |
| https://github.com/SonarSource/SonarJS/pull/7701 | `sonarsource/sonarjs` | `code_only` | `typescript` | JS-2205 USER-2389 Support Window onmessage in S2819 |
| https://github.com/SonarSource/SonarJS/pull/7734 | `sonarsource/sonarjs` | `code_only` | `typescript` | JS-2232: Implement S9153: Testing Library disappearance waits should use non-throwing queries |
| https://github.com/SonarSource/SonarJS/pull/7694 | `sonarsource/sonarjs` | `code_only` | `typescript` | JS-2192 Fix S4782 false positive for external indexed access |
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
| https://github.com/hynek/structlog/pull/737 | `hynek/structlog` | `code_only` | `python` | [pre-commit.ci] pre-commit autoupdate |
| https://github.com/hynek/structlog/pull/735 | `hynek/structlog` | `code_and_docs` | `python` | Raise useful error if trying to use RichTracebackFormatter w/o Rich |
| https://github.com/hynek/structlog/pull/728 | `hynek/structlog` | `code_and_docs` | `python` | Add processors param to capture_logs() |
| https://github.com/hynek/structlog/pull/720 | `hynek/structlog` | `code_and_docs` | `python` | tracebacks: Handle ExceptionGroup |
| https://github.com/hynek/structlog/pull/724 | `hynek/structlog` | `code_and_docs` | `python` | fix ExceptionPrettyPrinter custom formatter support |
| https://github.com/hynek/structlog/pull/725 | `hynek/structlog` | `code_and_docs` | `python` | Use dependency groups |
| https://github.com/hynek/structlog/pull/723 | `hynek/structlog` | `code_and_docs` | `python` | Add 3.14 |
| https://github.com/hynek/structlog/pull/722 | `hynek/structlog` | `code_only` | `python` | [pre-commit.ci] pre-commit autoupdate |
| https://github.com/hynek/structlog/pull/713 | `hynek/structlog` | `code_and_docs` | `python` | TimeStamper now returns UTC timezone for custom format string. |
| https://github.com/hynek/structlog/pull/694 | `hynek/structlog` | `code_only` | `python` | Typing: return Self in stdlib.BoundLogger |
| https://github.com/hynek/structlog/pull/709 | `hynek/structlog` | `code_and_docs` | `python` | TimeStamper() now uses TZ-aware objects |
| https://github.com/hynek/structlog/pull/704 | `hynek/structlog` | `code_only` | `python` | [pre-commit.ci] pre-commit autoupdate |
| https://github.com/hynek/structlog/pull/701 | `hynek/structlog` | `code_and_docs` | `python` | expose LogfmtRenderer for imports |
| https://github.com/hynek/structlog/pull/699 | `hynek/structlog` | `code_and_docs` | `python` | expose RichTracebackFormatter for imports in structlog.dev |
| https://github.com/hynek/structlog/pull/684 | `hynek/structlog` | `code_and_docs` | `python` | Include notes when logging exceptions |
| https://github.com/hynek/structlog/pull/691 | `hynek/structlog` | `code_and_docs` | `python` | Only build in RTD and only doctests in CI |
| https://github.com/hynek/structlog/pull/689 | `hynek/structlog` | `code_and_docs` | `python` | native loggers: add is_enabled_for & get_effective_level |
| https://github.com/hynek/structlog/pull/690 | `hynek/structlog` | `code_only` | `python` | docs: use uv & 3.13 for build |
| https://github.com/hynek/structlog/pull/668 | `hynek/structlog` | `code_and_docs` | `python` | Add 'structlog.stdlib.render_to_log_args_and_kwargs' processor |
| https://github.com/hynek/structlog/pull/688 | `hynek/structlog` | `code_only` | `python` | [pre-commit.ci] pre-commit autoupdate |
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
| https://github.com/rossoctl/rossoctl/pull/2225 | `rossoctl/rossoctl` | `code_only` | `python` | chore(release): pin image tags for v0.7.0-alpha.5 |
| https://github.com/rossoctl/rossoctl/pull/2221 | `rossoctl/rossoctl` | `code_only` | `python` | Chore: Remove orphaned in-cluster LiteLLM proxy deployment and scripts |
| https://github.com/rossoctl/rossoctl/pull/2219 | `rossoctl/rossoctl` | `code_only` | `python` | fix(e2e): best-effort token-exchange readiness wait + exec-script fix; keep xfail (#2129) |
| https://github.com/rossoctl/rossoctl/pull/1885 | `rossoctl/rossoctl` | `code_and_docs` | `python` | fix(ci): HyperShift OpenShell auto-trigger on push to main |
| https://github.com/rossoctl/rossoctl/pull/2201 | `rossoctl/rossoctl` | `code_only` | `python` | fix(ui): omit unset optional args on tool invoke (#2200) |
| https://github.com/rossoctl/rossoctl/pull/2171 | `rossoctl/rossoctl` | `code_only` | `python` | fix(k8s): sanitize user-controlled values in KubernetesService logs (CWE-117) |
| https://github.com/rossoctl/rossoctl/pull/2169 | `rossoctl/rossoctl` | `code_only` | `python` | feat(simulation): provision simulated-tool workload (StatefulSet + PVC + Service) |
| https://github.com/rossoctl/rossoctl/pull/2187 | `rossoctl/rossoctl` | `code_and_docs` | `python` | feat(examples,docs): simulated-tool worked example, E2E test, and docs (#2167) |
| https://github.com/rossoctl/rossoctl/pull/2186 | `rossoctl/rossoctl` | `code_only` | `python` | feat(ui): simulated-tool lifecycle controls + database seed/edit (#2166) |
| https://github.com/rossoctl/rossoctl/pull/2185 | `rossoctl/rossoctl` | `code_only` | `python` | feat(ui): simulated tools — import flow, generation progress, and SIMULATED badge (#2165) |
| https://github.com/rossoctl/rossoctl/pull/2184 | `rossoctl/rossoctl` | `code_only` | `python` | feat(simulation): database seed/edit and persistence across restart (#2164) |
| https://github.com/rossoctl/rossoctl/pull/2183 | `rossoctl/rossoctl` | `code_only` | `python` | feat(simulation): lifecycle — start / stop / reset / delete (#2163) |
| https://github.com/rossoctl/rossoctl/pull/2173 | `rossoctl/rossoctl` | `code_only` | `python` | feat(simulation): generation orchestration, status, and failure states (#2162) |
| https://github.com/rossoctl/rossoctl/pull/2168 | `rossoctl/rossoctl` | `code_only` | `python` | feat(simulation): feature flag and flagged simulation router scaffold |
| https://github.com/rossoctl/rossoctl/pull/1856 | `rossoctl/rossoctl` | `code_only` | `python` | Refactor: remove Keycloak operand/realm from chart (moved to operator) |
| https://github.com/rossoctl/rossoctl/pull/2141 | `rossoctl/rossoctl` | `code_and_docs` | `python` | feat(operator): add SPIFFE authentication bootstrap for operator client registration |
| https://github.com/rossoctl/rossoctl/pull/2181 | `rossoctl/rossoctl` | `code_only` | `python` | build(deps): Bump the minor-and-patch group across 1 directory with 3 updates |
| https://github.com/rossoctl/rossoctl/pull/2182 | `rossoctl/rossoctl` | `code_only` | `python` | chore(deps): Bump the minor-and-patch group with 6 updates |
| https://github.com/rossoctl/rossoctl/pull/2214 | `rossoctl/rossoctl` | `code_only_tests_or_fixtures` | `python` | Fix: Retry transient transport timeouts in agent conversation e2e tests |
| https://github.com/rossoctl/rossoctl/pull/2157 | `rossoctl/rossoctl` | `code_only` | `python` | feat(skills): make in-cluster skillberry-store run the Claude Code CLI |
| https://github.com/aeonfun/aeon/pull/998 | `aeonfun/aeon` | `code_only` | `typescript` | Add tiered GLM model mapping (GLM_MODEL_SONNET/OPUS/HAIKU) |
| https://github.com/aeonfun/aeon/pull/987 | `aeonfun/aeon` | `code_only` | `typescript` | fix(envelope): fail on unparseable adapter output |
| https://github.com/aeonfun/aeon/pull/989 | `aeonfun/aeon` | `code_only_tests_or_fixtures` | `typescript` | retry transient xai search failures |
| https://github.com/aeonfun/aeon/pull/988 | `aeonfun/aeon` | `code_only` | `typescript` | fix(chains): correlate dispatched skill runs uniquely |
| https://github.com/aeonfun/aeon/pull/993 | `aeonfun/aeon` | `code_only` | `typescript` | feat(dashboard): Connect copies gh token into GH_GLOBAL |
| https://github.com/aeonfun/aeon/pull/994 | `aeonfun/aeon` | `code_only` | `typescript` | style(dashboard): shorten harness picker labels |
| https://github.com/aeonfun/aeon/pull/990 | `aeonfun/aeon` | `code_and_docs` | `typescript` | feat: move GLM from harness to Claude AI Gateway |
| https://github.com/aeonfun/aeon/pull/986 | `aeonfun/aeon` | `code_only` | `typescript` | fix(dashboard): require exact origin host match |
| https://github.com/aeonfun/aeon/pull/984 | `aeonfun/aeon` | `code_only_tests_or_fixtures` | `typescript` | fail hermes runs on api errors |
| https://github.com/aeonfun/aeon/pull/983 | `aeonfun/aeon` | `code_and_docs` | `typescript` | trust cursor workspaces in headless runs |
| https://github.com/aeonfun/aeon/pull/982 | `aeonfun/aeon` | `code_only` | `typescript` | allow fx workflow dispatches |
| https://github.com/aeonfun/aeon/pull/954 | `aeonfun/aeon` | `code_and_docs` | `typescript` | feat: add cortx-reliability skill — x402 endpoint reliability check |
| https://github.com/aeonfun/aeon/pull/980 | `aeonfun/aeon` | `code_and_docs` | `typescript` | docs: sync PRs #957-#979 to aeon docs |
| https://github.com/aeonfun/aeon/pull/978 | `aeonfun/aeon` | `code_and_docs` | `typescript` | Add Spoolis Outcome Gate skill pack |
| https://github.com/aeonfun/aeon/pull/969 | `aeonfun/aeon` | `code_only` | `typescript` | add recommend-only harness comparison |
| https://github.com/aeonfun/aeon/pull/977 | `aeonfun/aeon` | `code_and_docs` | `typescript` | docs: list Farcaster Pack in the community skill-pack registry |
| https://github.com/aeonfun/aeon/pull/970 | `aeonfun/aeon` | `code_only` | `typescript` | fix: bound rendered telegram chunks |
| https://github.com/aeonfun/aeon/pull/974 | `aeonfun/aeon` | `code_and_docs` | `typescript` | feat: list CultOS Aeon skill pack |
| https://github.com/aeonfun/aeon/pull/975 | `aeonfun/aeon` | `code_only` | `typescript` | fix dashboard auth rows for new harnesses |
| https://github.com/aeonfun/aeon/pull/973 | `aeonfun/aeon` | `code_only` | `typescript` | fix(mcp-server): run skills async with a single-flight queue |
| https://github.com/aeonfun/aeon/pull/959 | `aeonfun/aeon` | `code_and_docs` | `typescript` | chore(plugin): prep operator-console plugin for OpenAI submission |
| https://github.com/aeonfun/aeon/pull/879 | `aeonfun/aeon` | `code_only` | `typescript` | security: bump nanoid to 3.3.18 (GHSA-2v37-7h3g-55p8) |
| https://github.com/aeonfun/aeon/pull/938 | `aeonfun/aeon` | `code_and_docs` | `typescript` | improve(memory-flush): deterministic prep + structured watermark |
| https://github.com/aeonfun/aeon/pull/930 | `aeonfun/aeon` | `code_and_docs` | `typescript` | fix: Windows Connect OAuth, setup-token timeout, config line-folding, Foundry install, mainnet flag masking |
| https://github.com/aeonfun/aeon/pull/953 | `aeonfun/aeon` | `code_only` | `typescript` | fix(mcp-server): dispatch fx harness |
| https://github.com/aeonfun/aeon/pull/906 | `aeonfun/aeon` | `code_only` | `typescript` | fix(scheduler): make reactive success_rate condition actually fire |
| https://github.com/aeonfun/aeon/pull/952 | `aeonfun/aeon` | `code_and_docs` | `typescript` | docs: normalize harness count to seven, drop fx singling-out |
| https://github.com/aeonfun/aeon/pull/901 | `aeonfun/aeon` | `code_only` | `typescript` | fix(cron-state): jittered backoff + 10 retries for commit-race |
| https://github.com/aeonfun/aeon/pull/915 | `aeonfun/aeon` | `code_only` | `typescript` | fix(workflow): bound apt installs so a dpkg-lock stall can't eat the job wall |
| https://github.com/aeonfun/aeon/pull/907 | `aeonfun/aeon` | `code_only` | `typescript` | feat(validate-config): validate reactive-trigger references and conditions |
| https://github.com/aeonfun/aeon/pull/914 | `aeonfun/aeon` | `code_and_docs` | `typescript` | feat(dry-run): gate self-authored skills before auto-merge |
| https://github.com/aeonfun/aeon/pull/801 | `aeonfun/aeon` | `code_and_docs` | `typescript` | feat(scheduler): auto-recovering circuit breaker for failing skills |
| https://github.com/aeonfun/aeon/pull/910 | `aeonfun/aeon` | `code_and_docs` | `typescript` | feat(scheduler): reactive handler learns which skill tripped it (item 3) |
| https://github.com/aeonfun/aeon/pull/931 | `aeonfun/aeon` | `code_and_docs` | `typescript` | feat(dashboard): auto-allowlist MCP secret names into the run workflows |
| https://github.com/aeonfun/aeon/pull/911 | `aeonfun/aeon` | `code_and_docs` | `typescript` | feat(chains): verdict routing on Haiku scores (when: on chain steps) |
| https://github.com/aeonfun/aeon/pull/908 | `aeonfun/aeon` | `code_and_docs` | `typescript` | feat(audit): structured audit log of privileged actions |
| https://github.com/aeonfun/aeon/pull/962 | `aeonfun/aeon` | `code_only` | `typescript` | chore(ci): add eslint + shellcheck lint gates |
| https://github.com/aeonfun/aeon/pull/900 | `aeonfun/aeon` | `code_only` | `typescript` | chore(harness): 30m skill-run timeout (harness 1800s, job 50m) |
| https://github.com/aeonfun/aeon/pull/965 | `aeonfun/aeon` | `code_only` | `typescript` | Add MiniMax plugin manifest for the aeon operator console |
| https://github.com/aeonfun/aeon/pull/832 | `aeonfun/aeon` | `code_and_docs` | `typescript` | create skill: aeon-update (downstream framework updater) |
| https://github.com/aeonfun/aeon/pull/967 | `aeonfun/aeon` | `code_and_docs` | `typescript` | add cursor hermes and glm harnesses |
| https://github.com/aeonfun/aeon/pull/968 | `aeonfun/aeon` | `code_only` | `typescript` | add machine-readable vuln scanner execution evidence |
| https://github.com/aeonfun/aeon/pull/964 | `aeonfun/aeon` | `code_and_docs` | `typescript` | feat(plugin): Agent Plugins plugin.json + privacy/support for Kiro Powers |
| https://github.com/aeonfun/aeon/pull/961 | `aeonfun/aeon` | `code_and_docs` | `typescript` | add rightstack web3 advisor |
| https://github.com/aeonfun/aeon/pull/956 | `aeonfun/aeon` | `code_only` | `typescript` | fix(dashboard): capture kimi auth config correctly |
| https://github.com/aeonfun/aeon/pull/955 | `aeonfun/aeon` | `code_only` | `typescript` | feat(notify): post-run delivery dispatcher, drop channel tokens from skill env (#912 Phase 2) |
| https://github.com/aeonfun/aeon/pull/951 | `aeonfun/aeon` | `code_only` | `typescript` | fix(secrets): drop dead channel creds from the in-run skill env (#912 item 2) |
| https://github.com/aeonfun/aeon/pull/949 | `aeonfun/aeon` | `code_only` | `typescript` | fix(scorer): grade the sent notify card, not the harness .result summary |
| https://github.com/aeonfun/aeon/pull/945 | `aeonfun/aeon` | `code_and_docs` | `typescript` | feat(skills): add skill-article — launch article for any skill, receipts-first |
| https://github.com/aeonfun/aeon/pull/943 | `aeonfun/aeon` | `code_only` | `typescript` | fix(dashboard): fx never showed up in the harness picker |
| https://github.com/aeonfun/aeon/pull/944 | `aeonfun/aeon` | `code_only` | `typescript` | fix(dashboard): lock aeon.yml read-modify-write to stop config races |
| https://github.com/aeonfun/aeon/pull/947 | `aeonfun/aeon` | `code_only` | `typescript` | Egress audit hardening (iron-proxy) - opt-in |
| https://github.com/aeonfun/aeon/pull/937 | `aeonfun/aeon` | `code_and_docs` | `typescript` | fix(webhook): dedupe Telegram updates by update_id before dispatch |
| https://github.com/aeonfun/aeon/pull/941 | `aeonfun/aeon` | `code_and_docs` | `typescript` | feat(harness): add fx (vercel) as a 7th harness |
| https://github.com/aeonfun/aeon/pull/936 | `aeonfun/aeon` | `code_only_tests_or_fixtures` | `typescript` | fix(state_store,health_issue): converge racing issue-store ensures |
| https://github.com/aeonfun/aeon/pull/935 | `aeonfun/aeon` | `code_only_tests_or_fixtures` | `typescript` | fix(secretcurl): keep substituted secrets out of curl's own argv |
| https://github.com/aeonfun/aeon/pull/934 | `aeonfun/aeon` | `code_only` | `typescript` | fix(aeon): scope the skill-runner concurrency group by target too |
| https://github.com/aeonfun/aeon/pull/932 | `aeonfun/aeon` | `code_only` | `typescript` | fix(harness): stop truncating diagnostic output on every failed dispatch |
| https://github.com/aeonfun/aeon/pull/929 | `aeonfun/aeon` | `code_only` | `typescript` | chore: drop the HOL plugin-scanner workflow + config |
| https://github.com/aeonfun/aeon/pull/928 | `aeonfun/aeon` | `code_and_docs` | `typescript` | ci: scan the operator-console plugin with the HOL AI Plugin Scanner |
| https://github.com/aeonfun/aeon/pull/919 | `aeonfun/aeon` | `code_only` | `typescript` | feat: Codex plugin + repo llms.txt |
| https://github.com/aeonfun/aeon/pull/921 | `aeonfun/aeon` | `code_and_docs` | `typescript` | fix(scorer): grade full output, align to strategy, flag fabrication |
| https://github.com/aeonfun/aeon/pull/920 | `aeonfun/aeon` | `code_only` | `typescript` | fix(dashboard): keep feed card content inside its box |
| https://github.com/aeonfun/aeon/pull/917 | `aeonfun/aeon` | `code_only` | `typescript` | security: SHA-pin all GitHub Actions to immutable commit refs |
| https://github.com/aeonfun/aeon/pull/916 | `aeonfun/aeon` | `code_and_docs` | `typescript` | feat(harness-adapter): generated capability manifest (harnesses.json) |
| https://github.com/aeonfun/aeon/pull/904 | `aeonfun/aeon` | `code_only` | `typescript` | fix(security): narrow messages.yml ALL_SECRETS to named allowlist |
| https://github.com/aeonfun/aeon/pull/898 | `aeonfun/aeon` | `code_only` | `typescript` | fix(aeon.yml): rm ./secretcurl before commit like ./notify |
| https://github.com/aeonfun/aeon/pull/896 | `aeonfun/aeon` | `code_only` | `typescript` | fix: unbreak main CI (stale harness-resolution test + eyebrow lockfile drift) |
| https://github.com/aeonfun/aeon/pull/890 | `aeonfun/aeon` | `code_and_docs` | `typescript` | fix(vuln-tracker,vuln-scanner): port scan-history, PR-match, and osv-scanner robustness from aeon-vuln |
| https://github.com/aeonfun/aeon/pull/895 | `aeonfun/aeon` | `code_and_docs` | `typescript` | feat(vuln-scanner): DoH MX/A deliverability gate before autonomous disclosure email |
| https://github.com/aeonfun/aeon/pull/894 | `aeonfun/aeon` | `code_and_docs` | `typescript` | feat(vuln-scanner): add A3.6 agentic logic audit alongside the fuzz pass |
| https://github.com/aeonfun/aeon/pull/893 | `aeonfun/aeon` | `code_and_docs` | `typescript` | chore: switch Opus pins from opus-5 to opus-4-8 |
| https://github.com/aeonfun/aeon/pull/891 | `aeonfun/aeon` | `code_and_docs` | `typescript` | chore: refresh hardcoded model pins to current generation |
| https://github.com/aeonfun/aeon/pull/889 | `aeonfun/aeon` | `code_and_docs` | `typescript` | fix(skill-icons): add taskmarket-delegate glyph |
| https://github.com/aeonfun/aeon/pull/887 | `aeonfun/aeon` | `code_only` | `typescript` | ci: add PR-scoped concurrency to lint/check workflows |
| https://github.com/aeonfun/aeon/pull/886 | `aeonfun/aeon` | `code_only` | `typescript` | refactor: ponytail-audit verified dead-code cuts (net -444) |
| https://github.com/aeonfun/aeon/pull/885 | `aeonfun/aeon` | `code_and_docs` | `typescript` | docs: document the aeon setup skill as an installable Claude Code plugin |
| https://github.com/aeonfun/aeon/pull/884 | `aeonfun/aeon` | `code_and_docs` | `typescript` | feat: package aeon operator skill as a Claude Code plugin |
| https://github.com/aeonfun/aeon/pull/882 | `aeonfun/aeon` | `code_only` | `typescript` | fix: pi/openrouter onboarding (CLI tsx runtime + dashboard run-gate) |
| https://github.com/aeonfun/aeon/pull/871 | `aeonfun/aeon` | `code_only` | `typescript` | fix(deps): patch nanoid security advisories |
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
| https://github.com/ansible/ansible-runner/pull/1393 | `ansible/ansible-runner` | `code_and_docs` | `python` | Docs: remove IRC remnants |
| https://github.com/ansible/ansible-runner/pull/1385 | `ansible/ansible-runner` | `code_only` | `python` | Move setuptools upperbound to most recent version |
| https://github.com/ansible/ansible-runner/pull/1379 | `ansible/ansible-runner` | `code_only` | `python` | Add Python 3.13 testing |
| https://github.com/ansible/ansible-runner/pull/1375 | `ansible/ansible-runner` | `code_only` | `python` | [backport] Fix roles_path type in docstring (#1373) |
| https://github.com/ansible/ansible-runner/pull/1373 | `ansible/ansible-runner` | `code_only` | `python` | Fix roles_path type in docstring |
| https://github.com/ansible/ansible-runner/pull/1372 | `ansible/ansible-runner` | `code_only` | `python` | Update CI action versions (#1370) |
| https://github.com/ansible/ansible-runner/pull/1370 | `ansible/ansible-runner` | `code_only` | `python` | Update CI action versions |
| https://github.com/ansible/ansible-runner/pull/1368 | `ansible/ansible-runner` | `code_only_tests_or_fixtures` | `python` | [backport][release_2.4] Update core integration testing versions (#1360) |
| https://github.com/ansible/ansible-runner/pull/1360 | `ansible/ansible-runner` | `code_only_tests_or_fixtures` | `python` | Update core integration testing versions |
| https://github.com/ansible/ansible-runner/pull/1364 | `ansible/ansible-runner` | `code_only` | `python` | [backport][release_2.4] Fix test for get_role_list and bump setuptools/setuptools_scm (#1361)(#1365) |
| https://github.com/ansible/ansible-runner/pull/1363 | `ansible/ansible-runner` | `code_only_tests_or_fixtures` | `python` | [backport][release_2.3] Fix test for get_role_list (#1361) |
| https://github.com/ansible/ansible-runner/pull/1365 | `ansible/ansible-runner` | `code_only` | `python` | Bump setuptools and setuptools_scm |
| https://github.com/ansible/ansible-runner/pull/1361 | `ansible/ansible-runner` | `code_only_tests_or_fixtures` | `python` | Fix test for get_role_list |
| https://github.com/ansible/ansible-runner/pull/1357 | `ansible/ansible-runner` | `code_only` | `python` | Remove CodeCov upload from CI |
| https://github.com/ansible/ansible-runner/pull/1348 | `ansible/ansible-runner` | `code_only` | `python` | Add Python 3.12 testing |
| https://github.com/ansible/ansible-runner/pull/1342 | `ansible/ansible-runner` | `code_only` | `python` | Untag instead of force remove image for podman |
| https://github.com/ansible/ansible-runner/pull/1344 | `ansible/ansible-runner` | `code_only` | `python` | Untag instead of force remove image for podman (#1342) |
| https://github.com/ansible/ansible-runner/pull/1336 | `ansible/ansible-runner` | `code_only` | `python` | [backport][2.3] fix pexpect child shutdown race (#1331) |
| https://github.com/ansible/ansible-runner/pull/1334 | `ansible/ansible-runner` | `code_only_tests_or_fixtures` | `python` | Add runner tests from ansible core test suite |
| https://github.com/ansible/ansible-runner/pull/1331 | `ansible/ansible-runner` | `code_only` | `python` | fix pexpect child shutdown race |
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
| https://github.com/astral-sh/ty/pull/3928 | `astral-sh/ty` | `code_only` | `python` | Update actions/attest-build-provenance action to v4.1.1 |
| https://github.com/astral-sh/ty/pull/3930 | `astral-sh/ty` | `code_only` | `python` | Update actions/cache action to v6.1.0 - autoclosed |
| https://github.com/astral-sh/ty/pull/3931 | `astral-sh/ty` | `code_only` | `python` | Update actions/setup-python action to v6.3.0 |
| https://github.com/astral-sh/ty/pull/3929 | `astral-sh/ty` | `code_only` | `python` | Update prek dependencies |
| https://github.com/astral-sh/ty/pull/3932 | `astral-sh/ty` | `code_only` | `python` | Update astral-sh/setup-uv action to v8.3.1 |
| https://github.com/astral-sh/ty/pull/3911 | `astral-sh/ty` | `code_and_docs` | `python` | Fix trailing whitespace |
| https://github.com/astral-sh/ty/pull/3897 | `astral-sh/ty` | `code_and_docs` | `python` | chore: pin pre-commit refs and lock prek in CI |
| https://github.com/astral-sh/ty/pull/3901 | `astral-sh/ty` | `code_only` | `python` | Revert "Revert "Use ICF for macOS release builds"" |
| https://github.com/astral-sh/ty/pull/3900 | `astral-sh/ty` | `code_only` | `python` | Revert "Use ICF for macOS release builds" |
| https://github.com/astral-sh/ty/pull/3709 | `astral-sh/ty` | `code_only` | `python` | Use ICF for macOS release builds |
| https://github.com/astral-sh/ty/pull/3895 | `astral-sh/ty` | `code_and_docs` | `python` | Bump version to 0.0.56 |
| https://github.com/astral-sh/ty/pull/3883 | `astral-sh/ty` | `code_only` | `python` | Update maturin to v1.14.1 |
| https://github.com/astral-sh/ty/pull/3884 | `astral-sh/ty` | `code_only` | `python` | Update prek dependencies |
| https://github.com/astral-sh/ty/pull/3885 | `astral-sh/ty` | `code_only` | `python` | Update actions/cache action to v6 |
| https://github.com/astral-sh/ty/pull/3886 | `astral-sh/ty` | `code_only` | `python` | Update actions/checkout action to v7 |
| https://github.com/astral-sh/ty/pull/3866 | `astral-sh/ty` | `code_and_docs` | `python` | Bump version to 0.0.55 |
| https://github.com/astral-sh/ty/pull/3856 | `astral-sh/ty` | `code_and_docs` | `python` | Bump version to 0.0.54 |
| https://github.com/astral-sh/ty/pull/3840 | `astral-sh/ty` | `code_only` | `python` | Update maturin to v1.14.0 |
| https://github.com/astral-sh/ty/pull/3839 | `astral-sh/ty` | `code_only` | `python` | Update prek dependencies |
| https://github.com/astral-sh/ty/pull/3841 | `astral-sh/ty` | `code_and_docs` | `python` | Bump version to 0.0.53 |
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
| https://github.com/callstack/agent-device/pull/2069 | `callstack/agent-device` | `code_only` | `typescript` | fix(ci): spawn the differential's agent-device CLI as argv, not one option |
| https://github.com/callstack/agent-device/pull/2075 | `callstack/agent-device` | `code_only` | `typescript` | fix(daemon): keep the recovery hint on Maestro replay errors |
| https://github.com/callstack/agent-device/pull/2057 | `callstack/agent-device` | `code_only` | `typescript` | fix(daemon): reconcile device claims held by a replaced daemon |
| https://github.com/callstack/agent-device/pull/2055 | `callstack/agent-device` | `code_and_docs` | `typescript` | fix(fuzz): run parser cases in a worker process, not the runner's thread (#2053) |
| https://github.com/callstack/agent-device/pull/2060 | `callstack/agent-device` | `code_only` | `typescript` | perf(apple): reuse booted simulator memo during open |
| https://github.com/callstack/agent-device/pull/2058 | `callstack/agent-device` | `code_only` | `typescript` | perf(apple): uninstall stale runner bundles concurrently |
| https://github.com/callstack/agent-device/pull/2056 | `callstack/agent-device` | `code_only` | `typescript` | perf(diagnostics): reuse redaction and directory work per scope |
| https://github.com/callstack/agent-device/pull/2052 | `callstack/agent-device` | `code_only` | `typescript` | refactor(android): one injectable host-adb transport for the remaining raw adb sites |
| https://github.com/callstack/agent-device/pull/2051 | `callstack/agent-device` | `code_only` | `typescript` | perf(harmonyos): memoize gesture viewport dumps |
| https://github.com/callstack/agent-device/pull/2035 | `callstack/agent-device` | `code_only` | `typescript` | fix(ios): grant the text-entry commit wait time against progress |
| https://github.com/callstack/agent-device/pull/2044 | `callstack/agent-device` | `code_and_docs` | `typescript` | refactor(android): extract the adb executor and IME cluster into packages/platform-android (#2041) |
| https://github.com/callstack/agent-device/pull/2046 | `callstack/agent-device` | `code_and_docs` | `typescript` | refactor: remove next-major compatibility surfaces |
| https://github.com/callstack/agent-device/pull/2049 | `callstack/agent-device` | `code_and_docs` | `typescript` | test(perf): raise local Vitest worker cap to four |
| https://github.com/callstack/agent-device/pull/2047 | `callstack/agent-device` | `code_only` | `typescript` | refactor(registry): flip react-devtools to none (Wave 6 residue, part of #2042) |
| https://github.com/callstack/agent-device/pull/2036 | `callstack/agent-device` | `code_only_tests_or_fixtures` | `typescript` | fix(ci): skip release instead of erroring when both fixtures are cached |
| https://github.com/callstack/agent-device/pull/2033 | `callstack/agent-device` | `code_and_docs` | `typescript` | fix(web): launch npm and the managed backend through node, not .cmd shims |
| https://github.com/callstack/agent-device/pull/2029 | `callstack/agent-device` | `code_only` | `typescript` | fix(daemon): close no longer throws tenant-isolation error on a never-allocated lease |
| https://github.com/callstack/agent-device/pull/2015 | `callstack/agent-device` | `code_only` | `typescript` | fix(daemon): stop branch-named daemon before replacement |
| https://github.com/callstack/agent-device/pull/2004 | `callstack/agent-device` | `code_only` | `typescript` | perf(daemon): revalidate the source code-signature cache by stat instead of rereading the graph |
| https://github.com/callstack/agent-device/pull/2023 | `callstack/agent-device` | `code_and_docs` | `typescript` | Harden the MCP surface: registry rug-pull fix, operator-only credentials/endpoints, device-shell argv gate, declared timeouts |
| https://github.com/callstack/agent-device/pull/2020 | `callstack/agent-device` | `code_and_docs` | `typescript` | feat: add deterministic device selection resolver |
| https://github.com/KyaniteLabs/kinocut/pull/490 | `kyanitelabs/kinocut` | `code_and_docs` | `python` | fix: CI lint-drift pin + CodeRabbit review residue (#473/#472/#457) |
| https://github.com/KyaniteLabs/kinocut/pull/491 | `kyanitelabs/kinocut` | `code_only` | `python` | fix(bundle): writer validates metadata under the verifier's contract |
| https://github.com/KyaniteLabs/kinocut/pull/473 | `kyanitelabs/kinocut` | `code_and_docs` | `python` | feat(revideo): bridge engine, pinned template, and winners-bundle envelope v0.1 |
| https://github.com/KyaniteLabs/kinocut/pull/489 | `kyanitelabs/kinocut` | `code_only` | `python` | feat(envelope): agreed license + judges fields for winners-bundle v0.1 |
| https://github.com/KyaniteLabs/kinocut/pull/475 | `kyanitelabs/kinocut` | `code_only` | `python` | fix(ffmpeg): POSIX filter-path escaping — quoted single-pass form |
| https://github.com/KyaniteLabs/kinocut/pull/472 | `kyanitelabs/kinocut` | `code_and_docs` | `python` | fix(release): complete the 1.15.1 version-constellation sweep |
| https://github.com/KyaniteLabs/kinocut/pull/469 | `kyanitelabs/kinocut` | `code_and_docs` | `python` | ci(publish): republish legacy io.github.KyaniteLabs/mcp-video registry entry |
| https://github.com/KyaniteLabs/kinocut/pull/460 | `kyanitelabs/kinocut` | `code_only` | `python` | feat(windows): contention-only lock contract + Windows CI smoke job |
| https://github.com/KyaniteLabs/kinocut/pull/458 | `kyanitelabs/kinocut` | `code_only` | `python` | fix(windows): escape filter-option paths for both FFmpeg unescaping passes |
| https://github.com/KyaniteLabs/kinocut/pull/459 | `kyanitelabs/kinocut` | `code_only` | `python` | fix(doctor): reject unsupported Python versions on PATH |
| https://github.com/KyaniteLabs/kinocut/pull/457 | `kyanitelabs/kinocut` | `code_and_docs` | `python` | release: Kinocut 1.15.0 (honest diagnostics + community-driven release) |
| https://github.com/KyaniteLabs/kinocut/pull/456 | `kyanitelabs/kinocut` | `code_only_tests_or_fixtures` | `python` | test: skip shebang-stub tests explicitly on Windows |
| https://github.com/KyaniteLabs/kinocut/pull/455 | `kyanitelabs/kinocut` | `code_only` | `python` | fix: doctor verifies the MCP server import path |
| https://github.com/KyaniteLabs/kinocut/pull/454 | `kyanitelabs/kinocut` | `code_only` | `python` | fix: surface real import failures in MCP mode entry |
| https://github.com/KyaniteLabs/kinocut/pull/444 | `kyanitelabs/kinocut` | `code_and_docs` | `python` | feat: 360 dual-cam assembly for Insta360 X4 exports |
| https://github.com/KyaniteLabs/kinocut/pull/442 | `kyanitelabs/kinocut` | `code_and_docs` | `python` | feat: Wave 3 lazy import + ship-seam honesty |
| https://github.com/KyaniteLabs/kinocut/pull/441 | `kyanitelabs/kinocut` | `code_and_docs` | `python` | feat: finish half-built compilers into product surfaces |
| https://github.com/KyaniteLabs/kinocut/pull/440 | `kyanitelabs/kinocut` | `code_and_docs` | `python` | feat: wishlist residuals + optional depth + Renovate/light CI ops |
| https://github.com/KyaniteLabs/kinocut/pull/439 | `kyanitelabs/kinocut` | `code_and_docs` | `python` | ultragoal: residual portfolio closeout (mirror of Forgejo #373) |
| https://github.com/KyaniteLabs/kinocut/pull/426 | `kyanitelabs/kinocut` | `code_only` | `python` | feat: mutate shorts plans with fail-closed review decisions |
| https://github.com/KyaniteLabs/kinocut/pull/425 | `kyanitelabs/kinocut` | `code_only` | `python` | feat: persist exact shorts review plans |
| https://github.com/KyaniteLabs/kinocut/pull/424 | `kyanitelabs/kinocut` | `code_only` | `python` | feat: package approved shorts with verified provenance |
| https://github.com/KyaniteLabs/kinocut/pull/423 | `kyanitelabs/kinocut` | `code_only` | `python` | feat: define deterministic shorts package contracts |
| https://github.com/KyaniteLabs/kinocut/pull/422 | `kyanitelabs/kinocut` | `code_only` | `python` | feat: fade audio edit boundaries before normalization |
| https://github.com/KyaniteLabs/kinocut/pull/420 | `kyanitelabs/kinocut` | `code_only` | `python` | feat: block unsafe caption placements |
| https://github.com/KyaniteLabs/kinocut/pull/419 | `kyanitelabs/kinocut` | `code_only` | `python` | feat: generate editable phrase captions |
| https://github.com/KyaniteLabs/kinocut/pull/418 | `kyanitelabs/kinocut` | `code_only` | `python` | feat: define truthful caption timing contracts |
| https://github.com/KyaniteLabs/kinocut/pull/417 | `kyanitelabs/kinocut` | `code_only` | `python` | feat: enrich candidate editorial evidence |
| https://github.com/KyaniteLabs/kinocut/pull/416 | `kyanitelabs/kinocut` | `code_only` | `python` | feat: discover bounded transcript moments |
| https://github.com/KyaniteLabs/kinocut/pull/415 | `kyanitelabs/kinocut` | `code_only` | `python` | feat: orchestrate replay-safe long-form transcription |
| https://github.com/KyaniteLabs/kinocut/pull/414 | `kyanitelabs/kinocut` | `code_only` | `python` | feat: merge long-form transcript overlaps truthfully |
| https://github.com/KyaniteLabs/kinocut/pull/413 | `kyanitelabs/kinocut` | `code_only` | `python` | feat: transcribe bounded long-form audio chunks |
| https://github.com/KyaniteLabs/kinocut/pull/412 | `kyanitelabs/kinocut` | `code_only` | `python` | feat: plan complete long-form transcription coverage |
| https://github.com/KyaniteLabs/kinocut/pull/411 | `kyanitelabs/kinocut` | `code_only` | `python` | feat: establish long-form transcription boundaries |
| https://github.com/KyaniteLabs/kinocut/pull/410 | `kyanitelabs/kinocut` | `code_only` | `python` | feat: centralize shorts configuration contracts |
| https://github.com/KyaniteLabs/kinocut/pull/409 | `kyanitelabs/kinocut` | `code_only` | `python` | feat: define strict stream candidate contracts |
| https://github.com/KyaniteLabs/kinocut/pull/421 | `kyanitelabs/kinocut` | `code_only` | `python` | fix: measure audio before loudness normalization |
| https://github.com/KyaniteLabs/kinocut/pull/408 | `kyanitelabs/kinocut` | `code_only` | `python` | feat: enforce Shorts and Reels duration budgets |
| https://github.com/KyaniteLabs/kinocut/pull/369 | `kyanitelabs/kinocut` | `code_and_docs` | `python` | Release Kinocut 1.8.0 |
| https://github.com/KyaniteLabs/kinocut/pull/371 | `kyanitelabs/kinocut` | `code_and_docs` | `python` | docs: flip public claims and marketing to published Kinocut 1.8.0 |
| https://github.com/KyaniteLabs/kinocut/pull/397 | `kyanitelabs/kinocut` | `code_and_docs` | `python` | docs: make GitHub the external contribution surface |
| https://github.com/KyaniteLabs/kinocut/pull/395 | `kyanitelabs/kinocut` | `code_only` | `python` | cli: add collision-safe edit namespace aliases |
| https://github.com/KyaniteLabs/kinocut/pull/394 | `kyanitelabs/kinocut` | `code_only` | `python` | cli: add QA namespace aliases |
| https://github.com/KyaniteLabs/kinocut/pull/393 | `kyanitelabs/kinocut` | `code_only` | `python` | cli: add audio namespace aliases |
| https://github.com/KyaniteLabs/kinocut/pull/389 | `kyanitelabs/kinocut` | `code_only` | `python` | cli: wire reserved-prefix router and aivideo aliases |
| https://github.com/KyaniteLabs/kinocut/pull/387 | `kyanitelabs/kinocut` | `code_and_docs` | `python` | feat: expose guarded audio-bed public workflow |
| https://github.com/KyaniteLabs/kinocut/pull/386 | `kyanitelabs/kinocut` | `code_only` | `python` | ci: promote Hyperframes integration to required gate |
| https://github.com/KyaniteLabs/kinocut/pull/384 | `kyanitelabs/kinocut` | `code_only` | `python` | ci: restore Node and FFmpeg matrix compatibility |
| https://github.com/KyaniteLabs/kinocut/pull/380 | `kyanitelabs/kinocut` | `code_only` | `python` | fix(hyperframes): restore skip-transcribe contract |
| https://github.com/KyaniteLabs/kinocut/pull/382 | `kyanitelabs/kinocut` | `code_only` | `python` | ci: restore repository-wide Ruff format baseline |
| https://github.com/KyaniteLabs/kinocut/pull/370 | `kyanitelabs/kinocut` | `code_only` | `python` | fix(release): exclude docs/ from sdist so 1.8.0 publish can land |
| https://github.com/KyaniteLabs/kinocut/pull/368 | `kyanitelabs/kinocut` | `code_and_docs` | `python` | docs: usage metrics, design interview, tastecheck ledger |
| https://github.com/KyaniteLabs/kinocut/pull/365 | `kyanitelabs/kinocut` | `code_and_docs` | `python` | feat: golden path, demo pack, and public claim-drift CI |
| https://github.com/KyaniteLabs/kinocut/pull/361 | `kyanitelabs/kinocut` | `code_and_docs` | `python` | fix(hyperframes): prevent init from hanging under MCP (no TTY) |
| https://github.com/KyaniteLabs/kinocut/pull/348 | `kyanitelabs/kinocut` | `code_and_docs` | `python` | fix: unblock uv security resolution |
| https://github.com/KyaniteLabs/kinocut/pull/346 | `kyanitelabs/kinocut` | `code_and_docs` | `python` | Fix Glama build metadata |
| https://github.com/KyaniteLabs/kinocut/pull/345 | `kyanitelabs/kinocut` | `code_only` | `python` | Improve public MCP tool metadata for Glama scoring |
| https://github.com/KyaniteLabs/kinocut/pull/344 | `kyanitelabs/kinocut` | `code_and_docs` | `python` | chore: prepare v1.5.0 release |
| https://github.com/KyaniteLabs/kinocut/pull/343 | `kyanitelabs/kinocut` | `code_only` | `python` | build(deps): bump actions/checkout from 6.0.2 to 6.0.3 in the github-actions group |
| https://github.com/KyaniteLabs/kinocut/pull/342 | `kyanitelabs/kinocut` | `code_and_docs` | `python` | docs: add mcp-video confidence proof workflows |
| https://github.com/KyaniteLabs/kinocut/pull/341 | `kyanitelabs/kinocut` | `code_and_docs` | `python` | docs: add public mcp-video agent skill |
| https://github.com/KyaniteLabs/kinocut/pull/336 | `kyanitelabs/kinocut` | `code_only` | `python` | Fix CheckYourself mcp-video findings |
| https://github.com/KyaniteLabs/kinocut/pull/330 | `kyanitelabs/kinocut` | `code_only` | `python` | Make v1.4.1 registry metadata publishable |
| https://github.com/KyaniteLabs/kinocut/pull/328 | `kyanitelabs/kinocut` | `code_only` | `python` | Fix 1.4.1 base import without NumPy |
| https://github.com/KyaniteLabs/kinocut/pull/324 | `kyanitelabs/kinocut` | `code_and_docs` | `python` | chore: address review followups before 1.4.1 release |
| https://github.com/KyaniteLabs/kinocut/pull/320 | `kyanitelabs/kinocut` | `code_and_docs` | `python` | feat: text overlay guardrails, MiniMax music, expanded fonts, audio engine rewrite |
| https://github.com/KyaniteLabs/kinocut/pull/319 | `kyanitelabs/kinocut` | `code_only` | `python` | Repair Hyperframes composition frames from HTML duration |
| https://github.com/KyaniteLabs/kinocut/pull/318 | `kyanitelabs/kinocut` | `code_and_docs` | `python` | Pin Hyperframes command resolution |
| https://github.com/KyaniteLabs/kinocut/pull/317 | `kyanitelabs/kinocut` | `code_only` | `python` | Unblock Hyperframes NucBox dogfood |
| https://github.com/KyaniteLabs/kinocut/pull/313 | `kyanitelabs/kinocut` | `code_and_docs` | `python` | Expose Hyperframes runtime data across public tools |
| https://github.com/KyaniteLabs/kinocut/pull/312 | `kyanitelabs/kinocut` | `code_only` | `python` | fix: video-quality-check handles silent videos and renders report |
| https://github.com/KyaniteLabs/kinocut/pull/310 | `kyanitelabs/kinocut` | `code_only` | `python` | [codex] Fix FPS handling for image sequences and HyperFrames |
| https://github.com/KyaniteLabs/kinocut/pull/308 | `kyanitelabs/kinocut` | `code_only` | `python` | Enable CodeRabbit public OSS review config |
| https://github.com/KyaniteLabs/kinocut/pull/305 | `kyanitelabs/kinocut` | `code_only` | `python` | Fix design-quality scoring for audio-first videos |
| https://github.com/KyaniteLabs/kinocut/pull/304 | `kyanitelabs/kinocut` | `code_only` | `python` | Harden public release workflow trust boundaries |
| https://github.com/KyaniteLabs/kinocut/pull/299 | `kyanitelabs/kinocut` | `code_only` | `python` | build(deps): bump actions/checkout from 4 to 6 in the github-actions group |
| https://github.com/KyaniteLabs/kinocut/pull/298 | `kyanitelabs/kinocut` | `code_only` | `python` | Add 12 CRUSH glitch video effects |
| https://github.com/KyaniteLabs/kinocut/pull/296 | `kyanitelabs/kinocut` | `code_and_docs` | `python` | Add agent-law workflow and supporting files |
| https://github.com/KyaniteLabs/kinocut/pull/294 | `kyanitelabs/kinocut` | `code_only` | `python` | Bump server.json to 1.4.0 |
| https://github.com/KyaniteLabs/kinocut/pull/293 | `kyanitelabs/kinocut` | `code_and_docs` | `python` | Release v1.4.0 |
| https://github.com/statelyai/agent/pull/112 | `statelyai/agent` | `code_and_docs` | `typescript` | Version Packages (alpha) |
| https://github.com/statelyai/agent/pull/111 | `statelyai/agent` | `code_and_docs` | `typescript` | Fix four API contract defects |
| https://github.com/statelyai/agent/pull/110 | `statelyai/agent` | `code_and_docs` | `typescript` | Version Packages (alpha) |
| https://github.com/statelyai/agent/pull/109 | `statelyai/agent` | `code_and_docs` | `typescript` | Bring frameworks, integrations, and examples up to date |
| https://github.com/statelyai/agent/pull/106 | `statelyai/agent` | `code_and_docs` | `typescript` | Verification upgrades + four new examples (chameleon, just-one, seam-scoring, snapshot-migration) |
| https://github.com/statelyai/agent/pull/104 | `statelyai/agent` | `code_and_docs` | `typescript` | Durable timer support for runDurableAgent |
| https://github.com/statelyai/agent/pull/103 | `statelyai/agent` | `code_and_docs` | `typescript` | Upgrade to xstate 6.0.0-alpha.46; lean on the execution's own waitForEvent |
| https://github.com/statelyai/agent/pull/101 | `statelyai/agent` | `code_and_docs` | `typescript` | Upgrade to xstate 6.0.0-alpha.43; pin executionId instead of rebinding sessions |
| https://github.com/statelyai/agent/pull/100 | `statelyai/agent` | `code_and_docs` | `typescript` | Version Packages (alpha) |
| https://github.com/statelyai/agent/pull/99 | `statelyai/agent` | `code_and_docs` | `typescript` | Upgrade to xstate 6.0.0-alpha.41 and add runDurableAgent on xstate/durable |
| https://github.com/statelyai/agent/pull/97 | `statelyai/agent` | `code_and_docs` | `typescript` | Version Packages (alpha) |
| https://github.com/statelyai/agent/pull/95 | `statelyai/agent` | `code_and_docs` | `typescript` | Version Packages (alpha) |
| https://github.com/statelyai/agent/pull/94 | `statelyai/agent` | `code_and_docs` | `typescript` | Version Packages (alpha) |
| https://github.com/statelyai/agent/pull/93 | `statelyai/agent` | `code_only` | `typescript` | Enable machine-carried isSuspended in game-loop-agent; add suspension registry guard |
| https://github.com/statelyai/agent/pull/92 | `statelyai/agent` | `code_and_docs` | `typescript` | Add suspension predicate support to setupAgent.fromConfig |
| https://github.com/statelyai/agent/pull/91 | `statelyai/agent` | `code_and_docs` | `typescript` | Version Packages (alpha) |
| https://github.com/statelyai/agent/pull/89 | `statelyai/agent` | `code_and_docs` | `typescript` | Version Packages (alpha) |
| https://github.com/statelyai/agent/pull/88 | `statelyai/agent` | `code_and_docs` | `typescript` | Validate machine input against its schema; add chat-with-pdf example |
| https://github.com/statelyai/agent/pull/87 | `statelyai/agent` | `code_and_docs` | `typescript` | Version Packages (alpha) |
| https://github.com/statelyai/agent/pull/86 | `statelyai/agent` | `code_and_docs` | `typescript` | Version Packages (alpha) |
| https://github.com/statelyai/agent/pull/85 | `statelyai/agent` | `code_and_docs` | `typescript` | Fix inspector protocol integration |
| https://github.com/statelyai/agent/pull/83 | `statelyai/agent` | `code_and_docs` | `typescript` | Version Packages (alpha) |
| https://github.com/statelyai/agent/pull/82 | `statelyai/agent` | `code_only` | `typescript` | Bump vitest from 2.1.9 to 3.2.6 |
| https://github.com/statelyai/agent/pull/81 | `statelyai/agent` | `code_and_docs` | `typescript` | Version Packages (alpha) |
| https://github.com/statelyai/agent/pull/80 | `statelyai/agent` | `code_and_docs` | `typescript` | Version Packages (alpha) |
| https://github.com/statelyai/agent/pull/79 | `statelyai/agent` | `code_and_docs` | `typescript` | Version Packages (alpha) |
| https://github.com/statelyai/agent/pull/78 | `statelyai/agent` | `code_and_docs` | `typescript` | Version Packages (alpha) |
| https://github.com/statelyai/agent/pull/77 | `statelyai/agent` | `code_and_docs` | `typescript` | Version Packages (alpha) |
| https://github.com/statelyai/agent/pull/75 | `statelyai/agent` | `code_and_docs` | `typescript` | Version Packages (alpha) |
| https://github.com/statelyai/agent/pull/74 | `statelyai/agent` | `code_and_docs` | `typescript` | Version Packages (alpha) |
| https://github.com/statelyai/agent/pull/73 | `statelyai/agent` | `code_and_docs` | `typescript` | Version Packages (alpha) |
| https://github.com/statelyai/agent/pull/72 | `statelyai/agent` | `code_and_docs` | `typescript` | Version Packages (alpha) |
| https://github.com/statelyai/agent/pull/71 | `statelyai/agent` | `code_and_docs` | `typescript` | Version Packages (alpha) |
| https://github.com/statelyai/agent/pull/69 | `statelyai/agent` | `code_and_docs` | `typescript` | Version Packages (alpha) |
| https://github.com/statelyai/agent/pull/70 | `statelyai/agent` | `code_and_docs` | `typescript` | DX P0: executor inheritance, wait tags, resume validation, canonical form |
| https://github.com/statelyai/agent/pull/60 | `statelyai/agent` | `code_only` | `typescript` | Exposes strategies in package |
| https://github.com/statelyai/agent/pull/51 | `statelyai/agent` | `code_and_docs` | `typescript` | Middleware |
| https://github.com/statelyai/agent/pull/55 | `statelyai/agent` | `code_and_docs` | `typescript` | Version Packages |
| https://github.com/statelyai/agent/pull/54 | `statelyai/agent` | `code_and_docs` | `typescript` | Explicitely copy AsyncIterator |
| https://github.com/statelyai/agent/pull/50 | `statelyai/agent` | `code_and_docs` | `typescript` | Version Packages |
| https://github.com/statelyai/agent/pull/49 | `statelyai/agent` | `code_and_docs` | `typescript` | Update `ai` (changeset test) |
| https://github.com/statelyai/agent/pull/48 | `statelyai/agent` | `code_and_docs` | `typescript` | Version Packages |
| https://github.com/statelyai/agent/pull/47 | `statelyai/agent` | `code_and_docs` | `typescript` | Update `ai` and `xstate` packages |
| https://github.com/statelyai/agent/pull/46 | `statelyai/agent` | `code_and_docs` | `typescript` | Version Packages |
| https://github.com/statelyai/agent/pull/45 | `statelyai/agent` | `code_and_docs` | `typescript` | Fix reading actor logic |
| https://github.com/statelyai/agent/pull/44 | `statelyai/agent` | `code_and_docs` | `typescript` | Version Packages |
| https://github.com/statelyai/agent/pull/43 | `statelyai/agent` | `code_and_docs` | `typescript` | Update dependencies |
| https://github.com/statelyai/agent/pull/42 | `statelyai/agent` | `code_and_docs` | `typescript` | Version Packages |
| https://github.com/statelyai/agent/pull/41 | `statelyai/agent` | `code_and_docs` | `typescript` | Update dependencies |
| https://github.com/statelyai/agent/pull/34 | `statelyai/agent` | `code_and_docs` | `typescript` | Version Packages |
| https://github.com/statelyai/agent/pull/40 | `statelyai/agent` | `code_and_docs` | `typescript` | Correlation ID |
| https://github.com/statelyai/agent/pull/37 | `statelyai/agent` | `code_and_docs` | `typescript` | Support messages in decision |
| https://github.com/statelyai/agent/pull/39 | `statelyai/agent` | `code_and_docs` | `typescript` | Add simpler agent context retrieval functions |
| https://github.com/statelyai/agent/pull/38 | `statelyai/agent` | `code_and_docs` | `typescript` | Add `context` field in agent |
| https://github.com/statelyai/agent/pull/35 | `statelyai/agent` | `code_only` | `typescript` | Use built-in ID function |
| https://github.com/statelyai/agent/pull/27 | `statelyai/agent` | `code_and_docs` | `typescript` | Version Packages |
| https://github.com/statelyai/agent/pull/32 | `statelyai/agent` | `code_and_docs` | `typescript` | Release 0.1 |
| https://github.com/statelyai/agent/pull/31 | `statelyai/agent` | `code_only` | `typescript` | More Agent API work |
| https://github.com/statelyai/agent/pull/30 | `statelyai/agent` | `code_and_docs` | `typescript` | API improvements, continued |
| https://github.com/statelyai/agent/pull/29 | `statelyai/agent` | `code_only` | `typescript` | More agent tweaks |
| https://github.com/statelyai/agent/pull/28 | `statelyai/agent` | `code_and_docs` | `typescript` | AI |
| https://github.com/statelyai/agent/pull/26 | `statelyai/agent` | `code_and_docs` | `typescript` | RL framework experimentation |
| https://github.com/statelyai/agent/pull/25 | `statelyai/agent` | `code_only` | `typescript` | Add newspaper example |
| https://github.com/statelyai/agent/pull/23 | `statelyai/agent` | `code_and_docs` | `typescript` | Version Packages |
| https://github.com/statelyai/agent/pull/22 | `statelyai/agent` | `code_and_docs` | `typescript` | Simplify event choices |
| https://github.com/statelyai/agent/pull/20 | `statelyai/agent` | `code_and_docs` | `typescript` | Version Packages |
| https://github.com/statelyai/agent/pull/18 | `statelyai/agent` | `code_and_docs` | `typescript` | Word guesser example |
| https://github.com/statelyai/agent/pull/17 | `statelyai/agent` | `code_and_docs` | `typescript` | Version Packages |
| https://github.com/statelyai/agent/pull/13 | `statelyai/agent` | `code_only` | `typescript` | Cleanup + add numberGuesser example |
| https://github.com/statelyai/agent/pull/16 | `statelyai/agent` | `code_and_docs` | `typescript` | Update to XState 5.8.0 |
| https://github.com/statelyai/agent/pull/11 | `statelyai/agent` | `code_only` | `typescript` | Create `vitest.config`, loading `dotenv` and set a higher global test timeout |
| https://github.com/statelyai/agent/pull/10 | `statelyai/agent` | `code_and_docs` | `typescript` | Version Packages |
| https://github.com/statelyai/agent/pull/9 | `statelyai/agent` | `code_and_docs` | `typescript` | Add tool choice |
| https://github.com/statelyai/agent/pull/8 | `statelyai/agent` | `code_and_docs` | `typescript` | Version Packages |
| https://github.com/statelyai/agent/pull/5 | `statelyai/agent` | `code_and_docs` | `typescript` | API updates |
| https://github.com/statelyai/agent/pull/4 | `statelyai/agent` | `code_and_docs` | `typescript` | Version Packages |
| https://github.com/statelyai/agent/pull/3 | `statelyai/agent` | `code_only` | `typescript` | Setup Changesets action |
| https://github.com/statelyai/agent/pull/1 | `statelyai/agent` | `code_and_docs` | `typescript` | Example runner |
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
| https://github.com/ColeMurray/background-agents/pull/1619 | `colemurray/background-agents` | `code_only` | `typescript` | fix(control-plane): show automation children in Mine |
| https://github.com/ColeMurray/background-agents/pull/1617 | `colemurray/background-agents` | `code_only` | `typescript` | chore(control-plane): define DEFAULT_BASE_BRANCH once |
| https://github.com/ColeMurray/background-agents/pull/1611 | `colemurray/background-agents` | `code_only` | `typescript` | fix(control-plane): keep quiet executions active |
| https://github.com/ColeMurray/background-agents/pull/1616 | `colemurray/background-agents` | `code_only` | `typescript` | test(control-plane): typecheck test/integration/** |
| https://github.com/ColeMurray/background-agents/pull/1615 | `colemurray/background-agents` | `code_only` | `typescript` | refactor(control-plane): drop vestigial logger thunks |
| https://github.com/ColeMurray/background-agents/pull/1612 | `colemurray/background-agents` | `code_only` | `typescript` | refactor(control-plane): convert session HTTP handler factories to classes |
| https://github.com/ColeMurray/background-agents/pull/1613 | `colemurray/background-agents` | `code_only` | `typescript` | fix(e2b): install Bun in runtime PATH |
| https://github.com/ColeMurray/background-agents/pull/1592 | `colemurray/background-agents` | `code_only` | `typescript` | ci: split checks by ecosystem |
| https://github.com/ColeMurray/background-agents/pull/1609 | `colemurray/background-agents` | `code_only` | `typescript` | refactor(control-plane): require the secrets encryption key and dissolve the storage middle-man |
| https://github.com/ColeMurray/background-agents/pull/1608 | `colemurray/background-agents` | `code_only` | `typescript` | refactor(control-plane): composition classes for the root's three biggest closure bags |
| https://github.com/ColeMurray/background-agents/pull/1606 | `colemurray/background-agents` | `code_only` | `typescript` | fix(control-plane): close sandbox admission race with two-phase spawn write |
| https://github.com/ColeMurray/background-agents/pull/1604 | `colemurray/background-agents` | `code_only` | `typescript` | refactor(control-plane): collapse socket layers onto one delivery seam |
| https://github.com/ColeMurray/background-agents/pull/1603 | `colemurray/background-agents` | `code_only` | `typescript` | refactor(control-plane): govern session boundaries, dedupe root wiring |
| https://github.com/ColeMurray/background-agents/pull/1602 | `colemurray/background-agents` | `code_only` | `typescript` | refactor(control-plane): construct session providers eagerly |

## Reject Summary Sample

| Repository | PR | Reason | Bucket |
| --- | ---: | --- | --- |
| `schmitech/orbit` | `274` | `docs_only_excluded` | `docs_only` |
| `schmitech/orbit` | `259` | `not_merged` | `None` |
| `schmitech/orbit` | `249` | `not_merged` | `None` |
| `schmitech/orbit` | `235` | `not_merged` | `None` |
| `schmitech/orbit` | `215` | `not_merged` | `None` |
| `schmitech/orbit` | `95` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `schmitech/orbit` | `49` | `not_merged` | `None` |
| `schmitech/orbit` | `47` | `not_merged` | `None` |
| `schmitech/orbit` | `44` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `schmitech/orbit` | `28` | `docs_only_excluded` | `docs_only` |
| `schmitech/orbit` | `26` | `not_merged` | `None` |
| `schmitech/orbit` | `25` | `docs_only_excluded` | `docs_only` |
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
| `jestjs/jest` | `16051` | `not_merged` | `None` |
| `jestjs/jest` | `15956` | `not_merged` | `None` |
| `jestjs/jest` | `16228` | `not_merged` | `None` |
| `jestjs/jest` | `16294` | `docs_only_excluded` | `docs_only` |
| `jestjs/jest` | `16213` | `docs_only_excluded` | `docs_only` |
| `jestjs/jest` | `16317` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `jestjs/jest` | `16262` | `not_merged` | `None` |
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
| `eleutherai/lm-evaluation-harness` | `3972` | `too_many_changed_files` | `code_only` |
| `eleutherai/lm-evaluation-harness` | `986` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `3892` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `3878` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `3876` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `3875` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `3874` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `3873` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `3872` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `3871` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `3828` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `3794` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `3939` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `3965` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `3940` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `3580` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `3852` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `3901` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `3936` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `3255` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `3934` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `3931` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `3904` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `3827` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `3897` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `3899` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `3898` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `3889` | `not_merged` | `None` |
| `eleutherai/lm-evaluation-harness` | `3867` | `not_merged` | `None` |
| `kdeldycke/click-extra` | `1920` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `kdeldycke/click-extra` | `1919` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `kdeldycke/click-extra` | `1725` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1730` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `kdeldycke/click-extra` | `1917` | `not_merged` | `None` |
| `kdeldycke/click-extra` | `1916` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1914` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1912` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1911` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1904` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1908` | `not_merged` | `None` |
| `kdeldycke/click-extra` | `1903` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1891` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `kdeldycke/click-extra` | `1902` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `kdeldycke/click-extra` | `1907` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `kdeldycke/click-extra` | `1905` | `not_merged` | `None` |
| `kdeldycke/click-extra` | `1900` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `kdeldycke/click-extra` | `1709` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `kdeldycke/click-extra` | `1707` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1710` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `kdeldycke/click-extra` | `1713` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `kdeldycke/click-extra` | `1714` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `kdeldycke/click-extra` | `1715` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `kdeldycke/click-extra` | `1718` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1722` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1897` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1896` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `kdeldycke/click-extra` | `1898` | `not_merged` | `None` |
| `kdeldycke/click-extra` | `1895` | `not_merged` | `None` |
| `kdeldycke/click-extra` | `1892` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1693` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `kdeldycke/click-extra` | `1695` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `kdeldycke/click-extra` | `1701` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `kdeldycke/click-extra` | `1699` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1698` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1702` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1704` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `kdeldycke/click-extra` | `1890` | `not_merged` | `None` |
| `kdeldycke/click-extra` | `1887` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1884` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `kdeldycke/click-extra` | `1882` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1877` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `kdeldycke/click-extra` | `1876` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `kdeldycke/click-extra` | `1874` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1687` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `kdeldycke/click-extra` | `1692` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `kdeldycke/click-extra` | `1691` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1690` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1671` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1678` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1675` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1670` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `kdeldycke/click-extra` | `1679` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `kdeldycke/click-extra` | `1676` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1681` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1682` | `not_merged` | `None` |
| `kdeldycke/click-extra` | `1684` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1685` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `kdeldycke/click-extra` | `1872` | `not_merged` | `None` |
| `kdeldycke/click-extra` | `1869` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1866` | `not_merged` | `None` |
| `kdeldycke/click-extra` | `1863` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1859` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1856` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `kdeldycke/click-extra` | `1853` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `kdeldycke/click-extra` | `1854` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1851` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1850` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `kdeldycke/click-extra` | `1849` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1845` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1846` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `kdeldycke/click-extra` | `1660` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1658` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `kdeldycke/click-extra` | `1662` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `kdeldycke/click-extra` | `1663` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1659` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1665` | `not_merged` | `None` |
| `kdeldycke/click-extra` | `1668` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1672` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1843` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1841` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `kdeldycke/click-extra` | `1840` | `not_merged` | `None` |
| `kdeldycke/click-extra` | `1839` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1834` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1837` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `kdeldycke/click-extra` | `1820` | `not_merged` | `None` |
| `kdeldycke/click-extra` | `1831` | `not_merged` | `None` |
| `kdeldycke/click-extra` | `1832` | `not_merged` | `None` |
| `kdeldycke/click-extra` | `1829` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `kdeldycke/click-extra` | `1830` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1630` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1626` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1628` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `kdeldycke/click-extra` | `1631` | `not_merged` | `None` |
| `kdeldycke/click-extra` | `1634` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `kdeldycke/click-extra` | `1577` | `not_merged` | `None` |
| `kdeldycke/click-extra` | `1557` | `not_merged` | `None` |
| `kdeldycke/click-extra` | `1552` | `not_merged` | `None` |
| `kdeldycke/click-extra` | `1523` | `not_merged` | `None` |
| `kdeldycke/click-extra` | `1513` | `not_merged` | `None` |
| `kdeldycke/click-extra` | `1520` | `not_merged` | `None` |
| `kdeldycke/click-extra` | `1509` | `not_merged` | `None` |
| `kdeldycke/click-extra` | `1637` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1636` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `kdeldycke/click-extra` | `1644` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1642` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1640` | `not_merged` | `None` |
| `kdeldycke/click-extra` | `1647` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `kdeldycke/click-extra` | `1641` | `docs_only_excluded` | `docs_only` |
| `kdeldycke/click-extra` | `1650` | `other_or_binary_only_excluded` | `other_or_binary_only` |