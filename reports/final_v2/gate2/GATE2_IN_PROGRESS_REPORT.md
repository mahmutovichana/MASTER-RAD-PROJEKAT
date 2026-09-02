# Gate 2 status — external compute required

Gate 1 remains PASS at gold SHA `68ebe23ab4dd8a02ee1ea459e3b6a374a3efa2891afc8d344a533676eb3b5a08`. The fail-closed Gate 2 loader used exactly 22,166 development rows and excluded all 3,747 sealed confirmation rows.

The study was preregistered before results at commit `e89cedfa87edbc1469d467713451a9441aa1360f`. Five valid repository-disjoint outer folds and three repository-disjoint inner folds are frozen for both tasks. Binary has 22,166 eligible rows; Category V8 has 4,820 eligible rows.

M0 completed. Binary M0 has mean/std/worst MCC `0.0000 / 0.0000 / 0.0000`. Category M0 has mean/std/worst Macro-F1 `0.117644 / 0.002450 / 0.115669`.

The exact M1 local attempt was interrupted before producing any outer-fold result because the 8-GB Windows host experienced severe memory pressure. The attempt is retained as FAILED in the append-only registry. This is not a performance finding and does not alter the preregistered study. M1 is included unchanged in the high-RAM Colab execution together with M2 and M3.

Gate 2 cannot PASS until the pinned Colab action returns aligned UniXcoder embeddings and complete M1/M2/M3 development-only OOF results. Confirmation remains sealed and Gate 3 is forbidden.

Gate 0 + Gate 1 + Gate 2 safe test suite: **138 passed, 0 failed, 0 skipped, 30 warnings**. Gate 1 verifier: **PASS**.
