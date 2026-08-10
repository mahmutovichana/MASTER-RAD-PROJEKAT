# External Dataset Research Plan 2026-08

## Candidate 1: CoDocBench

- Source/link: https://github.com/kunpai/codocbench
- Paper/link: https://arxiv.org/html/2502.00519v1
- Task type: code-documentation alignment during software maintenance.
- Expected fields: repository, commit, code before/after or diff, documentation/docstring before/after or diff.
- Mapping feasibility: high for positive examples where code and documentation/docstring changed together.
- Advantages: real GitHub commits; explicitly maintenance-oriented; closest current candidate to DocGuard's purpose.
- Limitations: likely docstring/code-documentation focus rather than broad project Markdown; negative examples may require careful conservative design.
- Recommended priority: 1 / primary pilot.
- Positive labels: yes, paired code+documentation changes can provide strong positives.
- Negative labels: only if provided or conservatively sampled; do not infer blindly.
- Patch generation: possible if doc_before/doc_after or doc_diff exists.
- Main or auxiliary: main external validation candidate.

## Candidate 2: Panthaplackel-Style Comment Update Dataset

- Source/link: https://github.com/panthap2/LearningToUpdateNLComments
- Paper/link: https://aclanthology.org/2020.acl-main.168/
- Task type: update natural language comments based on code changes.
- Expected fields: old code, new code, old comment, new comment, code/comment edit representation.
- Mapping feasibility: high for comment/docstring update detection and patch reconstruction.
- Advantages: real commit-derived code/comment pairs; directly studies update behavior.
- Limitations: focused on comments rather than repository Markdown docs.
- Recommended priority: 2 / strong auxiliary or second pilot.
- Positive labels: yes for code+comment changes.
- Negative labels: not automatic unless dataset supplies them or a conservative protocol is defined.
- Patch generation: yes, via comment_after or edit sequence.
- Main or auxiliary: auxiliary or complementary external benchmark.

## Candidate 3: CodeSearchNet

- Source/link: https://github.com/github/CodeSearchNet
- Paper/link: https://arxiv.org/pdf/1909.09436
- Task type: static code-comment/docstring retrieval.
- Expected fields: function code, docstring/comment, language, repository metadata.
- Mapping feasibility: low for update detection, moderate for embeddings/retrieval auxiliary work.
- Advantages: large and widely known benchmark; useful for representation learning or retrieval baselines.
- Limitations: not a code-change/update dataset; does not directly support docs_update_required.
- Recommended priority: auxiliary only.
- Positive labels: static association, not update-required label.
- Negative labels: no.
- Patch generation: no.
- Main or auxiliary: auxiliary benchmark only.

## Candidate 4: DocChecker / Code-Comment Inconsistency Datasets

- Source/link: https://github.com/FSoft-AI4Code/DocChecker
- Paper/link: https://arxiv.org/html/2306.06347v3
- Task type: code-comment inconsistency detection/rectification.
- Expected fields: code, comment, consistency label, possibly corrected comment.
- Mapping feasibility: moderate for consistency detection, lower for project-level patching.
- Advantages: strong related-work relevance; detection framing aligns with consistency analysis.
- Limitations: may include synthetic/noisy comments and may not model commit-time update decisions.
- Recommended priority: auxiliary.
- Positive labels: possible inconsistency/update-needed interpretation, but label semantics differ.
- Negative labels: possible consistent pairs.
- Patch generation: possible only where corrected text is available.
- Main or auxiliary: auxiliary consistency benchmark.

## Recommendation

Start with CoDocBench. It most directly supports a credible real-world validation story for code-documentation maintenance. Use the comment-update dataset as a second, focused benchmark for comment/docstring update behavior.

