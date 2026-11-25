"""Offline GR-07 documentary/source/evidence integrity checks, not a PDE proof."""
import ast,csv,hashlib,json,math,re,sys,tomllib
from collections import Counter
from pathlib import Path
from urllib.parse import unquote,urlsplit
from xml.etree import ElementTree as ET
from compare import compare

S=Path(__file__).resolve().parents[1];ROOT=S.parents[2];EV=S/'evidence';checks=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def check(name,value,**details):checks.append({'check':name,'passed':bool(value),**details})
def csvrows(p):
    with p.open() as f:return list(csv.DictReader(f))

for name,base in [('baseline.json',ROOT),('supplied-inputs.json',S/'reference')]:
    data=load(EV/name);bad=[n for n,item in data['files'].items() if not (base/n).is_file() or sha(base/n)!=item['sha256']]
    check('preserved:'+name,not bad,count=len(data['files']),discrepancies=bad)

records={};bad=[];failed=[]
for path in sorted((EV/'runs').glob('*.json')):
    d=load(path)
    if 'command' not in d:continue
    records[path.stem]=d
    for file,item in d['output'].items():
        p=path.parent/file
        if not p.is_file() or sha(p)!=item['sha256'] or p.stat().st_size!=item['bytes']:bad.append(str(p.relative_to(S)))
    for source,digest in d['source_sha256'].items():
        p=path.parent/(path.stem+'.'+Path(source).name+'.source.txt')
        if not p.is_file() or sha(p)!=digest:bad.append(str(p.relative_to(S)))
    cleanup=load(path.with_name(path.stem+'.namespace.json'))
    if not cleanup['namespace_cleanup_verified'] or cleanup['surviving_namespace_pids']:bad.append(path.stem+':cleanup')
    if d['returncode']!=0:failed.append(path.stem)
    if any('invalid_initial' in str(a) or 'benchmark_gr07_initial.py' in str(a) or re.search(r'verify_gr\d+.*_initial\.py',str(a)) for a in d['command']):bad.append(path.stem+':invalid initial executed')
check('run_sources_outputs_and_namespace_cleanup',not bad,records=len(records),discrepancies=bad)
check('failed_attempt_retained_and_excluded',failed==['local-oracle-01'],failed_attempts=failed,scope='New exact-zero oracle guard failure retained; corrected run is independently required by admission.')

admitted=tomllib.loads((EV/'admission.toml').read_text())
bad=[name for name,digest in admitted['files'].items() if sha(S/name)!=digest]
check('measured_admission_identity',admitted['status']=='admitted' and not bad,files=len(admitted['files']),discrepancies=bad)
manifest_fields={'source_sha256':'source','configuration_sha256':'configuration','inputs_sha256':'inputs','environment_sha256':'environment','oracles_sha256':'oracles','criteria_sha256':'criteria','suite_sha256':'suite'}
for folder in [EV/'admission',EV/'replays/replay-check/admission']:
    bad=[]
    for kind in ['baseline','candidate']:
        d=load(folder/(kind+'.json'))
        if d['admission_status']!='admitted':bad.append(kind)
        for field,file in manifest_fields.items():
            p=folder/(file+'.json')
            if sha(p)!=d['identities'][field]:bad.append(field)
            for name,digest in load(p)['files'].items():
                if sha(S/name)!=digest:bad.append(name)
        if sha(folder/'evidence.json')!=d['evidence_manifest_sha256']:bad.append('evidence manifest')
        for name,digest in load(folder/'evidence.json').items():
            if sha(S/name)!=digest:bad.append(name)
    check('correctness_admissions:'+str(folder.relative_to(S)),not bad,discrepancies=bad)

for first,second in [('reference/results.csv','results/python_reference.csv'),('results/python_reference.csv','results/julia_results.csv'),('results/python_reference.csv','results/replay-check/python_reference.csv'),('results/julia_results.csv','results/replay-check/julia_results.csv')]:
    result=compare(S/first,S/second)
    check('scientific_comparison:'+second,result['passed'],**{k:v for k,v in result.items() if k!='passed'})

perf=csvrows(S/'results/timing_repeats.csv');warm=csvrows(S/'results/warmups.csv')
groups=Counter((r['case'],r['variant'],r['grading'],r['N'],r['phase']) for r in perf)
check('timing_design',len(perf)==420 and len(warm)==84 and len(groups)==84 and all(v==5 for v in groups.values()),measured_solves=len(perf)//4,warmup_solves=len(warm)//4,phase_groups=len(groups))
check('measured_samples',all(float(r['scaled_residual'])<1e-9 and float(r['seconds'])>0 and float(r['total_compile_s'])==0 for r in perf))
summary=load(S/'results/summary.json')
check('count_summary',summary['experimental_unit_assertions']==7941 and summary['baseline_regression_assertions']==summary['final_regression_assertions']==669 and summary['julia_scientific_configurations']==156)

figure_data=load(S/'figures/figure-data.json');svgs=list((S/'figures').glob('*.svg'));bad=[]
for p in svgs:
    try:
        xml=ET.parse(p);assert xml.getroot().tag.endswith('svg')
        assert not re.search(r'\b(?:nan|inf)\b',p.read_text(),re.I)
    except (ET.ParseError,AssertionError):bad.append(p.name)
check('standalone_figures',len(svgs)==10 and not bad,figures=len(svgs),discrepancies=bad)
check('figure_input_identity',sha(S/figure_data['scientific_csv'])==figure_data['scientific_sha256'] and sha(S/figure_data['timing_csv'])==figure_data['timing_sha256'] and not figure_data['invalid_initial_input_used'])

links=0;broken=[]
def slugs(p):
    result=set();counts=Counter()
    for text in re.findall(r'^#{1,6}\s+(.+?)\s*#*\s*$',p.read_text(),re.M):
        slug=''.join(c for c in text.lower() if c.isalnum() or c in ' -_').replace(' ','-')
        n=counts[slug];counts[slug]+=1;result.add(slug if not n else f'{slug}-{n}')
    return result
for p in S.rglob('*.md'):
    text=re.sub(r'^```.*?^```[^\n]*','',p.read_text(),flags=re.M|re.S)
    text=re.sub(r'^(?: {4}|\t).*(?:\n|$)','',text,flags=re.M)
    text=re.sub(r'`[^`\n]+`','',text)
    for target in re.findall(r'(?<!\\)\[[^\]\n]+\]\(([^)]+)\)',text):
        parts=urlsplit(target.strip('<>'))
        if parts.scheme or parts.netloc:continue
        links+=1;dest=(p.parent/unquote(parts.path)).resolve() if parts.path else p
        if not dest.exists() or (parts.fragment and dest.suffix=='.md' and unquote(parts.fragment) not in slugs(dest)):broken.append([str(p.relative_to(S)),target])
check('markdown_links',not broken,checked=links,broken=broken,scope='Local relative links and anchors, excluding code; no external URL probes.')
math_errors=[]
for p in [S/'README.md',S/'VALIDATION.md']:
    text=re.sub(r'^```.*?^```[^\n]*','',p.read_text(),flags=re.M|re.S)
    if len(re.findall(r'(?<!\\)\$\$',text))%2 or len(re.findall(r'(?<![\\$])\$(?!\$)',text))%2:math_errors.append(p.name)
check('markdown_math_delimiters',not math_errors,discrepancies=math_errors,scope='Static delimiter check plus manual notation review; not a GitHub rendering execution.')
for p in (S/'scripts').glob('*.py'):
    try:ast.parse(p.read_text());ok=True
    except SyntaxError:ok=False
    check('python_syntax:'+p.name,ok)

preservation=load(EV/'workspace-preservation.json')
check('original_workspace_guard',preservation['original_workspace_files']==481 and not preservation['changed_or_missing'] and preservation['original_git_status_index_and_branch_unchanged'])
report={'passed':all(c['passed'] for c in checks),'checks':checks,'self_sha256':sha(Path(__file__)),'scope':'Source, evidence, numerical comparisons, admission bindings and documentation; no additional mathematical investigation.'}
print(json.dumps(report,indent=2));sys.exit(0 if report['passed'] else 1)
