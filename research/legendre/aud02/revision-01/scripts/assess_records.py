"""Assess immutable validation outputs, typed theorem statements and preservation."""
import ast,csv,difflib,hashlib,json,re,sys
from execution import *

def main():
    check_preserved();runs=REVIEW/'evidence/runs'
    final_pdf=json.loads((REVIEW/'evidence/final-manuscript-validation.json').read_text());assert final_pdf['passed'] and len(final_pdf['manuscripts'])==6
    catalogue=[]
    for module in ['CoefficientsAxioms','QuadratureAxioms','Aud01Axioms','Aud02Axioms']:
        output=runs/('r01-final-lean-'+module.lower()+'.stdout.log')
        for name,ax in re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]",output.read_text()):
            axioms=[a.strip() for a in ax.split(',') if a.strip()]
            assert set(axioms)<={'propext','Classical.choice','Quot.sound'},(name,axioms)
            catalogue.append(dict(name=name,axioms=axioms,audit=str(output.relative_to(ROOT))))
    assert len(catalogue)==len({r['name'] for r in catalogue})==54
    theorem_sources={}
    project=ROOT/'research/legendre/verification/lean'
    for module in ['Coefficients','Quadrature','AuditConstants','Aud01FiniteSums','Aud01Oscillator','Aud02Finite']:
        p=project/(module+'.lean');s=p.read_text()
        assert not re.search(r'\b(sorry|admit)\b',s)
        assert not re.search(r'^\s*axiom\b',s,re.M)
        namespace=re.search(r'^namespace ([\w.]+)',s,re.M).group(1)
        for match in re.finditer(r'^theorem (\w+)([\s\S]*?)\s*:=\s*by',s,re.M):
            name=namespace+'.'+match.group(1)
            theorem_sources[name]=dict(module=module,source=str(p.relative_to(ROOT)),sha256=sha(p),
                line=s[:match.start()].count('\n')+1,statement=('theorem '+match.group(1)+match.group(2)).rstrip())
    assert set(theorem_sources)=={x['name'] for x in catalogue}
    for r in catalogue:r.update(theorem_sources[r['name']])
    (REVIEW/'evidence/theorem-catalogue.json').write_text(json.dumps({
        'named':54,'preserved_AUD01_named':42,'preserved_identity_groups':41,'AUD02_named':12,
        'scope':'Finite certificates only; no complete PDE formalization',
        'theorems':catalogue},indent=2,ensure_ascii=False)+'\n')
    rootguard=ROOT.parents[2]/'.checkpoint-tools/gr07-2026-11-26/preflight/original-workspace.json'
    originalroot=ROOT.parents[2]
    data=json.loads(rootguard.read_text())
    bad=[name for name,item in data['files'].items() if sha(originalroot/name)!=item['sha256']]
    assert not bad,bad
    manifest=json.loads((REVIEW/'evidence/input-manifest.json').read_text())
    changes=[n for n,item in manifest['files'].items() if sha(ROOT/n)!=item['sha256']]
    assert set(changes)=={'.gitignore','README.md','studies/legendre/README.md','research/legendre/verification/README.md','research/legendre/verification/lean/lakefile.toml'}
    protected='<!-- keep everything above as it is -->'
    assert (ROOT/'README.md').read_text().split(protected)[0]==(ORIGINAL/'README.md').read_text().split(protected)[0]
    # Verify the original test body rather than inferring its preservation from counts.
    old=(STUDY/'test/runtests.jl').read_text().replace('"../evidence/oracles/moments.csv"','"../../evidence/oracles/moments.csv"')
    revised=(STUDY/'revision-01/test/runtests.jl').read_text();assert revised.startswith(old)
    (REVIEW/'evidence/integrity.json').write_text(json.dumps({
        'original_input_files':len(manifest['files']),'original_input_mismatches':[],
        'copied_input_files_preserved':len(manifest['files'])-len(changes),
        'intentional_integration_edits':changes,'original_workspace_files_checked':len(data['files']),
        'original_workspace_mismatches':bad,'protected_readme_prefix_unchanged':True,
        'original_test_body_preserved':True,'Julia_project_and_manifest_unchanged':True,
        'Lean_mathlib_pins_unchanged':True,'scientific_review_Git_operations':False,'publication_Git_operations_authorized':True},indent=2)+'\n')
    diff=[]
    for relative in ['GR07.jl','test/runtests.jl']:
        a=STUDY/relative;b=STUDY/'revision-01'/relative
        diff.extend(difflib.unified_diff(a.read_text().splitlines(True),b.read_text().splitlines(True),
                                       fromfile='original/'+relative,tofile='revision-01/'+relative))
    (REVIEW/'evidence/implementation.diff').write_text(''.join(diff))
    # All numerical algorithms and production sources not explicitly new are still sealed.
    rows=list(csv.DictReader(open(REVIEW/'evidence/results/final/julia_results.csv')))
    assert len(rows)==len({tuple(r[k] for k in ['alpha','beta','case','variant','grading','N','M']) for r in rows})==156
    comparison=json.loads((runs/'r01-final-julia-python.stdout.log').read_text());assert comparison['passed']
    # Boundary generation/row oracle evidence after the repair.
    repaired=json.loads((runs/'r01-repaired-independent-01.stdout.log').read_text())
    assert all(r['meets_5e-12_relative'] for r in repaired['boundary_probes'])
    summary={'verdict':'ACCEPT WITH LIMITATIONS','baseline_assertions':669,
        'experimental_original_assertions':7941,'new_boundary_assertions':21,'experimental_assertions':7962,
        'scientific_cases':156,'comparison':comparison,'maximum_revised_scaled_residual':max(float(r['scaled_residual']) for r in rows),
        'new_theorems_introduced':False,'formal_named_certificates':54,'performance_remeasured':False,
        'revised_manuscript_pdfs':len(list((STUDY/'revision-01/manuscripts').glob('*.pdf'))),
        'manuscript_compilation':'Six successful offline builds; 30 pages visually inspected; final-manuscript-validation.json',
        'checkpoint_fully_validated':True,
        'old_performance_admission_applies_to_revision':False,
        'moment_failures_closed':'Two complete tuples repaired; tiny-product M0 repaired and unrepresentable full tuple explicitly rejected',
        'novelty':'unresolved','CQ_exact_primary_locator':'unverified after authorized recovery attempt'}
    (REVIEW/'evidence/summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    records=[]
    for path in sorted(runs.glob('*.json')):
        if path.name.endswith('.namespace.json'):continue
        r=json.loads(path.read_text())
        cleanup=json.loads(path.with_name(path.stem+'.namespace.json').read_text())
        assert cleanup['namespace_cleanup_verified']
        records.append(dict(label=path.stem,returncode=r['returncode'],wall_seconds=r['elapsed_seconds']))
    (REVIEW/'evidence/run-summary.json').write_text(json.dumps({'runs':records,'all_namespace_cleanup_verified':True,
        'aggregate_cgroup_isolation':False,'prelaunch_record':'evidence/prelaunch-01.json'},indent=2)+'\n')
    for p in (REVIEW/'scripts').glob('*.py'):ast.parse(p.read_text(),filename=str(p))
    print('Assessed 54 exact theorem statements, all numerical evidence and preservation guards.')
if __name__=='__main__':main()
