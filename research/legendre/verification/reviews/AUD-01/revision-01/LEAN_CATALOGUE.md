# Lean certificate catalogue

The preserved certificates comprise **42 named declarations**: 23 from ST-04 and 19 from AUD-01. A fresh combined driver checked all types and printed all axiom dependencies. Source hashes also match their successful compilation records. The pinned project and its dependency lock were unchanged.

The project uses Lean **4.19.0** and mathlib **v4.19.0**, pinned at `c44e0c8ee63ca166450922a373c7409c5d26b00b`. The combined inspection ran serially with one Lean worker and the existing compiled cache; it fetched no dependencies.

There are **41 nonduplicate mathematical identity groups** under the explicit convention below. This avoids counting the same telescoping identity twice; it does not claim that all 41 results are logically independent.

## Counting the overlap

For any real sequence and every nonnegative integer N, the new `reversed_difference_sum` becomes `sum(b(r+1)-b(r)) = b(N)-b(0)` after reversing the index. Negating and rearranging gives the old `telescoping_history`. Both include N=0. They are two named certificates for the same identity. General statements and their specializations are retained as separate propositions; no broader notion of logical equivalence is used.

## Coverage

| Mathematical argument | Formal coverage | Analytical work outside the certificates |
| --- | --- | --- |
| L1-2 coefficients | Zeroth correction/leading identities, exact negative example, signed-history bounds and normalization | Interpolation-integral derivation and full recurrence stability |
| GLL example | Concrete M=3 mass polynomial, exact real integral, positive coefficient and discrepancy | General-degree quadrature and spatial convergence |
| SP-02 | Real-polynomial symbol numerator and bracket inequality | Laplace representation, complex disk estimates, weighted resolvent and Cauchy coefficient bound |
| Temporal residuals | General finite summation by parts and all-length quadratic-history collection | Infinite-series asymptotics, fractional regularity, accumulated residual limit and error bounds |
| ST-05 | Rational constants, exact admissible rational orders, oscillator derivatives/quarter-period identity, energy algebra | Pi/gamma/exponential inequalities, propagator and logistic perturbation bounds, order continuity, convergence transfer |
| Norm/Volterra qualifications | Abstract weighted-energy statement; beta=1/2 near-panel positivity | Sobolev-space norm equivalences and full Volterra order theorem |

All audited dependencies are `propext`, `Classical.choice`, and `Quot.sound`. No `sorry`, `admit`, `sorryAx`, or new unsupported axiom appears in accepted sources or audit output. Compilation of the combined inspection driver is not a claim that the full PDE theory was formalized.

## Declaration inventory

The [machine-readable catalogue](lean-catalogue.json) contains every exact Lean statement, source line/hash, compilation record, and axiom list. The [existing ST-04 catalogue](../../../lean/README.md) and [initial AUD-01 review](../REVIEW.md#formal-certificates) provide mathematical descriptions.

| Identity group | Named declaration | Cohort |
| --- | --- | --- |
| G01 | `LegendreAudit.bStarZero_identity` | ST-04 |
| G02 | `LegendreAudit.leading_identity` | ST-04 |
| G03 | `LegendreAudit.leading_gt_one` | ST-04 |
| G04 | `LegendreAudit.leading_three_quarters` | ST-04 |
| G05 | `LegendreAudit.fourthRootTwo_fourth` | ST-04 |
| G06 | `LegendreAudit.fourthRootTwo_lt_thirteen_tenths` | ST-04 |
| G07 | `LegendreAudit.oldestSecond_three_quarters` | ST-04 |
| G08 | `LegendreAudit.oldestSecond_three_quarters_neg` | ST-04 |
| G09 | `LegendreAudit.history_abs_budget` | ST-04 |
| G10 | `LegendreAudit.signedHistory_triangle` | ST-04 |
| G11 | `LegendreAudit.signed_sum_bound_false` | ST-04 |
| G12 | `LegendreAudit.l12_assigned_state_counterexample` | ST-04 |
| G13 | `LegendreAudit.telescoping_history` | ST-04 |
| G14 | `LegendreAudit.telescoping_not_one` | ST-04 |
| G15 | `LegendreAudit.normalized_history` | ST-04 |
| G16 | `LegendreAudit.no_uniform_weighted_energy_bound` | ST-04 |
| G17 | `LegendreAudit.volterra_half_near_panel_positive` | ST-04 |
| G18 | `LegendreAudit.mass_polynomial` | ST-04 |
| G19 | `LegendreAudit.gll3_mass` | ST-04 |
| G20 | `LegendreAudit.mass_hasDerivAt` | ST-04 |
| G21 | `LegendreAudit.mass_integral` | ST-04 |
| G22 | `LegendreAudit.positive_mass_coefficient` | ST-04 |
| G23 | `LegendreAudit.gll3_variable_coefficient_counterexample` | ST-04 |
| G24 | `LegendreAudit.AUD01.symbol_numerator` | AUD-01 |
| G25 | `LegendreAudit.AUD01.symbol_bracket` | AUD-01 |
| G26 | `LegendreAudit.AUD01.smoothing_denominator` | AUD-01 |
| G27 | `LegendreAudit.AUD01.smoothing_amplitude` | AUD-01 |
| G28 | `LegendreAudit.AUD01.smoothing_difference` | AUD-01 |
| G29 | `LegendreAudit.AUD01.weighted_contraction` | AUD-01 |
| G30 | `LegendreAudit.AUD01.homogeneous_contraction` | AUD-01 |
| G31 | `LegendreAudit.AUD01.fractional_parameter_bound` | AUD-01 |
| G32 | `LegendreAudit.AUD01.fractional_parameter_admissibility` | AUD-01 |
| G33 | `LegendreAudit.AUD01.finite_summation_by_parts` | AUD-01 |
| G34 | `LegendreAudit.AUD01.quadratic_history_collection` | AUD-01 |
| G13 | `LegendreAudit.AUD01.reversed_difference_sum` | AUD-01 |
| G35 | `LegendreAudit.AUD01.pre_derivative` | AUD-01 |
| G36 | `LegendreAudit.AUD01.critical_position` | AUD-01 |
| G37 | `LegendreAudit.AUD01.critical_velocity` | AUD-01 |
| G38 | `LegendreAudit.AUD01.post_derivative` | AUD-01 |
| G39 | `LegendreAudit.AUD01.quarter_velocity` | AUD-01 |
| G40 | `LegendreAudit.AUD01.st05_endpoint_identity` | AUD-01 |
| G41 | `LegendreAudit.AUD01.oscillator_energy_algebra` | AUD-01 |
