# Deep-JIT Validation Selection Audit 2026-08

## Split Facts

| Split | Included subsets | Records | Label distribution |
| --- | --- | ---: | --- |
| train | Return + Summary | 24,348 | 12,174 positive / 12,174 negative |
| validation | Return only | 1,790 | 895 positive / 895 negative |
| test | Return + Summary | 2,906 | 1,453 positive / 1,453 negative |

Param is excluded from the normalized benchmark because it has train only and no validation/test split.

## Audit Questions

| Question | Answer |
| --- | --- |
| Which subsets are included in train, validation, and test? | Train includes Return and Summary. Validation includes Return only. Test includes Return and Summary. |
| Is validation only Return? | Yes. |
| Is Summary represented in validation? | No. |
| Does model selection by validation F1 fairly select for combined Return+Summary test performance? | Partially. It is valid as a no-test-tuning procedure, but it is biased toward Return-style examples because Summary has no validation representation. |
| Should a small validation split be carved from Summary train while keeping Summary test untouched? | Methodologically yes. This would make model selection more representative of the combined test benchmark. |
| Would this improve methodology? | Yes. It would reduce subset-selection bias and allow threshold tuning to see both Return and Summary distributions. |
| Should this be implemented now? | Not unless the thesis needs another experimental refinement. Current results are usable with a clear limitation, but a small deterministic Summary-train carve-out would be the best next improvement before final thesis submission. |

## Red-Team Finding

The current validation strategy is not invalid, because it does not tune on test and it uses an official validation split where available. However, it is incomplete for the combined Return+Summary benchmark. Summary is the harder subset in current per-subset metrics, so a Return-only validation split can over-select models/thresholds that perform better on Return than Summary.

## Recommendation

For the thesis, report current results as:

> The lightweight classifier was selected using the available Deep-JIT validation split. Because the official validation file is available for Return but not Summary, validation-based model selection may be biased toward Return-style examples. Per-subset test metrics are therefore reported separately, and constructing a small deterministic validation split from Summary train is left as a recommended robustness improvement.

If one more small implementation step is allowed before thesis freeze, create a deterministic Summary validation carve-out from `Summary/train.json`, keep `Summary/test.json` untouched, and rerun model selection. Do not replace current results silently; report both or document the updated split clearly.
