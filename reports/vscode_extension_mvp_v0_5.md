# VS Code Extension MVP v0.5

## Motivation

DocGuard v0.5 turns the research pipeline into a visible developer workflow. Instead of only reporting dataset metrics, the user can run DocGuard from VS Code, inspect whether documentation needs to change, preview a proposed patch, and apply it manually.

## Architecture

```text
VS Code command/status bar/context menu
  -> TypeScript extension
  -> Python CLI runtime
  -> HF embedding staged classifier if available
  -> hybrid router fallback
  -> deterministic patch composer
  -> webview preview
  -> user-approved WorkspaceEdit
```

## User Workflow

1. Developer edits code.
2. Developer runs `DocGuard: Analyze Workspace Changes`.
3. The extension collects workspace context through the Python runtime.
4. The DocGuard panel shows no-update or a documentation patch proposal.
5. The user clicks `Apply Patch` or `Ignore`.

## Runtime Design

The MVP uses `python -m docguard_runtime.runtime_cli analyze-workspace --workspace <path> --format json`. A future version can replace this with a persistent daemon without changing the extension UI contract.

## Limitations

- The MVP uses git diff for changed-code collection.
- The TypeScript extension does not load ML models directly.
- Patch application is intentionally conservative and append-oriented.
- The classifier must be trained locally for the full HF path; otherwise the router fallback is used.
- In this sandbox, `npm install`/`pnpm install` could not complete because registry access is blocked. Run the extension compile commands locally with network access.

## Screenshot Placeholders

- Command Palette entry
- DocGuard bottom panel empty state
- Update-needed patch preview
- No-update result
- Applied patch confirmation

## Demo Steps

Open `examples/vscode_demo`, add an environment variable change in `src/config.ts`, run DocGuard, preview the patch, and apply it to `docs/configuration.md`. Then make an internal helper refactor and confirm that DocGuard reports no documentation update required.
