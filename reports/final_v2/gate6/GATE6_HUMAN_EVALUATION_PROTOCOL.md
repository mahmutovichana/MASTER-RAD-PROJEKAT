# Gate 6 Human Evaluation Protocol

Status: **FROZEN BEFORE HUMAN SCORES**
Scope: primary natural-distribution sample only (`n = 100`). The secondary stress sample is supplementary and must never be pooled into the primary estimate.

## Blind review contract

Reviewers receive only the case identifier, language, changed files, code-diff excerpt, documentation-before excerpt, selected target document, generated documentation patch, and reviewer-entry fields. Gold/reference labels, generation provenance, verifier outcomes, confidence, repair state, and the reason an output is absent are forbidden.

## Complete-case policy

Every one of the 100 sampled primary rows remains in Gate 6. A row with no accepted generated patch is preclassified as `NO_OUTPUT_SYSTEM_FAILURE`. It is complete/evaluated, not incomplete or excluded. Its five human-quality dimensions and accept-as-is judgment are structurally `N/A`, and it counts as a failure in the end-to-end accept-as-is estimate.

The end-to-end acceptance denominator is always all 100 primary rows. Human-quality means and distributions are conditional on rows with an actual generated output, and their denominator must be stated explicitly. Accept-as-is is reported twice: end-to-end over all 100 primary rows and conditional on output-bearing rows only. No-output rows are never assigned numeric quality scores.

## Output-bearing rows

For each actual output, the reviewer marks `review_status = approved`, completes all five dimensions, answers `human_accept_as_is` with `yes` or `no`, and may add notes.

- `human_factual_correctness`: integer 1--5.
- `human_semantic_completeness`: integer 1--5.
- `human_developer_usefulness`: integer 1--5.
- `human_readability`: integer 1--5.
- `human_style_fit`: integer 1--5.
- `human_accept_as_is`: `yes` or `no`.
- `human_notes`: optional free text.

The 1--5 ratings are ordinal, with 1 the lowest and 5 the highest assessment for the named dimension. No Gate 6 result is calculated by this preparation step.
