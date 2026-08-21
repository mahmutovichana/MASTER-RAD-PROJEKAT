from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "examples" / "vscode_demo"


BASE_FILES = {
    "package.json": """{
  "name": "docguard-vscode-demo",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "dependencies": {
    "express": "^4.18.2"
  },
  "devDependencies": {
    "typescript": "^5.3.3"
  }
}
""",
    "README.md": """# DocGuard VS Code Demo

1. Prepare a scenario with `python scripts/prepare_vscode_demo.py --scenario config-env`.
2. Open `examples/vscode_demo` in VS Code.
3. Run `DocGuard: Analyze Workspace Changes`.
4. Review the suggested documentation patch in the DocGuard panel.
5. Click `Apply Patch`.
6. Run DocGuard again and confirm that no documentation update is required.

Try `--scenario new-endpoint` for an API documentation case or `--scenario no-update` for an internal refactor case.
""",
    "src/config.ts": """export const env = {
  port: Number(process.env.PORT || 3000),
  reviewMode: process.env.REVIEW_MODE || 'standard'
};
""",
    "src/server.ts": """import express from 'express';
import { env } from './config';
import { createTicket } from './tickets';

const app = express();
app.use(express.json());

app.post('/tickets', (req, res) => {
  const ticket = createTicket(req.body.title);
  res.status(201).json({ ticket, reviewMode: env.reviewMode });
});

app.listen(env.port, () => {
  console.log(`Demo API running on ${env.port}`);
});
""",
    "src/tickets.ts": """export function createTicket(title: string) {
  const normalized = title.trim();
  return { id: crypto.randomUUID(), title: normalized };
}

function normalizeInternalLabel(value: string): string {
  return value.trim().toLowerCase();
}

export function internalOnlyFormat(value: string): string {
  return normalizeInternalLabel(value);
}
""",
    "docs/configuration.md": """# Configuration

## Environment Variables

- `PORT` controls the HTTP port.
- `REVIEW_MODE` controls the default ticket review mode.
""",
    "docs/api.md": """# API Reference

## API Reference

### POST /tickets

Creates a ticket.
""",
    "docs/workflows.md": """# Workflows

Ticket creation is handled synchronously by the API server.
""",
}


SCENARIOS = {
    "clean": {},
    "config-env": {
        "src/config.ts": """export const env = {
  port: Number(process.env.PORT || 3000),
  reviewMode: process.env.REVIEW_MODE || 'standard',
  reviewWindow: process.env.REVIEW_WINDOW || '7d'
};
""",
    },
    "new-endpoint": {
        "src/server.ts": """import express from 'express';
import { env } from './config';
import { createTicket } from './tickets';

const app = express();
app.use(express.json());

app.post('/tickets', (req, res) => {
  const ticket = createTicket(req.body.title);
  res.status(201).json({ ticket, reviewMode: env.reviewMode });
});

app.get('/ticket-health', (_req, res) => {
  res.status(200).json({ status: 'ok' });
});

app.listen(env.port, () => {
  console.log(`Demo API running on ${env.port}`);
});
""",
    },
    "no-update": {
        "src/tickets.ts": """export function createTicket(title: string) {
  const normalizedTitle = title.trim();
  return { id: crypto.randomUUID(), title: normalizedTitle };
}

function normalizeInternalLabel(value: string): string {
  return value.trim().toLowerCase();
}

export function internalOnlyFormat(value: string): string {
  return normalizeInternalLabel(value);
}
""",
    },
}


def run_git(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=DEMO, text=True, capture_output=True, check=False)


def write_files(files: dict[str, str]) -> None:
    for rel, content in files.items():
        path = DEMO / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def ensure_demo_repo() -> None:
    if not (DEMO / ".git").exists():
        subprocess.run(["git", "init"], cwd=DEMO, check=True)
    run_git(["add", "."])
    diff = run_git(["diff", "--cached", "--quiet"])
    if diff.returncode != 0:
        run_git(["-c", "user.email=docguard@example.test", "-c", "user.name=DocGuard", "commit", "-m", "Prepare DocGuard VS Code demo baseline"])


def prepare(scenario: str) -> None:
    write_files(BASE_FILES)
    ensure_demo_repo()
    write_files(SCENARIOS[scenario])
    result = {
        "status": "ok",
        "workspace": str(DEMO),
        "scenario": scenario,
        "next_command": "python -m docguard_runtime.runtime_cli analyze-workspace --workspace examples/vscode_demo --format json",
    }
    print(json.dumps(result, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", choices=sorted(SCENARIOS), default="config-env")
    args = parser.parse_args()
    prepare(args.scenario)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
