# Boundary repairs and manuscript correction record

The revision preserves the original implementation and AUD-02 evidence. The three exact inputs were replayed against the original module before evaluating the separate repaired module. The [independent oracle](scripts/boundary_oracle.py) uses the exact binary Float64 inputs in 400- and 500-digit arithmetic; all four final-panel moments stabilize to relative error below 1e-80. Supported results retain the original **5e-12 relative criterion**, without an absolute-error escape for these regressions.

## The three moment findings

| Original input `(h,r,d,H)` | Original M0 and mechanism | Revision-01 treatment |
| --- | --- | --- |
| `(1e-200,.5,1e-200,1e-200)` | Zero: `h*H` underflows before its fractional power; true M0 is approximately 1.12837916709551255e-200 | The separately scaled M0 calculation passes the oracle. The full tuple explicitly rejects because M1 is approximately 7.52252778063675e-401 and M2 approximately 6.0180222245094e-601, both positive but below Float64's minimum positive value |
| `(nextfloat(0.),.5,.55,.55)` | Approximately 2.508114666398235e-162 instead of 1.86006761944050332e-162: the subnormal intermediate product loses representability/precision before exponentiation | Separate scaled powers avoid that product. All four returned moments pass the independent oracle |
| `(1.,1e-310,1.,1.)` | Zero: Gamma(r) overflows and its reciprocal becomes zero, although normalized mass is near one | Final mass uses Gamma(1+r); the generic reciprocal uses r/Gamma(1+r) only if the original reciprocal is zero. All four moments pass the oracle |

These are underflow, intermediate rounding and overflow failures, respectively; cancellation is not the cause of the three original M0 failures. The first case has an additional unavoidable **output** representability limit for M1/M2. Rejecting the full tuple is not a claim that its M0 is unrepresentable: M0 is separately repaired and tested. The original input is retained in both the oracle and regression suite.

The complete tuple API conservatively requires finite, positive **normal** M0/M1/M2. This is stricter than bare nonzero representability and supplies an explicit precision domain. It does not classify every subnormal output as mathematically unrepresentable. The signed centered component may vanish. Unrepresentable tuple outputs raise an informative DomainError rather than silently returning zeros. There is no clamp or fitted threshold.

AUD-02 also identified conversion obligations. The revision checks orders and panel parameters after Float64 conversion, checks converted node increments, and requires representable strictly interior shifted evaluation times. A local moment can be representable for a subnormal panel step while a complete time mesh has no representable shifted interior point; those cases have distinct validation outcomes.

## Minimal implementation scope

Changes are confined to [the separate revised module](../../../../studies/legendre/gr07/revision-01/GR07.jl). The derivative, memory stencils, startup, quadrature formulas, normalization, spatial discretization, history equations and error-norm algorithms remain the same. No new numerical method, acceleration or benchmark optimization is introduced. The complete original 7,941 assertions remain, with 21 additional boundary/conversion assertions.

The first regression attempt failed while parsing the two unrepresentable oracle numbers directly as Float64. Its source and full error output are preserved. The corrected test reads them as BigFloat and checks their positivity and strict upper bound by the minimum positive Float64. This is stronger evidence for rejection; the acceptance tolerance was not weakened.

## Manuscript corrections mapped to the audit

All six revised sources and compiled PDFs are in [manuscripts/](../../../../studies/legendre/gr07/revision-01/manuscripts/); The offline builds and visual inspection pass; originals remain in [reference/theory/](../../../../studies/legendre/gr07/reference/theory/). Every original theorem-environment count and historical tabular block is preserved. No new theorem is introduced.

| AUD-02 obligation | Revision treatment |
| --- | --- |
| Pointwise versus almost-everywhere initial majorants | GR-01 explicitly qualifies representatives and the interpretation of the comparison |
| Established continuous resolvent machinery | GR-01 identifies prior theory and retains fixed-order/regularity limitations |
| Uniform versus graded identities | GR-02/03/04 state uniform-grid scope; GR-06 gives the separate nonuniform hypotheses and grading-dependent constants |
| Increment versus state coefficients; causal stencils | GR-02/03 explicitly retain increment collection, current-step implicit values, no later timestep, and distinct final-panel roles |
| Normalized versus unnormalized memory | GR-03 retains Gamma(r) exactly once in the equation |
| Negative PI-Q weight and absolute mass | GR-03 identifies -17/231 as the normalized factor and retains absolute matrices and initial columns |
| Ordered-vector hypothesis and noncommuting originals | GR-04 identifies the cone argument and commutation only of the Toeplitz majorants |
| Diagonal condition versus uniform-series condition | GR-04 keeps the two restrictions separate and the word-length-dependent simplex shift |
| Unbounded-operator domains | GR-04/05 retain fixed self-adjoint A, initial data in D(A), form testing and the base resolvent's range; GR-06 states this in the split-residual theorem |
| Sufficient versus necessary restrictions | GR-01/04/06 explicitly label their fine-grid restrictions sufficient |
| Ordinary H1 versus weighted norm | GR-04 limits its H norm; GR-05/06 state ordinary diffusion-energy/H1 results, with no timestep-weighted substitution |
| Legendre projection source obligation | GR-05 supplies the independent weighted-Legendre/Bessel input; the inaccessible exact CQ locator remains honestly unverified |
| Nodal representative and product regularity | GR-03/05/06 retain continuous representatives and actual pointwise nodal bounds, not essential bounds alone |
| Hilbert-valued singular residual | GR-06 gives the Bochner/integral-remainder and zero-trace justification, with positive error-convolution kernels |
| Residual not squared; physical-time absorption | GR-06 expands the split-energy argument and absorption of a term linear in the global energy maximum |
| Endpoint rate and grading threshold | GR-06 shows the maximum-based graded scaling, no harmonic sum/logarithm, and sufficient fixed grading 2/alpha |
| Assumed versus established PDE regularity | GR-01/05/06 state that the results do not prove arbitrary-data regularity |
| Analytical versus formal proof | Every revised note qualifies finite certificates; no full PDE formalization is claimed |
| Forced versus homogeneous sharpness and old theorem quantifiers | GR-05 and the closure guide preserve the forcing, temporal regularity and eventual-contractivity qualifications |
| Finite-grid data and performance scope | Tables remain historical; fresh results are separate. Old timings are not an admission for changed code |
| GR-04 novelty | Revised GR-04 cites the newly checked comparison precedent and explicitly retains unresolved novelty |

The [literature closure](LITERATURE.md) records the source-access attempts and the distinction between known comparison mechanisms and unresolved equivalence of the full quantitative theorem.
