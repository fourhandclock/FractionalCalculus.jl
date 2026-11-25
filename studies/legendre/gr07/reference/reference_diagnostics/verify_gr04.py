"""GR-04 checks. Requires unchanged verify_gr03.py, NumPy, SciPy, mpmath.
Tests finite matrices, not the infinite-grid proof. Run with one BLAS worker.
"""
import itertools
import math
import numpy as np
from scipy.linalg import solve_triangular
from scipy.special import gammaln
from numpy.polynomial.legendre import leggauss
from verify_gr03 import matrix as memory_matrix

rng=np.random.default_rng(404)

def majorant(s,C,N):
    l=np.arange(N,dtype=float); tau=1/N
    weights=C*tau**s*((l+1)**s-l**s)
    i,j=np.indices((N,N)); D=np.where(i>=j,weights[np.maximum(i-j,0)],0.)
    return D

def resolve(B,a):
    return solve_triangular(np.eye(len(B))-B,a,lower=True)

def ml(t,p,q,a,b,terms=100):
    # Diagnostic evaluation, no certified truncation error used in assertions.
    if t==0: return 1.
    z=0.
    for k in range(terms):
        for j in range(k+1):
            R=(k-j)*p+j*q
            z+=math.exp(gammaln(k+1)-gammaln(j+1)-gammaln(k-j+1)+(k-j)*math.log(a)+j*math.log(b)+R*math.log(t)-gammaln(1+R))
    return z

def shifted_bound(t,tau,p,q,a,b,xi,K=40):
    eta=math.exp(xi*tau)*(a*xi**(-p)+b*xi**(-q))
    assert eta<1
    z=1.
    for k in range(1,K+1):
        for j in range(k+1):
            R=(k-j)*p+j*q
            z+=math.exp(gammaln(k+1)-gammaln(j+1)-gammaln(k-j+1)+(k-j)*math.log(a)+j*math.log(b)+R*math.log(t+(k-1)*tau)-gammaln(1+R))
    return z+math.exp(xi*t)*eta**(K+1)/(1-eta)

def redistribute(D):
    B=D.copy(); N=len(B)
    for n in range(1,N):
        # Transfer diagonal mass backwards; tail domination holds, but
        # entrywise domination need not. Vary by row to break commutativity.
        f=rng.uniform(.15,.85); k=rng.integers(0,n)
        moved=B[n,n]*f; B[n,n]-=moved; B[n,k]+=moved
    return B

maxword=maxres=0.; mincomm=1e9; count=0
for p,q in [(.35,.85),(.75,1.25),(.95,1.6)]:
    for N in [8,16,32,64]:
        D=[majorant(p,.35,N),majorant(q,.45,N)]; B=[redistribute(x) for x in D]
        assert any(np.any(b>d+1e-14) for b,d in zip(B,D))
        for b,d in zip(B,D):
            assert np.all(np.cumsum(b[:,::-1],axis=1)<=np.cumsum(d[:,::-1],axis=1)+1e-13)
        comm=np.linalg.norm(B[0]@B[1]-B[1]@B[0],np.inf); mincomm=min(mincomm,comm); assert comm>1e-6
        for length in range(1,6):
            for word in itertools.product(range(2),repeat=length):
                u=v=np.ones(N)
                for j in word: u=B[j]@u; v=D[j]@v
                assert np.all(u<=v+1e-12); maxword=max(maxword,float(np.max(u-v)))
        a=np.linspace(1,2,N); y=resolve(sum(B),a); g=resolve(sum(D),np.ones(N))
        assert np.all(y>=0) and np.all(y<=a*g+1e-12)
        maxres=max(maxres,float(np.max(np.abs(y-a-sum(B)@y))))
        count+=1
print(f'Abstract noncommuting matrices: {count} cases, {count*62} word inequalities, minimum commutator infinity norm {mincomm:.6e}')
print(f'Max comparison excess (clipped at zero): {max(0.,maxword):.3e}; equality residual {maxres:.3e}')

print('Continuous limit of scalar majorant at T=1 (not a PDE solution):')
for p,q in [(.35,.85),(.75,1.25),(.95,1.6)]:
    C1=.35; C2=.45; a=C1*math.gamma(1+p); b=C2*math.gamma(1+q)
    exact=ml(1,p,q,a,b); xi=32. if p<.5 else 4.
    errors=[]
    for N in [32,64,128,256]:
        D=majorant(p,C1,N)+majorant(q,C2,N)
        g=resolve(D,np.ones(N))[-1]; errors.append(abs(g-exact))
        # Use sufficient geometric condition when available, independently
        # of whether the actual triangular resolvent exists.
        if math.exp(xi/N)*(a*xi**(-p)+b*xi**(-q))<.85:
            assert g<=shifted_bound(1,1/N,p,q,a,b,xi)+1e-10
    assert errors[-1]<errors[0]
    print(f'p={p:.2f} q={q:.2f}: continuous={exact:.9f}; errors='+', '.join(f'{x:.6e}' for x in errors))

# Actual Alikhanov increment matrix from independent panel integration.
def derivative(a,N):
    sig=1-a/2; x,w=leggauss(48); x=(x+1)/2; w=w/2
    A=np.zeros((N,N)); A[np.diag_indices(N)]=sig**(1-a)*N**a/math.gamma(2-a)
    for lag in range(1,N):
        kernel=(lag+sig-x)**(-a)*N**a/math.gamma(1-a)
        left=np.sum(w*kernel*(1.5-x)); right=np.sum(w*kernel*(x-.5))
        k=np.arange(N-lag); A[k+lag,k]+=left; A[k+lag,k+1]+=right
    return A

maxenergy=maxcompare=maxpde=0.; minratio=1e99; cases=0
for alpha,beta in [(.25,.1),(.5,.25),(.75,.5),(.95,.9)]:
    r=1-beta; sig=1-alpha/2; theta=1-sig; d=1/(2*math.gamma(1-alpha))
    for N in [32,64,128]:
        A=derivative(alpha,N); P=np.tril(np.ones_like(A))@solve_triangular(A,np.eye(N),lower=True)
        assert np.max(np.abs(P@A-np.tril(np.ones_like(A))))<2e-12
        S=np.zeros((N,N+1)); S[np.arange(N),np.arange(1,N+1)]=sig; S[np.arange(N),np.arange(N)]=theta
        L=np.diag([.7,3.,10.]); K0=np.array([[1.,.3,0.],[.3,.8,.2],[0.,.2,.6]])
        K=np.array([(1+.2*np.sin(7*n/N))*K0 for n in range(1,N+1)])
        lamgamma=.05; mu=lamgamma*max(np.linalg.norm(k,2) for k in K); eps=.10
        F=rng.normal(size=(N,3))*.1; f2=np.sum(F*F,axis=1); I=np.eye(3)
        for quad in [False,True]:
            W=memory_matrix(alpha,beta,N,quad); H=np.abs(W)
            Lx=1.25 if quad else 1.; Cx=Lx*2**r if quad else 1.
            b=eps+mu*Lx/math.gamma(1+r)
            B1=b*P@S[:,1:]; B2=mu*P@H[:,1:]; B=B1+B2
            C1=b/d; C2=mu*Cx/(d*math.gamma(1+r)); D=majorant(alpha,C1,N)+majorant(alpha+r,C2,N)
            assert np.all(np.cumsum(B[:,::-1],axis=1)<=np.cumsum(D[:,::-1],axis=1)+1e-12)
            assert D[0,0]<1
            U=np.zeros((N+1,3)); U[0]=[1.,-.2,.3]
            for n in range(N):
                mat=A[n,n]*I+sig*L+lamgamma*W[n,n+1]*K[n]
                rhs=F[n]+A[n,n]*U[n]-A[n,:n]@np.diff(U[:n+1],axis=0)-theta*L@U[n]-lamgamma*K[n]@(W[n,:n+1]@U[:n+1])
                U[n+1]=np.linalg.solve(mat,rhs)
                minratio=min(minratio,float(np.linalg.svd(mat,compute_uv=False)[-1]))
            V=S@U; R=A@np.diff(U,axis=0)+V@L.T+lamgamma*np.einsum('nij,nj->ni',K,W@U)-F
            res=np.max(np.abs(R))/(1+np.max(np.abs(A@np.diff(U,axis=0)))); maxpde=max(maxpde,res); assert res<2e-12
            E=np.sum(U*U,axis=1); lhs=A@np.diff(E); rhs=b*S@E+mu*H@E+f2/eps
            maxenergy=max(maxenergy,float(np.max(lhs-rhs))); assert np.all(lhs<=rhs+1e-11)
            a=E[0]*(1+b*P@S[:,0]+mu*P@H[:,0])+P@f2/eps
            g=resolve(D,np.ones(N)); envelope=np.maximum.accumulate(a)*g
            maxcompare=max(maxcompare,float(np.max(E[1:]-envelope))); assert np.all(E[1:]<=envelope+1e-11)
            cases+=1
print(f'Actual shifted schemes: {cases} configurations; noncommuting positive time-dependent K and diffusion')
print(f'Max scaled full-equation residual: {maxpde:.3e}; min sampled step singular value: {minratio:.6e}')
print(f'Max energy inequality/comparison excess (clipped at zero): {maxenergy:.3e}, {maxcompare:.3e}')
print('All assertions passed.')
