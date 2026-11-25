"""Exact finite adversarial checks of GR-04, independent of supplied diagnostics."""
from fractions import Fraction as F
from itertools import product
from math import factorial
import json,random
from pathlib import Path

def mm(A,B):return [[sum((a*b for a,b in zip(row,col)),F(0)) for col in zip(*B)] for row in A]
def mv(A,x):return [sum((a*b for a,b in zip(row,x)),F(0)) for row in A]
def majorant(n,s,c,tau):return [[c*tau**s*((i-j+1)**s-(i-j)**s) if j<=i else F(0) for j in range(n)] for i in range(n)]
def perturb(D,rng):
    B=[row[:] for row in D]
    for i in range(1,len(D)):
        for k in range(i,0,-1):
            amount=B[i][k]*F(rng.randrange(1,9),10)
            B[i][k]-=amount;B[i][rng.randrange(k)]+=amount
    return B
def resolvent_one(B):
    x=[]
    for i,row in enumerate(B):x.append((1+sum((row[j]*x[j] for j in range(i)),F(0)))/(1-row[i]))
    return x

def main():
    rng=random.Random(20261126);counts={'words':0,'ordered_vectors':0,'simplex_bounds':0,'resolvents':0}
    witnesses={}
    for n in (2,4,7):
      for p,q in ((1,2),(2,3),(1,1)):
        tau=F(1,16);C=[F(1,3),F(2,5)];ss=[p,q]
        D=[majorant(n,s,c,tau) for s,c in zip(ss,C)];B=[perturb(d,rng) for d in D]
        for i in range(2):
          for row in range(n):
            for m in range(row+1):assert sum(B[i][row][m:row+1])<=sum(D[i][row][m:row+1])
          v=[];v0=F(0)
          for _ in range(n):v0+=F(rng.randrange(10),7);v.append(v0)
          assert all(x<=y for x,y in zip(mv(B[i],v),mv(D[i],v)));counts['ordered_vectors']+=1
        if mm(B[0],B[1])!=mm(B[1],B[0]):witnesses['noncommuting_originals']=True
        if any(B[i][j][k]>D[i][j][k] for i in range(2) for j in range(n) for k in range(n)):witnesses['no_entrywise_domination']=True
        for h in range(1,7):
          for word in product(range(2),repeat=h):
            vb=vd=[F(1)]*n
            for i in reversed(word):vb=mv(B[i],vb);vd=mv(D[i],vd)
            assert all(x<=y for x,y in zip(vb,vd));counts['words']+=1
            R=sum(ss[i] for i in word);K=F(1)
            for i in word:K*=C[i]*factorial(ss[i])
            for j,x in enumerate(vd,1):
                lo=K*((j-1)*tau)**R/factorial(R)
                hi=K*((j+h-1)*tau)**R/factorial(R)
                assert lo<=x<=hi;counts['simplex_bounds']+=1
        BB=[[B[0][i][j]+B[1][i][j] for j in range(n)] for i in range(n)]
        DD=[[D[0][i][j]+D[1][i][j] for j in range(n)] for i in range(n)]
        assert all(x<=y for x,y in zip(resolvent_one(BB),resolvent_one(DD)));counts['resolvents']+=1
    # Row-tail domination is not a bound on arbitrary oscillating vectors.
    B=[[F(0),F(0)],[F(2),F(0)]];D=[[F(1),F(0)],[F(1),F(1)]]
    v=[F(1),F(0)];assert mv(B,v)[1]>mv(D,v)[1]
    witnesses['monotonicity_is_essential']={'Bv':list(map(str,mv(B,v))),'Dv':list(map(str,mv(D,v)))}
    out={'arithmetic':'fractions.Fraction, exact','seed':20261126,'counts':counts,'witnesses':witnesses,'result':'all required finite comparisons passed'}
    Path('/var/tmp/abstract.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
