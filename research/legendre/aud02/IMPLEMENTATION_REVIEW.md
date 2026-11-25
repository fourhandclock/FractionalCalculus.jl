# GR-07 implementation and numerical evidence review

The implemented Alikhanov–PI-L and Alikhanov–PI-Q formulas agree with the
analyzed interpolation definitions on the tested uniform, graded and additional
irregular nondecreasing-step meshes. The admitted 156-case matrix reproduces.
**The generic moment routine has three confirmed boundary failures.** Its
current guards therefore describe a wider domain than the accuracy evidence
supports. This review preserves the implementation and records the failures;
it does not repair or optimize it.

## Correspondence with the mathematics

Locators refer to [GR07.jl](../../../studies/legendre/gr07/GR07.jl).

| Source locator | Independent review | Status |
| --- | --- | --- |
| Lines 77–108 | Production state coefficients are retained for controls; converting them to increments uses reverse cumulative state sums | Accepted on review |
| Lines 94–142 | New derivative matrix acts on increments; memory matrix acts on states, including the initial column | Accepted on review |
| Lines 98–99, 111–112 | The same shifted time is used for derivative, diffusion, coefficient and forcing; the final local ratio is exactly sigma | Accepted on review in the admitted numerical range |
| Lines 114–120 | Nonuniform derivative correction divides by the current panel length and actual adjacent-step ratio | Accepted on review |
| Lines 123–137 | Forward nonuniform quadratic memory on completed panels; backward quadratic final panel; linear startup | Accepted on review |
| `advance` | Gamma(1-beta) is applied once to normalized memory; shifted diffusion and every history/initial term are retained | Accepted on review |
| `spatial_operators`, `project_initial` | Actual library GLL mass/stiffness, derivative Ritz initialization and separate reconstruction quadrature | Accepted on review for the tested degrees |
| `continuous_errors` | Integrates reconstructed function and derivative errors with separate Gauss quadrature; maximum includes time zero | Accepted as a numerical continuous-norm approximation |
| `local_moments`, lines 45–74 | Broad finite-Real input guards do not ensure stable representable arithmetic | Repair required outside the admitted range |

Current-level values at times later than the shifted point are unknowns in an
implicit step. No stencil uses a later timestep than the current solve. The
derivative and memory final-panel conventions are deliberately different.
The corrected endpoint L1-2 interpolation method and the published inconsistent
recurrence are not silently substituted for one another. The controls call
actual production functions; the source and tests were inspected for this,
rather than inferred from independent copied formulas.

## Independent probes and complete replay

The new oracle in [independent_rows.py](scripts/independent_rows.py) constructs
generic Lagrange polynomials and integrates them after a power substitution
removing the endpoint singularity. It does not call incomplete beta functions,
the supplied Python assembly, or the Julia moment formulas. It uses 80 decimal
digits and checks 24 complete derivative/memory row pairs on three additional
mesh/order configurations. All **156 scalar coefficient comparisons** meet the
predeclared scaled tolerance `8e-11`; the maximum scaled difference is
`4.311681156648209e-15`. These 156 coefficient comparisons are distinct from
the **156 full PDE cases** in the original experiment matrix. The oracle also
checks 72 derivative polynomial identities independently.

The exact rational [abstract probe](scripts/abstract_probe.py) checks 1,134
ordered products, 4,914 simplex-bound inequalities, 18 ordered-vector
comparisons and nine triangular resolvents. Its rational inequalities have
no tolerance. The examples include noncommuting original matrices and failure
of entrywise domination. They are finite tests, not the infinite-series proof.

Fresh bounded serial execution reproduced:

- All 7,941 GR-07 assertions and all 669 existing baseline assertions.
- Final supplied GR-02–GR-06 Python diagnostics, including the 60-case graded
  diagnostic; no observed-rate acceptance assertion was added.
- The corrected 156-case Python reference and 156-case Julia matrix. The largest
  H1-norm difference is `3.437441303821842e-14`, within the original
  `5e-11 + 2e-6*abs(reference)` criterion. All equation residual checks pass.

The initial invalid GR-07 adapter/output remains archival and was never an
oracle or acceptance input. Its missing backward-panel scaling factor is not
reintroduced. The original oracle's exact-zero stabilization correction and
other failed attempts remain preserved with their original status.

## Moment boundary counterexamples

For a final panel with `d=H`, the exact zeroth normalized moment is

$$
M_0=\frac{(hH)^r}{\Gamma(1+r)}.
$$

The tests below use the actual binary Float64 inputs interpreted as real
numbers by the high-precision reference. No result was fitted or replaced.

| Case and arguments `(h,r,d,H)` | Julia M0 | High-precision M0 | Relative error |
| --- | --- | --- | --- |
| Control `(.125,.5,.625,.625)` | `0.31539156525252` | `0.315391565252520006...` | `1.91e-17` |
| Tiny product `(1e-200,.5,1e-200,1e-200)` | `0.0` | `1.12837916709551255e-200` | `1.0` |
| Subnormal step `(nextfloat(0.),.5,.55,.55)` | `2.508114666398235e-162` | `1.86006761944050332e-162` | `0.3483997249264842` |
| Near-zero integral order `(1.,1e-310,1.,1.)` | `0.0` | `1.0` to the displayed precision | `1.0` |

In the tiny-product case, forming `h*H` underflows before taking the fractional
power, although the final moment is representable. In the subnormal case the
product rounds too coarsely before exponentiation. In the near-zero-order
case `gamma(r)` overflows, so its reciprocal becomes zero; the normalized
moment itself remains finite. The inputs pass `local_moments`' explicit guards.
The separate [boundary acceptance run](evidence/runs/aud02-boundary-acceptance-01.stdout.log)
**returns exit code 1**, applying the unchanged `5e-12` relative criterion.
The oracle-generation run's success is not reported as a pass for these cases.

The first and third examples exercise the generic routine beyond the actual
GR-07 panel/order combinations; the subnormal example uses a possible final
panel ratio but a step far outside the admitted meshes. None is evidence that
the preserved N=32–256 results are wrong. They are counterexamples to treating
the guard conditions as an accuracy guarantee for the generic API. Before
general use, either repair the arithmetic or specify and enforce an accurately
supported numerical range. The exact quadrature scheme is unaffected.

The `Real`-typed entry points also validate before Float64 conversion. A static
review identifies post-conversion finiteness, strict node ordering and order
range as additional obligations for wider-precision callers. These were not
executed boundary counterexamples in this review and remain separately labelled
as untested interface concerns.

## Continuous norms and convergence interpretation

The error formula is ordinary continuous H1, including the L2 and derivative
parts, approximated numerically by Gauss integration. It is not the paper's
timestep-weighted norm or a relative normalization. Existing 80/120-point
refinement checks passed on the tested smooth spatial functions. This is
not an exact integral certificate for arbitrary callbacks or degrees.

The singular examples are consistently forced and use Ritz initial data.
Neither current mesh-doubling windows nor the old homogeneous AUD-01 window
prove an asymptotic exponent. In particular the observed homogeneous rate
near `0.7498` remains an observation, not numerical confirmation of a
half-order asymptote. The nonmonotone uniform singular GR-07 errors remain
in the preserved and fresh tables. No coarse result was discarded to obtain
a preferred slope.

## Performance evidence and complexity

The existing performance protocol has 21 distinct warmups, then 105 fresh
solves with five repetitions and four phase records per solve. Its admission
hashes, tolerances and post-solve checks were inspected. Timing includes weight
assembly, spatial preparation and stepping, including callback evaluation and
Ritz projection. It excludes package loading, construction of the fixed
manufactured callbacks, residual/norm postprocessing and file I/O. Pre-sample
GC lies outside timing. Variant order rotates and the N traversal alternates.
No new timing experiment or optimization was performed for AUD-02.

The preserved CSV distinguishes allocation **count** from allocated **bytes**.
The progress print's `alloc=` field actually prints bytes; future presentation
should label it `allocated_bytes=`. This label issue does not alter the CSV.
The selected stored-array count includes A, W, the extra control state matrix
and U, not every live array, runtime object, temporary increment history or
coefficient/forcing cache. It is not peak memory. The sampled descendant RSS
figure includes the complete benchmark process, compilation and warmups, and
can count shared pages repeatedly. The launcher's `ru_maxrss` does not measure
the Julia payload's peak.

For m interior spatial unknowns, the current dense full-history realization
stores quadratic time-weight arrays and O(mN) history. Direct history products
cost O(mN²), and unfactored dense current-step solves add O(Nm³). These are
implementation-level operation counts, not measured asymptotic laws. The
diagnostic complementary matrix is not part of evolution. Production controls
use high-precision construction and retain extra state/increment arrays; the
new methods use Float64 moments. Those differences prevent interpreting the
timings as an intrinsic scheme advantage. Small PI-L/PI-Q timing differences
are comparable to five-repeat variability. No cross-language speedup,
universal efficiency claim or superior asymptotic accuracy is accepted.

## Required treatment before broader use

Keep the finite GR-07 admission and its numerical range explicit. Record the
three boundary failures as repair-required issues, distinguish static conversion
concerns from executed failures, and clarify the benchmark progress label and
stored-array scope. These changes are recommendations for a later authorized
implementation revision; the frozen algorithms and historical evidence were
not changed in this audit. Reproduction commands, versions and integrity checks
are collected once in [VALIDATION.md](VALIDATION.md).
