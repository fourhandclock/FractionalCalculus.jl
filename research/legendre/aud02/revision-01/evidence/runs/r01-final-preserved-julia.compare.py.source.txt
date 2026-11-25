"""Compare matched scientific rows; timing/memory fields are not acceptance targets."""
import csv,json,sys
from pathlib import Path

ATOL=5e-11
RTOL=2e-6
FIELDS=('l2_max','h1_max','h1_final')


def read(path):
    with Path(path).open() as f: return list(csv.DictReader(f))


def key(r):
    return (float(r['alpha']),float(r['beta']),r['case'],r['variant'],
            round(float(r['grading']),12),int(r['N']),int(r['M']))


def compare(reference,candidate):
    a,b={key(r):r for r in read(reference)},{key(r):r for r in read(candidate)}
    assert len(a)==len(b)==156 and a.keys()==b.keys(), 'scientific case identities differ'
    failures=[]; maxima={field:0. for field in FIELDS}
    for k,r in a.items():
        s=b[k]
        for field in FIELDS:
            x,y=float(r[field]),float(s[field]); difference=abs(x-y)
            maxima[field]=max(maxima[field],difference)
            if not difference<=ATOL+RTOL*abs(x):
                failures.append(dict(case=k,field=field,reference=x,candidate=y,difference=difference))
        assert float(s['scaled_residual'])<1e-9
    return dict(passed=not failures,rows=156,atol=ATOL,rtol=RTOL,
                maximum_absolute_differences=maxima,failures=failures,
                scope='Continuous norms only; no matching of timings, array layout or roundoff bit patterns.')

if __name__=='__main__':
    result=compare(sys.argv[1],sys.argv[2]);print(json.dumps(result,indent=2));raise SystemExit(0 if result['passed'] else 1)
