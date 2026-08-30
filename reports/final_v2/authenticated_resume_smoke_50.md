# DocGuard Real PR Seed Collector Report

This report summarizes neutral repo-based sampling of merged public GitHub PRs.

The collector does not assign gold labels and does not decide whether documentation should be updated.
It only creates seed PR URLs for the later candidate builder and manual validation workflow.

- Repositories scanned: `769`
- Seeds accepted: `50`
- Rejected/skipped PRs: `35`
- Acquisition status: `complete`
- Requirements satisfied: `True`
- Target observed/requested: `50` / `50`
- Target deficit: `0`
- Minimum language deficits: `{}`
- Collector bucket counts: `{'code_only': 50}`
- Language hint counts: `{'typescript': 50}`
- Repository counts per language: `{'typescript': 1}`
- Candidate bucket counts per language: `{'typescript': {'code_only': 50}}`
- Reject reason counts: `{'not_merged': 6, 'already_collected': 20, 'other_or_binary_only_excluded': 9}`

## Methodological Boundary

- This is real public GitHub PR sampling.
- No synthetic examples are generated.
- No final labels are assigned here.
- `collector_bucket` is audit metadata for balancing and review planning, not a model label.
- Final evaluation must use only the safe fields produced later by the candidate builder.

## Accepted Seeds

| PR | Repository | Bucket | Language hint | Title |
| --- | --- | --- | --- | --- |
| https://github.com/1111mp/nvm-desktop/pull/385 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update dependency shadcn to v4.16.1 |
| https://github.com/1111mp/nvm-desktop/pull/384 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update npm dependencies |
| https://github.com/1111mp/nvm-desktop/pull/382 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update dependency node to v24.18.1 |
| https://github.com/1111mp/nvm-desktop/pull/381 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update dependency motion to v12.43.0 |
| https://github.com/1111mp/nvm-desktop/pull/380 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update npm dependencies |
| https://github.com/1111mp/nvm-desktop/pull/379 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): lock file maintenance |
| https://github.com/1111mp/nvm-desktop/pull/378 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): lock file maintenance |
| https://github.com/1111mp/nvm-desktop/pull/376 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update npm dependencies |
| https://github.com/1111mp/nvm-desktop/pull/375 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update dependency undici to v8.9.0 |
| https://github.com/1111mp/nvm-desktop/pull/374 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update dependency shadcn to v4.14.1 |
| https://github.com/1111mp/nvm-desktop/pull/373 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update dependency lucide-react to v1.26.0 |
| https://github.com/1111mp/nvm-desktop/pull/372 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update dependency shadcn to v4.14.0 |
| https://github.com/1111mp/nvm-desktop/pull/370 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update dependency oxlint-tsgolint to v7 |
| https://github.com/1111mp/nvm-desktop/pull/371 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update dependency oxfmt to ^0.60.0 |
| https://github.com/1111mp/nvm-desktop/pull/369 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update npm dependencies to v19.2.8 |
| https://github.com/1111mp/nvm-desktop/pull/368 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update dependency undici to v8.8.0 |
| https://github.com/1111mp/nvm-desktop/pull/367 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update dependency @tauri-apps/plugin-dialog to v2.7.2 |
| https://github.com/1111mp/nvm-desktop/pull/366 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update dependency shadcn to v4.13.1 |
| https://github.com/1111mp/nvm-desktop/pull/365 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update dependency lucide-react to v1.25.0 |
| https://github.com/1111mp/nvm-desktop/pull/364 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update dependency oxlint-tsgolint to ^0.25.0 |
| https://github.com/1111mp/nvm-desktop/pull/363 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update dependency vite to v8.1.5 |
| https://github.com/1111mp/nvm-desktop/pull/362 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update dependency oxfmt to ^0.59.0 |
| https://github.com/1111mp/nvm-desktop/pull/360 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update actions/setup-node action to v7 |
| https://github.com/1111mp/nvm-desktop/pull/357 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): lock file maintenance |
| https://github.com/1111mp/nvm-desktop/pull/355 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update npm dependencies |
| https://github.com/1111mp/nvm-desktop/pull/354 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update dependency vite to v8.1.4 |
| https://github.com/1111mp/nvm-desktop/pull/353 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update dependency typescript to v7 |
| https://github.com/1111mp/nvm-desktop/pull/352 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update dependency i18next to v26.3.5 |
| https://github.com/1111mp/nvm-desktop/pull/351 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update dependency @types/node to v25.9.5 |
| https://github.com/1111mp/nvm-desktop/pull/350 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update dependency oxfmt to ^0.58.0 |
| https://github.com/1111mp/nvm-desktop/pull/348 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): lock file maintenance |
| https://github.com/1111mp/nvm-desktop/pull/346 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update dependency undici to v8.7.0 |
| https://github.com/1111mp/nvm-desktop/pull/345 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update dependency shadcn to v4.13.0 |
| https://github.com/1111mp/nvm-desktop/pull/344 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update dependency undici to v8.6.0 |
| https://github.com/1111mp/nvm-desktop/pull/343 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update dependency vite to v8.1.3 |
| https://github.com/1111mp/nvm-desktop/pull/342 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update dependency lucide-react to v1.23.0 |
| https://github.com/1111mp/nvm-desktop/pull/341 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update npm dependencies |
| https://github.com/1111mp/nvm-desktop/pull/340 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update dependency oxfmt to ^0.57.0 |
| https://github.com/1111mp/nvm-desktop/pull/338 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update npm dependencies |
| https://github.com/1111mp/nvm-desktop/pull/339 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update tauri-apps/tauri-action action to v1 |
| https://github.com/1111mp/nvm-desktop/pull/337 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): lock file maintenance |
| https://github.com/1111mp/nvm-desktop/pull/335 | `1111mp/nvm-desktop` | `code_only` | `typescript` | Handle embedded server bind failures |
| https://github.com/1111mp/nvm-desktop/pull/334 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update dependency shadcn to v4.12.0 |
| https://github.com/1111mp/nvm-desktop/pull/333 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update dependency i18next to v26.3.3 |
| https://github.com/1111mp/nvm-desktop/pull/332 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update dependency shadcn to v4.11.1 |
| https://github.com/1111mp/nvm-desktop/pull/331 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update dependency motion to v12.42.0 |
| https://github.com/1111mp/nvm-desktop/pull/330 | `1111mp/nvm-desktop` | `code_only` | `typescript` | Fix Windows Node extraction rename |
| https://github.com/1111mp/nvm-desktop/pull/329 | `1111mp/nvm-desktop` | `code_only` | `typescript` | Fix Node extraction rename handling on Windows |
| https://github.com/1111mp/nvm-desktop/pull/328 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update npm dependencies |
| https://github.com/1111mp/nvm-desktop/pull/327 | `1111mp/nvm-desktop` | `code_only` | `typescript` | chore(deps): update npm dependencies |

## Reject Summary Sample

| Repository | PR | Reason | Bucket |
| --- | ---: | --- | --- |
| `0xradikal/free-v2ray-configs` | `4` | `not_merged` | `None` |
| `0xradikal/free-v2ray-configs` | `3` | `not_merged` | `None` |
| `0xradikal/free-v2ray-configs` | `5` | `not_merged` | `None` |
| `0xradikal/free-v2ray-configs` | `2` | `not_merged` | `None` |
| `0xradikal/free-v2ray-configs` | `6` | `not_merged` | `None` |
| `1111mp/nvm-desktop` | `411` | `already_collected` | `None` |
| `1111mp/nvm-desktop` | `410` | `not_merged` | `None` |
| `1111mp/nvm-desktop` | `407` | `already_collected` | `None` |
| `1111mp/nvm-desktop` | `409` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `1111mp/nvm-desktop` | `408` | `already_collected` | `None` |
| `1111mp/nvm-desktop` | `406` | `already_collected` | `None` |
| `1111mp/nvm-desktop` | `405` | `already_collected` | `None` |
| `1111mp/nvm-desktop` | `404` | `already_collected` | `None` |
| `1111mp/nvm-desktop` | `403` | `already_collected` | `None` |
| `1111mp/nvm-desktop` | `402` | `already_collected` | `None` |
| `1111mp/nvm-desktop` | `400` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `1111mp/nvm-desktop` | `401` | `already_collected` | `None` |
| `1111mp/nvm-desktop` | `398` | `already_collected` | `None` |
| `1111mp/nvm-desktop` | `397` | `already_collected` | `None` |
| `1111mp/nvm-desktop` | `390` | `already_collected` | `None` |
| `1111mp/nvm-desktop` | `396` | `already_collected` | `None` |
| `1111mp/nvm-desktop` | `395` | `already_collected` | `None` |
| `1111mp/nvm-desktop` | `393` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `1111mp/nvm-desktop` | `394` | `already_collected` | `None` |
| `1111mp/nvm-desktop` | `392` | `already_collected` | `None` |
| `1111mp/nvm-desktop` | `391` | `already_collected` | `None` |
| `1111mp/nvm-desktop` | `389` | `already_collected` | `None` |
| `1111mp/nvm-desktop` | `388` | `already_collected` | `None` |
| `1111mp/nvm-desktop` | `386` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `1111mp/nvm-desktop` | `387` | `already_collected` | `None` |
| `1111mp/nvm-desktop` | `377` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `1111mp/nvm-desktop` | `356` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `1111mp/nvm-desktop` | `349` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `1111mp/nvm-desktop` | `347` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `1111mp/nvm-desktop` | `336` | `other_or_binary_only_excluded` | `other_or_binary_only` |