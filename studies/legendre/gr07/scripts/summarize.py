"""Produce finite-window convergence and five-repeat timing tables from actual CSVs."""
import csv,json,statistics,math,sys
from pathlib import Path
from collections import defaultdict


def read(p):
    with Path(p).open() as f:return list(csv.DictReader(f))


def write(p,rows):
    with p.open('x',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)


def main(science,timing,outdir):
    out=Path(outdir);out.mkdir(parents=True,exist_ok=True);groups=defaultdict(list)
    for r in read(science):
        if int(r['M'])==14:groups[tuple(r[k] for k in ['alpha','beta','case','variant','grading'])].append(r)
    rates=[]
    for key,rs in groups.items():
        rs=sorted(rs,key=lambda r:int(r['N']));assert [int(r['N']) for r in rs]==[32,64,128,256]
        e=[float(r['h1_max']) for r in rs];row=dict(zip(['alpha','beta','case','variant','grading'],key))
        row.update(rate_32_64=math.log2(e[0]/e[1]),rate_64_128=math.log2(e[1]/e[2]),rate_128_256=math.log2(e[2]/e[3]),window_64_256=math.log(e[1]/e[3],4))
        rates.append(row)
    write(out/'convergence_windows.csv',rates)
    groups=defaultdict(list)
    for r in read(timing):groups[tuple(r[k] for k in ['case','variant','grading','N','phase'])].append(r)
    summaries=[]
    for key,rs in sorted(groups.items()):
        assert len(rs)==5 and {int(r['repeat']) for r in rs}==set(range(1,6))
        row=dict(zip(['case','variant','grading','N','phase'],key));times=[float(r['seconds']) for r in rs]
        row.update(repeats=5,median_seconds=statistics.median(times),minimum_seconds=min(times),maximum_seconds=max(times),median_allocations=statistics.median(float(r['allocation_count']) for r in rs),median_allocated_bytes=statistics.median(float(r['allocated_bytes']) for r in rs),h1_max=float(rs[0]['h1_max']),time_weight_bytes=int(rs[0]['time_weight_bytes']),history_bytes=int(rs[0]['history_bytes']))
        summaries.append(row)
    write(out/'timing_summary.csv',summaries)
    print('Summarized',len(rates),'finite-grid trajectories and',len(summaries),'five-repeat phase groups; no rate assertions or cross-language speedups.')

if __name__=='__main__':main(*sys.argv[1:])
