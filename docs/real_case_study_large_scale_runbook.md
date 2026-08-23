# Real GitHub PR Large-Scale Evaluation Runbook

## Status

The 300-record dataset is a pilot. It validates the pipeline but is not the final empirical basis.

The large-scale run targets:
- 8k–10k real public GitHub PR candidates,
- repository-group split,
- no leakage from audit-only fields,
- large silver-labeled evaluation,
- reviewed locked-test subset before final thesis claims.

## Candidate Pool vs Evaluation Labels

A candidate pool is not an evaluation set.

Accuracy, precision, recall, F1, ROC AUC and PR AUC can only be claimed for records with labels.

If labels are AI-assisted, the result must be called silver evaluation.
If labels are human-reviewed or second-pass reviewed, the result must be called reviewed evaluation.

## Current Large-Scale Commands

Seed collection:

```powershell
python -m docguard_external.github_pr_seed_collector --repos data/external/project_case_study/repo_seed_list.scale_10k.txt --output data/external/project_case_study/generated/real_pr_seeds_10k_v1.jsonl --rejects data/external/project_case_study/generated/real_pr_seeds_10k_v1.rejects.jsonl --report reports/real_case_study/generated/real_pr_seed_collection_10k_v1.md --target-total 10000 --max-pages-per-repo 12 --max-prs-per-repo 180 --max-changed-files 40 --max-total-patch-lines 3000 --sleep-seconds 0.05