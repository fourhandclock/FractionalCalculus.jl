"""Authorized TeX-only resource acquisition; scientific acceptance uses offline builds."""
import json,shutil
from execution import *

def main():
    cache=ROOT/'.checkpoint-tools/tex-cache/Tectonic'
    before={str(p.relative_to(cache)):sha(p) for p in cache.rglob('*') if p.is_file()}
    # Preserve the complete named resource cache before acquisition, not just a guessed font list.
    report=REVIEW/'evidence/tex-resources-before-acquisition-03.json'
    assert not report.exists()
    report.write_text(json.dumps({'trigger':'r01-typeset02-latex-gr01:14: lmroman10-bold not cached',
        'known_missing_before_acquisition':['lmroman10-bold.otf'],
        'named_cache_manifests_before':{p.name:p.read_text() for p in (cache/'manifests').glob('*')},
        'policy':'Compile only the six requested sources to obtain their exact TeX transitive resources; do not use these acquisition PDFs as accepted artifacts',
        'cache_before':before},indent=2)+'\n')
    acquisitions=[]
    for source in sorted((STUDY/'revision-01/manuscripts').glob('*.tex')):
        work,_=run('r01-tex-acquisition-'+source.stem[:4].lower(),
            [ROOT/'.checkpoint-tools/bin/tectonic','--untrusted','--keep-logs','--keep-intermediates','--outdir','/var/tmp',source],
            wall=180,cpu=120,memory=2048,rss=1024,sources=[source,Path(__file__)],latex_cache=True)
        acquired=work/'cache/Tectonic'
        delta={str(p.relative_to(acquired)):sha(p) for p in acquired.rglob('*') if p.is_file() and
               (not (cache/p.relative_to(acquired)).exists() or sha(cache/p.relative_to(acquired))!=sha(p))}
        for name,h in delta.items():
            dest=cache/name;dest.parent.mkdir(parents=True,exist_ok=True)
            tmp=dest.with_name(dest.name+'.promotion');shutil.copyfile(acquired/name,tmp);tmp.replace(dest)
            assert sha(dest)==h
        acquisitions.append({'manuscript':source.name,'source_sha256':sha(source),'cache_delta':delta})
        (REVIEW/'evidence/tex-manuscript-resource-acquisition.json').write_text(json.dumps(acquisitions,indent=2)+'\n')
    print('Required manuscript resources acquired; all acceptance builds will be offline.')
if __name__=='__main__':main()
