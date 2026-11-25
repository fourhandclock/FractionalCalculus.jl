"""Independent Python comparison; not execution of the Julia library.
Run with OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python benchmark_gr07.py.
Normalized I^(1-beta) weights throughout; multiply by Gamma(1-beta) once.
"""
import csv, math, time, sys
from pathlib import Path
import numpy as np
from scipy.special import gamma, roots_jacobi, eval_legendre
from numpy.polynomial.legendre import leggauss, legvander, legval, legder
from verify_gr06_graded import matrices, moment

VARIANTS=['L1-printed','L12-printed','L12-PI-L','Alikhanov-PI-L','Alikhanov-PI-Q']

def endpoint(t,a,b,l12,printed):
    N=len(t)-1; r=1-b; dt=np.diff(t); D=np.zeros((N,N)); W=np.zeros((N,N+1))
    for n in range(1,N+1):
        h=dt[:n]; d=(t[n]-t[:n])/h; d[-1]=1.; z=np.ones(n)
        m0=moment(d,z,h,1-a,0); m1=moment(d,z,h,1-a,1)
        D[n-1,:n]=m0/h
        if l12 and n>1:
            # derivative of backward quadratic on each panel after the first
            correction=(2*m1[1:]-m0[1:])/(h[:-1]+h[1:])
            D[n-1,1:n]+=correction/h[1:]
            D[n-1,:n-1]-=correction/h[:-1]
        if printed:
            if n>1:
                W[n-1,:n-1]+=h[:-1]*(t[n]-t[:n-1])**(-b)/(2*gamma(r))
                W[n-1,1:n]+=h[:-1]*(t[n]-t[1:n])**(-b)/(2*gamma(r))
            W[n-1,n-1:n+1]+=h[-1]**r/(2*gamma(1+r))
        else:
            m0=moment(d,z,h,r,0); m1=moment(d,z,h,r,1)
            W[n-1,:n]+=m0-m1; W[n-1,1:n+1]+=m1
    return D,W,t[1:]

def spatial(M):
    x=np.r_[-1.,roots_jacobi(M-1,1,1)[0],1.]; P=eval_legendre(M,x); w=2/(M*(M+1)*P**2)
    dx=x[:,None]-x[None,:]; np.fill_diagonal(dx,1.)
    D=(P[:,None]/P[None,:])/dx; np.fill_diagonal(D,0.); np.fill_diagonal(D,-D.sum(axis=1))
    assert np.max(abs(D@x-1))<1e-10
    S=D[:,1:-1].T@(w[:,None]*D[:,1:-1]); mass=w[1:-1]; L=S/mass[:,None]
    z,wz=leggauss(max(80,2*M+10)); B=legvander(z,M)@np.linalg.inv(legvander(x,M)); dB=np.column_stack([legval(z,legder(c)) for c in np.linalg.inv(legvander(x,M)).T]); phi=np.cos(np.pi*z/2); phix=-np.pi/2*np.sin(np.pi*z/2)
    # derivative Ritz initial condition: integrate phi' times cardinal derivative
    ritz=np.linalg.solve(S,dB[:,1:-1].T@(wz*phix))
    return x[1:-1],L,B[:,1:-1],dB[:,1:-1],wz,phi,phix,ritz

def trial(a,b,N,M,kind,variant,grading):
    t=(np.arange(N+1)/N)**grading; r=1-b; lam=.4; lg=lam*gamma(r); p=2 if kind=='smooth' else a; base=0 if kind=='smooth' else 1; sig=1-a/2 if variant.startswith('Alikhanov') else 1.; theta=1-sig
    start=time.perf_counter()
    if variant.startswith('Alikhanov'): D,W,ts=matrices(t,a,b,variant.endswith('Q'))
    else: D,W,ts=endpoint(t,a,b,variant.startswith('L12'),variant.endswith('printed'))
    assemble=time.perf_counter()-start
    # Constant and linear checks on derivative; exact mass for all PI rules
    assert np.max(abs(D@np.diff(t)-ts**(1-a)/gamma(2-a)))<2e-9
    if not variant.endswith('printed'):
        assert np.max(abs(W.sum(axis=1)-ts**r/gamma(1+r)))<2e-11
        assert np.max(abs(W@t-ts**(1+r)/gamma(2+r)))<2e-11
    x,L,B,dB,wz,phi,phix,ritz=spatial(M); exact=base+t**p; amp=base+ts**p
    K=(1+.3*x[None,:])*(1+.2*np.sin(ts[:,None])); phi_nodes=np.cos(np.pi*x/2)
    forcing=(gamma(1+p)/gamma(1+p-a)*ts**(p-a)+np.pi**2/4*amp)[:,None]*phi_nodes+lg*K*(base*ts**r/gamma(1+r)+gamma(1+p)/gamma(1+p+r)*ts**(p+r))[:,None]*phi_nodes
    U=np.zeros((N+1,M-1)); U[0]=base*ritz; eye=np.eye(M-1)
    start=time.perf_counter()
    for n in range(N):
        rhs=forcing[n]+D[n,n]*U[n]-D[n,:n]@np.diff(U[:n+1],axis=0)-theta*(L@U[n])-lg*K[n]*(W[n,:n+1]@U[:n+1])
        U[n+1]=np.linalg.solve(D[n,n]*eye+sig*L+lg*W[n,n+1]*np.diag(K[n]),rhs)
    solve=time.perf_counter()-start
    V=sig*U[1:]+theta*U[:-1]; du=np.diff(U,axis=0); R=D@du+V@L.T+lg*K*(W@U)-forcing
    scale=1+abs(D)@abs(du)+abs(V)@abs(L.T)+lg*abs(K)*(abs(W)@abs(U))+abs(forcing)
    residual=np.max(abs(R)/scale); assert residual<1e-9
    e=B@U.T-phi[:,None]*exact; ex=dB@U.T-phix[:,None]*exact
    l2=np.sqrt(wz@(e**2)); h1=np.sqrt(wz@(e**2+ex**2))
    return dict(alpha=a,beta=b,case=kind,variant=variant,grading=grading,N=N,M=M,l2_max=float(max(l2)),h1_max=float(max(h1)),h1_final=float(h1[-1]),scaled_residual=float(residual),assembly_s=assemble,solve_s=solve,time_weight_bytes=D.nbytes+W.nbytes,history_bytes=U.nbytes)

if __name__=='__main__':
    out=Path(sys.argv[1] if len(sys.argv)>1 else 'results.csv'); assert not out.exists(), 'refusing to overwrite results'
    rows=[]
    for a,b in [(.5,.25),(.75,.5),(.9,.8)]:
        for kind in ['smooth','singular']:
            for variant in VARIANTS:
                for grading in ([1.,2/a] if kind=='singular' and variant.startswith('Alikhanov') else [1.]):
                    previous=None
                    for N in [32,64,128,256]:
                        row=trial(a,b,N,14,kind,variant,grading); row['h1_rate']=math.log2(previous/row['h1_max']) if previous else ''; previous=row['h1_max']; rows.append(row)
                    print(a,b,kind,variant,grading,f"H1={row['h1_max']:.6e} rate={row['h1_rate']:.5f}",flush=True)
    # Independent spatial refinement, graded singular case
    for variant in VARIANTS[-2:]:
        for M in [3,5,7,9,12,16]:
            row=trial(.75,.5,256,M,'singular',variant,2/.75); row['h1_rate']=''; rows.append(row)
    with out.open('x',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=rows[0].keys()); writer.writeheader(); writer.writerows(rows)
    print(f'PASS: {len(rows)} configurations; max scaled residual {max(r["scaled_residual"] for r in rows):.3e}; no rate assertions; single-shot Python timings only.')
