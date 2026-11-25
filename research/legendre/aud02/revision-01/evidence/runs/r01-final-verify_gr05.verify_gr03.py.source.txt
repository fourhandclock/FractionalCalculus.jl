"""GR-03 finite-grid diagnostics. No claim of a proof or PDE convergence.
Normalized I^r weights; direct quadrature checks use a separate basis evaluation.
"""
import numpy as np
from math import gamma
from scipy.special import betainc
from scipy.integrate import quad
from scipy.linalg import solve_triangular
from functools import lru_cache
import mpmath as mp

@lru_cache(None)
def moments(r,d,h):
    # Integral x^j (d-x)^(r-1) / Gamma(r), j=0,1,2.
    return np.array([d**(r+j)*gamma(j+1)/gamma(j+1+r)*betainc(j+1,r,h/d) for j in range(3)])

# Polynomial coefficient rows, increasing power.
L=np.array([[1,-1,0],[0,1,0]])
F=np.array([[1,-1.5,.5],[0,2,-1],[0,-.5,.5]])
B=np.array([[0,-.5,.5],[1,0,-1],[0,.5,.5]])

def panels(n,sigma,quadratic):
    for k in range(1,n+1):
        d=n-k+sigma; h=1. if k<n else sigma
        if not quadratic or n==1:
            yield d,h,np.arange(k-1,k+1),L
        elif k<n:
            yield d,h,np.arange(k-1,k+2),F
        else:
            yield d,h,np.arange(k-2,k+1),B

def matrix(alpha,beta,N,quadratic):
    r=1-beta; sigma=1-alpha/2; tau=1/N
    W=np.zeros((N,N+1))
    for n in range(1,N+1):
        for d,h,idx,coef in panels(n,sigma,quadratic):
            W[n-1,idx]+=tau**r*(coef@moments(r,d,h))
    return W

def direct(alpha,beta,N,quadratic):
    r=1-beta; sigma=1-alpha/2; tau=1/N
    W=np.zeros((N,N+1))
    # Independent Lagrange basis, with adaptive integration. Final panel uses
    # QUADPACK's algebraic endpoint weight, not the incomplete beta formula.
    for n in range(1,N+1):
        for k in range(1,n+1):
            d=n-k+sigma; h=1. if k<n else sigma
            nodes=[0,1] if not quadratic or n==1 else ([0,1,2] if k<n else [-1,0,1])
            for v in nodes:
                def basis(x):
                    z=1.
                    for w in nodes:
                        if w!=v: z*=(x-w)/(v-w)
                    return z
                if k==n:
                    integ=quad(basis,0,h,weight='alg',wvar=(0,r-1),epsabs=1e-12,epsrel=1e-12)[0]
                else:
                    integ=quad(lambda x:basis(x)*(d-x)**(r-1),0,h,epsabs=1e-12,epsrel=1e-12)[0]
                W[n-1,k-1+v]+=tau**r/gamma(r)*integ
    return W

def complement(alpha,N):
    with mp.workdps(50):
        a=mp.mpf(str(alpha)); s=1-a/2
        aa=np.array([float(s**(1-a))]+[float((l+s)**(1-a)-(l-1+s)**(1-a)) for l in range(1,N)])
        bb=np.array([0.]+[float(((l+s)**(2-a)-(l-1+s)**(2-a))/(2-a)-((l+s)**(1-a)+(l-1+s)**(1-a))/2) for l in range(1,N)])
    A=np.zeros((N,N)); A[0,0]=aa[0]
    for n in range(2,N+1):
        row=aa[:n].copy(); row[0]+=bb[1]; row[1:-1]+=bb[2:n]-bb[1:n-1]; row[-1]-=bb[n-1]; A[n-1,:n]=row[::-1]
    A*=N**alpha/gamma(2-alpha)
    P=np.tril(np.ones_like(A))@solve_triangular(A,np.eye(N),lower=True)
    assert np.min(P)>-1e-13
    assert np.max(np.abs(P@A-np.tril(np.ones_like(A))))<2e-12
    return P

def exact(r,t,k): return gamma(k+1)/gamma(k+1+r)*t**(k+r)

if __name__=='__main__':
    pairs=[(.25,.1),(.5,.25),(.75,.5),(.75,.75),(.95,.9),(.99,.98)]
    maxdirect=maxmass=maxpoly=maxtail=maxcomp=0.; minq=0.; cases=0; witness=None
    for a,b in pairs:
        r=1-b; s=1-a/2; d=1/(2*gamma(1-a))
        for N in [8,16,32]:
            t=np.arange(N+1)/N; ts=t[1:]-(1-s)/N; P=complement(a,N)
            for q in [False,True]:
                W=matrix(a,b,N,q); D=direct(a,b,N,q)
                err=np.max(np.abs(W-D)); maxdirect=max(maxdirect,err); assert err<3e-12
                err=np.max(np.abs(W.sum(axis=1)-exact(r,ts,0))); maxmass=max(maxmass,err); assert err<3e-12
                if not q: assert np.min(W)>-1e-14
                else:
                    loc=np.unravel_index(np.argmin(W),W.shape)
                    if W[loc]<minq: minq=W[loc]; witness=(a,b,N,loc[0]+1,loc[1],W[loc])
                for k in [0,1,2] if q else [0,1]:
                    sl=slice(1,None) if k==2 else slice(None)
                    err=np.max(np.abs((W@t**k-exact(r,ts,k))[sl])); maxpoly=max(maxpoly,err); assert err<3e-12
                if q:
                    # Exact first-step t^2 defect for the linear startup.
                    expected=N**(-r-2)*(moments(r,s,s)[1]-moments(r,s,s)[2])
                    assert abs((W@t**2-exact(r,ts,2))[0]-expected)<3e-14
                H=np.abs(W); C=1.25 if q else 1.; z=2**r if q else 1.
                assert np.all(H.sum(axis=1)<=C*exact(r,ts,0)+2e-13)
                PH=P@H[:,1:]
                for n in range(1,N+1):
                    for m in range(1,n+1):
                        ell=(n-m+1)/N
                        R=H[n-1,m:n+1].sum()/(C*z*ell**r/gamma(1+r))
                        S=PH[n-1,m-1:n].sum()/(C*z*ell**(a+r)/(d*gamma(1+r)))
                        maxtail=max(maxtail,R); maxcomp=max(maxcomp,S)
                        assert R<=1+2e-12 and S<=1+2e-12
                cases+=1
    assert witness is not None and minq<0
    print(f'{cases} scheme/order/grid configurations; direct adaptive quadrature check')
    print(f'max absolute direct/assembled discrepancy: {maxdirect:.3e}')
    print(f'max constant mass discrepancy: {maxmass:.3e}')
    print(f'max exact polynomial discrepancy (excluding quadratic startup): {maxpoly:.3e}')
    print(f'max absolute W tail bound ratio: {maxtail:.8f}')
    print(f'max P|W| tail bound ratio: {maxcomp:.8f}')
    print('negative assembled PI-Q weight witness (alpha,beta,N,n,k,value):',witness)
    print('Convergence on [0,1]: linear t^2, quadratic t^2 startup, quadratic t^3 post-startup')
    for a,b in [(.5,.25),(.75,.5),(.95,.9)]:
        r=1-b; errors=[]
        for N in [32,64,128,256]:
            t=np.arange(N+1)/N; ts=t[1:]-a/(2*N)
            WL=matrix(a,b,N,False); WQ=matrix(a,b,N,True)
            errors.append([np.max(np.abs(WL@t**2-exact(r,ts,2))),abs((WQ@t**2-exact(r,ts,2))[0]),np.max(np.abs((WQ@t**3-exact(r,ts,3))[1:]))])
        rates=np.log2(np.array(errors[-2])/errors[-1]); assert abs(rates[0]-2)<.06 and abs(rates[1]-(2+r))<.01 and abs(rates[2]-3)<.16
        print(f'alpha={a:.2f} beta={b:.2f}: rates {rates[0]:.6f}, {rates[1]:.6f}, {rates[2]:.6f}; targets 2, {2+r:.2f}, 3')
    print('All assertions passed.')
