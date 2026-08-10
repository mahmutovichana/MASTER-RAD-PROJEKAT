# External Binary Dataset Candidate Inspection 2026-08

This inspection is lightweight. It documents candidate datasets and repository instructions without downloading large data files or creating labels.

## 1. DocChecker / ICCD-Style Code-Comment Inconsistency Data

- Source URL: https://github.com/FSoft-AI4Code/DocChecker
- Paper URL: https://aclanthology.org/2024.eacl-demo.20/
- Task type: code-comment inconsistency detection and rectification.
- Repository/data availability: the repository is public. Its README says pre-training data comes from CodeXGLUE/CodeSearchNet and the Just-In-Time fine-tuning data is downloaded from a Google Drive link. The repository shows examples with `code`, `docstring`, `predict` (`Consistent!` / `Inconsistent!`), and `recommended_docstring`.
- Expected task: determine whether a comment/docstring is semantically out of sync with the corresponding code function.
- Explicit binary labels: likely yes for the Just-In-Time / ICCD task, but the downloadable local data must be inspected to confirm exact field names and label encoding.
- Code before/after: likely static code/comment pairs for inconsistency detection rather than code before/after diffs.
- Positive label meaning: inconsistent/outdated code-comment pair.
- Negative label meaning: consistent/up-to-date code-comment pair.
- Label strength: potentially strong external binary labels if the official Just-In-Time/ICCD labels are available.
- Mapping feasibility: high for `ExternalDocGuardRecord` as a binary code-comment consistency proxy, using code/comment pair fields.
- Precision/F1 support: yes, if explicit consistent and inconsistent labels are present in local data.
- Limitations: code-comment consistency is not identical to project-level Markdown documentation update detection; dataset access appears to require external download and schema inspection.
- Priority recommendation: high. This is the strongest next candidate for real external binary validation.

## 2. Panthaplackel ACL 2020 Comment-Update Dataset

- Source URL: https://github.com/panthap2/LearningToUpdateNLComments
- Paper URL: https://aclanthology.org/2020.acl-main.168/
- Task type: generate edits to update an existing natural language comment based on code changes.
- Repository/data availability: repository is public and points to Google Drive data for generation/update datasets.
- Expected task: comment update generation from code changes.
- Explicit binary labels: not confirmed. The paper/repository framing suggests update pairs, not necessarily non-update examples.
- Code before/after: likely yes, because the task is based on code changes.
- Positive label meaning: a code/comment update pair where the comment should change.
- Negative label meaning: not confirmed.
- Label strength: strong positive update labels if official pairs are available; binary negative label strength unknown.
- Mapping feasibility: high as a second positive external benchmark; uncertain for binary evaluation.
- Precision/F1 support: only if local data contains explicit non-update examples or detection labels.
- Limitations: data is behind external download; schema and negative availability must be inspected locally.
- Priority recommendation: medium-high as a second positive benchmark, lower than DocChecker for binary negatives.

## 3. Deep Just-In-Time Inconsistency Detection

- Source URL: https://github.com/panthap2/deep-jit-inconsistency-detection
- Paper/task: Deep Just-In-Time Inconsistency Detection Between Comments and Source Code.
- Task type: detect comment/source-code inconsistency, with combined detection/update variants.
- Repository/data availability: repository points to Google Drive data and model resources.
- Explicit binary labels: likely yes for the detection task, but local data inspection is required.
- Code before/after: likely edit-based representations and comment/code context; exact fields need confirmation.
- Mapping feasibility: high if labels are explicit.
- Precision/F1 support: likely yes if detection labels are available.
- Limitations: external download required; schema not confirmed.
- Priority recommendation: high as an alternative or companion to DocChecker for binary external validation.

## Overall Recommendation

Implement DocChecker / Just-In-Time inconsistency data first if local labeled files can be obtained. It is the best fit for a defensible external binary proxy: inconsistent comment means update required, consistent comment means no update required. Panthaplackel ACL 2020 should be inspected next, but should be treated as positive-only until non-update labels are verified.

Sources: DocChecker GitHub and EACL page; Panthaplackel ACL 2020 GitHub/ACL page; Deep-JIT GitHub page.
