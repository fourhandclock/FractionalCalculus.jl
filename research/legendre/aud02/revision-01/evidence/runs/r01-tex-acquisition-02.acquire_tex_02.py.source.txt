"""Acquire only required TeX resources after explicit user approval.

This is a separate acquisition fixture, not a research experiment. It uses the
existing engine and fixed default bundle, writes only workspace-local scratch,
then promotes its cache to the private revision cache. No global environment
or original cache is changed.
"""
import json,shutil
from execution import *

def manifest(base):
    return {str(p.relative_to(base)):sha(p) for p in base.rglob('*') if p.is_file()}

def main():
    fixture=REVIEW/'evidence/tex-resource-fixture-02.tex'
    assert not fixture.exists()
    fixture.write_text(r"""\documentclass[11pt,a4paper]{article}
\usepackage[margin=23mm]{geometry}
\usepackage{amsmath,amssymb,amsthm,mathtools,booktabs,microtype}
\usepackage[hidelinks]{hyperref}
\begin{document}
\title{Required manuscript title resources}
\author{Research validation}\date{26 November 2026}
\maketitle
\section{Manuscript-sized mathematics}
\begin{equation}
\mathbb{R}\ni x=\sum_{j=1}^{n}\int_0^t\frac{(t-s)^{r-1}}{\Gamma(r)}\,ds,
\quad \mathcal{L}=\left(\frac{1+\alpha}{2-\alpha}\right)^{3/2}.
\end{equation}
Required resource fixture: $x^2+\Gamma(1+r)$.
\begin{tabular}{cc}\toprule A&B\\\midrule 1&2\\\bottomrule\end{tabular}
\end{document}
""")
    assert (REVIEW/'evidence/tex-resources-before-acquisition.json').exists()
    cache=ROOT/'.checkpoint-tools/tex-cache/Tectonic';before=manifest(cache)
    work,_=run('r01-tex-acquisition-02',
       [ROOT/'.checkpoint-tools/bin/tectonic','--untrusted','--keep-logs','--keep-intermediates',
        '--outdir','/var/tmp',fixture],wall=180,cpu=120,memory=2048,rss=1024,
       sources=[fixture,Path(__file__)],latex_cache=True)
    acquired=work/'cache/Tectonic';after=manifest(acquired)
    # The engine is unchanged. Record every new/changed cached resource byte.
    record={'authorization':'User-approved required TeX resources only',
       'engine_sha256':sha(ROOT/'.checkpoint-tools/bin/tectonic'),
       'bundle':'https://relay.fullyjustified.net/default_bundle_v33.tar',
       'source':'separate synthetic acquisition fixture; all research builds remain --only-cached',
       'new_or_changed_files':{n:h for n,h in after.items() if before.get(n)!=h},
       'resource_names':[line.split()[0] for p in (acquired/'manifests').glob('*') for line in p.read_text().splitlines() if line.split()[0] in ['article.cls','size11.clo','booktabs.sty']],
       'global_environment_modified':False,'numerical_dependencies_acquired':False}
    (REVIEW/'evidence/tex-acquisition-02.json').write_text(json.dumps(record,indent=2)+'\n')
    for name,h in record['new_or_changed_files'].items():
        dest=cache/name
        if dest.exists() and sha(dest)==h:continue
        dest.parent.mkdir(parents=True,exist_ok=True)
        tmp=dest.with_name(dest.name+'.promotion')
        shutil.copyfile(acquired/name,tmp);tmp.replace(dest)
        assert sha(dest)==h
    print('Required TeX cache prepared; new/changed cache entries:',len(record['new_or_changed_files']))
if __name__=='__main__':main()
