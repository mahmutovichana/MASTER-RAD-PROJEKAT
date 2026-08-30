# DocGuard Real PR Seed Collector Report

This report summarizes neutral repo-based sampling of merged public GitHub PRs.

The collector does not assign gold labels and does not decide whether documentation should be updated.
It only creates seed PR URLs for the later candidate builder and manual validation workflow.

- Repositories scanned: `769`
- Seeds accepted: `1010`
- Rejected/skipped PRs: `6366`
- Acquisition status: `partial`
- Requirements satisfied: `False`
- Target observed/requested: `1010` / `18000`
- Target deficit: `16990`
- Minimum language deficits: `{'python': 6000}`
- Collector bucket counts: `{'code_only': 697, 'code_and_docs': 257, 'code_only_tests_or_fixtures': 56}`
- Language hint counts: `{'typescript': 1010}`
- Repository counts per language: `{'typescript': 53}`
- Candidate bucket counts per language: `{'typescript': {'code_only': 697, 'code_and_docs': 257, 'code_only_tests_or_fixtures': 56}}`
- Reject reason counts: `{'not_merged': 2555, 'too_many_changed_files': 204, 'docs_only_excluded': 446, 'already_collected': 2058, 'too_large_patch': 56, 'other_or_binary_only_excluded': 172, 'fetch_closed_pulls_failed': 695, 'fetch_pr_files_failed': 180}`

## Methodological Boundary

- This is real public GitHub PR sampling.
- No synthetic examples are generated.
- No final labels are assigned here.
- `collector_bucket` is audit metadata for balancing and review planning, not a model label.
- Final evaluation must use only the safe fields produced later by the candidate builder.

## Accepted Seeds

| PR | Repository | Bucket | Language hint | Title |
| --- | --- | --- | --- | --- |
| https://github.com/1111mp/nvm-desktop/pull/411 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update npm dependencies |
| https://github.com/1111mp/nvm-desktop/pull/407 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update rust crate async_zip to 0.0.19 |
| https://github.com/1111mp/nvm-desktop/pull/408 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update dependency shadcn to v4.19.0 |
| https://github.com/1111mp/nvm-desktop/pull/406 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update dependency motion to v13.1.1 |
| https://github.com/1111mp/nvm-desktop/pull/405 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update dependency i18next to v26.4.0 |
| https://github.com/1111mp/nvm-desktop/pull/404 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update dependency vite to v8.2.2 |
| https://github.com/1111mp/nvm-desktop/pull/403 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update dependency lucide-react to v1.33.0 |
| https://github.com/1111mp/nvm-desktop/pull/402 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update npm dependencies |
| https://github.com/1111mp/nvm-desktop/pull/401 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): lock file maintenance |
| https://github.com/1111mp/nvm-desktop/pull/398 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update dependency shadcn to v4.18.0 |
| https://github.com/1111mp/nvm-desktop/pull/397 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update dependency shadcn to v4.17.0 |
| https://github.com/1111mp/nvm-desktop/pull/390 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update npm dependencies (major) |
| https://github.com/1111mp/nvm-desktop/pull/396 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update dependency oxfmt to ^0.63.0 |
| https://github.com/1111mp/nvm-desktop/pull/395 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update dependency lucide-react to v1.31.0 |
| https://github.com/1111mp/nvm-desktop/pull/394 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): lock file maintenance |
| https://github.com/1111mp/nvm-desktop/pull/392 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update dependency lucide-react to v1.30.0 |
| https://github.com/1111mp/nvm-desktop/pull/391 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update npm dependencies |
| https://github.com/1111mp/nvm-desktop/pull/389 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update npm dependencies |
| https://github.com/1111mp/nvm-desktop/pull/388 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update dependency node to v24.19.0 |
| https://github.com/1111mp/nvm-desktop/pull/387 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): lock file maintenance |
| https://github.com/a2ui-project/a2ui/pull/2390 | `a2ui-project/a2ui` | `code_only` | `typescript` | Fix file resolve |
| https://github.com/a2ui-project/a2ui/pull/2396 | `a2ui-project/a2ui` | `code_and_docs` | `typescript` | fix(ci): use A2UI_REMEDIATION_PAT_TOKEN for draft PR creation and require banner in audit skill |
| https://github.com/a2ui-project/a2ui/pull/2392 | `a2ui-project/a2ui` | `code_only` | `typescript` | ci: switch GitHub Actions runners to ubuntu-latest |
| https://github.com/a2ui-project/a2ui/pull/2365 | `a2ui-project/a2ui` | `code_and_docs` | `typescript` | Improve script that labels items for triage. |
| https://github.com/a2ui-project/a2ui/pull/2331 | `a2ui-project/a2ui` | `code_only` | `typescript` | feat(swift): Core validation rules, reactivity, and type coercion |
| https://github.com/a2ui-project/a2ui/pull/2340 | `a2ui-project/a2ui` | `code_only` | `typescript` | feat(python): implement Catalog composition, function typing, and UAX 31 validation |
| https://github.com/angular/angular/pull/69892 | `angular/angular` | `code_and_docs` | `typescript` | Bump version to "v22.0.8" with changelog. |
| https://github.com/angular/angular/pull/69891 | `angular/angular` | `code_only` | `typescript` | build: update pnpm-lock.yaml |
| https://github.com/angular/angular/pull/69743 | `angular/angular` | `code_only` | `typescript` | fix(common): preserve crossorigin on image preloads |
| https://github.com/angular/angular/pull/69853 | `angular/angular` | `code_only` | `typescript` | fix(migrations): correctly migrate ngClass keys mixing space-separated and regular class names |
| https://github.com/angular/angular/pull/69830 | `angular/angular` | `code_only` | `typescript` | refactor(compiler): enforce exhaustive defer trigger handling |
| https://github.com/angular/angular/pull/69872 | `angular/angular` | `code_only` | `typescript` | build: update cross-repo angular dependencies (main) |
| https://github.com/angular/angular/pull/69871 | `angular/angular` | `code_only` | `typescript` | build: update cross-repo angular dependencies (22.0.x) |
| https://github.com/angular/angular/pull/69875 | `angular/angular` | `code_only` | `typescript` | feat(docs-infra): react with Angie in the playground minigame |
| https://github.com/angular/angular/pull/70313 | `angular/angular` | `code_only` | `typescript` | refactor(docs-infra): remove the orphaned home animation component |
| https://github.com/angular/angular/pull/70312 | `angular/angular` | `code_only` | `typescript` | refactor(docs-infra): type the API manifest in the nav entries |
| https://github.com/angular/angular/pull/70305 | `angular/angular` | `code_only` | `typescript` | refactor(docs-infra): share the angular.dev origin constant |
| https://github.com/angular/angular/pull/70306 | `angular/angular` | `code_only` | `typescript` | refactor(docs-infra): hold editor diagnostics in a signal |
| https://github.com/angular/angular/pull/70303 | `angular/angular` | `code_and_docs` | `typescript` | refactor(compiler-cli): add compiler option for enabling source locations |
| https://github.com/angular/angular/pull/70298 | `angular/angular` | `code_only` | `typescript` | fix(core): preserve namespace for dynamic component hosts |
| https://github.com/angular/angular/pull/70293 | `angular/angular` | `code_only` | `typescript` | refactor(router): add support for blocking router resources |
| https://github.com/angular/angular/pull/70273 | `angular/angular` | `code_only` | `typescript` | Avoid prototype collisions |
| https://github.com/angular/angular/pull/70322 | `angular/angular` | `code_only` | `typescript` | refactor(core):  widen ɵɵclassProp value parameter type to any |
| https://github.com/angular/angular/pull/70311 | `angular/angular` | `code_only` | `typescript` | docs(core): clarify toObservable synchronization behavior |
| https://github.com/angular/angular/pull/69912 | `angular/angular` | `code_and_docs` | `typescript` | refactor(compiler): support block-specific deferredImports mapping |
| https://github.com/angular/angular/pull/69812 | `angular/angular` | `code_only` | `typescript` | build: update all non-major dependencies (main) |
| https://github.com/angular/angular-cli/pull/33612 | `angular/angular-cli` | `code_only` | `typescript` | build: update cross-repo angular dependencies (main) |
| https://github.com/angular/angular-cli/pull/33620 | `angular/angular-cli` | `code_only_tests_or_fixtures` | `typescript` | fix(@angular/build): add bounded timeout to vitest executor disposal |
| https://github.com/angular/angular-cli/pull/33585 | `angular/angular-cli` | `code_only` | `typescript` | perf(@angular/build): skip semantic affected-file walk when type checking is disabled |
| https://github.com/angular/angular-cli/pull/33584 | `angular/angular-cli` | `code_only` | `typescript` | fix(@angular/build): remap metafile paths when workspace root is a symlink or junction |
| https://github.com/angular/angular-cli/pull/33624 | `angular/angular-cli` | `code_and_docs` | `typescript` | build: update dependency quicktype-core to v26 |
| https://github.com/angular/angular-cli/pull/33895 | `angular/angular-cli` | `code_only_tests_or_fixtures` | `typescript` | build: update cross-repo angular dependencies (main) |
| https://github.com/angular/angular-cli/pull/33896 | `angular/angular-cli` | `code_only` | `typescript` | build: remove scorecard workflow |
| https://github.com/angular/angular-cli/pull/33568 | `angular/angular-cli` | `code_only` | `typescript` | feat(@angular/build): migrate advanced optimization Babel plugins to oxc-parser + magic-string |
| https://github.com/angular/angular-cli/pull/33618 | `angular/angular-cli` | `code_only` | `typescript` | fix(@angular/build): ensure import map integrity keys are valid URL-like specifiers |
| https://github.com/angular/angular-cli/pull/33592 | `angular/angular-cli` | `code_only_tests_or_fixtures` | `typescript` | fix(@angular/build): preserve custom config options in runnerConfig for vitest |
| https://github.com/angular/angular-cli/pull/33565 | `angular/angular-cli` | `code_only` | `typescript` | fix(@angular/cli): resolve correct registry name when using npm alias syntax during update |
| https://github.com/angular/angular-cli/pull/33572 | `angular/angular-cli` | `code_only` | `typescript` | fix(@angular/build): anchor debug ID comment matching and make injection idempotent |
| https://github.com/angular/angular-cli/pull/33598 | `angular/angular-cli` | `code_only` | `typescript` | fix(@angular/cli): batch Prettier invocations during migration formatting |
| https://github.com/angular/angular-cli/pull/33611 | `angular/angular-cli` | `code_only_tests_or_fixtures` | `typescript` | build: update cross-repo angular dependencies (main) |
| https://github.com/angular/angular-cli/pull/33607 | `angular/angular-cli` | `code_only` | `typescript` | build: update cross-repo angular dependencies (22.0.x) |
| https://github.com/angular/angular-cli/pull/33887 | `angular/angular-cli` | `code_only` | `typescript` | build: update github/codeql-action action to v4.37.7 (main) |
| https://github.com/angular/angular-cli/pull/33881 | `angular/angular-cli` | `code_only` | `typescript` | build: update cross-repo angular dependencies (22.1.x) |
| https://github.com/angular/angular-cli/pull/33890 | `angular/angular-cli` | `code_only` | `typescript` | build: update github/codeql-action action to v4.37.7 (22.1.x) |
| https://github.com/angular/angular-cli/pull/33886 | `angular/angular-cli` | `code_only` | `typescript` | build: update cross-repo angular dependencies (main) |
| https://github.com/angular/angular-cli/pull/33888 | `angular/angular-cli` | `code_only` | `typescript` | build: update all non-major dependencies (main) |
| https://github.com/ant-design/ant-design/pull/59062 | `ant-design/ant-design` | `code_only` | `typescript` | site: restore relative component LLMs links |
| https://github.com/ant-design/ant-design/pull/59058 | `ant-design/ant-design` | `code_and_docs` | `typescript` | feat(Radio): support classNames and styles in Radio.Group |
| https://github.com/ant-design/ant-design/pull/59059 | `ant-design/ant-design` | `code_and_docs` | `typescript` | feat(Checkbox): support classNames and styles in Checkbox.Group |
| https://github.com/ant-design/ant-design/pull/59067 | `ant-design/ant-design` | `code_and_docs` | `typescript` | chore: merge master into feature |
| https://github.com/ant-design/ant-design/pull/59063 | `ant-design/ant-design` | `code_only` | `typescript` | site: fix code-box style with Badge |
| https://github.com/ant-design/ant-design/pull/58267 | `ant-design/ant-design` | `code_only` | `typescript` | feat(Cascader, Select, TreeSelect): improve clear button accessibility |
| https://github.com/ant-design/ant-design/pull/3531 | `ant-design/ant-design` | `code_only` | `typescript` | optimize declaration |
| https://github.com/ant-design/ant-design/pull/59065 | `ant-design/ant-design` | `code_only` | `typescript` | Revert "site: fix code-box style with Badge" |
| https://github.com/ant-design/ant-design/pull/59064 | `ant-design/ant-design` | `code_only` | `typescript` | fix(Descriptions): preserve item state when key is 0 |
| https://github.com/ant-design/ant-design/pull/57725 | `ant-design/ant-design` | `code_only` | `typescript` | fix: use ant.design URLs for component LLMs links |
| https://github.com/ant-design/ant-design/pull/59054 | `ant-design/ant-design` | `code_and_docs` | `typescript` | feat(Typography): support shimmer effect |
| https://github.com/ant-design/ant-design/pull/59060 | `ant-design/ant-design` | `code_only` | `typescript` | fix(List): recommend Listy in deprecation warning |
| https://github.com/ant-design/ant-design/pull/3753 | `ant-design/ant-design` | `code_and_docs` | `typescript` | feat: basic impl of RangePicker[ranges], ref: #1418 |
| https://github.com/ant-design/ant-design/pull/59048 | `ant-design/ant-design` | `code_only` | `typescript` | fix(Menu): upgrade dependencies for unique popup ids |
| https://github.com/ant-design/ant-design/pull/59029 | `ant-design/ant-design` | `code_only` | `typescript` | fix(Tree): handle zero key in DirectoryTree range selection |
| https://github.com/ant-design/ant-design/pull/59028 | `ant-design/ant-design` | `code_only` | `typescript` | fix(Cascader): respect null notFoundContent |
| https://github.com/ant-design/ant-design/pull/58894 | `ant-design/ant-design` | `code_and_docs` | `typescript` | feat: support progress ring for FloatButton.BackTop |
| https://github.com/ant-design/ant-design/pull/59040 | `ant-design/ant-design` | `code_and_docs` | `typescript` | chore: merge master into feature |
| https://github.com/ant-design/ant-design/pull/59002 | `ant-design/ant-design` | `code_and_docs` | `typescript` | fix(Upload): forward focus events |
| https://github.com/ant-design/ant-design/pull/59032 | `ant-design/ant-design` | `code_only` | `typescript` | test(Card): enable button-name accessibility checks |
| https://github.com/appwrite/appwrite/pull/13307 | `appwrite/appwrite` | `code_only` | `typescript` | chore: require utopia-php/cache ^5.0 |
| https://github.com/appwrite/appwrite/pull/13306 | `appwrite/appwrite` | `code_only` | `typescript` | chore: remove upload ID extension |
| https://github.com/appwrite/appwrite/pull/13305 | `appwrite/appwrite` | `code_only` | `typescript` | chore: remove redundant discriminator property names |
| https://github.com/appwrite/appwrite/pull/13303 | `appwrite/appwrite` | `code_only` | `typescript` | chore: autologin local Adminer at postgres.localhost |
| https://github.com/appwrite/appwrite/pull/13301 | `appwrite/appwrite` | `code_only` | `typescript` | feat(specs): emit annotated enumerations |
| https://github.com/appwrite/appwrite/pull/13299 | `appwrite/appwrite` | `code_only` | `typescript` | fix(deployments): reference _APP_COMPUTE_SIZE_LIMIT in size errors |
| https://github.com/appwrite/appwrite/pull/13294 | `appwrite/appwrite` | `code_only` | `typescript` | Bind project management authorization to path target |
| https://github.com/appwrite/appwrite/pull/13295 | `appwrite/appwrite` | `code_only` | `typescript` | fix(specs): keep open enums open in the generated spec |
| https://github.com/appwrite/appwrite/pull/13293 | `appwrite/appwrite` | `code_only` | `typescript` | fix: emit Project.wafEnabled for SDK 27 migration client |
| https://github.com/appwrite/appwrite/pull/13273 | `appwrite/appwrite` | `code_only` | `typescript` | Refactor webhook dispatches to use Utopia Fetch client |
| https://github.com/appwrite/appwrite/pull/13290 | `appwrite/appwrite` | `code_only` | `typescript` | Run the orchestrator from its all-in-one image |
| https://github.com/appwrite/appwrite/pull/13263 | `appwrite/appwrite` | `code_only` | `typescript` | Messaging targets subquery  |
| https://github.com/appwrite/appwrite/pull/13259 | `appwrite/appwrite` | `code_only` | `typescript` | feat(vcs): add Codebase (Cursor Origin) provider |
| https://github.com/appwrite/appwrite/pull/13252 | `appwrite/appwrite` | `code_only` | `typescript` | feat: Add Gravatar avatar support with session fallback |
| https://github.com/appwrite/appwrite/pull/13285 | `appwrite/appwrite` | `code_only` | `typescript` | feat: VCS adapter capabilities and provider-agnostic source archives |
| https://github.com/appwrite/appwrite/pull/13288 | `appwrite/appwrite` | `code_only_tests_or_fixtures` | `typescript` | test: drop HTTP action unit tests covered by e2e |
| https://github.com/appwrite/appwrite/pull/13287 | `appwrite/appwrite` | `code_only` | `typescript` | refactor(schedulers): record project access on consume, not on publish |
| https://github.com/appwrite/appwrite/pull/13123 | `appwrite/appwrite` | `code_only` | `typescript` | Feat 13067 huggingface oauth provider |
| https://github.com/appwrite/appwrite/pull/13283 | `appwrite/appwrite` | `code_only` | `typescript` | Bump utopia-php/platform |
| https://github.com/appwrite/appwrite/pull/13282 | `appwrite/appwrite` | `code_only` | `typescript` | Fix vectorsdb query size |
| https://github.com/appwrite/sdk-for-web/pull/178 | `appwrite/sdk-for-web` | `code_and_docs` | `typescript` | feat: Web SDK update for version 26.2.0 |
| https://github.com/appwrite/sdk-for-web/pull/176 | `appwrite/sdk-for-web` | `code_and_docs` | `typescript` | feat: SDK update for version 26.1.0 |
| https://github.com/appwrite/sdk-for-web/pull/175 | `appwrite/sdk-for-web` | `code_and_docs` | `typescript` | feat: Web SDK update for version 26.0.0 |
| https://github.com/appwrite/sdk-for-web/pull/174 | `appwrite/sdk-for-web` | `code_only` | `typescript` | feat: support concurrent chunk uploads |
| https://github.com/appwrite/sdk-for-web/pull/171 | `appwrite/sdk-for-web` | `code_and_docs` | `typescript` | feat: Web SDK update for version 25.1.1 |
| https://github.com/appwrite/sdk-for-web/pull/170 | `appwrite/sdk-for-web` | `code_and_docs` | `typescript` | feat: Web SDK update for version 25.1.0 |
| https://github.com/appwrite/sdk-for-web/pull/168 | `appwrite/sdk-for-web` | `code_and_docs` | `typescript` | feat: SDK update for version 25.0.0 |
| https://github.com/appwrite/sdk-for-web/pull/167 | `appwrite/sdk-for-web` | `code_and_docs` | `typescript` | feat: Web SDK update for version 24.2.0 |
| https://github.com/appwrite/sdk-for-web/pull/166 | `appwrite/sdk-for-web` | `code_and_docs` | `typescript` | feat: Web SDK update for version 24.1.1 |
| https://github.com/appwrite/sdk-for-web/pull/164 | `appwrite/sdk-for-web` | `code_and_docs` | `typescript` | feat: Web SDK update for version 24.1.0 |
| https://github.com/appwrite/sdk-for-web/pull/161 | `appwrite/sdk-for-web` | `code_and_docs` | `typescript` | feat: Web SDK update for version 24.0.0 |
| https://github.com/appwrite/sdk-for-web/pull/159 | `appwrite/sdk-for-web` | `code_and_docs` | `typescript` | feat: Web SDK update for version 23.0.0 |
| https://github.com/appwrite/sdk-for-web/pull/158 | `appwrite/sdk-for-web` | `code_and_docs` | `typescript` | feat: Web SDK update for version 22.4.1 |
| https://github.com/appwrite/sdk-for-web/pull/157 | `appwrite/sdk-for-web` | `code_and_docs` | `typescript` | feat: Web SDK update for version 22.4.0 |
| https://github.com/appwrite/sdk-for-web/pull/156 | `appwrite/sdk-for-web` | `code_and_docs` | `typescript` | feat: Web SDK update for version 22.3.1 |
| https://github.com/appwrite/sdk-for-web/pull/155 | `appwrite/sdk-for-web` | `code_and_docs` | `typescript` | feat: Web SDK update for version 22.3.0 |
| https://github.com/appwrite/sdk-for-web/pull/154 | `appwrite/sdk-for-web` | `code_only` | `typescript` | feat: Web SDK update for version 22.1.0 |
| https://github.com/appwrite/sdk-for-web/pull/153 | `appwrite/sdk-for-web` | `code_and_docs` | `typescript` | feat: Web SDK update for version 22.1.0 |
| https://github.com/appwrite/sdk-for-web/pull/150 | `appwrite/sdk-for-web` | `code_and_docs` | `typescript` | feat: Web SDK update for version 22.0.0 |
| https://github.com/appwrite/sdk-for-web/pull/148 | `appwrite/sdk-for-web` | `code_and_docs` | `typescript` | feat: Web SDK update for version 21.5.0 |
| https://github.com/babel/babel/pull/18179 | `babel/babel` | `code_only` | `typescript` | Enable `no-useless-computed-key` rule |
| https://github.com/babel/babel/pull/18153 | `babel/babel` | `code_only` | `typescript` | Handle null in `getAll{Prev,Next}Siblings` |
| https://github.com/babel/babel/pull/18088 | `babel/babel` | `code_only` | `typescript` | Fix initialization of nested for loop head declarations |
| https://github.com/babel/babel/pull/18046 | `babel/babel` | `code_only` | `typescript` | fix(generator): improve new callee parens check |
| https://github.com/babel/babel/pull/18145 | `babel/babel` | `code_only` | `typescript` | refactor: replace `semver` with `verkit` |
| https://github.com/babel/babel/pull/18137 | `babel/babel` | `code_only` | `typescript` | fix(babel-register): preserve app-managed graceful shutdown |
| https://github.com/babel/babel/pull/18177 | `babel/babel` | `code_only` | `typescript` | Update node flags list |
| https://github.com/babel/babel/pull/18144 | `babel/babel` | `code_only_tests_or_fixtures` | `typescript` | fix: Load ESM fixture options default exports |
| https://github.com/babel/babel/pull/18159 | `babel/babel` | `code_only` | `typescript` | fix: Define child node types correctly |
| https://github.com/babel/babel/pull/18160 | `babel/babel` | `code_only_tests_or_fixtures` | `typescript` | Update test262 |
| https://github.com/babel/babel/pull/18010 | `babel/babel` | `code_only_tests_or_fixtures` | `typescript` | Update test262 |
| https://github.com/babel/babel/pull/18103 | `babel/babel` | `code_only` | `typescript` | Simplify AST validators |
| https://github.com/babel/babel/pull/18129 | `babel/babel` | `code_only` | `typescript` | Fix top-level enter and exit visitor types |
| https://github.com/babel/babel/pull/18141 | `babel/babel` | `code_only` | `typescript` | fix: Avoid bundling `package/sub` |
| https://github.com/babel/babel/pull/18140 | `babel/babel` | `code_only` | `typescript` | chore: fix @babel/eslint-plugin peer deps |
| https://github.com/babel/babel/pull/18139 | `babel/babel` | `code_only` | `typescript` | Remove cycles support from tsconfig generator |
| https://github.com/babel/babel/pull/18131 | `babel/babel` | `code_only` | `typescript` | fix(register): do not inherit parent execArgv |
| https://github.com/babel/babel/pull/18138 | `babel/babel` | `code_only_tests_or_fixtures` | `typescript` | Add whitespace in source-map-visual tests |
| https://github.com/babel/babel/pull/18135 | `babel/babel` | `code_only` | `typescript` | Up source map packages |
| https://github.com/babel/babel/pull/18095 | `babel/babel` | `code_only` | `typescript` | Add types for `@babel/standalone` |
| https://github.com/chakra-ui/chakra-ui/pull/10943 | `chakra-ui/chakra-ui` | `code_and_docs` | `typescript` | docs: add Emotion style registry for Next.js App Router (Fixes #10942) |
| https://github.com/chakra-ui/chakra-ui/pull/10946 | `chakra-ui/chakra-ui` | `code_and_docs` | `typescript` | docs(date-picker): add Persian (Jalali) calendar example |
| https://github.com/chakra-ui/chakra-ui/pull/10948 | `chakra-ui/chakra-ui` | `code_and_docs` | `typescript` | docs(spinner): add custom indicator example |
| https://github.com/chakra-ui/chakra-ui/pull/10938 | `chakra-ui/chakra-ui` | `code_and_docs` | `typescript` | fix(radio-card): outline variant preserves border-width when disabled |
| https://github.com/chakra-ui/chakra-ui/pull/10939 | `chakra-ui/chakra-ui` | `code_and_docs` | `typescript` | chore(deps): update @ark-ui/react to 5.38.2 |
| https://github.com/chakra-ui/chakra-ui/pull/10934 | `chakra-ui/chakra-ui` | `code_and_docs` | `typescript` | feat(codemod): faster in-process upgrade with a real dry-run preview |
| https://github.com/chakra-ui/chakra-ui/pull/10933 | `chakra-ui/chakra-ui` | `code_and_docs` | `typescript` | fix(codemod): report dry-run output and fix parser/package-scan bugs |
| https://github.com/chakra-ui/chakra-ui/pull/10917 | `chakra-ui/chakra-ui` | `code_and_docs` | `typescript` | docs(compositions): add toggle-tip usage examples |
| https://github.com/chakra-ui/chakra-ui/pull/10915 | `chakra-ui/chakra-ui` | `code_only` | `typescript` | fix(compositions): support addons in InputGroup snippet |
| https://github.com/chakra-ui/chakra-ui/pull/10676 | `chakra-ui/chakra-ui` | `code_and_docs` | `typescript` | feat: improve createOverlay types |
| https://github.com/chakra-ui/chakra-ui/pull/10919 | `chakra-ui/chakra-ui` | `code_and_docs` | `typescript` | fix: preserve italic styles in preflight |
| https://github.com/chakra-ui/chakra-ui/pull/10908 | `chakra-ui/chakra-ui` | `code_and_docs` | `typescript` | fix: missing type="button" on Tag, ActionBar, Dialog, Drawer triggers |
| https://github.com/chakra-ui/chakra-ui/pull/10857 | `chakra-ui/chakra-ui` | `code_and_docs` | `typescript` | Version Packages |
| https://github.com/chakra-ui/chakra-ui/pull/10885 | `chakra-ui/chakra-ui` | `code_and_docs` | `typescript` | fix: correct css prop usage in Bleed component |
| https://github.com/chakra-ui/chakra-ui/pull/10879 | `chakra-ui/chakra-ui` | `code_and_docs` | `typescript` | fix: correct css prop usage in Float component |
| https://github.com/chakra-ui/chakra-ui/pull/10874 | `chakra-ui/chakra-ui` | `code_and_docs` | `typescript` | Rename TanStackRouterVite to tanstackRouter |
| https://github.com/chakra-ui/chakra-ui/pull/10873 | `chakra-ui/chakra-ui` | `code_and_docs` | `typescript` | fix: forward the rel attribute on LinkOverlay |
| https://github.com/chakra-ui/chakra-ui/pull/10870 | `chakra-ui/chakra-ui` | `code_only` | `typescript` | fix(listbox): prevent crash when filter empties collection in explorer demo |
| https://github.com/chakra-ui/chakra-ui/pull/10864 | `chakra-ui/chakra-ui` | `code_only` | `typescript` | fix: correct misspelled "permuations" variable in breakpoints |
| https://github.com/chakra-ui/chakra-ui/pull/10863 | `chakra-ui/chakra-ui` | `code_and_docs` | `typescript` | fix: correct className usage in Image component |
| https://github.com/denoland/deno/pull/36633 | `denoland/deno` | `code_only` | `typescript` | fix(ext/node_sqlite): invalidate sessions on database close |
| https://github.com/denoland/deno/pull/36353 | `denoland/deno` | `code_only` | `typescript` | fix(core): make Unix pipe fd ownership explicit |
| https://github.com/denoland/deno/pull/36559 | `denoland/deno` | `code_only` | `typescript` | fix(ext/napi): wake the event loop at the next uv_timer deadline |
| https://github.com/denoland/deno/pull/36629 | `denoland/deno` | `code_only` | `typescript` | fix(ext/http): keep request body readable after response is sent |
| https://github.com/denoland/deno/pull/36557 | `denoland/deno` | `code_only` | `typescript` | fix(ext/node): build the proxied request target with the URL parser |
| https://github.com/denoland/deno/pull/36558 | `denoland/deno` | `code_only` | `typescript` | fix(ext/fetch): raise default HTTP/2 SETTINGS_MAX_HEADER_LIST_SIZE to 256KB |
| https://github.com/denoland/deno/pull/36565 | `denoland/deno` | `code_only` | `typescript` | refactor(ext/node): remove unused `n` arg from `IncomingMessage._read` |
| https://github.com/denoland/deno/pull/36611 | `denoland/deno` | `code_only` | `typescript` | fix(ext/web): snapshot SharedArrayBuffer input in TextDecoder.decode() |
| https://github.com/denoland/deno/pull/36496 | `denoland/deno` | `code_only` | `typescript` | fix(http): truncate streaming responses to content length |
| https://github.com/denoland/deno/pull/36619 | `denoland/deno` | `code_only` | `typescript` | fix(npm): resolve bare npm specifier when latest is too new for min dependency age |
| https://github.com/denoland/deno/pull/36620 | `denoland/deno` | `code_only_tests_or_fixtures` | `typescript` | ci: stop node_compat shard 0 starving its runner |
| https://github.com/denoland/deno/pull/36617 | `denoland/deno` | `code_only` | `typescript` | ci: time out the sysroot setup step after 10 minutes |
| https://github.com/denoland/deno/pull/36608 | `denoland/deno` | `code_only` | `typescript` | fix(npm): flatten single-resolution peers when building package ids |
| https://github.com/denoland/deno/pull/36470 | `denoland/deno` | `code_only` | `typescript` | fix(fetch): require an initial multipart boundary |
| https://github.com/denoland/deno/pull/36436 | `denoland/deno` | `code_only` | `typescript` | fix(process): reject NULs in Windows arguments |
| https://github.com/denoland/deno/pull/36459 | `denoland/deno` | `code_only` | `typescript` | fix(node_crypto): size cipher updates by byte length |
| https://github.com/denoland/deno/pull/36460 | `denoland/deno` | `code_only` | `typescript` | fix(node): preserve v8 deserializer view offsets |
| https://github.com/denoland/deno/pull/36471 | `denoland/deno` | `code_only` | `typescript` | fix(node): validate raw outgoing HTTP headers |
| https://github.com/denoland/deno/pull/36478 | `denoland/deno` | `code_only` | `typescript` | fix(glob): retain valid gitignore rules after parse errors |
| https://github.com/denoland/deno/pull/36607 | `denoland/deno` | `code_only` | `typescript` | fix(npm): match peer fallbacks when checking peer resolution cache |
| https://github.com/freshframework/fresh/pull/3831 | `denoland/fresh` | `code_and_docs` | `typescript` | www: change domain to usefresh.dev |
| https://github.com/freshframework/fresh/pull/3825 | `denoland/fresh` | `code_only` | `typescript` | fix: stylesheet links in <Head> drop entry CSS |
| https://github.com/freshframework/fresh/pull/3781 | `denoland/fresh` | `code_only` | `typescript` | fix: CSS modules not working in _app/_layout/_error and across routes in non-island components |
| https://github.com/freshframework/fresh/pull/3810 | `denoland/fresh` | `code_only` | `typescript` | fix: inject client entry on islands-free pages for HMR |
| https://github.com/freshframework/fresh/pull/3823 | `denoland/fresh` | `code_only` | `typescript` | fix: support WebSocket upgrades in dev server |
| https://github.com/freshframework/fresh/pull/3808 | `denoland/fresh` | `code_only` | `typescript` | fix: handle non-standard HTTP methods in router |
| https://github.com/freshframework/fresh/pull/3820 | `denoland/fresh` | `code_only` | `typescript` | fix: type reconnectTimer as setTimeout return value |
| https://github.com/freshframework/fresh/pull/3706 | `denoland/fresh` | `code_only` | `typescript` | feat: support `deno create` for project initialization |
| https://github.com/freshframework/fresh/pull/3799 | `denoland/fresh` | `code_only` | `typescript` | chore: release 2.3.3 |
| https://github.com/freshframework/fresh/pull/3798 | `denoland/fresh` | `code_only` | `typescript` | revert: bring back Babel CJS transform |
| https://github.com/freshframework/fresh/pull/3745 | `denoland/fresh` | `code_only` | `typescript` | fix: change post_publish upload target to S3 |
| https://github.com/freshframework/fresh/pull/3796 | `denoland/fresh` | `code_only` | `typescript` | chore: release 2.3.2 |
| https://github.com/freshframework/fresh/pull/3793 | `denoland/fresh` | `code_only` | `typescript` | fix: CJS detection regression for packages with "export" in comments |
| https://github.com/freshframework/fresh/pull/3792 | `denoland/fresh` | `code_only` | `typescript` | chore: release 2.3.1 |
| https://github.com/freshframework/fresh/pull/3791 | `denoland/fresh` | `code_only` | `typescript` | ci: add dry-run publish check to PRs |
| https://github.com/freshframework/fresh/pull/3789 | `denoland/fresh` | `code_only` | `typescript` | chore: release @fresh/plugin-vite@1.1.0 and @fresh/plugin-tailwind-v3@1.1.0 |
| https://github.com/freshframework/fresh/pull/3776 | `denoland/fresh` | `code_only` | `typescript` | fix: keep ?fresh-partial an implementation detail |
| https://github.com/freshframework/fresh/pull/3767 | `denoland/fresh` | `code_only` | `typescript` | refactor: remove CJS and env var Babel transforms, let Vite handle natively |
| https://github.com/freshframework/fresh/pull/3780 | `denoland/fresh` | `code_only` | `typescript` | fix: update lockfile to unblock publish CI |
| https://github.com/freshframework/fresh/pull/3696 | `denoland/fresh` | `code_only` | `typescript` | feat:Actually ship no JS by default |
| https://github.com/elastic/apm-agent-nodejs/pull/5158 | `elastic/apm-agent-nodejs` | `code_only` | `typescript` | chore(deps): bump body-parser |
| https://github.com/elastic/apm-agent-nodejs/pull/5181 | `elastic/apm-agent-nodejs` | `code_only` | `typescript` | chore(deps): bump the github-actions group with 2 updates |
| https://github.com/elastic/apm-agent-nodejs/pull/5178 | `elastic/apm-agent-nodejs` | `code_only` | `typescript` | test: drop testing of apollo-server-core and apollo-server-express |
| https://github.com/elastic/apm-agent-nodejs/pull/5177 | `elastic/apm-agent-nodejs` | `code_and_docs` | `typescript` | test: drop azure functions v3 tests |
| https://github.com/elastic/apm-agent-nodejs/pull/5176 | `elastic/apm-agent-nodejs` | `code_only` | `typescript` | chore(deps): bump the github-actions group with 2 updates |
| https://github.com/elastic/apm-agent-nodejs/pull/5175 | `elastic/apm-agent-nodejs` | `code_only` | `typescript` | chore(deps-dev): bump js-yaml from 4.2.0 to 4.3.1 |
| https://github.com/elastic/apm-agent-nodejs/pull/5168 | `elastic/apm-agent-nodejs` | `code_only_tests_or_fixtures` | `typescript` | test: use awaitable apm.flush() in undici tests |
| https://github.com/elastic/apm-agent-nodejs/pull/5162 | `elastic/apm-agent-nodejs` | `code_only` | `typescript` | chore(deps-dev): bump find-my-way from 9.0.1 to 9.7.0 |
| https://github.com/elastic/apm-agent-nodejs/pull/5147 | `elastic/apm-agent-nodejs` | `code_only` | `typescript` | chore(deps-dev): bump @elastic/elasticsearch from 9.2.0 to 9.4.2 |
| https://github.com/elastic/apm-agent-nodejs/pull/5170 | `elastic/apm-agent-nodejs` | `code_only` | `typescript` | chore(deps-dev): bump brace-expansion from 1.1.13 to 1.1.18 |
| https://github.com/elastic/apm-agent-nodejs/pull/5169 | `elastic/apm-agent-nodejs` | `code_only` | `typescript` | chore(deps-dev): bump undici from 7.28.0 to 7.29.0 |
| https://github.com/elastic/apm-agent-nodejs/pull/5171 | `elastic/apm-agent-nodejs` | `code_only` | `typescript` | chore(deps-dev): bump fast-uri from 3.1.4 to 3.1.5 |
| https://github.com/elastic/apm-agent-nodejs/pull/5167 | `elastic/apm-agent-nodejs` | `code_only` | `typescript` | chore(deps): bump the github-actions group with 4 updates |
| https://github.com/elastic/apm-agent-nodejs/pull/5160 | `elastic/apm-agent-nodejs` | `code_only` | `typescript` | chore(deps): bump the github-actions group across 1 directory with 6 updates |
| https://github.com/elastic/apm-agent-nodejs/pull/5159 | `elastic/apm-agent-nodejs` | `code_only` | `typescript` | chore(deps-dev): bump fast-uri from 3.1.2 to 3.1.4 |
| https://github.com/elastic/apm-agent-nodejs/pull/5156 | `elastic/apm-agent-nodejs` | `code_only` | `typescript` | chore(deps-dev): bump axios from 1.16.0 to 1.18.1 |
| https://github.com/elastic/apm-agent-nodejs/pull/5150 | `elastic/apm-agent-nodejs` | `code_only` | `typescript` | chore(deps): bump the github-actions group with 2 updates |
| https://github.com/elastic/apm-agent-nodejs/pull/5126 | `elastic/apm-agent-nodejs` | `code_and_docs` | `typescript` | fix(opentelemetry-bridge): update to OTel SDK 2.x, fix `opentelemetryBridgeEnabled` to cover metrics integration |
| https://github.com/elastic/apm-agent-nodejs/pull/5137 | `elastic/apm-agent-nodejs` | `code_and_docs` | `typescript` | release 4.18.0 |
| https://github.com/elastic/apm-agent-nodejs/pull/5138 | `elastic/apm-agent-nodejs` | `code_only` | `typescript` | chore(deps): update OTel bridge API dep to @opentelemetry/api@v1.9.1 |
| https://github.com/elastic/elasticsearch-js/pull/3418 | `elastic/elasticsearch-js` | `code_only` | `typescript` | Auto-generated code for 9.4 |
| https://github.com/elastic/elasticsearch-js/pull/3417 | `elastic/elasticsearch-js` | `code_and_docs` | `typescript` | Auto-generated code for 9.5 |
| https://github.com/elastic/elasticsearch-js/pull/3416 | `elastic/elasticsearch-js` | `code_and_docs` | `typescript` | Auto-generated code for main |
| https://github.com/elastic/elasticsearch-js/pull/3413 | `elastic/elasticsearch-js` | `code_and_docs` | `typescript` | Auto-generated code for main |
| https://github.com/elastic/elasticsearch-js/pull/3415 | `elastic/elasticsearch-js` | `code_only` | `typescript` | Auto-generated code for 9.5 |
| https://github.com/elastic/elasticsearch-js/pull/3414 | `elastic/elasticsearch-js` | `code_only` | `typescript` | Auto-generated code for 9.3 |
| https://github.com/elastic/elasticsearch-js/pull/3412 | `elastic/elasticsearch-js` | `code_only` | `typescript` | Auto-generated code for 9.4 |
| https://github.com/elastic/elasticsearch-js/pull/3411 | `elastic/elasticsearch-js` | `code_only` | `typescript` | Auto-generated code for 8.19 |
| https://github.com/elastic/elasticsearch-js/pull/3399 | `elastic/elasticsearch-js` | `code_and_docs` | `typescript` | Auto-generated code for main |
| https://github.com/elastic/elasticsearch-js/pull/3397 | `elastic/elasticsearch-js` | `code_only` | `typescript` | Auto-generated code for 9.3 |
| https://github.com/elastic/elasticsearch-js/pull/3398 | `elastic/elasticsearch-js` | `code_only` | `typescript` | Auto-generated code for 9.4 |
| https://github.com/elastic/elasticsearch-js/pull/3396 | `elastic/elasticsearch-js` | `code_only` | `typescript` | chore(deps): update elastic/docs-actions digest to 3af947f |
| https://github.com/elastic/elasticsearch-js/pull/3395 | `elastic/elasticsearch-js` | `code_only` | `typescript` | chore(deps): update actions/checkout digest to 11d5960 |
| https://github.com/elastic/elasticsearch-js/pull/3400 | `elastic/elasticsearch-js` | `code_only` | `typescript` | Auto-generated code for 9.5 |
| https://github.com/elastic/elasticsearch-js/pull/3388 | `elastic/elasticsearch-js` | `code_only` | `typescript` | fix(ci): use VAULT_GITHUB_TOKEN in integration tests |
| https://github.com/elastic/elasticsearch-js/pull/3391 | `elastic/elasticsearch-js` | `code_only` | `typescript` | feat: expose maxPathLength client option |
| https://github.com/elastic/elasticsearch-js/pull/3389 | `elastic/elasticsearch-js` | `code_only` | `typescript` | feat: expose maxPathLength client option |
| https://github.com/elastic/elasticsearch-js/pull/3393 | `elastic/elasticsearch-js` | `code_and_docs` | `typescript` | chore: release 9.4.3 |
| https://github.com/elastic/elasticsearch-js/pull/3390 | `elastic/elasticsearch-js` | `code_only` | `typescript` | feat: expose maxPathLength client option |
| https://github.com/elastic/elasticsearch-js/pull/3380 | `elastic/elasticsearch-js` | `code_only` | `typescript` | feat: expose maxPathLength client option |
| https://github.com/elastic/kibana/pull/286574 | `elastic/kibana` | `code_only` | `typescript` | [Security Solution][Notes] Fix notes page not restoring filter UI state on return |
| https://github.com/elastic/kibana/pull/286428 | `elastic/kibana` | `code_only` | `typescript` | Update dependency chromedriver to v151.0.5 (main) |
| https://github.com/elastic/kibana/pull/286313 | `elastic/kibana` | `code_only` | `typescript` | [Entity Store] Fix consumers that only query the renamed neutral index names |
| https://github.com/elastic/kibana/pull/286685 | `elastic/kibana` | `code_only_tests_or_fixtures` | `typescript` | [Scout] Update test config manifests |
| https://github.com/elastic/kibana/pull/286644 | `elastic/kibana` | `code_and_docs` | `typescript` | [Notification Center] Remove the severity filter from the list route |
| https://github.com/elastic/kibana/pull/285263 | `elastic/kibana` | `code_only` | `typescript` | [Alerting V2] make the breach block optional in composed queries |
| https://github.com/elastic/kibana/pull/285748 | `elastic/kibana` | `code_only_tests_or_fixtures` | `typescript` | [Maps] Wait for join where popover to be visible before typing |
| https://github.com/elastic/kibana/pull/282710 | `elastic/kibana` | `code_only_tests_or_fixtures` | `typescript` | [Dashboard] Fix flaky links panel navigation test with fresh listing navigation |
| https://github.com/elastic/kibana/pull/284861 | `elastic/kibana` | `code_only_tests_or_fixtures` | `typescript` | [Lens] Stabilize include/exclude combobox Jest test timing |
| https://github.com/elastic/kibana/pull/286648 | `elastic/kibana` | `code_only` | `typescript` | [CPS] Remove outdated ML CPS banners |
| https://github.com/elastic/kibana/pull/286572 | `elastic/kibana` | `code_only_tests_or_fixtures` | `typescript` | [Discover][Metrics] Fix flaky share_session scout step |
| https://github.com/elastic/kibana/pull/286675 | `elastic/kibana` | `code_only_tests_or_fixtures` | `typescript` | [9.4] [Discover][Metrics] Fix flaky share_session scout step (#286572) |
| https://github.com/elastic/kibana/pull/282897 | `elastic/kibana` | `code_only_tests_or_fixtures` | `typescript` | [Dashboard] Read markdown editor value attribute to fix flaky read |
| https://github.com/elastic/kibana/pull/236992 | `elastic/kibana` | `code_only` | `typescript` | [Telemetry] Add CSPM Cloud Connector Usage Statistics Collection |
| https://github.com/elastic/kibana/pull/237893 | `elastic/kibana` | `code_only` | `typescript` | Update @elastic/appex-qa dependencies (main) |
| https://github.com/elastic/kibana/pull/244543 | `elastic/kibana` | `code_only` | `typescript` | [Cases] Fix stale submitting |
| https://github.com/elastic/kibana/pull/262509 | `elastic/kibana` | `code_only` | `typescript` | [Fleet] only auto-install content packages newer than the installed version |
| https://github.com/elastic/kibana/pull/272633 | `elastic/kibana` | `code_only` | `typescript` | [One Workflow] Fix workflow connector v2 menu labels and icons |
| https://github.com/elastic/kibana/pull/274388 | `elastic/kibana` | `code_only_tests_or_fixtures` | `typescript` | [Home] Fix flaky sample data API test cross-test state leak |
| https://github.com/elastic/kibana/pull/239659 | `elastic/kibana` | `code_only` | `typescript` | Update dependency liquidjs to ^10.21.1 (main) |
| https://github.com/electron/electron/pull/52089 | `electron/electron` | `code_only` | `typescript` | fix: update document title on back or forward navigation |
| https://github.com/electron/electron/pull/53031 | `electron/electron` | `code_only` | `typescript` | fix: set bounds on detached `WebContentsView` |
| https://github.com/electron/electron/pull/53109 | `electron/electron` | `code_only` | `typescript` | fix: avoid creating webFrameMain for transient frames |
| https://github.com/electron/electron/pull/53102 | `electron/electron` | `code_only` | `typescript` | fix: avoid creating webFrameMain for transient frames |
| https://github.com/electron/electron/pull/53099 | `electron/electron` | `code_only` | `typescript` | fix: update document title on back or forward navigation |
| https://github.com/electron/electron/pull/53107 | `electron/electron` | `code_only` | `typescript` | perf: trim GTK and FontConfig work off the linux startup path |
| https://github.com/electron/electron/pull/53070 | `electron/electron` | `code_only` | `typescript` | perf: trim GTK and FontConfig work off the linux startup path |
| https://github.com/electron/electron/pull/53108 | `electron/electron` | `code_only` | `typescript` | perf: trim GTK and FontConfig work off the linux startup path |
| https://github.com/electron/electron/pull/53111 | `electron/electron` | `code_and_docs` | `typescript` | build: skip linux-arm in PGO profile generation |
| https://github.com/electron/electron/pull/53112 | `electron/electron` | `code_and_docs` | `typescript` | build: skip linux-arm in PGO profile generation |
| https://github.com/electron/electron/pull/52964 | `electron/electron` | `code_only` | `typescript` | fix: illegal access errors when a same-process child window or subframe closes |
| https://github.com/electron/electron/pull/53042 | `electron/electron` | `code_only` | `typescript` | fix: illegal access errors when a same-process child window or subframe closes |
| https://github.com/electron/electron/pull/53088 | `electron/electron` | `code_only` | `typescript` | chore: remove fix_harden_blink_scriptstate_maybefrom.patch |
| https://github.com/electron/electron/pull/53057 | `electron/electron` | `code_only` | `typescript` | refactor: enable modernize-use-nullptr clang-tidy check |
| https://github.com/electron/electron/pull/53104 | `electron/electron` | `code_only` | `typescript` | refactor: enable modernize-use-nullptr clang-tidy check |
| https://github.com/electron/electron/pull/53105 | `electron/electron` | `code_only` | `typescript` | refactor: enable modernize-use-nullptr clang-tidy check |
| https://github.com/electron/electron/pull/53090 | `electron/electron` | `code_only` | `typescript` | ci: remove linker wrapper workaround on windows |
| https://github.com/electron/electron/pull/53067 | `electron/electron` | `code_only` | `typescript` | ci: remove linker wrapper workaround on windows |
| https://github.com/electron/electron/pull/53089 | `electron/electron` | `code_only` | `typescript` | ci: remove linker wrapper workaround on windows |
| https://github.com/electron/electron/pull/53032 | `electron/electron` | `code_only` | `typescript` | build: enable Clang Static Analyzer clang-tidy checks |
| https://github.com/eslint/eslint/pull/21243 | `eslint/eslint` | `code_only` | `typescript` | chore: update github/codeql-action action to v4.37.7 |
| https://github.com/eslint/eslint/pull/21218 | `eslint/eslint` | `code_only` | `typescript` | feat: handle underflow in no-loss-of-precision |
| https://github.com/eslint/eslint/pull/21216 | `eslint/eslint` | `code_and_docs` | `typescript` | docs: use eslint.config.* wherever config file names are listed |
| https://github.com/eslint/eslint/pull/21235 | `eslint/eslint` | `code_only_tests_or_fixtures` | `typescript` | chore: update ecosystem plugins |
| https://github.com/eslint/eslint/pull/21213 | `eslint/eslint` | `code_only` | `typescript` | fix: prevent unsafe `no-var` autofix with hoisted functions |
| https://github.com/eslint/eslint/pull/21208 | `eslint/eslint` | `code_only_tests_or_fixtures` | `typescript` | chore: update ecosystem plugins |
| https://github.com/eslint/eslint/pull/21204 | `eslint/eslint` | `code_only` | `typescript` | fix: Prevent no-var autofix when var is shadowed by catch parameter |
| https://github.com/eslint/eslint/pull/21207 | `eslint/eslint` | `code_only` | `typescript` | fix: prefer-template invalid autofix creates a tagged template call |
| https://github.com/eslint/eslint/pull/21175 | `eslint/eslint` | `code_and_docs` | `typescript` | feat: add checkConditionalExpressions to `no-unmodified-loop-condition` |
| https://github.com/eslint/eslint/pull/21173 | `eslint/eslint` | `code_only` | `typescript` | fix: prevent ASI hazard in `no-unused-labels` autofix |
| https://github.com/eslint/eslint/pull/21163 | `eslint/eslint` | `code_only` | `typescript` | fix: false positives in `getter-return` and `accessor-pairs` |
| https://github.com/eslint/eslint/pull/21198 | `eslint/eslint` | `code_and_docs` | `typescript` | docs: update moved JSX specification links |
| https://github.com/eslint/eslint/pull/21200 | `eslint/eslint` | `code_only` | `typescript` | ci: bump pnpm/action-setup from 6.0.9 to 6.0.10 |
| https://github.com/eslint/eslint/pull/21199 | `eslint/eslint` | `code_only` | `typescript` | ci: bump github/codeql-action from 4.37.4 to 4.37.6 |
| https://github.com/eslint/eslint/pull/21196 | `eslint/eslint` | `code_only` | `typescript` | chore: update github/codeql-action action to v4.37.4 |
| https://github.com/eslint/eslint/pull/21077 | `eslint/eslint` | `code_only` | `typescript` | chore: update `@eslint/eslintrc` and `@eslint/js` for v9.39.5 |
| https://github.com/eslint/eslint/pull/21191 | `eslint/eslint` | `code_only_tests_or_fixtures` | `typescript` | test: fix failing ecosystem test for `eslint-plugin-unicorn` |
| https://github.com/eslint/eslint/pull/21185 | `eslint/eslint` | `code_only_tests_or_fixtures` | `typescript` | test: add error locations info to `no-void` |
| https://github.com/eslint/eslint/pull/21176 | `eslint/eslint` | `code_only` | `typescript` | ci: bump github/codeql-action from 4 to 4.37.3 |
| https://github.com/eslint/eslint/pull/20937 | `eslint/eslint` | `code_only_tests_or_fixtures` | `typescript` | chore: improve ecosystem test failure reporting |
| https://github.com/expo/expo/pull/49215 | `expo/expo` | `code_and_docs` | `typescript` | [android][expo-ui] Forward `BottomSheet` dialog key events to the activity |
| https://github.com/expo/expo/pull/49161 | `expo/expo` | `code_and_docs` | `typescript` | chore: Update to `@expo/metro@~56.0.2` (metro@0.84.5) |
| https://github.com/expo/expo/pull/48826 | `expo/expo` | `code_and_docs` | `typescript` | fix(require-utils): Fix Node 26 `stripTypeScriptTypes` fallback call |
| https://github.com/expo/expo/pull/48127 | `expo/expo` | `code_and_docs` | `typescript` | [cli] Fix wireless iOS <= 16 devices missing from run:ios device list |
| https://github.com/expo/expo/pull/48589 | `expo/expo` | `code_and_docs` | `typescript` | [ios][widgets] Expose Live Activity IDs and restore token observation |
| https://github.com/expo/expo/pull/49130 | `expo/expo` | `code_and_docs` | `typescript` | [android][updates] Register the embedded update in a single transaction |
| https://github.com/expo/expo/pull/49211 | `expo/expo` | `code_and_docs` | `typescript` | [ui][ios] Yoga node holding old styles after props style update |
| https://github.com/expo/expo/pull/49195 | `expo/expo` | `code_and_docs` | `typescript` | [module-scripts] Remove the dangling `build-src` command |
| https://github.com/expo/expo/pull/48691 | `expo/expo` | `code_and_docs` | `typescript` | chore: replace deprecated Worklets APIs in Expo Modules Core |
| https://github.com/expo/expo/pull/49172 | `expo/expo` | `code_and_docs` | `typescript` | [router] Remove NavigationIndependentTree |
| https://github.com/expo/expo/pull/49196 | `expo/expo` | `code_and_docs` | `typescript` | [web][crypto] Respect the bounds of typed-array views in the AES module |
| https://github.com/expo/expo/pull/46223 | `expo/expo` | `code_and_docs` | `typescript` | [cli] Fix ESLint not found on first lint run |
| https://github.com/expo/expo/pull/49150 | `expo/expo` | `code_and_docs` | `typescript` | [ios][autolinking] Add derivations snapshot dump for precompiled modules [step 0] |
| https://github.com/expo/expo/pull/46225 | `expo/expo` | `code_and_docs` | `typescript` | [cli] Support TypeScript ESLint config files |
| https://github.com/expo/expo/pull/48059 | `expo/expo` | `code_and_docs` | `typescript` | [expo-modules-core][iOS] Cap synchronous Host size commits per run-loop turn to prevent an infinite SwiftUI/Yoga layout loop |
| https://github.com/expo/expo/pull/49146 | `expo/expo` | `code_and_docs` | `typescript` | [ios][secure-store] Reject `deleteItemAsync` when the keychain delete fails |
| https://github.com/expo/expo/pull/48957 | `expo/expo` | `code_and_docs` | `typescript` | [expo-video][android] Guard setAutoEnterEnabled against NoSuchMethodError on non-conformant firmwares |
| https://github.com/expo/expo/pull/49201 | `expo/expo` | `code_only` | `typescript` | [router] Remove deprecated InteractionManager usage |
| https://github.com/expo/expo/pull/49200 | `expo/expo` | `code_only` | `typescript` | [router] Remove RootModalContext |
| https://github.com/expo/expo/pull/48735 | `expo/expo` | `code_and_docs` | `typescript` | [ios][ui] Fix empty RNHostView taking up space in SwiftUI containers |
| https://github.com/facebook/docusaurus/pull/12380 | `facebook/docusaurus` | `code_only` | `typescript` | fix: upgrade rspack, fix i18n leak, reduce CI max memory |
| https://github.com/facebook/docusaurus/pull/12373 | `facebook/docusaurus` | `code_only` | `typescript` | chore(deps): bump github/codeql-action/analyze from 4.37.6 to 4.37.7 |
| https://github.com/facebook/docusaurus/pull/12375 | `facebook/docusaurus` | `code_only` | `typescript` | chore(deps): bump github/codeql-action/init from 4.37.6 to 4.37.7 |
| https://github.com/facebook/docusaurus/pull/12374 | `facebook/docusaurus` | `code_only` | `typescript` | chore(deps-dev): bump @types/lodash from 4.17.24 to 4.17.25 |
| https://github.com/facebook/docusaurus/pull/12377 | `facebook/docusaurus` | `code_only` | `typescript` | chore(deps): bump browserslist from 4.28.2 to 4.28.8 |
| https://github.com/facebook/docusaurus/pull/12326 | `facebook/docusaurus` | `code_only` | `typescript` | fix: memory leak in Link due to IntersectionObserver |
| https://github.com/facebook/docusaurus/pull/12372 | `facebook/docusaurus` | `code_only` | `typescript` | fix(ci): skip CI workflows that fail from forks |
| https://github.com/facebook/docusaurus/pull/12308 | `facebook/docusaurus` | `code_only` | `typescript` | fix(utils): correct auto-generated description when H1 heading text contains # (e.g. C#) |
| https://github.com/facebook/docusaurus/pull/12335 | `facebook/docusaurus` | `code_only` | `typescript` | fix(utils): allow MDX to detect title when a component is exported before h1 |
| https://github.com/facebook/docusaurus/pull/12370 | `facebook/docusaurus` | `code_only` | `typescript` | feat(theme-translations): add Azerbaijani (az) default theme translations |
| https://github.com/facebook/docusaurus/pull/12369 | `facebook/docusaurus` | `code_only` | `typescript` | fix(minifier): Keep attribute quotes in the SWC HTML minifier |
| https://github.com/facebook/docusaurus/pull/12342 | `facebook/docusaurus` | `code_only` | `typescript` | chore(deps): bump postcss from 8.5.25 to 8.5.26 |
| https://github.com/facebook/docusaurus/pull/12344 | `facebook/docusaurus` | `code_only` | `typescript` | chore(deps): bump js-yaml from 4.2.0 to 4.3.1 |
| https://github.com/facebook/docusaurus/pull/12329 | `facebook/docusaurus` | `code_only` | `typescript` | fix(utils): resolve site-relative paths in the eager Git VCS |
| https://github.com/facebook/docusaurus/pull/12347 | `facebook/docusaurus` | `code_only` | `typescript` | chore(deps): bump pnpm/action-setup from 6.0.9 to 6.0.10 |
| https://github.com/facebook/docusaurus/pull/12346 | `facebook/docusaurus` | `code_only` | `typescript` | chore(deps): bump github/codeql-action/analyze from 4.37.1 to 4.37.6 |
| https://github.com/facebook/docusaurus/pull/12349 | `facebook/docusaurus` | `code_only` | `typescript` | chore(deps): bump github/codeql-action/init from 4.37.1 to 4.37.6 |
| https://github.com/facebook/docusaurus/pull/12350 | `facebook/docusaurus` | `code_only` | `typescript` | chore(deps): bump postcss from 8.5.18 to 8.5.25 |
| https://github.com/facebook/docusaurus/pull/12260 | `facebook/docusaurus` | `code_only` | `typescript` | fix(core): fix BaseUrlIssueBanner little security issue |
| https://github.com/facebook/docusaurus/pull/12238 | `facebook/docusaurus` | `code_only` | `typescript` | fix(core): accept boolean attributes in headTags config validation  |
| https://github.com/jestjs/jest/pull/16390 | `facebook/jest` | `code_and_docs` | `typescript` | fix(jest-resolve): apply `moduleNameMapper` to both spellings of core modules |
| https://github.com/jestjs/jest/pull/16381 | `facebook/jest` | `code_and_docs` | `typescript` | fix(jest-util): honor picomatch options when a glob is already cached |
| https://github.com/jestjs/jest/pull/16389 | `facebook/jest` | `code_and_docs` | `typescript` | fix(jest-runtime): close ESM mocking, require(esm) and JSON module parity gaps |
| https://github.com/jestjs/jest/pull/16386 | `facebook/jest` | `code_and_docs` | `typescript` | perf(jest-haste-map): cache the watchman socket path and drop the version probe |
| https://github.com/jestjs/jest/pull/16388 | `facebook/jest` | `code_and_docs` | `typescript` | fix(jest-resolve): keep the `node:` prefix through async resolution |
| https://github.com/jestjs/jest/pull/16387 | `facebook/jest` | `code_and_docs` | `typescript` | perf(jest-snapshot): load babel, semver and synckit lazily |
| https://github.com/jestjs/jest/pull/16373 | `facebook/jest` | `code_and_docs` | `typescript` | perf(jest-resolve): make the warm default-resolver path about 3x cheaper |
| https://github.com/jestjs/jest/pull/16385 | `facebook/jest` | `code_and_docs` | `typescript` | refactor(jest-runtime): remove dead accessors and collapse duplicated module-loading shapes |
| https://github.com/jestjs/jest/pull/16379 | `facebook/jest` | `code_and_docs` | `typescript` | fix(jest-core): do not report CustomGC as an open handle |
| https://github.com/jestjs/jest/pull/16377 | `facebook/jest` | `code_and_docs` | `typescript` | fix(jest-runtime): bind `sandboxInjectedGlobals` to the right values |
| https://github.com/jestjs/jest/pull/16260 | `facebook/jest` | `code_and_docs` | `typescript` | feat(jest-resolve): honor `--preserve-symlinks` / `NODE_PRESERVE_SYMLINKS` in the default resolver |
| https://github.com/jestjs/jest/pull/16376 | `facebook/jest` | `code_and_docs` | `typescript` | perf(jest-runtime): cut per-require and per-specifier overhead |
| https://github.com/jestjs/jest/pull/16155 | `facebook/jest` | `code_and_docs` | `typescript` | fix(jest-console): buffer console output in CustomConsole for reporters |
| https://github.com/jestjs/jest/pull/16375 | `facebook/jest` | `code_and_docs` | `typescript` | fix(jest-runtime): key ES modules by full URL and share modules between overlapping graphs |
| https://github.com/jestjs/jest/pull/16371 | `facebook/jest` | `code_and_docs` | `typescript` | perf(jest-resolve): cut repeated work on the resolution hot path |
| https://github.com/jestjs/jest/pull/16370 | `facebook/jest` | `code_and_docs` | `typescript` | fix(jest-resolve): build and cache `data:` URI module IDs the same way sync and async |
| https://github.com/jestjs/jest/pull/16369 | `facebook/jest` | `code_and_docs` | `typescript` | fix(jest-resolve): repair the `shouldLoadAsEsm` lookup caches |
| https://github.com/jestjs/jest/pull/16367 | `facebook/jest` | `code_and_docs` | `typescript` | fix(jest-runtime): mirror Node's ESM/CJS interop and entry-point metadata |
| https://github.com/jestjs/jest/pull/16366 | `facebook/jest` | `code_and_docs` | `typescript` | fix(jest-runtime): throw ERR_REQUIRE_CYCLE_MODULE on require(esm) re-entry |
| https://github.com/jestjs/jest/pull/16364 | `facebook/jest` | `code_and_docs` | `typescript` | fix(jest-runtime): gate ESM registry reuse on module status |
| https://github.com/react/react/pull/37342 | `facebook/react` | `code_only` | `typescript` | [Flight] Abort the cache signal when debug objects are retained |
| https://github.com/react/react/pull/37315 | `facebook/react` | `code_only` | `typescript` | [Flight/Fizz] Stop the caller's signal from retaining a finished render |
| https://github.com/react/react/pull/37087 | `facebook/react` | `code_only` | `typescript` | [FlightReply] Performance improvements when decoding |
| https://github.com/react/react/pull/36425 | `facebook/react` | `code_only` | `typescript` | [FlightReply] Type hardening and performance improvements |
| https://github.com/react/react/pull/35623 | `facebook/react` | `code_only` | `typescript` | Fix typo: accomodate -> accommodate |
| https://github.com/react/react/pull/37326 | `facebook/react` | `code_only` | `typescript` | [Fiber] Detach Fragment refs during the mutation phase |
| https://github.com/react/react/pull/37290 | `facebook/react` | `code_only` | `typescript` | [flags] Enable enableParallelTransitions |
| https://github.com/react/react/pull/37169 | `facebook/react` | `code_only` | `typescript` | [DOM] Scope Fragment once listeners to the fragment, not each child |
| https://github.com/react/react/pull/37168 | `facebook/react` | `code_only` | `typescript` | [Fiber] Run Fragment deletion effects for HostText children |
| https://github.com/react/react/pull/37167 | `facebook/react` | `code_only` | `typescript` | [Fiber] Extract Fragment instance commit helpers into their own module |
| https://github.com/react/react/pull/37166 | `facebook/react` | `code_only` | `typescript` | [DOM] Apply Fragment listeners to children inserted into portals later |
| https://github.com/react/react/pull/37165 | `facebook/react` | `code_only` | `typescript` | [DOM] Fix Fragment dispatchEvent when the container is a Document |
| https://github.com/react/react/pull/37164 | `facebook/react` | `code_only` | `typescript` | [DOM] Attach Fragment event listeners to committed text children |
| https://github.com/react/react/pull/37163 | `facebook/react` | `code_only` | `typescript` | [DOM] Fix Fragment compareDocumentPosition for documentElement and empty portals |
| https://github.com/react/react/pull/37162 | `facebook/react` | `code_only` | `typescript` | [DOM] Find host siblings for nested empty Fragments |
| https://github.com/react/react/pull/37161 | `facebook/react` | `code_only` | `typescript` | [DOM] Blur portaled Fragment focus targets |
| https://github.com/react/react/pull/37160 | `facebook/react` | `code_only` | `typescript` | [DOM] Fix Fragment removeEventListener dropping tracked listeners |
| https://github.com/react/react/pull/34983 | `facebook/react` | `code_only` | `typescript` | [Fiber] Prevent metadata hoisting in hidden `<Activity>` trees |
| https://github.com/react/react/pull/37171 | `facebook/react` | `code_only` | `typescript` | [DOM] Drop empty Fragment scrollIntoView no-op warning |
| https://github.com/react/react/pull/37241 | `facebook/react` | `code_only` | `typescript` | Add lazy reasons to browser() |
| https://github.com/react/react-native/pull/58058 | `facebook/react-native` | `code_only` | `typescript` | [0.87] Use macOS 26 runners for iOS E2E tests |
| https://github.com/react/react-native/pull/58057 | `facebook/react-native` | `code_only` | `typescript` | [0.86] Use macOS 26 runners for iOS E2E tests |
| https://github.com/grafana/grafana/pull/131321 | `grafana/grafana` | `code_only` | `typescript` | I18n: Download translations from Crowdin |
| https://github.com/grafana/grafana/pull/128190 | `grafana/grafana` | `code_and_docs` | `typescript` | Docs: Clarify that experimental feature toggles aren't listed |
| https://github.com/grafana/grafana/pull/131278 | `grafana/grafana` | `code_only` | `typescript` | OFREP: Serve deprecated /apis/features.grafana.app path on standalone mux |
| https://github.com/grafana/grafana/pull/130014 | `grafana/grafana` | `code_only` | `typescript` | AuthZ: Make iam permissions delegation checks action-aware |
| https://github.com/grafana/grafana/pull/131276 | `grafana/grafana` | `code_only` | `typescript` | CodeMirror: Replace dashboard export viewer |
| https://github.com/grafana/grafana/pull/131300 | `grafana/grafana` | `code_only` | `typescript` | DateTime: Truncate fractional milliseconds in Luxon compat shim |
| https://github.com/grafana/grafana/pull/130452 | `grafana/grafana` | `code_only` | `typescript` | Table: fix JSON cell indentation, styling, and hover reveal |
| https://github.com/grafana/grafana/pull/131308 | `grafana/grafana` | `code_only` | `typescript` | Dashboards: Fix flaky datasource variable E2E test by awaiting async type options |
| https://github.com/grafana/grafana/pull/131039 | `grafana/grafana` | `code_only_tests_or_fixtures` | `typescript` | DataViz: test gardening 🧑‍🌾 — Sparkline render tests in grafana-ui Sparkline.test.tsx |
| https://github.com/grafana/grafana/pull/131081 | `grafana/grafana` | `code_only` | `typescript` | Chore: Lazy-load moment |
| https://github.com/grafana/grafana/pull/131193 | `grafana/grafana` | `code_only_tests_or_fixtures` | `typescript` | Stat: Fix E2E flake from page-wide panel locators |
| https://github.com/grafana/grafana/pull/130179 | `grafana/grafana` | `code_only` | `typescript` | FeatureControl: Show by default with a notice when preview assets are active |
| https://github.com/grafana/grafana/pull/131145 | `grafana/grafana` | `code_only` | `typescript` | Explore: Fix split double spacing  |
| https://github.com/grafana/grafana/pull/131195 | `grafana/grafana` | `code_only` | `typescript` | Frontend: Resolve build-directory assets through a window global |
| https://github.com/grafana/grafana/pull/131218 | `grafana/grafana` | `code_only` | `typescript` | Provisioning: Add repository operation metrics (size, duration, outcome) |
| https://github.com/grafana/grafana/pull/128116 | `grafana/grafana` | `code_only` | `typescript` | Correct annotation permission delegation |
| https://github.com/grafana/grafana/pull/129037 | `grafana/grafana` | `code_only` | `typescript` | Provisioning: Add link back to the original dashboard in preview banner |
| https://github.com/grafana/grafana/pull/131252 | `grafana/grafana` | `code_only` | `typescript` | Search: stop sending QueryField.type from in-tree clients |
| https://github.com/grafana/grafana/pull/129426 | `grafana/grafana` | `code_only` | `typescript` | Table: Fix nested apply-to-row coloring to use the nested frame's own fields |
| https://github.com/grafana/grafana/pull/131261 | `grafana/grafana` | `code_only` | `typescript` | Chore: disable nx analytics |
| https://github.com/grafana/k6/pull/6277 | `grafana/k6` | `code_only` | `typescript` | ci: automate the second approval for Renovate PRs |
| https://github.com/grafana/k6/pull/5949 | `grafana/k6` | `code_only` | `typescript` | fix(output/influxdb): support URL path prefixes in --out influxdb= |
| https://github.com/grafana/k6/pull/6279 | `grafana/k6` | `code_only` | `typescript` | Fix frozen pages on shared browser connections |
| https://github.com/grafana/k6/pull/6298 | `grafana/k6` | `code_only` | `typescript` | Shut down TracerProvider after the Exit event is handled |
| https://github.com/grafana/k6/pull/6209 | `grafana/k6` | `code_only` | `typescript` | refactor(cmd): decouple cloud subcommands from the parent cmdCloud |
| https://github.com/grafana/k6/pull/5794 | `grafana/k6` | `code_only` | `typescript` | fix: return error when --vus is used with scenarios (fixes #5793) |
| https://github.com/grafana/k6/pull/6236 | `grafana/k6` | `code_only` | `typescript` | Introduce a smoke test of the browser image in build workflow |
| https://github.com/grafana/k6/pull/6265 | `grafana/k6` | `code_only` | `typescript` | fix(deps): update golangx (master) |
| https://github.com/grafana/k6/pull/5971 | `grafana/k6` | `code_only` | `typescript` | Preserve module source on API errors |
| https://github.com/grafana/k6/pull/6238 | `grafana/k6` | `code_only` | `typescript` | Fix urlencoded form bodies encoding null as <nil> and objects as map[...] |
| https://github.com/grafana/k6/pull/6285 | `grafana/k6` | `code_only` | `typescript` | ci: backport GitHub Actions maintenance to v1.x |
| https://github.com/grafana/k6/pull/6282 | `grafana/k6` | `code_only` | `typescript` | Update k6 version to 1.8.1 |
| https://github.com/grafana/k6/pull/6220 | `grafana/k6` | `code_only` | `typescript` | fix(security/unknown/): update module github.com/klauspost/compress to v1.18.7 [security] (v1.x) |
| https://github.com/grafana/k6/pull/6193 | `grafana/k6` | `code_only` | `typescript` | fix(security/high/): update module google.golang.org/grpc to v1.82.1 [security] (v1.x) |
| https://github.com/grafana/k6/pull/6188 | `grafana/k6` | `code_only` | `typescript` | fix(security/unknown/): update module golang.org/x/text to v0.39.0 [security] (v1.x) |
| https://github.com/grafana/k6/pull/6187 | `grafana/k6` | `code_only` | `typescript` | fix(security/unknown/): update module golang.org/x/net to v0.56.0 [security] (v1.x) |
| https://github.com/grafana/k6/pull/6139 | `grafana/k6` | `code_only_tests_or_fixtures` | `typescript` | ci: force legacy x/net/http2 implementation on the gotip test job (backport to v1.x) |
| https://github.com/grafana/k6/pull/6235 | `grafana/k6` | `code_only` | `typescript` | fix(browser): use filepath.ToSlash for URL paths in file persister |
| https://github.com/grafana/k6/pull/6274 | `grafana/k6` | `code_only` | `typescript` | Stop enabling the cloud secret source by default |
| https://github.com/grafana/k6/pull/6275 | `grafana/k6` | `code_only` | `typescript` | Backport #6234: fix HTTP/2 error handling on Go 1.27 |
| https://github.com/microsoft/vscode/pull/331971 | `microsoft/vscode` | `code_only` | `typescript` | Hide the Changes pill for folderless chat sessions |
| https://github.com/microsoft/vscode/pull/331939 | `microsoft/vscode` | `code_and_docs` | `typescript` | sessions: disable unsupported editor splits |
| https://github.com/microsoft/vscode/pull/331945 | `microsoft/vscode` | `code_only` | `typescript` | sessions: streamline editor title actions |
| https://github.com/microsoft/vscode/pull/332036 | `microsoft/vscode` | `code_and_docs` | `typescript` | Adopt a sealed Agent Host service graph |
| https://github.com/microsoft/vscode/pull/332080 | `microsoft/vscode` | `code_only` | `typescript` | agentHost: don't report a session as missing while its catalog migration is in flight |
| https://github.com/microsoft/vscode/pull/332068 | `microsoft/vscode` | `code_only` | `typescript` | Fix hover on command status bar items |
| https://github.com/microsoft/vscode/pull/332062 | `microsoft/vscode` | `code_only` | `typescript` | Agent Host: Make debug log export best-effort |
| https://github.com/microsoft/vscode/pull/332058 | `microsoft/vscode` | `code_only` | `typescript` | Browser: never show query parameters in tab descriptions |
| https://github.com/microsoft/vscode/pull/332045 | `microsoft/vscode` | `code_only` | `typescript` | Add Agent Host hung turn lifecycle diagnostics |
| https://github.com/microsoft/vscode/pull/332059 | `microsoft/vscode` | `code_only` | `typescript` | chat: preserve conversation ID for BYOK Responses |
| https://github.com/microsoft/vscode/pull/332064 | `microsoft/vscode` | `code_only_tests_or_fixtures` | `typescript` | Disable Kerberos proxy smoke test on GitHub Actions |
| https://github.com/microsoft/vscode/pull/323154 | `microsoft/vscode` | `code_only` | `typescript` | fix: handle failed terminal quick fix model request to avoid unhandled rejection (fixes #323149) |
| https://github.com/microsoft/vscode/pull/332003 | `microsoft/vscode` | `code_only` | `typescript` | Agent Merge: recover from a checks fragment the host refuses |
| https://github.com/microsoft/vscode/pull/323663 | `microsoft/vscode` | `code_only` | `typescript` | fix: make sure register handler when ipc emitter add listener |
| https://github.com/microsoft/vscode/pull/323943 | `microsoft/vscode` | `code_only` | `typescript` | Fix multiple askQuestions in Agent Host |
| https://github.com/microsoft/vscode/pull/323940 | `microsoft/vscode` | `code_only` | `typescript` | build(deps-dev): bump tar from 7.5.11 to 7.5.19 in /build/npm/gyp |
| https://github.com/microsoft/vscode/pull/324595 | `microsoft/vscode` | `code_only` | `typescript` | Include request UUID in completion feedback (fix empty telemetry section) |
| https://github.com/microsoft/vscode/pull/324586 | `microsoft/vscode` | `code_only` | `typescript` | Only show completion feedback command for paid users |
| https://github.com/microsoft/vscode/pull/324571 | `microsoft/vscode` | `code_only` | `typescript` | Fix second Rerun Last Task failing to launch for reevaluateOnRerun tasks |
| https://github.com/microsoft/vscode/pull/324523 | `microsoft/vscode` | `code_only` | `typescript` | Use startColumn in growUntilVariableBoundaries |
| https://github.com/mui/material-ui/pull/48944 | `mui/material-ui` | `code_and_docs` | `typescript` | [docs] Move focus to the main content with the skip link |
| https://github.com/mui/material-ui/pull/48937 | `mui/material-ui` | `code_and_docs` | `typescript` | Bump MUI X |
| https://github.com/mui/material-ui/pull/48942 | `mui/material-ui` | `code_only` | `typescript` | [docs] Manage focus on Open in Chat button click |
| https://github.com/mui/material-ui/pull/48707 | `mui/material-ui` | `code_only` | `typescript` | [menulist] Preserve custom list padding when adjusting for the scrollbar |
| https://github.com/mui/material-ui/pull/48896 | `mui/material-ui` | `code_only` | `typescript` | Bump node |
| https://github.com/mui/material-ui/pull/48622 | `mui/material-ui` | `code_only` | `typescript` | [tooltip] Improve support for disabled button triggers |
| https://github.com/mui/material-ui/pull/48899 | `mui/material-ui` | `code_and_docs` | `typescript` | Bump playwright monorepo |
| https://github.com/mui/material-ui/pull/48877 | `mui/material-ui` | `code_and_docs` | `typescript` | [pagination] Manage focus whenever first / last / next / previous buttons become disabled |
| https://github.com/mui/material-ui/pull/48892 | `mui/material-ui` | `code_and_docs` | `typescript` | Bump code-infra:patchUpdates |
| https://github.com/mui/material-ui/pull/48935 | `mui/material-ui` | `code_and_docs` | `typescript` | [release] v9.3.1 |
| https://github.com/mui/material-ui/pull/48934 | `mui/material-ui` | `code_only` | `typescript` | [codemod] Include transforms in published package |
| https://github.com/mui/material-ui/pull/48881 | `mui/material-ui` | `code_only` | `typescript` | [transitions] Prevent exit transitions from getting stuck |
| https://github.com/mui/material-ui/pull/48927 | `mui/material-ui` | `code_only_tests_or_fixtures` | `typescript` | [test][pagination] Add more unit tests |
| https://github.com/mui/material-ui/pull/48909 | `mui/material-ui` | `code_and_docs` | `typescript` | v9.3.0 |
| https://github.com/mui/material-ui/pull/48871 | `mui/material-ui` | `code_only` | `typescript` | [tablepagination] Add focus style to default InputBase used in Select |
| https://github.com/mui/material-ui/pull/48572 | `mui/material-ui` | `code_only` | `typescript` | [autocomplete] Fix item removal when it receives focus from VoiceOver before using Backspace |
| https://github.com/mui/material-ui/pull/48895 | `mui/material-ui` | `code_and_docs` | `typescript` | Bump nextjs monorepo to 16.2.12 |
| https://github.com/mui/material-ui/pull/48863 | `mui/material-ui` | `code_and_docs` | `typescript` | Bump react-router to ^8.3.0 |
| https://github.com/mui/material-ui/pull/48912 | `mui/material-ui` | `code_only` | `typescript` | Bump postcss to ^8.5.22 [SECURITY] |
| https://github.com/mui/material-ui/pull/48902 | `mui/material-ui` | `code_only` | `typescript` | Bump chalk to 6.0.0 |
| https://github.com/nestjs/docs.nestjs.com/pull/3426 | `nestjs/docs.nestjs.com` | `code_only` | `typescript` | fix(router): redirect versioned deep-links to the correct page |
| https://github.com/nestjs/docs.nestjs.com/pull/3408 | `nestjs/docs.nestjs.com` | `code_only` | `typescript` | chore(deps): update dependency uuid to v14 |
| https://github.com/nestjs/docs.nestjs.com/pull/3259 | `nestjs/docs.nestjs.com` | `code_only` | `typescript` | chore(deps): update dependency lint-staged to v16 |
| https://github.com/nestjs/docs.nestjs.com/pull/3368 | `nestjs/docs.nestjs.com` | `code_only` | `typescript` | chore(deps): update node.js to v24 |
| https://github.com/nestjs/docs.nestjs.com/pull/3366 | `nestjs/docs.nestjs.com` | `code_only` | `typescript` | chore(deps): update dependency chokidar to v5 |
| https://github.com/nestjs/docs.nestjs.com/pull/3365 | `nestjs/docs.nestjs.com` | `code_only` | `typescript` | chore(deps): update commitlint monorepo to v20 (major) |
| https://github.com/nestjs/docs.nestjs.com/pull/3364 | `nestjs/docs.nestjs.com` | `code_only` | `typescript` | chore(deps): update actions/checkout action to v6 - autoclosed |
| https://github.com/nestjs/docs.nestjs.com/pull/3345 | `nestjs/docs.nestjs.com` | `code_only` | `typescript` | chore(deps): update actions/setup-node action to v6 |
| https://github.com/nestjs/docs.nestjs.com/pull/3326 | `nestjs/docs.nestjs.com` | `code_only` | `typescript` | chore(deps): update dependency uuid to v13 |
| https://github.com/nestjs/docs.nestjs.com/pull/3399 | `nestjs/docs.nestjs.com` | `code_only` | `typescript` | docs(suites): fix broken links in docs |
| https://github.com/nestjs/docs.nestjs.com/pull/2800 | `nestjs/docs.nestjs.com` | `code_only` | `typescript` | refactor(): update redirect guard |
| https://github.com/nestjs/docs.nestjs.com/pull/3233 | `nestjs/docs.nestjs.com` | `code_only` | `typescript` | chore: added link for api reference |
| https://github.com/nestjs/docs.nestjs.com/pull/3379 | `nestjs/docs.nestjs.com` | `code_only` | `typescript` | Add zenobank.io to who-uses.json |
| https://github.com/nestjs/docs.nestjs.com/pull/3343 | `nestjs/docs.nestjs.com` | `code_only` | `typescript` | Add runsystem in who-uses |
| https://github.com/nestjs/docs.nestjs.com/pull/3322 | `nestjs/docs.nestjs.com` | `code_only` | `typescript` | Bump GitHub action workflows |
| https://github.com/nestjs/docs.nestjs.com/pull/3310 | `nestjs/docs.nestjs.com` | `code_only` | `typescript` | Update who-uses.json |
| https://github.com/nestjs/docs.nestjs.com/pull/3227 | `nestjs/docs.nestjs.com` | `code_and_docs` | `typescript` | docs(fundamentals): add discovery service documentation |
| https://github.com/nestjs/nest/pull/17530 | `nestjs/nest` | `code_only` | `typescript` | fix(deps): update dependency uuid to v14.0.2 |
| https://github.com/nestjs/nest/pull/17531 | `nestjs/nest` | `code_only` | `typescript` | fix(deps): update nest-graphql monorepo to v13.4.5 |
| https://github.com/nestjs/nest/pull/17529 | `nestjs/nest` | `code_only` | `typescript` | fix(deps): update dependency mysql2 to v3.23.4 |
| https://github.com/nestjs/nest/pull/17500 | `nestjs/nest` | `code_only` | `typescript` | chore(deps): update dependency vite to v8.2.2 |
| https://github.com/nestjs/nest/pull/17527 | `nestjs/nest` | `code_only` | `typescript` | fix(deps): update dependency mongoose to v9.9.3 |
| https://github.com/nestjs/nest/pull/17526 | `nestjs/nest` | `code_only` | `typescript` | fix(deps): update dependency fastify to v5.12.1 |
| https://github.com/nestjs/nest/pull/17524 | `nestjs/nest` | `code_only` | `typescript` | chore(deps): update dependency lerna to v10.0.1 |
| https://github.com/nestjs/nest/pull/17523 | `nestjs/nest` | `code_only` | `typescript` | fix(deps): update apollo graphql packages to v2.14.4 |
| https://github.com/nestjs/nest/pull/17520 | `nestjs/nest` | `code_only` | `typescript` | chore(deps): update dependency fastify to v5.12.1 |
| https://github.com/nestjs/nest/pull/17517 | `nestjs/nest` | `code_only` | `typescript` | chore(deps): update dependency @types/supertest to v7 |
| https://github.com/nestjs/nest/pull/17516 | `nestjs/nest` | `code_only` | `typescript` | chore(deps): update dependency @types/sqlite3 to v5 |
| https://github.com/nestjs/nest/pull/17493 | `nestjs/nest` | `code_only` | `typescript` | fix(express,fastify): apply falsy status codes in `reply()` |
| https://github.com/nestjs/nest/pull/17514 | `nestjs/nest` | `code_only` | `typescript` | fix(deps): update dependency @nestjs/swagger to v11.4.7 |
| https://github.com/nestjs/nest/pull/17515 | `nestjs/nest` | `code_only` | `typescript` | fix(deps): update dependency mongoose to v9.9.2 |
| https://github.com/nestjs/nest/pull/16962 | `nestjs/nest` | `code_only` | `typescript` | chore: improve platform-socket.io types |
| https://github.com/nestjs/nest/pull/17513 | `nestjs/nest` | `code_only` | `typescript` | fix(deps): update dependency find-my-way to v9.8.0 |
| https://github.com/nestjs/nest/pull/17512 | `nestjs/nest` | `code_only` | `typescript` | fix(deps): update dependency fastify to v5.12.0 |
| https://github.com/nestjs/nest/pull/17506 | `nestjs/nest` | `code_only` | `typescript` | chore(deps-dev): bump @nats-io/transport-node from 3.3.1 to 3.4.0 |
| https://github.com/nestjs/nest/pull/17508 | `nestjs/nest` | `code_only` | `typescript` | chore(deps): bump ws from 8.21.2 to 8.21.3 |
| https://github.com/nestjs/nest/pull/17510 | `nestjs/nest` | `code_only` | `typescript` | chore(deps): update dependency webpack to v5.109.2 |
| https://github.com/nodejs/node/pull/65365 | `nodejs/node` | `code_only` | `typescript` | test: add Headers coverage and benchmark |
| https://github.com/nodejs/node/pull/61951 | `nodejs/node` | `code_only` | `typescript` | esm: avoid super-linear data URL MIME regex |
| https://github.com/nodejs/node/pull/65363 | `nodejs/node` | `code_only` | `typescript` | url: speed up URLSearchParams |
| https://github.com/nodejs/node/pull/62654 | `nodejs/node` | `code_only` | `typescript` | fs: pass symlink type in cp when filter is provided |
| https://github.com/nodejs/node/pull/63886 | `nodejs/node` | `code_only` | `typescript` | fs: allocate FSReqPromise stat arrays lazily |
| https://github.com/nodejs/node/pull/64512 | `nodejs/node` | `code_only` | `typescript` | src: fix out-of-bounds write when transcoding odd-length ucs2 |
| https://github.com/nodejs/node/pull/64988 | `nodejs/node` | `code_only` | `typescript` | http: cache maxHeaderPairs per header section |
| https://github.com/nodejs/node/pull/64949 | `nodejs/node` | `code_and_docs` | `typescript` | doc: document that an empty OPENSSL_CONF skips config loading |
| https://github.com/nodejs/node/pull/64097 | `nodejs/node` | `code_only_tests_or_fixtures` | `typescript` | benchmark: add test-only and mock timers cases |
| https://github.com/nodejs/node/pull/65329 | `nodejs/node` | `code_only` | `typescript` | lib: load fewer builtins when bootstrapping without a snapshot |
| https://github.com/nodejs/node/pull/63411 | `nodejs/node` | `code_and_docs` | `typescript` | crypto: enable SIV and GCM-SIV modes in Cipher/Decipher APIs |
| https://github.com/nodejs/node/pull/65417 | `nodejs/node` | `code_and_docs` | `typescript` | ffi: prefer canonical type names |
| https://github.com/nodejs/node/pull/64839 | `nodejs/node` | `code_only` | `typescript` | util: fix formatting of functions returned from getters |
| https://github.com/nodejs/node/pull/64173 | `nodejs/node` | `code_only_tests_or_fixtures` | `typescript` | test: deflake test-net-listen-ipv6only |
| https://github.com/nodejs/node/pull/65294 | `nodejs/node` | `code_only` | `typescript` | sqlite: reject reentry while binding parameters |
| https://github.com/nodejs/node/pull/65293 | `nodejs/node` | `code_and_docs` | `typescript` | module: do not split a portable compile cache by uid |
| https://github.com/nodejs/node/pull/65389 | `nodejs/node` | `code_and_docs` | `typescript` | build,src: make --use-largepages a no-op |
| https://github.com/nodejs/node/pull/65405 | `nodejs/node` | `code_only` | `typescript` | doc: reserve NMV 150 for Electron 45 |
| https://github.com/nodejs/node/pull/62248 | `nodejs/node` | `code_only` | `typescript` | src: use simdutf for two-byte string utf8 conversion in utf8 value |
| https://github.com/nodejs/node/pull/65403 | `nodejs/node` | `code_only` | `typescript` | tools: improve nix-changes coverage |
| https://github.com/npm/cli/pull/9877 | `npm/cli` | `code_only` | `typescript` | fix(arborist): don't fetch packuments for uninstallable optional peer deps |
| https://github.com/npm/cli/pull/9864 | `npm/cli` | `code_only` | `typescript` | fix: don't print the funding message for global installs |
| https://github.com/npm/cli/pull/9836 | `npm/cli` | `code_only` | `typescript` | chore: update `node-integration` workflow template to latest actions |
| https://github.com/npm/cli/pull/9792 | `npm/cli` | `code_and_docs` | `typescript` | chore: release 12.0.2 |
| https://github.com/npm/cli/pull/9822 | `npm/cli` | `code_only` | `typescript` | chore: pass nodedir to node-gyp via npm_package_config env in node integration |
| https://github.com/npm/cli/pull/9701 | `npm/cli` | `code_and_docs` | `typescript` | chore: release 11.19.0 |
| https://github.com/npm/cli/pull/9815 | `npm/cli` | `code_and_docs` | `typescript` | chore: release 10.9.9 |
| https://github.com/npm/cli/pull/9814 | `npm/cli` | `code_only` | `typescript` | deps: tar@7.5.22 |
| https://github.com/npm/cli/pull/9770 | `npm/cli` | `code_only` | `typescript` | fix(arborist): avoid crash when peer back-off detaches a node |
| https://github.com/npm/cli/pull/9811 | `npm/cli` | `code_only` | `typescript` | fix(pack): honor min-release-age-exclude |
| https://github.com/npm/cli/pull/9810 | `npm/cli` | `code_only` | `typescript` | fix(owner): use scoped registry for user lookup |
| https://github.com/npm/cli/pull/9808 | `npm/cli` | `code_only` | `typescript` | fix(arborist): avoid crash when peer back-off detaches a node |
| https://github.com/npm/cli/pull/9760 | `npm/cli` | `code_only` | `typescript` | fix(pack): honor min-release-age-exclude |
| https://github.com/npm/cli/pull/9786 | `npm/cli` | `code_only` | `typescript` | fix(owner): use scoped registry for user lookup |
| https://github.com/npm/cli/pull/9791 | `npm/cli` | `code_only` | `typescript` | fix(arborist): allow audit fix to install safe downgrades |
| https://github.com/npm/cli/pull/9761 | `npm/cli` | `code_only` | `typescript` | fix(arborist): allow audit fix to install safe downgrades |
| https://github.com/npm/cli/pull/9747 | `npm/cli` | `code_only` | `typescript` | chore: parse pack --json object output in node integration |
| https://github.com/npm/cli/pull/9746 | `npm/cli` | `code_only_tests_or_fixtures` | `typescript` | chore(arborist): add missing registry mock in bin links reify test |
| https://github.com/npm/cli/pull/9744 | `npm/cli` | `code_and_docs` | `typescript` | chore: release 12.0.1 |
| https://github.com/npm/cli/pull/9745 | `npm/cli` | `code_and_docs` | `typescript` | fix(view): avoid wrapping array results |
| https://github.com/nuxt/nuxt/pull/36140 | `nuxt/nuxt` | `code_only` | `typescript` | chore: enable `minimumReleaseAgeExcludePrune` & `catalogPrune` |
| https://github.com/nuxt/nuxt/pull/36143 | `nuxt/nuxt` | `code_only` | `typescript` | fix(vite): rewrite every public asset `url()` in CSS |
| https://github.com/nuxt/nuxt/pull/36141 | `nuxt/nuxt` | `code_only` | `typescript` | ci: preview release add pm option |
| https://github.com/nuxt/nuxt/pull/36138 | `nuxt/nuxt` | `code_only` | `typescript` | refactor(kit,nitro,nuxt,schema): migrate more build-time warnings -> nostics |
| https://github.com/nuxt/nuxt/pull/36137 | `nuxt/nuxt` | `code_only` | `typescript` | fix(vite): apply `baseURL` to public assets in inlined styles |
| https://github.com/nuxt/nuxt/pull/36117 | `nuxt/nuxt` | `code_and_docs` | `typescript` | feat(nuxt): add experimental early404 for unmatched page routes |
| https://github.com/nuxt/nuxt/pull/36115 | `nuxt/nuxt` | `code_and_docs` | `typescript` | feat(nuxt): add experimental early return after `navigateTo` |
| https://github.com/nuxt/nuxt/pull/36132 | `nuxt/nuxt` | `code_only` | `typescript` | fix(nuxt): resolve layout name override in layout `isCurrent` check |
| https://github.com/nuxt/nuxt/pull/36128 | `nuxt/nuxt` | `code_only` | `typescript` | fix(nuxt): bridge `AppConfigInput` augmentations into `nuxt/schema` |
| https://github.com/nuxt/nuxt/pull/35729 | `nuxt/nuxt` | `code_only` | `typescript` | fix(kit): avoid mutating layer configs when resolving options |
| https://github.com/nuxt/nuxt/pull/36127 | `nuxt/nuxt` | `code_only` | `typescript` | feat(kit): nitro version utils + version-tagged server utils |
| https://github.com/nuxt/nuxt/pull/36126 | `nuxt/nuxt` | `code_only` | `typescript` | test: don't orphan e2e dev servers on fixture setup timeout |
| https://github.com/nuxt/nuxt/pull/36124 | `nuxt/nuxt` | `code_only` | `typescript` | fix(nuxt): don't resolve awaited `useAsyncData` with unfetched data on hydration |
| https://github.com/nuxt/nuxt/pull/36125 | `nuxt/nuxt` | `code_only` | `typescript` | refactor(kit): inline minimal nitro v2/v3 types and drop nitro deps |
| https://github.com/nuxt/nuxt/pull/36116 | `nuxt/nuxt` | `code_only` | `typescript` | perf(nuxt,vite): migrate `isVue` calls into plugin filters |
| https://github.com/nuxt/nuxt/pull/36123 | `nuxt/nuxt` | `code_only` | `typescript` | fix(nitro): route base-prefixed vite internal urls to vite in dev |
| https://github.com/nuxt/nuxt/pull/36121 | `nuxt/nuxt` | `code_only` | `typescript` | fix(nitro): vary early 404 responses on accept |
| https://github.com/nuxt/nuxt/pull/36103 | `nuxt/nuxt` | `code_only` | `typescript` | chore(deps): lock file maintenance (main) |
| https://github.com/nuxt/nuxt/pull/36105 | `nuxt/nuxt` | `code_only` | `typescript` | chore(deps): update all non-major dependencies (4.x) |
| https://github.com/nuxt/nuxt/pull/36100 | `nuxt/nuxt` | `code_only` | `typescript` | chore(deps): update all non-major dependencies (main) |
| https://github.com/open-telemetry/opentelemetry-js/pull/7015 | `open-telemetry/opentelemetry-js` | `code_and_docs` | `typescript` | fix(sdk-metrics): ignore infinity in exponential histograms |
| https://github.com/open-telemetry/opentelemetry-js/pull/6989 | `open-telemetry/opentelemetry-js` | `code_and_docs` | `typescript` | fix(sdk-node)!: fixes for and fail-fast on Resource creation from config file |
| https://github.com/open-telemetry/opentelemetry-js/pull/6845 | `open-telemetry/opentelemetry-js` | `code_and_docs` | `typescript` | feat(api, context-async): add experimental attach/detach functionality |
| https://github.com/open-telemetry/opentelemetry-js/pull/6923 | `open-telemetry/opentelemetry-js` | `code_and_docs` | `typescript` | feat(sdk-logs): allow modifying ReadWriteLogRecord properties |
| https://github.com/open-telemetry/opentelemetry-js/pull/7016 | `open-telemetry/opentelemetry-js` | `code_only` | `typescript` | docs(otlp-transformer): mark log APIs experimental |
| https://github.com/open-telemetry/opentelemetry-js/pull/6920 | `open-telemetry/opentelemetry-js` | `code_and_docs` | `typescript` | ci: run documentation tests weekly |
| https://github.com/open-telemetry/opentelemetry-js/pull/6956 | `open-telemetry/opentelemetry-js` | `code_and_docs` | `typescript` | perf(api): add getGlobal fast-path |
| https://github.com/open-telemetry/opentelemetry-js/pull/6974 | `open-telemetry/opentelemetry-js` | `code_only` | `typescript` | chore(deps): update dependency lerna to v10 |
| https://github.com/open-telemetry/opentelemetry-js/pull/6994 | `open-telemetry/opentelemetry-js` | `code_only` | `typescript` | Use shared OSSF Scorecard workflow |
| https://github.com/open-telemetry/opentelemetry-js/pull/7005 | `open-telemetry/opentelemetry-js` | `code_and_docs` | `typescript` | docs: fix stale example links |
| https://github.com/open-telemetry/opentelemetry-js/pull/7012 | `open-telemetry/opentelemetry-js` | `code_only` | `typescript` | chore(deps): update dependency dpdm to v4.3.0 |
| https://github.com/open-telemetry/opentelemetry-js/pull/7013 | `open-telemetry/opentelemetry-js` | `code_only` | `typescript` | chore(deps): update dependency eslint to v10.8.1 |
| https://github.com/open-telemetry/opentelemetry-js/pull/6993 | `open-telemetry/opentelemetry-js` | `code_and_docs` | `typescript` | chore(examples): update jaeger image |
| https://github.com/open-telemetry/opentelemetry-js/pull/6997 | `open-telemetry/opentelemetry-js` | `code_and_docs` | `typescript` | fix(sdk-node): support headers_list for declarative exporters |
| https://github.com/open-telemetry/opentelemetry-js/pull/6992 | `open-telemetry/opentelemetry-js` | `code_only` | `typescript` | chore(deps): update dependency @bufbuild/buf to v1.72.0 |
| https://github.com/open-telemetry/opentelemetry-js/pull/6991 | `open-telemetry/opentelemetry-js` | `code_only` | `typescript` | chore(deps): update actions/stale action to v10.4.0 |
| https://github.com/open-telemetry/opentelemetry-js/pull/6987 | `open-telemetry/opentelemetry-js` | `code_and_docs` | `typescript` | chore(resources): Ensure that multiple uses of serviceInstanceIdDetector.detect() return the *same* value for `service.instance.id` |
| https://github.com/open-telemetry/opentelemetry-js/pull/6970 | `open-telemetry/opentelemetry-js` | `code_and_docs` | `typescript` | docs(configuration): document ConfigModel suffix naming convention |
| https://github.com/open-telemetry/opentelemetry-js/pull/6962 | `open-telemetry/opentelemetry-js` | `code_and_docs` | `typescript` | fix(sdk-node)!: fail-fast on TracerProvider creation from config file |
| https://github.com/open-telemetry/opentelemetry-js/pull/6954 | `open-telemetry/opentelemetry-js` | `code_and_docs` | `typescript` | fix(sdk-node)!: fail-fast on MeterProvider creation from config file |
| https://github.com/open-telemetry/opentelemetry-js-contrib/pull/3577 | `open-telemetry/opentelemetry-js-contrib` | `code_and_docs` | `typescript` | feat(instrumentation-kafkajs): add messaging.kafka.cluster.id span attribute |
| https://github.com/open-telemetry/opentelemetry-js-contrib/pull/3672 | `open-telemetry/opentelemetry-js-contrib` | `code_and_docs` | `typescript` | fix(winston-transport): serialize Error attributes |
| https://github.com/open-telemetry/opentelemetry-js-contrib/pull/3673 | `open-telemetry/opentelemetry-js-contrib` | `code_only` | `typescript` | chore: expose release-please validation script |
| https://github.com/open-telemetry/opentelemetry-js-contrib/pull/3666 | `open-telemetry/opentelemetry-js-contrib` | `code_and_docs` | `typescript` | feat(instrumentation-ioredis): support ioredis @v6 |
| https://github.com/open-telemetry/opentelemetry-js-contrib/pull/3653 | `open-telemetry/opentelemetry-js-contrib` | `code_only` | `typescript` | fix(instrumentation-user-interaction): preserve bare event listener calls |
| https://github.com/open-telemetry/opentelemetry-js-contrib/pull/3659 | `open-telemetry/opentelemetry-js-contrib` | `code_only` | `typescript` | fix(instrumentation-undici): use low-cardinality error.type |
| https://github.com/open-telemetry/opentelemetry-js-contrib/pull/3649 | `open-telemetry/opentelemetry-js-contrib` | `code_and_docs` | `typescript` | fix(resource-detector-azure): read AKS cluster metadata from a mounted ConfigMap |
| https://github.com/open-telemetry/opentelemetry-js-contrib/pull/3656 | `open-telemetry/opentelemetry-js-contrib` | `code_only` | `typescript` | ci: move security scanning to shared workflow |
| https://github.com/open-telemetry/opentelemetry-js-contrib/pull/3627 | `open-telemetry/opentelemetry-js-contrib` | `code_and_docs` | `typescript` | feat(instrumentation-tedious): add missing stable SemConv attributes |
| https://github.com/open-telemetry/opentelemetry-js-contrib/pull/3641 | `open-telemetry/opentelemetry-js-contrib` | `code_only` | `typescript` | fix(instrumentation-console): restore console methods on disable when constructed with { enabled: true } |
| https://github.com/open-telemetry/opentelemetry-js-contrib/pull/3626 | `open-telemetry/opentelemetry-js-contrib` | `code_only` | `typescript` | fix(scripts): build glob patterns with forward slashes for Windows |
| https://github.com/open-telemetry/opentelemetry-js-contrib/pull/3636 | `open-telemetry/opentelemetry-js-contrib` | `code_only` | `typescript` | fix(instrumentation-user-interaction): compute the XPath inside the span creation try/catch |
| https://github.com/open-telemetry/opentelemetry-js-contrib/pull/3643 | `open-telemetry/opentelemetry-js-contrib` | `code_only` | `typescript` | fix(examples/mysql): initialize tracing before requiring instrumented modules |
| https://github.com/open-telemetry/opentelemetry-js-contrib/pull/3632 | `open-telemetry/opentelemetry-js-contrib` | `code_and_docs` | `typescript` | feat(instrumentation-runtime-node)!: remove deprecated v8js.memory.heap.limit metric |
| https://github.com/open-telemetry/opentelemetry-js-contrib/pull/3608 | `open-telemetry/opentelemetry-js-contrib` | `code_and_docs` | `typescript` | fix(instrumentation-mysql, instrumentation-mongodb)!: replace deprecated db.client.connections.usage with db.client.connection.count in m... |
| https://github.com/open-telemetry/opentelemetry-js-contrib/pull/3631 | `open-telemetry/opentelemetry-js-contrib` | `code_only` | `typescript` | chore(resource-detector-azure): remove redundant test devDependencies |
| https://github.com/open-telemetry/opentelemetry-js-contrib/pull/3630 | `open-telemetry/opentelemetry-js-contrib` | `code_only` | `typescript` | chore(deps): add @opentelemetry/context-async-hooks dev dependency |
| https://github.com/open-telemetry/opentelemetry-js-contrib/pull/3502 | `open-telemetry/opentelemetry-js-contrib` | `code_only` | `typescript` | chore(deps): update dependency babel-plugin-istanbul to v8 |
| https://github.com/open-telemetry/opentelemetry-js-contrib/pull/3278 | `open-telemetry/opentelemetry-js-contrib` | `code_and_docs` | `typescript` | fix(instrumentation-ioredis): correctly mark MULTI/PIPELINE in operation name |
| https://github.com/open-telemetry/opentelemetry-js-contrib/pull/3618 | `open-telemetry/opentelemetry-js-contrib` | `code_only` | `typescript` | ci: update otelbot token workflows to use client IDs |
| https://github.com/oven-sh/bun/pull/40116 | `oven-sh/bun` | `code_only` | `typescript` | js_parser: tree-shake classes whose computed keys are side-effect-free references |
| https://github.com/oven-sh/bun/pull/40112 | `oven-sh/bun` | `code_only` | `typescript` | compile: create the temporary executable with mode 0600, not 000 |
| https://github.com/oven-sh/bun/pull/40064 | `oven-sh/bun` | `code_only` | `typescript` | ci: close issues and PRs linked from merged PR descriptions |
| https://github.com/oven-sh/bun/pull/40074 | `oven-sh/bun` | `code_only_tests_or_fixtures` | `typescript` | test: run the control-character check in bun-pm-licenses.test.ts with --no-summary |
| https://github.com/oven-sh/bun/pull/39615 | `oven-sh/bun` | `code_only` | `typescript` | socket: report a peer reset on Windows as close(socket, ECONNRESET) instead of a code-less error |
| https://github.com/oven-sh/bun/pull/40070 | `oven-sh/bun` | `code_only` | `typescript` | util.inspect: drop the unused RegExpPrototypeTest primordial |
| https://github.com/oven-sh/bun/pull/38952 | `oven-sh/bun` | `code_and_docs` | `typescript` | pm: polish dedupe, prune, pm ls and pm licenses output |
| https://github.com/oven-sh/bun/pull/40062 | `oven-sh/bun` | `code_only` | `typescript` | test: update bun-pm.test.ts `pm ls` snapshots for #38952's header; name prune's HoistedTree::init flags |
| https://github.com/oven-sh/bun/pull/39923 | `oven-sh/bun` | `code_only` | `typescript` | util.inspect: native getOwnNonIndexProperties |
| https://github.com/oven-sh/bun/pull/39921 | `oven-sh/bun` | `code_only` | `typescript` | perf_hooks: native toJSON (with detail) and inspect hook for performance entries |
| https://github.com/oven-sh/bun/pull/40010 | `oven-sh/bun` | `code_and_docs` | `typescript` | install: add --offline and --prefer-offline to bun install |
| https://github.com/oven-sh/bun/pull/39969 | `oven-sh/bun` | `code_only` | `typescript` | sys(windows): make Fd::cwd() a stable sentinel instead of the PEB handle |
| https://github.com/oven-sh/bun/pull/39825 | `oven-sh/bun` | `code_only` | `typescript` | install: accept --recursive with --global as a no-op again |
| https://github.com/oven-sh/bun/pull/39808 | `oven-sh/bun` | `code_only` | `typescript` | ws: one binaryType rule for both shim sockets, add binaryType "blob" to ServerWebSocket |
| https://github.com/oven-sh/bun/pull/39642 | `oven-sh/bun` | `code_only` | `typescript` | ws: let handleUpgrade() run after an await, and fail like the npm package |
| https://github.com/oven-sh/bun/pull/40019 | `oven-sh/bun` | `code_only` | `typescript` | ci: an opportunistic macOS beta test lane on PR builds |
| https://github.com/oven-sh/bun/pull/39907 | `oven-sh/bun` | `code_only` | `typescript` | Propagate instead of clear: JSON body parse and mock.module resolution |
| https://github.com/oven-sh/bun/pull/31940 | `oven-sh/bun` | `code_only` | `typescript` | Fix Windows use-after-free of the pipe reader buffer retained by in-flight libuv reads |
| https://github.com/oven-sh/bun/pull/40018 | `oven-sh/bun` | `code_only` | `typescript` | websocket client: remove the remaining unsafe from the module |
| https://github.com/oven-sh/bun/pull/40014 | `oven-sh/bun` | `code_and_docs` | `typescript` | install: self-contained workspaces for the hoisted linker (`workspaces.selfContained` / `installConfig.hoistingLimits`) |
| https://github.com/payloadcms/payload/pull/15844 | `payloadcms/payload` | `code_only` | `typescript` | feat: disambiguate media files by prefix via query parameter |
| https://github.com/payloadcms/payload/pull/17809 | `payloadcms/payload` | `code_only` | `typescript` | fix(richtext-lexical): preserve logical text alignment |
| https://github.com/payloadcms/payload/pull/17830 | `payloadcms/payload` | `code_only` | `typescript` | fix(translations): correct mistranslated and untranslated strings in ja locale |
| https://github.com/payloadcms/payload/pull/17831 | `payloadcms/payload` | `code_only` | `typescript` | fix(db-postgres): release the client checked out during connect |
| https://github.com/payloadcms/payload/pull/17838 | `payloadcms/payload` | `code_and_docs` | `typescript` | feat: support nested queries on has-many relationships |
| https://github.com/pmndrs/zustand/pull/3570 | `pmndrs/zustand` | `code_only` | `typescript` | Build the docs with pmndrs/docs@v4 |
| https://github.com/pmndrs/zustand/pull/3560 | `pmndrs/zustand` | `code_only` | `typescript` | chore(deps): update dev dependencies |
| https://github.com/pmndrs/zustand/pull/3555 | `pmndrs/zustand` | `code_only` | `typescript` | fix(persist): clearStorage() should invalidate concurrent async rehydration |
| https://github.com/pmndrs/zustand/pull/3514 | `pmndrs/zustand` | `code_only_tests_or_fixtures` | `typescript` | chore(workflows): remove resolutions |
| https://github.com/pmndrs/zustand/pull/3513 | `pmndrs/zustand` | `code_only` | `typescript` | chore(deps): update dev dependencies |
| https://github.com/pmndrs/zustand/pull/3511 | `pmndrs/zustand` | `code_only` | `typescript` | fix(devtools): improve type inference for Devtools initializer |
| https://github.com/pmndrs/zustand/pull/3512 | `pmndrs/zustand` | `code_only` | `typescript` | update pnpm etc |
| https://github.com/pmndrs/zustand/pull/3469 | `pmndrs/zustand` | `code_only` | `typescript` | fix(devtools): support Firefox/Safari stack format in findCallerName |
| https://github.com/pmndrs/zustand/pull/3486 | `pmndrs/zustand` | `code_only` | `typescript` | chore(deps): update dev dependencies |
| https://github.com/pmndrs/zustand/pull/3483 | `pmndrs/zustand` | `code_only_tests_or_fixtures` | `typescript` | fix(tests): change parameters for 'expect' in test |
| https://github.com/pmndrs/zustand/pull/725 | `pmndrs/zustand` | `code_and_docs` | `typescript` | breaking(types): Add higher kinded mutator types |
| https://github.com/pmndrs/zustand/pull/3471 | `pmndrs/zustand` | `code_only_tests_or_fixtures` | `typescript` | test(middleware/immer): add runtime tests for immer middleware |
| https://github.com/pmndrs/zustand/pull/3443 | `pmndrs/zustand` | `code_only` | `typescript` | refactor(devtools): remove duplicate module augmentation |
| https://github.com/pmndrs/zustand/pull/3442 | `pmndrs/zustand` | `code_only_tests_or_fixtures` | `typescript` | test: expand React subscribe test coverage |
| https://github.com/pmndrs/zustand/pull/3447 | `pmndrs/zustand` | `code_only` | `typescript` | chore(deps): bump actions/deploy-pages from 4.0.5 to 5.0.0 |
| https://github.com/pmndrs/zustand/pull/3414 | `pmndrs/zustand` | `code_only` | `typescript` | fix(devtools): correct redux devtools config type extension |
| https://github.com/pmndrs/zustand/pull/3427 | `pmndrs/zustand` | `code_only` | `typescript` | chore(deps): update dev dependencies |
| https://github.com/pmndrs/zustand/pull/3391 | `pmndrs/zustand` | `code_only` | `typescript` | fix(persist): use latest state in post-rehydration callback |
| https://github.com/pmndrs/zustand/pull/3403 | `pmndrs/zustand` | `code_and_docs` | `typescript` | Fix README internal links for GitHub rendering |
| https://github.com/pmndrs/zustand/pull/3396 | `pmndrs/zustand` | `code_only` | `typescript` | fix: update deploy-pages action commit hash |
| https://github.com/pnpm/pnpm/pull/14053 | `pnpm/pnpm` | `code_and_docs` | `typescript` | fix(update): scope pinned recursive updates by version line |
| https://github.com/pnpm/pnpm/pull/14086 | `pnpm/pnpm` | `code_and_docs` | `typescript` | feat(pacquet): support remaining install env vars |
| https://github.com/pnpm/pnpm/pull/14085 | `pnpm/pnpm` | `code_and_docs` | `typescript` | [pacquet] feat(hooks): support the globalPnpmfile setting |
| https://github.com/pnpm/pnpm/pull/14049 | `pnpm/pnpm` | `code_only` | `typescript` | chore: `lint:ts` script add `concurrency` option |
| https://github.com/pnpm/pnpm/pull/13954 | `pnpm/pnpm` | `code_and_docs` | `typescript` | fix(version): make --dry-run leave the manifests untouched |
| https://github.com/pnpm/pnpm/pull/13959 | `pnpm/pnpm` | `code_and_docs` | `typescript` | fix: stop the not-implemented stub from shadowing set-script |
| https://github.com/pnpm/pnpm/pull/14036 | `pnpm/pnpm` | `code_and_docs` | `typescript` | fix(fs-packlist): anchor `files` entries at the package root |
| https://github.com/pnpm/pnpm/pull/14083 | `pnpm/pnpm` | `code_and_docs` | `typescript` | feat(pacquet): support configurable state directory |
| https://github.com/pnpm/pnpm/pull/14037 | `pnpm/pnpm` | `code_and_docs` | `typescript` | fix(pkg): accept hyphens in dot-notation property paths |
| https://github.com/pnpm/pnpm/pull/14084 | `pnpm/pnpm` | `code_and_docs` | `typescript` | [pacquet] fix(hooks): name the configured pnpmfile that is missing |
| https://github.com/pnpm/pnpm/pull/13604 | `pnpm/pnpm` | `code_and_docs` | `typescript` | fix(deps-installer): prevent dedupe --check from moving hoisted dependencies |
| https://github.com/pnpm/pnpm/pull/14013 | `pnpm/pnpm` | `code_and_docs` | `typescript` | fix(install): enforce --frozen-lockfile for packageManagerDependencies |
| https://github.com/pnpm/pnpm/pull/14019 | `pnpm/pnpm` | `code_and_docs` | `typescript` | fix: honor minimumReleaseAgeIgnoreMissingTime in the trust check |
| https://github.com/pnpm/pnpm/pull/14079 | `pnpm/pnpm` | `code_and_docs` | `typescript` | feat(config): support the lockfileDir setting in the Rust CLI |
| https://github.com/pnpm/pnpm/pull/14075 | `pnpm/pnpm` | `code_and_docs` | `typescript` | fix(package-manager): let a filtered no-op install short-circuit |
| https://github.com/pnpm/pnpm/pull/14074 | `pnpm/pnpm` | `code_and_docs` | `typescript` | feat(pacquet): support includeWorkspaceRoot and the workspace-cycle settings |
| https://github.com/pnpm/pnpm/pull/13990 | `pnpm/pnpm` | `code_and_docs` | `typescript` | fix(config): normalize Windows store paths |
| https://github.com/pnpm/pnpm/pull/14032 | `pnpm/pnpm` | `code_only` | `typescript` | refactor: remove unused linked aliases set |
| https://github.com/pnpm/pnpm/pull/13937 | `pnpm/pnpm` | `code_and_docs` | `typescript` | fix(bins): clean up stale pnpm.ps1 shim on Windows |
| https://github.com/pnpm/pnpm/pull/14072 | `pnpm/pnpm` | `code_and_docs` | `typescript` | fix(sbom): honor --filter-prod and the universal --fail-if-no-match |
| https://github.com/prettier/prettier/pull/19891 | `prettier/prettier` | `code_only` | `typescript` | Align `characterReferenceRegex` with `micromark-util-decode-string` |
| https://github.com/prettier/prettier/pull/19909 | `prettier/prettier` | `code_only` | `typescript` | Fix TSX support for `oxc-ts` and `yuku-ts` parser |
| https://github.com/prettier/prettier/pull/19665 | `prettier/prettier` | `code_and_docs` | `typescript` | docs: replace unmaintained go-template plugin entry |
| https://github.com/prettier/prettier/pull/19904 | `prettier/prettier` | `code_only` | `typescript` | Update dependency @angular/compiler to v22.1.3 |
| https://github.com/prettier/prettier/pull/19902 | `prettier/prettier` | `code_and_docs` | `typescript` | Fix comment in destructuring patterns for Flow parser |
| https://github.com/prettier/prettier/pull/19901 | `prettier/prettier` | `code_only_tests_or_fixtures` | `typescript` | Test flow parser that both valid in ts and flow |
| https://github.com/prettier/prettier/pull/19900 | `prettier/prettier` | `code_only_tests_or_fixtures` | `typescript` | Add test for comment in destructuring patterns |
| https://github.com/prettier/prettier/pull/19898 | `prettier/prettier` | `code_only_tests_or_fixtures` | `typescript` | Add test for comments in parameter/argument list |
| https://github.com/prettier/prettier/pull/19897 | `prettier/prettier` | `code_and_docs` | `typescript` | Fix comments around heritage clauses |
| https://github.com/prettier/prettier/pull/19893 | `prettier/prettier` | `code_and_docs` | `typescript` | Fix unstable trailing comment on a nested parenthesized assignment |
| https://github.com/prettier/prettier/pull/19894 | `prettier/prettier` | `code_and_docs` | `typescript` | Fix unstable comment before the first element of a sequence expression |
| https://github.com/prettier/prettier/pull/19892 | `prettier/prettier` | `code_only` | `typescript` | Update dependency oxc-parser to v0.146.0 |
| https://github.com/prettier/prettier/pull/19890 | `prettier/prettier` | `code_only` | `typescript` | Simplify `printTitle` |
| https://github.com/prettier/prettier/pull/19849 | `prettier/prettier` | `code_and_docs` | `typescript` | Fix escaped character in links |
| https://github.com/prettier/prettier/pull/19888 | `prettier/prettier` | `code_only_tests_or_fixtures` | `typescript` | Add test for invalid initializer in `for..in` |
| https://github.com/prettier/prettier/pull/19885 | `prettier/prettier` | `code_only_tests_or_fixtures` | `typescript` | Add tests for decorators on rest parameters |
| https://github.com/prettier/prettier/pull/19884 | `prettier/prettier` | `code_only` | `typescript` | Update dependency oxc-parser to v0.145.0 |
| https://github.com/prettier/prettier/pull/19878 | `prettier/prettier` | `code_and_docs` | `typescript` | Strip blockquote markers from a setext heading's continuation lines |
| https://github.com/prettier/prettier/pull/19880 | `prettier/prettier` | `code_and_docs` | `typescript` | Fix range formatting expanding to a non-source-element node |
| https://github.com/prettier/prettier/pull/19742 | `prettier/prettier` | `code_and_docs` | `typescript` | Support JSX spread attributes in mdx |
| https://github.com/reduxjs/redux-toolkit/pull/5304 | `reduxjs/redux-toolkit` | `code_and_docs` | `typescript` | feat: Add option to generate all available schemas |
| https://github.com/reduxjs/redux-toolkit/pull/5356 | `reduxjs/redux-toolkit` | `code_only` | `typescript` | chore(toolkit): remove redundant and unused type declarations |
| https://github.com/reduxjs/redux-toolkit/pull/5358 | `reduxjs/redux-toolkit` | `code_only` | `typescript` | ci: bump GitHub Actions to their latest versions |
| https://github.com/reduxjs/redux-toolkit/pull/5353 | `reduxjs/redux-toolkit` | `code_and_docs` | `typescript` | feat(codegen): add enumStyle option |
| https://github.com/reduxjs/redux-toolkit/pull/5326 | `reduxjs/redux-toolkit` | `code_only` | `typescript` | fix(codegen): respect optional request bodies |
| https://github.com/reduxjs/redux-toolkit/pull/5236 | `reduxjs/redux-toolkit` | `code_and_docs` | `typescript` | feat(codegen): add `operationIdTransformer` option |
| https://github.com/reduxjs/redux-toolkit/pull/5350 | `reduxjs/redux-toolkit` | `code_only` | `typescript` | docs: fix `getOriginalState` example to use `Promise.resolve` |
| https://github.com/reduxjs/redux-toolkit/pull/5289 | `reduxjs/redux-toolkit` | `code_only` | `typescript` | feat(toolkit)!: switch to native `NoInfer` utility type |
| https://github.com/reduxjs/redux-toolkit/pull/5232 | `reduxjs/redux-toolkit` | `code_only_tests_or_fixtures` | `typescript` | chore(toolkit): update test imports to use public entry points |
| https://github.com/reduxjs/redux-toolkit/pull/5344 | `reduxjs/redux-toolkit` | `code_only` | `typescript` | fix(types): fix tsgo (TS 7.0) type errors and re-enable the native-preview CI job |
| https://github.com/reduxjs/redux-toolkit/pull/5335 | `reduxjs/redux-toolkit` | `code_only` | `typescript` | docs: fix `selectFromResult` example data access |
| https://github.com/reduxjs/redux-toolkit/pull/5333 | `reduxjs/redux-toolkit` | `code_only` | `typescript` | docs: fix `isJsonContentType` example to type-check |
| https://github.com/reduxjs/redux-toolkit/pull/5182 | `reduxjs/redux-toolkit` | `code_only` | `typescript` | fix(query): prevent `onQueryStarted` from triggering at end-of-list |
| https://github.com/reduxjs/redux-toolkit/pull/5323 | `reduxjs/redux-toolkit` | `code_only` | `typescript` | fix(entityAdapter): pre-merge same-ID updates in sorted adapter's updateMany |
| https://github.com/reduxjs/redux-toolkit/pull/5315 | `reduxjs/redux-toolkit` | `code_only` | `typescript` | Simplify `useRef<T \| undefined>(undefined)` usages in RTK Query hooks |
| https://github.com/reduxjs/redux-toolkit/pull/5314 | `reduxjs/redux-toolkit` | `code_only` | `typescript` | fix: don't swallow `createAsyncThunk` aborts that happen before pending |
| https://github.com/reduxjs/redux-toolkit/pull/5328 | `reduxjs/redux-toolkit` | `code_only` | `typescript` | docs: correct `autoBatchEnhancer` JSDoc default to `requestAnimationFrame` |
| https://github.com/reduxjs/redux-toolkit/pull/5327 | `reduxjs/redux-toolkit` | `code_only` | `typescript` | fix(query): reflect cache updates in hook data |
| https://github.com/reduxjs/redux-toolkit/pull/5321 | `reduxjs/redux-toolkit` | `code_only` | `typescript` | fix(`entityAdapter`): `setAll` with duplicate IDs keeps last occurrence (consistent with `setMany`) |
| https://github.com/reduxjs/redux-toolkit/pull/5319 | `reduxjs/redux-toolkit` | `code_only` | `typescript` | fix(combineSlices): scope stateProxyMap per instance to prevent cross-instance proxy collisions |
| https://github.com/rollup/rollup/pull/6483 | `rollup/rollup` | `code_only` | `typescript` | chore(deps): update minor/patch updates |
| https://github.com/rollup/rollup/pull/6482 | `rollup/rollup` | `code_only` | `typescript` | Remove unused rendered module sources map |
| https://github.com/rollup/rollup/pull/6480 | `rollup/rollup` | `code_only` | `typescript` | chore(deps): lock file maintenance |
| https://github.com/rollup/rollup/pull/6478 | `rollup/rollup` | `code_only` | `typescript` | chore(deps): lock file maintenance |
| https://github.com/rollup/rollup/pull/6477 | `rollup/rollup` | `code_only` | `typescript` | fix(deps): update minor/patch updates |
| https://github.com/rollup/rollup/pull/6476 | `rollup/rollup` | `code_only` | `typescript` | chore(deps): update dtolnay/rust-toolchain digest to 4360b52 |
| https://github.com/rollup/rollup/pull/6472 | `rollup/rollup` | `code_only` | `typescript` | chore(deps): update dependency eslint-plugin-unicorn to v73 |
| https://github.com/rollup/rollup/pull/6471 | `rollup/rollup` | `code_only` | `typescript` | chore(deps): lock file maintenance |
| https://github.com/rollup/rollup/pull/6470 | `rollup/rollup` | `code_only` | `typescript` | fix(deps): update swc monorepo (major) |
| https://github.com/rollup/rollup/pull/6469 | `rollup/rollup` | `code_only` | `typescript` | fix(deps): update minor/patch updates |
| https://github.com/rollup/rollup/pull/6468 | `rollup/rollup` | `code_only` | `typescript` | Keep the semicolon added after a replaced default export |
| https://github.com/rollup/rollup/pull/6467 | `rollup/rollup` | `code_only` | `typescript` | ci: fix linux-gnu glibc regression and enforce glibc ≤ 2.28 compatibility |
| https://github.com/rollup/rollup/pull/6466 | `rollup/rollup` | `code_only` | `typescript` | chore(deps): lock file maintenance |
| https://github.com/rollup/rollup/pull/6465 | `rollup/rollup` | `code_only` | `typescript` | chore(deps): lock file maintenance |
| https://github.com/rollup/rollup/pull/6464 | `rollup/rollup` | `code_only` | `typescript` | fix(deps): update minor/patch updates |
| https://github.com/rollup/rollup/pull/6459 | `rollup/rollup` | `code_only` | `typescript` | chore(deps): lock file maintenance |
| https://github.com/rollup/rollup/pull/6458 | `rollup/rollup` | `code_only` | `typescript` | fix(deps): update swc monorepo (major) |
| https://github.com/rollup/rollup/pull/6457 | `rollup/rollup` | `code_only` | `typescript` | chore(deps): update dependency magic-string to v1 |
| https://github.com/rollup/rollup/pull/6456 | `rollup/rollup` | `code_only` | `typescript` | fix(deps): update minor/patch updates |
| https://github.com/rollup/rollup/pull/6451 | `rollup/rollup` | `code_only` | `typescript` | chore(deps): lock file maintenance |
| https://github.com/shadcn-ui/ui/pull/11567 | `shadcn-ui/ui` | `code_and_docs` | `typescript` | chore(release): version packages |
| https://github.com/shadcn-ui/ui/pull/11582 | `shadcn-ui/ui` | `code_and_docs` | `typescript` | feat(shadcn): add private repository support for github registries |
| https://github.com/shadcn-ui/ui/pull/11517 | `shadcn-ui/ui` | `code_only` | `typescript` | feat(registry): add Honest UI to directory |
| https://github.com/shadcn-ui/ui/pull/11471 | `shadcn-ui/ui` | `code_only` | `typescript` | chore(directory): rename the snap-cn namespace to snapcn |
| https://github.com/shadcn-ui/ui/pull/11579 | `shadcn-ui/ui` | `code_and_docs` | `typescript` | fix(docs): exclude accordion from typeset styles |
| https://github.com/shadcn-ui/ui/pull/11485 | `shadcn-ui/ui` | `code_only` | `typescript` | feat(registry): add @motion-lexicon to the registry directory |
| https://github.com/shadcn-ui/ui/pull/11493 | `shadcn-ui/ui` | `code_only` | `typescript` | feat(registry): add @ilinxa to the registry directory |
| https://github.com/shadcn-ui/ui/pull/11496 | `shadcn-ui/ui` | `code_only` | `typescript` | feat(registry): add @persianlabsui to registry directory |
| https://github.com/shadcn-ui/ui/pull/11513 | `shadcn-ui/ui` | `code_only` | `typescript` | Add @brut-ui registry to the directory |
| https://github.com/shadcn-ui/ui/pull/11473 | `shadcn-ui/ui` | `code_only` | `typescript` | feat(registry): add @washiveil to the registry directory |
| https://github.com/shadcn-ui/ui/pull/11543 | `shadcn-ui/ui` | `code_only` | `typescript` | feat(registry): add @blode |
| https://github.com/shadcn-ui/ui/pull/11314 | `shadcn-ui/ui` | `code_only` | `typescript` | feat(registry): add @better-auth-ui to registry directory |
| https://github.com/shadcn-ui/ui/pull/11398 | `shadcn-ui/ui` | `code_only` | `typescript` | feat(registry): add @vernostudio to the registry directory |
| https://github.com/shadcn-ui/ui/pull/11248 | `shadcn-ui/ui` | `code_and_docs` | `typescript` | feat(shadcn): add migrate base-color |
| https://github.com/shadcn-ui/ui/pull/11546 | `shadcn-ui/ui` | `code_only` | `typescript` | fix(ci): use GitHub token for stale workflow |
| https://github.com/shadcn-ui/ui/pull/11492 | `shadcn-ui/ui` | `code_only` | `typescript` | registry: add @velobits to the registry directory |
| https://github.com/shadcn-ui/ui/pull/11436 | `shadcn-ui/ui` | `code_only` | `typescript` | fix(styles): unify questionnaire and field choice-card styles |
| https://github.com/shadcn-ui/ui/pull/9426 | `shadcn-ui/ui` | `code_only` | `typescript` | registry: add @inferencesh |
| https://github.com/shadcn-ui/ui/pull/11516 | `shadcn-ui/ui` | `code_only` | `typescript` | feat(registry): add @flagcn to directory |
| https://github.com/shadcn-ui/ui/pull/10998 | `shadcn-ui/ui` | `code_only` | `typescript` | feat(registry): add @remotionui registry |
| https://github.com/strapi/strapi/pull/27201 | `strapi/strapi` | `code_only` | `typescript` | fix(core): Access token rotation fails with asymmetric JWT algorithms |
| https://github.com/strapi/strapi/pull/27416 | `strapi/strapi` | `code_only` | `typescript` | fix(upload): list queued files in the upload progress dialog |
| https://github.com/strapi/strapi/pull/27352 | `strapi/strapi` | `code_only` | `typescript` | future(upload): fix drawer error messages |
| https://github.com/strapi/strapi/pull/27425 | `strapi/strapi` | `code_only` | `typescript` | fix(upload): move replace media to the drawer footer, add tooltips |
| https://github.com/strapi/strapi/pull/27414 | `strapi/strapi` | `code_and_docs` | `typescript` | fix(upload): sizeLimit is not enforced when replacing a file |
| https://github.com/strapi/strapi/pull/27311 | `strapi/strapi` | `code_only` | `typescript` | fix(core/strapi): local plugins duplicate the admin module graph and exhaust build memory |
| https://github.com/strapi/strapi/pull/27438 | `strapi/strapi` | `code_only` | `typescript` | enhancement(admin): slow startup with many roles due to redundant permission … |
| https://github.com/strapi/strapi/pull/27213 | `strapi/strapi` | `code_only` | `typescript` | fix(admin): honour redirectTo when the auth page redirects an authenticated user |
| https://github.com/strapi/strapi/pull/27394 | `strapi/strapi` | `code_only` | `typescript` | fix(content-manager): out of sort memory when listing history versions on mysql |
| https://github.com/strapi/strapi/pull/27420 | `strapi/strapi` | `code_only` | `typescript` | fix(admin): keep api token permissions on localized content types at boot |
| https://github.com/strapi/strapi/pull/27365 | `strapi/strapi` | `code_only` | `typescript` | future(upload): dismiss the bulk-actions bar while the asset drawer is open |
| https://github.com/strapi/strapi/pull/27423 | `strapi/strapi` | `code_only` | `typescript` | fix(content-manager): reject MCP relation writes combining set with connect or disconnect |
| https://github.com/strapi/strapi/pull/27383 | `strapi/strapi` | `code_only` | `typescript` | fix(i18n): correct broken placeholders in pt-BR translations (#27257) |
| https://github.com/strapi/strapi/pull/26525 | `strapi/strapi` | `code_only` | `typescript` | fix(core): propagate server updatedAt in addFirstPublishedAtToDraft to avoid false modified flag |
| https://github.com/strapi/strapi/pull/27426 | `strapi/strapi` | `code_and_docs` | `typescript` | chore: add worktree bootstrap command |
| https://github.com/strapi/strapi/pull/26835 | `strapi/strapi` | `code_only` | `typescript` | fix(content-manager): draft status filter with i18n sibling locale published |
| https://github.com/strapi/strapi/pull/27409 | `strapi/strapi` | `code_only` | `typescript` | chore: replace lodash forEach with native Object.entries/values |
| https://github.com/strapi/strapi/pull/27390 | `strapi/strapi` | `code_and_docs` | `typescript` | security(graphql): warn about unbounded operation limits |
| https://github.com/strapi/strapi/pull/27406 | `strapi/strapi` | `code_only` | `typescript` | chore(deps): upgrade memfs to 4.68.1 in @strapi/upgrade |
| https://github.com/strapi/strapi/pull/27360 | `strapi/strapi` | `code_and_docs` | `typescript` | security(upload): deny svg in generated project defaults |
| https://github.com/supabase/supabase/pull/49380 | `supabase/supabase` | `code_only` | `typescript` | QueryEditor to have the same validations as per SQL editor |
| https://github.com/supabase/supabase/pull/1 | `supabase/supabase` | `code_only` | `typescript` | Add Realtime, allowing realtime-js to initialise sockets from inside |
| https://github.com/supabase/supabase/pull/49402 | `supabase/supabase` | `code_only` | `typescript` | Restore notebook diff preview for completed updates |
| https://github.com/supabase/supabase/pull/49401 | `supabase/supabase` | `code_only` | `typescript` | Expose previous notebook content in update_notebook |
| https://github.com/supabase/supabase/pull/47851 | `supabase/supabase` | `code_and_docs` | `typescript` | feat(self-hosted): add update script |
| https://github.com/supabase/supabase/pull/49160 | `supabase/supabase` | `code_only` | `typescript` | feat(billing): Use the customer data endpoint to update billing emails |
| https://github.com/supabase/supabase/pull/49395 | `supabase/supabase` | `code_only` | `typescript` | fix(studio): validation scroll area bug in scoped pat |
| https://github.com/supabase/supabase/pull/49398 | `supabase/supabase` | `code_only` | `typescript` | test(studio): add eval cases for list_databases-driven notebook creation |
| https://github.com/supabase/supabase/pull/49399 | `supabase/supabase` | `code_only` | `typescript` | Stop re-deriving notebook update diffs after completion |
| https://github.com/supabase/supabase/pull/49393 | `supabase/supabase` | `code_only` | `typescript` | Scoped PAT: Fix projects handling when user has more than 100 projects |
| https://github.com/supabase/supabase/pull/49334 | `supabase/supabase` | `code_only` | `typescript` | docs(studio): instruct the notebook agent to use list_databases |
| https://github.com/supabase/supabase/pull/49343 | `supabase/supabase` | `code_only` | `typescript` | fix(www): name the /features page button controls |
| https://github.com/supabase/supabase/pull/49344 | `supabase/supabase` | `code_only` | `typescript` | fix(docs): stop rendering empty troubleshooting error-code pills |
| https://github.com/supabase/supabase/pull/49333 | `supabase/supabase` | `code_only` | `typescript` | fix(studio): reject unknown database_identifier before writing a notebook |
| https://github.com/supabase/supabase/pull/49332 | `supabase/supabase` | `code_only` | `typescript` | revert(studio): reinstate database_identifier on the agent notebook schema |
| https://github.com/supabase/supabase/pull/49331 | `supabase/supabase` | `code_only` | `typescript` | fix(studio): expose notebook diff validation errors for auto-retry |
| https://github.com/supabase/supabase/pull/49318 | `supabase/supabase` | `code_only` | `typescript` | fix(studio): require full authentication for the support form |
| https://github.com/supabase/supabase/pull/49328 | `supabase/supabase` | `code_only` | `typescript` | feat(studio): add list_databases tool for the AI assistant |
| https://github.com/supabase/supabase/pull/49303 | `supabase/supabase` | `code_and_docs` | `typescript` | docs(self-hosted): add poolers how-to guide |
| https://github.com/supabase/supabase/pull/49324 | `supabase/supabase` | `code_only` | `typescript` | Add update_notebook evals; fix prompt gaps they surfaced |
| https://github.com/supabase/supabase-js/pull/1882 | `supabase/supabase-js` | `code_only` | `typescript` | docs(postgrest): add upsert tsdoc examples and fix response/options |
| https://github.com/supabase/supabase-js/pull/2612 | `supabase/supabase-js` | `code_only` | `typescript` | fix(realtime): respect custom logger for send() REST fallback warning |
| https://github.com/supabase/supabase-js/pull/2610 | `supabase/supabase-js` | `code_only` | `typescript` | chore(deps): bump pnpm/action-setup from 6.0.9 to 6.0.10 in the actions-minor-and-patch group |
| https://github.com/supabase/supabase-js/pull/2609 | `supabase/supabase-js` | `code_only` | `typescript` | ci: pin supabase/sdk reusable workflows to v1.0.0 |
| https://github.com/supabase/supabase-js/pull/2606 | `supabase/supabase-js` | `code_only` | `typescript` | chore(supabase): bump supabase cli to 2.113.0 |
| https://github.com/supabase/supabase-js/pull/2587 | `supabase/supabase-js` | `code_only` | `typescript` | fix(auth): preserve 5xx error message |
| https://github.com/supabase/supabase-js/pull/2605 | `supabase/supabase-js` | `code_only` | `typescript` | fix(postgrest): move override fixtures out of generated types, repair codegen |
| https://github.com/supabase/supabase-js/pull/2607 | `supabase/supabase-js` | `code_only` | `typescript` | chore(deps-dev): bump nanoid from 3.3.12 to 3.3.17 in the npm_and_yarn group across 1 directory |
| https://github.com/supabase/supabase-js/pull/2604 | `supabase/supabase-js` | `code_and_docs` | `typescript` | fix(supabase): improve trace propagation sampling and diagnostics |
| https://github.com/supabase/supabase-js/pull/2603 | `supabase/supabase-js` | `code_only` | `typescript` | fix(supabase): add trace context headers to canonical CORS allow-list |
| https://github.com/supabase/supabase-js/pull/2602 | `supabase/supabase-js` | `code_only` | `typescript` | chore: sync new capability IDs from canonical spec |
| https://github.com/supabase/supabase-js/pull/2601 | `supabase/supabase-js` | `code_only` | `typescript` | chore: update sdk-compliance.yaml for renamed capability matrix IDs |
| https://github.com/supabase/supabase-js/pull/2600 | `supabase/supabase-js` | `code_only` | `typescript` | chore(deps-dev): bump postcss from 8.5.20 to 8.5.23 in the npm_and_yarn group across 1 directory |
| https://github.com/supabase/supabase-js/pull/2598 | `supabase/supabase-js` | `code_only` | `typescript` | ci(release): fix gotrue publishing |
| https://github.com/supabase/supabase-js/pull/2595 | `supabase/supabase-js` | `code_only` | `typescript` | chore(deps): bump actions/stale from 10.4.0 to 11.0.0 |
| https://github.com/supabase/supabase-js/pull/2597 | `supabase/supabase-js` | `code_only` | `typescript` | fix(realtime): clear stale join payload on sign-out |
| https://github.com/supabase/supabase-js/pull/2594 | `supabase/supabase-js` | `code_only` | `typescript` | fix(realtime): prevent duplicate on bindings |
| https://github.com/supabase/supabase-js/pull/2592 | `supabase/supabase-js` | `code_only` | `typescript` | fix(realtime): ensure setAuth doesn't disable token refresh |
| https://github.com/supabase/supabase-js/pull/2591 | `supabase/supabase-js` | `code_only` | `typescript` | chore(deps): bump the actions-minor-and-patch group across 1 directory with 2 updates |
| https://github.com/supabase/supabase-js/pull/2590 | `supabase/supabase-js` | `code_only` | `typescript` | test(realtime): stabilize supabase client instance in chat example |
| https://github.com/sveltejs/kit/pull/16890 | `sveltejs/kit` | `code_and_docs` | `typescript` | fix: Reject all pending query promises when a query fails before resolving with a value for the first time |
| https://github.com/sveltejs/kit/pull/16885 | `sveltejs/kit` | `code_only` | `typescript` | chore: move compile plugin |
| https://github.com/sveltejs/kit/pull/16894 | `sveltejs/kit` | `code_only_tests_or_fixtures` | `typescript` | chore: don't change directory in the basics test setup |
| https://github.com/sveltejs/kit/pull/16886 | `sveltejs/kit` | `code_only_tests_or_fixtures` | `typescript` | chore: flaky bot test part 2 |
| https://github.com/sveltejs/kit/pull/16884 | `sveltejs/kit` | `code_only_tests_or_fixtures` | `typescript` | chore: testing the flaky test bot |
| https://github.com/sveltejs/kit/pull/16883 | `sveltejs/kit` | `code_only` | `typescript` | chore: set oxc as vscode formatter |
| https://github.com/sveltejs/kit/pull/16727 | `sveltejs/kit` | `code_only` | `typescript` | chore: revert minimumReleaseAgeExclude additions |
| https://github.com/sveltejs/kit/pull/16868 | `sveltejs/kit` | `code_only` | `typescript` | chore: move remote plugin |
| https://github.com/sveltejs/kit/pull/16856 | `sveltejs/kit` | `code_and_docs` | `typescript` | Version Packages (next) |
| https://github.com/sveltejs/kit/pull/16790 | `sveltejs/kit` | `code_and_docs` | `typescript` | fix: make `query.live` stream teardown safe |
| https://github.com/sveltejs/kit/pull/16873 | `sveltejs/kit` | `code_and_docs` | `typescript` | chore: read build-time config from defines instead of SSROptions |
| https://github.com/sveltejs/kit/pull/16869 | `sveltejs/kit` | `code_only` | `typescript` | fix: keep the server-only import guard's manifest current |
| https://github.com/sveltejs/kit/pull/16849 | `sveltejs/kit` | `code_only` | `typescript` | test: live query teardown |
| https://github.com/sveltejs/kit/pull/16871 | `sveltejs/kit` | `code_and_docs` | `typescript` | chore: read options from one module instead of threading it through the server runtime |
| https://github.com/sveltejs/kit/pull/16665 | `sveltejs/kit` | `code_and_docs` | `typescript` | feat: add `applyReroute` helper for catch-all serverless functions |
| https://github.com/sveltejs/kit/pull/16865 | `sveltejs/kit` | `code_and_docs` | `typescript` | fix: tweak response logging for remote requests |
| https://github.com/sveltejs/kit/pull/16863 | `sveltejs/kit` | `code_only` | `typescript` | chore: move guard plugin |
| https://github.com/sveltejs/kit/pull/16858 | `sveltejs/kit` | `code_and_docs` | `typescript` | fix: route dev-server response logging through Vite's logger |
| https://github.com/sveltejs/kit/pull/16731 | `sveltejs/kit` | `code_and_docs` | `typescript` | fix: omit ISR data endpoints for server-only routes |
| https://github.com/sveltejs/kit/pull/16862 | `sveltejs/kit` | `code_only` | `typescript` | chore: resolve service worker entry once |
| https://github.com/sveltejs/svelte/pull/16070 | `sveltejs/svelte` | `code_and_docs` | `typescript` | docs: Updated docs to include information on easing functions |
| https://github.com/sveltejs/svelte/pull/18160 | `sveltejs/svelte` | `code_and_docs` | `typescript` | fix: don't apply scoped CSS class to elements inside <svelte:head> |
| https://github.com/sveltejs/svelte/pull/18390 | `sveltejs/svelte` | `code_and_docs` | `typescript` | perf: optimize simple object destructuring in @const tags |
| https://github.com/sveltejs/svelte/pull/18431 | `sveltejs/svelte` | `code_and_docs` | `typescript` | fix: don't resurrect outroing elements when an ancestor block is paused and resumed |
| https://github.com/sveltejs/svelte/pull/18444 | `sveltejs/svelte` | `code_only` | `typescript` | chore(deps-dev): bump vite from 7.3.2 to 7.3.5 |
| https://github.com/sveltejs/svelte/pull/18685 | `sveltejs/svelte` | `code_and_docs` | `typescript` | fix: preserve whitespace after inline elements when printing |
| https://github.com/sveltejs/svelte/pull/18430 | `sveltejs/svelte` | `code_and_docs` | `typescript` | fix: avoid NaN keyframe values in slide transition |
| https://github.com/sveltejs/svelte/pull/18466 | `sveltejs/svelte` | `code_and_docs` | `typescript` | fix: distinct memoizer on style/class directives |
| https://github.com/sveltejs/svelte/pull/18470 | `sveltejs/svelte` | `code_only` | `typescript` | docs: fix typo in read_version JSDoc |
| https://github.com/sveltejs/svelte/pull/18486 | `sveltejs/svelte` | `code_and_docs` | `typescript` | fix: route $derived teardown errors through invoke_error_boundary |
| https://github.com/sveltejs/svelte/pull/18667 | `sveltejs/svelte` | `code_and_docs` | `typescript` | fix: preserve CSS escape sequences when printing selectors |
| https://github.com/sveltejs/svelte/pull/18495 | `sveltejs/svelte` | `code_and_docs` | `typescript` | fix: prevent `selectedcontent` mutation from changing the selected option |
| https://github.com/sveltejs/svelte/pull/18534 | `sveltejs/svelte` | `code_and_docs` | `typescript` | docs: clarify when `$effect.pre` runs relative to DOM updates |
| https://github.com/sveltejs/svelte/pull/18585 | `sveltejs/svelte` | `code_and_docs` | `typescript` | fix: run `onDestroy` callbacks when a server render throws |
| https://github.com/sveltejs/svelte/pull/18582 | `sveltejs/svelte` | `code_and_docs` | `typescript` | fix: make template store subscriptions wait for the promise that assigns the store |
| https://github.com/sveltejs/svelte/pull/18646 | `sveltejs/svelte` | `code_and_docs` | `typescript` | fix: don't turn component instances stored in $state into state proxies |
| https://github.com/sveltejs/svelte/pull/18480 | `sveltejs/svelte` | `code_and_docs` | `typescript` | fix: warn on undeclared shorthand event handlers on svelte:window/document/body |
| https://github.com/sveltejs/svelte/pull/18593 | `sveltejs/svelte` | `code_and_docs` | `typescript` | fix: scope SSR boundary failed snippets to their boundary |
| https://github.com/sveltejs/svelte/pull/18602 | `sveltejs/svelte` | `code_and_docs` | `typescript` | perf: O(n²)→O(n) Map lookups for legacy reactive statements |
| https://github.com/sveltejs/svelte/pull/18648 | `sveltejs/svelte` | `code_and_docs` | `typescript` | feat: export RenderOutput, SyncRenderOutput, Csp and Sha256Source from svelte/server |
| https://github.com/tauri-apps/tauri/pull/15895 | `tauri-apps/tauri` | `code_and_docs` | `typescript` | feat(cli): warn when productName is left as the default (fix #14968) |
| https://github.com/tauri-apps/tauri/pull/15869 | `tauri-apps/tauri` | `code_only` | `typescript` | docs(api): clarify convertFileSrc asset protocol setup (fix #10755) |
| https://github.com/tauri-apps/tauri/pull/15887 | `tauri-apps/tauri` | `code_and_docs` | `typescript` | refactor: lock minor versions |
| https://github.com/tauri-apps/tauri/pull/15889 | `tauri-apps/tauri` | `code_only` | `typescript` | docs(api): Explicit Resource Management for `Resource` |
| https://github.com/tauri-apps/tauri/pull/14103 | `tauri-apps/tauri` | `code_and_docs` | `typescript` | fix: add ECMAScript Explicit Resource Management to Resource |
| https://github.com/tauri-apps/tauri/pull/15886 | `tauri-apps/tauri` | `code_only` | `typescript` | fix: do not close parent window when a child webview is closed |
| https://github.com/tauri-apps/tauri/pull/15883 | `tauri-apps/tauri` | `code_and_docs` | `typescript` | feat(build): add try_build_context for context-only packages |
| https://github.com/tauri-apps/tauri/pull/15882 | `tauri-apps/tauri` | `code_and_docs` | `typescript` | feat(resources): resolve resources at runtime in development |
| https://github.com/tauri-apps/tauri/pull/15880 | `tauri-apps/tauri` | `code_only` | `typescript` | fix(runtime-cef): serve custom-scheme requests that have no source browser |
| https://github.com/tauri-apps/tauri/pull/15873 | `tauri-apps/tauri` | `code_only` | `typescript` | chore(deps): Update pnpm to 11.21.0 |
| https://github.com/tauri-apps/tauri/pull/15875 | `tauri-apps/tauri` | `code_and_docs` | `typescript` | chore(deps): update rust crate png to 0.18 |
| https://github.com/tauri-apps/tauri/pull/15412 | `tauri-apps/tauri` | `code_and_docs` | `typescript` | Use workspace dependency management |
| https://github.com/tauri-apps/tauri/pull/15870 | `tauri-apps/tauri` | `code_only_tests_or_fixtures` | `typescript` | fix(ci): restore ndk symlinks on macos |
| https://github.com/tauri-apps/tauri/pull/15780 | `tauri-apps/tauri` | `code_and_docs` | `typescript` | feat(cli): warn when Java is too new for the bundled Gradle |
| https://github.com/tauri-apps/tauri/pull/15630 | `tauri-apps/tauri` | `code_and_docs` | `typescript` | fix(runtime-wry)!: query monitors on main thread from runtime handle |
| https://github.com/tauri-apps/tauri/pull/15862 | `tauri-apps/tauri` | `code_and_docs` | `typescript` | feat(android): update template to use targetSdk 37 |
| https://github.com/tauri-apps/tauri/pull/15860 | `tauri-apps/tauri` | `code_and_docs` | `typescript` | fix: menu related commands can panic |
| https://github.com/tauri-apps/tauri/pull/15828 | `tauri-apps/tauri` | `code_and_docs` | `typescript` | fix(android): update template to use gradle 9 |
| https://github.com/tauri-apps/tauri/pull/15796 | `tauri-apps/tauri` | `code_only` | `typescript` | chore(deps): update dependency rollup to v4.62.4 |
| https://github.com/tauri-apps/tauri/pull/15724 | `tauri-apps/tauri` | `code_only` | `typescript` | chore(deps): update napi-rs packages |
| https://github.com/typescript-eslint/typescript-eslint/pull/12289 | `typescript-eslint/typescript-eslint` | `code_only` | `typescript` | chore(eslint-plugin): switch auto-generated test cases to hand-written in no-unnecessary-template-expression.test.ts |
| https://github.com/typescript-eslint/typescript-eslint/pull/12291 | `typescript-eslint/typescript-eslint` | `code_only` | `typescript` | feat(rule-tester): added updates of RuleTester from upstream |
| https://github.com/typescript-eslint/typescript-eslint/pull/11324 | `typescript-eslint/typescript-eslint` | `code_only_tests_or_fixtures` | `typescript` | chore(eslint-plugin): switch auto-generated test cases to hand-written in no-unsafe-assignment.test.ts |
| https://github.com/typescript-eslint/typescript-eslint/pull/11328 | `typescript-eslint/typescript-eslint` | `code_only_tests_or_fixtures` | `typescript` | chore(eslint-plugin): switch auto-generated test cases to hand-written in ban-tslint-comment.test.ts |
| https://github.com/typescript-eslint/typescript-eslint/pull/11347 | `typescript-eslint/typescript-eslint` | `code_only` | `typescript` | chore(eslint-plugin): switch auto-generated test cases to hand-written in no-unused-expressions.test.ts |
| https://github.com/typescript-eslint/typescript-eslint/pull/11296 | `typescript-eslint/typescript-eslint` | `code_only_tests_or_fixtures` | `typescript` | chore(eslint-plugin): switch auto-generated test cases to hand-written in strict-boolean-expressions.test.ts |
| https://github.com/typescript-eslint/typescript-eslint/pull/11275 | `typescript-eslint/typescript-eslint` | `code_only_tests_or_fixtures` | `typescript` | chore(eslint-plugin): switch auto-generated test cases to hand-written in no-inferrable-types.test.ts |
| https://github.com/typescript-eslint/typescript-eslint/pull/11280 | `typescript-eslint/typescript-eslint` | `code_only_tests_or_fixtures` | `typescript` | chore(eslint-plugin): switch auto-generated test cases to hand-written in no-base-to-string.test.ts |
| https://github.com/typescript-eslint/typescript-eslint/pull/11288 | `typescript-eslint/typescript-eslint` | `code_only_tests_or_fixtures` | `typescript` | chore(eslint-plugin): switch auto-generated test cases to hand-written in prefer-readonly-parameter-types.test.ts |
| https://github.com/typescript-eslint/typescript-eslint/pull/9297 | `typescript-eslint/typescript-eslint` | `code_only` | `typescript` | fix(eslint-plugin): [strict-boolean-expressions] support branded booleans |
| https://github.com/typescript-eslint/typescript-eslint/pull/9167 | `typescript-eslint/typescript-eslint` | `code_only` | `typescript` | fix(eslint-plugin): [no-magic-numbers] fix implementation of the `ignore` option |
| https://github.com/typescript-eslint/typescript-eslint/pull/9304 | `typescript-eslint/typescript-eslint` | `code_only` | `typescript` | fix(eslint-plugin): [no-unsafe-call] differentiate a types-error any from a true any |
| https://github.com/typescript-eslint/typescript-eslint/pull/9443 | `typescript-eslint/typescript-eslint` | `code_and_docs` | `typescript` | feat(eslint-plugin): back-port new rules around empty object types from v8 |
| https://github.com/typescript-eslint/typescript-eslint/pull/12663 | `typescript-eslint/typescript-eslint` | `code_only` | `typescript` | feat(utils): support ESLint rule meta.languages |
| https://github.com/typescript-eslint/typescript-eslint/pull/12608 | `typescript-eslint/typescript-eslint` | `code_only` | `typescript` | fix(website): playground crashes on `extends` configs |
| https://github.com/typescript-eslint/typescript-eslint/pull/12739 | `typescript-eslint/typescript-eslint` | `code_only` | `typescript` | fix(eslint-plugin): [no-empty-object-type] ignore suggestions that result in invalid interfaces and export defaults |
| https://github.com/typescript-eslint/typescript-eslint/pull/7406 | `typescript-eslint/typescript-eslint` | `code_only` | `typescript` | fix(utils): add to JSONSchema4Type missing Array and Object |
| https://github.com/typescript-eslint/typescript-eslint/pull/12722 | `typescript-eslint/typescript-eslint` | `code_only` | `typescript` | chore(eslint-plugin): extract FunctionSignature and enum comparison utils |
| https://github.com/typescript-eslint/typescript-eslint/pull/12711 | `typescript-eslint/typescript-eslint` | `code_only` | `typescript` | fix(eslint-plugin): [no-unnecessary-type-assertion] prevent stack overflow in recursive types |
| https://github.com/typescript-eslint/typescript-eslint/pull/12726 | `typescript-eslint/typescript-eslint` | `code_only` | `typescript` | chore: [ci] fix nx outputs and enable snapshot checks |
| https://github.com/vitejs/vite/pull/23325 | `vitejs/vite` | `code_only` | `typescript` | chore: remove eslint comment |
| https://github.com/vitejs/vite/pull/23311 | `vitejs/vite` | `code_and_docs` | `typescript` | ci: set up bot workflow and ai policy |
| https://github.com/vitejs/vite/pull/23157 | `vitejs/vite` | `code_only_tests_or_fixtures` | `typescript` | test: add asset path replacement in `typeof` test |
| https://github.com/vitejs/vite/pull/22962 | `vitejs/vite` | `code_only` | `typescript` | refactor: use `urlId` of `import.meta.ROLLDOWN_FILE_URL` in wasm plugin |
| https://github.com/vitejs/vite/pull/23118 | `vitejs/vite` | `code_only_tests_or_fixtures` | `typescript` | test: add `renderBuiltUrl` change changes hash |
| https://github.com/vitejs/vite/pull/22894 | `vitejs/vite` | `code_only` | `typescript` | feat: use `import.meta.ROLLDOWN_FILE_URL_*` for other plugins |
| https://github.com/vitejs/vite/pull/22888 | `vitejs/vite` | `code_only` | `typescript` | feat: use `import.meta.ROLLDOWN_FILE_URL_*` for assets in JS |
| https://github.com/vitejs/vite/pull/22886 | `vitejs/vite` | `code_only` | `typescript` | refactor: exclude postfix from `__VITE_ASSET__` |
| https://github.com/vitejs/vite/pull/22280 | `vitejs/vite` | `code_only` | `typescript` | feat: searched params attached to workers are now preserved |
| https://github.com/vitejs/vite/pull/23133 | `vitejs/vite` | `code_and_docs` | `typescript` | feat: accept Rolldown watch options in `server.watch` |
| https://github.com/vitejs/vite/pull/23321 | `vitejs/vite` | `code_only_tests_or_fixtures` | `typescript` | test(hmr): skip virtual module `import.meta.hot.invalidate` test in bundled-dev |
| https://github.com/vitejs/vite/pull/23110 | `vitejs/vite` | `code_and_docs` | `typescript` | feat: add closeServer and closePreviewServer hooks |
| https://github.com/vitejs/vite/pull/22473 | `vitejs/vite` | `code_only` | `typescript` | feat(worker): remove worker chunk if it's detected that it's not referenced |
| https://github.com/vitejs/vite/pull/23183 | `vitejs/vite` | `code_only` | `typescript` | feat(css): minify style tag |
| https://github.com/vitejs/vite/pull/23185 | `vitejs/vite` | `code_and_docs` | `typescript` | feat: support subpath imports in dynamic import statements |
| https://github.com/vitejs/vite/pull/23042 | `vitejs/vite` | `code_and_docs` | `typescript` | feat(cli): support naming the CPU profile via --profile [name] |
| https://github.com/vitejs/vite/pull/23172 | `vitejs/vite` | `code_only` | `typescript` | refactor: remove HmrUrl concept |
| https://github.com/vitejs/vite/pull/23171 | `vitejs/vite` | `code_only` | `typescript` | fix(hmr): handle `import.meta.hot.invalidate` in virtual module |
| https://github.com/vitejs/vite/pull/23165 | `vitejs/vite` | `code_only` | `typescript` | fix(dev): run closeBundle after buildEnd failure |
| https://github.com/vitejs/vite/pull/23116 | `vitejs/vite` | `code_and_docs` | `typescript` | ci: setup PR-driven release |
| https://github.com/vitest-dev/vitest/pull/11031 | `vitest-dev/vitest` | `code_only` | `typescript` | fix(vm): fall back to compiling from source when a module's code cache is rejected |
| https://github.com/vitest-dev/vitest/pull/11029 | `vitest-dev/vitest` | `code_only` | `typescript` | perf(cache): hash the environment-invariant part of the fs module cache key once |
| https://github.com/vitest-dev/vitest/pull/10880 | `vitest-dev/vitest` | `code_only` | `typescript` | fix(browser): resolve `connectTimeout` from the project config (fix #10879) |
| https://github.com/vitest-dev/vitest/pull/10854 | `vitest-dev/vitest` | `code_only` | `typescript` | fix(vm): stop retaining every finished test file in vm pool workers |
| https://github.com/vitest-dev/vitest/pull/10829 | `vitest-dev/vitest` | `code_and_docs` | `typescript` | feat(vm): support `require(esm)` in vm pools |
| https://github.com/vitest-dev/vitest/pull/10841 | `vitest-dev/vitest` | `code_only` | `typescript` | test: deflake tests sharing the watch fixture |
| https://github.com/vitest-dev/vitest/pull/10842 | `vitest-dev/vitest` | `code_only` | `typescript` | fix: don't lose worker output on teardown, deflake timing-sensitive tests |
| https://github.com/vitest-dev/vitest/pull/10710 | `vitest-dev/vitest` | `code_and_docs` | `typescript` | feat: add `vitest doctor` |
| https://github.com/vitest-dev/vitest/pull/10821 | `vitest-dev/vitest` | `code_and_docs` | `typescript` | feat: print performance hints after the run (`experimental.diagnostics`) |
| https://github.com/vitest-dev/vitest/pull/10729 | `vitest-dev/vitest` | `code_only` | `typescript` | perf(browser): serve framework assets as immutable |
| https://github.com/vitest-dev/vitest/pull/10981 | `vitest-dev/vitest` | `code_only` | `typescript` | feat(ui): persist trace view selection in URL |
| https://github.com/vitest-dev/vitest/pull/11021 | `vitest-dev/vitest` | `code_only` | `typescript` | fix(browser): preserve trace popover state (fix #10906) |
| https://github.com/vitest-dev/vitest/pull/11023 | `vitest-dev/vitest` | `code_only` | `typescript` | fix(coverage): v8 to ignore Vite SSR's generated import bindings |
| https://github.com/vitest-dev/vitest/pull/11020 | `vitest-dev/vitest` | `code_only` | `typescript` | fix(worker): bind stdio's early in case overriden |
| https://github.com/vitest-dev/vitest/pull/11009 | `vitest-dev/vitest` | `code_only` | `typescript` | ci: cache `playwright install-deps` by using custom Docker image |
| https://github.com/vitest-dev/vitest/pull/6181 | `vitest-dev/vitest` | `code_only` | `typescript` | fix(spy): fix `mockImplementation` for function overload and unions |
| https://github.com/vitest-dev/vitest/pull/11014 | `vitest-dev/vitest` | `code_and_docs` | `typescript` | ci: close automated prs and issues after 1 day |
| https://github.com/vitest-dev/vitest/pull/10866 | `vitest-dev/vitest` | `code_only` | `typescript` | perf: lowers peak memory usage when using `--changed` on a large graph |
| https://github.com/vitest-dev/vitest/pull/10541 | `vitest-dev/vitest` | `code_only` | `typescript` | fix: stale mock metadata breaks automocking with isolate:false (fix #10145) |
| https://github.com/vitest-dev/vitest/pull/11010 | `vitest-dev/vitest` | `code_only` | `typescript` | ci: update agentscan |
| https://github.com/vuejs/core/pull/15329 | `vuejs/core` | `code_only` | `typescript` | perf(runtime-vapor): trim v-for hot-path allocations |
| https://github.com/vuejs/core/pull/15114 | `vuejs/core` | `code_only` | `typescript` | fix(runtime-core): restore SSR setup state when handling async setup result |
| https://github.com/vuejs/core/pull/15330 | `vuejs/core` | `code_only` | `typescript` | chore: enable pnpm trustPolicy: no-downgrade (supply-chain defense-in-depth) |
| https://github.com/vuejs/core/pull/15321 | `vuejs/core` | `code_only` | `typescript` | fix(runtime-vapor): resolve element namespace at interop boundaries |
| https://github.com/vuejs/core/pull/15319 | `vuejs/core` | `code_only` | `typescript` | fix(runtime-vapor): re-resolve transition hooks on prop change |
| https://github.com/vuejs/core/pull/15316 | `vuejs/core` | `code_only` | `typescript` | refactor(vapor): simplify template ref entry points |
| https://github.com/vuejs/core/pull/15312 | `vuejs/core` | `code_only` | `typescript` | fix(runtime-vapor): align attrs fallthrough semantics with vdom |
| https://github.com/vuejs/core/pull/15311 | `vuejs/core` | `code_only` | `typescript` | refactor(runtime-vapor): creation-time scope id model |
| https://github.com/vuejs/core/pull/14284 | `vuejs/core` | `code_only` | `typescript` | fix(runtime-vapor): Loss of css var in Teleport |
| https://github.com/vuejs/core/pull/15304 | `vuejs/core` | `code_only` | `typescript` | fix(runtime-vapor): preserve nested vdom slot content (fix #15303) |
| https://github.com/vuejs/core/pull/15293 | `vuejs/core` | `code_only` | `typescript` | fix(runtime-vapor): preserve cached input effects across nested branch teardown |
| https://github.com/vuejs/core/pull/15292 | `vuejs/core` | `code_only` | `typescript` | fix(runtime-vapor): preserve child keys in nested fragments |
| https://github.com/vuejs/core/pull/15283 | `vuejs/core` | `code_only` | `typescript` | fix(runtime-vapor): dispose component v-for item resources on removal |
| https://github.com/vuejs/core/pull/15286 | `vuejs/core` | `code_only` | `typescript` | fix(runtime-vapor): normalize declared style props (fix #15285) |
| https://github.com/vuejs/core/pull/15280 | `vuejs/core` | `code_only` | `typescript` | fix(vapor): preserve dynamic v-for slot state |
| https://github.com/vuejs/core/pull/15279 | `vuejs/core` | `code_only` | `typescript` | fix(runtime-vapor): respect inheritAttrs ownership for component roots |
| https://github.com/vuejs/core/pull/15275 | `vuejs/core` | `code_only` | `typescript` | fix(compiler-vapor): propagate component root through Transition |
| https://github.com/vuejs/core/pull/15273 | `vuejs/core` | `code_only` | `typescript` | chore(runtime-vapor): tree-shake teleport target anchor hydration |
| https://github.com/vuejs/core/pull/15272 | `vuejs/core` | `code_only` | `typescript` | fix(runtime-vapor): avoid redundant transition block resolution |
| https://github.com/vuejs/core/pull/15269 | `vuejs/core` | `code_only` | `typescript` | refactor(runtime-vapor): formalize fragment and interop boundaries |
| https://github.com/vuejs/router/pull/2780 | `vuejs/router` | `code_only` | `typescript` | fix(router): skip scroll saving for unknown pop direction (fix #1431) |
| https://github.com/vuejs/router/pull/2789 | `vuejs/router` | `code_only` | `typescript` | feat: prevent race condition dev-only error |
| https://github.com/vuejs/router/pull/2646 | `vuejs/router` | `code_only` | `typescript` | fix(unplugin): generate param types from override paths and stop inheritance on absolute overrides |
| https://github.com/vuejs/router/pull/2788 | `vuejs/router` | `code_only` | `typescript` | perf: avoid depending on the current route to resolve absolute locations |
| https://github.com/vuejs/router/pull/2785 | `vuejs/router` | `code_only` | `typescript` | build: deprecate `skipNodeModulesBundle` in favor of `deps.neverBundle: true` |
| https://github.com/vuejs/router/pull/2783 | `vuejs/router` | `code_only` | `typescript` | chore: update configuration file |
| https://github.com/vuejs/router/pull/2782 | `vuejs/router` | `code_only` | `typescript` | fix(unplugin): inherit query params and normalize params in generated types |
| https://github.com/vuejs/router/pull/2747 | `vuejs/router` | `code_only` | `typescript` | refactor: remove `@babel/generator` |
| https://github.com/vuejs/router/pull/2777 | `vuejs/router` | `code_and_docs` | `typescript` | vitepress 2 |
| https://github.com/vuejs/router/pull/2704 | `vuejs/router` | `code_only` | `typescript` | fix(history): remove visibilitychange listener to prevent focus steal… |
| https://github.com/vuejs/router/pull/2776 | `vuejs/router` | `code_only` | `typescript` | build: upgrade to vite 8 and vitest 4 |
| https://github.com/vuejs/router/pull/2769 | `vuejs/router` | `code_only` | `typescript` | perf: replace `json5` and `yaml` with `confbox` |
| https://github.com/vuejs/router/pull/2768 | `vuejs/router` | `code_only` | `typescript` | ci: bump the actions group with 2 updates |
| https://github.com/vuejs/router/pull/2765 | `vuejs/router` | `code_only` | `typescript` | ci: preview release add pm option |
| https://github.com/vuejs/router/pull/2761 | `vuejs/router` | `code_only` | `typescript` | build: include tsdown.config.ts in tsconfig |
| https://github.com/vuejs/router/pull/2764 | `vuejs/router` | `code_only` | `typescript` | docs: fix `@see` link to `MatcherPattern` in param parsers |
| https://github.com/vuejs/router/pull/2759 | `vuejs/router` | `code_only` | `typescript` | feat(volar): narrow `typeof useRoute` in a type context |
| https://github.com/vuejs/router/pull/2753 | `vuejs/router` | `code_only` | `typescript` | feat(unplugin): don't crash on duplicate definePage() calls |
| https://github.com/vuejs/router/pull/2752 | `vuejs/router` | `code_only` | `typescript` | fix(types): allow unsetting a route name with `false` in `EditableTreeNode` |
| https://github.com/vuejs/router/pull/2751 | `vuejs/router` | `code_only` | `typescript` | chore: move all pnpm settings to `pnpm-workspace.yaml` |
| https://github.com/webpack/webpack/pull/21795 | `webpack/webpack` | `code_only` | `typescript` | Revert "chore(deps): bump changesets/action (#21764)" |
| https://github.com/webpack/webpack/pull/21794 | `webpack/webpack` | `code_only` | `typescript` | chore: fix invalid JSDoc |
| https://github.com/webpack/webpack/pull/21764 | `webpack/webpack` | `code_only` | `typescript` | chore(deps): bump changesets/action from 1.9.0 to 2.1.0 in the dependencies group across 1 directory |
| https://github.com/webpack/webpack/pull/21788 | `webpack/webpack` | `code_and_docs` | `typescript` | feat(esm): bake the prefetch/preload url of a javascript chunk |
| https://github.com/webpack/webpack/pull/21787 | `webpack/webpack` | `code_and_docs` | `typescript` | fix(html): parse and print what the spec says around frameset, select and quirks |
| https://github.com/webpack/webpack/pull/21786 | `webpack/webpack` | `code_only` | `typescript` | fix(performance): read an alias's evidence from the request, not the module |
| https://github.com/webpack/webpack/pull/21784 | `webpack/webpack` | `code_and_docs` | `typescript` | feat(css): shorten custom property values behind an option |
| https://github.com/webpack/webpack/pull/21781 | `webpack/webpack` | `code_and_docs` | `typescript` | feat(analyzable): bake the stylesheet url a css chunk loads |
| https://github.com/webpack/webpack/pull/21782 | `webpack/webpack` | `code_only` | `typescript` | docs: retain dotenv and dotenv-expand license notices in DotenvPlugin |
| https://github.com/webpack/webpack/pull/21770 | `webpack/webpack` | `code_and_docs` | `typescript` | feat: generalize umdSapUiDefine into output.library.umdAmdContainers |
| https://github.com/webpack/webpack/pull/21780 | `webpack/webpack` | `code_and_docs` | `typescript` | feat(externals): provide the original request of a context module element |
| https://github.com/webpack/webpack/pull/21779 | `webpack/webpack` | `code_only` | `typescript` | perf(performance): ask each chunk once what is loaded where it runs |
| https://github.com/webpack/webpack/pull/21778 | `webpack/webpack` | `code_only` | `typescript` | fix(performance): judge a dynamic import by every path that can load it |
| https://github.com/webpack/webpack/pull/21777 | `webpack/webpack` | `code_only` | `typescript` | fix(performance): name the request cap that actually refused a split |
| https://github.com/webpack/webpack/pull/21773 | `webpack/webpack` | `code_and_docs` | `typescript` | feat(css): minify custom-property whitespace, merge longhands past a nested rule |
| https://github.com/webpack/webpack/pull/21768 | `webpack/webpack` | `code_only` | `typescript` | perf: remove props with inlined value when rendering a ns obj |
| https://github.com/webpack/webpack/pull/21772 | `webpack/webpack` | `code_and_docs` | `typescript` | feat(analyzable): bake a lazy context's chunk imports into its map |
| https://github.com/webpack/webpack/pull/21762 | `webpack/webpack` | `code_and_docs` | `typescript` | feat(css): drop repeated rules, gather named layer blocks, minify vendor spellings |
| https://github.com/webpack/webpack/pull/21759 | `webpack/webpack` | `code_and_docs` | `typescript` | refactor(performance): fold circular-dependency hints into one SCC scan |
| https://github.com/webpack/webpack/pull/21760 | `webpack/webpack` | `code_and_docs` | `typescript` | feat(analyzable): bake a wasm url under a relative public path |
| https://github.com/yarnpkg/berry/pull/7208 | `yarnpkg/berry` | `code_only` | `typescript` | chore(deps): upgrade `sigstore` to v4 |
| https://github.com/yarnpkg/berry/pull/6768 | `yarnpkg/berry` | `code_only` | `typescript` | feat: bump `js-yaml` to v4 |
| https://github.com/yarnpkg/berry/pull/7218 | `yarnpkg/berry` | `code_only` | `typescript` | Version: Reimplement `yarn version` and `yarn version apply` |
| https://github.com/yarnpkg/berry/pull/7209 | `yarnpkg/berry` | `code_only` | `typescript` | Skip OTP prompts in non-TTY mode |
| https://github.com/yarnpkg/berry/pull/7205 | `yarnpkg/berry` | `code_only` | `typescript` | fix(plugin-npm): resolve "*" to prereleases when no stable version exists |
| https://github.com/yarnpkg/berry/pull/7228 | `yarnpkg/berry` | `code_only` | `typescript` | E2E: Fix most E2E tests |
| https://github.com/yarnpkg/berry/pull/7220 | `yarnpkg/berry` | `code_only` | `typescript` | Docs: fix catalog schema |
| https://github.com/yarnpkg/berry/pull/7224 | `yarnpkg/berry` | `code_only` | `typescript` | CI: Aggregate acceptance test matrix result |
| https://github.com/yarnpkg/berry/pull/7232 | `yarnpkg/berry` | `code_only` | `typescript` | fix(extensions): declare the `typescript` peer for the Volar packages |
| https://github.com/yarnpkg/berry/pull/7223 | `yarnpkg/berry` | `code_only` | `typescript` | perf(nm): avoid redundant package map sorting |
| https://github.com/yarnpkg/berry/pull/7203 | `yarnpkg/berry` | `code_only` | `typescript` | fix: preserve root path in tryWorkspaceByCwd when cwd is / |
| https://github.com/yarnpkg/berry/pull/7189 | `yarnpkg/berry` | `code_only` | `typescript` | fix: make sure hoistingLimits are not bypassed |
| https://github.com/yarnpkg/berry/pull/7216 | `yarnpkg/berry` | `code_only` | `typescript` | fix(nm): prefer direct dependency binaries |
| https://github.com/yarnpkg/berry/pull/7184 | `yarnpkg/berry` | `code_only` | `typescript` | Adds support for package map generation |
| https://github.com/yarnpkg/berry/pull/7190 | `yarnpkg/berry` | `code_only` | `typescript` | Handle optional compat patch failures for TypeScript 7 |
| https://github.com/yarnpkg/berry/pull/7156 | `yarnpkg/berry` | `code_only` | `typescript` | feat(plugin-npm): allow npmMinimalAgeGate per npmScope |
| https://github.com/yarnpkg/berry/pull/7181 | `yarnpkg/berry` | `code_only` | `typescript` | Docs: fix npmMinimalAgeGate default |
| https://github.com/yarnpkg/berry/pull/7168 | `yarnpkg/berry` | `code_only` | `typescript` | fix: explain peer-default dependencies in why |
| https://github.com/yarnpkg/berry/pull/7179 | `yarnpkg/berry` | `code_only` | `typescript` | fix: add catalog settings to yarnrc schema |
| https://github.com/yarnpkg/berry/pull/7125 | `yarnpkg/berry` | `code_only` | `typescript` | docs: fix npmMinimalAgeGate default value. |

## Reject Summary Sample

| Repository | PR | Reason | Bucket |
| --- | ---: | --- | --- |
| `microsoft/typescript-go` | `4921` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4701` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4364` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4712` | `too_many_changed_files` | `code_and_docs` |
| `microsoft/typescript-go` | `4775` | `too_many_changed_files` | `code_only` |
| `microsoft/typescript-go` | `4849` | `too_many_changed_files` | `code_only` |
| `microsoft/typescript-go` | `1966` | `not_merged` | `None` |
| `microsoft/typescript-go` | `3331` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4919` | `docs_only_excluded` | `docs_only` |
| `microsoft/typescript-go` | `4858` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4914` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4911` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4903` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4902` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4865` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4846` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4841` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4779` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4733` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4726` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4716` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4674` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4666` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4653` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4600` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4597` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4596` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4555` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4496` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4446` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4440` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4422` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4418` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4297` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4211` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4200` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4197` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4102` | `not_merged` | `None` |
| `microsoft/typescript-go` | `3996` | `not_merged` | `None` |
| `microsoft/typescript-go` | `3943` | `not_merged` | `None` |
| `microsoft/typescript-go` | `3935` | `not_merged` | `None` |
| `microsoft/typescript-go` | `3728` | `not_merged` | `None` |
| `microsoft/typescript-go` | `3726` | `not_merged` | `None` |
| `microsoft/typescript-go` | `3690` | `not_merged` | `None` |
| `microsoft/typescript-go` | `3619` | `not_merged` | `None` |
| `microsoft/typescript-go` | `3385` | `not_merged` | `None` |
| `microsoft/typescript-go` | `3369` | `not_merged` | `None` |
| `microsoft/typescript-go` | `3362` | `not_merged` | `None` |
| `microsoft/typescript-go` | `3297` | `not_merged` | `None` |
| `microsoft/typescript-go` | `717` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4877` | `already_collected` | `None` |
| `microsoft/typescript-go` | `4917` | `already_collected` | `None` |
| `microsoft/typescript-go` | `4915` | `too_large_patch` | `code_and_docs` |
| `microsoft/typescript-go` | `4900` | `already_collected` | `None` |
| `microsoft/typescript-go` | `4723` | `already_collected` | `None` |
| `microsoft/typescript-go` | `4909` | `already_collected` | `None` |
| `microsoft/typescript-go` | `4889` | `already_collected` | `None` |
| `microsoft/typescript-go` | `4336` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4852` | `too_many_changed_files` | `code_only` |
| `microsoft/typescript-go` | `4248` | `not_merged` | `None` |
| `microsoft/typescript-go` | `3826` | `not_merged` | `None` |
| `microsoft/typescript-go` | `3630` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4836` | `already_collected` | `None` |
| `microsoft/typescript-go` | `4442` | `already_collected` | `None` |
| `microsoft/typescript-go` | `4913` | `already_collected` | `None` |
| `microsoft/typescript-go` | `4650` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4533` | `already_collected` | `None` |
| `microsoft/typescript-go` | `4540` | `already_collected` | `None` |
| `microsoft/typescript-go` | `4786` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4274` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4599` | `already_collected` | `None` |
| `microsoft/typescript-go` | `4791` | `already_collected` | `None` |
| `microsoft/typescript-go` | `4592` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4552` | `already_collected` | `None` |
| `microsoft/typescript-go` | `4912` | `not_merged` | `None` |
| `microsoft/typescript-go` | `3663` | `already_collected` | `None` |
| `microsoft/typescript-go` | `4450` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4449` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4682` | `already_collected` | `None` |
| `microsoft/typescript-go` | `4700` | `already_collected` | `None` |
| `microsoft/typescript-go` | `4803` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4564` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4784` | `already_collected` | `None` |
| `microsoft/typescript-go` | `3515` | `already_collected` | `None` |
| `microsoft/typescript-go` | `4910` | `already_collected` | `None` |
| `microsoft/typescript-go` | `4703` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4741` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4530` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4907` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4839` | `already_collected` | `None` |
| `microsoft/typescript-go` | `4906` | `already_collected` | `None` |
| `microsoft/typescript-go` | `4598` | `already_collected` | `None` |
| `microsoft/typescript-go` | `4847` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4905` | `not_merged` | `None` |
| `microsoft/typescript-go` | `3375` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4343` | `not_merged` | `None` |
| `microsoft/typescript-go` | `3720` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4829` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4551` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4646` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4855` | `not_merged` | `None` |
| `microsoft/typescript-go` | `3949` | `too_many_changed_files` | `code_only` |
| `microsoft/typescript-go` | `4873` | `already_collected` | `None` |
| `microsoft/typescript-go` | `4603` | `already_collected` | `None` |
| `microsoft/typescript-go` | `4685` | `already_collected` | `None` |
| `microsoft/typescript-go` | `4409` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4268` | `not_merged` | `None` |
| `microsoft/typescript-go` | `2908` | `already_collected` | `None` |
| `microsoft/typescript-go` | `3990` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4800` | `already_collected` | `None` |
| `microsoft/typescript-go` | `4623` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4676` | `already_collected` | `None` |
| `microsoft/typescript-go` | `3840` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4605` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4808` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4649` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4898` | `already_collected` | `None` |
| `microsoft/typescript-go` | `4328` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4670` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4756` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4730` | `not_merged` | `None` |
| `microsoft/typescript-go` | `3277` | `not_merged` | `None` |
| `microsoft/typescript-go` | `3871` | `already_collected` | `None` |
| `microsoft/typescript-go` | `4816` | `not_merged` | `None` |
| `microsoft/typescript-go` | `3989` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4881` | `already_collected` | `None` |
| `microsoft/typescript-go` | `4160` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4832` | `already_collected` | `None` |
| `microsoft/typescript-go` | `2944` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4734` | `already_collected` | `None` |
| `microsoft/typescript-go` | `4729` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4695` | `already_collected` | `None` |
| `microsoft/typescript-go` | `4835` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4821` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4812` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4810` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4772` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4769` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4721` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4698` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4693` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4668` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4667` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4570` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4482` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4444` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4412` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4158` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4270` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4266` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4003` | `not_merged` | `None` |
| `microsoft/typescript-go` | `3987` | `not_merged` | `None` |
| `microsoft/typescript-go` | `3738` | `not_merged` | `None` |
| `microsoft/typescript-go` | `3706` | `not_merged` | `None` |
| `microsoft/typescript-go` | `3252` | `not_merged` | `None` |
| `microsoft/typescript-go` | `3228` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4870` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4896` | `already_collected` | `None` |
| `microsoft/typescript-go` | `3271` | `not_merged` | `None` |
| `microsoft/typescript-go` | `3432` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4112` | `not_merged` | `None` |
| `microsoft/typescript-go` | `3309` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4401` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4767` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4365` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4515` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4894` | `already_collected` | `None` |
| `microsoft/typescript-go` | `4240` | `already_collected` | `None` |
| `microsoft/typescript-go` | `3264` | `not_merged` | `None` |
| `microsoft/typescript-go` | `3220` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4843` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4696` | `not_merged` | `None` |
| `microsoft/typescript-go` | `2602` | `not_merged` | `None` |
| `microsoft/typescript-go` | `2417` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4430` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4007` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4714` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4887` | `already_collected` | `None` |
| `microsoft/typescript-go` | `4901` | `already_collected` | `None` |
| `microsoft/typescript-go` | `4866` | `already_collected` | `None` |
| `microsoft/typescript-go` | `4833` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4828` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4762` | `already_collected` | `None` |
| `microsoft/typescript-go` | `3880` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4840` | `not_merged` | `None` |
| `microsoft/typescript-go` | `3627` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4407` | `too_many_changed_files` | `code_only` |
| `microsoft/typescript-go` | `4897` | `already_collected` | `None` |
| `microsoft/typescript-go` | `4893` | `already_collected` | `None` |
| `microsoft/typescript-go` | `4313` | `already_collected` | `None` |
| `microsoft/typescript-go` | `4888` | `already_collected` | `None` |
| `microsoft/typescript-go` | `4885` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4884` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4883` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4882` | `not_merged` | `None` |
| `microsoft/typescript-go` | `4218` | `already_collected` | `None` |
| `microsoft/typescript-go` | `4891` | `already_collected` | `None` |
| `microsoft/typescript-go` | `4825` | `already_collected` | `None` |
| `microsoft/typescript-go` | `2914` | `already_collected` | `None` |
| `microsoft/typescript-go` | `4421` | `docs_only_excluded` | `docs_only` |