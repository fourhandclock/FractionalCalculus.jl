"""Inventory the prepared tree and intended delta; no Git access or writes elsewhere."""
import hashlib,json
from pathlib import Path
from execution import ROOT,REVIEW,check_preserved,sha

OUTPUTS={'FILES.txt','SHA256SUMS','evidence/checkpoint-manifest.json'}
EXCLUDE={'.git','.checkpoint-tools','.lake','__pycache__','legacy-cache'}

def files():
    found=[]
    for p in sorted(ROOT.rglob('*')):
        rel=p.relative_to(ROOT)
        if set(rel.parts)&EXCLUDE or not p.is_file():continue
        if p.is_symlink():raise AssertionError(('unreviewed source symlink',str(rel)))
        if p.is_relative_to(REVIEW/'literature'):continue # local primary review copies
        if p.is_relative_to(REVIEW) and str(p.relative_to(REVIEW)) in OUTPUTS:continue
        found.append((str(rel),p))
    return found

def main():
    check_preserved()
    baseline=json.loads((REVIEW/'evidence/input-manifest.json').read_text())['files']
    rows=[dict(path=n,sha256=sha(p),bytes=p.stat().st_size) for n,p in files()]
    changes=[]
    for r in rows:
        if r['path'] not in baseline:changes.append(dict(**r,change='created'))
        elif baseline[r['path']]['sha256']!=r['sha256']:changes.append(dict(**r,change='modified'))
    assert len([r for r in changes if r['change']=='modified'])==5
    assert not any(p.startswith(('src/','test/','examples/')) for p in [r['path'] for r in changes])
    record=dict(purpose='Validated checkpoint source/artifact inventory; Git publication recorded separately',
        full_tree_files=len(rows),bytes=sum(r['bytes'] for r in rows),
        intended_delta_files=len(changes),changes=changes,
        excluded='Runtime/build caches, local downloaded review papers, and the three self-referential inventory outputs',
        preservation='All original files checked separately by input-manifest.json and integrity.json')
    (REVIEW/'evidence/checkpoint-manifest.json').write_text(json.dumps(record,indent=2)+'\n')
    (REVIEW/'FILES.txt').write_text('Intended local checkpoint delta (paths relative to prepared workspace root)\n\n'+
        ''.join(r['change'].ljust(9)+r['path']+'\n' for r in changes))
    sums=REVIEW/'SHA256SUMS'
    sums.write_text(''.join(r['sha256']+'  '+r['path']+'\n' for r in rows))
    for r in rows:assert sha(ROOT/r['path'])==r['sha256'],r['path']
    print(json.dumps({k:record[k] for k in ['full_tree_files','bytes','intended_delta_files']},indent=2))
if __name__=='__main__':main()
