"""Trusted GR-07 serial run controller; no scientific formulas or package setup.

New attempts get fresh scratch and evidence names. Reuses AUD-01's supervisor
under the user's explicit per-process/sampled resource-policy exception.
Sources, supplied evidence and baseline files are read-only inside each payload.
"""
from pathlib import Path
import hashlib,json,os,subprocess,sys,time

ROOT=Path(__file__).resolve().parents[4]
STUDY=ROOT/'studies/legendre/gr07'
EVIDENCE=STUDY/'evidence/runs'
RUNNER=ROOT/'research/legendre/verification/scripts/run_bounded.py'
ISOLATE=STUDY/'scripts/isolate.py'
PYTHON=ROOT/'.checkpoint-tools/python-aud01/bin/python'
JULIA=ROOT/'.checkpoint-tools/julia-1.12.6/bin/julia'


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def check_preserved():
    for filename,base in [('baseline.json',ROOT),('supplied-inputs.json',STUDY/'reference')]:
        manifest=json.loads((STUDY/'evidence'/filename).read_text())
        bad=[n for n,item in manifest['files'].items() if not (base/n).is_file() or sha(base/n)!=item['sha256']]
        assert not bad,('baseline/input drift',bad)


def namespace_survivors(identity):
    survivors=[]
    for p in Path('/proc').glob('[0-9]*/ns/pid'):
        try:
            if os.readlink(p)==identity:survivors.append(int(p.parents[1].name))
        except OSError:pass
    return survivors


def run(label,command,*,wall=300,cpu=240,memory=8192,rss=2048,sources=()):
    policy=json.loads((STUDY/'evidence/execution-policy.json').read_text())
    assert policy['user_approved_bounded_serial_policy'] is True
    check_preserved()
    scratch=ROOT/'.checkpoint-tools/runs'/label
    scratch.mkdir(parents=True,exist_ok=False)
    for p in ['tmp','cache','depot']: (scratch/p).mkdir()
    # Every payload records its PID-namespace identity before scientific code.
    wrapper=scratch/'payload.py'
    wrapper.write_text('import os,json,sys\nfrom pathlib import Path\nPath("/var/tmp/namespace.json").write_text(json.dumps({"pid_namespace":os.readlink("/proc/self/ns/pid")}))\nos.execv(sys.argv[1],sys.argv[1:])\n')
    env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',JULIA_NUM_THREADS='1',
             JULIA_NUM_PRECOMPILE_TASKS='1',JULIA_PKG_OFFLINE='true',JULIA_PKG_SERVER='',
             JULIA_LOAD_PATH='@:@stdlib',JULIA_DEPOT_PATH='/var/tmp/depot:'+str(ROOT/'.checkpoint-tools/shared-julia-depot'),
             PYTHONNOUSERSITE='1',XDG_CACHE_HOME=str(ROOT/'.checkpoint-tools/cache'))
    env.pop('PYTHONPATH',None)
    args=['python3','-B',str(RUNNER),'--label',label,'--timeout',str(wall),'--cpu-seconds',str(cpu),
          '--memory-mib',str(memory),'--resident-mib',str(rss),'--evidence',str(EVIDENCE)]
    for source in [ISOLATE,Path(__file__),wrapper,*sources]:args+=['--source',str(Path(source).resolve())]
    args+=['--',sys.executable,'-B',str(ISOLATE),str(scratch),'/usr/bin/python3','-B','/var/tmp/payload.py',*map(str,command)]
    subprocess.run(args,env=env,timeout=wall+30,check=False)
    record=json.loads((EVIDENCE/(label+'.json')).read_text())
    identity_file=scratch/'namespace.json'
    survivors=namespace_survivors(json.loads(identity_file.read_text())['pid_namespace']) if identity_file.exists() else []
    cleanup={'namespace_started':identity_file.exists(),'surviving_namespace_pids':survivors,
             'namespace_cleanup_verified':identity_file.exists() and not survivors,
             'bwrap_info':json.loads((scratch/'bwrap-info.json').read_text()) if (scratch/'bwrap-info.json').exists() else None,
             'scope':'Linux PID namespace; no cgroup aggregate-resource claim.'}
    (EVIDENCE/(label+'.namespace.json')).write_text(json.dumps(cleanup,indent=2)+'\n')
    check_preserved()
    assert cleanup['namespace_cleanup_verified'],('cleanup not verified',label,cleanup)
    assert record['returncode']==0,('run failed; exact source/output retained',label,record['returncode'])
    return scratch,record


def julia(script,*args,project=ROOT):
    return [JULIA,'--startup-file=no','--heap-size-hint=512M','--gcthreads=1','--project='+str(project),script,*args]

if __name__=='__main__':
    raise SystemExit('Import this local controller from the prescribed replay steps; no implicit runs.')
