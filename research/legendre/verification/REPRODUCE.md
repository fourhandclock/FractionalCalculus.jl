# Reproduce the audited Legendre checkpoint

The current checkpoint is **AUD-01 revision 01, ACCEPT WITH LIMITATIONS**. Start with the [mathematical overview](README.md) and [clean-tree validation report](results/checkpoint-aud01/VALIDATION.md). Commands below are run serially from the repository root unless another directory is specified. Table and figure generators are separate experiments: use a new output directory to preserve their historical data.

## Environments and setup

The replay uses Julia **1.12.6** with the committed root project/manifest; CPython **3.13.16**, NumPy **2.3.5**, SciPy **1.17.0**, mpmath **1.3.0**, SymPy **1.14.0**; Lean **4.19.0** with mathlib **v4.19.0**, immutable revision `c44e0c8ee63ca166450922a373c7409c5d26b00b`; and Tectonic **0.15.0**. [The requirements](reviews/AUD-01/revision-01/requirements.txt), [review environment](reviews/AUD-01/revision-01/python-environment.json), and [integration environment](results/checkpoint-aud01/environment.json) record the exact identities.

Tools, virtual environments, depots, caches and rebuilt objects belong in ignored `.checkpoint-tools/` or `lean/.lake/`. Use existing compatible installations, or provision these exact versions as a separate setup step. Dependency acquisition requires network access and approval where applicable; the integration itself reused cached tools and acquired no additional dependencies. Never run `lake update` or resolve Julia dependencies merely to replay these checks.

A fresh Python environment can be prepared, after dependency acquisition is authorized, with:

```bash
python3 -m venv .checkpoint-tools/python-aud01
.checkpoint-tools/python-aud01/bin/python -m pip --isolated install --only-binary=:all: \
  -r research/legendre/verification/reviews/AUD-01/revision-01/requirements.txt
```

The original ST-04 Python requirement and validation environment remain historical; their NumPy pin differs from this explicitly recorded replay. Do not silently substitute one environment for the other.

## Julia

With Julia and the pinned dependencies already available:

```bash
JULIA_PKG_OFFLINE=true JULIA_NUM_THREADS=1 JULIA_NUM_PRECOMPILE_TASKS=1 \
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  julia --startup-file=no --project=. test/runtests.jl
```

The clean branch's root runner discovers the Legendre study. Its **669 assertions** include `proof_audit.jl`: actual library Caputo/history rows, GLL operators, and the ST-04 printed-rule scalar reduction for both derivative schemes. The audit is included once by the study runner; a separate second execution is unnecessary. No table/figure generator runs during validation, and no saved numerical results are rewritten.

The numerical implementation follows quadratic interpolation where the printed L1–2 collection disagrees, retains L1 startup and the printed Volterra quadrature, and preserves the published error-normalization conventions. [The implementation audit](ST04_PROVENANCE.md#implementation-inspected-before-release) describes these choices. This checkpoint changes none of those algorithms.

## Python

Use the isolated four-dependency environment above. Set `OPENBLAS_NUM_THREADS=1` and `OMP_NUM_THREADS=1`, then execute these commands one at a time:

```bash
.checkpoint-tools/python-aud01/bin/python -I -B AUD01_review_package/aud01/check_exact_aud01.py
.checkpoint-tools/python-aud01/bin/python -I -B AUD01_review_package/aud01/verify_aud01_homogeneous.py
.checkpoint-tools/python-aud01/bin/python -I -B research/legendre/verification/scripts/verify_l12_stability.py
.checkpoint-tools/python-aud01/bin/python -I -B research/legendre/verification/scripts/verify_time_variable_kernel_st04.py
PYTHONNOUSERSITE=1 .checkpoint-tools/python-aud01/bin/python -s -B research/legendre/verification/scripts/check_counterexamples.py
```

The first four are identified original diagnostics. They cover exact identities, 12 homogeneous configurations, 432 ST-03 cases and 24 ST-04 configurations. The final program is a later independent 10-test suite, not a recovered original companion. The [criteria inventory](reviews/AUD-01/revision-01/acceptance-criteria.json) preserves the actual assertions and tolerances. No rate of 0.5 is required: the homogeneous observed last-doubling rate is 0.7498 for both methods. Its asymptotic half-order conclusion is analytical, not established by these grids.

The [diagnostic inventory](reviews/AUD-01/revision-01/DIAGNOSTIC_INVENTORY.md) identifies ten unavailable or unauthenticated original groups. Their historical results are not counted as replayed. Original supplied output, revision-01 replay output, and integration output remain separate.

## Lean

Reuse the pinned project in `research/legendre/verification/lean/` with its exact dependency sources and precompiled mathlib cache. This integration does not download them. On another checkout, the existing [source helper](scripts/fetch_lean_sources.py) and cache tooling can provision the committed revisions after acquisition is authorized; do not build all of mathlib or refresh its history.

From the Lean project directory, compile these modules serially:

```bash
mkdir -p .lake/build/lib/lean
LEAN_NUM_THREADS=1 lake env lean -j1 -o .lake/build/lib/lean/Coefficients.olean Coefficients.lean
LEAN_NUM_THREADS=1 lake env lean -j1 -o .lake/build/lib/lean/Quadrature.olean Quadrature.lean
LEAN_NUM_THREADS=1 lake env lean -j1 -o .lake/build/lib/lean/AuditConstants.olean AuditConstants.lean
LEAN_NUM_THREADS=1 lake env lean -j1 -o .lake/build/lib/lean/Aud01FiniteSums.olean Aud01FiniteSums.lean
LEAN_NUM_THREADS=1 lake env lean -j1 -o .lake/build/lib/lean/Aud01Oscillator.olean Aud01Oscillator.lean
LEAN_NUM_THREADS=1 lake env lean -j1 \
  --root=../reviews/AUD-01/revision-01 \
  ../reviews/AUD-01/revision-01/ConsolidateCertificates.lean
```

The last command checks all 42 names and prints every axiom dependency. Accepted dependencies are `propext`, `Classical.choice`, and `Quot.sound`; incomplete proofs and unsupported axioms are not accepted. [The catalogue](lean/README.md) explains the 41-group counting convention and the finite statements covered. The full PDE stability/convergence arguments remain analytical.

## LaTeX

The current mathematical authority is the accepted revision source, preserved unchanged during integration. From the repository root:

```bash
mkdir -p .checkpoint-tools/latex-build-aud01
tectonic --untrusted --only-cached --keep-logs --keep-intermediates \
  --outdir .checkpoint-tools/latex-build-aud01 \
  research/legendre/verification/reviews/AUD-01/revision-01/mathematical-verification-aud01-r1.tex
```

This offline command requires an already populated font/package cache; missing assets are an explicit build failure, not permission to download. The accepted source includes its documented cached-font sizing convention. The current build has 37 pages; inspect the log for missing references, undefined commands and box warnings. Earlier ST-04 source/PDF and all supplied AUD-01 versions remain unchanged.

## Bounded execution and integrity

The existing [runner](scripts/run_bounded.py) preserves commands, source snapshots, stdout/stderr, environment, resource limits and exit status. Give each new attempt a new label and evidence directory; it refuses to overwrite an existing record. For example:

```bash
python3 -B research/legendre/verification/scripts/run_bounded.py \
  --label aud01-exact-new --timeout 90 --cpu-seconds 60 \
  --memory-mib 1024 --resident-mib 768 --evidence .checkpoint-tools/replay-evidence \
  --source AUD01_review_package/aud01/check_exact_aud01.py \
  -- .checkpoint-tools/python-aud01/bin/python -I -B AUD01_review_package/aud01/check_exact_aud01.py
```

Run one expensive workload at a time. Recorded safeguards are single CPU affinity/thread, finite wall and CPU deadlines, per-process address-space and file-size limits, bounded logs, sampled descendant RSS and process-group cleanup. They are not cgroup aggregate isolation. Inspect workloads before execution; retained sources and historical evidence are inputs, not output destinations.

The [integrated integrity checker](scripts/check_aud01_checkpoint.py) checks protected algorithms, historical sources/results, fresh run hashes, formal-certificate bindings and local Markdown links:

```bash
python3 -B research/legendre/verification/scripts/check_aud01_checkpoint.py
```

The earlier revision-01 `validate_checkpoint.py` records a different scope: all 294 files of the original development workspace, including unrelated local work and a then-missing ST-04 PDF. Its unchanged historical output is retained; it is not a clean-checkout acceptance test. The clean branch preserves the ST-04 PDF from Git, excludes unrelated work, and checks those differences explicitly rather than altering historical expectations.
