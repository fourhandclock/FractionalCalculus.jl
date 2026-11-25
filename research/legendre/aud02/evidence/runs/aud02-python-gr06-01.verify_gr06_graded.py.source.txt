"""Standalone GR-06 scalar diagnostics; nonuniform panel integration via beta moments."""
import numpy as np
from scipy.special import beta, betainc, gamma
from scipy.linalg import solve_triangular

def moment(d,h,tau,r,j):
    return tau**r*d**(r+j)*beta(j+1,r)*betainc(j+1,r,np.minimum(h/d,1.0))/gamma(r)

def matrices(t,alpha,beta_order,quad):
    N=len(t)-1; dt=np.diff(t); sig=1-alpha/2; r=1-beta_order
    A=np.zeros((N,N)); W=np.zeros((N,N+1)); ts=t[:-1]+sig*dt
    for n in range(1,N+1):
        star=ts[n-1]; h=dt[:n]; d=(star-t[:n])/h; z=np.ones(n); z[-1]=sig; d[-1]=sig
        m0=moment(d,z,h,1-alpha,0); m1=moment(d,z,h,1-alpha,1)
        A[n-1,:n]=m0/h
        if n>1:
            R=h[1:]/h[:-1]; b=(2*m1[:-1]-m0[:-1])/(h[:-1]*(1+R))
            A[n-1,:n-1]-=b; A[n-1,1:n]+=b/R
        m0=moment(d,z,h,r,0); m1=moment(d,z,h,r,1); m2=moment(d,z,h,r,2)
        if not quad or n==1:
            W[n-1,:n]+=m0-m1; W[n-1,1:n+1]+=m1
        else:
            R=h[1:]/h[:-1]
            W[n-1,:n-1]+=(m2[:-1]-(2+R)*m1[:-1]+(1+R)*m0[:-1])/(1+R)
            W[n-1,1:n]+=((1+R)*m1[:-1]-m2[:-1])/R
            W[n-1,2:n+1]+=(m2[:-1]-m1[:-1])/(R*(1+R))
            rho=h[-2]/h[-1]
            W[n-1,n-2]+=(m2[-1]-m1[-1])/(rho*(1+rho))
            W[n-1,n-1]+=m0[-1]+((1-rho)*m1[-1]-m2[-1])/rho
            W[n-1,n]+=(m2[-1]+rho*m1[-1])/(1+rho)
    return A,W,ts

def run(alpha,beta_order,grading,N,quad):
    t=(np.arange(N+1)/N)**grading; dt=np.diff(t); sig=1-alpha/2; theta=1-sig; r=1-beta_order
    A,W,ts=matrices(t,alpha,beta_order,quad)
    assert np.all(A[np.tril_indices(N)]>0)
    for n in range(N):
        assert np.all(np.diff(A[n,:n+1])>0)
        if n: assert (2*sig-1)*A[n,n]>sig*A[n,n-1]
    d=4/(11*gamma(1-alpha)); L=1 if not quad else 1+1/(2*(dt[:-1]/dt[1:]).min()*(1+(dt[:-1]/dt[1:]).min()))
    assert np.max(np.abs(W.sum(axis=1)-ts**r/gamma(1+r)))<2e-12
    assert np.max(np.abs(W)@np.ones(N+1)-L*ts**r/gamma(1+r))<2e-12
    P=solve_triangular(A.T,np.tril(np.ones((N,N))).T,lower=False).T
    assert P.min()>-1e-12
    assert np.max(np.abs(P@A-np.tril(np.ones((N,N)))))<2e-10
    H=np.abs(W[:,1:]); PH=P@H
    for n in range(N):
        ell=t[n+1]-t[:n+1]
        assert np.all(np.cumsum(P[n,:n+1][::-1])[::-1]<=ell**alpha/d+1e-12)
        assert np.all(np.cumsum(PH[n,:n+1][::-1])[::-1]<=L*2**r*ell**(alpha+r)/(d*gamma(1+r))+1e-12)
    exact=1+t**alpha; a=2.; lam=.4
    f=gamma(1+alpha)+a*(1+ts**alpha)+lam*(ts**r/r+gamma(r)*gamma(1+alpha)/gamma(1+alpha+r)*ts**(alpha+r))
    U=np.empty(N+1); U[0]=1.
    for n in range(1,N+1):
        row=A[n-1,:n]; w=W[n-1,:n+1]; hist=np.dot(row[:-1],np.diff(U[:n]))-row[-1]*U[n-1]
        U[n]=(f[n-1]-hist-a*theta*U[n-1]-lam*gamma(r)*np.dot(w[:-1],U[:n]))/(row[-1]+a*sig+lam*gamma(r)*w[-1])
    residual=A@np.diff(U)+a*(sig*U[1:]+theta*U[:-1])+lam*gamma(r)*(W@U)-f
    # Scale by absolute terms to avoid cancellation from highly graded startup.
    scale=1+np.abs(A)@np.abs(np.diff(U))+a*(sig*np.abs(U[1:])+theta*np.abs(U[:-1]))+lam*gamma(r)*(np.abs(W)@np.abs(U))+np.abs(f)
    assert np.max(np.abs(residual)/scale)<1e-9
    derivative_defect=A@np.diff(exact)-gamma(1+alpha)
    ecs=np.max(P@np.abs(derivative_defect))
    return np.max(np.abs(U-exact)),ecs,np.max(np.abs(residual)/scale)

if __name__=='__main__':
    print('alpha,beta,grading,variant,N,max_error,global_caputo_defect,scaled_residual,rate')
    count=0
    for alpha,beta_order in [(0.5,0.25),(.75,.5),(.9,.8)]:
        for grading in [1.,2/alpha]:
            for quad in [False,True]:
                prev=None
                for N in [16,32,64,128,256]:
                    e,g,res=run(alpha,beta_order,grading,N,quad)
                    rate='' if prev is None else f'{np.log2(prev/e):.6f}'
                    print(f'{alpha},{beta_order},{grading:.8f},{"Q" if quad else "L"},{N},{e:.10e},{g:.10e},{res:.3e},{rate}',flush=True)
                    prev=e; count+=1
    print(f'PASS: {count} configurations; no convergence-rate assertions (diagnostic only).')
