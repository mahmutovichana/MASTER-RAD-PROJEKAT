# Jedan prompt za Codex na drugom laptopu

Kopiraj cijeli tekst ispod u novi Codex task na drugom Windows laptopu.

---

Radi autonomno do završetka. Korisnik želi približno 4.800 novih, stvarnih GitHub PR enrichment redova, potpuno odvojenih od originalnih 17.880 i od pilot sharda od 1.200. Ne traži potvrdu za normalne read/write/run/retry korake unutar ovog zadatka. Povremeno izvještavaj o napretku. Ne mijenjaj originalnih 17.880, njihove labele, hashove, partitions ili sealed confirmation.

1. Kloniraj `https://github.com/mahmutovichana/MASTER-RAD-PROJEKAT.git`, uđi u repo, pokreni `git lfs install` i `git lfs pull`. Instaliraj Python dependencies potrebne postojećem projektu, bez Docker servisa. Pročitaj `docs/targeted_enrichment_second_machine_setup.md`, `docs/final_human_review_protocol_v2.md`, `docguard_external/github_pr_seed_collector.py`, `docguard_external/github_pr_dataset_builder_v2.py`, `scripts/human_review_workflow_v2.py`, `scripts/prefill_human_label_sheet_v2.py` i `scripts/build_human_review_batches_v2.py` prije rada.

2. Zatraži od osobe da lokalno unese VLASTITI GitHub fine-grained token kroz `Read-Host`. Ne traži da token pošalje u chat. Token nikada ne zapisuj u repo, log, manifest ili tracked `.env`. Koristi ga samo kao process environment `GITHUB_TOKEN`.

3. Pokreni `python scripts/prepare_remaining_enrichment_repositories_v1.py`. Validiraj da output kaže 75 selected i 24 rejected protiv originalnih 17.880. Koristi tri liste:
   - `remaining_selected_repositories_shard_A.txt`
   - `remaining_selected_repositories_shard_B.txt`
   - `remaining_selected_repositories_shard_C.txt`

4. Sve outpute piši isključivo u `data/final_v2/expansion/targeted_positive_enrichment_v1_remaining_4800/`. Za svaki shard napravi zasebne `acquisition`, `candidates`, `cache/github_api`, `cache/git` i checkpoint foldere. Pokreni postojeći neutralni seed collector za svaki shard s ciljem približno 1.700 accepted seedova, `--max-prs-per-repo 80`, `--max-pages-per-repo 5`, `--max-changed-files 80`, `--max-total-patch-lines 12000`, authenticated bounded cacheom i `--allow-partial`. Seed selection ne smije koristiti docs changed/diff/after, human/gold/suggested labele ili bilo koji outcome.

5. Pokreni tri hardened V2 builder procesa paralelno, po jedan za svaki shard, svaki sa `--workers 1`, `--rest-max-inflight 1`, `--document-retrieval-backend auto`, `--max-generator-doc-files 12`, checkpointom svakih 25, durable `operational_pending.jsonl` i `--resume`. Napravi watcher za svaki proces: provjera svakih 60 sekundi; ako nema novog checkpointa 20 minuta i nema CPU/network aktivnosti, prekini samo taj proces i restartuj ga s `--resume`. Ne briši checkpoint. Network/timeout/rate-limit je operational pending, nikada scientific reject.

6. Nakon završetka svakog sharda ponavljaj `--retry-operational-pending` dok pending ne bude 0 ili dok tri uzastopna pokušaja ne vrate isti konkretan blocker. Validiraj `accepted + scientific_rejects + pending = attempted`. Prije nastavka mora biti pending=0.

7. Spoji accepted candidates iz tri sharda. Dodaj `acquisition_origin="targeted_positive_enrichment_v1_remaining_4800"`. Dedupe po normalized `repository + pr_number` unutar expansiona, protiv originalnih 17.880 i protiv `targeted_positive_enrichment_v1/acquisition/pilot_pr_seeds.jsonl`. Ne koristi docs outcome. Ako ima više od 4.800 validnih redova, odaberi deterministički 4.800 uz repository cap i približno balansirane enrichment surface signale API/config/setup/model; signali nisu labele. Ako ih ima manje, zadrži sve i jasno prijavi deficit — ne spuštaj scientific kriterije.

8. Očuvaj evidence semantiku: `case_id`, `repository`, `pr_number`, `language`, `code_changed_files`, `code_diff_excerpt`, `docs_before_excerpt`, `docs_before_retrieved_files`, do 12 `documentation_context_candidates`, sve isključivo iz BASE SHA. Nikada ne učitavaj docs-after, comments ili outcome metadata za labeliranje.

9. Pokreni prefill i napravi contextual CSV batcheve od po 100 redova. Zatim LIČNO pregledaj svaki red redom: `code_changed_files`, `code_diff_excerpt`, `docs_before_excerpt`, pa širi BASE-SHA context; suggested podatke eventualno tek kao secondary check. Pitanje je: bi li code change učinio postojeću dokumentaciju netačnom, zastarjelom ili materijalno nepotpunom u onome što već pokriva? Popuni samo `human_docs_update_required`, `human_doc_category`, `human_label_notes`, `review_status` u `reviewed_batches`. Sve labele su draft human-review prijedlozi za korisnikovu potpunu provjeru, ne automatski gold.

10. Taxonomy: false=`no_update`; true=`api_reference|configuration|developer_setup|model_contract|other_documentation`; insufficient evidence=`excluded`. `other_documentation` nije uncertainty bucket. Notes kratke, naročito za positive/granične/excluded. Ne dodaj/briši/sortiraj redove i ne mijenjaj evidence/context/hash kolone.

11. Nakon svakog batcha validiraj header, broj/redoslijed redova, UTF-8, dozvoljene kolone, `review_row_hash` i `review_context_hash`. Na kraju validiraj svih približno 4.800 redova i generiši manifest/report sa repoima, seedovima, accepted/reject/pending, surface/language/repo distribucijom, dedupe countom, SHA256 svih finalnih outputa, cache veličinom i listom cache foldera sigurnih za brisanje.

12. Ne mergeaj ovaj expansion s originalnih 17.880. Commitaj i pushaj samo kod, manifeste, reportove, final candidates/prefilled/review CSV-e koji su ispod GitHub limita. Ne pushaj token, regenerabilne cacheve, runtime logove ili nepotrebne working trees. Ako su finalni veliki fajlovi iznad GitHub limita, koristi postojeći Git LFS samo nakon provjere dostupne LFS kvote; inače ih ostavi lokalno i prijavi tačne putanje i veličine.

Ne završavaj task dok finalni reviewed CSV batchevi nisu popunjeni i validirani, ili dok ne postoji konkretan ponovljen blocker koji se ne može riješiti bez korisnika.

---
