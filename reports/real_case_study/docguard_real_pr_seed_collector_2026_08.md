# DocGuard Real PR Seed Collector Report

This report summarizes neutral repo-based sampling of merged public GitHub PRs.

The collector does not assign gold labels and does not decide whether documentation should be updated.
It only creates seed PR URLs for the later candidate builder and manual validation workflow.

- Repositories scanned: `5`
- Seeds accepted: `30`
- Rejected/skipped PRs: `25`
- Collector bucket counts: `{'code_and_docs': 23, 'code_only': 7}`
- Language hint counts: `{'typescript': 26, 'python': 4}`
- Reject reason counts: `{'docs_only_excluded': 13, 'too_many_changed_files': 3, 'not_merged': 5, 'too_large_patch': 2, 'other_or_binary_only_excluded': 2}`

## Methodological Boundary

- This is real public GitHub PR sampling.
- No synthetic examples are generated.
- No final labels are assigned here.
- `collector_bucket` is audit metadata for balancing and review planning, not a model label.
- Final evaluation must use only the safe fields produced later by the candidate builder.

## Accepted Seeds

| PR | Repository | Bucket | Language hint | Title |
| --- | --- | --- | --- | --- |
| https://github.com/ragpark/controltower/pull/14 | `ragpark/controltower` | `code_and_docs` | `typescript` | ENG-1102, ENG-1104: Duplicate order diagnostics and resolution |
| https://github.com/ragpark/controltower/pull/6 | `ragpark/controltower` | `code_only` | `typescript` | Show order trend as stacked bars with range-scoped headline metrics |
| https://github.com/ragpark/controltower/pull/5 | `ragpark/controltower` | `code_only` | `typescript` | Make the upload picker follow the selected source, not assume CSV |
| https://github.com/ragpark/controltower/pull/4 | `ragpark/controltower` | `code_and_docs` | `typescript` | Ingest the daily provisioning failure report and route ownership |
| https://github.com/ragpark/controltower/pull/3 | `ragpark/controltower` | `code_only` | `typescript` | Detect the CSV delimiter instead of blaming the column mapping |
| https://github.com/ragpark/controltower/pull/2 | `ragpark/controltower` | `code_and_docs` | `typescript` | Align ingestion to the ActiveHub export schema and fix container/mapping defects |
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
| https://github.com/torbido-hq/cicerone/pull/112 | `torbido-hq/cicerone` | `code_and_docs` | `python` | fix: load Google Analytics only after Accept |
| https://github.com/torbido-hq/cicerone/pull/107 | `torbido-hq/cicerone` | `code_and_docs` | `python` | Add custom consent banner and Consent Mode v2 on cicerone.dev |
| https://github.com/torbido-hq/cicerone/pull/97 | `torbido-hq/cicerone` | `code_and_docs` | `python` | Add PyPI package and cicerone CLI |
| https://github.com/torbido-hq/cicerone/pull/101 | `torbido-hq/cicerone` | `code_and_docs` | `python` | feat(website): static articles at /articles/, hidden until a post exists |

## Reject Summary Sample

| Repository | PR | Reason | Bucket |
| --- | ---: | --- | --- |
| `ragpark/controltower` | `15` | `docs_only_excluded` | `docs_only` |
| `ragpark/controltower` | `13` | `docs_only_excluded` | `docs_only` |
| `ragpark/controltower` | `12` | `docs_only_excluded` | `docs_only` |
| `ragpark/controltower` | `11` | `docs_only_excluded` | `docs_only` |
| `ragpark/controltower` | `10` | `docs_only_excluded` | `docs_only` |
| `ragpark/controltower` | `9` | `docs_only_excluded` | `docs_only` |
| `ragpark/controltower` | `8` | `docs_only_excluded` | `docs_only` |
| `ragpark/controltower` | `7` | `docs_only_excluded` | `docs_only` |
| `ragpark/controltower` | `1` | `too_many_changed_files` | `code_and_docs` |
| `eclipsefdn-ai-registry/ai-registry-core` | `80` | `not_merged` | `None` |
| `eclipsefdn-ai-registry/ai-registry-core` | `71` | `not_merged` | `None` |
| `eclipsefdn-ai-registry/ai-registry-core` | `81` | `too_large_patch` | `code_only` |
| `eclipsefdn-ai-registry/ai-registry-core` | `79` | `too_large_patch` | `code_and_docs` |
| `eclipsefdn-ai-registry/ai-registry-core` | `54` | `not_merged` | `None` |
| `eclipsefdn-ai-registry/ai-registry-core` | `58` | `not_merged` | `None` |
| `eclipsefdn-ai-registry/ai-registry-core` | `53` | `not_merged` | `None` |
| `torbido-hq/cicerone` | `113` | `docs_only_excluded` | `docs_only` |
| `torbido-hq/cicerone` | `111` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `torbido-hq/cicerone` | `108` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `torbido-hq/cicerone` | `106` | `docs_only_excluded` | `docs_only` |
| `torbido-hq/cicerone` | `104` | `too_many_changed_files` | `code_and_docs` |
| `torbido-hq/cicerone` | `103` | `docs_only_excluded` | `docs_only` |
| `torbido-hq/cicerone` | `105` | `docs_only_excluded` | `docs_only` |
| `torbido-hq/cicerone` | `102` | `docs_only_excluded` | `docs_only` |
| `torbido-hq/cicerone` | `98` | `too_many_changed_files` | `code_and_docs` |