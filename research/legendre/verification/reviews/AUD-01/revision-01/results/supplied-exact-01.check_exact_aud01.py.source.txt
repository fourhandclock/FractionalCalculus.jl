#!/usr/bin/env python3
"""Exact checks, not formal proofs of analytic estimates."""
from fractions import Fraction as F
import sympy as s
x,y,r,q=s.symbols('x y r q', real=True)
# Unit-circle real-part numerator: reduce modulo y^2 = 1-x^2.
z=x+s.I*y
num=s.expand(s.re((1-z)*(1+q*(1-z))*(1-r*s.conjugate(z))))
expected=(1-x)*(1+r+2*q*(r-x))
assert s.expand(num.subs(y**2,1-x**2)-expected)==0
assert s.expand(1+r+2*q*(r-x)-(2*r+(1-2*q)*(1-r)+2*q*(1-x)))==0
print('SP-02: real-part numerator and nonnegative decomposition exact.')
d=F(512,10**6); D=17
assert 1-D*d>0 and D/(1-D*d)<18 and D**2*d/(1-D*d)<F(1,4)
assert (3+F(800,64))/64==F(31,128)<F(1,4)
assert F(720000)*2**512*F(1,2**600)<F(1,2**68)<1
assert 0<F(1,2**600)<=1-F(1,2**600)<1
assert F(1,128)*F(21,4)*(3+F(1,16))<F(1,4)
print('ST-05 and homogeneous TM-01: rational inequalities exact.')
for N in range(2,21):
    c=s.symbols(f'c0:{N-1}'); u=(0,)+s.symbols(f'u1:{N+1}'); du=[u[j]-u[j-1] for j in range(1,N+1)]
    original=sum(sum(c[n-j]*(du[j-1]-du[j-2]) for j in range(2,n+1)) for n in range(2,N+1))
    collect=-sum(c)*du[0]+sum(c[N-j]*du[j-1] for j in range(2,N+1))
    assert s.expand(original-collect)==0
print('TM-01: quadratic summation identity checked symbolically for N=2..20.')

# Check the proposed real-polynomial Lean statement, independently of the complex expansion.
lhs=((1-x)+q*((1-x)**2-y**2))*(1-r*x)+(y+2*q*(1-x)*y)*(r*y)
assert s.expand(lhs-expected-(y**2-(1-x**2))*(-q*r*x+2*q*r-q+r))==0
print("Lean draft real-polynomial statement checked (not Lean compilation).")
