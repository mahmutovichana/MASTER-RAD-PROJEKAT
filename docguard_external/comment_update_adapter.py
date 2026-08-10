from __future__ import annotations

from pathlib import Path


def prepare_comment_update(limit: int, output: Path) -> dict:
    return {
        "status": "not_implemented",
        "dataset": "comment_update",
        "limit": limit,
        "output": str(output),
        "message": (
            "The ACL 2020 comment-update dataset adapter is scaffolded only. "
            "Confirm file layout and license before converting records."
        ),
    }

