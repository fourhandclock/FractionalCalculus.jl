"""Independent checks for Sabawi et al. Theorem 3.1 (L1-2 component).

This script uses the interpolatory two-sum coefficients, NOT the paper's
misindexed single sum or its d0=1 post-startup assertion.
The scalar problem is D_C^alpha u + sigma*u + lam*J[u] = 0, u(0)=1,
J[u](t)= integral_0^t (t-s)^(-beta) u(s) ds, K=1.

A scalar test can expose discrepancies but cannot prove PDE stability.
"""
import math


def weights(alpha, k):
    """The coefficients of increments from the two-sum interpolatory rule."""
    def b(r):
        return (r + 1.0)**(1-alpha) - r**(1-alpha)

    def bs(r):
        return ((r+1.0)**(2-alpha)-r**(2-alpha))/(2-alpha) - ((r+1.0)**(1-alpha)+r**(1-alpha))/2

    if k == 0:
        return [1.0]
    return [1+bs(0)] + [b(r)+bs(r)-bs(r-1) for r in range(1,k)] + [b(k)-bs(k-1)]


def memory_past(values, k, tau, beta):
    # k = current level - 1; values[0..k] are already known.
    # Ordinary trapezoid on panels j=0..k-1; final endpoint is separated.
    return 0.5*tau**(1-beta)*sum(
        (k+1-j)**(-beta)*values[j]+(k-j)**(-beta)*values[j+1]
        for j in range(k)
    )


def recurrence(alpha, beta, n, sigma, lam, style='collected'):
    tau=1.0/n
    a0=math.gamma(2-alpha)*tau**alpha
    mu=a0*sigma
    theta=lam*a0*tau**(1-beta)/(2*(1-beta))
    U=[1.0]
    for k in range(n):
        ds=weights(alpha,k)
        d0=ds[0]
        if style=='collected':
            old=(ds[0]-ds[1])*U[k]+sum((ds[r]-ds[r+1])*U[k-r] for r in range(1,k))+ds[k]*U[0] if k else U[0]
        elif style=='increments':
            old=d0*U[k]-sum(ds[r]*(U[k+1-r]-U[k-r]) for r in range(1,k+1))
        else:
            raise ValueError(style)
        jpast=memory_past(U,k,tau,beta)
        U.append((old-theta*U[k]-lam*a0*jpast)/(d0+mu+theta))
    return U,mu


def run():
    alpha=0.75
    d0,d1=weights(alpha,1)
    h1=[d0-d1,d1]
    print('Exact structural checks (alpha=3/4, k=1)')
    print('d0 = %.12f; d1 = %.12f; sum abs history / d0 = %.12f' % (d0,d1,sum(abs(v) for v in h1)/d0))
    assert d1<0
    assert sum(abs(v) for v in h1)>d0
    print('Why induction fails: admissible bounds |U0|,|U1|<=1 allow (U0,U1)=(-1,+1)')
    print('history magnitude = %.12f > d0 = %.12f' % (sum(abs(v) for v in h1),d0))
    print('This is NOT a numerical-scheme trajectory.')

    # A demonstrable difference between eq. (28) and the d0=1 substitution in (30).
    mu=0.3
    u1=1/(1+mu)
    correct=((d0-d1)*u1+d1)/(d0+mu)
    false_one=((1-d1)*u1+d1)/(1+mu)
    print('Reduced diffusion step: u1 %.10f, u2 corrected %.10f, u2 using d0=1 in eq. (30) %.10f' % (u1,correct,false_one))
    assert abs(correct-false_one)>1e-3

    checked=0
    maxdiff=0.0
    best=(0.0,None)
    for a in (.25,.5,.75,.9):
        for beta in (.2,.5,.8):
            for sig in (.25,1.0,10.0):
                for lam in (0.0,.1,1.0,10.0):
                    for n in (16,32,64):
                        vals,mu=recurrence(a,beta,n,sig,lam,'collected')
                        compare,_=recurrence(a,beta,n,sig,lam,'increments')
                        diff=max(abs(x-y) for x,y in zip(vals,compare))
                        maxdiff=max(maxdiff,diff)
                        assert diff<2.e-11, (a,beta,sig,lam,n,diff)
                        if all(math.isfinite(v) for v in vals):
                            weighted=max(abs(v)*math.sqrt(1+mu) for v in vals[1:])
                            if weighted>best[0]: best=weighted,(a,beta,sig,lam,n)
                        checked+=1
    print('Independent recurrence representations: %d parameter cases; maximum discrepancy %.3g' % (checked,maxdiff))
    print('Largest weighted amplification across tested trajectories = %.8f; parameters=%s' % (best[0],best[1]))
    print('Finite tests are diagnostic only, not a general PDE stability theorem.')

if __name__ == '__main__':
    run()
