# AUD-02 validation and reproduction

The admitted GR-07 scientific matrix reproduces, the complete existing Julia
tests pass, and all accepted Lean declarations compile and pass axiom audits.
**The three additional moment boundary cases fail their numerical criterion.**
They remain repair-required findings; this report does not declare every test
successful. No numerical algorithm, original manuscript or historical result
was edited to obtain these outcomes.

## Actual execution results

| Check | Result and scope | Evidence |
| --- | --- | --- |
| Read-only/cleanup preflight | Four mutation operations blocked; detached child removed with PID namespace | [preflight](evidence/runs/aud02-preflight-02.stdout.log) |
| Existing Julia suite | 669/669 assertions pass | [regression](evidence/runs/aud02-julia-regression-01.stdout.log) |
| GR-07 Julia suite | 7,941/7,941 assertions pass, including actual library control calls | [unit tests](evidence/runs/aud02-julia-unit-01.stdout.log) |
| Exact rational GR-04 probes | 1,134 words, 4,914 simplex comparisons, 18 ordered-vector checks, nine resolvents pass | [results](evidence/targeted/abstract.json) |
| New nonuniform interpolation oracle | 156 coefficient comparisons pass; largest scaled difference 4.311681156648209e-15 | [oracle and failures](evidence/targeted/independent_rows.json) |
| Generic moment boundary criterion | Three failures; acceptance command returns 1 | [failed acceptance](evidence/runs/aud02-boundary-acceptance-01.stdout.log) |
| Supplied final Python GR-02–05 diagnostics | All assertions pass; outputs preserved separately from originals | [GR-02](evidence/runs/aud02-python-gr02-01.stdout.log), [GR-03](evidence/runs/aud02-python-gr03-01.stdout.log), [GR-04](evidence/runs/aud02-python-gr04-01.stdout.log), [GR-05](evidence/runs/aud02-python-gr05-01.stdout.log) |
| Supplied final Python GR-06 diagnostic | 60 configurations pass; no convergence-rate assertion introduced | [GR-06](evidence/runs/aud02-python-gr06-01.stdout.log) |
| Full fresh reference and Julia matrix | 156 unique cases each; scaled residual maxima 4.3710194689557106e-13 / 4.1747833680964675e-13 | [data assessment](evidence/evidence-review.json) |
| Fresh Julia/Python norm comparison | All original tolerances pass; largest H1 difference 3.437441303821842e-14 | [comparison](evidence/runs/aud02-compare-fresh-01.stdout.log) |
| Fresh versus preserved norm fields | Zero differences for both Julia and Python tables; timing fields excluded | [Julia](evidence/runs/aud02-compare-julia-preserved-01.stdout.log), [Python](evidence/runs/aud02-compare-python-preserved-01.stdout.log) |
| Lean | Original 42 plus new 12 declarations compile; all 54 axiom records accepted | [catalogue](LEAN_CERTIFICATES.md), [machine inventory](evidence/lean-audit.json) |
| Historical performance assessment | 420 measured phase rows, 84 warmup phase rows, five distinct repeats per configuration/phase; measured compilation zero | [assessment](evidence/evidence-review.json) |
| Source/evidence preservation | 1,041 sealed files match in original GR-07 worktree and isolated copy; 481 original-workspace files also match their prior guard | [integrity](evidence/integrity.json), [workspace](evidence/workspace-preservation.json) |
| Markdown and notation | Relative paths, fragments, table column structure, fences and math delimiters checked | [documentation checks](evidence/documentation-checks.json) |

The integrity and documentation records summarize the final checks.
They are machine summaries, not replacements for the analytical
review. The original manuscript sources and PDFs were not revised or recompiled;
no LaTeX compilation is claimed for AUD-02. Exact source sections and line
locators were reviewed in full. There is no new mathematical LaTeX manuscript
whose compilation could certify the analytical conclusions.

## Environment and safeguards

Julia **1.12.6**, SpecialFunctions **2.9.0**, Python **3.13.16**, NumPy **2.3.5**,
SciPy **1.17.0**, mpmath **1.3.0** and SymPy **1.14.0** are the existing
versions. The Julia project/manifest and Lean/mathlib pins are unchanged.
Fresh environment records include binary/library/package-record hashes:
[Julia](evidence/runs/aud02-julia-environment-01.stdout.log),
[Python](evidence/runs/aud02-python-environment-01.stdout.log).
Lean uses 4.19.0 and the existing immutable mathlib revision listed in the
certificate catalogue. No new numerical dependency was installed or downloaded.
Existing host pypdf was used only to read primary papers, outside the numerical
dependency environment.

Scientific workloads used the existing serial bounded runner under the user's
explicit research-specific exception: one CPU affinity, one Julia/BLAS worker,
finite wall and per-process CPU/address-space limits, sampled descendant RSS,
bounded logs, process-group cleanup and checked PID-namespace teardown. The
filesystem visible to payloads was read-only except for fresh scratch. The
namespace fixture tested write/chmod/rename/unlink and a detached child.
**These safeguards do not provide strict aggregate cgroup resource isolation.**
Primary-source acquisition used separately authorized, finite-time curl calls;
it was not part of a numerical payload and acquired no dependencies.

Default Julia runs had 300-second wall / 240-second CPU deadlines, 8-GiB
per-process address-space limits and a 2-GiB sampled RSS threshold. The matrix
had 600/540-second deadlines. Python scientific runs used 2-GiB address-space /
1-GiB sampled RSS limits; shorter exact/acceptance jobs used smaller limits.
Lean runs used 120/90-second deadlines, 8-GiB address-space / 3.5-GiB sampled
RSS limits and `-j1`. Exact per-run limits, commands, source capsules, outputs,
hashes and cleanup records are in [evidence/runs/](evidence/runs/).
Every started scientific namespace was verified empty before another launch.

## Failures and unavailable checks

- A first prelaunch controller attempt computed the original workspace path
  one parent too high and stopped its integrity check **before launching a
  payload**. Correcting the path resolved the guard; the source snapshot and
  [prelaunch record](evidence/preflight/prelaunch-01.json) remain retained.
- New Lean attempt 01 failed from a missing ring-sum import. Attempt 03 failed
  from an incomplete tactic sequence. Final attempt 04 and the final axiom
  audit pass; all attempted source capsules and compiler outputs remain.
- The generic moment boundary acceptance fails as described in the implementation
  report. It is not converted into a passing criterion.
- `pdftotext` is unavailable. Existing pypdf extracted navigation text with font
  warnings on the first attempt; no parser or font package was installed.
- Restricted-shell DNS initially blocked one approved paper download; the
  authorized acquisition retry succeeded. CQ's publisher PDF returned HTTP
  403 at both official URLs. Some comparison full texts remain inaccessible;
  these are recorded in the literature inventory and are not treated as verified.
- No new benchmark, general PDE regularity experiment, asymptotic-rate proof,
  arbitrary-Hilbert Lean PDE proof or publication operation was performed.

The [run summary](evidence/run-summary.json) distinguishes successful commands
from the two failed compiler attempts and the failed boundary acceptance.
Retained GR-07 invalid/failed initial runs remain untouched and were not replayed
as evidence. No deadline, residual tolerance or scientific assertion was relaxed.

## Reproduction in the isolated review workspace

The source tree root for these commands is the isolated AUD-02 `workspace/`,
not the original development checkout. The existing controller locates the
sealed baseline and local runtime links. It will stop if an input hash changes.
No environment setup command below authorizes acquisition. On another machine,
first provision the exact dependencies through a separately approved process
and establish equivalent containment before executing scientific workloads.

The retained [replay_numerics.py](scripts/replay_numerics.py) is the exact
first-run orchestration used for the full diagnostic/matrix replay. It deliberately
refuses to overwrite its existing named evidence. For a new replay, choose fresh
labels through the controller, for example:

```bash
python3 -B - <<'PY'
import sys
sys.path.insert(0, 'research/legendre/aud02/scripts')
from execution import ROOT, REVIEW, STUDY, PYTHON, run, julia

run('repeat01-regression', julia(ROOT/'test/runtests.jl'),
    sources=[ROOT/'test/runtests.jl', ROOT/'Project.toml', ROOT/'Manifest.toml'])
run('repeat01-unit', julia(STUDY/'test/runtests.jl'),
    sources=[STUDY/'GR07.jl', STUDY/'test/runtests.jl',
             STUDY/'evidence/oracles/moments.csv'])
run('repeat01-abstract', [PYTHON, '-s', '-B', REVIEW/'scripts/abstract_probe.py'],
    wall=90, cpu=60, memory=1024, rss=512,
    sources=[REVIEW/'scripts/abstract_probe.py'])
PY
```

For each final supplied Python diagnostic, use the same `run` interface with
`PYTHON`, `-s`, `-B` and the path in
`studies/legendre/gr07/reference/reference_diagnostics/`. GR-04 and GR-05 also
import the unchanged `verify_gr03.py`. The full reference entrypoint is
`reference/benchmark_gr07.py /var/tmp/reference.csv`; the full Julia entrypoint
is `run.jl --output-dir=/var/tmp/results`. Outputs are available in the fresh
scratch path returned by `run`. Copy them to new evidence filenames, then run
the existing `scripts/compare.py reference.csv candidate.csv` through the
controller. Preserve all original tolerances and use new labels every time.

The new independent oracle requires the row exports from
`scripts/export_rows.jl /var/tmp/rows.csv /var/tmp/extremes.csv`; then run
`scripts/independent_rows.py rows.csv extremes.csv` in the pinned Python
environment. Its JSON contains both passing row checks and failing boundary
probes. `scripts/boundary_acceptance.py independent_rows.json` must currently
return 1. For recording that known failure, use `require_success=False`; do not
change its criterion.

To recompile certificates with fresh attempt identifiers:

```bash
python3 -B research/legendre/aud02/scripts/lean_check.py Aud02Finite repeat01
python3 -B research/legendre/aud02/scripts/lean_check.py Aud02Axioms repeat01
```

The helper uses unchanged pins and an existing package cache, compiles one
module at a time, copies only new local `.olean` outputs to the disposable
audit cache and records actual compiler status. The five earlier module names
and their three audit drivers are listed in the Lean catalogue. The cache is
disposable; compiler logs, source capsules and theorem statements are evidence.
No command here calls `lake update`, instantiates Julia or installs Python.
