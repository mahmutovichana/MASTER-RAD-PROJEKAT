from __future__ import annotations

import subprocess
from pathlib import Path


def run_git(workspace: Path, args: list[str]) -> str:
    result = subprocess.run(["git", *args], cwd=workspace, text=True, capture_output=True, timeout=20)
    if result.returncode != 0:
        return ""
    return result.stdout


def changed_files(workspace: Path) -> list[str]:
    output = run_git(workspace, ["diff", "--name-only"])
    staged = run_git(workspace, ["diff", "--cached", "--name-only"])
    names = [line.strip().replace("\\", "/") for line in (output + "\n" + staged).splitlines() if line.strip()]
    return sorted(set(names))


def workspace_diff(workspace: Path) -> str:
    unstaged = run_git(workspace, ["diff", "--no-ext-diff", "--"])
    staged = run_git(workspace, ["diff", "--cached", "--no-ext-diff", "--"])
    return "\n".join(part for part in [staged, unstaged] if part.strip())

