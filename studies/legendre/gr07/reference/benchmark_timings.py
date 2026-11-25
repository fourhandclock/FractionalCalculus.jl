"""Warm-up + five serial repeats. Run under the same thread settings as benchmark_gr07.py."""
import csv, statistics as s
from benchmark_gr07 import trial, VARIANTS
rows=[]
for kind,grading in [('smooth',1.),('singular',2/.75)]:
    for v in VARIANTS if kind=='smooth' else VARIANTS[-2:]:
        trial(.75,.5,256,14,kind,v,grading)
        for rep in range(5):
            row=trial(.75,.5,256,14,kind,v,grading); row['repeat']=rep+1; rows.append(row)
with open('timing_repeats.csv','x',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0]); w.writeheader(); w.writerows(rows)
for kind in ['smooth','singular']:
    for v in VARIANTS:
        x=[r for r in rows if r['case']==kind and r['variant']==v]
        if x: print(kind,v,'assembly median ms',round(s.median(r['assembly_s'] for r in x)*1000,2),'solve median ms',round(s.median(r['solve_s'] for r in x)*1000,2),'weights bytes',x[0]['time_weight_bytes'])
