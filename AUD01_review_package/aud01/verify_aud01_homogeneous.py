#!/usr/bin/env python3
"""AUD-01 independent constant-kernel homogeneous scalar diagnostics.
Not interval arithmetic. Reference: commuting fractional-integral Neumann series.
No imports from earlier research scripts. NumPy/SciPy/mpmath only.
"""
import math
import numpy as np
import mpmath as mp
from scipy.special import gamma

ALPHA=.75; BETA=.5; T=2**-10; SIGMA=math.pi**2/4

def reference(t, terms):
    a=np.ones_like(t); d=np.zeros_like(t); j=2*np.sqrt(t)
    # At t=0 the Caputo derivative is not assigned its right-hand limit here.
    for n in range(1,terms+1):
        for k in range(n+1):
            nu=n*ALPHA+k*(1-BETA)
            coeff=(-1)**n*math.comb(n,k)*SIGMA**(n-k)*gamma(1-BETA)**k
            a+=coeff*t**nu/gamma(1+nu)
            d[1:]+=coeff*t[1:]**(nu-ALPHA)/gamma(1+nu-ALPHA)
            j+=coeff*gamma(1-BETA)*t**(nu+1-BETA)/gamma(2+nu-BETA)
    return a,d,j

def weights(n):
    with mp.workdps(45):
        alpha=mp.mpf(3)/4
        p=[mp.mpf(r)**(1-alpha) for r in range(n+1)]
        q=[mp.mpf(r)**(2-alpha) for r in range(n+1)]
        b=np.array([float(p[r+1]-p[r]) for r in range(n)])
        c=np.array([float((q[r+1]-q[r])/(2-alpha)-(p[r+1]+p[r])/2) for r in range(n)])
    return b,c

def run(N):
    tau=T/N; a0=gamma(2-ALPHA)*tau**ALPHA; t=np.linspace(0,T,N+1)
    a,D,J=reference(t,24); aa,DD,JJ=reference(t,32)
    oracle=max(np.max(abs(a-aa)),np.max(abs(D-DD)),np.max(abs(J-JJ)),np.max(abs(D[1:]+SIGMA*a[1:]+J[1:])))
    assert oracle<2e-12 and np.min(a)>2/3
    b,c=weights(N); old=tau**(1-BETA)*np.arange(1,N+1,dtype=float)**(-BETA)/2
    last=tau**(1-BETA)/(2*(1-BETA)); W=2*T**(1-BETA)/(1-BETA)
    out=[]
    for mode in ['L1','L12']:
        u=np.zeros(N+1); u[0]=1; e=np.zeros(N+1); res=np.zeros(N+1); rd=np.zeros(N+1); rj=np.zeros(N+1); max_row=0.
        for n in range(1,N+1):
            coeff=b[:n].copy()
            if mode=='L12' and n>1: coeff[:-1]+=c[:n-1]; coeff[1:]-=c[:n-1]
            row=np.r_[-coeff[-1],(coeff[1:]-coeff[:-1])[::-1],coeff[0]]/a0
            w=np.zeros(n+1)
            if n>1: w[:n-1]+=old[n-1:0:-1]; w[1:n]+=old[n-2::-1]
            w[-2:]+=last
            du=np.diff(a[:n+1]); raw=np.dot(b[:n],du[::-1]);
            if mode=='L12': raw+=np.dot(c[:n-1],np.diff(du)[::-1])
            rd[n]=raw/a0-D[n]; rj[n]=np.dot(w,a[:n+1])-J[n]; res[n]=rd[n]+rj[n]
            row+=w; row[-1]+=SIGMA
            u[n]=-np.dot(row[:-1],u[:n])/row[-1]
            e[n]=(-res[n]-np.dot(row[:-1],e[:n]))/row[-1]
            # Check the actual original two-sum derivative and old-panel trapezoids.
            du=np.diff(u[:n+1]); deriv=np.dot(b[:n],du[::-1]);
            if mode=='L12': deriv+=np.dot(c[:n-1],np.diff(du)[::-1])
            mem=last*(u[n-1]+u[n]);
            if n>1: mem+=np.dot(old[n-1:0:-1],u[:n-1])+np.dot(old[n-2::-1],u[1:n])
            max_row=max(max_row,abs(deriv+a0*(SIGMA*u[n]+mem)))
        E=np.max(abs(u-a)); defect=np.max(abs(u-a-e)); integrated=tau*np.sum(res[1:]); lower=abs(integrated)/((1 if mode=='L1' else 3)*T**(1-ALPHA)/gamma(2-ALPHA)+T*(SIGMA+W))
        assert defect<2e-11 and max_row<2e-12 and E+2e-11>=lower
        out.append((mode,E,integrated/tau**(1-BETA),tau*np.sum(rj[1:])/tau**(1-BETA),tau*np.sum(abs(rd[1:]))/tau,lower,defect,max_row))
    return out, oracle

def main():
    print('AUD-01 homogeneous test: alpha=3/4 beta=1/2 T=2^-10 K=lambda=1 sigma=pi^2/4')
    print('Reference: 24 vs 32 term fractional Neumann expansion (not interval arithmetic).')
    print('N scheme max_error rate normalized_signed_residual normalized_memory_residual sum_abs_Caputo_residual_over_tau lower_bound direct_vs_error max_scaled_row')
    prev={}; oracle=0
    for N in (128,256,512,1024,2048,4096):
        results,o=run(N); oracle=max(oracle,o)
        for mode,E,res,mem,cap,lower,defect,row in results:
            rate=math.log2(prev[mode]/E) if mode in prev else float('nan'); prev[mode]=E
            print(f'{N:4d} {mode:3s} {E:.10e} {rate:7.4f} {res:.10e} {mem:.10e} {cap:.8e} {lower:.10e} {defect:.3e} {row:.3e}')
    print(f'Maximum continuous reference check: {oracle:.3e}')
    print('All finite checks passed. No requirement that finite-grid rates have reached 1-beta.')
if __name__=='__main__': main()
