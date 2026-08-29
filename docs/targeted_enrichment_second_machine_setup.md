# Targeted enrichment: setup na drugom Windows računaru

## Preduvjeti

- Git for Windows i Git LFS
- Python 3.11+ (projekat trenutno radi na Pythonu 3.14)
- najmanje 80 GB slobodnog prostora
- vlastiti GitHub fine-grained token s read pristupom javnim repozitorijima
- Codex prijavljen na korisnikov profil nije zamjena za `GITHUB_TOKEN`

Svaka osoba treba koristiti vlastiti token. Token se ne šalje u chat, ne commita i ne upisuje u `.env` koji se prati Gitom.

## Prvi setup

```powershell
git clone https://github.com/mahmutovichana/MASTER-RAD-PROJEKAT.git
cd MASTER-RAD-PROJEKAT
git lfs install
git lfs pull
python -m pip install -U pip
python -m pip install pytest scikit-learn
```

## Pokretanje unattended workflowa

```powershell
$token = Read-Host "GitHub token"
powershell -ExecutionPolicy Bypass -File scripts/start_targeted_enrichment_watcher.ps1 -GitHubToken $token
```

Watcher nastavlja iz checkpointa, nakon 15 minuta bez napretka restartuje builder s jednim workerom, provjerava `operational_pending` i po uspješnom završetku pravi `pilot_prefilled.jsonl` i CSV batcheve od po 100 redova. Ne pravi reviewed fajlove i ne mijenja originalnih 17.880.

## Provjera napretka

```powershell
Get-Content data/final_v2/expansion/targeted_positive_enrichment_v1/candidates/.checkpoints/progress_state.json
```

Regenerabilni `cache/github_api`, `cache/git`, logovi i `.checkpoints` mogu se obrisati tek nakon što su finalni candidates, manifesti i review batchevi validirani i sigurnosno kopirani.
