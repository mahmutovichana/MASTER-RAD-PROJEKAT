# External Deep-JIT Split Audit 2026-08

- Data directory: `data\external\raw\deep_jit_inconsistency`
- Status: `ok`
- Label polarity status: `plausible_manual_verification_needed`

## Available Files

| File | Subset | Split | Records | Label distribution | Balanced | Required fields |
| --- | --- | --- | ---: | --- | --- | --- |
| `data\external\raw\deep_jit_inconsistency\Param\train.json` | `Param` | `train` | 8640 | `{'1': 4320, '0': 4320}` | `True` | `True` |
| `data\external\raw\deep_jit_inconsistency\Return\test.json` | `Return` | `test` | 1840 | `{'1': 920, '0': 920}` | `True` | `True` |
| `data\external\raw\deep_jit_inconsistency\Return\train.json` | `Return` | `train` | 15950 | `{'1': 7975, '0': 7975}` | `True` | `True` |
| `data\external\raw\deep_jit_inconsistency\Return\valid.json` | `Return` | `validation` | 1790 | `{'1': 895, '0': 895}` | `True` | `True` |
| `data\external\raw\deep_jit_inconsistency\Summary\test.json` | `Summary` | `test` | 1066 | `{'1': 533, '0': 533}` | `True` | `True` |
| `data\external\raw\deep_jit_inconsistency\Summary\train.json` | `Summary` | `train` | 8398 | `{'1': 4199, '0': 4199}` | `True` | `True` |

## Split Availability

- `Param`: `train`
- `Return`: `test`, `train`, `validation`
- `Summary`: `test`, `train`

## Evaluation Policy

Return and Summary should be evaluated both separately and combined because they represent different comment types and both have test files. Return has train/validation/test. Summary has train/test but no validation file. Param has train only and is excluded from the normalized classifier benchmark to avoid introducing a train-only subset without validation/test coverage.

The normalized benchmark uses original splits where available. It does not randomly mix train and test.
