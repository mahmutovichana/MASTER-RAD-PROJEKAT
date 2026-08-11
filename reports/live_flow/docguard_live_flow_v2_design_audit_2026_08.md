# DocGuard Live Flow V2 Design Audit 2026-08

## Why V1 Was Useful

The first live flow verified that `docguard_hybrid.predict()` can route representative documentation classes end to end: code diff, update decision, category, target file, and generated patch.

## Why V2 Is Needed

V1 was class-focused and intentionally signal-compatible. It did not feel like a software project evolving through realistic PRs. V2 simulates multiple invented projects with baseline code, baseline docs, and PR-like sequences over time.

## How V2 Differs

- Three invented projects instead of one isolated mini API.
- At least eight PR-like changes per project.
- Baseline source and documentation folders are generated.
- Each case includes project, PR title, sequence number, difficulty, realism notes, code diff, and docs-before context.
- The runner passes only sanitized input to `docguard_hybrid.predict()`: code-side changed files, code diff, docs-before excerpt, project id, and case id.
- Gold labels, expected facts, scenario type, category, target file, and docs-after are not passed to the predictor.

## Thesis Alignment

V2 better supports the thesis goal because it demonstrates the intended DocGuard workflow in a project-evolution narrative: project baseline -> PR-like code diff -> DocGuard prediction -> documentation target -> patch suggestion -> developer review.

## Limitations

- Still synthetic and controlled.
- Still not an external benchmark.
- Diffs are designed to be runnable by the current deterministic hybrid signal extractor.
- Generated patches are concise starting points, not production-ready documentation.
- Real-world automatic evaluation still requires the hardened project-case adapter.
