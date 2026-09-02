# Gate 2 protocol-preserving implementation fixes

No experiment family, feature, fold, hyperparameter, threshold, metric, or winner rule changed.

1. After preregistration, the local M1 fold-0 attempt revealed that constructing the complement of validation indexes repeatedly was unnecessarily quadratic. The implementation now constructs the validation-index set once.
2. Interruptions such as `KeyboardInterrupt` are now appended as FAILED registry events rather than leaving only a STARTED event.
3. Registry records now use a compact machine-readable configuration identity and completed events include the selected inner configuration and threshold.
4. Fold completion is printed immediately for operational visibility. A self-referential summary hash field was removed; OOF and fold artifacts retain ordinary external hashes.

The first local M1 attempt was manually interrupted because the 8-GB non-CUDA host experienced severe memory pressure during the first outer fold. This is a compute-location issue, not a scientific result. The exact preregistered M1 run is therefore included in the high-RAM Colab action alongside M2/M3.
