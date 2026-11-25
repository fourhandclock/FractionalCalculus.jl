# GR-07 execution contract

Baseline: audited AUD-01 commit `bf43fd0e78bcbcaae94d4c95fd9e43fd562ba477`. The entire tracked baseline and the supplied package are hashed separately. Production code, pins, prior proofs, data and evidence are read-only inputs. The invalid initial GR-07 output is archived and excluded from scientific comparisons.

The implementation is confined to this experimental 1D study. No complete theorem audit, new method, 2D extension, literature expansion or publication is part of GR-07. GR-01–06 remain proposed theory for AUD-02.

## Predeclared numerical criteria

- Normalized panel moments: compare with independent transformed polynomial quadrature at 120 and 180 decimal digits (extra precision protects the tiny centered correction at lag 1e24), requiring relative stabilization below 1e-45; compare Julia at relative 5e-12, absolute 1e-300. Include r=.01,.1,.5,.99, final/ordinary panels, h through 1e-30 and lag through 1e24; test the centered derivative correction separately.
- Direct local interpolation: generic Lagrange basis evaluation and separate Gauss integration, not weight-assembly expressions. Completed panels use 64 Gauss points; singular final panels remove the singularity by substitution and use 512 points. Relative weight tolerance 5e-10, absolute 2e-12. Additional 256/512-point stabilization checks isolate numerical quadrature error.
- Coefficient structure: chronological increment A>0 and increasing towards newest, shifted newest-weight gap, complementary P>=-2e-12, PA=J within 2e-10, and correct uniform/graded lower/tail bounds with relative margin 2e-10. Energy tests use fixed RNG seed and scale-aware roundoff allowance. PI-Q is allowed signed entries, including the exact -17/231 normalized initial-column witness.
- Algebra/initialization: constants and linear/quadratic exactness, PI-Q linear startup, independent GLL stiffness/energy and Ritz orthogonality, polynomial manufactured evolution, one-step/nonzero initial column, variable and signed nodal coefficients, boundary and nonfinite-input failures. Printed controls must call actual library weight routines and agree with actual `solve_tfide` on small cases with matching initialization.
- Full equation residuals: all rows, normalized by one plus the sum of absolute operator/data terms, below 1e-9. Residuals alone do not admit a result.
- Reference comparison: all 156 scientific case keys match; continuous L2 maximum, H1 maximum and H1 final errors satisfy abs(Julia-Python)<=5e-11+2e-6*abs(Python). Gauss norm evaluation uses at least 80 points with an independent refinement check. This budget separates small spatial/solve roundoff from discretization error; it is not a theorem bound.
- Convergence is described over the predeclared adjacent doublings 32–64,64–128,128–256 and the last-two-doubling window 64–256. Do not force slopes or require the asymptotic exponent on every finite grid. Spatial sweeps are separate from temporal rate calculation.
- Run the complete original AUD-01 root regression suite before and after implementation; record actual counts rather than copying 669 from history.

## Experiment and timing design

The supplied 156-case matrix is reproduced exactly: three order pairs, two forced solutions, five uniform variants, graded singular Alikhanov variants, and the twelve graded spatial refinements. No original paper example is added because it has different coefficient/forcing/normalization choices.

Performance is gated on passing correctness and rowwise reference comparison. Selected sizes are N=64,128,256 at M=14, alpha=.75,beta=.5: all five smooth/uniform variants and two singular/graded variants. Each configuration receives one specialization warmup and five measured fresh-input evaluations. Rotate variant order across repeats; one BLAS/Julia thread. Include mesh/time-weight assembly, spatial assembly with projection/error-quadrature preparation, and stepping (including callbacks and Ritz projection) in total; exclude package loading, residual checking, continuous-error postprocessing and file I/O. Report those scope choices. Record wall time, allocation count and allocated bytes per phase and total. Fresh arrays on every evaluation; no mutated history is reused. Stored arrays, allocated bytes and sampled process RSS have different meanings. Do not compare Python and Julia wall clocks as a speedup. Controls retain both production state weights and their increment conversion for diagnostics; storage/cost reflects this research implementation, not minimal possible production storage.

## Resources and preservation

Planned serial process limits: 300 s wall/240 s CPU for regression tests; 300 s/240 s for unit/oracle/reference checks; 600 s/540 s for the full Julia matrix; 600 s/540 s for admitted timing. Address-space ceilings 8 GiB (Julia), 2 GiB (Python), sampled RSS ceilings 2 GiB/1 GiB; logs <=8 MiB per run, each generated file <=256 MiB. Each run has new scratch/output paths, exact source snapshots and recorded limits. No dependency acquisition is authorized implicitly. The pending preflight decision records whether the existing bounded runner can be used; no scientific execution is claimed by this plan.

Before performance, seal a correctness admission binding exact implementation, tests, configuration, reference, environment and wrapper contents. Preserve failed attempts and corrective diffs. Hashes monitor host integrity; read-only workload namespaces enforce source/input protection where available. Record actual isolation/cleanup semantics; do not claim unavailable aggregate cgroup limits.

## Recorded oracle correction before admission

`local-oracle-01` failed because its relative stabilization metric divided by a near-zero integral for the exact GR-02 shifted cancellation r=.1,H=d=.55. The supplied formulas/tests are unchanged. The corrected new oracle recognizes this exact rational zero and requires both high-precision quadratures below 1e-100 times panel mass, writing an exact zero; nonzero stabilization and Julia comparison tolerances are unchanged. The final centered moment is evaluated in cancellation-free form in the candidate. Sources, stderr and corrective diffs are retained.
