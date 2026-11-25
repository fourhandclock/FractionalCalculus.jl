"""Replay only the supplied final diagnostics and the admitted scientific matrix.

Preserved invalid/failed initial programs are never scientific inputs here.
No performance measurements or algorithm changes are made.
"""
import shutil
from execution import *

def copy_new(p,name):
    q=REVIEW/'evidence/targeted'/name
    assert not q.exists(),q
    shutil.copyfile(p,q)

def main():
    diag=STUDY/'reference/reference_diagnostics'
    for ident,name in [('gr02','verify_gr02.py'),('gr03','verify_gr03.py'),('gr04','verify_gr04.py'),('gr05','verify_gr05.py')]:
        deps=[diag/'verify_gr03.py'] if ident in ('gr04','gr05') else []
        run('aud02-python-'+ident+'-01',[PYTHON,'-s','-B',diag/name],memory=2048,rss=1024,sources=[diag/name,*deps])
    ref=STUDY/'reference'
    work,_=run('aud02-python-reference-01',[PYTHON,'-s','-B',ref/'benchmark_gr07.py','/var/tmp/reference.csv'],
       memory=2048,rss=1024,sources=[ref/'benchmark_gr07.py',ref/'verify_gr06_graded.py'])
    copy_new(work/'reference.csv','python_reference.csv')
    work,_=run('aud02-julia-matrix-01',julia(STUDY/'run.jl','--output-dir=/var/tmp/results'),
       wall=600,cpu=540,sources=[STUDY/'GR07.jl',STUDY/'run.jl',ROOT/'Manifest.toml'])
    copy_new(work/'results/julia_results.csv','julia_results.csv')
    compare=STUDY/'scripts/compare.py';out=REVIEW/'evidence/targeted'
    for label,a,b in [('fresh',out/'python_reference.csv',out/'julia_results.csv'),
                      ('julia-preserved',STUDY/'results/julia_results.csv',out/'julia_results.csv'),
                      ('python-preserved',STUDY/'results/python_reference.csv',out/'python_reference.csv')]:
        # Distinct basenames in source capsules avoid the old runner's basename collision.
        run('aud02-compare-'+label+'-01',[PYTHON,'-s','-B',compare,a,b],wall=60,cpu=45,memory=1024,rss=512,
           sources=[compare])
    run('aud02-python-environment-01',[PYTHON,'-s','-B',STUDY/'scripts/python_environment.py'],
        wall=60,cpu=45,memory=1024,rss=512,sources=[STUDY/'scripts/python_environment.py'])
    run('aud02-julia-environment-01',julia(STUDY/'scripts/environment.jl'),wall=90,cpu=60,
        sources=[STUDY/'scripts/environment.jl',ROOT/'Manifest.toml'])
    print('AUD-02 final-diagnostic and matrix replay completed; original results unchanged.')
if __name__=='__main__':main()
