"""Finite-grid checks for GR-02; not a proof of uniform inequalities."""
import numpy as np
import mpmath as mp
from scipy.linalg import solve_triangular
from numpy.polynomial.legendre import leggauss
from math import gamma
mp.mp.dps = 50

def matrix(alpha,N):
    a=mp.mpf(str(alpha)); sig=1-a/2; h=1/N
    aa=np.array([float(sig**(1-a))]+[float((l+sig)**(1-a)-(l-1+sig)**(1-a)) for l in range(1,N)])
    bb=np.array([0.]+[float(((l+sig)**(2-a)-(l-1+sig)**(2-a))/(2-a)-((l+sig)**(1-a)+(l-1+sig)**(1-a))/2) for l in range(1,N)])
    A=np.zeros((N,N)); A[0,0]=aa[0]
    for n in range(2,N+1):
        row=aa[:n].copy(); row[0]+=bb[1]; row[1:-1]+=bb[2:n]-bb[1:n-1]; row[-1]-=bb[n-1]; A[n-1,:n]=row[::-1]
    return A/(gamma(2-alpha)*h**alpha)

rng=np.random.default_rng(421)
max_id=max_integral=max_quad=max_tail=0.; min_energy=1e100; cases=0
nodes,weights=leggauss(32); x=(nodes+1)/2; w=weights/2
for a in [.05,.25,.5,.75,.95,.99]:
    sig=1-a/2
    for N in [16,64,128]:
        tau=1/N; A=matrix(a,N); P=np.tril(np.ones_like(A))@solve_triangular(A,np.eye(N),lower=True)
        # Independent direct integration on completed panels. Final panel integrated exactly.
        Q=np.zeros_like(A)
        for n in range(1,N+1):
            Q[n-1,n-1]=sig**(1-a)*tau**(-a)/gamma(2-a)
            for k in range(1,n):
                l=n-k; kernel=(l+sig-x)**(-a)*tau**(-a)/gamma(1-a)
                Q[n-1,k-1]+=np.sum(w*kernel*(1.5-x)); Q[n-1,k]+=np.sum(w*kernel*(x-.5))
        discrepancy=np.max(np.abs(Q-A))/np.max(A); max_integral=max(max_integral,discrepancy); assert discrepancy<2e-13
        assert np.all(A[np.tril_indices(N)]>0)
        assert all(np.all(np.diff(A[n,:n+1])>0) for n in range(1,N))
        assert np.all((2*sig-1)*A.diagonal()[1:]>sig*np.diag(A,k=-1))
        assert np.min(P)>-2e-14
        d=1/(2*gamma(1-a))
        for n in range(1,N+1):
            for k in range(1,n+1):
                assert A[n-1,k-1]>=d*((n-k+1)*tau)**(-a)
                ratio=P[n-1,k-1:n].sum()/(d**(-1)*((n-k+1)*tau)**a); max_tail=max(max_tail,ratio); assert ratio<=1+1e-12
        err=np.max(np.abs(P@A-np.tril(np.ones_like(A)))); max_id=max(max_id,err); assert err<2e-12
        t=np.arange(N+1)*tau; ts=t[1:]-(1-sig)*tau
        for degree in [1,2]:
            exact=gamma(degree+1)/gamma(degree+1-a)*ts**(degree-a)
            err=np.max(np.abs(A@np.diff(t**degree)-exact)); max_quad=max(max_quad,err); assert err<2e-12
        for _ in range(10):
            v=rng.normal(size=(N+1,4)); dv=A@np.diff(v,axis=0); vs=sig*v[1:]+(1-sig)*v[:-1]
            energy=2*np.sum(dv*vs,axis=1)-A@np.diff(np.sum(v*v,axis=1)); min_energy=min(min_energy,np.min(energy)); assert np.min(energy)>-1e-11
        cases+=1
print(f'{cases} configurations; 180 random vector trajectories')
print(f'max scaled direct-integration/weight discrepancy: {max_integral:.3e}')
print(f'max complementary identity discrepancy: {max_id:.3e}')
print(f'max linear/quadratic derivative error: {max_quad:.3e}')
print(f'max complementary tail ratio: {max_tail:.6f}')
print(f'min sampled energy gap: {min_energy:.6e}')
print('Cubic derivative convergence (max error over shifted levels):')
for a in [.25,.5,.75]:
    errors=[]
    for N in [32,64,128,256]:
        A=matrix(a,N); t=np.arange(N+1)/N; ts=t[1:]-a/(2*N)
        exact=6/gamma(4-a)*ts**(3-a); errors.append(np.max(np.abs(A@np.diff(t**3)-exact)))
    rate=np.log2(errors[-2]/errors[-1]); assert abs(rate-(3-a))<.08
    print(f'alpha={a:.2f}: errors='+', '.join(f'{e:.6e}' for e in errors)+f'; last rate={rate:.6f}; target={3-a:.2f}')
print('All assertions passed.')
