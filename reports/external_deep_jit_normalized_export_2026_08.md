# External Deep-JIT Normalized Export 2026-08

- Raw data directory: `data\external\raw\deep_jit_inconsistency`
- Output directory: `data\external\deep_jit_binary`
- Label polarity status: `plausible_manual_verification_needed`

## Written Files

| Split | Path | Records | Label distribution |
| --- | --- | ---: | --- |
| `train` | `data\external\deep_jit_binary\train.jsonl` | 24348 | `{'True': 12174, 'False': 12174}` |
| `validation` | `data\external\deep_jit_binary\validation.jsonl` | 1790 | `{'True': 895, 'False': 895}` |
| `test` | `data\external\deep_jit_binary\test.jsonl` | 2906 | `{'True': 1453, 'False': 1453}` |

## Leakage Rule

The normalized records retain `new_comment_raw` / `doc_after` only for audit. The training module input builders do not include `new_comment_raw`, `doc_after`, or `doc_diff`.

## Skipped Files

- `data\external\raw\deep_jit_inconsistency\Param\train.json`
