# Gate 2 external compute incident 001

Date recorded: 2026-09-02. Classification: **technical FAILED/INTERRUPTED run; scientifically inadmissible for model selection**.

## Execution context

- Execution commit: `1553c31e73eb705d555028170a86fd79a3d61859`.
- Python 3.13.15; Torch 2.11.0+cu128; Tesla T4.
- Transformers 4.56.2; tokenizers 0.22.0; accelerate 1.10.1; huggingface_hub 0.35.3.
- Frozen gold SHA matched: `68ebe23ab4dd8a02ee1ea459e3b6a374a3efa2891afc8d344a533676eb3b5a08`.

The Gate 1 verifier returned FAIL with `partition manifest SHA-256 mismatch`. The notebook used separate IPython `!python` commands, so the failed verifier did not prevent later cells from running. This violated the intended fail-closed execution boundary even though confirmation remained sealed.

UniXcoder extraction temporarily reached all 22,166 development rows, excluded all 3,747 confirmation rows, and reported development-view SHA `f01255edd74aa5153747c5468daf64b49b771f3b0ff38df72c0b054ea33d04b4` and encoder revision `5604afdc964f6c53782a6813140ade5216b99006`. The temporary artifact SHA was `ca75376fb304f37c45c6a733450352d2eb6ca9f6117b56dd58d368016b70d1eb`.

Technical truncation observations were code 14,332/22,166 (64.6576%) and docs 17,346/22,166 (78.2550%). These are retained only as incident diagnostics and must be reproduced by the valid run. No truncation, pooling, encoder, or token-budget rule changes in response.

M1 began and at least Binary outer fold 0 completed in the temporary runtime. Colab then removed GPU availability because of usage limits. No verified `gate2_colab_return.tar.gz` was returned, and **no model performance from this attempt is admissible or used for family selection**.

Confirmation was not accessed. Gate 2 remains `IN_PROGRESS_EXTERNAL_COMPUTE_REQUIRED`.

## Root cause and remediation

The partition-manifest mismatch was CRLF/LF serialization only: Gate 1 recorded the Windows working-tree CRLF SHA while Git stores an LF blob. Parsed JSON and canonical JSON are identical. Remediation adds canonical semantic verification bound to the exact Gate 1 commit/blob, a single fail-closed wrapper, Drive-persistent embedding checkpoints, and hashed fold-level resume. It changes no research state or preregistered scientific choice.
