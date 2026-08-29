from __future__ import annotations

import argparse, hashlib, json, os, random, re, time, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ORIGIN = "targeted_positive_enrichment_v1"
SURFACES = {
    "api_reference": ("api", "sdk", "client", "endpoint", "reference"),
    "configuration": ("config", "configuration", "environment", "settings", "options"),
    "developer_setup": ("install", "installation", "setup", "build", "development", "getting started"),
    "model_contract": ("schema", "model", "types", "payload", "interface", "data model"),
}
QUERIES = [
    "language:Python stars:100..20000 archived:false fork:false pushed:>2025-01-01 size:<200000",
    "language:TypeScript stars:100..20000 archived:false fork:false pushed:>2025-01-01 size:<200000",
    "language:Go stars:100..20000 archived:false fork:false pushed:>2025-01-01 size:<200000",
    "language:Rust stars:100..20000 archived:false fork:false pushed:>2025-01-01 size:<200000",
]

def api(path, token):
    req=urllib.request.Request("https://api.github.com"+path,headers={"Authorization":"Bearer "+token,"Accept":"application/vnd.github+json","X-GitHub-Api-Version":"2022-11-28","User-Agent":"docguard-targeted-enrichment-v1"})
    with urllib.request.urlopen(req,timeout=30) as r: return json.load(r)

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def main():
    p=argparse.ArgumentParser(); p.add_argument('--original',type=Path,required=True); p.add_argument('--output-dir',type=Path,required=True); p.add_argument('--seed',type=int,default=20260829); p.add_argument('--select',type=int,default=12); a=p.parse_args()
    token=os.environ['GITHUB_TOKEN']; a.output_dir.mkdir(parents=True,exist_ok=True)
    existing=set(); pairs=set()
    with a.original.open(encoding='utf-8') as f:
        for line in f:
            r=json.loads(line); repo=str(r['repository']).strip().lower(); existing.add(repo); pairs.add((repo,int(r['pr_number'])))
    found={}
    for q in QUERIES:
        data=api('/search/repositories?'+urllib.parse.urlencode({'q':q,'sort':'updated','order':'desc','per_page':100}),token)
        for x in data['items']:
            name=x['full_name'].lower()
            if name not in existing: found[name]=x
    rows=[]
    preselected=sorted(found.items(),key=lambda kv:(kv[1]['open_issues_count'],kv[1]['pushed_at']),reverse=True)[:80]
    for name,x in preselected:
        try:
            tree=api(f"/repos/{name}/git/trees/{x['default_branch']}?recursive=1",token).get('tree',[])
        except Exception: continue
        docs=[i['path'] for i in tree if i.get('type')=='blob' and re.search(r'(^|/)(readme[^/]*|docs?/.*\.(md|mdx|rst)|.*(api|config|schema|setup).*\.(md|mdx|rst))$',i['path'],re.I)]
        if len(docs)<4: continue
        text=' '.join(docs).lower(); signals={k:sum(1 for t in terms if t in text) for k,terms in SURFACES.items()}
        coverage=sum(v>0 for v in signals.values())
        if coverage<2: continue
        try: pulls=api(f'/repos/{name}/pulls?state=closed&per_page=1&sort=updated&direction=desc',token)
        except Exception: pulls=[]
        score=coverage*10+min(len(docs),40)/4+sum(min(v,3) for v in signals.values())+min(x['open_issues_count'],100)/25
        rows.append({'repository':name,'language':x.get('language'),'stars':x['stargazers_count'],'size_kb':x['size'],'pushed_at':x['pushed_at'],'documentation_file_count':len(docs),'documentation_surface_signals':signals,'surface_coverage':coverage,'has_closed_pr_history':bool(pulls),'score':round(score,3),'selection_reason':'first-party docs cover '+', '.join(k for k,v in signals.items() if v),'acquisition_origin':ORIGIN})
    rng=random.Random(a.seed); rng.shuffle(rows); rows.sort(key=lambda r:(r['has_closed_pr_history'],r['score']),reverse=True)
    selected=[]; owners={}
    for r in rows:
        owner=r['repository'].split('/')[0]
        if owners.get(owner,0)>=2: continue
        selected.append(r); owners[owner]=owners.get(owner,0)+1
        if len(selected)>=a.select: break
    allp=a.output_dir/'repository_candidates.jsonl'; selp=a.output_dir/'selected_repositories.jsonl'; listp=a.output_dir/'selected_repositories.txt'
    for path,data in ((allp,rows),(selp,selected)):
        path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in data),encoding='utf-8')
    listp.write_text('\n'.join(x['repository'] for x in selected)+'\n',encoding='utf-8')
    manifest={'schema':'docguard_targeted_repository_selection_v1','acquisition_origin':ORIGIN,'created_at':datetime.now(timezone.utc).isoformat(),'seed':a.seed,'queries':QUERIES,'original_repository_count':len(existing),'discovered_not_in_original':len(found),'metadata_preselection_count':len(preselected),'ranked_candidate_count':len(rows),'selected_count':len(selected),'selected_repositories':[x['repository'] for x in selected],'configuration':{'select':a.select,'metadata_preselection_limit':80,'minimum_docs':4,'minimum_surface_coverage':2,'owner_cap':2},'forbidden_selection_fields':['docs_changed_files','docs_diff_excerpt','docs_after_excerpt','human_label','gold_label','suggested_label'],'sha256':{allp.name:sha(allp),selp.name:sha(selp),listp.name:sha(listp)}}
    (a.output_dir/'repo_selection_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'selected':manifest['selected_repositories'],'ranked':len(rows),'existing_repos':len(existing)},indent=2))
if __name__=='__main__': main()
