"""Independent arbitrary-precision complete-beta moments for exact Float64 inputs."""
import csv,json,sys
from pathlib import Path
import mpmath as mp

def moments(values,precision):
    with mp.workdps(precision):
        h,r,H=map(lambda x:mp.mpf(float(x)),values)
        mass=(h*H)**r/mp.gamma(1+r)
        m1=mass*H/(1+r);m2=mass*H**2*2/((1+r)*(2+r))
        return tuple(+v for v in (mass,m1,m2,2*m1-mass))

def main(dest):
    cases=[('tiny_product','1e-200','.5','1e-200','reject'),
           ('subnormal_step',str(float.fromhex('0x0.0000000000001p-1022')),'.5','.55','supported'),
           ('near_zero_order','1','1e-310','1','supported')]
    rows=[]
    for name,h,r,H,status in cases:
        a=moments((h,r,H),400);b=moments((h,r,H),500)
        with mp.workdps(400):
            assert all(abs(x-y)/abs(y)<mp.mpf('1e-80') for x,y in zip(a,b))
            if status=='reject':assert 0<b[1]<mp.mpf(float.fromhex('0x0.0000000000001p-1022')) and 0<b[2]<mp.mpf(float.fromhex('0x0.0000000000001p-1022'))
        rows.append(dict(case=name,h=h,r=r,H=H,status=status,**{k:mp.nstr(v,90) for k,v in zip(['m0','m1','m2','center'],b)}))
    out=Path(dest);assert not out.exists()
    with out.open('x',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
    print(json.dumps({'precision':[400,500],'stabilization_relative':'<1e-80','criterion_relative':'5e-12','cases':rows},indent=2))
if __name__=='__main__':main(sys.argv[1])
