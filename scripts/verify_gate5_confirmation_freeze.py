from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MANIFEST = (
    ROOT
    / "reports/final_v2/gate5/"
      "GATE5_CONFIRMATION_FREEZE_MANIFEST.json"
)

STATE = (
    ROOT
    / "reports/final_v2/finalization_state.json"
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(
            lambda: f.read(1024 * 1024),
            b"",
        ):
            h.update(chunk)

    return h.hexdigest()


m = json.loads(
    MANIFEST.read_text(
        encoding="utf-8"
    )
)

assert m["status"] == "PASS_FROZEN_CLOSED"
assert m["gate"] == 5
assert m["rerun_allowed"] is False
assert m["post_confirmation_tuning_allowed"] is False

assert (
    m["confirmation_dataset_sha256"]
    == "e73caca3b9ef46de284c4755127e3d7cfc0b5db9f3d1c8cd2b85be80b2c6d01b"
)

assert (
    m["gate5_preregistration_sha256"]
    == "dd4ed749774c144d3533128e93749fa003925dbdf73b1a121fee1a3fd40dc3b8"
)

for item in m["artifacts"]:
    path = ROOT / item["path"]

    assert path.is_file(), path
    assert path.stat().st_size == item["bytes"]
    assert sha256(path) == item["sha256"], item["path"]

state = json.loads(
    STATE.read_text(
        encoding="utf-8"
    )
)

assert state["current_gate"] == 6
assert state["confirmation_results_accessed_by_gate_5"] is True

assert (
    state["gate_5_summary"]["status"]
    == "PASS_FROZEN_CLOSED"
)

assert (
    state["gate_5_summary"]["rerun_allowed"]
    is False
)

print(
    json.dumps(
        {
            "status":
                "PASS",

            "gate5":
                "FROZEN_CLOSED",

            "current_gate":
                6,

            "frozen_artifact_count":
                len(
                    m["artifacts"]
                ),

            "confirmation_results_accessed":
                True,

            "rerun_allowed":
                False,
        },
        indent=2,
    )
)
