"""Fresh serial GR-07 replay; preserve every previous result and run record.

Dependencies must already be present. A new run ID creates separate results and
metadata. --performance additionally validates admissions before timing. No
Git operation, dependency setup, remote service or network request occurs here.
"""
import argparse,hashlib,json,os,shutil,tomllib
from pathlib import Path
from execution import run,julia,ROOT,STUDY,PYTHON,check_preserved
from admit import main as admit


def copy_output(source,dest):
    assert not dest.exists(),dest
    shutil.copyfile(source,dest)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-id',required=True)
    parser.add_argument('--performance',action='store_true')
    args=parser.parse_args();ident=args.run_id
    assert ident and all(c.isalnum() or c in '-_' for c in ident)
    out=STUDY/'results'/ident;meta=STUDY/'evidence/replays'/ident
    out.mkdir(exist_ok=False);meta.mkdir(parents=True,exist_ok=False)
    prefix=ident+'-';self_source=Path(__file__).resolve()
    def launch(label,command,**kwargs):
        kwargs['sources']=[*kwargs.get('sources',()),self_source]
        return run(prefix+label,command,**kwargs)
    check_preserved()
    fixture=STUDY/'evidence/runs/isolation-fixture-01.fixture_gr07.py.source.txt'
    probe=ROOT/'.checkpoint-tools'/('probe-'+ident);probe.mkdir()
    (probe/'input.txt').write_text('immutable replay probe\n')
    os.environ['GR07_PROBE_SOURCE']=str(probe/'input.txt')
    launch('isolation-fixture-01',['/usr/bin/python3','-B',fixture],wall=10,cpu=5,memory=512,rss=256,sources=[fixture])
    del os.environ['GR07_PROBE_SOURCE']
    launch('baseline-regression-01',julia(ROOT/'test/runtests.jl'),sources=[ROOT/'Project.toml',ROOT/'Manifest.toml',ROOT/'test/runtests.jl'])
    work,_=launch('local-oracle-02',[PYTHON,'-s','-B',STUDY/'scripts/make_oracles.py','/var/tmp/moments.csv'],memory=2048,rss=1024,sources=[STUDY/'scripts/make_oracles.py'])
    copy_output(work/'moments.csv',out/'moments.csv')
    launch('julia-unit-02',julia(STUDY/'test/runtests.jl','--oracles='+str(out/'moments.csv')),sources=[STUDY/'GR07.jl',STUDY/'test/runtests.jl',out/'moments.csv'])
    launch('environment-01',julia(STUDY/'scripts/environment.jl'),wall=90,cpu=60,sources=[STUDY/'scripts/environment.jl',ROOT/'Manifest.toml'])
    launch('python-environment-01',[PYTHON,'-s','-B',STUDY/'scripts/python_environment.py'],wall=60,cpu=45,memory=1024,rss=512,sources=[STUDY/'scripts/python_environment.py'])
    logs=STUDY/'evidence/runs'
    env=tomllib.loads((logs/(prefix+'environment-01.stdout.log')).read_text())
    env['python']=json.loads((logs/(prefix+'python-environment-01.stdout.log')).read_text())
    (meta/'environment.json').write_text(json.dumps(env,indent=2)+'\n')
    diag=STUDY/'reference/reference_diagnostics'
    for label,file in [('python-gr02-01','verify_gr02.py'),('python-gr03-01','verify_gr03.py'),('python-gr04-01','verify_gr04.py'),('python-gr05-01','verify_gr05.py'),('python-gr06-01','verify_gr06_graded.py')]:
        deps=[diag/'verify_gr03.py'] if 'gr04' in file or 'gr05' in file else []
        launch(label,[PYTHON,'-s','-B',diag/file],memory=2048,rss=1024,sources=[diag/file,*deps])
    ref=STUDY/'reference'
    work,_=launch('python-reference-01',[PYTHON,'-s','-B',ref/'benchmark_gr07.py','/var/tmp/reference.csv'],memory=2048,rss=1024,sources=[ref/'benchmark_gr07.py',ref/'verify_gr06_graded.py'])
    copy_output(work/'reference.csv',out/'python_reference.csv')
    compare=STUDY/'scripts/compare.py'
    launch('reference-replay-comparison-01',[PYTHON,'-s','-B',compare,ref/'results.csv',out/'python_reference.csv'],wall=60,cpu=45,memory=1024,rss=512,sources=[compare,ref/'results.csv',out/'python_reference.csv'])
    work,_=launch('julia-matrix-01',julia(STUDY/'run.jl','--output-dir=/var/tmp/results'),wall=600,cpu=540,sources=[STUDY/'GR07.jl',STUDY/'run.jl',ROOT/'Manifest.toml'])
    copy_output(work/'results/julia_results.csv',out/'julia_results.csv')
    launch('julia-reference-comparison-01',[PYTHON,'-s','-B',compare,out/'python_reference.csv',out/'julia_results.csv'],wall=60,cpu=45,memory=1024,rss=512,sources=[compare,out/'python_reference.csv',out/'julia_results.csv'])
    copy_output(logs/(prefix+'julia-reference-comparison-01.stdout.log'),out/'julia_reference_comparison.json')
    launch('final-regression-01',julia(ROOT/'test/runtests.jl'),sources=[ROOT/'Project.toml',ROOT/'Manifest.toml',ROOT/'test/runtests.jl'])
    admit(out,prefix,meta)
    if args.performance:
        work,_=launch('julia-performance-01',julia(STUDY/'benchmark.jl','--admission='+str(meta/'admission.toml'),'--output-dir=/var/tmp/performance'),wall=600,cpu=540,sources=[STUDY/'GR07.jl',STUDY/'benchmark.jl',meta/'admission.toml',meta/'environment.json'])
        for name in ['timing_repeats.csv','warmups.csv']:copy_output(work/'performance'/name,out/name)
        work,_=launch('summary-01',[PYTHON,'-s','-B',STUDY/'scripts/summarize.py',out/'julia_results.csv',out/'timing_repeats.csv','/var/tmp/summary'],wall=60,cpu=45,memory=1024,rss=512,sources=[STUDY/'scripts/summarize.py'])
        for p in (work/'summary').iterdir():copy_output(p,out/p.name)
        work,_=launch('figures-01',[PYTHON,'-s','-B',STUDY/'scripts/plots.py',out/'julia_results.csv',out/'timing_repeats.csv','/var/tmp/figures'],wall=60,cpu=45,memory=1024,rss=512,sources=[STUDY/'scripts/plots.py'])
        dest=STUDY/'figures'/ident;dest.mkdir()
        for p in (work/'figures').iterdir():copy_output(p,dest/p.name)
    check_preserved()
    print('REPLAY COMPLETE:',ident,'performance:',args.performance,'results:',out)

if __name__=='__main__':main()
