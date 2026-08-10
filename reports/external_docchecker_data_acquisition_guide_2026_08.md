# External DocChecker Data Acquisition Guide 2026-08

## Source Repositories To Inspect Manually

- DocChecker: https://github.com/FSoft-AI4Code/DocChecker
- Deep Just-In-Time inconsistency detection: https://github.com/panthap2/deep-jit-inconsistency-detection
- Deep-JIT data folder: https://drive.google.com/drive/folders/1heqEQGZHgO6gZzCjuQD1EyYertN4SAYZ?usp=sharing
- Deep-JIT model/resources folder: https://drive.google.com/drive/folders/1cutxr4rMDkT1g2BbmCAR2wqKTxeFH11K?usp=sharing
- Deep-JIT SHA metadata files:
  - https://drive.google.com/file/d/1YU8mPwIXFTKXGYV17lOzyeZeH4xOjnuT/view?usp=drive_link
  - https://drive.google.com/file/d/1Bh3I4SUpKTXB6CmJTiwVCxlQqofBVLhv/view?usp=drive_link
- Panthaplackel comment-update data: https://drive.google.com/open?id=12VMmdE67bp5UFYIoBUf0ibKGXFCH6fQo
- Panthaplackel resources: https://drive.google.com/drive/folders/1YZB7FK58LcDCpabj7hlD5vQx_axbdBCQ?usp=sharing

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

## Confirmed Local Deep-JIT Schema

The local folder `data/external/raw/deep_jit_inconsistency/` has been inspected. The usable partition files include explicit `label` plus `old_code_raw`, `new_code_raw`, `old_comment_raw`, and `new_comment_raw` fields.

The conservative mapper now supports creating a balanced external binary proxy sample:

```bash
python -m docguard_external.cli prepare --dataset docchecker --data-dir data/external/raw/deep_jit_inconsistency --limit 500 --output data/external/docchecker_binary_sample_500.jsonl
python -m docguard_external.cli validate --input data/external/docchecker_binary_sample_500.jsonl
python -m docguard_external.cli evaluate-existing-binary --input data/external/docchecker_binary_sample_500.jsonl --output reports/external_docchecker_existing_docguard_binary_evaluation_2026_08.md
```

This dataset should be described as a Deep-JIT / DocChecker-style code-comment inconsistency proxy, not as full project-level Markdown documentation update detection.
