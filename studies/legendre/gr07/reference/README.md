# GR-07 independent reference checkpoint

Status: reference experiments complete; actual-library Julia implementation and validation pending. No repository mutations. GR-01–06 remain proposed theory pending AUD-02. The reference base is `bf43fd0e78bcbcaae94d4c95fd9e43fd562ba477` on `research/legendre-verification-aud01`; at inspection it was one commit ahead of main, zero behind. See the repository's `src/TimeDiscretization.jl`, `src/Legendre.jl`, `src/Solver.jl` and `studies/legendre/README.md`. The Python controls reconstruct interpolation-defined L1/L1-2 and the printed memory rule; they are **not executions of the actual Julia baseline**.

## Reference experiments

T=1; lambda=.4; x in (-1,1), homogeneous Dirichlet; u(x,t)=cos(pi*x/2) times t^2 (smooth) or 1+t^alpha (singular); K=(1+.3*x)*(1+.2*sin(t)); exact consistent forcing evaluated at endpoints or shifted points as required. All five variants use the same GLL basis, consistent stiffness and Ritz initial approximation, with independent Gauss quadrature for continuous H1 errors. The uniform reference comparison uses N=32,64,128,256, M=14, (alpha,beta)=(.5,.25),(.75,.5),(.9,.8). Both proposed variants additionally use grading 2/alpha on the singular problem. Twelve separate graded spatial cases at alpha=.75,beta=.5,N=256,M=3,5,7,9,12,16 complete the 156 cases.

`benchmark_gr07.py` imports the unchanged GR-06 diagnostic's assembly routine for Alikhanov/PI. Its endpoint adapter integrates the original local interpolants and reconstructs the literal memory rule. All memory weights are normalized for I^(1-beta), with Gamma(1-beta) applied once in the equation. The original library uses unnormalized memory weights; normalize carefully in comparisons. A separate integration check evaluates 96 endpoint derivative rows by polynomial fitting and independent quadrature with the singularity removed by substitution. All 156 final configurations passed derivative/memory checks and scaled residual assertions (maximum 4.371e-13). Rates are diagnostic, not asserted or treated as proof. Independent Gauss error integration is numerical, not a rigorous bound.

`results.csv` is the corrected output. `invalid_initial_results.csv`, `invalid_initial_execution.log`, and `benchmark_gr07_initial.py` are retained as INVALID: the first endpoint L1-2 adapter omitted a factor of the panel length in the backward-quadratic correction, so its L1-2 comparisons must not be used. A self-consistent equation residual did not catch this; the corrected adapter has the independent direct-integration test. No earlier supplied reference script was modified. The reported 156 runs exclude the invalid attempt. No rate threshold was relaxed.

`timing_repeats.csv` records five warm repeated Python assembly/solve measurements per selected variant, following one warmup. Timings exclude spatial assembly, residual checking and error evaluation; they are not Julia performance or end-to-end runtime. Dense time weight and solution-history sizes are exact NumPy array byte counts, not peak memory. `benchmark_timings.py` recreates the timing experiment design; timings vary. `environment.txt` records the execution environment.

## Reproduce

In a fresh directory with this code and no existing output files, using the recorded dependencies:

```
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -B benchmark_gr07.py results.csv
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -B benchmark_timings.py
```

The scripts refuse to overwrite existing CSV results. Use bounded serial execution and no unapproved dependency changes. The `theory/` directory contains the six original GR manuscripts and their source files. `reference_diagnostics/` retains the original prior diagnostic sources and results, including their failed attempts. Do not treat historical outputs as a fresh replay. See `GR07_JULIA_HANDOFF.md` for the remaining local work.
