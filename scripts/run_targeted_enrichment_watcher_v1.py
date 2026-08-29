from __future__ import annotations

import argparse, json, os, subprocess, sys, time
from pathlib import Path

ORIGIN = "targeted_positive_enrichment_v1"

def load(path):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}

def lines(path):
    if not path.exists(): return []
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]

def run_builder(root, workers, resume=True):
    base=root/'data/final_v2/expansion'/ORIGIN
    cmd=[sys.executable,'-m','docguard_external.github_pr_dataset_builder_v2','--input',str(base/'acquisition/pilot_pr_seeds.jsonl'),'--output',str(base/'candidates/pilot_candidates_raw.jsonl'),'--rejects',str(base/'acquisition/scientific_rejects.jsonl'),'--report',str(base/'candidates/candidate_build_report.md'),'--max-cases','1200','--max-generator-doc-files','12','--cache-dir',str(base/'cache/github_api'),'--git-cache-dir',str(base/'cache/git'),'--document-retrieval-backend','auto','--checkpoint-dir',str(base/'candidates/.checkpoints'),'--checkpoint-every','25','--progress-every','25','--workers',str(workers),'--rest-max-inflight',str(workers),'--operational-pending',str(base/'acquisition/operational_pending.jsonl'),'--require-authenticated','--min-request-interval-seconds','0.05']
    if resume: cmd.append('--resume')
    return subprocess.Popen(cmd,cwd=root,stdout=(base/'candidates/watcher_builder.stdout.log').open('a',encoding='utf-8'),stderr=(base/'candidates/watcher_builder.stderr.log').open('a',encoding='utf-8'))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',type=Path,default=Path.cwd()); ap.add_argument('--stall-minutes',type=int,default=15); a=ap.parse_args()
    if not os.environ.get('GITHUB_TOKEN'): raise SystemExit('GITHUB_TOKEN is required')
    root=a.root.resolve(); base=root/'data/final_v2/expansion'/ORIGIN; progress=base/'candidates/.checkpoints/progress_state.json'
    workers=4; proc=run_builder(root,workers); last_count=-1; last_change=time.monotonic()
    while True:
        state=load(progress); count=int(state.get('completed_seed_count',0))
        if count!=last_count: print(f"progress {count}/{state.get('total_seed_count',1200)}",flush=True); last_count=count; last_change=time.monotonic()
        if state.get('complete'):
            if proc.poll() is None: proc.wait(timeout=120)
            break
        if proc.poll() is not None or time.monotonic()-last_change>a.stall_minutes*60:
            if proc.poll() is None: proc.terminate(); time.sleep(5); proc.kill() if proc.poll() is None else None
            workers=1
            print(f"restart from checkpoint {count} with workers=1",flush=True)
            proc=run_builder(root,workers); last_change=time.monotonic()
        time.sleep(30)
    pending=lines(base/'acquisition/operational_pending.jsonl')
    if pending: raise SystemExit(f"Builder complete but operational_pending={len(pending)}; run retry before review batching")
    raw=lines(base/'candidates/pilot_candidates_raw.jsonl')
    final=base/'candidates/pilot_candidates.jsonl'
    for row in raw: row['acquisition_origin']=ORIGIN
    final.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in raw),encoding='utf-8')
    human=base/'human_review'; human.mkdir(parents=True,exist_ok=True)
    subprocess.run([sys.executable,'scripts/prefill_human_label_sheet_v2.py','--input',str(final),'--output',str(human/'pilot_prefilled.jsonl')],cwd=root,check=True)
    subprocess.run([sys.executable,'scripts/build_human_review_batches_v2.py','--input',str(human/'pilot_prefilled.jsonl'),'--output-dir',str(human/'review_batches'),'--batch-size','100','--seed','20260829'],cwd=root,check=True)
    print(f"DONE candidates={len(raw)} review_batches={human/'review_batches'}",flush=True)
if __name__=='__main__': main()
