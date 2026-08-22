# DocGuard Real GitHub PR Candidate Dataset Builder Report

This report describes a real public GitHub PR candidate dataset created for later manual validation.
The builder does not assign final gold labels and does not use synthetic data.

- Seed input: `data\external\project_case_study\pr_candidate_seeds_collected_v1.jsonl`
- Candidate output: `data\external\project_case_study\real_pr_candidates_collected_v1.jsonl`
- Accepted candidate records: `30`
- Rejected seed records: `0`

## Leakage Policy

Allowed model input fields:

- `language`
- `code_changed_files`
- `code_diff_excerpt`
- `docs_before_excerpt`

Audit-only fields:

- `source_url`
- `repository`
- `pr_number`
- `pr_title`
- `pr_state`
- `merged_at`
- `base_sha`
- `head_sha`
- `changed_files`
- `docs_changed_files`
- `docs_diff_excerpt`
- `docs_after_excerpt`
- `gold_docs_update_required`
- `gold_doc_category`
- `gold_target_doc_file`
- `gold_target_section`
- `gold_patch_summary`
- `label_confidence`
- `manual_label_notes`
- `candidate_evidence`

## Candidate Counts

- Candidate type counts: `{'code_and_docs_changed_needs_manual_validation': 23, 'code_only_needs_manual_validation': 7}`
- Language counts: `{'python': 4, 'typescript': 26}`
- Label confidence counts: `{'needs_manual_review': 30}`

## Accepted Candidates

| Case | Repository | PR | Language | Code files | Docs files | Candidate type | Title |
| --- | --- | ---: | --- | ---: | ---: | --- | --- |
| `GH-CAND-0001` | `ragpark/controltower` | `14` | `typescript` | `15` | `1` | `code_and_docs_changed_needs_manual_validation` | ENG-1102, ENG-1104: Duplicate order diagnostics and resolution |
| `GH-CAND-0002` | `ragpark/controltower` | `6` | `typescript` | `11` | `0` | `code_only_needs_manual_validation` | Show order trend as stacked bars with range-scoped headline metrics |
| `GH-CAND-0003` | `ragpark/controltower` | `5` | `typescript` | `9` | `0` | `code_only_needs_manual_validation` | Make the upload picker follow the selected source, not assume CSV |
| `GH-CAND-0004` | `ragpark/controltower` | `4` | `typescript` | `36` | `1` | `code_and_docs_changed_needs_manual_validation` | Ingest the daily provisioning failure report and route ownership |
| `GH-CAND-0005` | `ragpark/controltower` | `3` | `typescript` | `5` | `0` | `code_only_needs_manual_validation` | Detect the CSV delimiter instead of blaming the column mapping |
| `GH-CAND-0006` | `ragpark/controltower` | `2` | `typescript` | `25` | `5` | `code_and_docs_changed_needs_manual_validation` | Align ingestion to the ActiveHub export schema and fix container/mapping defects |
| `GH-CAND-0007` | `d-hinders/Haven-AI` | `1783` | `typescript` | `13` | `2` | `code_and_docs_changed_needs_manual_validation` | chore(release): bump all published packages to 0.1.29-alpha.0 |
| `GH-CAND-0008` | `d-hinders/Haven-AI` | `1782` | `typescript` | `9` | `1` | `code_and_docs_changed_needs_manual_validation` | fix(backend): a no-database test run fails, and says what it skipped after the summary (#1763) |
| `GH-CAND-0009` | `d-hinders/Haven-AI` | `1781` | `typescript` | `3` | `1` | `code_and_docs_changed_needs_manual_validation` | test(frontend): anchor the mobile-shell guards against the viewport (#1779) |
| `GH-CAND-0010` | `d-hinders/Haven-AI` | `1780` | `typescript` | `18` | `2` | `code_and_docs_changed_needs_manual_validation` | feat(connect): resolve the runtime itself — agent self-report, installed-client prompt, real failure vocabulary (#1719) |
| `GH-CAND-0011` | `d-hinders/Haven-AI` | `1778` | `typescript` | `2` | `1` | `code_and_docs_changed_needs_manual_validation` | fix(frontend): give the mobile sidebar toggle a 44px tap target without moving a pixel (#1766) |
| `GH-CAND-0012` | `d-hinders/Haven-AI` | `1775` | `typescript` | `4` | `1` | `code_and_docs_changed_needs_manual_validation` | fix(frontend): stop /transactions clipping 106px of its table on mobile (#1772) |
| `GH-CAND-0013` | `d-hinders/Haven-AI` | `1776` | `typescript` | `7` | `2` | `code_and_docs_changed_needs_manual_validation` | test(frontend): make the horizontal-overflow guard able to fail inside the app shell (#1771) |
| `GH-CAND-0014` | `d-hinders/Haven-AI` | `1770` | `typescript` | `5` | `3` | `code_and_docs_changed_needs_manual_validation` | ci(frontend): gate every PR on a real mobile viewport (#1768) |
| `GH-CAND-0015` | `d-hinders/Haven-AI` | `1769` | `typescript` | `21` | `2` | `code_and_docs_changed_needs_manual_validation` | fix(frontend): make the mobile navigation toggle reachable, on a named z-index scale (#1749) |
| `GH-CAND-0016` | `d-hinders/Haven-AI` | `1765` | `typescript` | `10` | `4` | `code_and_docs_changed_needs_manual_validation` | fix(passport): a re-mint requires positive evidence the prior attest is dead (#1745) |
| `GH-CAND-0017` | `eclipsefdn-ai-registry/ai-registry-core` | `88` | `typescript` | `5` | `0` | `code_only_needs_manual_validation` | Extend trust delegation to Agent Plugins and A2A agents |
| `GH-CAND-0018` | `eclipsefdn-ai-registry/ai-registry-core` | `87` | `typescript` | `9` | `5` | `code_and_docs_changed_needs_manual_validation` | Add per-type and per-organization JSON feeds, with an org view page |
| `GH-CAND-0019` | `eclipsefdn-ai-registry/ai-registry-core` | `85` | `typescript` | `15` | `8` | `code_and_docs_changed_needs_manual_validation` | Add client integration guidance and CLI install commands |
| `GH-CAND-0020` | `eclipsefdn-ai-registry/ai-registry-core` | `78` | `typescript` | `19` | `3` | `code_and_docs_changed_needs_manual_validation` | Add "agent" (A2A) artifact type |
| `GH-CAND-0021` | `eclipsefdn-ai-registry/ai-registry-core` | `69` | `typescript` | `16` | `0` | `code_only_needs_manual_validation` | Add generic MCP server config with cross-vendor derivation and MCP trust delegation |
| `GH-CAND-0022` | `eclipsefdn-ai-registry/ai-registry-core` | `72` | `typescript` | `7` | `1` | `code_and_docs_changed_needs_manual_validation` | Remove homepage preview banner, refresh hero messaging (#68) |
| `GH-CAND-0023` | `eclipsefdn-ai-registry/ai-registry-core` | `70` | `typescript` | `1` | `0` | `code_only_needs_manual_validation` | Bump fast-uri from 3.1.2 to 3.1.5 |
| `GH-CAND-0024` | `eclipsefdn-ai-registry/ai-registry-core` | `63` | `typescript` | `4` | `2` | `code_and_docs_changed_needs_manual_validation` | Rename "verified by publisher" to "Publisher claimed" |
| `GH-CAND-0025` | `eclipsefdn-ai-registry/ai-registry-core` | `64` | `typescript` | `1` | `0` | `code_only_needs_manual_validation` | Adapt inferred badge |
| `GH-CAND-0026` | `eclipsefdn-ai-registry/ai-registry-core` | `62` | `typescript` | `8` | `2` | `code_and_docs_changed_needs_manual_validation` | Add vendor-supplied fallback metadata and publisher self-attestation of MCP servers |
| `GH-CAND-0027` | `torbido-hq/cicerone` | `112` | `python` | `1` | `2` | `code_and_docs_changed_needs_manual_validation` | fix: load Google Analytics only after Accept |
| `GH-CAND-0028` | `torbido-hq/cicerone` | `107` | `python` | `2` | `2` | `code_and_docs_changed_needs_manual_validation` | Add custom consent banner and Consent Mode v2 on cicerone.dev |
| `GH-CAND-0029` | `torbido-hq/cicerone` | `97` | `python` | `18` | `5` | `code_and_docs_changed_needs_manual_validation` | Add PyPI package and cicerone CLI |
| `GH-CAND-0030` | `torbido-hq/cicerone` | `101` | `python` | `5` | `5` | `code_and_docs_changed_needs_manual_validation` | feat(website): static articles at /articles/, hidden until a post exists |

## Interpretation Boundary

- This is a dataset construction step, not a model result.
- Candidate labels are intentionally left as `needs_manual_review`.
- Documentation-after text and documentation-file changes are stored only for audit/labeling.
- Model-facing evaluation scripts must use only `language`, `code_changed_files`, `code_diff_excerpt`, and `docs_before_excerpt`.