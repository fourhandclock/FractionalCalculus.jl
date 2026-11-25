# GR-07 implementation and validation

**Verdict: ACCEPT WITH LIMITATIONS.** The separate Julia implementation reproduces the corrected independent reference and passes the declared finite correctness gates. The performance measurements apply to the recorded implementations and workloads. GR-01–06 remain proposed mathematics for AUD-02; passing GR-07 does not audit or formally certify those theorems.

## Implementation and mathematical verification

[GR07.jl](GR07.jl) implements shifted Alikhanov–PI-L and Alikhanov–PI-Q on uniform and nondecreasing-step graded grids. The derivative is assembled as an increment matrix; memory is assembled as the normalized fractional integral. The full equation applies Gamma(1-beta) exactly once. The shifted derivative, diffusion average, nodal coefficient and forcing use the same evaluation point. Completed quadratic panels use forward stencils with actual adjacent step ratios; the last memory panel uses a backward quadratic, with linear startup. The exact final local ratio sigma avoids cancellation on graded grids.

The spatial operators reuse actual library GLL mass/stiffness. Initial data use a derivative Ritz projection. The initial memory column and all derivative/diffusion history terms remain in the solve. The three endpoint controls use actual library derivative weights; printed-memory controls also call the actual library memory routine. Small-grid tests compare their evolution directly with `solve_tfide` under matching Ritz values. Endpoint PI-L remains a separate control, rather than a modification of production dispatch.

Local moments are checked against independent transformed quadrature at 120/180 decimal digits. This includes h as small as 1e-30 and d as large as 1e24, near-singular exponents, final panels and the centered correction separately. Generic Lagrange-basis quadrature independently checks assembled rows on uniform/graded meshes; uniform closed forms, exact polynomials, signed PI-Q weights, startup and complementary/energy/tail properties have separate tests. No new global proof or formal certificate is inferred from them.

## Actual validation results

| Check | Result and evidence |
| --- | --- |
| Complete AUD-01 root regression, baseline | **669/669 pass**; [output](evidence/runs/baseline-regression-01.stdout.log) |
| Experimental Julia suite | **7,941 assertions pass**; [output](evidence/runs/julia-unit-02.stdout.log), [exact sources and command](evidence/runs/julia-unit-02.json) |
| Independent local moment oracle | 24 panels / 96 polynomial integrals pass; [output](evidence/runs/local-oracle-02.stdout.log) |
| Supplied GR-02–06 Python diagnostics | All original final-script assertions pass; [GR-02](evidence/runs/python-gr02-01.stdout.log), [GR-03](evidence/runs/python-gr03-01.stdout.log), [GR-04](evidence/runs/python-gr04-01.stdout.log), [GR-05](evidence/runs/python-gr05-01.stdout.log), [GR-06](evidence/runs/python-gr06-01.stdout.log) |
| Corrected Python reference | **156 cases pass** plus 96 independent endpoint derivative-row checks; [output](evidence/runs/python-reference-01.stdout.log), [fresh-versus-supplied comparison](results/reference_replay_comparison.json) |
| Julia scientific matrix | **156 cases pass**; maximum full-row scaled residual **4.175e-13**; [CSV](results/julia_results.csv), [run record](evidence/runs/julia-matrix-01.json) |
| Rowwise Julia/Python comparison | All cases pass the predeclared 5e-11 + 2e-6 relative norm budget; maximum H1 norm difference **3.44e-14**; [comparison](results/julia_reference_comparison.json) |
| Complete AUD-01 root regression, final | **669/669 pass**; [output](evidence/runs/final-regression-01.stdout.log) |
| Controlled Julia performance | **21 warmup solves + 105 measured solves**, five repeats per configuration, four phase records each; [raw samples](results/timing_repeats.csv), [warmups](results/warmups.csv), [run record](evidence/runs/julia-performance-01.json) |
| Fresh reproduction entry point | `reproduce.py --run-id replay-check` passes the complete correctness pipeline in separate outputs; [replayed comparison](results/replay-check/julia_reference_comparison.json), [fresh admissions](evidence/replays/replay-check/admission/candidate.json) |

The regression count describes the entire selected AUD-01 branch, which contains the Legendre study. Uncommitted metric-graph development belongs to the untouched original workspace and was not imported into this baseline. The earlier 7,925-assertion unit run is retained; the final run adds the planned quadrature-refinement checks and a continuous polynomial representation for the production-control Ritz initial values.

The [summary JSON](results/summary.json) records counts, residuals, scope and limitations. [Integrity checks](evidence/integrity.json) cover source/evidence identities, admissions, local links and figure data. A fresh replay checks reproducibility; it does not double the number of distinct scientific configurations.

## Finite-grid numerical findings

For smooth solutions, the Alikhanov last-doubling H1 rates range from approximately **2.000 to 2.009** across the tested orders and memory rules. The singular graded rates are:

| alpha, beta | Grading | PI-L, 128→256 | PI-Q, 128→256 |
| --- | --- | --- | --- |
| .5, .25 | 4 | 1.9821 | 1.9809 |
| .75, .5 | 2/.75 | 1.9612 | 1.9613 |
| .9, .8 | 2/.9 | 1.8625 | 1.8658 |

These are finite-window observations, not asserted asymptotic rates. The [complete predeclared windows](results/convergence_windows.csv) include all adjacent doublings and the 64–256 window. In the uniform singular alpha=.5 case the first rate is **-0.09049**, followed by 0.15739 and 0.28088. This nonmonotone/crossover behavior is preserved rather than removed or fitted to a target. The two memory rules have identical tested uniform singular maximum errors; their shared startup is not altered to manufacture an improvement.

At alpha=.75, beta=.5, N=256, M=14, the smooth H1 errors are **5.6371e-6** (PI-L) and **4.5351e-6** (PI-Q). On the graded singular problem they are **4.4930e-6** and **4.4931e-6**, respectively. PI-Q improves the smooth error constant here but is not uniformly more accurate and does not establish a higher full-scheme order. The twelve spatial refinements show rapid decay followed by a temporal floor. All errors are continuous L2/H1 maxima including level zero, not the original paper's normalized discrete error definition.

The [figures](figures/figure-data.json) use only actual Julia CSV values. Runtime bars are the five-repeat minimum–maximum, not confidence intervals; coincident curves have not been jittered. Final singular-refinement and runtime plots were visually inspected, with sample N/M ticks and legends outside the data region. The initial overlapping legend and its corrective source diff are retained in the [layout record](evidence/corrections/figure-layout.json).

## Controlled performance and memory

All timings below are warm instrumented totals at alpha=.75, beta=.5, N=256, M=14, with one Julia execution thread and one BLAS thread. Samples use fresh arrays, with explicit pre-sample GC outside the timed region. No measured sample reports compilation time. Package loading, fixed manufactured-callback construction, residual checking, continuous-error evaluation and I/O are excluded; actual callback evaluation and Ritz projection occur inside stepping; time-weight assembly, spatial assembly/projection preparation and stepping are included.

| Problem / variant | Median ms | Min–max ms | H1 maximum |
| --- | --- | --- | --- |
| Smooth, L1 printed | 16.041 | 15.917–16.307 | 2.8356e-4 |
| Smooth, L1–2 printed | 19.745 | 19.694–19.805 | 4.1008e-4 |
| Smooth, L1–2 endpoint PI-L | 21.316 | 21.259–21.412 | 1.7729e-5 |
| Smooth, Alikhanov PI-L | 8.597 | 8.537–8.614 | 5.6371e-6 |
| Smooth, Alikhanov PI-Q | 8.832 | 8.769–9.006 | 4.5351e-6 |
| Graded singular, Alikhanov PI-L | 8.096 | 8.068–8.111 | 4.4930e-6 |
| Graded singular, Alikhanov PI-Q | 8.269 | 8.231–8.453 | 4.4931e-6 |

[Phase summaries](results/timing_summary.csv) retain medians, ranges, allocation counts and allocated bytes at N=64,128,256. At N=256 the new-method measured total allocates 3,285,416 bytes / 11,781 allocations; the selected stored time arrays plus solution history occupy 1,077,352 bytes. These are different quantities. The benchmark's sampled descendant RSS peak is **665.4 MiB**, including warmup/JIT/runtime state. Shared pages can be counted repeatedly; this is not an exact per-case peak or a memory quota. The outer launcher `ru_maxrss` is not used as the Julia memory figure.

Controls retain both their actual production state weights and an increment conversion for diagnostic consistency, and their library weights use high-precision construction. New weights use stabilized Float64 moments. Consequently the table describes these explicit research implementations and setup choices; it is **not a production-solver or cross-language speedup claim**. The small PI-L/PI-Q timing differences are comparable to repeat variation in some cases, so no general overhead advantage is established. The clear accuracy/cost observation is the recorded case-specific smooth error constant, not intrinsic superiority of PI-Q.

## Preservation, failures and environment

All **521 tracked AUD-01 files** and **41 supplied-package files** retain their original bytes, including production source, Julia/Lean pins, earlier proofs, tables, figures and evidence. The original development workspace, Git index and unrelated metric-graph work remain unchanged; see [workspace preservation](evidence/workspace-preservation.json). The implementation lives only on local `research/legendre-gr07` in an isolated worktree. No commit, push, merge or pull request was made.

The supplied initial GR-07 adapter omitted a panel-length factor. Its script, CSV and log remain archived as **INVALID** and were neither executed nor used in comparisons/figures. The final supplied diagnostics were replayed unchanged.

A distinct newly written oracle attempt, [local-oracle-01](evidence/runs/local-oracle-01.stderr.log), stopped on a relative-error test at an exactly zero centered integral. The correction recognizes the known GR-02 cancellation with exact rational input arithmetic and requires both high-precision integrals below 1e-100 times positive panel mass; nonzero relative stabilization remains 1e-45. The [source diff](evidence/corrections/local-oracle-01.patch) and all attempted sources/outputs remain available. No supplied assertion, norm tolerance or expected convergence rate was relaxed.

The [environment record](evidence/environment.json) identifies Julia 1.12.6, SpecialFunctions 2.9.0, the unchanged project/manifest, OpenBLAS, native hashes and the existing isolated Python versions. No dependencies were acquired. Original Python and Julia environments were not modified; each workload receives its own writable compilation depot/scratch over read-only inputs.

Execution uses the [explicitly approved bounded-process policy](evidence/execution-policy.json): finite wall/CPU deadlines, per-process address-space/file limits, sampled descendant RSS, single-CPU affinity, bounded logs and cleanup. Read-only mounts and PID/user namespaces were tested against write/chmod/rename/unlink attempts and a detached child. Namespace cleanup and input integrity are checked after every job. User-manager/cgroup controls are unavailable, so **aggregate cgroup isolation is not claimed**. Exact commands, timings, failed attempts and snapshots are behind [evidence/runs/](evidence/runs/), rather than the primary reading path.

## Limitations and AUD-02 handoff

This closes GR-07 for the declared 1D forced examples, fixed orders, supported Float64 meshes and measured sizes. Extreme unrepresentable orders/steps, arbitrary decreasing meshes, 2D, general PDE regularity and order-uniform constants are outside the validation domain. Five timing samples do not establish broad statistical performance claims, and the implementation is dense with full history.

AUD-02 should review the supplied GR-01–06 arguments independently, including GR-04's tail-majorant comparison, GR-05's spatial/nodal regularity and energy interpretation, and GR-06's Hilbert-valued consistency extension and split-residual argument. The observed finite-grid crossovers are retained as data for that review, not investigated further here. No theorem, new scheme or additional mathematical investigation was introduced beyond the handoff's implementation and verification requirements.
