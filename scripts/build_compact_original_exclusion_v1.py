import hashlib, json
from pathlib import Path

root=Path(__file__).resolve().parents[1]
source=root/'data/final_v2/human_review/candidate_partitioned_17880.jsonl'
out=root/'data/final_v2/expansion/original_17880_exclusion_v1'
out.mkdir(parents=True,exist_ok=True)
repos=set(); pairs=set(); rows=0
with source.open(encoding='utf-8') as f:
    for line in f:
        r=json.loads(line); repo=str(r['repository']).strip().lower(); pr=int(r['pr_number'])
        repos.add(repo); pairs.add((repo,pr)); rows+=1
repo_path=out/'original_repositories_normalized.txt'
pair_path=out/'original_repository_pr_keys.jsonl'
repo_path.write_text('\n'.join(sorted(repos))+'\n',encoding='utf-8')
pair_path.write_text(''.join(json.dumps({'repository':r,'pr_number':p},separators=(',',':'))+'\n' for r,p in sorted(pairs)),encoding='utf-8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
manifest={'schema':'docguard_original_17880_compact_exclusion_v1','source_row_count':rows,'normalized_repository_count':len(repos),'repository_pr_key_count':len(pairs),'files':{repo_path.name:{'sha256':sha(repo_path),'bytes':repo_path.stat().st_size},pair_path.name:{'sha256':sha(pair_path),'bytes':pair_path.stat().st_size}}}
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print(json.dumps(manifest,indent=2))
