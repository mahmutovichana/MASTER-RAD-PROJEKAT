from __future__ import annotations

import hashlib
import json
from pathlib import Path


def main() -> int:
    base = Path(__file__).resolve().parents[1]
    files = []
    for path in sorted(base.rglob("*")):
        relative = path.relative_to(base).as_posix()
        if not path.is_file() or relative == "artifact_manifest.json" or "repository_cache/" in relative or "__pycache__/" in relative:
            continue
        files.append({"path": relative, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size})
    payload = {
        "experiment": "S1 Repository-Grounded Documentation Agent",
        "scientific_status": "POST_HOC_STAGE3_CHALLENGER_DEVELOPMENT_ONLY",
        "confirmation_accessed": False,
        "gate6_row_level_human_data_accessed": False,
        "file_count": len(files),
        "files": files,
    }
    (base / "artifact_manifest.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
