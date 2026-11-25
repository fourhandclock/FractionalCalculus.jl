"""GR-05 smooth temporal/full spatial diagnostics. Requires verify_gr03.py.
No singular-startup convergence, proof certification or production modifications.
"""
import math
import numpy as np
from scipy.linalg import solve_triangular
from scipy.special import roots_jacobi, eval_legendre
from numpy.polynomial.legendre import leggauss
from verify_gr03 import matrix as memory_matrix

def derivative(a,N):
    sig=1-a/2; x,w=leggauss(48); x=(x+1)/2; w=w/2
    D=np.zeros((N,N)); D[np.diag_indices(N)]=sig**(1-a)*N**a/math.gamma(2-a)
    for lag in range(1,N):
        kernel=(lag+sig-x)**(-a)*N**a/math.gamma(1-a)
        k=np.arange(N-lag)
        D[k+lag,k]+=np.sum(w*kernel*(1.5-x))
        D[k+lag,k+1]+=np.sum(w*kernel*(x-.5))
    return D

def solve(D,W,sig,L,K,F,U0,lamgamma):
    N=len(D); m=len(U0); I=np.eye(m); theta=1-sig
    U=np.zeros((N+1,m)); U[0]=U0
    for n in range(N):
        M=D[n,n]*I+sig*L+lamgamma*W[n,n+1]*K[n]
        rhs=F[n]+D[n,n]*U[n]-D[n,:n]@np.diff(U[:n+1],axis=0)-theta*L@U[n]-lamgamma*K[n]@(W[n,:n+1]@U[:n+1])
        U[n+1]=np.linalg.solve(M,rhs)
    V=sig*U[1:]+theta*U[:-1]
    R=D@np.diff(U,axis=0)+V@L.T+lamgamma*np.einsum('nij,nj->ni',K,W@U)-F
    res=np.max(np.abs(R))/(1+np.max(np.abs(F)))
    assert res<5e-10, res
    return U,res

def exact_frac(t,order,k):
    return math.gamma(k+1)/math.gamma(k+1+order)*t**(k+order)

def cap(t,a,k): return math.gamma(k+1)/math.gamma(k+1-a)*t**(k-a)

print('Scalar smooth sharpness: u=t^2, diffusion eigenvalue pi^2/4, positive memory lambda=.1, K=1')
maxres=0.; cases=0
for a,b in [(.25,.1),(.75,.5),(.95,.9)]:
    sig=1-a/2; theta=1-sig; r=1-b; L=np.array([[math.pi**2/4]]); lamgamma=.1*math.gamma(r)
    errs=[[],[]]
    for N in [32,64,128,256]:
        t=np.linspace(0,1,N+1); ts=t[1:]-theta/N; D=derivative(a,N)
        P=np.tril(np.ones((N,N)))@solve_triangular(D,np.eye(N),lower=True)
        assert np.min(P)>-1e-12
        assert P[-1].sum()>=math.gamma(2-a)-1e-12
        F=(cap(ts,a,2)+L[0,0]*ts**2+lamgamma*exact_frac(ts,r,2))[:,None]
        for q in [False,True]:
            W=memory_matrix(a,b,N,q); U,res=solve(D,W,sig,L,np.ones((N,1,1)),F,np.zeros(1),lamgamma)
            err=np.max(np.abs(U[:,0]-t**2)); errs[q].append(err); maxres=max(res,maxres); cases+=1
            # Exact discrete residual of sampled u, derived independently.
            R=D@np.diff(t**2)+L[0,0]*(sig*t[1:]**2+theta*t[:-1]**2)+lamgamma*W@t**2-F[:,0]
            expected=L[0,0]*sig*theta/N**2+lamgamma*(W@t**2-exact_frac(ts,r,2))
            assert np.max(np.abs(R-expected))<1e-11
            assert np.min(R)>=L[0,0]*sig*theta/N**2-1e-11
            lower=math.gamma(2-a)*L[0,0]*sig*theta/N**2/(1+(L[0,0]+lamgamma*(1.25 if q else 1)/math.gamma(1+r))*P[-1].sum())
            assert err>=lower-1e-12
    for q in [False,True]:
        rates=np.log2(np.array(errs[q][:-1])/errs[q][1:]); assert 1.85<rates[-1]<2.15
        print(f'alpha={a:.2f} beta={b:.2f} {"PI-Q" if q else "PI-L"}: errors '+', '.join(f'{e:.8e}' for e in errs[q])+f'; last rate {rates[-1]:.6f}')

def gll(M):
    x=np.r_[-1.,roots_jacobi(M-1,1,1)[0],1.]; L=eval_legendre(M,x); w=2/(M*(M+1)*L**2)
    # Cardinal differentiation matrix via barycentric ratios.
    dx=x[:,None]-x[None,:]; np.fill_diagonal(dx,1.)
    D=(L[:,None]/L[None,:])/dx; np.fill_diagonal(D,0.); np.fill_diagonal(D,-D.sum(axis=1))
    assert np.max(np.abs(D@x-1))<1e-11
    S=D[:,1:-1].T@(w[:,None]*D[:,1:-1]); mass=w[1:-1]
    return x,w,D,S/mass[:,None]

# Nonconstant spatial/time K: test actual GLL mass and stiffness; smooth eigenmode.
# Ritz initial state is zero (a(0)=0); exact forcing includes variable K.
a=.75; b=.5; r=1-b; sig=1-a/2; theta=1-sig; lamgamma=.4*math.gamma(r)
print('GLL spectral diffusion, u=t^2 cos(pi*x/2), K=(1+.3*x)*(1+.2*sin(t)), lambda=.4')
def spectral(M,N,q):
    global maxres,cases
    x,w,Dx,L=gll(M); xx=x[1:-1]; phi=np.cos(np.pi*xx/2); t=np.linspace(0,1,N+1); ts=t[1:]-theta/N
    Kvals=(1+.2*np.sin(ts[:,None]))*(1+.3*xx[None,:]); K=np.array([np.diag(row) for row in Kvals]);
    F=(cap(ts,a,2)+np.pi**2/4*ts**2)[:,None]*phi + lamgamma*Kvals*exact_frac(ts,r,2)[:,None]*phi
    D=derivative(a,N); W=memory_matrix(a,b,N,q)
    U,res=solve(D,W,sig,L,K,F,np.zeros(M-1),lamgamma); cases+=1; maxres=max(maxres,res)
    # Evaluate continuous polynomial error in L2 and H1 via independent Gauss quadrature.
    z,wz=leggauss(max(80,2*M+10)); from numpy.polynomial.legendre import legvander,legder,legval
    C=np.linalg.solve(legvander(x,M),np.pad(U,((0,0),(1,1))).T)
    V=legvander(z,M)@C; Vx=np.column_stack([legval(z,legder(c)) for c in C.T]);
    ex=V-np.cos(np.pi*z[:,None]/2)*t[None,:]**2; exx=Vx+np.pi/2*np.sin(np.pi*z[:,None]/2)*t[None,:]**2
    l2=np.sqrt(wz@(ex**2)); h1=np.sqrt(wz@(ex**2+exx**2))
    return float(l2.max()),float(h1.max())
for q in [False,True]:
    rows=[spectral(16,N,q) for N in [16,32,64,128,256]]
    rates=np.log2(np.array(rows[-2])/np.array(rows[-1])); assert np.all((rates>1.85)&(rates<2.15))
    print(f'{"PI-Q" if q else "PI-L"} M=16 time sweep: '+', '.join(f'({x:.8e},{y:.8e})' for x,y in rows)+f'; last L2/H1 rates {rates[0]:.6f}/{rates[1]:.6f}')
    rows=[spectral(M,256,q) for M in [3,5,7,9,12]]
    assert rows[2][1]<rows[0][1]/100 and rows[-1][1]<rows[0][1]/100
    print(f'{"PI-Q" if q else "PI-L"} N=256 space sweep M=3,5,7,9,12: '+', '.join(f'({x:.8e},{y:.8e})' for x,y in rows))
print(f'{cases} configurations; max scaled full-equation residual {maxres:.3e}; all assertions passed.')
