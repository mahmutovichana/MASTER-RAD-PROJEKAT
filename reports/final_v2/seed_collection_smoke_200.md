# DocGuard Real PR Seed Collector Report

This report summarizes neutral repo-based sampling of merged public GitHub PRs.

The collector does not assign gold labels and does not decide whether documentation should be updated.
It only creates seed PR URLs for the later candidate builder and manual validation workflow.

- Repositories scanned: `191`
- Seeds accepted: `200`
- Rejected/skipped PRs: `393`
- Collector bucket counts: `{'code_only': 98, 'code_only_tests_or_fixtures': 8, 'code_and_docs': 94}`
- Language hint counts: `{'go': 30, 'python': 110, 'typescript': 60}`
- Repository counts per language: `{'go': 1, 'python': 4, 'typescript': 2}`
- Candidate bucket counts per language: `{'go': {'code_only': 27, 'code_only_tests_or_fixtures': 3}, 'python': {'code_and_docs': 57, 'code_only': 51, 'code_only_tests_or_fixtures': 2}, 'typescript': {'code_and_docs': 37, 'code_only_tests_or_fixtures': 3, 'code_only': 20}}`
- Reject reason counts: `{'not_merged': 318, 'too_many_changed_files': 15, 'docs_only_excluded': 33, 'too_large_patch': 9, 'other_or_binary_only_excluded': 17, 'fetch_closed_pulls_failed': 1}`

## Methodological Boundary

- This is real public GitHub PR sampling.
- No synthetic examples are generated.
- No final labels are assigned here.
- `collector_bucket` is audit metadata for balancing and review planning, not a model label.
- Final evaluation must use only the safe fields produced later by the candidate builder.

## Accepted Seeds

| PR | Repository | Bucket | Language hint | Title |
| --- | --- | --- | --- | --- |
| https://github.com/microsoft/typescript-go/pull/4877 | `microsoft/TypeScript-go` | `code_only` | `go` | Gate ES2025 regex syntax behind target |
| https://github.com/microsoft/typescript-go/pull/4917 | `microsoft/TypeScript-go` | `code_only_tests_or_fixtures` | `go` | Fix test:api on windows |
| https://github.com/microsoft/typescript-go/pull/4900 | `microsoft/TypeScript-go` | `code_only` | `go` | Prevent crash when computing emit output paths |
| https://github.com/microsoft/typescript-go/pull/4723 | `microsoft/TypeScript-go` | `code_only` | `go` | Preserve comments when downleveling arrow expression bodies |
| https://github.com/microsoft/typescript-go/pull/4909 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix go-to-definition functionality at JS JSX tag edge |
| https://github.com/microsoft/typescript-go/pull/4889 | `microsoft/TypeScript-go` | `code_only` | `go` | Use semantic type identity for JSDoc augments checks |
| https://github.com/microsoft/typescript-go/pull/4836 | `microsoft/TypeScript-go` | `code_only` | `go` | Preserve nested module resolution diagnostics in concurrent mode |
| https://github.com/microsoft/typescript-go/pull/4442 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix false implicit-return/unreachable diagnostics in `try/finally` with logical assignment (`\|\|=`) |
| https://github.com/microsoft/typescript-go/pull/4913 | `microsoft/TypeScript-go` | `code_only` | `go` | Improve recursion identities and `isDeeplyNestedType` |
| https://github.com/microsoft/typescript-go/pull/4533 | `microsoft/TypeScript-go` | `code_only` | `go` | [api] Add `.getNonPrimitiveType()` getter |
| https://github.com/microsoft/typescript-go/pull/4540 | `microsoft/TypeScript-go` | `code_only` | `go` | [api] Add `StructuredType` type |
| https://github.com/microsoft/typescript-go/pull/4599 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix crash in CFA when for loop initializer throws |
| https://github.com/microsoft/typescript-go/pull/4791 | `microsoft/TypeScript-go` | `code_only` | `go` | Add getSymbolOfSourceFile to the API |
| https://github.com/microsoft/typescript-go/pull/4552 | `microsoft/TypeScript-go` | `code_only` | `go` | Add versions of get*Diagostics that allow passing in an array of files. |
| https://github.com/microsoft/typescript-go/pull/3663 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix hover JSDoc for mapped type properties |
| https://github.com/microsoft/typescript-go/pull/4682 | `microsoft/TypeScript-go` | `code_only` | `go` | [api] Always update inferred project if one is open |
| https://github.com/microsoft/typescript-go/pull/4700 | `microsoft/TypeScript-go` | `code_only` | `go` | Expose getFullyQualifiedName on the API Checker |
| https://github.com/microsoft/typescript-go/pull/4784 | `microsoft/TypeScript-go` | `code_only` | `go` | Build checker cache keys in an inline buffer with one-shot hashing |
| https://github.com/microsoft/typescript-go/pull/3515 | `microsoft/TypeScript-go` | `code_only` | `go` | Expose formatNodeForInsertion in internal API |
| https://github.com/microsoft/typescript-go/pull/4910 | `microsoft/TypeScript-go` | `code_only_tests_or_fixtures` | `go` | Fix extension temp paths on macOS |
| https://github.com/microsoft/typescript-go/pull/4839 | `microsoft/TypeScript-go` | `code_only` | `go` | fix(63726): fix declaration emit for multiline jsdoc literal types |
| https://github.com/microsoft/typescript-go/pull/4906 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix tsdk resolution for npm aliases |
| https://github.com/microsoft/typescript-go/pull/4598 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix optionality stripping when mapping over tuples under EOPT |
| https://github.com/microsoft/typescript-go/pull/4873 | `microsoft/TypeScript-go` | `code_only` | `go` | fix(4863): fix declaration emit for jsdoc functions |
| https://github.com/microsoft/typescript-go/pull/4603 | `microsoft/TypeScript-go` | `code_only` | `go` | fix(checker): avoid computed enum member stack overflow |
| https://github.com/microsoft/typescript-go/pull/4685 | `microsoft/TypeScript-go` | `code_only` | `go` | fix(4677): preserve JSDoc for mapped type properties in hover |
| https://github.com/microsoft/typescript-go/pull/2908 | `microsoft/TypeScript-go` | `code_only_tests_or_fixtures` | `go` | Add regression test for inlay hints crash on reparsed nodes (#2460) |
| https://github.com/microsoft/typescript-go/pull/4800 | `microsoft/TypeScript-go` | `code_only` | `go` | Don't report TS1293 for destructured require under --module preserve |
| https://github.com/microsoft/typescript-go/pull/4676 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix parsing of `as`/`satisfies` between `**` operators |
| https://github.com/microsoft/typescript-go/pull/4898 | `microsoft/TypeScript-go` | `code_only` | `go` | Parse dotted private names in type queries, forbid in declaration emit |
| https://github.com/torbido-hq/cicerone/pull/130 | `torbido-hq/cicerone` | `code_and_docs` | `python` | feat: inspect recent events next to dashboard top-K |
| https://github.com/torbido-hq/cicerone/pull/133 | `torbido-hq/cicerone` | `code_and_docs` | `python` | ci: run sequential extra tests in a separate compose service |
| https://github.com/torbido-hq/cicerone/pull/131 | `torbido-hq/cicerone` | `code_and_docs` | `python` | Adopt RecTools 0.19 sequential defaults and opt-in AutoML debias |
| https://github.com/torbido-hq/cicerone/pull/129 | `torbido-hq/cicerone` | `code_and_docs` | `python` | chore: land Dependabot bumps on 0.7 |
| https://github.com/torbido-hq/cicerone/pull/109 | `torbido-hq/cicerone` | `code_and_docs` | `python` | perf: thread recommend after fit and vectorize blend RRF |
| https://github.com/torbido-hq/cicerone/pull/121 | `torbido-hq/cicerone` | `code_and_docs` | `python` | docs: mark the nightly-table article as updated Aug 24 |
| https://github.com/torbido-hq/cicerone/pull/119 | `torbido-hq/cicerone` | `code_and_docs` | `python` | fix: complete the serve source labels; correct architecture and tutorial claims |
| https://github.com/torbido-hq/cicerone/pull/112 | `torbido-hq/cicerone` | `code_and_docs` | `python` | fix: load Google Analytics only after Accept |
| https://github.com/torbido-hq/cicerone/pull/107 | `torbido-hq/cicerone` | `code_and_docs` | `python` | Add custom consent banner and Consent Mode v2 on cicerone.dev |
| https://github.com/torbido-hq/cicerone/pull/97 | `torbido-hq/cicerone` | `code_and_docs` | `python` | Add PyPI package and cicerone CLI |
| https://github.com/torbido-hq/cicerone/pull/101 | `torbido-hq/cicerone` | `code_and_docs` | `python` | feat(website): static articles at /articles/, hidden until a post exists |
| https://github.com/torbido-hq/cicerone/pull/100 | `torbido-hq/cicerone` | `code_and_docs` | `python` | Revert accidental merge of website articles (#96) |
| https://github.com/torbido-hq/cicerone/pull/96 | `torbido-hq/cicerone` | `code_and_docs` | `python` | feat(website): static articles at /articles/, hidden until a post exists |
| https://github.com/torbido-hq/cicerone/pull/95 | `torbido-hq/cicerone` | `code_and_docs` | `python` | feat(dashboard): add user-id recommendation inspector |
| https://github.com/torbido-hq/cicerone/pull/94 | `torbido-hq/cicerone` | `code_and_docs` | `python` | feat(model): optional SASRec/BERT4Rec sequential strategy |
| https://github.com/torbido-hq/cicerone/pull/93 | `torbido-hq/cicerone` | `code_and_docs` | `python` | feat(events): leader-only apply lease for incremental HA |
| https://github.com/torbido-hq/cicerone/pull/92 | `torbido-hq/cicerone` | `code_and_docs` | `python` | fix(events): buffer ack bookkeeping, DB cursor paging, drain on stop |
| https://github.com/torbido-hq/cicerone/pull/91 | `torbido-hq/cicerone` | `code_and_docs` | `python` | feat(events): Redis Streams EventSource |
| https://github.com/torbido-hq/cicerone/pull/84 | `torbido-hq/cicerone` | `code_and_docs` | `python` | feat(events): user-scoped incremental recommendation I/O |
| https://github.com/torbido-hq/cicerone/pull/83 | `torbido-hq/cicerone` | `code_and_docs` | `python` | feat(events): S3 EventSource (list/marker and SQS) |
| https://github.com/torbido-hq/cicerone/pull/82 | `torbido-hq/cicerone` | `code_and_docs` | `python` | feat(events): metrics and dashboard wiring for incremental ingest |
| https://github.com/torbido-hq/cicerone/pull/76 | `torbido-hq/cicerone` | `code_and_docs` | `python` | Add DB watermark EventSource (events.kind=db) |
| https://github.com/torbido-hq/cicerone/pull/81 | `torbido-hq/cicerone` | `code_and_docs` | `python` | chore: Dependabot — Pages upload-pages-artifact v5 + deploy-pages v5 |
| https://github.com/torbido-hq/cicerone/pull/78 | `torbido-hq/cicerone` | `code_only` | `python` | Bump actions/setup-node from 4 to 7 |
| https://github.com/torbido-hq/cicerone/pull/77 | `torbido-hq/cicerone` | `code_and_docs` | `python` | chore: Dependabot — take fastapi 0.141.1; block numpy/boto3 |
| https://github.com/torbido-hq/cicerone/pull/60 | `torbido-hq/cicerone` | `code_and_docs` | `python` | Prepare 0.5.1: correctness/performance refactorings |
| https://github.com/torbido-hq/cicerone/pull/68 | `torbido-hq/cicerone` | `code_only` | `python` | Consolidate Dependabot dependency bumps |
| https://github.com/torbido-hq/cicerone/pull/53 | `torbido-hq/cicerone` | `code_and_docs` | `python` | chore: Dependabot dependency bumps (consolidated) |
| https://github.com/torbido-hq/cicerone/pull/61 | `torbido-hq/cicerone` | `code_and_docs` | `python` | Add Ruby OpenAPI code samples for serve API |
| https://github.com/torbido-hq/cicerone/pull/59 | `torbido-hq/cicerone` | `code_and_docs` | `python` | Add Prometheus /metrics endpoint for serve mode |
| https://github.com/CryptoJones/omind/pull/266 | `CryptoJones/omind` | `code_and_docs` | `python` | feat: add DeepSeek Harness (DSH) agent support |
| https://github.com/CryptoJones/omind/pull/264 | `CryptoJones/omind` | `code_only_tests_or_fixtures` | `python` | test: fix the seven POSIX-form guard tests on windows-latest |
| https://github.com/CryptoJones/omind/pull/263 | `CryptoJones/omind` | `code_and_docs` | `python` | fix: native Windows Claude hooks — closes the last Windows finding (#259) — 8.7.2 |
| https://github.com/CryptoJones/omind/pull/262 | `CryptoJones/omind` | `code_and_docs` | `python` | fix: Windows codex hook recognition (#261) + graceful setup without claude (#258) — 8.7.1 |
| https://github.com/CryptoJones/omind/pull/257 | `CryptoJones/omind` | `code_and_docs` | `python` | release: 8.7.0 — stop injecting weak preflight matches |
| https://github.com/CryptoJones/omind/pull/255 | `CryptoJones/omind` | `code_only` | `python` | feat(guard): minimum term overlap before preflight injects a memory |
| https://github.com/CryptoJones/omind/pull/256 | `CryptoJones/omind` | `code_only` | `python` | fix(rules): narrow the 'when' mapping so mypy accepts it (CI unbreak) |
| https://github.com/CryptoJones/omind/pull/254 | `CryptoJones/omind` | `code_and_docs` | `python` | fix(rules): judge the pushed refspec, not just the checked-out branch (#240) |
| https://github.com/CryptoJones/omind/pull/253 | `CryptoJones/omind` | `code_and_docs` | `python` | build(deps): bump cryptography 49.0.0 → 50.0.0 (high-severity Dependabot alert) |
| https://github.com/CryptoJones/omind/pull/251 | `CryptoJones/omind` | `code_and_docs` | `python` | feat(rules,guard): compile machine-readable note rules into deterministic PreToolUse checks (#240) |
| https://github.com/CryptoJones/omind/pull/250 | `CryptoJones/omind` | `code_and_docs` | `python` | feat(doctor,hooks): loudly surface sustained vault-write failures (#243) |
| https://github.com/CryptoJones/omind/pull/249 | `CryptoJones/omind` | `code_and_docs` | `python` | feat(guard): place governing rule text adjacent to the action it governs (#241) |
| https://github.com/CryptoJones/omind/pull/248 | `CryptoJones/omind` | `code_and_docs` | `python` | fix(recall,guard): actionable truncation markers; truncated demanded reads keep the gate armed (#239) |
| https://github.com/CryptoJones/omind/pull/247 | `CryptoJones/omind` | `code_and_docs` | `python` | fix(hooks,guard): stop the injected-memory framing from inviting discount (#242) |
| https://github.com/CryptoJones/omind/pull/245 | `CryptoJones/omind` | `code_and_docs` | `python` | fix(hooks): inject priming notes whole or not at all; default profile is balanced (#238) |
| https://github.com/CryptoJones/omind/pull/237 | `CryptoJones/omind` | `code_and_docs` | `python` | release: 8.2.7 — a locked guard config reads as hardened, not broken |
| https://github.com/CryptoJones/omind/pull/236 | `CryptoJones/omind` | `code_and_docs` | `python` | release: 8.2.6 — setup is idempotent when its guard entry is first |
| https://github.com/CryptoJones/omind/pull/235 | `CryptoJones/omind` | `code_and_docs` | `python` | release: 8.2.5 — explain an immutable settings.json, not just hook scripts |
| https://github.com/CryptoJones/omind/pull/234 | `CryptoJones/omind` | `code_and_docs` | `python` | release: 8.2.4 — stop gating legitimate work; count refusals, not ceremonies |
| https://github.com/CryptoJones/omind/pull/232 | `CryptoJones/omind` | `code_and_docs` | `python` | release: 8.2.3 — deny-rate warning stops recommending a command that tightens the gate |
| https://github.com/CryptoJones/omind/pull/231 | `CryptoJones/omind` | `code_and_docs` | `python` | release: 8.2.2 — keep installed extras across self-update |
| https://github.com/CryptoJones/omind/pull/230 | `CryptoJones/omind` | `code_and_docs` | `python` | release: 8.2.1 |
| https://github.com/CryptoJones/omind/pull/229 | `CryptoJones/omind` | `code_and_docs` | `python` | fix(provision,guard,store): pin hooks to a canonical omind, fix title recall |
| https://github.com/CryptoJones/omind/pull/228 | `CryptoJones/omind` | `code_and_docs` | `python` | release: 8.2.0 |
| https://github.com/CryptoJones/omind/pull/227 | `CryptoJones/omind` | `code_only` | `python` | feat(memory): optional retrieval scope on notes (#222) |
| https://github.com/CryptoJones/omind/pull/226 | `CryptoJones/omind` | `code_only` | `python` | feat(memory): notice when a session did work and wrote nothing down (#221) |
| https://github.com/CryptoJones/omind/pull/224 | `CryptoJones/omind` | `code_only` | `python` | feat(retrieval): score separation, a token budget, and cursor-paged search |
| https://github.com/CryptoJones/omind/pull/225 | `CryptoJones/omind` | `code_only` | `python` | provision: default crossSessionInbound to "accept" fleet-wide |
| https://github.com/CryptoJones/omind/pull/199 | `CryptoJones/omind` | `code_only` | `python` | chore(deps): bump the github-actions group across 1 directory with 2 updates |
| https://github.com/CryptoJones/omind/pull/219 | `CryptoJones/omind` | `code_only` | `python` | chore(deps): update cryptography requirement from <50.0,>=48.0.1 to >=48.0.1,<51.0 in the python-deps group |
| https://github.com/d-hinders/Haven-AI/pull/2062 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(frontend): give UnmanagedDelegateCard the revoke /custody promises (#1980) |
| https://github.com/d-hinders/Haven-AI/pull/2061 | `d-hinders/Haven-AI` | `code_only_tests_or_fixtures` | `typescript` | test(outbound): characterize the stuck passport_attest lane wedge on real Postgres (#1743) |
| https://github.com/d-hinders/Haven-AI/pull/2060 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | feat(safe-retirement): retire the agent_allowances surface (#2020) |
| https://github.com/d-hinders/Haven-AI/pull/2059 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(rekey): an abandoned post-revoke re-key hands its frozen carry to the successor (#1868) |
| https://github.com/d-hinders/Haven-AI/pull/2058 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | test(casp): Red Line #4's structural guard parses import structure, every shape mutation-proven (#2049) |
| https://github.com/d-hinders/Haven-AI/pull/2031 | `d-hinders/Haven-AI` | `code_only` | `typescript` | fix(frontend): dedupe the hero Contact-the-team CTA on /investor-briefing (#1956) |
| https://github.com/d-hinders/Haven-AI/pull/2034 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | chore(money-path): widen the perimeter to the edge signer + core machine-payment domain (#1905, #1896, #1903) |
| https://github.com/d-hinders/Haven-AI/pull/2057 | `d-hinders/Haven-AI` | `code_only` | `typescript` | test(backend): remove the stale allowance-nonce-watermarks vi.mock from six suites (#2048) |
| https://github.com/d-hinders/Haven-AI/pull/2056 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(mcp): bind the spending cap to the option actually authorized (#2051) |
| https://github.com/d-hinders/Haven-AI/pull/2024 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | feat(safe-retirement): drop safe_approver_metadata (#1990) |
| https://github.com/d-hinders/Haven-AI/pull/2052 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(mcp): let the generic plain-HTTP x402 path reach erc7710 (#2041) |
| https://github.com/d-hinders/Haven-AI/pull/2053 | `d-hinders/Haven-AI` | `code_only_tests_or_fixtures` | `typescript` | test(frontend): address WalletIdentityBlock's tooltip trigger by identity, not by ordinal (#2038) |
| https://github.com/d-hinders/Haven-AI/pull/2047 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(frontend): make Tooltip content reachable without a mouse, and let it wrap (#2038) |
| https://github.com/d-hinders/Haven-AI/pull/2050 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | test(casp): remove three unfalsifiable spies from the Red Line #4 regulatory proof (#2044) |
| https://github.com/d-hinders/Haven-AI/pull/2045 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | test(casp): prove the deployed caveat enforcers are Red Line #4's final gate (#2004) |
| https://github.com/d-hinders/Haven-AI/pull/2042 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(screenshot): refuse a capture that is still loading (#2036) |
| https://github.com/d-hinders/Haven-AI/pull/2033 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(frontend): semantic danger tone for the backup/recovery loadError state (#1937) |
| https://github.com/d-hinders/Haven-AI/pull/2032 | `d-hinders/Haven-AI` | `code_only` | `typescript` | fix(frontend): separate the sidebar menu focus ring from the popover border (#1877) |
| https://github.com/d-hinders/Haven-AI/pull/2039 | `d-hinders/Haven-AI` | `code_only` | `typescript` | fix(frontend): give the Approvers badge positive evidence, not an absence (#2017) |
| https://github.com/d-hinders/Haven-AI/pull/2037 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | feat(frontend): let a capture run shoot a width the committed set does not (#2006) |
| https://github.com/d-hinders/Haven-AI/pull/2035 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | Remove retired QA credential requirements |
| https://github.com/d-hinders/Haven-AI/pull/2029 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | Block revoked agents from new budget delegations |
| https://github.com/d-hinders/Haven-AI/pull/2028 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(safe-exec): report a confirmation timeout as pending, not as a revert (#1754, #1755) |
| https://github.com/d-hinders/Haven-AI/pull/2026 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(qa): prevent revoked agent seed reuse |
| https://github.com/d-hinders/Haven-AI/pull/2022 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(qa): re-base the three legacy money-flow legs onto the delegation rail (#2016) |
| https://github.com/d-hinders/Haven-AI/pull/2014 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(frontend): key Table's column collapse on the container, not the viewport (#1999) |
| https://github.com/d-hinders/Haven-AI/pull/2013 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(safe-retirement): re-base the QA seed on the delegation rail (#2007) |
| https://github.com/d-hinders/Haven-AI/pull/2009 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | feat(safe-retirement): delete the Safe creation and owner-change machinery (#1988) |
| https://github.com/d-hinders/Haven-AI/pull/2010 | `d-hinders/Haven-AI` | `code_only_tests_or_fixtures` | `typescript` | test(frontend): render WalletButton's collapsed connected-avatar and wrong-network states (#1944) |
| https://github.com/d-hinders/Haven-AI/pull/2003 | `d-hinders/Haven-AI` | `code_only` | `typescript` | docs(frontend): correct why WalletPopover's presentational role swap exists (#1982) |
| https://github.com/microsoft/autogen/pull/593 | `microsoft/autogen` | `code_and_docs` | `python` | Sets the umask before executing the task in Docker. |
| https://github.com/microsoft/autogen/pull/710 | `microsoft/autogen` | `code_only` | `python` | bump version to 0.2.0b6 |
| https://github.com/microsoft/autogen/pull/1132 | `microsoft/autogen` | `code_only_tests_or_fixtures` | `python` | Change `contrib-tests.yml` tests to use `--skip-openai` |
| https://github.com/microsoft/autogen/pull/2703 | `microsoft/autogen` | `code_only` | `python` | Update groupchat.py to remove Optional type hint when they are not ch… |
| https://github.com/microsoft/autogen/pull/31 | `microsoft/autogen` | `code_only` | `python` | minor fix |
| https://github.com/microsoft/autogen/pull/931 | `microsoft/autogen` | `code_only` | `python` | correcting typo |
| https://github.com/microsoft/autogen/pull/2171 | `microsoft/autogen` | `code_only` | `python` | fix(): fix word spelling errors |
| https://github.com/microsoft/autogen/pull/1748 | `microsoft/autogen` | `code_only` | `python` | Use jupyer-kernel-gateway for ipython executor |
| https://github.com/microsoft/autogen/pull/2785 | `microsoft/autogen` | `code_only` | `python` | Improve the error messge of RetrieveUserProxyAgent import error |
| https://github.com/microsoft/autogen/pull/1787 | `microsoft/autogen` | `code_and_docs` | `python` | Ability to fine tune custom model on conversable agents |
| https://github.com/microsoft/autogen/pull/2002 | `microsoft/autogen` | `code_only` | `python` | fix: [autogenbench] writing to stdout encoding error in win-os |
| https://github.com/microsoft/autogen/pull/1981 | `microsoft/autogen` | `code_only` | `python` | Update local cli executor to use same filename strategy as docker |
| https://github.com/microsoft/autogen/pull/1803 | `microsoft/autogen` | `code_only` | `python` | Don't require notebooks to have all imports at top |
| https://github.com/microsoft/autogen/pull/616 | `microsoft/autogen` | `code_and_docs` | `python` | Introducing Experimental GPT Assistant Agent  in AutoGen |
| https://github.com/microsoft/autogen/pull/1882 | `microsoft/autogen` | `code_only` | `python` | Add initial type check CI |
| https://github.com/microsoft/autogen/pull/2241 | `microsoft/autogen` | `code_only` | `python` | Allow custom name for functions module |
| https://github.com/microsoft/autogen/pull/1912 | `microsoft/autogen` | `code_only` | `python` | Adjusts send_introductions Type Hint in GroupChat |
| https://github.com/microsoft/autogen/pull/1841 | `microsoft/autogen` | `code_only` | `python` | adjust the order of message processing |
| https://github.com/microsoft/autogen/pull/1791 | `microsoft/autogen` | `code_and_docs` | `python` | Allow user to pass in a customized speaker selection method |
| https://github.com/microsoft/autogen/pull/1034 | `microsoft/autogen` | `code_and_docs` | `python` | Fix/typo |
| https://github.com/microsoft/autogen/pull/6578 | `microsoft/autogen` | `code_only` | `python` | Default usage statistics for streaming responses |
| https://github.com/microsoft/autogen/pull/4847 | `microsoft/autogen` | `code_only` | `python` | Add coverage task & integrate with poe check |
| https://github.com/microsoft/autogen/pull/1124 | `microsoft/autogen` | `code_only` | `python` | Use PIL Image internally for the Multimodal Agent |
| https://github.com/microsoft/autogen/pull/1435 | `microsoft/autogen` | `code_only` | `python` | Refactoring web surfer to use function decorators |
| https://github.com/microsoft/autogen/pull/1539 | `microsoft/autogen` | `code_only` | `python` | Fix docstrings of a_initiate_chat |
| https://github.com/microsoft/autogen/pull/1254 | `microsoft/autogen` | `code_only` | `python` | def _prepare_chat for groupchat manager to reset the groupchat |
| https://github.com/microsoft/autogen/pull/123 | `microsoft/autogen` | `code_only` | `python` | fix doc typo |
| https://github.com/microsoft/autogen/pull/2062 | `microsoft/autogen` | `code_only` | `python` | Fix type issues in openai_utils.py |
| https://github.com/microsoft/autogen/pull/1352 | `microsoft/autogen` | `code_and_docs` | `python` | Autogenstudio - Add GroupChat Support to UI |
| https://github.com/microsoft/autogen/pull/1443 | `microsoft/autogen` | `code_and_docs` | `python` | Function calling upgrade |
| https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/88 | `eclipsefdn-ai-registry/ai-registry-core` | `code_only` | `typescript` | Extend trust delegation to Agent Plugins and A2A agents |
| https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/87 | `eclipsefdn-ai-registry/ai-registry-core` | `code_and_docs` | `typescript` | Add per-type and per-organization JSON feeds, with an org view page |
| https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/85 | `eclipsefdn-ai-registry/ai-registry-core` | `code_and_docs` | `typescript` | Add client integration guidance and CLI install commands |
| https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/78 | `eclipsefdn-ai-registry/ai-registry-core` | `code_and_docs` | `typescript` | Add "agent" (A2A) artifact type |
| https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/69 | `eclipsefdn-ai-registry/ai-registry-core` | `code_only` | `typescript` | Add generic MCP server config with cross-vendor derivation and MCP trust delegation |
| https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/72 | `eclipsefdn-ai-registry/ai-registry-core` | `code_and_docs` | `typescript` | Remove homepage preview banner, refresh hero messaging (#68) |
| https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/70 | `eclipsefdn-ai-registry/ai-registry-core` | `code_only` | `typescript` | Bump fast-uri from 3.1.2 to 3.1.5 |
| https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/63 | `eclipsefdn-ai-registry/ai-registry-core` | `code_and_docs` | `typescript` | Rename "verified by publisher" to "Publisher claimed" |
| https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/64 | `eclipsefdn-ai-registry/ai-registry-core` | `code_only` | `typescript` | Adapt inferred badge |
| https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/62 | `eclipsefdn-ai-registry/ai-registry-core` | `code_and_docs` | `typescript` | Add vendor-supplied fallback metadata and publisher self-attestation of MCP servers |
| https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/57 | `eclipsefdn-ai-registry/ai-registry-core` | `code_and_docs` | `typescript` | Add mechanism to trust other vendors |
| https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/45 | `eclipsefdn-ai-registry/ai-registry-core` | `code_only` | `typescript` | Add AWS vendor repo |
| https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/51 | `eclipsefdn-ai-registry/ai-registry-core` | `code_only` | `typescript` | Bump brace-expansion and eslint |
| https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/52 | `eclipsefdn-ai-registry/ai-registry-core` | `code_only` | `typescript` | Trigger Jenkins deployment after successful GitHub Pages build |
| https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/49 | `eclipsefdn-ai-registry/ai-registry-core` | `code_only` | `typescript` | Fix glob pattern verification in skill source validation |
| https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/43 | `eclipsefdn-ai-registry/ai-registry-core` | `code_only` | `typescript` | Fix skill installUrl to use expanded skillId |
| https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/39 | `eclipsefdn-ai-registry/ai-registry-core` | `code_and_docs` | `typescript` | Update url and api page |
| https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/32 | `eclipsefdn-ai-registry/ai-registry-core` | `code_and_docs` | `typescript` | Move tools to /tools |
| https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/38 | `eclipsefdn-ai-registry/ai-registry-core` | `code_and_docs` | `typescript` | Expand glob patterns inside array source.path |
| https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/36 | `eclipsefdn-ai-registry/ai-registry-core` | `code_only` | `typescript` | Add Get Involved section to About page |
| https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/35 | `eclipsefdn-ai-registry/ai-registry-core` | `code_only` | `typescript` | Bump vite from 8.0.12 to 8.0.16 in /website |
| https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/33 | `eclipsefdn-ai-registry/ai-registry-core` | `code_only` | `typescript` | Bump esbuild and tsx |
| https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/31 | `eclipsefdn-ai-registry/ai-registry-core` | `code_and_docs` | `typescript` | Allow auto-generate installUrl from prefix + artifact ID |
| https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/18 | `eclipsefdn-ai-registry/ai-registry-core` | `code_only` | `typescript` | Issue 17 - Create Jenkinsfile |
| https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/30 | `eclipsefdn-ai-registry/ai-registry-core` | `code_only` | `typescript` | Include skill approvals in org approval count, fixed #28 |
| https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/29 | `eclipsefdn-ai-registry/ai-registry-core` | `code_and_docs` | `typescript` | Supported inferred vendors |
| https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/25 | `eclipsefdn-ai-registry/ai-registry-core` | `code_and_docs` | `typescript` | Allow to approve arrays of skills and wildcards |
| https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/19 | `eclipsefdn-ai-registry/ai-registry-core` | `code_and_docs` | `typescript` | Allow vendor apporvals without tools |
| https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/20 | `eclipsefdn-ai-registry/ai-registry-core` | `code_only` | `typescript` | Fix external content escaping for skills, URLs, and colors  |
| https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/14 | `eclipsefdn-ai-registry/ai-registry-core` | `code_and_docs` | `typescript` | Add support to host Skills |
| https://github.com/microsoft/semantic-kernel/pull/14306 | `microsoft/semantic-kernel` | `code_and_docs` | `python` | Python: [Breaking] Remove unsupported service auth mode from Copilot Studio agent |
| https://github.com/microsoft/semantic-kernel/pull/14293 | `microsoft/semantic-kernel` | `code_only` | `python` | .NET: [Breaking] Update OpenAPI HTTP client defaults |
| https://github.com/microsoft/semantic-kernel/pull/14183 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Honor FunctionChoiceBehavior function list in Gemini connector |
| https://github.com/microsoft/semantic-kernel/pull/14277 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Bump Python version to 1.44.1 for a release |
| https://github.com/microsoft/semantic-kernel/pull/14270 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Document x5t certificate thumbprint hashing in Copilot Studio agent |
| https://github.com/microsoft/semantic-kernel/pull/14234 | `microsoft/semantic-kernel` | `code_only` | `python` | Bump form-data from 4.0.5 to 4.0.6 in ProcessFrameworkWithSignalR React frontend |
| https://github.com/microsoft/semantic-kernel/pull/14235 | `microsoft/semantic-kernel` | `code_only` | `python` | Bump .NET SDK from 10.0.301 to 10.0.302 |
| https://github.com/microsoft/semantic-kernel/pull/14236 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Skip MCP tools and prompts whose normalized names collide |
| https://github.com/microsoft/semantic-kernel/pull/14222 | `microsoft/semantic-kernel` | `code_only` | `python` | Consolidate Python and .NET dependency updates |
| https://github.com/microsoft/semantic-kernel/pull/14210 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: [Breaking] Add MCP tool approval callback for Azure AI Agent |
| https://github.com/microsoft/semantic-kernel/pull/14223 | `microsoft/semantic-kernel` | `code_only` | `python` | Suppress CodeQL false positive in internal HTTP utility |
| https://github.com/microsoft/semantic-kernel/pull/14201 | `microsoft/semantic-kernel` | `code_only` | `python` | .NET: Harden dotnet-format workflow shell handling |
| https://github.com/microsoft/semantic-kernel/pull/14182 | `microsoft/semantic-kernel` | `code_only` | `python` | Fix cosmosdb vectorstore bug |
| https://github.com/microsoft/semantic-kernel/pull/14112 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: [.NET] Add TimeProvider injection to TimePlugin for deterministic testing |
| https://github.com/microsoft/semantic-kernel/pull/14166 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Reject mixed-separator UNC paths in file plugins |
| https://github.com/microsoft/semantic-kernel/pull/14169 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: [BREAKING] Upgrade Prompty.Core to 2.0.0-beta.3 to resolve NU1903 vulnerability |
| https://github.com/microsoft/semantic-kernel/pull/13925 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: fix: address three static analysis issues (audio format, text search, KernelProcess) |
| https://github.com/microsoft/semantic-kernel/pull/14146 | `microsoft/semantic-kernel` | `code_only` | `python` | Encode OpenAPI server variable values |
| https://github.com/microsoft/semantic-kernel/pull/14122 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: feat(ollama): add Think property to OllamaPromptExecutionSettings |
| https://github.com/microsoft/semantic-kernel/pull/14141 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Bump Python version to 1.44.0 for a release |

## Reject Summary Sample

| Repository | PR | Reason | Bucket |
| --- | ---: | --- | --- |
| `microsoft/TypeScript-go` | `4921` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4701` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4364` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4712` | `too_many_changed_files` | `code_and_docs` |
| `microsoft/TypeScript-go` | `4775` | `too_many_changed_files` | `code_only` |
| `microsoft/TypeScript-go` | `4849` | `too_many_changed_files` | `code_only` |
| `microsoft/TypeScript-go` | `1966` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `3331` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4919` | `docs_only_excluded` | `docs_only` |
| `microsoft/TypeScript-go` | `4858` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4914` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4911` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4903` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4902` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4865` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4846` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4841` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4779` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4733` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4726` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4716` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4674` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4666` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4653` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4600` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4597` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4596` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4555` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4496` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4446` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4440` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4422` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4418` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4297` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4211` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4200` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4197` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4102` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `3996` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `3943` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `3935` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `3728` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `3726` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `3690` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `3619` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `3385` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `3369` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `3362` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `3297` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `717` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4915` | `too_large_patch` | `code_and_docs` |
| `microsoft/TypeScript-go` | `4336` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4852` | `too_many_changed_files` | `code_only` |
| `microsoft/TypeScript-go` | `4248` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `3826` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `3630` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4650` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4786` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4274` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4592` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4912` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4450` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4449` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4803` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4564` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4703` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4741` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4530` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4907` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4847` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4905` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `3375` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4343` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `3720` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4829` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4551` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4646` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4855` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `3949` | `too_many_changed_files` | `code_only` |
| `microsoft/TypeScript-go` | `4409` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4268` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `3990` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4623` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `3840` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4605` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4808` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4649` | `not_merged` | `None` |
| `torbido-hq/cicerone` | `132` | `not_merged` | `None` |
| `torbido-hq/cicerone` | `134` | `docs_only_excluded` | `docs_only` |
| `torbido-hq/cicerone` | `126` | `not_merged` | `None` |
| `torbido-hq/cicerone` | `128` | `not_merged` | `None` |
| `torbido-hq/cicerone` | `127` | `not_merged` | `None` |
| `torbido-hq/cicerone` | `125` | `not_merged` | `None` |
| `torbido-hq/cicerone` | `124` | `not_merged` | `None` |
| `torbido-hq/cicerone` | `123` | `not_merged` | `None` |
| `torbido-hq/cicerone` | `122` | `not_merged` | `None` |
| `torbido-hq/cicerone` | `110` | `too_many_changed_files` | `code_and_docs` |
| `torbido-hq/cicerone` | `120` | `docs_only_excluded` | `docs_only` |
| `torbido-hq/cicerone` | `116` | `docs_only_excluded` | `docs_only` |
| `torbido-hq/cicerone` | `118` | `docs_only_excluded` | `docs_only` |
| `torbido-hq/cicerone` | `117` | `docs_only_excluded` | `docs_only` |
| `torbido-hq/cicerone` | `115` | `docs_only_excluded` | `docs_only` |
| `torbido-hq/cicerone` | `114` | `docs_only_excluded` | `docs_only` |
| `torbido-hq/cicerone` | `113` | `docs_only_excluded` | `docs_only` |
| `torbido-hq/cicerone` | `111` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `torbido-hq/cicerone` | `108` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `torbido-hq/cicerone` | `106` | `docs_only_excluded` | `docs_only` |
| `torbido-hq/cicerone` | `104` | `too_many_changed_files` | `code_and_docs` |
| `torbido-hq/cicerone` | `103` | `docs_only_excluded` | `docs_only` |
| `torbido-hq/cicerone` | `105` | `docs_only_excluded` | `docs_only` |
| `torbido-hq/cicerone` | `102` | `docs_only_excluded` | `docs_only` |
| `torbido-hq/cicerone` | `98` | `too_many_changed_files` | `code_and_docs` |
| `torbido-hq/cicerone` | `99` | `not_merged` | `None` |
| `torbido-hq/cicerone` | `90` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `torbido-hq/cicerone` | `89` | `docs_only_excluded` | `docs_only` |
| `torbido-hq/cicerone` | `86` | `not_merged` | `None` |
| `torbido-hq/cicerone` | `88` | `not_merged` | `None` |
| `torbido-hq/cicerone` | `87` | `not_merged` | `None` |
| `torbido-hq/cicerone` | `85` | `not_merged` | `None` |
| `torbido-hq/cicerone` | `75` | `too_many_changed_files` | `code_and_docs` |
| `torbido-hq/cicerone` | `80` | `not_merged` | `None` |
| `torbido-hq/cicerone` | `79` | `not_merged` | `None` |
| `torbido-hq/cicerone` | `74` | `not_merged` | `None` |
| `torbido-hq/cicerone` | `70` | `not_merged` | `None` |
| `torbido-hq/cicerone` | `71` | `not_merged` | `None` |
| `torbido-hq/cicerone` | `69` | `not_merged` | `None` |
| `torbido-hq/cicerone` | `73` | `docs_only_excluded` | `docs_only` |
| `torbido-hq/cicerone` | `72` | `too_large_patch` | `code_and_docs` |
| `torbido-hq/cicerone` | `67` | `not_merged` | `None` |
| `torbido-hq/cicerone` | `66` | `not_merged` | `None` |
| `torbido-hq/cicerone` | `65` | `not_merged` | `None` |
| `torbido-hq/cicerone` | `64` | `not_merged` | `None` |
| `torbido-hq/cicerone` | `62` | `not_merged` | `None` |
| `torbido-hq/cicerone` | `63` | `not_merged` | `None` |
| `﻿ragpark/controltower` | `None` | `fetch_closed_pulls_failed` | `None` |
| `CryptoJones/omind` | `260` | `docs_only_excluded` | `docs_only` |
| `CryptoJones/omind` | `252` | `docs_only_excluded` | `docs_only` |
| `CryptoJones/omind` | `246` | `docs_only_excluded` | `docs_only` |
| `CryptoJones/omind` | `244` | `docs_only_excluded` | `docs_only` |
| `CryptoJones/omind` | `233` | `docs_only_excluded` | `docs_only` |
| `d-hinders/Haven-AI` | `2040` | `docs_only_excluded` | `docs_only` |
| `d-hinders/Haven-AI` | `2019` | `docs_only_excluded` | `docs_only` |
| `d-hinders/Haven-AI` | `1974` | `too_many_changed_files` | `code_and_docs` |
| `d-hinders/Haven-AI` | `2018` | `docs_only_excluded` | `docs_only` |
| `d-hinders/Haven-AI` | `2015` | `too_many_changed_files` | `code_and_docs` |
| `d-hinders/Haven-AI` | `2008` | `too_large_patch` | `code_and_docs` |
| `d-hinders/Haven-AI` | `2005` | `too_large_patch` | `code_and_docs` |
| `microsoft/autogen` | `7394` | `not_merged` | `None` |
| `microsoft/autogen` | `7861` | `not_merged` | `None` |
| `microsoft/autogen` | `7857` | `not_merged` | `None` |
| `microsoft/autogen` | `7860` | `not_merged` | `None` |
| `microsoft/autogen` | `7864` | `not_merged` | `None` |
| `microsoft/autogen` | `7863` | `not_merged` | `None` |
| `microsoft/autogen` | `7856` | `not_merged` | `None` |
| `microsoft/autogen` | `7855` | `not_merged` | `None` |
| `microsoft/autogen` | `7937` | `not_merged` | `None` |
| `microsoft/autogen` | `7831` | `not_merged` | `None` |
| `microsoft/autogen` | `7642` | `not_merged` | `None` |
| `microsoft/autogen` | `7582` | `not_merged` | `None` |
| `microsoft/autogen` | `8055` | `not_merged` | `None` |
| `microsoft/autogen` | `8054` | `not_merged` | `None` |
| `microsoft/autogen` | `7952` | `not_merged` | `None` |
| `microsoft/autogen` | `7169` | `not_merged` | `None` |
| `microsoft/autogen` | `7816` | `not_merged` | `None` |
| `microsoft/autogen` | `7981` | `not_merged` | `None` |
| `microsoft/autogen` | `7975` | `not_merged` | `None` |
| `microsoft/autogen` | `8004` | `not_merged` | `None` |
| `microsoft/autogen` | `7969` | `not_merged` | `None` |
| `microsoft/autogen` | `7972` | `not_merged` | `None` |
| `microsoft/autogen` | `7976` | `not_merged` | `None` |
| `microsoft/autogen` | `7607` | `not_merged` | `None` |
| `microsoft/autogen` | `7211` | `not_merged` | `None` |
| `microsoft/autogen` | `7198` | `not_merged` | `None` |
| `microsoft/autogen` | `7958` | `not_merged` | `None` |
| `microsoft/autogen` | `7957` | `not_merged` | `None` |
| `microsoft/autogen` | `7858` | `not_merged` | `None` |
| `microsoft/autogen` | `7652` | `not_merged` | `None` |
| `microsoft/autogen` | `7962` | `not_merged` | `None` |
| `microsoft/autogen` | `7880` | `not_merged` | `None` |
| `microsoft/autogen` | `7882` | `not_merged` | `None` |
| `microsoft/autogen` | `7932` | `not_merged` | `None` |
| `microsoft/autogen` | `7940` | `not_merged` | `None` |
| `microsoft/autogen` | `7333` | `not_merged` | `None` |
| `microsoft/autogen` | `7777` | `not_merged` | `None` |
| `microsoft/autogen` | `7934` | `not_merged` | `None` |
| `microsoft/autogen` | `7699` | `not_merged` | `None` |
| `microsoft/autogen` | `7581` | `not_merged` | `None` |
| `microsoft/autogen` | `7424` | `not_merged` | `None` |
| `microsoft/autogen` | `7414` | `not_merged` | `None` |
| `microsoft/autogen` | `7396` | `not_merged` | `None` |
| `microsoft/autogen` | `7390` | `not_merged` | `None` |
| `microsoft/autogen` | `7389` | `not_merged` | `None` |
| `microsoft/autogen` | `7734` | `not_merged` | `None` |
| `microsoft/autogen` | `7738` | `not_merged` | `None` |
| `microsoft/autogen` | `7756` | `not_merged` | `None` |
| `microsoft/autogen` | `7751` | `not_merged` | `None` |
| `microsoft/autogen` | `7744` | `not_merged` | `None` |
| `microsoft/autogen` | `7740` | `not_merged` | `None` |
| `microsoft/autogen` | `7735` | `not_merged` | `None` |
| `microsoft/autogen` | `7733` | `not_merged` | `None` |