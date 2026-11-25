"""Read-only assessment of sealed evidence and fresh runs; writes new summaries only."""
import csv,hashlib,json,re,shutil
from pathlib import Path
from execution import ROOT,REVIEW,ORIGINAL,check_preserved,sha

def write(name,data):
    path=REVIEW/'evidence'/name
    assert not path.exists(),path
    path.write_text(json.dumps(data,indent=2)+'\n')

def main():
    check_preserved();runs=REVIEW/'evidence/runs'
    for label,name in [('aud02-abstract-01','abstract.json')]:
        source=ROOT/'.checkpoint-tools/runs'/label/name
        shutil.copyfile(source,REVIEW/'evidence/targeted'/name)
    records=[]
    for module in ['CoefficientsAxioms','QuadratureAxioms','Aud01Axioms','Aud02Axioms']:
        path=runs/('aud02-lean-'+module.lower()+'-01.stdout.log')
        for name,axioms in re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]",path.read_text()):
            ax=[a.strip() for a in axioms.split(',') if a.strip()]
            assert set(ax)<= {'propext','Classical.choice','Quot.sound'},(name,ax)
            records.append({'name':name,'axioms':ax,'audit_output':str(path.relative_to(REVIEW))})
        for name in re.findall(r"'([^']+)' does not depend on any axioms",path.read_text()):
            records.append({'name':name,'axioms':[],'audit_output':str(path.relative_to(REVIEW))})
    assert len(records)==len({r['name'] for r in records})==54
    old=[r for r in records if '.AUD02.' not in r['name']];assert len(old)==42
    olddir=ROOT/'research/legendre/verification/lean'
    sources=[olddir/(n+'.lean') for n in ['Coefficients','Quadrature','AuditConstants','Aud01FiniteSums','Aud01Oscillator']]+[REVIEW/'lean/Aud02Finite.lean']
    for path in sources:
        source=path.read_text()
        assert not re.search(r'\b(sorry|admit)\b',source),path
        assert not re.search(r'^\s*axiom\b',source,re.M),path
    write('lean-audit.json',{'toolchain':(olddir/'lean-toolchain').read_text().strip(),
        'mathlib_revision':'c44e0c8ee63ca166450922a373c7409c5d26b00b',
        'preserved_named':42,'preserved_identity_groups':41,'new_named':12,'total_named':54,
        'new_identity_independence_claim':False,'sources':{str(p.relative_to(ROOT)):sha(p) for p in sources},'theorems':records})
    cases={}
    for name in ['julia_results.csv','python_reference.csv']:
        rows=list(csv.DictReader(open(REVIEW/'evidence/targeted'/name)))
        keys=[tuple(r[k] for k in ['alpha','beta','case','variant','grading','N','M']) for r in rows]
        assert len(rows)==len(set(keys))==156
        cases[name]={'rows':len(rows),'unique_keys':len(set(keys)),
                     'maximum_scaled_residual':max(float(r['scaled_residual']) for r in rows)}
    timing=list(csv.DictReader(open(ROOT/'studies/legendre/gr07/results/timing_repeats.csv')))
    warm=list(csv.DictReader(open(ROOT/'studies/legendre/gr07/results/warmups.csv')))
    assert len(timing)==420 and len(warm)==84
    assert all(float(r['total_compile_s'])==0 and float(r['total_recompile_s'])==0 for r in timing)
    groups={}
    for r in timing:
        key=tuple(r[k] for k in ['N','case','variant','grading','phase'])
        groups.setdefault(key,[]).append(int(r['repeat']))
    assert len(groups)==84 and all(sorted(v)==[1,2,3,4,5] for v in groups.values())
    write('evidence-review.json',{'fresh_cases':cases,'preserved_timing_rows':len(timing),
         'preserved_warmup_rows':len(warm),'timing_phase_groups':len(groups),
         'all_groups_have_five_distinct_repetitions':True,'measured_compilation_seconds':0,
         'performance_remeasured':False,'invalid_initial_reference_used':False})
    source_root=ROOT.parents[2]
    guard_path=source_root/'.checkpoint-tools/gr07-2026-11-26/preflight/original-workspace.json'
    guard=json.loads(guard_path.read_text())
    bad=[name for name,item in guard['files'].items() if not (source_root/name).is_file() or sha(source_root/name)!=item['sha256']]
    write('workspace-preservation.json',{'guard':'original GR-07 preflight workspace snapshot',
        'guard_sha256':sha(guard_path),'files_checked':len(guard['files']),'mismatches':bad,
        'scope':'Existing source/navigation/metric-graph files in the original workspace; audit outputs are separate additions.'})
    assert not bad,bad
    successful=[];failed=[]
    for path in sorted(runs.glob('*.json')):
        if path.name.endswith('.namespace.json'):continue
        d=json.loads(path.read_text());label=path.stem
        assert json.loads((runs/(label+'.namespace.json')).read_text())['namespace_cleanup_verified']
        (successful if d['returncode']==0 else failed).append({'label':label,'returncode':d['returncode'],'elapsed_seconds':d['elapsed_seconds']})
    assert {r['label'] for r in failed}=={'aud02-lean-aud02finite-01','aud02-lean-aud02finite-03','aud02-boundary-acceptance-01'}
    write('run-summary.json',{'successful':successful,'failed':failed,'all_started_namespaces_cleaned':True,
        'prelaunch_attempt':'evidence/preflight/prelaunch-01.json','all_scientific_runs_serial':True,
        'aggregate_cgroup_isolation':False})
    print('PASS: 54 theorem axiom records, 156+156 unique cases, 420 timing rows, source and original-workspace guards; known boundary failure retained.')
if __name__=='__main__':main()
