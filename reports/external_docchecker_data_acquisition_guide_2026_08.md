# External DocChecker Data Acquisition Guide 2026-08

## Source Repositories To Inspect Manually

- DocChecker: https://github.com/FSoft-AI4Code/DocChecker
- Deep Just-In-Time inconsistency detection: https://github.com/panthap2/deep-jit-inconsistency-detection

## What To Look For

- Dataset download links, especially Google Drive or release links.
- Processed data folders.
- Train/dev/test files.
- Label definitions for consistent, inconsistent, outdated, or up-to-date comments.
- README instructions describing how labels were created.
- Scripts that create or preprocess datasets.

## What Not To Do

- Do not commit large downloaded raw datasets blindly.
- Do not invent negative labels.
- Do not mix datasets without explicit source labels.
- Do not treat weak or inferred labels as strong external labels.

## Recommended Local Folder Structure

```text
data/external/raw/docchecker/
data/external/raw/deep_jit_inconsistency/
```

The raw folder is ignored by git. Keep small processed samples only after schema, label provenance, and licensing expectations are checked.

## Inspection Commands

```bash
python -m docguard_external.cli inspect --dataset docchecker --data-dir data/external/raw/docchecker --limit 10
python -m docguard_external.cli inspect --dataset docchecker --data-dir data/external/raw/deep_jit_inconsistency --limit 10
```

If the inspector finds explicit binary labels and code/comment fields, the next step is to implement a conservative `prepare --dataset docchecker` mapping. Until then, no records should be created.
