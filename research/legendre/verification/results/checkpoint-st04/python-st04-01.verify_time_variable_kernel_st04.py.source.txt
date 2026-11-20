"""ST-04 diagnostic: paper's homogeneous time-semidiscrete stability claim.

On (-1,1), take U(x,t)=a(t)*cos(pi*x/2), homogeneous Dirichlet,
- U_xx = sigma U, sigma = (pi/2)**2, lambda = 1, and
K(x,t)=0.05 + 500/(1+exp(-45*(t-0.3))) > 0, smooth.

This uses interpolation-defined L1-2 and the paper's printed Eq.(6)
for Volterra quadrature. Independent product integration is a control.
Finite-grid experiments are not formal proof of a N->infinity counterexample.
"""
from __future__ import annotations
import math
import numpy as np

T=0.8
SIGMA=(math.pi/2)**2
LAMBDA=1.0
ALPHA=0.95
BETA=0.05

def kernel(t):
    z = max(-600.0, min(600.0, -45*(t-0.3)))
    return .05 + 500/(1+math.exp(z))

def make_coeffs(alpha, n):
    r=np.arange(n+1, dtype=np.float64)
    b=r[1:]**(1-alpha)-r[:-1]**(1-alpha)
    bs=(r[1:]**(2-alpha)-r[:-1]**(2-alpha))/(2-alpha) - .5*(r[1:]**(1-alpha)+r[:-1]**(1-alpha))
    return b,bs

def increments_weights(b,bs,k,scheme):
    if k==0 or scheme=='L1': return b[:k+1]
    return np.r_[b[0]+bs[0], b[1:k]+bs[1:k]-bs[:k-1], b[k]-bs[k-1]]

def memory_quadrature(u,k,tau,beta,variant):
    """For n=k+1, return (past contribution, present coefficient)."""
    if variant=='published':
        if k:
            j=np.arange(k,dtype=float)
            past=.5*tau**(1-beta)*np.sum((k+1-j)**(-beta)*u[:k] + (k-j)**(-beta)*u[1:k+1])
        else: past=0.
        last=tau**(1-beta)/(2*(1-beta))
        return past+last*u[k],last
    if variant=='product_integration':
        j=np.arange(k+1,dtype=float)
        a=k+1-j  # dimensionless distances
        c=k-j
        int0=(a**(1-beta)-c**(1-beta))/(1-beta)
        int1=(a**(2-beta)-c**(2-beta))/(2-beta)
        wleft=tau**(1-beta)*(int1-c*int0)
        wright=tau**(1-beta)*(a*int0-int1)
        present=wright[-1]
        past=np.dot(wleft,u[:k+1])+np.dot(wright[:-1],u[1:k+1])
        return past,present
    raise ValueError(variant)

def solve(n,scheme='L12',variant='published',alpha=ALPHA,beta=BETA):
    tau=T/n
    a0=math.gamma(2-alpha)*tau**alpha
    mu=a0*SIGMA
    b,bs=make_coeffs(alpha,n)
    u=np.zeros(n+1);u[0]=1.
    max_res=0
    for k in range(n):
        d=increments_weights(b,bs,k,scheme)
        d0=d[0]
        old=d0*u[k] - (np.dot(d[1:],u[k:0:-1]-u[k-1::-1]) if k else 0.)
        qpast,qnow=memory_quadrature(u,k,tau,beta,variant)
        gamma=LAMBDA*a0*kernel((k+1)*tau)
        u[k+1]=(old-gamma*qpast)/(d0+mu+gamma*qnow)
    return u,mu,b,bs

def verify_direct_residual(u,mu,b,bs,scheme,variant):
    n=len(u)-1; tau=T/n
    alpha=ALPHA;beta=BETA
    a0=math.gamma(2-alpha)*tau**alpha
    sample=sorted(set([0,1,2,n//4,n//2,n-1]))
    e=0
    for k in sample:
        differences=np.diff(u[:k+2])
        frac=np.dot(b[:k+1],differences[::-1])
        if scheme=='L12' and k>=1:
            second=u[2:k+2]-2*u[1:k+1]+u[:k]
            frac+=np.dot(bs[:k],second[::-1])
        qpast,qnow=memory_quadrature(u,k,tau,beta,variant)
        residual=frac+mu*u[k+1]+LAMBDA*a0*kernel((k+1)*tau)*(qpast+qnow*u[k+1])
        e=max(e,abs(residual))
    return e

def run():
    print('Scalar Dirichlet eigenmode on (-1,1): sigma=(pi/2)^2')
    print('alpha=%.2f beta=%.2f lambda=%.1f T=%.1f K(t)=0.05+500/(1+exp(-45*(t-0.3)))' % (ALPHA,BETA,LAMBDA,T))
    print('Claim: max_{k>=1} sqrt(1+sigma*Gamma(2-alpha)*tau^alpha)*|u_k| <= |u_0| = 1')
    print('Scheme             Quadrature                N       max |u|   t at peak  weighted peak  residual')
    results=[]
    for scheme in ('L1','L12'):
        for variant in ('published','product_integration'):
            for n in (128,256,512,1024,2048,4096):
                u,mu,b,bs=solve(n,scheme,variant)
                j=1+np.argmax(abs(u[1:]))
                peak=abs(u[j])*math.sqrt(1+mu)
                res=verify_direct_residual(u,mu,b,bs,scheme,variant)
                assert np.isfinite(u).all() and res<5.e-10,(scheme,variant,n,res)
                print('%-18s %-24s %5d %12.8f %11.7f %14.8f %.2g' % (scheme,variant,n,abs(u[j]),j*T/n,peak,res))
                results.append((scheme,variant,n,peak))
    # The goal is a robust finite-grid observation, not a theorem of non-convergence.
    for scheme in ('L1','L12'):
        for variant in ('published','product_integration'):
            vals=[x for s,v,n,x in results if s==scheme and v==variant and n>=1024]
            assert all(v>2 for v in vals), (scheme,variant,vals)
    print('PASS: all checked recurrences satisfy the original two-sum operator to floating-point residual')
    print('PASS: contractivity violated by a margin > 1 at each tested fine grid, also with alternative quadrature')
    print('STATUS: numerical counterexample candidate for published global contractivity claim; not a formal theorem refutation')

if __name__=='__main__': run()
