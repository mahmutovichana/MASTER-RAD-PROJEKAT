# Real GitHub PR Case Study Scaling Protocol — 10k v1

## Purpose

The 300-record dataset is treated as a pilot dataset used to validate the data
collection, labeling, splitting, leakage prevention, model training, and review
workflow. It is not treated as the final empirical basis for the thesis.

The final real-world evaluation will be based on a substantially larger dataset
of real public GitHub pull requests. The target candidate pool is 10,000 real
merged PRs sampled from a broad set of repositories.

## Scope

The experiment evaluates whether an NLP-based DocGuard agent can detect when a
software change requires a documentation update.

The evaluation must avoid:
- synthetic examples as final evidence,
- rule-based decision logic as the main model,
- leakage from documentation-after text, documentation diffs, PR titles, URLs,
  manual notes, or gold labels into model input,
- accuracy/F1 claims based only on a very small reviewed test set.

## Dataset Layers

### Candidate Pool

The large-scale candidate pool contains real public GitHub PRs. Candidate records
are not labels. They are raw evaluation candidates containing safe model-facing
fields and audit-only fields.

Target size:

- 10,000 candidate records
- 100–150+ repositories
- mixed TypeScript/Python/other code-heavy repositories
- mixed candidate types:
  - code and documentation changed
  - code only
  - tests/fixtures
  - configuration/API/schema/workflow-related changes

### Silver Labels

Silver labels may be produced using an AI-assisted labeling process. These labels
can be used for training and preliminary evaluation, but they must be described
as AI-assisted unless independently reviewed by a human.

### Reviewed Evaluation Set

Final thesis metrics should be computed on a larger reviewed evaluation set, not
only on the 32-case pilot locked test.

Target reviewed set:

- minimum acceptable: 500 reviewed locked-test records
- preferred: 1,000–2,000 reviewed locked-test records
- ambiguous records excluded from final metric calculation
- all exclusions must be reported

## Leakage Boundary

Only the following fields are model-facing:

- `language`
- `code_changed_files`
- `code_diff_excerpt`
- `docs_before_excerpt`

The following fields are audit-only and must not be used as model input:

- `source_url`
- `repository`
- `pr_number`
- `pr_title`
- `docs_changed_files`
- `docs_diff_excerpt`
- `docs_after_excerpt`
- `gold_docs_update_required`
- `gold_doc_category`
- `gold_target_doc_file`
- `gold_target_section`
- `gold_patch_summary`
- `label_confidence`
- `manual_label_notes`
- `candidate_evidence`

## Splitting Strategy

The final evaluation must use repository-group splitting to avoid repository
overlap between train, validation, and locked-test splits.

The threshold must be selected on the validation split only. The locked-test split
must not be used for threshold tuning.

## Metrics

The final report should include:

- accuracy
- precision
- recall
- F1
- specificity
- false positive rate
- confusion matrix
- bootstrap confidence intervals
- per-language breakdown
- per-candidate-type breakdown
- per-repository-family breakdown where possible

## Interpretation of Pilot Results

The 300 v1 experiment and the 32-case reviewed locked-test result are pilot
evidence. They demonstrate that the workflow is operational and that a
non-rule-based classifier can be trained on real PR records.

They must not be presented as the final empirical claim of the thesis.

## Final Claim Requirement

A final performance claim is allowed only after evaluating on a substantially
larger labeled/reviewed locked-test set.

If the large-scale labels are AI-assisted, the result must be described as
AI-assisted silver evaluation. If a subset is manually reviewed, that subset may
be described as reviewed evaluation.