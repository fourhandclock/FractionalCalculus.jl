# Reproduce the checkpoint

Run from a clean checkout of the research verification branch. This checkpoint's numerical target is the Legendre study; unrelated uncommitted metric-graph work in the originating workspace is not part of the release. The exact library/project snapshot used for validation is described in [CHECKPOINT_SCOPE.md](CHECKPOINT_SCOPE.md).

## Reference environment

Julia 1.12.6, CPython 3.13.16 with NumPy 2.2.6, Lean 4.19.0, matching mathlib v4.19.0 at `c44e0c8ee63ca166450922a373c7409c5d26b00b`, and Tectonic 0.15.0. Exact binary/source identifiers, commands, limits, outputs, and any failed attempts are retained under `results/checkpoint-st04/`. The Lean dependency manifest locks transitive revisions. The Python diagnostic uses only NumPy plus the standard library; the other independent checks need only the standard library.

Tools and caches in the originating workspace were placed in the ignored `.checkpoint-tools/` directory. They are not included in the branch. Another researcher may use their own local installations of the pinned versions. Toolchain acquisition and registry/cache access need network access; numerical/proof validation after setup can run offline.

## Julia

Use an isolated depot if desired and instantiate the existing root project without changing dependency versions:

```bash
JULIA_NUM_THREADS=1 JULIA_NUM_PRECOMPILE_TASKS=1 OPENBLAS_NUM_THREADS=1 \
  julia --startup-file=no --project=. \
  -e 'using Pkg; Pkg.instantiate(;allow_autoprecomp=false)'

JULIA_NUM_THREADS=1 JULIA_NUM_PRECOMPILE_TASKS=1 OPENBLAS_NUM_THREADS=1 \
  julia --startup-file=no --project=. studies/legendre/test/runtests.jl
```

The suite includes `proof_audit.jl`; it tests actual package coefficients, historical-state collection, GLL weights, and an ST-04 scalar reduction using the actual Caputo and memory matrices. Its ST-04 subset is N=128 with the printed memory rule for both derivative formulas, compared with supplied rounded amplitudes at absolute tolerance 5e-8. It checks the full discrete residual vector at tolerance 5e-10. This complements the standalone Python refinement study and does not implement product integration in the production library.

The original 645 assertions plus the 24 audit assertions pass in the reference run: **669 total**. Do not run the table or figure generators to validate this checkpoint; their default destinations contain historical results. No numerical table target, error norm, source problem, or result file was adjusted to achieve a pass.

## Python

Install the pinned NumPy requirement into a local environment, then run:

```bash
python3 -B research/legendre/verification/scripts/check_counterexamples.py
python3 -B research/legendre/verification/scripts/verify_l12_stability.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  python3 -B research/legendre/verification/scripts/verify_time_variable_kernel_st04.py
```

The first command runs 10 tests covering VQ-01, CF-02, signed-history reductions, and the exact-rational GLL example. Its numerical domain/tolerances are retained in the historical [test plan](results/TEST_PLAN.md). It uses analytical panel moments, not the missing original CF-02 integration oracle.

ST-03 checks 432 parameter combinations with a fixed representation tolerance 2e-11. The supplied source is unchanged. ST-04 checks 24 configurations: L1/L1-2, printed quadrature/product-integration control, and six N values through 4096. It asserts finite trajectories, sampled residual <5e-10, and weighted peaks >2 for N≥1024. These are finite-grid tests, not an all-fine-grid contractivity refutation. The original source uses six sampled residual levels; do not report them as an exhaustive residual test. Its optional `solve` arguments are not a validated general-parameter interface in this checkpoint.

## Lean

First, from the repository root, populate the exact committed dependency
revisions without refreshing full repository history:

```bash
python3 -B research/legendre/verification/scripts/fetch_lean_sources.py
```

Then from `research/legendre/verification/lean/`, with the matching toolchain:

```bash
LEAN_NUM_THREADS=1 lake exe cache get \
  Mathlib.Analysis.SpecialFunctions.Pow.Real \
  Mathlib.Analysis.SpecialFunctions.Integrals \
  Mathlib.Analysis.Normed.Group.Basic \
  Mathlib.Tactic.FieldSimp Mathlib.Tactic.Linarith \
  Mathlib.Tactic.NormNum Mathlib.Tactic.Positivity Mathlib.Tactic.Ring
mkdir -p .lake/build/lib/lean
LEAN_NUM_THREADS=1 lake env lean -j1 -o .lake/build/lib/lean/Coefficients.olean Coefficients.lean
LEAN_NUM_THREADS=1 lake env lean -j1 CoefficientsAxioms.lean
LEAN_NUM_THREADS=1 lake env lean -j1 -o .lake/build/lib/lean/Quadrature.olean Quadrature.lean
LEAN_NUM_THREADS=1 lake env lean -j1 QuadratureAxioms.lean
```

Use the committed dependency manifest; the explicit mathlib source revision is immutable. It was constructed from that revision's own transitive lockfile and checked by Lake. The shallow setup helper refuses to change an existing checkout at another revision. `lake update` is not needed for replay and can fetch full mathlib history; two bounded attempts at that operation exceeded the file-size budget during setup and are preserved as failures. The cache command fetches only the listed modules and their imports. The four final commands compile the two local modules against those caches and print every theorem's trusted-axiom dependencies. It does not ask Lake to rebuild the entire library. If a cache is missing, resolve that missing dependency rather than launching an unrestricted full mathlib build. A source file or a draft is not a proof certificate until compilation and the axiom audit succeed. Run these commands serially: the reference bounded runs used 8 GiB per-process virtual-address limits, 120 s wall / 90 s CPU deadlines, and sampled descendant RSS ceilings of 2.25 GiB for the algebra module and 3.5 GiB for the integral module. Shared mappings can be counted more than once. Do not use Lean’s `-M` flag in this pinned setup: diagnostic attempts ended in memory exceptions or an unknown `max_memory` option; the successful runs used the external limits instead. See `lean/README.md` for the exact statements and current compilation status.

## LaTeX

The main TeX file is identical to the supplied original ST-04 source. From this verification directory:

```bash
mkdir -p results/latex-build
tectonic --untrusted --keep-logs --keep-intermediates --print \
  --outdir results/latex-build mathematical-verification.tex
```

Tectonic automatically repeats passes to resolve references. Alternatively use two ordinary `pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error` passes with the same output directory. Check the final log and rendered pages; static syntax checks cannot certify layout. Build products remain ignored. The supplied PDF is an input, not a substituted claim that this TeX source was compiled here.

## Limits and evidence

`scripts/run_bounded.py` records new stdout/stderr files, command, source hashes, environment settings, return code, elapsed time, and limits. Use a new label per attempt; it refuses to overwrite existing evidence. Example:

```bash
python3 -B research/legendre/verification/scripts/run_bounded.py \
  --label python-st03-new --timeout 60 --cpu-seconds 45 --memory-mib 256 \
  --source research/legendre/verification/scripts/verify_l12_stability.py \
  -- python3 -B research/legendre/verification/scripts/verify_l12_stability.py
```

Runs inherit one CPU affinity and explicit single-thread settings. The wrapper uses finite wall/CPU deadlines, per-process virtual-address-space and per-file size limits, log-size monitoring, optional sampled descendant RSS limits, and process-group cleanup. These limits are resource-conscious local safeguards, not cgroup aggregate isolation or protection against deliberately detaching workloads. Run only inspected commands and keep expensive builds serial. Numerical inputs and retained source/evidence are not writable outputs of the scripts.

Raw failures and setup attempts are preserved. Public evidence may normalize local path prefixes, with raw hashes and original local copies explicitly recorded. Such normalization changes no numerical values, statements, or failure text. Never replace old stdout, loosen a tolerance to fit a failure, or describe the supplied historical output as a fresh run.
