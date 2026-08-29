# Targeted enrichment: setup na drugom računaru

## macOS / MacBook

Instalacija:

```bash
xcode-select --install
brew install git git-lfs python@3.12
git lfs install
git clone https://github.com/mahmutovichana/MASTER-RAD-PROJEKAT.git
cd MASTER-RAD-PROJEKAT
git lfs pull
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip pytest scikit-learn
```

Token treba postaviti prije ponovnog pokretanja Codexa:

```bash
read -s GITHUB_TOKEN
echo
launchctl setenv GITHUB_TOKEN "$GITHUB_TOKEN"
unset GITHUB_TOKEN
```

Potpuno zatvoriti Codex sa `Cmd+Q`, pa ga ponovo otvoriti. Nakon završetka:

```bash
launchctl unsetenv GITHUB_TOKEN
```

## Windows preduvjeti

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
