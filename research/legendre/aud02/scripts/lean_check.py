"""Compile one pinned-source Lean module and retain compiler output/axioms."""
import argparse,shutil
from execution import *

def main():
    p=argparse.ArgumentParser();p.add_argument('module');p.add_argument('attempt');a=p.parse_args()
    legacy=ROOT/'research/legendre/verification/lean'
    source=(REVIEW/'lean' if a.module.startswith('Aud02') else legacy)/(a.module+'.lean')
    cache=REVIEW/'lean/legacy-cache'
    packages=legacy/'.lake/packages'
    paths=[str(cache),*[str(q) for q in packages.glob('*/.lake/build/lib/lean')]]
    work,record=run('aud02-lean-'+a.module.lower()+'-'+a.attempt,
       [LEAN,'-j1','--root='+str(source.parent),'-o','/var/tmp/'+a.module+'.olean',source],
       wall=120,cpu=90,memory=8192,rss=3584,sources=[source,legacy/'lean-toolchain',legacy/'lake-manifest.json'],
       extra_env={'LEAN_PATH':':'.join(paths),'LEAN_NUM_THREADS':'1'},require_success=False)
    if record['returncode']==0 and (work/(a.module+'.olean')).exists():
        shutil.copyfile(work/(a.module+'.olean'),cache/(a.module+'.olean'))
    raise SystemExit(0 if record['returncode']==0 else 1)
if __name__=='__main__':main()
