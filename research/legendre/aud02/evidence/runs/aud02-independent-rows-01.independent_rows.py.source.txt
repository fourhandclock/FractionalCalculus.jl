"""Generic Lagrange plus transformed quadrature; no beta functions or assembly formulas."""
import csv,json,sys
from pathlib import Path
import mpmath as mp
mp.mp.dps=80

def basis(nodes,j,x):
    ans=mp.mpf(1)
    for k,node in enumerate(nodes):
        if k!=j:ans*=(x-node)/(nodes[j]-node)
    return ans

def derivative(nodes,j,x):
    ans=mp.mpf(0)
    for k,node in enumerate(nodes):
        if k==j:continue
        term=1/(nodes[j]-node)
        for ell,other in enumerate(nodes):
            if ell not in (j,k):term*=(x-other)/(nodes[j]-other)
        ans+=term
    return ans

def integral(fun,left,right,star,r):
    # Substitute y=(star-s)^r: removes endpoint singularity exactly.
    lo=(star-right)**r;hi=(star-left)**r
    return mp.quad(lambda y:fun(star-y**(1/r)),[lo,(lo+hi)/2,hi])/mp.gamma(1+r)

def main():
    rows=list(csv.DictReader(open(sys.argv[1])));worst=mp.mpf(0);count=0
    for case in sorted({r['case'] for r in rows}):
      subset=[r for r in rows if r['case']==case];a=mp.mpf(subset[0]['alpha']);b=mp.mpf(subset[0]['beta'])
      if case=='irregular':t=list(map(mp.mpf,['0','.013','.041','.122','.379','1']))
      else:
        N=5 if case=='graded' else 2;g=mp.mpf(float(2/float(a))) if case=='graded' else mp.mpf(7)
        # Match the actual Float64 input nodes; quadrature itself remains high precision.
        t=[mp.mpf(float((k/N)**float(g))) for k in range(N+1)]
      for variant in sorted({r['variant'] for r in subset}):
        for n in range(1,len(t)):
          sig=1-a/2;star=t[n-1]+sig*(t[n]-t[n-1]);A=[mp.mpf(0)]*n;W=[mp.mpf(0)]*(n+1)
          for panel in range(1,n+1):
            di=list(range(panel-1,panel+2)) if panel<n else [panel-1,panel]
            dn=[t[k] for k in di];right=t[panel] if panel<n else star
            for ell in range(1,n+1):
                f=lambda s:sum(derivative(dn,j,s) for j,k in enumerate(di) if k>=ell)
                A[ell-1]+=integral(f,t[panel-1],right,star,1-a)
            mi=[panel-1,panel] if variant.endswith('_L') or n==1 else (list(range(panel-1,panel+2)) if panel<n else [n-2,n-1,n])
            mn=[t[k] for k in mi]
            for j,k in enumerate(mi):W[k]+=integral(lambda s:basis(mn,j,s),t[panel-1],right,star,1-b)
          record=[r for r in subset if r['variant']==variant and int(r['n'])==n]
          for rec in record:
            k=int(rec['k']);pairs=[(mp.mpf(rec['W']),W[k])]
            if k:pairs.append((mp.mpf(rec['A']),A[k-1]))
            for got,want in pairs:
                err=abs(got-want)/(1+abs(want));worst=max(worst,err);assert err<mp.mpf('8e-11'),(case,variant,n,k,got,want);count+=1
          for degree in (0,1,2):
            computed=sum(A[k-1]*(t[k]**degree-t[k-1]**degree) for k in range(1,n+1))
            exact=0 if degree==0 else mp.gamma(1+degree)/mp.gamma(1+degree-a)*star**(degree-a)
            assert abs(computed-exact)<mp.mpf('1e-60')*(1+abs(exact))
    extremes=[]
    for row in csv.DictReader(open(sys.argv[2])):
        h,r,d,H=[mp.mpf(float(row[k])) for k in ('h','r','d','H')]
        # All probes are final panels: exact complete-beta identity, distinct from numerical quadrature above.
        exact=(h*H)**r/mp.gamma(1+r);got=mp.mpf(row['m0']);rel=abs(got-exact)/abs(exact)
        extremes.append({'case':row['case'],'m0':row['m0'],'exact_m0':mp.nstr(exact,25),'relative_error':float(rel),'meets_5e-12_relative':bool(rel<mp.mpf('5e-12'))})
    result={'oracle':'80-digit generic Lagrange and endpoint-transformed mpmath quadrature',
       'coefficient_comparisons':count,'maximum_scaled_weight_error':float(worst),
       'boundary_probes':extremes,'scope':'boundary discrepancies are recorded, not waived or repaired'}
    Path('/var/tmp/independent_rows.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
