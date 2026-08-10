from __future__ import annotations

from pathlib import Path


def prepare_codocbench(limit: int, output: Path) -> dict:
    return {
        "status": "not_implemented",
        "dataset": "codocbench",
        "limit": limit,
        "output": str(output),
        "message": (
            "Download/format-specific parsing is intentionally not implemented in this recovery step. "
            "First inspect the CoDocBench release files, then map records into ExternalDocGuardRecord."
        ),
        "next_step": "Fetch a small CoDocBench sample manually and rerun the adapter once field names are confirmed.",
    }

