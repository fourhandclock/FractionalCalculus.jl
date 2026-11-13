"""Auditable transcription of published error cells; no inferred numerical targets.

Run with Python's standard library only. The source paper, not this helper,
remains the authority. Rates and CPU columns are deliberately not transcribed.
"""
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parent
rows = []

def group(table, example, scheme, *, alpha=None, beta=None, nu=None, M=9,
          N=None, vary="N", values="", grading=1, lam=1, page=None):
    """Each input line: varying alpha/beta/nu, then three published error rows.

    A block is 'parameter: L2 Linf H1; L2 Linf H1; L2 Linf H1'.
    Use '-' for an absent printed metric; no numerical estimate replaces it.
    """
    axis = (2,4,8) if vary == "M" and N == 16 and example == 1 else None
    if vary == "M" and axis is None:
        axis = (2,4,8) if example == 3 else (3,6,12)
    if vary == "N":
        axis = {5:(2,4,8),12:(16,32,64),16:(64,128,256),17:(8,16,32)}.get(table,(4,8,16))
    for block in values.strip().splitlines():
        param, cells = block.strip().split(":",1)
        av,bv,vv = alpha,beta,nu
        if param.startswith("("):
            av,bv = map(float,param.strip("() ").split("/"))
        elif alpha is None:
            av = float(param)
        elif beta is None and example == 2:
            bv = float(param)
        elif nu is None and example == 1:
            vv = float(param)
        else:
            raise ValueError((table,param))
        rv = grading(av) if callable(grading) else grading
        parsed = [s.split() for s in cells.split(";")]
        assert len(parsed) == len(axis), (table,param)
        for coordinate, errors in zip(axis,parsed):
            assert len(errors) in (1,2,3), (table,param,errors)
            errors += ["-"] * (3-len(errors))
            mm = coordinate if vary == "M" else M
            nn = coordinate if vary == "N" else N
            mx,my = mm if isinstance(mm,tuple) else (mm,None)
            rows.append(dict(table=table,example=example,scheme=scheme,alpha=av,
                             beta=bv,nu=vv,**{"lambda":lam},M1=mx,M2=my,N=nn,
                             grading=rv,L2=errors[0],Linf=errors[1],H1=errors[2],source_page=page))

group(1,1,"L1",nu=2.3,page=31,values="""
0.4: 2.2245e-3 8.9474e-3 1.8335e-2; 7.9370e-4 3.0034e-3 7.1851e-3; 2.6466e-4 9.5135e-4 2.7441e-3
0.6: 4.8330e-3 1.9924e-2 3.9023e-2; 1.9642e-3 7.7592e-3 1.6798e-2; 7.6673e-4 2.9108e-3 7.0429e-3
0.8: 9.2860e-3 3.9516e-2 7.3711e-2; 4.2896e-3 1.7699e-2 3.5125e-2; 1.9253e-3 7.7503e-3 1.6211e-2
""")
group(2,1,"L12",nu=2.3,page=30,values="""
0.4: 3.3273e-3 2.1915e-2 4.7303e-2; 9.7371e-4 8.4491e-3 2.3838e-2; 2.6784e-4 3.0923e-3 1.2063e-2
0.6: 6.8230e-3 4.1205e-2 9.1589e-2; 2.3175e-3 1.7583e-2 5.0856e-2; 7.4134e-4 7.1553e-3 2.8510e-2
0.8: 1.3028e-2 6.8748e-2 1.6056e-1; 5.3848e-3 3.2754e-2 9.9720e-2; 2.1331e-3 1.4965e-2 6.2554e-2
""")
group(3,1,"L1",alpha=.5,N=16,vary="M",page=31,values="""
2.7: 2.8750e-1 9.5546e-1 28.416e-1; 1.0008e-2 4.1633e-2 9.1194e-2; 4.6937e-4 1.7656e-3 4.5397e-3
3.7: 4.5594e-1 15.160e-1 45.110e-1; 3.5212e-2 2.0287e-1 3.7169e-1; 4.5663e-4 1.6658e-3 4.2011e-3
4.7: 6.2438e-1 20.765e-1 61.805e-1; 9.5333e-2 5.3319e-1 10.112e-1; 4.4232e-4 2.4642e-3 4.1733e-3
""")
group(4,1,"L12",alpha=.5,N=16,vary="M",page=32,values="""
2.7: 2.8528e-1 9.5014e-1 28.302e-1; 1.0038e-2 4.2414e-2 9.3919e-2; 4.4860e-4 4.8023e-3 1.9005e-2
3.7: 4.5301e-1 15.089e-1 44.957e-1; 3.4732e-2 2.0078e-1 3.6935e-1; 4.0920e-4 4.4270e-3 1.7258e-2
4.7: 6.2073e-1 20.677e-1 61.613e-1; 9.4565e-2 5.3033e-1 10.069e-1; 4.0943e-4 4.1382e-3 1.6009e-2
""")
group(5,1,"L1",nu=4.5,page=32,values="""
0.3: 3.1966e-3; 1.1500e-3; 3.9688e-4
0.5: 6.8464e-3; 2.7495e-3; 1.0611e-3
0.9: 2.0063e-2; 1.0203e-2; 5.0339e-3
""")
group(5,1,"L12",nu=4.5,page=32,values="""
0.3: 5.6050e-3; 1.7703e-3; 4.8876e-4
0.5: 1.1034e-2; 3.9354e-3; 1.2341e-3
0.9: 2.8232e-2; 1.4459e-2; 6.7021e-3
""")
group(6,2,"L1",beta=.2,page=34,values="""
0.3: 1.0560e-3 6.9093e-3 9.2909e-3; 3.5642e-4 2.2920e-3 3.2797e-3; 1.2164e-4 7.4440e-4 1.1767e-3
0.5: 2.7891e-3 1.7685e-2 2.4939e-2; 1.0518e-3 6.8253e-3 9.8430e-3; 3.9073e-4 2.5489e-3 3.7479e-3
0.8: 8.8480e-3 5.6221e-2 8.2104e-2; 3.9382e-3 2.6502e-2 3.8986e-2; 1.7387e-3 1.2054e-2 1.7789e-2
""")
group(7,2,"L12",beta=.2,page=34,values="""
0.3: 3.5250e-4 2.0597e-3 3.3269e-3; 6.2081e-5 3.0688e-4 7.9029e-4; 3.3468e-5 1.4231e-4 4.0303e-4
0.5: 8.8231e-4 4.9827e-3 7.4226e-3; 1.6838e-4 8.9013e-4 1.5351e-3; 4.4035e-5 2.1745e-4 4.7118e-4
0.8: 3.0385e-3 1.7500e-2 2.5063e-2; 7.2806e-4 4.1104e-3 6.1301e-3; 1.6928e-4 9.0468e-4 1.4661e-3
""")
group(8,2,"L1",alpha=.4,page=35,values="""
0.1: 1.7823e-3 1.1745e-2 1.5836e-2; 6.3448e-4 4.2384e-3 5.8559e-3; 2.2246e-4 1.4845e-3 2.0940e-3
0.3: 1.7571e-3 1.0467e-2 1.5480e-2; 6.3424e-4 3.9682e-3 5.8672e-3; 2.3139e-4 1.4668e-3 2.2364e-3
0.5: 1.9386e-3 1.4508e-2 1.8120e-2; 8.0336e-4 6.0853e-3 7.5348e-3; 3.7528e-4 2.3746e-3 3.4279e-3
0.7: 4.6449e-3 3.1419e-2 4.4790e-2; 2.3427e-3 1.4836e-2 2.1810e-2; 1.2409e-3 6.5369e-3 1.0421e-2
0.9: 3.4643e-2 2.2368e-1 3.4770e-1; 1.9314e-2 1.4147e-1 2.0844e-1; 1.0545e-2 7.9591e-2 1.1159e-1
""")
group(9,2,"L12",alpha=.4,page=35,values="""
0.1: 5.9439e-4 3.6707e-3 5.3742e-3; 1.0572e-4 7.1772e-4 1.0762e-3; 2.0020e-5 1.3703e-4 2.6890e-4
0.3: 5.4075e-4 2.4679e-3 4.6512e-3; 1.4170e-4 7.3520e-4 1.3233e-3; 8.1877e-5 3.1141e-4 7.6276e-4
0.5: 1.0919e-3 7.1331e-3 1.0099e-2; 5.7381e-4 2.9415e-3 4.6737e-3; 3.3002e-4 1.2372e-3 2.6476e-3
0.7: 4.5411e-3 2.4311e-2 4.3560e-2; 2.3894e-3 1.3488e-2 2.2228e-2; 1.2774e-3 6.6339e-3 1.0739e-2
0.9: 3.4890e-2 2.3187e-1 3.5235e-1; 1.9712e-2 1.4701e-1 2.1341e-1; 1.0768e-2 8.2188e-2 1.1414e-1
""")
group(10,2,"L1",N=32,vary="M",page=36,values="""
(0.3/0.1): 1.3976e-1 2.7591e-1 2.6600e+0; 2.7927e-4 8.4145e-4 5.2322e-3; 3.4532e-5 2.6009e-4 3.6333e-4
(0.5/0.3): 1.4179e-1 2.8509e-1 2.2732e+0; 3.6259e-4 1.2217e-3 5.0232e-3; 1.3122e-5 1.5458e-4 4.3912e-4
(0.8/0.5): 1.4763e-1 3.1086e-1 1.7775e+0; 1.0486e-3 5.5663e-3 9.7273e-3; 1.7901e-4 5.5097e-3 1.5565e-3
""")
group(11,2,"L12",N=16,vary="M",page=36,values="""
(0.4/0.2): 1.4111e-1 2.8052e-1 2.3030e+0; 2.6837e-4 9.1842e-4 4.3114e-3; 3.1565e-5 1.6431e-4 3.6334e-4
(0.6/0.3): 1.4829e-1 2.9191e-1 2.3391e+0; 3.1038e-4 1.1433e-3 4.4778e-3; 8.3640e-5 4.7060e-4 7.8372e-4
(0.8/0.1): 1.5951e-1 3.1499e-1 2.4241e+0; 4.0768e-4 1.3283e-3 4.8115e-3; 1.4713e-4 4.7020e-4 1.4192e-3
""")
group(12,2,"L1",lam=0,page=36,values="""
0.2: 5.6599e-5 3.3365e-4 5.0785e-4; 1.7699e-5 1.0214e-4 1.5885e-4; 5.4833e-6 2.8916e-5 4.8892e-5
0.4: 2.2202e-4 1.3746e-3 2.0688e-3; 7.6927e-5 4.7744e-4 7.2126e-4; 2.6349e-5 1.6146e-4 2.4694e-4
0.6: 6.5985e-4 4.2689e-3 6.4212e-3; 2.5659e-4 1.6779e-3 2.5239e-3; 9.9001e-5 6.4854e-4 9.7773e-4
""")
group(13,2,"L12",lam=0,page=37,values="""
0.2: 1.7581e-4 7.6705e-4 1.7265e-3; 2.6508e-5 1.1347e-4 3.1627e-4; 4.0555e-6 1.6097e-5 5.9493e-5
0.4: 5.3978e-4 2.3767e-3 4.6158e-3; 9.5926e-5 4.2885e-4 8.6539e-4; 1.6839e-5 7.2001e-5 1.5898e-4
0.6: 1.3412e-3 6.6298e-3 1.0921e-2; 2.7848e-4 1.3840e-3 2.3085e-3; 5.5997e-5 2.7304e-4 4.6768e-4
""")
group(14,2,"L1",lam=0,page=37,values="""
0.3: 1.0402e-3; 3.5520e-4; 1.1864e-4
0.5: 2.7757e-3; 1.0510e-3; 3.9049e-4
0.9: 1.2419e-2; 5.8429e-3; 2.7372e-3
""")
group(14,2,"L12",lam=0,page=37,values="""
0.3: 3.2216e-4; 5.2730e-5; 8.6300e-6
0.5: 8.6379e-4; 1.6618e-4; 3.1235e-5
0.9: 4.4181e-3; 1.1430e-3; 2.8185e-4
""")
group(15,3,"L1",beta=.5,grading=lambda a:(2-a)/a,page=39,values="""
0.3: 5.3499e-3 3.1299e-2; 2.0140e-3 1.0478e-2; 7.0119e-4 3.4409e-3
0.6: 3.8685e-3 2.0226e-2; 2.0274e-3 1.1306e-2; 1.0175e-3 5.6123e-3
0.9: 1.3795e-3 7.0480e-3; 9.6039e-4 5.8760e-3; 7.2354e-4 3.8656e-3
""")
group(16,3,"L1",beta=.5,M=3,page=39,values="""
0.3: 3.4379e-3 2.2657e-2; 3.0906e-3 2.0791e-2; 2.8675e-3 1.8484e-2
0.6: 2.9085e-3 1.0903e-2; 2.5492e-3 7.6572e-3; 2.3730e-3 5.6356e-3
0.9: 2.2244e-3 5.9286e-3; 2.0736e-3 5.7662e-3; 1.9797e-3 5.6398e-3
""")
group(17,3,"L12",beta=.5,grading=lambda a:(3-a)/a,page=39,values="""
0.3: 3.3589e-3 2.7550e-2; 9.1473e-4 7.5779e-3; 2.3131e-4 1.1198e-3
0.6: 6.0870e-3 3.3119e-2; 1.5080e-3 8.4824e-3; 2.7758e-4 1.8099e-3
0.9: 1.5379e-3 7.7990e-3; 4.0562e-4 1.5634e-3; 1.0425e-4 6.2404e-4
""")
group(18,3,"L1",beta=.5,N=64,vary="M",grading=lambda a:2*(2-a)/a,page=40,values="""
0.3: 2.5252e-2 1.0026e-1; 2.2019e-4 1.1063e-3; 1.0234e-4 5.5096e-4
0.6: 2.6346e-2 1.0526e-1; 3.0986e-4 1.4488e-3; 1.0882e-4 6.2803e-4
0.9: 2.7409e-2 1.0538e-1; 3.2195e-4 1.4413e-3; 1.1007e-4 5.2171e-4
""")
group(19,4,"L1",beta=.3,M=(5,5),grading=lambda a:(2-a)/a,page=41,values="""
0.45: 5.9062e-3 3.8958e-2; 3.5429e-3 3.5706e-2; 2.1928e-3 3.2754e-2
0.65: 5.3477e-3 3.4206e-2; 3.3389e-3 3.1436e-2; 2.1465e-3 2.9346e-2
0.85: 4.9945e-3 3.0738e-2; 3.2165e-3 2.8470e-2; 2.1254e-3 2.6955e-2
""")
group(19,4,"L1",beta=.3,M=(5,5),page=41,values="""
0.45: 6.1532e-3 3.2421e-2; 4.2507e-3 3.0477e-2; 2.9293e-3 2.9248e-2
0.65: 5.4924e-3 3.0609e-2; 3.7581e-3 2.8827e-2; 2.5734e-3 2.7665e-2
0.85: 5.0543e-3 2.9275e-2; 3.3834e-3 2.7502e-2; 2.2942e-3 2.6356e-2
""")
group(20,4,"L12",beta=.3,M=(4,4),grading=lambda a:(3-a)/a,page=42,values="""
0.4: 6.2904e-3 6.0567e-2; 2.6129e-3 3.8054e-2; 1.6703e-3 1.4049e-2
0.6: 4.1192e-3 4.2625e-2; 3.8102e-3 3.3203e-2; 3.4659e-3 2.3433e-2
0.8: 1.0139e-2 1.4625e-1; 8.7059e-3 8.9614e-2; 6.5564e-3 4.9235e-2
""")
for grading, data in [
    (lambda a:(2-a)/a,"""
0.55: 6.7186e-2 3.3624e-1; 4.2058e-3 3.8167e-2; 3.8733e-4 3.9043e-3
0.85: 6.8786e-2 3.2251e-1; 3.4688e-3 2.9247e-2; 2.0014e-4 3.5303e-3
"""),
    (1,"""
0.55: 8.0675e-2 3.2365e-1; 4.0357e-3 3.0414e-2; 2.1104e-4 4.0103e-3
0.85: 7.3010e-2 3.1880e-1; 3.4118e-3 2.6950e-2; 3.4916e-4 2.8176e-3
""")]:
    start = len(rows)
    group(21,4,"L1",beta=.3,N=4,vary="M",grading=grading,page=42,values=data)
    for row in rows[start:]:
        row["M2"] = row["M1"]

rows.sort(key=lambda r:(r["table"],r["scheme"],r["alpha"],r["beta"] or 0,
                        r["nu"] or 0,r["grading"],r["M1"],r["N"]))
assert len(rows) == 231, len(rows)
assert {row["table"] for row in rows} == set(range(1,22))
assert sum(row[name] not in (None,"-") for row in rows for name in ("L2","Linf","H1")) == 546
with (ROOT / "reference_tables.csv").open("w",newline="",encoding="utf-8") as stream:
    writer = csv.DictWriter(stream,fieldnames=list(rows[0]))
    writer.writeheader()
    for row in rows:
        writer.writerow({key:"" if value in (None,"-") else value for key,value in row.items()})
print(f"Transcribed {len(rows)} configurations across 21 tables.")
