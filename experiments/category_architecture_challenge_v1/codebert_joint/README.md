# CodeBERT Joint Architecture Challenge V1

This directory is reserved for the bounded Stage-2 CodeBERT joint classifier
outputs produced by `notebooks/category_codebert_architecture_challenge_v1.ipynb`.

The notebook trains `microsoft/codebert-base` as a joint code/docs pair
classifier using only natural, independently reviewed primary-four
development-training positives.  It evaluates once on the frozen 322-row
natural development validation set and compares against:

`hybrid__natural_only__multinomial_logreg__natural_diversity_expansion_v1`

No local CPU fine-tuning has been run for this experiment.
