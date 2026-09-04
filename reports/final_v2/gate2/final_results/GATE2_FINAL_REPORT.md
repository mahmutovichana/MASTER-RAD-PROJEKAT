# Gate 2 Final Development-Only Model Study

**Status: PASS.** This report closes Gate 2 only. Confirmation remained sealed and Gate 3 was not executed.

## Verified scope

- Development rows: 22,166
- Category-eligible rows: 4,820
- Verified learned outer folds: 30/30
- Structurally accounted preregistered candidate fits: 930/930
- Return archive SHA-256: `0b5840e1ce600f0df44f935f9c2ec9ce4608694e0dc0e73eb0f9a2e75b63abfd`

## Model comparison

| Task | Family | Primary mean | Std | Worst | Best | Overall OOF primary |
|---|---:|---:|---:|---:|---:|---:|
| binary | M0 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| binary | M1 | 0.830265 | 0.092756 | 0.690457 | 0.925698 | 0.832147 |
| binary | M2 | 0.810961 | 0.099579 | 0.687829 | 0.898248 | 0.813598 |
| binary | M3 | 0.829474 | 0.102177 | 0.700491 | 0.921541 | 0.832042 |
| category | M0 | 0.117644 | 0.002450 | 0.115669 | 0.122414 | 0.117278 |
| category | M1 | 0.857705 | 0.101458 | 0.663750 | 0.942515 | 0.860982 |
| category | M2 | 0.835404 | 0.099351 | 0.665016 | 0.940023 | 0.840533 |
| category | M3 | 0.839713 | 0.095623 | 0.672263 | 0.940979 | 0.844696 |

## Preregistered winner rule

- **Binary: M1** — M1 is inside the 0.005 mean tolerance and has the lowest outer-fold standard deviation among eligible families; simplicity applies only if standard deviations tie.
- **Category: M1** — M1 is inside the 0.005 mean tolerance and has the lowest outer-fold standard deviation among eligible families; simplicity applies only if standard deviations tie.

## Repository bootstrap

2,000 repository-level resamples, seed 42, 95% percentile intervals. These intervals reflect repository clustering; rows were not resampled independently.

### Binary

- M0: 0.000000 (95% CI 0.000000–0.000000)
- M1: 0.832147 (95% CI 0.699005–0.898874)
- M2: 0.813598 (95% CI 0.661293–0.885629)
- M3: 0.832042 (95% CI 0.694906–0.898048)
- M1_minus_M2: 0.018549 (95% CI -0.015327–0.066054; P(diff>0)=0.861)
- M1_minus_M3: 0.000104 (95% CI -0.033293–0.036628; P(diff>0)=0.518)
- M2_minus_M3: -0.018444 (95% CI -0.039941–-0.007344; P(diff>0)=0.000)

### Category

- M0: 0.117278 (95% CI 0.106273–0.130014)
- M1: 0.860982 (95% CI 0.736054–0.925118)
- M2: 0.840533 (95% CI 0.712228–0.910283)
- M3: 0.844696 (95% CI 0.717883–0.913240)
- M1_minus_M2: 0.020449 (95% CI 0.002389–0.044078; P(diff>0)=0.992)
- M1_minus_M3: 0.016285 (95% CI -0.000974–0.037636; P(diff>0)=0.968)
- M2_minus_M3: -0.004164 (95% CI -0.011225–0.001537; P(diff>0)=0.080)

## Leakage and interpretation

Leakage audit: **PASS**. Repository overlap across outer folds, case duplication, accidental fold reuse, unsafe model fields, post-change documentation features, provenance model features, and confirmation-result contamination were not found. Model-visible duplicate groups are reported transparently in the machine-readable audit.

The high aggregate scores are not uniform across provenance. For selected M1, Category Macro-F1 is **1.000** on 3,460 controlled-design rows but **0.363** on 1,360 natural rows. Binary M1 has **MCC 0.413** on 18,166 natural rows; the 4,000 controlled rows are all positive, so MCC is mathematically uninformative (reported as 0.000) for that one-class slice. On the Natural Diversity subset, Binary MCC is **-0.028** over 619 rows and Category Macro-F1 is **0.267** over only 7 eligible rows. Therefore the overall results are valid as observed, but the very strong aggregate score is materially influenced by the controlled augmentation and must not be presented as uniform natural-case generalization.

Five development-only model-visible duplicate groups (10 rows) were found. None crosses an outer fold; one has conflicting labels and remains a documented label/input ambiguity rather than train/test leakage.

Slice diagnostics are development-only. Slices below 100 rows (and repository slices below 20 rows) are flagged as low support and must not be overinterpreted. Strong performance on controlled-design data is reported separately from natural data.

## Boundary

No final classifier freeze manifest was created. Gate 3 remains `NOT_EXECUTED`; its remaining prerequisite is an explicit, separate authorization to start the preregistered selection/freeze procedure using only these closed Gate 2 results.
