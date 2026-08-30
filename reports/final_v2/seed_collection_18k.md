# DocGuard Real PR Seed Collector Report

This report summarizes neutral repo-based sampling of merged public GitHub PRs.

The collector does not assign gold labels and does not decide whether documentation should be updated.
It only creates seed PR URLs for the later candidate builder and manual validation workflow.

- Repositories scanned: `191`
- Seeds accepted: `5619`
- Rejected/skipped PRs: `6827`
- Collector bucket counts: `{'code_only': 3919, 'code_only_tests_or_fixtures': 292, 'code_and_docs': 1408}`
- Language hint counts: `{'go': 180, 'python': 2850, 'typescript': 2589}`
- Repository counts per language: `{'go': 1, 'python': 17, 'typescript': 16}`
- Candidate bucket counts per language: `{'go': {'code_only': 173, 'code_only_tests_or_fixtures': 4, 'code_and_docs': 3}, 'python': {'code_and_docs': 706, 'code_only': 1994, 'code_only_tests_or_fixtures': 150}, 'typescript': {'code_and_docs': 699, 'code_only_tests_or_fixtures': 138, 'code_only': 1752}}`
- Reject reason counts: `{'not_merged': 4684, 'too_many_changed_files': 446, 'docs_only_excluded': 684, 'too_large_patch': 150, 'other_or_binary_only_excluded': 685, 'fetch_closed_pulls_failed': 158, 'fetch_pr_files_failed': 20}`

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
| https://github.com/microsoft/typescript-go/pull/3871 | `microsoft/TypeScript-go` | `code_only` | `go` | Use named-function overload diagnostic for JSDoc `@overload` return-type omissions |
| https://github.com/microsoft/typescript-go/pull/4881 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix TS1515 not reported when duplicate named group is nested inside a group |
| https://github.com/microsoft/typescript-go/pull/4832 | `microsoft/TypeScript-go` | `code_only` | `go` | Report TS1518 for all negated Unicode-set union operands |
| https://github.com/microsoft/typescript-go/pull/4734 | `microsoft/TypeScript-go` | `code_only` | `go` | Add Android ARM64 release target |
| https://github.com/microsoft/typescript-go/pull/4695 | `microsoft/TypeScript-go` | `code_only` | `go` | Update imports in unloaded composite projects after file rename |
| https://github.com/microsoft/typescript-go/pull/4896 | `microsoft/TypeScript-go` | `code_only` | `go` | Keep LSP server alive after response marshal failures |
| https://github.com/microsoft/typescript-go/pull/4894 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix hover for merged generic namespace exports |
| https://github.com/microsoft/typescript-go/pull/4240 | `microsoft/TypeScript-go` | `code_only` | `go` | Inline `GetCombinedNodeFlags` and `GetCombinedModifierFlags` bodies |
| https://github.com/microsoft/typescript-go/pull/4887 | `microsoft/TypeScript-go` | `code_only` | `go` | Make `NodeHandle` generic and generate .Handle members of is-guards for guarding node handles (sync and async) |
| https://github.com/microsoft/typescript-go/pull/4901 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix diagnostics lookup across source file replacements |
| https://github.com/microsoft/typescript-go/pull/4866 | `microsoft/TypeScript-go` | `code_only` | `go` | Add `--clientProcessId` like reference LSP server |
| https://github.com/microsoft/typescript-go/pull/4762 | `microsoft/TypeScript-go` | `code_only` | `go` | Prevent panic and duplicate diagnostics for malformed tsconfig properties |
| https://github.com/microsoft/typescript-go/pull/4897 | `microsoft/TypeScript-go` | `code_only` | `go` | Add checker.getSymbolsInScope to native-preview API |
| https://github.com/microsoft/typescript-go/pull/4893 | `microsoft/TypeScript-go` | `code_only` | `go` | [api] Move language service methods into dedicated namespace |
| https://github.com/microsoft/typescript-go/pull/4313 | `microsoft/TypeScript-go` | `code_only` | `go` | Assign files to checkers using balanced import affinity |
| https://github.com/microsoft/typescript-go/pull/4888 | `microsoft/TypeScript-go` | `code_only` | `go` | Port `parseCommandLine`, `readConfigFile`, and `parseJsonConfigFileContent` |
| https://github.com/microsoft/typescript-go/pull/4218 | `microsoft/TypeScript-go` | `code_only` | `go` | Allow lone & in Unicode sets regexp classes |
| https://github.com/microsoft/typescript-go/pull/4891 | `microsoft/TypeScript-go` | `code_only` | `go` | Update submodule |
| https://github.com/microsoft/typescript-go/pull/4825 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix deprecated contextual property memory regression |
| https://github.com/microsoft/typescript-go/pull/2914 | `microsoft/TypeScript-go` | `code_only` | `go` | adds tracing (--generateTrace) |
| https://github.com/microsoft/typescript-go/pull/4879 | `microsoft/TypeScript-go` | `code_only_tests_or_fixtures` | `go` | Fix Darwin realpath test lint failures |
| https://github.com/microsoft/typescript-go/pull/4872 | `microsoft/TypeScript-go` | `code_only` | `go` | Preserve local auto-imports in circular workspace symlink topologies |
| https://github.com/microsoft/typescript-go/pull/4867 | `microsoft/TypeScript-go` | `code_only` | `go` | Remove macOS realpath fast path |
| https://github.com/microsoft/typescript-go/pull/4557 | `microsoft/TypeScript-go` | `code_only` | `go` | Account nested declaration emits as emit time |
| https://github.com/microsoft/typescript-go/pull/4823 | `microsoft/TypeScript-go` | `code_only` | `go` | Preserve await context for exported classes in nested containers |
| https://github.com/microsoft/typescript-go/pull/4848 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix watch diagnostics when global declaration is removed |
| https://github.com/microsoft/typescript-go/pull/4661 | `microsoft/TypeScript-go` | `code_only` | `go` | Fall back to inotify when filesystem has errors in fanotify (fix watch in Docker) |
| https://github.com/microsoft/typescript-go/pull/4628 | `microsoft/TypeScript-go` | `code_only` | `go` | Handle extensionless root files gracefully instead of panicking |
| https://github.com/microsoft/typescript-go/pull/4805 | `microsoft/TypeScript-go` | `code_only` | `go` | Support js/ts.workspaceSymbols.scope and extra textDocument param on workspace/symbol request |
| https://github.com/microsoft/typescript-go/pull/4845 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix LSP Watcher panic when Close races with WatchFiles |
| https://github.com/microsoft/typescript-go/pull/4820 | `microsoft/TypeScript-go` | `code_only` | `go` | Order variance computation by associated type symbol |
| https://github.com/microsoft/typescript-go/pull/4813 | `microsoft/TypeScript-go` | `code_only` | `go` | Avoid false symlink mappings for physical dependencies |
| https://github.com/microsoft/typescript-go/pull/4309 | `microsoft/TypeScript-go` | `code_only` | `go` | feat(4294): report deprecated diagnostics for contextual props |
| https://github.com/microsoft/typescript-go/pull/4798 | `microsoft/TypeScript-go` | `code_only` | `go` | Avoid temporary composite mapper allocations |
| https://github.com/microsoft/typescript-go/pull/4781 | `microsoft/TypeScript-go` | `code_only` | `go` | Optimize `narrowTypeByEquality` and `narrowTypeBySwitchOnDiscriminant` |
| https://github.com/microsoft/typescript-go/pull/4799 | `microsoft/TypeScript-go` | `code_only` | `go` | Refresh tsconfig/jsconfig diagnostics without relying on the client to re-pull |
| https://github.com/microsoft/typescript-go/pull/4796 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix O(K^2) OOM issue in go-to-implementation |
| https://github.com/microsoft/typescript-go/pull/4655 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix stack overflow in `getExplicitTypeOfSymbol()` for self-referential `for...of` |
| https://github.com/microsoft/typescript-go/pull/4793 | `microsoft/TypeScript-go` | `code_only` | `go` | chore: Fix typo in variable name for diagnostic context setup. |
| https://github.com/microsoft/typescript-go/pull/4658 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix build mode setup stall on large solutions |
| https://github.com/microsoft/typescript-go/pull/4778 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix "Not a subspan" crash in signature help on error-recovered JSX |
| https://github.com/microsoft/typescript-go/pull/4776 | `microsoft/TypeScript-go` | `code_only` | `go` | Remove easily-removable wasted work in parse/bind |
| https://github.com/microsoft/typescript-go/pull/4792 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix program reuse across resolution mode changes |
| https://github.com/microsoft/typescript-go/pull/4577 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix stack overflow in inherited JSDoc resolution |
| https://github.com/microsoft/typescript-go/pull/4399 | `microsoft/TypeScript-go` | `code_only` | `go` | Watcher performance improvements |
| https://github.com/microsoft/typescript-go/pull/4699 | `microsoft/TypeScript-go` | `code_only` | `go` | API emit |
| https://github.com/microsoft/typescript-go/pull/4783 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix module specifier rename trigger spans |
| https://github.com/microsoft/typescript-go/pull/4787 | `microsoft/TypeScript-go` | `code_only` | `go` | Check the arrow-function line-terminator rule without the line map |
| https://github.com/microsoft/typescript-go/pull/4785 | `microsoft/TypeScript-go` | `code_only` | `go` | Skip the speculative expression parse in the async arrow lookahead |
| https://github.com/microsoft/typescript-go/pull/4711 | `microsoft/TypeScript-go` | `code_only` | `go` | Optimize `getAssignmentReducedType` in CFA |
| https://github.com/microsoft/typescript-go/pull/4788 | `microsoft/TypeScript-go` | `code_only` | `go` | Embed zero-size marker bases first in generated AST structs |
| https://github.com/microsoft/typescript-go/pull/4710 | `microsoft/TypeScript-go` | `code_only` | `go` | Add an LSP init flag that enables flaky diagnostics tracking |
| https://github.com/microsoft/typescript-go/pull/4764 | `microsoft/TypeScript-go` | `code_only` | `go` | Remove unused classifiable name tracking |
| https://github.com/microsoft/typescript-go/pull/4604 | `microsoft/TypeScript-go` | `code_only` | `go` | fix: prevent unnecessary diagnostic refreshes on irrelevant watch events (#4589) |
| https://github.com/microsoft/typescript-go/pull/4770 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix rewritten CJS dynamic import arguments |
| https://github.com/microsoft/typescript-go/pull/4731 | `microsoft/TypeScript-go` | `code_only` | `go` | Lazily collect source file identifiers |
| https://github.com/microsoft/typescript-go/pull/4765 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix quadratic slowdown when renaming files with duplicate unresolved imports |
| https://github.com/microsoft/typescript-go/pull/4759 | `microsoft/TypeScript-go` | `code_only` | `go` | Restore spelling suggestions for unknown tsconfig options |
| https://github.com/microsoft/typescript-go/pull/4761 | `microsoft/TypeScript-go` | `code_only` | `go` | Report compiler options misplaced at the tsconfig root |
| https://github.com/microsoft/typescript-go/pull/3102 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix a formatting crash caused by template literal in parser-recovered property signature |
| https://github.com/microsoft/typescript-go/pull/4760 | `microsoft/TypeScript-go` | `code_only` | `go` | Restore source location for TS5092 |
| https://github.com/microsoft/typescript-go/pull/4744 | `microsoft/TypeScript-go` | `code_only` | `go` | Reorganize AST to prevent duplicate fields |
| https://github.com/microsoft/typescript-go/pull/4746 | `microsoft/TypeScript-go` | `code_only` | `go` | fix: emit missing TS7059 errors |
| https://github.com/microsoft/typescript-go/pull/2628 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix dedupe/redirect nondeterminism |
| https://github.com/microsoft/typescript-go/pull/4735 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix panic in variadic tuple relationship checking |
| https://github.com/microsoft/typescript-go/pull/4724 | `microsoft/TypeScript-go` | `code_only` | `go` | [api] Add proper ParsedCommandLine type, provide APIs for getting config source files |
| https://github.com/microsoft/typescript-go/pull/4566 | `microsoft/TypeScript-go` | `code_only` | `go` | Use published packages for stable releases |
| https://github.com/microsoft/typescript-go/pull/4660 | `microsoft/TypeScript-go` | `code_only` | `go` | Respect configured TypeScript diagnostic locale |
| https://github.com/microsoft/typescript-go/pull/4725 | `microsoft/TypeScript-go` | `code_only` | `go` | Show repopulate info in readable buildinfo |
| https://github.com/microsoft/typescript-go/pull/4708 | `microsoft/TypeScript-go` | `code_only` | `go` | Add lint rule for identifying common patterns in the checker that lead to inconsistent diagnostic output |
| https://github.com/microsoft/typescript-go/pull/4665 | `microsoft/TypeScript-go` | `code_only` | `go` | Return all files from getFilesAffectedBy when a changed file affects global scope |
| https://github.com/microsoft/typescript-go/pull/4602 | `microsoft/TypeScript-go` | `code_only` | `go` | fix(lsp): respect editor formatting in organize imports |
| https://github.com/microsoft/typescript-go/pull/4329 | `microsoft/TypeScript-go` | `code_only` | `go` | Paged link stores with fallback from array to map representation |
| https://github.com/microsoft/typescript-go/pull/4606 | `microsoft/TypeScript-go` | `code_only` | `go` | Keep dependent destructuring narrowing during re-entrant checks |
| https://github.com/microsoft/typescript-go/pull/4663 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix crash: JSTypeAliasDeclaration passed to GetTypeOfDeclaration during CJS declaration emit |
| https://github.com/microsoft/typescript-go/pull/4694 | `microsoft/TypeScript-go` | `code_only` | `go` | Recognize jsxImportSource namespaces in checked JavaScript |
| https://github.com/microsoft/typescript-go/pull/4691 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix over-eager `isMatchingConstructorReference` function |
| https://github.com/microsoft/typescript-go/pull/4654 | `microsoft/TypeScript-go` | `code_only` | `go` | Use canonical paths for the semantic tokens defaultLibrary check |
| https://github.com/microsoft/typescript-go/pull/4561 | `microsoft/TypeScript-go` | `code_only` | `go` | Resolve native-preview tsdk symlinks before locating platform package |
| https://github.com/microsoft/typescript-go/pull/4591 | `microsoft/TypeScript-go` | `code_only` | `go` | Sort by type depth in `inferFromMatchingTypes` function |
| https://github.com/microsoft/typescript-go/pull/4687 | `microsoft/TypeScript-go` | `code_only` | `go` | Optimize construction of union types |
| https://github.com/microsoft/typescript-go/pull/4689 | `microsoft/TypeScript-go` | `code_only` | `go` | [api] Add Type convenience methods, cache consistently |
| https://github.com/microsoft/typescript-go/pull/4627 | `microsoft/TypeScript-go` | `code_only` | `go` | [api] Include `projectReferences` in parsed config |
| https://github.com/microsoft/typescript-go/pull/4556 | `microsoft/TypeScript-go` | `code_only` | `go` | Add getConstraint() and getDefault() getters to TypeParameter |
| https://github.com/microsoft/typescript-go/pull/4688 | `microsoft/TypeScript-go` | `code_only` | `go` |  smart-selection ranges for mapped types |
| https://github.com/microsoft/typescript-go/pull/4651 | `microsoft/TypeScript-go` | `code_only` | `go` | Do not issue diagnostics when fetching parameter types for context-sensitive parameters |
| https://github.com/microsoft/typescript-go/pull/4662 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix declaration emit synthesizing extensionless import() specifier under allowImportingTsExtensions + nodenext |
| https://github.com/microsoft/typescript-go/pull/4657 | `microsoft/TypeScript-go` | `code_only` | `go` | Add even more bails on unchecked identifiers to markLinkedReferences |
| https://github.com/microsoft/typescript-go/pull/4586 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix TS2871 false positive for `??` operator in nullish coalescing check |
| https://github.com/microsoft/typescript-go/pull/4565 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix stack overflow in `checkTypeExpandability()` |
| https://github.com/microsoft/typescript-go/pull/4656 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix nil pointer dereference in signature help for error-recovered parameter types |
| https://github.com/microsoft/typescript-go/pull/4640 | `microsoft/TypeScript-go` | `code_only` | `go` | Always accumulate deferred diagnostics |
| https://github.com/microsoft/typescript-go/pull/4648 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix declaration emit crash on export assigned arrow function using external name |
| https://github.com/microsoft/typescript-go/pull/4637 | `microsoft/TypeScript-go` | `code_only` | `go` | Skip project recheck for no-op file watch events |
| https://github.com/microsoft/typescript-go/pull/4641 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix computed name error emit reusing the name expression cache |
| https://github.com/microsoft/typescript-go/pull/4594 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix "Token end is child end" crash when range formatting is inside a JSDoc comment |
| https://github.com/microsoft/typescript-go/pull/4636 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix emit mistakenly marking enums used in their own emit as used for unused refs errors |
| https://github.com/microsoft/typescript-go/pull/4639 | `microsoft/TypeScript-go` | `code_only` | `go` | Make JSX missing module error span be issued at a stable location |
| https://github.com/microsoft/typescript-go/pull/4642 | `microsoft/TypeScript-go` | `code_only` | `go` | Add `runWithTemporaryFileUpdate` to API |
| https://github.com/microsoft/typescript-go/pull/4643 | `microsoft/TypeScript-go` | `code_only` | `go` | [api] Use super(length) to avoid RemoteNodeArray array subclass deopt |
| https://github.com/microsoft/typescript-go/pull/3881 | `microsoft/TypeScript-go` | `code_only` | `go` | Expose ImportAdder to IPC API |
| https://github.com/microsoft/typescript-go/pull/4494 | `microsoft/TypeScript-go` | `code_only` | `go` | fix(tsoptions): validate project reference fields |
| https://github.com/microsoft/typescript-go/pull/4562 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix concurrent extractionCache read/write |
| https://github.com/microsoft/typescript-go/pull/4569 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix more return types that can’t actually be undefined |
| https://github.com/microsoft/typescript-go/pull/4535 | `microsoft/TypeScript-go` | `code_only` | `go` | Emit expando properties for functions that only become visible late in declaration emit |
| https://github.com/microsoft/typescript-go/pull/4558 | `microsoft/TypeScript-go` | `code_only` | `go` | Prepare main for 7.1 nightly builds |
| https://github.com/microsoft/typescript-go/pull/4541 | `microsoft/TypeScript-go` | `code_only` | `go` | Bump the github-actions group across 1 directory with 3 updates |
| https://github.com/microsoft/typescript-go/pull/4550 | `microsoft/TypeScript-go` | `code_and_docs` | `go` | Set up stable / nightly extension split, other prep |
| https://github.com/microsoft/typescript-go/pull/4549 | `microsoft/TypeScript-go` | `code_only` | `go` | [api] Optimize RemoteNodeList child access |
| https://github.com/microsoft/typescript-go/pull/4554 | `microsoft/TypeScript-go` | `code_only` | `go` | Move dprint plugins to npm |
| https://github.com/microsoft/typescript-go/pull/4366 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix namespaced JSX intrinsic completions and hover |
| https://github.com/microsoft/typescript-go/pull/4543 | `microsoft/TypeScript-go` | `code_only` | `go` | New setting to control whether error notifications are displayed |
| https://github.com/microsoft/typescript-go/pull/4489 | `microsoft/TypeScript-go` | `code_and_docs` | `go` | New extension layout |
| https://github.com/microsoft/typescript-go/pull/4546 | `microsoft/TypeScript-go` | `code_only` | `go` | Release configs of removed project references |
| https://github.com/microsoft/typescript-go/pull/4547 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix bulk cache invalidation of non-existent referenced configs |
| https://github.com/microsoft/typescript-go/pull/4542 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix data race in `snapshotFSBuilder.GetAccessibleEntries()` |
| https://github.com/microsoft/typescript-go/pull/4529 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix wildcard directories being dropped for "./"-prefixed includes with dot-directory excludes |
| https://github.com/microsoft/typescript-go/pull/4420 | `microsoft/TypeScript-go` | `code_only` | `go` | [api] Add SourceFile line mapping methods |
| https://github.com/microsoft/typescript-go/pull/4522 | `microsoft/TypeScript-go` | `code_only` | `go` | [api] Fix panic in handleGetCompletionsAtPosition |
| https://github.com/microsoft/typescript-go/pull/4512 | `microsoft/TypeScript-go` | `code_only` | `go` | [api] Add option to collect timing info |
| https://github.com/microsoft/typescript-go/pull/4523 | `microsoft/TypeScript-go` | `code_only` | `go` | Move ID error to favor class expression inference failure when present |
| https://github.com/microsoft/typescript-go/pull/4483 | `microsoft/TypeScript-go` | `code_only` | `go` | Handle unloaded projects in API snapshot responses |
| https://github.com/microsoft/typescript-go/pull/4518 | `microsoft/TypeScript-go` | `code_only` | `go` | Remove runtime metric logging |
| https://github.com/microsoft/typescript-go/pull/4517 | `microsoft/TypeScript-go` | `code_only` | `go` | Move ID error for accessor inference failure from return expression to (both) accessors |
| https://github.com/microsoft/typescript-go/pull/4516 | `microsoft/TypeScript-go` | `code_only` | `go` | [api] Add CompilerOptions type |
| https://github.com/microsoft/typescript-go/pull/4514 | `microsoft/TypeScript-go` | `code_only` | `go` | Move ID inferred param errors to the param from the initializer |
| https://github.com/microsoft/typescript-go/pull/4513 | `microsoft/TypeScript-go` | `code_only` | `go` | Don't emit follow-on ID errors on expando props that get an expando prop ID error |
| https://github.com/microsoft/typescript-go/pull/4510 | `microsoft/TypeScript-go` | `code_only` | `go` | [api] Port ts.getJSDocTags and related utilities |
| https://github.com/microsoft/typescript-go/pull/4495 | `microsoft/TypeScript-go` | `code_and_docs` | `go` | Fix fswatch coalescing |
| https://github.com/microsoft/typescript-go/pull/4509 | `microsoft/TypeScript-go` | `code_only` | `go` | Add missing isolatedDeclarations error on non-simple class base expressions |
| https://github.com/microsoft/typescript-go/pull/4488 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix project-reference redirect bug for symlinked subpaths |
| https://github.com/microsoft/typescript-go/pull/4508 | `microsoft/TypeScript-go` | `code_only` | `go` | Names from expanded param lists shouldnt block lookups within those param lists |
| https://github.com/microsoft/typescript-go/pull/4507 | `microsoft/TypeScript-go` | `code_only` | `go` | Allow declaration emit to consider variable assigned function expressions for `typeof` printback |
| https://github.com/microsoft/typescript-go/pull/4504 | `microsoft/TypeScript-go` | `code_only` | `go` | [api] Use stable order for symbol tables |
| https://github.com/microsoft/typescript-go/pull/4487 | `microsoft/TypeScript-go` | `code_only` | `go` | Rename LSP push diag collection |
| https://github.com/microsoft/typescript-go/pull/4346 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix RemoteNodeList inherited array methods throwing `this.view.getUint32 is not a function` |
| https://github.com/microsoft/typescript-go/pull/4497 | `microsoft/TypeScript-go` | `code_only` | `go` | [api] Fix compatibility with older @types/node and exactOptionalPropertyTypes |
| https://github.com/microsoft/typescript-go/pull/4498 | `microsoft/TypeScript-go` | `code_only` | `go` | [api] Fix generated .text type for JSDocText |
| https://github.com/microsoft/typescript-go/pull/4493 | `microsoft/TypeScript-go` | `code_only` | `go` | [api] Batch of improvements, fixes, and additions |
| https://github.com/microsoft/typescript-go/pull/4490 | `microsoft/TypeScript-go` | `code_only` | `go` | Fixed formatting for dotted tag names |
| https://github.com/microsoft/typescript-go/pull/4492 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix jsdoc type reference reuse check TODO to use new corsa jsdoc node remapping logic |
| https://github.com/microsoft/typescript-go/pull/4491 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix fswatch on windows |
| https://github.com/microsoft/typescript-go/pull/3518 | `microsoft/TypeScript-go` | `code_only` | `go` | fix(native-preview): preserve lone surrogate string literals |
| https://github.com/microsoft/typescript-go/pull/4485 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix const enum elision on merged symbols |
| https://github.com/microsoft/typescript-go/pull/4480 | `microsoft/TypeScript-go` | `code_only` | `go` | Run symbol-returning completion on the API checker |
| https://github.com/microsoft/typescript-go/pull/4479 | `microsoft/TypeScript-go` | `code_only` | `go` | Avoid nil package.json crash when resolving peer dependencies |
| https://github.com/microsoft/typescript-go/pull/4477 | `microsoft/TypeScript-go` | `code_only` | `go` | Update submodule |
| https://github.com/microsoft/typescript-go/pull/4468 | `microsoft/TypeScript-go` | `code_only` | `go` | Add conditional type base constraint limiter |
| https://github.com/microsoft/typescript-go/pull/4473 | `microsoft/TypeScript-go` | `code_only` | `go` | Fix RemoteNode.forEachChild visiting array children twice when a visitList callback is supplied |
| https://github.com/microsoft/typescript-go/pull/4395 | `microsoft/TypeScript-go` | `code_only` | `go` | Devirtualize ForEachChild and IterChildren |
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
| https://github.com/torbido-hq/cicerone/pull/58 | `torbido-hq/cicerone` | `code_and_docs` | `python` | Optional distributed lock for scheduler HA |
| https://github.com/torbido-hq/cicerone/pull/47 | `torbido-hq/cicerone` | `code_and_docs` | `python` | Three-tier fallback: default item_based + optional content cold-item |
| https://github.com/torbido-hq/cicerone/pull/45 | `torbido-hq/cicerone` | `code_and_docs` | `python` | Serve OpenAPI schema + thin client examples |
| https://github.com/torbido-hq/cicerone/pull/44 | `torbido-hq/cicerone` | `code_and_docs` | `python` | 0.4.0: weighted multi-source blending + serve read contract |
| https://github.com/torbido-hq/cicerone/pull/38 | `torbido-hq/cicerone` | `code_and_docs` | `python` | Pythonic cleanup of the whole implementation |
| https://github.com/torbido-hq/cicerone/pull/42 | `torbido-hq/cicerone` | `code_and_docs` | `python` | LightFM hardening 0.3.2: top-K audit, epoch metrics, native eval docs |
| https://github.com/torbido-hq/cicerone/pull/36 | `torbido-hq/cicerone` | `code_and_docs` | `python` | Add declarative eligibility and boost policy layer |
| https://github.com/torbido-hq/cicerone/pull/35 | `torbido-hq/cicerone` | `code_and_docs` | `python` | Add compose Postgres, system DB e2e, and docs for latest features |
| https://github.com/torbido-hq/cicerone/pull/27 | `torbido-hq/cicerone` | `code_and_docs` | `python` | Add optional versioned fitted-model artifact |
| https://github.com/torbido-hq/cicerone/pull/25 | `torbido-hq/cicerone` | `code_and_docs` | `python` | Parallelize AutoML folds, strategy fitting, and job input reads |
| https://github.com/torbido-hq/cicerone/pull/24 | `torbido-hq/cicerone` | `code_and_docs` | `python` | Release 0.2.0: documentation fixes + changelog |
| https://github.com/torbido-hq/cicerone/pull/22 | `torbido-hq/cicerone` | `code_and_docs` | `python` | Add serve mode and event-driven retrain trigger |
| https://github.com/torbido-hq/cicerone/pull/21 | `torbido-hq/cicerone` | `code_and_docs` | `python` | Batch dependency updates (sqlalchemy/types-croniter/pyarrow/s3fs+boto3), getting-started tutorial, small job.py refactor |
| https://github.com/torbido-hq/cicerone/pull/11 | `torbido-hq/cicerone` | `code_and_docs` | `python` | Add pluggable multi-model strategy registry (collaborative/item_based… |
| https://github.com/torbido-hq/cicerone/pull/12 | `torbido-hq/cicerone` | `code_and_docs` | `python` | Add weighted reciprocal rank fusion for multi-model blending |
| https://github.com/torbido-hq/cicerone/pull/20 | `torbido-hq/cicerone` | `code_and_docs` | `python` | Add AutoML candidate backtesting and selection |
| https://github.com/torbido-hq/cicerone/pull/13 | `torbido-hq/cicerone` | `code_only` | `python` | Batch dependency updates (actions/checkout, pytest-mock, ruff) + dependabot guardrail |
| https://github.com/torbido-hq/cicerone/pull/3 | `torbido-hq/cicerone` | `code_only` | `python` | Bump github/codeql-action from 3 to 4 |
| https://github.com/torbido-hq/cicerone/pull/2 | `torbido-hq/cicerone` | `code_and_docs` | `python` | Add docs and CI linting/security tooling |
| https://github.com/torbido-hq/cicerone/pull/1 | `torbido-hq/cicerone` | `code_and_docs` | `python` | Generic, TOML-based configuration and open-source rebrand |
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
| https://github.com/CryptoJones/omind/pull/220 | `CryptoJones/omind` | `code_only` | `python` | fix(guard): treat "would you ..." as a request, not a capability question |
| https://github.com/CryptoJones/omind/pull/218 | `CryptoJones/omind` | `code_only` | `python` | docs(mesh): record why `* -text` is in GITATTRIBUTES |
| https://github.com/CryptoJones/omind/pull/217 | `CryptoJones/omind` | `code_and_docs` | `python` | fix(doctor): stop printing the embed install hint twice (v8.1.1) |
| https://github.com/CryptoJones/omind/pull/216 | `CryptoJones/omind` | `code_and_docs` | `python` | fix(observability): stop reporting degraded and failed states as fine |
| https://github.com/CryptoJones/omind/pull/215 | `CryptoJones/omind` | `code_and_docs` | `python` | fix(durability): journal the migration, make the merge driver atomic |
| https://github.com/CryptoJones/omind/pull/214 | `CryptoJones/omind` | `code_and_docs` | `python` | fix(store): write notes with LF on every platform |
| https://github.com/CryptoJones/omind/pull/213 | `CryptoJones/omind` | `code_and_docs` | `python` | feat(store): journaled multi-note transactions and `omind recover` (v8.0.0) |
| https://github.com/CryptoJones/omind/pull/212 | `CryptoJones/omind` | `code_and_docs` | `python` | chore(index): name the FTS snippet column + record the declined #193 result |
| https://github.com/CryptoJones/omind/pull/211 | `CryptoJones/omind` | `code_and_docs` | `python` | fix(index): drop and recreate on a schema bump instead of deleting rows |
| https://github.com/CryptoJones/omind/pull/209 | `CryptoJones/omind` | `code_and_docs` | `python` | fix(hooks): isolate each PostToolUse side effect so one failure can't cancel enforcement |
| https://github.com/CryptoJones/omind/pull/208 | `CryptoJones/omind` | `code_and_docs` | `python` | feat(memory): typed confidence and symmetric conflict provenance (v6.6.0) |
| https://github.com/CryptoJones/omind/pull/207 | `CryptoJones/omind` | `code_and_docs` | `python` | feat(graph): rank the frontier — what to consolidate next (v6.5.0) |
| https://github.com/CryptoJones/omind/pull/206 | `CryptoJones/omind` | `code_and_docs` | `python` | docs(serve): state the unauthenticated-API risk model where it can be found (v6.4.0) |
| https://github.com/CryptoJones/omind/pull/205 | `CryptoJones/omind` | `code_and_docs` | `python` | test(hooks): pin every PostToolUse side effect, not just the detector (v6.3.0) |
| https://github.com/CryptoJones/omind/pull/203 | `CryptoJones/omind` | `code_and_docs` | `python` | fix(hardening): open the append-only writers with O_NOFOLLOW (v6.2.0) |
| https://github.com/CryptoJones/omind/pull/201 | `CryptoJones/omind` | `code_and_docs` | `python` | perf(enforcement): memoize the compliance log parse and rotate it at 8 MiB (v6.1.0) |
| https://github.com/CryptoJones/omind/pull/200 | `CryptoJones/omind` | `code_and_docs` | `python` | perf(retrieval): cache the search weighting maps per index generation (v6.0.0) |
| https://github.com/CryptoJones/omind/pull/192 | `CryptoJones/omind` | `code_and_docs` | `python` | feat!: adopt MCP revision 2026-07-28 via the mcp 2.x SDK |
| https://github.com/CryptoJones/omind/pull/185 | `CryptoJones/omind` | `code_and_docs` | `python` | chore(mcp): remove deprecated graph aliases |
| https://github.com/CryptoJones/omind/pull/184 | `CryptoJones/omind` | `code_and_docs` | `python` | fix(guard): auto-clear the per-turn gate on a genuine preflight miss (v5.0.1) |
| https://github.com/CryptoJones/omind/pull/183 | `CryptoJones/omind` | `code_and_docs` | `python` | release: v5.0.0 |
| https://github.com/CryptoJones/omind/pull/182 | `CryptoJones/omind` | `code_and_docs` | `python` | feat: complete the hybrid retrieval backlog |
| https://github.com/CryptoJones/omind/pull/180 | `CryptoJones/omind` | `code_only` | `python` | chore(deps): bump the github-actions group with 2 updates |
| https://github.com/CryptoJones/omind/pull/179 | `CryptoJones/omind` | `code_and_docs` | `python` | Feat/hybrid retrieval token budgets |
| https://github.com/CryptoJones/omind/pull/166 | `CryptoJones/omind` | `code_only` | `python` | chore(deps): bump the github-actions group with 4 updates |
| https://github.com/CryptoJones/omind/pull/165 | `CryptoJones/omind` | `code_and_docs` | `python` | chore: update CodeQL together and release 4.2.3 |
| https://github.com/CryptoJones/omind/pull/164 | `CryptoJones/omind` | `code_and_docs` | `python` | fix(guard): scope the freshness gate to git commit, and fix its hint |
| https://github.com/CryptoJones/omind/pull/163 | `CryptoJones/omind` | `code_and_docs` | `python` | fix: waive freshness outside git repositories |
| https://github.com/CryptoJones/omind/pull/157 | `CryptoJones/omind` | `code_only` | `python` | chore(deps): bump github/codeql-action/init from 4.36.2 to 4.37.0 |
| https://github.com/CryptoJones/omind/pull/156 | `CryptoJones/omind` | `code_only` | `python` | chore(deps): bump github/codeql-action/analyze from 4.36.2 to 4.37.0 |
| https://github.com/CryptoJones/omind/pull/160 | `CryptoJones/omind` | `code_and_docs` | `python` | feat: token-efficient recall and live help (v4.2.0) |
| https://github.com/CryptoJones/omind/pull/159 | `CryptoJones/omind` | `code_and_docs` | `python` | feat: AI token accounting and expense profiles (v4.0.0) |
| https://github.com/CryptoJones/omind/pull/154 | `CryptoJones/omind` | `code_only` | `python` | style(guard): wrap GIT_FRESHNESS_MESSAGE under 100 chars (fix ruff E501 from #153) |
| https://github.com/CryptoJones/omind/pull/153 | `CryptoJones/omind` | `code_and_docs` | `python` | guard: freshness-block message gives the exact remediation syntax (3.8.6) |
| https://github.com/CryptoJones/omind/pull/152 | `CryptoJones/omind` | `code_and_docs` | `python` | fix(guard): waive same-turn freshness for repos with no remote (v3.8.5) |
| https://github.com/CryptoJones/omind/pull/145 | `CryptoJones/omind` | `code_and_docs` | `python` | fix(web): strip OKF frontmatter from note body; colour graph by type |
| https://github.com/CryptoJones/omind/pull/144 | `CryptoJones/omind` | `code_and_docs` | `python` | feat(okf): read/write notes as an Open Knowledge Format bundle + omind convert |
| https://github.com/CryptoJones/omind/pull/143 | `CryptoJones/omind` | `code_and_docs` | `python` | fix(provision): write managed hook scripts atomically at 0o755 |
| https://github.com/CryptoJones/omind/pull/142 | `CryptoJones/omind` | `code_and_docs` | `python` | release: 3.7.7 |
| https://github.com/CryptoJones/omind/pull/141 | `CryptoJones/omind` | `code_and_docs` | `python` | fix(security): sanitize note HTML (XSS) and add a Host allowlist (#125) |
| https://github.com/CryptoJones/omind/pull/140 | `CryptoJones/omind` | `code_and_docs` | `python` | fix: bound graph settle + stop leaking graph render loops (#129) |
| https://github.com/CryptoJones/omind/pull/139 | `CryptoJones/omind` | `code_and_docs` | `python` | fix: lock the store's summary cache and cache the MCP graph build (#130) |
| https://github.com/CryptoJones/omind/pull/138 | `CryptoJones/omind` | `code_and_docs` | `python` | ci: add macOS matrix + wheel build/smoke-test (#126) |
| https://github.com/CryptoJones/omind/pull/137 | `CryptoJones/omind` | `code_and_docs` | `python` | chore: pin dependency upper bounds and install the fleet by tag (#131) |
| https://github.com/CryptoJones/omind/pull/136 | `CryptoJones/omind` | `code_and_docs` | `python` | fix: expire purge tombstones after a TTL so re-created notes survive (#127) |
| https://github.com/CryptoJones/omind/pull/135 | `CryptoJones/omind` | `code_and_docs` | `python` | fix: scope the autonomous-loop guard to one owner session (#128) |
| https://github.com/CryptoJones/omind/pull/124 | `CryptoJones/omind` | `code_and_docs` | `python` | fix: hardening batch from adversarial code review (v3.7.6) |
| https://github.com/CryptoJones/omind/pull/123 | `CryptoJones/omind` | `code_and_docs` | `python` | Fix explicit action authorization guard |
| https://github.com/CryptoJones/omind/pull/120 | `CryptoJones/omind` | `code_and_docs` | `python` | Fix read-only global path guard checks |
| https://github.com/CryptoJones/omind/pull/119 | `CryptoJones/omind` | `code_and_docs` | `python` | Enforce repo freshness before guarded repo work |
| https://github.com/CryptoJones/omind/pull/117 | `CryptoJones/omind` | `code_and_docs` | `python` | fix: bootstrap and trust Codex OMI hooks |
| https://github.com/CryptoJones/omind/pull/116 | `CryptoJones/omind` | `code_and_docs` | `python` | Fix Codex hooks config schema |
| https://github.com/CryptoJones/omind/pull/115 | `CryptoJones/omind` | `code_and_docs` | `python` | feat(agents): Codex CLI gets omi MCP server registration, not just guard |
| https://github.com/CryptoJones/omind/pull/110 | `CryptoJones/omind` | `code_only_tests_or_fixtures` | `python` | chore(deps): bump actions/setup-python from 5.6.0 to 6.3.0 |
| https://github.com/CryptoJones/omind/pull/94 | `CryptoJones/omind` | `code_only` | `python` | chore(deps): bump actions/checkout from 4.3.1 to 7.0.0 |
| https://github.com/CryptoJones/omind/pull/74 | `CryptoJones/omind` | `code_only` | `python` | chore(deps): bump github/codeql-action from 3.36.2 to 4.36.2 |
| https://github.com/CryptoJones/omind/pull/111 | `CryptoJones/omind` | `code_only` | `python` | chore(deps): bump github/codeql-action/init from 3.36.2 to 4.36.2 |
| https://github.com/CryptoJones/omind/pull/112 | `CryptoJones/omind` | `code_only` | `python` | chore(deps): bump github/codeql-action/analyze from 3.36.2 to 4.36.2 |
| https://github.com/CryptoJones/omind/pull/85 | `CryptoJones/omind` | `code_and_docs` | `python` | feat(setup): install the omind Claude Code skill alongside the MCP server |
| https://github.com/CryptoJones/omind/pull/84 | `CryptoJones/omind` | `code_and_docs` | `python` | fix(guard): make git-fresh-base fetch timeout-portable; release 2.33.0 |
| https://github.com/CryptoJones/omind/pull/82 | `CryptoJones/omind` | `code_and_docs` | `python` | feat(agents): prime OMI at session start for Hermes Agent and OpenClaw |
| https://github.com/CryptoJones/omind/pull/80 | `CryptoJones/omind` | `code_only` | `python` | fix(store): preserve non-template ## sections through the edit path |
| https://github.com/CryptoJones/omind/pull/78 | `CryptoJones/omind` | `code_only_tests_or_fixtures` | `python` | fix(test): make guard-hook executable-bit assertion POSIX-only |
| https://github.com/CryptoJones/omind/pull/77 | `CryptoJones/omind` | `code_and_docs` | `python` | feat(provision): install fresh-base git guard hook via omind setup |
| https://github.com/CryptoJones/omind/pull/72 | `CryptoJones/omind` | `code_and_docs` | `python` | Baseline adoption: green up gates + conformance + CI hardening |
| https://github.com/CryptoJones/omind/pull/71 | `CryptoJones/omind` | `code_and_docs` | `python` | chore(release): 2.31.0 |
| https://github.com/CryptoJones/omind/pull/70 | `CryptoJones/omind` | `code_and_docs` | `python` | docs: align documentation with the 2.30.0 state of the code |
| https://github.com/CryptoJones/omind/pull/69 | `CryptoJones/omind` | `code_and_docs` | `python` | feat(e2e): real-world mesh testing on disposable VMs (RunPod + podman) |
| https://github.com/CryptoJones/omind/pull/67 | `CryptoJones/omind` | `code_and_docs` | `python` | Code review sweep: 16 bug fixes + 14 cleanups, releases 2.1.0–2.29.0 |
| https://github.com/CryptoJones/omind/pull/66 | `CryptoJones/omind` | `code_only` | `python` | test(cli): compare __version__ to pyproject, not a hardcoded string |
| https://github.com/CryptoJones/omind/pull/65 | `CryptoJones/omind` | `code_only` | `python` | fix(release): bump __version__ to 2.0.1 |
| https://github.com/CryptoJones/omind/pull/64 | `CryptoJones/omind` | `code_and_docs` | `python` | feat(mesh): add-seed — provision a passive bare seed repo as a peer |
| https://github.com/CryptoJones/omind/pull/62 | `CryptoJones/omind` | `code_only` | `python` | fix(mesh): resolve peer URLs via remote get-url, not remote -v parsing |
| https://github.com/CryptoJones/omind/pull/60 | `CryptoJones/omind` | `code_and_docs` | `python` | chore(release): 2.0.0 — the memory mesh |
| https://github.com/CryptoJones/omind/pull/59 | `CryptoJones/omind` | `code_and_docs` | `python` | feat(setup): wire setup/doctor/agents to the mesh; retire obsidian-mcp |
| https://github.com/CryptoJones/omind/pull/58 | `CryptoJones/omind` | `code_only` | `python` | feat(mesh): replication daemon + user-service install |
| https://github.com/CryptoJones/omind/pull/57 | `CryptoJones/omind` | `code_only` | `python` | feat(mesh): replication — sync, peers, clone, purge; privacy hardening |
| https://github.com/CryptoJones/omind/pull/56 | `CryptoJones/omind` | `code_only` | `python` | feat(merge): field-level 3-way note merge — the mesh merge driver |
| https://github.com/CryptoJones/omind/pull/55 | `CryptoJones/omind` | `code_only` | `python` | feat(mesh): node identity, git wrapper, and mesh init |
| https://github.com/CryptoJones/omind/pull/54 | `CryptoJones/omind` | `code_only_tests_or_fixtures` | `python` | test(node): deracify the stdio smoke test — await replies before EOF |
| https://github.com/CryptoJones/omind/pull/53 | `CryptoJones/omind` | `code_only` | `python` | feat(node): omind node — the local mesh-node MCP server |
| https://github.com/CryptoJones/omind/pull/52 | `CryptoJones/omind` | `code_only` | `python` | feat(web): archive support — hide, badge, restore soft-deleted notes |
| https://github.com/CryptoJones/omind/pull/51 | `CryptoJones/omind` | `code_and_docs` | `python` | feat(store): per-note Lamport revisions and soft-delete for the mesh |
| https://github.com/CryptoJones/omind/pull/50 | `CryptoJones/omind` | `code_and_docs` | `python` | fix: eof-guard watchdog for silent transport detach; manage guard updates |
| https://github.com/CryptoJones/omind/pull/47 | `CryptoJones/omind` | `code_only_tests_or_fixtures` | `python` | test: isolate XDG_STATE_HOME suite-wide via conftest |
| https://github.com/CryptoJones/omind/pull/46 | `CryptoJones/omind` | `code_and_docs` | `python` | chore(release): 1.3.0 — subprocess timeouts, Windows CI + fixes, hook observability |
| https://github.com/CryptoJones/omind/pull/45 | `CryptoJones/omind` | `code_only_tests_or_fixtures` | `python` | test: make CLI integration tests Windows-clean |
| https://github.com/CryptoJones/omind/pull/43 | `CryptoJones/omind` | `code_only` | `python` | refactor(paths): centralize canonical filenames in one module |
| https://github.com/CryptoJones/omind/pull/41 | `CryptoJones/omind` | `code_only_tests_or_fixtures` | `python` | test(cli): integration coverage for the subcommand wiring |
| https://github.com/CryptoJones/omind/pull/42 | `CryptoJones/omind` | `code_and_docs` | `python` | fix(hooks): breadcrumb swallowed errors; surface them in doctor |
| https://github.com/CryptoJones/omind/pull/39 | `CryptoJones/omind` | `code_and_docs` | `python` | fix(proc): shared subprocess runner with timeouts |
| https://github.com/CryptoJones/omind/pull/40 | `CryptoJones/omind` | `code_and_docs` | `python` | ci: test on windows-latest and Python 3.13/3.14 |
| https://github.com/CryptoJones/omind/pull/38 | `CryptoJones/omind` | `code_and_docs` | `python` | chore(release): 1.2.0 |
| https://github.com/CryptoJones/omind/pull/37 | `CryptoJones/omind` | `code_and_docs` | `python` | fix(store): render index descriptions from note summaries, cap Recent Memories |
| https://github.com/CryptoJones/omind/pull/36 | `CryptoJones/omind` | `code_and_docs` | `python` | feat(hooks): prime latest Session State note and journal tail at SessionStart |
| https://github.com/CryptoJones/omind/pull/34 | `CryptoJones/omind` | `code_and_docs` | `python` | fix(hooks): keep daily journals in Journal/, out of the index; add rollup |
| https://github.com/CryptoJones/omind/pull/33 | `CryptoJones/omind` | `code_and_docs` | `python` | fix(hooks): stop treating stderr presence as tool failure |
| https://github.com/CryptoJones/omind/pull/32 | `CryptoJones/omind` | `code_and_docs` | `python` | feat(agents): provision Hermes Agent and OpenClaw alongside Claude Code |
| https://github.com/CryptoJones/omind/pull/30 | `CryptoJones/omind` | `code_and_docs` | `python` | docs: generalize headline description from Claude Code to AI agents |
| https://github.com/CryptoJones/omind/pull/28 | `CryptoJones/omind` | `code_only` | `python` | fix(provision): honor CLAUDE_CONFIG_DIR when resolving Claude config paths |
| https://github.com/CryptoJones/omind/pull/26 | `CryptoJones/omind` | `code_and_docs` | `python` | feat: `omind quickstart` — print manual-wiring steps for hooks and MCP |
| https://github.com/CryptoJones/omind/pull/18 | `CryptoJones/omind` | `code_only` | `python` | Add a pip-audit dependency CVE scan to CI |
| https://github.com/CryptoJones/omind/pull/16 | `CryptoJones/omind` | `code_and_docs` | `python` | chore: trim dead code and run mypy in CI |
| https://github.com/CryptoJones/omind/pull/14 | `CryptoJones/omind` | `code_and_docs` | `python` | fix: stop obsidian-mcp orphaning when Claude Code exits (v1.1.0) |
| https://github.com/CryptoJones/omind/pull/12 | `CryptoJones/omind` | `code_and_docs` | `python` | v1.0.0: offline UI, conflict guard, backlinks, shortcuts, doctor |
| https://github.com/CryptoJones/omind/pull/10 | `CryptoJones/omind` | `code_and_docs` | `python` | i18n: switchable UI in six languages with RTL support |
| https://github.com/CryptoJones/omind/pull/6 | `CryptoJones/omind` | `code_and_docs` | `python` | feat(web): redesign UI + theme switcher (v0.2.0) |
| https://github.com/CryptoJones/omind/pull/2 | `CryptoJones/omind` | `code_only` | `python` | feat: omind setup (MCP provisioning) + serve (web UI) |
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
| https://github.com/d-hinders/Haven-AI/pull/2001 | `d-hinders/Haven-AI` | `code_only` | `typescript` | fix(frontend): measure the allowance countdown from chain time, not the device clock (#1995) |
| https://github.com/d-hinders/Haven-AI/pull/2000 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | feat(safe-retirement): close the inflow — 410 on Safe deploy/import, Hybrid-only onboarding (#1984) |
| https://github.com/d-hinders/Haven-AI/pull/1996 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | test(frontend): capture UnmanagedDelegateCard, and re-derive the three surfaces that stay unreachable (#1930) |
| https://github.com/d-hinders/Haven-AI/pull/1997 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(frontend): reveal the showcase's transaction columns in two stages, not one (#1827) |
| https://github.com/d-hinders/Haven-AI/pull/1983 | `d-hinders/Haven-AI` | `code_only` | `typescript` | test(frontend): make WalletPopover's presentational prop self-enforcing (#1975) |
| https://github.com/d-hinders/Haven-AI/pull/1977 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | feat(catalog): verified discovery + agent-side submission in SDK and MCP (#1716) |
| https://github.com/d-hinders/Haven-AI/pull/1976 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | feat(catalog): verified-directory listing badges + public submission status + self-service dashboard flow (#1715) |
| https://github.com/d-hinders/Haven-AI/pull/1979 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(frontend): every chain Haven offers has a wagmi transport, and a capture that never asked for its data is fatal (#1971) |
| https://github.com/d-hinders/Haven-AI/pull/1978 | `d-hinders/Haven-AI` | `code_only` | `typescript` | fix(catalog): refuse IP-literal hostnames at CLAIM level, so both ownership paths agree (#1959) |
| https://github.com/d-hinders/Haven-AI/pull/1973 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(frontend): name the passkeys[0] signing fallback instead of hiding it (#1952) |
| https://github.com/d-hinders/Haven-AI/pull/1814 | `d-hinders/Haven-AI` | `code_only` | `typescript` | feat: surface the settlement scheme (eip3009\|erc7710) in the x402 transaction feed and detail (#1706, #1707) |
| https://github.com/d-hinders/Haven-AI/pull/1837 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | feat(catalog): public self-service submission queue — POST /catalog/submit (#1711) |
| https://github.com/d-hinders/Haven-AI/pull/1967 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(frontend): hide the landing page's decorative arrows and give the investor-briefing header CTA a 44px tap target (#1954, #1955) |
| https://github.com/d-hinders/Haven-AI/pull/1966 | `d-hinders/Haven-AI` | `code_only` | `typescript` | feat(catalog): SSRF-hardened verification probe + catalogIngest leader lock (#1713) |
| https://github.com/d-hinders/Haven-AI/pull/1964 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | Fix re-key authority copy before production promotion |
| https://github.com/d-hinders/Haven-AI/pull/1962 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | chore(release): bump all published packages to 0.1.30-alpha.0 |
| https://github.com/d-hinders/Haven-AI/pull/1960 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(frontend): move the contacts dialog's actions into ui/Modal's footer (#1946) |
| https://github.com/d-hinders/Haven-AI/pull/1958 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | feat(catalog): domain-ownership proof — HMAC-bound expiring token + shared SSRF guard (#1712) |
| https://github.com/d-hinders/Haven-AI/pull/1957 | `d-hinders/Haven-AI` | `code_only` | `typescript` | fix(frontend): hide the decorative marketing CTA arrows from the accessibility tree (#1940) |
| https://github.com/d-hinders/Haven-AI/pull/1953 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(screenshot): say why a capture produced nothing (#1936, #1939, #1943) |
| https://github.com/d-hinders/Haven-AI/pull/1951 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | refactor(frontend): one device-marker passkey selector, shared by both signing paths (#1933) |
| https://github.com/d-hinders/Haven-AI/pull/1949 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(frontend): give ui/Modal's scrolling body a continuation cue (#1893) |
| https://github.com/d-hinders/Haven-AI/pull/1948 | `d-hinders/Haven-AI` | `code_only` | `typescript` | feat(frontend): catalogue ApprovalRequiredBanner's full tone ladder on /design-system (#1880) |
| https://github.com/d-hinders/Haven-AI/pull/1942 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(frontend): drop the wallet label below sm so TopBar fits a 320px phone (#1803) |
| https://github.com/d-hinders/Haven-AI/pull/1941 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | test(frontend): capture the Backup & recovery card's one-way and loadError states (#1725) |
| https://github.com/d-hinders/Haven-AI/pull/1938 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(frontend): absorb the White-on-brand CTA pattern into a primitive and guard its focus ring (#1867) |
| https://github.com/d-hinders/Haven-AI/pull/1934 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(design-system): converge the two remove-budget controls on the 14 px icon rung (#1923) |
| https://github.com/d-hinders/Haven-AI/pull/1931 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | test(frontend): render AgentPanel empty states and AgentCard warning banners (#1924) |
| https://github.com/d-hinders/Haven-AI/pull/1926 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | feat(agents): report and show which MCP pair an agent is wired as (#1878) |
| https://github.com/d-hinders/Haven-AI/pull/1929 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(connect): --doctor sees a directory holding only rekey-pending.json (#1915) |
| https://github.com/d-hinders/Haven-AI/pull/1925 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(design-system): resolve § 5's false icon-size claim — add 12/24/28 to the scale, convert the 11 outliers, and gate it (#1858) |
| https://github.com/d-hinders/Haven-AI/pull/1922 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(frontend): keep the previous screenshot run addressable instead of rm -rf'ing it (#1888) |
| https://github.com/d-hinders/Haven-AI/pull/1921 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(rekey): plan the budget carry on the metering clock, not the issue clock (#1849) |
| https://github.com/d-hinders/Haven-AI/pull/1920 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(connect): --repair writes the named MCP pair; --doctor reports a parked re-key (#1910, #1911) |
| https://github.com/d-hinders/Haven-AI/pull/1919 | `d-hinders/Haven-AI` | `code_only` | `typescript` | ci: name the ci_config_checks glob step for what it runs (#1874) |
| https://github.com/d-hinders/Haven-AI/pull/1918 | `d-hinders/Haven-AI` | `code_only` | `typescript` | fix(agents): AgentCard action-row focus-ring clearance, and stop 'Restore to list' wrapping on Linux (#1909) |
| https://github.com/d-hinders/Haven-AI/pull/1913 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | chore(ci): close the general fifth-copy detector with a measurement, not a threshold (#1904) |
| https://github.com/d-hinders/Haven-AI/pull/1912 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | feat(connect): --rekey replaces an agent's signing key in place (#1700) |
| https://github.com/d-hinders/Haven-AI/pull/1908 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | test(frontend): render the four AgentCard states the fixture never served — #1831's eleven focus indicators, all eleven (#1873) |
| https://github.com/d-hinders/Haven-AI/pull/1907 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | feat(passport): re-anchor on re-key, with standing unbroken (#1699) |
| https://github.com/d-hinders/Haven-AI/pull/1906 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(ci): retire the dead machine-payments glob and pin the fourth copy of the money-path list (#1897, #1899) |
| https://github.com/d-hinders/Haven-AI/pull/1902 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(frontend): the re-key sends its signing scheme, and the type stops lying (#1890) |
| https://github.com/d-hinders/Haven-AI/pull/1900 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(ci): the money-path perimeter learns about re-key, and its copies agree in both directions (#1892) |
| https://github.com/d-hinders/Haven-AI/pull/1895 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | test(frontend): a durable, mutation-proven CI gate for the clip guard (#1886) |
| https://github.com/d-hinders/Haven-AI/pull/1894 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(frontend): the re-key point-of-no-return button moves below its own gate (#1887) |
| https://github.com/d-hinders/Haven-AI/pull/1891 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(backend): the re-key revoke tells the account which signer will sign (#1870) |
| https://github.com/d-hinders/Haven-AI/pull/1881 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | feat(frontend): the dashboard can replace an agent's signing key (#1701) |
| https://github.com/d-hinders/Haven-AI/pull/1875 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | test(frontend): drive keyboard focus onto #1831's eleven indicators and capture them (#1863) |
| https://github.com/d-hinders/Haven-AI/pull/1872 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(ci): make the baseline-push deadlock visible on the PR, and name the runs to approve (#1777) |
| https://github.com/d-hinders/Haven-AI/pull/1865 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(frontend): convert the ten gated raw arrows to lucide icons (#1857) |
| https://github.com/d-hinders/Haven-AI/pull/1860 | `d-hinders/Haven-AI` | `code_only` | `typescript` | fix(frontend): scope the compact row's fixed height to the breakpoint it was measured for (#1833) |
| https://github.com/d-hinders/Haven-AI/pull/1864 | `d-hinders/Haven-AI` | `code_only_tests_or_fixtures` | `typescript` | test(frontend): capture SendModal's review step — the last unphotographed TransactionMovement consumer (#1856) |
| https://github.com/d-hinders/Haven-AI/pull/1861 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | test(frontend): scope-capture the app shell sidebar in the visual gate (#1820) |
| https://github.com/d-hinders/Haven-AI/pull/1859 | `d-hinders/Haven-AI` | `code_only` | `typescript` | fix(frontend): ConfiguredAllowanceRow renders no meter — it has nothing to measure (#1846) |
| https://github.com/d-hinders/Haven-AI/pull/1835 | `d-hinders/Haven-AI` | `code_only` | `typescript` | fix(frontend): stop the mobile transaction row stranding its arrow and collapsing its title (#1774, #1750) |
| https://github.com/d-hinders/Haven-AI/pull/1855 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(frontend): stop ReceiveFundsModal throwing on an unresolved chain, and hedge the network it names (#1852) |
| https://github.com/d-hinders/Haven-AI/pull/1853 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(frontend): stop defaulting an unresolved chain to Base mainnet in Add funds (#1844) |
| https://github.com/d-hinders/Haven-AI/pull/1845 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(frontend): sweep the last 9 dead colour utilities and make the gate absolute (#1710) |
| https://github.com/d-hinders/Haven-AI/pull/1851 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | feat(docs): fail a PR that drops an entry from a doc's last-verified chain (#1843) |
| https://github.com/d-hinders/Haven-AI/pull/1841 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | test(frontend): run the dialog overflow guard at a mobile viewport (#1797) |
| https://github.com/d-hinders/Haven-AI/pull/1832 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(frontend): give the e2e run a per-worktree port and a server it can identify (#1816) |
| https://github.com/d-hinders/Haven-AI/pull/1836 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(frontend): make TopBar's background actually compile, and guard the pattern rather than the instance (#1818) |
| https://github.com/d-hinders/Haven-AI/pull/1831 | `d-hinders/Haven-AI` | `code_only` | `typescript` | fix(frontend): destructive controls get a focus indicator at all (#1819) |
| https://github.com/d-hinders/Haven-AI/pull/1829 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(frontend): destructive controls focus in their own tone, solid fills included (#1817, #1809) |
| https://github.com/d-hinders/Haven-AI/pull/1811 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(frontend): give the visual gate a budget it cannot outgrow, and baselines it can actually refresh (#1805, #1760) |
| https://github.com/d-hinders/Haven-AI/pull/1821 | `d-hinders/Haven-AI` | `code_only` | `typescript` | fix(frontend): destructive icon buttons focus in their own tone (#1792) |
| https://github.com/d-hinders/Haven-AI/pull/1822 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(frontend): a per-worktree capture port, and a server that has to prove it is ours (#1800) |
| https://github.com/d-hinders/Haven-AI/pull/1812 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | feat(connect): remove the runtime picker — one setup command for every environment (#1720) |
| https://github.com/d-hinders/Haven-AI/pull/1808 | `d-hinders/Haven-AI` | `code_only_tests_or_fixtures` | `typescript` | fix(backend): derive the ops-probe subprocess budget and make its timeout legible |
| https://github.com/d-hinders/Haven-AI/pull/1804 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(frontend): make TopBar's reserved hamburger slot survive a phone (#1767) |
| https://github.com/d-hinders/Haven-AI/pull/1799 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | test(frontend): measure horizontal overflow inside fixed-position overlays (#1773) |
| https://github.com/d-hinders/Haven-AI/pull/1798 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(frontend): one focus-ring treatment that clears WCAG 3:1 (#1741, #1746) |
| https://github.com/d-hinders/Haven-AI/pull/1786 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(backend): converge revocation_status when a revoke mines after its wait expires (#1758) |
| https://github.com/d-hinders/Haven-AI/pull/1783 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | chore(release): bump all published packages to 0.1.29-alpha.0 |
| https://github.com/d-hinders/Haven-AI/pull/1782 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(backend): a no-database test run fails, and says what it skipped after the summary (#1763) |
| https://github.com/d-hinders/Haven-AI/pull/1781 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | test(frontend): anchor the mobile-shell guards against the viewport (#1779) |
| https://github.com/d-hinders/Haven-AI/pull/1780 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | feat(connect): resolve the runtime itself — agent self-report, installed-client prompt, real failure vocabulary (#1719) |
| https://github.com/d-hinders/Haven-AI/pull/1778 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(frontend): give the mobile sidebar toggle a 44px tap target without moving a pixel (#1766) |
| https://github.com/d-hinders/Haven-AI/pull/1775 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(frontend): stop /transactions clipping 106px of its table on mobile (#1772) |
| https://github.com/d-hinders/Haven-AI/pull/1776 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | test(frontend): make the horizontal-overflow guard able to fail inside the app shell (#1771) |
| https://github.com/d-hinders/Haven-AI/pull/1770 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | ci(frontend): gate every PR on a real mobile viewport (#1768) |
| https://github.com/d-hinders/Haven-AI/pull/1769 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(frontend): make the mobile navigation toggle reachable, on a named z-index scale (#1749) |
| https://github.com/d-hinders/Haven-AI/pull/1765 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(passport): a re-mint requires positive evidence the prior attest is dead (#1745) |
| https://github.com/d-hinders/Haven-AI/pull/1764 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(sdk): bound the delegate sweep's confirmation waits and report an expiry instead of hanging the caller (#1756) |
| https://github.com/d-hinders/Haven-AI/pull/1759 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(passport): bound the revoke's confirmation wait, hand expiry to the bump worker, and sweep the repo for the same defect (#1742) |
| https://github.com/d-hinders/Haven-AI/pull/1748 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(frontend): capture the whole page for rendered evidence, and prove it is not blank (#1738) |
| https://github.com/d-hinders/Haven-AI/pull/1752 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | feat(connect): per-agent doctor inventory and a hosted-vs-local identity check (#1697) |
| https://github.com/d-hinders/Haven-AI/pull/1751 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(passport): a wait timeout leaves the anchor reconcilable instead of failed (#1735) |
| https://github.com/d-hinders/Haven-AI/pull/1740 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(ui): give Button sm/md a 44px tap target without moving any pixels |
| https://github.com/d-hinders/Haven-AI/pull/1737 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(rails): bound the hybrid deploy's confirmation wait and hand expiry to the bump worker (#1722) |
| https://github.com/d-hinders/Haven-AI/pull/1734 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | feat(api): add settlementScheme to the transaction wire contract (#1705) |
| https://github.com/d-hinders/Haven-AI/pull/1732 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | feat(connect): --name wiring slug end to end (#1696) |
| https://github.com/d-hinders/Haven-AI/pull/1733 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(connect): visible step connectors, one gate name, and a promoted restart (#1684) |
| https://github.com/d-hinders/Haven-AI/pull/1727 | `d-hinders/Haven-AI` | `code_only_tests_or_fixtures` | `typescript` | test(screenshot): capture the Backup &amp; recovery card unobstructed (#1693) |
| https://github.com/d-hinders/Haven-AI/pull/1730 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | feat(connect): named MCP server pairs in every runtime config writer (#1695) |
| https://github.com/d-hinders/Haven-AI/pull/1729 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | feat(connect): tombstone retired agent directories and restart-every-host guidance (#1681) |
| https://github.com/d-hinders/Haven-AI/pull/1728 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | feat(connect): a superseded agent with a live key fails the doctor, and setup names it (#1688) |
| https://github.com/d-hinders/Haven-AI/pull/1724 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | feat(signer): refuse to sign another agent's quote — payer identity in the x402 expected context (#1690) |
| https://github.com/d-hinders/Haven-AI/pull/1723 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | docs(scaling): record the accepted cost of the deploy lock's pooled connection (#1686) |
| https://github.com/d-hinders/Haven-AI/pull/1718 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(catalog): label the stranded-funds test fixture so agents know it will not settle (#1669) |
| https://github.com/d-hinders/Haven-AI/pull/1692 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | Passkey terminology: "Passkey · added {date}" replaces "Face ID / Touch ID" credential names (#1679) |
| https://github.com/d-hinders/Haven-AI/pull/1703 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | test(qa): cover the fresh agent whose first-ever payment is erc7710 (#1674) |
| https://github.com/d-hinders/Haven-AI/pull/1691 | `d-hinders/Haven-AI` | `code_only_tests_or_fixtures` | `typescript` | test(rate-limit): prove the plugin → store → Postgres wiring end to end (#1680) |
| https://github.com/d-hinders/Haven-AI/pull/1689 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | feat(connect): name-first runtime picker — pick your app by name; modality is the row's property (#1682) |
| https://github.com/d-hinders/Haven-AI/pull/1687 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(hybrid): serialize concurrent deploys of the same counterfactual account (#1673) |
| https://github.com/d-hinders/Haven-AI/pull/1683 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | feat(rate-limit): share the counters across replicas (#1680) |
| https://github.com/d-hinders/Haven-AI/pull/1677 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | feat(connect): detection-first runtime resolution — the setup command drops --runtime (#1672) |
| https://github.com/d-hinders/Haven-AI/pull/1678 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(config): make the trust-proxy state observable, and its parsing refuse to guess (#1670) |
| https://github.com/d-hinders/Haven-AI/pull/1676 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | feat(auth): per-client rate limits on signup/login, armed by a trusted proxy (#1670) |
| https://github.com/d-hinders/Haven-AI/pull/1675 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(x402): deploy the counterfactual delegate account on erc7710 authorize (#1667) |
| https://github.com/d-hinders/Haven-AI/pull/1671 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | docs(auth): accept the signup enumeration disclosure, with the reasoning written down (#1654) |
| https://github.com/d-hinders/Haven-AI/pull/1668 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(release): make the lockfile bump deterministic and guarded (#1663) |
| https://github.com/d-hinders/Haven-AI/pull/1662 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | chore(release): bump all published packages to 0.1.28-alpha.0 |
| https://github.com/d-hinders/Haven-AI/pull/1661 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | tooling: measure branch hygiene instead of hoping for it (#1500) |
| https://github.com/d-hinders/Haven-AI/pull/1660 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | refactor(sdk): reduce HavenClient to a compatibility facade (#1620) |
| https://github.com/d-hinders/Haven-AI/pull/1659 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | refactor(sdk): extract the erc7710 no-funding-leg lifecycle (#1619) |
| https://github.com/d-hinders/Haven-AI/pull/1658 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | refactor(sdk): extract the EIP-3009 x402 funding-leg lifecycle (#1618) |
| https://github.com/d-hinders/Haven-AI/pull/1657 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(x402): format receipt amount_human with the token's own decimals (#1630) |
| https://github.com/d-hinders/Haven-AI/pull/1656 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(auth): equalise login cost so latency cannot enumerate accounts (#1646) |
| https://github.com/d-hinders/Haven-AI/pull/1655 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | refactor(sdk): extract account reads and delegate sweeps |
| https://github.com/d-hinders/Haven-AI/pull/1653 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | fix(auth): a purpose-scoped token is not a session credential (#1640) |
| https://github.com/d-hinders/Haven-AI/pull/1649 | `d-hinders/Haven-AI` | `code_only` | `typescript` | refactor(ci): derive job fan-out from one package dependency table (#1625) |
| https://github.com/d-hinders/Haven-AI/pull/1650 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | docs(api): document the ten individually-excluded routes — the spec backfill is complete (#1446 slice 13) |
| https://github.com/d-hinders/Haven-AI/pull/1648 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | docs(api): document the activity feed and onboarding funnel in the OpenAPI spec (#1446 slice 12) |
| https://github.com/d-hinders/Haven-AI/pull/1647 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | docs(api): document the session and passkey surface in the OpenAPI spec (#1446 slice 11) |
| https://github.com/d-hinders/Haven-AI/pull/1644 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | docs(api): document the approval queue in the OpenAPI spec (#1446 slice 10) |
| https://github.com/d-hinders/Haven-AI/pull/1645 | `d-hinders/Haven-AI` | `code_only` | `typescript` | refactor(ci): declarative root-guard ownership manifest (#1624) |
| https://github.com/d-hinders/Haven-AI/pull/1643 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | docs(api): document the Hybrid DeleGator account surface in the OpenAPI spec (#1446 slice 9) |
| https://github.com/d-hinders/Haven-AI/pull/1641 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | docs(api): document the Fortnox OAuth surface in the OpenAPI spec (#1446 slice 8) |
| https://github.com/d-hinders/Haven-AI/pull/1639 | `d-hinders/Haven-AI` | `code_only` | `typescript` | refactor(ci): extract the change classifier into a dependency-free tested script (#1622) |
| https://github.com/d-hinders/Haven-AI/pull/1637 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | docs(api): document the bookkeeping export + reporting feed in the OpenAPI spec (#1446 slice 7) |
| https://github.com/d-hinders/Haven-AI/pull/1636 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | refactor(sdk): extract paid MCP merchant transport |
| https://github.com/d-hinders/Haven-AI/pull/1635 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | docs(api): document the dashboard account + owner directory in the OpenAPI spec (#1446 slice 6) |
| https://github.com/d-hinders/Haven-AI/pull/1634 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | refactor(sdk): extract Haven API transport and payment mapping |
| https://github.com/d-hinders/Haven-AI/pull/1633 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | docs(api): document the Safe-management surface in the OpenAPI spec (#1446 slice 5) |
| https://github.com/d-hinders/Haven-AI/pull/1632 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | docs(api): document the Agent Passport surface in the OpenAPI spec (#1446 slice 4) |
| https://github.com/d-hinders/Haven-AI/pull/1629 | `d-hinders/Haven-AI` | `code_only` | `typescript` | docs(api): document the x402 demo-resource surface in the OpenAPI spec (#1446 slice 3) |
| https://github.com/d-hinders/Haven-AI/pull/1631 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | SDK: Characterize HavenClient boundaries and growth |
| https://github.com/d-hinders/Haven-AI/pull/1628 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | docs(api): document the delegation lifecycle API in the OpenAPI spec (#1446 slice 2) |
| https://github.com/d-hinders/Haven-AI/pull/1610 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | chore(release): bump all published packages to 0.1.27-alpha.0 |
| https://github.com/d-hinders/Haven-AI/pull/1611 | `d-hinders/Haven-AI` | `code_only` | `typescript` | ci: gate Playwright install on browser-cache hit — apt-get leaves the warm-cache path (#1609) |
| https://github.com/d-hinders/Haven-AI/pull/1606 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | docs(code): correct four stale 'until #N' comments that claim to wait for shipped work (#1605) |
| https://github.com/d-hinders/Haven-AI/pull/1608 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | docs: ship-next corrections — CI-waiting claims, outbound money-path coverage, flake triage, sdk playbook refresh (#1607) |
| https://github.com/d-hinders/Haven-AI/pull/1601 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | connect: harden the LOCAL MCP runtime install like #1586 did the signer's (#1593) |
| https://github.com/d-hinders/Haven-AI/pull/1600 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | backend: normalize catalog price_display — drop the redundant $ prefix (#1592) |
| https://github.com/d-hinders/Haven-AI/pull/1599 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | mcp: slim tool descriptions — shared guidance into server instructions (#1591) |
| https://github.com/d-hinders/Haven-AI/pull/1598 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | feat(sdk,mcp): spend_authority_readiness — name the signal for what it covers (#1590) |
| https://github.com/d-hinders/Haven-AI/pull/1597 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | feat(connect): --doctor and --repair — one-command setup diagnosis (#1589) |
| https://github.com/d-hinders/Haven-AI/pull/1596 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | feat(mcp): runtime-neutral next_tool — next_tool_server + next_tool_name (#1588) |
| https://github.com/d-hinders/Haven-AI/pull/1595 | `d-hinders/Haven-AI` | `code_and_docs` | `typescript` | feat(connect): handshake-probe the local signer before reporting success (#1587) |
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
| https://github.com/microsoft/autogen/pull/1826 | `microsoft/autogen` | `code_and_docs` | `python` | StateFlow Blog |
| https://github.com/microsoft/autogen/pull/1739 | `microsoft/autogen` | `code_only` | `python` | fix some docstring issues affecting rendering |
| https://github.com/microsoft/autogen/pull/3357 | `microsoft/autogen` | `code_only` | `python` | Missing backticks breaking documentation in groupchat.last_speaker |
| https://github.com/microsoft/autogen/pull/2091 | `microsoft/autogen` | `code_only` | `python` | Pin databind version to fix pydoc-markdown failure in CI |
| https://github.com/microsoft/autogen/pull/1809 | `microsoft/autogen` | `code_only` | `python` | Add documentation for jupyter code executor |
| https://github.com/microsoft/autogen/pull/1982 | `microsoft/autogen` | `code_and_docs` | `python` | AutoDefense Blog |
| https://github.com/microsoft/autogen/pull/3356 | `microsoft/autogen` | `code_only` | `python` | Update Mistral client class to support new Mistral v1.0.1 package |
| https://github.com/microsoft/autogen/pull/2229 | `microsoft/autogen` | `code_only` | `python` | Replace unofficial with official pre-commit hook for ruff |
| https://github.com/microsoft/autogen/pull/2600 | `microsoft/autogen` | `code_only` | `python` | fix: event logging with nested chats |
| https://github.com/microsoft/autogen/pull/2078 | `microsoft/autogen` | `code_only` | `python` | Update GitHub actions |
| https://github.com/microsoft/autogen/pull/1842 | `microsoft/autogen` | `code_only` | `python` | add doc about effects for capabilities |
| https://github.com/microsoft/autogen/pull/2438 | `microsoft/autogen` | `code_only` | `python` | conversable agent: actually print the response in the warning |
| https://github.com/microsoft/autogen/pull/1786 | `microsoft/autogen` | `code_only` | `python` | Support functions removing  in ConversableAgent |
| https://github.com/microsoft/autogen/pull/1291 | `microsoft/autogen` | `code_and_docs` | `python` | More documentation for Cache. Updated FAQ to include database Locked error  |
| https://github.com/microsoft/autogen/pull/1938 | `microsoft/autogen` | `code_only` | `python` | Fix a initiate chats |
| https://github.com/microsoft/autogen/pull/915 | `microsoft/autogen` | `code_and_docs` | `python` | Add collate file and more tests from autogpt into testbed |
| https://github.com/microsoft/autogen/pull/1241 | `microsoft/autogen` | `code_only` | `python` | Add dev container for AutoGen Studio |
| https://github.com/microsoft/autogen/pull/1333 | `microsoft/autogen` | `code_and_docs` | `python` | Cleanup and unify Dockerfiles  |
| https://github.com/microsoft/autogen/pull/1366 | `microsoft/autogen` | `code_only` | `python` | fix website production css |
| https://github.com/microsoft/autogen/pull/2815 | `microsoft/autogen` | `code_and_docs` | `python` | [.Net] Release note for 0.0.14 |
| https://github.com/microsoft/autogen/pull/141 | `microsoft/autogen` | `code_only` | `python` | bump version to 0.1.7 |
| https://github.com/microsoft/autogen/pull/1724 | `microsoft/autogen` | `code_and_docs` | `python` |  Async version of multiple sequential chat |
| https://github.com/microsoft/autogen/pull/1903 | `microsoft/autogen` | `code_only` | `python` | Compressible Agent require `model` field for `llm_config` |
| https://github.com/microsoft/autogen/pull/1082 | `microsoft/autogen` | `code_only` | `python` | [Core] Throw an error when the OAI_CONFIG_LIST is missing. |
| https://github.com/microsoft/autogen/pull/2102 | `microsoft/autogen` | `code_only` | `python` | Implement User Defined Functions for Local CLI Executor |
| https://github.com/microsoft/autogen/pull/1140 | `microsoft/autogen` | `code_only` | `python` | bump version to 0.2.3 |
| https://github.com/microsoft/autogen/pull/1856 | `microsoft/autogen` | `code_only` | `python` | Implement docker based command line code executor |
| https://github.com/microsoft/autogen/pull/2271 | `microsoft/autogen` | `code_only` | `python` | Add html parser for RAG and some improvements |
| https://github.com/microsoft/autogen/pull/1836 | `microsoft/autogen` | `code_and_docs` | `python` | Upgrade Quarto and use notebook metadata for frontmatter  |
| https://github.com/microsoft/autogen/pull/1279 | `microsoft/autogen` | `code_only` | `python` | removed alpine image |
| https://github.com/microsoft/autogen/pull/951 | `microsoft/autogen` | `code_only` | `python` | Refined the user_proxy description. |
| https://github.com/microsoft/autogen/pull/1501 | `microsoft/autogen` | `code_and_docs` | `python` | Introducing AutoAnny: A New Discord Bot Built with AutoGen |
| https://github.com/microsoft/autogen/pull/1909 | `microsoft/autogen` | `code_only` | `python` | Accept path for work_dir in LocalCommandLineCodeExecutor |
| https://github.com/microsoft/autogen/pull/2082 | `microsoft/autogen` | `code_only` | `python` | Print slow tests in CI |
| https://github.com/microsoft/autogen/pull/2005 | `microsoft/autogen` | `code_only` | `python` | refactor: [conversable_agent] remove list of func pointers |
| https://github.com/microsoft/autogen/pull/455 | `microsoft/autogen` | `code_and_docs` | `python` | Added a simple Testbed tool for repeatedly running templated Autogen scenarios with tightly-controlled initial conditions. |
| https://github.com/microsoft/autogen/pull/1014 | `microsoft/autogen` | `code_only` | `python` | Fix exception causes all over the codebase #1007 |
| https://github.com/microsoft/autogen/pull/1901 | `microsoft/autogen` | `code_only` | `python` | Fix threading issue for logging |
| https://github.com/microsoft/autogen/pull/1485 | `microsoft/autogen` | `code_only` | `python` | Bump autogenbench version. |
| https://github.com/microsoft/autogen/pull/1448 | `microsoft/autogen` | `code_and_docs` | `python` | docs: initial Jupyter support for website docs, move config notebook |
| https://github.com/microsoft/autogen/pull/333 | `microsoft/autogen` | `code_only` | `python` | bump version to 0.1.13 |
| https://github.com/microsoft/autogen/pull/1627 | `microsoft/autogen` | `code_only` | `python` | Command line code sanitation |
| https://github.com/microsoft/autogen/pull/7463 | `microsoft/autogen` | `code_and_docs` | `python` | fix: restrict importlib provider loading to trusted namespaces |
| https://github.com/microsoft/autogen/pull/1692 | `microsoft/autogen` | `code_and_docs` | `python` | Update Azure OpenAI API version to 2024-02-15-preview |
| https://github.com/microsoft/autogen/pull/85 | `microsoft/autogen` | `code_only` | `python` | bump version to 0.1.6 |
| https://github.com/microsoft/autogen/pull/1495 | `microsoft/autogen` | `code_and_docs` | `python` | Add notebooks section on website |
| https://github.com/microsoft/autogen/pull/119 | `microsoft/autogen` | `code_and_docs` | `python` | document about docker |
| https://github.com/microsoft/autogen/pull/603 | `microsoft/autogen` | `code_only` | `python` | Added warnings for some GroupChat misconfigurations and selection errors |
| https://github.com/microsoft/autogen/pull/2159 | `microsoft/autogen` | `code_only` | `python` | add warning if duplicate function is registered |
| https://github.com/microsoft/autogen/pull/1127 | `microsoft/autogen` | `code_only` | `python` | [Core] Sanitize filename before using it as docker image tag. Fix #1069 |
| https://github.com/microsoft/autogen/pull/1766 | `microsoft/autogen` | `code_only` | `python` | Add sidebar for notebooks page |
| https://github.com/microsoft/autogen/pull/1718 | `microsoft/autogen` | `code_only` | `python` | Add agent robot example to gallery |
| https://github.com/microsoft/autogen/pull/7362 | `microsoft/autogen` | `code_and_docs` | `python` | fix: Improve AutoGen Studio: deprecate FunctionTool, harden MCP WebSocket endpoint |
| https://github.com/microsoft/autogen/pull/5123 | `microsoft/autogen` | `code_only` | `python` | RichConsole: Prettify m1 CLI console using rich #4806 |
| https://github.com/microsoft/autogen/pull/2046 | `microsoft/autogen` | `code_only` | `python` | Parse Any HTML-esh Style Tags |
| https://github.com/microsoft/autogen/pull/466 | `microsoft/autogen` | `code_only` | `python` | Adding async support to get_human_input |
| https://github.com/microsoft/autogen/pull/667 | `microsoft/autogen` | `code_only` | `python` | Fix typos in my affiliation |
| https://github.com/microsoft/autogen/pull/636 | `microsoft/autogen` | `code_only` | `python` | Add basic notebook for gptassistant |
| https://github.com/microsoft/autogen/pull/6888 | `microsoft/autogen` | `code_only` | `python` | Add parallel_tool_call to openai model client config |
| https://github.com/microsoft/autogen/pull/1991 | `microsoft/autogen` | `code_only` | `python` | Redirect from /docs/tutorial/termination to /docs/tutorial/chat-termination |
| https://github.com/microsoft/autogen/pull/6969 | `microsoft/autogen` | `code_only` | `python` | Fix message ID for correlation between streaming chunks and final mes… |
| https://github.com/microsoft/autogen/pull/1516 | `microsoft/autogen` | `code_only` | `python` | Disable default code execution on society_of_mind and web_surfer. |
| https://github.com/microsoft/autogen/pull/7051 | `microsoft/autogen` | `code_only` | `python` | fix: order by clause |
| https://github.com/microsoft/autogen/pull/7060 | `microsoft/autogen` | `code_and_docs` | `python` | Update website for 0.7.5 |
| https://github.com/microsoft/autogen/pull/7058 | `microsoft/autogen` | `code_only` | `python` | Update version to 0.7.5 |
| https://github.com/microsoft/autogen/pull/7054 | `microsoft/autogen` | `code_only` | `python` | Add missing reasoning_effort parameter support for OpenAI GPT-5 models |
| https://github.com/microsoft/autogen/pull/7045 | `microsoft/autogen` | `code_only` | `python` | Fix(mcp): drain pending command futures on McpSessionActor failure |
| https://github.com/microsoft/autogen/pull/5863 | `microsoft/autogen` | `code_only` | `python` | Supporting Teams as Participants in a GroupChat |
| https://github.com/microsoft/autogen/pull/6987 | `microsoft/autogen` | `code_only` | `python` | Fix not supported field warnings in count_tokens_openai |
| https://github.com/microsoft/autogen/pull/6993 | `microsoft/autogen` | `code_only` | `python` | Fix: Handle nested objects in array items for JSON schema conversion |
| https://github.com/microsoft/autogen/pull/7035 | `microsoft/autogen` | `code_only` | `python` | Add security warnings and default to DockerCommandLineCodeExecutor |
| https://github.com/microsoft/autogen/pull/7025 | `microsoft/autogen` | `code_only` | `python` | Fix spurious </think> tags caused by empty string reasoning_content in streaming |
| https://github.com/microsoft/autogen/pull/6963 | `microsoft/autogen` | `code_only` | `python` | Fix finish_reason logic in Azure AI client streaming response |
| https://github.com/microsoft/autogen/pull/7030 | `microsoft/autogen` | `code_only` | `python` | Fix OllamaChatCompletionClient load_component() error by adding to WELL_KNOWN_PROVIDERS |
| https://github.com/microsoft/autogen/pull/7022 | `microsoft/autogen` | `code_only` | `python` | Fix Redis caching always returning False due to unhandled string values |
| https://github.com/microsoft/autogen/pull/7026 | `microsoft/autogen` | `code_only` | `python` | Fix GraphFlow cycle detection to properly clean up recursion state |
| https://github.com/microsoft/autogen/pull/7002 | `microsoft/autogen` | `code_only` | `python` | Add thinking mode support for anthropic client |
| https://github.com/microsoft/autogen/pull/7006 | `microsoft/autogen` | `code_only` | `python` | fix: extra args not work to disable thinking |
| https://github.com/microsoft/autogen/pull/395 | `microsoft/autogen` | `code_only_tests_or_fixtures` | `python` | config list for test |
| https://github.com/microsoft/autogen/pull/431 | `microsoft/autogen` | `code_only` | `python` | spelling fix for  math_user_proxy_agent.py |
| https://github.com/microsoft/autogen/pull/6529 | `microsoft/autogen` | `code_only` | `python` | feat: support multiple workbenches in assistant agent |
| https://github.com/microsoft/autogen/pull/551 | `microsoft/autogen` | `code_only` | `python` | copy dicts before modifying |
| https://github.com/microsoft/autogen/pull/1946 | `microsoft/autogen` | `code_only` | `python` | improve validation of llm_config |
| https://github.com/microsoft/autogen/pull/6889 | `microsoft/autogen` | `code_only` | `python` | Fix structured logging serialization data loss with SerializeAsAny annotations |
| https://github.com/microsoft/autogen/pull/6972 | `microsoft/autogen` | `code_only` | `python` | Support linear memory in RedisMemory |
| https://github.com/microsoft/autogen/pull/6979 | `microsoft/autogen` | `code_only` | `python` | Fix loading streaming Bedrock response with tool usage with empty argument |
| https://github.com/microsoft/autogen/pull/6956 | `microsoft/autogen` | `code_and_docs` | `python` | Update doc 0.7.4 |
| https://github.com/microsoft/autogen/pull/6955 | `microsoft/autogen` | `code_only` | `python` | update version to 0.7.4 |
| https://github.com/microsoft/autogen/pull/6954 | `microsoft/autogen` | `code_only` | `python` | Redis Doesn't Support Streaming |
| https://github.com/microsoft/autogen/pull/6952 | `microsoft/autogen` | `code_only` | `python` | Fix Redis Deserialization Error |
| https://github.com/microsoft/autogen/pull/6948 | `microsoft/autogen` | `code_and_docs` | `python` | Update docs for 0.7.3 |
| https://github.com/microsoft/autogen/pull/6947 | `microsoft/autogen` | `code_only` | `python` | Update version to 0.7.3 |
| https://github.com/microsoft/autogen/pull/6946 | `microsoft/autogen` | `code_only` | `python` | Ensure task runner tools are always strict |
| https://github.com/microsoft/autogen/pull/6943 | `microsoft/autogen` | `code_only` | `python` | Update OpenAIAgent to reflect gap in supporting custom function tool |
| https://github.com/microsoft/autogen/pull/6945 | `microsoft/autogen` | `code_only` | `python` | Add model info for gpt-5 |
| https://github.com/microsoft/autogen/pull/6936 | `microsoft/autogen` | `code_only` | `python` | Fix OpenAIAgent function tool schema |
| https://github.com/microsoft/autogen/pull/6905 | `microsoft/autogen` | `code_only` | `python` | fix: Add proper serialization to RedisStore for complex objects |
| https://github.com/microsoft/autogen/pull/6418 | `microsoft/autogen` | `code_only` | `python` | Feature: Add OpenAIAgent backed by OpenAI Response API |
| https://github.com/microsoft/autogen/pull/6925 | `microsoft/autogen` | `code_only` | `python` | Extend pydantic model capability for anyOf/oneOf item typing |
| https://github.com/microsoft/autogen/pull/6901 | `microsoft/autogen` | `code_and_docs` | `python` | Add warning for MCP server docs |
| https://github.com/microsoft/autogen/pull/6902 | `microsoft/autogen` | `code_and_docs` | `python` | Update website for 0.7.2 |
| https://github.com/microsoft/autogen/pull/6897 | `microsoft/autogen` | `code_only` | `python` | Adds support for JSON and MARKDOWN in Redis agent memory |
| https://github.com/microsoft/autogen/pull/6895 | `microsoft/autogen` | `code_only` | `python` | Update version 0.7.2 |
| https://github.com/microsoft/autogen/pull/6678 | `microsoft/autogen` | `code_only` | `python` | Fix output task messages 6150 |
| https://github.com/microsoft/autogen/pull/1317 | `microsoft/autogen` | `code_and_docs` | `python` | Support for Python 3.12 |
| https://github.com/microsoft/autogen/pull/6883 | `microsoft/autogen` | `code_only` | `python` | Add documentation warnings for AgentTool/TeamTool parallel tool calls limitation |
| https://github.com/microsoft/autogen/pull/6886 | `microsoft/autogen` | `code_and_docs` | `python` | Add approval_func option to CodeExecutorAgent |
| https://github.com/microsoft/autogen/pull/1511 | `microsoft/autogen` | `code_only` | `python` | Added new models to token_count_utils |
| https://github.com/microsoft/autogen/pull/6684 | `microsoft/autogen` | `code_only` | `python` | Make DockerCommandLineCodeExecutor the default for MagenticOne team |
| https://github.com/microsoft/autogen/pull/6866 | `microsoft/autogen` | `code_only` | `python` | Remove assistant related methods from OpenAIAgent |
| https://github.com/microsoft/autogen/pull/6743 | `microsoft/autogen` | `code_only` | `python` | Adds Redis Memory extension class |
| https://github.com/microsoft/autogen/pull/6871 | `microsoft/autogen` | `code_only` | `python` | Update 0.7.1 website ref |
| https://github.com/microsoft/autogen/pull/6870 | `microsoft/autogen` | `code_only` | `python` | Update OpenAIAssistantAgent doc |
| https://github.com/microsoft/autogen/pull/6869 | `microsoft/autogen` | `code_and_docs` | `python` | Update website 0.7.1 |
| https://github.com/microsoft/autogen/pull/6868 | `microsoft/autogen` | `code_only` | `python` | Update version to 0.7.1 |
| https://github.com/microsoft/autogen/pull/6867 | `microsoft/autogen` | `code_only` | `python` | Bring back OpenAIAssistantAgent |
| https://github.com/microsoft/autogen/pull/6744 | `microsoft/autogen` | `code_and_docs` | `python` | upgrade graphrag sample to v2.3+ |
| https://github.com/microsoft/autogen/pull/6860 | `microsoft/autogen` | `code_only` | `python` | fix: load agent correctly in test service |
| https://github.com/microsoft/autogen/pull/6864 | `microsoft/autogen` | `code_only` | `python` | fix: use ```sh consistently |
| https://github.com/microsoft/autogen/pull/6865 | `microsoft/autogen` | `code_and_docs` | `python` | Update version to 0.7.0 |
| https://github.com/microsoft/autogen/pull/6863 | `microsoft/autogen` | `code_only` | `python` | Update installation guide in _openai_assistant_agent.py |
| https://github.com/microsoft/autogen/pull/6845 | `microsoft/autogen` | `code_only` | `python` | Add `include_name_in_message` parameter to make `name` field optional in OpenAI messages |
| https://github.com/microsoft/autogen/pull/6846 | `microsoft/autogen` | `code_only` | `python` | Add support for `"format": "json"` in JSON schemas |
| https://github.com/microsoft/autogen/pull/6831 | `microsoft/autogen` | `code_only` | `python` | fix: use correct format when adding memory to mem0 |
| https://github.com/microsoft/autogen/pull/6697 | `microsoft/autogen` | `code_only` | `python` | Add `tool_choice` parameter to `ChatCompletionClient` `create` and `create_stream` methods |
| https://github.com/microsoft/autogen/pull/6799 | `microsoft/autogen` | `code_only` | `python` | Fix OpenAI UnprocessableEntityError when AssistantAgent makes multiple tool calls |
| https://github.com/microsoft/autogen/pull/6827 | `microsoft/autogen` | `code_only` | `python` | Deprecating openai assistant agent. Apply version conditioned import for open ai version < 1.83 |
| https://github.com/microsoft/autogen/pull/6818 | `microsoft/autogen` | `code_only` | `python` | feat: add timeout for http tools |
| https://github.com/microsoft/autogen/pull/6814 | `microsoft/autogen` | `code_only` | `python` | Upgrade_mcp_version |
| https://github.com/microsoft/autogen/pull/6797 | `microsoft/autogen` | `code_only` | `python` | Fix JSON serialization of team state by handling datetime objects in message dump |
| https://github.com/microsoft/autogen/pull/6813 | `microsoft/autogen` | `code_and_docs` | `python` | Setup publishing for pyautogen package |
| https://github.com/microsoft/autogen/pull/172 | `microsoft/autogen` | `code_only` | `python` | Warn if use_docker evaluates to True but the python docker package is not available. |
| https://github.com/microsoft/autogen/pull/6671 | `microsoft/autogen` | `code_only` | `python` | Feat/OpenAI agent builtin tools 6657 |
| https://github.com/microsoft/autogen/pull/6682 | `microsoft/autogen` | `code_only` | `python` | Added DuckDuckGo Search Tool and Agent in AutoGen Extensions |
| https://github.com/microsoft/autogen/pull/6784 | `microsoft/autogen` | `code_and_docs` | `python` | Update to version 0.6.4 |
| https://github.com/microsoft/autogen/pull/6783 | `microsoft/autogen` | `code_only` | `python` | Remove duckduckgo search tools and agents |
| https://github.com/microsoft/autogen/pull/6782 | `microsoft/autogen` | `code_and_docs` | `python` | Update website to 0.6.3 |
| https://github.com/microsoft/autogen/pull/6781 | `microsoft/autogen` | `code_only` | `python` | Update version to 0.6.3 |
| https://github.com/microsoft/autogen/pull/6775 | `microsoft/autogen` | `code_only` | `python` | Remove otel semcov package from core dependencies |
| https://github.com/microsoft/autogen/pull/4874 | `microsoft/autogen` | `code_only` | `python` | Fix: Correct cancellation token usage in UserProxyAgent docstring |
| https://github.com/microsoft/autogen/pull/6731 | `microsoft/autogen` | `code_only` | `python` | SingleThreadedAgentRuntime to use subclass check for factory_wrapper instead of equality |
| https://github.com/microsoft/autogen/pull/6650 | `microsoft/autogen` | `code_only` | `python` | feat: add qwen2.5vl support |
| https://github.com/microsoft/autogen/pull/6759 | `microsoft/autogen` | `code_only` | `python` | Update GitHub Models url to the new url |
| https://github.com/microsoft/autogen/pull/6763 | `microsoft/autogen` | `code_only` | `python` | Add reflection for claude model in AssistantAgent |
| https://github.com/microsoft/autogen/pull/6690 | `microsoft/autogen` | `code_only` | `python` | Add tool name and description override functionality to Workbench implementations |
| https://github.com/microsoft/autogen/pull/6752 | `microsoft/autogen` | `code_only` | `python` | Fix GraphFlowManager termination to prevent _StopAgent from polluting conversation context |
| https://github.com/microsoft/autogen/pull/6747 | `microsoft/autogen` | `code_only` | `python` | Fix GraphFlow to support multiple task execution without explicit reset |
| https://github.com/microsoft/autogen/pull/6750 | `microsoft/autogen` | `code_only` | `python` | Fix function calling support for Llama3.3 |
| https://github.com/microsoft/autogen/pull/233 | `microsoft/autogen` | `code_only` | `python` |  docstr updated for `use_docker` in `execute_code ` |
| https://github.com/microsoft/autogen/pull/1252 | `microsoft/autogen` | `code_only_tests_or_fixtures` | `python` | Improve test for function call in groupchat |
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
| https://github.com/microsoft/semantic-kernel/pull/14135 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: [Breaking] Update runtime handling |
| https://github.com/microsoft/semantic-kernel/pull/14140 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: OpenApi: Harden operation path handling for consistent selection and request targeting (.Net & Python) |
| https://github.com/microsoft/semantic-kernel/pull/14132 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Disable automatic HTTP redirects in HttpPlugin and WebFileDownloadPlugin default clients |
| https://github.com/microsoft/semantic-kernel/pull/14127 | `microsoft/semantic-kernel` | `code_and_docs` | `python` | Python: Default MCP SSE server samples to loopback with host validation |
| https://github.com/microsoft/semantic-kernel/pull/14124 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Enforce excluded_functions on MCP tool invocation path |
| https://github.com/microsoft/semantic-kernel/pull/14119 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Update .NET SDK to 10.0.301 |
| https://github.com/microsoft/semantic-kernel/pull/13858 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Bump axios to 1.16.0 and form-data to 4.0.6 in /dotnet/samples/Demos/ProcessFrameworkWithSignalR |
| https://github.com/microsoft/semantic-kernel/pull/14118 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Harden file path validation in Core, Document, and Web plugins |
| https://github.com/microsoft/semantic-kernel/pull/14044 | `microsoft/semantic-kernel` | `code_only` | `python` | Bump axios from 1.13.2 to 1.16.0 in /dotnet/samples/Demos/ProcessFrameworkWithSignalR/src/ProcessFramework.Aspire.SignalR.ReactFrontend |
| https://github.com/microsoft/semantic-kernel/pull/14114 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Adjust request validation |
| https://github.com/microsoft/semantic-kernel/pull/14097 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Add OpenAPI server URL validation |
| https://github.com/microsoft/semantic-kernel/pull/14065 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Bump torch from 2.8.0 to 2.12.0 in /python |
| https://github.com/microsoft/semantic-kernel/pull/14058 | `microsoft/semantic-kernel` | `code_only` | `python` | Bump pyarrow from 21.0.0 to 23.0.1 in /python |
| https://github.com/microsoft/semantic-kernel/pull/14089 | `microsoft/semantic-kernel` | `code_only_tests_or_fixtures` | `python` | Python: Bump bleach from 6.3.0 to 6.4.0 in /python |
| https://github.com/microsoft/semantic-kernel/pull/14070 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Bump esbuild, @vitejs/plugin-react, vite, and transitive lockfile deps in /dotnet/samples/Demos/ProcessFrameworkWithSignalR/src/Pro... |
| https://github.com/microsoft/semantic-kernel/pull/13866 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Update pymongo requirement from <4.16,>=4.8.0 to >=4.8.0,<4.17 in /python |
| https://github.com/microsoft/semantic-kernel/pull/13604 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Bump minimatch from 3.1.2 to 3.1.5 in /dotnet/samples/Demos/ProcessWithCloudEvents/ProcessWithCloudEvents.Client |
| https://github.com/microsoft/semantic-kernel/pull/14092 | `microsoft/semantic-kernel` | `code_only_tests_or_fixtures` | `python` | Python: Bump starlette from 0.52.1 to 1.3.1 in /python |
| https://github.com/microsoft/semantic-kernel/pull/14083 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Bump @babel/core from 7.26.10 to 7.29.7 in /dotnet/samples/Demos/ProcessWithCloudEvents/ProcessWithCloudEvents.Client |
| https://github.com/microsoft/semantic-kernel/pull/14090 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Bump tornado from 6.5.5 to 6.5.7 in /python |
| https://github.com/microsoft/semantic-kernel/pull/13877 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Bump follow-redirects from 1.15.11 to 1.16.0 in /dotnet/samples/Demos/ProcessFrameworkWithSignalR/src/ProcessFramework.Aspire.Signa... |
| https://github.com/microsoft/semantic-kernel/pull/14082 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Bump form-data from 4.0.5 to 4.0.6 in /dotnet/samples/Demos/ProcessFrameworkWithSignalR/src/ProcessFramework.Aspire.SignalR.ReactFr... |
| https://github.com/microsoft/semantic-kernel/pull/14093 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Bump Python version to 1.43.1 for a release. |
| https://github.com/microsoft/semantic-kernel/pull/14086 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Reject encoded dot-segment paths in OpenAPI plugin (.NET and Python) |
| https://github.com/microsoft/semantic-kernel/pull/13635 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: fix: prevent duplicate "null" in JSON Schema type arrays for nullable parameters |
| https://github.com/microsoft/semantic-kernel/pull/14057 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Add function_choice_behavior support to Azure AI and OpenAI Assistant agents |
| https://github.com/microsoft/semantic-kernel/pull/14052 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Bump Python package version to 1.43.0 for a release |
| https://github.com/microsoft/semantic-kernel/pull/14026 | `microsoft/semantic-kernel` | `code_only_tests_or_fixtures` | `python` | ci: harden Python test coverage workflow |
| https://github.com/microsoft/semantic-kernel/pull/14029 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Enable default-on server URL validation for OpenAPI plugins |
| https://github.com/microsoft/semantic-kernel/pull/14009 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: [Breaking] Update OpenAPI document parsing options |
| https://github.com/microsoft/semantic-kernel/pull/14014 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Improve function call invocation parameter consistency |
| https://github.com/microsoft/semantic-kernel/pull/14007 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Bump Python pkg version to 1.42.0 for a release. |
| https://github.com/microsoft/semantic-kernel/pull/14003 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Improvements for MCP |
| https://github.com/microsoft/semantic-kernel/pull/13969 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Harden HttpPlugin request validation |
| https://github.com/microsoft/semantic-kernel/pull/13971 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Stop accessing private Azure SDK attributes in Azure AI Search connector |
| https://github.com/microsoft/semantic-kernel/pull/13967 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Percent-encode OpenAPI path params & pin azure-search-documents |
| https://github.com/microsoft/semantic-kernel/pull/13958 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Harden CloudDrivePlugin defaults and add path validation |
| https://github.com/microsoft/semantic-kernel/pull/13962 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Improve input validation in OpenAPI plugin |
| https://github.com/microsoft/semantic-kernel/pull/13431 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: feat(connectors): Support ImageContent in tool/function results |
| https://github.com/microsoft/semantic-kernel/pull/13961 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Harden gRPC plugin address handling |
| https://github.com/microsoft/semantic-kernel/pull/13956 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Fix DocumentPlugin path validation order |
| https://github.com/microsoft/semantic-kernel/pull/13953 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Add deny-by-default AllowedUploadDirectories to CloudDrivePlugin |
| https://github.com/microsoft/semantic-kernel/pull/13884 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: fix: fall back to ToString() when logging function results with unregistered types |
| https://github.com/microsoft/semantic-kernel/pull/13621 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Fix VertexAI global endpoint URI construction (#13620) |
| https://github.com/microsoft/semantic-kernel/pull/13941 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Fix whitespace formatting in PromptExecutionSettingsExtensions.cs |
| https://github.com/microsoft/semantic-kernel/pull/13934 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Add ExtraBody to OpenAIPromptExecutionSettings (#12307) |
| https://github.com/microsoft/semantic-kernel/pull/13886 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Update Step04_AzureAIAgent_CodeInterpreter.cs |
| https://github.com/microsoft/semantic-kernel/pull/13864 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Update pydantic requirement from !=2.10.0,!=2.10.1,!=2.10.2,!=2.10.3,<2.13,>=2.0 to >=2.0,!=2.10.0,!=2.10.1,!=2.10.2,!=2.10.3,<2.... |
| https://github.com/microsoft/semantic-kernel/pull/13865 | `microsoft/semantic-kernel` | `code_only` | `python` | Update google-genai requirement from ~=1.51.0 to >=1.51,<1.75 in /python |
| https://github.com/microsoft/semantic-kernel/pull/13577 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Bump google-cloud-aiplatform from 1.114.0 to 1.133.0 in /python |
| https://github.com/microsoft/semantic-kernel/pull/13867 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Update boto3 requirement from <1.41.0,>=1.36.4 to >=1.36.4,<1.43.0 in /python |
| https://github.com/microsoft/semantic-kernel/pull/13868 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Bump onnxruntime from 1.22.1 to 1.24.3 in /python |
| https://github.com/microsoft/semantic-kernel/pull/13928 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: VectorData connector bugfix release |
| https://github.com/microsoft/semantic-kernel/pull/13926 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Bump package version to 1.41.3 for a release |
| https://github.com/microsoft/semantic-kernel/pull/13910 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Harden AllowedBaseUrls validation in RestApiOperationRunner |
| https://github.com/microsoft/semantic-kernel/pull/13897 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Extend InMemoryCollection filter attribute blocklist |
| https://github.com/microsoft/semantic-kernel/pull/13893 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Add field and table name escaping for python SqlServer connector |
| https://github.com/microsoft/semantic-kernel/pull/13901 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Validate step types |
| https://github.com/microsoft/semantic-kernel/pull/13902 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Add backslash escaping to redis text search values |
| https://github.com/microsoft/semantic-kernel/pull/13900 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Fix single-quote escaping in OBJECT_ID and dynamic SQL string literals |
| https://github.com/microsoft/semantic-kernel/pull/13863 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Update SQL Server vector search to latest VECTOR_SEARCH() syntax |
| https://github.com/microsoft/semantic-kernel/pull/13850 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: bump py version to 1.41.2 for a release |
| https://github.com/microsoft/semantic-kernel/pull/13330 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Update ipykernel requirement from ~=6.29 to >=6.29,<8.0 in /python |
| https://github.com/microsoft/semantic-kernel/pull/13235 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Respect FunctionChoiceBehavior filters in OpenAI responses agent tools |
| https://github.com/microsoft/semantic-kernel/pull/13246 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Update pydantic requirement from !=2.10.0,!=2.10.1,!=2.10.2,!=2.10.3,<2.12,>=2.0 to >=2.0,!=2.10.0,!=2.10.1,!=2.10.2,!=2.10.3,<2.... |
| https://github.com/microsoft/semantic-kernel/pull/13124 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Update pymongo requirement from <4.15,>=4.8.0 to >=4.8.0,<4.16 in /python |
| https://github.com/microsoft/semantic-kernel/pull/13331 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Update chromadb requirement from <1.1,>=0.5 to >=0.5,<1.4 in /python |
| https://github.com/microsoft/semantic-kernel/pull/13329 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Update redis[hiredis] requirement from ~=6.0 to >=6,<8 in /python |
| https://github.com/microsoft/semantic-kernel/pull/13738 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Improve prompt-template msg serialize and sample usage |
| https://github.com/microsoft/semantic-kernel/pull/13699 | `microsoft/semantic-kernel` | `code_only` | `python` | Refactor CollectionModel/builder and introduce read-only property interfaces |
| https://github.com/microsoft/semantic-kernel/pull/13705 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Bump Python version to 1.41.1 for a release |
| https://github.com/microsoft/semantic-kernel/pull/13624 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: fix Google AI/Vertex AI crash on anyOf schema (#12442) |
| https://github.com/microsoft/semantic-kernel/pull/13607 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: fix(google-ai): skip api_key check when use_vertexai is True |
| https://github.com/microsoft/semantic-kernel/pull/13596 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Default Dapr module allowlist to semantic_kernel prefix |
| https://github.com/microsoft/semantic-kernel/pull/13689 | `microsoft/semantic-kernel` | `code_only` | `python` | Simplify PR parsing for automated review workflow |
| https://github.com/microsoft/semantic-kernel/pull/13608 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: fix: ChatHistoryTruncationReducer orphans TOOL role messages |
| https://github.com/microsoft/semantic-kernel/pull/13698 | `microsoft/semantic-kernel` | `code_only` | `python` | [MEVD] Fix VectorStoreKeyAttribute.IsAutoGenerated to be usable as a compile-time attribute argument |
| https://github.com/microsoft/semantic-kernel/pull/13612 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: feat: Add support for dimensions in Vertex AI embedding services |
| https://github.com/microsoft/semantic-kernel/pull/13687 | `microsoft/semantic-kernel` | `code_only` | `python` | DF PR Review workflow |
| https://github.com/microsoft/semantic-kernel/pull/13668 | `microsoft/semantic-kernel` | `code_only` | `python` | Update OpenAI to 2.9.1, Azure.AI.OpenAI to 2.9.0-beta.1, Azure.AI.Projects to 2.0.0-beta.2, Microsoft.Extensions.AI* to 10.4.0 |
| https://github.com/microsoft/semantic-kernel/pull/13683 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: [Breaking] Harden DocumentPlugin security defaults with deny-by-default AllowedDirectories |
| https://github.com/microsoft/semantic-kernel/pull/13610 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Fix ChatHistoryTruncationReducer deleting system prompt |
| https://github.com/microsoft/semantic-kernel/pull/13686 | `microsoft/semantic-kernel` | `code_only_tests_or_fixtures` | `python` | Reduce macos runner coverage due to capacity |
| https://github.com/microsoft/semantic-kernel/pull/13644 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: [Breaking] Harden plugin security defaults for WebFileDownloadPlugin |
| https://github.com/microsoft/semantic-kernel/pull/13638 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Fixes Qdrant 1.17 issue with returning empty vectors |
| https://github.com/microsoft/semantic-kernel/pull/13650 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Migrate from deprecated DALL-E models to gpt-image-1 |
| https://github.com/microsoft/semantic-kernel/pull/13633 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: fix prompt template engine blocking HTML tags in content |
| https://github.com/microsoft/semantic-kernel/pull/13680 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Fix image integration tests that are now blocked due to bot policies |
| https://github.com/microsoft/semantic-kernel/pull/11430 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Add ChatCompletionAgent integration tests |
| https://github.com/microsoft/semantic-kernel/pull/13609 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: fix(python/google): preserve thought_signature in Gemini function call parts |
| https://github.com/microsoft/semantic-kernel/pull/13655 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Bump Python version to 1.41.0 for a release |
| https://github.com/microsoft/semantic-kernel/pull/13651 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Add support to new openai text to image model |
| https://github.com/microsoft/semantic-kernel/pull/13637 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Refinement of in memory vector collection filter |
| https://github.com/microsoft/semantic-kernel/pull/13645 | `microsoft/semantic-kernel` | `code_only` | `python` | Updating recommended extensions list. |
| https://github.com/microsoft/semantic-kernel/pull/11584 | `microsoft/semantic-kernel` | `code_and_docs` | `python` | .Net: Fix Nullable Bug Gemini Schema Generation |
| https://github.com/microsoft/semantic-kernel/pull/11827 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Per deprecation message and date remove add_chat_message from AzureAIAgent and OpenAIAssistantAgent |
| https://github.com/microsoft/semantic-kernel/pull/11783 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Feature process v2 |
| https://github.com/microsoft/semantic-kernel/pull/11518 | `microsoft/semantic-kernel` | `code_only_tests_or_fixtures` | `python` | Python: New tests for azure_cosmos_db_mongodb_collection and local_step |
| https://github.com/microsoft/semantic-kernel/pull/11342 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: MCP prompt sample |
| https://github.com/microsoft/semantic-kernel/pull/11298 | `microsoft/semantic-kernel` | `code_and_docs` | `python` | Python: Fix sample and README |
| https://github.com/microsoft/semantic-kernel/pull/11254 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Add support for setting agent configuration for declarative agents |
| https://github.com/microsoft/semantic-kernel/pull/11232 | `microsoft/semantic-kernel` | `code_and_docs` | `python` | .Net: Add MCP server/client sample |
| https://github.com/microsoft/semantic-kernel/pull/13631 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Add server URL validation options for OpenAPI plugins |
| https://github.com/microsoft/semantic-kernel/pull/11210 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Update the getting started samples to use the new Agent invoke API |
| https://github.com/microsoft/semantic-kernel/pull/11166 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Bedrock dotnet |
| https://github.com/microsoft/semantic-kernel/pull/11056 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Pass api_key to azure config base init |
| https://github.com/microsoft/semantic-kernel/pull/11034 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Bump Python version to 1.25.0 for a release. |
| https://github.com/microsoft/semantic-kernel/pull/10902 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Update websockets requirement from <15,>=13 to >=13,<16 in /python |
| https://github.com/microsoft/semantic-kernel/pull/10946 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Model dump json step info for Dapr step actor |
| https://github.com/microsoft/semantic-kernel/pull/10858 | `microsoft/semantic-kernel` | `code_and_docs` | `python` | .Net: Structured Data Plugin - Query and CRUD Operations |
| https://github.com/microsoft/semantic-kernel/pull/10748 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Allow OpenAIAssistant model id to pass into setup resources |
| https://github.com/microsoft/semantic-kernel/pull/10726 | `microsoft/semantic-kernel` | `code_and_docs` | `python` | Python: Cleanup ChatCompletionAgent concept samples |
| https://github.com/microsoft/semantic-kernel/pull/10704 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: improve feature decorator return type so it doesn't affect Pylance |
| https://github.com/microsoft/semantic-kernel/pull/10660 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Update boto3 requirement from ~=1.36.4 to >=1.36.4,<1.38.0 in /python |
| https://github.com/microsoft/semantic-kernel/pull/10616 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net Agents - Refine client provider/factory |
| https://github.com/microsoft/semantic-kernel/pull/10462 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Remove old references of plugin import |
| https://github.com/microsoft/semantic-kernel/pull/10378 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Update motor requirement from <3.7.0,>=3.3.2 to >=3.3.2,<3.8.0 in /python |
| https://github.com/microsoft/semantic-kernel/pull/10356 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Graduate OpenAPI package |
| https://github.com/microsoft/semantic-kernel/pull/10245 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Grab function_name from kwargs if present in ProcessStepEdgeBuilder |
| https://github.com/microsoft/semantic-kernel/pull/10123 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Use UriKind.Relative |
| https://github.com/microsoft/semantic-kernel/pull/13629 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Fix input checking in Cosmos NoSQL, Redis and Weaviate providers |
| https://github.com/microsoft/semantic-kernel/pull/13622 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Fix column nullability in SQL MEVD providers |
| https://github.com/microsoft/semantic-kernel/pull/13611 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Net: Address roji/westey review feedback round 2 on text search connectors (#10456) |
| https://github.com/microsoft/semantic-kernel/pull/13615 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Deduplicate embedding generation management |
| https://github.com/microsoft/semantic-kernel/pull/13291 | `microsoft/semantic-kernel` | `code_and_docs` | `python` | Python: support (Azure) OpenAI realtime audio models |
| https://github.com/microsoft/semantic-kernel/pull/13600 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Handle installation of pgvector on PostgreSQL |
| https://github.com/microsoft/semantic-kernel/pull/13594 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: [MEVD] Add validation for mismatched collection key |
| https://github.com/microsoft/semantic-kernel/pull/13580 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Add provider-specific search parameters to Bing/Google connectors |
| https://github.com/microsoft/semantic-kernel/pull/13593 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: [MEVD] Make PG schema nullable |
| https://github.com/microsoft/semantic-kernel/pull/13465 | `microsoft/semantic-kernel` | `code_and_docs` | `python` | .Net: Use testcontainer for SQL Server 2025 |
| https://github.com/microsoft/semantic-kernel/pull/13485 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: [MEVD] Introduce FilterTranslatorBase and remove duplication |
| https://github.com/microsoft/semantic-kernel/pull/13569 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: [MEVD] Support DateTime/DateTimeOffset/DateOnly/TimeOnly across providers |
| https://github.com/microsoft/semantic-kernel/pull/13544 | `microsoft/semantic-kernel` | `code_and_docs` | `python` | .Net: Update Microsoft.Extensions.AI dependencies to 10.3.0 and OpenAI SDK to 2.8.0 |
| https://github.com/microsoft/semantic-kernel/pull/13573 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: [MEVD] SQL Server approximate vector search |
| https://github.com/microsoft/semantic-kernel/pull/13546 | `microsoft/semantic-kernel` | `code_and_docs` | `python` | .Net: docs: Fix ADR numbering |
| https://github.com/microsoft/semantic-kernel/pull/13572 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: [TINY] [MEVD] Remove SupportsMultipleKeys |
| https://github.com/microsoft/semantic-kernel/pull/13564 | `microsoft/semantic-kernel` | `code_and_docs` | `python` | .Net: fix: Remove OldFilter dependency from VectorStoreTextSearch (#1… |
| https://github.com/microsoft/semantic-kernel/pull/13550 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: [MEVD] Cosmos NoSQL provider work on keys, partition keys and point reads |
| https://github.com/microsoft/semantic-kernel/pull/13543 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: fix: Address Bing negation and Google property mapping bugs |
| https://github.com/microsoft/semantic-kernel/pull/13541 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: fix: Fix AOT Compatibility - Remove Expression.Compile() from Brave/Tavily TextSearch |
| https://github.com/microsoft/semantic-kernel/pull/13545 | `microsoft/semantic-kernel` | `code_only` | `python` | Remove unused workflow |
| https://github.com/microsoft/semantic-kernel/pull/13542 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: fix: Revert Brave legacy interface breaking change |
| https://github.com/microsoft/semantic-kernel/pull/13535 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: fix: Remove obsolete ITextSearch vector store integration tests |
| https://github.com/microsoft/semantic-kernel/pull/13514 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: [MEVD] Map DateTime to timestamptz on PostgreSQL |
| https://github.com/microsoft/semantic-kernel/pull/13512 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Implement SQL Server hybrid search |
| https://github.com/microsoft/semantic-kernel/pull/13526 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Update DirectoryObjects.yml URL from dev to main branch |
| https://github.com/microsoft/semantic-kernel/pull/13505 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: refinement of filtering |
| https://github.com/microsoft/semantic-kernel/pull/13478 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Add file upload security controls to SessionsPythonPlugin |
| https://github.com/microsoft/semantic-kernel/pull/13502 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Implement PostgreSQL hybrid search |
| https://github.com/microsoft/semantic-kernel/pull/13501 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: [MEVD] Implement support for score threshold |
| https://github.com/microsoft/semantic-kernel/pull/13503 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Bump Python version to 1.39.3 for a release |
| https://github.com/microsoft/semantic-kernel/pull/13499 | `microsoft/semantic-kernel` | `code_only` | `python` | Python: Add class validation for Dapr Runtime step loading |
| https://github.com/microsoft/semantic-kernel/pull/13137 | `microsoft/semantic-kernel` | `code_only` | `python` | Bump actions/setup-dotnet from 4 to 5 |
| https://github.com/microsoft/semantic-kernel/pull/13409 | `microsoft/semantic-kernel` | `code_only` | `python` | Bump mdast-util-to-hast from 13.2.0 to 13.2.1 in /dotnet/samples/Demos/ProcessWithCloudEvents/ProcessWithCloudEvents.Client |
| https://github.com/microsoft/semantic-kernel/pull/12979 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Bump form-data from 4.0.2 to 4.0.4 in /dotnet/samples/Demos/ProcessFrameworkWithSignalR |
| https://github.com/microsoft/semantic-kernel/pull/13388 | `microsoft/semantic-kernel` | `code_only` | `python` | Bump vite from 6.2.7 to 6.4.1 in /dotnet/samples/Demos/ProcessFrameworkWithSignalR/src/ProcessFramework.Aspire.SignalR.ReactFrontend |
| https://github.com/microsoft/semantic-kernel/pull/13479 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: Adding copilot cli to the codespace definition |
| https://github.com/microsoft/semantic-kernel/pull/13471 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: [MEVD] Support .Any(x => x.Contains(...)) in filters  |
| https://github.com/microsoft/semantic-kernel/pull/13470 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: [MEVD] Ensure identifiers are properly quoted |
| https://github.com/microsoft/semantic-kernel/pull/13472 | `microsoft/semantic-kernel` | `code_only` | `python` | .Net: ItCanReturnImageUrlAsync test is flakey so skipping |
| https://github.com/microsoft/vscode/pull/332609 | `microsoft/vscode` | `code_only` | `typescript` | Preserve user picker state for orchestration when Agent Merge is enabled |
| https://github.com/microsoft/vscode/pull/160703 | `microsoft/vscode` | `code_only` | `typescript` | Rename leftover respectAutoSaveConfig variable to isRefactoring |
| https://github.com/microsoft/vscode/pull/332643 | `microsoft/vscode` | `code_only` | `typescript` | chat: verify exact plugin commit checkouts |
| https://github.com/microsoft/vscode/pull/332634 | `microsoft/vscode` | `code_only` | `typescript` | agentHost: apply customization changes made before the first message |
| https://github.com/microsoft/vscode/pull/332638 | `microsoft/vscode` | `code_only` | `typescript` | mcp: normalize install URI configurations |
| https://github.com/microsoft/vscode/pull/332574 | `microsoft/vscode` | `code_only` | `typescript` | Rename from the session header uses the inline title input |
| https://github.com/microsoft/vscode/pull/329157 | `microsoft/vscode` | `code_only` | `typescript` | Update error message in inlineChatIntent.ts |
| https://github.com/microsoft/vscode/pull/332581 | `microsoft/vscode` | `code_only` | `typescript` | Agent Host: Make debug log export best effort |
| https://github.com/microsoft/vscode/pull/332598 | `microsoft/vscode` | `code_only` | `typescript` | chat: explain why Agent Merge turned itself off |
| https://github.com/microsoft/vscode/pull/332584 | `microsoft/vscode` | `code_only` | `typescript` | managed settings: fix claude enablement |
| https://github.com/microsoft/vscode/pull/332590 | `microsoft/vscode` | `code_and_docs` | `typescript` | Add valid permissions presets to mock-policy-server |
| https://github.com/microsoft/vscode/pull/332588 | `microsoft/vscode` | `code_only` | `typescript` | Back off GitHub requests instead of hammering a failing service |
| https://github.com/microsoft/vscode/pull/332589 | `microsoft/vscode` | `code_and_docs` | `typescript` | agent host: anchor side chat forks at the last completed turn |
| https://github.com/microsoft/vscode/pull/262910 | `microsoft/vscode` | `code_only` | `typescript` | Fix out of bounds text selection with line wrapping |
| https://github.com/microsoft/vscode/pull/332594 | `microsoft/vscode` | `code_only` | `typescript` | Fix Electron types in PR checks |
| https://github.com/microsoft/vscode/pull/175525 | `microsoft/vscode` | `code_only` | `typescript` | Note that InlayHints with the same position are shown in-order |
| https://github.com/microsoft/vscode/pull/332569 | `microsoft/vscode` | `code_only` | `typescript` | sessions: add chat background management actions |
| https://github.com/microsoft/vscode/pull/332372 | `microsoft/vscode` | `code_only` | `typescript` | Keep terminal task icon when holding Alt |
| https://github.com/microsoft/vscode/pull/332564 | `microsoft/vscode` | `code_only` | `typescript` | Fix lone json surrogate breaking requests |
| https://github.com/microsoft/vscode/pull/332539 | `microsoft/vscode` | `code_only` | `typescript` | ci: fix electron types in product builds |
| https://github.com/microsoft/vscode/pull/332460 | `microsoft/vscode` | `code_only` | `typescript` | Fix terminal tool progress listener leak |
| https://github.com/microsoft/vscode/pull/332554 | `microsoft/vscode` | `code_and_docs` | `typescript` | Fix slight misalignment of compact model picker button |
| https://github.com/microsoft/vscode/pull/332553 | `microsoft/vscode` | `code_only` | `typescript` | agentHost: keep restarted Codex drafts provisional |
| https://github.com/microsoft/vscode/pull/332485 | `microsoft/vscode` | `code_only` | `typescript` | agent host: fix task completion summary |
| https://github.com/microsoft/vscode/pull/332562 | `microsoft/vscode` | `code_only` | `typescript` | Add developer reset pet size command |
| https://github.com/microsoft/vscode/pull/332547 | `microsoft/vscode` | `code_and_docs` | `typescript` | sessions: Fix External Agent Session Visibility Settings |
| https://github.com/microsoft/vscode/pull/332548 | `microsoft/vscode` | `code_only` | `typescript` | Address review feedback on external session files removal |
| https://github.com/microsoft/vscode/pull/332549 | `microsoft/vscode` | `code_only` | `typescript` | refactor(chat): remove CHAT_CONFIG_MENU_ID references from chat actions |
| https://github.com/microsoft/vscode/pull/332535 | `microsoft/vscode` | `code_only` | `typescript` | files: stop Windows watcher flood after folder deletion |
| https://github.com/microsoft/vscode/pull/332446 | `microsoft/vscode` | `code_only` | `typescript` | terminal: hide View in Chat for Agent Host sessions |
| https://github.com/microsoft/vscode/pull/331731 | `microsoft/vscode` | `code_only` | `typescript` | Use synchronous hooks for ESM ASAR resolution |
| https://github.com/microsoft/vscode/pull/332538 | `microsoft/vscode` | `code_only` | `typescript` | Remove external session files from the agent host adaptor |
| https://github.com/microsoft/vscode/pull/332541 | `microsoft/vscode` | `code_only` | `typescript` | agentHost: retry Codex model discovery after transient failures |
| https://github.com/microsoft/vscode/pull/332512 | `microsoft/vscode` | `code_only` | `typescript` | Move to nightly build |
| https://github.com/microsoft/vscode/pull/332532 | `microsoft/vscode` | `code_only` | `typescript` | Update modernActivityBar styles across multiple themes |
| https://github.com/microsoft/vscode/pull/332503 | `microsoft/vscode` | `code_only` | `typescript` | sessions: harden ChatGPT profile image handling |
| https://github.com/microsoft/vscode/pull/332504 | `microsoft/vscode` | `code_only` | `typescript` | Enable Node.js system certificates by default |
| https://github.com/microsoft/vscode/pull/332517 | `microsoft/vscode` | `code_and_docs` | `typescript` | Add injected text component fixtures |
| https://github.com/microsoft/vscode/pull/332528 | `microsoft/vscode` | `code_only` | `typescript` | Modern UI: keep floating surfaces aligned across startup and layout changes |
| https://github.com/microsoft/vscode/pull/332521 | `microsoft/vscode` | `code_only` | `typescript` | [cherry-pick] Cache active session external changes for agent feedback scope checks |
| https://github.com/microsoft/vscode/pull/332496 | `microsoft/vscode` | `code_only` | `typescript` | chat: summarize the Agent Merge prompt as a widget |
| https://github.com/microsoft/vscode/pull/332520 | `microsoft/vscode` | `code_only` | `typescript` | Update Markdown editor to 0.0.2-84 |
| https://github.com/microsoft/vscode/pull/332495 | `microsoft/vscode` | `code_only` | `typescript` | sessions: share the session hover between the sessions list and chat pills |
| https://github.com/microsoft/vscode/pull/332269 | `microsoft/vscode` | `code_only` | `typescript` | Use Package Icon for Artifacts Pill |
| https://github.com/microsoft/vscode/pull/332343 | `microsoft/vscode` | `code_only` | `typescript` | sessions: show ChatGPT profile picture in the Agents account menu |
| https://github.com/microsoft/vscode/pull/332245 | `microsoft/vscode` | `code_only_tests_or_fixtures` | `typescript` | Re-enable Kerberos proxy smoke test on GitHub Actions |
| https://github.com/microsoft/vscode/pull/332266 | `microsoft/vscode` | `code_only` | `typescript` | [cherry-pick] Enable Chat Customizations prompt migration by default |
| https://github.com/microsoft/vscode/pull/332133 | `microsoft/vscode` | `code_only` | `typescript` | Track chat session type selection reasons |
| https://github.com/microsoft/vscode/pull/332457 | `microsoft/vscode` | `code_only` | `typescript` | Keep locally provisioned sessions out of the list until they are real |
| https://github.com/microsoft/vscode/pull/332489 | `microsoft/vscode` | `code_only` | `typescript` | build: include electron types in node modules cache |
| https://github.com/microsoft/vscode/pull/332456 | `microsoft/vscode` | `code_only` | `typescript` | Let agent host sessions tolerate hosts that differ from the client |
| https://github.com/microsoft/vscode/pull/332330 | `microsoft/vscode` | `code_only` | `typescript` | Modern UI: add compact density and connect the activity bar to the side bar |
| https://github.com/microsoft/vscode/pull/331833 | `microsoft/vscode` | `code_only` | `typescript` | chore: bump electron@42.9.3 |
| https://github.com/microsoft/vscode/pull/332455 | `microsoft/vscode` | `code_only` | `typescript` | Wait for complete sandbox credentials before connecting |
| https://github.com/microsoft/vscode/pull/332454 | `microsoft/vscode` | `code_only` | `typescript` | Give sandbox task creation a realistic timeout and diagnosable failures |
| https://github.com/microsoft/vscode/pull/332449 | `microsoft/vscode` | `code_only` | `typescript` | agentHost: retain recently used sessions |
| https://github.com/microsoft/vscode/pull/332453 | `microsoft/vscode` | `code_only` | `typescript` | Log AHP frames for the Web PubSub relay transport |
| https://github.com/microsoft/vscode/pull/332465 | `microsoft/vscode` | `code_only_tests_or_fixtures` | `typescript` | agentHost: Test lifecycle config path casing |
| https://github.com/microsoft/vscode/pull/332462 | `microsoft/vscode` | `code_only` | `typescript` | sessions: refine custom chat background surfaces |
| https://github.com/microsoft/vscode/pull/332466 | `microsoft/vscode` | `code_only_tests_or_fixtures` | `typescript` | Avoid loading vm in Electron renderer tests |
| https://github.com/microsoft/vscode/pull/318017 | `microsoft/vscode` | `code_only` | `typescript` | fix: handle 422 embeddings errors gracefully instead of throwing (fixes #318009) |
| https://github.com/microsoft/vscode/pull/332448 | `microsoft/vscode` | `code_only` | `typescript` | sessions: support Open Chat Agent keybinding |
| https://github.com/microsoft/vscode/pull/332451 | `microsoft/vscode` | `code_only` | `typescript` | [cherry-pick] github-authentication: prevent session hydration write loop |
| https://github.com/microsoft/vscode/pull/332450 | `microsoft/vscode` | `code_and_docs` | `typescript` | Add opt-in strict service registration |
| https://github.com/microsoft/vscode/pull/321799 | `microsoft/vscode` | `code_only` | `typescript` | fix: validate file stat size/mtime before SQLite bind in external ingest index (fixes #321794) |
| https://github.com/microsoft/vscode/pull/332447 | `microsoft/vscode` | `code_only` | `typescript` | github-authentication: prevent session hydration write loop |
| https://github.com/microsoft/vscode/pull/332445 | `microsoft/vscode` | `code_only` | `typescript` | inline chat: scope Agent Host permissions and fix its file context |
| https://github.com/microsoft/vscode/pull/332084 | `microsoft/vscode` | `code_and_docs` | `typescript` | Simplify Agent Host service construction |
| https://github.com/microsoft/vscode/pull/322383 | `microsoft/vscode` | `code_and_docs` | `typescript` | build: enforce agent SDK version pin lockstep in CI |
| https://github.com/microsoft/vscode/pull/323670 | `microsoft/vscode` | `code_only` | `typescript` | workbench: fix ObjectSettingCheckboxWidget memory leaky |
| https://github.com/microsoft/vscode/pull/323651 | `microsoft/vscode` | `code_only` | `typescript` | AHP: opt into SDK managed-settings self-fetch |
| https://github.com/microsoft/vscode/pull/323767 | `microsoft/vscode` | `code_only` | `typescript` | Fix bugs related to setting the right Chat model. (Fixes Issue #323765) |
| https://github.com/microsoft/vscode/pull/324341 | `microsoft/vscode` | `code_only` | `typescript` | Fix empty chat widget when opening an archived worktree session |
| https://github.com/microsoft/vscode/pull/325212 | `microsoft/vscode` | `code_only` | `typescript` | Propagate MCP App metadata eagerly for Copilot tool calls |
| https://github.com/microsoft/vscode/pull/325249 | `microsoft/vscode` | `code_and_docs` | `typescript` | sessions: use Worktree checkbox for isolation instead of dropdown |
| https://github.com/microsoft/vscode/pull/325247 | `microsoft/vscode` | `code_only` | `typescript` | AgentHost - pull in the latest protocol changes |
| https://github.com/microsoft/vscode/pull/325239 | `microsoft/vscode` | `code_only` | `typescript` | sessions: remember agent mode/approvals picks as new-session defaults |
| https://github.com/microsoft/vscode/pull/325238 | `microsoft/vscode` | `code_only` | `typescript` | MCP: preserve authorization server context on auth re-validation |
| https://github.com/microsoft/vscode/pull/325233 | `microsoft/vscode` | `code_only` | `typescript` | fix: remote server node_modules lookup |
| https://github.com/microsoft/vscode/pull/325226 | `microsoft/vscode` | `code_only` | `typescript` | Stop session/customizationsChanged log spam in agent host |
| https://github.com/microsoft/vscode/pull/325223 | `microsoft/vscode` | `code_only` | `typescript` | Add session provider picker to automations dialog |
| https://github.com/microsoft/vscode/pull/325222 | `microsoft/vscode` | `code_and_docs` | `typescript` | Add Agent Host debug logs analysis skill |
| https://github.com/microsoft/vscode/pull/325211 | `microsoft/vscode` | `code_only` | `typescript` | SessionTypePicker: Add optional folder source support |
| https://github.com/microsoft/vscode/pull/325207 | `microsoft/vscode` | `code_and_docs` | `typescript` | otel: correlate child spans with session id |
| https://github.com/microsoft/vscode/pull/325203 | `microsoft/vscode` | `code_only` | `typescript` | Make promos harness aware |
| https://github.com/microsoft/vscode/pull/325202 | `microsoft/vscode` | `code_only` | `typescript` | Voice: fix deferred responses not read on session switch |
| https://github.com/microsoft/vscode/pull/325200 | `microsoft/vscode` | `code_only` | `typescript` | Prevent duplicate model picker icons |
| https://github.com/microsoft/vscode/pull/325198 | `microsoft/vscode` | `code_only` | `typescript` | chat ux: collapse animations, thinking cleanup |
| https://github.com/microsoft/vscode/pull/325196 | `microsoft/vscode` | `code_only` | `typescript` | Improve Copilot Cloud Sessions error handling and messaging |
| https://github.com/microsoft/vscode/pull/325175 | `microsoft/vscode` | `code_only` | `typescript` | feat: use form_post for default flow |
| https://github.com/microsoft/vscode/pull/325129 | `microsoft/vscode` | `code_only` | `typescript` | Add telemetry for disallowed API proposal usage |
| https://github.com/microsoft/vscode/pull/325122 | `microsoft/vscode` | `code_and_docs` | `typescript` | sessions: move Create Pull Request bar to the editor tabs title |
| https://github.com/microsoft/vscode/pull/325374 | `microsoft/vscode` | `code_only` | `typescript` | Update "Worktree" label to "New Worktree" in session providers |
| https://github.com/microsoft/vscode/pull/325358 | `microsoft/vscode` | `code_only` | `typescript` | Rename agents.voice.textToSpeech to agents.voice.speakResponses |
| https://github.com/microsoft/vscode/pull/325351 | `microsoft/vscode` | `code_only` | `typescript` | Let focus settle before focusing the browser view |
| https://github.com/microsoft/vscode/pull/325347 | `microsoft/vscode` | `code_only` | `typescript` | fix: truncate Claude session customTitle label to bound RPC payload (fixes #322754) |
| https://github.com/microsoft/vscode/pull/325346 | `microsoft/vscode` | `code_only` | `typescript` | Don't let voice-controls init break the new-session picker render |
| https://github.com/microsoft/vscode/pull/325344 | `microsoft/vscode` | `code_only` | `typescript` | MCP: fix infinite sign-in loop for servers that grant scopes but advertise none |
| https://github.com/microsoft/vscode/pull/325343 | `microsoft/vscode` | `code_only_tests_or_fixtures` | `typescript` | Skip flaky test (see #325266) |
| https://github.com/microsoft/vscode/pull/325337 | `microsoft/vscode` | `code_only` | `typescript` | Add support for detecting latest sdk canary versions |
| https://github.com/microsoft/vscode/pull/325332 | `microsoft/vscode` | `code_and_docs` | `typescript` | sessions: model docked (Changes/Files) editors as DockedEditorInput |
| https://github.com/microsoft/vscode/pull/325321 | `microsoft/vscode` | `code_and_docs` | `typescript` | sessions: reveal Files detail when the empty Files editor is opened |
| https://github.com/microsoft/vscode/pull/325320 | `microsoft/vscode` | `code_only` | `typescript` | Remove agents.voice.turn.autoEndMode; derive auto-end from silenceMs/stopPhrases |
| https://github.com/microsoft/vscode/pull/325316 | `microsoft/vscode` | `code_only` | `typescript` | Refactor copilot session launcher for cache handling |
| https://github.com/microsoft/vscode/pull/325314 | `microsoft/vscode` | `code_and_docs` | `typescript` | sessions: add Open Pull Request to session context menu |
| https://github.com/microsoft/vscode/pull/325309 | `microsoft/vscode` | `code_and_docs` | `typescript` | sessions: single source of truth for single-pane layout enablement |
| https://github.com/microsoft/vscode/pull/325307 | `microsoft/vscode` | `code_only` | `typescript` | Only show breadcrumb editor picker for default-capable editors (which excludes hex editor) |
| https://github.com/microsoft/vscode/pull/325304 | `microsoft/vscode` | `code_only` | `typescript` | Support 0% discounts just boosting the model rather than discounting it |
| https://github.com/microsoft/vscode/pull/325303 | `microsoft/vscode` | `code_and_docs` | `typescript` | sessions: bridge extension editor/title actions into single-pane editor menu |
| https://github.com/microsoft/vscode/pull/325302 | `microsoft/vscode` | `code_and_docs` | `typescript` | Harden automation run lifecycle |
| https://github.com/microsoft/vscode/pull/325301 | `microsoft/vscode` | `code_and_docs` | `typescript` | sessions: default single-pane side pane to 60% and persist its width reliably |
| https://github.com/microsoft/vscode/pull/325300 | `microsoft/vscode` | `code_only` | `typescript` | sessions: fix editor tabs bleeding through sticky add-tab button |
| https://github.com/microsoft/vscode/pull/325299 | `microsoft/vscode` | `code_only` | `typescript` | Remove fragile chat notification model switching |
| https://github.com/microsoft/vscode/pull/325298 | `microsoft/vscode` | `code_only` | `typescript` | sessions: remember Changes editor view state across scenarios |
| https://github.com/microsoft/vscode/pull/325295 | `microsoft/vscode` | `code_and_docs` | `typescript` | Track automation runs until sessions complete |
| https://github.com/microsoft/vscode/pull/325296 | `microsoft/vscode` | `code_and_docs` | `typescript` | Fix opening automation history sessions |
| https://github.com/microsoft/vscode/pull/325294 | `microsoft/vscode` | `code_only` | `typescript` | Record scheduled automation runs atomically |
| https://github.com/microsoft/vscode/pull/325293 | `microsoft/vscode` | `code_only` | `typescript` | Adds "Reopen with" submenu to editor toolbar |
| https://github.com/microsoft/vscode/pull/325284 | `microsoft/vscode` | `code_only_tests_or_fixtures` | `typescript` | Skip flaky `reopening a session keeps sub-agent messages out of the parent transcript (replay path)` |
| https://github.com/microsoft/vscode/pull/325283 | `microsoft/vscode` | `code_only` | `typescript` | sessions: toggle Changes diff view via the renderSideBySide setting |
| https://github.com/microsoft/vscode/pull/325278 | `microsoft/vscode` | `code_only` | `typescript` | Fix inline suggestion false negatives via canonical cursor-edit rebasing |
| https://github.com/microsoft/vscode/pull/325276 | `microsoft/vscode` | `code_only` | `typescript` | Fix NES feedback context in issue reporter |
| https://github.com/microsoft/vscode/pull/325275 | `microsoft/vscode` | `code_only` | `typescript` | Fix windowed token cache eviction |
| https://github.com/microsoft/vscode/pull/325272 | `microsoft/vscode` | `code_only` | `typescript` | NES: Correct line numbering for prompt context |
| https://github.com/microsoft/vscode/pull/325258 | `microsoft/vscode` | `code_only` | `typescript` | Add experiment for api proposals |
| https://github.com/microsoft/vscode/pull/325254 | `microsoft/vscode` | `code_only` | `typescript` | AgentHost - pull in the correct protocol version |
| https://github.com/microsoft/vscode/pull/332440 | `microsoft/vscode` | `code_only` | `typescript` | chat: format terminal chat commands as code blocks |
| https://github.com/microsoft/vscode/pull/332435 | `microsoft/vscode` | `code_only` | `typescript` | Add customizable Agents chat backgrounds |
| https://github.com/microsoft/vscode/pull/332209 | `microsoft/vscode` | `code_only` | `typescript` | Persist session archiving without restoring the session |
| https://github.com/microsoft/vscode/pull/332427 | `microsoft/vscode` | `code_and_docs` | `typescript` | agentHost: move side chat behavior into a contribution |
| https://github.com/microsoft/vscode/pull/332415 | `microsoft/vscode` | `code_and_docs` | `typescript` | Launch skill: Focus chat input reliably |
| https://github.com/microsoft/vscode/pull/332426 | `microsoft/vscode` | `code_only` | `typescript` | Report the message origin kind in agent host message telemetry |
| https://github.com/microsoft/vscode/pull/332425 | `microsoft/vscode` | `code_and_docs` | `typescript` | agentHost: expose open links from list sessions |
| https://github.com/microsoft/vscode/pull/332411 | `microsoft/vscode` | `code_only` | `typescript` | Fix incorrect units used in reset date from SDK |
| https://github.com/microsoft/vscode/pull/332412 | `microsoft/vscode` | `code_and_docs` | `typescript` | [cherry-pick] sessions: Preserve Details visibility while resizing |
| https://github.com/microsoft/vscode/pull/332414 | `microsoft/vscode` | `code_only` | `typescript` | [cherry-pick] Agent Host: apply multi-root capability change to open drafts without a reload |
| https://github.com/microsoft/vscode/pull/332413 | `microsoft/vscode` | `code_only` | `typescript` | [cherry-pick] Enhance ChatModeService: Sort custom modes alphabetically by label |
| https://github.com/microsoft/vscode/pull/332408 | `microsoft/vscode` | `code_only` | `typescript` | Fix extension host OOM when listing Copilot CLI sessions |
| https://github.com/microsoft/vscode/pull/332403 | `microsoft/vscode` | `code_only` | `typescript` | Agent Host: apply multi-root capability change to open drafts without a reload |
| https://github.com/microsoft/vscode/pull/332401 | `microsoft/vscode` | `code_only` | `typescript` | Enhance ChatModeService: Sort custom modes alphabetically by label |
| https://github.com/microsoft/vscode/pull/332405 | `microsoft/vscode` | `code_and_docs` | `typescript` | sessions: Preserve Details visibility while resizing |
| https://github.com/microsoft/vscode/pull/332398 | `microsoft/vscode` | `code_only` | `typescript` | [cherry-pick] Implement overlap-aware sticky-scroll ellipsis positioning |
| https://github.com/microsoft/vscode/pull/332389 | `microsoft/vscode` | `code_only` | `typescript` | [cherry-pick] Fix pet run input visibility issue and enhance regression tests |
| https://github.com/microsoft/vscode/pull/332382 | `microsoft/vscode` | `code_only` | `typescript` | Implement overlap-aware sticky-scroll ellipsis positioning |
| https://github.com/microsoft/vscode/pull/332229 | `microsoft/vscode` | `code_only` | `typescript` | Agent Host: wait for Copilot debug journal |
| https://github.com/microsoft/vscode/pull/332195 | `microsoft/vscode` | `code_only` | `typescript` | Default external sessions to recent |
| https://github.com/microsoft/vscode/pull/332175 | `microsoft/vscode` | `code_only` | `typescript` | Restore persisted platform root config on agent host startup |
| https://github.com/microsoft/vscode/pull/332174 | `microsoft/vscode` | `code_only` | `typescript` | sessions: hide external Recent sessions superseded by newer local ones |
| https://github.com/microsoft/vscode/pull/331181 | `microsoft/vscode` | `code_only` | `typescript` | Add recent external sessions filter |
| https://github.com/microsoft/vscode/pull/332368 | `microsoft/vscode` | `code_only` | `typescript` | Harden content exclusion failrue condition |
| https://github.com/microsoft/vscode/pull/332029 | `microsoft/vscode` | `code_only` | `typescript` | sessions: Remove bracket navigation keybindings |
| https://github.com/microsoft/vscode/pull/332381 | `microsoft/vscode` | `code_only` | `typescript` | Fix pet run input visibility issue and enhance regression tests |
| https://github.com/microsoft/vscode/pull/332375 | `microsoft/vscode` | `code_only` | `typescript` | Fix Copilot client cold-start and Kerberos proxy handling |
| https://github.com/microsoft/vscode/pull/332227 | `microsoft/vscode` | `code_only` | `typescript` | agentHost: Avoid spurious resource and config errors |
| https://github.com/microsoft/vscode/pull/332271 | `microsoft/vscode` | `code_only` | `typescript` | chat: clear progress when session provider is disposed |
| https://github.com/microsoft/vscode/pull/332332 | `microsoft/vscode` | `code_only` | `typescript` | fix: memory leak in explorer viewer |
| https://github.com/microsoft/vscode/pull/332374 | `microsoft/vscode` | `code_and_docs` | `typescript` | [cherry-pick] sessions: Show Changes view for new sessions |
| https://github.com/microsoft/vscode/pull/331867 | `microsoft/vscode` | `code_and_docs` | `typescript` | chore: fix build for ADO pipeline runs |
| https://github.com/microsoft/vscode/pull/332218 | `microsoft/vscode` | `code_only` | `typescript` | agentHost: add tool invocation telemetry |
| https://github.com/microsoft/vscode/pull/332365 | `microsoft/vscode` | `code_and_docs` | `typescript` | sessions: Show Changes view for new sessions |
| https://github.com/microsoft/vscode/pull/331975 | `microsoft/vscode` | `code_only` | `typescript` | Refactor inline survey and ask question tool CSS into shared components |
| https://github.com/microsoft/vscode/pull/332350 | `microsoft/vscode` | `code_only` | `typescript` | [cherry-pick] sessions: Preserve side pane size across custom views |
| https://github.com/microsoft/vscode/pull/332316 | `microsoft/vscode` | `code_only` | `typescript` | [cherry-pick] nes: add optimized PatchBased02 prompt strategy |
| https://github.com/microsoft/vscode/pull/332312 | `microsoft/vscode` | `code_only` | `typescript` | [cherry-pick] chat: don't prompt for workspace trust on internal agent-session folders |
| https://github.com/microsoft/vscode/pull/332103 | `microsoft/vscode` | `code_only_tests_or_fixtures` | `typescript` | Modern UI: Fix CSS specificity for tab action fading |
| https://github.com/microsoft/vscode/pull/332337 | `microsoft/vscode` | `code_only` | `typescript` | sessions: Preserve side pane size across custom views |
| https://github.com/microsoft/vscode/pull/332041 | `microsoft/vscode` | `code_only` | `typescript` | chore: bump gulp-electron |
| https://github.com/microsoft/vscode/pull/332306 | `microsoft/vscode` | `code_only` | `typescript` | agent host: normalize empty Kerberos proxy SPN to avoid spurious restart |
| https://github.com/microsoft/vscode/pull/332322 | `microsoft/vscode` | `code_only` | `typescript` | chat: Avoid duplicate generated image hover previews |
| https://github.com/microsoft/vscode/pull/332297 | `microsoft/vscode` | `code_only` | `typescript` | chat: keep an agent turn's changes summary from flickering |
| https://github.com/microsoft/vscode/pull/296712 | `microsoft/vscode` | `code_only` | `typescript` | Normalize end of line cursor move operation |
| https://github.com/microsoft/vscode/pull/332018 | `microsoft/vscode` | `code_only` | `typescript` | nes: add optimized PatchBased02 prompt strategy |
| https://github.com/microsoft/vscode/pull/332280 | `microsoft/vscode` | `code_only` | `typescript` | chat: don't prompt for workspace trust on internal agent-session folders |
| https://github.com/microsoft/vscode/pull/332288 | `microsoft/vscode` | `code_only` | `typescript` | [cherry-pick] sessions: Shorten session action labels |
| https://github.com/microsoft/vscode/pull/332256 | `microsoft/vscode` | `code_only` | `typescript` | agent host: self-heal Copilot client cold-start config-changed abort |
| https://github.com/microsoft/vscode/pull/332284 | `microsoft/vscode` | `code_only` | `typescript` | sessions: Shorten session action labels |
| https://github.com/microsoft/vscode/pull/332262 | `microsoft/vscode` | `code_only` | `typescript` | Enable Chat Customizations prompt migration by default |
| https://github.com/microsoft/vscode/pull/331938 | `microsoft/vscode` | `code_only_tests_or_fixtures` | `typescript` | Modern UI: Add function to create editor tab labels and corresponding test for foreground colors |
| https://github.com/microsoft/vscode/pull/332252 | `microsoft/vscode` | `code_only` | `typescript` | [cherry-pick] Add response headers for remote resources |
| https://github.com/microsoft/vscode/pull/332253 | `microsoft/vscode` | `code_only` | `typescript` | Avoid false listener leak warnings for many inputs |
| https://github.com/microsoft/onnxruntime/pull/32262 | `microsoft/onnxruntime` | `code_only_tests_or_fixtures` | `python` | Harden head-size-256 paged XQA coverage |
| https://github.com/microsoft/onnxruntime/pull/32214 | `microsoft/onnxruntime` | `code_and_docs` | `python` | Run wgsl_template Python tests in CI |
| https://github.com/microsoft/onnxruntime/pull/32068 | `microsoft/onnxruntime` | `code_only` | `python` | [MLAS] Reject Arm® KleidiAI™ Q4 prepack with dynamic scales |
| https://github.com/microsoft/onnxruntime/pull/31720 | `microsoft/onnxruntime` | `code_only` | `python` | [MLAS] Refactor QNBit KleidiAI integration into dedicated layer |
| https://github.com/microsoft/onnxruntime/pull/31643 | `microsoft/onnxruntime` | `code_only` | `python` | Validate MatMulNBits 8-bit g_idx bounds on CUDA |
| https://github.com/microsoft/onnxruntime/pull/29906 | `microsoft/onnxruntime` | `code_only` | `python` | Upgrade Protobuf to v33.6 |
| https://github.com/microsoft/onnxruntime/pull/32208 | `microsoft/onnxruntime` | `code_only` | `python` | pin review dog |
| https://github.com/microsoft/onnxruntime/pull/29726 | `microsoft/onnxruntime` | `code_only` | `python` | Extend memory importer with host pointer support |
| https://github.com/microsoft/onnxruntime/pull/31674 | `microsoft/onnxruntime` | `code_and_docs` | `python` | [MLAS] Add an AVX-512 fused kernel for LinearAttention |
| https://github.com/microsoft/onnxruntime/pull/29892 | `microsoft/onnxruntime` | `code_only` | `python` | Fix LinearAttention output shape inference for standard GQA (q > kv) |
| https://github.com/microsoft/onnxruntime/pull/32168 | `microsoft/onnxruntime` | `code_and_docs` | `python` | [CUDA] Add VarlenCausalConvWithState for continuous batching |
| https://github.com/microsoft/onnxruntime/pull/32221 | `microsoft/onnxruntime` | `code_only` | `python` | Support LoRA adapters with plugin EP allocators |
| https://github.com/microsoft/onnxruntime/pull/32229 | `microsoft/onnxruntime` | `code_only` | `python` | [CUDA] Extend paged XQA decode to head size 256 |
| https://github.com/microsoft/onnxruntime/pull/32193 | `microsoft/onnxruntime` | `code_and_docs` | `python` | Move ort-release-notes skill to new .github/skills location. |
| https://github.com/microsoft/onnxruntime/pull/32116 | `microsoft/onnxruntime` | `code_only` | `python` | [WebGPU] Supply fused activation parameters to Conv/MatMul as uniforms |
| https://github.com/microsoft/onnxruntime/pull/18501 | `microsoft/onnxruntime` | `code_only` | `python` | Update setup.py: replace libcudart.so.12.0 with libcudart.so.12 |
| https://github.com/microsoft/onnxruntime/pull/29820 | `microsoft/onnxruntime` | `code_only` | `python` | [WebGPU] Scale Dawn pipeline compilation workers with CPU count |
| https://github.com/microsoft/onnxruntime/pull/32210 | `microsoft/onnxruntime` | `code_only` | `python` | Fix C API docs Doxygen download |
| https://github.com/microsoft/onnxruntime/pull/32178 | `microsoft/onnxruntime` | `code_only` | `python` | [MLAS] Add a NEON fused kernel for LinearAttention |
| https://github.com/microsoft/onnxruntime/pull/32048 | `microsoft/onnxruntime` | `code_only` | `python` | [WebGPU] Make MatMulNaiveProgram's pipeline cache key cover everything it bakes into WGSL |
| https://github.com/microsoft/onnxruntime/pull/32188 | `microsoft/onnxruntime` | `code_only` | `python` | [WebGPU EP] 0.3.0 cherry-picks round 2 |
| https://github.com/microsoft/onnxruntime/pull/32180 | `microsoft/onnxruntime` | `code_only` | `python` | Fix homepage carousel keyboard accessibility |
| https://github.com/microsoft/onnxruntime/pull/32190 | `microsoft/onnxruntime` | `code_and_docs` | `python` | Resolve possible onnx CVE in python docs |
| https://github.com/microsoft/onnxruntime/pull/31958 | `microsoft/onnxruntime` | `code_only` | `python` | [MLAS] AVX-512 16-wide Erf kernel and NCHWc reorder transpose for MobileClip-S0 model |
| https://github.com/microsoft/onnxruntime/pull/31727 | `microsoft/onnxruntime` | `code_and_docs` | `python` | [WebGPU] Optimized PagedAttention implementation (2/n) |
| https://github.com/microsoft/onnxruntime/pull/31957 | `microsoft/onnxruntime` | `code_only` | `python` | [MLAS] Hardswish Fusion implement for Mobilenetv3 models |
| https://github.com/microsoft/onnxruntime/pull/32157 | `microsoft/onnxruntime` | `code_only` | `python` | Harden Crop operator validation |
| https://github.com/microsoft/onnxruntime/pull/29461 | `microsoft/onnxruntime` | `code_only` | `python` | Validate per-element split sizes on the input-tensor path to prevent OOB read |
| https://github.com/microsoft/onnxruntime/pull/32041 | `microsoft/onnxruntime` | `code_only` | `python` | Retain Python async run resources |
| https://github.com/microsoft/onnxruntime/pull/32034 | `microsoft/onnxruntime` | `code_only` | `python` | Validate ScatterND index depth |
| https://github.com/microsoft/onnxruntime/pull/32144 | `microsoft/onnxruntime` | `code_and_docs` | `python` | Validate QEmbed segment inputs |
| https://github.com/microsoft/onnxruntime/pull/32156 | `microsoft/onnxruntime` | `code_only` | `python` | Validate empty reduction axes |
| https://github.com/microsoft/onnxruntime/pull/32160 | `microsoft/onnxruntime` | `code_only` | `python` | Validate Conv bias size |
| https://github.com/microsoft/onnxruntime/pull/32161 | `microsoft/onnxruntime` | `code_only` | `python` | Reject scalar Normalizer inputs |
| https://github.com/microsoft/onnxruntime/pull/32143 | `microsoft/onnxruntime` | `code_only` | `python` | Skip overridable initializer fusion |
| https://github.com/microsoft/onnxruntime/pull/32138 | `microsoft/onnxruntime` | `code_only` | `python` | Handle empty initializer axis scaling |
| https://github.com/microsoft/onnxruntime/pull/32135 | `microsoft/onnxruntime` | `code_only` | `python` | Canonicalize external data locations |
| https://github.com/microsoft/onnxruntime/pull/32012 | `microsoft/onnxruntime` | `code_only` | `python` | Avoid overflow in CPU TensorScatter indices |
| https://github.com/microsoft/onnxruntime/pull/32063 | `microsoft/onnxruntime` | `code_only` | `python` | [WebGPU] Zero-initialize writable device allocator buffers |
| https://github.com/microsoft/onnxruntime/pull/32057 | `microsoft/onnxruntime` | `code_only_tests_or_fixtures` | `python` | Fix #31573, prevent ARM64 SymmQgemm int16 overflow |
| https://github.com/microsoft/onnxruntime/pull/32053 | `microsoft/onnxruntime` | `code_only` | `python` | [WebGPU] Enable GeluFusion and BiasGeluFusion for the WebGPU EP |
| https://github.com/microsoft/onnxruntime/pull/32165 | `microsoft/onnxruntime` | `code_only` | `python` | [Build] Update cuda plugin linux aarch64 parallel to 8 |
| https://github.com/microsoft/onnxruntime/pull/32095 | `microsoft/onnxruntime` | `code_only` | `python` | Use commit timestamps for plugin EP dev versions |
| https://github.com/microsoft/onnxruntime/pull/32111 | `microsoft/onnxruntime` | `code_only` | `python` | [CUDA] upgrade cutlass 4.7 and cudnn-frontend 1.27 |
| https://github.com/microsoft/onnxruntime/pull/32106 | `microsoft/onnxruntime` | `code_and_docs` | `python` | Add more kernels for Qwen-3.5 ops |
| https://github.com/microsoft/onnxruntime/pull/32128 | `microsoft/onnxruntime` | `code_and_docs` | `python` | [CUDA] Vectorize the NVFP4 weight dequantization for prefill |
| https://github.com/microsoft/onnxruntime/pull/32129 | `microsoft/onnxruntime` | `code_and_docs` | `python` | [CUDA] Bound the FP8 weight dequant scratch by tiling over N |
| https://github.com/microsoft/onnxruntime/pull/32102 | `microsoft/onnxruntime` | `code_and_docs` | `python` | Enable split-KV for paged FlashAttention decode |
| https://github.com/microsoft/onnxruntime/pull/32088 | `microsoft/onnxruntime` | `code_only` | `python` | [WebGPU EP] 0.3.0 cherry-picks round 1 |
| https://github.com/microsoft/onnxruntime/pull/31660 | `microsoft/onnxruntime` | `code_only` | `python` | Improve MLAS NCHWc conv thread utilization via cost-weighted work par… |
| https://github.com/microsoft/onnxruntime/pull/32098 | `microsoft/onnxruntime` | `code_only` | `python` | ORT 1.28.1 Cherry Picks, pt. 2 |
| https://github.com/microsoft/onnxruntime/pull/32127 | `microsoft/onnxruntime` | `code_and_docs` | `python` | Use native block tables for 128-token XQA pages |
| https://github.com/microsoft/onnxruntime/pull/32056 | `microsoft/onnxruntime` | `code_only` | `python` | Implement WebGPU subgroup-size-control infrastructure |
| https://github.com/microsoft/onnxruntime/pull/32077 | `microsoft/onnxruntime` | `code_only` | `python` | Fix/ort runtime optimization trust |
| https://github.com/microsoft/onnxruntime/pull/32076 | `microsoft/onnxruntime` | `code_only` | `python` | Fix/pool negative pad validation |
| https://github.com/microsoft/onnxruntime/pull/32108 | `microsoft/onnxruntime` | `code_and_docs` | `python` | Add group size 6 support to paged XQA |
| https://github.com/microsoft/onnxruntime/pull/32092 | `microsoft/onnxruntime` | `code_only` | `python` | [CUDA] Parallelize ArgMax/ArgMin over wide last axes |
| https://github.com/microsoft/onnxruntime/pull/32099 | `microsoft/onnxruntime` | `code_only` | `python` | Improve PagedAttention dispatch diagnostics |
| https://github.com/microsoft/onnxruntime/pull/32096 | `microsoft/onnxruntime` | `code_and_docs` | `python` | [CUDA] Enable FP4 QMoE by default |
| https://github.com/microsoft/onnxruntime/pull/32097 | `microsoft/onnxruntime` | `code_only` | `python` | Bound QMoE workspace with configurable row tiling |
| https://github.com/microsoft/onnxruntime/pull/31704 | `microsoft/onnxruntime` | `code_and_docs` | `python` | Support bidirectional GroupQueryAttention on CPU and CUDA |
| https://github.com/microsoft/onnxruntime/pull/32090 | `microsoft/onnxruntime` | `code_only` | `python` | Enable WebGPU CI for WebGPU plugin EP release branches |
| https://github.com/microsoft/onnxruntime/pull/32078 | `microsoft/onnxruntime` | `code_only` | `python` | Validate generation subgraph shapes |
| https://github.com/microsoft/onnxruntime/pull/32030 | `microsoft/onnxruntime` | `code_only` | `python` | Validate CUDA GatherElements count |
| https://github.com/microsoft/onnxruntime/pull/32042 | `microsoft/onnxruntime` | `code_only` | `python` | Validate in-memory initializer references |
| https://github.com/microsoft/onnxruntime/pull/32051 | `microsoft/onnxruntime` | `code_only` | `python` | Fix/qdq optional zero point input |
| https://github.com/microsoft/onnxruntime/pull/32032 | `microsoft/onnxruntime` | `code_only` | `python` | Validate MatMulFpQ4 shape inputs |
| https://github.com/microsoft/onnxruntime/pull/32029 | `microsoft/onnxruntime` | `code_only` | `python` | Validate CUDA QDQ element counts |
| https://github.com/microsoft/onnxruntime/pull/32018 | `microsoft/onnxruntime` | `code_only` | `python` | Validate GQA fusion projection shapes |
| https://github.com/microsoft/onnxruntime/pull/31971 | `microsoft/onnxruntime` | `code_only` | `python` | [WebGPU] Add robustness provider option |
| https://github.com/microsoft/onnxruntime/pull/31714 | `microsoft/onnxruntime` | `code_only` | `python` | [WebGPU] Add Gather int64 support and make kernel version numbers function params |
| https://github.com/microsoft/onnxruntime/pull/32016 | `microsoft/onnxruntime` | `code_only` | `python` | Validate FastGelu fusion scale node |
| https://github.com/microsoft/onnxruntime/pull/31989 | `microsoft/onnxruntime` | `code_only` | `python` | [CUDA] Update cuda archs in packaging pipelines |
| https://github.com/microsoft/onnxruntime/pull/32067 | `microsoft/onnxruntime` | `code_only` | `python` | [WebNN EP] Fix bug introduced by output rank validation |
| https://github.com/microsoft/onnxruntime/pull/32072 | `microsoft/onnxruntime` | `code_only_tests_or_fixtures` | `python` | [Build] Update cuda plugin package test pipeline |
| https://github.com/microsoft/onnxruntime/pull/31477 | `microsoft/onnxruntime` | `code_only_tests_or_fixtures` | `python` | [CUDA] Fix Abs signed zero handling |
| https://github.com/microsoft/onnxruntime/pull/31648 | `microsoft/onnxruntime` | `code_only` | `python` | Harden contrib CPU int narrowing for attention attrs |
| https://github.com/microsoft/onnxruntime/pull/32035 | `microsoft/onnxruntime` | `code_only` | `python` | Validate Rust tensor element types |
| https://github.com/microsoft/onnxruntime/pull/32033 | `microsoft/onnxruntime` | `code_only` | `python` | Serialize CPU ScatterND string updates |
| https://github.com/microsoft/onnxruntime/pull/32031 | `microsoft/onnxruntime` | `code_only` | `python` | Validate TreeEnsemble v5 node references |
| https://github.com/microsoft/onnxruntime/pull/32037 | `microsoft/onnxruntime` | `code_only` | `python` | Fix Whisper encoder input diagnostic |
| https://github.com/microsoft/onnxruntime/pull/32040 | `microsoft/onnxruntime` | `code_only` | `python` | Fix prepacked weight reference lifetime |
| https://github.com/microsoft/onnxruntime/pull/32070 | `microsoft/onnxruntime` | `code_only` | `python` | Add BTI support to MLAS AArch64 assembly |
| https://github.com/microsoft/onnxruntime/pull/32015 | `microsoft/onnxruntime` | `code_only` | `python` | Pin C# RunAsync arguments until completion |
| https://github.com/microsoft/onnxruntime/pull/32045 | `microsoft/onnxruntime` | `code_only` | `python` | Extract Rust string tensor outputs safely |
| https://github.com/microsoft/onnxruntime/pull/32043 | `microsoft/onnxruntime` | `code_only` | `python` | Bound TreeEnsemble subtree comparison |
| https://github.com/microsoft/onnxruntime/pull/32044 | `microsoft/onnxruntime` | `code_only` | `python` | Validate Slice starts rank in transpose optimizer |
| https://github.com/microsoft/onnxruntime/pull/32011 | `microsoft/onnxruntime` | `code_only` | `python` | Reject non-finite CPU RoiAlign coordinates |
| https://github.com/microsoft/onnxruntime/pull/32046 | `microsoft/onnxruntime` | `code_only` | `python` | Fix/winml image dimension overflow |
| https://github.com/microsoft/onnxruntime/pull/31996 | `microsoft/onnxruntime` | `code_only` | `python` | Compute SparseAttention CUDA buffer sizes and offsets in size_t |
| https://github.com/microsoft/onnxruntime/pull/31994 | `microsoft/onnxruntime` | `code_only` | `python` | Bound sequence_token_count in CUDA RemovePadding |
| https://github.com/microsoft/onnxruntime/pull/31968 | `microsoft/onnxruntime` | `code_only` | `python` | Fix CUDA MHA shared-cache scratch lifetime |
| https://github.com/microsoft/onnxruntime/pull/31678 | `microsoft/onnxruntime` | `code_only` | `python` | Add upper bound validation for DQ block_size in MatMulNBits fusion |
| https://github.com/microsoft/onnxruntime/pull/32007 | `microsoft/onnxruntime` | `code_only` | `python` | Validate MLAS blockwise QDQ index ranges |
| https://github.com/microsoft/onnxruntime/pull/32013 | `microsoft/onnxruntime` | `code_only` | `python` | Handle extreme diagonal values in CPU Trilu |
| https://github.com/microsoft/onnxruntime/pull/32014 | `microsoft/onnxruntime` | `code_only_tests_or_fixtures` | `python` | Validate CUDA NMS mask size |
| https://github.com/microsoft/onnxruntime/pull/32000 | `microsoft/onnxruntime` | `code_only` | `python` | Narrow active_sessions_mutex_ scope around ETW callback registration |
| https://github.com/microsoft/onnxruntime/pull/31999 | `microsoft/onnxruntime` | `code_only` | `python` | Validate kernel_shape and output_padding lengths in DML kernel setup |
| https://github.com/microsoft/onnxruntime/pull/32019 | `microsoft/onnxruntime` | `code_only` | `python` | Fix NodeAttrHelper string default lifetime |
| https://github.com/microsoft/onnxruntime/pull/32008 | `microsoft/onnxruntime` | `code_only` | `python` | Use int64 loop counters in CPU Compress |
| https://github.com/microsoft/onnxruntime/pull/32010 | `microsoft/onnxruntime` | `code_only` | `python` | Use checked rounding for BFC arena allocations |
| https://github.com/microsoft/onnxruntime/pull/32002 | `microsoft/onnxruntime` | `code_only` | `python` | Require ImageScaler bias to have one entry per channel |
| https://github.com/microsoft/onnxruntime/pull/31997 | `microsoft/onnxruntime` | `code_only_tests_or_fixtures` | `python` | Handle zero-sized outputs in CUDA random generator kernels |
| https://github.com/microsoft/onnxruntime/pull/32020 | `microsoft/onnxruntime` | `code_only` | `python` | Handle empty CPU LpNormalization inputs |
| https://github.com/microsoft/onnxruntime/pull/32009 | `microsoft/onnxruntime` | `code_only` | `python` | Use dynamic shape storage in BeamSearch ExpandBuffer |
| https://github.com/microsoft/onnxruntime/pull/31478 | `microsoft/onnxruntime` | `code_only` | `python` | [CUDA] MatMul: add an opt-in split-K GEMV for small-N fp16 shapes |
| https://github.com/microsoft/onnxruntime/pull/32005 | `microsoft/onnxruntime` | `code_only` | `python` | Use authenticated package feeds in packaging pipelines |
| https://github.com/microsoft/onnxruntime/pull/31703 | `microsoft/onnxruntime` | `code_only` | `python` | [WebGPU] Optimize MatMulNBits wide-tile with subgroup shuffle |
| https://github.com/microsoft/onnxruntime/pull/31966 | `microsoft/onnxruntime` | `code_and_docs` | `python` | ORT 1.28.1 Cherry Picks |
| https://github.com/microsoft/onnxruntime/pull/31708 | `microsoft/onnxruntime` | `code_only` | `python` | [WebNN EP] Add output rank validation |
| https://github.com/microsoft/onnxruntime/pull/32021 | `microsoft/onnxruntime` | `code_only` | `python` | Update cuda plugin pipelines |
| https://github.com/microsoft/onnxruntime/pull/32006 | `microsoft/onnxruntime` | `code_only` | `python` | Filter display adapters that are using the Microsoft Basic Render Driver |
| https://github.com/microsoft/onnxruntime/pull/31698 | `microsoft/onnxruntime` | `code_only` | `python` | Handle zero-element input/bias in BiasGelu and FastGelu as a no-op |
| https://github.com/microsoft/onnxruntime/pull/31687 | `microsoft/onnxruntime` | `code_only` | `python` | [Test] Enable CUDA coverage for shared PagedAttention contrib-op tests via cache aliasing harness |
| https://github.com/microsoft/onnxruntime/pull/31992 | `microsoft/onnxruntime` | `code_only` | `python` | [CUDA] Update cuda archs in packaging pipelines |
| https://github.com/microsoft/onnxruntime/pull/31701 | `microsoft/onnxruntime` | `code_only` | `python` | Validate input rank/size for BifurcationDetector before indexing |
| https://github.com/microsoft/onnxruntime/pull/31670 | `microsoft/onnxruntime` | `code_only` | `python` | Guard three graph-optimizer passes against unbounded model-supplied indices |
| https://github.com/microsoft/onnxruntime/pull/31682 | `microsoft/onnxruntime` | `code_only` | `python` | Allowlist safe LoRA adapter parameter data types |
| https://github.com/microsoft/onnxruntime/pull/31972 | `microsoft/onnxruntime` | `code_and_docs` | `python` | Bump ORT Version to 1.30 |
| https://github.com/microsoft/onnxruntime/pull/31835 | `microsoft/onnxruntime` | `code_and_docs` | `python` | [CUDA] Add GatedAdd contrib operator |
| https://github.com/microsoft/onnxruntime/pull/31676 | `microsoft/onnxruntime` | `code_only` | `python` | Validate SkipLayerNorm prepacked input shapes |
| https://github.com/microsoft/onnxruntime/pull/31636 | `microsoft/onnxruntime` | `code_only` | `python` | Validate whisper beginning_timestamp_token_id bounds |
| https://github.com/microsoft/onnxruntime/pull/31675 | `microsoft/onnxruntime` | `code_only` | `python` | Handle RNN activation parameters safely |
| https://github.com/microsoft/onnxruntime/pull/31644 | `microsoft/onnxruntime` | `code_only_tests_or_fixtures` | `python` | Harden CUDA fp16 transpose index math against int overflow |
| https://github.com/microsoft/onnxruntime/pull/31684 | `microsoft/onnxruntime` | `code_only` | `python` | Validate QLinearConv bias size against output channels |
| https://github.com/microsoft/onnxruntime/pull/31649 | `microsoft/onnxruntime` | `code_only` | `python` | Fix TfIdfVectorizer weight indexing semantics |
| https://github.com/microsoft/onnxruntime/pull/31671 | `microsoft/onnxruntime` | `code_only` | `python` | Validate FeatureVectorizer batch sizes |
| https://github.com/microsoft/onnxruntime/pull/31976 | `microsoft/onnxruntime` | `code_only` | `python` | [WebGPU] Add MRotaryEmbedding support |
| https://github.com/microsoft/onnxruntime/pull/31982 | `microsoft/onnxruntime` | `code_only` | `python` | Fix LinearAttention on GPUs with limited shared memory |
| https://github.com/microsoft/onnxruntime/pull/31699 | `microsoft/onnxruntime` | `code_and_docs` | `python` | [WebGPU plugin EP] Update Python package test to only pass one WebGPU EP device |
| https://github.com/microsoft/onnxruntime/pull/31645 | `microsoft/onnxruntime` | `code_only_tests_or_fixtures` | `python` | Validate GatherBlockQuantized CUDA indices bounds |
| https://github.com/microsoft/onnxruntime/pull/31728 | `microsoft/onnxruntime` | `code_and_docs` | `python` | Add fused MRotaryEmbedding contrib op for Qwen mRoPE variants |
| https://github.com/microsoft/onnxruntime/pull/31959 | `microsoft/onnxruntime` | `code_only` | `python` | [Build] Fix cuda plugin CI test failure |
| https://github.com/microsoft/onnxruntime/pull/31157 | `microsoft/onnxruntime` | `code_and_docs` | `python` | [CUDA] Add state_window to LinearAttention and CausalConvWithState to support MTP |
| https://github.com/microsoft/onnxruntime/pull/31964 | `microsoft/onnxruntime` | `code_only` | `python` | Avoid eager static initialization in ORT |
| https://github.com/microsoft/onnxruntime/pull/29396 | `microsoft/onnxruntime` | `code_only` | `python` | Fix path traversal in TensorRT EP RefitEngine |
| https://github.com/microsoft/onnxruntime/pull/29557 | `microsoft/onnxruntime` | `code_only` | `python` | [WebGPU] Deferred-dispatch to parallelize cold-start shader compilation |
| https://github.com/microsoft/onnxruntime/pull/31709 | `microsoft/onnxruntime` | `code_only` | `python` | [WebGPU EP] Support int64 for Min and Max |
| https://github.com/microsoft/onnxruntime/pull/31613 | `microsoft/onnxruntime` | `code_and_docs` | `python` | Wire max-shape inference into workspace estimation |
| https://github.com/microsoft/onnxruntime/pull/29607 | `microsoft/onnxruntime` | `code_only` | `python` | Weightless support for all initializers |
| https://github.com/microsoft/onnxruntime/pull/31748 | `microsoft/onnxruntime` | `code_only` | `python` | [CUDA] Fix CUDA 13 packaging build failures |
| https://github.com/microsoft/onnxruntime/pull/31693 | `microsoft/onnxruntime` | `code_only_tests_or_fixtures` | `python` | Fix GatherBlockQuantized default zero point on CUDA |
| https://github.com/microsoft/onnxruntime/pull/31664 | `microsoft/onnxruntime` | `code_only` | `python` | Make DML runtime fused graph kernel own its model path |
| https://github.com/microsoft/onnxruntime/pull/31729 | `microsoft/onnxruntime` | `code_only` | `python` | [Build] Reduce nvcc_threads to 1 for linux cuda plugin ci |
| https://github.com/microsoft/onnxruntime/pull/28975 | `microsoft/onnxruntime` | `code_and_docs` | `python` | Add double support for Cos op on CPU EP |
| https://github.com/microsoft/onnxruntime/pull/11534 | `microsoft/onnxruntime` | `code_and_docs` | `python` | [CUDA] Implement BitmaskDropout, BitmaskBiasDropout and BitmaskDropoutGrad |
| https://github.com/microsoft/onnxruntime/pull/31724 | `microsoft/onnxruntime` | `code_only` | `python` | [Build] Install complete Perl runtime in Linux packaging images |
| https://github.com/microsoft/onnxruntime/pull/31606 | `microsoft/onnxruntime` | `code_only_tests_or_fixtures` | `python` | [MLAS] Add int8 extreme-value coverage for ARM64 SymmQgemm |
| https://github.com/microsoft/onnxruntime/pull/31665 | `microsoft/onnxruntime` | `code_only` | `python` | Validate constant tensor byte size in DML OnnxTensorWrapper |
| https://github.com/microsoft/onnxruntime/pull/31702 | `microsoft/onnxruntime` | `code_only` | `python` | WebGPU: Support int32 and uint32 for CumSum |
| https://github.com/microsoft/onnxruntime/pull/31479 | `microsoft/onnxruntime` | `code_only` | `python` | [CUDA] Skip FP4 QMoE fc1 activation expansion |
| https://github.com/microsoft/onnxruntime/pull/29826 | `microsoft/onnxruntime` | `code_only_tests_or_fixtures` | `python` | Add regression test ConstantFoldingCopiesAliasedTensorBuffer for PR 29789 |
| https://github.com/microsoft/onnxruntime/pull/31722 | `microsoft/onnxruntime` | `code_and_docs` | `python` | Update CUDA plugin package outputs |
| https://github.com/microsoft/onnxruntime/pull/31611 | `microsoft/onnxruntime` | `code_and_docs` | `python` | [WebGPU] Initial PagedAttention implementation (1/n) |
| https://github.com/microsoft/onnxruntime/pull/31158 | `microsoft/onnxruntime` | `code_and_docs` | `python` | [CUDA] Add LinearAttentionGate and GatedRMSNorm contrib operators |
| https://github.com/microsoft/onnxruntime/pull/31642 | `microsoft/onnxruntime` | `code_only` | `python` | Use stream-aware scratch buffer in CUDA DeformConv |
| https://github.com/microsoft/onnxruntime/pull/31640 | `microsoft/onnxruntime` | `code_only_tests_or_fixtures` | `python` | Fix CUDA BeamSearch fp16 score mapping and add regression test |
| https://github.com/microsoft/onnxruntime/pull/29752 | `microsoft/onnxruntime` | `code_only` | `python` | webgpu: Fix TurboQuant quantized KV cache for batch>1 with per-batch seqlens |
| https://github.com/microsoft/onnxruntime/pull/29893 | `microsoft/onnxruntime` | `code_only` | `python` | [WebGPU] Support odd-N subgroup matrix MatMul weights |
| https://github.com/microsoft/onnxruntime/pull/31669 | `microsoft/onnxruntime` | `code_and_docs` | `python` | Update ort release skill for cuda plugin |
| https://github.com/microsoft/onnxruntime/pull/31159 | `microsoft/onnxruntime` | `code_and_docs` | `python` | [CUDA] Speed up the NVFP4 QMoE decode GEMV and enable it for MTP verify |
| https://github.com/microsoft/onnxruntime/pull/31656 | `microsoft/onnxruntime` | `code_only` | `python` | [DML EP] Fix wide string handling in OpKernelInfoWrapper::GetWideName |
| https://github.com/microsoft/onnxruntime/pull/31634 | `microsoft/onnxruntime` | `code_only` | `python` | [CPU] Tighten cache_indirection shape contract in MultiHeadAttention |
| https://github.com/microsoft/onnxruntime/pull/31650 | `microsoft/onnxruntime` | `code_only` | `python` | Guard CUDA LayerNorm/RMSNorm int32 offset range |
| https://github.com/microsoft/onnxruntime/pull/31632 | `microsoft/onnxruntime` | `code_only` | `python` | [CUDA] Add build option for TensorRT fused attention cubins |
| https://github.com/microsoft/onnxruntime/pull/31614 | `microsoft/onnxruntime` | `code_and_docs` | `python` | Add ort-release-notes skill to draft release notes |
| https://github.com/microsoft/onnxruntime/pull/31635 | `microsoft/onnxruntime` | `code_only` | `python` | [CUDA] Add win-arm64 packaging and size options to plugin pipeline |
| https://github.com/microsoft/onnxruntime/pull/29059 | `microsoft/onnxruntime` | `code_and_docs` | `python` | [WebGPU plugin EP] Update release and packaging-related docs |
| https://github.com/microsoft/onnxruntime/pull/31647 | `microsoft/onnxruntime` | `code_only` | `python` | Handle empty tensors in CUDA InstanceNormalization |
| https://github.com/microsoft/onnxruntime/pull/31652 | `microsoft/onnxruntime` | `code_only_tests_or_fixtures` | `python` | web: fix webpack/Terser release build crash in Web CI Pipeline |
| https://github.com/microsoft/onnxruntime/pull/31481 | `microsoft/onnxruntime` | `code_only` | `python` | [CUDA] MatMulBlockQuantizedFp8Weight: fold the W8A8 activation QDQ into the decode GEMV |
| https://github.com/microsoft/onnxruntime/pull/31151 | `microsoft/onnxruntime` | `code_only` | `python` | [WebNN EP] Reuse shared WASM loader for Blob-backed external data |
| https://github.com/microsoft/onnxruntime/pull/31149 | `microsoft/onnxruntime` | `code_only` | `python` | Throw error on negative Split tensor axis [CPU] |
| https://github.com/microsoft/onnxruntime/pull/31622 | `microsoft/onnxruntime` | `code_only` | `python` | [Build] update build flags of cuda plugin CI to avoid OOM |
| https://github.com/microsoft/onnxruntime/pull/31049 | `microsoft/onnxruntime` | `code_only` | `python` | [WebGPU EP] Support int64 for Tile and Concat |
| https://github.com/microsoft/onnxruntime/pull/31616 | `microsoft/onnxruntime` | `code_only` | `python` | [Build] Fix cuda plugin linux build errors |
| https://github.com/microsoft/onnxruntime/pull/31617 | `microsoft/onnxruntime` | `code_only` | `python` | [Build] Fix Windows ARM64 CUDA plugin build |
| https://github.com/microsoft/onnxruntime/pull/31568 | `microsoft/onnxruntime` | `code_only` | `python` | Fix WebGPU data transfer callbacks on Windows x86 |
| https://github.com/microsoft/onnxruntime/pull/31571 | `microsoft/onnxruntime` | `code_only` | `python` | [CUDA] Support bfloat16 in AllReduce, AllGather and AllToAll |
| https://github.com/microsoft/onnxruntime/pull/31141 | `microsoft/onnxruntime` | `code_only` | `python` | Fix segfault in MatMulNBits prepacking when weights/scales are parent-graph initializers in subgraph |
| https://github.com/microsoft/playwright/pull/42400 | `microsoft/playwright` | `code_and_docs` | `typescript` | revert(locator): page-free `by` locators resolved with page.get() |
| https://github.com/microsoft/playwright/pull/42190 | `microsoft/playwright` | `code_only` | `typescript` | fix(mcp): honor --user-data-dir in extension mode |
| https://github.com/microsoft/playwright/pull/42359 | `microsoft/playwright` | `code_and_docs` | `typescript` | feat(mcp): add start/stop recording commands |
| https://github.com/microsoft/playwright/pull/42374 | `microsoft/playwright` | `code_only_tests_or_fixtures` | `typescript` | test: roll stable-test-runner to 1.63.0-alpha-2026-08-24 |
| https://github.com/microsoft/playwright/pull/42383 | `microsoft/playwright` | `code_only` | `typescript` | fix(recorder): support re-enabling recorder on the same context |
| https://github.com/microsoft/playwright/pull/42358 | `microsoft/playwright` | `code_and_docs` | `typescript` | feat(reporter): report step params in the chrome://tracing report |
| https://github.com/microsoft/playwright/pull/42357 | `microsoft/playwright` | `code_and_docs` | `typescript` | feat(reporter): report step params to the reporters |
| https://github.com/microsoft/playwright/pull/42354 | `microsoft/playwright` | `code_and_docs` | `typescript` | feat(reporter): add chrome://tracing reporter |
| https://github.com/microsoft/playwright/pull/42328 | `microsoft/playwright` | `code_only` | `typescript` | feat(trace): attribute requests to service workers and api request contexts |
| https://github.com/microsoft/playwright/pull/42331 | `microsoft/playwright` | `code_only` | `typescript` | fix(fetch): report security details for resumed TLS sessions |
| https://github.com/microsoft/playwright/pull/42337 | `microsoft/playwright` | `code_only` | `typescript` | feat(webkit): roll to r2355 |
| https://github.com/microsoft/playwright/pull/42340 | `microsoft/playwright` | `code_and_docs` | `typescript` | feat(chromium): roll to r1241 |
| https://github.com/microsoft/playwright/pull/42335 | `microsoft/playwright` | `code_only` | `typescript` | fix(html-reporter): make settings and metadata controls keyboard accessible |
| https://github.com/microsoft/playwright/pull/42336 | `microsoft/playwright` | `code_only` | `typescript` | fix(trace-viewer): use ToolbarButton for Show all and the console badge |
| https://github.com/microsoft/playwright/pull/42339 | `microsoft/playwright` | `code_only_tests_or_fixtures` | `typescript` | test(mcp): cover --sandbox at the config resolution level |
| https://github.com/microsoft/playwright/pull/42333 | `microsoft/playwright` | `code_only` | `typescript` | fix(cli): parse negative numbers as arguments |
| https://github.com/microsoft/playwright/pull/42306 | `microsoft/playwright` | `code_only_tests_or_fixtures` | `typescript` | fix(test): unflake MCP cli-core 'click link' on Firefox |
| https://github.com/microsoft/playwright/pull/42322 | `microsoft/playwright` | `code_and_docs` | `typescript` | feat(codegen): add --http-credentials option |
| https://github.com/microsoft/playwright/pull/42268 | `microsoft/playwright` | `code_only` | `typescript` | fix(aria): annotate aria-hidden elements in AI snapshots |
| https://github.com/microsoft/playwright/pull/41942 | `microsoft/playwright` | `code_only` | `typescript` | fix(registry): evaluate `defaultCacheDirectory` lazily |
| https://github.com/microsoft/playwright/pull/42313 | `microsoft/playwright` | `code_only_tests_or_fixtures` | `typescript` | test(credentials): httpCredentials should not override page's Authorization header |
| https://github.com/microsoft/playwright/pull/42319 | `microsoft/playwright` | `code_only` | `typescript` | feat(trace-viewer): webm-based film strip |
| https://github.com/microsoft/playwright/pull/42318 | `microsoft/playwright` | `code_only` | `typescript` | fix(cli): add .playwright-cli/ to .gitignore on workspace install |
| https://github.com/microsoft/playwright/pull/42311 | `microsoft/playwright` | `code_only` | `typescript` | fix(web): make image diff mode switcher keyboard accessible |
| https://github.com/microsoft/playwright/pull/42310 | `microsoft/playwright` | `code_only` | `typescript` | fix(web): make expandable section titles keyboard accessible |
| https://github.com/microsoft/playwright/pull/42303 | `microsoft/playwright` | `code_only` | `typescript` | feat(webkit): roll to r2354 |
| https://github.com/microsoft/playwright/pull/42297 | `microsoft/playwright` | `code_only` | `typescript` | fix(trace-viewer): pretty-print JSON without losing precision |
| https://github.com/microsoft/playwright/pull/42247 | `microsoft/playwright` | `code_only` | `typescript` | fix(dispatcher): do not lose abort requests between progress controllers |
| https://github.com/microsoft/playwright/pull/42289 | `microsoft/playwright` | `code_only` | `typescript` | chore(html-reporter): render a thumbnail for every trace attachment |
| https://github.com/microsoft/playwright/pull/42294 | `microsoft/playwright` | `code_only` | `typescript` | fix(chromium): stop disabling BoundaryEventDispatchTracksNodeRemoval |
| https://github.com/microsoft/playwright/pull/42283 | `microsoft/playwright` | `code_and_docs` | `typescript` | feat(tracing): allow configuring the screenshots size |
| https://github.com/microsoft/playwright/pull/42285 | `microsoft/playwright` | `code_only` | `typescript` | chore(trace-viewer): show only the screencast frame on timeline hover |
| https://github.com/microsoft/playwright/pull/42288 | `microsoft/playwright` | `code_only` | `typescript` | fix(mcp): do not clobber chromiumSandbox from the config file |
| https://github.com/microsoft/playwright/pull/42277 | `microsoft/playwright` | `code_only` | `typescript` | chore(highlight): resolve highlights periodically in HighlightController |
| https://github.com/microsoft/playwright/pull/42282 | `microsoft/playwright` | `code_only` | `typescript` | fix(chromium): dispose worker sessions when their frame session is disposed |
| https://github.com/microsoft/playwright/pull/42276 | `microsoft/playwright` | `code_only_tests_or_fixtures` | `typescript` | test: roll stable-test-runner to 1.63.0-alpha-2026-08-17 |
| https://github.com/microsoft/playwright/pull/42254 | `microsoft/playwright` | `code_only_tests_or_fixtures` | `typescript` | test: race between disabling interception and network request in chromium |
| https://github.com/microsoft/playwright/pull/42253 | `microsoft/playwright` | `code_only` | `typescript` | chore(recorder): render highlights via the shared element highlight |
| https://github.com/microsoft/playwright/pull/42259 | `microsoft/playwright` | `code_and_docs` | `typescript` | feat(extension): support multiple simultaneous client connections |
| https://github.com/microsoft/playwright/pull/42260 | `microsoft/playwright` | `code_only` | `typescript` | fix(storageState): close IndexedDB connections opened by collect and restore |
| https://github.com/microsoft/playwright/pull/42255 | `microsoft/playwright` | `code_only` | `typescript` | fix(net): pass a generous autoSelectFamilyAttemptTimeout |
| https://github.com/microsoft/playwright/pull/42240 | `microsoft/playwright` | `code_only` | `typescript` | chore(net): use native happy eyeballs instead of the manual implementation |
| https://github.com/microsoft/playwright/pull/42252 | `microsoft/playwright` | `code_only_tests_or_fixtures` | `typescript` | test: setOffline() persists across navigations |
| https://github.com/microsoft/playwright/pull/42251 | `microsoft/playwright` | `code_only_tests_or_fixtures` | `typescript` | test: race between close() and navigation with RenderDocument |
| https://github.com/microsoft/playwright/pull/42250 | `microsoft/playwright` | `code_only` | `typescript` | chore(expect): pass expect title explicitly to library calls |
| https://github.com/microsoft/playwright/pull/42241 | `microsoft/playwright` | `code_only` | `typescript` | feat(webkit): roll to r2349 |
| https://github.com/microsoft/playwright/pull/42229 | `microsoft/playwright` | `code_only` | `typescript` | feat(firefox): roll to r1540 |
| https://github.com/microsoft/playwright/pull/42242 | `microsoft/playwright` | `code_only` | `typescript` | fix(har): do not stall context close when saving the har fails |
| https://github.com/microsoft/playwright/pull/42217 | `microsoft/playwright` | `code_and_docs` | `typescript` | feat(trace): add --grep filter to trace console |
| https://github.com/microsoft/playwright/pull/42239 | `microsoft/playwright` | `code_only` | `typescript` | fix(types): remove stale screencast annotate option |
| https://github.com/microsoft/playwright/pull/42238 | `microsoft/playwright` | `code_only` | `typescript` | chore(deps): roll chokidar to 4.0.3, drop fsevents optional dependency |
| https://github.com/microsoft/playwright/pull/42236 | `microsoft/playwright` | `code_only_tests_or_fixtures` | `typescript` | fix(tests): remove stale devtools path alias |
| https://github.com/microsoft/playwright/pull/42228 | `microsoft/playwright` | `code_only` | `typescript` | fix(mcp): report the actual remote browser name in browserInfo |
| https://github.com/microsoft/playwright/pull/42221 | `microsoft/playwright` | `code_only` | `typescript` | fix(extension): recover the debugger after an involuntary detach |
| https://github.com/microsoft/playwright/pull/42230 | `microsoft/playwright` | `code_only` | `typescript` | feat(trace-viewer): render action point and target box in aria mode |
| https://github.com/microsoft/playwright/pull/42039 | `microsoft/playwright` | `code_only_tests_or_fixtures` | `typescript` | test(clipboard): check that the headless clipboard is isolated from the operating system |
| https://github.com/microsoft/playwright/pull/42222 | `microsoft/playwright` | `code_and_docs` | `typescript` | feat(install): add --no-remove option to keep unused browsers |
| https://github.com/microsoft/playwright/pull/42224 | `microsoft/playwright` | `code_only` | `typescript` | fix(extension): do not treat orphaned preferences entries as an installed extension |
| https://github.com/microsoft/playwright/pull/42210 | `microsoft/playwright` | `code_only` | `typescript` | feat(webkit): roll to r2346 |
| https://github.com/microsoft/playwright/pull/42215 | `microsoft/playwright` | `code_only_tests_or_fixtures` | `typescript` | devops: gate PR CI triage on write access |
| https://github.com/microsoft/playwright/pull/42148 | `microsoft/playwright` | `code_only_tests_or_fixtures` | `typescript` | test(connect): unblock hung launchServer teardown with SIGKILL fallback |
| https://github.com/microsoft/playwright/pull/42211 | `microsoft/playwright` | `code_and_docs` | `typescript` | feat(trace-viewer): add "Display Aria" mode |
| https://github.com/microsoft/playwright/pull/42191 | `microsoft/playwright` | `code_and_docs` | `typescript` | fix(trace): record failed request durations, print request start times |
| https://github.com/microsoft/playwright/pull/42209 | `microsoft/playwright` | `code_only` | `typescript` | chore(tracing): name action snapshots after call id, clarify chunk file sets |
| https://github.com/microsoft/playwright/pull/42208 | `microsoft/playwright` | `code_only` | `typescript` | chore(trace): remove context attribution from the trace model |
| https://github.com/microsoft/playwright/pull/42201 | `microsoft/playwright` | `code_only` | `typescript` | fix(chromium): use resource type when deciding if evicted body can be re-fetched |
| https://github.com/microsoft/playwright/pull/42202 | `microsoft/playwright` | `code_only_tests_or_fixtures` | `typescript` | test: update webkit expectations for NWLoader on macOS |
| https://github.com/microsoft/playwright/pull/42192 | `microsoft/playwright` | `code_only` | `typescript` | chore(tracing): reference trace and har blobs via relative file paths |
| https://github.com/microsoft/playwright/pull/42204 | `microsoft/playwright` | `code_only` | `typescript` | fix(ci): do not turn complete clones shallow when capturing git diff |
| https://github.com/microsoft/playwright/pull/42200 | `microsoft/playwright` | `code_only` | `typescript` | chore: cleanup more ct remnants |
| https://github.com/microsoft/playwright/pull/42073 | `microsoft/playwright` | `code_and_docs` | `typescript` | feat(trace): split API requests into a separate network stream |
| https://github.com/microsoft/playwright/pull/41986 | `microsoft/playwright` | `code_only` | `typescript` | fix(chromium): refuse WebUI navigations that crash the browser |
| https://github.com/microsoft/playwright/pull/42196 | `microsoft/playwright` | `code_only` | `typescript` | devops(fix-flakes): request review from Suggested-reviewer |
| https://github.com/microsoft/playwright/pull/42195 | `microsoft/playwright` | `code_only_tests_or_fixtures` | `typescript` | test(mcp): de-flake annotate screencast session switch startup |
| https://github.com/microsoft/playwright/pull/42189 | `microsoft/playwright` | `code_only` | `typescript` | fix(mcp): do not run heartbeat for clients without the event stream |
| https://github.com/microsoft/playwright/pull/42164 | `microsoft/playwright` | `code_only` | `typescript` | feat(test-runner): annotate serial suites for custom sharding |
| https://github.com/microsoft/playwright/pull/42185 | `microsoft/playwright` | `code_only` | `typescript` | fix(cli): hash unix socket basenames to stay within sun_path |
| https://github.com/microsoft/playwright/pull/42131 | `microsoft/playwright` | `code_only` | `typescript` | test(firefox): fixme flaky codegen pierceFrames disambiguation on Intel macOS |
| https://github.com/microsoft/playwright/pull/42162 | `microsoft/playwright` | `code_only` | `typescript` | feat(types): generics for APIRequestContext and APIResponse |
| https://github.com/microsoft/playwright/pull/42167 | `microsoft/playwright` | `code_and_docs` | `typescript` | feat(trace): add action screenshot and aria snapshot events |
| https://github.com/microsoft/playwright/pull/42171 | `microsoft/playwright` | `code_only` | `typescript` | devops: move npm publishing to ESRP pipeline |
| https://github.com/microsoft/playwright/pull/42169 | `microsoft/playwright` | `code_and_docs` | `typescript` | chore(aria): derive yaml aria snapshots from the JSON snapshot |
| https://github.com/microsoft/playwright/pull/42144 | `microsoft/playwright` | `code_only` | `typescript` | devops: add ESRP pipeline for publishing npm alpha versions |
| https://github.com/microsoft/playwright/pull/42145 | `microsoft/playwright` | `code_only_tests_or_fixtures` | `typescript` | test(filechooser): allow exact one second `lastModified` rounding |
| https://github.com/microsoft/playwright/pull/42157 | `microsoft/playwright` | `code_and_docs` | `typescript` | feat(locator): page-free `by` locators resolved with page.get() |
| https://github.com/microsoft/playwright/pull/42136 | `microsoft/playwright` | `code_and_docs` | `typescript` | docs(locator): drop type markup from ariaSnapshotJSON details |
| https://github.com/microsoft/playwright/pull/42133 | `microsoft/playwright` | `code_only` | `typescript` | fix(mcp): only enable /killkillkill under test |
| https://github.com/microsoft/playwright/pull/42158 | `microsoft/playwright` | `code_only` | `typescript` | chore(extension): mark 0.3.0 |
| https://github.com/microsoft/playwright/pull/42138 | `microsoft/playwright` | `code_only` | `typescript` | fix(cli): print -s instead of --s after attach |
| https://github.com/microsoft/playwright/pull/42150 | `microsoft/playwright` | `code_only` | `typescript` | feat(mcp): default codegen language from PW_LANG_NAME |
| https://github.com/microsoft/playwright/pull/42151 | `microsoft/playwright` | `code_only` | `typescript` | fix(html-reporter): use h2 for non-expandable chip headers |
| https://github.com/microsoft/playwright/pull/42147 | `microsoft/playwright` | `code_only` | `typescript` | devops: pass npm dist-tag to ESRP via productstate |
| https://github.com/microsoft/playwright/pull/42155 | `microsoft/playwright` | `code_only` | `typescript` | fix(cli): hide Windows daemon consoles |
| https://github.com/microsoft/playwright/pull/42149 | `microsoft/playwright` | `code_only` | `typescript` | fix(html-reporter): use a button element for the chip header |
| https://github.com/microsoft/playwright/pull/42146 | `microsoft/playwright` | `code_only` | `typescript` | devops: authenticate stable-test-runner npm registry in ESRP pipeline |
| https://github.com/microsoft/playwright/pull/42134 | `microsoft/playwright` | `code_only` | `typescript` | devops: add 7-day Dependabot cooldown for npm |
| https://github.com/microsoft/playwright/pull/42141 | `microsoft/playwright` | `code_only_tests_or_fixtures` | `typescript` | test: mark new test as failing on macos |
| https://github.com/microsoft/playwright/pull/42132 | `microsoft/playwright` | `code_only` | `typescript` | chore(deps): bump the github-actions group with 7 updates |
| https://github.com/microsoft/playwright/pull/42116 | `microsoft/playwright` | `code_only` | `typescript` | fix(fetch): do not crash on late EPIPE after refused body |
| https://github.com/microsoft/playwright/pull/42107 | `microsoft/playwright` | `code_only` | `typescript` | Pin GitHub Actions to full-length commit SHAs |
| https://github.com/microsoft/playwright/pull/42130 | `microsoft/playwright` | `code_only_tests_or_fixtures` | `typescript` | test(bidi): unskip new websocket header tests |
| https://github.com/microsoft/playwright/pull/42126 | `microsoft/playwright` | `code_only` | `typescript` | test: unflake har-websocket timing assertions |
| https://github.com/microsoft/playwright/pull/42037 | `microsoft/playwright` | `code_only_tests_or_fixtures` | `typescript` | test(websocket): cover `setExtraHTTPHeaders` and `locale` on the handshake request |
| https://github.com/microsoft/playwright/pull/42124 | `microsoft/playwright` | `code_only` | `typescript` | fix(chromium): only re-fetch replay-safe requests when reading response body |
| https://github.com/microsoft/playwright/pull/42123 | `microsoft/playwright` | `code_only_tests_or_fixtures` | `typescript` | test(firefox): drop init-script console workaround |
| https://github.com/microsoft/playwright/pull/42122 | `microsoft/playwright` | `code_only` | `typescript` | fix(mcp): mention PLAYWRIGHT_MCP_EXECUTABLE_PATH in extension not found error |
| https://github.com/microsoft/playwright/pull/42121 | `microsoft/playwright` | `code_only_tests_or_fixtures` | `typescript` | Revert "test: roll stable-test-runner to 1.63.0-alpha-2026-08-03" |
| https://github.com/microsoft/playwright/pull/42119 | `microsoft/playwright` | `code_only` | `typescript` | fix(mcp): pass noDefaults for extension CDP connections |
| https://github.com/microsoft/playwright/pull/42103 | `microsoft/playwright` | `code_only` | `typescript` | fix(mcp): validate Host and Origin on CDP relay WebSocket upgrades |
| https://github.com/microsoft/playwright/pull/42114 | `microsoft/playwright` | `code_only` | `typescript` | Revert "chore(deps): bump ip-address from 10.2.0 to 10.4.0" |
| https://github.com/microsoft/playwright/pull/42106 | `microsoft/playwright` | `code_only` | `typescript` | feat(mcp): support python, java and csharp in --codegen |
| https://github.com/microsoft/playwright/pull/42118 | `microsoft/playwright` | `code_only` | `typescript` | chore(bidi): mark all `no such frame` errors with type `closed` |
| https://github.com/microsoft/playwright/pull/42101 | `microsoft/playwright` | `code_only` | `typescript` | feat(webkit): roll to r2342 |
| https://github.com/microsoft/playwright/pull/42097 | `microsoft/playwright` | `code_only` | `typescript` | chore(deps): bump undici |
| https://github.com/microsoft/playwright/pull/42096 | `microsoft/playwright` | `code_only` | `typescript` | chore(deps): bump ip-address from 10.2.0 to 10.4.0 |
| https://github.com/microsoft/playwright/pull/42091 | `microsoft/playwright` | `code_only_tests_or_fixtures` | `typescript` | test: roll stable-test-runner to 1.63.0-alpha-2026-08-03 |
| https://github.com/microsoft/playwright/pull/42088 | `microsoft/playwright` | `code_only_tests_or_fixtures` | `typescript` | fix(mcp): bump firefox action timeout for flaky dialog cli tests |
| https://github.com/microsoft/playwright/pull/42098 | `microsoft/playwright` | `code_and_docs` | `typescript` | feat(mcp): emit structured snapshot in --json responses |
| https://github.com/microsoft/playwright/pull/42102 | `microsoft/playwright` | `code_only` | `typescript` | feat(mcp): add snapshot.boxes config to include bounding boxes in snapshots |
| https://github.com/microsoft/playwright/pull/42099 | `microsoft/playwright` | `code_and_docs` | `typescript` | feat(cli): add -g flag to install skills globally |
| https://github.com/microsoft/playwright/pull/42090 | `microsoft/playwright` | `code_only` | `typescript` | devops: extract reusable PR CI triage workflow |
| https://github.com/microsoft/playwright/pull/42071 | `microsoft/playwright` | `code_only` | `typescript` | fix(trace-viewer): remove speculative 1s isUnderTest startup delay |
| https://github.com/microsoft/playwright/pull/41966 | `microsoft/playwright` | `code_only` | `typescript` | fix(mcp): reconnect to the browser after disconnect |
| https://github.com/microsoft/playwright/pull/42072 | `microsoft/playwright` | `code_and_docs` | `typescript` | feat(chromium): roll to r1237 |
| https://github.com/microsoft/playwright/pull/41923 | `microsoft/playwright` | `code_only` | `typescript` | perf(mcp): skip aria snapshot capture when the response discards it |
| https://github.com/microsoft/playwright/pull/41982 | `microsoft/playwright` | `code_only` | `typescript` | chore(mcp): replace BackendManager with backend dispose callback and events |
| https://github.com/microsoft/playwright/pull/42060 | `microsoft/playwright` | `code_only` | `typescript` | feat(trace-viewer): show test annotations in the trace viewer |
| https://github.com/microsoft/playwright/pull/42059 | `microsoft/playwright` | `code_only` | `typescript` | feat(codegen): do not use contenteditable text in generated fill selectors |
| https://github.com/microsoft/playwright/pull/42061 | `microsoft/playwright` | `code_only` | `typescript` | feat(webkit): roll to r2341 |
| https://github.com/microsoft/playwright/pull/42005 | `microsoft/playwright` | `code_only` | `typescript` | fix(tsconfig): do not throw when "extends"/"references" cannot be resolved |
| https://github.com/microsoft/playwright/pull/42056 | `microsoft/playwright` | `code_only` | `typescript` | fix(test-runner): recover beforeAll-skipped tests for --last-failed |
| https://github.com/microsoft/playwright/pull/42055 | `microsoft/playwright` | `code_only_tests_or_fixtures` | `typescript` | test(bidi): unskip accept-language header websocket test |
| https://github.com/microsoft/playwright/pull/42042 | `microsoft/playwright` | `code_only` | `typescript` | fix(cli): exit with non-zero code when the tool result is an error |
| https://github.com/microsoft/playwright/pull/42057 | `microsoft/playwright` | `code_and_docs` | `typescript` | fix(cli): accept multiple files in upload command |
| https://github.com/microsoft/playwright/pull/42038 | `microsoft/playwright` | `code_only` | `typescript` | feat(chromium): roll to r1236 |
| https://github.com/microsoft/playwright/pull/42054 | `microsoft/playwright` | `code_only` | `typescript` | chore(bidi): add support for the local-network-access permission |
| https://github.com/microsoft/playwright/pull/42053 | `microsoft/playwright` | `code_only_tests_or_fixtures` | `typescript` | test(page): cover file URL to about:blank navigation |
| https://github.com/microsoft/playwright/pull/42051 | `microsoft/playwright` | `code_and_docs` | `typescript` | feat(test): add reducedMotion, forcedColors, contrast as standalone test options |
| https://github.com/microsoft/playwright/pull/42049 | `microsoft/playwright` | `code_only_tests_or_fixtures` | `typescript` | test(mcp): fix flaky dashboard -s activation test on firefox |
| https://github.com/microsoft/playwright/pull/42033 | `microsoft/playwright` | `code_and_docs` | `typescript` | feat(selectors): add pierceFrames context option |
| https://github.com/microsoft/playwright/pull/42032 | `microsoft/playwright` | `code_only` | `typescript` | fix(mcp): clear dialog modal state when dialog is closed out of band |
| https://github.com/microsoft/playwright/pull/42030 | `microsoft/playwright` | `code_only` | `typescript` | chore: remove firefox-beta and chromium-tip-of-tree channels |
| https://github.com/microsoft/playwright/pull/42031 | `microsoft/playwright` | `code_only` | `typescript` | feat(selectors): support entering frames while piercing |
| https://github.com/microsoft/playwright/pull/42034 | `microsoft/playwright` | `code_only` | `typescript` | fix(aria): keep icon-only clickable elements in ai snapshots |
| https://github.com/microsoft/playwright/pull/42027 | `microsoft/playwright` | `code_only` | `typescript` | fix(recorder): don't record duplicate goto for repeated navigation signal |
| https://github.com/microsoft/playwright/pull/42017 | `microsoft/playwright` | `code_only` | `typescript` | chore: remove ubuntu 20.04 browser builds |
| https://github.com/microsoft/playwright/pull/42014 | `microsoft/playwright` | `code_and_docs` | `typescript` | feat(dialog): add dialogclosed event |
| https://github.com/microsoft/playwright/pull/42018 | `microsoft/playwright` | `code_and_docs` | `typescript` | fix(selectors): respect scope when piercing frames |
| https://github.com/microsoft/playwright/pull/42010 | `microsoft/playwright` | `code_only` | `typescript` | fix(runner): do not force-kill worker while its teardown is in progress |
| https://github.com/microsoft/playwright/pull/42016 | `microsoft/playwright` | `code_and_docs` | `typescript` | devops: do not swallow doc generation failures when rolling browsers |
| https://github.com/microsoft/playwright/pull/42019 | `microsoft/playwright` | `code_only_tests_or_fixtures` | `typescript` | test: remove "page/page-evaluate.spec.ts:894 › promise collected" |
| https://github.com/microsoft/playwright/pull/42020 | `microsoft/playwright` | `code_only` | `typescript` | chore: mark v1.62.1 |
| https://github.com/microsoft/playwright/pull/41993 | `microsoft/playwright` | `code_and_docs` | `typescript` | feat(cli): add --add-reporter to append reporters without replacing existing config |
| https://github.com/microsoft/playwright/pull/42009 | `microsoft/playwright` | `code_only` | `typescript` | fix(types): support branded primitives in evaluate arguments |
| https://github.com/microsoft/playwright/pull/41974 | `microsoft/playwright` | `code_only` | `typescript` | feat(chromium): roll to r1235 |
| https://github.com/microsoft/playwright/pull/42011 | `microsoft/playwright` | `code_only` | `typescript` | feat(webkit): roll to r2340 |
| https://github.com/microsoft/playwright/pull/41946 | `microsoft/playwright` | `code_only_tests_or_fixtures` | `typescript` | test(mcp): mark dashboard tests as slow |
| https://github.com/microsoft/playwright/pull/41988 | `microsoft/playwright` | `code_only` | `typescript` | fix(aria): preserve names from collapsed text contributors |
| https://github.com/microsoft/playwright/pull/42003 | `microsoft/playwright` | `code_only_tests_or_fixtures` | `typescript` | Revert "chore: roll stable test runner to 1.62.0-beta-1784842988000" |
| https://github.com/microsoft/playwright/pull/41984 | `microsoft/playwright` | `code_only` | `typescript` | feat(webkit): roll to r2339 |
| https://github.com/microsoft/playwright/pull/41981 | `microsoft/playwright` | `code_only` | `typescript` | chore: mark v1.62.0 |
| https://github.com/microsoft/playwright/pull/41979 | `microsoft/playwright` | `code_and_docs` | `typescript` | feat: support multiple HTTP credentials |
| https://github.com/microsoft/playwright/pull/41980 | `microsoft/playwright` | `code_only_tests_or_fixtures` | `typescript` | chore: roll stable test runner to 1.62.0-beta-1784842988000 |
| https://github.com/microsoft/playwright/pull/41969 | `microsoft/playwright` | `code_only` | `typescript` | chore: roll `browser_patches` |
| https://github.com/microsoft/playwright/pull/40844 | `microsoft/playwright` | `code_and_docs` | `typescript` | feat(test): allow testIdAttribute to be a comma-separated list of names |
| https://github.com/microsoft/playwright/pull/41968 | `microsoft/playwright` | `code_and_docs` | `typescript` | feat(reporter): add `omitTags` option to omit auto-appended tags |
| https://github.com/microsoft/playwright/pull/41962 | `microsoft/playwright` | `code_only` | `typescript` | fix(mcp): escape user input in codegen output |
| https://github.com/microsoft/playwright/pull/41971 | `microsoft/playwright` | `code_only` | `typescript` | feat(webkit): roll to r2337 |
| https://github.com/microsoft/playwright/pull/41855 | `microsoft/playwright` | `code_and_docs` | `typescript` | Revert "feat(test-runner): add httpCache config option" |
| https://github.com/microsoft/playwright/pull/41978 | `microsoft/playwright` | `code_only` | `typescript` | Revert "chore(deps-dev): bump fast-uri from 3.1.3 to 3.1.4" |
| https://github.com/microsoft/playwright/pull/41970 | `microsoft/playwright` | `code_only` | `typescript` | feat(firefox): roll to r1539 |
| https://github.com/microsoft/playwright/pull/41963 | `microsoft/playwright` | `code_and_docs` | `typescript` | feat: add pierceFrames() locator API |
| https://github.com/microsoft/playwright/pull/41958 | `microsoft/playwright` | `code_only` | `typescript` | chore(recorder): unify action coalescing and simplify action types |
| https://github.com/microsoft/playwright/pull/41862 | `microsoft/playwright` | `code_and_docs` | `typescript` | feat(test-runner): support named test locks |
| https://github.com/microsoft/playwright/pull/41965 | `microsoft/playwright` | `code_and_docs` | `typescript` | cherry-pick(#41964): Revert "feat(routeFromHar): add interceptAPIRequests option (#41294)" |
| https://github.com/microsoft/playwright/pull/41964 | `microsoft/playwright` | `code_and_docs` | `typescript` | Revert "feat(routeFromHar): add interceptAPIRequests option (#41294)" |
| https://github.com/microsoft/playwright/pull/41711 | `microsoft/playwright` | `code_only` | `typescript` | feat(dashboard): add a debugger actions panel |
| https://github.com/microsoft/playwright/pull/41919 | `microsoft/playwright` | `code_only` | `typescript` | fix(webview): route `exposeFunctions` callbacks to the originating frame |
| https://github.com/microsoft/playwright/pull/41956 | `microsoft/playwright` | `code_only` | `typescript` | chore(deps-dev): bump fast-uri from 3.1.3 to 3.1.4 |
| https://github.com/microsoft/playwright/pull/41961 | `microsoft/playwright` | `code_only` | `typescript` | perf(test): avoid redundant stack capture |
| https://github.com/microsoft/markitdown/pull/2316 | `microsoft/markitdown` | `code_only` | `python` | Pin GitHub Actions to full-length commit SHAs |
| https://github.com/microsoft/markitdown/pull/2258 | `microsoft/markitdown` | `code_only` | `python` | Bump version to 0.1.7 |
| https://github.com/microsoft/markitdown/pull/2257 | `microsoft/markitdown` | `code_only` | `python` | Fix omml template bugs. |
| https://github.com/microsoft/markitdown/pull/2233 | `microsoft/markitdown` | `code_only` | `python` | fix: handle PPTX SVG images without a rasterized fallback |
| https://github.com/microsoft/markitdown/pull/2223 | `microsoft/markitdown` | `code_and_docs` | `python` | Fix typos and formatting in comments, docstrings, and markdown |
| https://github.com/microsoft/markitdown/pull/2228 | `microsoft/markitdown` | `code_only` | `python` | Fix invalid LaTeX macros for mu, nu, tau, and down-arrow in equation conversion |
| https://github.com/microsoft/markitdown/pull/2227 | `microsoft/markitdown` | `code_only` | `python` | fix: avoid O(n^2) value lookups in PPTX chart conversion |
| https://github.com/microsoft/markitdown/pull/1914 | `microsoft/markitdown` | `code_only` | `python` | Bump version to 0.1.6 |
| https://github.com/microsoft/markitdown/pull/1525 | `microsoft/markitdown` | `code_only` | `python` | Fix: PDF parsing doesn't support partially numbered lists |
| https://github.com/microsoft/markitdown/pull/1865 | `microsoft/markitdown` | `code_and_docs` | `python` | feat: Add Azure Content Understanding converter |
| https://github.com/microsoft/markitdown/pull/1644 | `microsoft/markitdown` | `code_only` | `python` | fix: handle deeply nested HTML that triggers RecursionError |
| https://github.com/microsoft/markitdown/pull/1551 | `microsoft/markitdown` | `code_only` | `python` | Remove onnxruntime<=1.20.1 Windows pin |
| https://github.com/microsoft/markitdown/pull/1653 | `microsoft/markitdown` | `code_and_docs` | `python` | Updated warning about binding to non-local interfaces. |
| https://github.com/microsoft/markitdown/pull/1612 | `microsoft/markitdown` | `code_only` | `python` | Fix O(n) memory growth in PDF conversion by calling page.close() afte… |
| https://github.com/microsoft/markitdown/pull/1564 | `microsoft/markitdown` | `code_only` | `python` | Bump version for release. |
| https://github.com/microsoft/markitdown/pull/1499 | `microsoft/markitdown` | `code_only` | `python` | [MS] Update PDF table extraction to support aligned Markdown |
| https://github.com/microsoft/markitdown/pull/1155 | `microsoft/markitdown` | `code_and_docs` | `python` | Basic SSE MCP Server for MarkItDown  |
| https://github.com/microsoft/markitdown/pull/1554 | `microsoft/markitdown` | `code_only` | `python` | Add text/markdown to Accept header |
| https://github.com/microsoft/markitdown/pull/1552 | `microsoft/markitdown` | `code_and_docs` | `python` | [MS] Extend table support for wide tables |
| https://github.com/microsoft/markitdown/pull/1208 | `microsoft/markitdown` | `code_only` | `python` | Feat: Add checkbox support to _CustomMarkdownify |
| https://github.com/microsoft/markitdown/pull/1245 | `microsoft/markitdown` | `code_and_docs` | `python` | support streamable http mcp |
| https://github.com/microsoft/markitdown/pull/1452 | `microsoft/markitdown` | `code_only` | `python` | Upgrade mammoth to 1.11.0 |
| https://github.com/microsoft/markitdown/pull/98 | `microsoft/markitdown` | `code_only` | `python` | fix incorrect comments for "bail if not ..." for WAV and image cases. |
| https://github.com/microsoft/markitdown/pull/267 | `microsoft/markitdown` | `code_only` | `python` | Set exiftool path explicitly. |
| https://github.com/microsoft/markitdown/pull/1160 | `microsoft/markitdown` | `code_and_docs` | `python` | feat: render math equations in .docx documents |
| https://github.com/microsoft/markitdown/pull/1492 | `microsoft/markitdown` | `code_only` | `python` | Bump versions of mammoth and pdfminer.six |
| https://github.com/microsoft/markitdown/pull/1451 | `microsoft/markitdown` | `code_only` | `python` | Test if mammoth resolves rlinks. |
| https://github.com/microsoft/markitdown/pull/1161 | `microsoft/markitdown` | `code_only` | `python` | Handle PPTX shapes where position is None |
| https://github.com/microsoft/markitdown/pull/1163 | `microsoft/markitdown` | `code_only` | `python` | fix docx parse error (docx testcase: \n in alt) |
| https://github.com/microsoft/markitdown/pull/1226 | `microsoft/markitdown` | `code_only` | `python` | Adding support for data-src Attribute |
| https://github.com/microsoft/markitdown/pull/1319 | `microsoft/markitdown` | `code_and_docs` | `python` | fix: correctly pass custom llm prompt parameter |
| https://github.com/microsoft/markitdown/pull/1352 | `microsoft/markitdown` | `code_only` | `python` | HTML\| Update document intelligence file type handling |
| https://github.com/microsoft/markitdown/pull/1394 | `microsoft/markitdown` | `code_only` | `python` | Bump actions/checkout from 4 to 5 |
| https://github.com/microsoft/markitdown/pull/1399 | `microsoft/markitdown` | `code_only` | `python` | Ensure safe ExifTool usage: require >= 12.24 |
| https://github.com/microsoft/markitdown/pull/1393 | `microsoft/markitdown` | `code_only` | `python` | Fixed documentation typos in _base_converter.py |
| https://github.com/microsoft/markitdown/pull/1405 | `microsoft/markitdown` | `code_only` | `python` | Resolved an issue with linked images in docx [mammoth] |
| https://github.com/microsoft/markitdown/pull/1256 | `microsoft/markitdown` | `code_only` | `python` | Chore: Make linter happy |
| https://github.com/microsoft/markitdown/pull/1140 | `microsoft/markitdown` | `code_only` | `python` | Add support for preserving base64 encoded images |
| https://github.com/microsoft/markitdown/pull/1273 | `microsoft/markitdown` | `code_only` | `python` | Have the MarkItDown MCP server read MARKITDOWN_ENABLE_PLUGINS from ENV |
| https://github.com/microsoft/markitdown/pull/1274 | `microsoft/markitdown` | `code_only` | `python` | Pin `onnxruntime` on Windows |
| https://github.com/microsoft/markitdown/pull/1272 | `microsoft/markitdown` | `code_only` | `python` | Promoting 0.1.2a1 to 0.1.2 |
| https://github.com/microsoft/markitdown/pull/1264 | `microsoft/markitdown` | `code_and_docs` | `python` | Small changes to favor streamable HTTP over deprecated SSE |
| https://github.com/microsoft/markitdown/pull/1260 | `microsoft/markitdown` | `code_only` | `python` | Preparing a pre-release of 0.1.2 |
| https://github.com/microsoft/markitdown/pull/1253 | `microsoft/markitdown` | `code_only` | `python` | feat: support API version selection for Document Intelligence |
| https://github.com/microsoft/markitdown/pull/1241 | `microsoft/markitdown` | `code_only` | `python` | FIX YouTube transcript errors |
| https://github.com/microsoft/markitdown/pull/1259 | `microsoft/markitdown` | `code_only` | `python` | Switched from the stdlib minidom parser to defusedxml. |
| https://github.com/microsoft/markitdown/pull/1176 | `microsoft/markitdown` | `code_only` | `python` | Add CSV to Markdown table conversion - fixes #1144 |
| https://github.com/microsoft/markitdown/pull/1131 | `microsoft/markitdown` | `code_and_docs` | `python` | EPub Support. Adapted #123 to not use epublib. |
| https://github.com/microsoft/markitdown/pull/1154 | `microsoft/markitdown` | `code_only` | `python` | Bump version. |
| https://github.com/microsoft/markitdown/pull/1151 | `microsoft/markitdown` | `code_only` | `python` | Make it easier to use AzureKeyCredentials with Azure Doc Intelligence |
| https://github.com/microsoft/markitdown/pull/1153 | `microsoft/markitdown` | `code_only` | `python` | convert_url renamed to convert_uri, and now handles data and file URIs |
| https://github.com/microsoft/markitdown/pull/1150 | `microsoft/markitdown` | `code_and_docs` | `python` | Bump version to 0.1.0 |
| https://github.com/microsoft/markitdown/pull/1149 | `microsoft/markitdown` | `code_only` | `python` | Bump version and resolve a console encoding error. |
| https://github.com/microsoft/markitdown/pull/1143 | `microsoft/markitdown` | `code_only` | `python` | Adjust warning filters and update dependencies |
| https://github.com/microsoft/markitdown/pull/1142 | `microsoft/markitdown` | `code_only` | `python` | Consider anything with a charset as plain text-convertible. |
| https://github.com/microsoft/markitdown/pull/1136 | `microsoft/markitdown` | `code_only` | `python` | Have magika read from the stream. |
| https://github.com/microsoft/markitdown/pull/1133 | `microsoft/markitdown` | `code_only` | `python` | Investigate and silence warnings. |
| https://github.com/microsoft/markitdown/pull/1132 | `microsoft/markitdown` | `code_only` | `python` | Fix remaining mypy errors. |
| https://github.com/microsoft/markitdown/pull/1121 | `microsoft/markitdown` | `code_only` | `python` | Fix string formatting in FileConversionException error message |
| https://github.com/microsoft/markitdown/pull/1124 | `microsoft/markitdown` | `code_only` | `python` | Small fixes for autogen integration. |
| https://github.com/microsoft/markitdown/pull/1123 | `microsoft/markitdown` | `code_only` | `python` | Bumping version to 0.1.0a2 |
| https://github.com/microsoft/markitdown/pull/1122 | `microsoft/markitdown` | `code_only` | `python` | Handle not supported plot type in pptx |
| https://github.com/microsoft/markitdown/pull/1120 | `microsoft/markitdown` | `code_only` | `python` | Refactored tests. |
| https://github.com/microsoft/markitdown/pull/130 | `microsoft/markitdown` | `code_only` | `python` | Update CLI helpdoc formatting to allow indentation in code |
| https://github.com/microsoft/markitdown/pull/1115 | `microsoft/markitdown` | `code_only` | `python` | Added CLI options for extension, mime-types, and charset. |
| https://github.com/microsoft/markitdown/pull/1114 | `microsoft/markitdown` | `code_only` | `python` | Minimize guesses when guesses are compatible. |
| https://github.com/microsoft/markitdown/pull/1108 | `microsoft/markitdown` | `code_only` | `python` | Switch from puremagic to magika. |
| https://github.com/microsoft/markitdown/pull/1109 | `microsoft/markitdown` | `code_only` | `python` | fix typo in well-known path list |
| https://github.com/microsoft/markitdown/pull/1106 | `microsoft/markitdown` | `code_only` | `python` | Fix exiftool in well-known paths. |
| https://github.com/microsoft/markitdown/pull/220 | `microsoft/markitdown` | `code_only` | `python` | feat(docker): improve dockerfile build |
| https://github.com/microsoft/markitdown/pull/1104 | `microsoft/markitdown` | `code_and_docs` | `python` | feat: sort pptx shapes to be parsed in top-to-bottom, left-to-right order |
| https://github.com/microsoft/markitdown/pull/1105 | `microsoft/markitdown` | `code_only` | `python` | Removed deprecation and other warnings. |
| https://github.com/microsoft/markitdown/pull/1101 | `microsoft/markitdown` | `code_only` | `python` | Addresses #1068 |
| https://github.com/microsoft/markitdown/pull/1098 | `microsoft/markitdown` | `code_only` | `python` | Fixed formatting. |
| https://github.com/microsoft/markitdown/pull/1089 | `microsoft/markitdown` | `code_only` | `python` | Fixed deepcopy failure when passing llm_client |
| https://github.com/microsoft/markitdown/pull/1097 | `microsoft/markitdown` | `code_only` | `python` | Fixed version. |
| https://github.com/microsoft/markitdown/pull/1096 | `microsoft/markitdown` | `code_only` | `python` | Fixed loading of plugins. |
| https://github.com/microsoft/markitdown/pull/1095 | `microsoft/markitdown` | `code_only` | `python` | Bump version |
| https://github.com/microsoft/markitdown/pull/1094 | `microsoft/markitdown` | `code_only` | `python` | Bump version. |
| https://github.com/microsoft/markitdown/pull/1085 | `microsoft/markitdown` | `code_only` | `python` | Fixed property name |
| https://github.com/microsoft/markitdown/pull/1079 | `microsoft/markitdown` | `code_and_docs` | `python` | [Draft] Exploring ways to allow Optional dependencies |
| https://github.com/microsoft/markitdown/pull/1082 | `microsoft/markitdown` | `code_only` | `python` | Exceptions should subclass Exception not BaseException. |
| https://github.com/microsoft/markitdown/pull/1080 | `microsoft/markitdown` | `code_only` | `python` | Print and log better exceptions when file conversions fail. |
| https://github.com/microsoft/markitdown/pull/1078 | `microsoft/markitdown` | `code_only` | `python` | Don't have ZipConverter accept OOXML files. |
| https://github.com/microsoft/markitdown/pull/1038 | `microsoft/markitdown` | `code_only` | `python` | Fix UnboundLocalError in MarkItDown._convert |
| https://github.com/microsoft/markitdown/pull/1076 | `microsoft/markitdown` | `code_only` | `python` | Make sure extensions are unique in MarkItDown's convert methods. |
| https://github.com/microsoft/markitdown/pull/1075 | `microsoft/markitdown` | `code_only` | `python` | Bump version. |
| https://github.com/microsoft/markitdown/pull/1072 | `microsoft/markitdown` | `code_only` | `python` | Unable to convert HTML to Markdown |
| https://github.com/microsoft/markitdown/pull/331 | `microsoft/markitdown` | `code_only` | `python` | Add Support For PPTX Shape Groups (Fix in code design to not miss out on slide content) |
| https://github.com/microsoft/markitdown/pull/1035 | `microsoft/markitdown` | `code_and_docs` | `python` | fix: Implement retry logic for YouTube transcript fetching and fix URL decoding issue |
| https://github.com/microsoft/markitdown/pull/861 | `microsoft/markitdown` | `code_only` | `python` | add necessary imports |
| https://github.com/microsoft/markitdown/pull/1069 | `microsoft/markitdown` | `code_only` | `python` | Pin Markdownify version. |
| https://github.com/microsoft/markitdown/pull/303 | `microsoft/markitdown` | `code_only` | `python` | Add support for conversion via Document Intelligence |
| https://github.com/microsoft/markitdown/pull/327 | `microsoft/markitdown` | `code_only` | `python` | Added CLI tests. |
| https://github.com/microsoft/markitdown/pull/325 | `microsoft/markitdown` | `code_only` | `python` | Doc Intelligence fixes for refactored code |
| https://github.com/microsoft/markitdown/pull/324 | `microsoft/markitdown` | `code_only` | `python` | Added priority argument to all converter constructors. |
| https://github.com/microsoft/markitdown/pull/320 | `microsoft/markitdown` | `code_only` | `python` | Fix a typo in sample RTF plugin |
| https://github.com/microsoft/markitdown/pull/322 | `microsoft/markitdown` | `code_only` | `python` | Skip generating md links in 'pre' blocks |
| https://github.com/microsoft/markitdown/pull/306 | `microsoft/markitdown` | `code_only` | `python` | feat(pptx): support image description with LLM for pptx files |
| https://github.com/microsoft/markitdown/pull/273 | `microsoft/markitdown` | `code_only` | `python` | Fix for mimetype issue with csv files on windows. |
| https://github.com/microsoft/markitdown/pull/290 | `microsoft/markitdown` | `code_only` | `python` | fix: argparse CLI option ordering, fixes #268 |
| https://github.com/microsoft/markitdown/pull/270 | `microsoft/markitdown` | `code_only` | `python` | Typo fixed in function comment |
| https://github.com/microsoft/markitdown/pull/262 | `microsoft/markitdown` | `code_only` | `python` | remove leading and trailing \n for HtmlConverter |
| https://github.com/microsoft/markitdown/pull/261 | `microsoft/markitdown` | `code_only` | `python` | Recognize json as plain text (if no other handlers are present). |
| https://github.com/microsoft/markitdown/pull/260 | `microsoft/markitdown` | `code_only` | `python` | If puremagic has no guesses, try again after ltrim. |
| https://github.com/microsoft/markitdown/pull/258 | `microsoft/markitdown` | `code_only_tests_or_fixtures` | `python` | Added a test for leading spaces. |
| https://github.com/microsoft/markitdown/pull/169 | `microsoft/markitdown` | `code_only` | `python` | Feature/ Add xls support |
| https://github.com/microsoft/markitdown/pull/196 | `microsoft/markitdown` | `code_only` | `python` | feat: outlook ".msg" file converter |
| https://github.com/microsoft/markitdown/pull/194 | `microsoft/markitdown` | `code_only` | `python` | fix(transcription): TRANSCRIPTION_CAPABLE should be iniztialized |
| https://github.com/microsoft/markitdown/pull/87 | `microsoft/markitdown` | `code_only_tests_or_fixtures` | `python` | refactor(tests): add helper function for tests |
| https://github.com/microsoft/markitdown/pull/112 | `microsoft/markitdown` | `code_only` | `python` | chore: configure Dependabot for GitHub Actions updates |
| https://github.com/microsoft/markitdown/pull/172 | `microsoft/markitdown` | `code_only` | `python` | feat: add version option to markitdown CLI |
| https://github.com/microsoft/markitdown/pull/136 | `microsoft/markitdown` | `code_only` | `python` | feat: enable Git support in devcontainer |
| https://github.com/microsoft/markitdown/pull/179 | `microsoft/markitdown` | `code_only` | `python` | Bump actions/setup-python from 2 to 5 |
| https://github.com/microsoft/markitdown/pull/178 | `microsoft/markitdown` | `code_only_tests_or_fixtures` | `python` | Bump actions/cache from 3 to 4 |
| https://github.com/microsoft/markitdown/pull/116 | `microsoft/markitdown` | `code_and_docs` | `python` | fix: support -o param to avoid encoding issues |
| https://github.com/microsoft/markitdown/pull/177 | `microsoft/markitdown` | `code_only` | `python` | Bump actions/checkout from 2 to 4 |
| https://github.com/microsoft/markitdown/pull/93 | `microsoft/markitdown` | `code_only` | `python` | Added support to use Pathlib |
| https://github.com/microsoft/markitdown/pull/64 | `microsoft/markitdown` | `code_and_docs` | `python` | feat(devcontainer): Add DevContainer Configuration for Easier Contribution Setup |
| https://github.com/microsoft/markitdown/pull/121 | `microsoft/markitdown` | `code_only` | `python` | feat: add project description in pyproject.toml |
| https://github.com/microsoft/markitdown/pull/129 | `microsoft/markitdown` | `code_only` | `python` | Safeguard against path traversal for ZipConverter |
| https://github.com/microsoft/markitdown/pull/71 | `microsoft/markitdown` | `code_only` | `python` | feat: Add IpynbConverter |
| https://github.com/microsoft/markitdown/pull/97 | `microsoft/markitdown` | `code_only` | `python` | feat: Add RSSConverter  |
| https://github.com/microsoft/markitdown/pull/100 | `microsoft/markitdown` | `code_only` | `python` | Added llm tests to the local test set. |
| https://github.com/microsoft/markitdown/pull/102 | `microsoft/markitdown` | `code_only` | `python` | Bump version. |
| https://github.com/microsoft/markitdown/pull/101 | `microsoft/markitdown` | `code_only` | `python` | Added deprecation warnings for mlm_* arguments. |
| https://github.com/microsoft/markitdown/pull/38 | `microsoft/markitdown` | `code_only` | `python` | Add passing style_map kwarg to Mammoth when converting docx to allow keeping comments |
| https://github.com/microsoft/markitdown/pull/77 | `microsoft/markitdown` | `code_only` | `python` | Kevinclb/main |
| https://github.com/microsoft/markitdown/pull/46 | `microsoft/markitdown` | `code_only` | `python` | feature: add argument parsing and setup.py file for cli tool capability |
| https://github.com/microsoft/markitdown/pull/67 | `microsoft/markitdown` | `code_only` | `python` | fix issue #65 |
| https://github.com/microsoft/markitdown/pull/73 | `microsoft/markitdown` | `code_only` | `python` | Fix LLM terminology in code |
| https://github.com/microsoft/markitdown/pull/60 | `microsoft/markitdown` | `code_and_docs` | `python` | Added Dockerfile  |
| https://github.com/microsoft/markitdown/pull/50 | `microsoft/markitdown` | `code_only` | `python` | Support specifying YouTube transcript language |
| https://github.com/microsoft/markitdown/pull/48 | `microsoft/markitdown` | `code_and_docs` | `python` | Fix: pass the kwargs to _convert method when converting an url file |
| https://github.com/microsoft/markitdown/pull/39 | `microsoft/markitdown` | `code_only` | `python` | Catching pydub's warning of ffmpeg or avconv missing |
| https://github.com/microsoft/markitdown/pull/33 | `microsoft/markitdown` | `code_only` | `python` | Add PPTX chart support |
| https://github.com/microsoft/markitdown/pull/22 | `microsoft/markitdown` | `code_and_docs` | `python` | Add zip handling |
| https://github.com/microsoft/markitdown/pull/19 | `microsoft/markitdown` | `code_only` | `python` | Fix character decoding issues with text-like files |
| https://github.com/microsoft/markitdown/pull/10 | `microsoft/markitdown` | `code_only` | `python` | Remove invalid classifiers |
| https://github.com/microsoft/markitdown/pull/4 | `microsoft/markitdown` | `code_only` | `python` | Small fixes for the file surfer. |
| https://github.com/microsoft/markitdown/pull/3 | `microsoft/markitdown` | `code_only` | `python` | Added a simple CLI. |
| https://github.com/microsoft/markitdown/pull/1 | `microsoft/markitdown` | `code_and_docs` | `python` | Testing CI |
| https://github.com/microsoft/TypeScript/pull/64020 | `microsoft/TypeScript` | `code_only` | `typescript` | Fix release pipeline |
| https://github.com/microsoft/TypeScript/pull/63937 | `microsoft/TypeScript` | `code_only` | `typescript` | Add arbitrary API request batching |
| https://github.com/microsoft/TypeScript/pull/64016 | `microsoft/TypeScript` | `code_only` | `typescript` | Disable concurrent test programs job in merge queue |
| https://github.com/microsoft/TypeScript/pull/64009 | `microsoft/TypeScript` | `code_only` | `typescript` | Don't depend on vfstest for transpile |
| https://github.com/microsoft/TypeScript/pull/63935 | `microsoft/TypeScript` | `code_only` | `typescript` |  Port `formatDiagnostics` and `formatDiagnosticsWithColorAndContext` |
| https://github.com/microsoft/TypeScript/pull/64010 | `microsoft/TypeScript` | `code_only` | `typescript` | Remove free-disk-space step from CI |
| https://github.com/microsoft/TypeScript/pull/64015 | `microsoft/TypeScript` | `code_only` | `typescript` | Fix content mapper flaky test |
| https://github.com/microsoft/TypeScript/pull/63991 | `microsoft/TypeScript` | `code_only` | `typescript` | Update and pin GHA actions |
| https://github.com/microsoft/TypeScript/pull/63992 | `microsoft/TypeScript` | `code_only` | `typescript` | Update publish naming |
| https://github.com/microsoft/TypeScript/pull/63984 | `microsoft/TypeScript` | `code_only` | `typescript` | Fix TS2454 false positive for closed-over mutable variables |
| https://github.com/microsoft/TypeScript/pull/63952 | `microsoft/TypeScript` | `code_only` | `typescript` | Fix binder race |
| https://github.com/microsoft/TypeScript/pull/63932 | `microsoft/TypeScript` | `code_only` | `typescript` | Fix `getDeclarationModifierFlagsFromSymbolEx` for synthetic properties |
| https://github.com/microsoft/TypeScript/pull/63985 | `microsoft/TypeScript` | `code_and_docs` | `typescript` | Fix extension launching |
| https://github.com/microsoft/TypeScript/pull/63983 | `microsoft/TypeScript` | `code_only` | `typescript` | Speed up CI with more jobs, less work |
| https://github.com/microsoft/TypeScript/pull/63977 | `microsoft/TypeScript` | `code_only` | `typescript` | Avoid allocations when checking project reference declaration directories |
| https://github.com/microsoft/TypeScript/pull/63961 | `microsoft/TypeScript` | `code_only` | `typescript` | Use pinned gzip for localization generation |
| https://github.com/microsoft/TypeScript/pull/63967 | `microsoft/TypeScript` | `code_only` | `typescript` | fix: panic on nil point on name check |
| https://github.com/microsoft/TypeScript/pull/63954 | `microsoft/TypeScript` | `code_only` | `typescript` | Replace Quill CLI with focused Mach-O tool |
| https://github.com/microsoft/TypeScript/pull/63974 | `microsoft/TypeScript` | `code_only` | `typescript` | Bump the github-actions group with 3 updates |
| https://github.com/microsoft/TypeScript/pull/62016 | `microsoft/TypeScript` | `code_only` | `typescript` | Clear out checker-level stacks on pop |
| https://github.com/microsoft/TypeScript/pull/63940 | `microsoft/TypeScript` | `code_only_tests_or_fixtures` | `typescript` | Fix TypeScript package major-minor version |
| https://github.com/microsoft/TypeScript/pull/63941 | `microsoft/TypeScript` | `code_only` | `typescript` | Handle FORCE_COLOR values like Node |
| https://github.com/microsoft/TypeScript/pull/63947 | `microsoft/TypeScript` | `code_only` | `typescript` | Bump the github-actions group across 1 directory with 7 updates |
| https://github.com/microsoft/TypeScript/pull/63939 | `microsoft/TypeScript` | `code_only` | `typescript` | Use setup-go with custom download URL |
| https://github.com/microsoft/TypeScript/pull/63938 | `microsoft/TypeScript` | `code_only` | `typescript` | Use new GitHub runner pool |
| https://github.com/microsoft/TypeScript/pull/63927 | `microsoft/TypeScript` | `code_only` | `typescript` | Add package feed CI check |
| https://github.com/microsoft/TypeScript/pull/63899 | `microsoft/TypeScript` | `code_only` | `typescript` | [api] Add `.getReducedType()` method |
| https://github.com/microsoft/TypeScript/pull/63911 | `microsoft/TypeScript` | `code_only` | `typescript` | [api] Add `TypeFormatFlags` enum |
| https://github.com/microsoft/TypeScript/pull/63925 | `microsoft/TypeScript` | `code_only` | `typescript` | Downgrade too-new npm deps |
| https://github.com/microsoft/TypeScript/pull/63912 | `microsoft/TypeScript` | `code_only` | `typescript` | Fix crash in CFA when for-in/for-of expression throws |
| https://github.com/microsoft/TypeScript/pull/59002 | `microsoft/TypeScript` | `code_only` | `typescript` | Cherry-pick #58966 to release-5.5 |
| https://github.com/microsoft/TypeScript/pull/60777 | `microsoft/TypeScript` | `code_only` | `typescript` | Cherry-pick #60402, #60440, #60616 into release-5.7 |
| https://github.com/microsoft/TypeScript/pull/61175 | `microsoft/TypeScript` | `code_only` | `typescript` | Ban import=require and export= under erasableSyntaxOnly |
| https://github.com/microsoft/TypeScript/pull/62727 | `microsoft/TypeScript` | `code_only` | `typescript` | Switch 1ESPT pipelines to 1ESPT-AzureLinux3 |
| https://github.com/microsoft/TypeScript/pull/62754 | `microsoft/TypeScript` | `code_only_tests_or_fixtures` | `typescript` | Shrink relationComplexityError test size |
| https://github.com/microsoft/TypeScript/pull/63127 | `microsoft/TypeScript` | `code_only` | `typescript` | Ensure node is installed in release publisher |
| https://github.com/microsoft/TypeScript/pull/63123 | `microsoft/TypeScript` | `code_only` | `typescript` | Bump github/codeql-action from 4.32.0 to 4.32.2 in the github-actions group |
| https://github.com/microsoft/TypeScript/pull/62971 | `microsoft/TypeScript` | `code_only` | `typescript` | add `collation` to `Intl.CollatorOptions` |
| https://github.com/microsoft/TypeScript/pull/62013 | `microsoft/TypeScript` | `code_only` | `typescript` | Add approximatelySign to NumberFormatRangePartTypeRegistry for ES2023 |
| https://github.com/microsoft/TypeScript/pull/60656 | `microsoft/TypeScript` | `code_only` | `typescript` | Implement Intl Locale Info proposal |
| https://github.com/microsoft/TypeScript/pull/60569 | `microsoft/TypeScript` | `code_only` | `typescript` | Document indexOf return value when not found |
| https://github.com/microsoft/TypeScript/pull/60516 | `microsoft/TypeScript` | `code_only` | `typescript` | Return iterable of RegExpExecArray from RegExp#[Symbol.matchAll] |
| https://github.com/microsoft/TypeScript/pull/57661 | `microsoft/TypeScript` | `code_only` | `typescript` | Update Map.clear and Set.clear jsdoc in es2015.collection.d.ts |
| https://github.com/microsoft/TypeScript/pull/56713 | `microsoft/TypeScript` | `code_only` | `typescript` | Un‑consolidate and fix `WeakMap` constructor overloads |
| https://github.com/microsoft/TypeScript/pull/63097 | `microsoft/TypeScript` | `code_only` | `typescript` | Disable macOS in PR CI |
| https://github.com/microsoft/TypeScript/pull/63095 | `microsoft/TypeScript` | `code_only` | `typescript` | Update descriptions for strict-related flags |
| https://github.com/microsoft/TypeScript/pull/63086 | `microsoft/TypeScript` | `code_only_tests_or_fixtures` | `typescript` | Fix some tests that should have stayed ES5 |
| https://github.com/microsoft/TypeScript/pull/61534 | `microsoft/TypeScript` | `code_only` | `typescript` | fix(jsx): correct source location when react-jsx and whitespace before jsx |
| https://github.com/microsoft/TypeScript/pull/63078 | `microsoft/TypeScript` | `code_only` | `typescript` | Bump the github-actions group with 2 updates |
| https://github.com/microsoft/TypeScript/pull/63076 | `microsoft/TypeScript` | `code_only` | `typescript` | Update implied default for module based on target |
| https://github.com/microsoft/TypeScript/pull/63075 | `microsoft/TypeScript` | `code_only` | `typescript` | Remove ES5 references, misc cleanup |
| https://github.com/microsoft/TypeScript/pull/63026 | `microsoft/TypeScript` | `code_only` | `typescript` | Fixed a crash caused by circularly-reentrant `getEffectsSignature` |
| https://github.com/microsoft/TypeScript/pull/63055 | `microsoft/TypeScript` | `code_only` | `typescript` | Support FORCE_COLOR |
| https://github.com/microsoft/TypeScript/pull/62477 | `microsoft/TypeScript` | `code_only` | `typescript` | Add --ignoreConfig and dont allow specifying files on commandline without it if there is config file present |
| https://github.com/microsoft/TypeScript/pull/63608 | `microsoft/TypeScript` | `code_only` | `typescript` | fix(lib): remove callable signature without new from Intl.PluralRules… |
| https://github.com/microsoft/TypeScript/pull/63053 | `microsoft/TypeScript` | `code_only` | `typescript` | Bump the github-actions group with 2 updates |
| https://github.com/microsoft/TypeScript/pull/63043 | `microsoft/TypeScript` | `code_only` | `typescript` | Fix transform crash with destructured parameter property  |
| https://github.com/microsoft/TypeScript/pull/63038 | `microsoft/TypeScript` | `code_only` | `typescript` | Fix: Consult referenced project options for synthetic default export eligibility |
| https://github.com/microsoft/TypeScript/pull/63675 | `microsoft/TypeScript` | `code_only` | `typescript` | Remove twoslash-repros workflow |
| https://github.com/microsoft/TypeScript/pull/63013 | `microsoft/TypeScript` | `code_only` | `typescript` | Bump the github-actions group across 1 directory with 3 updates |
| https://github.com/microsoft/TypeScript/pull/63022 | `microsoft/TypeScript` | `code_only_tests_or_fixtures` | `typescript` | More test suite strictness fixups |
| https://github.com/microsoft/TypeScript/pull/63020 | `microsoft/TypeScript` | `code_only` | `typescript` | Fix a typo in the JSDoc of `Math.trunc(…)` |
| https://github.com/microsoft/TypeScript/pull/60528 | `microsoft/TypeScript` | `code_only` | `typescript` | Fixed crash related to index type deferral on generic mapped types with name types |
| https://github.com/microsoft/TypeScript/pull/62987 | `microsoft/TypeScript` | `code_only` | `typescript` | Correctly split line endings for `// @testOption: value` parsing |
| https://github.com/microsoft/TypeScript/pull/62275 | `microsoft/TypeScript` | `code_only` | `typescript` | Discard types that reduce to `never` before discriminating by discriminable items |
| https://github.com/microsoft/TypeScript/pull/62789 | `microsoft/TypeScript` | `code_only` | `typescript` | Fix "never nullish" diagnostic missing expressions wrapped in parentheses |
| https://github.com/microsoft/TypeScript/pull/61376 | `microsoft/TypeScript` | `code_only` | `typescript` | Fixed an issue causing spurious "used before being assigned" errors in for of/in loops |
| https://github.com/microsoft/TypeScript/pull/62955 | `microsoft/TypeScript` | `code_only` | `typescript` | Simplify "Configure Build Tools" devcontainer step. |
| https://github.com/microsoft/TypeScript/pull/62923 | `microsoft/TypeScript` | `code_only` | `typescript` | Fix crash in abstract property checking |
| https://github.com/microsoft/TypeScript/pull/63581 | `microsoft/TypeScript` | `code_only` | `typescript` | Fix infinite loop |
| https://github.com/microsoft/TypeScript/pull/62928 | `microsoft/TypeScript` | `code_only` | `typescript` | Fix crash in mixin checking |
| https://github.com/microsoft/TypeScript/pull/63483 | `microsoft/TypeScript` | `code_only` | `typescript` | docs: add JSDoc comments to ReadonlySet interface |
| https://github.com/microsoft/TypeScript/pull/62897 | `microsoft/TypeScript` | `code_only` | `typescript` | Bump the github-actions group with 4 updates |
| https://github.com/microsoft/TypeScript/pull/63571 | `microsoft/TypeScript` | `code_only` | `typescript` | Bump actions/checkout from 6.0.3 to 7.0.0 in the github-actions group |
| https://github.com/microsoft/TypeScript/pull/62891 | `microsoft/TypeScript` | `code_only_tests_or_fixtures` | `typescript` | Fix typo: MERCHANTABLITY → MERCHANTABILITY |
| https://github.com/microsoft/TypeScript/pull/62890 | `microsoft/TypeScript` | `code_only_tests_or_fixtures` | `typescript` | Fix accidental module replacements in tests |
| https://github.com/microsoft/TypeScript/pull/62885 | `microsoft/TypeScript` | `code_only` | `typescript` | Revert "ES2020: fix String.prototype.matchAll type and description" |
| https://github.com/microsoft/TypeScript/pull/62873 | `microsoft/TypeScript` | `code_only` | `typescript` | ES2020: fix String.prototype.matchAll type and description |
| https://github.com/microsoft/TypeScript/pull/63544 | `microsoft/TypeScript` | `code_only` | `typescript` | Update git identity from typescript-bot to typescript-automation[bot] |
| https://github.com/microsoft/TypeScript/pull/63529 | `microsoft/TypeScript` | `code_only` | `typescript` | Bump the github-actions group across 1 directory with 7 updates |
| https://github.com/microsoft/TypeScript/pull/63538 | `microsoft/TypeScript` | `code_only` | `typescript` | Switch from bot PAT to GitHub App token via Azure Key Vault |
| https://github.com/microsoft/TypeScript/pull/62871 | `microsoft/TypeScript` | `code_only` | `typescript` | Disable some more merge queue jobs |
| https://github.com/microsoft/TypeScript/pull/62865 | `microsoft/TypeScript` | `code_only` | `typescript` | Move knip args |
| https://github.com/microsoft/TypeScript/pull/62856 | `microsoft/TypeScript` | `code_only` | `typescript` | Reenable fail-fast in merge queues |
| https://github.com/microsoft/TypeScript/pull/62855 | `microsoft/TypeScript` | `code_only` | `typescript` | Fix ContextFlags compile error |
| https://github.com/microsoft/TypeScript/pull/62851 | `microsoft/TypeScript` | `code_only` | `typescript` | Bump the github-actions group with 3 updates |
| https://github.com/microsoft/TypeScript/pull/62361 | `microsoft/TypeScript` | `code_only` | `typescript` | Make go to definition go to the constraint's properties for object literals in argument positions |
| https://github.com/microsoft/TypeScript/pull/62189 | `microsoft/TypeScript` | `code_only_tests_or_fixtures` | `typescript` | Add tests for contextual param type assignment in nested return type inference scenarios |
| https://github.com/microsoft/TypeScript/pull/56182 | `microsoft/TypeScript` | `code_only` | `typescript` | Include source node inferences in string literal completions deeper in arguments |
| https://github.com/microsoft/TypeScript/pull/63525 | `microsoft/TypeScript` | `code_only` | `typescript` | Fix JSDoc grammar typo: 'returns a undefined' → 'returns undefined' |
| https://github.com/microsoft/TypeScript/pull/63516 | `microsoft/TypeScript` | `code_only` | `typescript` | Update toFixed/toExponential/toPrecision digit range in docs to match the spec |
| https://github.com/microsoft/TypeScript/pull/62722 | `microsoft/TypeScript` | `code_only` | `typescript` | Widen reverse mapped type properties to fix them being treated as EPC-valid sources |
| https://github.com/microsoft/TypeScript/pull/62283 | `microsoft/TypeScript` | `code_only` | `typescript` | Avoid `silentNeverType` leaking into generator types inferred based on inner generic calls at `yield`s |
| https://github.com/microsoft/TypeScript/pull/61560 | `microsoft/TypeScript` | `code_only` | `typescript` | Don't set parent on non-transient symbols in mergeSymbolTable |
| https://github.com/microsoft/TypeScript/pull/63528 | `microsoft/TypeScript` | `code_only` | `typescript` | Delete browser-integration job from ci.yml |
| https://github.com/microsoft/TypeScript/pull/58910 | `microsoft/TypeScript` | `code_only` | `typescript` | Filter return type inferences by constraint applicability |
| https://github.com/microsoft/TypeScript/pull/62799 | `microsoft/TypeScript` | `code_only` | `typescript` | Bump the github-actions group across 1 directory with 2 updates |
| https://github.com/microsoft/TypeScript/pull/63504 | `microsoft/TypeScript` | `code_only` | `typescript` | lib: fix misleading `maxLength` param on string pad* methods |
| https://github.com/microsoft/TypeScript/pull/29510 | `microsoft/TypeScript` | `code_only` | `typescript` | Const contexts for literal expressions |
| https://github.com/microsoft/TypeScript/pull/63489 | `microsoft/TypeScript` | `code_only` | `typescript` | Fix `es2020.intl.d.ts` formatting |
| https://github.com/microsoft/TypeScript/pull/63491 | `microsoft/TypeScript` | `code_only` | `typescript` | 63480 |
| https://github.com/microsoft/TypeScript/pull/62784 | `microsoft/TypeScript` | `code_only` | `typescript` | Update deps |
| https://github.com/microsoft/TypeScript/pull/62783 | `microsoft/TypeScript` | `code_only` | `typescript` | Fix unreachable code detection persisting after incremental edits |
| https://github.com/microsoft/TypeScript/pull/62751 | `microsoft/TypeScript` | `code_only` | `typescript` | Move unreachable checks to checker |
| https://github.com/microsoft/TypeScript/pull/62760 | `microsoft/TypeScript` | `code_only` | `typescript` | 🤖 Pick PR #62751 (Move unreachable checks to checker) into tsgo-port |
| https://github.com/microsoft/TypeScript/pull/62557 | `microsoft/TypeScript` | `code_only` | `typescript` | Update error for allowImportingTsExtensions to mention rewriteRelativeImportExtensions |
| https://github.com/microsoft/TypeScript/pull/62690 | `microsoft/TypeScript` | `code_only` | `typescript` | Remove watchdogs workflow |
| https://github.com/microsoft/TypeScript/pull/62661 | `microsoft/TypeScript` | `code_only` | `typescript` | fix: `[Symbol.iterator]()` lost on union with `never` |
| https://github.com/microsoft/TypeScript/pull/61788 | `microsoft/TypeScript` | `code_only` | `typescript` | Fixed control flow Analysis of aliased discriminants with parenthesized initializers |
| https://github.com/microsoft/TypeScript/pull/62728 | `microsoft/TypeScript` | `code_only` | `typescript` | 🤖 Pick PR #62727 (Switch 1ESPT pipelines to 1ESPT-Azu...) into release-5.9 |
| https://github.com/microsoft/TypeScript/pull/62515 | `microsoft/TypeScript` | `code_only_tests_or_fixtures` | `typescript` | Fix incorrect test options |
| https://github.com/microsoft/TypeScript/pull/62423 | `microsoft/TypeScript` | `code_only` | `typescript` | Revert PR 61928 |
| https://github.com/microsoft/TypeScript/pull/62710 | `microsoft/TypeScript` | `code_only` | `typescript` | Bump github/codeql-action from 4.31.0 to 4.31.2 in the github-actions group |
| https://github.com/microsoft/TypeScript/pull/62701 | `microsoft/TypeScript` | `code_only` | `typescript` | 🤖 Pick PR #62604 (Propagate variance reliability) into tsgo-port |
| https://github.com/microsoft/TypeScript/pull/62699 | `microsoft/TypeScript` | `code_only` | `typescript` | 🤖 Pick PR #62697 (Switch custom runners from mariner-...) into tsgo-port |
| https://github.com/microsoft/TypeScript/pull/62698 | `microsoft/TypeScript` | `code_only` | `typescript` | 🤖 Pick PR #62697 (Switch custom runners from mariner-...) into release-5.9 |
| https://github.com/microsoft/TypeScript/pull/62697 | `microsoft/TypeScript` | `code_only` | `typescript` | Switch custom runners from mariner-2.0 to azure-linux-3 |
| https://github.com/microsoft/TypeScript/pull/62604 | `microsoft/TypeScript` | `code_only` | `typescript` | Propagate variance reliability |
| https://github.com/microsoft/TypeScript/pull/62696 | `microsoft/TypeScript` | `code_only` | `typescript` | Apply tsgo PR 1987 to tsgo-port |
| https://github.com/microsoft/TypeScript/pull/61383 | `microsoft/TypeScript` | `code_only` | `typescript` | Improve references search and quick info on properties with type errors within nullable contextual types |
| https://github.com/microsoft/TypeScript/pull/57912 | `microsoft/TypeScript` | `code_only` | `typescript` | Allow implicit `undefined` returns when the contextual union type contains it |
| https://github.com/microsoft/TypeScript/pull/56859 | `microsoft/TypeScript` | `code_only` | `typescript` | Keep returned (and yielded) literal types as const when their types using `const` type variables |
| https://github.com/microsoft/TypeScript/pull/62676 | `microsoft/TypeScript` | `code_only` | `typescript` | Fixed an issue with "slow" sync iteration types spoiling cached value for async ones |
| https://github.com/microsoft/TypeScript/pull/61211 | `microsoft/TypeScript` | `code_only` | `typescript` | Use comparability for discriminant properties when narrowing types for a default switch clause |
| https://github.com/microsoft/TypeScript/pull/63433 | `microsoft/TypeScript` | `code_only` | `typescript` | docs: improve Math.sign JSDoc grammar and clarity |
| https://github.com/microsoft/TypeScript/pull/62246 | `microsoft/TypeScript` | `code_only` | `typescript` | Add missing whitespace after type parameter's modifiers in interactive inlay hints |
| https://github.com/microsoft/TypeScript/pull/62678 | `microsoft/TypeScript` | `code_only` | `typescript` | Bump the github-actions group with 2 updates |
| https://github.com/microsoft/TypeScript/pull/62659 | `microsoft/TypeScript` | `code_only` | `typescript` | Fixed a crash when parsing invalid decorator on await expression |
| https://github.com/microsoft/TypeScript/pull/62656 | `microsoft/TypeScript` | `code_only` | `typescript` | Fix TS2783 false positive for union types in object spread expressions |
| https://github.com/microsoft/TypeScript/pull/62642 | `microsoft/TypeScript` | `code_only` | `typescript` | 🤖 Pick PR #62641 (Fix fourslash tests) into tsgo-port |
| https://github.com/microsoft/TypeScript/pull/62641 | `microsoft/TypeScript` | `code_only` | `typescript` | Fix fourslash tests |
| https://github.com/microsoft/TypeScript/pull/62632 | `microsoft/TypeScript` | `code_only` | `typescript` | Bump the github-actions group across 1 directory with 2 updates |
| https://github.com/microsoft/TypeScript/pull/62611 | `microsoft/TypeScript` | `code_only` | `typescript` | add allowJs default value description |
| https://github.com/microsoft/TypeScript/pull/55969 | `microsoft/TypeScript` | `code_only` | `typescript` | Prefer local module specifier over relative node_modules ones in auto-import, even when it reaches into a monorepo package |
| https://github.com/microsoft/TypeScript/pull/63327 | `microsoft/TypeScript` | `code_only` | `typescript` | 🤖 Pick PR #63310 (Mark class property initializers as...) into release-6.0 |
| https://github.com/microsoft/TypeScript/pull/63310 | `microsoft/TypeScript` | `code_only` | `typescript` | Mark class property initializers as outside of CFA containers |
| https://github.com/microsoft/TypeScript/pull/63368 | `microsoft/TypeScript` | `code_only` | `typescript` | Harden ATA package name filtering |
| https://github.com/microsoft/TypeScript/pull/63407 | `microsoft/TypeScript` | `code_only` | `typescript` | 🤖 Pick PR #63401 (Also check package name validity in...) into release-6.0 |
| https://github.com/microsoft/TypeScript/pull/63401 | `microsoft/TypeScript` | `code_only` | `typescript` | Also check package name validity in InstallPackageRequest |
| https://github.com/microsoft/TypeScript/pull/63372 | `microsoft/TypeScript` | `code_only` | `typescript` | 🤖 Pick PR #63368 (Harden ATA package name filtering) into release-6.0 |
| https://github.com/microsoft/TypeScript/pull/61813 | `microsoft/TypeScript` | `code_only` | `typescript` | tsc --init update |
| https://github.com/microsoft/TypeScript/pull/62620 | `microsoft/TypeScript` | `code_only` | `typescript` | Handle more child types when generating navigation tree items for `export default` |
| https://github.com/microsoft/TypeScript/pull/62593 | `microsoft/TypeScript` | `code_only` | `typescript` | Allow line break before import attributes `with` keyword |
| https://github.com/microsoft/TypeScript/pull/62516 | `microsoft/TypeScript` | `code_only_tests_or_fixtures` | `typescript` | Fix: Make discriminant property selection order-independent in unions (#62512) |
| https://github.com/microsoft/TypeScript/pull/62574 | `microsoft/TypeScript` | `code_only_tests_or_fixtures` | `typescript` | Add extra test for extending multiple bases with incompatible optional property under EOPT |
| https://github.com/microsoft/TypeScript/pull/63344 | `microsoft/TypeScript` | `code_only` | `typescript` | Document charCodeAt edge case behavior in first line |
| https://github.com/microsoft/TypeScript/pull/62551 | `microsoft/TypeScript` | `code_only` | `typescript` | Bump the github-actions group with 2 updates |
| https://github.com/microsoft/TypeScript/pull/62549 | `microsoft/TypeScript` | `code_only` | `typescript` | Consistently resolve to the `errorType` on `arguments` with error |
| https://github.com/microsoft/TypeScript/pull/59860 | `microsoft/TypeScript` | `code_only` | `typescript` | Support interpreting non-literal computed properties in classes as implicit index signatures |
| https://github.com/microsoft/TypeScript/pull/62538 | `microsoft/TypeScript` | `code_only` | `typescript` | Update DOM types for FileSystemDirectoryHandle changes |
| https://github.com/microsoft/TypeScript/pull/62522 | `microsoft/TypeScript` | `code_only` | `typescript` | Fix releaser tag creation |
| https://github.com/microsoft/TypeScript/pull/62510 | `microsoft/TypeScript` | `code_only` | `typescript` | Port microsoft/typescript-go#1764 |
| https://github.com/microsoft/TypeScript/pull/62507 | `microsoft/TypeScript` | `code_only` | `typescript` | Bump the github-actions group across 1 directory with 2 updates |
| https://github.com/microsoft/TypeScript/pull/62502 | `microsoft/TypeScript` | `code_only` | `typescript` | Port https://github.com/microsoft/typescript-go/pull/1759 |
| https://github.com/microsoft/TypeScript/pull/62501 | `microsoft/TypeScript` | `code_only` | `typescript` | Port microsoft/typescript-go#1757 |
| https://github.com/microsoft/TypeScript/pull/62465 | `microsoft/TypeScript` | `code_only` | `typescript` | fix(error message): fixes issue in  error message TS1355 |
| https://github.com/microsoft/TypeScript/pull/62440 | `microsoft/TypeScript` | `code_only` | `typescript` | 🤖 Pick PR #62438 (Fix incorrectly ignored dts file fr...) into release-5.9 |
| https://github.com/microsoft/TypeScript/pull/62438 | `microsoft/TypeScript` | `code_only` | `typescript` | Fix incorrectly ignored dts file from project reference for resolution |
| https://github.com/microsoft/TypeScript/pull/62426 | `microsoft/TypeScript` | `code_only` | `typescript` | 🤖 Pick PR #62351 (Add missing Float16Array constructo...) into release-5.9 |
| https://github.com/microsoft/TypeScript/pull/62425 | `microsoft/TypeScript` | `code_only` | `typescript` | 🤖 Pick PR #62423 (Revert PR 61928) into release-5.9 |
| https://github.com/microsoft/TypeScript/pull/62424 | `microsoft/TypeScript` | `code_only` | `typescript` | 🤖 Pick PR #62311 (Fix parenthesizer rules for manuall...) into release-5.9 |
| https://github.com/microsoft/TypeScript/pull/62170 | `microsoft/TypeScript` | `code_only` | `typescript` | Enhance type argument completions |
| https://github.com/microsoft/TypeScript/pull/61683 | `microsoft/TypeScript` | `code_only` | `typescript` | Don't compare "missing" to `undefined` in `compareProperties` under `exactOptionalPropertyTypes` |
| https://github.com/microsoft/TypeScript/pull/39560 | `microsoft/TypeScript` | `code_only` | `typescript` | --noUncheckedIndexedAccess |
| https://github.com/microsoft/TypeScript/pull/63341 | `microsoft/TypeScript` | `code_only` | `typescript` | Fix redundant leading apostrophe in TS1344 diagnostic message |
| https://github.com/microsoft/TypeScript/pull/63319 | `microsoft/TypeScript` | `code_only` | `typescript` | Bump the github-actions group with 2 updates |
| https://github.com/microsoft/TypeScript/pull/63296 | `microsoft/TypeScript` | `code_only` | `typescript` | Update deps |
| https://github.com/microsoft/TypeScript/pull/63285 | `microsoft/TypeScript` | `code_only` | `typescript` | Bump the github-actions group with 3 updates |
| https://github.com/microsoft/TypeScript/pull/62483 | `microsoft/TypeScript` | `code_only` | `typescript` | Disable conditional exports fallbacks on `null` values |
| https://github.com/microsoft/TypeScript/pull/62320 | `microsoft/TypeScript` | `code_only` | `typescript` | Allow `--module commonjs --moduleResolution bundler` |
| https://github.com/microsoft/TypeScript/pull/62844 | `microsoft/TypeScript` | `code_only` | `typescript` | Allow subpath imports that start with `#/` |
| https://github.com/microsoft/TypeScript/pull/57749 | `microsoft/TypeScript` | `code_only` | `typescript` | Report grammar errors for invalid decorator grammar |
| https://github.com/microsoft/TypeScript/pull/63246 | `microsoft/TypeScript` | `code_only` | `typescript` | 🤖 Pick PR #63239 (Fix missing lib files in reused pro...) into release-6.0 |
| https://github.com/microsoft/TypeScript/pull/61079 | `microsoft/TypeScript` | `code_only` | `typescript` | Fix RegExpIndicesArray by adding undefined to type definition |
| https://github.com/microsoft/TypeScript/pull/63224 | `microsoft/TypeScript` | `code_only` | `typescript` | Bump the github-actions group with 2 updates |
| https://github.com/microsoft/TypeScript/pull/63239 | `microsoft/TypeScript` | `code_only` | `typescript` | Fix missing lib files in reused programs |
| https://github.com/microsoft/TypeScript/pull/62411 | `microsoft/TypeScript` | `code_only` | `typescript` | Bump the github-actions group across 1 directory with 4 updates |
| https://github.com/microsoft/TypeScript/pull/62351 | `microsoft/TypeScript` | `code_only` | `typescript` | Add missing Float16Array constructors |
| https://github.com/microsoft/TypeScript/pull/62311 | `microsoft/TypeScript` | `code_only` | `typescript` | Fix parenthesizer rules for manually constructed binary expressions with `??` and `\|\|`/`&&` mix |
| https://github.com/microsoft/TypeScript/pull/61668 | `microsoft/TypeScript` | `code_only` | `typescript` | Fix type variable leaks and cache inconsistencies |
| https://github.com/microsoft/graphrag/pull/2528 | `microsoft/graphrag` | `code_and_docs` | `python` | Cleanup |
| https://github.com/microsoft/graphrag/pull/2523 | `microsoft/graphrag` | `code_only` | `python` | Update dependencies to latest versions (dependency sweep) |
| https://github.com/microsoft/graphrag/pull/2507 | `microsoft/graphrag` | `code_and_docs` | `python` | Automate dependency updates. |
| https://github.com/microsoft/graphrag/pull/2487 | `microsoft/graphrag` | `code_and_docs` | `python` | Pr 2480/docs/spelling sweep |
| https://github.com/microsoft/graphrag/pull/2485 | `microsoft/graphrag` | `code_only` | `python` | Pr 2481/danfiedler/pin actions |
| https://github.com/microsoft/graphrag/pull/2484 | `microsoft/graphrag` | `code_only` | `python` | Fix/cache event loop lifecycle |
| https://github.com/microsoft/graphrag/pull/2434 | `microsoft/graphrag` | `code_only` | `python` | Fix JSONL loader handling of blank/invalid lines |
| https://github.com/microsoft/graphrag/pull/2457 | `microsoft/graphrag` | `code_only` | `python` | Fix cannot release un-acquired lock in Blob logger |
| https://github.com/microsoft/graphrag/pull/2442 | `microsoft/graphrag` | `code_only` | `python` | Issue 2265: Column length mismatch |
| https://github.com/microsoft/graphrag/pull/2443 | `microsoft/graphrag` | `code_only` | `python` | Missing return type hints on generator functions in query/llm/text_utils.py |
| https://github.com/microsoft/graphrag/pull/2431 | `microsoft/graphrag` | `code_only` | `python` | Fix .strip call |
| https://github.com/microsoft/graphrag/pull/2430 | `microsoft/graphrag` | `code_only` | `python` | Loosen service_tier type to str \| None to allow for more flexibility … |
| https://github.com/microsoft/graphrag/pull/2429 | `microsoft/graphrag` | `code_only` | `python` | Fix logging bug. |
| https://github.com/microsoft/graphrag/pull/2366 | `microsoft/graphrag` | `code_and_docs` | `python` | Release v3.1.0 |
| https://github.com/microsoft/graphrag/pull/2354 | `microsoft/graphrag` | `code_and_docs` | `python` | feat: native CosmosTableProvider with namespace partitioning |
| https://github.com/microsoft/graphrag/pull/2321 | `microsoft/graphrag` | `code_and_docs` | `python` | Release v3.0.9 |
| https://github.com/microsoft/graphrag/pull/2306 | `microsoft/graphrag` | `code_only` | `python` | Support client side json validation. |
| https://github.com/microsoft/graphrag/pull/2305 | `microsoft/graphrag` | `code_and_docs` | `python` | Fix broken documentation links. |
| https://github.com/microsoft/graphrag/pull/2299 | `microsoft/graphrag` | `code_and_docs` | `python` | Release v3.0.8 |
| https://github.com/microsoft/graphrag/pull/2298 | `microsoft/graphrag` | `code_only` | `python` | bump nltk to resolve [CVE-2025-14009](https://github.com/advisories/GHSA-7p94-766c-hgjp) |
| https://github.com/microsoft/graphrag/pull/2297 | `microsoft/graphrag` | `code_only` | `python` | bump nltk to resolve [CVE-2025-14009](https://github.com/advisories/GHSA-7p94-766c-hgjp) |
| https://github.com/microsoft/graphrag/pull/2296 | `microsoft/graphrag` | `code_only` | `python` | bump nltk to resolve [CVE-2025-14009](https://github.com/advisories/G… |
| https://github.com/microsoft/graphrag/pull/2291 | `microsoft/graphrag` | `code_and_docs` | `python` | Release v3.0.7 |
| https://github.com/microsoft/graphrag/pull/2290 | `microsoft/graphrag` | `code_only` | `python` | Pin litellm dependency |
| https://github.com/microsoft/graphrag/pull/2281 | `microsoft/graphrag` | `code_only` | `python` | reconfigure vector store size |
| https://github.com/microsoft/graphrag/pull/2267 | `microsoft/graphrag` | `code_and_docs` | `python` | Release v3.0.6 |
| https://github.com/microsoft/graphrag/pull/2264 | `microsoft/graphrag` | `code_only` | `python` | nlp streaming |
| https://github.com/microsoft/graphrag/pull/2261 | `microsoft/graphrag` | `code_only` | `python` | remove relationships with phantom entities |
| https://github.com/microsoft/graphrag/pull/2251 | `microsoft/graphrag` | `code_only` | `python` | vector load_documents in batches |
| https://github.com/microsoft/graphrag/pull/2248 | `microsoft/graphrag` | `code_only` | `python` | fix csv file reader |
| https://github.com/microsoft/graphrag/pull/2247 | `microsoft/graphrag` | `code_and_docs` | `python` | Release v3.0.4 |
| https://github.com/microsoft/graphrag/pull/2244 | `microsoft/graphrag` | `code_only` | `python` | write stats per workflow |
| https://github.com/microsoft/graphrag/pull/2243 | `microsoft/graphrag` | `code_only` | `python` | streaming create_final_documents |
| https://github.com/microsoft/graphrag/pull/2240 | `microsoft/graphrag` | `code_only` | `python` | streaming finalize_graph  |
| https://github.com/microsoft/graphrag/pull/2241 | `microsoft/graphrag` | `code_and_docs` | `python` | generate_text_embeddings streaming |
| https://github.com/microsoft/graphrag/pull/2237 | `microsoft/graphrag` | `code_and_docs` | `python` | Streaming create communities |
| https://github.com/microsoft/graphrag/pull/2235 | `microsoft/graphrag` | `code_and_docs` | `python` | add release doc |
| https://github.com/microsoft/graphrag/pull/2232 | `microsoft/graphrag` | `code_only` | `python` | Cosmosdb communities bug |
| https://github.com/microsoft/graphrag/pull/2229 | `microsoft/graphrag` | `code_only` | `python` | modify smoke tests to include csv table provider |
| https://github.com/microsoft/graphrag/pull/2221 | `microsoft/graphrag` | `code_only` | `python` | load_input_documents and create_base_text_units streaming |
| https://github.com/microsoft/graphrag/pull/2227 | `microsoft/graphrag` | `code_only` | `python` | add memory profiling |
| https://github.com/microsoft/graphrag/pull/2226 | `microsoft/graphrag` | `code_only` | `python` | Add async iterator support to InputReader and use in load workflows |
| https://github.com/microsoft/graphrag/pull/2225 | `microsoft/graphrag` | `code_and_docs` | `python` | Streamline workflows |
| https://github.com/microsoft/graphrag/pull/2220 | `microsoft/graphrag` | `code_only` | `python` | Add DataReader class for typed dataframe loading |
| https://github.com/microsoft/graphrag/pull/2215 | `microsoft/graphrag` | `code_only` | `python` | add csv table provider |
| https://github.com/microsoft/graphrag/pull/2213 | `microsoft/graphrag` | `code_only` | `python` | Remove unnecessary response format check. |
| https://github.com/microsoft/graphrag/pull/2214 | `microsoft/graphrag` | `code_only` | `python` | Table factory |
| https://github.com/microsoft/graphrag/pull/2208 | `microsoft/graphrag` | `code_only` | `python` | Python 3.13 |
| https://github.com/microsoft/graphrag/pull/2195 | `microsoft/graphrag` | `code_and_docs` | `python` | Release v3.0.1 |
| https://github.com/microsoft/graphrag/pull/2193 | `microsoft/graphrag` | `code_only` | `python` | Fix deps |
| https://github.com/microsoft/graphrag/pull/2191 | `microsoft/graphrag` | `code_and_docs` | `python` | Release v3.0.0 |
| https://github.com/microsoft/graphrag/pull/2180 | `microsoft/graphrag` | `code_and_docs` | `python` | Migration update |
| https://github.com/microsoft/graphrag/pull/2188 | `microsoft/graphrag` | `code_only` | `python` | Update Python publish workflow for PyPI |
| https://github.com/microsoft/graphrag/pull/2187 | `microsoft/graphrag` | `code_only` | `python` | Release v2.7.1 |
| https://github.com/microsoft/graphrag/pull/2186 | `microsoft/graphrag` | `code_and_docs` | `python` | Release v2.7.1 |
| https://github.com/microsoft/graphrag/pull/2181 | `microsoft/graphrag` | `code_and_docs` | `python` | Graphrag llm cleanup |
| https://github.com/microsoft/graphrag/pull/2173 | `microsoft/graphrag` | `code_and_docs` | `python` | Update index bug |
| https://github.com/microsoft/graphrag/pull/2161 | `microsoft/graphrag` | `code_only` | `python` | Mismatch between header in community report generation prompt examples and input data (id vs human_readable_id) |
| https://github.com/microsoft/graphrag/pull/2159 | `microsoft/graphrag` | `code_and_docs` | `python` | Issue #2004 fix |
| https://github.com/microsoft/graphrag/pull/2154 | `microsoft/graphrag` | `code_only` | `python` | Fix a bunch of module comments and function visibility |
| https://github.com/microsoft/graphrag/pull/2137 | `microsoft/graphrag` | `code_and_docs` | `python` | Init command asks for models |
| https://github.com/microsoft/graphrag/pull/2133 | `microsoft/graphrag` | `code_only` | `python` | Add empty checks for NLP graphs |
| https://github.com/microsoft/graphrag/pull/2128 | `microsoft/graphrag` | `code_and_docs` | `python` | Remove embeddings optional new |
| https://github.com/microsoft/graphrag/pull/2126 | `microsoft/graphrag` | `code_only` | `python` | Empty graph guards |
| https://github.com/microsoft/graphrag/pull/2120 | `microsoft/graphrag` | `code_and_docs` | `python` | Nov 2025 housekeeping |
| https://github.com/microsoft/graphrag/pull/2118 | `microsoft/graphrag` | `code_only` | `python` | Storage fixes and cleanup |
| https://github.com/microsoft/graphrag/pull/2106 | `microsoft/graphrag` | `code_and_docs` | `python` | Prefix vector store |
| https://github.com/microsoft/graphrag/pull/2100 | `microsoft/graphrag` | `code_and_docs` | `python` | V3 docs and cleanup |
| https://github.com/microsoft/graphrag/pull/2093 | `microsoft/graphrag` | `code_and_docs` | `python` | Remove multi search |
| https://github.com/microsoft/graphrag/pull/2095 | `microsoft/graphrag` | `code_and_docs` | `python` | Remove fnllm |
| https://github.com/microsoft/graphrag/pull/2089 | `microsoft/graphrag` | `code_only` | `python` | reduce schema fields |
| https://github.com/microsoft/graphrag/pull/2084 | `microsoft/graphrag` | `code_only` | `python` | Init config cleanup |
| https://github.com/microsoft/graphrag/pull/2077 | `microsoft/graphrag` | `code_only` | `python` | Clean vector store |
| https://github.com/microsoft/graphrag/pull/2070 | `microsoft/graphrag` | `code_and_docs` | `python` | Docs/2.6.0 |
| https://github.com/microsoft/graphrag/pull/2068 | `microsoft/graphrag` | `code_and_docs` | `python` | Release v2.6.0 |
| https://github.com/microsoft/graphrag/pull/2056 | `microsoft/graphrag` | `code_only` | `python` | Remove community reports rate limiter |
| https://github.com/microsoft/graphrag/pull/2062 | `microsoft/graphrag` | `code_only` | `python` | Custom vector store schema implementation |
| https://github.com/microsoft/graphrag/pull/2063 | `microsoft/graphrag` | `code_only` | `python` | Fix multi-index search |
| https://github.com/microsoft/graphrag/pull/2059 | `microsoft/graphrag` | `code_only` | `python` | Configure async for NLP extraction |
| https://github.com/microsoft/graphrag/pull/2049 | `microsoft/graphrag` | `code_only` | `python` | Re-implement hierarchical Leiden |
| https://github.com/microsoft/graphrag/pull/2052 | `microsoft/graphrag` | `code_and_docs` | `python` | Remove text unit grouping |
| https://github.com/microsoft/graphrag/pull/2050 | `microsoft/graphrag` | `code_and_docs` | `python` | Remove file filtering |
| https://github.com/microsoft/graphrag/pull/2034 | `microsoft/graphrag` | `code_and_docs` | `python` | Input docs API parameter |
| https://github.com/microsoft/graphrag/pull/2036 | `microsoft/graphrag` | `code_only` | `python` | Fix id baseline |
| https://github.com/microsoft/graphrag/pull/2035 | `microsoft/graphrag` | `code_only` | `python` | Selective embeddings loading |
| https://github.com/microsoft/graphrag/pull/2030 | `microsoft/graphrag` | `code_only` | `python` | Logging improvements |
| https://github.com/microsoft/graphrag/pull/2021 | `microsoft/graphrag` | `code_only` | `python` | Feat/additional context |
| https://github.com/microsoft/graphrag/pull/2019 | `microsoft/graphrag` | `code_only` | `python` | Users/snehitgajjar/add optional api param for pipeline state |
| https://github.com/microsoft/graphrag/pull/1994 | `microsoft/graphrag` | `code_and_docs` | `python` | Release v2.4.0 |
| https://github.com/microsoft/graphrag/pull/1993 | `microsoft/graphrag` | `code_only` | `python` | Fix/fnllm embedding limiter defaults |
| https://github.com/microsoft/graphrag/pull/1944 | `microsoft/graphrag` | `code_only` | `python` | Refactor StorageFactory class to use registration functionality |
| https://github.com/microsoft/graphrag/pull/1958 | `microsoft/graphrag` | `code_only` | `python` | Update typer |
| https://github.com/microsoft/graphrag/pull/1951 | `microsoft/graphrag` | `code_and_docs` | `python` | Release v2.3.0 |
| https://github.com/microsoft/graphrag/pull/1948 | `microsoft/graphrag` | `code_only` | `python` | Fix/drift search reduce |
| https://github.com/microsoft/graphrag/pull/1947 | `microsoft/graphrag` | `code_only` | `python` | Task/raw model answer |
| https://github.com/microsoft/graphrag/pull/1942 | `microsoft/graphrag` | `code_only` | `python` | Fix/global reduce prompt |
| https://github.com/microsoft/graphrag/pull/1939 | `microsoft/graphrag` | `code_only` | `python` | Upgrade pyarrow dependency to >=17.0.0 to fix CVE-2024-52338 |
| https://github.com/microsoft/graphrag/pull/1941 | `microsoft/graphrag` | `code_only` | `python` | Task/remove dynamic retries |
| https://github.com/microsoft/graphrag/pull/1932 | `microsoft/graphrag` | `code_and_docs` | `python` | Various minor updates |
| https://github.com/microsoft/graphrag/pull/1930 | `microsoft/graphrag` | `code_only` | `python` | Update to latest fnllm |
| https://github.com/microsoft/graphrag/pull/1910 | `microsoft/graphrag` | `code_and_docs` | `python` | Release v2.2.1 |
| https://github.com/microsoft/graphrag/pull/1909 | `microsoft/graphrag` | `code_only` | `python` | Fix/community report tuning |
| https://github.com/microsoft/graphrag/pull/1908 | `microsoft/graphrag` | `code_only` | `python` | Update Index as workflows |
| https://github.com/microsoft/graphrag/pull/1905 | `microsoft/graphrag` | `code_only` | `python` | Fix graph creation |
| https://github.com/microsoft/graphrag/pull/1842 | `microsoft/graphrag` | `code_and_docs` | `python` | Docs: Add models page |
| https://github.com/microsoft/graphrag/pull/1897 | `microsoft/graphrag` | `code_and_docs` | `python` | Release/v2.2.0 |
| https://github.com/microsoft/graphrag/pull/1890 | `microsoft/graphrag` | `code_only` | `python` | Optional embeddings |
| https://github.com/microsoft/graphrag/pull/1888 | `microsoft/graphrag` | `code_and_docs` | `python` | NLP graph parity |
| https://github.com/microsoft/graphrag/pull/1889 | `microsoft/graphrag` | `code_only` | `python` | Snapshot full graph |
| https://github.com/microsoft/graphrag/pull/1893 | `microsoft/graphrag` | `code_only` | `python` | Fix/minor query fixes |
| https://github.com/microsoft/graphrag/pull/1874 | `microsoft/graphrag` | `code_only` | `python` | Update .vsts-ci.yml |
| https://github.com/microsoft/graphrag/pull/1873 | `microsoft/graphrag` | `code_only` | `python` | fix yaml path in unified-search-app |
| https://github.com/microsoft/graphrag/pull/1869 | `microsoft/graphrag` | `code_only` | `python` | add vsts deploy file for unified search app |
| https://github.com/microsoft/graphrag/pull/1856 | `microsoft/graphrag` | `code_only` | `python` | Vector Store Integration Tests |
| https://github.com/microsoft/graphrag/pull/1826 | `microsoft/graphrag` | `code_only` | `python` | Gnievesponce prompt tune embedd chunking |
| https://github.com/microsoft/graphrag/pull/405 | `microsoft/graphrag` | `code_and_docs` | `python` | [bug fix]Fix community_report config doesn't work in settings.yaml |
| https://github.com/microsoft/graphrag/pull/1368 | `microsoft/graphrag` | `code_only` | `python` | [bugfix]Fix query error with --streaming |
| https://github.com/microsoft/graphrag/pull/1777 | `microsoft/graphrag` | `code_only` | `python` | Support JSON input files |
| https://github.com/microsoft/graphrag/pull/1835 | `microsoft/graphrag` | `code_only` | `python` | fnllm version fix |
| https://github.com/microsoft/graphrag/pull/1818 | `microsoft/graphrag` | `code_and_docs` | `python` | Update config docs (2.1.0) |
| https://github.com/microsoft/graphrag/pull/1821 | `microsoft/graphrag` | `code_only` | `python` | Fix  API key reference for gh-pages |
| https://github.com/microsoft/graphrag/pull/1784 | `microsoft/graphrag` | `code_and_docs` | `python` | Add docs page about input formats |
| https://github.com/microsoft/graphrag/pull/1800 | `microsoft/graphrag` | `code_and_docs` | `python` | Release v2.1.0 |
| https://github.com/microsoft/graphrag/pull/1799 | `microsoft/graphrag` | `code_only` | `python` | Fix/model provider key injection check |
| https://github.com/microsoft/graphrag/pull/1789 | `microsoft/graphrag` | `code_only` | `python` | Added support for verbose logging and csv-metadata to the prompt tune… |
| https://github.com/microsoft/graphrag/pull/1773 | `microsoft/graphrag` | `code_only_tests_or_fixtures` | `python` | Add more verb tests |
| https://github.com/microsoft/graphrag/pull/1771 | `microsoft/graphrag` | `code_only` | `python` | Remove spacy model from toml |
| https://github.com/microsoft/graphrag/pull/1769 | `microsoft/graphrag` | `code_and_docs` | `python` | Release v2.0.0 |
| https://github.com/microsoft/graphrag/pull/1768 | `microsoft/graphrag` | `code_only` | `python` | Fix summarization and relationship grouping on Inc Indexing |
| https://github.com/microsoft/graphrag/pull/1729 | `microsoft/graphrag` | `code_only` | `python` | Pipeline callbacks |
| https://github.com/microsoft/graphrag/pull/1736 | `microsoft/graphrag` | `code_only` | `python` | Speed up smoke tests |
| https://github.com/microsoft/graphrag/pull/1766 | `microsoft/graphrag` | `code_and_docs` | `python` | Incremental model alignment |
| https://github.com/microsoft/graphrag/pull/1738 | `microsoft/graphrag` | `code_only` | `python` | Update FNLLM |
| https://github.com/microsoft/graphrag/pull/1737 | `microsoft/graphrag` | `code_only` | `python` | Move embeddings snapshots |
| https://github.com/microsoft/graphrag/pull/1734 | `microsoft/graphrag` | `code_only` | `python` | Fix text unit incremental ID updates |
| https://github.com/microsoft/graphrag/pull/1730 | `microsoft/graphrag` | `code_only` | `python` | Fix StopAsyncIteration catch |
| https://github.com/microsoft/graphrag/pull/1723 | `microsoft/graphrag` | `code_only` | `python` | Refactor config defaults |
| https://github.com/microsoft/graphrag/pull/1721 | `microsoft/graphrag` | `code_only` | `python` | Query callbacks |
| https://github.com/microsoft/graphrag/pull/1720 | `microsoft/graphrag` | `code_only` | `python` | Tuck flow functions under their workflows |
| https://github.com/microsoft/graphrag/pull/1713 | `microsoft/graphrag` | `code_only` | `python` | Fix/json mode community reports |
| https://github.com/microsoft/graphrag/pull/1691 | `microsoft/graphrag` | `code_only` | `python` | Register workflows |
| https://github.com/microsoft/graphrag/pull/1704 | `microsoft/graphrag` | `code_and_docs` | `python` | Community children |
| https://github.com/microsoft/graphrag/pull/1696 | `microsoft/graphrag` | `code_only` | `python` | Incremental flow rework |
| https://github.com/microsoft/graphrag/pull/1708 | `microsoft/graphrag` | `code_only` | `python` | Chore/remove iterrows |
| https://github.com/microsoft/graphrag/pull/1690 | `microsoft/graphrag` | `code_and_docs` | `python` | Cleanup query api - remove code duplication |
| https://github.com/microsoft/graphrag/pull/1697 | `microsoft/graphrag` | `code_only` | `python` | Export NLP community reports prompt |
| https://github.com/microsoft/graphrag/pull/1681 | `microsoft/graphrag` | `code_only` | `python` | add option to add metadata into text chunks |
| https://github.com/microsoft/graphrag/pull/1694 | `microsoft/graphrag` | `code_only` | `python` | Fix/streamline workflow miq bugs |
| https://github.com/microsoft/graphrag/pull/1689 | `microsoft/graphrag` | `code_only` | `python` | Nlp cache |
| https://github.com/microsoft/graphrag/pull/1675 | `microsoft/graphrag` | `code_only` | `python` | Multi-index query CLI support |
| https://github.com/microsoft/graphrag/pull/1676 | `microsoft/graphrag` | `code_only` | `python` | Fix/drift n depth |
| https://github.com/microsoft/graphrag/pull/1672 | `microsoft/graphrag` | `code_only` | `python` | remove unused columns and rename document_attribute_columns  |
| https://github.com/microsoft/graphrag/pull/1669 | `microsoft/graphrag` | `code_only` | `python` | Fix recursive report generation |
| https://github.com/microsoft/graphrag/pull/1667 | `microsoft/graphrag` | `code_only` | `python` | Add generate_text_embeddings to FGR |
| https://github.com/microsoft/graphrag/pull/1665 | `microsoft/graphrag` | `code_only` | `python` | Require explicit azure auth settings when using AOI. |
| https://github.com/microsoft/graphrag/pull/1662 | `microsoft/graphrag` | `code_only` | `python` | Add vector store id reference to embeddings config. |
| https://github.com/microsoft/graphrag/pull/1644 | `microsoft/graphrag` | `code_only` | `python` | Multi-index querying for API layer |
| https://github.com/microsoft/graphrag/pull/1658 | `microsoft/graphrag` | `code_only_tests_or_fixtures` | `python` | Add smoke tests for drift |
| https://github.com/microsoft/graphrag/pull/1645 | `microsoft/graphrag` | `code_only` | `python` | Fix DRIFT search on Azure AI Search |
| https://github.com/microsoft/graphrag/pull/1625 | `microsoft/graphrag` | `code_and_docs` | `python` | Release v1.2.0 |
| https://github.com/microsoft/graphrag/pull/1624 | `microsoft/graphrag` | `code_only` | `python` | Reduce Drift Response and Streaming endpoint |
| https://github.com/microsoft/graphrag/pull/1587 | `microsoft/graphrag` | `code_only` | `python` | Implement CosmosDB vector store |
| https://github.com/microsoft/graphrag/pull/1547 | `microsoft/graphrag` | `code_only` | `python` | Test and unify text splitter functionality |
| https://github.com/microsoft/graphrag/pull/1611 | `microsoft/graphrag` | `code_only` | `python` | Limiter defaults |
| https://github.com/microsoft/graphrag/pull/1607 | `microsoft/graphrag` | `code_and_docs` | `python` | Release/v1.1.2 |
| https://github.com/microsoft/graphrag/pull/1606 | `microsoft/graphrag` | `code_only` | `python` | fix basic search minor bug |
| https://github.com/microsoft/graphrag/pull/1595 | `microsoft/graphrag` | `code_and_docs` | `python` | Release v1.1.1 |
| https://github.com/microsoft/graphrag/pull/1591 | `microsoft/graphrag` | `code_only` | `python` | Fix/dynamic search hierarchy maps |
| https://github.com/microsoft/graphrag/pull/1589 | `microsoft/graphrag` | `code_only` | `python` | Chore/increase search community prop def |
| https://github.com/microsoft/graphrag/pull/1588 | `microsoft/graphrag` | `code_and_docs` | `python` | Release v1.1.0 |
| https://github.com/microsoft/graphrag/pull/1582 | `microsoft/graphrag` | `code_only` | `python` | Fix storage class instantiation |
| https://github.com/microsoft/graphrag/pull/1579 | `microsoft/graphrag` | `code_only` | `python` | Bump ruff from 0.8.4 to 0.8.5 |
| https://github.com/microsoft/graphrag/pull/1570 | `microsoft/graphrag` | `code_only` | `python` | Remove config input models |
| https://github.com/microsoft/graphrag/pull/1563 | `microsoft/graphrag` | `code_only` | `python` | Basic search implementation |
| https://github.com/microsoft/graphrag/pull/1569 | `microsoft/graphrag` | `code_only` | `python` | Chore/gleanings any encoding |
| https://github.com/microsoft/graphrag/pull/1564 | `microsoft/graphrag` | `code_only` | `python` | Fix/gleanings loop |
| https://github.com/microsoft/graphrag/pull/1507 | `microsoft/graphrag` | `code_only` | `python` | Solved graphrag index can't use other llm problem |
| https://github.com/microsoft/graphrag/pull/1431 | `microsoft/graphrag` | `code_and_docs` | `python` | Add Cosmos DB storage/cache option |
| https://github.com/microsoft/graphrag/pull/1510 | `microsoft/graphrag` | `code_only` | `python` | Flow cleanup |
| https://github.com/microsoft/graphrag/pull/1534 | `microsoft/graphrag` | `code_and_docs` | `python` | Release v1.0.1 |
| https://github.com/microsoft/tsdoc/pull/477 | `microsoft/tsdoc` | `code_only` | `typescript` | Pin GitHub Actions to full-length commit SHAs |
| https://github.com/microsoft/tsdoc/pull/443 | `microsoft/tsdoc` | `code_only` | `typescript` | feat(tsdoc): Don't replace line breaks when emitting comments |
| https://github.com/microsoft/tsdoc/pull/465 | `microsoft/tsdoc` | `code_only` | `typescript` | Update Rush and replace record-versions with Rush plugin |
| https://github.com/microsoft/tsdoc/pull/462 | `microsoft/tsdoc` | `code_and_docs` | `typescript` | Bump versions. |
| https://github.com/microsoft/tsdoc/pull/461 | `microsoft/tsdoc` | `code_only` | `typescript` | fix(eslint-plugin-tsdoc): replace deprecated ESLint APIs for v10 compatibility |
| https://github.com/microsoft/tsdoc/pull/459 | `microsoft/tsdoc` | `code_only` | `typescript` | Bump rushstack dependencies. |
| https://github.com/microsoft/tsdoc/pull/460 | `microsoft/tsdoc` | `code_only` | `typescript` | Update post-publish.yaml scripts and paths |
| https://github.com/microsoft/tsdoc/pull/458 | `microsoft/tsdoc` | `code_and_docs` | `typescript` | Bump verisons. |
| https://github.com/microsoft/tsdoc/pull/456 | `microsoft/tsdoc` | `code_only` | `typescript` | fix(deps): bump ajv to v8.18.0 |
| https://github.com/microsoft/tsdoc/pull/457 | `microsoft/tsdoc` | `code_only` | `typescript` | fix(deps): upgrade @typescript-eslint/utils to fix minimatch vulnerability |
| https://github.com/microsoft/tsdoc/pull/177 | `microsoft/tsdoc` | `code_only` | `typescript` | Improve parse for module sources |
| https://github.com/microsoft/tsdoc/pull/451 | `microsoft/tsdoc` | `code_and_docs` | `typescript` | Bump versions |
| https://github.com/microsoft/tsdoc/pull/452 | `microsoft/tsdoc` | `code_only` | `typescript` | Fix publishing. |
| https://github.com/microsoft/tsdoc/pull/448 | `microsoft/tsdoc` | `code_and_docs` | `typescript` | Handle TS buit-in @jsx* directives. |
| https://github.com/microsoft/tsdoc/pull/449 | `microsoft/tsdoc` | `code_only` | `typescript` | Collect JSON Schemas during publish. |
| https://github.com/microsoft/tsdoc/pull/445 | `microsoft/tsdoc` | `code_only` | `typescript` | Do not include tests and typescript declaration mappings in package |
| https://github.com/microsoft/tsdoc/pull/441 | `microsoft/tsdoc` | `code_only` | `typescript` | Reorder TSDoc comments to match HTML rendering for clarity |
| https://github.com/microsoft/tsdoc/pull/427 | `microsoft/tsdoc` | `code_only` | `typescript` | The content after @defaultValue should remain on the same line |
| https://github.com/microsoft/tsdoc/pull/432 | `microsoft/tsdoc` | `code_only` | `typescript` | Bump cross-spawn from 7.0.3 to 7.0.6 in /common/autoinstallers/rush-prettier |
| https://github.com/microsoft/tsdoc/pull/430 | `microsoft/tsdoc` | `code_only` | `typescript` | Bump dependencies. |
| https://github.com/microsoft/tsdoc/pull/433 | `microsoft/tsdoc` | `code_only` | `typescript` | Trim the test matrix. |
| https://github.com/microsoft/tsdoc/pull/431 | `microsoft/tsdoc` | `code_only` | `typescript` | Bump RushStack dependencies and expand test matrix. |
| https://github.com/microsoft/tsdoc/pull/429 | `microsoft/tsdoc` | `code_only` | `typescript` | [eslint-plugin-tsdoc] Leverage tsConfigRootDir setting |
| https://github.com/microsoft/tsdoc/pull/420 | `microsoft/tsdoc` | `code_only` | `typescript` | Include CHANGELOG.md in published releases again |
| https://github.com/microsoft/tsdoc/pull/419 | `microsoft/tsdoc` | `code_only` | `typescript` | Bundle react, react-dom, and Monaco. |
| https://github.com/microsoft/tsdoc/pull/330 | `microsoft/tsdoc` | `code_only` | `typescript` | Clean up some functional components. |
| https://github.com/microsoft/tsdoc/pull/386 | `microsoft/tsdoc` | `code_only` | `typescript` | Fix one more publishing issue. |
| https://github.com/microsoft/tsdoc/pull/385 | `microsoft/tsdoc` | `code_only` | `typescript` | Fix an issue with playground build. |
| https://github.com/microsoft/tsdoc/pull/384 | `microsoft/tsdoc` | `code_only` | `typescript` | Fix playground publish. |
| https://github.com/microsoft/tsdoc/pull/383 | `microsoft/tsdoc` | `code_only` | `typescript` | Include a missing option. |
| https://github.com/microsoft/tsdoc/pull/382 | `microsoft/tsdoc` | `code_only` | `typescript` | Refactor AzDO pipelines. |
| https://github.com/microsoft/tsdoc/pull/381 | `microsoft/tsdoc` | `code_only` | `typescript` | Update the node supported version range. |
| https://github.com/microsoft/tsdoc/pull/380 | `microsoft/tsdoc` | `code_only` | `typescript` | Use GitHub CI. |
| https://github.com/microsoft/tsdoc/pull/373 | `microsoft/tsdoc` | `code_only` | `typescript` | Fix an issue where the selected tab isn't selectable via keyboard navigation. |
| https://github.com/microsoft/tsdoc/pull/358 | `microsoft/tsdoc` | `code_and_docs` | `typescript` | Update an image URL that changed during the Docusaurus migration |
| https://github.com/microsoft/tsdoc/pull/352 | `microsoft/tsdoc` | `code_only` | `typescript` | Fix issues with publishing to the gh-pages branch. |
| https://github.com/microsoft/tsdoc/pull/351 | `microsoft/tsdoc` | `code_only` | `typescript` | Convert the TSDoc Playground to be loadable as an iframe |
| https://github.com/microsoft/tsdoc/pull/339 | `microsoft/tsdoc` | `code_only` | `typescript` | Fix duplicated react element key in playground |
| https://github.com/microsoft/tsdoc/pull/334 | `microsoft/tsdoc` | `code_only` | `typescript` | Fixed Sev2 accessibility bugs for TSDoc Playground |
| https://github.com/microsoft/tsdoc/pull/329 | `microsoft/tsdoc` | `code_only` | `typescript` | Fix an accessability issue where a user can't keyboard-navigate out of the code editor. |
| https://github.com/microsoft/tsdoc/pull/328 | `microsoft/tsdoc` | `code_only` | `typescript` | Change import path to avoid circular reference |
| https://github.com/microsoft/tsdoc/pull/327 | `microsoft/tsdoc` | `code_only` | `typescript` | Fix circular reference by type import |
| https://github.com/microsoft/tsdoc/pull/326 | `microsoft/tsdoc` | `code_only` | `typescript` | Accessibility fix to set correct role on playground tabs |
| https://github.com/microsoft/tsdoc/pull/319 | `microsoft/tsdoc` | `code_and_docs` | `typescript` | Rename master to main. |
| https://github.com/microsoft/tsdoc/pull/318 | `microsoft/tsdoc` | `code_and_docs` | `typescript` | Improve presentation of "illustrative purposes" notice |
| https://github.com/microsoft/tsdoc/pull/317 | `microsoft/tsdoc` | `code_and_docs` | `typescript` | Add allowlist for HTML tags and corresponding validation |
| https://github.com/microsoft/tsdoc/pull/310 | `microsoft/tsdoc` | `code_only` | `typescript` | [playground] Add TSDoc parsing, banner |
| https://github.com/microsoft/tsdoc/pull/306 | `microsoft/tsdoc` | `code_and_docs` | `typescript` | [tsdoc] remove "const" keyword before enum to use with typescript isolatedModules |
| https://github.com/microsoft/tsdoc/pull/303 | `microsoft/tsdoc` | `code_only` | `typescript` | Address accessibility bugs |
| https://github.com/microsoft/tsdoc/pull/291 | `microsoft/tsdoc` | `code_only` | `typescript` | Upgrade to Rush 5.44.0 |
| https://github.com/microsoft/tsdoc/pull/290 | `microsoft/tsdoc` | `code_only` | `typescript` | More error handling improvements |
| https://github.com/microsoft/tsdoc/pull/289 | `microsoft/tsdoc` | `code_and_docs` | `typescript` | Improve error reporting for tsdoc.json issues |
| https://github.com/microsoft/tsdoc/pull/288 | `microsoft/tsdoc` | `code_only` | `typescript` | Add TSDocConfigFile.loadFromObject() |
| https://github.com/microsoft/tsdoc/pull/279 | `microsoft/tsdoc` | `code_only` | `typescript` | Add a new tsdoc.json setting "noStandardTags" |
| https://github.com/microsoft/tsdoc/pull/278 | `microsoft/tsdoc` | `code_and_docs` | `typescript` | Enable API Extractor and fix some syntax issues identified by it |
| https://github.com/microsoft/tsdoc/pull/277 | `microsoft/tsdoc` | `code_only` | `typescript` | Add "supportForTags" field to tsdoc.json schema |
| https://github.com/microsoft/tsdoc/pull/273 | `microsoft/tsdoc` | `code_only` | `typescript` | Add a missing .d.ts file |
| https://github.com/microsoft/tsdoc/pull/272 | `microsoft/tsdoc` | `code_only` | `typescript` | Add a "@decorator" tag definition (RFC 271) |
| https://github.com/microsoft/tsdoc/pull/270 | `microsoft/tsdoc` | `code_and_docs` | `typescript` | Update documentation to reference https://tsdoc.org |
| https://github.com/microsoft/tsdoc/pull/269 | `microsoft/tsdoc` | `code_only` | `typescript` | Integrate TSDoc Playground into https://tsdoc.org/play template |
| https://github.com/microsoft/tsdoc/pull/268 | `microsoft/tsdoc` | `code_only` | `typescript` | Add ESLint as a dev dependency |
| https://github.com/microsoft/tsdoc/pull/261 | `microsoft/tsdoc` | `code_only` | `typescript` | Fix typo |
| https://github.com/microsoft/tsdoc/pull/260 | `microsoft/tsdoc` | `code_only` | `typescript` | Upgrade ESLint rules |
| https://github.com/microsoft/tsdoc/pull/259 | `microsoft/tsdoc` | `code_only` | `typescript` | Fix an issue where line extractor sometimes incorrectly trimmed a non-whitespace character |
| https://github.com/microsoft/tsdoc/pull/255 | `microsoft/tsdoc` | `code_only` | `typescript` | Upgrade to Heft 0.8.0 |
| https://github.com/microsoft/tsdoc/pull/254 | `microsoft/tsdoc` | `code_only` | `typescript` | eslint-plugin-tsdoc: Reenable unit tests |
| https://github.com/microsoft/tsdoc/pull/252 | `microsoft/tsdoc` | `code_only` | `typescript` | Upgrade build tools |
| https://github.com/microsoft/tsdoc/pull/249 | `microsoft/tsdoc` | `code_only` | `typescript` | Bump ajv dependency to ~6.12.3 |
| https://github.com/microsoft/tsdoc/pull/247 | `microsoft/tsdoc` | `code_only` | `typescript` | Upgrade ESLint and Rush |
| https://github.com/microsoft/tsdoc/pull/236 | `microsoft/tsdoc` | `code_only` | `typescript` | Add support for the `@see` tag |
| https://github.com/microsoft/tsdoc/pull/238 | `microsoft/tsdoc` | `code_and_docs` | `typescript` | Fix typo in README.md |
| https://github.com/microsoft/tsdoc/pull/232 | `microsoft/tsdoc` | `code_only` | `typescript` | Clarify the behavior of @inheritDoc |
| https://github.com/microsoft/tsdoc/pull/233 | `microsoft/tsdoc` | `code_only` | `typescript` | Upgrade Rush |
| https://github.com/microsoft/tsdoc/pull/212 | `microsoft/tsdoc` | `code_only` | `typescript` | Add tsdoc-characters-after-block-tag in allTsdocMessageIds |
| https://github.com/microsoft/tsdoc/pull/221 | `microsoft/tsdoc` | `code_only` | `typescript` | eslint-plugin-tsdoc: set docs url to eslint-plugin/README.md |
| https://github.com/microsoft/tsdoc/pull/225 | `microsoft/tsdoc` | `code_only` | `typescript` | Fix an issue where "h1" was not allowed as an HTML element name |
| https://github.com/microsoft/tsdoc/pull/222 | `microsoft/tsdoc` | `code_only` | `typescript` | Update dependencies |
| https://github.com/microsoft/tsdoc/pull/218 | `microsoft/tsdoc` | `code_only` | `typescript` | Improve parsing of JSDoc optional parameter declarations |
| https://github.com/microsoft/tsdoc/pull/206 | `microsoft/tsdoc` | `code_only` | `typescript` | Flexible parsing of param/typeParam |
| https://github.com/microsoft/tsdoc/pull/217 | `microsoft/tsdoc` | `code_only` | `typescript` | Upgrade handlebars |
| https://github.com/microsoft/tsdoc/pull/210 | `microsoft/tsdoc` | `code_only` | `typescript` | eslint-plugin-tsdoc: Use a cache to avoid reloading tsdoc.json |
| https://github.com/microsoft/tsdoc/pull/195 | `microsoft/tsdoc` | `code_only` | `typescript` | eslint-plugin-tsdoc: Avoid importing internal API |
| https://github.com/microsoft/tsdoc/pull/194 | `microsoft/tsdoc` | `code_only` | `typescript` | eslint-plugin-tsdoc: A couple minor improvements |
| https://github.com/microsoft/tsdoc/pull/193 | `microsoft/tsdoc` | `code_only` | `typescript` | Fix the publishing pipeline |
| https://github.com/microsoft/tsdoc/pull/192 | `microsoft/tsdoc` | `code_and_docs` | `typescript` | Enable publishing for eslint-plugin-tsdoc |
| https://github.com/microsoft/tsdoc/pull/190 | `microsoft/tsdoc` | `code_only` | `typescript` | Addition of eslint plugin |
| https://github.com/microsoft/tsdoc/pull/189 | `microsoft/tsdoc` | `code_only` | `typescript` | Fix issue with ESLint command on Mac |
| https://github.com/microsoft/tsdoc/pull/188 | `microsoft/tsdoc` | `code_only` | `typescript` | Update ESLint dependencies |
| https://github.com/microsoft/tsdoc/pull/187 | `microsoft/tsdoc` | `code_only` | `typescript` | Typo |
| https://github.com/microsoft/tsdoc/pull/183 | `microsoft/tsdoc` | `code_only` | `typescript` | Fix an invalid regular expression. |
| https://github.com/microsoft/tsdoc/pull/173 | `microsoft/tsdoc` | `code_only` | `typescript` | Adds ':call', ':new', and ':index' and fixes a parsing bug. |
| https://github.com/microsoft/tsdoc/pull/175 | `microsoft/tsdoc` | `code_only` | `typescript` | Add a definition for the `@throws` block tag |
| https://github.com/microsoft/tsdoc/pull/172 | `microsoft/tsdoc` | `code_only` | `typescript` | Add DeclarationReference beta implementation |
| https://github.com/microsoft/tsdoc/pull/155 | `microsoft/tsdoc` | `code_only` | `typescript` | Change year in footer |
| https://github.com/microsoft/tsdoc/pull/162 | `microsoft/tsdoc` | `code_only_tests_or_fixtures` | `typescript` | Remove invalid label from interface member |
| https://github.com/microsoft/tsdoc/pull/158 | `microsoft/tsdoc` | `code_only` | `typescript` | Improve the wording of error messages related to tag syntax |
| https://github.com/microsoft/tsdoc/pull/149 | `microsoft/tsdoc` | `code_only` | `typescript` | Fix an issue where tsdoc-param-tag-with-invalid-name was incorrectly reported |
| https://github.com/microsoft/tsdoc/pull/150 | `microsoft/tsdoc` | `code_only` | `typescript` | Creating publishing pipeline. |
| https://github.com/microsoft/tsdoc/pull/146 | `microsoft/tsdoc` | `code_only` | `typescript` | Add new API TSDocConfiguration.isKnownMessageId() |
| https://github.com/microsoft/tsdoc/pull/145 | `microsoft/tsdoc` | `code_only` | `typescript` | Introduce message IDs for selective suppressing of TSDoc parser errors, as well as lookups |
| https://github.com/microsoft/tsdoc/pull/143 | `microsoft/tsdoc` | `code_only` | `typescript` | Creating playground master build. |
| https://github.com/microsoft/tsdoc/pull/142 | `microsoft/tsdoc` | `code_and_docs` | `typescript` | Use VSTS CI and GitHub "CODEOWNERS" file |
| https://github.com/microsoft/tsdoc/pull/141 | `microsoft/tsdoc` | `code_only` | `typescript` | Add support for `$` character in identifiers |
| https://github.com/microsoft/tsdoc/pull/133 | `microsoft/tsdoc` | `code_only` | `typescript` | Add IStringBuilder interface |
| https://github.com/microsoft/tsdoc/pull/132 | `microsoft/tsdoc` | `code_only` | `typescript` | Add a new API PlainTextEmitter.hasAnyTextContent() |
| https://github.com/microsoft/tsdoc/pull/129 | `microsoft/tsdoc` | `code_only` | `typescript` | Improve trimming of spacing for link text in @link tags |
| https://github.com/microsoft/tsdoc/pull/127 | `microsoft/tsdoc` | `code_only` | `typescript` | Some miscellaneous minor fixes |
| https://github.com/microsoft/tsdoc/pull/125 | `microsoft/tsdoc` | `code_only` | `typescript` | Change DocErrorText organization in tree, add emit helpers for HTML and declaration references |
| https://github.com/microsoft/tsdoc/pull/124 | `microsoft/tsdoc` | `code_only` | `typescript` |  Introduce DocParamCollection node to support efficient lookup of @param blocks |
| https://github.com/microsoft/tsdoc/pull/121 | `microsoft/tsdoc` | `code_only` | `typescript` | Upgrade tooling dependencies |
| https://github.com/microsoft/tsdoc/pull/119 | `microsoft/tsdoc` | `code_only` | `typescript` | Fix issue where `DocErrorText.text` returned `[object Object]` instead of the text |
| https://github.com/microsoft/tsdoc/pull/113 | `microsoft/tsdoc` | `code_only` | `typescript` | Fix stack overflow in DocFencedCode.language property getter |
| https://github.com/microsoft/tsdoc/pull/112 | `microsoft/tsdoc` | `code_only` | `typescript` | Fix a regression where the paragraph splitter was sometimes skipping blocks |
| https://github.com/microsoft/tsdoc/pull/111 | `microsoft/tsdoc` | `code_only` | `typescript` | Fix build script |
| https://github.com/microsoft/tsdoc/pull/109 | `microsoft/tsdoc` | `code_only` | `typescript` | Change DocNode to have a section property rather than inheriting from DocSection |
| https://github.com/microsoft/tsdoc/pull/102 | `microsoft/tsdoc` | `code_only` | `typescript` | [playground] Including an option to select the editor theme. |
| https://github.com/microsoft/tsdoc/pull/100 | `microsoft/tsdoc` | `code_only` | `typescript` | [playground] Add a sample selector |
| https://github.com/microsoft/tsdoc/pull/106 | `microsoft/tsdoc` | `code_only` | `typescript` | Playground: Fix accessibility errors due to input controls missing labels |
| https://github.com/microsoft/tsdoc/pull/62 | `microsoft/tsdoc` | `code_only` | `typescript` | tests: test Node.js 8 and 10 |
| https://github.com/microsoft/tsdoc/pull/105 | `microsoft/tsdoc` | `code_and_docs` | `typescript` | Update README.md and CONTRIBUTING.md |
| https://github.com/microsoft/tsdoc/pull/103 | `microsoft/tsdoc` | `code_only` | `typescript` | Fix <pre> overflow in flex container |
| https://github.com/microsoft/tsdoc/pull/101 | `microsoft/tsdoc` | `code_only` | `typescript` | [playground] Highlighting package names and paths in declaration links. |
| https://github.com/microsoft/tsdoc/pull/98 | `microsoft/tsdoc` | `code_only` | `typescript` | Fixes a11y error due to missing label for errors pane |
| https://github.com/microsoft/tsdoc/pull/97 | `microsoft/tsdoc` | `code_only` | `typescript` | [playground] Clean up the page layout and add a header |
| https://github.com/microsoft/tsdoc/pull/91 | `microsoft/tsdoc` | `code_only` | `typescript` | [playground] Add "DOM" tab and fix Monaco layout |
| https://github.com/microsoft/tsdoc/pull/84 | `microsoft/tsdoc` | `code_only` | `typescript` | [playground] Fix tsdoc resolution |
| https://github.com/microsoft/tsdoc/pull/86 | `microsoft/tsdoc` | `code_only` | `typescript` | [playground] Extract playground initial sample code into a *.ts file |
| https://github.com/microsoft/tsdoc/pull/87 | `microsoft/tsdoc` | `code_only` | `typescript` | [playground] Add "HTML" and "Lines" tabs |
| https://github.com/microsoft/tsdoc/pull/92 | `microsoft/tsdoc` | `code_only` | `typescript` | [playground] Include squiggly lines for TSDoc errors. |
| https://github.com/microsoft/tsdoc/pull/94 | `microsoft/tsdoc` | `code_only` | `typescript` | [playground] Remove empty DIVs by using React.Fragment & paddingTop |
| https://github.com/microsoft/tsdoc/pull/96 | `microsoft/tsdoc` | `code_only` | `typescript` | [playground] Open default browser on npm start |
| https://github.com/microsoft/tsdoc/pull/82 | `microsoft/tsdoc` | `code_and_docs` | `typescript` | Improve error reporting for declaration references that are probably missing a `"#"` delimiter |
| https://github.com/microsoft/tsdoc/pull/81 | `microsoft/tsdoc` | `code_and_docs` | `typescript` | Rename DocCodeFence to DocFencedCode |
| https://github.com/microsoft/tsdoc/pull/80 | `microsoft/tsdoc` | `code_and_docs` | `typescript` | Implement warnings for undefined/unused tags, plus some other fixes |
| https://github.com/microsoft/tsdoc/pull/78 | `microsoft/tsdoc` | `code_and_docs` | `typescript` | Add support for @defaultValue and @typeParam |
| https://github.com/microsoft/tsdoc/pull/71 | `microsoft/tsdoc` | `code_only_tests_or_fixtures` | `typescript` | [spec] Change declaration reference notation to accommodate ECMAScript 6 symbols |
| https://github.com/microsoft/tsdoc/pull/76 | `microsoft/tsdoc` | `code_and_docs` | `typescript` | Add support for the @inheritDoc tag |
| https://github.com/microsoft/tsdoc/pull/74 | `microsoft/tsdoc` | `code_only` | `typescript` | Parsing of @link tags: URL destinations (part 1 of 2) |
| https://github.com/microsoft/tsdoc/pull/59 | `microsoft/tsdoc` | `code_and_docs` | `typescript` | Improve api-demo's strategy for discovering doc comments |
| https://github.com/microsoft/tsdoc/pull/61 | `microsoft/tsdoc` | `code_and_docs` | `typescript` | Add trimSpacesInParagraphNodes() transform |
| https://github.com/microsoft/tsdoc/pull/69 | `microsoft/tsdoc` | `code_only` | `typescript` | Convert DocNode subclasses to be mutable |
| https://github.com/microsoft/tsdoc/pull/64 | `microsoft/tsdoc` | `code_only_tests_or_fixtures` | `typescript` | [spec] Adding snippets for "declaration references" |
| https://github.com/microsoft/tsdoc/pull/55 | `microsoft/tsdoc` | `code_and_docs` | `typescript` | Add an "advanced" scenario for the api-demo |
| https://github.com/microsoft/tsdoc/pull/54 | `microsoft/tsdoc` | `code_and_docs` | `typescript` | Add support for code fences |
| https://github.com/microsoft/tsdoc/pull/53 | `microsoft/tsdoc` | `code_and_docs` | `typescript` | Implement paragraph splitting |
| https://github.com/microsoft/tsdoc/pull/51 | `microsoft/tsdoc` | `code_and_docs` | `typescript` | Implement @privateRemarks and @deprecated tags |
| https://github.com/microsoft/tsdoc/pull/52 | `microsoft/tsdoc` | `code_only` | `typescript` | Rearrange some definitions to eliminate a circular import |
| https://github.com/microsoft/tsdoc/pull/50 | `microsoft/tsdoc` | `code_and_docs` | `typescript` | Add more standard tag definitions |
| https://github.com/microsoft/tsdoc/pull/45 | `microsoft/tsdoc` | `code_only` | `typescript` | Improve reporting of parser errors |
| https://github.com/microsoft/tsdoc/pull/49 | `microsoft/tsdoc` | `code_and_docs` | `typescript` | Clarify how to build the api-demo project |
| https://github.com/microsoft/tsdoc/pull/43 | `microsoft/tsdoc` | `code_only` | `typescript` | Introduce DocParticle node type |
| https://github.com/microsoft/tsdoc/pull/42 | `microsoft/tsdoc` | `code_only` | `typescript` | Implement extraction of summary, remarks, params, returns, and custom blocks |
| https://github.com/microsoft/tsdoc/pull/41 | `microsoft/tsdoc` | `code_only` | `typescript` | Introduce DocCommentAssembler |
| https://github.com/microsoft/tsdoc/pull/32 | `microsoft/tsdoc` | `code_only` | `typescript` | Add more TSDoc syntax elements |
| https://github.com/microsoft/tsdoc/pull/24 | `microsoft/tsdoc` | `code_only` | `typescript` | Initial parser skeleton |
| https://github.com/microsoft/tsdoc/pull/25 | `microsoft/tsdoc` | `code_only` | `typescript` | Initial implementation of line extraction |
| https://github.com/microsoft/tsdoc/pull/28 | `microsoft/tsdoc` | `code_only` | `typescript` | Initial implementation of tokenizer |
| https://github.com/microsoft/tsdoc/pull/2 | `microsoft/tsdoc` | `code_and_docs` | `typescript` | Initial draft of README.me content |
| https://github.com/microsoft/promptflow/pull/4160 | `microsoft/promptflow` | `code_and_docs` | `python` | Add docs related to devui and connections |
| https://github.com/microsoft/promptflow/pull/4155 | `microsoft/promptflow` | `code_and_docs` | `python` | add component sample |
| https://github.com/microsoft/promptflow/pull/4151 | `microsoft/promptflow` | `code_only` | `python` | Promptflow-release-1-18-5 (#4148) |
| https://github.com/microsoft/promptflow/pull/4150 | `microsoft/promptflow` | `code_only` | `python` | fix doc publish pipeline |
| https://github.com/microsoft/promptflow/pull/4148 | `microsoft/promptflow` | `code_only` | `python` | Promptflow-release-1-18-5 |
| https://github.com/microsoft/promptflow/pull/4128 | `microsoft/promptflow` | `code_and_docs` | `python` | ICM: Protect RCE sandbox |
| https://github.com/microsoft/promptflow/pull/4140 | `microsoft/promptflow` | `code_and_docs` | `python` | Lusu/0417 |
| https://github.com/microsoft/promptflow/pull/4090 | `microsoft/promptflow` | `code_only` | `python` | Fix wildcard CORS and auth bypass in Promptflow Service (PFS) |
| https://github.com/microsoft/promptflow/pull/4087 | `microsoft/promptflow` | `code_only` | `python` | chore: Upper-bound opentelemetry-sdk to 1.39.0 |
| https://github.com/microsoft/promptflow/pull/4084 | `microsoft/promptflow` | `code_and_docs` | `python` | fix: Bump pillow to 12.1.1 for promptflow-devkit |
| https://github.com/microsoft/promptflow/pull/4068 | `microsoft/promptflow` | `code_only` | `python` | fix: Guard against ssrf attacks when creating image input |
| https://github.com/microsoft/promptflow/pull/4065 | `microsoft/promptflow` | `code_only` | `python` | fix: pin starlette minimum version |
| https://github.com/microsoft/promptflow/pull/4062 | `microsoft/promptflow` | `code_only` | `python` | Update Pillow Range |
| https://github.com/microsoft/promptflow/pull/4061 | `microsoft/promptflow` | `code_only` | `python` | Update Pillow Version |
| https://github.com/microsoft/promptflow/pull/4054 | `microsoft/promptflow` | `code_only_tests_or_fixtures` | `python` | [no ci] chore: Remove pull_request_target trigger |
| https://github.com/microsoft/promptflow/pull/2226 | `microsoft/promptflow` | `code_and_docs` | `python` | [SDK] Flow as async function |
| https://github.com/microsoft/promptflow/pull/4029 | `microsoft/promptflow` | `code_and_docs` | `python` | Migration storage account to mlsdkfdnprod |
| https://github.com/microsoft/promptflow/pull/4001 | `microsoft/promptflow` | `code_only` | `python` | fix:AttributeError in _openai_utils.py with Azure OpenAI Async Streaming #4000 |
| https://github.com/microsoft/promptflow/pull/4023 | `microsoft/promptflow` | `code_only` | `python` | Main to Release Branch 1.18.1 |
| https://github.com/microsoft/promptflow/pull/4021 | `microsoft/promptflow` | `code_only` | `python` | v1.18.1 change |
| https://github.com/microsoft/promptflow/pull/4010 | `microsoft/promptflow` | `code_only` | `python` | Wrap all template usage, disable internal endpoint |
| https://github.com/microsoft/promptflow/pull/4019 | `microsoft/promptflow` | `code_only` | `python` | Update flask-cors dependency in devkit |
| https://github.com/microsoft/promptflow/pull/4015 | `microsoft/promptflow` | `code_and_docs` | `python` | fix: Resolve tool_call ACE + prompt injection from chat history |
| https://github.com/microsoft/promptflow/pull/4013 | `microsoft/promptflow` | `code_only` | `python` | Use SandboxedEnvironment for Template |
| https://github.com/microsoft/promptflow/pull/4007 | `microsoft/promptflow` | `code_only` | `python` | update version refs |
| https://github.com/microsoft/promptflow/pull/4006 | `microsoft/promptflow` | `code_only` | `python` | Add support to python 3.13 (#4005) |
| https://github.com/microsoft/promptflow/pull/4005 | `microsoft/promptflow` | `code_only` | `python` | Add support to python 3.13 |
| https://github.com/microsoft/promptflow/pull/3997 | `microsoft/promptflow` | `code_only` | `python` | fix: Create a deny list for environment variables that can be set by users |
| https://github.com/microsoft/promptflow/pull/3907 | `microsoft/promptflow` | `code_only` | `python` | Disable tracing in Promptflow by default |
| https://github.com/microsoft/promptflow/pull/3989 | `microsoft/promptflow` | `code_and_docs` | `python` | Promptflow-Eval-Deprecation |
| https://github.com/microsoft/promptflow/pull/3959 | `microsoft/promptflow` | `code_only` | `python` | RCE-fix-promptflow-tools |
| https://github.com/microsoft/promptflow/pull/3935 | `microsoft/promptflow` | `code_only` | `python` | fix(ci): Fix "poetry could not find a pyproject.toml" in import lint workflow |
| https://github.com/microsoft/promptflow/pull/3941 | `microsoft/promptflow` | `code_only` | `python` | PF-change-version-1.17.2 |
| https://github.com/microsoft/promptflow/pull/3927 | `microsoft/promptflow` | `code_and_docs` | `python` | MSRC93736-RCE-Fix |
| https://github.com/microsoft/promptflow/pull/3475 | `microsoft/promptflow` | `code_only` | `python` | Add user agent to prompty standalone execution |
| https://github.com/microsoft/promptflow/pull/3903 | `microsoft/promptflow` | `code_only` | `python` | remove _T dependency |
| https://github.com/microsoft/promptflow/pull/3887 | `microsoft/promptflow` | `code_and_docs` | `python` | Remove support for Python 3.8 |
| https://github.com/microsoft/promptflow/pull/3885 | `microsoft/promptflow` | `code_and_docs` | `python` | Fixed TypeError in Tracing issue with tokens that are dicts |
| https://github.com/microsoft/promptflow/pull/3820 | `microsoft/promptflow` | `code_only` | `python` | prompty: fix parsing of tool_calls when array in arguments |
| https://github.com/microsoft/promptflow/pull/3856 | `microsoft/promptflow` | `code_only_tests_or_fixtures` | `python` | Vulnerability Fix - gunicorn to 22.0.0 |
| https://github.com/microsoft/promptflow/pull/3863 | `microsoft/promptflow` | `code_and_docs` | `python` | CHANGELOG.md broken link fix  |
| https://github.com/microsoft/promptflow/pull/3838 | `microsoft/promptflow` | `code_only` | `python` | Upgrade to waitress 3.x and flask-cors 5.x |
| https://github.com/microsoft/promptflow/pull/3815 | `microsoft/promptflow` | `code_and_docs` | `python` | Add promptflow runtime release note |
| https://github.com/microsoft/promptflow/pull/3793 | `microsoft/promptflow` | `code_and_docs` | `python` | Fix bug in token usage merging logic for promptflow-tracing SDK |
| https://github.com/microsoft/promptflow/pull/3791 | `microsoft/promptflow` | `code_and_docs` | `python` | [promptflow][release] 1.16.0 release branch merge back |
| https://github.com/microsoft/promptflow/pull/3784 | `microsoft/promptflow` | `code_only` | `python` | Enhance the validation of local media_save API  |
| https://github.com/microsoft/promptflow/pull/3771 | `microsoft/promptflow` | `code_only` | `python` | Change eci prefix from upper case to lowercase |
| https://github.com/microsoft/promptflow/pull/3729 | `microsoft/promptflow` | `code_only` | `python` | Rename IndirectAttack evaluation enum to "xpia" |
| https://github.com/microsoft/promptflow/pull/3727 | `microsoft/promptflow` | `code_only` | `python` | Include xpia in handled_metrics for evaluation aggregation |
| https://github.com/microsoft/promptflow/pull/3719 | `microsoft/promptflow` | `code_only` | `python` | Math Evaluators |
| https://github.com/microsoft/promptflow/pull/3720 | `microsoft/promptflow` | `code_only` | `python` | PM/ECI defect rates in evaluation |
| https://github.com/microsoft/promptflow/pull/3705 | `microsoft/promptflow` | `code_and_docs` | `python` | rename direct attack sim |
| https://github.com/microsoft/promptflow/pull/3711 | `microsoft/promptflow` | `code_and_docs` | `python` | rename PMs to PM |
| https://github.com/microsoft/promptflow/pull/3702 | `microsoft/promptflow` | `code_only` | `python` | changes to align with spec |
| https://github.com/microsoft/promptflow/pull/3691 | `microsoft/promptflow` | `code_and_docs` | `python` | Update documents to include rerank tool |
| https://github.com/microsoft/promptflow/pull/3698 | `microsoft/promptflow` | `code_only` | `python` | Remove urllib3 dependency |
| https://github.com/microsoft/promptflow/pull/3683 | `microsoft/promptflow` | `code_only` | `python` | refactor: Remove networking imports outside azure core |
| https://github.com/microsoft/promptflow/pull/3685 | `microsoft/promptflow` | `code_only` | `python` | [experiment] Verify command injection when starting experiments asynchronously |
| https://github.com/microsoft/promptflow/pull/3680 | `microsoft/promptflow` | `code_only` | `python` | Set logger level instead of using debug |
| https://github.com/microsoft/promptflow/pull/3658 | `microsoft/promptflow` | `code_only` | `python` | Add custom exception class and helper classes for promptflow-evals |
| https://github.com/microsoft/promptflow/pull/3659 | `microsoft/promptflow` | `code_only` | `python` | Move eval rai call to shared package |
| https://github.com/microsoft/promptflow/pull/3614 | `microsoft/promptflow` | `code_and_docs` | `python` | [pf-evals] Enable async batch run for evaluators by default |
| https://github.com/microsoft/promptflow/pull/3664 | `microsoft/promptflow` | `code_only_tests_or_fixtures` | `python` | skip test_log_artifact . |
| https://github.com/microsoft/promptflow/pull/3616 | `microsoft/promptflow` | `code_and_docs` | `python` | Unify AI flex flow example |
| https://github.com/microsoft/promptflow/pull/3655 | `microsoft/promptflow` | `code_and_docs` | `python` | [promptflow][release] 1.15.0 release branch merge back |
| https://github.com/microsoft/promptflow/pull/3661 | `microsoft/promptflow` | `code_only` | `python` | [azure][test] pin `azure-ai-ml` to aovid azure replay test breaking |
| https://github.com/microsoft/promptflow/pull/3644 | `microsoft/promptflow` | `code_and_docs` | `python` | Tutorial on Continuous Monitoring using ML Pipelines |
| https://github.com/microsoft/promptflow/pull/3651 | `microsoft/promptflow` | `code_only` | `python` | [Fundamental] Check enforcer change. |
| https://github.com/microsoft/promptflow/pull/3640 | `microsoft/promptflow` | `code_only` | `python` | Remove pylint-azure-guidelines references |
| https://github.com/microsoft/promptflow/pull/3636 | `microsoft/promptflow` | `code_and_docs` | `python` | Revert "Bugfix/non azure open ai prompty (#3621)" (release branch only) |
| https://github.com/microsoft/promptflow/pull/3621 | `microsoft/promptflow` | `code_and_docs` | `python` | Bugfix/non azure open ai prompty |
| https://github.com/microsoft/promptflow/pull/3630 | `microsoft/promptflow` | `code_only_tests_or_fixtures` | `python` | [pf-evals] Switch to OIDC Login for evals test pipelines |
| https://github.com/microsoft/promptflow/pull/3620 | `microsoft/promptflow` | `code_and_docs` | `python` | [internal][feat] update trace view js bundle |
| https://github.com/microsoft/promptflow/pull/3624 | `microsoft/promptflow` | `code_only` | `python` | [test] Fix breaking devkit test by adding `uvicorn` to devkit pyproject.toml |
| https://github.com/microsoft/promptflow/pull/3623 | `microsoft/promptflow` | `code_and_docs` | `python` | [Fundamental]Check enforcer print more messsage and fix some nits on readme parser |
| https://github.com/microsoft/promptflow/pull/3603 | `microsoft/promptflow` | `code_and_docs` | `python` | [pf-evals] Fix the evaluate API relative data path is not working due to underlying working directory change |
| https://github.com/microsoft/promptflow/pull/3618 | `microsoft/promptflow` | `code_only` | `python` | Check enforcer print merge commit diffs |
| https://github.com/microsoft/promptflow/pull/3606 | `microsoft/promptflow` | `code_only` | `python` | Add pylint back to pre-commit |
| https://github.com/microsoft/promptflow/pull/3609 | `microsoft/promptflow` | `code_only` | `python` | [pf-evals] Document improvements and convert timeout to constant |
| https://github.com/microsoft/promptflow/pull/3601 | `microsoft/promptflow` | `code_and_docs` | `python` | Convert composite evaluators to async based implementation |
| https://github.com/microsoft/promptflow/pull/3607 | `microsoft/promptflow` | `code_and_docs` | `python` | [SDK/CLI][Azure] Add POST method to retry method list |
| https://github.com/microsoft/promptflow/pull/3598 | `microsoft/promptflow` | `code_only` | `python` | Fix openai error handler not working for async prompty |
| https://github.com/microsoft/promptflow/pull/3599 | `microsoft/promptflow` | `code_only` | `python` | More eval test coverage |
| https://github.com/microsoft/promptflow/pull/3587 | `microsoft/promptflow` | `code_only_tests_or_fixtures` | `python` | Fix Test Case by Replacing `text-ada-001` with `gpt-35-turbo-instruct` |
| https://github.com/microsoft/promptflow/pull/3545 | `microsoft/promptflow` | `code_only` | `python` |  AB#3250444 Fixing user agent header name |
| https://github.com/microsoft/promptflow/pull/3581 | `microsoft/promptflow` | `code_and_docs` | `python` | Release promptflow 1.14.0 |
| https://github.com/microsoft/promptflow/pull/3572 | `microsoft/promptflow` | `code_only` | `python` | [Example] Add flow.flex.yaml for chat-minimal |
| https://github.com/microsoft/promptflow/pull/3501 | `microsoft/promptflow` | `code_and_docs` | `python` | Add batch timeout override |
| https://github.com/microsoft/promptflow/pull/3548 | `microsoft/promptflow` | `code_only` | `python` | Remove dependency on docutils package |
| https://github.com/microsoft/promptflow/pull/3556 | `microsoft/promptflow` | `code_and_docs` | `python` | [devkit] Add promptflow package to dockerfile |
| https://github.com/microsoft/promptflow/pull/3542 | `microsoft/promptflow` | `code_and_docs` | `python` | Leverage async batch run for first async-enabled evaluator - FluencyEvaluator |
| https://github.com/microsoft/promptflow/pull/3546 | `microsoft/promptflow` | `code_only` | `python` | Split installation tests from other e2e tests. |
| https://github.com/microsoft/promptflow/pull/3544 | `microsoft/promptflow` | `code_and_docs` | `python` | add category to template_parameters in the output of simulations |
| https://github.com/microsoft/promptflow/pull/3534 | `microsoft/promptflow` | `code_only` | `python` | Add local e2e test gate |
| https://github.com/microsoft/promptflow/pull/3529 | `microsoft/promptflow` | `code_only` | `python` | Make evaluation run a context manager instead of a singleton. |
| https://github.com/microsoft/promptflow/pull/3527 | `microsoft/promptflow` | `code_only` | `python` | Update dependency for pf dependences and local import for dependences related to pf-azure |
| https://github.com/microsoft/promptflow/pull/3523 | `microsoft/promptflow` | `code_only` | `python` | Adding the credential to jailbreak adv sim init to make sure it can b… |
| https://github.com/microsoft/promptflow/pull/3455 | `microsoft/promptflow` | `code_and_docs` | `python` | Task/jailbreak adv sim |
| https://github.com/microsoft/promptflow/pull/3518 | `microsoft/promptflow` | `code_and_docs` | `python` | [doc] highlight tracing feature |
| https://github.com/microsoft/promptflow/pull/3507 | `microsoft/promptflow` | `code_only` | `python` | [Bug fix] Use default pfs host to ping service when pfs host in wildcard address |
| https://github.com/microsoft/promptflow/pull/3505 | `microsoft/promptflow` | `code_only_tests_or_fixtures` | `python` | Update chat group tests to check output content |
| https://github.com/microsoft/promptflow/pull/3506 | `microsoft/promptflow` | `code_and_docs` | `python` | [Fundamental] Limit output tracebacks and add documentation on rotate aoai keys |
| https://github.com/microsoft/promptflow/pull/3497 | `microsoft/promptflow` | `code_and_docs` | `python` | Release/promptflow/1.13.0 |
| https://github.com/microsoft/promptflow/pull/3498 | `microsoft/promptflow` | `code_only` | `python` | [SDK/CLI] Add telemetry for run upload |
| https://github.com/microsoft/promptflow/pull/3496 | `microsoft/promptflow` | `code_only` | `python` | Fix complince check config |
| https://github.com/microsoft/promptflow/pull/3491 | `microsoft/promptflow` | `code_only` | `python` | Using token Cache to reduce token get calls |
| https://github.com/microsoft/promptflow/pull/3487 | `microsoft/promptflow` | `code_only` | `python` | Adding user agent to prompt based evaluators |
| https://github.com/microsoft/promptflow/pull/3299 | `microsoft/promptflow` | `code_and_docs` | `python` | [Release] Release 1.11.0 |
| https://github.com/microsoft/promptflow/pull/3481 | `microsoft/promptflow` | `code_only` | `python` | [fundamental] Touch result file for fork repository |
| https://github.com/microsoft/promptflow/pull/3430 | `microsoft/promptflow` | `code_only` | `python` | [Flow test] Remove useless code to support prompty/flex return stream output |
| https://github.com/microsoft/promptflow/pull/3470 | `microsoft/promptflow` | `code_only` | `python` | Support config local pfs host and remove pfs auto-stop |
| https://github.com/microsoft/promptflow/pull/3473 | `microsoft/promptflow` | `code_only` | `python` | Adding telemetry for evaluate API |
| https://github.com/microsoft/promptflow/pull/3464 | `microsoft/promptflow` | `code_only_tests_or_fixtures` | `python` | Add lower bound for test coverage and upper bond for installation time. |
| https://github.com/microsoft/promptflow/pull/3449 | `microsoft/promptflow` | `code_only` | `python` | Fix docstrings |
| https://github.com/microsoft/promptflow/pull/3448 | `microsoft/promptflow` | `code_only` | `python` | Bugfix/large sim jinja exception |
| https://github.com/microsoft/promptflow/pull/3446 | `microsoft/promptflow` | `code_only` | `python` | [pf-evals] ContentSafety: Use new way to check RAI availability and perf improve via reusing the token |
| https://github.com/microsoft/promptflow/pull/3453 | `microsoft/promptflow` | `code_only` | `python` | PR to unblock release |
| https://github.com/microsoft/promptflow/pull/3457 | `microsoft/promptflow` | `code_only` | `python` | Skip the unit test for e2e run in recording. |
| https://github.com/microsoft/promptflow/pull/2981 | `microsoft/promptflow` | `code_and_docs` | `python` | [Doc] Add flex flow doc |
| https://github.com/microsoft/promptflow/pull/3403 | `microsoft/promptflow` | `code_only` | `python` | Make the promptflow-azure an optional dependency; fix artifact logging. |
| https://github.com/microsoft/promptflow/pull/3414 | `microsoft/promptflow` | `code_and_docs` | `python` | [Prompty] AsyncFlow.load on prompty should return AsyncPrompty |
| https://github.com/microsoft/promptflow/pull/3427 | `microsoft/promptflow` | `code_only` | `python` | [perf] Reduce eval local to remote tracking latency by caching the arm token |
| https://github.com/microsoft/promptflow/pull/3417 | `microsoft/promptflow` | `code_only` | `python` | Remove sys sxit when show pfs status |
| https://github.com/microsoft/promptflow/pull/3387 | `microsoft/promptflow` | `code_only_tests_or_fixtures` | `python` | [Test] Update error msg response from backend |
| https://github.com/microsoft/promptflow/pull/3429 | `microsoft/promptflow` | `code_only` | `python` | [fundamental][bugfix] Replace retired model `"text-ada-001"` |
| https://github.com/microsoft/promptflow/pull/3421 | `microsoft/promptflow` | `code_and_docs` | `python` | [devkit][bugfix] Add missing user agent in trace telemetry |
| https://github.com/microsoft/promptflow/pull/3412 | `microsoft/promptflow` | `code_only` | `python` | [Perf] Evaluate API: Using threads to infer signatures for eval batch runs instead of processes.  |
| https://github.com/microsoft/promptflow/pull/3426 | `microsoft/promptflow` | `code_only` | `python` | Show user friendly error message for multi-process boostrapping error |
| https://github.com/microsoft/promptflow/pull/3380 | `microsoft/promptflow` | `code_only` | `python` | [Perf] Evaluate API: Support parallelized evaluator batch run through pf.run |
| https://github.com/microsoft/promptflow/pull/3424 | `microsoft/promptflow` | `code_only` | `python` | [fundamental][bugfix] Pin `tenacity`<8.4.0 to fix import-linter CI |
| https://github.com/microsoft/promptflow/pull/3423 | `microsoft/promptflow` | `code_only_tests_or_fixtures` | `python` | [Internal] Fix tool ci by skipping acs test since the test resource is not valid |
| https://github.com/microsoft/promptflow/pull/3422 | `microsoft/promptflow` | `code_only` | `python` | [bugfix] Pin numpy in CI to avoid incompatible pandas |
| https://github.com/microsoft/promptflow/pull/3406 | `microsoft/promptflow` | `code_only` | `python` | Pass subscription/resource_group/workspace settings define in customer folder repo to PF SDK |
| https://github.com/microsoft/promptflow/pull/3407 | `microsoft/promptflow` | `code_and_docs` | `python` | [devkit][bugfix] Add check for `trace.NoOpTracerProvider` to avoid crash |
| https://github.com/microsoft/promptflow/pull/3400 | `microsoft/promptflow` | `code_and_docs` | `python` | [Release] Release 1.12.0 |
| https://github.com/microsoft/promptflow/pull/3397 | `microsoft/promptflow` | `code_only` | `python` | [Doc]fix typo |
| https://github.com/microsoft/promptflow/pull/3404 | `microsoft/promptflow` | `code_only` | `python` | [azure][bugfix] Fix Azure replay test wrong sanitizations |
| https://github.com/microsoft/promptflow/pull/3361 | `microsoft/promptflow` | `code_only` | `python` | Fixing timezone issue with local to cloud run |
| https://github.com/microsoft/promptflow/pull/3399 | `microsoft/promptflow` | `code_only` | `python` | Log aggregated metric generated by flex flow to eval run |
| https://github.com/microsoft/promptflow/pull/3366 | `microsoft/promptflow` | `code_only` | `python` | Fix stream test case failed due to modifying GeneratorProxy |
| https://github.com/microsoft/promptflow/pull/3368 | `microsoft/promptflow` | `code_and_docs` | `python` | [trace][feature] Add trace usage telemetry |
| https://github.com/microsoft/promptflow/pull/3363 | `microsoft/promptflow` | `code_only_tests_or_fixtures` | `python` | install langchain_community to fix failed executor e2e test case |
| https://github.com/microsoft/promptflow/pull/3356 | `microsoft/promptflow` | `code_only` | `python` | Adding more custom dimensions |
| https://github.com/microsoft/promptflow/pull/3359 | `microsoft/promptflow` | `code_only` | `python` | Adding activity logger for evaluator API |
| https://github.com/microsoft/promptflow/pull/3354 | `microsoft/promptflow` | `code_only` | `python` | Ignore aggregation node for trace telemetry. |
| https://github.com/microsoft/promptflow/pull/3357 | `microsoft/promptflow` | `code_and_docs` | `python` | [Bugfix] Fix the bug that generator in subflow would fail. |
| https://github.com/microsoft/promptflow/pull/3358 | `microsoft/promptflow` | `code_only` | `python` | Update the chat window UI |
| https://github.com/microsoft/promptflow/pull/3360 | `microsoft/promptflow` | `code_only` | `python` | Move load save example from the bug bash to the main branch. |
| https://github.com/microsoft/promptflow/pull/3353 | `microsoft/promptflow` | `code_only` | `python` | [Perf] Allow disabling tracing & serialization check to avoid extra overhead in serving scenario. |
| https://github.com/microsoft/promptflow/pull/3220 | `microsoft/promptflow` | `code_and_docs` | `python` | update build flex flow test |
| https://github.com/microsoft/promptflow/pull/2245 | `microsoft/promptflow` | `code_only` | `python` | [Internal] improve token connection error message |
| https://github.com/microsoft/promptflow/pull/3333 | `microsoft/promptflow` | `code_and_docs` | `python` | [Serve]Update flow name in swagger.json to fix container chat ui not work |
| https://github.com/microsoft/promptflow/pull/3304 | `microsoft/promptflow` | `code_and_docs` | `python` | [SDK/CLI] Add retry for async calls |
| https://github.com/microsoft/promptflow/pull/3334 | `microsoft/promptflow` | `code_only` | `python` | Fix Core Recording. |
| https://github.com/microsoft/promptflow/pull/3326 | `microsoft/promptflow` | `code_only_tests_or_fixtures` | `python` | Add Debug Information to Test Cases in test_logs.py |
| https://github.com/microsoft/promptflow/pull/3328 | `microsoft/promptflow` | `code_only_tests_or_fixtures` | `python` | Fix Executor Recording |
| https://github.com/microsoft/promptflow/pull/3314 | `microsoft/promptflow` | `code_only_tests_or_fixtures` | `python` | Move evals recordings to its own folder |
| https://github.com/microsoft/promptflow/pull/3316 | `microsoft/promptflow` | `code_only` | `python` | [trace][bugfix] Skip exporter to PFS with environ set in serving scenario |
| https://github.com/microsoft/promptflow/pull/3327 | `microsoft/promptflow` | `code_only_tests_or_fixtures` | `python` | Fix Recording |
| https://github.com/microsoft/promptflow/pull/3305 | `microsoft/promptflow` | `code_only` | `python` | PFServing otlp support improvement |
| https://github.com/microsoft/promptflow/pull/3303 | `microsoft/promptflow` | `code_only` | `python` | [prompty] Prompty supports image as input |
| https://github.com/microsoft/promptflow/pull/3308 | `microsoft/promptflow` | `code_only` | `python` | Handle numeric columns |
| https://github.com/microsoft/promptflow/pull/3319 | `microsoft/promptflow` | `code_and_docs` | `python` | update llmlingua tool doc |
| https://github.com/microsoft/promptflow/pull/3322 | `microsoft/promptflow` | `code_only` | `python` | Defect Rate calculation handling none values |
| https://github.com/microsoft/promptflow/pull/3320 | `microsoft/promptflow` | `code_and_docs` | `python` | update example flow for llmlingua prompt compression tool |
| https://github.com/microsoft/promptflow/pull/3315 | `microsoft/promptflow` | `code_only` | `python` | only pass user parameter when it is not empty for chat api |
| https://github.com/microsoft/promptflow/pull/3309 | `microsoft/promptflow` | `code_only` | `python` | [pf-evals] Fix the user agent not populated |
| https://github.com/microsoft/promptflow/pull/3307 | `microsoft/promptflow` | `code_only` | `python` | Fixing prompty threadpool implementation |
| https://github.com/microsoft/promptflow/pull/3306 | `microsoft/promptflow` | `code_only` | `python` | [pf-evals] regression fix for threadtool in evaluate API |
| https://github.com/microsoft/promptflow/pull/3302 | `microsoft/promptflow` | `code_and_docs` | `python` | [Doc] refine docsite after v.11 release |
| https://github.com/microsoft/promptflow/pull/3300 | `microsoft/promptflow` | `code_only` | `python` | [Internal] Fix gen schema file name bug |
| https://github.com/microsoft/promptflow/pull/3298 | `microsoft/promptflow` | `code_only_tests_or_fixtures` | `python` | [Test Fix]Fix test nit, there is no public is_live method provided. |
| https://github.com/microsoft/promptflow/pull/3179 | `microsoft/promptflow` | `code_only` | `python` | Support context manager protocol for traced iterator APIs |
| https://github.com/microsoft/promptflow/pull/3296 | `microsoft/promptflow` | `code_only` | `python` | Users/singankit/fix remote tracking |
| https://github.com/microsoft/promptflow/pull/3297 | `microsoft/promptflow` | `code_only` | `python` | Append user agent for OpenAI calls |
| https://github.com/microsoft/promptflow/pull/3294 | `microsoft/promptflow` | `code_only` | `python` | Remove unnecessary keys and values from simulator output |
| https://github.com/microsoft/promptflow/pull/3281 | `microsoft/promptflow` | `code_only` | `python` | Enable threadpool in evaluate API |
| https://github.com/microsoft/promptflow/pull/3290 | `microsoft/promptflow` | `code_and_docs` | `python` | clear temp doc changes |
| https://github.com/microsoft/promptflow/pull/3268 | `microsoft/promptflow` | `code_and_docs` | `python` | refine rag related documents |
| https://github.com/microsoft/promptflow/pull/3287 | `microsoft/promptflow` | `code_only` | `python` | feat: support specifying flow file for test --ui |
| https://github.com/microsoft/fluentui/pull/36615 | `microsoft/fluentui` | `code_and_docs` | `typescript` | chore(workspace-plugin): add export-maps-sync generator to prevent export map drift |
| https://github.com/microsoft/fluentui/pull/36627 | `microsoft/fluentui` | `code_only` | `typescript` | fix(deprecated): keep deprecated packages on their named prerelease line |
| https://github.com/microsoft/fluentui/pull/36623 | `microsoft/fluentui` | `code_and_docs` | `typescript` | fix(react-headless-components-preview): narrow positioning prop to headless PositioningShorthand |
| https://github.com/microsoft/fluentui/pull/36570 | `microsoft/fluentui` | `code_only_tests_or_fixtures` | `typescript` | docs(docsite-v9): clarify brand-background demo in ColorAndAppearance story |
| https://github.com/microsoft/fluentui/pull/36608 | `microsoft/fluentui` | `code_and_docs` | `typescript` | fix(react-headless-components-preview): use global focusgroup typing for MenuListState |
| https://github.com/microsoft/fluentui/pull/36609 | `microsoft/fluentui` | `code_only` | `typescript` | fix(react-headless-components-preview): use tab navigation in Nav instead of arrow keys |
| https://github.com/microsoft/fluentui/pull/36612 | `microsoft/fluentui` | `code_only` | `typescript` | test: cover overflow menu convergence loop |
| https://github.com/microsoft/fluentui/pull/36607 | `microsoft/fluentui` | `code_only` | `typescript` | chore: scope docsite tsconfig types so ambient typings don't leak into Storybook props tables |
| https://github.com/microsoft/fluentui/pull/36621 | `microsoft/fluentui` | `code_only` | `typescript` | fix(web-components): TextArea overflow scrolling in Firefox |
| https://github.com/microsoft/fluentui/pull/36603 | `microsoft/fluentui` | `code_only` | `typescript` | fix(web-components): submenu sizing in webkit |
| https://github.com/microsoft/fluentui/pull/36565 | `microsoft/fluentui` | `code_and_docs` | `typescript` | feat(skills): add /release-recovery skill for npm/repo release desync |
| https://github.com/microsoft/fluentui/pull/36587 | `microsoft/fluentui` | `code_and_docs` | `typescript` | chore: add verify-bundle-isolation to workspace plugin, cleanup deps and onboard react-components to track base hooks creep |
| https://github.com/microsoft/fluentui/pull/36606 | `microsoft/fluentui` | `code_only` | `typescript` | fix: correct headless component subpath exports |
| https://github.com/microsoft/fluentui/pull/36602 | `microsoft/fluentui` | `code_only` | `typescript` | Fix overflow menu teardown convergence |
| https://github.com/microsoft/fluentui/pull/36600 | `microsoft/fluentui` | `code_only` | `typescript` | fix(web-component): sanitize token values in set theme |
| https://github.com/microsoft/fluentui/pull/36573 | `microsoft/fluentui` | `code_only` | `typescript` | chore: delete unused pipelines, variables, path references |
| https://github.com/microsoft/fluentui/pull/36581 | `microsoft/fluentui` | `code_and_docs` | `typescript` | feat(eslint-rules): add prefer-direct-reexport eslint rule |
| https://github.com/microsoft/fluentui/pull/36586 | `microsoft/fluentui` | `code_and_docs` | `typescript` | feat(verify-bundle-isolation)!: select fixtures via per-fixture config |
| https://github.com/microsoft/fluentui/pull/36589 | `microsoft/fluentui` | `code_and_docs` | `typescript` | feat: add assign-prs skill |
| https://github.com/microsoft/fluentui/pull/36588 | `microsoft/fluentui` | `code_only` | `typescript` | Fix redundant Overflow update work |
| https://github.com/microsoft/fluentui/pull/36580 | `microsoft/fluentui` | `code_and_docs` | `typescript` | feat(headless-components-preview): add Combobox filtering and root state attributes |
| https://github.com/microsoft/fluentui/pull/36582 | `microsoft/fluentui` | `code_and_docs` | `typescript` | fix(merge-styles): escape style tag terminators in serialized CSS and stylesheet state |
| https://github.com/microsoft/fluentui/pull/36583 | `microsoft/fluentui` | `code_only` | `typescript` | chore(scripts): replace custom format executor with nx format |
| https://github.com/microsoft/fluentui/pull/36468 | `microsoft/fluentui` | `code_and_docs` | `typescript` | fix(react-tag-picker): drop no-op `supportsSize` field control option |
| https://github.com/microsoft/fluentui/pull/36551 | `microsoft/fluentui` | `code_only` | `typescript` | fix: align react peerDependencies across react-components packages |
| https://github.com/microsoft/fluentui/pull/36575 | `microsoft/fluentui` | `code_only` | `typescript` | docs(react-docsite-components): flag Markdown enableRenderHtmlBlock as unsafe |
| https://github.com/microsoft/fluentui/pull/36578 | `microsoft/fluentui` | `code_only` | `typescript` | fix(react): warn in dev when DocumentCard onClickHref is a script URL |
| https://github.com/microsoft/fluentui/pull/36547 | `microsoft/fluentui` | `code_only` | `typescript` | fix(web-components): align MessageBar multiline dismiss button |
| https://github.com/microsoft/fluentui/pull/36568 | `microsoft/fluentui` | `code_and_docs` | `typescript` | feat(react-headless-components-preview): add focusgroup typings |
| https://github.com/microsoft/fluentui/pull/36571 | `microsoft/fluentui` | `code_and_docs` | `typescript` | feat(headless-dropdown): expose data-attributes |
| https://github.com/microsoft/fluentui/pull/36499 | `microsoft/fluentui` | `code_only` | `typescript` | chore: migrate to monosize v0.10 and add scoped bundle-size threshold |
| https://github.com/microsoft/fluentui/pull/36549 | `microsoft/fluentui` | `code_only` | `typescript` | fix(react-message-bar): keep motion ref out of base hook |
| https://github.com/microsoft/fluentui/pull/36560 | `microsoft/fluentui` | `code_only` | `typescript` | fix(react-headless-components-preview): use valid focusgroup nomemory token for TabList |
| https://github.com/microsoft/fluentui/pull/36546 | `microsoft/fluentui` | `code_and_docs` | `typescript` | Bump web components packages to latest |
| https://github.com/microsoft/fluentui/pull/36562 | `microsoft/fluentui` | `code_only_tests_or_fixtures` | `typescript` | test(react-tabs): Use valid `nomemory` focusgroup token in TabList example |
| https://github.com/microsoft/fluentui/pull/36555 | `microsoft/fluentui` | `code_only` | `typescript` | fix(react-color-picker): use valid modern HSL syntax |
| https://github.com/microsoft/fluentui/pull/36552 | `microsoft/fluentui` | `code_only` | `typescript` | refactor(react-color-picker): move CSS vars to constants |
| https://github.com/microsoft/fluentui/pull/36550 | `microsoft/fluentui` | `code_only` | `typescript` | refactor(react-swatch-picker): move styles out of base hook |
| https://github.com/microsoft/fluentui/pull/36553 | `microsoft/fluentui` | `code_and_docs` | `typescript` |  fix(react-headless-components-preview): use a custom renderTagPicker function so Portal isn't pulled in |
| https://github.com/microsoft/fluentui/pull/36525 | `microsoft/fluentui` | `code_and_docs` | `typescript` | feat(react-headless-components-preview): add headless SplitButton |
| https://github.com/microsoft/fluentui/pull/36524 | `microsoft/fluentui` | `code_and_docs` | `typescript` | feat(react-button): expose useSplitButtonBase_unstable base hook |
| https://github.com/microsoft/fluentui/pull/36548 | `microsoft/fluentui` | `code_only` | `typescript` | refactor(react-color-picker): remove tinycolor dependency |
| https://github.com/microsoft/fluentui/pull/36478 | `microsoft/fluentui` | `code_only` | `typescript` | chore(deps): bump minimatch from 3.1.2 to 3.1.4 |
| https://github.com/microsoft/fluentui/pull/36475 | `microsoft/fluentui` | `code_only` | `typescript` | chore(deps): bump @babel/runtime from 7.25.0 to 7.29.7 |
| https://github.com/microsoft/fluentui/pull/36533 | `microsoft/fluentui` | `code_only_tests_or_fixtures` | `typescript` | test(react-swatch-picker): add hook state coverage |
| https://github.com/microsoft/fluentui/pull/36534 | `microsoft/fluentui` | `code_and_docs` | `typescript` | feat(react-swatch-picker): expose headless base APIs |
| https://github.com/microsoft/fluentui/pull/36516 | `microsoft/fluentui` | `code_only` | `typescript` | Update beachball to v3 alpha |
| https://github.com/microsoft/fluentui/pull/36542 | `microsoft/fluentui` | `code_and_docs` | `typescript` | fix(react-link): remove inline prop from base hook |
| https://github.com/microsoft/fluentui/pull/36517 | `microsoft/fluentui` | `code_and_docs` | `typescript` | feat(react-color-picker): expose headless base APIs |
| https://github.com/microsoft/fluentui/pull/36518 | `microsoft/fluentui` | `code_and_docs` | `typescript` | feat(react-headless-components-preview): add color picker controls |
| https://github.com/microsoft/fluentui/pull/36527 | `microsoft/fluentui` | `code_only_tests_or_fixtures` | `typescript` | test(react-color-picker): add hook state coverage |
| https://github.com/microsoft/fluentui/pull/36523 | `microsoft/fluentui` | `code_only` | `typescript` | test(react-button): add SplitButton regression test before base-hook extraction |
| https://github.com/microsoft/fluentui/pull/36531 | `microsoft/fluentui` | `code_and_docs` | `typescript` | feat(react-headless-components-preview): add CompoundButton |
| https://github.com/microsoft/fluentui/pull/36530 | `microsoft/fluentui` | `code_and_docs` | `typescript` | feat(react-button): expose CompoundButton headless base APIs |
| https://github.com/microsoft/fluentui/pull/36529 | `microsoft/fluentui` | `code_only` | `typescript` | test(react-button): add CompoundButton regression coverage |
| https://github.com/microsoft/fluentui/pull/36537 | `microsoft/fluentui` | `code_only` | `typescript` | fix(bundle-size): correct non-existent named imports in fixtures + surface compare-reports failures |
| https://github.com/microsoft/fluentui/pull/36522 | `microsoft/fluentui` | `code_only` | `typescript` | perf(workspace-plugin): reuse a single api-extractor compiler state in generate-api |
| https://github.com/microsoft/fluentui/pull/36511 | `microsoft/fluentui` | `code_and_docs` | `typescript` | feat(verify-bundle-isolation): implement verify bundle isolation CLI and hook it to headless package |
| https://github.com/microsoft/fluentui/pull/36498 | `microsoft/fluentui` | `code_only` | `typescript` | fix(eslint-rules): base-hook-no-forbidden-runtime - analyze base hook dependencies per symbol, not per file |
| https://github.com/microsoft/fluentui/pull/36361 | `microsoft/fluentui` | `code_only` | `typescript` | feat(scripts-cypress): ship a real dual ESM/CJS build for type:module consumers |
| https://github.com/microsoft/fluentui/pull/36521 | `microsoft/fluentui` | `code_only` | `typescript` | Fix/message bar max width |
| https://github.com/microsoft/fluentui/pull/36507 | `microsoft/fluentui` | `code_only` | `typescript` | fix(react-file-type-icons): map clpx extension to clipchamp icon |
| https://github.com/microsoft/fluentui/pull/36360 | `microsoft/fluentui` | `code_only` | `typescript` | feat(workspace-plugin): recognize .cjs configs + add optional attw target |
| https://github.com/microsoft/fluentui/pull/36362 | `microsoft/fluentui` | `code_only` | `typescript` | feat(workspace-plugin): opt-in ESM-first emit gated on package type:module for migrate-converged-pkg generator |
| https://github.com/microsoft/fluentui/pull/36504 | `microsoft/fluentui` | `code_only` | `typescript` | fix(react-teaching-popover): isolate bundled dismiss icon |
| https://github.com/microsoft/fluentui/pull/36503 | `microsoft/fluentui` | `code_only` | `typescript` | fix(react-tag-picker): remove default icon from headless state |
| https://github.com/microsoft/fluentui/pull/36506 | `microsoft/fluentui` | `code_and_docs` | `typescript` | chore: sync web components versions after broken release |
| https://github.com/microsoft/fluentui/pull/36457 | `microsoft/fluentui` | `code_only` | `typescript` | fix(web-components): remove the pattern of using `data-indent` for styling |
| https://github.com/microsoft/fluentui/pull/36359 | `microsoft/fluentui` | `code_and_docs` | `typescript` | feat(workspace-plugin): opt-in ESM-first build postprocessing via inline SWC transforms (.cjs + .d.cts) |
| https://github.com/microsoft/fluentui/pull/36505 | `microsoft/fluentui` | `code_and_docs` | `typescript` | chore(react-tabster): update to Tabster 9 canary |
| https://github.com/microsoft/fluentui/pull/36497 | `microsoft/fluentui` | `code_only` | `typescript` | fix(react-combobox,react-tag-picker): separate tabster logic from the base hooks |
| https://github.com/microsoft/fluentui/pull/36453 | `microsoft/fluentui` | `code_only` | `typescript` | fix(react-input, react-textarea): Fix Field control size handling |
| https://github.com/microsoft/fluentui/pull/36501 | `microsoft/fluentui` | `code_only` | `typescript` | build(web-components): use repo root level dependencies to run local commands |
| https://github.com/microsoft/fluentui/pull/36440 | `microsoft/fluentui` | `code_only` | `typescript` | fix(react-popover): dismiss after focus leaves the surface |
| https://github.com/microsoft/fluentui/pull/36469 | `microsoft/fluentui` | `code_and_docs` | `typescript` | ci(dependabot): remove grouping of production deps to be updated |
| https://github.com/microsoft/fluentui/pull/36494 | `microsoft/fluentui` | `code_only` | `typescript` | Updated key value in HorizontalBarChartWithAxis |
| https://github.com/microsoft/fluentui/pull/36470 | `microsoft/fluentui` | `code_only` | `typescript` | chore(deps): roll up 11 Dependabot patch and minor updates |
| https://github.com/microsoft/fluentui/pull/36437 | `microsoft/fluentui` | `code_only_tests_or_fixtures` | `typescript` | feat(vrt): stabilize date-dependent Calendar and DatePicker stories |
| https://github.com/microsoft/fluentui/pull/36464 | `microsoft/fluentui` | `code_only` | `typescript` | fix: escape FluentProvider SSR style selectors |
| https://github.com/microsoft/fluentui/pull/36479 | `microsoft/fluentui` | `code_and_docs` | `typescript` | feat(react-headless-components-preview): export Drawer context |
| https://github.com/microsoft/fluentui/pull/36406 | `microsoft/fluentui` | `code_and_docs` | `typescript` | docs: minor story-only accessibility fixes in v9 stories |
| https://github.com/microsoft/fluentui/pull/36386 | `microsoft/fluentui` | `code_and_docs` | `typescript` | fix(react-tooltip): hide tooltip when trigger scrolls out of overflow container |
| https://github.com/microsoft/fluentui/pull/36455 | `microsoft/fluentui` | `code_and_docs` | `typescript` | fix: improve Dependabot rollup handling |
| https://github.com/microsoft/fluentui/pull/36465 | `microsoft/fluentui` | `code_only` | `typescript` | chore: fix beachball pre-commit after yarn v4 |
| https://github.com/microsoft/fluentui/pull/36461 | `microsoft/fluentui` | `code_only` | `typescript` | fix(docsite): restore LLM documentation after yarn v4 migration  |
| https://github.com/microsoft/fluentui/pull/36454 | `microsoft/fluentui` | `code_only` | `typescript` | fix(react-headless-components-preview): fix multiple anchors support on the same element |
| https://github.com/microsoft/fluentui/pull/36350 | `microsoft/fluentui` | `code_and_docs` | `typescript` | feat(react-headless-components-preview): add AvatarGroup component |
| https://github.com/microsoft/fluentui/pull/36395 | `microsoft/fluentui` | `code_and_docs` | `typescript` | fix(web-components): select a tab when click() is called on it |
| https://github.com/microsoft/fluentui/pull/36443 | `microsoft/fluentui` | `code_and_docs` | `typescript` | fix(react-tag-picker): allow base states in render functions |
| https://github.com/microsoft/fluentui/pull/36404 | `microsoft/fluentui` | `code_and_docs` | `typescript` | feat(babel-preset-storybook-full-source): add opt-in per-story fullSource slicing |
| https://github.com/microsoft/fluentui/pull/36452 | `microsoft/fluentui` | `code_and_docs` | `typescript` | fix(react-headless-components-preview): export useFieldContext and useFieldControlProps hooks |
| https://github.com/microsoft/fluentui/pull/36322 | `microsoft/fluentui` | `code_and_docs` | `typescript` | docs: add browser support information to headless components docs |
| https://github.com/microsoft/fluentui/pull/36441 | `microsoft/fluentui` | `code_only` | `typescript` | make native disabled state support SSR better |
| https://github.com/microsoft/fluentui/pull/36385 | `microsoft/fluentui` | `code_only` | `typescript` | feat(react-storybook-addon-export-to-sandbox): remove custom-babel-loader workaround |
| https://github.com/microsoft/fluentui/pull/36432 | `microsoft/fluentui` | `code_only` | `typescript` | feat(react-positioning): expose visibility flags in positioning callback |
| https://github.com/microsoft/fluentui/pull/36438 | `microsoft/fluentui` | `code_and_docs` | `typescript` | ci(dependabot): cap npm rollups at 11 for minor + patch |
| https://github.com/microsoft/fluentui/pull/36384 | `microsoft/fluentui` | `code_only` | `typescript` | fix(react-tree): expose tree selection control to assistive technologies |
| https://github.com/microsoft/fluentui/pull/36420 | `microsoft/fluentui` | `code_only` | `typescript` | chore: bump vulnerable deps and apply targeted security resolutions |
| https://github.com/microsoft/fluentui/pull/36390 | `microsoft/fluentui` | `code_only` | `typescript` | test(react-menu): add regression tests for previously fixed issue |
| https://github.com/microsoft/fluentui/pull/36419 | `microsoft/fluentui` | `code_and_docs` | `typescript` | ci(dependabot): remove overlapping Dependabot npm config |
| https://github.com/microsoft/fluentui/pull/36410 | `microsoft/fluentui` | `code_and_docs` | `typescript` | docs: update documentation for Yarn 4 |
| https://github.com/microsoft/fluentui/pull/36405 | `microsoft/fluentui` | `code_only` | `typescript` | fix(MessageBar): v9 MessageBar Resize Flicker Fix |
| https://github.com/microsoft/fluentui/pull/36393 | `microsoft/fluentui` | `code_and_docs` | `typescript` | feat: group Dependabot updates and add a repeatable rollup task |
| https://github.com/microsoft/fluentui/pull/36401 | `microsoft/fluentui` | `code_only` | `typescript` | fix(priority-overflow): avoid teardown notifications |
| https://github.com/microsoft/fluentui/pull/36381 | `microsoft/fluentui` | `code_only` | `typescript` | ci: scope headless experimental yarn change to release-headless config |
| https://github.com/microsoft/fluentui/pull/36379 | `microsoft/fluentui` | `code_only` | `typescript` | fix(web-components): fix focusgroup in tree when focusgroup is natively supported |
| https://github.com/microsoft/fluentui/pull/36374 | `microsoft/fluentui` | `code_only` | `typescript` | ci(monosize): upgrade to monosize 0.9 and switch bundle-size storage from Azure to git |
| https://github.com/microsoft/fluentui/pull/36377 | `microsoft/fluentui` | `code_only` | `typescript` | ci: add experimental headless release pipeline |
| https://github.com/microsoft/fluentui/pull/36375 | `microsoft/fluentui` | `code_only` | `typescript` | chore: upgrade webpack to 5.108.4 |
| https://github.com/microsoft/fluentui/pull/36372 | `microsoft/fluentui` | `code_and_docs` | `typescript` | docs(web-components): Update v2 to v3 migration doc |
| https://github.com/microsoft/fluentui/pull/36373 | `microsoft/fluentui` | `code_and_docs` | `typescript` | docs(web-components): fix sticker sheet quirks |
| https://github.com/microsoft/fluentui/pull/36371 | `microsoft/fluentui` | `code_only` | `typescript` | fix(web-components): selected indicator position in vertical tablist |
| https://github.com/microsoft/fluentui/pull/36353 | `microsoft/fluentui` | `code_and_docs` | `typescript` | feat(react-tag-picker): export headless building blocks and align TagPicker with base-type pattern |
| https://github.com/microsoft/fluentui/pull/36367 | `microsoft/fluentui` | `code_and_docs` | `typescript` | docs(web-components): add component sticker sheet page to storybook |
| https://github.com/microsoft/fluentui/pull/36276 | `microsoft/fluentui` | `code_only` | `typescript` | fix(react-charts): prevent DonutChart from growing infinitely inside an unconstrained ResponsiveContainer |
| https://github.com/microsoft/fluentui/pull/36358 | `microsoft/fluentui` | `code_and_docs` | `typescript` | feat(react-storybook-addon): allow theme picker options configuration |
| https://github.com/microsoft/fluentui/pull/36356 | `microsoft/fluentui` | `code_and_docs` | `typescript` | Promote web components to stable |
| https://github.com/microsoft/fluentui/pull/36336 | `microsoft/fluentui` | `code_and_docs` | `typescript` | fix(react-file-type-icons): update CDN to 20260623 drop, new file icon registrations for PowerBI etc, aligned to v9 boostrap of pkg |
| https://github.com/microsoft/fluentui/pull/36355 | `microsoft/fluentui` | `code_only` | `typescript` | fix(web-components): set focus on autofocus element when a dialog is open |
| https://github.com/microsoft/fluentui/pull/36354 | `microsoft/fluentui` | `code_only` | `typescript` | fix(fluent2-theme): high contrast focus styles for PrimaryButton |
| https://github.com/microsoft/fluentui/pull/36352 | `microsoft/fluentui` | `code_only` | `typescript` | fix: update link focus style to match latest treatment |
| https://github.com/microsoft/fluentui/pull/36320 | `microsoft/fluentui` | `code_and_docs` | `typescript` | feat(react-headless-components-preview): add headless MenuButton |
| https://github.com/microsoft/fluentui/pull/36345 | `microsoft/fluentui` | `code_only` | `typescript` | fix(react-button): do not expose default menuIcon in useMenuButtonBase_unstable |
| https://github.com/microsoft/fluentui/pull/36343 | `microsoft/fluentui` | `code_only` | `typescript` | fix(Calendar): year prev/next buttons don't lose focus when they become disabled |
| https://github.com/microsoft/fluentui/pull/36338 | `microsoft/fluentui` | `code_only` | `typescript` | fix: ensure toggle button text is readable in high contrast themes |
| https://github.com/microsoft/fluentui/pull/36340 | `microsoft/fluentui` | `code_only` | `typescript` | fix: add accessible name to message bar stories dismiss button and fixup component color in dark mode |
| https://github.com/microsoft/fluentui/pull/36335 | `microsoft/fluentui` | `code_only` | `typescript` | fix(react-headless-components-preview): fix Tooltip, Dialog, Menu, and Popover trigger components |
| https://github.com/microsoft/fluentui/pull/36342 | `microsoft/fluentui` | `code_only_tests_or_fixtures` | `typescript` | chore: fix inline and wrapping examples in link stories |
| https://github.com/microsoft/fluentui/pull/36341 | `microsoft/fluentui` | `code_only_tests_or_fixtures` | `typescript` | chore: fix tab panel content example in stories |
| https://github.com/microsoft/fluentui/pull/36339 | `microsoft/fluentui` | `code_only` | `typescript` | fix: ensure accordion content inherits color properly |
| https://github.com/microsoft/fluentui/pull/36329 | `microsoft/fluentui` | `code_only` | `typescript` | fix(web-components): SB docsite build |
| https://github.com/microsoft/fluentui/pull/36319 | `microsoft/fluentui` | `code_and_docs` | `typescript` | feat(react-button): add useMenuButtonBase_unstable base hook |
| https://github.com/microsoft/fluentui/pull/36325 | `microsoft/fluentui` | `code_only` | `typescript` | test(react-button): add hook regression tests for MenuButton |
| https://github.com/microsoft/fluentui/pull/36321 | `microsoft/fluentui` | `code_and_docs` | `typescript` | fix(web-components): fix anchor positioning for RTL |
| https://github.com/microsoft/fluentui/pull/36305 | `microsoft/fluentui` | `code_and_docs` | `typescript` | feat(react-headless-components-preview):  add headless Overflow |
| https://github.com/microsoft/fluentui/pull/36313 | `microsoft/fluentui` | `code_only` | `typescript` | fix: Escape in an open Menu does not trigger tabster actions |
| https://github.com/microsoft/fluentui/pull/36076 | `microsoft/fluentui` | `code_and_docs` | `typescript` | fix: updates web-components broken release |
| https://github.com/microsoft/fluentui/pull/36254 | `microsoft/fluentui` | `code_only` | `typescript` | feat(eslint-plugin): wire base-hook-signature and base-hook-no-forbidden-runtime |
| https://github.com/microsoft/fluentui/pull/36253 | `microsoft/fluentui` | `code_only` | `typescript` | feat(eslint-rules): add base-hook-no-forbidden-runtime rule |
| https://github.com/microsoft/fluentui/pull/36312 | `microsoft/fluentui` | `code_only` | `typescript` | fix(react-checkbox, react-input, react-select, react-spinbutton): merge Field control props in base hooks |
| https://github.com/microsoft/fluentui/pull/36311 | `microsoft/fluentui` | `code_and_docs` | `typescript` | feat(react-headless-components-preview): export useRadioGroupContextValues from RadioGroup |
| https://github.com/microsoft/fluentui/pull/36303 | `microsoft/fluentui` | `code_and_docs` | `typescript` | fix(react-headless-components-preview): export useSkeletonContextValues from Skeleton |
| https://github.com/microsoft/fluentui/pull/36275 | `microsoft/fluentui` | `code_only` | `typescript` | fix: Escape in an open Combobox or Dropdown does not trigger tabster actions |
| https://github.com/microsoft/fluentui/pull/36304 | `microsoft/fluentui` | `code_and_docs` | `typescript` | feat(react-overflow): split and expose hooks for headless reuse |
| https://github.com/microsoft/fluentui/pull/36187 | `microsoft/fluentui` | `code_and_docs` | `typescript` | docs(react-dialog): add comprehensive nested dialogs documentation |
| https://github.com/microsoft/fluentui/pull/36296 | `microsoft/fluentui` | `code_and_docs` | `typescript` | fix(web-components): make sure `autofocus` works on all focusable custom elements during initial page load |
| https://github.com/microsoft/fluentui/pull/36302 | `microsoft/fluentui` | `code_and_docs` | `typescript` | feat(react-headless-components-preview): stabilize Dialog function and hook exports |
| https://github.com/microsoft/fluentui/pull/36301 | `microsoft/fluentui` | `code_only` | `typescript` | fix(react-headless-components-preview): add missing jsx-runtime dependency |
| https://github.com/microsoft/fluentui/pull/36300 | `microsoft/fluentui` | `code_and_docs` | `typescript` | fix(react-headless-components-preview): export useContextValues for components requiring context in render functions |
| https://github.com/microsoft/fluentui/pull/36297 | `microsoft/fluentui` | `code_only` | `typescript` | fix(deps): patch critical/high CVEs in transitive deps (minimatch, handlebars, shell-quote, basic-ftp) |
| https://github.com/microsoft/fluentui/pull/36278 | `microsoft/fluentui` | `code_only` | `typescript` | fix(web-components): avoid dialog from focusing on non-active tab upon showing |
| https://github.com/microsoft/fluentui/pull/36284 | `microsoft/fluentui` | `code_only` | `typescript` | fix(eslint-plugin-react-components): remove invalid ESM module entrypoint |
| https://github.com/microsoft/fluentui/pull/36261 | `microsoft/fluentui` | `code_only` | `typescript` | feat(react-headless-components): use AriaLiveAnnouncer for Toast component and update tests |
| https://github.com/microsoft/fluentui/pull/36277 | `microsoft/fluentui` | `code_only` | `typescript` | fix(Link): add disabled styles for high contrast mode |
| https://github.com/microsoft/fluentui/pull/36258 | `microsoft/fluentui` | `code_only` | `typescript` | fix(web-components): make anchor position targets fixed positioned |
| https://github.com/microsoft/fluentui/pull/36264 | `microsoft/fluentui` | `code_and_docs` | `typescript` | fix(react-overflow,priority-overflow): correct overflow snapshot on first paint |
| https://github.com/microsoft/fluentui/pull/36280 | `microsoft/fluentui` | `code_only` | `typescript` | fix(deps): bump tar to >=7.5.8 to address CVE-2026-26960 |
| https://github.com/microsoft/fluentui/pull/36232 | `microsoft/fluentui` | `code_and_docs` | `typescript` | feat(web-components): add keyboard support for printable characters in Dropdown |
| https://github.com/microsoft/fluentui/pull/36260 | `microsoft/fluentui` | `code_and_docs` | `typescript` | feat(react-tag-picker): export base hooks |
| https://github.com/microsoft/fluentui/pull/36269 | `microsoft/fluentui` | `code_only_tests_or_fixtures` | `typescript` | test(react-tag-picker): add hooks regression tests |
| https://github.com/microsoft/fluentui/pull/36263 | `microsoft/fluentui` | `code_and_docs` | `typescript` | refactor(react-overflow,priority-overflow): subscribe model removes intermediate state from <Overflow> |
| https://github.com/microsoft/fluentui/pull/36266 | `microsoft/fluentui` | `code_only` | `typescript` | fix(react-tabster): support dynamic attributes in useMergedTabsterAttributes |
| https://github.com/microsoft/fluentui/pull/35666 | `microsoft/fluentui` | `code_only` | `typescript` | refactor(Calendar): migrate to motion components |
| https://github.com/microsoft/fluentui/pull/36267 | `microsoft/fluentui` | `code_and_docs` | `typescript` | feat(react-headless-components-preview): export BadgeSlots, ComboboxSlots, useMenuListContextValues to complete consumer-side composition... |
| https://github.com/microsoft/fluentui/pull/36262 | `microsoft/fluentui` | `code_and_docs` | `typescript` | refactor(react-overflow,priority-overflow): pure manager + strict-mode-safe lifecycle |
| https://github.com/microsoft/fluentui/pull/36240 | `microsoft/fluentui` | `code_and_docs` | `typescript` | fix(web-components): prevent text-input from submitting twice when Enter is pressed |
| https://github.com/microsoft/fluentui/pull/36241 | `microsoft/fluentui` | `code_only` | `typescript` | fix(web-components): remove tooltip id from target’s aria-describedby attribute when the t… |
| https://github.com/microsoft/fluentui/pull/36257 | `microsoft/fluentui` | `code_only` | `typescript` | fix(web-components): build package before running e2e tests |
| https://github.com/microsoft/fluentui/pull/36252 | `microsoft/fluentui` | `code_only` | `typescript` | feat(eslint-rules): add base-hook-signature rule |
| https://github.com/microsoft/fluentui/pull/35914 | `microsoft/fluentui` | `code_and_docs` | `typescript` | feat(react-toast): add base hooks/types and re-exports for headless composition |
| https://github.com/microsoft/fluentui/pull/36228 | `microsoft/fluentui` | `code_and_docs` | `typescript` | fix(react-tags): decouple useTagGroupBase_unstable from Tabster |
| https://github.com/microsoft/fluentui/pull/36244 | `microsoft/fluentui` | `code_and_docs` | `typescript` | fix(react-headless-components-preview): update non-modal dialog implementation to use popover API |
| https://github.com/microsoft/fluentui/pull/36245 | `microsoft/fluentui` | `code_only` | `typescript` | fix(react-headless-components-preview): descendant clicks no longer trigger dialog backdrop dismissal |
| https://github.com/microsoft/fluentui/pull/36246 | `microsoft/fluentui` | `code_only` | `typescript` | fix(ci): install latest 22.x Node to satisfy @microsoft/fast-build engines |
| https://github.com/microsoft/fluentui/pull/36229 | `microsoft/fluentui` | `code_and_docs` | `typescript` | test(react-tags): add hook regression tests for Tag family |
| https://github.com/microsoft/fluentui/pull/36235 | `microsoft/fluentui` | `code_only` | `typescript` | Revert removal of Griffel dependency from usePortalMount |
| https://github.com/microsoft/fluentui/pull/35720 | `microsoft/fluentui` | `code_only` | `typescript` | refactor(react-switch): add base state hooks for Switch component |
| https://github.com/microsoft/fluentui/pull/35639 | `microsoft/fluentui` | `code_only` | `typescript` | Fix Popover positioning docs link resolving to iframe URL |
| https://github.com/microsoft/fluentui/pull/35824 | `microsoft/fluentui` | `code_and_docs` | `typescript` | feat(react-card): add useCardBase_unstable hook |
| https://github.com/microsoft/fluentui/pull/35825 | `microsoft/fluentui` | `code_and_docs` | `typescript` | feat(react-search): add useSearchBoxBase_unstable hook |
| https://github.com/open-telemetry/opentelemetry-python/pull/5407 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | opentelemetry-configuration: substitute env vars after parsing (#5406) |
| https://github.com/open-telemetry/opentelemetry-python/pull/5563 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | ci: use shared OSSF Scorecard workflow |
| https://github.com/open-telemetry/opentelemetry-python/pull/5562 | `open-telemetry/opentelemetry-python` | `code_only_tests_or_fixtures` | `python` | fix: otel-weaver flaky tests |
| https://github.com/open-telemetry/opentelemetry-python/pull/5266 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | Expand `attribute` value type to support complex values everywhere and cleanup surrounding code |
| https://github.com/open-telemetry/opentelemetry-python/pull/5453 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | Fix TypeError in os.fork() for garbage-collected processors |
| https://github.com/open-telemetry/opentelemetry-python/pull/5354 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | Add AlwaysRecordSampler |
| https://github.com/open-telemetry/opentelemetry-python/pull/5415 | `open-telemetry/opentelemetry-python` | `code_only_tests_or_fixtures` | `python` | Fix Flaky opentelemetry-sdk tests |
| https://github.com/open-telemetry/opentelemetry-python/pull/5440 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | Add typechecking to the Jaeger propagator |
| https://github.com/open-telemetry/opentelemetry-python/pull/5122 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | opentelemetry-exporter-prometheus: add support to configure Resource attributes as metric labels |
| https://github.com/open-telemetry/opentelemetry-python/pull/5540 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | chore(ci): update ci |
| https://github.com/open-telemetry/opentelemetry-python/pull/5548 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | fix: benchmarks ci |
| https://github.com/open-telemetry/opentelemetry-python/pull/5535 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | opentelemetry-sdk: fix values for process.executable resource attributes |
| https://github.com/open-telemetry/opentelemetry-python/pull/5534 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | opentelemetry-configuration: fix default service name |
| https://github.com/open-telemetry/opentelemetry-python/pull/5513 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | fix(sdk): correct instrument name validation error message length |
| https://github.com/open-telemetry/opentelemetry-python/pull/5430 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | Fix View instrument-name matching to be case-insensitive and platform-independent |
| https://github.com/open-telemetry/opentelemetry-python/pull/5520 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | chore(ci): pin dependencies |
| https://github.com/open-telemetry/opentelemetry-python/pull/5523 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | build(deps-dev): bump gitpython from 3.1.52 to 3.1.58 |
| https://github.com/open-telemetry/opentelemetry-python/pull/5512 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | Drop and count spans ended after SimpleSpanProcessor shutdown as already_shutdown |
| https://github.com/open-telemetry/opentelemetry-python/pull/5522 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | ci: use uv action instead of pip install tox-uv |
| https://github.com/open-telemetry/opentelemetry-python/pull/5516 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | infra: pin digest SHA for github-actions |
| https://github.com/open-telemetry/opentelemetry-python/pull/5509 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | Count post-shutdown-dropped records as `already_shutdown` on processor.processed |
| https://github.com/open-telemetry/opentelemetry-python/pull/5472 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | Count otel.sdk.processor.{span,log}.processed at exporter-submit time |
| https://github.com/open-telemetry/opentelemetry-python/pull/5437 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | opentelemetry-sdk: make methods on FixedSizeExemplarReservoirABC thread safe |
| https://github.com/open-telemetry/opentelemetry-python/pull/5471 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | Upgrade ruff to 0.16 |
| https://github.com/open-telemetry/opentelemetry-python/pull/5465 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | Import code_attributes from stable semconv package |
| https://github.com/open-telemetry/opentelemetry-python/pull/5412 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | opentelemetry-exporter-otlp-json-file: add OTLP JSON file Docker tests |
| https://github.com/open-telemetry/opentelemetry-python/pull/5351 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | feat(config): wire top-level log_level field in declarative configuration |
| https://github.com/open-telemetry/opentelemetry-python/pull/5436 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | opentelemetry-configuration: resolve false-positive warning logs for newer schema minor version |
| https://github.com/open-telemetry/opentelemetry-python/pull/5454 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | opentelemetry-configuration: treat present-null config value as empty mapping |
| https://github.com/open-telemetry/opentelemetry-python/pull/5456 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | build(deps-dev): bump gitpython from 3.1.50 to 3.1.52 |
| https://github.com/open-telemetry/opentelemetry-python/pull/5455 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | Fix copy-pasted log message in SpanContext.__delattr__ |
| https://github.com/open-telemetry/opentelemetry-python/pull/5434 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | Fix missing f-prefix in exponential histogram max_size error messages |
| https://github.com/open-telemetry/opentelemetry-python/pull/5369 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | opentelemetry-exporter-otlp-proto-http: add max request size limit to OTLP HTTP exporters |
| https://github.com/open-telemetry/opentelemetry-python/pull/5408 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | Substitute empty for unset config env vars without defaults |
| https://github.com/open-telemetry/opentelemetry-python/pull/5417 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | Fixup eachdist.py handling of package names |
| https://github.com/open-telemetry/opentelemetry-python/pull/5366 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | opentelemetry-api: remove env carrier environment snapshot caching |
| https://github.com/open-telemetry/opentelemetry-python/pull/5413 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | opentelemetry-semantic-conventions: Bump to 1.43.0 |
| https://github.com/open-telemetry/opentelemetry-python/pull/5404 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | Update otelbot token workflows to use client IDs |
| https://github.com/open-telemetry/opentelemetry-python/pull/5399 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | Fix Context in-place mutability bypass via inherited dict methods |
| https://github.com/open-telemetry/opentelemetry-python/pull/5410 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | Bump semconv to 1.42.0 |
| https://github.com/open-telemetry/opentelemetry-python/pull/5294 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | opentelemetry-sdk: add 'force_flush' method to LogRecordExporter ABC |
| https://github.com/open-telemetry/opentelemetry-python/pull/5327 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | opentelemetry-sdk: expose SynchronousMultiLogRecordProcessor and ConcurrentMultiLogRecordProcessor publicly |
| https://github.com/open-telemetry/opentelemetry-python/pull/5280 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | opentelemetry-sdk: Add ability to refresh process sensitive Resource attributes |
| https://github.com/open-telemetry/opentelemetry-python/pull/5300 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | opentelemetry-sdk: add log record limits environment variables |
| https://github.com/open-telemetry/opentelemetry-python/pull/5372 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | opentelemetry-sdk: activate instrumentors from declarative config |
| https://github.com/open-telemetry/opentelemetry-python/pull/5370 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | opentelemetry-exporter-otlp-proto-http: fix metric self-observability over-count on batch split |
| https://github.com/open-telemetry/opentelemetry-python/pull/5377 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | Add record_min_max option to exponential histogram aggregation |
| https://github.com/open-telemetry/opentelemetry-python/pull/5296 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | fix(sdk): add max_spans limit to InMemorySpanExporter |
| https://github.com/open-telemetry/opentelemetry-python/pull/5293 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | Remove Events API/SDK |
| https://github.com/open-telemetry/opentelemetry-python/pull/5364 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | Update ProcessResourceDetector to not set full CLI attrs by default |
| https://github.com/open-telemetry/opentelemetry-python/pull/5265 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | feat(sdk): add MissingDependencyError for declarative configuration |
| https://github.com/open-telemetry/opentelemetry-python/pull/5353 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | docs(config): document OTEL_PYTHON_* bypass when OTEL_CONFIG_FILE is set |
| https://github.com/open-telemetry/opentelemetry-python/pull/5336 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | opentelemetry-sdk: drop NaN measurements at instrument level to prevent aggregation poisoning |
| https://github.com/open-telemetry/opentelemetry-python/pull/5340 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | fix: raise ValueError for unsorted ExplicitBucketHistogramAggregation boundaries |
| https://github.com/open-telemetry/opentelemetry-python/pull/5220 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | opentelemetry-docker-tests: Refactor Docker tests to properly validate contents of exported telemetry |
| https://github.com/open-telemetry/opentelemetry-python/pull/5329 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | opentelemetry-sdk: revert RLock back to Lock |
| https://github.com/open-telemetry/opentelemetry-python/pull/5363 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | feat(config): wire id_generator from declarative configuration to TracerProvider |
| https://github.com/open-telemetry/opentelemetry-python/pull/5383 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | Refresh uv.lock |
| https://github.com/open-telemetry/opentelemetry-python/pull/5252 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | opentelemetry-exporter-otlp-common: add shared package for common OTLP utilities |
| https://github.com/open-telemetry/opentelemetry-python/pull/5311 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | opentelemetry-sdk: add support for file exporter with declarative config |
| https://github.com/open-telemetry/opentelemetry-python/pull/5345 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | feat(config): bump declarative configuration schema to v1.1.0 |
| https://github.com/open-telemetry/opentelemetry-python/pull/4977 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | fix(logs): optimize LogRecord memory by removing redundant context |
| https://github.com/open-telemetry/opentelemetry-python/pull/5320 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | opentelemetry-exporter-http-transport: enable entry-point loading of transport implementations |
| https://github.com/open-telemetry/opentelemetry-python/pull/5251 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | opentelemetry-proto: bump maximum supported protobuf version to 7.x.x |
| https://github.com/open-telemetry/opentelemetry-python/pull/5328 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | opentelemetry-api: normalize empty environment propagation names to "_" in EnvironmentSetter and EnvironmentGetter |
| https://github.com/open-telemetry/opentelemetry-python/pull/5326 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | opentelemetry-sdk: merge doesn't need a copy, dict already does this |
| https://github.com/open-telemetry/opentelemetry-python/pull/5271 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | feat(config): support OTEL_CONFIG_FILE in the SDK configurator |
| https://github.com/open-telemetry/opentelemetry-python/pull/5201 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | Add support for composite samplers in declarative config |
| https://github.com/open-telemetry/opentelemetry-python/pull/5305 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | Update json and proto encoder to always accept None type, cleanup code / tests a little bit |
| https://github.com/open-telemetry/opentelemetry-python/pull/5324 | `open-telemetry/opentelemetry-python` | `code_only_tests_or_fixtures` | `python` | chore: cleanup typo found in test |
| https://github.com/open-telemetry/opentelemetry-python/pull/5321 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | opentelemetry-sdk: make 'consume_measurement' lock free |
| https://github.com/open-telemetry/opentelemetry-python/pull/5315 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | feat(config): validate declarative config file_format version |
| https://github.com/open-telemetry/opentelemetry-python/pull/5289 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | opentelemetry-api: update EnvironmentGetter to ignore non-normalized environment variable names |
| https://github.com/open-telemetry/opentelemetry-python/pull/5277 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | Remove typing aliases deprecated in python 3.9. Also replace usages of typing.Union/Optional with \| |
| https://github.com/open-telemetry/opentelemetry-python/pull/5307 | `open-telemetry/opentelemetry-python` | `code_only_tests_or_fixtures` | `python` | test(config): use file_format 1.0 in test fixtures |
| https://github.com/open-telemetry/opentelemetry-python/pull/5123 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | feat: add support for configuring metric scope labels |
| https://github.com/open-telemetry/opentelemetry-python/pull/5298 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | opentelemetry-sdk: reduce lock contention in attributes |
| https://github.com/open-telemetry/opentelemetry-python/pull/5299 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | opentelemetry-sdk: update declarative config to use ServiceInstanceIdResourceDetector |
| https://github.com/open-telemetry/opentelemetry-python/pull/5207 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | feat: add file exporter implementation |
| https://github.com/open-telemetry/opentelemetry-python/pull/5297 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | opentelemetry-sdk: update iterator for BoundedList |
| https://github.com/open-telemetry/opentelemetry-python/pull/5270 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | feat(config): add configure_sdk orchestrator for declarative config |
| https://github.com/open-telemetry/opentelemetry-python/pull/5194 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | feat: add opentelemetry-exporter-http-transport package |
| https://github.com/open-telemetry/opentelemetry-python/pull/4646 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | opentelemetry-sdk: sketch of an OpAMP integration |
| https://github.com/open-telemetry/opentelemetry-python/pull/5292 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | chore: Clean up stale Python 3.10 baseline TODOs |
| https://github.com/open-telemetry/opentelemetry-python/pull/5288 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | opentelemetry-api: remove unnecessary copy in iterator |
| https://github.com/open-telemetry/opentelemetry-python/pull/5259 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | opentelemetry-sdk: add ServiceInstanceIdResourceDetector for populating service.instance.id |
| https://github.com/open-telemetry/opentelemetry-python/pull/5287 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | opentelemetry-sdk: remove generator in the accessor for links/events |
| https://github.com/open-telemetry/opentelemetry-python/pull/5269 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | feat(config): recursively convert parsed dicts to typed dataclasses in loader |
| https://github.com/open-telemetry/opentelemetry-python/pull/5275 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | opentelemetry-sdk: inline the method `_clean_attribute_value` |
| https://github.com/open-telemetry/opentelemetry-python/pull/5274 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | opentelemetry-sdk: remove unnecessary dict in set_attribute method |
| https://github.com/open-telemetry/opentelemetry-python/pull/5250 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | opentelemetry-api: fix SelectableGroups deprecation warning |
| https://github.com/open-telemetry/opentelemetry-python/pull/5272 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | opentelemetry-sdk: remove copy on span instantiation |
| https://github.com/open-telemetry/opentelemetry-python/pull/5215 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | refactor(config): add shared _resolve_component utility for plugin loading |
| https://github.com/open-telemetry/opentelemetry-python/pull/5214 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | refactor(config): rename 'known/unknown' to 'built-in/user-defined' terminology |
| https://github.com/open-telemetry/opentelemetry-python/pull/5143 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | Add error details to OTLP GRPC exporter error messages.. |
| https://github.com/open-telemetry/opentelemetry-python/pull/4863 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | New APIs to add/remove metric readers at run-time |
| https://github.com/open-telemetry/opentelemetry-python/pull/5247 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | fix(infra): Backport of patch release changelog to main |
| https://github.com/open-telemetry/opentelemetry-python/pull/5144 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | api: conditionally load entrypoints for OTEL_PYTHON_CONTEXT |
| https://github.com/open-telemetry/opentelemetry-python/pull/5243 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | [release/v1.42.x-0.63bx] Prepare release 1.42.1/0.63b1 |
| https://github.com/open-telemetry/opentelemetry-python/pull/5242 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | [release/v1.42.x-0.63bx] Preserve random trace ID flag for child spans |
| https://github.com/open-telemetry/opentelemetry-python/pull/5241 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | Preserve random trace ID flag for child spans |
| https://github.com/open-telemetry/opentelemetry-python/pull/5233 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | document merge queue deadlock workaround and merge order |
| https://github.com/open-telemetry/opentelemetry-python/pull/5017 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | docs: add missing modules to sphinx documentation build |
| https://github.com/open-telemetry/opentelemetry-python/pull/5224 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | opentelemetry-proto-json: update to use opentelemetry-proto v1.10.0 |
| https://github.com/open-telemetry/opentelemetry-python/pull/5223 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | Bump bundled opentelemetry-proto to v1.10.0 and regenerate |
| https://github.com/open-telemetry/opentelemetry-python/pull/5216 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | feat(config): add pull metric reader support to declarative config |
| https://github.com/open-telemetry/opentelemetry-python/pull/5209 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | ci: Enable GitHub Merge Queue support |
| https://github.com/open-telemetry/opentelemetry-python/pull/5075 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | fix(config): allow deflate for OTLP HTTP exporters |
| https://github.com/open-telemetry/opentelemetry-python/pull/5212 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | ci: validate changelog fragment filenames |
| https://github.com/open-telemetry/opentelemetry-python/pull/5128 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | feat(config): exporter plugin loading via entry points for declarative config |
| https://github.com/open-telemetry/opentelemetry-python/pull/5129 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | feat(config): generic resource detector plugin loading for declarative config |
| https://github.com/open-telemetry/opentelemetry-python/pull/5106 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | sdk/metrics: copy attributes dict to prevent post-recording mutation |
| https://github.com/open-telemetry/opentelemetry-python/pull/5098 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | feat(config): propagator plugin loading via entry points for declarative config |
| https://github.com/open-telemetry/opentelemetry-python/pull/5208 | `open-telemetry/opentelemetry-python` | `code_only_tests_or_fixtures` | `python` | weaver live check: send weaver logs to tmp file instead of pipe to avoid overflow |
| https://github.com/open-telemetry/opentelemetry-python/pull/5203 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | Remove importlib-metadata dependency |
| https://github.com/open-telemetry/opentelemetry-python/pull/5200 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | Bump semconv to 1.41.1 |
| https://github.com/open-telemetry/opentelemetry-python/pull/5030 | `open-telemetry/opentelemetry-python` | `code_only_tests_or_fixtures` | `python` | Add docker-tests coverage of metrics export |
| https://github.com/open-telemetry/opentelemetry-python/pull/4056 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | Benchmarks job is failing on CI |
| https://github.com/open-telemetry/opentelemetry-python/pull/5187 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | ci: introduce towncrier to generate changelog from fragments |
| https://github.com/open-telemetry/opentelemetry-python/pull/4854 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | feat: add support for 'random-trace-id' flags in W3C traceparent header trace flags |
| https://github.com/open-telemetry/opentelemetry-python/pull/5179 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | fix(sdk): improve force flush logic |
| https://github.com/open-telemetry/opentelemetry-python/pull/5193 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | chore(deps-dev): bump gitpython from 3.1.47 to 3.1.50 |
| https://github.com/open-telemetry/opentelemetry-python/pull/5151 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | feat: Add ability to selectively enable exporting of SDK internal metrics |
| https://github.com/open-telemetry/opentelemetry-python/pull/5055 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | Add registry keyword argument to PrometheusMetricReader |
| https://github.com/open-telemetry/opentelemetry-python/pull/5095 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | feat(config): sampler plugin loading via entry points for declarative config |
| https://github.com/open-telemetry/opentelemetry-python/pull/5145 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | update SDK to call version directly |
| https://github.com/open-telemetry/opentelemetry-python/pull/5119 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | feat: update EnvironmentGetter and EnvironmentSetter to use normalized environment variable names |
| https://github.com/open-telemetry/opentelemetry-python/pull/5116 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | misc: set opentelemetry-codegen-json package version to '0.0.0' |
| https://github.com/open-telemetry/opentelemetry-python/pull/4917 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | feat: make retryable gRPC error codes configurable for gRPC exporters |
| https://github.com/open-telemetry/opentelemetry-python/pull/5026 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | ci: add GHA to add PRs to project board when marked ready for review |
| https://github.com/open-telemetry/opentelemetry-python/pull/5163 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | Fix/baggage propagator outbound limits |
| https://github.com/open-telemetry/opentelemetry-python/pull/5142 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | opentelemetry-test-utils: don't install grpc in test requirements on PyPy  |
| https://github.com/open-telemetry/opentelemetry-python/pull/5135 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | Use a covariant type for detectors argument |
| https://github.com/open-telemetry/opentelemetry-python/pull/5153 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | Bump GitPython to latest 3.1.47 |
| https://github.com/open-telemetry/opentelemetry-python/pull/5162 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | ci: only check new links on pull requests to avoid rate limiting |
| https://github.com/open-telemetry/opentelemetry-python/pull/5131 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | feat(config): add additionalProperties support to generated config models |
| https://github.com/open-telemetry/opentelemetry-python/pull/5138 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | [release/v1.41.x-0.62bx] Prepare release 1.41.1/0.62b1 |
| https://github.com/open-telemetry/opentelemetry-python/pull/5137 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | Unreleased changelog for 1.41.1 |
| https://github.com/open-telemetry/opentelemetry-python/pull/5083 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | fix(sdk): use sys.orig_argv for process.command to handle python -m invocations |
| https://github.com/open-telemetry/opentelemetry-python/pull/5120 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | feat: make resource detector ordering deterministic |
| https://github.com/open-telemetry/opentelemetry-python/pull/5105 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | Misc fixes towards opentelemetry-sdk being type checked |
| https://github.com/open-telemetry/opentelemetry-python/pull/5088 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | Weaver live check test util |
| https://github.com/open-telemetry/opentelemetry-python/pull/4930 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | docs: document why map_to_index assumes value is not 0, inf, or NaN |
| https://github.com/open-telemetry/opentelemetry-python/pull/4981 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | Fix logarithm mapping max scale comment and align with Go implementation |
| https://github.com/open-telemetry/opentelemetry-python/pull/5130 | `open-telemetry/opentelemetry-python` | `code_only_tests_or_fixtures` | `python` | Fix flaky test_race_concurrent_measurements on Windows CI |
| https://github.com/open-telemetry/opentelemetry-python/pull/4976 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | feat(sdk): implement exporter metrics |
| https://github.com/open-telemetry/opentelemetry-python/pull/5082 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | opentelemetry-sdk: fix typing issues for metrics instruments |
| https://github.com/open-telemetry/opentelemetry-python/pull/5077 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | Fix shim docstring example |
| https://github.com/open-telemetry/opentelemetry-python/pull/5093 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | feat(config): add shared load_entry_point utility for declarative config plugin loading |
| https://github.com/open-telemetry/opentelemetry-python/pull/5114 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | Add rst files for link checking |
| https://github.com/open-telemetry/opentelemetry-python/pull/5096 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | semconv: use X \| Y union annotation |
| https://github.com/open-telemetry/opentelemetry-python/pull/5091 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | fix(config): prevent YAML structure injection via env var substitution |
| https://github.com/open-telemetry/opentelemetry-python/pull/5102 | `open-telemetry/opentelemetry-python` | `code_only_tests_or_fixtures` | `python` | opentelemetry-sdk: make test_force_flush_late_by_timeout less flaky on pypy/windows |
| https://github.com/open-telemetry/opentelemetry-python/pull/5090 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | scripts: drop unused update_sha.py |
| https://github.com/open-telemetry/opentelemetry-python/pull/5036 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | Redo OTLPMetricExporter unit tests of `max_export_batch_size` to use real `export` |
| https://github.com/open-telemetry/opentelemetry-python/pull/4990 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | feat(config): Add LoggerProvider support for declarative config |
| https://github.com/open-telemetry/opentelemetry-python/pull/4908 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | Add logger exception support for logs API/SDK |
| https://github.com/open-telemetry/opentelemetry-python/pull/5081 | `open-telemetry/opentelemetry-python` | `code_only_tests_or_fixtures` | `python` | opentelemetry-sdk: make SynchronousMeasurementConsumer collect deadline test more robust |
| https://github.com/open-telemetry/opentelemetry-python/pull/5003 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | feat(config): add service resource detector support for declarative config |
| https://github.com/open-telemetry/opentelemetry-python/pull/5078 | `open-telemetry/opentelemetry-python` | `code_only_tests_or_fixtures` | `python` | Fix tracer_scope argument in benchmark test |
| https://github.com/open-telemetry/opentelemetry-python/pull/5063 | `open-telemetry/opentelemetry-python` | `code_only_tests_or_fixtures` | `python` | opentelemetry-sdk: fix a couple of unbound variables in tests |
| https://github.com/open-telemetry/opentelemetry-python/pull/5066 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | eachdist.ini: opentelemetry-proto-json is still a prerelease |
| https://github.com/open-telemetry/opentelemetry-python/pull/5062 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | opentelemetry-sdk: fix a bunch of wrong type imports |
| https://github.com/open-telemetry/opentelemetry-python/pull/5065 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | Update version to 1.42.0.dev/0.63b0.dev |
| https://github.com/open-telemetry/opentelemetry-python/pull/5064 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | [release/v1.41.x-0.62bx] Prepare release 1.41.0/0.62b0 |
| https://github.com/open-telemetry/opentelemetry-python/pull/5004 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | feat(config): wire container resource detector via entry point loading |
| https://github.com/open-telemetry/opentelemetry-python/pull/5002 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | feat(config): add host resource detector support for declarative config |
| https://github.com/open-telemetry/opentelemetry-python/pull/4979 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | feat(config): add resource and propagator creation from declarative config |
| https://github.com/open-telemetry/opentelemetry-python/pull/4985 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | feat(config): Add TracerProvider support for declarative config |
| https://github.com/open-telemetry/opentelemetry-python/pull/4987 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | feat(config): Add MeterProvider support for declarative config |
| https://github.com/open-telemetry/opentelemetry-python/pull/4980 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | feat: add experimental logger configurator |
| https://github.com/open-telemetry/opentelemetry-python/pull/5061 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | misc: update version for codegen-json and proto-json packages |
| https://github.com/open-telemetry/opentelemetry-python/pull/5021 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | feat(config): add shared _parse_headers helper for declarative config exporters |
| https://github.com/open-telemetry/opentelemetry-python/pull/5001 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | feat(config): add process resource detector support for declarative config |
| https://github.com/open-telemetry/opentelemetry-python/pull/4965 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | feat(config): upgrade OTel configuration schema to v1.0.0 |
| https://github.com/open-telemetry/opentelemetry-python/pull/5019 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | Enabled flake8-tidy-import rule for ruff linter |
| https://github.com/open-telemetry/opentelemetry-python/pull/460 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | Improve attributes validation |
| https://github.com/open-telemetry/opentelemetry-python/pull/454 | `open-telemetry/opentelemetry-python` | `code_and_docs` | `python` | Adding OT Collector metrics exporter |
| https://github.com/open-telemetry/opentelemetry-python/pull/312 | `open-telemetry/opentelemetry-python` | `code_only_tests_or_fixtures` | `python` | Adding link to docs |
| https://github.com/open-telemetry/opentelemetry-python/pull/5025 | `open-telemetry/opentelemetry-python` | `code_only` | `python` | Docs/fix-trace-config-docstring |
| https://github.com/microsoft/rushstack/pull/5961 | `microsoft/rushstack` | `code_only` | `typescript` | [rush] Fix manual ESRP publish pipeline runs |
| https://github.com/microsoft/rushstack/pull/5949 | `microsoft/rushstack` | `code_and_docs` | `typescript` | [rush-daemon][WS2.3][2/9] Add warm engine component factory |
| https://github.com/microsoft/rushstack/pull/5953 | `microsoft/rushstack` | `code_only` | `typescript` | Updating the publish pipelines for NPM packages |
| https://github.com/microsoft/rushstack/pull/5952 | `microsoft/rushstack` | `code_only` | `typescript` | chore: bump decoupled local dependencies |
| https://github.com/microsoft/rushstack/pull/5947 | `microsoft/rushstack` | `code_only` | `typescript` | Fix no-new-null for native private members |
| https://github.com/microsoft/rushstack/pull/5925 | `microsoft/rushstack` | `code_and_docs` | `typescript` | [api-extractor] Report unresolvable inline import paths in .d.ts rollups |
| https://github.com/microsoft/rushstack/pull/5936 | `microsoft/rushstack` | `code_and_docs` | `typescript` | [rush-daemon][WS2] Add warm workspace session foundation |
| https://github.com/microsoft/rushstack/pull/5944 | `microsoft/rushstack` | `code_only` | `typescript` | Add `npm config list` step to install-node.yaml |
| https://github.com/microsoft/rushstack/pull/5911 | `microsoft/rushstack` | `code_only` | `typescript` | chore: bump decoupled local dependencies |
| https://github.com/microsoft/rushstack/pull/5938 | `microsoft/rushstack` | `code_only` | `typescript` | Bump the github-actions group with 2 updates |
| https://github.com/microsoft/rushstack/pull/5937 | `microsoft/rushstack` | `code_only` | `typescript` | Pin GitHub Actions to full-length commit SHAs |
| https://github.com/microsoft/rushstack/pull/5928 | `microsoft/rushstack` | `code_and_docs` | `typescript` | [rush-daemon][WS2] Add daemon host bootstrap |
| https://github.com/microsoft/rushstack/pull/5933 | `microsoft/rushstack` | `code_and_docs` | `typescript` | Use native Node.js standard APIs |
| https://github.com/microsoft/rushstack/pull/5932 | `microsoft/rushstack` | `code_only` | `typescript` | Expose ParseError cause |
| https://github.com/microsoft/rushstack/pull/5929 | `microsoft/rushstack` | `code_only` | `typescript` | [playwright-browser-tunnel] Widen playwright-core peer dependency range |
| https://github.com/microsoft/rushstack/pull/5931 | `microsoft/rushstack` | `code_only` | `typescript` | Target ES2022 for Node.js packages |
| https://github.com/microsoft/rushstack/pull/5888 | `microsoft/rushstack` | `code_and_docs` | `typescript` | [rush] Add per-iteration runner persistence control |
| https://github.com/microsoft/rushstack/pull/5927 | `microsoft/rushstack` | `code_only` | `typescript` | Add Node.js 26 support |
| https://github.com/microsoft/rushstack/pull/5926 | `microsoft/rushstack` | `code_and_docs` | `typescript` | Drop Node.js 18 support |
| https://github.com/microsoft/rushstack/pull/5921 | `microsoft/rushstack` | `code_and_docs` | `typescript` | [rush-daemon] Add request scheduler foundation |
| https://github.com/microsoft/rushstack/pull/5889 | `microsoft/rushstack` | `code_and_docs` | `typescript` | [operation-graph] Add Rush-compatible operation statuses |
| https://github.com/microsoft/rushstack/pull/5802 | `microsoft/rushstack` | `code_only` | `typescript` | [rush-resolver-cache-plugin] Fix `file:` dependency context resolution mismatch (pnpm v9/v10) |
| https://github.com/microsoft/rushstack/pull/5918 | `microsoft/rushstack` | `code_only` | `typescript` | [rush-serve-dashboard] Preserve Ctrl+A in dashboard text fields |
| https://github.com/microsoft/rushstack/pull/5904 | `microsoft/rushstack` | `code_only` | `typescript` | feat(rush-lib): early cycle detection for workspace packages in rush install/update |
| https://github.com/microsoft/rushstack/pull/5702 | `microsoft/rushstack` | `code_only` | `typescript` | fix: Remove external filter in PnpmShrinkwrapFile.getIntegrityForImporter |
| https://github.com/microsoft/rushstack/pull/5919 | `microsoft/rushstack` | `code_only` | `typescript` | Align subspace registries with pipeline proxy |
| https://github.com/microsoft/rushstack/pull/5917 | `microsoft/rushstack` | `code_only` | `typescript` | Ensure Rush bootstrap precedes npmrc clearing in Azure publish pipelines |
| https://github.com/microsoft/rushstack/pull/5913 | `microsoft/rushstack` | `code_only` | `typescript` | [rush] Fix cross-subspace workspace:* dependencies failing under pnpm 11 (globalPnpmfile via pnpm-workspace.yaml) |
| https://github.com/microsoft/rushstack/pull/5916 | `microsoft/rushstack` | `code_only` | `typescript` | Change nextBump from 'minor' to 'patch' |
| https://github.com/microsoft/rushstack/pull/5915 | `microsoft/rushstack` | `code_only` | `typescript` | [rush] Treat a phased command with zero operations as success |
| https://github.com/microsoft/rushstack/pull/5907 | `microsoft/rushstack` | `code_and_docs` | `typescript` | [typings-generator] Emit declaration source maps for generated typings |
| https://github.com/microsoft/rushstack/pull/5585 | `microsoft/rushstack` | `code_and_docs` | `typescript` | Add 'rush-pnpm up' support for catalogs |
| https://github.com/microsoft/rushstack/pull/5890 | `microsoft/rushstack` | `code_only` | `typescript` | chore: bump decoupled local dependencies |
| https://github.com/microsoft/rushstack/pull/5886 | `microsoft/rushstack` | `code_only` | `typescript` | [rush] Add the `useDirectFileTransfersForBuildCache` experiment to the `rush init` template. |
| https://github.com/microsoft/rushstack/pull/5878 | `microsoft/rushstack` | `code_only` | `typescript` | [api-extractor] Fix O(n^2) condenseTokens cost |
| https://github.com/microsoft/rushstack/pull/5885 | `microsoft/rushstack` | `code_only` | `typescript` | Make the next release of Rush a minor bump. |
| https://github.com/microsoft/rushstack/pull/5883 | `microsoft/rushstack` | `code_only` | `typescript` | [rush] Avoid redundant downloads when local processes race for the same build cache entry |
| https://github.com/microsoft/rushstack/pull/5882 | `microsoft/rushstack` | `code_only` | `typescript` | [rush] Relocate remaining pnpm settings to pnpm-workspace.yaml for pnpm 11 |
| https://github.com/microsoft/rushstack/pull/5875 | `microsoft/rushstack` | `code_only` | `typescript` | [rush] Fix "rush-pnpm patch-commit" writing absolute paths into pnpm-config.json |
| https://github.com/microsoft/rushstack/pull/5881 | `microsoft/rushstack` | `code_only` | `typescript` | Enable noImplicitOverride in local builds. |
| https://github.com/microsoft/rushstack/pull/5880 | `microsoft/rushstack` | `code_and_docs` | `typescript` | [rush] Consolidate pnpm options handling into InstallHelpers.resolvePnpmSettings |
| https://github.com/microsoft/rushstack/pull/5746 | `microsoft/rushstack` | `code_and_docs` | `typescript` | Add file-based transfer APIs to build cache provider interface and all cache plugins |
| https://github.com/microsoft/rushstack/pull/5838 | `microsoft/rushstack` | `code_only` | `typescript` | [rush] Relocate pnpm settings to pnpm-workspace.yaml for pnpm 11 |
| https://github.com/microsoft/rushstack/pull/5874 | `microsoft/rushstack` | `code_only` | `typescript` | [rush] Clean up PNPM options saving |
| https://github.com/microsoft/rushstack/pull/5873 | `microsoft/rushstack` | `code_only` | `typescript` | chore: bump decoupled local dependencies |
| https://github.com/microsoft/rushstack/pull/5872 | `microsoft/rushstack` | `code_only_tests_or_fixtures` | `typescript` | [rush] Fix an issue that occurs when you run rush-lib tests twice without cleaning. |
| https://github.com/microsoft/rushstack/pull/5871 | `microsoft/rushstack` | `code_only` | `typescript` | Bump `ajv` in `@rushstack/node-core-library` to unblock vulnerable `fast-uri` transitive resolution |
| https://github.com/microsoft/rushstack/pull/5859 | `microsoft/rushstack` | `code_only` | `typescript` | [rush] Fix minimumReleaseAge and minimumReleaseAgeExclude for PNPM by moving to pnpm-workspace.yaml |
| https://github.com/microsoft/rushstack/pull/5862 | `microsoft/rushstack` | `code_only` | `typescript` | [rush] Prevent shell injection in publish commit details |
| https://github.com/microsoft/rushstack/pull/5840 | `microsoft/rushstack` | `code_only` | `typescript` | chore: bump decoupled local dependencies |
| https://github.com/microsoft/rushstack/pull/5861 | `microsoft/rushstack` | `code_only` | `typescript` | Upgrade pnpm-sync-lib to 0.3.4 in rush-lib |
| https://github.com/microsoft/rushstack/pull/5848 | `microsoft/rushstack` | `code_and_docs` | `typescript` | [webpack-plugin-utilities] Add evaluateConstantEstreeExpression |
| https://github.com/microsoft/rushstack/pull/5842 | `microsoft/rushstack` | `code_only` | `typescript` | Bump 'ws' to mitigate CVE-2026-48779. |
| https://github.com/microsoft/rushstack/pull/5797 | `microsoft/rushstack` | `code_only` | `typescript` | fix(cobuilds): add socket + connect timeout |
| https://github.com/microsoft/rushstack/pull/5815 | `microsoft/rushstack` | `code_only` | `typescript` | [package-deps-hash] Fix build cache failures in git linked worktrees caused by GIT_DIR set by pre-commit hooks |
| https://github.com/microsoft/rushstack/pull/4952 | `microsoft/rushstack` | `code_only` | `typescript` | [api-extractor] Add support for new TS declaration format when using module resolution 'bundler' or 'nodenext' |
| https://github.com/microsoft/rushstack/pull/5832 | `microsoft/rushstack` | `code_only` | `typescript` | chore: bump decoupled local dependencies |
| https://github.com/microsoft/rushstack/pull/5831 | `microsoft/rushstack` | `code_only` | `typescript` | [ts-command-line] Fix env var name shown in EnvironmentVariableParser error messages |
| https://github.com/microsoft/rushstack/pull/5824 | `microsoft/rushstack` | `code_only` | `typescript` | [heft-sass-plugin] Fix resolution of plain .css files imported via @use / @import |
| https://github.com/microsoft/rushstack/pull/5829 | `microsoft/rushstack` | `code_only` | `typescript` | chore: bump decoupled local dependencies |
| https://github.com/microsoft/rushstack/pull/5828 | `microsoft/rushstack` | `code_only` | `typescript` | [heft-jest-plugin] Fix --test-path-pattern being ignored on Jest 30 |
| https://github.com/microsoft/rushstack/pull/5827 | `microsoft/rushstack` | `code_only` | `typescript` | chore: bump decoupled local dependencies |
| https://github.com/microsoft/rushstack/pull/5818 | `microsoft/rushstack` | `code_only` | `typescript` | [rush] Include seconds in generated change file names so repeated "rush change" runs do not collide |
| https://github.com/microsoft/rushstack/pull/5826 | `microsoft/rushstack` | `code_only` | `typescript` | Make the next release of Rush a minor bump. |
| https://github.com/microsoft/rushstack/pull/5825 | `microsoft/rushstack` | `code_only` | `typescript` | chore: bump decoupled local dependencies |
| https://github.com/microsoft/rushstack/pull/5822 | `microsoft/rushstack` | `code_only` | `typescript` | fix(rush): default rush-pnpm query commands to recursive |
| https://github.com/microsoft/rushstack/pull/5817 | `microsoft/rushstack` | `code_and_docs` | `typescript` | [rush] Add pnpm 11 support: allowBuilds in pnpm-workspace.yaml |
| https://github.com/microsoft/rushstack/pull/5811 | `microsoft/rushstack` | `code_only` | `typescript` | [rush] Fix sync-back when dependencies move to devDependencies |
| https://github.com/microsoft/rushstack/pull/5819 | `microsoft/rushstack` | `code_only` | `typescript` | [heft-storybook-plugin] Add --port flag to set the Storybook dev server port in serve mode |
| https://github.com/microsoft/rushstack/pull/5820 | `microsoft/rushstack` | `code_only` | `typescript` | fix: [rush] Parse pnpm-config.json with JsonSyntax.JsonWithComments |
| https://github.com/microsoft/rushstack/pull/5814 | `microsoft/rushstack` | `code_only` | `typescript` | fix(heft-sass-plugin): set sourceMapUrl in loadAsync to prevent data:… |
| https://github.com/microsoft/rushstack/pull/5627 | `microsoft/rushstack` | `code_only` | `typescript` | [rush-lib] Add pnpm global catalog detection to rush change |
| https://github.com/microsoft/rushstack/pull/5792 | `microsoft/rushstack` | `code_only` | `typescript` | chore: bump decoupled local dependencies |
| https://github.com/microsoft/rushstack/pull/5806 | `microsoft/rushstack` | `code_only` | `typescript` | Add opt-in sourceMap option to emit .css.map files and sourceMappingURL comments alongside compiled CSS |
| https://github.com/microsoft/rushstack/pull/5809 | `microsoft/rushstack` | `code_only` | `typescript` | [debug-certificate-manager] add homeDirectory config |
| https://github.com/microsoft/rushstack/pull/5799 | `microsoft/rushstack` | `code_only` | `typescript` | Fix: [api-extractor] Syntax error in resulting d.ts file |
| https://github.com/microsoft/rushstack/pull/5804 | `microsoft/rushstack` | `code_only` | `typescript` | [rush] Route lockfile-changed warning to stderr (fixes #5406) |
| https://github.com/microsoft/rushstack/pull/5805 | `microsoft/rushstack` | `code_only` | `typescript` | [package-deps-hash] Skip Windows reserved device names when computing repo state (fixes #5604) |
| https://github.com/microsoft/rushstack/pull/5681 | `microsoft/rushstack` | `code_only` | `typescript` | feat(heft-storybook-plugin): add `--quiet` opt-out and `--no-open` flag |
| https://github.com/microsoft/rushstack/pull/5796 | `microsoft/rushstack` | `code_only` | `typescript` | Bump postcss@~8.5.10 to address CVE GHSA-qx2v-qp2m-jg93 |
| https://github.com/microsoft/rushstack/pull/5795 | `microsoft/rushstack` | `code_only` | `typescript` | chore: bump ws to ~8.20.0 |
| https://github.com/microsoft/rushstack/pull/5642 | `microsoft/rushstack` | `code_only` | `typescript` | [rush] Fix .npmrc syncing cache bug that strips pnpm hoisting properties |
| https://github.com/microsoft/rushstack/pull/5790 | `microsoft/rushstack` | `code_only` | `typescript` | chore: bump decoupled local dependencies |
| https://github.com/microsoft/rushstack/pull/5787 | `microsoft/rushstack` | `code_and_docs` | `typescript` | [terminal] Improve TerminalTable and PrintUtilities: color options, row separators, printToTerminal() |
| https://github.com/microsoft/rushstack/pull/5786 | `microsoft/rushstack` | `code_only` | `typescript` | [lockfile-explorer] Replace update-notifier with a built-in solution |
| https://github.com/microsoft/rushstack/pull/5736 | `microsoft/rushstack` | `code_and_docs` | `typescript` | [api-extractor] Fixed empty lines for removed lines |
| https://github.com/microsoft/rushstack/pull/5779 | `microsoft/rushstack` | `code_only` | `typescript` | chore: bump decoupled local dependencies |
| https://github.com/microsoft/rushstack/pull/5784 | `microsoft/rushstack` | `code_only` | `typescript` | [rush-lib, rig-package, etc.] Dependency cleanup: remove several small third-party packages |
| https://github.com/microsoft/rushstack/pull/5781 | `microsoft/rushstack` | `code_only` | `typescript` | Bump semver to ~7.7.4; fix INpmCheckVersionBumpType for new 'release' ReleaseType |
| https://github.com/microsoft/rushstack/pull/5785 | `microsoft/rushstack` | `code_and_docs` | `typescript` | [terminal] Add TerminalTable class; [rush-lib] remove cli-table dependency |
| https://github.com/microsoft/rushstack/pull/5783 | `microsoft/rushstack` | `code_only` | `typescript` | Enable strictChangefileValidation experiment |
| https://github.com/microsoft/rushstack/pull/5780 | `microsoft/rushstack` | `code_only` | `typescript` | Replace deprecated inquirer package with @inquirer/* packages |
| https://github.com/microsoft/rushstack/pull/5778 | `microsoft/rushstack` | `code_and_docs` | `typescript` | [node-core-library] Remove lodash from production packages; add Objects.mergeWith and Objects.isRecord |
| https://github.com/microsoft/rushstack/pull/5774 | `microsoft/rushstack` | `code_only` | `typescript` | Bump @azure/identity to ~4.13.1 in rush-azure-storage-build-cache-plugin |
| https://github.com/microsoft/rushstack/pull/5777 | `microsoft/rushstack` | `code_only` | `typescript` | chore: bump decoupled local dependencies |
| https://github.com/microsoft/rushstack/pull/5703 | `microsoft/rushstack` | `code_only` | `typescript` | fix(rush): skip injected dep hash updates for devDeps |
| https://github.com/microsoft/rushstack/pull/5715 | `microsoft/rushstack` | `code_and_docs` | `typescript` | [rush] Add stricter changefile validation to ensure changefiles target extant, correct projects. |
| https://github.com/microsoft/rushstack/pull/5773 | `microsoft/rushstack` | `code_and_docs` | `typescript` | Deprecate `minimumReleaseAge` in pnpm-config.json, replace with `minimumReleaseAgeMinutes` |
| https://github.com/microsoft/rushstack/pull/5751 | `microsoft/rushstack` | `code_and_docs` | `typescript` | feat: read `trustPolicy`, `trustPolicyExclude`, and `trustPolicyIgnoreAfter` from pnpm-config.json |
| https://github.com/microsoft/rushstack/pull/5770 | `microsoft/rushstack` | `code_only` | `typescript` | [heft-web-rig] Add temp/image-typings to build clean folders |
| https://github.com/microsoft/rushstack/pull/5758 | `microsoft/rushstack` | `code_and_docs` | `typescript` | Enhance package-extractor: batch folder collection and add hoisting skip option |
| https://github.com/microsoft/rushstack/pull/5749 | `microsoft/rushstack` | `code_only` | `typescript` | rush-resolver-cache-plugin: add pnpm 10 / lockfile v9 compatibility |
| https://github.com/microsoft/rushstack/pull/5769 | `microsoft/rushstack` | `code_and_docs` | `typescript` | [heft-sass-plugin] Replace build-tests project with SassProcessor unit tests |
| https://github.com/microsoft/rushstack/pull/5768 | `microsoft/rushstack` | `code_and_docs` | `typescript` | [heft-sass-plugin] Improve README and sass.json template |
| https://github.com/microsoft/rushstack/pull/5766 | `microsoft/rushstack` | `code_only` | `typescript` | [heft-sass-plugin] Fix JS shims and `.d.ts` for `.module.scss` files with only `:global` styles |
| https://github.com/microsoft/rushstack/pull/5740 | `microsoft/rushstack` | `code_and_docs` | `typescript` | [heft-config-file] Improve README documentation |
| https://github.com/microsoft/rushstack/pull/5765 | `microsoft/rushstack` | `code_only` | `typescript` | Prepare to publish a MINOR release of Rush |
| https://github.com/microsoft/rushstack/pull/5733 | `microsoft/rushstack` | `code_only` | `typescript` | [api-documenter] Add support for @defaultValue in Markdown and Yaml documenters |
| https://github.com/microsoft/rushstack/pull/5756 | `microsoft/rushstack` | `code_only` | `typescript` | [rush] Use AsyncRecycler for autoinstaller cleanup |
| https://github.com/microsoft/rushstack/pull/5764 | `microsoft/rushstack` | `code_only` | `typescript` | chore: bump decoupled local dependencies |
| https://github.com/microsoft/rushstack/pull/5762 | `microsoft/rushstack` | `code_only` | `typescript` | [heft-sass-plugin] Add `preserveIcssExports` option |
| https://github.com/microsoft/rushstack/pull/5763 | `microsoft/rushstack` | `code_only` | `typescript` | [npm-post-publish] Update plugins autoinstaller lockfile before rush update |
| https://github.com/microsoft/rushstack/pull/5755 | `microsoft/rushstack` | `code_and_docs` | `typescript` | [heft-sass-plugin] Add doNotTrimOriginalFileExtension option |
| https://github.com/microsoft/rushstack/pull/5754 | `microsoft/rushstack` | `code_and_docs` | `typescript` | [lookup-by-path] Add toJson()/fromJson() methods |
| https://github.com/microsoft/rushstack/pull/5757 | `microsoft/rushstack` | `code_and_docs` | `typescript` | [node-core-library] Add createReadStream/createWriteStream to FileSystem |
| https://github.com/microsoft/rushstack/pull/5741 | `microsoft/rushstack` | `code_only` | `typescript` | [rush] cobuilds: yield priority to other tasks in the queue |
| https://github.com/microsoft/rushstack/pull/5747 | `microsoft/rushstack` | `code_only` | `typescript` | Refactor repeated object property access to destructuring across repo |
| https://github.com/microsoft/rushstack/pull/5738 | `microsoft/rushstack` | `code_only` | `typescript` | Bump node-forge to 1.4.0 & @types/node-forge to address CVEs |
| https://github.com/microsoft/rushstack/pull/5737 | `microsoft/rushstack` | `code_only` | `typescript` | [npm audit] Upgrade serialize-javscript to 7.0.5 to address GHSA-hxcc-f52p-wc94 |
| https://github.com/microsoft/rushstack/pull/5727 | `microsoft/rushstack` | `code_only` | `typescript` | [api-extractor] Upgrade bundled TypeScript to 5.9 |
| https://github.com/microsoft/rushstack/pull/5716 | `microsoft/rushstack` | `code_only` | `typescript` | [rush]Fix "Unknown env config" npm warnings during rush-pnpm operations |
| https://github.com/microsoft/rushstack/pull/5734 | `microsoft/rushstack` | `code_only` | `typescript` | [node-core-library] Fix LockFile API issues that caused Rush autoinstaller failures |
| https://github.com/microsoft/rushstack/pull/5728 | `microsoft/rushstack` | `code_only` | `typescript` | chore: bump playwright-local-browser-server version to 0.1.5 |
| https://github.com/microsoft/rushstack/pull/5726 | `microsoft/rushstack` | `code_only` | `typescript` | chore: bump decoupled local dependencies |
| https://github.com/microsoft/rushstack/pull/5725 | `microsoft/rushstack` | `code_only` | `typescript` | fix(post-publish): handle Rush version bump in npm-post-publish pipeline |
| https://github.com/microsoft/rushstack/pull/5724 | `microsoft/rushstack` | `code_and_docs` | `typescript` | [rush-lib] Add async APIs for disk-touching methods in PackageJsonEditor, CommonVersionsConfiguration, and VersionPolicy |
| https://github.com/microsoft/rushstack/pull/5723 | `microsoft/rushstack` | `code_only` | `typescript` | Wire up plugin for recording published versions; update autoinstaller bumping |
| https://github.com/microsoft/rushstack/pull/5720 | `microsoft/rushstack` | `code_and_docs` | `typescript` | [package-extractor]: fix issue #5719, preventing duplicate-copy conflicts across npm-packlist versions |
| https://github.com/microsoft/rushstack/pull/5722 | `microsoft/rushstack` | `code_only` | `typescript` | chore: bump decoupled local dependencies |
| https://github.com/microsoft/rushstack/pull/5701 | `microsoft/rushstack` | `code_and_docs` | `typescript` | [rush][rush-published-versions-json-plugin] Add plugin-native global commands; add published versions JSON plugin. |
| https://github.com/microsoft/rushstack/pull/5718 | `microsoft/rushstack` | `code_only` | `typescript` | Override fast-xml-parser@^5.3.3 to 5.3.5 to fix vulnerability |
| https://github.com/microsoft/rushstack/pull/5714 | `microsoft/rushstack` | `code_only` | `typescript` | chore: bump decoupled local dependencies |
| https://github.com/microsoft/rushstack/pull/5713 | `microsoft/rushstack` | `code_only` | `typescript` | Make the next release of Rush a minor bump |
| https://github.com/microsoft/rushstack/pull/5712 | `microsoft/rushstack` | `code_only` | `typescript` | Fix package name in concurrency cap change log |
| https://github.com/microsoft/rushstack/pull/5711 | `microsoft/rushstack` | `code_only` | `typescript` | [rush] Fix rush init. |
| https://github.com/microsoft/rushstack/pull/5707 | `microsoft/rushstack` | `code_only` | `typescript` | [rush] fix: wire ProblemCollector correctly into the terminal pipeline |
| https://github.com/microsoft/rushstack/pull/5708 | `microsoft/rushstack` | `code_only` | `typescript` | fix: conditionally assign `logFilePaths` only when value is not `undefined` |
| https://github.com/microsoft/rushstack/pull/5700 | `microsoft/rushstack` | `code_and_docs` | `typescript` | Add `RUSH_QUIET_MODE` environment variable equivalent to `--quiet` |
| https://github.com/microsoft/rushstack/pull/5646 | `microsoft/rushstack` | `code_only` | `typescript` | [rush-lib] Fix weighted concurrency budget being capped by operation count |
| https://github.com/microsoft/rushstack/pull/5698 | `microsoft/rushstack` | `code_only` | `typescript` | heft-storybook-plugin: add `disableTelemetry` option; always set `COREPACK_ENABLE_AUTO_PIN=0` |
| https://github.com/microsoft/rushstack/pull/5697 | `microsoft/rushstack` | `code_only` | `typescript` | [rush-lib] Add ensureFolderExists to plugin autoinstaller file writes |
| https://github.com/microsoft/rushstack/pull/5696 | `microsoft/rushstack` | `code_only` | `typescript` | chore: bump decoupled local dependencies |
| https://github.com/microsoft/rushstack/pull/5679 | `microsoft/rushstack` | `code_and_docs` | `typescript` | [rush] Support percentage-based weights for operationSettings in rush-project.json |
| https://github.com/microsoft/rushstack/pull/5689 | `microsoft/rushstack` | `code_only` | `typescript` | [CVE] Bump serialize-javascript |
| https://github.com/microsoft/rushstack/pull/5692 | `microsoft/rushstack` | `code_only` | `typescript` | chore: bump decoupled local dependencies |
| https://github.com/microsoft/rushstack/pull/5675 | `microsoft/rushstack` | `code_only` | `typescript` | chore: bump minimatch to 10.2.3 to fix vulnerability |
| https://github.com/microsoft/rushstack/pull/5629 | `microsoft/rushstack` | `code_only` | `typescript` | [rush] Fix(#5552): sort additionalFilesForOperation for hashing |
| https://github.com/microsoft/rushstack/pull/5688 | `microsoft/rushstack` | `code_only` | `typescript` | [playwright-browser-tunnel] Fix launch option for playwright tunnel  |
| https://github.com/microsoft/rushstack/pull/4655 | `microsoft/rushstack` | `code_and_docs` | `typescript` | feat: support subspace in package-extractor |
| https://github.com/microsoft/rushstack/pull/5678 | `microsoft/rushstack` | `code_only` | `typescript` | [rush-lib] Normalize plugin autoinstaller file line endings |
| https://github.com/microsoft/rushstack/pull/5668 | `microsoft/rushstack` | `code_only` | `typescript` | Update ajv to version 8.18.0 and adjust related dependencies in package.json and pnpm-lock.yaml |
| https://github.com/microsoft/rushstack/pull/5674 | `microsoft/rushstack` | `code_only` | `typescript` | chore: bump decoupled local dependencies |
| https://github.com/microsoft/rushstack/pull/5672 | `microsoft/rushstack` | `code_only` | `typescript` | Bump TSDoc and @typescript-eslint/* dependencies to address CVEs. |
| https://github.com/microsoft/rushstack/pull/5660 | `microsoft/rushstack` | `code_only` | `typescript` | chore: bump decoupled local dependencies |
| https://github.com/microsoft/rushstack/pull/5670 | `microsoft/rushstack` | `code_only` | `typescript` | Prefer to get the 'api' artifact from the triggering pipeline in the post-publish pipeline. |
| https://github.com/microsoft/rushstack/pull/5661 | `microsoft/rushstack` | `code_only` | `typescript` | Add AzDO pipeline to bump decoupled deps and update API docs after publish |
| https://github.com/microsoft/rushstack/pull/5669 | `microsoft/rushstack` | `code_and_docs` | `typescript` | [playwright-browser-tunnel] Add playwright-versioning and remove semver-coersion |
| https://github.com/microsoft/rushstack/pull/5665 | `microsoft/rushstack` | `code_and_docs` | `typescript` | [heft-typescript-plugin] Add emitModulePackageJson option for ESM output folders |
| https://github.com/microsoft/rushstack/pull/5664 | `microsoft/rushstack` | `code_and_docs` | `typescript` | [rush-azure-storage-build-cache-plugin] Add custom endpoint support via storageEndpoint |
| https://github.com/microsoft/rushstack/pull/5655 | `microsoft/rushstack` | `code_only` | `typescript` | Fix race condition in FileSystem.create*Link helpers |
| https://github.com/microsoft/rushstack/pull/5657 | `microsoft/rushstack` | `code_only` | `typescript` | [rush] Replace deprecated url.parse() with WHATWG URL API |
| https://github.com/microsoft/rushstack/pull/5659 | `microsoft/rushstack` | `code_only` | `typescript` | Add missing `exports` entries for published JSON config files |
| https://github.com/microsoft/rushstack/pull/5651 | `microsoft/rushstack` | `code_only` | `typescript` | Bump minimatch from 10.1.2 to 10.2.1 in /webpack/webpack4-localization-plugin |
| https://github.com/microsoft/rushstack/pull/5653 | `microsoft/rushstack` | `code_only_tests_or_fixtures` | `typescript` | Fix build-tests-subspace lockfile out of date after minimatch 10.1.2 → 10.2.1 bump |
| https://github.com/microsoft/rushstack/pull/5652 | `microsoft/rushstack` | `code_only` | `typescript` | Bump minimatch from 10.1.2 to 10.2.1 with changelog entries and updated lockfile |
| https://github.com/microsoft/rushstack/pull/5643 | `microsoft/rushstack` | `code_only` | `typescript` | Publish a patch release of lockfile-explorer. |
| https://github.com/microsoft/rushstack/pull/5574 | `microsoft/rushstack` | `code_only` | `typescript` | [rush] Filter npm-incompatible properties from .npmrc in utility operations |
| https://github.com/microsoft/rushstack/pull/5637 | `microsoft/rushstack` | `code_only` | `typescript` | Fix publish of package-extractor. |
| https://github.com/microsoft/rushstack/pull/5634 | `microsoft/rushstack` | `code_and_docs` | `typescript` | Include missing `.npmrc`, `LICENSE`, and `README.md` files. |
| https://github.com/microsoft/rushstack/pull/5635 | `microsoft/rushstack` | `code_only` | `typescript` | Fix publishing. |
| https://github.com/microsoft/rushstack/pull/5631 | `microsoft/rushstack` | `code_and_docs` | `typescript` | [heft-json-schema-typings-plugin]/[node-core-library] Add `x-tsdoc-release-tag` support and improve `compile()` usage |
| https://github.com/microsoft/rushstack/pull/5630 | `microsoft/rushstack` | `code_and_docs` | `typescript` | [rush] Add an option to make the Rush operation hash depend on the NodeJS version. |
| https://github.com/microsoft/rushstack/pull/5626 | `microsoft/rushstack` | `code_and_docs` | `typescript` | Rename filterAppleDoubleFiles to excludeAppleDoubleFiles |
| https://github.com/microsoft/rushstack/pull/5625 | `microsoft/rushstack` | `code_and_docs` | `typescript` | [rush] Add experiment to omit macOS AppleDouble files from build cache |
| https://github.com/microsoft/rushstack/pull/5595 | `microsoft/rushstack` | `code_and_docs` | `typescript` | Add excludeVersionOnlyChanges option to prevent version bumps and changelog updates from requiring change files |
| https://github.com/microsoft/rushstack/pull/5620 | `microsoft/rushstack` | `code_and_docs` | `typescript` | Add ECMAScript method shorthand support to webpack5-module-minifier-plugin |
| https://github.com/microsoft/rushstack/pull/5609 | `microsoft/rushstack` | `code_only` | `typescript` | [playwright-browser-tunnel] Seperate out tunnelBrowserConnection and createTunneledBrowser to remove playwright dependency from tunnelBro... |
| https://github.com/microsoft/rushstack/pull/5603 | `microsoft/rushstack` | `code_only` | `typescript` | Upgrade lodash to 4.17.23 and @types/lodash to 4.17.23 |
| https://github.com/microsoft/rushstack/pull/5567 | `microsoft/rushstack` | `code_only` | `typescript` | [npm-check-fork] Fix API docs claiming interface extends when it doesn't |
| https://github.com/microsoft/rushstack/pull/5568 | `microsoft/rushstack` | `code_only_tests_or_fixtures` | `typescript` | [npm-check-fork] Add comprehensive unit tests for NpmRegistryClient with http mocking |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4957 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | tox: remove google-genai tox environments |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4828 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | fix(redis): treat explicit db=None as database index 0 |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4973 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | Add Azure resource detector component owners |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4831 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | fix(aws-lambda): use the correct camel case when accessing the SQS message attributes |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4977 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | Update opentelemetry-resource-detector-azure version to v0.3.0 |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4976 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | [package-release/opentelemetry-resource-detector-azure/v0.2.x] Prepare release for opentelemetry-resource-detector-azure v0.2.0 |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4935 | `open-telemetry/opentelemetry-python-contrib` | `code_only_tests_or_fixtures` | `python` | opentelemetry-instrumentation-kafka-python: add regression tests for producer span error recording |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4956 | `open-telemetry/opentelemetry-python-contrib` | `code_only_tests_or_fixtures` | `python` | opentelemetry-instrumentation-logging: decouple tests from service.name resource attribute |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4952 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | ci: use shared OSSF Scorecard workflow |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4851 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | opentelemetry-instrumentation-botocore: Don't error on 3xx responses |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4897 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | feat(opamp): allow configuring agent capabilities |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4858 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | fix(kafka-python): record actual producer partition from send() future |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4686 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | docs(django): document ASGI extra |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4918 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | Deprecate google-genai and vertexai instrumentations, deprecate the genai folder |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4951 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | opentelemetry-instrumentation-mysql: support mysql-connector-python 26.7.0 and later |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4912 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | opentelemetry-instrumentation-logging: fix documented name of code attributes env var |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4930 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | fix(opamp-client): add missing requests dependency |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4841 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | Re-enable PyPy botocore test matrix |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4870 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | opentelemetry-instrumentation-grpc: respect suppressed instrumentation in server interceptors |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4838 | `open-telemetry/opentelemetry-python-contrib` | `code_only_tests_or_fixtures` | `python` | Psycopg semconv optin tests |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4835 | `open-telemetry/opentelemetry-python-contrib` | `code_only_tests_or_fixtures` | `python` | Pymysql semconv optin tests |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4833 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | opentelemetry-instrumentation-httpx: support strict typing |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4834 | `open-telemetry/opentelemetry-python-contrib` | `code_only_tests_or_fixtures` | `python` | opentelemetry-instrumentation-mysqlclient: add semconv stability opt-in test coverage |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4836 | `open-telemetry/opentelemetry-python-contrib` | `code_only_tests_or_fixtures` | `python` | Sqlite3 semconv optin tests |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4894 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | Upgrade ruff to 0.16 |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4826 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | Add DB client metrics to aiopg instrumentation |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4267 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | Support enable_commenter for instrument_connection (version 2) |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4904 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | Deprecate openai-v2 and openai-agents-v2 instrumentations |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4685 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | feat(fastapi): add checked inline type annotations |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4898 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | Deprecate gcp resource mapping function |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4873 | `open-telemetry/opentelemetry-python-contrib` | `code_only_tests_or_fixtures` | `python` | Import code attributes from stable semconv package |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4821 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | opentelemetry-instrumentation-aiopg: fix manual connection attributes |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4864 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | fix(opentelemetry-instrumentation-logging): Promote `otel.event.name` to `LogRecord.event_name` in `_translate` |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4857 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | infra(backport): add backport label to generated PRs |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4856 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | infra: validate changelog file format |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4867 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | Update opentelemetry-resourcedetector-gcp version to v1.15.0 |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4866 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | [package-release/opentelemetry-resourcedetector-gcp/v1.14.x] Prepare release for opentelemetry-resourcedetector-gcp v1.14.0 |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4865 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | Add `gcp_resource_detector` back as entry point name |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4861 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | [`opentelemetry-resourcedetector-gcp`] Fix directory structure and version number |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4852 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | Update opentelemetry-resourcedetector-gcp version to v1.14.0 |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4853 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | [package-release/opentelemetry-resourcedetector-gcp/v1.13.x] Prepare release for opentelemetry-resourcedetector-gcp v1.13.0 |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4846 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | Add release for GCP resource detector |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4839 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | opentelemetry-instrumentation-kafka-python: drop support for kafka-python-ng |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4786 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | feat: Update kafka python instrumentation to support kafka-python>=3 |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4592 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | fix(pymssql): Complete semconv stability migration for attributes set in wrapped_connection |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4728 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | fix(redis): build ClusterPipeline span metadata from _execution_strategy in redis-py 6+ |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4810 | `open-telemetry/opentelemetry-python-contrib` | `code_only_tests_or_fixtures` | `python` | opentelemetry-instrumentation-mysql: add semconv stability opt-in test coverage |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4812 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | Update opentelemetry-opamp-client version to v0.4b0 |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4813 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | [package-release/opentelemetry-opamp-client/v0.3bx] Prepare release for opentelemetry-opamp-client v0.3b0 |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4820 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | opentelemetry-instrumentation-aiopg: semantic convention stability migration |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4730 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | Feature/httpx2 instrumentor |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4668 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | opentelemetry-instrumentation-aws-lambda: add SQS context propagation support |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4741 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | Fix duplicate Pyramid traversal subscribers |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4749 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | Migrate GCP resource detector (`opentelemetry-resourcedetector-gcp`) to contrib |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4429 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | fix(grpc): handle NotImplementedError from add_done_callback in aio client |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4784 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | Update otelbot token workflows to use client IDs |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4814 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | `opentelemetry-util-genai`, `instrumentation-genai/*`: ignore now deprecated genai enums |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4768 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | opentelemetry-instrumentation-aiohttp-server: fix span name and http.route attribute according to semconv |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4772 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | opentelemetry-instrumentation-pymongo: semantic convention stability migration |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4746 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | opentelemetry-instrumentation-boto3sqs: avoid KeyError when all messages in send_message_batch fail |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4537 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | celery: allow using links instead of child spans for task execution |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4764 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | fix(logging): export formatter-added attributes |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4781 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | fix(dbapi): add missing instrumentation enabled check |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4782 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | fix(instr-redis): don't fail commands when connection pool lacks `connection_kwargs` |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4751 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | openai-v2: await AsyncStream.close on default async streaming path |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4740 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | opentelemetry-instrumentation-pika: prevent duplicate consumer spans |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4739 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | opentelemetry-instrumentation-pymemcache: add semconv stability migration support |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4747 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | opentelemetry-instrumentation-cassandra: implement semconv stability opt-in |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4718 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | opentelemetry-instrumentation-urllib3: remove multiple calls to sanitize_method |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4763 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | Prepare a bunch of genai packages for towncrier |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/3174 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | click: ignore click based servers |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4734 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | opentelemetry-util-http: QUERY is a known method in sanitize_method |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4759 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | Drop elasticsearch instrumentation |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4733 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | opentelemetry-instrumentation-asyncpg: semantic convention stability migration |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4731 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | opentelemetry-instrumentation-tortoiseorm: add semconv stability migration support |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4735 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | opentelemetry-instrumentation-tornado: sanitize the http method |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4626 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | opentelemetry-instrumentation-logging: add optional `inject_trace_context` argument for injecting trace context attributes |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4719 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | opentelemetry-instrumentation-requests: remove multiple calls to sanitize_method |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4697 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | opentelemetry-instrumentation-dbapi: implement proper handling of t-string queries |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4503 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | New package: unhandled Exceptions logging instrumentation |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4700 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | fastapi: fix AttributeError on partially matched routes with FastAPI 0.137 included routers |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4696 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | opentelemetry-instrumentation-redis: gracefully handle hook exceptions |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4657 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | docs(dbapi): fix pyodbc connect method example |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4709 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | opentelemetry-instrumentation-vertexai: remove unnecessary type ignore comments |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4601 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | opentelemetry-instrumentation-botocore: loosen aiobotocore version constraints to allow for 3.x |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/1414 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | Add support for regular expression matching and sanitizing of headers in Pyramid. |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/1413 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | Add support for regular expression matching and sanitizing of headers in Flask. |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/1359 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | Update prom rw exporter |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/2323 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | Remove [test] package from exporter-prometheus-remote-write |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/252 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | Add readTheDocs |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/250 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | Commit benchmark results to gh-pages branch |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4433 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | fix(flask): wrap wsgi_app call in try/except to prevent active_requests gauge leak |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4594 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | fix: declare opentelemetry-semantic-conventions for aio-pika, logging, pika and system-metrics |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/1304 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | Update package metadata opentelemetry-distro |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/1269 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | Update package metadata opentelemetry-instrumentation-boto |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/29 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | Add eachdist and move tox to root folder |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/26 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | adding instructions to port instrumentation |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/1412 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | Add support for regular expression matching and sanitizing of headers in Falcon. |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/1310 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | Update package metadata _template |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/1308 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | Update package metadata opentelemetry-sdk-extension-aws |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/1307 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | Update package metadata opentelemetry-propagator-ot-trace |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/1773 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | Add otelTraceSampled to instrumetation-logging |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/1778 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | Expand sqlalchemy pool.name to follow the semantic conventions |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/1806 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | Skip requests tests for pypy3 |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/1584 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | Resource detector for container properties |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4666 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | tornado: reduce cardinality with old semconv metrics attributes |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4689 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | opentelemetry-instrumentation-langchain: fix typecheck error |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4665 | `open-telemetry/opentelemetry-python-contrib` | `code_only_tests_or_fixtures` | `python` | tornado: make metrics tests less flaky on pypy |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4646 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | Fix broken botocore tests, minor change to HTTPX instrumentation test, remove `_ExtendedAttributes` import from logging instrumentation |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4613 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | docs: fix malformed RST formatting in kafka instrumentation docstrings |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4618 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | fix(infra): Backport of patch release changelog to main |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4620 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | fix failing tests for docs and py312-asgi |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4414 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | fix(sdk-extension-aws): replace deprecated aws-auth ConfigMap check with JWT iss claim detection in AwsEksResourceDetector |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4529 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | fix(asyncpg): instrument prepared statements |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4367 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | Remove duplicate query logging that breaks Django's assertNumQueries |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4598 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | [package-release/opentelemetry-instrumentation-google-genai/v0.7bx] Prepare patch release for opentelemetry-instrumentation-google-genai ... |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4597 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | backport(google-genai): loosen instrumented version restriction |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4596 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | ci: Enable GitHub Merge Queue support |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4112 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | opentelemetry-instrumentation-logging: don't add out of spec attributes by default |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4590 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | fix(confluent-kafka): declare opentelemetry-semantic-conventions as a direct dependency |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4586 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | ci: validate changelog fragment filenames |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4551 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | Fix wsgi invalid request uri |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4563 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | fix(pika): pass destination instead of task_name to _enrich_span |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4536 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | opamp-client: support text effective config bodies |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4577 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | opentelemetry-instrumentation-tornado: reduce cardinality of span names and metrics attributes |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4448 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | fix(pyramid): add missing http.response.status_code in duration metrics |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4583 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | Move from httpretty to mocket as http mocking library |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4481 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | opentelemetry-instrumentation-dbapi: Add Database client operation duration and returned rows metrics |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4469 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | feat: update auto-instrumentation to re-inject instrumentation path after init |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4585 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | opentelemetry-util-genai: fix typecheck after importlib metadata shim changes |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4505 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | fix(celery): type getter and harden utility helpers |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4216 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | opentelemetry-instrumentation-aws-lambda: fix improper handling of header casing |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4493 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | Add reasoning tokens attribute to span / log when new sem conv is set |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4504 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | fix(celery): clear task timing state after postrun |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4576 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | fix: changelog workflow |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4500 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | genai-util: refactor streams to a generic ABC wrapper. |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4109 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | DB semantic convention stability migration for DB-API and 7 inheriting db client instrumentors |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4370 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | DB and HTTP semantic convention stability migration for Redis instrumentation |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4569 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | gen-ai: Specify oldest version of genai util for tests |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4565 | `open-telemetry/opentelemetry-python-contrib` | `code_only_tests_or_fixtures` | `python` | requirements: bump requests to 2.33.1 |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4438 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | fix(instrumentation): add OTEL_SEMCONV_STABILITY_OPT_IN to CLI args |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4423 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | fix(confluent-kafka): populate bootstrap.servers span attributes |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4499 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | gen-ai instrumentation(feat): anthropic messages stream method instrumentation |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4560 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | opentelemetry-instrumentation-mysqlclient: update unit tests to properly validate trace context trace flags values |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4478 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | docker-tests: use docker from the system |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4372 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | Always use `LogRecord.getMessage` to get the log body |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4368 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | fix #4251: wrap BackgroundTasks in their own span |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4030 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | feat: update xray trace id generator for 'random-trace-id' flags changes |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4556 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | Small changes and cleanup to GenAi Utils package to enable google's GenAi instrumentation to use it |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4553 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | refactor(genai-util): pass sampling attributes at span creation for rest of invocation types |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4554 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | openai: pass tool definitions to genai utils |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4550 | `open-telemetry/opentelemetry-python-contrib` | `code_only_tests_or_fixtures` | `python` | Fix flaky tornado test by increasing delta tolerance to 0.02 |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4397 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | Add support for process.disk.io metric in system-metrics instrumentation |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4361 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | fix(celery): coerce timelimit values to strings in span attributes |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4298 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | Add log handler configuration to autoinstrumentation |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4288 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | (Redo) Add experimental Labeler to store custom attributes in OTel Context |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4371 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | feat: Add BaggageLogProcessor to opentelemetry-processor-baggage |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/3839 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | refactor: remove redundant pylint disable from celery instrumentation |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/3761 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | AWS X-Ray Remote Sampler Part 2 - Add Rules Caching, Rules Matching Logic, Rate Limiter, and Sampling Targets Poller |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/3898 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | opentelemetry-exporter-richconsole: add option to suppress resource information |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4538 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | refactor(genai-util): pass sampling attributes at span creation time |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4380 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | ci: add GHA to add PRs to project board when marked ready for review |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4522 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | ci: only check new links on pull requests to avoid rate limiting |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4531 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | fix(precommit): ignore autodoc_entry.rst in rstcheck |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4525 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | Update opentelemetry-instrumentation-openai-v2 version to v2.5b0 |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4526 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | [package-release/opentelemetry-instrumentation-openai-v2/v2.4bx] Prepare release for opentelemetry-instrumentation-openai-v2 v2.4b0 |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4517 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | Update opentelemetry-util-genai version to v0.5b0 |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4516 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | [package-release/opentelemetry-util-genai/v0.4bx] Prepare release for opentelemetry-util-genai v0.4b0 |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4523 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | Back-porting recent commits to release/opentelemetry util genai/v0.4bx |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4520 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | anthropic and claude-agent-sdk: bump opentelemetry-util-genai |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4513 | `open-telemetry/opentelemetry-python-contrib` | `code_only` | `python` | Add PR labeler workflow for genai label |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4506 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | GenAI utils: make completion hook safe to call |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4315 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | OpenAI v2: completion hook support and minor fixes |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4494 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | openai-v2: default empty string for GEN_AI_REQUEST_MODEL on missing model |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4502 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | openai-v2: migrate _v_new path from LLMInvocation to InferenceInvocation |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4501 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | openai-v2: use genai-utils histogram factories for metrics |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4395 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | Enabled flake8-tidy-imports for ruff linter |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4274 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | Genai utils \| Add AgentInvocation type |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4486 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | Add __iter__ method to TracedCursorProxy (#4427) |
| https://github.com/open-telemetry/opentelemetry-python-contrib/pull/4485 | `open-telemetry/opentelemetry-python-contrib` | `code_and_docs` | `python` | fix(pika): use ObjectProxy for ReadyMessagesDequeProxy to restore iterability with wrapt 2.x (#4461) |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22443 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Fix UnexpectedDbghelpdllExpected0Actual1 string formatting in PublishSymbolsV2 |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22431 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Fix ArchiveFilesV2 file name option injection |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22441 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Fix flaky macOS L0 test timeouts in AzureRmWebAppDeploymentV3 |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22440 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Generate signed task binaries for WDAC validation \| Set 1 |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22416 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Kudu-scoped tokens: App Service-audience token + KuduAuthMode telemetry across App Service tasks (ADO 2401907) |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22439 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | pin github actions to specific commit |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22409 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Sanitization arguments |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22427 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Rename the package files for the deprecated DownloadPackageV0 task |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22434 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Remove SfSafeParser feature flag |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22433 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Nadiabugarin users/nadiab/update nugetauthenticate cr |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22430 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | update task-lib for the CmdLineV2 task |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22417 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Bump package versions to address security vulnerabilities in BicepDeployV0 task |
| https://github.com/microsoft/azure-pipelines-tasks/pull/21650 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Users/davidmiri/fix docker buildkit warnings 17893 |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22414 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Fix MavenV4 Token Leak (MSRC 129543) |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22418 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Igortsoi/msrc 129544 |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22419 | `microsoft/azure-pipelines-tasks` | `code_and_docs` | `typescript` | Remove external sprint dependency and update CI networking |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22403 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Add task binary signing: sign scripts & third-party files, preserve embedded MS signatures |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22413 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Avoid PowerShell Gallery repository probe in CI |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22407 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Reduce duplicate Courtesy Push malware scanning |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22412 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Update picomatch to 2.3.2 in PowerShellV2 and CmdLineV2 |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22410 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Add agent version field to issue forms |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22401 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Remediate transitive dependency CVEs across multiple pipeline tasks |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22406 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | [BicepDeployV0] Fix designer dropdowns, multi-agent login race, drop preview flag |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22395 | `microsoft/azure-pipelines-tasks` | `code_and_docs` | `typescript` | fix: isolate SQL token from shared ARM credential + sovereign cloud audience |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22372 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | SqlDacpacDeploymentOnMachineGroupV0: preserve original sqlQuery failures instead of masking with format-spec errors |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22392 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | [DownloadGitHubReleaseV0] Sanitize release name to prevent ##vso logging-command injection |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22398 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | update form-data package in the JavaToolInstaller Tasks |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22394 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Revert "fix: address nemanjarogic review comments on PR #22379" |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22385 | `microsoft/azure-pipelines-tasks` | `code_and_docs` | `typescript` | feat: sqlcmd execution for .sql files + telemetry (task4_final) |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22388 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Validate publish profile values to prevent command injection in AzureRmWebAppDeployment V4/V5 |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22389 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Use fixed Azure ARM REST package in app deploy tasks |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22379 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | feat: Add SQL project build support (task3b) |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22384 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | [AzureContainerAppsV0][AzureContainerAppsV1] Harden appSourcePath handling to prevent command injection |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22351 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | [AzureAppConfiguration] Fix agent base package version mismatch |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22376 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | feat: Add connection string parsing, firewall management, and SQL project build (task3) |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22380 | `microsoft/azure-pipelines-tasks` | `code_and_docs` | `typescript` | Add external dependency support to task minifier |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22374 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | feat: Add SqlPackage and sqlcmd discovery (task2) |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22364 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | feat: Add MicrosoftSqlDeploymentV1 task infrastructure (task1) |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22319 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Update .NET SDK version to v10 |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22368 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Fix PackerBuildV1 credential Leak |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22369 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | [SshV0] add  enableVsoCommands  input to control remote VSO command execution (default off) |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22365 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Upgrading the Vstest task after amr64 changes |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22370 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | AzureFunctionAppV2: correct help link to V2 task documentation |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22357 | `microsoft/azure-pipelines-tasks` | `code_and_docs` | `typescript` | Add opt-in minified (bundled) build option for Node tasks |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22367 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Upgrade azure-pipelines-task-lib to version 5.277.0 across regressed tasks |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22363 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | GitHubReleaseV1: Skip Discussion NOT_FOUNDs during changelog issue resolution |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22324 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | [AzureContainerAppsV1] Use array-based execSync to block arg injection |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22360 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Fix SqlAzureDacpacDeployment: unique GUID filenames for Extract/Export to prevent file collision and data loss |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22358 | `microsoft/azure-pipelines-tasks` | `code_and_docs` | `typescript` | Top up Copilot nomination pool to N outstanding candidates (POC) |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22350 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Fix HelmDeploy@1 uninstall command ignoring `arguments` input |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22346 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | VsTestV3: update TestAgent.zip with changes for coverage file upload limit increase from 75MB to 100MB |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22348 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Use internal Microsoft package feed proxy for triage-report npm deps |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22347 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Enable weekly schedule for Triage report - Release/RM workflow |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22344 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Add .NET 10.0 runtime stack option to AzureWebAppV1 task |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22343 | `microsoft/azure-pipelines-tasks` | `code_and_docs` | `typescript` | Split Copilot Issue Triage into nominate + approved-processing workflows (POC) |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22340 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Fix triage-report workflow: install deps from public npm registry (E401 on ADO feed) |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22313 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Fix Key not found error in Tasks |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22335 | `microsoft/azure-pipelines-tasks` | `code_and_docs` | `typescript` | Add reusable, per-team-customizable issue triage report workflow |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22336 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Remove task signing and disable CI |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22330 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Improve stale workflow: author-blocked fast-track, ArtifactsPackages scope fix, bump to stale@v10 |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22331 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Remove assign rules from issue-rules.yml (owner assignment now handled by assignOwners.yml) |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22327 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Resolve issue Task: labels from real Tasks/ folders (drop hardcoded values) |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22328 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Stop logging token |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22323 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Auto-assign issues to the affected task's code owner (from CODEOWNERS) |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22322 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Fix issue labeler for YAML issue forms and decouple file-bugs from the private npm feed |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22325 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Update dependencies and bump version for AzureVmssDeployment and JenkinsDownloadArtifacts tasks |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22326 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | AzureCLIV3: emit telemetry for azure-devops extension install outcome |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22321 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Dependency update and version bump in AzurePowerShellV4 and AzurePowerShellV5 Tasks |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22318 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | fixing build |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22314 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Dependency update and version bump in KubernetesV1 Task |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22309 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Remediate minimatch dependency vulnerabilities across impacted tasks |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22287 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Use New-PSSession splatting instead of Invoke-Expression in RemoteDeployer SessionHelper |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22250 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Fix AzurePowerShell V5 cleanup failures overriding task result |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22293 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Bump common package dependencies for pipeline tasks |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22296 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Update VstsAzureRestHelpers to update Azure SQL API version |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22303 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Dependency update and version bump in JenkinsDownloadArtifactsV1 Task |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22301 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | add PowerShellOnTargetMachinesV1 to make-options to allow builds |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22297 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Fix SshV0 ##vso logging-command injection via remote output |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22259 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | [AzureContainerAppsV1,V0] Log Docker out of ACR after task completes |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22295 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | PublishCodeCoverageResultsV1: dependency refresh and version bump |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22288 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | AzureIoTEdgeV2: harden docker login and command invocation |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22286 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Sanitize NewPsSessionOptionArguments / new-service inputs in PowerShellOnTargetMachinesV3 and AzureCloudPowerShellDeploymentV1 |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22294 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Update task dependencies and bump task versions to 277.0 |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22275 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Update dependencies and increment patch versions |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22289 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | AzureIoTEdgeV2: add Node24 handler and migrate to Node 24 |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22260 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | KubernetesV1: Sanitize kubectl version output to prevent ##vso[ comma… |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22277 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Update NuGetInstaller task to version 276 and bump dependencies for security improvements |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22281 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Update azure-pipelines-tasks-docker-common to 2.276.0 (security fix) |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22284 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Bump form-data dependency to version 4.0.6 in PublishTestResultsV1 ,PublishTestResultsV2 and VsTestPlatformToolInstallerV1 |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22274 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Patch vulnerable dependencies in MavenV2/V3/V4 Tasks and CI utilities |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22278 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Bump azure-pipelines-task-lib and form-data versions in AzureSpringCloudV0 Task |
| https://github.com/microsoft/azure-pipelines-tasks/pull/21378 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Handle dotnet publish logging the same way as dotnet build. |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22261 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | AppCenterDistributeV3: remediate package vulnerabilities with minimal dependency update |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22272 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Update packages to eliminate security issues in Common/coveragepublisher |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22266 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Fix AzurePowerShell token leak and temp file cleanup |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22267 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Fix credential leak in ContainerBuild@0: add connection.close() after build/push |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22246 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Bump package versions to address security vulnerabilities in CopyFilesV2 Task |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22262 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Bump package versions to address security vulnerabilities in DownloadGitHubNugetPackageV1 Task  |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22257 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | AzureCLIV3: surface warnings on azure-devops extension install fallback and add L0 coverage |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22252 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Vulnerability fix for GradleAuthenticateV0 task |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22199 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | DockerV1: skip redundant tag and bump task version |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22249 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Update PowerShell argument sanitizer to allow special characters |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22247 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Update make-options.json to include PowerShellOnTargetMachinesV2 |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22241 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Allowing downloads from Nuget.org |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22239 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Adding continueOnError to teams notification step |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22238 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Updated Network Policy |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22231 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Remove skipping of Node Download if node version is already present |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22217 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Update serialize-javascript package to fix vulnerability |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22227 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Bump azure-pipelines-task-lib to ^5.2.10 for 8 Kubernetes tasks |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22219 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Bump azure-pipelines-task-lib to ^5.2.10 for AzureKeyVaultV2, AzurePowerShellV4, AzurePowerShellV5 |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22209 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Update packages to eliminate security issues |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22215 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Enable fast build option by default for local development |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22208 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Update dependencies to patch security flaws |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22213 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Bump package versions to address security vulnerabilities in AzureSpringCloudV0 |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22210 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Bump artifact-engine to ^2.275.2 for DownloadBuildArtifactsV0 |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22181 | `microsoft/azure-pipelines-tasks` | `code_and_docs` | `typescript` | Enhance argument validation for PowerShell and Bash scripts in AzureCLI |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22139 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Fix vulnerabilities with dependency upgrades |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22197 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Bump dependencies to remediate vulnerabilities |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22104 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Fixing removal of unused node components |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22192 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Update NuGetCommandV2 Timeout Option |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22198 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Updated packages to eliminate security issues |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22183 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Add AzureFunctionV2 to localization pipeline |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22177 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Updated Docker tasks to docker-common 2.274.0 after EnableDockerReservedNameCheck removal |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22125 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Add L0 tests for AzureFunctionAppV1 and AzureFunctionAppV2 |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22060 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Fix `checkForExistingVersion` ignoring installed SDKs with `useGlobalJson` + `rollForward` |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22175 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Update Task AzureTestPlanV0 & PublishTestResultsV1 versions to align with repository versioning scheme |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22174 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Fix macOS-only L0 timeouts in LateBoundIdToken tests |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22160 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | AzureCLIV3: Add PIP_NO_DEPS fallback for azure-devops extension installation |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22168 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Fix symlink regression: bump webdeployment-common to ^4.274.1 in AzureFunctionAppV1 and V2 |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22164 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | JenkinsDownloadArtifactsV2: include Node 24 in extract-zip path (AB#2392160) |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22158 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Import missing helper functions used in V2 commands |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22155 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Update TestAgent.zip blob URL to build 31482278 (VsTestV3 only) |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22001 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Fix findGlobalJsonFile boundary check for custom checkout paths (#21989) |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22152 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Add timeout option to nuget command task |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22147 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Add Azure DevOps service connection (WorkloadIdentityUser) support to InvokeRestAPI@1 |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22129 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Updated required version to fix vulnerabilities in AzureIoTEdgeV2 task |
| https://github.com/microsoft/azure-pipelines-tasks/pull/21920 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Add parameter array to prevent command injection |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22138 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Fix indent ping-pong: bump-versions.js writes 2-space JSON |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22136 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | update axios package dependency to fix vulnerabilities |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22115 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Updated required version to fix vulnerabilities in AzureSpringCloudV0 |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22120 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Update node24 publishsymbolsv2 task changes as suggested  |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22127 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Localize: bump tasks with _generated/ mirror by +2 to avoid BuildConfigGen version collision |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22096 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Fix CVE-2026-41672: Update @xmldom/xmldom 0.8.12 to 0.8.13 (CG Alert 433157) |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22098 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Fix CVE-2026-41672: Upgrade webdeployment-common to 4.274.0 in AzureMysqlDeploymentV2 |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22094 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Bump azure-pipelines-tasks-webdeployment-common to version 4.274.0 an… |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22107 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Add tests for issueregex in GithubReleaseV1 |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22103 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Revert "Utility function to remove unused node_modules and components from downloaded node zip binary" |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22085 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | ReTake: update packages to fix vulnerabilities |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22057 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Utility function to remove unused node_modules and components from downloaded node zip binary |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22087 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Updated basic-ftp package to fix vulnerability in AppCenterDistributeV3 task |
| https://github.com/microsoft/azure-pipelines-tasks/pull/21985 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Update docker-common package in AzureTestPlanV0 and ContainerStructureTestV0 tasks |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22088 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Deprecating the ContainerStructureTest task |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22043 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Enhancement: Add support for configurable Node.js binary mirror sources |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22091 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Add AzureMysqlDeploymentV2 to make-options.json |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22073 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Fix GitHubReleaseV1 issueid regex to avoid referencing incorrect issues |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22031 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Remove AppCenterTestV1, AppCenterDistributeV1, AppCenterDistributeV2 task from the repository |
| https://github.com/microsoft/azure-pipelines-tasks/pull/21848 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Update docker-common package in AzureIoTEdgeV2 task |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22082 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | fix bump version in Loc |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22080 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Localize/bump-versions.js: rebuild affected _generated/ tasks via make.js build to keep en-US resjson and versionmaps in sync |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22079 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Revert "Auto-regenerate _generated/ in Localize/bump-versions.js" |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22077 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Auto-regenerate _generated/ in Localize/bump-versions.js |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22076 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Revert "update package dependencies to latest versions to fix vulnerabilities" |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22064 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Update codecoverage-tools package in MavenV4 to fix JaCoCo Java 25 incompatibility |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22061 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | update package dependencies to latest versions to fix vulnerabilities |
| https://github.com/microsoft/azure-pipelines-tasks/pull/21984 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Fix axios supply chain vulnerability in CI scripts |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22042 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | BicepDeployV0: defer tl.loc() until after setResourcePath |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22032 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Fix Invoke‑Expression usage in ServiceTypeHealthPolicyMap and add tests |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22015 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Fix CG alert 413698: Update artifact-engine to 2.273.0 in DownloadFileshareArtifactsV1 |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22002 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | ## Fix CG Alert 353384: Update `qs` dependency in AzureStaticWebAppV0 |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22029 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Bump task versions for tasks using signed 7zip binaries |
| https://github.com/microsoft/azure-pipelines-tasks/pull/21712 | `microsoft/azure-pipelines-tasks` | `code_and_docs` | `typescript` | Update GoTool task documentation to clarify download URL options and … |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22026 | `microsoft/azure-pipelines-tasks` | `code_and_docs` | `typescript` | BicepDeployV0: Update to latest bicep-deploy-common package and update README issue |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22023 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Add feature flag for wheel fallback in AzureCLIV3 |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22013 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | UseDotNetV2: fix silent logging and add rollForward resolution output |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22020 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Fix localization pipeline merge conflict caused by npm install |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22018 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | updated axios package version to address vulnerability |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22019 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Fixed. Moved npm install from before the git sync step to the bump-vesions step that actually needs it. |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22017 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Bump basic-ftp to version 5.3.0 in FtpUploadV2 task for vulnerability fixes |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22005 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Fix vstest version parsing to handle non-numeric version strings |
| https://github.com/microsoft/azure-pipelines-tasks/pull/22010 | `microsoft/azure-pipelines-tasks` | `code_only` | `typescript` | Add support for installing the Azure DevOps CLI extension from a wheel file in the AzureCLIV3 task |
| https://github.com/apache/superset/pull/43524 | `apache/superset` | `code_and_docs` | `python` | feat(websocket): support JWT secret rotation |
| https://github.com/apache/superset/pull/42309 | `apache/superset` | `code_and_docs` | `python` | feat(maps): Add Italy regions and autonomous provinces country map |
| https://github.com/apache/superset/pull/43131 | `apache/superset` | `code_only` | `python` | fix(mcp): defer unknown numeric types to compile |
| https://github.com/apache/superset/pull/43130 | `apache/superset` | `code_only` | `python` | fix(mcp): accept common chart input variants |
| https://github.com/apache/superset/pull/42898 | `apache/superset` | `code_only` | `python` | fix(dashboard): preserve native filter keys for dataset-less filters on save |
| https://github.com/apache/superset/pull/42411 | `apache/superset` | `code_only` | `python` | chore(database): remove dead extra validation exception classes |
| https://github.com/apache/superset/pull/43521 | `apache/superset` | `code_only` | `python` | chore(deps): restore permissive marshmallow lower bound (>=3.0, <5) |
| https://github.com/apache/superset/pull/43493 | `apache/superset` | `code_and_docs` | `python` | docs(versioning): fix post-flip doc and comment drift |
| https://github.com/apache/superset/pull/39506 | `apache/superset` | `code_only` | `python` | fix(explore): skip re-fetch when navigating away from /explore |
| https://github.com/apache/superset/pull/43485 | `apache/superset` | `code_and_docs` | `python` | feat(deletion-retention): persist purge block reason codes on the audit log |
| https://github.com/apache/superset/pull/43516 | `apache/superset` | `code_and_docs` | `python` | feat(websocket): gate realtime notifications by permission |
| https://github.com/apache/superset/pull/43495 | `apache/superset` | `code_only` | `python` | chore(ci): drop inert SQLALCHEMY_WARN_20 flag from unit-test CI |
| https://github.com/apache/superset/pull/43439 | `apache/superset` | `code_only` | `python` | fix(number-format): preserve custom smart formatter id |
| https://github.com/apache/superset/pull/43421 | `apache/superset` | `code_only` | `python` | fix(table): keep each metric's own aggregate in the summary row by default |
| https://github.com/apache/superset/pull/36856 | `apache/superset` | `code_only` | `python` | feat(snowflake): Add support for OAuth 2.0 authentication |
| https://github.com/apache/superset/pull/43507 | `apache/superset` | `code_only` | `python` | chore(deps-dev): bump the storybook group across 1 directory with 5 updates |
| https://github.com/apache/superset/pull/43509 | `apache/superset` | `code_only` | `python` | chore(deps): bump antd from 6.6.0 to 6.6.1 in /superset-frontend |
| https://github.com/apache/superset/pull/43508 | `apache/superset` | `code_only` | `python` | chore(deps-dev): bump baseline-browser-mapping from 2.11.14 to 2.11.15 in /superset-frontend |
| https://github.com/apache/superset/pull/43510 | `apache/superset` | `code_only` | `python` | chore(deps): bump dayjs from 1.11.22 to 1.11.23 in /superset-frontend |
| https://github.com/apache/superset/pull/43511 | `apache/superset` | `code_only` | `python` | chore(deps): bump dompurify from 3.4.12 to 3.4.13 in /superset-frontend |
| https://github.com/apache/superset/pull/43497 | `apache/superset` | `code_only` | `python` | chore: remove obsolete pandas/SQLAlchemy version compat shim |
| https://github.com/apache/superset/pull/42479 | `apache/superset` | `code_only` | `python` | fix(sqllab): allow SQL Lab query owners to create charts without all_datasource_access |
| https://github.com/apache/superset/pull/43469 | `apache/superset` | `code_only` | `python` | fix(soft-delete): card-view chart delete shows the archive dialog |
| https://github.com/apache/superset/pull/43465 | `apache/superset` | `code_and_docs` | `python` | fix(archived-list): use the semantic-layers-aware label for the dataset type |
| https://github.com/apache/superset/pull/43446 | `apache/superset` | `code_only` | `python` | chore(deps-dev): bump @swc/core from 1.15.47 to 1.16.0 in /superset-frontend |
| https://github.com/apache/superset/pull/43492 | `apache/superset` | `code_only` | `python` | fix(gtf): wait for the task lock instead of failing concurrent submits |
| https://github.com/apache/superset/pull/43401 | `apache/superset` | `code_only` | `python` | fix(soft-delete): name the recovery location in the archive confirmation |
| https://github.com/apache/superset/pull/43486 | `apache/superset` | `code_only` | `python` | fix(gtf): stop async poll when idle + back off; second-granularity durations |
| https://github.com/apache/superset/pull/43350 | `apache/superset` | `code_only` | `python` | fix(versioning): suppress automatic chart normalization changes |
| https://github.com/apache/superset/pull/43419 | `apache/superset` | `code_only` | `python` | chore(deps-dev): update clickhouse-connect requirement from <2.0,>=1.6.0 to >=1.7.1,<2.0 |
| https://github.com/apache/superset/pull/43440 | `apache/superset` | `code_only` | `python` | chore(deps): bump the rjsf group in /superset-frontend with 3 updates |
| https://github.com/apache/superset/pull/43196 | `apache/superset` | `code_only` | `python` | fix(roles): let the permissions dropdown size to its content |
| https://github.com/apache/superset/pull/43266 | `apache/superset` | `code_only` | `python` | fix(ci): restore scheduled CI checks |
| https://github.com/apache/superset/pull/43473 | `apache/superset` | `code_only` | `python` | fix(gtf): async chart-data robustness + accurate DB errors; retire async_events |
| https://github.com/apache/superset/pull/43388 | `apache/superset` | `code_and_docs` | `python` | fix(mcp): tighten auth and request validation edge cases |
| https://github.com/apache/superset/pull/43306 | `apache/superset` | `code_only` | `python` | fix(frontend): ignore stale list responses |
| https://github.com/apache/superset/pull/43353 | `apache/superset` | `code_only` | `python` | fix(query-object): reject malformed ad-hoc metrics |
| https://github.com/apache/superset/pull/43355 | `apache/superset` | `code_only` | `python` | fix(gsheets): correctly format Date-column filter literals |
| https://github.com/apache/superset/pull/43404 | `apache/superset` | `code_only` | `python` | fix(explore): honor column Label in filter search and pill |
| https://github.com/apache/superset/pull/43173 | `apache/superset` | `code_only` | `python` | fix(dataset): correct Hours Offset filter bounds and grain-truncation order |
| https://github.com/apache/superset/pull/43146 | `apache/superset` | `code_only` | `python` | fix(explore): clear stale custom time-shift date error |
| https://github.com/apache/superset/pull/43139 | `apache/superset` | `code_only` | `python` | fix(plugin-chart-table): guard row-indexed comparison-color lookups against undefined entries |
| https://github.com/apache/superset/pull/42821 | `apache/superset` | `code_only` | `python` | fix(mysql): resolve wire-protocol column types and mutate rows from immutable results |
| https://github.com/apache/superset/pull/42392 | `apache/superset` | `code_only` | `python` | fix(plugin/chart/parallel-coordinate): prevent frontend crash with empty/undefined metrics when moving between pages quickly |
| https://github.com/apache/superset/pull/41437 | `apache/superset` | `code_only` | `python` | test(dashboard): migrate drill-to-detail E2E from Cypress to Playwright |
| https://github.com/apache/superset/pull/43177 | `apache/superset` | `code_only` | `python` | fix(datasets): keep a metric's warning text when editing from Explore |
| https://github.com/apache/superset/pull/43411 | `apache/superset` | `code_only` | `python` | chore(deps-dev): bump gevent from 26.7.0 to 26.8.0 |
| https://github.com/apache/superset/pull/43412 | `apache/superset` | `code_only` | `python` | chore(deps-dev): bump prophet from 1.3.0 to 1.4.0 |
| https://github.com/apache/superset/pull/43414 | `apache/superset` | `code_only` | `python` | chore(deps): bump pyarrow from 25.0.0 to 25.0.1 |
| https://github.com/apache/superset/pull/43415 | `apache/superset` | `code_only` | `python` | chore(deps): bump sqlalchemy from 2.0.51 to 2.0.52 |
| https://github.com/apache/superset/pull/43416 | `apache/superset` | `code_only` | `python` | chore(deps-dev): update teradatasql requirement from >=20.0.0.64 to >=20.0.0.65 |
| https://github.com/apache/superset/pull/43417 | `apache/superset` | `code_only` | `python` | chore(deps): bump marshmallow from 4.3.0 to 4.3.1 |
| https://github.com/apache/superset/pull/43418 | `apache/superset` | `code_only` | `python` | chore(deps): bump sqlglot from 30.16.0 to 30.17.0 |
| https://github.com/apache/superset/pull/43466 | `apache/superset` | `code_only` | `python` | fix(tags): fix broken import in daos/tag.py |
| https://github.com/apache/superset/pull/43390 | `apache/superset` | `code_only` | `python` | fix: add missing ownership checks to tag, report-log, and dataset-schema endpoints |
| https://github.com/apache/superset/pull/43384 | `apache/superset` | `code_only` | `python` | fix(plugin-chart-echarts): apply contribution before rename with time comparison |
| https://github.com/apache/superset/pull/43463 | `apache/superset` | `code_only` | `python` | feat(gaq): minimum result-cache TTL for async chart-data queries |
| https://github.com/apache/superset/pull/43462 | `apache/superset` | `code_only` | `python` | fix(distributed-lock): ownership-checked release (compare-and-delete) |
| https://github.com/apache/superset/pull/43389 | `apache/superset` | `code_only` | `python` | fix: add missing access checks to semantic-layer and theme endpoints |
| https://github.com/apache/superset/pull/43461 | `apache/superset` | `code_only` | `python` | fix(gtf): close async-chart-data waiter race + widen guest_key column |
| https://github.com/apache/superset/pull/43445 | `apache/superset` | `code_only` | `python` | chore(deps): bump docker/setup-buildx-action from 4.2.0 to 4.3.0 |
| https://github.com/apache/superset/pull/43448 | `apache/superset` | `code_only` | `python` | chore(deps): bump immer from 11.1.16 to 11.1.17 in /superset-frontend |
| https://github.com/apache/superset/pull/43438 | `apache/superset` | `code_only` | `python` | chore: remove two stale codecov ignore paths |
| https://github.com/apache/superset/pull/43449 | `apache/superset` | `code_only` | `python` | chore(deps-dev): bump concurrently from 10.0.4 to 10.0.5 in /superset-frontend |
| https://github.com/apache/superset/pull/43450 | `apache/superset` | `code_only` | `python` | chore(deps): bump dayjs from 1.11.21 to 1.11.22 in /superset-frontend |
| https://github.com/apache/superset/pull/43451 | `apache/superset` | `code_only` | `python` | chore(deps): bump react-error-boundary from 6.1.2 to 6.1.3 in /superset-frontend |
| https://github.com/apache/superset/pull/43392 | `apache/superset` | `code_only` | `python` | fix(security): surface extra_editors in dashboard/chart lists |
| https://github.com/apache/superset/pull/43056 | `apache/superset` | `code_only` | `python` | fix: set maxHeight of List components to height when in AutoSizer |
| https://github.com/apache/superset/pull/43436 | `apache/superset` | `code_only` | `python` | feat(listview): realtime list updates baked into useListViewResource |
| https://github.com/apache/superset/pull/43437 | `apache/superset` | `code_and_docs` | `python` | feat(docker): ship the websocket server in the official image |
| https://github.com/apache/superset/pull/43435 | `apache/superset` | `code_only` | `python` | feat(coordination): accept a callable key generator in the KV API |
| https://github.com/apache/superset/pull/43434 | `apache/superset` | `code_and_docs` | `python` | feat(websocket): generic task push transport — per-principal chart-data + guest face pile |
| https://github.com/apache/superset/pull/43431 | `apache/superset` | `code_only` | `python` | feat(websocket): realtime transport backend — entity-change nudges + channel tokens |
| https://github.com/apache/superset/pull/43429 | `apache/superset` | `code_only` | `python` | feat(gaq): async chart data opt-in per request (async_mode) + auto-enable GTF |
| https://github.com/apache/superset/pull/43422 | `apache/superset` | `code_only` | `python` | fix(examples): replace deprecated timeseries_limit_metric with series_limit_metric |
| https://github.com/apache/superset/pull/43410 | `apache/superset` | `code_only` | `python` | feat(common): canonical single-query serialization for async chart data |
| https://github.com/apache/superset/pull/43408 | `apache/superset` | `code_and_docs` | `python` | feat(gtf): add task dependencies (DAG) with chain-icon Task List display |
| https://github.com/apache/superset/pull/43409 | `apache/superset` | `code_and_docs` | `python` | refactor(coordination): reliable Redis Streams await/notify (replace at-most-once pub/sub) |
| https://github.com/apache/superset/pull/43351 | `apache/superset` | `code_only` | `python` | fix(sqllab): default PostgreSQL port to 5432 in the dynamic connection form |
| https://github.com/apache/superset/pull/43316 | `apache/superset` | `code_and_docs` | `python` | refactor(coordination): centralize distributed coordination in a single service |
| https://github.com/apache/superset/pull/42792 | `apache/superset` | `code_only` | `python` | feat(chart): enable cross-filter on temporal x-axis (bar/label click) |
| https://github.com/apache/superset/pull/43329 | `apache/superset` | `code_only` | `python` | fix(mcp): fail closed when MCP_AUTH_FACTORY raises |
| https://github.com/apache/superset/pull/43402 | `apache/superset` | `code_and_docs` | `python` | fix(charts): surface blocking alerts/reports when archiving a chart |
| https://github.com/apache/superset/pull/43396 | `apache/superset` | `code_only` | `python` | fix(export): escape formula-triggering values consistently and bound post-processing inputs |
| https://github.com/apache/superset/pull/43394 | `apache/superset` | `code_only` | `python` | fix(sqllab): re-validate access against rendered SQL and tighten cache/permalink scoping |
| https://github.com/apache/superset/pull/43397 | `apache/superset` | `code_only` | `python` | fix(charts): escape untrusted strings before rendering into chart tooltips and popups |
| https://github.com/apache/superset/pull/43395 | `apache/superset` | `code_only` | `python` | fix: tighten SSRF validation, executor resolution, and cache scoping across reports/thumbnails |
| https://github.com/apache/superset/pull/43398 | `apache/superset` | `code_only` | `python` | fix(frontend): tighten SQL Lab autorun scoping and HTML-rendering defaults |
| https://github.com/apache/superset/pull/43393 | `apache/superset` | `code_only` | `python` | fix(import): tighten ownership and validation checks across asset importers |
| https://github.com/apache/superset/pull/43354 | `apache/superset` | `code_only` | `python` | fix(explore): exclude permalink_key from chart URL params |
| https://github.com/apache/superset/pull/43373 | `apache/superset` | `code_only` | `python` | fix(explore): align viz type gallery thumbnails and Featured tag |
| https://github.com/apache/superset/pull/43387 | `apache/superset` | `code_only` | `python` | fix(embedded-sdk): grant fullscreen and clipboard-write by default (#39943) |
| https://github.com/apache/superset/pull/42299 | `apache/superset` | `code_only` | `python` | fix: last date label hidden on time series x-axis (#39899) |
| https://github.com/apache/superset/pull/43111 | `apache/superset` | `code_only` | `python` | fix(embedded): block custom SQL injection in guest user chart payloads |
| https://github.com/apache/superset/pull/43330 | `apache/superset` | `code_only` | `python` | fix(sqllab): disable Save dataset until the query runs successfully |
| https://github.com/apache/superset/pull/40882 | `apache/superset` | `code_only` | `python` | ci: pull CI service images from GHCR mirror (fork-safe) [depends on #40880] |
| https://github.com/apache/superset/pull/43378 | `apache/superset` | `code_only` | `python` | chore(deps): bump astral-sh/setup-uv from 10.0.0 to 10.0.1 |
| https://github.com/apache/superset/pull/43379 | `apache/superset` | `code_only` | `python` | chore(deps-dev): bump the storybook group in /superset-frontend with 5 updates |
| https://github.com/apache/superset/pull/43380 | `apache/superset` | `code_only` | `python` | chore(deps): bump dompurify from 3.4.12 to 3.4.13 in /superset-frontend |
| https://github.com/apache/superset/pull/43381 | `apache/superset` | `code_only` | `python` | chore(deps-dev): bump baseline-browser-mapping from 2.11.13 to 2.11.14 in /superset-frontend |
| https://github.com/apache/superset/pull/43310 | `apache/superset` | `code_only` | `python` | fix(listview): stop card clicks creating a duplicate history entry |
| https://github.com/apache/superset/pull/40048 | `apache/superset` | `code_only` | `python` | fix(ux): use title case for button labels |
| https://github.com/apache/superset/pull/43349 | `apache/superset` | `code_only` | `python` | fix(mcp): honor use_cache and cache_timeout in get_chart_data |
| https://github.com/apache/superset/pull/43369 | `apache/superset` | `code_only` | `python` | fix(plugin-chart-echarts): restore tooltips for metrics labelled like… |
| https://github.com/apache/superset/pull/43147 | `apache/superset` | `code_only` | `python` | fix(sqllab): stop copying a permalink when opening a saved query |
| https://github.com/apache/superset/pull/43315 | `apache/superset` | `code_only` | `python` | fix(charts): align grain-less time comparisons safely |
| https://github.com/apache/superset/pull/43307 | `apache/superset` | `code_only` | `python` | fix(reports): humanize day-of-month + day-of-week crontabs as OR |
| https://github.com/apache/superset/pull/43337 | `apache/superset` | `code_only` | `python` | feat(config): add EXTRA_PANDAS_POSTPROCESSING_OPS extension point |
| https://github.com/apache/superset/pull/43264 | `apache/superset` | `code_only_tests_or_fixtures` | `python` | test(frontend): shrink flaky/misplaced recently-archived e2e coverage to Jest unit tests |
| https://github.com/apache/superset/pull/42756 | `apache/superset` | `code_only` | `python` | fix(plugin-chart-echarts): omit stacked value labels on zero-height segments |
| https://github.com/apache/superset/pull/43115 | `apache/superset` | `code_only` | `python` | fix(explore): show the empty state when Samples returns no result payload |
| https://github.com/apache/superset/pull/42875 | `apache/superset` | `code_only` | `python` | fix(explore): keep x-axis label when overriding Time Column with time comparison |
| https://github.com/apache/superset/pull/43228 | `apache/superset` | `code_only` | `python` | fix(chart): ignore chart actions for a chart no longer in state |
| https://github.com/apache/superset/pull/43357 | `apache/superset` | `code_and_docs` | `python` | fix(github): point the issue templates at labels that exist |
| https://github.com/apache/superset/pull/40984 | `apache/superset` | `code_only` | `python` | fix(native-filters): persist created/pasted default values in select filter |
| https://github.com/apache/superset/pull/43348 | `apache/superset` | `code_only` | `python` | fix(reports): prevent blank/partial report PDFs from virtualized charts |
| https://github.com/apache/superset/pull/43361 | `apache/superset` | `code_only` | `python` | chore(deps): bump github/codeql-action/analyze from 4.37.6 to 4.37.7 |
| https://github.com/apache/superset/pull/43360 | `apache/superset` | `code_only` | `python` | chore(deps-dev): bump globals from 17.10.0 to 17.11.0 in /superset-websocket |
| https://github.com/apache/superset/pull/43362 | `apache/superset` | `code_only` | `python` | chore(deps): bump github/codeql-action/init from 4.37.6 to 4.37.7 |
| https://github.com/apache/superset/pull/43364 | `apache/superset` | `code_only` | `python` | chore(deps): bump google-auth-library from 11.0.1 to 11.0.2 in /superset-frontend |
| https://github.com/apache/superset/pull/42927 | `apache/superset` | `code_only` | `python` | fix: drop post-processing options the operation no longer accepts |
| https://github.com/apache/superset/pull/43304 | `apache/superset` | `code_only` | `python` | fix(plugin-chart-chord): declare react as a peerDependency |
| https://github.com/apache/superset/pull/43341 | `apache/superset` | `code_only` | `python` | fix(explore): legacy boolean filters and limit available operators based on calculated column type |
| https://github.com/apache/superset/pull/43213 | `apache/superset` | `code_only` | `python` | chore(ci): disable Git commit info capture in Playwright E2E tests to avoid timeout |
| https://github.com/apache/superset/pull/43269 | `apache/superset` | `code_only` | `python` | feat(semantic layers): optional metadata for metrics/dimensions |
| https://github.com/apache/superset/pull/43322 | `apache/superset` | `code_only` | `python` | chore(deps): bump astral-sh/setup-uv from 9.0.0 to 10.0.0 |
| https://github.com/apache/superset/pull/43191 | `apache/superset` | `code_only` | `python` | fix(users): show password validation errors |
| https://github.com/apache/superset/pull/43267 | `apache/superset` | `code_only` | `python` | fix(chart): stop contextmenu propagation in BigNumberViz |
| https://github.com/apache/superset/pull/43190 | `apache/superset` | `code_only` | `python` | fix(dataset): preserve legacy default dashboard URLs |
| https://github.com/apache/superset/pull/43321 | `apache/superset` | `code_only` | `python` | chore(deps-dev): bump globals from 17.9.0 to 17.10.0 in /superset-websocket |
| https://github.com/apache/superset/pull/43326 | `apache/superset` | `code_only` | `python` | chore(deps): bump dompurify from 3.4.12 to 3.4.13 in /superset-frontend |
| https://github.com/apache/superset/pull/43328 | `apache/superset` | `code_only` | `python` | chore(deps-dev): bump @swc/plugin-emotion from 14.15.0 to 14.19.0 in /superset-frontend |
| https://github.com/apache/superset/pull/41279 | `apache/superset` | `code_only` | `python` | feat(multi-value): array-typed column filters with two-tier operators (ClickHouse MVP) |
| https://github.com/apache/superset/pull/43129 | `apache/superset` | `code_only` | `python` | fix(mcp): validate virtual dataset metadata and surface errors |
| https://github.com/apache/superset/pull/43183 | `apache/superset` | `code_only_tests_or_fixtures` | `python` | test(chart): mock the event log endpoint in the drill-to-detail menu test |
| https://github.com/apache/superset/pull/43270 | `apache/superset` | `code_only` | `python` | fix: remove a labeler glob that matches no files |
| https://github.com/apache/superset/pull/43217 | `apache/superset` | `code_and_docs` | `python` | fix(clickhouse): add PT1S time grain |
| https://github.com/apache/superset/pull/43272 | `apache/superset` | `code_only` | `python` | feat(tooltip): add Truncate labels control to timeseries charts |
| https://github.com/apache/superset/pull/43256 | `apache/superset` | `code_and_docs` | `python` | fix(dashboard): align list OpenAPI schema |
| https://github.com/apache/superset/pull/43290 | `apache/superset` | `code_only` | `python` | chore(deps): bump supercluster from 8.0.1 to 9.0.0 in /superset-frontend |
| https://github.com/apache/superset/pull/43284 | `apache/superset` | `code_only` | `python` | chore(deps-dev): bump @typescript-eslint/eslint-plugin from 8.65.0 to 8.67.0 in /superset-websocket |
| https://github.com/apache/superset/pull/42297 | `apache/superset` | `code_and_docs` | `python` | feat(mcp): per-resource token scopes with user-permission intersection |
| https://github.com/apache/superset/pull/42879 | `apache/superset` | `code_only` | `python` | fix(dashboard): mute the Group By display control loading spinner |
| https://github.com/apache/superset/pull/42934 | `apache/superset` | `code_only` | `python` | fix(security): harden account password-change and session-invalidation handling |
| https://github.com/apache/superset/pull/43148 | `apache/superset` | `code_and_docs` | `python` | fix(explore): samples endpoint now honors requested row limit |
| https://github.com/apache/superset/pull/43293 | `apache/superset` | `code_only` | `python` | chore(deps-dev): bump oxfmt from 0.62.0 to 0.63.0 in /superset-frontend |
| https://github.com/apache/superset/pull/43294 | `apache/superset` | `code_only` | `python` | chore(deps): bump antd from 6.5.4 to 6.6.0 in /superset-frontend |
| https://github.com/apache/superset/pull/43281 | `apache/superset` | `code_only` | `python` | chore(deps-dev): bump @typescript-eslint/parser from 8.66.0 to 8.67.0 in /superset-websocket |
| https://github.com/apache/superset/pull/43282 | `apache/superset` | `code_only` | `python` | chore(deps-dev): bump typescript-eslint from 8.66.0 to 8.67.0 in /superset-websocket |
| https://github.com/apache/superset/pull/43283 | `apache/superset` | `code_only` | `python` | chore(deps-dev): bump oxfmt from 0.62.0 to 0.63.0 in /superset-websocket |
| https://github.com/apache/superset/pull/43285 | `apache/superset` | `code_only` | `python` | chore(deps-dev): bump @typescript-eslint/eslint-plugin from 8.66.0 to 8.67.0 in /superset-frontend in the typescript-eslint group |
| https://github.com/apache/superset/pull/43288 | `apache/superset` | `code_only` | `python` | chore(deps-dev): bump oxlint from 1.77.0 to 1.78.0 in /superset-frontend |
| https://github.com/apache/superset/pull/43291 | `apache/superset` | `code_only` | `python` | chore(deps): bump dompurify from 3.4.12 to 3.4.13 in /superset-frontend |
| https://github.com/apache/superset/pull/43292 | `apache/superset` | `code_only` | `python` | chore(deps): bump google-auth-library from 11.0.0 to 11.0.1 in /superset-frontend |
| https://github.com/apache/superset/pull/42930 | `apache/superset` | `code_and_docs` | `python` | fix(api): improved request handling and embedded dashboard scoping |
| https://github.com/apache/superset/pull/43031 | `apache/superset` | `code_only` | `python` | fix(reports): fail closed on alert screenshot capture instead of delivering a blank |
| https://github.com/apache/superset/pull/43077 | `apache/superset` | `code_only` | `python` | fix(reports): wait for ECharts paint before capturing report screenshots |
| https://github.com/apache/superset/pull/43140 | `apache/superset` | `code_only` | `python` | fix(dashboard): report the real error when saving a dashboard fails |
| https://github.com/apache/superset/pull/43110 | `apache/superset` | `code_only` | `python` | fix(db_engine_specs): skip malformed third-party dialect entry points |
| https://github.com/apache/superset/pull/43226 | `apache/superset` | `code_only` | `python` | fix(sql-lab): catch TemplateError in StreamingSqlResultExportCommand.validate |
| https://github.com/apache/superset/pull/43240 | `apache/superset` | `code_only` | `python` | chore(deps-dev): bump @types/node from 26.1.2 to 26.2.0 in /superset-websocket |
| https://github.com/apache/superset/pull/43241 | `apache/superset` | `code_only` | `python` | chore(deps): bump ws from 8.21.2 to 8.21.3 in /superset-websocket |
| https://github.com/apache/superset/pull/43242 | `apache/superset` | `code_only` | `python` | chore(deps-dev): bump eslint from 10.8.0 to 10.8.1 in /superset-websocket |
| https://github.com/apache/superset/pull/43246 | `apache/superset` | `code_only` | `python` | chore(deps-dev): bump @testing-library/jest-dom from 7.0.0 to 7.0.1 in /superset-frontend |
| https://github.com/apache/superset/pull/43247 | `apache/superset` | `code_only` | `python` | chore(deps-dev): bump @types/node from 26.1.2 to 26.2.0 in /superset-frontend |
| https://github.com/apache/superset/pull/43248 | `apache/superset` | `code_only` | `python` | chore(deps-dev): bump eslint from 10.8.0 to 10.8.1 in /superset-frontend |
| https://github.com/apache/superset/pull/43249 | `apache/superset` | `code_only` | `python` | chore(deps-dev): bump baseline-browser-mapping from 2.11.12 to 2.11.13 in /superset-frontend |
| https://github.com/apache/superset/pull/43250 | `apache/superset` | `code_only` | `python` | chore(deps-dev): bump tsx from 4.23.10 to 4.23.12 in /superset-frontend |
| https://github.com/apache/superset/pull/43255 | `apache/superset` | `code_only` | `python` | fix(datasets): keep metric certified_by when certification details are typed next |
| https://github.com/apache/superset/pull/43252 | `apache/superset` | `code_only` | `python` | fix(dashboard): derive filter scope on read instead of serving a stale cache |
| https://github.com/apache/superset/pull/43163 | `apache/superset` | `code_and_docs` | `python` | fix(calendar): localize date labels |
| https://github.com/apache/superset/pull/42763 | `apache/superset` | `code_only` | `python` | fix(datasets): preserve metric warning_markdown when extra is absent |
| https://github.com/apache/superset/pull/43166 | `apache/superset` | `code_only` | `python` | fix(ci): update vulnerable transitive nanoid |
| https://github.com/apache/superset/pull/43197 | `apache/superset` | `code_only` | `python` | ci: declare top-level permissions on the remaining workflows |
| https://github.com/apache/superset/pull/43207 | `apache/superset` | `code_only` | `python` | chore(deps): bump mako from 1.3.12 to 1.4.1 |
| https://github.com/apache/superset/pull/43209 | `apache/superset` | `code_only` | `python` | chore(deps-dev): bump sqlalchemy-bigquery from 1.17.1 to 1.17.2 |
| https://github.com/apache/superset/pull/43212 | `apache/superset` | `code_only` | `python` | chore(deps-dev): bump pandas-gbq from 0.35.0 to 0.35.1 |
| https://github.com/apache/superset/pull/43210 | `apache/superset` | `code_only` | `python` | chore(deps-dev): bump fastmcp from 3.4.5 to 3.4.7 |
| https://github.com/apache/superset/pull/43208 | `apache/superset` | `code_only` | `python` | chore(deps): bump cachetools from 7.1.6 to 7.1.7 |
| https://github.com/apache/superset/pull/43211 | `apache/superset` | `code_only` | `python` | chore(deps-dev): update pyocient requirement from <4,>=1.0.15 to >=3.9.0,<4 |
| https://github.com/microsoft/kiota/pull/8082 | `microsoft/kiota` | `code_only` | `typescript` | build(deps): bump the codeql group with 2 updates |
| https://github.com/microsoft/kiota/pull/8081 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump brace-expansion from 1.1.14 to 1.1.18 in /vscode |
| https://github.com/microsoft/kiota/pull/8079 | `microsoft/kiota` | `code_only` | `typescript` | Group CodeQL GitHub Actions Dependabot updates |
| https://github.com/microsoft/kiota/pull/8064 | `microsoft/kiota` | `code_and_docs` | `typescript` | Collapse oneOf nullable reference types to the target type |
| https://github.com/microsoft/kiota/pull/8070 | `microsoft/kiota` | `code_only` | `typescript` | build(deps): bump dotnet-sdk from 10.0.302 to 10.0.400 |
| https://github.com/microsoft/kiota/pull/8057 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump esbuild from 0.28.1 to 0.28.2 in /it/typescript |
| https://github.com/microsoft/kiota/pull/8066 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump @typescript-eslint/eslint-plugin from 8.66.0 to 8.67.0 in /it/typescript in the eslint group |
| https://github.com/microsoft/kiota/pull/7889 | `microsoft/kiota` | `code_only_tests_or_fixtures` | `typescript` | Test optional operation security auth |
| https://github.com/microsoft/kiota/pull/8069 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump @typescript-eslint/eslint-plugin from 8.66.0 to 8.67.0 in /vscode in the eslint group |
| https://github.com/microsoft/kiota/pull/8063 | `microsoft/kiota` | `code_and_docs` | `typescript` | Fix: additonal default value check for all languages |
| https://github.com/microsoft/kiota/pull/8059 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump @types/node from 26.1.1 to 26.2.0 in /it/typescript |
| https://github.com/microsoft/kiota/pull/8060 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump @types/node from 26.1.2 to 26.2.0 in /vscode |
| https://github.com/microsoft/kiota/pull/8062 | `microsoft/kiota` | `code_only_tests_or_fixtures` | `typescript` | build(deps): bump jimschubert/delete-artifacts-action from 1.0.3 to 1.0.4 |
| https://github.com/microsoft/kiota/pull/7996 | `microsoft/kiota` | `code_only` | `typescript` | Fix missing (de)serializer registration after workspace refresh |
| https://github.com/microsoft/kiota/pull/8054 | `microsoft/kiota` | `code_and_docs` | `typescript` | Fix: Adding additional check to boolean and numeric values in code writer |
| https://github.com/microsoft/kiota/pull/8024 | `microsoft/kiota` | `code_only_tests_or_fixtures` | `typescript` | build(deps): bump dart-lang/setup-dart from 1.7.2 to 1.8.0 |
| https://github.com/microsoft/kiota/pull/8055 | `microsoft/kiota` | `code_and_docs` | `typescript` | fix: check oauth card path |
| https://github.com/microsoft/kiota/pull/8051 | `microsoft/kiota` | `code_only` | `typescript` | Pin GitHub Actions to full-length commit SHAs |
| https://github.com/microsoft/kiota/pull/8053 | `microsoft/kiota` | `code_and_docs` | `typescript` | fix(ruby): resolve enum default values by wire name instead of raw value |
| https://github.com/microsoft/kiota/pull/8052 | `microsoft/kiota` | `code_and_docs` | `typescript` | fix(ruby): fix factory method syntax errors and RuboCop offenses |
| https://github.com/microsoft/kiota/pull/8050 | `microsoft/kiota` | `code_and_docs` | `typescript` | build(deps): bump Microsoft.OpenApi to 3.10.0 |
| https://github.com/microsoft/kiota/pull/8049 | `microsoft/kiota` | `code_only` | `typescript` | build(deps): bump actions/upload-code-coverage from 1.4.1 to 1.4.2 |
| https://github.com/microsoft/kiota/pull/8048 | `microsoft/kiota` | `code_only` | `typescript` | ci: adds condition to skip dependabot PRs since it doesn't have permissions |
| https://github.com/microsoft/kiota/pull/7978 | `microsoft/kiota` | `code_and_docs` | `typescript` | feat: resolve $dynamicRef generic bindings with per-context classes |
| https://github.com/microsoft/kiota/pull/8046 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump flit-core from 3.12.0 to 4.0.2 in /it/python |
| https://github.com/microsoft/kiota/pull/8022 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump @types/node from 26.1.1 to 26.1.2 in /vscode |
| https://github.com/microsoft/kiota/pull/8039 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump the eslint group in /it/typescript with 2 updates |
| https://github.com/microsoft/kiota/pull/7994 | `microsoft/kiota` | `code_and_docs` | `typescript` | fix: map numeric scalar unions with a format to the numeric type |
| https://github.com/microsoft/kiota/pull/8042 | `microsoft/kiota` | `code_only` | `typescript` | build(deps): bump github/codeql-action from 4.37.5 to 4.37.6 |
| https://github.com/microsoft/kiota/pull/8041 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump the eslint group in /vscode with 2 updates |
| https://github.com/microsoft/kiota/pull/8027 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump webpack from 5.108.4 to 5.109.2 in /vscode |
| https://github.com/microsoft/kiota/pull/8036 | `microsoft/kiota` | `code_and_docs` | `typescript` | ci: cleans up sonarcloud backing up the merge queue |
| https://github.com/microsoft/kiota/pull/7987 | `microsoft/kiota` | `code_and_docs` | `typescript` | ci: adds validation and message for changelog entry |
| https://github.com/microsoft/kiota/pull/8026 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump webpack-cli from 7.2.1 to 7.2.2 in /vscode |
| https://github.com/microsoft/kiota/pull/8017 | `microsoft/kiota` | `code_only` | `typescript` | fix(java,php): neutralize doc-comment delimiters instead of deleting them |
| https://github.com/microsoft/kiota/pull/8015 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump @vscode/test-electron from 3.0.0 to 3.1.0 in /vscode |
| https://github.com/microsoft/kiota/pull/8037 | `microsoft/kiota` | `code_and_docs` | `typescript` | Fix/ruby 4262 indentation |
| https://github.com/microsoft/kiota/pull/8035 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump mocha from 11.7.6 to 11.8.0 in /vscode |
| https://github.com/microsoft/kiota/pull/8029 | `microsoft/kiota` | `code_only` | `typescript` | fix(vscode): sanitize and lock down Dependencies webview to prevent XSS |
| https://github.com/microsoft/kiota/pull/8028 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump fast-uri from 3.1.4 to 3.1.5 in /vscode |
| https://github.com/microsoft/kiota/pull/8034 | `microsoft/kiota` | `code_only` | `typescript` | build(deps): bump github/codeql-action from 4.37.1 to 4.37.5 |
| https://github.com/microsoft/kiota/pull/8033 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump js-yaml from 4.3.0 to 4.3.1 in /it/typescript |
| https://github.com/microsoft/kiota/pull/8004 | `microsoft/kiota` | `code_only_tests_or_fixtures` | `typescript` | build(deps): bump ruby/setup-ruby from 1.319.0 to 1.321.0 |
| https://github.com/microsoft/kiota/pull/7992 | `microsoft/kiota` | `code_only` | `typescript` | build(deps): bump actions/upload-code-coverage from 1.4.0 to 1.4.1 |
| https://github.com/microsoft/kiota/pull/7985 | `microsoft/kiota` | `code_only` | `typescript` | Route update_appsettings version lookups through private Azure Artifacts feed |
| https://github.com/microsoft/kiota/pull/7993 | `microsoft/kiota` | `code_only` | `typescript` | ci: switches to merge queue for the dependabot auto-merge workflow |
| https://github.com/microsoft/kiota/pull/7995 | `microsoft/kiota` | `code_and_docs` | `typescript` | fix/typescript binary type |
| https://github.com/microsoft/kiota/pull/7983 | `microsoft/kiota` | `code_only` | `typescript` | build(deps): bump github/codeql-action from 4 to 4.37.1 |
| https://github.com/microsoft/kiota/pull/7984 | `microsoft/kiota` | `code_only_tests_or_fixtures` | `typescript` | build(deps): bump ruby/setup-ruby from 1 to 1.319.0 |
| https://github.com/microsoft/kiota/pull/7982 | `microsoft/kiota` | `code_only` | `typescript` | build(deps): bump actions/upload-code-coverage from 1 to 1.4.0 |
| https://github.com/microsoft/kiota/pull/7979 | `microsoft/kiota` | `code_only` | `typescript` | ci(dependabot): add cooldown default delay |
| https://github.com/microsoft/kiota/pull/7981 | `microsoft/kiota` | `code_only` | `typescript` | Enable merge queue on main and drop strict status checks |
| https://github.com/microsoft/kiota/pull/7881 | `microsoft/kiota` | `code_only` | `typescript` | build(deps): bump vscode-jsonrpc from 8.2.1 to 9.0.1 in /vscode |
| https://github.com/microsoft/kiota/pull/7943 | `microsoft/kiota` | `code_and_docs` | `typescript` | Add OpenAPI webhook model generation |
| https://github.com/microsoft/kiota/pull/7977 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump ts-jest from 29.4.11 to 29.4.12 in /vscode |
| https://github.com/microsoft/kiota/pull/7973 | `microsoft/kiota` | `code_and_docs` | `typescript` | fix(go): emit LF line endings for generated Go code |
| https://github.com/microsoft/kiota/pull/7972 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump fast-uri from 3.1.2 to 3.1.4 in /vscode |
| https://github.com/microsoft/kiota/pull/7774 | `microsoft/kiota` | `code_and_docs` | `typescript` | ci: Replace APIGurus as source for IT |
| https://github.com/microsoft/kiota/pull/7817 | `microsoft/kiota` | `code_and_docs` | `typescript` | feat: resolve $dynamicRef against $dynamicAnchor for recursive types |
| https://github.com/microsoft/kiota/pull/7967 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump the eslint group in /it/typescript with 2 updates |
| https://github.com/microsoft/kiota/pull/7968 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump prettier from 3.9.5 to 3.9.6 in /it/typescript |
| https://github.com/microsoft/kiota/pull/7970 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump the eslint group in /vscode with 2 updates |
| https://github.com/microsoft/kiota/pull/7971 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump sinon from 22.0.0 to 22.1.0 in /vscode |
| https://github.com/microsoft/kiota/pull/7965 | `microsoft/kiota` | `code_only` | `typescript` | build(deps): bump body-parser from 2.2.1 to 2.3.0 in /it/typescript |
| https://github.com/microsoft/kiota/pull/7964 | `microsoft/kiota` | `code_only` | `typescript` | Fix S360 open-source vulnerabilities (SFI-ES5.2) |
| https://github.com/microsoft/kiota/pull/7962 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump brace-expansion from 1.1.14 to 1.1.16 in /it/typescript |
| https://github.com/microsoft/kiota/pull/7961 | `microsoft/kiota` | `code_only` | `typescript` | Route NuGet restore through the CFS central package feed |
| https://github.com/microsoft/kiota/pull/7954 | `microsoft/kiota` | `code_and_docs` | `typescript` | Fix non-idempotent model class descriptions for shared component schemas (#7927) |
| https://github.com/microsoft/kiota/pull/7957 | `microsoft/kiota` | `code_only_tests_or_fixtures` | `typescript` | build(deps): bump actions/setup-python from 6 to 7 |
| https://github.com/microsoft/kiota/pull/7950 | `microsoft/kiota` | `code_only` | `typescript` | build(deps): bump actions/setup-go from 6 to 7 |
| https://github.com/microsoft/kiota/pull/6416 | `microsoft/kiota` | `code_and_docs` | `typescript` | Format generated Go code to adhere to golang coding standards |
| https://github.com/microsoft/kiota/pull/7944 | `microsoft/kiota` | `code_only_tests_or_fixtures` | `typescript` | build(deps): bump actions/setup-go from 6 to 7 |
| https://github.com/microsoft/kiota/pull/7945 | `microsoft/kiota` | `code_only` | `typescript` | build(deps): bump actions/setup-dotnet from 5 to 6 |
| https://github.com/microsoft/kiota/pull/7937 | `microsoft/kiota` | `code_only` | `typescript` | build(deps): bump dotnet-sdk from 10.0.301 to 10.0.302 |
| https://github.com/microsoft/kiota/pull/7934 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump the eslint group in /it/typescript with 2 updates |
| https://github.com/microsoft/kiota/pull/7936 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump the eslint group in /vscode with 2 updates |
| https://github.com/microsoft/kiota/pull/7933 | `microsoft/kiota` | `code_only` | `typescript` | build(deps): bump actions/setup-node from 6 to 7 |
| https://github.com/microsoft/kiota/pull/7928 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump eslint from 9.39.4 to 9.39.5 in /it/typescript in the eslint group |
| https://github.com/microsoft/kiota/pull/7930 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump eslint from 9.39.4 to 9.39.5 in /vscode in the eslint group across 1 directory |
| https://github.com/microsoft/kiota/pull/7931 | `microsoft/kiota` | `code_only` | `typescript` | build(deps): bump adm-zip from 0.5.18 to 0.6.0 in /vscode |
| https://github.com/microsoft/kiota/pull/7924 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump prettier from 3.9.4 to 3.9.5 in /it/typescript |
| https://github.com/microsoft/kiota/pull/7914 | `microsoft/kiota` | `code_and_docs` | `typescript` | Increase namespace/type-name shortening threshold from 64 to 200 |
| https://github.com/microsoft/kiota/pull/7920 | `microsoft/kiota` | `code_and_docs` | `typescript` | Fix path traversal via workspace consumer identifiers in DescriptionStorageService |
| https://github.com/microsoft/kiota/pull/7915 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump @types/node from 26.1.0 to 26.1.1 in /it/typescript |
| https://github.com/microsoft/kiota/pull/7918 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump @types/node from 26.1.0 to 26.1.1 in /vscode |
| https://github.com/microsoft/kiota/pull/7913 | `microsoft/kiota` | `code_only` | `typescript` | Harden IsSafeFileReference against NUL, deep-encoding, and Unicode homoglyph traversal |
| https://github.com/microsoft/kiota/pull/7910 | `microsoft/kiota` | `code_only` | `typescript` | Fix percent-encoded path traversal in static_template IsSafeFileReference |
| https://github.com/microsoft/kiota/pull/7904 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump the eslint group in /it/typescript with 2 updates |
| https://github.com/microsoft/kiota/pull/7907 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump the eslint group in /vscode with 2 updates |
| https://github.com/microsoft/kiota/pull/7901 | `microsoft/kiota` | `code_and_docs` | `typescript` | Shorten oversized namespace segments for TypeScript generation |
| https://github.com/microsoft/kiota/pull/7897 | `microsoft/kiota` | `code_only` | `typescript` | ci: reset exit codes in idempotent npm/vsce publish checks |
| https://github.com/microsoft/kiota/pull/7899 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump webpack-cli from 7.1.0 to 7.2.1 in /vscode |
| https://github.com/microsoft/kiota/pull/7900 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump webpack from 5.108.3 to 5.108.4 in /vscode |
| https://github.com/microsoft/kiota/pull/7895 | `microsoft/kiota` | `code_only` | `typescript` | ci: make release publish jobs idempotent on re-run |
| https://github.com/microsoft/kiota/pull/7892 | `microsoft/kiota` | `code_and_docs` | `typescript` | fix: reject unsafe static_template.file references in plugin manifest generation |
| https://github.com/microsoft/kiota/pull/7888 | `microsoft/kiota` | `code_and_docs` | `typescript` | feat: adds an allow list parameter for external references resolution |
| https://github.com/microsoft/kiota/pull/7857 | `microsoft/kiota` | `code_and_docs` | `typescript` | feat: map confirmation isNonConsequential in AI capabilities extension |
| https://github.com/microsoft/kiota/pull/7859 | `microsoft/kiota` | `code_and_docs` | `typescript` | ci: add DOM-surface regression integration test |
| https://github.com/microsoft/kiota/pull/7886 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump @types/node from 26.0.1 to 26.1.0 in /it/typescript |
| https://github.com/microsoft/kiota/pull/7887 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump @types/node from 26.0.1 to 26.1.0 in /vscode |
| https://github.com/microsoft/kiota/pull/7885 | `microsoft/kiota` | `code_and_docs` | `typescript` | fix: validate workspace output paths are sub-directories |
| https://github.com/microsoft/kiota/pull/7884 | `microsoft/kiota` | `code_and_docs` | `typescript` | fix: sanitizes the client class and namespace names to avoid code injection |
| https://github.com/microsoft/kiota/pull/7883 | `microsoft/kiota` | `code_and_docs` | `typescript` | fix: do not use the install command from the OpenAPI extension |
| https://github.com/microsoft/kiota/pull/7880 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump @types/sinon from 21.0.1 to 22.0.0 in /vscode |
| https://github.com/microsoft/kiota/pull/7871 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump the eslint group across 1 directory with 2 updates |
| https://github.com/microsoft/kiota/pull/7872 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump prettier from 3.9.1 to 3.9.4 in /it/typescript |
| https://github.com/microsoft/kiota/pull/7873 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump the eslint group across 1 directory with 2 updates |
| https://github.com/microsoft/kiota/pull/7874 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump webpack from 5.108.1 to 5.108.3 in /vscode |
| https://github.com/microsoft/kiota/pull/7875 | `microsoft/kiota` | `code_only` | `typescript` | build(deps): bump adm-zip from 0.5.17 to 0.5.18 in /vscode |
| https://github.com/microsoft/kiota/pull/7867 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump prettier from 3.8.4 to 3.9.1 in /it/typescript |
| https://github.com/microsoft/kiota/pull/7868 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump webpack-cli from 7.0.3 to 7.1.0 in /vscode |
| https://github.com/microsoft/kiota/pull/7869 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump webpack from 5.108.0 to 5.108.1 in /vscode |
| https://github.com/microsoft/kiota/pull/7865 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump webpack from 5.107.2 to 5.108.0 in /vscode |
| https://github.com/microsoft/kiota/pull/7863 | `microsoft/kiota` | `code_only` | `typescript` | fix(php): Escape $ in double-quoted string literals to prevent code injection |
| https://github.com/microsoft/kiota/pull/7847 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump @types/node from 26.0.0 to 26.0.1 in /it/typescript |
| https://github.com/microsoft/kiota/pull/7851 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump @types/node from 26.0.0 to 26.0.1 in /vscode |
| https://github.com/microsoft/kiota/pull/7832 | `microsoft/kiota` | `code_only` | `typescript` | build(deps): bump actions/cache from 5 to 6 |
| https://github.com/microsoft/kiota/pull/7831 | `microsoft/kiota` | `code_only` | `typescript` | fix(csharp): strip newlines from doc comment text to prevent code injection |
| https://github.com/microsoft/kiota/pull/7810 | `microsoft/kiota` | `code_and_docs` | `typescript` | fix(php): call parent constructor only if it exists in parent class |
| https://github.com/microsoft/kiota/pull/7824 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump the eslint group in /it/typescript with 2 updates |
| https://github.com/microsoft/kiota/pull/7825 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump the eslint group across 1 directory with 2 updates |
| https://github.com/microsoft/kiota/pull/7826 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump @vscode/test-cli from 0.0.12 to 0.0.15 in /vscode |
| https://github.com/microsoft/kiota/pull/7819 | `microsoft/kiota` | `code_only` | `typescript` | build(deps): bump uuid from 14.0.0 to 14.0.1 in /vscode |
| https://github.com/microsoft/kiota/pull/7820 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump ts-loader from 9.6.1 to 9.6.2 in /vscode |
| https://github.com/microsoft/kiota/pull/7812 | `microsoft/kiota` | `code_only` | `typescript` | build(deps): bump actions/checkout from 6 to 7 |
| https://github.com/microsoft/kiota/pull/7813 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump @types/node from 25.9.3 to 26.0.0 in /it/typescript |
| https://github.com/microsoft/kiota/pull/7814 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump @types/node from 25.9.3 to 26.0.0 in /vscode |
| https://github.com/microsoft/kiota/pull/7804 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump @types/vscode from 1.120.0 to 1.125.0 in /vscode |
| https://github.com/microsoft/kiota/pull/7800 | `microsoft/kiota` | `code_only` | `typescript` | Emit TypeScript primitive collection deserialization types |
| https://github.com/microsoft/kiota/pull/7760 | `microsoft/kiota` | `code_only` | `typescript` | Improve OpenAPI parsing exception logging |
| https://github.com/microsoft/kiota/pull/7801 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump ts-loader from 9.6.0 to 9.6.1 in /vscode |
| https://github.com/microsoft/kiota/pull/7796 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump the eslint group across 1 directory with 2 updates |
| https://github.com/microsoft/kiota/pull/7799 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump js-yaml from 4.1.1 to 4.2.0 in /it/typescript |
| https://github.com/microsoft/kiota/pull/7797 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump the eslint group in /vscode with 2 updates |
| https://github.com/microsoft/kiota/pull/7792 | `microsoft/kiota` | `code_and_docs` | `typescript` | Fix empty model when allOf inheritance schema is reached via a composed type |
| https://github.com/microsoft/kiota/pull/7789 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump esbuild from 0.28.0 to 0.28.1 in /it/typescript |
| https://github.com/microsoft/kiota/pull/7780 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump @types/node from 25.9.2 to 25.9.3 in /it/typescript |
| https://github.com/microsoft/kiota/pull/7781 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump @types/node from 25.9.2 to 25.9.3 in /vscode |
| https://github.com/microsoft/kiota/pull/7776 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump prettier from 3.8.3 to 3.8.4 in /it/typescript |
| https://github.com/microsoft/kiota/pull/7775 | `microsoft/kiota` | `code_only` | `typescript` | build(deps): bump dotnet-sdk from 10.0.300 to 10.0.301 |
| https://github.com/microsoft/kiota/pull/7773 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump @vscode/test-electron from 2.5.2 to 3.0.0 in /vscode |
| https://github.com/microsoft/kiota/pull/7771 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump the eslint group in /it/typescript with 2 updates |
| https://github.com/microsoft/kiota/pull/7772 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump the eslint group in /vscode with 2 updates |
| https://github.com/microsoft/kiota/pull/7768 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump @types/node from 25.9.1 to 25.9.2 in /it/typescript |
| https://github.com/microsoft/kiota/pull/7769 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump @types/node from 25.9.1 to 25.9.2 in /vscode |
| https://github.com/microsoft/kiota/pull/7765 | `microsoft/kiota` | `code_only` | `typescript` | Fix: Updating kiota to Esrp v12 |
| https://github.com/microsoft/kiota/pull/7764 | `microsoft/kiota` | `code_only` | `typescript` | Fix: template override sensibility |
| https://github.com/microsoft/kiota/pull/7756 | `microsoft/kiota` | `code_and_docs` | `typescript` | Fix URL template override regressions for sibling operations |
| https://github.com/microsoft/kiota/pull/7752 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump ts-loader from 9.5.7 to 9.6.0 in /vscode |
| https://github.com/microsoft/kiota/pull/7751 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump the eslint group in /vscode with 2 updates |
| https://github.com/microsoft/kiota/pull/7747 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump the eslint group in /it/typescript with 2 updates |
| https://github.com/microsoft/kiota/pull/7746 | `microsoft/kiota` | `code_only` | `typescript` | fix(ruby): escape interpolation markers in generated string literals |
| https://github.com/microsoft/kiota/pull/7735 | `microsoft/kiota` | `code_and_docs` | `typescript` | fix(writers/python): prevent code injection via x-ms-enum description |
| https://github.com/microsoft/kiota/pull/7744 | `microsoft/kiota` | `code_only` | `typescript` | ci: skip coverage uploads off default branch |
| https://github.com/microsoft/kiota/pull/7743 | `microsoft/kiota` | `code_only` | `typescript` | ci: use GitHub code coverage uploads |
| https://github.com/microsoft/kiota/pull/7741 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump webpack-cli from 7.0.2 to 7.0.3 in /vscode |
| https://github.com/microsoft/kiota/pull/7731 | `microsoft/kiota` | `code_only` | `typescript` | chore(deps): bump the kiota-dependencies group across 1 directory with 7 updates |
| https://github.com/microsoft/kiota/pull/7732 | `microsoft/kiota` | `code_only` | `typescript` | chore(deps-dev): bump the eslint group in /it/typescript with 2 updates |
| https://github.com/microsoft/kiota/pull/7733 | `microsoft/kiota` | `code_only` | `typescript` | chore(deps-dev): bump the eslint group across 1 directory with 2 updates |
| https://github.com/microsoft/kiota/pull/7734 | `microsoft/kiota` | `code_only` | `typescript` | chore(deps-dev): bump webpack from 5.107.1 to 5.107.2 in /vscode |
| https://github.com/microsoft/kiota/pull/7714 | `microsoft/kiota` | `code_only` | `typescript` | fix: shorten oversized namespace segments and class names for Java, Python, PHP |
| https://github.com/microsoft/kiota/pull/7701 | `microsoft/kiota` | `code_only` | `typescript` | chore(deps-dev): bump @types/vscode from 1.116.0 to 1.120.0 in /vscode |
| https://github.com/microsoft/kiota/pull/7728 | `microsoft/kiota` | `code_only` | `typescript` | build(deps): bump qs from 6.14.2 to 6.15.2 in /it/typescript |
| https://github.com/microsoft/kiota/pull/7717 | `microsoft/kiota` | `code_only` | `typescript` | ci: upgrades python for the integration tests |
| https://github.com/microsoft/kiota/pull/7720 | `microsoft/kiota` | `code_only` | `typescript` | ci: adds dart version refresh to the script |
| https://github.com/microsoft/kiota/pull/7727 | `microsoft/kiota` | `code_only` | `typescript` | build(deps): bump @nevware21/ts-utils from 0.13.0 to 0.14.0 in /vscode |
| https://github.com/microsoft/kiota/pull/7725 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump ts-jest from 29.4.10 to 29.4.11 in /vscode |
| https://github.com/microsoft/kiota/pull/7726 | `microsoft/kiota` | `code_only` | `typescript` | build(deps-dev): bump webpack from 5.107.0 to 5.107.1 in /vscode |
| https://github.com/microsoft/kiota/pull/7721 | `microsoft/kiota` | `code_only` | `typescript` | build(deps): bump uuid and @azure/msal-node in /it/typescript |
| https://github.com/microsoft/kiota/pull/7718 | `microsoft/kiota` | `code_only` | `typescript` | chore(deps-dev): bump mocha from 11.7.5 to 11.7.6 in /vscode |
| https://github.com/microsoft/kiota/pull/7670 | `microsoft/kiota` | `code_and_docs` | `typescript` | Enable API Explorer filter during regeneration path editing |
| https://github.com/microsoft/kiota/pull/7719 | `microsoft/kiota` | `code_only` | `typescript` | chore(deps-dev): update phpunit/phpunit requirement from ^11.5 to ^11.5 \|\| ^13.0 in /it/php/basic |
| https://github.com/microsoft/kiota/pull/7682 | `microsoft/kiota` | `code_only` | `typescript` | chore(deps-dev): bump @types/node from 25.6.0 to 25.9.1 in /vscode |
| https://github.com/microsoft/kiota/pull/7680 | `microsoft/kiota` | `code_only` | `typescript` | chore(deps-dev): bump @types/node from 25.6.0 to 25.9.1 in /it/typescript |
| https://github.com/microsoft/kiota/pull/7706 | `microsoft/kiota` | `code_only` | `typescript` | chore(deps-dev): bump the eslint group in /it/typescript with 2 updates |
| https://github.com/microsoft/kiota/pull/7705 | `microsoft/kiota` | `code_only` | `typescript` | chore(deps-dev): bump the eslint group across 1 directory with 2 updates |
| https://github.com/microsoft/kiota/pull/7707 | `microsoft/kiota` | `code_only` | `typescript` | chore(deps-dev): bump ts-jest from 29.4.9 to 29.4.10 in /vscode |
| https://github.com/microsoft/kiota/pull/7712 | `microsoft/kiota` | `code_only` | `typescript` | chore(deps-dev): bump webpack from 5.106.2 to 5.107.0 in /vscode |
| https://github.com/microsoft/kiota/pull/7710 | `microsoft/kiota` | `code_only` | `typescript` | ci: Exclude some API patterns from integration tests |
| https://github.com/microsoft/kiota/pull/7703 | `microsoft/kiota` | `code_only` | `typescript` | Bump the coverlet group with 2 updates |
| https://github.com/apache/airflow/pull/72080 | `apache/airflow` | `code_only` | `python` | Allow Niko Oliveira to publish provider docs to S3 |
| https://github.com/apache/airflow/pull/72076 | `apache/airflow` | `code_only` | `python` | [v3-3-test] Fix Sphinx error in CLI reference docs for dags test command (#71120) |
| https://github.com/apache/airflow/pull/71120 | `apache/airflow` | `code_only` | `python` | Fix Sphinx error in CLI reference docs for dags test command |
| https://github.com/apache/airflow/pull/72065 | `apache/airflow` | `code_only` | `python` | Bump eslint from 10.8.1 to 10.9.0 in /providers/fab/src/airflow/providers/fab/www in the fab-ui-package-updates group across 1 directory |
| https://github.com/apache/airflow/pull/72069 | `apache/airflow` | `code_and_docs` | `python` | Prepare providers release 2026-08-25 |
| https://github.com/apache/airflow/pull/70238 | `apache/airflow` | `code_and_docs` | `python` | Add securityContexts.disableDefaults flag for OpenShift SCC compatibility |
| https://github.com/apache/airflow/pull/72067 | `apache/airflow` | `code_only_tests_or_fixtures` | `python` | [chart/v1-2x-test] Add Worker Set override tests for Kerberos sidecar startup probe (#72017) |
| https://github.com/apache/airflow/pull/71919 | `apache/airflow` | `code_only` | `python` | Authorize team-scoped plugin API endpoints in multi-team mode |
| https://github.com/apache/airflow/pull/72066 | `apache/airflow` | `code_only` | `python` | Bump eslint from 10.8.1 to 10.9.0 in /providers/fab/src/airflow/providers/fab/www in the 3-3-fab-ui-package-updates group across 1 directory |
| https://github.com/apache/airflow/pull/64422 | `apache/airflow` | `code_and_docs` | `python` | Add GitHub App authentication for git DAG bundles |
| https://github.com/apache/airflow/pull/72017 | `apache/airflow` | `code_only_tests_or_fixtures` | `python` | Test Kerberos startup probe overrides in Worker Sets |
| https://github.com/apache/airflow/pull/68627 | `apache/airflow` | `code_only` | `python` | Tidy DagVersion/DagCode metadata helpers |
| https://github.com/apache/airflow/pull/71956 | `apache/airflow` | `code_only` | `python` | [v3-3-test] Fix nested non-Dag with-statement exiting the Dag context in version inflation checker (#68795) |
| https://github.com/apache/airflow/pull/71975 | `apache/airflow` | `code_only` | `python` | Surface provider triggers in the operators and hooks reference |
| https://github.com/apache/airflow/pull/72022 | `apache/airflow` | `code_only` | `python` | Enable the airflow.utils.timezone ban rule |
| https://github.com/apache/airflow/pull/71783 | `apache/airflow` | `code_only` | `python` | Add prek hook to catch operators missing from common-ai docs index |
| https://github.com/apache/airflow/pull/72005 | `apache/airflow` | `code_only` | `python` | UI: Stop list pages jumping while a filter loads |
| https://github.com/apache/airflow/pull/71799 | `apache/airflow` | `code_only_tests_or_fixtures` | `python` | Fix asset events test for Dag runs without start date |
| https://github.com/apache/airflow/pull/69829 | `apache/airflow` | `code_only` | `python` | Update providers metadata 2026-07-13 |
| https://github.com/apache/airflow/pull/68685 | `apache/airflow` | `code_only` | `python` | Fix mypy errors for task_instance access in provider triggers |
| https://github.com/apache/airflow/pull/72045 | `apache/airflow` | `code_and_docs` | `python` | Update multi-team docs to match the teams CLI and name rules |
| https://github.com/apache/airflow/pull/72029 | `apache/airflow` | `code_only` | `python` | `is_scheduled` REST API parameter |
| https://github.com/apache/airflow/pull/71916 | `apache/airflow` | `code_and_docs` | `python` | UI: Add team column and filter to the audit log |
| https://github.com/apache/airflow/pull/69965 | `apache/airflow` | `code_only` | `python` | Warn on suspicious Dag and task IDs at Go SDK build time |
| https://github.com/apache/airflow/pull/71158 | `apache/airflow` | `code_only` | `python` | Clarify which signal each duplicated otel_* config option applies to |
| https://github.com/apache/airflow/pull/72010 | `apache/airflow` | `code_and_docs` | `python` | Support Azure national clouds in FAB Azure AD id_token validation |
| https://github.com/apache/airflow/pull/67881 | `apache/airflow` | `code_only` | `python` | Drain result_queue in LocalExecutor to prevent process join deadlock |
| https://github.com/apache/airflow/pull/69827 | `apache/airflow` | `code_and_docs` | `python` | Java SDK: Clearer error when a task class cannot be instantiated |
| https://github.com/apache/airflow/pull/71170 | `apache/airflow` | `code_only` | `python` | Fix OpenSearch remote logging crash if port is empty |
| https://github.com/apache/airflow/pull/68833 | `apache/airflow` | `code_only` | `python` | Display owner_display_name in Audit Log |
| https://github.com/apache/airflow/pull/71900 | `apache/airflow` | `code_only` | `python` | Bump @7nohe/openapi-react-query-codegen from 2.2.0 to 3.0.2 in /airflow-core/src/airflow/api_fastapi/auth/managers/simple/ui |
| https://github.com/apache/airflow/pull/70839 | `apache/airflow` | `code_only` | `python` | Make KeycloakAuthManager cache configurable |
| https://github.com/apache/airflow/pull/71933 | `apache/airflow` | `code_only` | `python` | Make the FAB roles PATCH endpoint replace permissions, not just add them |
| https://github.com/apache/airflow/pull/71920 | `apache/airflow` | `code_and_docs` | `python` | Fix Azure AD tenant identifier canonicalization in FAB auth manager |
| https://github.com/apache/airflow/pull/68884 | `apache/airflow` | `code_only` | `python` | UI: Show partition preview in backfill form for partitioned Dags |
| https://github.com/apache/airflow/pull/71963 | `apache/airflow` | `code_only` | `python` | [v3-3-test] Surface connection test errors in the UI instead of failing silently (#71954) |
| https://github.com/apache/airflow/pull/71953 | `apache/airflow` | `code_only` | `python` | [v3-3-test] Include the JSON parse-error message in the Variable form warning (#71780) |
| https://github.com/apache/airflow/pull/71952 | `apache/airflow` | `code_only` | `python` | [v3-3-test] UI: Allow file downloads from plugin external view iframes (#71803) |
| https://github.com/apache/airflow/pull/72012 | `apache/airflow` | `code_and_docs` | `python` | Fix Vertex AI hook silently discarding credentials when vertexai flag is set |
| https://github.com/apache/airflow/pull/70517 | `apache/airflow` | `code_and_docs` | `python` | Support a Unix Domain Socket for the metrics clients |
| https://github.com/apache/airflow/pull/70665 | `apache/airflow` | `code_only` | `python` | reject mixed-separator path traversal in imap attachment names |
| https://github.com/apache/airflow/pull/70215 | `apache/airflow` | `code_only` | `python` | reject backslash-after-scheme urls in is_safe_url |
| https://github.com/apache/airflow/pull/72009 | `apache/airflow` | `code_only` | `python` | Update providers metadata 2026-08-23 |
| https://github.com/apache/airflow/pull/71682 | `apache/airflow` | `code_only` | `python` | [chart/v1-2x-test] Add startup probe for Kerberos worker sidecars (#71221) |
| https://github.com/apache/airflow/pull/71856 | `apache/airflow` | `code_and_docs` | `python` | Document LLMFileAnalysisOperator's inherited LLM and HITL parameters |
| https://github.com/apache/airflow/pull/71611 | `apache/airflow` | `code_and_docs` | `python` | Support .md file in LLMFileAnalysisOperator |
| https://github.com/apache/airflow/pull/71841 | `apache/airflow` | `code_only` | `python` | Add test_connection support to LangChainHook and LlamaIndexHook |
| https://github.com/apache/airflow/pull/69231 | `apache/airflow` | `code_only_tests_or_fixtures` | `python` | Add unit tests for HTTP provider exceptions |
| https://github.com/apache/airflow/pull/71980 | `apache/airflow` | `code_only` | `python` | Updated tutorial DAGs to use named parameters |
| https://github.com/apache/airflow/pull/71946 | `apache/airflow` | `code_and_docs` | `python` | Add BaseManagedAgentToolset for vendor-managed AI agents  |
| https://github.com/apache/airflow/pull/71937 | `apache/airflow` | `code_only` | `python` | [v3-3-test] Reduce memory used when deleting queued asset events (#71917) |
| https://github.com/apache/airflow/pull/70228 | `apache/airflow` | `code_only` | `python` | Parse additional Kafka, Redis & SQS options in `broker_transport_options` |
| https://github.com/apache/airflow/pull/71971 | `apache/airflow` | `code_only` | `python` | Fix typo in dbt cloud hook docstring |
| https://github.com/apache/airflow/pull/70699 | `apache/airflow` | `code_only` | `python` | UI: Preserve Dag tab when switching Dags |
| https://github.com/apache/airflow/pull/71180 | `apache/airflow` | `code_and_docs` | `python` | Document config-backed enum Dag Params |
| https://github.com/apache/airflow/pull/71954 | `apache/airflow` | `code_only` | `python` | Surface connection test errors in the UI instead of failing silently |
| https://github.com/apache/airflow/pull/71517 | `apache/airflow` | `code_only` | `python` | Drop extraneous "common" tag in i18n |
| https://github.com/apache/airflow/pull/71790 | `apache/airflow` | `code_only` | `python` | [v3-3-test] Complete French UI translations (#71666) |
| https://github.com/apache/airflow/pull/71857 | `apache/airflow` | `code_only` | `python` | Use the operator's AWS settings for deferred SageMaker tasks |
| https://github.com/apache/airflow/pull/71789 | `apache/airflow` | `code_only` | `python` | [v3-3-test] Improve-arabic-translations (#71519) |
| https://github.com/apache/airflow/pull/71951 | `apache/airflow` | `code_only` | `python` | [v3-3-test] Make GridButton tooltip label timezone aware (#71944) |
| https://github.com/apache/airflow/pull/68795 | `apache/airflow` | `code_only` | `python` | Fix nested non-Dag with-statement exiting the Dag context in version inflation checker |
| https://github.com/apache/airflow/pull/71488 | `apache/airflow` | `code_only` | `python` | Reuse the ambient session when skipping pending TIs in dag-run terminal state |
| https://github.com/apache/airflow/pull/71943 | `apache/airflow` | `code_only` | `python` | Prevent React plugins from inheriting a prior bundle's component |
| https://github.com/apache/airflow/pull/71780 | `apache/airflow` | `code_only` | `python` | Show the JSON parse-error message on the Variable form warning |
| https://github.com/apache/airflow/pull/71803 | `apache/airflow` | `code_only` | `python` | UI: Allow file downloads from plugin external view iframes |
| https://github.com/apache/airflow/pull/71944 | `apache/airflow` | `code_only` | `python` | Make GridButton tooltip label use the selected UI timezone |
| https://github.com/apache/airflow/pull/71849 | `apache/airflow` | `code_only` | `python` | Remove utkarsharma2 from allowed publish provider docs to S3 |
| https://github.com/apache/airflow/pull/71866 | `apache/airflow` | `code_only` | `python` | Keep MSGraph path parameters across paginated pages |
| https://github.com/apache/airflow/pull/71935 | `apache/airflow` | `code_only` | `python` | [v3-3-test] Show assets materialized from an AssetAlias in the Assets tab |
| https://github.com/apache/airflow/pull/71924 | `apache/airflow` | `code_and_docs` | `python` | [main] Upgrade important CI environment |
| https://github.com/apache/airflow/pull/71912 | `apache/airflow` | `code_only` | `python` | Clarify Breeze CI image build helper names |
| https://github.com/apache/airflow/pull/71917 | `apache/airflow` | `code_only` | `python` | Reduce memory used when deleting queued asset events |
| https://github.com/apache/airflow/pull/71889 | `apache/airflow` | `code_only` | `python` | [v3-3-test] Reduce memory used when deleting a Dag with a large history (#71185) |
| https://github.com/apache/airflow/pull/71878 | `apache/airflow` | `code_and_docs` | `python` | Publish standalone Apache Airflow Mypy documentation |
| https://github.com/apache/airflow/pull/71643 | `apache/airflow` | `code_only_tests_or_fixtures` | `python` | Collect the test classes pytest silently skipped |
| https://github.com/apache/airflow/pull/71815 | `apache/airflow` | `code_only` | `python` | Report Dag cache metrics under each component's own namespace |
| https://github.com/apache/airflow/pull/71057 | `apache/airflow` | `code_and_docs` | `python` | Java SDK: Register tasks as first-class TaskDef objects |
| https://github.com/apache/airflow/pull/71826 | `apache/airflow` | `code_only` | `python` | Fix reversed credential precedence in Bedrock hook docstring |
| https://github.com/apache/airflow/pull/71712 | `apache/airflow` | `code_only` | `python` | Ignore shadow-gradle-plugin and jsonschema2pojo bumps |
| https://github.com/apache/airflow/pull/69125 | `apache/airflow` | `code_only` | `python` | Harden frame processing on large data |
| https://github.com/apache/airflow/pull/64751 | `apache/airflow` | `code_and_docs` | `python` | Deadline Alerts: Add dynamic interval resolution support via Variables |
| https://github.com/apache/airflow/pull/71888 | `apache/airflow` | `code_only` | `python` | [chart/v1-2x-test] Add match schema update prek hook for Helm `values_schema.schema.json` file (#71680) |
| https://github.com/apache/airflow/pull/71185 | `apache/airflow` | `code_only` | `python` | Reduce memory used when deleting a Dag with a large history |
| https://github.com/apache/airflow/pull/71910 | `apache/airflow` | `code_and_docs` | `python` | [v3-3-test] Reuse CI image built from the same sources in another checkout (#71886) |
| https://github.com/apache/airflow/pull/71705 | `apache/airflow` | `code_only` | `python` | Fix InfluxDB hook methods failing when called before get_conn |
| https://github.com/apache/airflow/pull/71902 | `apache/airflow` | `code_only` | `python` | Bump the edge-ui-package-updates group across 1 directory with 5 updates |
| https://github.com/apache/airflow/pull/71901 | `apache/airflow` | `code_only` | `python` | Bump the 3-3-edge-ui-package-updates group across 1 directory with 5 updates |
| https://github.com/apache/airflow/pull/71896 | `apache/airflow` | `code_only` | `python` | Bump the auth-ui-package-updates group across 1 directory with 4 updates |
| https://github.com/apache/airflow/pull/71680 | `apache/airflow` | `code_only` | `python` | Add match schema update prek hook for Helm `values_schema.schema.json` file |
| https://github.com/apache/airflow/pull/71904 | `apache/airflow` | `code_only` | `python` | [v3-3-test] Fix Variable.set rewriting team_name of existing variables (#71823) |
| https://github.com/apache/airflow/pull/71894 | `apache/airflow` | `code_only` | `python` | Bump the 3-3-auth-ui-package-updates group across 1 directory with 4 updates |
| https://github.com/apache/airflow/pull/69400 | `apache/airflow` | `code_only` | `python` | Validate Dag and task IDs in the ts-sdk task registry |
| https://github.com/apache/airflow/pull/71886 | `apache/airflow` | `code_and_docs` | `python` | Avoid force CI image rebuild in another worktree when same image exists |
| https://github.com/apache/airflow/pull/71823 | `apache/airflow` | `code_only` | `python` | Fix Variable.set rewriting team_name of existing variables |
| https://github.com/apache/airflow/pull/71784 | `apache/airflow` | `code_only` | `python` | Fail loudly when a UI dev server dies in breeze dev mode |
| https://github.com/apache/airflow/pull/70993 | `apache/airflow` | `code_only` | `python` | Warn on suspicious Dag and task IDs at TS SDK build time |
| https://github.com/apache/airflow/pull/71555 | `apache/airflow` | `code_only` | `python` | Show assets materialized from an AssetAlias in the Assets tab |
| https://github.com/apache/airflow/pull/71876 | `apache/airflow` | `code_only` | `python` | [v3-3-test] UI: Show an empty object for object params with no value (#71710) |
| https://github.com/apache/airflow/pull/71668 | `apache/airflow` | `code_only` | `python` | Complete German UI translations |
| https://github.com/apache/airflow/pull/71710 | `apache/airflow` | `code_only` | `python` | UI: Show an empty object for object params with no value |
| https://github.com/apache/airflow/pull/71846 | `apache/airflow` | `code_only` | `python` | [v3-3-test] UI - french-  less literal translation (#71792) |
| https://github.com/apache/airflow/pull/71873 | `apache/airflow` | `code_only` | `python` | [v3-3-test] Drop the stale RFC 9457 TODO on the task-instance-run endpoint (#71552) |
| https://github.com/apache/airflow/pull/71346 | `apache/airflow` | `code_and_docs` | `python` | Add trigger `queue` support for `AsyncCallback` and `BaseEventTrigger` |
| https://github.com/apache/airflow/pull/71860 | `apache/airflow` | `code_only` | `python` | [v3-3-test] Return 404 from task state store endpoints for unknown task instances (#70983) |
| https://github.com/apache/airflow/pull/71833 | `apache/airflow` | `code_and_docs` | `python` | Improve TypeScript SDK API reference navigation |
| https://github.com/apache/airflow/pull/70819 | `apache/airflow` | `code_only` | `python` | Added dompurify override to UI to resolve CVEs |
| https://github.com/apache/airflow/pull/71552 | `apache/airflow` | `code_only` | `python` | Drop the stale RFC 9457 TODO on the task-instance-run endpoint |
| https://github.com/apache/airflow/pull/71720 | `apache/airflow` | `code_only_tests_or_fixtures` | `python` | Pin the statement budget for persisting Dag parse results |
| https://github.com/apache/airflow/pull/71865 | `apache/airflow` | `code_only` | `python` | [v3-3-test] Fix Dag callbacks silently dropped when version inflation check blocks parsing (#70987) |
| https://github.com/apache/airflow/pull/71670 | `apache/airflow` | `code_only` | `python` | Bump Java SDK dependencies with Java 11 compatibility |
| https://github.com/apache/airflow/pull/70987 | `apache/airflow` | `code_only` | `python` | Fix Dag callbacks silently dropped when version inflation check blocks parsing |
| https://github.com/apache/airflow/pull/71151 | `apache/airflow` | `code_and_docs` | `python` | Add Java SDK capability manifest and compatibility matrix |
| https://github.com/apache/airflow/pull/71822 | `apache/airflow` | `code_and_docs` | `python` | Prepare TypeScript SDK 0.1.0-beta1 |
| https://github.com/apache/airflow/pull/70657 | `apache/airflow` | `code_and_docs` | `python` | Split task execution architecture docs: concise overview + dev guide |
| https://github.com/apache/airflow/pull/70430 | `apache/airflow` | `code_only` | `python` | Fail deferred Cloud Composer tasks when the GCP operation errors |
| https://github.com/apache/airflow/pull/71649 | `apache/airflow` | `code_only` | `python` | Keep MSGraph request configuration across paginated pages |
| https://github.com/apache/airflow/pull/71646 | `apache/airflow` | `code_only` | `python` | Use the configured region for deferred Neptune cluster tasks |
| https://github.com/apache/airflow/pull/71825 | `apache/airflow` | `code_only_tests_or_fixtures` | `python` | Fix flaky Iceberg snapshot trigger tests under CI thread-pool latency |
| https://github.com/apache/airflow/pull/71805 | `apache/airflow` | `code_only_tests_or_fixtures` | `python` | Test team scoping of plugin UI views in multi-team mode |
| https://github.com/apache/airflow/pull/71792 | `apache/airflow` | `code_only` | `python` | UI - french-  less literal translation of keywords |
| https://github.com/apache/airflow/pull/71848 | `apache/airflow` | `code_only` | `python` | Allow Hussein Awala to publish provider docs to S3 |
| https://github.com/apache/airflow/pull/71839 | `apache/airflow` | `code_only` | `python` | Auto-skip dev-only tooling changes and release-preparation commits in provider documentation prep |
| https://github.com/apache/airflow/pull/71446 | `apache/airflow` | `code_only` | `python` | UI: Show owning team in asset dependency popovers |
| https://github.com/apache/airflow/pull/71814 | `apache/airflow` | `code_and_docs` | `python` | Honor the API server Dag cache TTL when no size limit is set |
| https://github.com/apache/airflow/pull/71788 | `apache/airflow` | `code_only` | `python` | [v3-3-test] Fix datetime pickers unusable on Firefox and Safari (#71627) |
| https://github.com/apache/airflow/pull/71304 | `apache/airflow` | `code_only` | `python` | Allow skipping the git fetch when preparing provider distributions |
| https://github.com/apache/airflow/pull/71709 | `apache/airflow` | `code_only` | `python` | Stop sending GitHub Actions job notifications to the jobs mailing list |
| https://github.com/apache/airflow/pull/71834 | `apache/airflow` | `code_only` | `python` | Clarify prompt for doc-only provider changes during release prep |
| https://github.com/apache/airflow/pull/70886 | `apache/airflow` | `code_and_docs` | `python` | Require team names to be lower case with no doubled underscores |
| https://github.com/apache/airflow/pull/71838 | `apache/airflow` | `code_only` | `python` | [v3-3-test] Regenerate API datamodels after the CI environment lock u… |
| https://github.com/apache/airflow/pull/66751 | `apache/airflow` | `code_only` | `python` | Use parameterized queries in HiveStatsCollectionOperator |
| https://github.com/apache/airflow/pull/71764 | `apache/airflow` | `code_only` | `python` | [v3-3-test] Stop dag processor from warning on every file path normalized for stats (#71091) |
| https://github.com/apache/airflow/pull/71718 | `apache/airflow` | `code_only` | `python` | Regenerate API datamodels after the CI environment lock upgrade |
| https://github.com/apache/airflow/pull/70623 | `apache/airflow` | `code_only` | `python` | Pin apache/infrastructure-actions to its released tags |
| https://github.com/apache/airflow/pull/71828 | `apache/airflow` | `code_and_docs` | `python` | [v3-3-test] Require Dag edit to delete asset queued events (#71736) |
| https://github.com/apache/airflow/pull/71736 | `apache/airflow` | `code_and_docs` | `python` | Require Dag edit to delete asset queued events |
| https://github.com/apache/airflow/pull/71238 | `apache/airflow` | `code_only_tests_or_fixtures` | `python` | Vertex ai/feature store dag system test |
| https://github.com/apache/airflow/pull/71821 | `apache/airflow` | `code_and_docs` | `python` | [v3-3-test] Bound the scheduler's deserialized Dag cache (#71704) |
| https://github.com/apache/airflow/pull/71704 | `apache/airflow` | `code_and_docs` | `python` | Fix scheduler DBDagBag unbounded cache |
| https://github.com/apache/airflow/pull/71144 | `apache/airflow` | `code_and_docs` | `python` | TS SDK: replace registerTask with Dag and registerDags |
| https://github.com/apache/airflow/pull/71787 | `apache/airflow` | `code_only` | `python` | [chart/v1-2x-test] Add terminationGracePeriodSeconds support for PgBouncer in Helm chart (#71237) |
| https://github.com/apache/airflow/pull/69148 | `apache/airflow` | `code_and_docs` | `python` | UI: Allow scoping plugin tabs to specific Dags and tasks |
| https://github.com/apache/airflow/pull/71741 | `apache/airflow` | `code_only` | `python` | Scope /assets/events to the Dags the caller may read |
| https://github.com/apache/airflow/pull/70835 | `apache/airflow` | `code_only` | `python` | Prepare Cloud Batch jobs before template rendering |
| https://github.com/apache/airflow/pull/70001 | `apache/airflow` | `code_only` | `python` | Support sovereign console links |
| https://github.com/apache/airflow/pull/71529 | `apache/airflow` | `code_only` | `python` | Keep the MeterProvider configured via OTEL_CONFIG_FILE |
| https://github.com/apache/airflow/pull/71785 | `apache/airflow` | `code_only` | `python` | [v3-3-test] Scope /assets/events to the Dags the caller may read (#71741) |
| https://github.com/apache/airflow/pull/70979 | `apache/airflow` | `code_only` | `python` | Stop airflow config update from writing a backup during dry-run |
| https://github.com/apache/airflow/pull/70944 | `apache/airflow` | `code_only` | `python` | Stop variables export/import from silently corrupting values |
| https://github.com/apache/airflow/pull/71379 | `apache/airflow` | `code_only` | `python` | API: Return asset events for Dag Runs without a start date |
| https://github.com/apache/airflow/pull/71746 | `apache/airflow` | `code_only` | `python` | Build pgbouncer-exporter image from a pinned commit rather than a tag |
| https://github.com/apache/airflow/pull/71237 | `apache/airflow` | `code_only` | `python` | Add terminationGracePeriodSeconds support for PgBouncer in Helm chart |
| https://github.com/apache/airflow/pull/71666 | `apache/airflow` | `code_only` | `python` | Complete French UI translations |
| https://github.com/apache/airflow/pull/71519 | `apache/airflow` | `code_only` | `python` | Improve-arabic-translations |
| https://github.com/apache/airflow/pull/71762 | `apache/airflow` | `code_only` | `python` | UI: Avoid 404 links for tasks outside run dates |
| https://github.com/apache/airflow/pull/71627 | `apache/airflow` | `code_only` | `python` | Fix datetime pickers unusable on Firefox and Safari |
| https://github.com/apache/airflow/pull/71755 | `apache/airflow` | `code_only` | `python` | [v3-3-test] Increase padding bottom to make last section clickable. (#71679) |
| https://github.com/apache/airflow/pull/71735 | `apache/airflow` | `code_only` | `python` | Validate issuer and audience of Azure AD id_tokens in FAB auth manager |
| https://github.com/apache/airflow/pull/71781 | `apache/airflow` | `code_only` | `python` | [v3-3-test] Serve logs from scheduler if any executor is LocalExecutor (#71283) |
| https://github.com/apache/airflow/pull/71283 | `apache/airflow` | `code_only` | `python` | Serve logs from scheduler if any executor is LocalExecutor |
| https://github.com/apache/airflow/pull/71722 | `apache/airflow` | `code_only` | `python` | Improve DAG authorization filtering performance |
| https://github.com/apache/airflow/pull/71760 | `apache/airflow` | `code_only` | `python` | i18n(Ko): add missing translations in assets.json (Aug 18) |
| https://github.com/apache/airflow/pull/71696 | `apache/airflow` | `code_and_docs` | `python` | Fix cleared tasks getting stuck when a Dag run has no version |
| https://github.com/apache/airflow/pull/71740 | `apache/airflow` | `code_only` | `python` | Fix incorrect documented defaults for MwaaTriggerDagRunOperator waiter params |
| https://github.com/apache/airflow/pull/71745 | `apache/airflow` | `code_only_tests_or_fixtures` | `python` | Probe AOSS index readiness as the Knowledge Base role in Bedrock RAG system test |
| https://github.com/apache/airflow/pull/71071 | `apache/airflow` | `code_and_docs` | `python` | Azure batch 15x migration |
| https://github.com/apache/airflow/pull/71091 | `apache/airflow` | `code_only` | `python` | Stop dag processor from warning on every file path normalized for stats |
| https://github.com/apache/airflow/pull/71679 | `apache/airflow` | `code_only` | `python` | Add padding bottom to log content to make last section header clickable. |
| https://github.com/apache/airflow/pull/71534 | `apache/airflow` | `code_and_docs` | `python` | Make SparkSubmitOperator durable execution inert below Airflow 3.3 |
| https://github.com/apache/airflow/pull/71701 | `apache/airflow` | `code_only` | `python` | Halve external vault API lookup requests per airflow secret lookup |
| https://github.com/apache/airflow/pull/70088 | `apache/airflow` | `code_and_docs` | `python` | Add Databricks SQL warehouse lifecycle operators |
| https://github.com/apache/airflow/pull/71380 | `apache/airflow` | `code_only` | `python` | Prevent a broken job from stalling AWS Batch executor sync |
| https://github.com/apache/airflow/pull/70148 | `apache/airflow` | `code_only` | `python` |  allow deadline alert UUID references in serialized Dag schema |
| https://github.com/apache/airflow/pull/71733 | `apache/airflow` | `code_only_tests_or_fixtures` | `python` | Make DMS system-test databases non-public |
| https://github.com/apache/airflow/pull/71387 | `apache/airflow` | `code_only` | `python` | Add IcebergTableSnapshotTrigger for event-driven scheduling |
| https://github.com/apache/airflow/pull/71714 | `apache/airflow` | `code_and_docs` | `python` | [v3-3-test] Keep ZIP-archived Dags active when dag_discovery_safe_mode is False (#68518) |
| https://github.com/apache/airflow/pull/71715 | `apache/airflow` | `code_only` | `python` | [v3-3-test] Dispatch the highest priority tasks first in the executor (#70942) |
| https://github.com/apache/airflow/pull/71726 | `apache/airflow` | `code_only` | `python` | [v3-3-test] Fix deadline serialization, repr, and prune edge cases (#70421) |
| https://github.com/apache/airflow/pull/71708 | `apache/airflow` | `code_and_docs` | `python` | [v3-3-test] Honor FORWARDED_ALLOW_IPS when the API server runs under gunicorn (#71429) |
| https://github.com/vercel/next.js/pull/97825 | `vercel/next.js` | `code_and_docs` | `typescript` | Fix Turbopack resolution through chained symlinks |
| https://github.com/vercel/next.js/pull/97816 | `vercel/next.js` | `code_and_docs` | `typescript` | Add evals for whether agents actually use Next.js |
| https://github.com/vercel/next.js/pull/97826 | `vercel/next.js` | `code_only` | `typescript` | evals: judge behavior instead of matching source text |
| https://github.com/vercel/next.js/pull/97885 | `vercel/next.js` | `code_only` | `typescript` | Bump @vercel/agent-eval to 2.2.1 |
| https://github.com/vercel/next.js/pull/97799 | `vercel/next.js` | `code_only` | `typescript` | feat(turbopack): resolve `/`-rooted imports from the project directory |
| https://github.com/vercel/next.js/pull/97256 | `vercel/next.js` | `code_only` | `typescript` | [ci] Use short-lived access tokens for preview-build uploads instead of static token |
| https://github.com/vercel/next.js/pull/97697 | `vercel/next.js` | `code_only` | `typescript` | Turbopack: correctly trace through TypeScript `__importStar` |
| https://github.com/vercel/next.js/pull/97771 | `vercel/next.js` | `code_only` | `typescript` | [turbopack] simplify ecmascript effect queue |
| https://github.com/vercel/next.js/pull/97876 | `vercel/next.js` | `code_only` | `typescript` | Fix ISR misses with backslashes in segments when deployed on Windows |
| https://github.com/vercel/next.js/pull/97875 | `vercel/next.js` | `code_only` | `typescript` | [next/image]: disable avif image optimization |
| https://github.com/vercel/next.js/pull/97859 | `vercel/next.js` | `code_only` | `typescript` | fix(wasm): don't enable SWC's plugin host for wasm targets |
| https://github.com/vercel/next.js/pull/97858 | `vercel/next.js` | `code_only` | `typescript` | fix(turbopack-node): make process_pool inert on wasm |
| https://github.com/vercel/next.js/pull/97857 | `vercel/next.js` | `code_only` | `typescript` | fix(turbopack): make the SWC wasm-plugin backend native-only |
| https://github.com/vercel/next.js/pull/97856 | `vercel/next.js` | `code_only` | `typescript` | fix(turbopack-trace-utils): skip the ctrl-c handler on wasm |
| https://github.com/vercel/next.js/pull/97855 | `vercel/next.js` | `code_only` | `typescript` | refactor(turbopack-cli-utils): replace crossterm with owo-colors |
| https://github.com/vercel/next.js/pull/97854 | `vercel/next.js` | `code_only` | `typescript` | fix(turbo-tasks-fs): create symlinks through the WASI API on wasi |
| https://github.com/vercel/next.js/pull/97579 | `vercel/next.js` | `code_only` | `typescript` | fix(turbo-tasks): compile EventListener::wait on wasm |
| https://github.com/vercel/next.js/pull/97853 | `vercel/next.js` | `code_only` | `typescript` | fix(turbo-tasks): compile EventListener::wait on wasm |
| https://github.com/vercel/next.js/pull/97852 | `vercel/next.js` | `code_only` | `typescript` | fix(turbo-rcstr): allow the napi feature on wasm targets |
| https://github.com/vercel/next.js/pull/97576 | `vercel/next.js` | `code_only` | `typescript` | fix(next-napi-bindings): detect the target, not the host, in build.rs |
| https://github.com/vercel/next.js/pull/97829 | `vercel/next.js` | `code_only` | `typescript` | Stop printing a stack frame for error message text |
| https://github.com/vercel/next.js/pull/97563 | `vercel/next.js` | `code_and_docs` | `typescript` | Add deploy release test skill |
| https://github.com/vercel/next.js/pull/97848 | `vercel/next.js` | `code_only_tests_or_fixtures` | `typescript` | [test] Deflake the page config test for a string config value |
| https://github.com/vercel/next.js/pull/97584 | `vercel/next.js` | `code_only` | `typescript` | fix(turbopack-node): make process_pool inert on wasm |
| https://github.com/vercel/next.js/pull/97582 | `vercel/next.js` | `code_only` | `typescript` | fix(turbopack-trace-utils): skip the ctrl-c handler on wasm |
| https://github.com/vercel/next.js/pull/97581 | `vercel/next.js` | `code_only` | `typescript` | refactor(turbopack-cli-utils): replace crossterm with owo-colors |
| https://github.com/vercel/next.js/pull/97580 | `vercel/next.js` | `code_only` | `typescript` | fix(turbo-tasks-fs): create symlinks through the WASI API on wasi |
| https://github.com/vercel/next.js/pull/97583 | `vercel/next.js` | `code_only` | `typescript` | fix(turbopack): make the SWC wasm-plugin backend native-only |
| https://github.com/vercel/next.js/pull/96808 | `vercel/next.js` | `code_only` | `typescript` | turbo-tasks: execute scheduled tasks inline when they are read |
| https://github.com/vercel/next.js/pull/97674 | `vercel/next.js` | `code_only_tests_or_fixtures` | `typescript` | test: stabilize read-only page recreation |
| https://github.com/vercel/next.js/pull/97830 | `vercel/next.js` | `code_only` | `typescript` | Show the errors of an AggregateError behind a cause |
| https://github.com/vercel/next.js/pull/97698 | `vercel/next.js` | `code_only` | `typescript` | fix: reuse a single drain listener when piping Node streams through gzip |
| https://github.com/vercel/next.js/pull/97724 | `vercel/next.js` | `code_only_tests_or_fixtures` | `typescript` | test: preserve server cache after compile error |
| https://github.com/vercel/next.js/pull/97835 | `vercel/next.js` | `code_only` | `typescript` | Revert "Record fallback cache lifetime for blocking PPR routes (#97821)" |
| https://github.com/vercel/next.js/pull/97591 | `vercel/next.js` | `code_only` | `typescript` | Sweep stale Turbopack output from distDir on dev startup |
| https://github.com/vercel/next.js/pull/97729 | `vercel/next.js` | `code_only` | `typescript` | Fix metadata prefetch cache key for search params |
| https://github.com/vercel/next.js/pull/97717 | `vercel/next.js` | `code_and_docs` | `typescript` | Turbopack: Improve file existence error handling in realpath_with_links and in module resolution |
| https://github.com/vercel/next.js/pull/97592 | `vercel/next.js` | `code_and_docs` | `typescript` | Add next/cache-handlers types entrypoint |
| https://github.com/vercel/next.js/pull/97395 | `vercel/next.js` | `code_only` | `typescript` | Turbopack: Split the read and write codepath data structures for symlinks |
| https://github.com/vercel/next.js/pull/96874 | `vercel/next.js` | `code_only` | `typescript` | Write traces with buffered synchronous IO |
| https://github.com/vercel/next.js/pull/97821 | `vercel/next.js` | `code_only` | `typescript` | Record fallback cache lifetime for blocking PPR routes |
| https://github.com/vercel/next.js/pull/96410 | `vercel/next.js` | `code_only` | `typescript` | clippy: allow needless late init where it makes sense |
| https://github.com/vercel/next.js/pull/97774 | `vercel/next.js` | `code_only` | `typescript` | Turn off the adapter route collapses by default |
| https://github.com/vercel/next.js/pull/97783 | `vercel/next.js` | `code_only` | `typescript` | [15.5.x] Remove generated error codes |
| https://github.com/vercel/next.js/pull/97762 | `vercel/next.js` | `code_only` | `typescript` | Deduplicate the regress, wat/wasmparser and base64 dependencies |
| https://github.com/vercel/next.js/pull/97780 | `vercel/next.js` | `code_and_docs` | `typescript` | [16.3.x] Stop generating error codes |
| https://github.com/vercel/next.js/pull/97726 | `vercel/next.js` | `code_only` | `typescript` | Stop emitting a separate route entry for a dynamic route's RSC form |
| https://github.com/vercel/next.js/pull/97767 | `vercel/next.js` | `code_only` | `typescript` | perf: split cold TurboMalloc accounting paths |
| https://github.com/vercel/next.js/pull/97661 | `vercel/next.js` | `code_only` | `typescript` | Remove unused return values from getPageStaticInfo |
| https://github.com/vercel/next.js/pull/97773 | `vercel/next.js` | `code_only` | `typescript` | [turbopack] defer NFT module content hashes |
| https://github.com/vercel/next.js/pull/97611 | `vercel/next.js` | `code_only_tests_or_fixtures` | `typescript` | test: deflake basePath external navigation |
| https://github.com/vercel/next.js/pull/97701 | `vercel/next.js` | `code_only` | `typescript` | Migrate remaining async blocks to async closures |
| https://github.com/vercel/next.js/pull/97738 | `vercel/next.js` | `code_only` | `typescript` | Serve a run of fallback shells from one route entry |
| https://github.com/vercel/next.js/pull/97728 | `vercel/next.js` | `code_only_tests_or_fixtures` | `typescript` | [test] Capture the route table for apps with several param shapes |
| https://github.com/vercel/next.js/pull/97720 | `vercel/next.js` | `code_only` | `typescript` | Stop emitting a redundant route per prefetch segment |
| https://github.com/vercel/next.js/pull/97719 | `vercel/next.js` | `code_only_tests_or_fixtures` | `typescript` | [test] Capture the dynamic routes a build passes to an adapter |
| https://github.com/vercel/next.js/pull/97763 | `vercel/next.js` | `code_only` | `typescript` | turbo-tasks: compile conditional cell updates once, not per cell type |
| https://github.com/vercel/next.js/pull/97743 | `vercel/next.js` | `code_only` | `typescript` | Turbopack: add unit test coverage for FileSystemPath::hash_file |
| https://github.com/vercel/next.js/pull/97723 | `vercel/next.js` | `code_only` | `typescript` | [devtools] Fix indicator dragging on touch screens |
| https://github.com/vercel/next.js/pull/97284 | `vercel/next.js` | `code_only` | `typescript` | introduce an options struct for constructing backend storage |
| https://github.com/vercel/next.js/pull/97655 | `vercel/next.js` | `code_only` | `typescript` | Turbopack: Avoid cloning paths in fs watcher if the path is already in a map |
| https://github.com/vercel/next.js/pull/97309 | `vercel/next.js` | `code_only` | `typescript` | [PPF] Instant validation for unstable_navigation() |
| https://github.com/vercel/next.js/pull/97694 | `vercel/next.js` | `code_only` | `typescript` | Turbopack: trace graceful-fs calls |
| https://github.com/vercel/next.js/pull/95974 | `vercel/next.js` | `code_only` | `typescript` | turbo-tasks: add scope_unbounded, a scoped execution primitive that allows more work to be discovered |
| https://github.com/vercel/next.js/pull/97682 | `vercel/next.js` | `code_only_tests_or_fixtures` | `typescript` | test: make app-document-import-order more robust |
| https://github.com/vercel/next.js/pull/96525 | `vercel/next.js` | `code_only` | `typescript` | [testmode] Fix infinite recursion in testmode passthrough fetch |
| https://github.com/vercel/next.js/pull/97639 | `vercel/next.js` | `code_only` | `typescript` | Add a Turbopack error for missing root layouts |
| https://github.com/vercel/next.js/pull/97609 | `vercel/next.js` | `code_only_tests_or_fixtures` | `typescript` | test: stabilize poisoned proxy error overlay |
| https://github.com/vercel/next.js/pull/97622 | `vercel/next.js` | `code_only` | `typescript` | [PPF] unstable_prefetch() |
| https://github.com/vercel/next.js/pull/97618 | `vercel/next.js` | `code_only` | `typescript` | [PPF] Scaffold unstable_prefetch() |
| https://github.com/vercel/next.js/pull/96559 | `vercel/next.js` | `code_only` | `typescript` | fix(turbopack): give eager `import.meta.glob` values the ESM namespace |
| https://github.com/vercel/next.js/pull/95997 | `vercel/next.js` | `code_only` | `typescript` | feat(turbopack): isolate HMR listeners across microfrontends |
| https://github.com/vercel/next.js/pull/97664 | `vercel/next.js` | `code_only` | `typescript` | Turbopack: deduplicate Pages Router app chunks |
| https://github.com/vercel/next.js/pull/97638 | `vercel/next.js` | `code_only` | `typescript` | [react-sync] Check assignability before assigning the actor |
| https://github.com/vercel/next.js/pull/97613 | `vercel/next.js` | `code_only` | `typescript` | fix: preserve trailing slash during export MPA fallback |
| https://github.com/vercel/next.js/pull/97648 | `vercel/next.js` | `code_only` | `typescript` | Turbopack: Show last modified file when waiting for the filesystem to settle |
| https://github.com/vercel/next.js/pull/97603 | `vercel/next.js` | `code_only` | `typescript` | [16.3.x] Authenticate Turborepo remote caching with OIDC instead of a static PAT |
| https://github.com/vercel/next.js/pull/97604 | `vercel/next.js` | `code_only` | `typescript` | [15.5.x] Authenticate Turborepo remote caching with OIDC instead of a static PAT |
| https://github.com/vercel/next.js/pull/94427 | `vercel/next.js` | `code_only` | `typescript` | Turbopack: rename to use turbopack: no side effects |
| https://github.com/vercel/next.js/pull/96908 | `vercel/next.js` | `code_only` | `typescript` | [PPF] unstable_navigation() |
| https://github.com/vercel/next.js/pull/97360 | `vercel/next.js` | `code_only` | `typescript` | refactor: move useDynamic{Route,Search}Params to reduce snapshot churn |
| https://github.com/vercel/next.js/pull/97236 | `vercel/next.js` | `code_only` | `typescript` | [PPF] Scaffold unstable_navigation() |
| https://github.com/vercel/next.js/pull/97614 | `vercel/next.js` | `code_only_tests_or_fixtures` | `typescript` | [test] Use a non-native stub for the server externals list test |
| https://github.com/vercel/next.js/pull/97612 | `vercel/next.js` | `code_only` | `typescript` | Avoid GitHub API rate limits for create-next-app examples |
| https://github.com/vercel/next.js/pull/97543 | `vercel/next.js` | `code_only` | `typescript` | [test] Cover the prerender worker-thread backend with an addon we control |
| https://github.com/vercel/next.js/pull/97542 | `vercel/next.js` | `code_only` | `typescript` | [test] Convert the `prerender-native-module` suite to local fixture packages |
| https://github.com/vercel/next.js/pull/97541 | `vercel/next.js` | `code_only` | `typescript` | [test] Replace the `turbopack-reports` `sqlite3` dependency with a local addon fixture |
| https://github.com/vercel/next.js/pull/97540 | `vercel/next.js` | `code_only_tests_or_fixtures` | `typescript` | [test] Drop the dead `sqlite3` build approval from the `sharp-basic` suite |
| https://github.com/vercel/next.js/pull/97590 | `vercel/next.js` | `code_only` | `typescript` | [ci] Authenticate Turborepo remote caching with OIDC instead of a static PAT |
| https://github.com/vercel/next.js/pull/97419 | `vercel/next.js` | `code_only` | `typescript` | [16.3.x] Fix Turbopack worker chunk loading with asset prefix |
| https://github.com/vercel/next.js/pull/96686 | `vercel/next.js` | `code_only` | `typescript` | Serialize frozen collections by value only |
| https://github.com/vercel/next.js/pull/97253 | `vercel/next.js` | `code_only` | `typescript` | Remove HmrTarget |
| https://github.com/vercel/next.js/pull/96569 | `vercel/next.js` | `code_only` | `typescript` | Keep HMR instructions typed until serialization |
| https://github.com/vercel/next.js/pull/97524 | `vercel/next.js` | `code_and_docs` | `typescript` | [PPF] Remove `unstable_eager` |
| https://github.com/vercel/next.js/pull/97503 | `vercel/next.js` | `code_only` | `typescript` | [PPF] Do not mark complete shell requests as partial |
| https://github.com/vercel/next.js/pull/96334 | `vercel/next.js` | `code_only` | `typescript` | fix: add accessible label to icon-only link |
| https://github.com/vercel/next.js/pull/97453 | `vercel/next.js` | `code_only` | `typescript` | [16.3] Turbopack: retain conditions when replacing resolve request keys |
| https://github.com/vercel/next.js/pull/96004 | `vercel/next.js` | `code_only` | `typescript` | Move preview props into separate manifest |
| https://github.com/vercel/next.js/pull/97515 | `vercel/next.js` | `code_only` | `typescript` | Turbopack: allow TURBOPACK_PRINT_CHUNK_GROUPS in release builds |
| https://github.com/vercel/next.js/pull/97545 | `vercel/next.js` | `code_only_tests_or_fixtures` | `typescript` | [test] Point next-image-legacy images at a reachable endpoint |
| https://github.com/vercel/next.js/pull/97553 | `vercel/next.js` | `code_only_tests_or_fixtures` | `typescript` | test: improve error-on-next-codemod-comment flakiness |
| https://github.com/vercel/next.js/pull/97546 | `vercel/next.js` | `code_only_tests_or_fixtures` | `typescript` | test: better isolate concurrent-install suite |
| https://github.com/vercel/next.js/pull/97502 | `vercel/next.js` | `code_only` | `typescript` | Turbopack: support character class ranges in regex |
| https://github.com/vercel/next.js/pull/97476 | `vercel/next.js` | `code_only` | `typescript` | Fix use cache prerender signal retention |
| https://github.com/vercel/next.js/pull/94863 | `vercel/next.js` | `code_only` | `typescript` | fix: preserve repeated search params in client page segment cache keys |
| https://github.com/vercel/next.js/pull/96116 | `vercel/next.js` | `code_only` | `typescript` | Turbopack: More aggressively debounce filesystem watch events if we detected changes to node_modules |
| https://github.com/vercel/next.js/pull/97222 | `vercel/next.js` | `code_only` | `typescript` | style(examples): remove redundant justify-content declaration |
| https://github.com/vercel/next.js/pull/96335 | `vercel/next.js` | `code_only` | `typescript` | fix: improve form accessibility by associating labels with inputs |
| https://github.com/vercel/next.js/pull/97223 | `vercel/next.js` | `code_only` | `typescript` | fix(examples): correct error message typo |
| https://github.com/vercel/next.js/pull/95602 | `vercel/next.js` | `code_only` | `typescript` | [fragment-scroll] Remove `config.experimental.appNewScrollHandler` |
| https://github.com/vercel/next.js/pull/97431 | `vercel/next.js` | `code_only` | `typescript` | Model prerenders as render candidates |
| https://github.com/vercel/next.js/pull/97510 | `vercel/next.js` | `code_only` | `typescript` | Remove the development debug channel persistence |
| https://github.com/vercel/next.js/pull/97505 | `vercel/next.js` | `code_only` | `typescript` | Stop the browser from restoring stale pages in development |
| https://github.com/vercel/next.js/pull/97507 | `vercel/next.js` | `code_only` | `typescript` | Turbopack: gracefully handle outputFileTracingIncludes matching a symlink |
| https://github.com/vercel/next.js/pull/97488 | `vercel/next.js` | `code_only_tests_or_fixtures` | `typescript` | test: Don't wait trying to load non-existing images |
| https://github.com/vercel/next.js/pull/97439 | `vercel/next.js` | `code_only` | `typescript` | Trace lazy App Route module loading |
| https://github.com/vercel/next.js/pull/97460 | `vercel/next.js` | `code_only_tests_or_fixtures` | `typescript` | [ci] Wait for the `next` version to be available on npm before deploy tests |
| https://github.com/vercel/next.js/pull/97463 | `vercel/next.js` | `code_only` | `typescript` | [16.3] Turbopack: don't trace embedded WASM loader helpers (#97353) |
| https://github.com/vercel/next.js/pull/97367 | `vercel/next.js` | `code_only_tests_or_fixtures` | `typescript` | test: cover dynamic APIs with i18n base path |
| https://github.com/vercel/next.js/pull/97459 | `vercel/next.js` | `code_only_tests_or_fixtures` | `typescript` | test: restore missing NFT `exports*` unit fixtures |
| https://github.com/vercel/next.js/pull/97288 | `vercel/next.js` | `code_only` | `typescript` | fix(turbo-persistence): allow 32-bit usize conversion |
| https://github.com/vercel/next.js/pull/97383 | `vercel/next.js` | `code_only` | `typescript` | [ci] Fix backport canary release dispatch |
| https://github.com/vercel/next.js/pull/96600 | `vercel/next.js` | `code_only` | `typescript` | [turbopack] Add `turbopack_ecmascript` and `turbopack_wasm`'s embeded FS to `internal_assets_conditions` |
| https://github.com/vercel/next.js/pull/97017 | `vercel/next.js` | `code_only_tests_or_fixtures` | `typescript` | test: re-enable a few more passing NFT unit cases |
| https://github.com/vercel/next.js/pull/97353 | `vercel/next.js` | `code_only` | `typescript` | Turbopack: don't trace embedded WASM loader helpers |
| https://github.com/vercel/next.js/pull/97259 | `vercel/next.js` | `code_only` | `typescript` | [15.5] [ci] Use OIDC tokens to read private preview builds |
| https://github.com/vercel/next.js/pull/96043 | `vercel/next.js` | `code_only` | `typescript` | turbo-tasks-backend: Enforce that tasks exist when accessing them |
| https://github.com/vercel/next.js/pull/95975 | `vercel/next.js` | `code_only` | `typescript` | turbo-tasks-backend: add persistence delete/tombstone plumbing for GC |
| https://github.com/vercel/next.js/pull/96929 | `vercel/next.js` | `code_and_docs` | `typescript` | turbo-persistence: add key-value tombstones for MultiValue families |
| https://github.com/vercel/next.js/pull/97255 | `vercel/next.js` | `code_only` | `typescript` | Anchor the async local storage instances to global symbols |
| https://github.com/vercel/next.js/pull/97421 | `vercel/next.js` | `code_only_tests_or_fixtures` | `typescript` | test: deflake use-cache-size-zero warm reload |
| https://github.com/vercel/next.js/pull/97413 | `vercel/next.js` | `code_only` | `typescript` | Scaffolding for concurrentRouterQueue flag |
| https://github.com/vercel/next.js/pull/97402 | `vercel/next.js` | `code_only` | `typescript` | Reorganize client router modules |
| https://github.com/vercel/next.js/pull/97278 | `vercel/next.js` | `code_only` | `typescript` | fix(next/image): reject empty image on read/write to disk cache  |
| https://github.com/vercel/next.js/pull/97321 | `vercel/next.js` | `code_only_tests_or_fixtures` | `typescript` | Wait for back-before-hydration recoveries in the browser |
| https://github.com/vercel/next.js/pull/97388 | `vercel/next.js` | `code_only` | `typescript` | Extract metadata resolution primitives |
| https://github.com/vercel/next.js/pull/97416 | `vercel/next.js` | `code_only` | `typescript` | [backport] Fix catch-all index page being served for every other slug |
| https://github.com/vercel/next.js/pull/97415 | `vercel/next.js` | `code_only_tests_or_fixtures` | `typescript` | test: update React 18 redbox snapshot |
| https://github.com/vercel/next.js/pull/97372 | `vercel/next.js` | `code_only` | `typescript` | Turbopack: retain conditions when replacing resolve request keys |
| https://github.com/vercel/next.js/pull/97387 | `vercel/next.js` | `code_only` | `typescript` | Adopt SelectedMetadata for metadata rendering |
| https://github.com/vercel/next.js/pull/97333 | `vercel/next.js` | `code_only` | `typescript` | Turbopack: remove stale manifests for deleted routes |
| https://github.com/vercel/next.js/pull/97385 | `vercel/next.js` | `code_only` | `typescript` | Turbopack: make unreachable codegen more generic |
| https://github.com/vercel/next.js/pull/97373 | `vercel/next.js` | `code_only_tests_or_fixtures` | `typescript` | Turbopack: add imports_wildcard NFT unit test |
| https://github.com/vercel/next.js/pull/97370 | `vercel/next.js` | `code_only` | `typescript` | Turbopack: improve chunk_item_content docs |
| https://github.com/vercel/next.js/pull/96898 | `vercel/next.js` | `code_only_tests_or_fixtures` | `typescript` | test: Reenable i18n-api-support deploy test for Turbopack with adapters |
| https://github.com/vercel/next.js/pull/97296 | `vercel/next.js` | `code_only` | `typescript` | Trace instrumentation startup |
| https://github.com/vercel/next.js/pull/97295 | `vercel/next.js` | `code_only` | `typescript` | Trace route module preparation |
| https://github.com/vercel/next.js/pull/97318 | `vercel/next.js` | `code_only` | `typescript` | Trace route module loading |
| https://github.com/vercel/next.js/pull/97287 | `vercel/next.js` | `code_only` | `typescript` | Emit whole-app server NFTs when `output: 'standalone'` is used with an adapter |
| https://github.com/vercel/next.js/pull/97349 | `vercel/next.js` | `code_and_docs` | `typescript` | [test] Cover `'use cache: private'` in route handlers |
| https://github.com/vercel/next.js/pull/96819 | `vercel/next.js` | `code_only` | `typescript` | Fix missing Pages runtime in adapter Pages API outputs |
| https://github.com/vercel/next.js/pull/97342 | `vercel/next.js` | `code_only` | `typescript` | Update blob version. |
| https://github.com/vercel/next.js/pull/96878 | `vercel/next.js` | `code_only` | `typescript` | Unify how a response's shell and full payloads are written |
| https://github.com/vercel/next.js/pull/96877 | `vercel/next.js` | `code_only` | `typescript` | Convert per-segment prefetches to NavigationFlightResponse format |
| https://github.com/vercel/next.js/pull/96876 | `vercel/next.js` | `code_only` | `typescript` | Unify how server responses are written into the client cache |
| https://github.com/vercel/next.js/pull/96788 | `vercel/next.js` | `code_only` | `typescript` | Convert tree prefetches to NavigationFlightResponse format |
| https://github.com/vercel/next.js/pull/97330 | `vercel/next.js` | `code_only` | `typescript` | [backport] Revert i18n localization change for dynamic Pages API routes (#94905) |
| https://github.com/vercel/next.js/pull/97304 | `vercel/next.js` | `code_and_docs` | `typescript` | [backport] Retain fewer stale cache versions and use a TTL, plus the mtime fallback |
| https://github.com/vercel/next.js/pull/97327 | `vercel/next.js` | `code_only` | `typescript` | Revert i18n localization change for dynamic Pages API routes (#94905) |
| https://github.com/vercel/next.js/pull/97325 | `vercel/next.js` | `code_only` | `typescript` | [backport] Fix: Optimistic routing bugs leading to repeated prefetch loops |
| https://github.com/vercel/next.js/pull/97326 | `vercel/next.js` | `code_only` | `typescript` | [backport] Fix Nav Inspector request loop on repeat captures |
| https://github.com/vercel/next.js/pull/97328 | `vercel/next.js` | `code_only_tests_or_fixtures` | `typescript` | [backport] [test] Compile the middleware redirect routes up front in dev |
| https://github.com/vercel/next.js/pull/97258 | `vercel/next.js` | `code_only` | `typescript` | [16.3] [ci] Use OIDC tokens to read private preview builds |
| https://github.com/vercel/next.js/pull/96653 | `vercel/next.js` | `code_only` | `typescript` | [16.x] Turbopack: don't strip async-module runtime from shared runtime chunks |
| https://github.com/vercel/next.js/pull/96675 | `vercel/next.js` | `code_only` | `typescript` | [16.x] [turbopack] Collapse nested promises in the analyzer |
| https://github.com/vercel/next.js/pull/96655 | `vercel/next.js` | `code_only` | `typescript` | [16.x] [turbopack] Add `turbopack_ecmascript` and `turbopack_wasm`'s embeded FS to `internal_assets_conditions` |
| https://github.com/vercel/next.js/pull/96733 | `vercel/next.js` | `code_only` | `typescript` | [16.x] fix(next/image): preserve image response after optimization |
| https://github.com/vercel/next.js/pull/96885 | `vercel/next.js` | `code_only` | `typescript` | [backport] Bump @swc/helpers |
| https://github.com/vercel/next.js/pull/96900 | `vercel/next.js` | `code_only_tests_or_fixtures` | `typescript` | [16.3.x] Default deploy e2e tests to the repo next version |
| https://github.com/vercel/next.js/pull/97302 | `vercel/next.js` | `code_only` | `typescript` | [backport] Fix missing styled-jsx styles in Pages Router SSR on adapter builds |
| https://github.com/vercel/next.js/pull/97308 | `vercel/next.js` | `code_only` | `typescript` | [backport] [turbopack] Raise registration calls in hoisted modules to the top |
| https://github.com/vercel/next.js/pull/97311 | `vercel/next.js` | `code_only` | `typescript` | [backport] Restore the live `headers()` view of the incoming request |
| https://github.com/vercel/next.js/pull/97312 | `vercel/next.js` | `code_only` | `typescript` | [backport] Allow literal exports in `'use cache'` files |
| https://github.com/vercel/next.js/pull/97314 | `vercel/next.js` | `code_only` | `typescript` | [backport] Discard only cache entries that predate a tag revalidation, and reuse completed entries |
| https://github.com/vercel/next.js/pull/97313 | `vercel/next.js` | `code_only` | `typescript` | [backport] Encode the cache item name built by `unstable_cache` |
| https://github.com/vercel/next.js/pull/97315 | `vercel/next.js` | `code_and_docs` | `typescript` | [backport] Keep the dev validation worker alive across HMR updates |
| https://github.com/vercel/next.js/pull/97317 | `vercel/next.js` | `code_only` | `typescript` | [backport] [turbopack] Fix HMR for dynamic imports evaluated from layouts |
| https://github.com/vercel/next.js/pull/94068 | `vercel/next.js` | `code_only` | `typescript` | fix(next/image): skip 0-byte entries when initializing disk LRU cache |
| https://github.com/vercel/next.js/pull/97252 | `vercel/next.js` | `code_and_docs` | `typescript` | Add a script for adopting fork pull requests |
| https://github.com/vercel/next.js/pull/96632 | `vercel/next.js` | `code_only` | `typescript` | Fix missing styled-jsx styles in Pages Router SSR on adapter builds |
| https://github.com/apache/beam/pull/39594 | `apache/beam` | `code_and_docs` | `python` | Adds a new CoderTranslator for Java SchemaCoders. |
| https://github.com/apache/beam/pull/39843 | `apache/beam` | `code_only` | `python` | [Bigtable] Fix Bigtable segment truncation when open end key is startKey + null byte (#39842) |
| https://github.com/apache/beam/pull/39844 | `apache/beam` | `code_only` | `python` | Fix KafkaIO write SchemaTransform parallelism |
| https://github.com/apache/beam/pull/39877 | `apache/beam` | `code_only` | `python` | Revert "Install Cloud Spanner emulator component in Go PreCommit CI" |
| https://github.com/apache/beam/pull/39868 | `apache/beam` | `code_only` | `python` | use LocalStack TLS hostname in Kinesis YAML IT |
| https://github.com/apache/beam/pull/39864 | `apache/beam` | `code_only` | `python` | Bump github/codeql-action from 4.37.7 to 4.37.8 |
| https://github.com/apache/beam/pull/39859 | `apache/beam` | `code_only` | `python` | Bump actions/checkout from 6 to 7 |
| https://github.com/apache/beam/pull/39836 | `apache/beam` | `code_only` | `python` | AddFiles: regenerate name mapping, read footers once, error helper |
| https://github.com/apache/beam/pull/39769 | `apache/beam` | `code_only` | `python` | [GSoC-273] Fix: Remove invalid external ML6 identities to unblock Terraform IAM deployment |
| https://github.com/apache/beam/pull/39794 | `apache/beam` | `code_only_tests_or_fixtures` | `python` | [GSoC-273] Fix Duplicated Subscription Path in stale_cleaner.py |
| https://github.com/apache/beam/pull/39728 | `apache/beam` | `code_only_tests_or_fixtures` | `python` | [GSoC-273] Active cleanup of orphaned subscriptions for the taxirides topic |
| https://github.com/apache/beam/pull/39538 | `apache/beam` | `code_only_tests_or_fixtures` | `python` | [GSoC-273] Feat: new cleaning rule to orphaned subscriptions |
| https://github.com/apache/beam/pull/39116 | `apache/beam` | `code_and_docs` | `python` | [GSoC-273] including GitHub Actions to schedule daily audits and Add documentation. |
| https://github.com/apache/beam/pull/38992 | `apache/beam` | `code_only` | `python` | [GSOC-273] Add logic to validate and generate an error if there are unmanaged keys. |
| https://github.com/apache/beam/pull/39853 | `apache/beam` | `code_and_docs` | `python` | Revert "[GSoC-273] Feat: Integrate TestPubsubContext to prevent Pub/Sub resource leaks and expand stale cleaner scope" |
| https://github.com/apache/beam/pull/39854 | `apache/beam` | `code_only` | `python` | [GSoC 2026] Publish the Kafka Streams runner to nightly snapshots |
| https://github.com/apache/beam/pull/39826 | `apache/beam` | `code_and_docs` | `python` | [GSoC-273] Feat: Integrate TestPubsubContext to prevent Pub/Sub resource leaks and expand stale cleaner scope |
| https://github.com/apache/beam/pull/39850 | `apache/beam` | `code_only` | `python` | Install Cloud Spanner emulator component in Go PreCommit CI |
| https://github.com/apache/beam/pull/39847 | `apache/beam` | `code_and_docs` | `python` | [GSoC 2026] Kafka Streams runner: say what the Python side is, and is not |
| https://github.com/apache/beam/pull/39758 | `apache/beam` | `code_and_docs` | `python` | Adds support for reading at a given Delta Lake version or timestamp |
| https://github.com/apache/beam/pull/39834 | `apache/beam` | `code_only` | `python` | Support Secret Manager in JdbcIO for Java, Python and YAML |
| https://github.com/apache/beam/pull/39597 | `apache/beam` | `code_and_docs` | `python` | Support lakehouse PCNT format in BigQueryIO storage read. |
| https://github.com/apache/beam/pull/39818 | `apache/beam` | `code_only` | `python` | JmsIO yaml |
| https://github.com/apache/beam/pull/39572 | `apache/beam` | `code_only` | `python` | [Prism] Schedule consumers of a self checkpointing source |
| https://github.com/apache/beam/pull/39738 | `apache/beam` | `code_only` | `python` | Implement Vertex AI Model Monitoring v2 |
| https://github.com/apache/beam/pull/39719 | `apache/beam` | `code_only` | `python` | Cp39645 |
| https://github.com/apache/beam/pull/39763 | `apache/beam` | `code_only` | `python` | normalize KinesisIO |
| https://github.com/apache/beam/pull/39793 | `apache/beam` | `code_and_docs` | `python` | [runners-spark] Support stateful ParDo in the Structured Streaming batch runner |
| https://github.com/apache/beam/pull/39832 | `apache/beam` | `code_only` | `python` | Make primary channel failover timeout configurable (#39646) |
| https://github.com/apache/beam/pull/39724 | `apache/beam` | `code_only` | `python` | [#39723] Implement model for Iceberg side input cache |
| https://github.com/apache/beam/pull/39831 | `apache/beam` | `code_only` | `python` | [CP] bigtable: Require google-cloud-bigtable>=2.42.0 and test Python BigtableIO write error surfacing (#39820) |
| https://github.com/apache/beam/pull/39803 | `apache/beam` | `code_only` | `python` | Fix stale broken cluster connection in CassandraIO (#39788) |
| https://github.com/apache/beam/pull/39820 | `apache/beam` | `code_only` | `python` | bigtable: Require google-cloud-bigtable>=2.42.0 and test Python BigtableIO write error surfacing |
| https://github.com/apache/beam/pull/39646 | `apache/beam` | `code_only` | `python` | Make primary channel failover timeout configurable |
| https://github.com/apache/beam/pull/39685 | `apache/beam` | `code_only_tests_or_fixtures` | `python` | [GSoC-273] Implement TestPubsubContext for Python GCP Integration Tests |
| https://github.com/apache/beam/pull/39792 | `apache/beam` | `code_only` | `python` | bigtable: Set Apache Beam user agent for Python BigtableIO write client |
| https://github.com/apache/beam/pull/39817 | `apache/beam` | `code_only` | `python` | Set getSession to synchronized to avoid race conditions |
| https://github.com/apache/beam/pull/39473 | `apache/beam` | `code_only` | `python` | [Dataflow Streaming] Commit size validation for multi key commits |
| https://github.com/apache/beam/pull/39177 | `apache/beam` | `code_and_docs` | `python` | [GSoC-273] Fixing the github action Unmanaged Service Account Keys |
| https://github.com/apache/beam/pull/39636 | `apache/beam` | `code_only` | `python` | [python] Add Secret management module in apache_beam.utils.secret |
| https://github.com/apache/beam/pull/39806 | `apache/beam` | `code_only` | `python` |  Refactor Java Secret classes to align with Python SDK |
| https://github.com/apache/beam/pull/39465 | `apache/beam` | `code_only` | `python` | Fix PeriodicImpulse/PeriodicSequence watermark regression (#39026) |
| https://github.com/apache/beam/pull/39796 | `apache/beam` | `code_only` | `python` | Updates Dataflow Python container |
| https://github.com/apache/beam/pull/39638 | `apache/beam` | `code_only` | `python` | Fix Golang Zip Slip Vulnerability |
| https://github.com/apache/beam/pull/39788 | `apache/beam` | `code_only` | `python` | Fix stale broken cluster connection in CassandraIO |
| https://github.com/apache/beam/pull/39739 | `apache/beam` | `code_only_tests_or_fixtures` | `python` | [IcebergIO] add test for column default values |
| https://github.com/apache/beam/pull/39549 | `apache/beam` | `code_only` | `python` | Add Delta Lake to Iceberg Yaml blueprint IT |
| https://github.com/apache/beam/pull/39461 | `apache/beam` | `code_only` | `python` | [Python] Refactor MatchContinuously onto the Watch transform |
| https://github.com/apache/beam/pull/39756 | `apache/beam` | `code_only` | `python` | Bump cryptography from 48.0.1 to 50.0.0 in Python SDK |
| https://github.com/apache/beam/pull/39775 | `apache/beam` | `code_only` | `python` | Bump github/codeql-action from 4.37.6 to 4.37.7 |
| https://github.com/apache/beam/pull/39784 | `apache/beam` | `code_only` | `python` | Build Kafka Streams runner during javaPreCommit (#18479) |
| https://github.com/apache/beam/pull/39781 | `apache/beam` | `code_only` | `python` | [GSoC 2026] Kafka Streams runner: shorten comments, and fix the license header and Python formatting |
| https://github.com/apache/beam/pull/39752 | `apache/beam` | `code_only` | `python` | [GSoC 2026] Kafka Streams runner: an application for measuring instances coming and going |
| https://github.com/apache/beam/pull/39762 | `apache/beam` | `code_and_docs` | `python` | [GSoC 2026] Kafka Streams runner: put the runner behind an opt-in build flag |
| https://github.com/apache/beam/pull/39766 | `apache/beam` | `code_only` | `python` | [GSoC 2026] Kafka Streams runner: ask for primitive reads in the Java wrapper |
| https://github.com/apache/beam/pull/39761 | `apache/beam` | `code_and_docs` | `python` | [GSoC 2026] Kafka Streams runner: bound a source poll in time, not only in elements |
| https://github.com/apache/beam/pull/39757 | `apache/beam` | `code_only` | `python` | [GSoC 2026] Requesting permissions for the TestPubSubContext cleanup handler tests |
| https://github.com/apache/beam/pull/38920 | `apache/beam` | `code_only` | `python` | [Dataflow Streaming] [Multi Key] Drop failed work in BoundedQueueExecutor::pollWork |
| https://github.com/apache/beam/pull/39150 | `apache/beam` | `code_only` | `python` | [OpenTelemetry] Add tracing support to GCP PubsubIO |
| https://github.com/apache/beam/pull/39151 | `apache/beam` | `code_only` | `python` | [OpenTelemetry] Add tracing support to KafkaIO |
| https://github.com/apache/beam/pull/39149 | `apache/beam` | `code_only` | `python` | [OpenTelemetry] Add tracing support to GCP Spanner IO |
| https://github.com/apache/beam/pull/39590 | `apache/beam` | `code_only` | `python` | [OpenTelemetry] Redistribute - trace propagation |
| https://github.com/apache/beam/pull/39152 | `apache/beam` | `code_only` | `python` | [OpenTelemetry] Context propagation for Runner v1 and SimpleDoFnRunner |
| https://github.com/apache/beam/pull/39665 | `apache/beam` | `code_only` | `python` | Log the System name in more places instead of the computationId |
| https://github.com/apache/beam/pull/39748 | `apache/beam` | `code_only` | `python` | [GSoC 2026] Kafka Streams runner: separate source poll size from bundle size, expose the session timeout |
| https://github.com/apache/beam/pull/39705 | `apache/beam` | `code_only` | `python` | [IcebergIO] Serialize using json partition |
| https://github.com/apache/beam/pull/39736 | `apache/beam` | `code_only` | `python` | [GSoC 2026] Kafka Streams runner: portable ValidatesRunner suite for Python |
| https://github.com/apache/beam/pull/39735 | `apache/beam` | `code_and_docs` | `python` | [KafkaIO] Remove beam_fn_api requirement for dynamic reads |
| https://github.com/apache/beam/pull/39615 | `apache/beam` | `code_only` | `python` | [Python] Create temporary dataset with a 24 hour ttl. |
| https://github.com/apache/beam/pull/39721 | `apache/beam` | `code_only` | `python` | bump FnAPI container to beam-master-20260811 |
| https://github.com/apache/beam/pull/39722 | `apache/beam` | `code_only` | `python` | Python timestamp fixes. |
| https://github.com/apache/beam/pull/39713 | `apache/beam` | `code_only` | `python` | Fixes to delta CDC read |
| https://github.com/apache/beam/pull/39650 | `apache/beam` | `code_only_tests_or_fixtures` | `python` | Enable Apache Iceberg REST Metrics Reporting for Lakehouse |
| https://github.com/apache/beam/pull/39668 | `apache/beam` | `code_only_tests_or_fixtures` | `python` | [Python] Deflake TextIO footer test |
| https://github.com/apache/beam/pull/39645 | `apache/beam` | `code_only` | `python` | (IcebergIO) document writeProperties param more clearly |
| https://github.com/apache/beam/pull/39655 | `apache/beam` | `code_only` | `python` | normalize io.gcp.DicomSearch |
| https://github.com/apache/beam/pull/39666 | `apache/beam` | `code_only` | `python` | [Dataflow Streaming] Mark worker as unhealthy in presence of stuck commits |
| https://github.com/apache/beam/pull/39716 | `apache/beam` | `code_only` | `python` | [Cherrypick] Fix Python Tests job |
| https://github.com/apache/beam/pull/39715 | `apache/beam` | `code_only` | `python` | Fix Python Tests job |
| https://github.com/apache/beam/pull/39700 | `apache/beam` | `code_only` | `python` | [GSoC 2026] Kafka Streams runner: terminate a bounded pipeline when it is drained |
| https://github.com/apache/beam/pull/39693 | `apache/beam` | `code_only` | `python` | Bump dorny/paths-filter from 4.0.1 to 4.0.3 |
| https://github.com/apache/beam/pull/39504 | `apache/beam` | `code_only` | `python` | feat: add MongoDB driver handshake metadata for Java-based client connections |
| https://github.com/apache/beam/pull/37342 | `apache/beam` | `code_only` | `python` | Fix RequestResponseIO parseAndThrow to preserve retryable exception types |
| https://github.com/apache/beam/pull/39625 | `apache/beam` | `code_only` | `python` | [OpenTelemetry] Enable OpenTelemetry stitching with Logs for Dataflow worker |
| https://github.com/apache/beam/pull/39699 | `apache/beam` | `code_only` | `python` | [Cherrypick] fix ensurepip bundled pip cleanup for Python 3.12+ containers |
| https://github.com/apache/beam/pull/39506 | `apache/beam` | `code_only` | `python` | sdks/java: re-enable nullness checks in WithKeys |
| https://github.com/apache/beam/pull/39444 | `apache/beam` | `code_only` | `python` | Fix nullness for PubsubIO |
| https://github.com/apache/beam/pull/39681 | `apache/beam` | `code_only_tests_or_fixtures` | `python` | [Cherrypick] fix iceberg CDC test - #39675 |
| https://github.com/apache/beam/pull/39697 | `apache/beam` | `code_only` | `python` | CP: Fix mobile gaming release validation background process cleanup (#39658) |
| https://github.com/apache/beam/pull/39658 | `apache/beam` | `code_only` | `python` | Fix mobile gaming release validation background process cleanup for Java 21 compatibility |
| https://github.com/apache/beam/pull/39442 | `apache/beam` | `code_and_docs` | `python` | Add Sample.Any to the Python SDK to match Java's Sample.any |
| https://github.com/apache/beam/pull/39680 | `apache/beam` | `code_only` | `python` | [GSoC 2026] Kafka Streams runner: Python wrapper that starts its own job server |
| https://github.com/apache/beam/pull/39627 | `apache/beam` | `code_and_docs` | `python` | [GSoC 2026] Kafka Streams runner: user documentation, marked experimental |
| https://github.com/apache/beam/pull/39683 | `apache/beam` | `code_only` | `python` | fix ensurepip bundled pip cleanup for Python 3.12+ containers |
| https://github.com/apache/beam/pull/39595 | `apache/beam` | `code_and_docs` | `python` | Add helpers to interact with pipeline options in boot entrypoints |
| https://github.com/apache/beam/pull/39649 | `apache/beam` | `code_only` | `python` | add closing dependabot step |
| https://github.com/apache/beam/pull/39331 | `apache/beam` | `code_only` | `python` | [Spark] Support splittable DoFn self-checkpointing in portable batch |
| https://github.com/apache/beam/pull/39621 | `apache/beam` | `code_only` | `python` | [examples] Atomically publish subprocess executables |
| https://github.com/apache/beam/pull/39622 | `apache/beam` | `code_only_tests_or_fixtures` | `python` | [BigQueryIO] Parallelize schema update integration tests |
| https://github.com/apache/beam/pull/39587 | `apache/beam` | `code_only` | `python` | Fix Row.toString NPE on a null nested inside an array, map or row |
| https://github.com/apache/beam/pull/39675 | `apache/beam` | `code_only` | `python` | fix iceberg CDC test |
| https://github.com/apache/beam/pull/39673 | `apache/beam` | `code_only` | `python` | Bump github/codeql-action from 4.37.5 to 4.37.6 |
| https://github.com/apache/beam/pull/39659 | `apache/beam` | `code_only` | `python` | Fix Python 3.14 Container Build, Streamline Installation |
| https://github.com/apache/beam/pull/39652 | `apache/beam` | `code_only` | `python` | [Dataflow Streaming] Remove redundant onKeyTransition call |
| https://github.com/apache/beam/pull/39651 | `apache/beam` | `code_only` | `python` | Bump github/codeql-action from 4.37.4 to 4.37.5 |
| https://github.com/apache/beam/pull/39648 | `apache/beam` | `code_only` | `python` | [Dataflow Streaming] Remove finalizeCommits from processWork |
| https://github.com/apache/beam/pull/39617 | `apache/beam` | `code_only` | `python` | add aws hadoop to DeltaIO |
| https://github.com/apache/beam/pull/39592 | `apache/beam` | `code_only` | `python` | add Timestamp.MICROS for iceberg timestamptz |
| https://github.com/apache/beam/pull/39600 | `apache/beam` | `code_and_docs` | `python` | [Iceberg CDC] Finish wiring CDC source together and add external API |
| https://github.com/apache/beam/pull/39581 | `apache/beam` | `code_only` | `python` | fix(dataframe): claim remaining restriction range on empty/header-only CSV reads |
| https://github.com/apache/beam/pull/39637 | `apache/beam` | `code_only` | `python` | fix PostCommit Python Dependency |
| https://github.com/apache/beam/pull/39571 | `apache/beam` | `code_and_docs` | `python` | Deflake JmsIO tests |
| https://github.com/apache/beam/pull/39614 | `apache/beam` | `code_and_docs` | `python` | Fix Dataflow ValueProvider serialization |
| https://github.com/apache/beam/pull/39623 | `apache/beam` | `code_only` | `python` | Support sharded coder for Prism runner cross-lang |
| https://github.com/apache/beam/pull/39599 | `apache/beam` | `code_and_docs` | `python` | Adds the Delta Lake CDC read transforms to the Managed I/O API |
| https://github.com/apache/beam/pull/39604 | `apache/beam` | `code_only` | `python` | Bump zizmorcore/zizmor-action from 0.6.1 to 0.6.2 |
| https://github.com/apache/beam/pull/39611 | `apache/beam` | `code_only` | `python` | [GSoC 2026] Kafka Streams runner: read unbounded sources |
| https://github.com/apache/beam/pull/38220 | `apache/beam` | `code_and_docs` | `python` | [Go SDK] Add GroupIntoBatches transform (#19868) |
| https://github.com/apache/beam/pull/39602 | `apache/beam` | `code_only` | `python` | Bump com.gradle.common-custom-user-data-gradle-plugin from 2.7.0 to 2.8.0 |
| https://github.com/apache/beam/pull/39610 | `apache/beam` | `code_only` | `python` | [GSoC 2026] Kafka Streams runner: CombineTest coverage and two review follow-ups |
| https://github.com/apache/beam/pull/39567 | `apache/beam` | `code_only` | `python` | [OpenTelemetry] Create span in spanner CDC to start new trace when otel is enabled. |
| https://github.com/apache/beam/pull/39561 | `apache/beam` | `code_only` | `python` | Part 1: Log systemName in DataflowWorkUnitClient, Commit, and core worker states |
| https://github.com/apache/beam/pull/38942 | `apache/beam` | `code_only` | `python` | Potential fix for environment variable built from user-controlled sources |
| https://github.com/apache/beam/pull/38837 | `apache/beam` | `code_only` | `python` | [Iceberg CDC] Add Changelog readers and update resolver |
| https://github.com/apache/beam/pull/39344 | `apache/beam` | `code_and_docs` | `python` | [Iceberg] Make timestamptz return new Timestamp.MICROS logical type |
| https://github.com/apache/beam/pull/39448 | `apache/beam` | `code_and_docs` | `python` | remove gsutil usage |
| https://github.com/apache/beam/pull/39596 | `apache/beam` | `code_only` | `python` | Update Python SDK container tag |
| https://github.com/apache/beam/pull/39090 | `apache/beam` | `code_only` | `python` | [Python] Bound Watch state with a timestamp cursor |
| https://github.com/apache/beam/pull/39569 | `apache/beam` | `code_and_docs` | `python` | [DebeziumIO] Upgrade to Debezium 3.5.2.Final |
| https://github.com/apache/beam/pull/39160 | `apache/beam` | `code_only` | `python` | Add query_output_schema to ReadFromBigQuery for BEAM_ROW + query support |
| https://github.com/apache/beam/pull/39591 | `apache/beam` | `code_only` | `python` | Fix internal test failure after #39487 |
| https://github.com/apache/beam/pull/39583 | `apache/beam` | `code_only` | `python` | Support array-valued schema options in Python |
| https://github.com/apache/beam/pull/39563 | `apache/beam` | `code_only` | `python` | Fix dataframe CSV tests on Windows |
| https://github.com/apache/beam/pull/39484 | `apache/beam` | `code_and_docs` | `python` | Support core dump analysis with pystack and gdb. |
| https://github.com/apache/beam/pull/39586 | `apache/beam` | `code_only` | `python` | Bump github/codeql-action from 4.37.3 to 4.37.4 |
| https://github.com/apache/beam/pull/39578 | `apache/beam` | `code_only` | `python` | [GSoC 2026] Kafka Streams runner: bound a bundle by element count |
| https://github.com/apache/beam/pull/38047 | `apache/beam` | `code_only_tests_or_fixtures` | `python` | Fix flaky FileIOTest.testMatchWatchForNewFiles test under CI filesystems |
| https://github.com/apache/beam/pull/39546 | `apache/beam` | `code_only` | `python` | [GSoC 2026] Kafka Streams runner: run on a real broker, correctly across partitions |
| https://github.com/apache/beam/pull/39575 | `apache/beam` | `code_only` | `python` | Update SDK container tags |
| https://github.com/apache/beam/pull/39570 | `apache/beam` | `code_only` | `python` | use Java 17 harness |
| https://github.com/apache/beam/pull/39439 | `apache/beam` | `code_and_docs` | `python` | Remove remaining artifacts from dataflow apitools client |
| https://github.com/apache/beam/pull/39467 | `apache/beam` | `code_only` | `python` | Support IBM MQ for Python JmsIO |
| https://github.com/apache/beam/pull/39564 | `apache/beam` | `code_only` | `python` | Bump github/codeql-action from 4 to 4.37.3 |
| https://github.com/apache/beam/pull/39562 | `apache/beam` | `code_only_tests_or_fixtures` | `python` | Fix flaky unit test to pass post-submit checks |
| https://github.com/apache/beam/pull/39161 | `apache/beam` | `code_only` | `python` | [Interactive Beam] Fix caching deadlock, wait race conditions, and stale graph in notebooks |
| https://github.com/apache/beam/pull/39433 | `apache/beam` | `code_only` | `python` | Clean up legacy references to apitools in GCS I/O |
| https://github.com/apache/beam/pull/39487 | `apache/beam` | `code_only` | `python` | Fix DataflowOutputCounter calculation for ValueInEmptyWindows |
| https://github.com/apache/beam/pull/39288 | `apache/beam` | `code_only` | `python` | Buffer BufferedLogger by newline to avoid log splitting |
| https://github.com/apache/beam/pull/39537 | `apache/beam` | `code_and_docs` | `python` | Enhance Python Timestamp to be precision-variable up to nanos, and map it to Timestamp logical type |
| https://github.com/apache/beam/pull/39533 | `apache/beam` | `code_only_tests_or_fixtures` | `python` | fix AddFilesIT filter for BigLake |
| https://github.com/apache/beam/pull/38833 | `apache/beam` | `code_only` | `python` | Preserve partitioning on temp FILE_LOADS tables |
| https://github.com/apache/beam/pull/39552 | `apache/beam` | `code_only` | `python` | Bump docker/login-action from 4.5.2 to 4.6.0 |
| https://github.com/apache/beam/pull/39457 | `apache/beam` | `code_only` | `python` | Debezium IO yaml |
| https://github.com/apache/beam/pull/39558 | `apache/beam` | `code_only` | `python` | Fix Unmanaged Service Accounts Keys Audit workflow |
| https://github.com/apache/beam/pull/39462 | `apache/beam` | `code_only_tests_or_fixtures` | `python` | Fix module-level side effects and global random seeding |
| https://github.com/apache/beam/pull/39426 | `apache/beam` | `code_only` | `python` | Updates the Delta Lake source to support reading bounded change data |
| https://github.com/apache/beam/pull/39440 | `apache/beam` | `code_only` | `python` | Provide a better error when beam plugin was supplied but wasn't staged. |
| https://github.com/apache/beam/pull/39064 | `apache/beam` | `code_and_docs` | `python` | [IcebergIO] Raise Java 17 floor for IcebergIO's Java 11 dependents |
| https://github.com/apache/beam/pull/39535 | `apache/beam` | `code_only` | `python` | Changes SplittableDoFn to call TruncateRestriction on drain |
| https://github.com/apache/beam/pull/39530 | `apache/beam` | `code_only` | `python` | Bump lower and upper bounds for pyarrow + related dependencies, remove unnecessary CVE hotfix |
| https://github.com/apache/beam/pull/39547 | `apache/beam` | `code_only` | `python` | [Python] Convert typing and native generic hints in Watch coder inference |
| https://github.com/apache/beam/pull/39539 | `apache/beam` | `code_only_tests_or_fixtures` | `python` | Fix flaky BigQuery persistent retry test |
| https://github.com/apache/beam/pull/39445 | `apache/beam` | `code_only` | `python` | Override default fadvise to fix regression from gcs-connector v3 upgrade |
| https://github.com/apache/beam/pull/39491 | `apache/beam` | `code_only` | `python` | add workflow_dispatch to other workflow files |
| https://github.com/apache/beam/pull/38919 | `apache/beam` | `code_only` | `python` | [Dataflow Streaming] [Multi Key] MultiKey failure handling + Integration  |
| https://github.com/apache/beam/pull/39534 | `apache/beam` | `code_only` | `python` | Fix Update Python Dependencies |
| https://github.com/apache/beam/pull/36926 | `apache/beam` | `code_only` | `python` | Offset deduplication - Propagate offset and record  in output builder |
| https://github.com/apache/beam/pull/36886 | `apache/beam` | `code_only_tests_or_fixtures` | `python` | ParDoLifecycleTest concurrency bug - callStateMap  |
| https://github.com/apache/beam/pull/36534 | `apache/beam` | `code_only` | `python` | [Java] Dataflow runner v1 - Propagate drain mode |
| https://github.com/apache/beam/pull/36524 | `apache/beam` | `code_only` | `python` | Drain - model part + windowedValue changes |
| https://github.com/apache/beam/pull/36329 | `apache/beam` | `code_only` | `python` | increase timeout for "Publish Beam SDK Snapshots" |
| https://github.com/apache/beam/pull/39148 | `apache/beam` | `code_only` | `python` | Write append tables can be asynchronous (#39120) |
| https://github.com/apache/beam/pull/39540 | `apache/beam` | `code_only` | `python` | Bump docker/login-action from 4.5.1 to 4.5.2 |
| https://github.com/apache/beam/pull/39528 | `apache/beam` | `code_only` | `python` | [Gemini] Fix pyrefly check unexpected-keyword |
| https://github.com/apache/beam/pull/39490 | `apache/beam` | `code_only` | `python` | fix golangci-lint issue - tour of beam |
| https://github.com/apache/beam/pull/39316 | `apache/beam` | `code_only` | `python` | KeyCommitTooLarge logging improvements |
| https://github.com/apache/beam/pull/39437 | `apache/beam` | `code_only` | `python` | Support JmsIO SchemaTransform and cross-lang |
| https://github.com/apache/beam/pull/37904 | `apache/beam` | `code_and_docs` | `python` | [Java IO] Add ArrowFlight IO connector |
| https://github.com/apache/beam/pull/39531 | `apache/beam` | `code_only` | `python` | Update ruff and pyrefly dependencies |
| https://github.com/apache/beam/pull/39527 | `apache/beam` | `code_only` | `python` | Replace non-PEP 585 types in watch.py |
| https://github.com/vercel/turborepo/pull/13845 | `vercel/turborepo` | `code_only` | `typescript` | fix: Remove unsupported remote cache environment variable |
| https://github.com/vercel/turborepo/pull/13844 | `vercel/turborepo` | `code_and_docs` | `typescript` | chore: Release Turborepo 2.10.12 |
| https://github.com/vercel/turborepo/pull/13843 | `vercel/turborepo` | `code_only` | `typescript` | fix: Run pnpm directly on Windows |
| https://github.com/vercel/turborepo/pull/13842 | `vercel/turborepo` | `code_and_docs` | `typescript` | feat: Require high confidence for issue fixes |
| https://github.com/vercel/turborepo/pull/13841 | `vercel/turborepo` | `code_and_docs` | `typescript` | chore: Alert Slack for low-confidence issues |
| https://github.com/vercel/turborepo/pull/13840 | `vercel/turborepo` | `code_and_docs` | `typescript` | chore: Add automatic issue handling |
| https://github.com/vercel/turborepo/pull/13839 | `vercel/turborepo` | `code_only` | `typescript` | fix: Escape ampersands in RSS feed enclosure URLs |
| https://github.com/vercel/turborepo/pull/13836 | `vercel/turborepo` | `code_and_docs` | `typescript` | chore: Handle feedback on Factory pull requests |
| https://github.com/vercel/turborepo/pull/13834 | `vercel/turborepo` | `code_only` | `typescript` | chore: Use geistdocs 1.23.1 |
| https://github.com/vercel/turborepo/pull/13837 | `vercel/turborepo` | `code_and_docs` | `typescript` | chore: Skip redundant Factory PR approval |
| https://github.com/vercel/turborepo/pull/13835 | `vercel/turborepo` | `code_only` | `typescript` | fix: Move model selector to workspace creation |
| https://github.com/vercel/turborepo/pull/13833 | `vercel/turborepo` | `code_only` | `typescript` | chore: Add operator chat model selector |
| https://github.com/vercel/turborepo/pull/13831 | `vercel/turborepo` | `code_and_docs` | `typescript` | fix: Update Factory pull request branches |
| https://github.com/vercel/turborepo/pull/13828 | `vercel/turborepo` | `code_only` | `typescript` | fix: Prevent chat SSH command overflow |
| https://github.com/vercel/turborepo/pull/13827 | `vercel/turborepo` | `code_only` | `typescript` | fix: Add workspace approval controls |
| https://github.com/vercel/turborepo/pull/13805 | `vercel/turborepo` | `code_only` | `typescript` | fix: Include virtual tasks in affected query |
| https://github.com/vercel/turborepo/pull/13824 | `vercel/turborepo` | `code_and_docs` | `typescript` | chore: Update basic example |
| https://github.com/vercel/turborepo/pull/13809 | `vercel/turborepo` | `code_only` | `typescript` | perf: Batch package detail queries |
| https://github.com/vercel/turborepo/pull/13808 | `vercel/turborepo` | `code_only` | `typescript` | chore: Update non-monorepo example |
| https://github.com/vercel/turborepo/pull/13820 | `vercel/turborepo` | `code_only` | `typescript` | perf: Skip Factory chat verification |
| https://github.com/vercel/turborepo/pull/13819 | `vercel/turborepo` | `code_only` | `typescript` | feat: Standardize Factory meta titles to Turborepo suffix |
| https://github.com/vercel/turborepo/pull/13817 | `vercel/turborepo` | `code_only` | `typescript` | fix: Install Factory publishing skill |
| https://github.com/vercel/turborepo/pull/13815 | `vercel/turborepo` | `code_only` | `typescript` | fix: Improve Factory terminal line spacing |
| https://github.com/vercel/turborepo/pull/13814 | `vercel/turborepo` | `code_only` | `typescript` | fix: Update Factory session network policy |
| https://github.com/vercel/turborepo/pull/13812 | `vercel/turborepo` | `code_only` | `typescript` | fix: Restore Factory workspace creation |
| https://github.com/vercel/turborepo/pull/13803 | `vercel/turborepo` | `code_only` | `typescript` | refactor: Migrate Factory styles to Tailwind |
| https://github.com/vercel/turborepo/pull/13802 | `vercel/turborepo` | `code_and_docs` | `typescript` | feat: Add factory navigation |
| https://github.com/vercel/turborepo/pull/13801 | `vercel/turborepo` | `code_and_docs` | `typescript` | fix: Rebuild factory images without custom workflows |
| https://github.com/vercel/turborepo/pull/13797 | `vercel/turborepo` | `code_only` | `typescript` | chore: Update with-solid example |
| https://github.com/vercel/turborepo/pull/13798 | `vercel/turborepo` | `code_and_docs` | `typescript` | feat: Start ad-hoc factory work from the operator page |
| https://github.com/vercel/turborepo/pull/13799 | `vercel/turborepo` | `code_and_docs` | `typescript` | fix: Decouple graceful shutdown tests from the shell commands example |
| https://github.com/vercel/turborepo/pull/13782 | `vercel/turborepo` | `code_only` | `typescript` | chore: Allow SSH terminal for completed-run sandboxes in Factory |
| https://github.com/vercel/turborepo/pull/13791 | `vercel/turborepo` | `code_and_docs` | `typescript` | chore: Update with-shell-commands example |
| https://github.com/vercel/turborepo/pull/13780 | `vercel/turborepo` | `code_only` | `typescript` | chore: Add full-page terminal SSH sessions to Factory sandbox inventory |
| https://github.com/vercel/turborepo/pull/13792 | `vercel/turborepo` | `code_only` | `typescript` | perf: Skip unused repository indexing for package listings |
| https://github.com/vercel/turborepo/pull/13793 | `vercel/turborepo` | `code_only` | `typescript` | fix: Show invalid affected task glob |
| https://github.com/vercel/turborepo/pull/13779 | `vercel/turborepo` | `code_only` | `typescript` | feat: Add SSH command affordance for factory sandboxes |
| https://github.com/vercel/turborepo/pull/13789 | `vercel/turborepo` | `code_and_docs` | `typescript` | chore: Update remote cache action to v1.1.0 |
| https://github.com/vercel/turborepo/pull/13787 | `vercel/turborepo` | `code_only` | `typescript` | perf: Index Berry lockfile resolution overrides by dependency name |
| https://github.com/vercel/turborepo/pull/13786 | `vercel/turborepo` | `code_only` | `typescript` | chore: Update with-rsbuild-module-federation example |
| https://github.com/vercel/turborepo/pull/13783 | `vercel/turborepo` | `code_and_docs` | `typescript` | chore: Upgrade the factory eve agent to 0.39.3 |
| https://github.com/vercel/turborepo/pull/13776 | `vercel/turborepo` | `code_only` | `typescript` | perf: Replace regex captures with hand-written parsers in berry lockfile identifiers |
| https://github.com/vercel/turborepo/pull/13775 | `vercel/turborepo` | `code_only` | `typescript` | feat: Redesign factory control plane |
| https://github.com/vercel/turborepo/pull/13778 | `vercel/turborepo` | `code_and_docs` | `typescript` | feat: Add security.txt endpoint |
| https://github.com/vercel/turborepo/pull/13777 | `vercel/turborepo` | `code_only` | `typescript` | chore: Update oxlint and oxfmt |
| https://github.com/vercel/turborepo/pull/13773 | `vercel/turborepo` | `code_and_docs` | `typescript` | fix: Remove incremental task caching |
| https://github.com/vercel/turborepo/pull/13763 | `vercel/turborepo` | `code_only` | `typescript` | perf: Merge same-prefix tree-wildcard globs into one directory walk |
| https://github.com/vercel/turborepo/pull/13772 | `vercel/turborepo` | `code_only` | `typescript` | chore: Update with-ultracite example |
| https://github.com/vercel/turborepo/pull/13760 | `vercel/turborepo` | `code_only` | `typescript` | perf: Stream dry-run JSON output |
| https://github.com/vercel/turborepo/pull/13746 | `vercel/turborepo` | `code_only` | `typescript` | perf: Skip unused Package Configuration `stat`s |
| https://github.com/vercel/turborepo/pull/13771 | `vercel/turborepo` | `code_only` | `typescript` | chore: Update Geistdocs to 1.20.4 |
| https://github.com/vercel/turborepo/pull/13770 | `vercel/turborepo` | `code_only` | `typescript` | fix: Prevent homepage KPI overflow |
| https://github.com/vercel/turborepo/pull/13769 | `vercel/turborepo` | `code_only` | `typescript` | fix: Align homepage KPIs to the right |
| https://github.com/vercel/turborepo/pull/13767 | `vercel/turborepo` | `code_only` | `typescript` | fix: Refine mobile homepage interactions |
| https://github.com/vercel/turborepo/pull/13766 | `vercel/turborepo` | `code_only` | `typescript` | fix: Preserve showcase logo sizes |
| https://github.com/vercel/turborepo/pull/13764 | `vercel/turborepo` | `code_and_docs` | `typescript` | feat: Refresh documentation social cards |
| https://github.com/vercel/turborepo/pull/13765 | `vercel/turborepo` | `code_and_docs` | `typescript` | chore: Release Turborepo 2.10.11 |
| https://github.com/vercel/turborepo/pull/13734 | `vercel/turborepo` | `code_and_docs` | `typescript` | fix: Tolerate transient input files |
| https://github.com/vercel/turborepo/pull/13761 | `vercel/turborepo` | `code_and_docs` | `typescript` | feat: Expand performance agent toolbox |
| https://github.com/vercel/turborepo/pull/13759 | `vercel/turborepo` | `code_and_docs` | `typescript` | chore: Release Turborepo 2.10.11-canary.4 |
| https://github.com/vercel/turborepo/pull/13756 | `vercel/turborepo` | `code_only` | `typescript` | fix: Respect gitignore without git metadata |
| https://github.com/vercel/turborepo/pull/13751 | `vercel/turborepo` | `code_and_docs` | `typescript` | chore: Forbid release-age exclusions in examples maintenance |
| https://github.com/vercel/turborepo/pull/13750 | `vercel/turborepo` | `code_only` | `typescript` | fix: Isolate concurrent generator config bundles |
| https://github.com/vercel/turborepo/pull/13749 | `vercel/turborepo` | `code_and_docs` | `typescript` | chore: Release Turborepo 2.10.11-canary.3 |
| https://github.com/vercel/turborepo/pull/13748 | `vercel/turborepo` | `code_and_docs` | `typescript` | feat: Cache native uv tool tasks |
| https://github.com/vercel/turborepo/pull/13747 | `vercel/turborepo` | `code_and_docs` | `typescript` | chore: Release Turborepo 2.10.11-canary.2 |
| https://github.com/vercel/turborepo/pull/13745 | `vercel/turborepo` | `code_only` | `typescript` | fix: Avoid repeated strict entrypoint traversal |
| https://github.com/vercel/turborepo/pull/13744 | `vercel/turborepo` | `code_and_docs` | `typescript` | chore: Release Turborepo 2.10.11-canary.1 |
| https://github.com/vercel/turborepo/pull/13743 | `vercel/turborepo` | `code_and_docs` | `typescript` | fix: Automatically approve release workflows |
| https://github.com/vercel/turborepo/pull/13741 | `vercel/turborepo` | `code_and_docs` | `typescript` | chore: Release Turborepo 2.10.10 |
| https://github.com/vercel/turborepo/pull/13740 | `vercel/turborepo` | `code_only` | `typescript` | fix(bun): Preserve overrides objects, trustedDependencies, workspace bins and git integrity through prune; accept lockfileVersion 3 |
| https://github.com/vercel/turborepo/pull/13739 | `vercel/turborepo` | `code_only` | `typescript` | chore: Release Turbo repository packages 0.0.1-canary.24 |
| https://github.com/vercel/turborepo/pull/13738 | `vercel/turborepo` | `code_only` | `typescript` | fix: Scope musl library dependency installation |
| https://github.com/vercel/turborepo/pull/13737 | `vercel/turborepo` | `code_and_docs` | `typescript` | feat: Support cross-toolchain repository affectedness |
| https://github.com/vercel/turborepo/pull/13729 | `vercel/turborepo` | `code_and_docs` | `typescript` | feat: Add daily performance agent |
| https://github.com/vercel/turborepo/pull/13730 | `vercel/turborepo` | `code_only` | `typescript` | chore: Update with-rsbuild example |
| https://github.com/vercel/turborepo/pull/13727 | `vercel/turborepo` | `code_only` | `typescript` | chore: Update non-monorepo example |
| https://github.com/vercel/turborepo/pull/13733 | `vercel/turborepo` | `code_only` | `typescript` | fix: Expose Slack delivery diagnostics |
| https://github.com/vercel/turborepo/pull/13731 | `vercel/turborepo` | `code_and_docs` | `typescript` | feat: Trigger daily performance improvements from the dashboard |
| https://github.com/vercel/turborepo/pull/13726 | `vercel/turborepo` | `code_only` | `typescript` | chore: Enforce draft pull requests |
| https://github.com/vercel/turborepo/pull/13722 | `vercel/turborepo` | `code_only` | `typescript` | feat: Notify Slack when agents open PRs |
| https://github.com/vercel/turborepo/pull/13723 | `vercel/turborepo` | `code_and_docs` | `typescript` | chore: Validate updated examples with turbo |
| https://github.com/vercel/turborepo/pull/13721 | `vercel/turborepo` | `code_and_docs` | `typescript` | chore: Release Turborepo 2.10.10-canary.3 |
| https://github.com/vercel/turborepo/pull/13720 | `vercel/turborepo` | `code_and_docs` | `typescript` | feat: Add pytest task discovery |
| https://github.com/vercel/turborepo/pull/13690 | `vercel/turborepo` | `code_only` | `typescript` | fix: Apply nested parent gitignore patterns in manual hashing |
| https://github.com/vercel/turborepo/pull/13709 | `vercel/turborepo` | `code_only` | `typescript` | fix(cli): Move EXPERIMENTAL label from ls command to --output flag |
| https://github.com/vercel/turborepo/pull/13713 | `vercel/turborepo` | `code_and_docs` | `typescript` | chore: Upgrade TypeScript to 7.0.2 |
| https://github.com/vercel/turborepo/pull/13716 | `vercel/turborepo` | `code_only` | `typescript` | fix: Resolve agent lint errors |
| https://github.com/vercel/turborepo/pull/13715 | `vercel/turborepo` | `code_and_docs` | `typescript` | feat: Rotate Eve example maintenance daily |
| https://github.com/vercel/turborepo/pull/13712 | `vercel/turborepo` | `code_only` | `typescript` | fix: Remove unsupported sandbox network policy |
| https://github.com/vercel/turborepo/pull/13710 | `vercel/turborepo` | `code_and_docs` | `typescript` | feat: Add Eve operator dashboard |
| https://github.com/vercel/turborepo/pull/13708 | `vercel/turborepo` | `code_and_docs` | `typescript` | fix: Enable Eve examples pull requests |
| https://github.com/vercel/turborepo/pull/13707 | `vercel/turborepo` | `code_and_docs` | `typescript` | chore: Release Turborepo 2.10.10-canary.2 |
| https://github.com/vercel/turborepo/pull/13706 | `vercel/turborepo` | `code_only` | `typescript` | chore: Move pnpm overrides to pnpm-workspace.yaml |
| https://github.com/vercel/turborepo/pull/13704 | `vercel/turborepo` | `code_only` | `typescript` | fix(deps): Upgrade js-yaml to 4.3.1 (GHSA-5p4m-2wfm-xmqj) |
| https://github.com/vercel/turborepo/pull/13705 | `vercel/turborepo` | `code_only` | `typescript` | perf: Walk the repository once when pruning |
| https://github.com/vercel/turborepo/pull/13703 | `vercel/turborepo` | `code_and_docs` | `typescript` | chore: Release Turborepo 2.10.10-canary.1 |
| https://github.com/vercel/turborepo/pull/13699 | `vercel/turborepo` | `code_only` | `typescript` | feat: Support nub.lock files |
| https://github.com/vercel/turborepo/pull/13701 | `vercel/turborepo` | `code_only` | `typescript` | docs: Update Geistdocs to 1.19.6 |
| https://github.com/vercel/turborepo/pull/13696 | `vercel/turborepo` | `code_and_docs` | `typescript` | chore: Release Turborepo 2.10.9 |
| https://github.com/vercel/turborepo/pull/13695 | `vercel/turborepo` | `code_only` | `typescript` | fix: Prevent Windows process cleanup PID reuse |
| https://github.com/vercel/turborepo/pull/13694 | `vercel/turborepo` | `code_only` | `typescript` | fix: Prune Bun wildcard workspace dev dependencies |
| https://github.com/vercel/turborepo/pull/13687 | `vercel/turborepo` | `code_and_docs` | `typescript` | chore: Release Turborepo 2.10.9-canary.1 |
| https://github.com/vercel/turborepo/pull/13675 | `vercel/turborepo` | `code_only_tests_or_fixtures` | `typescript` | test: Cover Python quality task graph |
| https://github.com/vercel/turborepo/pull/13674 | `vercel/turborepo` | `code_only` | `typescript` | feat: Hash Python quality task inputs |
| https://github.com/vercel/turborepo/pull/13673 | `vercel/turborepo` | `code_only` | `typescript` | test: Cover Python quality task commands |
| https://github.com/vercel/turborepo/pull/13672 | `vercel/turborepo` | `code_only` | `typescript` | feat: Synthesize Python quality tasks |
| https://github.com/vercel/turborepo/pull/13671 | `vercel/turborepo` | `code_only` | `typescript` | refactor: Extract uv native task specs |
| https://github.com/vercel/turborepo/pull/13670 | `vercel/turborepo` | `code_only` | `typescript` | feat: Resolve Python quality plans |
| https://github.com/vercel/turborepo/pull/13669 | `vercel/turborepo` | `code_only` | `typescript` | feat: Parse Python quality tool declarations |
| https://github.com/vercel/turborepo/pull/13686 | `vercel/turborepo` | `code_and_docs` | `typescript` | test: Stabilize watch task inputs regression test |
| https://github.com/vercel/turborepo/pull/13668 | `vercel/turborepo` | `code_only` | `typescript` | fix: Respect aggregate task overrides |
| https://github.com/vercel/turborepo/pull/13667 | `vercel/turborepo` | `code_only` | `typescript` | feat: Compose aggregate native task dependencies |
| https://github.com/vercel/turborepo/pull/13666 | `vercel/turborepo` | `code_only` | `typescript` | refactor: Model native task execution explicitly |
| https://github.com/vercel/turborepo/pull/13665 | `vercel/turborepo` | `code_only` | `typescript` | refactor: Move native contracts to tasks |
| https://github.com/vercel/turborepo/pull/13664 | `vercel/turborepo` | `code_only` | `typescript` | refactor: Generalize native command arguments |
| https://github.com/vercel/turborepo/pull/13685 | `vercel/turborepo` | `code_and_docs` | `typescript` | docs: Update redirected vercel.com/nextjs.org links to current targets |
| https://github.com/vercel/turborepo/pull/13632 | `vercel/turborepo` | `code_and_docs` | `typescript` | fix: Invalidate only when Git ignore sources change |
| https://github.com/vercel/turborepo/pull/13682 | `vercel/turborepo` | `code_only` | `typescript` | docs: Use the geistdocs Turborepo logo in the navbar |
| https://github.com/vercel/turborepo/pull/13681 | `vercel/turborepo` | `code_only` | `typescript` | docs: Exclude Turborepo from its own OSS products menu |
| https://github.com/vercel/turborepo/pull/13680 | `vercel/turborepo` | `code_only` | `typescript` | docs: Update Geistdocs to 1.19.4 |
| https://github.com/vercel/turborepo/pull/13637 | `vercel/turborepo` | `code_only` | `typescript` | fix: Don't use `eprintln!` in the panic hook |
| https://github.com/vercel/turborepo/pull/13658 | `vercel/turborepo` | `code_only` | `typescript` | fix: Upgrade brace-expansion to 5.0.9 |
| https://github.com/vercel/turborepo/pull/13656 | `vercel/turborepo` | `code_and_docs` | `typescript` | fix: Compose affected tasks with package filters |
| https://github.com/vercel/turborepo/pull/13645 | `vercel/turborepo` | `code_only` | `typescript` | perf: Intern resolution identities as Arc&lt;str&gt; across closures |
| https://github.com/vercel/turborepo/pull/13643 | `vercel/turborepo` | `code_only` | `typescript` | perf: Build resolution identity lists in parallel |
| https://github.com/vercel/turborepo/pull/13642 | `vercel/turborepo` | `code_only` | `typescript` | perf: Parallelize resolution fingerprint hashing |
| https://github.com/vercel/turborepo/pull/13640 | `vercel/turborepo` | `code_only` | `typescript` | perf: Parse pnpm explicit-key entries in the lockfile fast path |
| https://github.com/vercel/turborepo/pull/13635 | `vercel/turborepo` | `code_only` | `typescript` | perf: Enable shared closure DP for npm and yarn1 lockfiles |
| https://github.com/vercel/turborepo/pull/13646 | `vercel/turborepo` | `code_only` | `typescript` | perf: Avoid materializing transient declarations in external_dependencies |
| https://github.com/vercel/turborepo/pull/13634 | `vercel/turborepo` | `code_only` | `typescript` | perf: Memoize framework inference per package during task hashing |
| https://github.com/vercel/turborepo/pull/13633 | `vercel/turborepo` | `code_only` | `typescript` | perf: Index Bun nested lockfile entries by name for fallback resolution |
| https://github.com/vercel/turborepo/pull/13631 | `vercel/turborepo` | `code_and_docs` | `typescript` | refactor: Remove turborepo-lsp dependency on turborepo-lib |
| https://github.com/vercel/turborepo/pull/13641 | `vercel/turborepo` | `code_only` | `typescript` | perf: Share resolution identity lists across identical workspace closures |
| https://github.com/vercel/turborepo/pull/13647 | `vercel/turborepo` | `code_only` | `typescript` | perf: Index workspace nodes by name in project_relationships |
| https://github.com/vercel/turborepo/pull/13649 | `vercel/turborepo` | `code_only` | `typescript` | perf(lockfiles): Drop redundant human_name clone for pnpm v7/v9 |
| https://github.com/vercel/turborepo/pull/13650 | `vercel/turborepo` | `code_only` | `typescript` | perf(repository): Avoid discarded alias allocation in Relationship |
| https://github.com/vercel/turborepo/pull/13648 | `vercel/turborepo` | `code_only` | `typescript` | perf(lockfiles): Borrow field-name scalars in the pnpm fast parser |
| https://github.com/vercel/turborepo/pull/13623 | `vercel/turborepo` | `code_only` | `typescript` | fix: Accept semver ranges in devEngines.packageManager.version |
| https://github.com/vercel/turborepo/pull/13522 | `vercel/turborepo` | `code_only` | `typescript` | perf: Walk literal-prefix tree globs without wax compilation |
| https://github.com/vercel/turborepo/pull/13626 | `vercel/turborepo` | `code_and_docs` | `typescript` | chore: Release Turborepo 2.10.8 |
| https://github.com/vercel/turborepo/pull/13602 | `vercel/turborepo` | `code_and_docs` | `typescript` | test: Add uv workspace integration coverage |
| https://github.com/vercel/turborepo/pull/13622 | `vercel/turborepo` | `code_and_docs` | `typescript` | fix: Fall back to polling on macOS |
| https://github.com/vercel/turborepo/pull/13613 | `vercel/turborepo` | `code_only` | `typescript` | feat: Prune uv workspaces |
| https://github.com/vercel/turborepo/pull/13612 | `vercel/turborepo` | `code_only` | `typescript` | feat: Watch uv workspace changes |
| https://github.com/vercel/turborepo/pull/13621 | `vercel/turborepo` | `code_only` | `typescript` | fix: Make Windows Cap'n Proto cache relocatable |
| https://github.com/vercel/turborepo/pull/13611 | `vercel/turborepo` | `code_only` | `typescript` | feat: Hash uv lockfile closures |
| https://github.com/vercel/turborepo/pull/13610 | `vercel/turborepo` | `code_only` | `typescript` | feat: Run native uv tasks |
| https://github.com/vercel/turborepo/pull/13609 | `vercel/turborepo` | `code_only` | `typescript` | feat: Discover uv workspaces |
| https://github.com/vercel/turborepo/pull/13616 | `vercel/turborepo` | `code_only` | `typescript` | ci: Invalidate Cap'n Proto caches |
| https://github.com/vercel/turborepo/pull/13608 | `vercel/turborepo` | `code_only` | `typescript` | refactor: Compose repository graphs for optional toolchains |
| https://github.com/vercel/turborepo/pull/13606 | `vercel/turborepo` | `code_and_docs` | `typescript` | feat: Add native Cargo format task |
| https://github.com/vercel/turborepo/pull/13603 | `vercel/turborepo` | `code_and_docs` | `typescript` | refactor: Remove retained package payloads |
| https://github.com/vercel/turborepo/pull/13601 | `vercel/turborepo` | `code_only` | `typescript` | refactor: Resolve MFE package ownership from graph |
| https://github.com/vercel/turborepo/pull/13600 | `vercel/turborepo` | `code_and_docs` | `typescript` | perf: Reuse Cargo metadata discovery snapshot |
| https://github.com/vercel/turborepo/pull/13599 | `vercel/turborepo` | `code_only` | `typescript` | refactor: Fail closed on invalid relationships |
| https://github.com/vercel/turborepo/pull/13598 | `vercel/turborepo` | `code_and_docs` | `typescript` | refactor: Own resolution fingerprints in repository |
| https://github.com/vercel/turborepo/pull/13597 | `vercel/turborepo` | `code_only` | `typescript` | refactor: Route N-API package listing by manifest |
| https://github.com/vercel/turborepo/pull/13596 | `vercel/turborepo` | `code_and_docs` | `typescript` | refactor: Route resolution through explicit domains |
| https://github.com/vercel/turborepo/pull/13595 | `vercel/turborepo` | `code_and_docs` | `typescript` | refactor: Route residual task behavior by capability |
| https://github.com/vercel/turborepo/pull/13593 | `vercel/turborepo` | `code_and_docs` | `typescript` | refactor: Project manifest-derived repository facts |
| https://github.com/vercel/turborepo/pull/13592 | `vercel/turborepo` | `code_and_docs` | `typescript` | refactor: Route MFE eligibility by manifest |
| https://github.com/vercel/turborepo/pull/13591 | `vercel/turborepo` | `code_only` | `typescript` | refactor: Route package consumers by manifest |
| https://github.com/vercel/turborepo/pull/13589 | `vercel/turborepo` | `code_and_docs` | `typescript` | refactor: Route task behavior through contract domains |
| https://github.com/vercel/turborepo/pull/13587 | `vercel/turborepo` | `code_and_docs` | `typescript` | refactor: Remove ToolchainId runtime dispatch |
| https://github.com/vercel/turborepo/pull/13586 | `vercel/turborepo` | `code_and_docs` | `typescript` | refactor: Remove Cargo contributor plumbing |
| https://github.com/vercel/turborepo/pull/13585 | `vercel/turborepo` | `code_and_docs` | `typescript` | refactor: Replace toolchains with repository contributors |
| https://github.com/vercel/turborepo/pull/13588 | `vercel/turborepo` | `code_only_tests_or_fixtures` | `typescript` | ci: Restore Cargo target for lockfile tests |
| https://github.com/vercel/turborepo/pull/13584 | `vercel/turborepo` | `code_and_docs` | `typescript` | refactor: Remove runtime toolchain dispatch |
| https://github.com/vercel/turborepo/pull/13582 | `vercel/turborepo` | `code_and_docs` | `typescript` | refactor: Port Cargo watch and prune knowledge |
| https://github.com/vercel/turborepo/pull/13581 | `vercel/turborepo` | `code_and_docs` | `typescript` | refactor: Port Cargo task and contract knowledge |
| https://github.com/vercel/turborepo/pull/13576 | `vercel/turborepo` | `code_and_docs` | `typescript` | refactor: Complete Cargo relationship and resolution knowledge |
| https://github.com/vercel/turborepo/pull/13572 | `vercel/turborepo` | `code_and_docs` | `typescript` | docs: Audit Cargo package knowledge |
| https://github.com/vercel/turborepo/pull/13571 | `vercel/turborepo` | `code_and_docs` | `typescript` | refactor: Migrate boundary diagnostics off PackageInfo |
| https://github.com/vercel/turborepo/pull/13564 | `vercel/turborepo` | `code_and_docs` | `typescript` | refactor: Remove residual runtime PackageInfo gates |
| https://github.com/vercel/turborepo/pull/13562 | `vercel/turborepo` | `code_and_docs` | `typescript` | refactor: Remove prune PackageInfo dependencies |
| https://github.com/vercel/turborepo/pull/13558 | `vercel/turborepo` | `code_and_docs` | `typescript` | refactor: Migrate MFE dependency detection off PackageInfo |
| https://github.com/vercel/turborepo/pull/13556 | `vercel/turborepo` | `code_and_docs` | `typescript` | refactor: Audit remaining JS knowledge consumer reads |
| https://github.com/vercel/turborepo/pull/13554 | `vercel/turborepo` | `code_and_docs` | `typescript` | refactor: Delete JS format interpretation from prune orchestration |
| https://github.com/vercel/turborepo/pull/13546 | `vercel/turborepo` | `code_only` | `typescript` | refactor: Separate prune rendering with golden coverage |
| https://github.com/apache/libcloud/pull/2183 | `apache/libcloud` | `code_only` | `python` | Bump astral-sh/setup-uv from 9.0.0 to 10.0.1 |
| https://github.com/apache/libcloud/pull/2168 | `apache/libcloud` | `code_and_docs` | `python` | [S3] Respect chunk_size in download_object_as_stream |
| https://github.com/apache/libcloud/pull/2173 | `apache/libcloud` | `code_and_docs` | `python` | [DigitalOcean] Include IPv6 addresses in node public/private IPs |
| https://github.com/apache/libcloud/pull/2175 | `apache/libcloud` | `code_and_docs` | `python` | [Cloudflare] Fix list_record_types advertising URL instead of LOC |
| https://github.com/apache/libcloud/pull/2174 | `apache/libcloud` | `code_only` | `python` | Bump astral-sh/setup-uv from 8.3.2 to 9.0.0 |
| https://github.com/apache/libcloud/pull/2169 | `apache/libcloud` | `code_and_docs` | `python` | [Azure Blobs] Forward chunk_size in download_object_as_stream |
| https://github.com/apache/libcloud/pull/2167 | `apache/libcloud` | `code_only` | `python` | Fix pypy test in dockerfile |
| https://github.com/apache/libcloud/pull/2166 | `apache/libcloud` | `code_only` | `python` | Add support for Python 3.14 in pyproject.toml |
| https://github.com/apache/libcloud/pull/2134 | `apache/libcloud` | `code_only` | `python` | Add support for axfr_ips and PTR records in Linode DNS v4 |
| https://github.com/apache/libcloud/pull/2161 | `apache/libcloud` | `code_only` | `python` | Bump actions/setup-python from 6 to 7 |
| https://github.com/apache/libcloud/pull/2162 | `apache/libcloud` | `code_only` | `python` | Bump codecov/codecov-action from e53489f4d376d79066609109e7a95a29eb3740b1 to fb8b3582c8e4def4969c97caa2f19720cb33a72f |
| https://github.com/apache/libcloud/pull/2156 | `apache/libcloud` | `code_only` | `python` | Bump pytest from 9.0.3 to 9.1.1 |
| https://github.com/apache/libcloud/pull/2159 | `apache/libcloud` | `code_and_docs` | `python` | Fix Azure ARM create_node JSON error with ex_customdata (#1893) |
| https://github.com/apache/libcloud/pull/2147 | `apache/libcloud` | `code_and_docs` | `python` | Add new functions to complete the Upcloud driver and move it to the last API version 1.3. |
| https://github.com/apache/libcloud/pull/2160 | `apache/libcloud` | `code_only` | `python` | Fix CodeQL atmos error |
| https://github.com/apache/libcloud/pull/2155 | `apache/libcloud` | `code_only` | `python` | Bump astral-sh/setup-uv from 8.3.0 to 8.3.2 |
| https://github.com/apache/libcloud/pull/2154 | `apache/libcloud` | `code_only` | `python` | Bump actions/cache from 5 to 6 |
| https://github.com/apache/libcloud/pull/2157 | `apache/libcloud` | `code_only` | `python` | Correct dependencies |
| https://github.com/apache/libcloud/pull/2152 | `apache/libcloud` | `code_only` | `python` | Move tests to py3.12. Implements #2146 |
| https://github.com/apache/libcloud/pull/2153 | `apache/libcloud` | `code_only` | `python` | Disable tests temporary to move to py12 |
| https://github.com/apache/libcloud/pull/2151 | `apache/libcloud` | `code_only` | `python` | Bump pytest-timeout from 2.3.1 to 2.4.0 |
| https://github.com/apache/libcloud/pull/2149 | `apache/libcloud` | `code_only` | `python` | Bump actions/checkout from 6 to 7 |
| https://github.com/apache/libcloud/pull/2148 | `apache/libcloud` | `code_only` | `python` | Bump astral-sh/setup-uv from 8.1.0 to 8.3.0 |
| https://github.com/apache/libcloud/pull/2141 | `apache/libcloud` | `code_only` | `python` | Bump actions/dependency-review-action from 4 to 5 |
| https://github.com/apache/libcloud/pull/2145 | `apache/libcloud` | `code_only` | `python` | Fix error in tests using paramiko > 4 |
| https://github.com/apache/libcloud/pull/2132 | `apache/libcloud` | `code_only` | `python` | Remove Linode APIv3 support |
| https://github.com/apache/libcloud/pull/2120 | `apache/libcloud` | `code_only` | `python` | Bump rstcheck from 6.2.4 to 6.2.5 |
| https://github.com/apache/libcloud/pull/2126 | `apache/libcloud` | `code_only` | `python` | Bump actions/upload-artifact from 6 to 7 |
| https://github.com/apache/libcloud/pull/2139 | `apache/libcloud` | `code_only` | `python` | Bump astral-sh/setup-uv from 7.1.6 to 8.1.0 |
| https://github.com/apache/libcloud/pull/2136 | `apache/libcloud` | `code_only` | `python` | Prepare release 3.9.1 |
| https://github.com/apache/libcloud/pull/2135 | `apache/libcloud` | `code_only` | `python` | Support paramiko 4 changes |
| https://github.com/apache/libcloud/pull/2137 | `apache/libcloud` | `code_only` | `python` | Update deps |
| https://github.com/apache/libcloud/pull/1415 | `apache/libcloud` | `code_only` | `python` | Try fixing Travis CI Windows build |
| https://github.com/apache/libcloud/pull/1326 | `apache/libcloud` | `code_and_docs` | `python` | Fix hash validation with stream uploads |
| https://github.com/apache/libcloud/pull/1716 | `apache/libcloud` | `code_only` | `python` | Bump actions/dependency-review-action from 1 to 2 |
| https://github.com/apache/libcloud/pull/1570 | `apache/libcloud` | `code_only` | `python` | Fix null value in DigitalOcean create a record |
| https://github.com/apache/libcloud/pull/1673 | `apache/libcloud` | `code_and_docs` | `python` | Fix error creating and getting node in OpenStack |
| https://github.com/apache/libcloud/pull/1525 | `apache/libcloud` | `code_only` | `python` | Storage: Add support for the SFO2 datacenter |
| https://github.com/apache/libcloud/pull/1579 | `apache/libcloud` | `code_and_docs` | `python` | Use pytest for running integration tests |
| https://github.com/apache/libcloud/pull/1708 | `apache/libcloud` | `code_only` | `python` | Bump actions/setup-dotnet from 1 to 2 |
| https://github.com/apache/libcloud/pull/1506 | `apache/libcloud` | `code_only` | `python` | allow vultr.list_nodes to return extra values |
| https://github.com/apache/libcloud/pull/1638 | `apache/libcloud` | `code_and_docs` | `python` | OpenStack: Move floating IP functions to use network service instead of nova |
| https://github.com/apache/libcloud/pull/1754 | `apache/libcloud` | `code_only` | `python` | Update development / testing Docker image, add new bandit lint check |
| https://github.com/apache/libcloud/pull/1762 | `apache/libcloud` | `code_only` | `python` | Also run pip audit check in dev / testing / lint dependency |
| https://github.com/apache/libcloud/pull/2049 | `apache/libcloud` | `code_only` | `python` | Initial Blazar support #2048 |
| https://github.com/apache/libcloud/pull/1630 | `apache/libcloud` | `code_and_docs` | `python` | Add Server Groups functions in OpenStack driver |
| https://github.com/apache/libcloud/pull/1522 | `apache/libcloud` | `code_only` | `python` | Fix for apache/libcloud #1521 |
| https://github.com/apache/libcloud/pull/1999 | `apache/libcloud` | `code_only` | `python` | Bump actions/upload-artifact from 3 to 4 |
| https://github.com/apache/libcloud/pull/1704 | `apache/libcloud` | `code_only` | `python` | Set minimum permissions got github token for GHA workflows |
| https://github.com/apache/libcloud/pull/1299 | `apache/libcloud` | `code_only_tests_or_fixtures` | `python` | Add test for changed made in PR #1295 |
| https://github.com/apache/libcloud/pull/1664 | `apache/libcloud` | `code_only` | `python` | Enable Retrying of Raw Requests parse_error |
| https://github.com/apache/libcloud/pull/1505 | `apache/libcloud` | `code_only` | `python` | dns/digitalocean: send attributes in body for PUT and POST operations. |
| https://github.com/apache/libcloud/pull/1844 | `apache/libcloud` | `code_only` | `python` | Bump json5 from 1.0.1 to 1.0.2 in /.github/actions/skip-duplicate-actions |
| https://github.com/apache/libcloud/pull/1549 | `apache/libcloud` | `code_and_docs` | `python` | Make libcloud compliant with the latest Outscale API. |
| https://github.com/apache/libcloud/pull/1637 | `apache/libcloud` | `code_and_docs` | `python` | Avoid raising exception if ip is not found: Fix #1595 |
| https://github.com/apache/libcloud/pull/1797 | `apache/libcloud` | `code_only` | `python` | Bump actions/dependency-review-action from 2 to 3 |
| https://github.com/apache/libcloud/pull/1977 | `apache/libcloud` | `code_only` | `python` | Bump actions/setup-python from 4 to 5 |
| https://github.com/apache/libcloud/pull/1959 | `apache/libcloud` | `code_only` | `python` | Bump build from 0.10.0 to 1.0.3 |
| https://github.com/apache/libcloud/pull/1620 | `apache/libcloud` | `code_and_docs` | `python` | Drop support for Python 3.5 |
| https://github.com/apache/libcloud/pull/1685 | `apache/libcloud` | `code_and_docs` | `python` | Fix compatibility with paramiko >= 2.9.0 and older OpenSSH server versions |
| https://github.com/apache/libcloud/pull/1793 | `apache/libcloud` | `code_only` | `python` | Bump actions/setup-dotnet from 3.0.2 to 3.0.3 |
| https://github.com/apache/libcloud/pull/1781 | `apache/libcloud` | `code_only` | `python` | Update the new US based locations. |
| https://github.com/apache/libcloud/pull/1622 | `apache/libcloud` | `code_and_docs` | `python` | Update development and test dependencies |
| https://github.com/apache/libcloud/pull/1697 | `apache/libcloud` | `code_only_tests_or_fixtures` | `python` | tests: add way to skip tests that require access to the network/Internet |
| https://github.com/apache/libcloud/pull/1621 | `apache/libcloud` | `code_and_docs` | `python` | [Google] Don't retry failed requests on auth when determining if GCE metadata server is available |
| https://github.com/apache/libcloud/pull/1616 | `apache/libcloud` | `code_only` | `python` | Integration tests changes and fixes |
| https://github.com/apache/libcloud/pull/2117 | `apache/libcloud` | `code_only` | `python` | Update vulnerable deps |
| https://github.com/apache/libcloud/pull/2079 | `apache/libcloud` | `code_only` | `python` | Consistent handling of HTTP/S proxy environment variables |
| https://github.com/apache/libcloud/pull/2122 | `apache/libcloud` | `code_only` | `python` | Add python 3.14 unit tests |
| https://github.com/apache/libcloud/pull/2038 | `apache/libcloud` | `code_and_docs` | `python` | RcodeZero Driver: fix issue when adding a record where a record with a different type already exists |
| https://github.com/apache/libcloud/pull/2058 | `apache/libcloud` | `code_and_docs` | `python` | Add signed upload to azure and s3 |
| https://github.com/apache/libcloud/pull/2121 | `apache/libcloud` | `code_only_tests_or_fixtures` | `python` | Fix error in py313 |
| https://github.com/apache/libcloud/pull/2060 | `apache/libcloud` | `code_only` | `python` | [GCP IMDS] Use fully qualified name |
| https://github.com/apache/libcloud/pull/2068 | `apache/libcloud` | `code_only` | `python` | Removal of zone_name from Cloudflare record response following API deprecation |
| https://github.com/apache/libcloud/pull/2063 | `apache/libcloud` | `code_only` | `python` | Add hypervisor_hostname attribute to OpenStack node |
| https://github.com/apache/libcloud/pull/2062 | `apache/libcloud` | `code_only` | `python` | Update US GovCloud AD endpoint for AZURE_ARM provider |
| https://github.com/apache/libcloud/pull/2113 | `apache/libcloud` | `code_only` | `python` | Bump requests-mock from 1.11.0 to 1.12.1 |
| https://github.com/apache/libcloud/pull/2112 | `apache/libcloud` | `code_only` | `python` | dep: bump test dependency libvirt to 12.0.0 . |
| https://github.com/apache/libcloud/pull/2115 | `apache/libcloud` | `code_only` | `python` | Release v3.9.0 version |
| https://github.com/apache/libcloud/pull/2105 | `apache/libcloud` | `code_only` | `python` | Update setuptools requirement from ~=75.3.0 to >=75.3,<80.11 |
| https://github.com/apache/libcloud/pull/2110 | `apache/libcloud` | `code_only` | `python` | Fix Build and Verify Docker Image test |
| https://github.com/apache/libcloud/pull/2102 | `apache/libcloud` | `code_and_docs` | `python` | Move dev deps from extras to uv dependency groups |
| https://github.com/apache/libcloud/pull/2106 | `apache/libcloud` | `code_only` | `python` | Bump bandit[toml] from 1.7.8 to 1.9.3 |
| https://github.com/apache/libcloud/pull/2103 | `apache/libcloud` | `code_only` | `python` | Bump astral-sh/setup-uv from 4 to 7 |
| https://github.com/apache/libcloud/pull/2108 | `apache/libcloud` | `code_only` | `python` | Fix scrape Azure prices |
| https://github.com/apache/libcloud/pull/2104 | `apache/libcloud` | `code_only` | `python` | Bump codecov/codecov-action from 5.4.3 to 5.5.2 |
| https://github.com/apache/libcloud/pull/2101 | `apache/libcloud` | `code_and_docs` | `python` | Add prek-based pre-commit setup and normalize whitespace |
| https://github.com/apache/libcloud/pull/2100 | `apache/libcloud` | `code_only` | `python` | Fix EC2 scrape pricing script |
| https://github.com/apache/libcloud/pull/2098 | `apache/libcloud` | `code_only` | `python` | Fix Trigger ReadTheDocs build |
| https://github.com/apache/libcloud/pull/2096 | `apache/libcloud` | `code_only` | `python` | Remove fake tasks added to revert name change in required tests  |
| https://github.com/apache/libcloud/pull/2072 | `apache/libcloud` | `code_only` | `python` | Bump codecov/codecov-action from 5.4.0 to 5.4.3 |
| https://github.com/apache/libcloud/pull/2095 | `apache/libcloud` | `code_only` | `python` | Revert name change in required tests |
| https://github.com/apache/libcloud/pull/2085 | `apache/libcloud` | `code_and_docs` | `python` | Adopt uv for dependency management and require Python 3.10 |
| https://github.com/apache/libcloud/pull/2093 | `apache/libcloud` | `code_only` | `python` | ci: Drop Python 3.9 checks |
| https://github.com/apache/libcloud/pull/2091 | `apache/libcloud` | `code_only` | `python` | ci: restore status checks for Lint and Docs |
| https://github.com/apache/libcloud/pull/2083 | `apache/libcloud` | `code_only` | `python` | Move test actions to python 3.10 |
| https://github.com/apache/libcloud/pull/2090 | `apache/libcloud` | `code_only` | `python` | chore: remove duplicated keys |
| https://github.com/apache/libcloud/pull/2089 | `apache/libcloud` | `code_only` | `python` | chore: touch .asf.yaml to try to refresh the config |
| https://github.com/apache/libcloud/pull/2087 | `apache/libcloud` | `code_only` | `python` | Refine ASF metadata and enable pull request options |
| https://github.com/apache/libcloud/pull/2086 | `apache/libcloud` | `code_and_docs` | `python` | ci: use first-party actions |
| https://github.com/apache/libcloud/pull/1976 | `apache/libcloud` | `code_only` | `python` | Bump actions/setup-dotnet from 3.2.0 to 4.0.0 |
| https://github.com/apache/libcloud/pull/2082 | `apache/libcloud` | `code_only` | `python` | ci: coalesce styles |
| https://github.com/apache/libcloud/pull/1920 | `apache/libcloud` | `code_only` | `python` | Also run unit tests under Python 3.12 beta |
| https://github.com/apache/libcloud/pull/1965 | `apache/libcloud` | `code_only` | `python` | Add resize node function for azure driver |
| https://github.com/apache/libcloud/pull/2028 | `apache/libcloud` | `code_and_docs` | `python` | Enable to specify port in OpenStack ex_attach_floating_ip_to_node #2027 |
| https://github.com/apache/libcloud/pull/2040 | `apache/libcloud` | `code_only` | `python` | Fix Incorrect bundle creation #2039 |
| https://github.com/apache/libcloud/pull/2008 | `apache/libcloud` | `code_only` | `python` | Bump github/codeql-action from 2 to 3 |
| https://github.com/apache/libcloud/pull/2055 | `apache/libcloud` | `code_only` | `python` | Update dev dependencies, fix typos |
| https://github.com/apache/libcloud/pull/2054 | `apache/libcloud` | `code_only` | `python` | Improve build + dist install checks |
| https://github.com/apache/libcloud/pull/2051 | `apache/libcloud` | `code_only` | `python` | Update Github status checks |
| https://github.com/apache/libcloud/pull/1940 | `apache/libcloud` | `code_only` | `python` | Fix inappropriate length comparison |
| https://github.com/apache/libcloud/pull/1572 | `apache/libcloud` | `code_and_docs` | `python` | Add integration tests for Azure Storage driver |
| https://github.com/apache/libcloud/pull/1663 | `apache/libcloud` | `code_and_docs` | `python` | Authenticate with Azure Ad for Provider AZURE_BLOBS |
| https://github.com/apache/libcloud/pull/1376 | `apache/libcloud` | `code_only` | `python` | Label support for GCP volumes |
| https://github.com/apache/libcloud/pull/1414 | `apache/libcloud` | `code_and_docs` | `python` | Fix incorrect type annotations in the base compute API |
| https://github.com/apache/libcloud/pull/1546 | `apache/libcloud` | `code_and_docs` | `python` | Fix authentication related regression in EC2 driver introduced in v3.3.0 |
| https://github.com/apache/libcloud/pull/1412 | `apache/libcloud` | `code_only` | `python` | Fix error getting node_id in OpenStack_1_1_FloatingIpAddress:  #1411 |
| https://github.com/apache/libcloud/pull/1564 | `apache/libcloud` | `code_and_docs` | `python` | Enable auth to Cloudflare DNS via API Tokens |
| https://github.com/apache/libcloud/pull/2024 | `apache/libcloud` | `code_and_docs` | `python` | Add new CI job which builds the release artifact, remove MANIFEST.in |
| https://github.com/apache/libcloud/pull/2016 | `apache/libcloud` | `code_only` | `python` | Add some extra fields in the OpenStack Network Object: #2015 |
| https://github.com/apache/libcloud/pull/2052 | `apache/libcloud` | `code_only_tests_or_fixtures` | `python` | Bump pyyaml from 5.1 to 5.4.1 in /.github/actions/gh-action-pip-audit/test/pyproject |
| https://github.com/apache/libcloud/pull/2033 | `apache/libcloud` | `code_and_docs` | `python` | Only call super() during MockHttp if required |
| https://github.com/apache/libcloud/pull/2053 | `apache/libcloud` | `code_only` | `python` | Bump codecov/codecov-action from 4.5.0 to 5.4.0 |
| https://github.com/apache/libcloud/pull/1453 | `apache/libcloud` | `code_and_docs` | `python` | Implement s3 get_object_cdn_url using pre-signed urls |
| https://github.com/apache/libcloud/pull/1957 | `apache/libcloud` | `code_and_docs` | `python` | [azure arm] delete VM OS disk if it is a managed disk |
| https://github.com/apache/libcloud/pull/1994 | `apache/libcloud` | `code_and_docs` | `python` | Bump pytest from 7.4.0 to 8.0.2 |
| https://github.com/apache/libcloud/pull/2023 | `apache/libcloud` | `code_only` | `python` | Bump twine from 4.0.2 to 5.1.1 |
| https://github.com/apache/libcloud/pull/1983 | `apache/libcloud` | `code_and_docs` | `python` | Enhance `KubeVirtNodeDriver` Compute Driver |
| https://github.com/apache/libcloud/pull/2020 | `apache/libcloud` | `code_only` | `python` | Bump codecov/codecov-action from 4.4.1 to 4.5.0 |
| https://github.com/apache/libcloud/pull/2019 | `apache/libcloud` | `code_only` | `python` | Bump build from 1.0.3 to 1.2.1 |
| https://github.com/apache/libcloud/pull/2011 | `apache/libcloud` | `code_only` | `python` | Bump codecov/codecov-action from 4.3.0 to 4.4.1 |
| https://github.com/apache/libcloud/pull/2003 | `apache/libcloud` | `code_only` | `python` | Bump codecov/codecov-action from 3.1.4 to 4.3.0 |
| https://github.com/apache/libcloud/pull/2002 | `apache/libcloud` | `code_only` | `python` | Bump actions/cache from 3 to 4 |
| https://github.com/apache/libcloud/pull/1972 | `apache/libcloud` | `code_only` | `python` | chore: Remove storage and volume interface implementation |
| https://github.com/apache/libcloud/pull/1971 | `apache/libcloud` | `code_only` | `python` | chore: Deprecate facility in the favor of metro |
| https://github.com/apache/libcloud/pull/1982 | `apache/libcloud` | `code_and_docs` | `python` | Add os_distro and os_version in OpenStack images #1981 |
| https://github.com/apache/libcloud/pull/1996 | `apache/libcloud` | `code_only` | `python` | added eu-west-3 AWS region  |
| https://github.com/apache/libcloud/pull/2000 | `apache/libcloud` | `code_only` | `python` | Bump actions/dependency-review-action from 3 to 4 |
| https://github.com/apache/libcloud/pull/1941 | `apache/libcloud` | `code_and_docs` | `python` | Remove support for Python 3.7 which is EOL |
| https://github.com/apache/libcloud/pull/1973 | `apache/libcloud` | `code_only` | `python` | fix for TB in list_sizes for eqnx |
| https://github.com/apache/libcloud/pull/1954 | `apache/libcloud` | `code_only` | `python` | Add VPC IP and Elastic IP to ECS node as private and public IP |
| https://github.com/apache/libcloud/pull/1946 | `apache/libcloud` | `code_and_docs` | `python` | Updated Linode (Akamai Connected Cloud) support (including cloud-init) |
| https://github.com/apache/libcloud/pull/1944 | `apache/libcloud` | `code_only` | `python` | Make classes inheriting from Type hashable |
| https://github.com/apache/libcloud/pull/1950 | `apache/libcloud` | `code_only` | `python` | S3 eu south |
| https://github.com/apache/libcloud/pull/1952 | `apache/libcloud` | `code_only` | `python` | Bump actions/checkout from 3 to 4 |
| https://github.com/apache/libcloud/pull/1937 | `apache/libcloud` | `code_and_docs` | `python` | Sphinx API docs improvements |
| https://github.com/apache/libcloud/pull/1933 | `apache/libcloud` | `code_and_docs` | `python` | Update changelog documentation file to link to Github and Jira issues |
| https://github.com/apache/libcloud/pull/1796 | `apache/libcloud` | `code_only` | `python` | Fix Aliyun OSS storage upload_object KeyError: 'ETag' issue |
| https://github.com/apache/libcloud/pull/1847 | `apache/libcloud` | `code_and_docs` | `python` | optimize read_in_chunks |
| https://github.com/apache/libcloud/pull/1875 | `apache/libcloud` | `code_only` | `python` | Support all S3 storage classes |
| https://github.com/apache/libcloud/pull/1877 | `apache/libcloud` | `code_only` | `python` | Fix list_volumes, and list_nodes in Outscale provider |
| https://github.com/apache/libcloud/pull/1884 | `apache/libcloud` | `code_only` | `python` | Fix exception when using internal URL |
| https://github.com/apache/libcloud/pull/1886 | `apache/libcloud` | `code_only` | `python` | [OpenStack] Reuse connections to same host/port |
| https://github.com/apache/libcloud/pull/1891 | `apache/libcloud` | `code_only` | `python` | Fix list_volumes in the Azure arm driver |
| https://github.com/apache/libcloud/pull/1904 | `apache/libcloud` | `code_only` | `python` | Bump DISK_API_VERSION for Premium v2 SSDs |
| https://github.com/apache/libcloud/pull/1906 | `apache/libcloud` | `code_only` | `python` | BaseEC2NodeDriver.ex_register_image: support additional parameters |
| https://github.com/apache/libcloud/pull/1916 | `apache/libcloud` | `code_only` | `python` | fixed `ValueError` error when iterating over `meta_data` dictionary inside `_perform_upload` function for `BackblazeB2StorageDriver` |
| https://github.com/apache/libcloud/pull/1925 | `apache/libcloud` | `code_only` | `python` | Remove deprecated and unused ApiDocs command from setup.py |
| https://github.com/apache/libcloud/pull/1926 | `apache/libcloud` | `code_only` | `python` | Fix tox dist install checks |
| https://github.com/apache/libcloud/pull/1928 | `apache/libcloud` | `code_and_docs` | `python` | Also run unit tests under PyPy 3.8 |
| https://github.com/apache/libcloud/pull/1929 | `apache/libcloud` | `code_and_docs` | `python` | Migrate from setup.py to pyproject.toml |
| https://github.com/apache/libcloud/pull/1811 | `apache/libcloud` | `code_and_docs` | `python` | Drop support for Python 3.6  |
| https://github.com/apache/libcloud/pull/1807 | `apache/libcloud` | `code_only` | `python` | Fix google oauth desktop |
| https://github.com/apache/libcloud/pull/1818 | `apache/libcloud` | `code_and_docs` | `python` | Indicate we support Python 3.11, run tests under 3.11 |
| https://github.com/apache/libcloud/pull/1821 | `apache/libcloud` | `code_only` | `python` | Add support for af south 1 in s3 driver |
| https://github.com/apache/libcloud/pull/1279 | `apache/libcloud` | `code_and_docs` | `python` | Make tests pass after 2031 |
| https://github.com/apache/libcloud/pull/1785 | `apache/libcloud` | `code_only` | `python` | Bump actions/setup-dotnet from 3.0.1 to 3.0.2 |
| https://github.com/apache/libcloud/pull/1778 | `apache/libcloud` | `code_only` | `python` | Bump actions/setup-dotnet from 3.0.0 to 3.0.1 |
| https://github.com/apache/libcloud/pull/1773 | `apache/libcloud` | `code_only` | `python` | Bump actions/setup-dotnet from 2 to 3.0.0 |
| https://github.com/apache/libcloud/pull/1732 | `apache/libcloud` | `code_and_docs` | `python` | Add a new OVH driver for storage |
| https://github.com/apache/libcloud/pull/1676 | `apache/libcloud` | `code_and_docs` | `python` | Fix #1675: Error in volume api calls if microversion is set in OpenStack |
| https://github.com/apache/libcloud/pull/1677 | `apache/libcloud` | `code_and_docs` | `python` | Attach/Detach a Floating IP to an OpenStack node does not work with new versions |
| https://github.com/apache/libcloud/pull/1681 | `apache/libcloud` | `code_only` | `python` | Add expires condition |
| https://github.com/apache/libcloud/pull/1683 | `apache/libcloud` | `code_only` | `python` | Fix crash on missing etag in s3 storage driver |
| https://github.com/apache/libcloud/pull/1690 | `apache/libcloud` | `code_only_tests_or_fixtures` | `python` | test/test_http.py: stop HTTP server (thread) properly |
| https://github.com/apache/libcloud/pull/1691 | `apache/libcloud` | `code_and_docs` | `python` | Replace 3rd party mock package with unittest.mock package from stdlib |
| https://github.com/apache/libcloud/pull/1692 | `apache/libcloud` | `code_only_tests_or_fixtures` | `python` | tests/test_connection.py: fix test failing when https_proxy is set |
| https://github.com/apache/libcloud/pull/1693 | `apache/libcloud` | `code_only_tests_or_fixtures` | `python` | test: fix test_ssh_client on big-endian architectures |
| https://github.com/apache/libcloud/pull/1694 | `apache/libcloud` | `code_only_tests_or_fixtures` | `python` | Use tuple to compare versions for test against Paramiko. |
| https://github.com/apache/libcloud/pull/1695 | `apache/libcloud` | `code_only` | `python` | make content-type header is optional to work with S3 servers that do not support content-type header |
| https://github.com/vercel/swr/pull/4315 | `vercel/swr` | `code_only` | `typescript` | chore: bump version to 2.5.1 |
| https://github.com/vercel/swr/pull/4310 | `vercel/swr` | `code_only` | `typescript` | fix: clean up completed subscription state |
| https://github.com/vercel/swr/pull/4312 | `vercel/swr` | `code_only` | `typescript` | fix: revalidate suspense cacheData on remount |
| https://github.com/vercel/swr/pull/4293 | `vercel/swr` | `code_only` | `typescript` | fix: hydrate cacheData for hooks without a fetcher |
| https://github.com/vercel/swr/pull/4309 | `vercel/swr` | `code_only` | `typescript` | 2.5.0 |
| https://github.com/vercel/swr/pull/4307 | `vercel/swr` | `code_only` | `typescript` | chore: upgrade bunchee to 7.0.0 |
| https://github.com/vercel/swr/pull/4305 | `vercel/swr` | `code_only` | `typescript` | chore: upgrade to TypeScript 7 |
| https://github.com/vercel/swr/pull/4304 | `vercel/swr` | `code_only` | `typescript` | chore: bump bunchee to 6.12.2 |
| https://github.com/vercel/swr/pull/4299 | `vercel/swr` | `code_only` | `typescript` | 2.5.0-beta.1 |
| https://github.com/vercel/swr/pull/4298 | `vercel/swr` | `code_only` | `typescript` | feat: unload() api |
| https://github.com/vercel/swr/pull/4275 | `vercel/swr` | `code_only` | `typescript` | feat: rsc fetches and prefill swr cache |
| https://github.com/vercel/swr/pull/4291 | `vercel/swr` | `code_only` | `typescript` | 2.5.0-beta.0 |
| https://github.com/vercel/swr/pull/4288 | `vercel/swr` | `code_only` | `typescript` | chore: use oxfmt and oxlint |
| https://github.com/vercel/swr/pull/4272 | `vercel/swr` | `code_only` | `typescript` | fix: point _internal react-server export at existing file |
| https://github.com/vercel/swr/pull/4280 | `vercel/swr` | `code_only_tests_or_fixtures` | `typescript` | ci: remove legacy release from the test pipeline |
| https://github.com/vercel/swr/pull/4279 | `vercel/swr` | `code_only` | `typescript` | 2.4.2 |
| https://github.com/vercel/swr/pull/4278 | `vercel/swr` | `code_only` | `typescript` | ci: update release job |
| https://github.com/vercel/swr/pull/4277 | `vercel/swr` | `code_only` | `typescript` | ci: remove registry url |
| https://github.com/vercel/swr/pull/4274 | `vercel/swr` | `code_only_tests_or_fixtures` | `typescript` | ci: switch npm publish to OIDC trusted publishing |
| https://github.com/vercel/swr/pull/4271 | `vercel/swr` | `code_only` | `typescript` | Prevent resolved promise to suspend due to missing status |
| https://github.com/vercel/swr/pull/4263 | `vercel/swr` | `code_and_docs` | `typescript` | chore: remove the axios examples |
| https://github.com/vercel/swr/pull/4254 | `vercel/swr` | `code_only` | `typescript` | ci: update GitHub Actions for Node 24 |
| https://github.com/vercel/swr/pull/4258 | `vercel/swr` | `code_only` | `typescript` | chore: pin pnpm 10.33.0 |
| https://github.com/vercel/swr/pull/4252 | `vercel/swr` | `code_only` | `typescript` | fix: guard against double-unsubscribe removing wrong subscriber in cache.ts |
| https://github.com/vercel/swr/pull/4243 | `vercel/swr` | `code_only` | `typescript` | Security: Update axios versions in the examples |
| https://github.com/vercel/swr/pull/4223 | `vercel/swr` | `code_only` | `typescript` | fix: Fix #4221 |
| https://github.com/vercel/swr/pull/4216 | `vercel/swr` | `code_only` | `typescript` | Remove deprecated downlevelIteration option |
| https://github.com/vercel/swr/pull/4212 | `vercel/swr` | `code_only` | `typescript` | fix: isHydration will cause unnecessary rerender  |
| https://github.com/vercel/swr/pull/4213 | `vercel/swr` | `code_only` | `typescript` | fix: Ensure preload runs only on client |
| https://github.com/vercel/swr/pull/4209 | `vercel/swr` | `code_only` | `typescript` | fix: extra render when changing to new key with useSWRImmutable |
| https://github.com/vercel/swr/pull/4208 | `vercel/swr` | `code_only` | `typescript` | fix: Ensure useSWRImmutable overrides global refreshInterval |
| https://github.com/vercel/swr/pull/4206 | `vercel/swr` | `code_only_tests_or_fixtures` | `typescript` | ci: add missing flag for canary test |
| https://github.com/vercel/swr/pull/4202 | `vercel/swr` | `code_only_tests_or_fixtures` | `typescript` | test: Import `act` from React |
| https://github.com/vercel/swr/pull/4203 | `vercel/swr` | `code_only` | `typescript` | enhance: Improve TSDoc comments |
| https://github.com/vercel/swr/pull/4200 | `vercel/swr` | `code_only` | `typescript` | update dev dependencies to address cve |
| https://github.com/vercel/swr/pull/4199 | `vercel/swr` | `code_only` | `typescript` | upgrade dev dep nextjs |
| https://github.com/vercel/swr/pull/4198 | `vercel/swr` | `code_only` | `typescript` | fix: cve-2025-55184 & CVE-2025-55183 |
| https://github.com/vercel/swr/pull/4192 | `vercel/swr` | `code_only` | `typescript` | fix: cve-2025-55182 critical rce vulnerability |
| https://github.com/vercel/swr/pull/4189 | `vercel/swr` | `code_only` | `typescript` | update use-sync-external-store to latest |
| https://github.com/vercel/swr/pull/4188 | `vercel/swr` | `code_only` | `typescript` | deps: upgrade dev deps for build |
| https://github.com/vercel/swr/pull/4183 | `vercel/swr` | `code_only` | `typescript` | feat: Add `strictServerPrefetchWarning` |
| https://github.com/vercel/swr/pull/4187 | `vercel/swr` | `code_only` | `typescript` | deps: upgrade eslint version and fix lint problem |
| https://github.com/vercel/swr/pull/4186 | `vercel/swr` | `code_only` | `typescript` | deps: upgrade playwright version |
| https://github.com/vercel/swr/pull/4184 | `vercel/swr` | `code_only` | `typescript` | deps: upgrade ci node version to 22 |
| https://github.com/vercel/swr/pull/4156 | `vercel/swr` | `code_only` | `typescript` | fix: do not error when not enabled during suspense |
| https://github.com/vercel/swr/pull/4154 | `vercel/swr` | `code_only` | `typescript` | test: e2e test for 2702 |
| https://github.com/vercel/swr/pull/4150 | `vercel/swr` | `code_only` | `typescript` | fix: react.use should not depend on data condition |
| https://github.com/vercel/swr/pull/4151 | `vercel/swr` | `code_only` | `typescript` | Revert "feat: modify cache type to allow generic usage" |
| https://github.com/vercel/swr/pull/2947 | `vercel/swr` | `code_only` | `typescript` | feat: modify cache type to allow generic usage |
| https://github.com/vercel/swr/pull/4076 | `vercel/swr` | `code_only` | `typescript` | doc: Sync `PublicConfiguration.onDiscarded` tsdoc with SWR official website |
| https://github.com/vercel/swr/pull/4110 | `vercel/swr` | `code_only` | `typescript` | perf: optimize `useSWRConfig` with `useMemo` to maintain stable reference |
| https://github.com/vercel/swr/pull/4138 | `vercel/swr` | `code_only` | `typescript` | fix: Optimize the revalidation logic for same key requests. |
| https://github.com/vercel/swr/pull/4092 | `vercel/swr` | `code_only` | `typescript` | fix: Performance improvement by reducing calls to toString() |
| https://github.com/vercel/swr/pull/4126 | `vercel/swr` | `code_and_docs` | `typescript` | feat: Improve global suspense-enabled `data` type |
| https://github.com/vercel/swr/pull/4118 | `vercel/swr` | `code_only` | `typescript` | fix: check "if (!error)" skip error if value is cast to false |
| https://github.com/vercel/swr/pull/4075 | `vercel/swr` | `code_only` | `typescript` | refactor: type improvement of `useSWRHandler` |
| https://github.com/vercel/swr/pull/2857 | `vercel/swr` | `code_only` | `typescript` | Initialise nextFocusRevalidatedAt on mount |
| https://github.com/vercel/swr/pull/4099 | `vercel/swr` | `code_only` | `typescript` | enhance: use empty prototype object |
| https://github.com/vercel/swr/pull/3027 | `vercel/swr` | `code_only` | `typescript` | Improve-Type-Safety-and-State-Access-in-useStateWithDeps-Hook |
| https://github.com/vercel/swr/pull/4087 | `vercel/swr` | `code_only` | `typescript` | (fix) keepPreviousData: return fallback instead of undefined value |
| https://github.com/vercel/swr/pull/4086 | `vercel/swr` | `code_only` | `typescript` | build: bump bundler |
| https://github.com/vercel/swr/pull/4084 | `vercel/swr` | `code_only` | `typescript` | keepPreviousData: return fallback instead of undefined value |
| https://github.com/vercel/swr/pull/4085 | `vercel/swr` | `code_only` | `typescript` | ci: update pnpm setup and lock pnpm vesion |
| https://github.com/vercel/swr/pull/4064 | `vercel/swr` | `code_only` | `typescript` | fix: sever env detection for deno |
| https://github.com/vercel/swr/pull/2891 | `vercel/swr` | `code_only` | `typescript` | [Experimental] Support promises as fallback data |
| https://github.com/vercel/swr/pull/2301 | `vercel/swr` | `code_only` | `typescript` | types: conditional swr response |
| https://github.com/vercel/swr/pull/2915 | `vercel/swr` | `code_only` | `typescript` | fix: Replace the deprecated 'window' with 'globalThis' for Deno |
| https://github.com/vercel/swr/pull/3054 | `vercel/swr` | `code_only` | `typescript` | fix: missing `throwOnError` in SWRMutationHook options |
| https://github.com/vercel/swr/pull/3052 | `vercel/swr` | `code_only_tests_or_fixtures` | `typescript` | fix type check in tests |
| https://github.com/vercel/swr/pull/3050 | `vercel/swr` | `code_only` | `typescript` | upgrade use-sync-external-store to support react 19 |
| https://github.com/vercel/swr/pull/3049 | `vercel/swr` | `code_only` | `typescript` | Bump bundler and reorganize serialize exports |
| https://github.com/vercel/swr/pull/3048 | `vercel/swr` | `code_only` | `typescript` | chore: reorganize entries |
| https://github.com/vercel/swr/pull/2770 | `vercel/swr` | `code_only` | `typescript` | ci: simplify ci config and bump some deps version |
| https://github.com/vercel/swr/pull/3047 | `vercel/swr` | `code_only` | `typescript` | Update React 19 peer dependency version |
| https://github.com/vercel/swr/pull/3045 | `vercel/swr` | `code_only` | `typescript` | fix: Only suspend when using the `fallback` |
| https://github.com/vercel/swr/pull/3036 | `vercel/swr` | `code_only` | `typescript` | fix #3030 and run relateive test in edge-runtime |
| https://github.com/vercel/swr/pull/3044 | `vercel/swr` | `code_only` | `typescript` | chore: upgrade nextjs dev dep for e2e testing |
| https://github.com/vercel/swr/pull/1174 | `vercel/swr` | `code_only` | `typescript` | enhance: add $ prefix for non-major keys |
| https://github.com/vercel/swr/pull/2973 | `vercel/swr` | `code_only` | `typescript` | fix: Improve comparison performance |
| https://github.com/vercel/swr/pull/2905 | `vercel/swr` | `code_only` | `typescript` | examples: add RSC streaming pre-render with promise fallback example |
| https://github.com/vercel/swr/pull/2963 | `vercel/swr` | `code_only` | `typescript` | chore: add react peerDeps 19 |
| https://github.com/vercel/swr/pull/2900 | `vercel/swr` | `code_only` | `typescript` | fix(infinte): export SWRInfiniteKeyedMutator type |
| https://github.com/vercel/swr/pull/2913 | `vercel/swr` | `code_only` | `typescript` | fix: check if config.fallback is undefined |
| https://github.com/vercel/swr/pull/2937 | `vercel/swr` | `code_only` | `typescript` | Export ScopedMutator type |
| https://github.com/vercel/swr/pull/2954 | `vercel/swr` | `code_only` | `typescript` | Add SWRInfiniteMutatorOptions type to export |
| https://github.com/vercel/swr/pull/2955 | `vercel/swr` | `code_only_tests_or_fixtures` | `typescript` | test: update the revalidate function test for useSWRInfinite |
| https://github.com/vercel/swr/pull/2952 | `vercel/swr` | `code_only` | `typescript` | ci: fix ci error and upgrade action version |
| https://github.com/vercel/swr/pull/2862 | `vercel/swr` | `code_only` | `typescript` | feat: pass a function to the revalidate option in mutate |
| https://github.com/vercel/swr/pull/2932 | `vercel/swr` | `code_only` | `typescript` | Fix bundling of client entry chunks  |
| https://github.com/vercel/swr/pull/2929 | `vercel/swr` | `code_only` | `typescript` | build: bump bundler for perf |
| https://github.com/vercel/swr/pull/2918 | `vercel/swr` | `code_only_tests_or_fixtures` | `typescript` | test: remove console.error times check |
| https://github.com/vercel/swr/pull/2920 | `vercel/swr` | `code_only` | `typescript` | chore: update pkg script watch |
| https://github.com/vercel/swr/pull/2911 | `vercel/swr` | `code_only` | `typescript` | Drop exports module field |
| https://github.com/vercel/swr/pull/2904 | `vercel/swr` | `code_only` | `typescript` | Mark package as side-effect free |
| https://github.com/vercel/swr/pull/2897 | `vercel/swr` | `code_only` | `typescript` | build: simplify react-server export and update bundler |
| https://github.com/vercel/swr/pull/2910 | `vercel/swr` | `code_only` | `typescript` | Drop client-only |
| https://github.com/vercel/swr/pull/2909 | `vercel/swr` | `code_only` | `typescript` | chore: simplify test coverage strategy |
| https://github.com/vercel/swr/pull/2903 | `vercel/swr` | `code_only` | `typescript` | chore: Improve test coverage |
| https://github.com/vercel/swr/pull/2895 | `vercel/swr` | `code_only` | `typescript` | build: fix beta release job |
| https://github.com/vercel/swr/pull/2894 | `vercel/swr` | `code_only` | `typescript` | chore: bump dev deps and change example react version to latest |
| https://github.com/vercel/swr/pull/2882 | `vercel/swr` | `code_only` | `typescript` | fix: SWRConfiguration type |
| https://github.com/vercel/swr/pull/2848 | `vercel/swr` | `code_only` | `typescript` | fix: allow onErrorRetry on inactive tab without focus/reconnect revalidation |
| https://github.com/vercel/swr/pull/2875 | `vercel/swr` | `code_only` | `typescript` | types: isLoading typed as boolean when using fallbackData (#2866) |
| https://github.com/vercel/swr/pull/2868 | `vercel/swr` | `code_only` | `typescript` | chore: remove useless comment |
| https://github.com/vercel/swr/pull/2874 | `vercel/swr` | `code_only` | `typescript` | chore: update pnpm-lock.yaml |
| https://github.com/vercel/swr/pull/2872 | `vercel/swr` | `code_only_tests_or_fixtures` | `typescript` | test: run pnpm test on CI |
| https://github.com/vercel/swr/pull/2861 | `vercel/swr` | `code_only_tests_or_fixtures` | `typescript` | fix: all act warnings |
| https://github.com/vercel/swr/pull/2756 | `vercel/swr` | `code_only` | `typescript` | fix: It should use startTransition only when IS_REACT_LEGACY is false |
| https://github.com/vercel/swr/pull/2753 | `vercel/swr` | `code_only` | `typescript` | fix: default to fetch type in keyed mutator |
| https://github.com/vercel/swr/pull/2182 | `vercel/swr` | `code_only` | `typescript` | breaking: Change the error broadcasting behavior in mutations and add `throwOnError` option |
| https://github.com/vercel/swr/pull/2830 | `vercel/swr` | `code_only` | `typescript` | Update bundler |
| https://github.com/vercel/swr/pull/1 | `vercel/swr` | `code_only` | `typescript` | Fix repo and homepage in `package.json` |
| https://github.com/vercel/swr/pull/2802 | `vercel/swr` | `code_only` | `typescript` | Revert "Remove `index.js` suffix of `use-sync-external-store/shim` to support React Native" |
| https://github.com/vercel/swr/pull/2767 | `vercel/swr` | `code_only` | `typescript` | Remove `index.js` suffix of `use-sync-external-store/shim` to support React Native |
| https://github.com/vercel/swr/pull/2781 | `vercel/swr` | `code_only_tests_or_fixtures` | `typescript` | test: update tests, use matched types for mutate api |
| https://github.com/vercel/swr/pull/2780 | `vercel/swr` | `code_only` | `typescript` | types: export mutation types |
| https://github.com/vercel/swr/pull/2759 | `vercel/swr` | `code_only` | `typescript` | fix: remove permissive type |
| https://github.com/vercel/swr/pull/2761 | `vercel/swr` | `code_only` | `typescript` | fix: simplify `ArgumentsTuple` |
| https://github.com/vercel/swr/pull/2668 | `vercel/swr` | `code_only` | `typescript` | Pass displayed data as second parameter of functional optimistic data |
| https://github.com/vercel/swr/pull/2506 | `vercel/swr` | `code_only` | `typescript` | fix: swr infers incorrect `data` type for default `SWRConfig` generic type |
| https://github.com/vercel/swr/pull/2734 | `vercel/swr` | `code_and_docs` | `typescript` | docs: use isLoading instead of !data |
| https://github.com/vercel/swr/pull/2736 | `vercel/swr` | `code_only` | `typescript` | build(deps-dev): bump json5 from 2.2.1 to 2.2.3 |
| https://github.com/vercel/swr/pull/2735 | `vercel/swr` | `code_only` | `typescript` | build(deps-dev): bump tough-cookie from 4.1.2 to 4.1.3 |
| https://github.com/vercel/swr/pull/2708 | `vercel/swr` | `code_only` | `typescript` | fix(mutate): fix types of mutate/trigger; make mutate/trigger always return the result of fetcher |
| https://github.com/vercel/swr/pull/2731 | `vercel/swr` | `code_only` | `typescript` | Fix the issue that useSWR revalidation isn't triggered if the useSWR call happens after mutation |
| https://github.com/vercel/swr/pull/2727 | `vercel/swr` | `code_only` | `typescript` | fix: preload request should be consumed within `revalidate` to support `parallel` option |
| https://github.com/vercel/swr/pull/2726 | `vercel/swr` | `code_only` | `typescript` | fix: Ensure that using preload with useSWRInfinite returns back an array of data |
| https://github.com/vercel/swr/pull/2723 | `vercel/swr` | `code_only` | `typescript` | fix(infinite): Fix the ability to use preload along with useSWRInfinite |
| https://github.com/vercel/swr/pull/2695 | `vercel/swr` | `code_only` | `typescript` | build: generate d.mts for for .mjs, so typescript could resolve types correctly |
| https://github.com/vercel/swr/pull/2691 | `vercel/swr` | `code_only` | `typescript` | fix: only make data and error update as a non-blocking transition |
| https://github.com/vercel/swr/pull/2720 | `vercel/swr` | `code_only` | `typescript` | build(deps-dev): bump word-wrap from 1.2.3 to 1.2.4 |
| https://github.com/vercel/swr/pull/2711 | `vercel/swr` | `code_only` | `typescript` | fix: should serialize subscription fn key |
| https://github.com/vercel/swr/pull/2705 | `vercel/swr` | `code_only` | `typescript` | remove the 'use client' directive and add client-only to useSWR entry. |
| https://github.com/vercel/swr/pull/2563 | `vercel/swr` | `code_only` | `typescript` | types: Allow auto-import by improving generated types |
| https://github.com/vercel/swr/pull/2696 | `vercel/swr` | `code_only` | `typescript` | Add use client directive for client components exports |
| https://github.com/vercel/swr/pull/2671 | `vercel/swr` | `code_only` | `typescript` | test: add e2e test for react-server entry |
| https://github.com/vercel/swr/pull/2681 | `vercel/swr` | `code_only` | `typescript` | Revert "fix: remove startTransition so mutation hook could update immediately (#2654)" |
| https://github.com/vercel/swr/pull/2654 | `vercel/swr` | `code_only` | `typescript` | fix: remove `startTransition` so mutation hook could update immediately |
| https://github.com/vercel/swr/pull/2677 | `vercel/swr` | `code_only` | `typescript` | build: fix conflict types for index and index.react-server |
| https://github.com/vercel/swr/pull/2673 | `vercel/swr` | `code_only` | `typescript` | Adjust rsc exports |
| https://github.com/vercel/swr/pull/2666 | `vercel/swr` | `code_only` | `typescript` | Fix Conditional Typing in useSWRMutation to Allow Optional ExtraArg Without Explicitly Passing Undefined |
| https://github.com/vercel/swr/pull/2670 | `vercel/swr` | `code_only` | `typescript` | types: fix immutable export paths |
| https://github.com/vercel/swr/pull/2592 | `vercel/swr` | `code_only` | `typescript` | fix: reset the error when mutate succeeded |
| https://github.com/vercel/swr/pull/2669 | `vercel/swr` | `code_only` | `typescript` | Fix mutation types order |
| https://github.com/vercel/swr/pull/2658 | `vercel/swr` | `code_only` | `typescript` | feat: improve preload and suspense integration |
| https://github.com/vercel/swr/pull/2657 | `vercel/swr` | `code_only_tests_or_fixtures` | `typescript` | test: improve preload test |
| https://github.com/vercel/swr/pull/2655 | `vercel/swr` | `code_only_tests_or_fixtures` | `typescript` | test: fix flaky suspense test in canary |
| https://github.com/vercel/swr/pull/2386 | `vercel/swr` | `code_only` | `typescript` | fix: when inifinite key changes, should use cached pagesize instead of initialSize |
| https://github.com/vercel/swr/pull/2431 | `vercel/swr` | `code_only` | `typescript` | refactor: remove useless dataRef, always compare cached data |
| https://github.com/vercel/swr/pull/2479 | `vercel/swr` | `code_only` | `typescript` | refactor: initialize the cache only on first access |
| https://github.com/vercel/swr/pull/2649 | `vercel/swr` | `code_only` | `typescript` | fix: keepPreviousData should also work in suspense |
| https://github.com/vercel/swr/pull/2651 | `vercel/swr` | `code_only` | `typescript` | ci: use script to bump semver version |
| https://github.com/vercel/swr/pull/2648 | `vercel/swr` | `code_only` | `typescript` | fix: do unsubscribe synchronously |
| https://github.com/vercel/swr/pull/2604 | `vercel/swr` | `code_only` | `typescript` | types: improve `useSWRMutation` type. |
| https://github.com/vercel/swr/pull/2605 | `vercel/swr` | `code_and_docs` | `typescript` | chore: upgrade to pnpm8 |
| https://github.com/vercel/swr/pull/2637 | `vercel/swr` | `code_only` | `typescript` | ci: use gh token credentials for cloning repo |
| https://github.com/vercel/swr/pull/2636 | `vercel/swr` | `code_only` | `typescript` | ci: update github token |
| https://github.com/vercel/swr/pull/2630 | `vercel/swr` | `code_only` | `typescript` | build: fix release semver |
| https://github.com/vercel/swr/pull/2629 | `vercel/swr` | `code_only` | `typescript` | build: fix bad runner |
| https://github.com/vercel/swr/pull/2628 | `vercel/swr` | `code_only` | `typescript` | build: fix equal signs |
| https://github.com/vercel/swr/pull/2627 | `vercel/swr` | `code_only` | `typescript` | build: use prepatch/minor/major command for prerelease |
| https://github.com/vercel/swr/pull/2624 | `vercel/swr` | `code_only` | `typescript` | ci: drop unused inputs and step |
| https://github.com/vercel/swr/pull/2616 | `vercel/swr` | `code_only` | `typescript` | build: determin release tag |
| https://github.com/vercel/swr/pull/2615 | `vercel/swr` | `code_only` | `typescript` | build: add trigger release job |
| https://github.com/vercel/swr/pull/2601 | `vercel/swr` | `code_only` | `typescript` | ci: Add daily test job for react canary |
| https://github.com/vercel/swr/pull/2596 | `vercel/swr` | `code_only` | `typescript` | feat: use `React.use` API |
| https://github.com/vercel/swr/pull/2583 | `vercel/swr` | `code_only` | `typescript` | test: add a new test setting to run tests with build files |
| https://github.com/vercel/swr/pull/2582 | `vercel/swr` | `code_only` | `typescript` | fix: missing interop helpers in bundle |
| https://github.com/vercel/swr/pull/2578 | `vercel/swr` | `code_only` | `typescript` | deps: update @testing-library/react to v14 |
| https://github.com/vercel/swr/pull/2576 | `vercel/swr` | `code_only` | `typescript` | fix: Fix dependency tracking and useSES bug |
| https://github.com/vercel/swr/pull/2577 | `vercel/swr` | `code_only` | `typescript` | refactor: update `memorizedSanpshot` without changing its reference  |
| https://github.com/vercel/swr/pull/2571 | `vercel/swr` | `code_only_tests_or_fixtures` | `typescript` | chore: use provenance for release |
| https://github.com/vercel/swr/pull/2564 | `vercel/swr` | `code_only` | `typescript` | fix: pass serialized args to preload fetcher |
| https://github.com/vercel/swr/pull/2559 | `vercel/swr` | `code_only` | `typescript` | examples: fix invalid links |
| https://github.com/vercel/swr/pull/2557 | `vercel/swr` | `code_only` | `typescript` | Upgrade bundler |
| https://github.com/vercel/swr/pull/2551 | `vercel/swr` | `code_only` | `typescript` | types: allow passing function as `Data` for `useSWRSubscriptionOptions` |
| https://github.com/vercel/swr/pull/2354 | `vercel/swr` | `code_only` | `typescript` | fix: data passed to refreshInterval function is not latest |
| https://github.com/vercel/swr/pull/2554 | `vercel/swr` | `code_only` | `typescript` | Update Cache Interface types |
| https://github.com/vercel/swr/pull/2552 | `vercel/swr` | `code_only` | `typescript` | Examples: fix type in axios-typescript example |
| https://github.com/vercel/swr/pull/2550 | `vercel/swr` | `code_only` | `typescript` | Fix #2548: pass origin key to subcription callback |
| https://github.com/apache/iceberg-python/pull/3724 | `apache/iceberg-python` | `code_and_docs` | `python` | feat: Add async REST scan planning poll and plan storage credentials |
| https://github.com/apache/iceberg-python/pull/3818 | `apache/iceberg-python` | `code_only` | `python` | Fail when explicitly deleted data file is missing |
| https://github.com/apache/iceberg-python/pull/3831 | `apache/iceberg-python` | `code_only` | `python` | Fix strict evaluation for negative record counts |
| https://github.com/apache/iceberg-python/pull/3823 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump the codeql-action group with 2 updates |
| https://github.com/apache/iceberg-python/pull/3822 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump pytest-lazy-fixtures from 1.4.0 to 1.4.1 |
| https://github.com/apache/iceberg-python/pull/3689 | `apache/iceberg-python` | `code_only` | `python` | Fix residual NotNaN for null partition values |
| https://github.com/apache/iceberg-python/pull/3746 | `apache/iceberg-python` | `code_only` | `python` | fix(decimal): use minimal byte length for negative powers of two |
| https://github.com/apache/iceberg-python/pull/3815 | `apache/iceberg-python` | `code_only` | `python` | Infra: Enable pull request auto-merge |
| https://github.com/apache/iceberg-python/pull/3811 | `apache/iceberg-python` | `code_only` | `python` | Validate replaced data files during commit retries |
| https://github.com/apache/iceberg-python/pull/3780 | `apache/iceberg-python` | `code_only` | `python` | bug: fix delete_data_file on partitioned tables |
| https://github.com/apache/iceberg-python/pull/3804 | `apache/iceberg-python` | `code_only_tests_or_fixtures` | `python` | fix: stop calling deprecated PuffinFile.to_vector in Spark DV test |
| https://github.com/apache/iceberg-python/pull/3320 | `apache/iceberg-python` | `code_and_docs` | `python` | Add commit retry and concurrency validation for writes |
| https://github.com/apache/iceberg-python/pull/3261 | `apache/iceberg-python` | `code_only` | `python` | Fix pa.Schema type annotations in schema_to_pyarrow |
| https://github.com/apache/iceberg-python/pull/3476 | `apache/iceberg-python` | `code_only_tests_or_fixtures` | `python` | Add Spark interop test for reading Puffin deletion vectors |
| https://github.com/apache/iceberg-python/pull/3614 | `apache/iceberg-python` | `code_only` | `python` | fix: pad sub-microsecond digits when parsing nanosecond timestamps |
| https://github.com/apache/iceberg-python/pull/3612 | `apache/iceberg-python` | `code_only_tests_or_fixtures` | `python` | test: fix operator precedence in manifest v2 assertions |
| https://github.com/apache/iceberg-python/pull/3603 | `apache/iceberg-python` | `code_only` | `python` | fix: compare timestamps for partitions metadata last_updated_at |
| https://github.com/apache/iceberg-python/pull/3617 | `apache/iceberg-python` | `code_only` | `python` | fix: raise TypeError for unsupported partition source type |
| https://github.com/apache/iceberg-python/pull/3602 | `apache/iceberg-python` | `code_only` | `python` | fix: use removeprefix to decode DynamoDB namespace property keys |
| https://github.com/apache/iceberg-python/pull/3492 | `apache/iceberg-python` | `code_only` | `python` | fix(fsspec): parse S3 virtual addressing as a boolean |
| https://github.com/apache/iceberg-python/pull/3634 | `apache/iceberg-python` | `code_only` | `python` | fix: correct class name in Long{AboveMax,BelowMin} type-change error |
| https://github.com/apache/iceberg-python/pull/3173 | `apache/iceberg-python` | `code_and_docs` | `python` | feat: add S3 SSE configs (FsspecFileIO only) |
| https://github.com/apache/iceberg-python/pull/3802 | `apache/iceberg-python` | `code_only` | `python` | Add docstrings to pyiceberg/table/inspect.py |
| https://github.com/apache/iceberg-python/pull/3795 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump pypa/cibuildwheel from 4.1.1 to 4.2.0 |
| https://github.com/apache/iceberg-python/pull/3793 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump actions/stale from 10.4.0 to 11.0.0 |
| https://github.com/apache/iceberg-python/pull/3792 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump the codeql-action group with 2 updates |
| https://github.com/apache/iceberg-python/pull/3665 | `apache/iceberg-python` | `code_only` | `python` | Make metrics evaluation stateless |
| https://github.com/apache/iceberg-python/pull/3709 | `apache/iceberg-python` | `code_only` | `python` | Fix/sqlcatalog iceberg type filter |
| https://github.com/apache/iceberg-python/pull/3774 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump setuptools to 83.0.0 |
| https://github.com/apache/iceberg-python/pull/3766 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump tcort/github-action-markdown-link-check from 1.1.2 to 1.1.3 |
| https://github.com/apache/iceberg-python/pull/3730 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump zizmorcore/zizmor-action from 0.5.6 to 0.6.2 |
| https://github.com/apache/iceberg-python/pull/3767 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump actions/setup-python from 6.3.0 to 7.0.0 |
| https://github.com/apache/iceberg-python/pull/3765 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump pypa/gh-action-pypi-publish from 1.13.0 to 1.14.2 |
| https://github.com/apache/iceberg-python/pull/3764 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump the codeql-action group with 2 updates |
| https://github.com/apache/iceberg-python/pull/3535 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump protobuf from 6.33.5 to 7.35.1 |
| https://github.com/apache/iceberg-python/pull/3705 | `apache/iceberg-python` | `code_only_tests_or_fixtures` | `python` | Build: Bump ray from 2.55.1 to 2.56.1 |
| https://github.com/apache/iceberg-python/pull/3718 | `apache/iceberg-python` | `code_and_docs` | `python` | Add `--purge` option to drop table CLI |
| https://github.com/apache/iceberg-python/pull/3759 | `apache/iceberg-python` | `code_only_tests_or_fixtures` | `python` | Fix flaky moto_server fixture by using an OS-assigned ephemeral port |
| https://github.com/apache/iceberg-python/pull/3755 | `apache/iceberg-python` | `code_only` | `python` | INFRA: Use PR titles for squash commits |
| https://github.com/apache/iceberg-python/pull/3750 | `apache/iceberg-python` | `code_only` | `python` | refactor: simplify CLI property lookup |
| https://github.com/apache/iceberg-python/pull/3748 | `apache/iceberg-python` | `code_only` | `python` | Bump version to 0.12.0 |
| https://github.com/apache/iceberg-python/pull/3723 | `apache/iceberg-python` | `code_only` | `python` | CI: Add Windows unit test job |
| https://github.com/apache/iceberg-python/pull/3745 | `apache/iceberg-python` | `code_only` | `python` | fix: preserve empty property values in CLI |
| https://github.com/apache/iceberg-python/pull/3742 | `apache/iceberg-python` | `code_only` | `python` | Remove stale VariantType transform TODO |
| https://github.com/apache/iceberg-python/pull/3740 | `apache/iceberg-python` | `code_and_docs` | `python` | ci: enable ASF Copilot code review |
| https://github.com/apache/iceberg-python/pull/3711 | `apache/iceberg-python` | `code_and_docs` | `python` | build: bump pyiceberg-core from 0.9.1 to 0.10.1 |
| https://github.com/apache/iceberg-python/pull/3733 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump pypa/cibuildwheel from 4.1.0 to 4.1.1 |
| https://github.com/apache/iceberg-python/pull/3731 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump actions/setup-python from 6.3.0 to 7.0.0 |
| https://github.com/apache/iceberg-python/pull/3729 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump the codeql-action group with 2 updates |
| https://github.com/apache/iceberg-python/pull/3739 | `apache/iceberg-python` | `code_only` | `python` | chore(ci): Update ASF allowlist check action dependency to track versioned releases |
| https://github.com/apache/iceberg-python/pull/3042 | `apache/iceberg-python` | `code_only` | `python` | Support storage-credentials in REST catalog LoadTableResult |
| https://github.com/apache/iceberg-python/pull/3692 | `apache/iceberg-python` | `code_only` | `python` | Convert FileFormatModel from ABC to typing.Protocol |
| https://github.com/apache/iceberg-python/pull/3664 | `apache/iceberg-python` | `code_only` | `python` | Make partition expression evaluation stateless |
| https://github.com/apache/iceberg-python/pull/3263 | `apache/iceberg-python` | `code_only` | `python` | fix: add iceberg_type column for SqlCatalog |
| https://github.com/apache/iceberg-python/pull/3595 | `apache/iceberg-python` | `code_only` | `python` | fix: preserve dictionary encoding in to_arrow_batch_reader |
| https://github.com/apache/iceberg-python/pull/3660 | `apache/iceberg-python` | `code_only` | `python` | fix: preserve manifest min sequence number of 0 |
| https://github.com/apache/iceberg-python/pull/3703 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump mkdocs-material from 9.7.6 to 9.7.7 |
| https://github.com/apache/iceberg-python/pull/3701 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump actions/checkout from 7.0.0 to 7.0.1 |
| https://github.com/apache/iceberg-python/pull/3699 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump the codeql-action group with 2 updates |
| https://github.com/apache/iceberg-python/pull/3381 | `apache/iceberg-python` | `code_only` | `python` | Implement ParquetFormatModel and update write_file to use the format API |
| https://github.com/apache/iceberg-python/pull/3686 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump the codeql-action group with 2 updates |
| https://github.com/apache/iceberg-python/pull/3683 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump mkdocstrings from 1.0.5 to 1.0.6 |
| https://github.com/apache/iceberg-python/pull/3585 | `apache/iceberg-python` | `code_only` | `python` | fix: raise ValidationError for decimal precision outside 1-38 range |
| https://github.com/apache/iceberg-python/pull/3610 | `apache/iceberg-python` | `code_only` | `python` | Only run integration tests on Python changes |
| https://github.com/apache/iceberg-python/pull/3601 | `apache/iceberg-python` | `code_only` | `python` | fix: preserve write_default when applying a name mapping |
| https://github.com/apache/iceberg-python/pull/3592 | `apache/iceberg-python` | `code_only` | `python` | fix: Pass metadata location to StaticTable FileIO for scheme inference |
| https://github.com/apache/iceberg-python/pull/3590 | `apache/iceberg-python` | `code_only` | `python` | feat: support pyarrow float16 by widening to float on read/write |
| https://github.com/apache/iceberg-python/pull/3648 | `apache/iceberg-python` | `code_only` | `python` | Infra: Group github/codeql-action bumps into a single dependabot PR |
| https://github.com/apache/iceberg-python/pull/3575 | `apache/iceberg-python` | `code_only` | `python` | Support zstd blob decompression in Puffin |
| https://github.com/apache/iceberg-python/pull/3669 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump actions/stale from 10.3.0 to 10.4.0 |
| https://github.com/apache/iceberg-python/pull/3678 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump mkdocstrings from 1.0.4 to 1.0.5 |
| https://github.com/apache/iceberg-python/pull/3639 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump typing-extensions from 4.15.0 to 4.16.0 |
| https://github.com/apache/iceberg-python/pull/3646 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump github/codeql-action/init and github/codeql-action/analyze from 4.36.2 to 4.36.3 |
| https://github.com/apache/iceberg-python/pull/3517 | `apache/iceberg-python` | `code_only` | `python` | Reject unsupported identity transform types |
| https://github.com/apache/iceberg-python/pull/3605 | `apache/iceberg-python` | `code_only` | `python` | fix(ci): correct stale-issue-label and exempt security issues |
| https://github.com/apache/iceberg-python/pull/3606 | `apache/iceberg-python` | `code_only` | `python` | fix: require pyarrow>=18.0.0 for native UUID type support |
| https://github.com/apache/iceberg-python/pull/3594 | `apache/iceberg-python` | `code_only` | `python` | Docs: Add missing _downcast_ns_timestamp_to_us to ArrowScan docstring |
| https://github.com/apache/iceberg-python/pull/3599 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump actions/setup-python from 6.2.0 to 6.3.0 |
| https://github.com/apache/iceberg-python/pull/3389 | `apache/iceberg-python` | `code_only` | `python` | Bump to Java Iceberg 1.11.0 |
| https://github.com/apache/iceberg-python/pull/3576 | `apache/iceberg-python` | `code_only` | `python` | Fix strip spec-mandated DV blob framing before deserializing |
| https://github.com/apache/iceberg-python/pull/3587 | `apache/iceberg-python` | `code_only` | `python` | CI: Pass args through docker-compose |
| https://github.com/apache/iceberg-python/pull/3581 | `apache/iceberg-python` | `code_only` | `python` | Infra: Set timeout for jobs in python-ci.yml |
| https://github.com/apache/iceberg-python/pull/3579 | `apache/iceberg-python` | `code_only` | `python` | Rename _scan_plan_helper method to _plan_manifest_entries |
| https://github.com/apache/iceberg-python/pull/2993 | `apache/iceberg-python` | `code_and_docs` | `python` | Make manifest cache size configurable |
| https://github.com/apache/iceberg-python/pull/3553 | `apache/iceberg-python` | `code_only` | `python` | Make scan_plan_helper internal (#3541) |
| https://github.com/apache/iceberg-python/pull/3512 | `apache/iceberg-python` | `code_only` | `python` | Feature: Incremental Append Scan |
| https://github.com/apache/iceberg-python/pull/3567 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump mkdocstrings-python from 2.0.4 to 2.0.5 |
| https://github.com/apache/iceberg-python/pull/3538 | `apache/iceberg-python` | `code_only_tests_or_fixtures` | `python` | Build: Bump pyarrow from 23.0.1 to 24.0.0 |
| https://github.com/apache/iceberg-python/pull/3561 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump actions/upload-artifact/merge from 4.6.2 to 7.0.1 |
| https://github.com/apache/iceberg-python/pull/3559 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump actions/checkout from 6.0.3 to 7.0.0 |
| https://github.com/apache/iceberg-python/pull/3532 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump pypa/cibuildwheel from 3.4.1 to 4.1.0 |
| https://github.com/apache/iceberg-python/pull/3570 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump pytest from 9.0.3 to 9.1.1 |
| https://github.com/apache/iceberg-python/pull/3571 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump griffe from 2.0.2 to 2.1.0 |
| https://github.com/apache/iceberg-python/pull/3491 | `apache/iceberg-python` | `code_only` | `python` | Extract DeletionVector logic from PuffinFile |
| https://github.com/apache/iceberg-python/pull/3505 | `apache/iceberg-python` | `code_only` | `python` | fix(datetime): raise specific "Missing zone offset" error in  timestamptz_to_nanos |
| https://github.com/apache/iceberg-python/pull/3448 | `apache/iceberg-python` | `code_only` | `python` | Fix duplicate filtering path in Arrow task batches |
| https://github.com/apache/iceberg-python/pull/3550 | `apache/iceberg-python` | `code_only` | `python` | CI: Check ASF action allowlist on every PR |
| https://github.com/apache/iceberg-python/pull/3547 | `apache/iceberg-python` | `code_only_tests_or_fixtures` | `python` | Add strict NotEqualTo/NotIn null and NaN tests |
| https://github.com/apache/iceberg-python/pull/3521 | `apache/iceberg-python` | `code_only` | `python` | Fix strict NotEqualTo/NotIn pruning with partial nulls or NaNs |
| https://github.com/apache/iceberg-python/pull/3546 | `apache/iceberg-python` | `code_only` | `python` | Return bounds sentinels for long date literals |
| https://github.com/apache/iceberg-python/pull/3501 | `apache/iceberg-python` | `code_only` | `python` | Fix string-based `starts_with` and `not_starts_with` methods |
| https://github.com/apache/iceberg-python/pull/3502 | `apache/iceberg-python` | `code_only` | `python` | Return overflow sentinel in LongLiteral.to(FloatType) |
| https://github.com/apache/iceberg-python/pull/3503 | `apache/iceberg-python` | `code_only` | `python` | Fix NotStartsWith residual evaluation to return correct result |
| https://github.com/apache/iceberg-python/pull/3528 | `apache/iceberg-python` | `code_only` | `python` | fix: correct NOT STARTS WITH projection for truncated partitions |
| https://github.com/apache/iceberg-python/pull/3499 | `apache/iceberg-python` | `code_only` | `python` | feat: Add REST loadCredentials support |
| https://github.com/apache/iceberg-python/pull/3511 | `apache/iceberg-python` | `code_only` | `python` | Refactor: extract `BaseScan` and `ManifestGroupPlanner` |
| https://github.com/apache/iceberg-python/pull/3461 | `apache/iceberg-python` | `code_only` | `python` | feat: add dictionary_columns to to_arrow() / to_arrow_batch_reader() for memory-efficient reads |
| https://github.com/apache/iceberg-python/pull/3456 | `apache/iceberg-python` | `code_only` | `python` | Add rambleraptor to collaborators list |
| https://github.com/apache/iceberg-python/pull/3510 | `apache/iceberg-python` | `code_only` | `python` | Update astral-sh/setup-uv to v8.2.0 |
| https://github.com/apache/iceberg-python/pull/3481 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump github/codeql-action from 4.36.0 to 4.36.2 |
| https://github.com/apache/iceberg-python/pull/3482 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump actions/checkout from 6.0.2 to 6.0.3 |
| https://github.com/apache/iceberg-python/pull/3487 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump mkdocstrings-python from 2.0.3 to 2.0.4 |
| https://github.com/apache/iceberg-python/pull/3490 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump fsspec from 2026.2.0 to 2026.4.0 |
| https://github.com/apache/iceberg-python/pull/3458 | `apache/iceberg-python` | `code_only` | `python` | Add defaults to ViewVersion fields |
| https://github.com/apache/iceberg-python/pull/3470 | `apache/iceberg-python` | `code_only` | `python` | fix(literals): return long bounds for decimal conversion |
| https://github.com/apache/iceberg-python/pull/3472 | `apache/iceberg-python` | `code_only_tests_or_fixtures` | `python` | Fix misleading file extension for partition statistics |
| https://github.com/apache/iceberg-python/pull/3445 | `apache/iceberg-python` | `code_only` | `python` | Make `View.version` return None for unknown id |
| https://github.com/apache/iceberg-python/pull/3432 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump zizmorcore/zizmor-action from 0.5.3 to 0.5.6 |
| https://github.com/apache/iceberg-python/pull/3431 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump actions/stale from 10.2.0 to 10.3.0 |
| https://github.com/apache/iceberg-python/pull/3430 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump github/codeql-action from 4.35.5 to 4.36.0 |
| https://github.com/apache/iceberg-python/pull/3424 | `apache/iceberg-python` | `code_only_tests_or_fixtures` | `python` | Fix typo |
| https://github.com/apache/iceberg-python/pull/3362 | `apache/iceberg-python` | `code_only` | `python` | Chore: Updated PyArrow Dependencies |
| https://github.com/apache/iceberg-python/pull/3411 | `apache/iceberg-python` | `code_only` | `python` | Reject empty `source-ids` in `PartitionField` / `SortField` |
| https://github.com/apache/iceberg-python/pull/3412 | `apache/iceberg-python` | `code_only` | `python` | Fix walrus truthiness on metrics bounds and identity-partition projection |
| https://github.com/apache/iceberg-python/pull/3405 | `apache/iceberg-python` | `code_only` | `python` | Fix precision loss in large integral string conversions |
| https://github.com/apache/iceberg-python/pull/3407 | `apache/iceberg-python` | `code_only` | `python` | Make `View.sql_for` case-insensitive and return None for unknown dialect |
| https://github.com/apache/iceberg-python/pull/3406 | `apache/iceberg-python` | `code_only_tests_or_fixtures` | `python` | REST: Add integration test for views |
| https://github.com/apache/iceberg-python/pull/3408 | `apache/iceberg-python` | `code_only` | `python` | REST: Allow Identifier type in `drop_view` method |
| https://github.com/apache/iceberg-python/pull/3206 | `apache/iceberg-python` | `code_only` | `python` | feat(cli): deprecate version command in favor of --version flag |
| https://github.com/apache/iceberg-python/pull/3377 | `apache/iceberg-python` | `code_only` | `python` | REST: Add support for page-size in list_namespaces, list_tables, and list_views |
| https://github.com/apache/iceberg-python/pull/3348 | `apache/iceberg-python` | `code_only` | `python` | REST: Add pagination support for list_tables |
| https://github.com/apache/iceberg-python/pull/3347 | `apache/iceberg-python` | `code_only` | `python` | REST: Add pagination support for list_namespaces |
| https://github.com/apache/iceberg-python/pull/3338 | `apache/iceberg-python` | `code_only` | `python` | feat(view): View object API |
| https://github.com/apache/iceberg-python/pull/3357 | `apache/iceberg-python` | `code_only` | `python` | fix: avoid TSaslClientTransport reuse to eliminate server-side SASL noise |
| https://github.com/apache/iceberg-python/pull/3391 | `apache/iceberg-python` | `code_only_tests_or_fixtures` | `python` | Test: Replace rest-scan-planning-enabled with scan-planning-mode |
| https://github.com/apache/iceberg-python/pull/3401 | `apache/iceberg-python` | `code_only` | `python` | Build: Update actions/upload-artifact to v7.0.1 |
| https://github.com/apache/iceberg-python/pull/3400 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump prek from 0.3.13 to 0.4.0 |
| https://github.com/apache/iceberg-python/pull/3393 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump github/codeql-action from 4.35.4 to 4.35.5 |
| https://github.com/apache/iceberg-python/pull/3376 | `apache/iceberg-python` | `code_only` | `python` | REST: Rename rest-scan-planning-enabled to scan-planning-mode |
| https://github.com/apache/iceberg-python/pull/3360 | `apache/iceberg-python` | `code_only` | `python` | Add @typing.override annotations to catalog and FileIO implementations |
| https://github.com/apache/iceberg-python/pull/3287 | `apache/iceberg-python` | `code_only` | `python` | perf(add_files): stream manifest entries for duplicate-files check |
| https://github.com/apache/iceberg-python/pull/3354 | `apache/iceberg-python` | `code_only` | `python` | fix(table): avoid committing update builders after exceptions |
| https://github.com/apache/iceberg-python/pull/3335 | `apache/iceberg-python` | `code_and_docs` | `python` | feat(2152): support pa.RecordBatchReader in Table.append/overwrite |
| https://github.com/apache/iceberg-python/pull/3366 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump github/codeql-action from 4.35.3 to 4.35.4 |
| https://github.com/apache/iceberg-python/pull/3378 | `apache/iceberg-python` | `code_only_tests_or_fixtures` | `python` | Fix typo in test_add_files |
| https://github.com/apache/iceberg-python/pull/3349 | `apache/iceberg-python` | `code_only` | `python` | REST: Add pagination support for list_views |
| https://github.com/apache/iceberg-python/pull/3353 | `apache/iceberg-python` | `code_only` | `python` | fix(fsspec): handle zero-byte files in __len__ |
| https://github.com/apache/iceberg-python/pull/3330 | `apache/iceberg-python` | `code_only` | `python` | add papermill-based notebook tests for pyiceberg examples |
| https://github.com/apache/iceberg-python/pull/3334 | `apache/iceberg-python` | `code_only_tests_or_fixtures` | `python` | fix(tests): isolate state in test_write_optional_list |
| https://github.com/apache/iceberg-python/pull/3288 | `apache/iceberg-python` | `code_and_docs` | `python` | Add support for registering views |
| https://github.com/apache/iceberg-python/pull/3339 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump github/codeql-action from 4.35.2 to 4.35.3 |
| https://github.com/apache/iceberg-python/pull/3224 | `apache/iceberg-python` | `code_only` | `python` | feat: add load_view to REST catalog |
| https://github.com/apache/iceberg-python/pull/3331 | `apache/iceberg-python` | `code_only` | `python` | CI: Use specific patch versions in workflow action comments |
| https://github.com/apache/iceberg-python/pull/3326 | `apache/iceberg-python` | `code_only` | `python` | Remove unused code |
| https://github.com/apache/iceberg-python/pull/3290 | `apache/iceberg-python` | `code_and_docs` | `python` | Add support for 'overwrite' option in register_table |
| https://github.com/apache/iceberg-python/pull/3327 | `apache/iceberg-python` | `code_only` | `python` | fix:update config during table refresh |
| https://github.com/apache/iceberg-python/pull/3119 | `apache/iceberg-python` | `code_only` | `python` | Initial work for file format writer API |
| https://github.com/apache/iceberg-python/pull/3273 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump zizmorcore/zizmor-action from 0.5.2 to 0.5.3 |
| https://github.com/apache/iceberg-python/pull/3289 | `apache/iceberg-python` | `code_only` | `python` | Document TableAlreadyExistsError in catalog.rename_table |
| https://github.com/apache/iceberg-python/pull/3240 | `apache/iceberg-python` | `code_only` | `python` | CI: Lock REST Fixture to 1.10.1 |
| https://github.com/apache/iceberg-python/pull/3295 | `apache/iceberg-python` | `code_only` | `python` | Fix deepcopy for And, Or, and Not expressions |
| https://github.com/apache/iceberg-python/pull/3301 | `apache/iceberg-python` | `code_only` | `python` | perf: Hoist table_metadata at remaining repeat-access sites in snapshot update |
| https://github.com/apache/iceberg-python/pull/3323 | `apache/iceberg-python` | `code_only` | `python` | Bump daft dependency to >=0.7.10 (fix Python 3.14 compatibility) |
| https://github.com/apache/iceberg-python/pull/3305 | `apache/iceberg-python` | `code_only_tests_or_fixtures` | `python` | fix: SaslServer busy-loop causes process hang after test suite |
| https://github.com/apache/iceberg-python/pull/3299 | `apache/iceberg-python` | `code_only` | `python` | infra: add python 3.14 support |
| https://github.com/apache/iceberg-python/pull/3310 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump fastavro from 1.12.1 to 1.12.2 |
| https://github.com/apache/iceberg-python/pull/3237 | `apache/iceberg-python` | `code_only` | `python` | Fix DELETED manifest entry snapshot_id in OverwriteFiles |
| https://github.com/apache/iceberg-python/pull/3293 | `apache/iceberg-python` | `code_only` | `python` | Reading upper/lower bounds values with type promotions |
| https://github.com/apache/iceberg-python/pull/3283 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump rich from 14.3.3 to 15.0.0 |
| https://github.com/apache/iceberg-python/pull/3282 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump mkdocstrings from 1.0.3 to 1.0.4 |
| https://github.com/apache/iceberg-python/pull/3284 | `apache/iceberg-python` | `code_only` | `python` | bug: NoopCatalog should return False, not throw error |
| https://github.com/apache/iceberg-python/pull/3276 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump mkdocs-section-index from 0.3.11 to 0.3.12 |
| https://github.com/apache/iceberg-python/pull/3264 | `apache/iceberg-python` | `code_only` | `python` | perf: build partition filter with balanced tree to avoid RecursionError |
| https://github.com/apache/iceberg-python/pull/3257 | `apache/iceberg-python` | `code_only` | `python` | Fix ManifestEntry.snapshot_id setter writing to wrong index |
| https://github.com/apache/iceberg-python/pull/3238 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump pytest from 9.0.2 to 9.0.3 |
| https://github.com/apache/iceberg-python/pull/3243 | `apache/iceberg-python` | `code_only` | `python` | ci: fix zizmor workflow |
| https://github.com/apache/iceberg-python/pull/3245 | `apache/iceberg-python` | `code_only` | `python` | fix zizmor ci issue by bumping codeql-action to v4.35.2 |
| https://github.com/apache/iceberg-python/pull/3225 | `apache/iceberg-python` | `code_only` | `python` | Build: Bump pypa/cibuildwheel from 3.4.0 to 3.4.1 |
| https://github.com/apache/iceberg-python/pull/3169 | `apache/iceberg-python` | `code_only` | `python` | fix: Handle optional properties in load namespace properties response |
| https://github.com/apache/iceberg-python/pull/3215 | `apache/iceberg-python` | `code_only` | `python` | ci: fix nightly and release |
| https://github.com/remix-run/remix/pull/11739 | `remix-run/remix` | `code_and_docs` | `typescript` | Fix reset scroll implementation and defer scrolling to the browser |
| https://github.com/remix-run/remix/pull/11729 | `remix-run/remix` | `code_and_docs` | `typescript` | Use remix db workflows across demos |
| https://github.com/remix-run/remix/pull/11702 | `remix-run/remix` | `code_and_docs` | `typescript` | Expose OAuth provider runtime |
| https://github.com/remix-run/remix/pull/11701 | `remix-run/remix` | `code_and_docs` | `typescript` | Remove Atmosphere auth provider |
| https://github.com/remix-run/remix/pull/11727 | `remix-run/remix` | `code_and_docs` | `typescript` | Align Remix UI attributes under the data-rmx namespace |
| https://github.com/remix-run/remix/pull/11728 | `remix-run/remix` | `code_and_docs` | `typescript` | Use remix db commands in bookstore demo |
| https://github.com/remix-run/remix/pull/11723 | `remix-run/remix` | `code_and_docs` | `typescript` | feat(cli): add `remix db rollback` |
| https://github.com/remix-run/remix/pull/11721 | `remix-run/remix` | `code_only` | `typescript` | Keep Remix as the latest GitHub release |
| https://github.com/remix-run/remix/pull/11720 | `remix-run/remix` | `code_and_docs` | `typescript` | Release |
| https://github.com/remix-run/remix/pull/11717 | `remix-run/remix` | `code_only` | `typescript` | Use npm 12 for trusted publishing |
| https://github.com/remix-run/remix/pull/11713 | `remix-run/remix` | `code_and_docs` | `typescript` | Release |
| https://github.com/remix-run/remix/pull/11716 | `remix-run/remix` | `code_and_docs` | `typescript` | Remove old static middleware package |
| https://github.com/remix-run/remix/pull/11715 | `remix-run/remix` | `code_and_docs` | `typescript` | Preserve unpublished entries in release notes |
| https://github.com/remix-run/remix/pull/11714 | `remix-run/remix` | `code_only` | `typescript` | Use npm CLI for trusted publishing |
| https://github.com/remix-run/remix/pull/11693 | `remix-run/remix` | `code_and_docs` | `typescript` | Add a default browser frame resolver |
| https://github.com/remix-run/remix/pull/11712 | `remix-run/remix` | `code_and_docs` | `typescript` | Rename static files middleware package |
| https://github.com/remix-run/remix/pull/11711 | `remix-run/remix` | `code_and_docs` | `typescript` | Release |
| https://github.com/remix-run/remix/pull/11710 | `remix-run/remix` | `code_and_docs` | `typescript` | Replace blocked static middleware package |
| https://github.com/remix-run/remix/pull/11704 | `remix-run/remix` | `code_and_docs` | `typescript` | Release |
| https://github.com/remix-run/remix/pull/11709 | `remix-run/remix` | `code_and_docs` | `typescript` | Publish static middleware 0.4.14 |
| https://github.com/remix-run/remix/pull/11700 | `remix-run/remix` | `code_and_docs` | `typescript` | Bump static middleware back to 0.4.14 |
| https://github.com/remix-run/remix/pull/11681 | `remix-run/remix` | `code_and_docs` | `typescript` | Support preloads in resolved client entries |
| https://github.com/remix-run/remix/pull/11698 | `remix-run/remix` | `code_and_docs` | `typescript` | Skip blocked static middleware publish |
| https://github.com/remix-run/remix/pull/11697 | `remix-run/remix` | `code_and_docs` | `typescript` | Recover static middleware release as 0.4.15 |
| https://github.com/remix-run/remix/pull/11695 | `remix-run/remix` | `code_and_docs` | `typescript` | Polish beta.6 release notes and prerelease publishing |
| https://github.com/remix-run/remix/pull/11648 | `remix-run/remix` | `code_and_docs` | `typescript` | Use class and css mixins consistently in template and examples |
| https://github.com/remix-run/remix/pull/11688 | `remix-run/remix` | `code_and_docs` | `typescript` | Harden client entry and frame boundary reconciliation |
| https://github.com/remix-run/remix/pull/11683 | `remix-run/remix` | `code_and_docs` | `typescript` | Show destination SSR while client entry modules load |
| https://github.com/remix-run/remix/pull/11680 | `remix-run/remix` | `code_and_docs` | `typescript` | Fix sibling removal when disposing hydration ranges |
| https://github.com/remix-run/remix/pull/11692 | `remix-run/remix` | `code_only` | `typescript` | Ignore HMR updates for unloaded browser assets |
| https://github.com/remix-run/remix/pull/11691 | `remix-run/remix` | `code_only` | `typescript` | Ignore stale node-hmr server ready events |
| https://github.com/remix-run/remix/pull/11682 | `remix-run/remix` | `code_only` | `typescript` | Stabilize HMR tests and limit Windows test concurrency |
| https://github.com/remix-run/remix/pull/11670 | `remix-run/remix` | `code_and_docs` | `typescript` | Add rmx-history navigation attribute |
| https://github.com/remix-run/remix/pull/11667 | `remix-run/remix` | `code_and_docs` | `typescript` | Support redirects from frame reloads |
| https://github.com/remix-run/remix/pull/11671 | `remix-run/remix` | `code_and_docs` | `typescript` | Fix top frame reloads after navigation targets a named frame |
| https://github.com/remix-run/remix/pull/11678 | `remix-run/remix` | `code_only_tests_or_fixtures` | `typescript` | Increase node-hmr test timeouts on Windows |
| https://github.com/remix-run/remix/pull/11677 | `remix-run/remix` | `code_only_tests_or_fixtures` | `typescript` | Increase HMR test connection timeout on Windows |
| https://github.com/remix-run/remix/pull/11676 | `remix-run/remix` | `code_only` | `typescript` | Skip assets HMR e2e tests in Bun |
| https://github.com/remix-run/remix/pull/11674 | `remix-run/remix` | `code_and_docs` | `typescript` | Align multipart boundary handling with RFC 2046 |
| https://github.com/remix-run/remix/pull/11672 | `remix-run/remix` | `code_and_docs` | `typescript` | Escape server-rendered CSS style text |
| https://github.com/remix-run/remix/pull/11601 | `remix-run/remix` | `code_and_docs` | `typescript` | Define the Remix contribution workflow |
| https://github.com/remix-run/remix/pull/11599 | `remix-run/remix` | `code_and_docs` | `typescript` | Remove legacy Remix export aliases |
| https://github.com/remix-run/remix/pull/11590 | `remix-run/remix` | `code_and_docs` | `typescript` | Add dark mode-compatible UI component styles |
| https://github.com/remix-run/remix/pull/11664 | `remix-run/remix` | `code_and_docs` | `typescript` | Fix frame marker matching during DOM diffing |
| https://github.com/remix-run/remix/pull/11663 | `remix-run/remix` | `code_only` | `typescript` | Fix guides navigation highlights |
| https://github.com/remix-run/remix/pull/11589 | `remix-run/remix` | `code_only_tests_or_fixtures` | `typescript` | Add regression coverage for function-valued component children |
| https://github.com/remix-run/remix/pull/11650 | `remix-run/remix` | `code_and_docs` | `typescript` | Fix frame region scans rewinding into an infinite loop |
| https://github.com/remix-run/remix/pull/11661 | `remix-run/remix` | `code_only` | `typescript` | Improve guides navigation and demo code rendering |
| https://github.com/remix-run/remix/pull/11659 | `remix-run/remix` | `code_and_docs` | `typescript` | Model UI VNodes with explicit lifecycle states |
| https://github.com/remix-run/remix/pull/11657 | `remix-run/remix` | `code_and_docs` | `typescript` | route-pattern: support relative URL matching and href generation |
| https://github.com/remix-run/remix/pull/11652 | `remix-run/remix` | `code_and_docs` | `typescript` | route-pattern: replace variant expansion with bounded state matching |
| https://github.com/remix-run/remix/pull/11506 | `remix-run/remix` | `code_and_docs` | `typescript` | Reload client frames on ancestor frame reload |
| https://github.com/remix-run/remix/pull/11566 | `remix-run/remix` | `code_and_docs` | `typescript` | Fix hydrated fragment updates losing existing content |
| https://github.com/remix-run/remix/pull/11635 | `remix-run/remix` | `code_and_docs` | `typescript` | Fix compression cache variation for identity responses |
| https://github.com/remix-run/remix/pull/11606 | `remix-run/remix` | `code_and_docs` | `typescript` | Fix UI mixin variance for subtype hosts |
| https://github.com/remix-run/remix/pull/11638 | `remix-run/remix` | `code_and_docs` | `typescript` | Add typed Remix doctor invocation and strict config |
| https://github.com/remix-run/remix/pull/11627 | `remix-run/remix` | `code_and_docs` | `typescript` | Use native Requests in node-fetch-server handlers |
| https://github.com/remix-run/remix/pull/11636 | `remix-run/remix` | `code_and_docs` | `typescript` | Fix data-table-sqlite wipe tests on Windows |
| https://github.com/remix-run/remix/pull/11633 | `remix-run/remix` | `code_only` | `typescript` | Retry sqlite file removal during wipe on Windows |
| https://github.com/remix-run/remix/pull/11614 | `remix-run/remix` | `code_only` | `typescript` | Fix API demo build test file exclusion |
| https://github.com/remix-run/remix/pull/11480 | `remix-run/remix` | `code_and_docs` | `typescript` | Add `allowPackages` option to `createAssetServer` |
| https://github.com/remix-run/remix/pull/11619 | `remix-run/remix` | `code_and_docs` | `typescript` | Default session cookies to HTTP-only |
| https://github.com/remix-run/remix/pull/11613 | `remix-run/remix` | `code_only` | `typescript` | Optimize UI runtime hot paths and fix benchmark runner measurement |
| https://github.com/remix-run/remix/pull/11612 | `remix-run/remix` | `code_only` | `typescript` | Rework css mixin style ownership into a pinned global registry |
| https://github.com/remix-run/remix/pull/11611 | `remix-run/remix` | `code_only` | `typescript` | Polish the guide search controls |
| https://github.com/remix-run/remix/pull/11565 | `remix-run/remix` | `code_and_docs` | `typescript` | Strip stale encoding and framing headers in fetch-proxy |
| https://github.com/remix-run/remix/pull/11419 | `remix-run/remix` | `code_only` | `typescript` | Migrate demo esbuild usage to `assets` |
| https://github.com/remix-run/remix/pull/11609 | `remix-run/remix` | `code_and_docs` | `typescript` | Update guides prerendering |
| https://github.com/remix-run/remix/pull/11578 | `remix-run/remix` | `code_only` | `typescript` | Change literal function to use 'const' for value |
| https://github.com/remix-run/remix/pull/11461 | `remix-run/remix` | `code_and_docs` | `typescript` | Add Pagefind search to prerendered docs |
| https://github.com/remix-run/remix/pull/11600 | `remix-run/remix` | `code_only_tests_or_fixtures` | `typescript` | Fix Bun regex error assertion |
| https://github.com/remix-run/remix/pull/11596 | `remix-run/remix` | `code_and_docs` | `typescript` | Update stale Remix examples and demo conventions |
| https://github.com/remix-run/remix/pull/11595 | `remix-run/remix` | `code_and_docs` | `typescript` | Make plain test filters case-insensitive |
| https://github.com/remix-run/remix/pull/11594 | `remix-run/remix` | `code_and_docs` | `typescript` | data-table: use bound parameters for compiled `limit` and `offset` clauses |
| https://github.com/remix-run/remix/pull/11504 | `remix-run/remix` | `code_and_docs` | `typescript` | Add rmx-preserve-dom support to UI reconciler |
| https://github.com/remix-run/remix/pull/11588 | `remix-run/remix` | `code_only` | `typescript` | pnpm: replace deprecated `onlyBuiltDependencies` with `allowBuilds` |
| https://github.com/remix-run/remix/pull/11581 | `remix-run/remix` | `code_and_docs` | `typescript` | Add test runner --only flag |
| https://github.com/remix-run/remix/pull/11579 | `remix-run/remix` | `code_and_docs` | `typescript` | Treat custom cookie codecs as raw value codecs |
| https://github.com/remix-run/remix/pull/11572 | `remix-run/remix` | `code_and_docs` | `typescript` | Fix test .only filtering across modules |
| https://github.com/remix-run/remix/pull/11582 | `remix-run/remix` | `code_only` | `typescript` | Fix docs method links |
| https://github.com/remix-run/remix/pull/11514 | `remix-run/remix` | `code_and_docs` | `typescript` | Pass named Frame targets during client resolution |
| https://github.com/remix-run/remix/pull/11516 | `remix-run/remix` | `code_and_docs` | `typescript` | Preserve Frame markers at clientEntry Fragment boundaries |
| https://github.com/remix-run/remix/pull/11523 | `remix-run/remix` | `code_only` | `typescript` | Treat lint warnings as errors |
| https://github.com/remix-run/remix/pull/11496 | `remix-run/remix` | `code_and_docs` | `typescript` | Improve default template asset and frame defaults |
| https://github.com/remix-run/remix/pull/11561 | `remix-run/remix` | `code_and_docs` | `typescript` | Simplify RoutePattern construction and rename params to captures |
| https://github.com/remix-run/remix/pull/11560 | `remix-run/remix` | `code_and_docs` | `typescript` | Document route-pattern API and benchmarks |
| https://github.com/remix-run/remix/pull/11559 | `remix-run/remix` | `code_and_docs` | `typescript` | Fix route pattern correctness issues |
| https://github.com/remix-run/remix/pull/11558 | `remix-run/remix` | `code_and_docs` | `typescript` | Align route pattern helper types with runtime grammar |
| https://github.com/remix-run/remix/pull/11557 | `remix-run/remix` | `code_and_docs` | `typescript` | Make RoutePattern opaque and nominal |
| https://github.com/remix-run/remix/pull/11555 | `remix-run/remix` | `code_and_docs` | `typescript` | Add trusted proxy support |
| https://github.com/remix-run/remix/pull/11553 | `remix-run/remix` | `code_and_docs` | `typescript` | Clarify session storage cookie docs |
| https://github.com/remix-run/remix/pull/11552 | `remix-run/remix` | `code_and_docs` | `typescript` | Fix node fetch server abort handling |
| https://github.com/remix-run/remix/pull/11551 | `remix-run/remix` | `code_and_docs` | `typescript` | Prevent doctor --fix writes through external symlinks |
| https://github.com/remix-run/remix/pull/11549 | `remix-run/remix` | `code_and_docs` | `typescript` | Fix fetch proxy host header |
| https://github.com/remix-run/remix/pull/11548 | `remix-run/remix` | `code_and_docs` | `typescript` | Fix Atmosphere handle resolution race |
| https://github.com/remix-run/remix/pull/11546 | `remix-run/remix` | `code_and_docs` | `typescript` | Fix custom multi-part MIME extension detection |
| https://github.com/remix-run/remix/pull/11547 | `remix-run/remix` | `code_and_docs` | `typescript` | Fix urlencoded form data parser limits |
| https://github.com/remix-run/remix/pull/11524 | `remix-run/remix` | `code_and_docs` | `typescript` | Fix `clientEntry` collision for entries sharing an entry id |
| https://github.com/remix-run/remix/pull/11513 | `remix-run/remix` | `code_and_docs` | `typescript` | Fix createHref optional param values |
| https://github.com/remix-run/remix/pull/11544 | `remix-run/remix` | `code_only_tests_or_fixtures` | `typescript` | test: native sqlite refactor |
| https://github.com/remix-run/remix/pull/11543 | `remix-run/remix` | `code_only` | `typescript` | Downgrade back to pnpm@10 |
| https://github.com/remix-run/remix/pull/11540 | `remix-run/remix` | `code_and_docs` | `typescript` | Simplify data-table integration test configuration |
| https://github.com/remix-run/remix/pull/11536 | `remix-run/remix` | `code_only` | `typescript` | fix CI flows on pnpm@11 |
| https://github.com/remix-run/remix/pull/11531 | `remix-run/remix` | `code_only_tests_or_fixtures` | `typescript` | Move UI render coverage out of test package |
| https://github.com/remix-run/remix/pull/11530 | `remix-run/remix` | `code_only` | `typescript` | Remove test package UI dependency cycle |
| https://github.com/remix-run/remix/pull/11529 | `remix-run/remix` | `code_only_tests_or_fixtures` | `typescript` | Fix Bun assert compatibility test |
| https://github.com/remix-run/remix/pull/11528 | `remix-run/remix` | `code_and_docs` | `typescript` | Remove Codex PR review workflow |
| https://github.com/remix-run/remix/pull/11527 | `remix-run/remix` | `code_only` | `typescript` | Update GitHub actions to Node 24 versions |
| https://github.com/remix-run/remix/pull/11526 | `remix-run/remix` | `code_and_docs` | `typescript` | Fix browser script abort handling |
| https://github.com/remix-run/remix/pull/11511 | `remix-run/remix` | `code_and_docs` | `typescript` | Fix route-pattern default port matching |
| https://github.com/remix-run/remix/pull/11512 | `remix-run/remix` | `code_and_docs` | `typescript` | Handle malformed route-pattern pathnames |
| https://github.com/remix-run/remix/pull/11505 | `remix-run/remix` | `code_and_docs` | `typescript` | Add version flag to docs prerender |
| https://github.com/remix-run/remix/pull/11498 | `remix-run/remix` | `code_and_docs` | `typescript` | Add composable fetch-router mounts and middleware inference |
| https://github.com/remix-run/remix/pull/11489 | `remix-run/remix` | `code_and_docs` | `typescript` | Improve assert Node compatibility |
| https://github.com/remix-run/remix/pull/11491 | `remix-run/remix` | `code_and_docs` | `typescript` | Add remix test timeouts |
| https://github.com/remix-run/remix/pull/11492 | `remix-run/remix` | `code_and_docs` | `typescript` | Require middleware to explicitly continue |
| https://github.com/remix-run/remix/pull/11488 | `remix-run/remix` | `code_only` | `typescript` | Make GitHub release publishing resilient |
| https://github.com/remix-run/remix/pull/11487 | `remix-run/remix` | `code_and_docs` | `typescript` | v2 updates |
| https://github.com/remix-run/remix/pull/11474 | `remix-run/remix` | `code_and_docs` | `typescript` | Fix frame fallback flicker when reloading ancestor frames |
| https://github.com/remix-run/remix/pull/11448 | `remix-run/remix` | `code_and_docs` | `typescript` | Prevent static middleware symlink escapes |
| https://github.com/remix-run/remix/pull/11456 | `remix-run/remix` | `code_and_docs` | `typescript` | Fix long Memcache session TTLs |
| https://github.com/remix-run/remix/pull/11475 | `remix-run/remix` | `code_and_docs` | `typescript` | Use OS-assigned ports for browser test servers |
| https://github.com/remix-run/remix/pull/11482 | `remix-run/remix` | `code_and_docs` | `typescript` | Fix recursive CSS nesting in UI css mixin |
| https://github.com/remix-run/remix/pull/11468 | `remix-run/remix` | `code_and_docs` | `typescript` | route-pattern: param encoding and validation |
| https://github.com/remix-run/remix/pull/11481 | `remix-run/remix` | `code_and_docs` | `typescript` | Fix browser test package resolution |
| https://github.com/remix-run/remix/pull/11486 | `remix-run/remix` | `code_only` | `typescript` | Pin node to 24.15.0 on windows CI tests to avoid libuv issue |
| https://github.com/remix-run/remix/pull/11473 | `remix-run/remix` | `code_and_docs` | `typescript` | Fix duplicate modules for bare imports in `assets` |
| https://github.com/remix-run/remix/pull/11469 | `remix-run/remix` | `code_and_docs` | `typescript` | Add menu.contextTrigger() for right-click context menus |
| https://github.com/remix-run/remix/pull/11463 | `remix-run/remix` | `code_and_docs` | `typescript` | Add @remix-run/headers parser subpath exports |
| https://github.com/remix-run/remix/pull/11455 | `remix-run/remix` | `code_and_docs` | `typescript` | Report test lifecycle hook failures |
| https://github.com/remix-run/remix/pull/11452 | `remix-run/remix` | `code_and_docs` | `typescript` | Fix SQLite transaction token checks |
| https://github.com/remix-run/remix/pull/11449 | `remix-run/remix` | `code_and_docs` | `typescript` | Reject unsafe OAuth returnTo redirects |
| https://github.com/remix-run/remix/pull/11450 | `remix-run/remix` | `code_and_docs` | `typescript` | Fix lazy-file nested slice ranges |
| https://github.com/remix-run/remix/pull/11447 | `remix-run/remix` | `code_only_tests_or_fixtures` | `typescript` | Speed up slow CI test files |
| https://github.com/remix-run/remix/pull/11446 | `remix-run/remix` | `code_only_tests_or_fixtures` | `typescript` | Harden memcache fake server tests |
| https://github.com/remix-run/remix/pull/11444 | `remix-run/remix` | `code_and_docs` | `typescript` | Clarify Remix component prop guidance |
| https://github.com/remix-run/remix/pull/11426 | `remix-run/remix` | `code_and_docs` | `typescript` | Add SuperHeaders apply method |
| https://github.com/remix-run/remix/pull/11434 | `remix-run/remix` | `code_and_docs` | `typescript` | Fix booleanish attribute rendering |
| https://github.com/remix-run/remix/pull/11431 | `remix-run/remix` | `code_and_docs` | `typescript` | Handle request aborts in renderToStream and createRequestListener |
| https://github.com/remix-run/remix/pull/11438 | `remix-run/remix` | `code_and_docs` | `typescript` | Fix pnpm package import resolution in assets |
| https://github.com/remix-run/remix/pull/11441 | `remix-run/remix` | `code_and_docs` | `typescript` | Fix node-tsx built loadModule hook path |
| https://github.com/remix-run/remix/pull/11432 | `remix-run/remix` | `code_and_docs` | `typescript` | Fix node-fetch-server response body cancellation on close |
| https://github.com/remix-run/remix/pull/11439 | `remix-run/remix` | `code_and_docs` | `typescript` | Remove node-serve from next beta |
| https://github.com/remix-run/remix/pull/11425 | `remix-run/remix` | `code_and_docs` | `typescript` | Fix UI hydration fragment anchors |
| https://github.com/remix-run/remix/pull/11436 | `remix-run/remix` | `code_only_tests_or_fixtures` | `typescript` | fix cli tests so that they pass when run from a tty |
| https://github.com/remix-run/remix/pull/11430 | `remix-run/remix` | `code_and_docs` | `typescript` | Align LazyFile and file-storage type contracts |
| https://github.com/remix-run/remix/pull/11427 | `remix-run/remix` | `code_and_docs` | `typescript` | Clarify Remix UI context identity semantics |
| https://github.com/remix-run/remix/pull/11409 | `remix-run/remix` | `code_and_docs` | `typescript` | fix: don't highlight hyphens in path arguments as single-character flags |
| https://github.com/remix-run/remix/pull/11423 | `remix-run/remix` | `code_and_docs` | `typescript` | Preserve duplicate Cookie header values |
| https://github.com/remix-run/remix/pull/11422 | `remix-run/remix` | `code_and_docs` | `typescript` | Fix stale component updates after frame reload |
| https://github.com/remix-run/remix/pull/11421 | `remix-run/remix` | `code_and_docs` | `typescript` | Consolidate repo agent skills |
| https://github.com/remix-run/remix/pull/11420 | `remix-run/remix` | `code_and_docs` | `typescript` | Preserve package symlink identity paths in asset server |
| https://github.com/remix-run/remix/pull/11417 | `remix-run/remix` | `code_only` | `typescript` | Gate Codex PR review workflows |
| https://github.com/remix-run/remix/pull/11380 | `remix-run/remix` | `code_and_docs` | `typescript` | Fix CLI template gitignore scaffolding |
| https://github.com/remix-run/remix/pull/11414 | `remix-run/remix` | `code_only` | `typescript` | Expand frames demo |
| https://github.com/remix-run/remix/pull/11413 | `remix-run/remix` | `code_and_docs` | `typescript` | Add package meta validation script |
| https://github.com/remix-run/remix/pull/11407 | `remix-run/remix` | `code_and_docs` | `typescript` | Clarify frame resolver setup and run hook docs |
| https://github.com/remix-run/remix/pull/11385 | `remix-run/remix` | `code_and_docs` | `typescript` | ui: improved type inference for `on` mixin |
| https://github.com/remix-run/remix/pull/11345 | `remix-run/remix` | `code_and_docs` | `typescript` | Add favicon and clean up app template shell |
| https://github.com/remix-run/remix/pull/11397 | `remix-run/remix` | `code_and_docs` | `typescript` | Add UI component demos to the docs site |
| https://github.com/remix-run/remix/pull/11408 | `remix-run/remix` | `code_and_docs` | `typescript` | Layer Remix UI theme reset |
| https://github.com/remix-run/remix/pull/11402 | `remix-run/remix` | `code_and_docs` | `typescript` | Fix FOUC when navigating between hydrated client entries |
| https://github.com/remix-run/remix/pull/11406 | `remix-run/remix` | `code_and_docs` | `typescript` | Avoid eager Web Encoding globals in multipart parser |
| https://github.com/remix-run/remix/pull/11405 | `remix-run/remix` | `code_only_tests_or_fixtures` | `typescript` | Fix assets error message test in Bun |
| https://github.com/remix-run/remix/pull/11401 | `remix-run/remix` | `code_and_docs` | `typescript` | ui: animateLayout interruptions resume from current visual position |
| https://github.com/remix-run/remix/pull/11396 | `remix-run/remix` | `code_and_docs` | `typescript` | Propagate skip and only from parent describes to nested describes |
| https://github.com/remix-run/remix/pull/11363 | `remix-run/remix` | `code_and_docs` | `typescript` | route-pattern: remove `compareFn` parameter from `Matcher.{match,matchAll}` |
| https://github.com/remix-run/remix/pull/11395 | `remix-run/remix` | `code_only` | `typescript` | Simplify frame navigation demo rendering |
| https://github.com/remix-run/remix/pull/11393 | `remix-run/remix` | `code_and_docs` | `typescript` | Update dependencies to clear audit alerts |
| https://github.com/remix-run/remix/pull/11391 | `remix-run/remix` | `code_only` | `typescript` | Disable pnpm cache on publish workflow |
| https://github.com/remix-run/remix/pull/11377 | `remix-run/remix` | `code_and_docs` | `typescript` | Simplify context entry helper types |
| https://github.com/remix-run/remix/pull/11376 | `remix-run/remix` | `code_and_docs` | `typescript` | Fix browser test progress timeout |
| https://github.com/remix-run/remix/pull/11371 | `remix-run/remix` | `code_and_docs` | `typescript` | Simplify async context typing |
| https://github.com/remix-run/remix/pull/11343 | `remix-run/remix` | `code_and_docs` | `typescript` | Add support for variables to API docs |
| https://github.com/remix-run/remix/pull/11369 | `remix-run/remix` | `code_and_docs` | `typescript` | Optimize UI runtime hot paths. |
| https://github.com/remix-run/remix/pull/11362 | `remix-run/remix` | `code_only` | `typescript` | route-pattern: remove redundant exclusion of `.types.bench.ts` files from package.json |
| https://github.com/remix-run/remix/pull/11360 | `remix-run/remix` | `code_and_docs` | `typescript` | Fix textarea stream rendering |
| https://github.com/remix-run/remix/pull/11368 | `remix-run/remix` | `code_and_docs` | `typescript` | route-pattern: do not allow partial matches for variables and wildcards in pathname |
| https://github.com/remix-run/remix/pull/11359 | `remix-run/remix` | `code_and_docs` | `typescript` | Simplify fetch-router action and middleware types |
| https://github.com/remix-run/remix/pull/11365 | `remix-run/remix` | `code_only_tests_or_fixtures` | `typescript` | cli: consolidate `withEnv` test utility |
| https://github.com/apache/arrow/pull/50972 | `apache/arrow` | `code_only` | `python` | GH-50971: [C++][Parquet] Fix usage of disparate length types for metadata reading |
| https://github.com/apache/arrow/pull/50986 | `apache/arrow` | `code_only` | `python` | GH-50985: [CI][Dev][Python] Update cython-lint and pin Cython to 3.2.9 |
| https://github.com/apache/arrow/pull/50927 | `apache/arrow` | `code_only` | `python` | GH-50623: [C++][IPC] Fix extension-wrapped union IPC roundtrip |
| https://github.com/apache/arrow/pull/50874 | `apache/arrow` | `code_only` | `python` | GH-50901: [C++] Replace RapidJSON with simdjson in tensor extension types |
| https://github.com/apache/arrow/pull/50858 | `apache/arrow` | `code_only` | `python` | GH-50524: [C++] Honor array offset in pairwise_diff |
| https://github.com/apache/arrow/pull/50914 | `apache/arrow` | `code_only_tests_or_fixtures` | `python` | GH-50913: [C++][Dataset] Replace RapidJSON with JsonWriter |
| https://github.com/apache/arrow/pull/50970 | `apache/arrow` | `code_only` | `python` | GH-48977: [C++] Fix quadratic field name index construction on libc++ |
| https://github.com/apache/arrow/pull/50974 | `apache/arrow` | `code_only` | `python` | MINOR: [CI] Bump apache/infrastructure-actions/stash/restore from bc817c8e9ad7d8216aab74223e32ea391e233b2c to 69afc125e535c4c41e7f1b7470f... |
| https://github.com/apache/arrow/pull/50973 | `apache/arrow` | `code_only` | `python` | MINOR: [CI] Bump apache/infrastructure-actions/stash/save from bc817c8e9ad7d8216aab74223e32ea391e233b2c to 69afc125e535c4c41e7f1b7470f583... |
| https://github.com/apache/arrow/pull/50785 | `apache/arrow` | `code_only` | `python` | GH-50784: [C++] Align write in `TransferBitmap` |
| https://github.com/apache/arrow/pull/50742 | `apache/arrow` | `code_only` | `python` | MINOR: [CI][C++] Fix Docker caching on JNI builds |
| https://github.com/apache/arrow/pull/50905 | `apache/arrow` | `code_only` | `python` | GH-50904: [C++] Replace RapidJSON with simdjson in OpaqueType |
| https://github.com/apache/arrow/pull/50827 | `apache/arrow` | `code_only` | `python` | GH-41670: [C++][Python] Move to DLPack 1.3 |
| https://github.com/apache/arrow/pull/50854 | `apache/arrow` | `code_only` | `python` | GH-50832: [Ruby] Add `ArrowFormat::FixedSizeBinaryArray.new(byte_width, values)` |
| https://github.com/apache/arrow/pull/50325 | `apache/arrow` | `code_only` | `python` | GH-50312: [Python] Fix UUID extension type round-trip to pandas returning bytes |
| https://github.com/apache/arrow/pull/50153 | `apache/arrow` | `code_only` | `python` | GH-48740: [C++] Add missing CTypeTraits for decimal types |
| https://github.com/apache/arrow/pull/50769 | `apache/arrow` | `code_and_docs` | `python` | GH-48473: [CI][Python] Require numpy 2.0 |
| https://github.com/apache/arrow/pull/48191 | `apache/arrow` | `code_only` | `python` | GH-48172: [Python] Add cp315 to build |
| https://github.com/apache/arrow/pull/50918 | `apache/arrow` | `code_only` | `python` | GH-50917: [C++] Fix shellcheck errors in cpp/build-support/*-flatbuffers.sh |
| https://github.com/apache/arrow/pull/50851 | `apache/arrow` | `code_and_docs` | `python` | GH-46646: [dev][R] Replace linr with jarl for R linting / pre-commit check |
| https://github.com/apache/arrow/pull/50912 | `apache/arrow` | `code_only` | `python` | GH-50911: [C++][FlightSQL][ODBC] Replace RapidJSON with JsonWriter |
| https://github.com/apache/arrow/pull/50887 | `apache/arrow` | `code_only_tests_or_fixtures` | `python` | GH-50868: [C++][CI] Suppress deprecated Abseil API warnings for GCS on macOS |
| https://github.com/apache/arrow/pull/50896 | `apache/arrow` | `code_only` | `python` | MINOR: [CI] Bump apache/infrastructure-actions/stash/save from 0ba14156c9f4c3cfbe4b0c9f36339ab0f8d81e53 to bc817c8e9ad7d8216aab74223e32ea... |
| https://github.com/apache/arrow/pull/50895 | `apache/arrow` | `code_only` | `python` | MINOR: [CI] Bump apache/infrastructure-actions/stash/restore from 0ba14156c9f4c3cfbe4b0c9f36339ab0f8d81e53 to bc817c8e9ad7d8216aab74223e3... |
| https://github.com/apache/arrow/pull/50547 | `apache/arrow` | `code_only` | `python` | GH-50542: [C++] Fix ARROW_SIMD_LEVEL=NONE build, compile SSE4.2 kernels |
| https://github.com/apache/arrow/pull/50799 | `apache/arrow` | `code_only` | `python` | GH-50862: [C++][Gandiva] Fix Gandiva tests on riscv64 with an LLVM JIT relocation error |
| https://github.com/apache/arrow/pull/50709 | `apache/arrow` | `code_only` | `python` | GH-50707: [C++][Gandiva] fix out-of-bounds read in mask utf8proc length |
| https://github.com/apache/arrow/pull/50861 | `apache/arrow` | `code_only` | `python` | GH-50860: [Dev][R][Swift][GLib] Simplify pre-commit file patterns for the r, swift, and c_glib directories |
| https://github.com/apache/arrow/pull/50856 | `apache/arrow` | `code_only` | `python` | GH-50855: [R] Fix shellcheck errors in the r/inst/build_arrow_static.sh |
| https://github.com/apache/arrow/pull/49978 | `apache/arrow` | `code_only` | `python` | GH-49977: [C++][Gandiva] Add regexp_extract optional third parameter function version |
| https://github.com/apache/arrow/pull/50137 | `apache/arrow` | `code_only` | `python` | GH-50136: [C++][Gandiva] Enhance CHR to work with unicode |
| https://github.com/apache/arrow/pull/50781 | `apache/arrow` | `code_only` | `python` | GH-50779: [C++][Parquet] Replace remaining RapidJSON usage with simdjson |
| https://github.com/apache/arrow/pull/50850 | `apache/arrow` | `code_only_tests_or_fixtures` | `python` | GH-50849: [Python] Return correct ParquetLogicalType.type for geometry/geography |
| https://github.com/apache/arrow/pull/50835 | `apache/arrow` | `code_only` | `python` | GH-50819: [Release] Increase YUM verification timeout |
| https://github.com/apache/arrow/pull/50802 | `apache/arrow` | `code_and_docs` | `python` | GH-50801: [Python] Expose the `record_batch_reader_source` Acero node (RecordBatchReaderSourceNodeOptions)   |
| https://github.com/apache/arrow/pull/50825 | `apache/arrow` | `code_only` | `python` | GH-50824: [R] Fix shellcheck errors in the r/tools/download_dependencies_R.sh |
| https://github.com/apache/arrow/pull/50187 | `apache/arrow` | `code_only` | `python` | GH-50186: [C++][Gandiva] REPLACE throws "Buffer overflow for output string" for results larger than 64 KB   |
| https://github.com/apache/arrow/pull/50841 | `apache/arrow` | `code_only` | `python` | GH-50840: [C++] Fix dead overflow guard in Take on binary-like arrays |
| https://github.com/apache/arrow/pull/50021 | `apache/arrow` | `code_only` | `python` | GH-49482: [C++][FlightRPC][ODBC] Fix inconsistent SQLGetInfo values in global connection |
| https://github.com/apache/arrow/pull/50815 | `apache/arrow` | `code_and_docs` | `python` | WIP: [Release] Verify release-25.0.1-rc1 |
| https://github.com/apache/arrow/pull/50751 | `apache/arrow` | `code_only` | `python` | GH-50750: [C++][Parquet] Remove code marked as deprecated except flight in versions 23.0.0 and earlier |
| https://github.com/apache/arrow/pull/50821 | `apache/arrow` | `code_only` | `python` | GH-50820: [CI][Dev] Bump ShellCheck to v0.11.0 and simplify pre-commit file patterns for the ci directory |
| https://github.com/apache/arrow/pull/50818 | `apache/arrow` | `code_only` | `python` | GH-50803: [CI][Dev] Fix shellcheck errors in the ci/scripts/r_windows_build.sh |
| https://github.com/apache/arrow/pull/50359 | `apache/arrow` | `code_only` | `python` | GH-50358: [Release] Fix permission issues when binary signing release candidate artifacts |
| https://github.com/apache/arrow/pull/50798 | `apache/arrow` | `code_only` | `python` | GH-50796: [CI][Dev] Fix shellcheck errors in the ci/scripts/r_valgrind.sh |
| https://github.com/apache/arrow/pull/50562 | `apache/arrow` | `code_only` | `python` | GH-50560: [C++][FlightRPC][ODBC] Fix SQLDescribeCol column_size/decimal_digits width |
| https://github.com/apache/arrow/pull/50757 | `apache/arrow` | `code_only` | `python` | GH-50756: [C++][FlightSQL][ODBC] Fix Clang 20 compilation on macOS 26 |
| https://github.com/apache/arrow/pull/50141 | `apache/arrow` | `code_only` | `python` | GH-50140: [C++][Gandiva] Fix castVARCHAR(decimal128) native memory corruption / SIGSEGV on allocation failure |
| https://github.com/apache/arrow/pull/50685 | `apache/arrow` | `code_and_docs` | `python` | GH-50808: [Python] Narrow Feather deprecation to V1 format |
| https://github.com/apache/arrow/pull/50795 | `apache/arrow` | `code_only` | `python` | GH-50777: [CI][Dev] Fix shellcheck errors in the ci/scripts/r_test.sh |
| https://github.com/apache/arrow/pull/50789 | `apache/arrow` | `code_only` | `python` | MINOR: [CI] Bump actions/stale from 10 to 11 |
| https://github.com/apache/arrow/pull/50788 | `apache/arrow` | `code_only` | `python` | MINOR: [CI] Bump docker/login-action from 4.5.1 to 4.6.0 |
| https://github.com/apache/arrow/pull/50786 | `apache/arrow` | `code_only` | `python` | GH-50495: [R] 25.0.0 Release followups |
| https://github.com/apache/arrow/pull/50650 | `apache/arrow` | `code_only` | `python` | GH-50648: [Packaging][Linux] Enable OpenTelemetry |
| https://github.com/apache/arrow/pull/50782 | `apache/arrow` | `code_only` | `python` | MINOR: [Dev] Update collaborators list |
| https://github.com/apache/arrow/pull/50761 | `apache/arrow` | `code_only` | `python` | GH-50760: [CI][Python] Create venv for test-fedora-42-python-3 |
| https://github.com/apache/arrow/pull/50772 | `apache/arrow` | `code_only` | `python` | GH-50771: [CI][Dev] Fix shellcheck errors in the ci/scripts/r_install_system_dependencies.sh |
| https://github.com/apache/arrow/pull/50775 | `apache/arrow` | `code_only` | `python` | GH-50773: [CI][Dev] Fix shellcheck errors in the ci/scripts/r_sanitize.sh |
| https://github.com/apache/arrow/pull/50767 | `apache/arrow` | `code_only` | `python` | GH-50766: [CI][Dev] Fix shellcheck errors in the ci/scripts/r_docker_configure.sh |
| https://github.com/apache/arrow/pull/50610 | `apache/arrow` | `code_only` | `python` | GH-50609: [CI][Dev] Fix shellcheck errors in the ci/scripts/r_deps.sh |
| https://github.com/apache/arrow/pull/50725 | `apache/arrow` | `code_only` | `python` | GH-50724: [C++] Add `JsonWriter::WriteValue` for simdjson values |
| https://github.com/apache/arrow/pull/50759 | `apache/arrow` | `code_only` | `python` | GH-50758: [CI][C++] Use LLVM 22 on Debian experimental |
| https://github.com/apache/arrow/pull/50738 | `apache/arrow` | `code_only` | `python` | GH-50737: [C++][Parquet] mark `MakeStatistics` method without `ColumnDescriptor` as deprecated |
| https://github.com/apache/arrow/pull/50754 | `apache/arrow` | `code_only` | `python` | GH-50752: [C++][Compute] Fix unused variable warning when ARROW_WITH_RE2 is disabled |
| https://github.com/apache/arrow/pull/50675 | `apache/arrow` | `code_only` | `python` | GH-50395: [C++] Support duration inputs in temporal rounding |
| https://github.com/apache/arrow/pull/50745 | `apache/arrow` | `code_only` | `python` | GH-50744: [R] Add read_ipc_file and write_ipc_file to _pkgdown.yml reference index |
| https://github.com/apache/arrow/pull/50687 | `apache/arrow` | `code_only` | `python` | GH-50684: [Python][FlightRPC] Break the reference cycle between the C++ FlightServerBase and the Python object to avoid leaking server |
| https://github.com/apache/arrow/pull/50700 | `apache/arrow` | `code_only` | `python` | GH-50578: [C++][FlightRPC][ODBC] Always return SQL_NO_DATA from GetMoreResults |
| https://github.com/apache/arrow/pull/50714 | `apache/arrow` | `code_only` | `python` | GH-50713: [C++] Replace `return_type` and `enable_if_return` with <type_traits> helpers |
| https://github.com/apache/arrow/pull/50611 | `apache/arrow` | `code_only` | `python` | GH-50503: [Parquet] Remove SVE128 unpack |
| https://github.com/apache/arrow/pull/50734 | `apache/arrow` | `code_only` | `python` | GH-50688: [CI] Remove brew update to fix macOS arrow-s3fs-test segfaults |
| https://github.com/apache/arrow/pull/50646 | `apache/arrow` | `code_only_tests_or_fixtures` | `python` | GH-49305: [Python] Expose RecordBatchFileReader.count_rows |
| https://github.com/apache/arrow/pull/50732 | `apache/arrow` | `code_only` | `python` | GH-50730: [C++] Do not use throwing <simdjson> api |
| https://github.com/apache/arrow/pull/50681 | `apache/arrow` | `code_and_docs` | `python` | GH-50674: [Release] Add support for recovering Yum repositories |
| https://github.com/apache/arrow/pull/50534 | `apache/arrow` | `code_only` | `python` | GH-44183: [C++] Support run-end encoded struct, list (view), large list (view) and map values |
| https://github.com/apache/arrow/pull/50723 | `apache/arrow` | `code_only` | `python` | GH-50660: [C++][Dev] Add Decimal32 and Decimal64 GDB pretty-printers |
| https://github.com/apache/arrow/pull/50705 | `apache/arrow` | `code_only` | `python` | GH-50636: [C++] Replace std::span/ranges usage to fix macOS CRAN |
| https://github.com/apache/arrow/pull/50717 | `apache/arrow` | `code_only` | `python` | GH-50716: [C++][CI] Make simdjson required for Parquet |
| https://github.com/apache/arrow/pull/50672 | `apache/arrow` | `code_only` | `python` | GH-50654: [C++] Support simdjson without exceptions |
| https://github.com/apache/arrow/pull/50721 | `apache/arrow` | `code_only_tests_or_fixtures` | `python` | GH-50718: [C++][CI] Fix valgrind use of uninitialised value on FixedSizeListTestCase |
| https://github.com/apache/arrow/pull/50708 | `apache/arrow` | `code_only` | `python` | GH-50706: [C++] Migrate extension type serialization to JsonWriter |
| https://github.com/apache/arrow/pull/50691 | `apache/arrow` | `code_only` | `python` | GH-50690: [C++] Migrate ObjectWriter users to JsonWriter |
| https://github.com/apache/arrow/pull/50347 | `apache/arrow` | `code_only` | `python` | GH-50338: [C++] Add ComputeLogicalNullCount to Datum |
| https://github.com/apache/arrow/pull/50649 | `apache/arrow` | `code_only` | `python` | GH-50600: [Release][Python] Fix verification jobs after dropping Python 3.10 |
| https://github.com/apache/arrow/pull/50475 | `apache/arrow` | `code_only` | `python` | GH-37476: [C++][Python] Preserve unsigned dictionary index types when building from values |
| https://github.com/apache/arrow/pull/50653 | `apache/arrow` | `code_only` | `python` | GH-50627: [C++] Migrate from_string.cc to simdjson |
| https://github.com/apache/arrow/pull/50568 | `apache/arrow` | `code_only` | `python` | GH-50567: [C++] Introduce JsonWriter and migrate integration JSON writer |
| https://github.com/apache/arrow/pull/50669 | `apache/arrow` | `code_only` | `python` | GH-40163: [Archery] Avoid setuptools_scm internal API |
| https://github.com/apache/arrow/pull/50683 | `apache/arrow` | `code_only` | `python` | GH-50680: [C++][Dev] Extend type IDs in gdb_arrow.py |
| https://github.com/apache/arrow/pull/50679 | `apache/arrow` | `code_only` | `python` | GH-50678: [C++][Parquet] Remove unused member `null_slot_usage` in struct `LevelInfo` |
| https://github.com/apache/arrow/pull/50642 | `apache/arrow` | `code_only` | `python` | GH-50641: [C++][Compute] Fix correctness error in decimal round_binary kernel |
| https://github.com/apache/arrow/pull/50520 | `apache/arrow` | `code_only` | `python` | GH-50519: [C++][FlightRPC][ODBC] Add missing `ARROW_FLIGHT_SQL_ODBC_INSTALLER` option entry |
| https://github.com/apache/arrow/pull/50671 | `apache/arrow` | `code_only` | `python` | GH-50670: [Release][Dev] Fix only shellcheck SC2086 errors in the dev directory |
| https://github.com/apache/arrow/pull/50271 | `apache/arrow` | `code_only` | `python` | GH-35692: [C++][Parquet] Support to read fixed size list array with nulls |
| https://github.com/apache/arrow/pull/50664 | `apache/arrow` | `code_only` | `python` | MINOR: [CI] Bump actions/labeler from 6 to 7 |
| https://github.com/apache/arrow/pull/50663 | `apache/arrow` | `code_only` | `python` | MINOR: [CI] Bump docker/login-action from 4.4.0 to 4.5.1 |
| https://github.com/apache/arrow/pull/50625 | `apache/arrow` | `code_only` | `python` | GH-50624: [C++][Compute] Tighten case_when exact dispatch for parameterized types |
| https://github.com/apache/arrow/pull/50584 | `apache/arrow` | `code_only` | `python` | GH-50508: [C++] Support scalar values in AppendScalars |
| https://github.com/apache/arrow/pull/50616 | `apache/arrow` | `code_only` | `python` | GH-50615: [C++] Reduce code generation for string kernels |
| https://github.com/apache/arrow/pull/50248 | `apache/arrow` | `code_only` | `python` | GH-50247: [C++] Reuse abstraction for null partitions in sorting functions |
| https://github.com/apache/arrow/pull/50640 | `apache/arrow` | `code_only_tests_or_fixtures` | `python` | GH-49046: [Dev][Python] Remove unused scripts under python/scripts |
| https://github.com/apache/arrow/pull/50602 | `apache/arrow` | `code_only` | `python` | GH-50601: [C++] Refactor TranslateTo for clearer semantics |
| https://github.com/apache/arrow/pull/47403 | `apache/arrow` | `code_only` | `python` | GH-47402: [CI][Dev] Fix shellcheck errors in the ci/scripts/python_test_emscripten.sh |
| https://github.com/apache/arrow/pull/50606 | `apache/arrow` | `code_only` | `python` | GH-50565: [CI][C++] Add a JNI Windows CI job |
| https://github.com/apache/arrow/pull/50281 | `apache/arrow` | `code_only` | `python` | GH-50280: [C++] Implement VisitTwoBitRuns and VisitTwoSetBitRuns methods |
| https://github.com/apache/arrow/pull/50465 | `apache/arrow` | `code_only` | `python` | GH-50464: [C++][Python] Simplify arrow_to_pandas DateOffset handling for nanoseconds/milliseconds |
| https://github.com/apache/arrow/pull/50590 | `apache/arrow` | `code_only` | `python` | GH-50572: [Ruby] Add `ArrowFormat::RecordBatch#records` |
| https://github.com/apache/arrow/pull/50608 | `apache/arrow` | `code_only_tests_or_fixtures` | `python` | GH-50579: [Python] Fix test_categorical_order_survives_roundtrip pandas 3.X deprecation |
| https://github.com/apache/arrow/pull/50327 | `apache/arrow` | `code_only_tests_or_fixtures` | `python` | GH-50326: [Python] Convert arrays to Python objects without per-element Scalars in to_pylist |
| https://github.com/apache/arrow/pull/50598 | `apache/arrow` | `code_only_tests_or_fixtures` | `python` | GH-50597: [CI] Retry Chrome PyArrow load and fix Snappy Emscripten configure |
| https://github.com/apache/arrow/pull/50594 | `apache/arrow` | `code_only` | `python` | GH-50591: [Python] Fix reference in ConvertToSequenceAndInferSize when an iterator raises on array conversion |
| https://github.com/apache/arrow/pull/50502 | `apache/arrow` | `code_only` | `python` | GH-37004: [C++][Python] Fix dropped child data when viewing/casting e… |
| https://github.com/apache/arrow/pull/50423 | `apache/arrow` | `code_only` | `python` | GH-48679: [C++] Fix pivot_wider with non-monotonic group ids |
| https://github.com/apache/arrow/pull/50214 | `apache/arrow` | `code_only` | `python` | GH-50210: [C++][Gandiva] Replace precompiled std::string to fix _Unwind_Resume JIT failure on JNI builds |
| https://github.com/apache/arrow/pull/50066 | `apache/arrow` | `code_only` | `python` | GH-50065: [Packaging][CI][C++] Drop unused libboost-system-dev |
| https://github.com/apache/arrow/pull/50425 | `apache/arrow` | `code_only` | `python` | GH-50424: [CI] install Chrome latest for test-conda-python-emscripten |
| https://github.com/apache/arrow/pull/50396 | `apache/arrow` | `code_only` | `python` | GH-50394: [Docs][C++] Reduce Sphinx warnings when building HTML |
| https://github.com/apache/arrow/pull/50321 | `apache/arrow` | `code_only` | `python` | GH-49231: [C++] Deprecate Feather reader and writer |
| https://github.com/apache/arrow/pull/50361 | `apache/arrow` | `code_only` | `python` | MINOR: [CI] Install libncurses-dev from unstable on Debian experimental |
| https://github.com/apache/arrow/pull/50586 | `apache/arrow` | `code_only` | `python` | GH-50585: [CI][C++] Use bundled simdjson on Alpine Linux |
| https://github.com/apache/arrow/pull/50583 | `apache/arrow` | `code_only` | `python` | GH-50582: [CI][C++] Install missing `simdjson-static` on Alpine Linux |
| https://github.com/apache/arrow/pull/50483 | `apache/arrow` | `code_only` | `python` | GH-50481: [C++] Fix CSV reader mis-parsing rows with an embedded NUL byte |
| https://github.com/apache/arrow/pull/50557 | `apache/arrow` | `code_only` | `python` | GH-50573: [CI][C++] Remove brew workaround for aws-sdk-cpp |
| https://github.com/apache/arrow/pull/50577 | `apache/arrow` | `code_only` | `python` | GH-50575: [CI][Dev] Fix shellcheck errors in the ci/scripts/python_wheel_xlinux_build.sh |
| https://github.com/apache/arrow/pull/50570 | `apache/arrow` | `code_only` | `python` | GH-50569: [Ruby] Add `ArrowFormat::RecordBatch.new(values)` |
| https://github.com/apache/arrow/pull/50589 | `apache/arrow` | `code_only` | `python` | GH-50588: [Ruby] Add `ArrowFormat::Array#[]` |
| https://github.com/apache/arrow/pull/50469 | `apache/arrow` | `code_only` | `python` | GH-50566: [C++] Introduce simdjson and migrate ObjectParser |
| https://github.com/apache/arrow/pull/49858 | `apache/arrow` | `code_only` | `python` | GH-39961: [C++][Python] Propagate CSV parse delimiter to write options |
| https://github.com/apache/arrow/pull/50564 | `apache/arrow` | `code_only` | `python` | MINOR: [CI] Bump actions/setup-python from 6 to 7 |
| https://github.com/apache/arrow/pull/50552 | `apache/arrow` | `code_only` | `python` | GH-50551: [CI][Dev] Fix shellcheck errors in the ci/scripts/python_wheel_macos_build.sh |
| https://github.com/apache/arrow/pull/50536 | `apache/arrow` | `code_only` | `python` | GH-50535: [CI][Dev] Fix shellcheck errors in the ci/scripts/python_test.sh |
| https://github.com/apache/arrow/pull/50563 | `apache/arrow` | `code_only` | `python` | MINOR: [R] Update backwards compatibility matrix for 25.0.0 release |
| https://github.com/apache/arrow/pull/50489 | `apache/arrow` | `code_only` | `python` | GH-50487: [C++] Extra semicolon warning from ARROW_SUPPRESS_DEPRECATION_WARNING macro with -Wpedantic |
| https://github.com/apache/arrow/pull/50494 | `apache/arrow` | `code_only` | `python` | GH-50493: [Python] Use scikit-build-core force-include and remove custom build-backend to copy license files |
| https://github.com/apache/arrow/pull/50543 | `apache/arrow` | `code_only_tests_or_fixtures` | `python` | GH-49255: [Python] Fix pandas Categorical DeprecationWarnings in tests |
| https://github.com/apache/arrow/pull/50533 | `apache/arrow` | `code_only` | `python` | GH-50532: [R][CI] R nightly binary upload broken since github3 to pygithub migration |
| https://github.com/apache/arrow/pull/50529 | `apache/arrow` | `code_only` | `python` | GH-50528: [Ruby] Add `ArrowFormat::ArrayBuilder` |
| https://github.com/apache/arrow/pull/50463 | `apache/arrow` | `code_only` | `python` | GH-50462: [C++][Gandiva] fix out-of-bounds read in translate_utf8_utf8_utf8 |
| https://github.com/apache/arrow/pull/50511 | `apache/arrow` | `code_only` | `python` | GH-50510: [CI][Dev] Fix shellcheck error in the ci/scripts/ccache_fix_perms.sh |
| https://github.com/apache/arrow/pull/48223 | `apache/arrow` | `code_only` | `python` | GH-48222: [CI][Dev] Fix shellcheck errors in ci/scripts/cpp_build.sh |
| https://github.com/apache/arrow/pull/50467 | `apache/arrow` | `code_only` | `python` | GH-50379: [Dev] Convert invalid PRs to draft automatically |
| https://github.com/apache/arrow/pull/49553 | `apache/arrow` | `code_only` | `python` | GH-32123: [R] Expose azure blob filesystem |
| https://github.com/apache/arrow/pull/50458 | `apache/arrow` | `code_only` | `python` | GH-50457: [C++][Gandiva] Add LN alias for LOG |
| https://github.com/apache/arrow/pull/50422 | `apache/arrow` | `code_only` | `python` | GH-50421: [C++][Parquet] Add LevelDecoder Skip and Count |
| https://github.com/apache/arrow/pull/50460 | `apache/arrow` | `code_only` | `python` | GH-50456: [Ruby] Add `ArrowFormat::DurationType#==` |
| https://github.com/apache/arrow/pull/50452 | `apache/arrow` | `code_only` | `python` | GH-50439: Add ArrowFormat::{,Large}{Binary,UTF8}Array.new(values) |
| https://github.com/apache/arrow/pull/50461 | `apache/arrow` | `code_only` | `python` | GH-50455: [Ruby] Add `ArrowFormat::TimeType#==` |
| https://github.com/apache/arrow/pull/50447 | `apache/arrow` | `code_only` | `python` | GH-50438: Add ArrowFormat::DurationArray.new(unit, values) |
| https://github.com/apache/arrow/pull/50445 | `apache/arrow` | `code_only` | `python` | GH-50436: [Ruby] Add `ArrowFormat::TimestampArray.new(unit, values)` |
| https://github.com/apache/arrow/pull/50411 | `apache/arrow` | `code_and_docs` | `python` | GH-50410: [Python][Packaging] Drop Python 3.10 support |
| https://github.com/apache/arrow/pull/50443 | `apache/arrow` | `code_only` | `python` | GH-50435: [Ruby] Add `ArrowFormat::Time{32,64}.new(unit, values)` |
| https://github.com/apache/arrow/pull/50416 | `apache/arrow` | `code_only_tests_or_fixtures` | `python` | GH-37853: [Python] Remove test and fixture involving fastparquet |
| https://github.com/apache/arrow/pull/50442 | `apache/arrow` | `code_only` | `python` | GH-50434: [Ruby] Add `ArrowFormat::Date{32,64}.new(values)` |
| https://github.com/apache/arrow/pull/50433 | `apache/arrow` | `code_only` | `python` | GH-50432: [Ruby] Add `ArrowFormat::{Array,Bitmap}#==` |
| https://github.com/apache/arrow/pull/50413 | `apache/arrow` | `code_only` | `python` | GH-50412: [CI][GLib][Ruby] Remove some unnecessary Ubuntu 20.04 cases |
| https://github.com/apache/arrow/pull/50401 | `apache/arrow` | `code_only` | `python` | GH-50302: [GLib][Ruby][FlightRPC] Fix GC related problems |
| https://github.com/apache/arrow/pull/50444 | `apache/arrow` | `code_and_docs` | `python` | GH-48808: [Python] Drop support for Pandas < 2.0.3 |
| https://github.com/apache/arrow/pull/50357 | `apache/arrow` | `code_and_docs` | `python` | WIP: [Release] Verify release-25.0.0-rc1 |
| https://github.com/apache/arrow/pull/50459 | `apache/arrow` | `code_only` | `python` | GH-50437: [Ruby] Add `ArrowFormat::*IntervalArray.new(values)` |
| https://github.com/apache/arrow/pull/50418 | `apache/arrow` | `code_only` | `python` | GH-50417: [CI][Dev] Fix shellcheck error in ci/scripts/install_bison.sh |
| https://github.com/apache/arrow/pull/47206 | `apache/arrow` | `code_only` | `python` | GH-47395: [R] Update fedora-clang to install latest clang version to match CRAN setup |
| https://github.com/apache/arrow/pull/50356 | `apache/arrow` | `code_only` | `python` | GH-50355: [C++][Gandiva] fix out-of-bounds read in utf8_length_ignore_invalid |
| https://github.com/apache/arrow/pull/50374 | `apache/arrow` | `code_and_docs` | `python` | GH-50339: [R] read_ipc_stream fails to unify nested uint64 fields inside a Struct array across record batches |
| https://github.com/apache/arrow/pull/50381 | `apache/arrow` | `code_only` | `python` | GH-50380: [C++][Gandiva] fix out-of-bounds read in byte_substr past end |
| https://github.com/apache/arrow/pull/50400 | `apache/arrow` | `code_only_tests_or_fixtures` | `python` | GH-50399: [C++][Gandiva] Use timegm in DaysSince helper in Gandiva date_time_test |
| https://github.com/apache/arrow/pull/50366 | `apache/arrow` | `code_only` | `python` | GH-50251: [C++] Add GetSpan to ArrayData |
| https://github.com/apache/arrow/pull/50404 | `apache/arrow` | `code_only` | `python` | GH-50403: [C++] Remove ArrayBuilder::AppendToBitmap |
| https://github.com/apache/arrow/pull/50224 | `apache/arrow` | `code_only` | `python` | GH-50223: [C++][Compute] Support string_view/binary_view keys in the hash-aggregate Grouper |
| https://github.com/apache/arrow/pull/50391 | `apache/arrow` | `code_only` | `python` | GH-50390: [Ruby] Add int/float array builder for red-arrow-format |
| https://github.com/apache/arrow/pull/50393 | `apache/arrow` | `code_only` | `python` | MINOR: [CI] Bump docker/login-action from 4.2.0 to 4.4.0 |
| https://github.com/apache/arrow/pull/50387 | `apache/arrow` | `code_only` | `python` | GH-50388: [C++][CI] Make ccache effective MSVC-based builds |
| https://github.com/apache/arrow/pull/50124 | `apache/arrow` | `code_only` | `python` | MINOR: [C++][Gandiva] cast to unsigned char before ctype calls |
| https://github.com/apache/arrow/pull/50386 | `apache/arrow` | `code_only` | `python` | GH-50385: [Ruby] Add bitmap builder for red-arrow-format |
| https://github.com/apache/arrow/pull/50288 | `apache/arrow` | `code_only` | `python` | GH-47877: [Packaging][C++][FlightRPC][ODBC] Add arrow-flight-sql-odbc |
| https://github.com/apache/arrow/pull/50346 | `apache/arrow` | `code_only` | `python` | GH-50345: [CI] Remove redundant checkout step from check_labels.yml |
| https://github.com/apache/arrow/pull/50337 | `apache/arrow` | `code_only` | `python` | GH-50336: [Release][Archery] Fix archery GitHub integration for release scripts |
| https://github.com/apache/arrow/pull/50340 | `apache/arrow` | `code_only` | `python` | GH-50293: [CI] Run check-labels for all triggers to avoid cancelling further steps and add tag to set_enabled |
| https://github.com/apache/arrow/pull/41870 | `apache/arrow` | `code_only` | `python` | GH-40062: [C++][Python] Conversion of Table to Arrow Tensor |
| https://github.com/apache/arrow/pull/50323 | `apache/arrow` | `code_only` | `python` | GH-50316: [C++][CI] Install libboost-process-dev on Debian experimental |
| https://github.com/apache/arrow/pull/50322 | `apache/arrow` | `code_only` | `python` | GH-50311: [C++] `KeyValueMetadata::Delete` returns IndexError instead of crashing due to seg fault |
| https://github.com/storybookjs/storybook/pull/36040 | `storybookjs/storybook` | `code_only` | `typescript` | Vue: Raise the vue-component-meta floor to ^3.3.9 |
| https://github.com/storybookjs/storybook/pull/36038 | `storybookjs/storybook` | `code_only` | `typescript` | Core: Keep Tabs memo out of an esbuild joined var |
| https://github.com/storybookjs/storybook/pull/36029 | `storybookjs/storybook` | `code_only` | `typescript` | CLI: Render the same toolset output as MCP |
| https://github.com/storybookjs/storybook/pull/35980 | `storybookjs/storybook` | `code_only` | `typescript` | Core: Allow token-only WebSocket upgrade without Origin |
| https://github.com/storybookjs/storybook/pull/36027 | `storybookjs/storybook` | `code_only` | `typescript` | Vue: Substitute static arg values in template snippet expressions |
| https://github.com/storybookjs/storybook/pull/36030 | `storybookjs/storybook` | `code_only` | `typescript` | Vue: Fix Component Metadata in Production Builds |
| https://github.com/storybookjs/storybook/pull/36003 | `storybookjs/storybook` | `code_only` | `typescript` | Angular: hoist non-literal args onto the host component instead of inlining them |
| https://github.com/storybookjs/storybook/pull/35417 | `storybookjs/storybook` | `code_and_docs` | `typescript` | CLI: Offer the new 10.5 experimental feature flags during upgrade |
| https://github.com/storybookjs/storybook/pull/36024 | `storybookjs/storybook` | `code_only` | `typescript` | CLI: Point the init outro at `storybook skills get setup` and remove duplicate sandbox addon |
| https://github.com/storybookjs/storybook/pull/36026 | `storybookjs/storybook` | `code_only` | `typescript` | Angular Vite: Resolve tsConfig against the workspace root |
| https://github.com/storybookjs/storybook/pull/35959 | `storybookjs/storybook` | `code_only` | `typescript` | Core: Resolve tsconfig paths from the defining config |
| https://github.com/storybookjs/storybook/pull/35951 | `storybookjs/storybook` | `code_only` | `typescript` | Performance: Halve the tools CLI cold-boot time |
| https://github.com/storybookjs/storybook/pull/36001 | `storybookjs/storybook` | `code_only` | `typescript` | Vue: Fix docgen fidelity gaps |
| https://github.com/storybookjs/storybook/pull/36002 | `storybookjs/storybook` | `code_only` | `typescript` | Angular: Install the `@storybook/angular-vite` peers that nothing else brings in |
| https://github.com/storybookjs/storybook/pull/35999 | `storybookjs/storybook` | `code_only` | `typescript` | Angular: Resolve `@angular/core` through the package manager, not the raw specifier |
| https://github.com/storybookjs/storybook/pull/36000 | `storybookjs/storybook` | `code_only` | `typescript` | Manifest debugger: Show the API description and snippet warnings |
| https://github.com/storybookjs/storybook/pull/35963 | `storybookjs/storybook` | `code_only` | `typescript` | Mcp: Support JsDoc annotations in component documentation |
| https://github.com/storybookjs/storybook/pull/35993 | `storybookjs/storybook` | `code_and_docs` | `typescript` | Open-Service: Share dynamic snippets across browser surfaces |
| https://github.com/storybookjs/storybook/pull/33593 | `storybookjs/storybook` | `code_only` | `typescript` | Search: Add docs headings to search results |
| https://github.com/storybookjs/storybook/pull/35998 | `storybookjs/storybook` | `code_only` | `typescript` | Angular: Resolve builder `styles` the way the Angular builders do |
| https://github.com/storybookjs/storybook/pull/35979 | `storybookjs/storybook` | `code_only` | `typescript` | Vue: Extract component JSDoc through TypeScript's APIs |
| https://github.com/storybookjs/storybook/pull/35977 | `storybookjs/storybook` | `code_only` | `typescript` | Angular: Extract component JSDoc through TypeScript's APIs |
| https://github.com/storybookjs/storybook/pull/35976 | `storybookjs/storybook` | `code_only` | `typescript` | Core: Make TypeScript's JSDoc semantics canonical for component docgen |
| https://github.com/storybookjs/storybook/pull/35974 | `storybookjs/storybook` | `code_only` | `typescript` | Angular: Resolve builder styles against the workspace root |
| https://github.com/storybookjs/storybook/pull/35971 | `storybookjs/storybook` | `code_only` | `typescript` | Angular: Migrate Analog projects to angular-vite instead of refusing them |
| https://github.com/storybookjs/storybook/pull/35975 | `storybookjs/storybook` | `code_only` | `typescript` | CI: Allow Verdaccio to republish vite-plugin-storybook-nextjs |
| https://github.com/storybookjs/storybook/pull/35965 | `storybookjs/storybook` | `code_only` | `typescript` | Docs: Surface the story-docs snippet warning in docs and the Code panel |
| https://github.com/storybookjs/storybook/pull/35950 | `storybookjs/storybook` | `code_and_docs` | `typescript` | ESLint Plugin: Bundle CSF helpers so the plugin loads without storybook |
| https://github.com/storybookjs/storybook/pull/35966 | `storybookjs/storybook` | `code_only` | `typescript` | Docs: Declare the font on overlay surfaces so docs tooltips are not left to inherit |
| https://github.com/storybookjs/storybook/pull/35945 | `storybookjs/storybook` | `code_only` | `typescript` | Core: Fetch static open-service snapshots relative to the document |
| https://github.com/storybookjs/storybook/pull/35939 | `storybookjs/storybook` | `code_only` | `typescript` | Build: Fix React Native sandbox generation under age gate |
| https://github.com/storybookjs/storybook/pull/35929 | `storybookjs/storybook` | `code_only` | `typescript` | Core: Pin oxc-resolver to 11.21.2 to keep tsconfig path aliases on solution-style tsconfigs |
| https://github.com/storybookjs/storybook/pull/35844 | `storybookjs/storybook` | `code_only` | `typescript` | React: Preserve discriminated union prop values in metadata extraction |
| https://github.com/storybookjs/storybook/pull/35530 | `storybookjs/storybook` | `code_only` | `typescript` | Dependencies: Bump Vitest to 4.1.6 (CVE-2026-47428) |
| https://github.com/storybookjs/storybook/pull/35942 | `storybookjs/storybook` | `code_and_docs` | `typescript` | Release: Patch 10.5.10 |
| https://github.com/storybookjs/storybook/pull/35882 | `storybookjs/storybook` | `code_only` | `typescript` | Nextjs-Vite: Recover from Next.js 16.3 raw config cache |
| https://github.com/storybookjs/storybook/pull/9123 | `storybookjs/storybook` | `code_only` | `typescript` | Preact: Fix story function typescript type |
| https://github.com/storybookjs/storybook/pull/35797 | `storybookjs/storybook` | `code_only` | `typescript` | Angular: Read the story shapes that supply their own markup |
| https://github.com/storybookjs/storybook/pull/35946 | `storybookjs/storybook` | `code_and_docs` | `typescript` | Angular: Fix eight upgrade and migration bugs |
| https://github.com/storybookjs/storybook/pull/35964 | `storybookjs/storybook` | `code_only` | `typescript` | Core: Recover from a docgen worker death instead of going dark for the session |
| https://github.com/storybookjs/storybook/pull/35952 | `storybookjs/storybook` | `code_and_docs` | `typescript` | Angular: Fix component resolution, MCP output, and dev/build path aliasing |
| https://github.com/storybookjs/storybook/pull/35948 | `storybookjs/storybook` | `code_only` | `typescript` | Vue: Add a dedicated sandbox for server docgen |
| https://github.com/storybookjs/storybook/pull/35943 | `storybookjs/storybook` | `code_only` | `typescript` | Angular: Bind only what the component accepts in story snippets, and report the rest |
| https://github.com/storybookjs/storybook/pull/35953 | `storybookjs/storybook` | `code_only` | `typescript` | Angular: Render self-closing tags in server-side docs snippets |
| https://github.com/storybookjs/storybook/pull/35927 | `storybookjs/storybook` | `code_and_docs` | `typescript` | Vue: Deprecate vue-docgen-api |
| https://github.com/storybookjs/storybook/pull/35821 | `storybookjs/storybook` | `code_only` | `typescript` | Vue: Follow a re-export to the component that declares it |
| https://github.com/storybookjs/storybook/pull/35924 | `storybookjs/storybook` | `code_and_docs` | `typescript` | MCP: Document the AI surface for every framework, not just React |
| https://github.com/storybookjs/storybook/pull/35931 | `storybookjs/storybook` | `code_only` | `typescript` | Core: Warn when multiple story files collapse onto one componentId |
| https://github.com/storybookjs/storybook/pull/35940 | `storybookjs/storybook` | `code_only` | `typescript` | Docgen server: Fix the MCP snapshot CI break, and two snippet-printing bugs from review |
| https://github.com/storybookjs/storybook/pull/35900 | `storybookjs/storybook` | `code_only` | `typescript` | Vue: Provide apiDescription in the manifest |
| https://github.com/storybookjs/storybook/pull/35938 | `storybookjs/storybook` | `code_only` | `typescript` | CI: Parse Yarn publish output when lines include ANSI color codes |
| https://github.com/storybookjs/storybook/pull/35930 | `storybookjs/storybook` | `code_only` | `typescript` | Docgen server: Share the story-args pass and honor write order in static resolution |
| https://github.com/storybookjs/storybook/pull/35937 | `storybookjs/storybook` | `code_only` | `typescript` | CI: Fix staged npm publish retries on latest-release |
| https://github.com/storybookjs/storybook/pull/34318 | `storybookjs/storybook` | `code_only` | `typescript` | Addon-Pseudo-States: Fix pseudo-states rewriting for nested functional selectors |
| https://github.com/storybookjs/storybook/pull/35533 | `storybookjs/storybook` | `code_only` | `typescript` | Webpack: Prevent long preview output filenames |
| https://github.com/storybookjs/storybook/pull/35505 | `storybookjs/storybook` | `code_only_tests_or_fixtures` | `typescript` | TanStack: Render real link hrefs in the Link mock |
| https://github.com/storybookjs/storybook/pull/35660 | `storybookjs/storybook` | `code_only` | `typescript` | TanStack: Keep the layout id when cloning a standalone index file route |
| https://github.com/storybookjs/storybook/pull/35521 | `storybookjs/storybook` | `code_only` | `typescript` | Preview: Fix crash when initialising UrlStore on a docs path |
| https://github.com/storybookjs/storybook/pull/35831 | `storybookjs/storybook` | `code_only` | `typescript` | Core: Split module-graph into hot revisions and cold index services |
| https://github.com/storybookjs/storybook/pull/35825 | `storybookjs/storybook` | `code_only` | `typescript` | Core: Skip module-graph reverse-index mirror when a patch is a no-op |
| https://github.com/storybookjs/storybook/pull/35629 | `storybookjs/storybook` | `code_only` | `typescript` | Pseudo-States: Make stylesheet rewrites WebKit-safe |
| https://github.com/storybookjs/storybook/pull/35918 | `storybookjs/storybook` | `code_and_docs` | `typescript` | Release: Patch 10.5.9 |
| https://github.com/storybookjs/storybook/pull/35921 | `storybookjs/storybook` | `code_only` | `typescript` | Angular: Keep the function control on constructor and generic signatures |
| https://github.com/storybookjs/storybook/pull/35884 | `storybookjs/storybook` | `code_only` | `typescript` | Nextjs-Vite: Support % in next/font/local declarations |
| https://github.com/storybookjs/storybook/pull/35917 | `storybookjs/storybook` | `code_only` | `typescript` | CI: Recover publish from staged npm 409s |
| https://github.com/storybookjs/storybook/pull/35896 | `storybookjs/storybook` | `code_only` | `typescript` | Angular: Give agents real input and output documentation |
| https://github.com/storybookjs/storybook/pull/35920 | `storybookjs/storybook` | `code_only` | `typescript` | Vue: Decouple server side docgen from docgen options |
| https://github.com/storybookjs/storybook/pull/35907 | `storybookjs/storybook` | `code_only` | `typescript` | Core: Restore the args a server-docgen preview cannot type |
| https://github.com/storybookjs/storybook/pull/35902 | `storybookjs/storybook` | `code_only` | `typescript` | Vue: Don't override story-snippet if already provided |
| https://github.com/storybookjs/storybook/pull/35906 | `storybookjs/storybook` | `code_only` | `typescript` | Angular: Skip the runtime source decorator when the docgen server produces snippets |
| https://github.com/storybookjs/storybook/pull/35899 | `storybookjs/storybook` | `code_only` | `typescript` | Angular: Stop marking a defaulted input as required in the props table |
| https://github.com/storybookjs/storybook/pull/35895 | `storybookjs/storybook` | `code_only` | `typescript` | Angular: Declare story args the snippet markup binds by name |
| https://github.com/storybookjs/storybook/pull/35897 | `storybookjs/storybook` | `code_only` | `typescript` | Core: Scope in-flight open-service loads to their runtime |
| https://github.com/storybookjs/storybook/pull/35888 | `storybookjs/storybook` | `code_only` | `typescript` | Angular: Print unevaluable story args instead of slicing the file |
| https://github.com/storybookjs/storybook/pull/35839 | `storybookjs/storybook` | `code_only` | `typescript` | Vue: Support h() render trees and @import overrides for snippets |
| https://github.com/storybookjs/storybook/pull/35867 | `storybookjs/storybook` | `code_only` | `typescript` | Vue: Fix h() snippet markup and unify arg classification |
| https://github.com/storybookjs/storybook/pull/35798 | `storybookjs/storybook` | `code_only` | `typescript` | Angular: Report what a snippet could not resolve |
| https://github.com/storybookjs/storybook/pull/35706 | `storybookjs/storybook` | `code_only` | `typescript` | Tanstack React: Remove @cloudflare/vite-plugin from the inherited Vite config |
| https://github.com/storybookjs/storybook/pull/35528 | `storybookjs/storybook` | `code_only_tests_or_fixtures` | `typescript` | Test: Fix Illegal invocation when reading prototype.focus |
| https://github.com/storybookjs/storybook/pull/35784 | `storybookjs/storybook` | `code_and_docs` | `typescript` | Tanstack: Wait for router to load before rendering |
| https://github.com/storybookjs/storybook/pull/35785 | `storybookjs/storybook` | `code_only_tests_or_fixtures` | `typescript` | Build: Stop snapshotting patch-label clientMutationId UUIDs |
| https://github.com/storybookjs/storybook/pull/35772 | `storybookjs/storybook` | `code_only` | `typescript` | Build: Age-gate npm installs during sandbox scaffold |
| https://github.com/storybookjs/storybook/pull/35743 | `storybookjs/storybook` | `code_only` | `typescript` | React: Fix RDT tsconfig selection for Vite project references |
| https://github.com/storybookjs/storybook/pull/35801 | `storybookjs/storybook` | `code_and_docs` | `typescript` | Release: Patch 10.5.8 |
| https://github.com/storybookjs/storybook/pull/35823 | `storybookjs/storybook` | `code_only` | `typescript` | Vue: Support story template for snippet generation |
| https://github.com/storybookjs/storybook/pull/35881 | `storybookjs/storybook` | `code_only` | `typescript` | Nextjs: Replace archived image-size with probe-image-size |
| https://github.com/storybookjs/storybook/pull/35866 | `storybookjs/storybook` | `code_only` | `typescript` | Vue: Rebuild template snippet transform on @vue/compiler-dom loc surgery |
| https://github.com/storybookjs/storybook/pull/35868 | `storybookjs/storybook` | `code_and_docs` | `typescript` | Angular: Harden story-shape reading against unreadable configs |
| https://github.com/storybookjs/storybook/pull/35851 | `storybookjs/storybook` | `code_only` | `typescript` | Build: Restore the node_modules cache behaviour from #35828 |
| https://github.com/storybookjs/storybook/pull/35845 | `storybookjs/storybook` | `code_only` | `typescript` | Core: Centralize import-statement generation in csf-tools |
| https://github.com/storybookjs/storybook/pull/35840 | `storybookjs/storybook` | `code_only` | `typescript` | Dependencies: Bump @testing-library/user-event to 14.6.3 |
| https://github.com/storybookjs/storybook/pull/35843 | `storybookjs/storybook` | `code_only` | `typescript` | Angular: resolve story-docs snippets through the core/docgen service instead of a second analyzer |
| https://github.com/storybookjs/storybook/pull/35683 | `storybookjs/storybook` | `code_and_docs` | `typescript` | Addon-docs: Move CSF Enrichment Into Addon Docs |
| https://github.com/storybookjs/storybook/pull/35820 | `storybookjs/storybook` | `code_only` | `typescript` | Core: Share the program-backed half of a component-meta project |
| https://github.com/storybookjs/storybook/pull/35806 | `storybookjs/storybook` | `code_only` | `typescript` | Core: Move the component-meta invalidation state machine into core |
| https://github.com/storybookjs/storybook/pull/35828 | `storybookjs/storybook` | `code_only` | `typescript` | Build: Give node_modules a cache key that cannot fall back |
| https://github.com/storybookjs/storybook/pull/35827 | `storybookjs/storybook` | `code_only` | `typescript` | Build: Stop nissuer from treating every repro URL as blocklisted |
| https://github.com/storybookjs/storybook/pull/35803 | `storybookjs/storybook` | `code_only` | `typescript` | Core: Share the CSF story-shape helpers snippet generators need |
| https://github.com/storybookjs/storybook/pull/35776 | `storybookjs/storybook` | `code_and_docs` | `typescript` | Angular-Vite: Run Compodoc on demand |
| https://github.com/storybookjs/storybook/pull/35800 | `storybookjs/storybook` | `code_only_tests_or_fixtures` | `typescript` | Build: Normalize CRLF in story-shape print assertions |
| https://github.com/storybookjs/storybook/pull/35766 | `storybookjs/storybook` | `code_only` | `typescript` | Core: Extract React CSF tools into Core |
| https://github.com/storybookjs/storybook/pull/35793 | `storybookjs/storybook` | `code_only` | `typescript` | Build: Run yarn dedupe after sandbox install |
| https://github.com/storybookjs/storybook/pull/35794 | `storybookjs/storybook` | `code_only` | `typescript` | Manifests: Add a warning field to story entries |
| https://github.com/storybookjs/storybook/pull/35777 | `storybookjs/storybook` | `code_and_docs` | `typescript` | Angular: Stop treating input/output alias collisions as two-way bindings |
| https://github.com/storybookjs/storybook/pull/35795 | `storybookjs/storybook` | `code_only_tests_or_fixtures` | `typescript` | Build: Give the addon-mcp component-stories test room to import |
| https://github.com/storybookjs/storybook/pull/35468 | `storybookjs/storybook` | `code_only` | `typescript` | React: Share a TypeScript DocumentRegistry across component-meta projects |
| https://github.com/storybookjs/storybook/pull/35790 | `storybookjs/storybook` | `code_only` | `typescript` | Build: Keep the published lockfile and age gate in sandbox CI |
| https://github.com/storybookjs/storybook/pull/35787 | `storybookjs/storybook` | `code_only_tests_or_fixtures` | `typescript` | Build: Fix Windows failure in the Angular docgen worker test |
| https://github.com/storybookjs/storybook/pull/35710 | `storybookjs/storybook` | `code_and_docs` | `typescript` | Bench: Gate the docgen perf suite on budgets in CI |
| https://github.com/storybookjs/storybook/pull/35758 | `storybookjs/storybook` | `code_only` | `typescript` | Angular: Derive required inputs from Compodoc's own flag |
| https://github.com/storybookjs/storybook/pull/35600 | `storybookjs/storybook` | `code_only` | `typescript` | Angular: Serve ancestor node_modules for addon-vitest in browser mode |
| https://github.com/storybookjs/storybook/pull/35783 | `storybookjs/storybook` | `code_only` | `typescript` | Build: Exempt @tailwindcss/turbopack from the sandbox age gate |
| https://github.com/storybookjs/storybook/pull/35782 | `storybookjs/storybook` | `code_only` | `typescript` | Build: Keep Yarn's output plain so age-gate rejections stay parseable |
| https://github.com/storybookjs/storybook/pull/35775 | `storybookjs/storybook` | `code_only` | `typescript` | Build: Narrow only quarantined ranges when generating sandboxes |
| https://github.com/storybookjs/storybook/pull/35773 | `storybookjs/storybook` | `code_only` | `typescript` | Release: Report prereleases to DX also |
| https://github.com/storybookjs/storybook/pull/35771 | `storybookjs/storybook` | `code_only` | `typescript` | Build: Also exempt `@vue/language-core` from Vue sandbox age gate |
| https://github.com/storybookjs/storybook/pull/35770 | `storybookjs/storybook` | `code_only` | `typescript` | Build: Preapprove `vue-component-meta` for sandbox age gate |
| https://github.com/storybookjs/storybook/pull/35769 | `storybookjs/storybook` | `code_only` | `typescript` | Refactor: Update getVersionedPackages method to handle non-Storybook packages correctly |
| https://github.com/storybookjs/storybook/pull/35767 | `storybookjs/storybook` | `code_only` | `typescript` | Build: Update Yarn configuration and set dependencies to latest version |
| https://github.com/storybookjs/storybook/pull/35764 | `storybookjs/storybook` | `code_only` | `typescript` | Build: Update to yarn v4.18.0 |
| https://github.com/storybookjs/storybook/pull/35763 | `storybookjs/storybook` | `code_only` | `typescript` | Build: Add 7d minimum release age gate to the repository's Yarn config |
| https://github.com/storybookjs/storybook/pull/35654 | `storybookjs/storybook` | `code_only` | `typescript` | Release: Add a step to register stable release in DX |
| https://github.com/storybookjs/storybook/pull/35510 | `storybookjs/storybook` | `code_only` | `typescript` | CI: Run the tail-defining Playwright dev jobs on xlarge with more workers |
| https://github.com/storybookjs/storybook/pull/35492 | `storybookjs/storybook` | `code_and_docs` | `typescript` | CI: Adopt TypeScript 7 native compiler for package typechecking |
| https://github.com/storybookjs/storybook/pull/35490 | `storybookjs/storybook` | `code_only` | `typescript` | Build: Remove baseUrl from tsconfigs for TypeScript 7 compatibility |
| https://github.com/storybookjs/storybook/pull/35486 | `storybookjs/storybook` | `code_only` | `typescript` | CLI: Run addon postinstall automigrations with the local storybook binary |
| https://github.com/storybookjs/storybook/pull/35480 | `storybookjs/storybook` | `code_only` | `typescript` | CI: Skip the redundant Compodoc run when documentation.json ships with the sandbox |
| https://github.com/storybookjs/storybook/pull/35479 | `storybookjs/storybook` | `code_only` | `typescript` | CI: Overlap the node_modules workspace pack with compile in build--linux |
| https://github.com/storybookjs/storybook/pull/35352 | `storybookjs/storybook` | `code_only` | `typescript` | CI: Build sandbox static output inside the create job |
| https://github.com/storybookjs/storybook/pull/35348 | `storybookjs/storybook` | `code_only` | `typescript` | CI: Pack sandboxes into zstd workspace tarballs |
| https://github.com/storybookjs/storybook/pull/35347 | `storybookjs/storybook` | `code_only` | `typescript` | CI: Parallel Playwright workers for sandbox E2E |
| https://github.com/storybookjs/storybook/pull/35343 | `storybookjs/storybook` | `code_only` | `typescript` | Build: Reduce build--linux orchestration and workspace overhead |
| https://github.com/storybookjs/storybook/pull/35341 | `storybookjs/storybook` | `code_only` | `typescript` | Build: Replace rollup-plugin-dts with rolldown-plugin-dts for d.ts generation |
| https://github.com/storybookjs/storybook/pull/34852 | `storybookjs/storybook` | `code_only` | `typescript` | Build: Migrate sandbox generation to Yarn 4 with 7d npmMinimalAgeGate |
| https://github.com/storybookjs/storybook/pull/35749 | `storybookjs/storybook` | `code_and_docs` | `typescript` | Angular: Extract Compodoc parsing into its own package |
| https://github.com/storybookjs/storybook/pull/35488 | `storybookjs/storybook` | `code_only` | `typescript` | Build: Compress the pipeline workspace tarball with zstd via node:zlib |
| https://github.com/storybookjs/storybook/pull/34851 | `storybookjs/storybook` | `code_only` | `typescript` | Build: Sanitize publish-time .yarnrc.yml in after-storybook sandboxes |
| https://github.com/storybookjs/storybook/pull/35720 | `storybookjs/storybook` | `code_only` | `typescript` | CLI: Categorize Execa failures for init telemetry |
| https://github.com/storybookjs/storybook/pull/35742 | `storybookjs/storybook` | `code_only` | `typescript` | CLI: Allow esbuild builds for Storybook-owned pnpm dlx |
| https://github.com/storybookjs/storybook/pull/35666 | `storybookjs/storybook` | `code_only` | `typescript` | Vue: Run docgen through component-meta project manager |
| https://github.com/storybookjs/storybook/pull/35670 | `storybookjs/storybook` | `code_only` | `typescript` | Vue: Expose docgen provider, inject in manifest and gate behind vue-component-meta only |
| https://github.com/storybookjs/storybook/pull/35687 | `storybookjs/storybook` | `code_only` | `typescript` | Core: Add lazy-docgen-middleware |
| https://github.com/storybookjs/storybook/pull/35713 | `storybookjs/storybook` | `code_and_docs` | `typescript` | Agents: Add Cursor Cloud environment setup notes |
| https://github.com/storybookjs/storybook/pull/35321 | `storybookjs/storybook` | `code_and_docs` | `typescript` | A11y: Handle lang attribute throughout preview |
| https://github.com/storybookjs/storybook/pull/35722 | `storybookjs/storybook` | `code_only` | `typescript` | CI: Remove mcp and addon-mcp from verdaccio proxy |
| https://github.com/storybookjs/storybook/pull/35655 | `storybookjs/storybook` | `code_and_docs` | `typescript` | ESLint Plugin: Add plugin meta and document oxlint usage |
| https://github.com/storybookjs/storybook/pull/35614 | `storybookjs/storybook` | `code_only` | `typescript` | Dependencies: Pin `@testing-library/jest-dom` to `6.9.1` |
| https://github.com/storybookjs/storybook/pull/35692 | `storybookjs/storybook` | `code_and_docs` | `typescript` | CI: Require Core or DX approval before merging PRs |
| https://github.com/storybookjs/storybook/pull/35598 | `storybookjs/storybook` | `code_only` | `typescript` | Vue: Skip docgen for module ids carrying a query |
| https://github.com/storybookjs/storybook/pull/35711 | `storybookjs/storybook` | `code_and_docs` | `typescript` | Release: Patch 10.5.6 |
| https://github.com/storybookjs/storybook/pull/35657 | `storybookjs/storybook` | `code_only` | `typescript` | Core: Extract ComponentMetaManager to Core |
| https://github.com/storybookjs/storybook/pull/24205 | `storybookjs/storybook` | `code_only` | `typescript` | UI: Improve contrast ratio between focus / hover |
| https://github.com/storybookjs/storybook/pull/35585 | `storybookjs/storybook` | `code_only` | `typescript` | Core: Add additionnal field for component API in manifest |
| https://github.com/storybookjs/storybook/pull/35263 | `storybookjs/storybook` | `code_only` | `typescript` | Manager: Toggle the mobile navigation drawer with the sidebar keyboard shortcut |
| https://github.com/storybookjs/storybook/pull/35434 | `storybookjs/storybook` | `code_only` | `typescript` | Review: Use correct role for footer |
| https://github.com/storybookjs/storybook/pull/35681 | `storybookjs/storybook` | `code_only_tests_or_fixtures` | `typescript` | Builder-Webpack5: Use strict mtime equality for mock cache reuse |
| https://github.com/storybookjs/storybook/pull/35498 | `storybookjs/storybook` | `code_only` | `typescript` | TanStack: Select the story leaf by mount path and params |
| https://github.com/storybookjs/storybook/pull/35609 | `storybookjs/storybook` | `code_only` | `typescript` | Build: Fix repository.directory path in @storybook/nextjs-vite package.json |
| https://github.com/storybookjs/storybook/pull/35500 | `storybookjs/storybook` | `code_only` | `typescript` | TanStack: Carry lazy route bindings onto cloned routes |
| https://github.com/storybookjs/storybook/pull/35470 | `storybookjs/storybook` | `code_only` | `typescript` | Manifest Debugger: Stable deep-link anchors for component cards |
| https://github.com/storybookjs/storybook/pull/35595 | `storybookjs/storybook` | `code_only` | `typescript` | Icons: Add missing @storybook/icons to the toolbar icon map |
| https://github.com/storybookjs/storybook/pull/35686 | `storybookjs/storybook` | `code_and_docs` | `typescript` | Bench: Declare the React renderer dependency the harnesses rely on |
| https://github.com/storybookjs/storybook/pull/35675 | `storybookjs/storybook` | `code_and_docs` | `typescript` | Bench: Compare an engine against another release of itself |
| https://github.com/storybookjs/storybook/pull/35651 | `storybookjs/storybook` | `code_only` | `typescript` | Bench: Add the React and Vue docgen perf engines |
| https://github.com/storybookjs/storybook/pull/35634 | `storybookjs/storybook` | `code_and_docs` | `typescript` | Bench: Make the docgen perf suite runnable |
| https://github.com/storybookjs/storybook/pull/35636 | `storybookjs/storybook` | `code_only` | `typescript` | Bench: Add the docgen perf engine framework and the compodoc engine |
| https://github.com/storybookjs/storybook/pull/35631 | `storybookjs/storybook` | `code_only` | `typescript` | Bench: Add the shared docgen bench plumbing and move the memory harness onto it |
| https://github.com/storybookjs/storybook/pull/35560 | `storybookjs/storybook` | `code_only` | `typescript` | ReactNative: Telemetry framework detection fix |
| https://github.com/storybookjs/storybook/pull/31980 | `storybookjs/storybook` | `code_only` | `typescript` | Svelte: Fix union types generating invalid labels in argTypes |
| https://github.com/storybookjs/storybook/pull/35684 | `storybookjs/storybook` | `code_and_docs` | `typescript` | Vue3: Support TypeScript enum props in vue-component-meta docgen |
| https://github.com/storybookjs/storybook/pull/35599 | `storybookjs/storybook` | `code_only` | `typescript` | Core: Include null union members as enum options in TS argTypes conversion |
| https://github.com/storybookjs/storybook/pull/35596 | `storybookjs/storybook` | `code_only` | `typescript` | Build: Fix repository.directory path in create-storybook package.json |
| https://github.com/storybookjs/storybook/pull/35572 | `storybookjs/storybook` | `code_only` | `typescript` | Addon Vitest: Pin storybook/test in optimizeDeps so its CJS-only deps are prebundled |
| https://github.com/storybookjs/storybook/pull/35567 | `storybookjs/storybook` | `code_only` | `typescript` | Core: Use npm 12-compatible registry flags |
| https://github.com/storybookjs/storybook/pull/35593 | `storybookjs/storybook` | `code_only` | `typescript` | Vue: Resolve docgen per export so a type-only export does not drop a file's prop tables |
| https://github.com/storybookjs/storybook/pull/35565 | `storybookjs/storybook` | `code_only` | `typescript` | Vue3 Vite: Enable Schema Extraction for Vue Component Meta |
| https://github.com/storybookjs/storybook/pull/35589 | `storybookjs/storybook` | `code_only` | `typescript` | NextJS: Normalize trailing slash in the next/link mock |
| https://github.com/storybookjs/storybook/pull/35499 | `storybookjs/storybook` | `code_only` | `typescript` | TanStack: Preserve explicit route ids on pathful clones |
| https://github.com/storybookjs/storybook/pull/35501 | `storybookjs/storybook` | `code_only` | `typescript` | TanStack: Resolve mock redirects through Vite's resolver |
| https://github.com/storybookjs/storybook/pull/35669 | `storybookjs/storybook` | `code_only` | `typescript` | Ci: Force clean cache for circleCI |
| https://github.com/fastapi/fastapi/pull/16249 | `fastapi/fastapi` | `code_only` | `python` | ⬆️ Bump `setup-uv` action to `10.0.1` |
| https://github.com/fastapi/fastapi/pull/16224 | `fastapi/fastapi` | `code_only` | `python` | 👷 Update translation PR branches with PR Push |
| https://github.com/fastapi/fastapi/pull/16216 | `fastapi/fastapi` | `code_only` | `python` | ⏪️ Restore `commit_in_place` input in `translate.yml` |
| https://github.com/fastapi/fastapi/pull/16185 | `fastapi/fastapi` | `code_only` | `python` | 👷 Migrate automatic labels to Latest Changes |
| https://github.com/fastapi/fastapi/pull/16178 | `fastapi/fastapi` | `code_only` | `python` | 👷 Fix branch name in `zizmor.yml` workflow (`main` -> `master`) |
| https://github.com/fastapi/fastapi/pull/16180 | `fastapi/fastapi` | `code_only` | `python` | 👷 Remove legacy label check |
| https://github.com/fastapi/fastapi/pull/16174 | `fastapi/fastapi` | `code_only` | `python` | 🐛 Fix Sponsors Git authentication |
| https://github.com/fastapi/fastapi/pull/16172 | `fastapi/fastapi` | `code_only` | `python` | 🔐 Use PR Submit for automated updates |
| https://github.com/fastapi/fastapi/pull/16168 | `fastapi/fastapi` | `code_only` | `python` | 🔐 Use PR Submit for translations |
| https://github.com/fastapi/fastapi/pull/16170 | `fastapi/fastapi` | `code_only` | `python` | ⬆️ Raise pytest-xdist minimum |
| https://github.com/fastapi/fastapi/pull/16167 | `fastapi/fastapi` | `code_only` | `python` | 🔐 Use PR Submit for pull requests |
| https://github.com/fastapi/fastapi/pull/16166 | `fastapi/fastapi` | `code_only` | `python` | 👷 Use GitHub CLI for Git authentication |
| https://github.com/fastapi/fastapi/pull/16164 | `fastapi/fastapi` | `code_only` | `python` | 👷 Use PR Push commit identity |
| https://github.com/fastapi/fastapi/pull/16161 | `fastapi/fastapi` | `code_only` | `python` | 🔒 Replace pre-commit PAT with PR Push |
| https://github.com/fastapi/fastapi/pull/16156 | `fastapi/fastapi` | `code_only` | `python` | 👷 Disable saving Zensical's `.cache` in `build-docs.yml` |
| https://github.com/fastapi/fastapi/pull/16148 | `fastapi/fastapi` | `code_only` | `python` | 🔥 Remove the old Latest Changes workflow |
| https://github.com/fastapi/fastapi/pull/16076 | `fastapi/fastapi` | `code_only` | `python` | ⚡️ Avoid flattening dependencies for OpenAPI |
| https://github.com/fastapi/fastapi/pull/16121 | `fastapi/fastapi` | `code_only` | `python` | ⬆ Bump the python-packages group with 12 updates |
| https://github.com/fastapi/fastapi/pull/15077 | `fastapi/fastapi` | `code_only` | `python` | 🐛 Fix stream item type lost when using `include_router()` |
| https://github.com/fastapi/fastapi/pull/16120 | `fastapi/fastapi` | `code_only` | `python` | ⬆ Bump the github-actions group with 6 updates |
| https://github.com/fastapi/fastapi/pull/16106 | `fastapi/fastapi` | `code_and_docs` | `python` | 🔖 Release version 0.141.1 |
| https://github.com/fastapi/fastapi/pull/16105 | `fastapi/fastapi` | `code_and_docs` | `python` | 🐛 Fix support for background tasks and headers from dependencies in `app.frontend()` |
| https://github.com/fastapi/fastapi/pull/16103 | `fastapi/fastapi` | `code_and_docs` | `python` | 🔖 Release version 0.141.0 |
| https://github.com/fastapi/fastapi/pull/16102 | `fastapi/fastapi` | `code_and_docs` | `python` | ✨ Add `app.frontend(check_dir="auto")`, to make local development more convenient with `fastapi dev` |
| https://github.com/fastapi/fastapi/pull/15937 | `fastapi/fastapi` | `code_only` | `python` | 🐛 Fix `status_code` being ignored for SSE and JSONL streaming endpoints |
| https://github.com/fastapi/fastapi/pull/16096 | `fastapi/fastapi` | `code_and_docs` | `python` | 🔖 Release version 0.140.13 |
| https://github.com/fastapi/fastapi/pull/15613 | `fastapi/fastapi` | `code_only` | `python` | 📝 Fix `format_sse_event` docstring rendering of `\n\n` terminator |
| https://github.com/fastapi/fastapi/pull/16095 | `fastapi/fastapi` | `code_and_docs` | `python` | 🔖 Release version 0.140.12 |
| https://github.com/fastapi/fastapi/pull/15515 | `fastapi/fastapi` | `code_only` | `python` | 🐛 Fix line splitting in `format_sse_event` to comply with SSE spec |
| https://github.com/fastapi/fastapi/pull/16094 | `fastapi/fastapi` | `code_and_docs` | `python` | 🔖 Release version 0.140.11 |
| https://github.com/fastapi/fastapi/pull/15093 | `fastapi/fastapi` | `code_only` | `python` | 🐛 Fix `response_model_*` params ignored for non-generator endpoints with `Iterable[..]` return type |
| https://github.com/fastapi/fastapi/pull/16093 | `fastapi/fastapi` | `code_and_docs` | `python` | 🔖 Release version 0.140.10 |
| https://github.com/fastapi/fastapi/pull/14874 | `fastapi/fastapi` | `code_only` | `python` | 🐛 Fix handling sequences with nested Annotated types |
| https://github.com/fastapi/fastapi/pull/16092 | `fastapi/fastapi` | `code_only_tests_or_fixtures` | `python` | 🐛 Accept any base test failure as regression |
| https://github.com/fastapi/fastapi/pull/16091 | `fastapi/fastapi` | `code_only_tests_or_fixtures` | `python` | 🐛 Preserve pytest exit code in regression check |
| https://github.com/fastapi/fastapi/pull/16090 | `fastapi/fastapi` | `code_only_tests_or_fixtures` | `python` | ✅ Test PR regressions against base code |
| https://github.com/fastapi/fastapi/pull/16089 | `fastapi/fastapi` | `code_and_docs` | `python` | 🔖 Release version 0.140.9 |
| https://github.com/fastapi/fastapi/pull/16043 | `fastapi/fastapi` | `code_only` | `python` | 🐛 Fix `exclude_defaults` not propagated to dict keys and values in `jsonable_encoder` |
| https://github.com/fastapi/fastapi/pull/16088 | `fastapi/fastapi` | `code_and_docs` | `python` | 🔖 Release version 0.140.8 |
| https://github.com/fastapi/fastapi/pull/16078 | `fastapi/fastapi` | `code_and_docs` | `python` | 🔖 Release version 0.140.7 |
| https://github.com/fastapi/fastapi/pull/16077 | `fastapi/fastapi` | `code_only` | `python` | ⬆️ Upgrade latest-changes to 0.7.1 |
| https://github.com/fastapi/fastapi/pull/16075 | `fastapi/fastapi` | `code_only_tests_or_fixtures` | `python` | 👷 Add OpenAPI dependency benchmarks |
| https://github.com/fastapi/fastapi/pull/16074 | `fastapi/fastapi` | `code_and_docs` | `python` | 🔖 Release version 0.140.6 |
| https://github.com/fastapi/fastapi/pull/16073 | `fastapi/fastapi` | `code_only` | `python` | ⚡️ Avoid flattening dependencies for request parameters, mainly for OpenAPI |
| https://github.com/fastapi/fastapi/pull/16072 | `fastapi/fastapi` | `code_and_docs` | `python` | 🔖 Release version 0.140.5 |
| https://github.com/fastapi/fastapi/pull/16071 | `fastapi/fastapi` | `code_only` | `python` | ⚡️ Avoid flattening dependencies for body fields |
| https://github.com/fastapi/fastapi/pull/16070 | `fastapi/fastapi` | `code_and_docs` | `python` | 🔖 Release version 0.140.4 |
| https://github.com/fastapi/fastapi/pull/16069 | `fastapi/fastapi` | `code_only` | `python` | ⚡️ Skip unused dependency repeat bookkeeping |
| https://github.com/fastapi/fastapi/pull/16068 | `fastapi/fastapi` | `code_and_docs` | `python` | 🔖 Release version 0.140.3 |
| https://github.com/fastapi/fastapi/pull/16067 | `fastapi/fastapi` | `code_only` | `python` | ⚡️ Avoid repeated dependency flattening in OpenAPI |
| https://github.com/fastapi/fastapi/pull/16066 | `fastapi/fastapi` | `code_and_docs` | `python` | 🔖 Release version 0.140.2 |
| https://github.com/fastapi/fastapi/pull/16065 | `fastapi/fastapi` | `code_only` | `python` | ⚡️ Stop retaining flat dependency trees |
| https://github.com/fastapi/fastapi/pull/16049 | `fastapi/fastapi` | `code_only` | `python` | ⚡️ Reduce memory usage in dependencies |
| https://github.com/fastapi/fastapi/pull/16064 | `fastapi/fastapi` | `code_only_tests_or_fixtures` | `python` | 👷 Add new memory benchmark |
| https://github.com/fastapi/fastapi/pull/16063 | `fastapi/fastapi` | `code_and_docs` | `python` | 🔖 Release version 0.140.1 |
| https://github.com/fastapi/fastapi/pull/16062 | `fastapi/fastapi` | `code_only` | `python` | ♻️ Update the lru_cache limit for dependencies to account for large apps |
| https://github.com/fastapi/fastapi/pull/16050 | `fastapi/fastapi` | `code_and_docs` | `python` | 🔖 Release version 0.140.0 |
| https://github.com/fastapi/fastapi/pull/16046 | `fastapi/fastapi` | `code_only` | `python` | 👷 Add CI memory benchmark |
| https://github.com/fastapi/fastapi/pull/16016 | `fastapi/fastapi` | `code_only` | `python` | 🔥 Remove now-obsolete scripts to generate data for FastAPI People |
| https://github.com/fastapi/fastapi/pull/16014 | `fastapi/fastapi` | `code_and_docs` | `python` | 🔖 Release version 0.139.2 |
| https://github.com/fastapi/fastapi/pull/16013 | `fastapi/fastapi` | `code_only` | `python` | 🐛 Refactor router route building to make it thread-safe, mainly relevant for tests running in parallel threads (uncommon) |
| https://github.com/fastapi/fastapi/pull/16012 | `fastapi/fastapi` | `code_and_docs` | `python` | 🔖 Release version 0.139.1 |
| https://github.com/fastapi/fastapi/pull/16011 | `fastapi/fastapi` | `code_and_docs` | `python` | 🐛 Fix frontend fallback support for doted paths like `/users/john.doe` |
| https://github.com/fastapi/fastapi/pull/15995 | `fastapi/fastapi` | `code_and_docs` | `python` | 📝 Fix topic repository list not being displayed and `skip_users` not being applied |
| https://github.com/fastapi/fastapi/pull/15983 | `fastapi/fastapi` | `code_only` | `python` | ⬆ Bump the github-actions group across 1 directory with 4 updates |
| https://github.com/fastapi/fastapi/pull/15985 | `fastapi/fastapi` | `code_only` | `python` | ⬆ Bump pre-commit hooks |
| https://github.com/fastapi/fastapi/pull/15984 | `fastapi/fastapi` | `code_only` | `python` | 👷 Use `FASTAPI_LATEST_CHANGES` token in `bump-pre-commit-hooks` workflow |
| https://github.com/fastapi/fastapi/pull/15873 | `fastapi/fastapi` | `code_only` | `python` | 👷 Add GH workflow to bump pre-commit hook versions |
| https://github.com/fastapi/fastapi/pull/15874 | `fastapi/fastapi` | `code_only` | `python` | 🔧 Set Dependabot schedule interval to "monthly" |
| https://github.com/fastapi/fastapi/pull/15950 | `fastapi/fastapi` | `code_only_tests_or_fixtures` | `python` | ⬆ Bump CodSpeedHQ/action from 4.17.6 to 4.18.1 in the github-actions group |
| https://github.com/fastapi/fastapi/pull/15933 | `fastapi/fastapi` | `code_only` | `python` | 👷 Fix notify translations checkout target |
| https://github.com/fastapi/fastapi/pull/15932 | `fastapi/fastapi` | `code_only` | `python` | 👷 Fix latest-changes checkout target |
| https://github.com/fastapi/fastapi/pull/15928 | `fastapi/fastapi` | `code_only` | `python` | ⬆️ Update issue-manager to 0.8.1 |
| https://github.com/fastapi/fastapi/pull/15926 | `fastapi/fastapi` | `code_only` | `python` | ⬆️ Update latest-changes to 0.6.1 |
| https://github.com/fastapi/fastapi/pull/15910 | `fastapi/fastapi` | `code_and_docs` | `python` | 🔖 Release version 0.139.0 |
| https://github.com/fastapi/fastapi/pull/15908 | `fastapi/fastapi` | `code_and_docs` | `python` | ✨ Support dependencies in `app.frontend()`, e.g. for automatic cookie authentication for the frontend |
| https://github.com/fastapi/fastapi/pull/15876 | `fastapi/fastapi` | `code_only` | `python` | 👷 Remove not needed `allow-unsafe-pr-checkout: true` |
| https://github.com/fastapi/fastapi/pull/15872 | `fastapi/fastapi` | `code_only` | `python` | ⬆ Bump the github-actions group with 5 updates |
| https://github.com/fastapi/fastapi/pull/15826 | `fastapi/fastapi` | `code_only_tests_or_fixtures` | `python` | ⬆ Bump CodSpeedHQ/action from 4.17.0 to 4.17.5 in the github-actions group |
| https://github.com/fastapi/fastapi/pull/15864 | `fastapi/fastapi` | `code_and_docs` | `python` | 🔖 Release version 0.138.2 |
| https://github.com/fastapi/fastapi/pull/15863 | `fastapi/fastapi` | `code_and_docs` | `python` | ♻️ Make `app.frontend()` return 404 for methods other than `GET` or `HEAD` with no static file matches |
| https://github.com/fastapi/fastapi/pull/14873 | `fastapi/fastapi` | `code_only` | `python` | 🐛 Fix `on_startup` and `on_shutdown` parameters of `APIRouter` |
| https://github.com/fastapi/fastapi/pull/15852 | `fastapi/fastapi` | `code_and_docs` | `python` | ♻️ Refactor how sponsors data is handled for banners |
| https://github.com/fastapi/fastapi/pull/15842 | `fastapi/fastapi` | `code_and_docs` | `python` | 🔖 Release version 0.138.1 |
| https://github.com/fastapi/fastapi/pull/15836 | `fastapi/fastapi` | `code_only` | `python` | 👷 Simplify pull request workflow triggers |
| https://github.com/fastapi/fastapi/pull/15833 | `fastapi/fastapi` | `code_only` | `python` | 👷 Update issue-manager to 0.7.1 |
| https://github.com/fastapi/fastapi/pull/15831 | `fastapi/fastapi` | `code_only` | `python` | ⬆️ Update issue-manager to 0.7.0 |
| https://github.com/fastapi/fastapi/pull/15820 | `fastapi/fastapi` | `code_only` | `python` | 🔒️ Update zizmor workflow security checks |
| https://github.com/fastapi/fastapi/pull/15808 | `fastapi/fastapi` | `code_and_docs` | `python` | 🔖 Release version 0.138.0 |
| https://github.com/fastapi/fastapi/pull/15804 | `fastapi/fastapi` | `code_only` | `python` | 🐛 Fix failing test, update format for raised errors |
| https://github.com/fastapi/fastapi/pull/15803 | `fastapi/fastapi` | `code_only_tests_or_fixtures` | `python` | 👷 Fix test-alls-green |
| https://github.com/fastapi/fastapi/pull/15800 | `fastapi/fastapi` | `code_and_docs` | `python` | ✨ Add support for `app.frontend("/", directory="dist")` and `router.frontend("/", directory="dist")` |
| https://github.com/fastapi/fastapi/pull/15796 | `fastapi/fastapi` | `code_only` | `python` | 🔧 Enable checking `release-notes.md` for typos |
| https://github.com/fastapi/fastapi/pull/15554 | `fastapi/fastapi` | `code_and_docs` | `python` | 🌐 Enable Hindi docs translations |
| https://github.com/fastapi/fastapi/pull/15785 | `fastapi/fastapi` | `code_only` | `python` | ✨ Add `iter_route_contexts()` for advanced use cases that used to use `router.routes` (e.g. Jupyverse) |
| https://github.com/fastapi/fastapi/pull/15792 | `fastapi/fastapi` | `code_only` | `python` | 🔨 Use `gpt-5.5` model in `translate.py`, specify `-chat` to avoid warnings |
| https://github.com/fastapi/fastapi/pull/15790 | `fastapi/fastapi` | `code_and_docs` | `python` | 🔖 Release version 0.137.2 |
| https://github.com/fastapi/fastapi/pull/15786 | `fastapi/fastapi` | `code_and_docs` | `python` | 🔨 Update sponsors script to simplify previews |
| https://github.com/fastapi/fastapi/pull/15776 | `fastapi/fastapi` | `code_only` | `python` | ⬆ Bump astral-sh/setup-uv from 8.1.0 to 8.2.0 in the github-actions group |
| https://github.com/fastapi/fastapi/pull/15775 | `fastapi/fastapi` | `code_only` | `python` | ⬆ Bump https://github.com/crate-ci/typos from v1.47.1 to v1.47.2 in the pre-commit group |
| https://github.com/fastapi/fastapi/pull/15280 | `fastapi/fastapi` | `code_and_docs` | `python` | ✨ Add support for `@app.vibe()` |
| https://github.com/fastapi/fastapi/pull/15769 | `fastapi/fastapi` | `code_only` | `python` | 🔧 Add ty configs to check docs sources |
| https://github.com/fastapi/fastapi/pull/15766 | `fastapi/fastapi` | `code_and_docs` | `python` | 🔖 Release version 0.137.1 |
| https://github.com/fastapi/fastapi/pull/15765 | `fastapi/fastapi` | `code_only` | `python` | 🚨 Fix typing checks for APIRoute |
| https://github.com/fastapi/fastapi/pull/15763 | `fastapi/fastapi` | `code_only` | `python` | 🐛 Fix bug, allow empty path in path operation in prefixless router |
| https://github.com/fastapi/fastapi/pull/15748 | `fastapi/fastapi` | `code_and_docs` | `python` | 🔖 Release version 0.137.0 |
| https://github.com/fastapi/fastapi/pull/15745 | `fastapi/fastapi` | `code_and_docs` | `python` | ♻️ Refactor internals to preserve `APIRouter` and `APIRoute` instances |
| https://github.com/fastapi/fastapi/pull/15720 | `fastapi/fastapi` | `code_only` | `python` | ⬆ Bump the github-actions group with 3 updates |
| https://github.com/fastapi/fastapi/pull/15719 | `fastapi/fastapi` | `code_only` | `python` | ⬆ Bump https://github.com/crate-ci/typos from v1.46.0 to v1.47.1 in the pre-commit group |
| https://github.com/fastapi/fastapi/pull/15682 | `fastapi/fastapi` | `code_only` | `python` | ⬆ Bump the github-actions group with 2 updates |
| https://github.com/fastapi/fastapi/pull/15661 | `fastapi/fastapi` | `code_only` | `python` | 👷 Automate release preparation |
| https://github.com/fastapi/fastapi/pull/1 | `fastapi/fastapi` | `code_only_tests_or_fixtures` | `python` | Add tests for path endpoints |
| https://github.com/fastapi/fastapi/pull/15513 | `fastapi/fastapi` | `code_only_tests_or_fixtures` | `python` | ⬆ Bump CodSpeedHQ/action from 4.14.0 to 4.15.1 |
| https://github.com/fastapi/fastapi/pull/15607 | `fastapi/fastapi` | `code_only` | `python` | 🔒️ Improve GitHub actions security |
| https://github.com/fastapi/fastapi/pull/15610 | `fastapi/fastapi` | `code_only` | `python` | ⚰️ Remove ruff and coverage ignores for non-existing files |
| https://github.com/fastapi/fastapi/pull/15616 | `fastapi/fastapi` | `code_only_tests_or_fixtures` | `python` | ✅ Use custom `changing_dir` instead of `CLIRunner.isolated_filesystem` to set working dir |
| https://github.com/fastapi/fastapi/pull/15603 | `fastapi/fastapi` | `code_only` | `python` | ✅ Add `httpx2` test dependency to avoid deprecation warning |
| https://github.com/fastapi/fastapi/pull/15588 | `fastapi/fastapi` | `code_only` | `python` | ♻️ Validate Server Sent Event fields to avoid applications from sending broken data |
| https://github.com/fastapi/fastapi/pull/15587 | `fastapi/fastapi` | `code_only_tests_or_fixtures` | `python` | ✅ Update tests, don't double dispose the engine |
| https://github.com/fastapi/fastapi/pull/15560 | `fastapi/fastapi` | `code_only` | `python` | 👷 Configure Dependabot to group updates and update weekly |
| https://github.com/fastapi/fastapi/pull/15589 | `fastapi/fastapi` | `code_only` | `python` | ♻️ Do not accept underscore headers when using `convert_underscores=True` (the default) |
| https://github.com/fastapi/fastapi/pull/13583 | `fastapi/fastapi` | `code_only_tests_or_fixtures` | `python` | ⚡️ Speed up test suite via caching and fixture scopes to make it ~24% faster |
| https://github.com/fastapi/fastapi/pull/15585 | `fastapi/fastapi` | `code_and_docs` | `python` | 🔥 Remove config files now in central GitHub repo |
| https://github.com/fastapi/fastapi/pull/15580 | `fastapi/fastapi` | `code_and_docs` | `python` | 📝 Add docs references to central contributing docs |
| https://github.com/fastapi/fastapi/pull/15571 | `fastapi/fastapi` | `code_only` | `python` | ⬆ Bump cloudflare/wrangler-action from 3.15.0 to 4.0.0 |
| https://github.com/fastapi/fastapi/pull/15563 | `fastapi/fastapi` | `code_and_docs` | `python` | 🔧 Migrate docs from MkDocs to Zensical |
| https://github.com/fastapi/fastapi/pull/15548 | `fastapi/fastapi` | `code_and_docs` | `python` | 🔒️ Only allow team members to modify dependencies |
| https://github.com/fastapi/fastapi/pull/15490 | `fastapi/fastapi` | `code_only` | `python` | ⬆ Bump actions/add-to-project from 1.0.2 to 2.0.0 |
| https://github.com/fastapi/fastapi/pull/15507 | `fastapi/fastapi` | `code_only` | `python` | ⬆ Bump actions/labeler from 6.0.1 to 6.1.0 |
| https://github.com/fastapi/fastapi/pull/15533 | `fastapi/fastapi` | `code_only` | `python` | 🔧 Remove Ruff ignored rule for tabs |
| https://github.com/fastapi/fastapi/pull/100 | `fastapi/fastapi` | `code_only` | `python` | Add websocket to APIRouter |
| https://github.com/fastapi/fastapi/pull/15443 | `fastapi/fastapi` | `code_only` | `python` | ⬆ Bump ty from 0.0.21 to 0.0.34 |
| https://github.com/fastapi/fastapi/pull/15101 | `fastapi/fastapi` | `code_only` | `python` | ⬆️ Update Pydantic v2 code to address deprecations |
| https://github.com/fastapi/fastapi/pull/15482 | `fastapi/fastapi` | `code_only` | `python` | 👷 Add pre-commit to check typos |
| https://github.com/fastapi/fastapi/pull/15468 | `fastapi/fastapi` | `code_only` | `python` | 👷 Fix missing credentials issue in `translate` workflow |
| https://github.com/fastapi/fastapi/pull/15462 | `fastapi/fastapi` | `code_and_docs` | `python` | 💄 Improve layout and styling |
| https://github.com/fastapi/fastapi/pull/15436 | `fastapi/fastapi` | `code_only_tests_or_fixtures` | `python` | ⬆ Bump CodSpeedHQ/action from 4.12.1 to 4.14.0 |
| https://github.com/fastapi/fastapi/pull/15415 | `fastapi/fastapi` | `code_only` | `python` | ⬆ Bump astral-sh/setup-uv from 7.6.0 to 8.1.0 |
| https://github.com/fastapi/fastapi/pull/15174 | `fastapi/fastapi` | `code_and_docs` | `python` | 🔨 Tweak translation script |
| https://github.com/fastapi/fastapi/pull/15405 | `fastapi/fastapi` | `code_only` | `python` | ⬆ Bump cloudflare/wrangler-action from 3.14.1 to 3.15.0 |
| https://github.com/fastapi/fastapi/pull/15374 | `fastapi/fastapi` | `code_only` | `python` | ⬆ Bump actions/upload-artifact from 7.0.0 to 7.0.1 |
| https://github.com/fastapi/fastapi/pull/15385 | `fastapi/fastapi` | `code_only` | `python` | ⬆ Bump actions/cache from 5.0.4 to 5.0.5 |
| https://github.com/fastapi/fastapi/pull/15316 | `fastapi/fastapi` | `code_only` | `python` | 🔒️ Add zizmor and fix audit findings |
| https://github.com/fastapi/fastapi/pull/15149 | `fastapi/fastapi` | `code_only` | `python` | ⬆️ Support free-threaded Python 3.14t |
| https://github.com/fastapi/fastapi/pull/15363 | `fastapi/fastapi` | `code_and_docs` | `python` | 🔥 Remove April Fool's `@app.vibe()` 🤪 |
| https://github.com/fastapi/fastapi/pull/15030 | `fastapi/fastapi` | `code_and_docs` | `python` | ✨ Add support for Server Sent Events |
| https://github.com/fastapi/fastapi/pull/14962 | `fastapi/fastapi` | `code_and_docs` | `python` | ✨ Serialize JSON response with Pydantic (in Rust), when there's a Pydantic return type or response model |
| https://github.com/fastapi/fastapi/pull/15293 | `fastapi/fastapi` | `code_only` | `python` | 🔨 Add pre-commit hook to ensure latest release header has date |
| https://github.com/fastapi/fastapi/pull/15139 | `fastapi/fastapi` | `code_only` | `python` | ⬆️ Increase lower bound to `pydantic >=2.9.0.` and fix the test suite |
| https://github.com/fastapi/fastapi/pull/42 | `fastapi/fastapi` | `code_and_docs` | `python` | Add contributing/development docs |
| https://github.com/fastapi/fastapi/pull/14946 | `fastapi/fastapi` | `code_only` | `python` | ✏️ Fix typo for `client_secret` in OAuth2 form docstrings |
| https://github.com/fastapi/fastapi/pull/15088 | `fastapi/fastapi` | `code_only` | `python` | 🔨 Exclude spam comments from statistics in `scripts/people.py` |
| https://github.com/fastapi/fastapi/pull/15166 | `fastapi/fastapi` | `code_only` | `python` | 🔨 Tweak translation workflow and translation fixer tool |
| https://github.com/fastapi/fastapi/pull/15151 | `fastapi/fastapi` | `code_only` | `python` | 🔨 Fix `commit_in_place` passed via env variable in `translate.yml` workflow |
| https://github.com/fastapi/fastapi/pull/15145 | `fastapi/fastapi` | `code_only` | `python` | 👷 Re-enable translation workflow run by cron in CI (twice a month) |
| https://github.com/fastapi/fastapi/pull/15116 | `fastapi/fastapi` | `code_only` | `python` | 📝 Fix duplicated words in docstrings |
| https://github.com/fastapi/fastapi/pull/15091 | `fastapi/fastapi` | `code_only` | `python` | 👷 Add `ty` to precommit |
| https://github.com/fastapi/fastapi/pull/14964 | `fastapi/fastapi` | `code_and_docs` | `python` | 🗑️ Deprecate `ORJSONResponse` and `UJSONResponse` |
| https://github.com/fastapi/fastapi/pull/15106 | `fastapi/fastapi` | `code_only` | `python` | ⬆ Bump dorny/paths-filter from 3 to 4 |
| https://github.com/fastapi/fastapi/pull/15062 | `fastapi/fastapi` | `code_only` | `python` | 🔨 Update script to autofix permalinks to account for headers with Markdown links |
| https://github.com/fastapi/fastapi/pull/15057 | `fastapi/fastapi` | `code_only` | `python` | 📌 Pin Click for MkDocs live reload |
| https://github.com/fastapi/fastapi/pull/14944 | `fastapi/fastapi` | `code_only` | `python` | 📝 Fix doctrings for `max_digits` and `decimal_places` |
| https://github.com/fastapi/fastapi/pull/15020 | `fastapi/fastapi` | `code_only` | `python` | ⬆ Bump actions/download-artifact from 7 to 8 |
| https://github.com/fastapi/fastapi/pull/15019 | `fastapi/fastapi` | `code_only` | `python` | ⬆ Bump actions/upload-artifact from 6 to 7 |
| https://github.com/fastapi/fastapi/pull/15038 | `fastapi/fastapi` | `code_only` | `python` | 🐛 Fix, avoid yield from a TaskGroup, only as an async context manager, closed in the request async exit stack |
| https://github.com/fastapi/fastapi/pull/15022 | `fastapi/fastapi` | `code_and_docs` | `python` | ✨ Add support for streaming JSON Lines and binary data with `yield` |
| https://github.com/fastapi/fastapi/pull/15023 | `fastapi/fastapi` | `code_and_docs` | `python` | 📝 Update docs for responses and new stream with `yield` |
| https://github.com/fastapi/fastapi/pull/14681 | `fastapi/fastapi` | `code_and_docs` | `python` | 📝 Add `await` in `StreamingResponse` code example to allow cancellation |
| https://github.com/fastapi/fastapi/pull/14953 | `fastapi/fastapi` | `code_and_docs` | `python` | ♻️ Fix JSON Schema for bytes, use `"contentMediaType": "application/octet-stream"` instead of `"format": "binary"` |
| https://github.com/fastapi/fastapi/pull/14979 | `fastapi/fastapi` | `code_and_docs` | `python` | 📝 Rename `docs_src/websockets` to `docs_src/websockets_` to avoid import errors |
| https://github.com/fastapi/fastapi/pull/14992 | `fastapi/fastapi` | `code_only` | `python` | 🔨 Run tests with `pytest-xdist` and `pytest-cov` |
| https://github.com/fastapi/fastapi/pull/14994 | `fastapi/fastapi` | `code_only_tests_or_fixtures` | `python` | ✅ Fix all tests are skipped on Windows |
| https://github.com/fastapi/fastapi/pull/14987 | `fastapi/fastapi` | `code_only` | `python` | ⬆️ Add support for Starlette 1.0.0+ |
| https://github.com/fastapi/fastapi/pull/14986 | `fastapi/fastapi` | `code_only` | `python` | ♻️ Refactor logic to handle OpenAPI and Swagger UI escaping data |
| https://github.com/fastapi/fastapi/pull/14978 | `fastapi/fastapi` | `code_and_docs` | `python` | 🔒️ Add `strict_content_type` checking for JSON requests |
| https://github.com/fastapi/fastapi/pull/14974 | `fastapi/fastapi` | `code_only_tests_or_fixtures` | `python` | 👷 Allow skipping `benchmark` job in `test` workflow |
| https://github.com/fastapi/fastapi/pull/14951 | `fastapi/fastapi` | `code_only` | `python` | 🔨 Fix `FastAPI People` workflow |
| https://github.com/fastapi/fastapi/pull/14966 | `fastapi/fastapi` | `code_only_tests_or_fixtures` | `python` | 👷 Do not run codspeed with coverage as it's not tracked |
| https://github.com/fastapi/fastapi/pull/14965 | `fastapi/fastapi` | `code_only` | `python` | 👷 Do not include benchmark tests in coverage to speed up coverage processing |
| https://github.com/fastapi/fastapi/pull/14959 | `fastapi/fastapi` | `code_only` | `python` | ⬆️ Upgrade pytest |
| https://github.com/mui/material-ui/pull/48936 | `mui/material-ui` | `code_only_tests_or_fixtures` | `typescript` | [test] Automate the CSS-dependent WCAG criteria |
| https://github.com/mui/material-ui/pull/49030 | `mui/material-ui` | `code_only` | `typescript` | [code-infra] Update CircleCI orb |
| https://github.com/mui/material-ui/pull/49025 | `mui/material-ui` | `code_only` | `typescript` | [core] Use @typescript/typescript6 for the docs tooling |
| https://github.com/mui/material-ui/pull/49007 | `mui/material-ui` | `code_only_tests_or_fixtures` | `typescript` | [test] Use the shared loadFonts from @mui/internal-test-utils |
| https://github.com/mui/material-ui/pull/49010 | `mui/material-ui` | `code_and_docs` | `typescript` | Bump @tanstack/react-virtual to ^3.14.10 |
| https://github.com/mui/material-ui/pull/49014 | `mui/material-ui` | `code_only` | `typescript` | Bump code-infra:devDependencies |
| https://github.com/mui/material-ui/pull/49015 | `mui/material-ui` | `code_and_docs` | `typescript` | Bump es-toolkit to ^1.51.0 |
| https://github.com/mui/material-ui/pull/49013 | `mui/material-ui` | `code_only` | `typescript` | Bump lerna to 10.0.1 |
| https://github.com/mui/material-ui/pull/49017 | `mui/material-ui` | `code_only` | `typescript` | Bump vale-cli/vale to 3.18.0 |
| https://github.com/mui/material-ui/pull/49019 | `mui/material-ui` | `code_and_docs` | `typescript` | Bump postcss-import to ^17.0.0 |
| https://github.com/mui/material-ui/pull/49018 | `mui/material-ui` | `code_only` | `typescript` | Bump @netlify/functions to ^6.0.0 |
| https://github.com/mui/material-ui/pull/49016 | `mui/material-ui` | `code_only` | `typescript` | Bump pnpm to 11.22.0 |
| https://github.com/mui/material-ui/pull/49011 | `mui/material-ui` | `code_and_docs` | `typescript` | Bump code-infra:patchUpdates |
| https://github.com/mui/material-ui/pull/49012 | `mui/material-ui` | `code_only` | `typescript` | Bump GitHub Actions |
| https://github.com/mui/material-ui/pull/49009 | `mui/material-ui` | `code_only` | `typescript` | Bump code-infra-orb digest to 487b5aa |
| https://github.com/mui/material-ui/pull/49008 | `mui/material-ui` | `code_only` | `typescript` | Pin @vitest/eslint-plugin to 1.6.27 |
| https://github.com/mui/material-ui/pull/49006 | `mui/material-ui` | `code_and_docs` | `typescript` | Bump MUI X to 9.12.0 |
| https://github.com/mui/material-ui/pull/49005 | `mui/material-ui` | `code_only` | `typescript` | Bump MUI infra packages |
| https://github.com/mui/material-ui/pull/48995 | `mui/material-ui` | `code_only` | `typescript` | [test] Replace webfontloader with the CSS Font Loading API |
| https://github.com/mui/material-ui/pull/48914 | `mui/material-ui` | `code_only` | `typescript` | [code-infra] Fix team sync review requests |
| https://github.com/mui/material-ui/pull/48603 | `mui/material-ui` | `code_only` | `typescript` | [styled-engine] Prevent enableCssLayer styles from being overridden by unlayered styles |
| https://github.com/mui/material-ui/pull/48915 | `mui/material-ui` | `code_and_docs` | `typescript` | [test] Add an `assertions` mode to the axe regression harness |
| https://github.com/mui/material-ui/pull/48978 | `mui/material-ui` | `code_and_docs` | `typescript` | Bump nextjs monorepo to 16.3.1 |
| https://github.com/mui/material-ui/pull/48998 | `mui/material-ui` | `code_only` | `typescript` | Bump MUI infra packages |
| https://github.com/mui/material-ui/pull/48886 | `mui/material-ui` | `code_and_docs` | `typescript` | [docs] Bump @docsearch/react to ^4.7.0 |
| https://github.com/mui/material-ui/pull/48985 | `mui/material-ui` | `code_only` | `typescript` | Bump supports-color to 11.0.0 |
| https://github.com/mui/material-ui/pull/48903 | `mui/material-ui` | `code_only` | `typescript` | Bump jsdom to 30.0.1 |
| https://github.com/mui/material-ui/pull/48994 | `mui/material-ui` | `code_only` | `typescript` | Bump MUI infra packages |
| https://github.com/mui/material-ui/pull/48993 | `mui/material-ui` | `code_only` | `typescript` | [ButtonGroup] Prevent sticky hover border on touch devices |
| https://github.com/mui/material-ui/pull/48948 | `mui/material-ui` | `code_only_tests_or_fixtures` | `typescript` | [test] Fail the regression run when a webfont does not load |
| https://github.com/mui/material-ui/pull/48984 | `mui/material-ui` | `code_and_docs` | `typescript` | Bump react-intersection-observer to ^11.0.0 |
| https://github.com/mui/material-ui/pull/48976 | `mui/material-ui` | `code_only` | `typescript` | Bump code-infra:devDependencies |
| https://github.com/mui/material-ui/pull/48955 | `mui/material-ui` | `code_only` | `typescript` | [utils] Fix resolveProps to correctly merge slotProps defined as functions |
| https://github.com/mui/material-ui/pull/48974 | `mui/material-ui` | `code_only` | `typescript` | Bump @base-ui/react to ^1.7.0 |
| https://github.com/mui/material-ui/pull/48986 | `mui/material-ui` | `code_only` | `typescript` | Bump vale-cli/vale-action action to v3.0.0 |
| https://github.com/mui/material-ui/pull/48979 | `mui/material-ui` | `code_only` | `typescript` | Bump pnpm to 11.21.0 |
| https://github.com/mui/material-ui/pull/48981 | `mui/material-ui` | `code_only` | `typescript` | Bump recast to ^0.24.0 |
| https://github.com/mui/material-ui/pull/48980 | `mui/material-ui` | `code_and_docs` | `typescript` | Bump postcss-import to ^16.2.0 |
| https://github.com/mui/material-ui/pull/48977 | `mui/material-ui` | `code_and_docs` | `typescript` | Bump markdown-to-jsx to ^9.10.2 |
| https://github.com/mui/material-ui/pull/48975 | `mui/material-ui` | `code_and_docs` | `typescript` | Bump @types/semver to 7.8.0 |
| https://github.com/mui/material-ui/pull/48973 | `mui/material-ui` | `code_and_docs` | `typescript` | Bump react monorepo |
| https://github.com/mui/material-ui/pull/48962 | `mui/material-ui` | `code_only` | `typescript` | [website] Fix focus-visible style non-text contrast failure for keyboard accessibility on banner announcement link |
| https://github.com/mui/material-ui/pull/48972 | `mui/material-ui` | `code_only` | `typescript` | Bump GitHub Actions |
| https://github.com/mui/material-ui/pull/48971 | `mui/material-ui` | `code_only` | `typescript` | Bump eslint |
| https://github.com/mui/material-ui/pull/48966 | `mui/material-ui` | `code_and_docs` | `typescript` | [utils][docs] Replace deprecated `clip` CSS property with `clip-path` |
| https://github.com/mui/material-ui/pull/48970 | `mui/material-ui` | `code_and_docs` | `typescript` | Bump code-infra:patchUpdates |
| https://github.com/mui/material-ui/pull/48969 | `mui/material-ui` | `code_only` | `typescript` | Bump babel monorepo to ^7.29.8 |
| https://github.com/mui/material-ui/pull/48987 | `mui/material-ui` | `code_only_tests_or_fixtures` | `typescript` | [test] Fix typo 'overriden' -> 'overridden' in Alert test comment |
| https://github.com/mui/material-ui/pull/48963 | `mui/material-ui` | `code_only` | `typescript` | [website] Fix WCAG criteria for code copy button |
| https://github.com/mui/material-ui/pull/37726 | `mui/material-ui` | `code_only` | `typescript` | [internal] Fix priority support prompt action flow |
| https://github.com/mui/material-ui/pull/37824 | `mui/material-ui` | `code_only` | `typescript` | [internal] Update priority support issue template and prompt |
| https://github.com/mui/material-ui/pull/41276 | `mui/material-ui` | `code_and_docs` | `typescript` | [website] Use MUI X Data Grid v7-beta |
| https://github.com/mui/material-ui/pull/44176 | `mui/material-ui` | `code_and_docs` | `typescript` | [website] Remove Boeing logo from X product page |
| https://github.com/mui/material-ui/pull/47606 | `mui/material-ui` | `code_and_docs` | `typescript` | [website] Implement the latest price changes proposal |
| https://github.com/mui/material-ui/pull/48187 | `mui/material-ui` | `code_and_docs` | `typescript` | [docs] Add agent skills for styling, theming, Next.js, and Tailwind CSS integrations |
| https://github.com/mui/material-ui/pull/48209 | `mui/material-ui` | `code_only` | `typescript` | [docs-infra] Add x-chat to MuiProductId type and product switcher |
| https://github.com/mui/material-ui/pull/48387 | `mui/material-ui` | `code_and_docs` | `typescript` | [docs] Link to agent skills in relevant docs |
| https://github.com/mui/material-ui/pull/48904 | `mui/material-ui` | `code_only` | `typescript` | Bump lerna to 10.0.0 |
| https://github.com/mui/material-ui/pull/48947 | `mui/material-ui` | `code_only_tests_or_fixtures` | `typescript` | [test][tooltip] Keep the disabled trigger away from the real pointer |
| https://github.com/mui/material-ui/pull/48953 | `mui/material-ui` | `code_only` | `typescript` | [website] Fix overline duplicating the h2 heading |
| https://github.com/mui/material-ui/pull/48946 | `mui/material-ui` | `code_only` | `typescript` | [l10n] Complete Traditional Chinese localization |

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
| `microsoft/TypeScript-go` | `4328` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4670` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4756` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4730` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `3277` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4816` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `3989` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4160` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `2944` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4729` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4835` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4821` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4812` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4810` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4772` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4769` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4721` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4698` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4693` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4668` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4667` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4570` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4482` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4444` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4412` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4158` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4270` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4266` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4003` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `3987` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `3738` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `3706` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `3252` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `3228` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4870` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `3271` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `3432` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4112` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `3309` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4401` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4767` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4365` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4515` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `3264` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `3220` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4843` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4696` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `2602` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `2417` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4430` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4007` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4714` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4833` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4828` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `3880` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4840` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `3627` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4407` | `too_many_changed_files` | `code_only` |
| `microsoft/TypeScript-go` | `4885` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4884` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4883` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4882` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4421` | `docs_only_excluded` | `docs_only` |
| `microsoft/TypeScript-go` | `4886` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4868` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `microsoft/TypeScript-go` | `4797` | `too_many_changed_files` | `code_only` |
| `microsoft/TypeScript-go` | `4578` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4871` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4811` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4611` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4857` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4856` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4749` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4853` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4842` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4732` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4790` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4777` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4739` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4794` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4584` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4239` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4690` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4582` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4766` | `docs_only_excluded` | `docs_only` |
| `microsoft/TypeScript-go` | `4763` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4717` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4679` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4728` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4737` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4283` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4736` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4574` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `3616` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4707` | `docs_only_excluded` | `docs_only` |
| `microsoft/TypeScript-go` | `4638` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4575` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4474` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4615` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4645` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4659` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `microsoft/TypeScript-go` | `4443` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4625` | `too_large_patch` | `code_only` |
| `microsoft/TypeScript-go` | `4590` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4652` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4644` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4634` | `too_many_changed_files` | `code_only` |
| `microsoft/TypeScript-go` | `4280` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4624` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4621` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4179` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4427` | `not_merged` | `None` |
| `microsoft/TypeScript-go` | `4534` | `not_merged` | `None` |