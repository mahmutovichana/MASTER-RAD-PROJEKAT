# External Deep-JIT Combined-Validation Split Audit 2026-08

## Reason

The previous Deep-JIT model-selection setup used Return validation only while the combined test set contained Return and Summary. This robustness export adds a deterministic balanced Summary validation carve-out from Summary train while keeping Summary test untouched.

## Old Split Setup

- Train: Return train + Summary train
- Validation: Return validation only
- Test: Return test + Summary test
- Param: excluded/audit-only

## New Split Setup

- Seed: `42`
- Summary validation carve-out: `420` positive + `420` negative from Summary train
- Return train/validation/test preserved exactly as before.
- Summary test preserved untouched.
- Param remains excluded/audit-only.

## Written Files

| Split | Path | Records | Label distribution | Subset distribution |
| --- | --- | ---: | --- | --- |
| `train` | `data\external\deep_jit_binary_combined_validation\train.jsonl` | 23508 | `{'True': 11754, 'False': 11754}` | `{'Return': 15950, 'Summary': 7558}` |
| `validation` | `data\external\deep_jit_binary_combined_validation\validation.jsonl` | 2630 | `{'True': 1315, 'False': 1315}` | `{'Return': 1790, 'Summary': 840}` |
| `test` | `data\external\deep_jit_binary_combined_validation\test.jsonl` | 2906 | `{'True': 1453, 'False': 1453}` | `{'Return': 1840, 'Summary': 1066}` |

## Confirmations

- Summary validation came only from `Summary/train.json`.
- Summary test source `Summary/test.json` remains untouched with `1066` records.
- No Summary test records were used for train or validation.
- No Param records were used in the classifier benchmark.

## Skipped Files

- `data\external\raw\deep_jit_inconsistency\Param\train.json`
