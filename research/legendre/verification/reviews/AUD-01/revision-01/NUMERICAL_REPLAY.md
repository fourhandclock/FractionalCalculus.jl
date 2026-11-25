# Numerical replay

**All four identified original diagnostics pass unchanged** in the isolated pinned environment. An existing independent 10-test regression suite also passes. The [source inventory](DIAGNOSTIC_INVENTORY.md) identifies ten other referenced originals that remain unavailable; their historical results are not counted as replayed.

## Results

| Program | Scope | Result |
| --- | --- | --- |
| `check_exact_aud01.py` | Symbol numerator, rational inequalities, finite sums for N=2…20 | Pass; stdout matches the supplied text exactly |
| `verify_aud01_homogeneous.py` | L1/L1-2, six grids through N=4096 | 12 configurations pass |
| `verify_l12_stability.py` | Original ST-03 collected/increment recurrences | 432 parameter cases pass; maximum representation difference 3.77e-15 |
| `verify_time_variable_kernel_st04.py` | Original ST-04 kernel; both schemes and both memory rules | 24 configurations pass; remains a numerical candidate |
| `check_counterexamples.py` | Existing independent VQ/CF/history/GLL regressions | 10 tests pass; not an original-companion recovery |

## Homogeneous observations

| N=4096 | L1 | L1-2 |
| --- | --- | --- |
| Maximum scalar error | 5.0190267128e-06 | 4.8350130274e-06 |
| Last-doubling rate | 0.7498 | 0.7498 |
| Normalized signed total residual | -5.2010746803e-04 | -1.0051543624e-04 |
| Normalized memory residual | 3.8361747868e-05 | 3.8361747868e-05 |

The observed exponent is **approximately 0.75**, not 0.5. The total signed residual is negative on these grids, although its memory component is positive. These observations are compatible with an initial-layer contribution still dominating the tested range. They do not establish the sign or exponent in the asymptotic limit. The standalone half-order result is analytical and uses fixed-parameter limiting arguments; the program contains no assertion requiring the half-order regime to have been reached.

The maximum reference-equation check printed by the program is `2.422e-15`. Across the 12 cases, the maximum direct/error-recurrence difference is `1.415e-13` and maximum scaled full-row residual is `8.259e-16`. These floating-point checks are not interval enclosures.

## Acceptance criteria and discrepancies

The supplied homogeneous program retains `oracle < 2e-12`, sampled reference positivity above `2/3`, `direct_vs_error < 2e-11`, `max_scaled_row < 2e-12`, and `E + 2e-11 >= lower`. It does not add a rate target. The original symbolic assertions are exact SymPy/Fraction comparisons. [The criteria inventory](acceptance-criteria.json) records every actual assertion and the existing unittest checks; [run records](numerical-replay.json) bind unchanged source hashes to captured outputs.

The symbolic stdout is byte-identical to its historical counterpart. The homogeneous output differs in **25 printed fields**, with maximum printed error difference approximately **1e-16**. Roundoff-sized recurrence/residual differences are also retained in the [field-by-field comparison](replay-comparison.json). This comparison uses printed values, not historical full-precision arrays. The original platform/BLAS details are insufficient to assign a unique cause. No tolerance was introduced or relaxed to obtain agreement, and no historical output was rewritten.

## Environment and execution

The workspace-local virtual environment uses CPython 3.13.16, NumPy 2.3.5, SciPy 1.17.0, mpmath 1.3.0, and SymPy 1.14.0. [Environment metadata](python-environment.json) records installed distributions and RECORD hashes; [requirements.txt](requirements.txt) fixes the four research dependencies. Global Python, Julia dependencies, and the pinned Lean project are unchanged. Network access was used only for the approved Python packages.

Runs were serial, with one CPU affinity and BLAS/OpenMP thread. The symbolic run had a 90 s wall/60 s CPU deadline, 1 GiB per-process address-space limit and 768 MiB sampled RSS ceiling. The homogeneous run had 180 s/120 s, 2 GiB address space and 1 GiB sampled RSS. The ST-03, ST-04 and supplementary limits are retained in their JSON records. The inspected programs write stdout/stderr; source preservation is monitored by hashes. Process-group cleanup and per-process/sampled controls are not cgroup aggregate isolation.

No numerical assertion failed. The dependency installation completed within its 240 s deadline. Separately, manuscript builds retain an initial missing-font failure and an output-directory setup failure, as well as the successful offline builds. No fonts were downloaded.

## Reproduction

Run from the repository root with a fresh local environment and new evidence labels. The installed environment used here is `.checkpoint-tools/aud01-close-2026-11-25/venv`. For a new checkout, create an isolated venv and install the exact requirements before invoking the programs:

```bash
python3 -m venv .checkpoint-tools/aud01-replay-venv
.checkpoint-tools/aud01-replay-venv/bin/python -m pip --isolated install --only-binary=:all: -r research/legendre/verification/reviews/AUD-01/revision-01/requirements.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 .checkpoint-tools/aud01-replay-venv/bin/python -I -B AUD01_review_package/aud01/check_exact_aud01.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 .checkpoint-tools/aud01-replay-venv/bin/python -I -B AUD01_review_package/aud01/verify_aud01_homogeneous.py
```

For bounded retained runs, use [the existing runner](../../../scripts/run_bounded.py), a new `--label`, explicit `--timeout`, `--cpu-seconds`, `--memory-mib`, `--resident-mib`, `--source`, and a new `--evidence` directory. The exact recorded commands and complete stdout/stderr are in `results/`; replay does not require changing source code or expected results.
