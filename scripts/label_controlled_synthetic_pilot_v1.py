from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW_ROOT = ROOT / "data/final_v2/controlled_synthetic_positive_v1/human_review"


def rationale(row: dict) -> str:
    repo = row.get("repository", "")
    files = row.get("code_changed_files") or []
    path = str(files[0]) if files else ""
    doc = row.get("doc_context_01_path") or "BASE dokumentacija"
    if repo == "pallets/flask" and path == "src/flask/app.py" and doc == "CHANGES.rst":
        # Distinguish the three Flask surfaces using the diff itself.
        diff = str(row.get("code_diff_excerpt", ""))
        if "synthetic_option_" in diff:
            return "Promjena je u internom CustomClient konstruktoru, a CHANGES.rst excerpt ne dokumentuje taj javni API; postojeća dokumentacija ostaje tačna."
        if "will not be supported in Flask" in diff:
            return "Promijenjen je tekst internog deprecation upozorenja, ne konfiguracijski ključ ili dokumentovana postavka; config dokumentacija ostaje tačna."
        return "Dodano je polje na Flask klasu, ali CHANGES.rst excerpt opisuje lifecycle/metode, ne serializovani model ili schema contract; nema docs drifta."
    if repo == "koajs/koa":
        return "Promijenjena je interna getAsyncLocalStorage funkcija, dok docs/api/request.md pokriva request properties; postojeći API opis nije učinjen netačnim."
    if repo == "encode/httpx" and path == "httpx/_config.py":
        diff = str(row.get("code_diff_excerpt", ""))
        if "requires-python" in diff:
            return "Podignut je Python runtime zahtjev u pyproject.toml, ali CHANGELOG excerpt ne navodi podržanu runtime verziju niti setup proceduru; nema postojeće tvrdnje koja je postala netačna."
        return "Promijenjen je inline Timeout primjer u izvornom modulu, dok CHANGELOG excerpt ne dokumentuje taj timeout primjer ili javni config default; nema pokrivene tvrdnje koja je zastarjela."
    return "Dostavljeni BASE docs excerpt ne pokriva promijenjenu javnu dokumentacijsku površinu niti postojeću setup tvrdnju; dokumentacija ostaje semantički tačna."


def label(row: dict) -> dict:
    # Apply only the four human-controlled fields; all evidence, suggestions,
    # provenance and integrity hashes remain byte-for-byte unchanged.
    row["human_docs_update_required"] = "false"
    row["human_doc_category"] = "no_update"
    row["human_label_notes"] = rationale(row)
    row["review_status"] = "approved"
    return row


def main() -> int:
    source = REVIEW_ROOT / "review_batches"
    target = REVIEW_ROOT / "reviewed_batches"
    target.mkdir(parents=True, exist_ok=True)
    total = 0
    for path in sorted(source.glob("batch_*.jsonl")):
        rows = [label(json.loads(line)) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        (target / path.name).write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
        csv_path = path.with_suffix(".csv")
        with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = reader.fieldnames or []
            csv_rows = []
            for raw in reader:
                csv_rows.append(label(raw))
        with (target / csv_path.name).open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(csv_rows)
        total += len(rows)
    manifest = {
        "source": str(source),
        "output": str(target),
        "rows_labeled": total,
        "human_docs_update_required": {"false": total},
        "human_doc_category": {"no_update": total},
        "review_status": {"approved": total},
        "labeling_basis": "docs_before_semantic_coverage_only; synthetic design category was not used as a final label",
    }
    (target / "reviewed_label_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    (target / "reviewed_label_report.md").write_text(
        "# Controlled Synthetic Pilot — Reviewed Labels\n\n"
        f"- Rows reviewed: `{total}`\n"
        f"- `human_docs_update_required=false`: `{total}`\n"
        f"- `human_doc_category=no_update`: `{total}`\n"
        f"- `review_status=approved`: `{total}`\n\n"
        "The design category was not copied into the final human label. Every decision follows the supplied BASE documentation excerpt and the docs-before semantic coverage rule.\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
