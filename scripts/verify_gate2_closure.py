from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from docguard_ml_v2.gate2_closure import EXPECTED, sha256_file


def verify(root: Path = PROJECT_ROOT) -> dict:
    output = root / "reports/final_v2/gate2/final_results"
    summary = json.loads((output / "gate2_final_summary.json").read_text(encoding="utf-8"))
    decision = json.loads((output / "winner_decision.json").read_text(encoding="utf-8"))
    bootstrap = json.loads((output / "repository_bootstrap.json").read_text(encoding="utf-8"))
    leakage = json.loads((output / "leakage_audit.json").read_text(encoding="utf-8"))
    state = json.loads((root / "reports/final_v2/finalization_state.json").read_text(encoding="utf-8"))
    if summary.get("status") != "PASS" or summary.get("confirmation_accessed") is not False or summary.get("gate3_status") != "NOT_EXECUTED":
        raise RuntimeError("Gate 2 summary is not a sealed PASS")
    for key in ("gold_sha256", "scientific_config_sha256", "development_view_sha256", "raw_return_archive_sha256"):
        expected_key = "config_sha256" if key == "scientific_config_sha256" else "return_archive_sha256" if key == "raw_return_archive_sha256" else key
        if summary.get(key) != EXPECTED[expected_key]:
            raise RuntimeError(f"Gate 2 closure identity mismatch: {key}")
    if summary["verified_counts"]["learned_outer_folds"] != 30 or summary["verified_counts"]["candidate_fits_accounted"] != 930:
        raise RuntimeError("Gate 2 completion counts are invalid")
    if decision["binary"]["selected_family"] != summary["selected_families"]["binary"] or decision["category"]["selected_family"] != summary["selected_families"]["category"]:
        raise RuntimeError("Winner decision mismatch")
    if any(bootstrap[task].get("replicates") != 2000 or bootstrap[task].get("unit") != "repository" or bootstrap[task].get("seed") != 42 for task in ("binary", "category")):
        raise RuntimeError("Bootstrap contract mismatch")
    if leakage.get("status") != "PASS" or leakage.get("confirmation_accessed") is not False:
        raise RuntimeError("Leakage audit did not pass")
    if state["gate_statuses"]["gate_2_development_only_ml_model_study"] != "PASS" or int(state["current_gate"]) < 3 or state["confirmation_results_accessed_by_gate_2"] is not False or state["confirmation_sealed"] is not True:
        raise RuntimeError("Finalization state does not preserve a sealed Gate 2 PASS")
    manifest = json.loads((output / "artifact_manifest.json").read_text(encoding="utf-8"))
    for item in manifest["artifacts"]:
        path = root / item["path"]
        if not path.is_file() or path.stat().st_size != item["bytes"] or sha256_file(path) != item["sha256"]:
            raise RuntimeError(f"Gate 2 artifact integrity mismatch: {item['path']}")
    return {"status": "PASS", "gate": 2, "confirmation_accessed": False, "gate3_status": "NOT_EXECUTED", "verified_artifacts": len(manifest["artifacts"])}


def main() -> int:
    parser = argparse.ArgumentParser(); parser.parse_args()
    print(json.dumps(verify(), indent=2, sort_keys=True)); return 0


if __name__ == "__main__":
    raise SystemExit(main())
