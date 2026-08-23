# Blind Label Audit Interpretation — 4k V2

## Purpose

The blind label audit was performed to estimate the quality and limitations of the protocol-derived labels used in the large-scale 4k real GitHub PR experiment.

The audit subset was intentionally stratified by prediction outcome types and is therefore not a representative random sample of the full dataset.

## Important limitation

The audit subset must not be used as a replacement for the frozen locked-test result.

The frozen V2 locked-test result remains the primary quantitative result for the protocol-derived 4k dataset.

## Label quality result

The human-corrected audit labels show moderate agreement with the protocol-derived labels.

This indicates that the protocol-derived labels are useful for large-scale experimentation, but they contain label noise and should not be described as fully human-reviewed gold labels.

## Methodological conclusion

The audit strengthens the thesis because it makes the label-quality limitation explicit instead of hiding it.

The final thesis should distinguish between:

1. protocol-derived large-scale labels used for the 4k experiment
2. human-corrected blind audit labels used for label-quality estimation
3. frozen locked-test metrics used for primary model reporting

## Thesis-safe wording

The 4k real PR experiment uses reproducible protocol-derived labels. To estimate label quality, a stratified blind audit was conducted on 233 cases. The audit showed moderate agreement between protocol-derived and human-corrected labels, indicating that the large-scale labels are useful but noisy. Therefore, the final results are interpreted as performance against a reproducible protocol-labeled dataset, with label noise acknowledged as a limitation.