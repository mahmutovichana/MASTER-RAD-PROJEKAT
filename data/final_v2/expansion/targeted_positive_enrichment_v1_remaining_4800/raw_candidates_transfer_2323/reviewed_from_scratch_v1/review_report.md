# Raw candidate review (from scratch)

Rows reviewed: **2323**

This review uses only the safe evidence fields in the requested order: `code_changed_files`, `code_diff_excerpt`, then `docs_before_excerpt`. A positive label requires a changed public/config/setup/model token to be explicitly covered by docs-before. Generic terms and internal/test-only changes do not qualify.

## Label distribution

| Category | Count |
|---|---:|
| `api_reference` | 33 |
| `configuration` | 13 |
| `developer_setup` | 1 |
| `model_contract` | 7 |
| `no_update` | 2269 |

## Review status

| Status | Count |
|---|---:|
| `approved` | 2323 |

## Positive categories

| Category | Count |
|---|---:|
| `api_reference` | 33 |
| `configuration` | 13 |
| `developer_setup` | 1 |
| `model_contract` | 7 |

## Languages

| Language | Rows | Positive |
|---|---:|---:|
| `go` | 668 | 22 |
| `java` | 71 | 0 |
| `javascript` | 10 | 0 |
| `python` | 897 | 30 |
| `rust` | 10 | 0 |
| `typescript` | 86 | 2 |
| `unknown` | 581 | 0 |

## Shards

| Shard | Rows | Positive |
|---|---:|---:|
| `A` | 812 | 12 |
| `B` | 704 | 13 |
| `C` | 807 | 29 |

## Integrity

- Source rows were not modified.
- Output preserves source field values and adds only the four human review fields.
- No docs-after, comments, source URLs, or outcome metadata were used for decisions.
- `decision_samples.jsonl` contains a compact audit sample; the full row-level rationale is in `reviewed_2323.jsonl` and the 24 batch files.
