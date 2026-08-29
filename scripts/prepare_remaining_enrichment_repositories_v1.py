import json
from pathlib import Path

root=Path(__file__).resolve().parents[1]
base=root/'data/final_v2/expansion/targeted_positive_enrichment_v1/repository_discovery'
original=root/'data/final_v2/human_review/candidate_partitioned_17880.jsonl'
existing=set()
compact=root/'data/final_v2/expansion/original_17880_exclusion_v1/original_repositories_normalized.txt'
if original.exists():
    with original.open(encoding='utf-8') as f:
        for line in f: existing.add(json.loads(line)['repository'].strip().lower())
elif compact.exists():
    existing={x.strip().lower() for x in compact.read_text(encoding='utf-8').splitlines() if x.strip()}
else:
    raise SystemExit('Missing both full original dataset and compact original exclusion manifest')
current={x.strip().lower() for x in (base/'explicit_repository_universe.txt').read_text().splitlines() if x.strip()}
candidates=[x.strip().lower() for x in (base/'remaining_repository_candidates.txt').read_text().splitlines() if x.strip()]
selected=[]; rejected=[]
for repo in candidates:
    reason='original_17880' if repo in existing else ('pilot_1200' if repo in current else None)
    if reason: rejected.append({'repository':repo,'reason':reason})
    elif repo not in selected: selected.append(repo)
out=base/'remaining_selected_repositories.txt'
out.write_text('\n'.join(selected)+'\n',encoding='utf-8')
for i in range(3):
    shard=selected[i::3]
    (base/f'remaining_selected_repositories_shard_{chr(65+i)}.txt').write_text('\n'.join(shard)+'\n',encoding='utf-8')
(base/'remaining_repository_dedupe_report.json').write_text(json.dumps({'candidate_count':len(candidates),'selected_count':len(selected),'rejected_count':len(rejected),'rejected':rejected},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'selected':len(selected),'rejected':len(rejected)},indent=2))
