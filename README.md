# DocGuard — Intelligent NLP Agent for Software Project Consistency Analysis

DocGuard is an MSc thesis prototype for detecting whether a real software change
requires a documentation update. The current research direction is a large-scale
real GitHub pull-request case study, not a synthetic-only benchmark.

## Current Research Status, August 2026

The original synthetic dataset factory remains useful as a controlled prototype,
regression suite, and demo environment. It is not treated as final thesis-level
evidence.

The current empirical focus is:

- real public GitHub pull requests,
- repository-group train/validation/locked-test splitting,
- non-rule-based classifiers trained on labeled real PR records,
- strict leakage prevention,
- large-scale candidate collection targeting 8k–10k real PR candidates,
- final accuracy/F1 only on labeled or reviewed records.

The 300-record real PR dataset is a pilot used to validate the workflow. It must
not be presented as the final empirical result. The large-scale evaluation is
tracked in:

- `docs/real_case_study_scaling_protocol_10k.md`
- `data/external/project_case_study/repo_seed_list.scale_10k.txt`
- `scripts/watch_real_case_job.py`
- `scripts/run_real_dataset_builder_checkpointed.py`
- `scripts/plot_real_case_evaluation.py`
- `scripts/bootstrap_real_case_metrics.py`
- `scripts/audit_real_candidate_dataset.py`

## Large-Scale Real GitHub PR Workflow

Seed collection:

```powershell
python -m docguard_external.github_pr_seed_collector --repos data/external/project_case_study/repo_seed_list.scale_10k.txt --output data/external/project_case_study/generated/real_pr_seeds_10k_v1.jsonl --rejects data/external/project_case_study/generated/real_pr_seeds_10k_v1.rejects.jsonl --report reports/real_case_study/generated/real_pr_seed_collection_10k_v1.md --target-total 10000 --max-pages-per-repo 12 --max-prs-per-repo 180 --max-changed-files 40 --max-total-patch-lines 3000 --sleep-seconds 0.05