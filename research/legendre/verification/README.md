# Mathematical verification of the Legendre method

[Study guide](../../../studies/legendre/README.md) · [Current manuscript (PDF)](reviews/AUD-01/revision-01/mathematical-verification-aud01-r1.pdf) · [LaTeX source](reviews/AUD-01/revision-01/mathematical-verification-aud01-r1.tex) · [Lean certificates](lean/README.md) · [Reproduce](REPRODUCE.md)

**AUD-01 revision 01: ACCEPT WITH LIMITATIONS.** This checkpoint joins the numerical reproduction of Sabawi et al. (2025) to an independent mathematical audit. It preserves the earlier ST-04 work, adds the accepted spatial and temporal investigations, and records which arguments are analytical, machine-checked, or supported only by finite-grid experiments.

## GR-01–07 closure

The [AUD-02 revision-01 checkpoint](../aud02/revision-01/README.md) adds the revised uniform/graded Alikhanov–product-integration analysis and its separate Julia research module. Its conditional ordinary-H1 results, 54 named finite certificates, repaired moment-domain contract and actual validation are distinct from the endpoint L1/L1-2 results below. See the [research-method study guide](../../../studies/legendre/gr07/revision-01/README.md). Original AUD-01/ST-04 mathematical sources and all historical evidence remain preserved.

## Problem and published claims

The model couples a Caputo time derivative to diffusion and weakly singular Volterra memory:

$$
{}_0^C D_t^\alpha u-u_{xx}
+\lambda K(x,t)\int_0^t(t-s)^{-\beta}u(x,s)\,ds=f(x,t),
\qquad 0<\alpha,\beta<1.
$$

The paper uses L1 or L1–2 time differentiation, a trapezoidal/singular-panel memory rule, and Legendre–Gauss–Lobatto (GLL, also called LGL) spatial quadrature. L1–2 uses a linear first panel and quadratic interpolation thereafter. The main claims concern memory-quadrature consistency, stability of the time-discrete problems (Theorem 3.1), temporal convergence (Theorem 3.2), and spatial/full discretization (Theorems 4.1–4.2).

The [Julia study](../../../studies/legendre/README.md) compares implementations with published tables. Full numerical reproduction remains incomplete. This audit asks which mathematical estimates follow from the printed formulas, and which conditional replacement estimates can be justified.

## Verification status

A **confirmed discrepancy** has an exact derivation or counterexample. A **proof gap** identifies an unsupported inference without establishing instability. **Accepted on review** is an analytical judgment under stated hypotheses; **formally certified** applies only to an exact compiled Lean proposition. A **finite-grid candidate** has not established the theorem's limiting quantifiers.

| Investigation | Conclusion and manuscript locator |
| --- | --- |
| [VQ-01 / Observation 8](observations/README.md#vq-01-volterra-quadrature-observation-8) | Confirmed sharp general memory-quadrature order $1-\beta$, instead of the claimed $2-\beta$; §4 |
| [CF-02 / Observation 2](observations/README.md#cf-02-l1-2-coefficients-observation-2) | Confirmed mismatch between interpolation and the printed L1–2 collection; post-startup $d_0>1$ and signed history; §5 |
| [ST-03](observations/README.md#st-03-the-contraction-argument-observation-1) | Established gap in the signed-history contraction argument; §6 |
| [ST-04](observations/README.md#st-04-amplification-with-a-positive-time-dependent-kernel) | Separate finite-grid amplification candidate; its own all-fine-grid conclusion remains unproved; §7 |
| [OB-03 / OB-04](observations/README.md#ob-03-and-ob-04-startup-and-spatial-exactness) | Verified startup consistency and variable-coefficient GLL exactness defects; §§8–9 |
| [SP-01 / SP-02](observations/README.md#sp-01-and-sp-02-conditional-spatial-convergence-and-stability) | Conditional spatial convergence and uniform finite-time stability accepted on review, with repaired nodal hypotheses; §§10–11 |
| [TM-01](observations/README.md#tm-01-smooth-forced-sharpness-and-initial-layers) | Smooth forced temporal sharpness and conditional initial-layer propagation accepted analytically; §12 |
| [ST-05](observations/README.md#st-05-eventual-contractivity) | Analytical failure of eventual contractivity for fixed admissible data, on every sufficiently fine uniform grid; §13 |
| [AUD-01](observations/README.md#aud-01-homogeneous-temporal-sharpness-and-independent-review) | Homogeneous initially singular half-order sharpness accepted analytically; independent review corrections retained; §14 |

The [observation dossier](observations/README.md) connects each question to its claim, finding, evidence and limits. The [independent review](reviews/AUD-01/revision-01/REVIEW.md) gives precise proposition and source-paper locators. Observations 5–7 retain their norm, normalization and model-assumption qualifications.

## Replacement results and their limits

SP-02 establishes a uniform finite-time estimate for the interpolation-defined L1–2 rule, including its actual startup and bounded memory. Its constant depends on fixed orders, final time and coefficient bounds; it is not contractivity with constant one. The norm is timestep-weighted: this is not a uniform ordinary-$H^1$ estimate. SP-01 and its spatial applications require product regularity and compatible continuous coefficient representatives with uniform **pointwise** nodal bounds. An essential bound on an arbitrary equivalence class does not supply those values.

ST-05 concerns the *eventual* reading of Theorem 3.1: contraction on every sufficiently fine grid. The paper also says “there exists one” timestep. The construction does not exclude contraction on every possible coarse grid. Its L1 argument is independent of SP-02; its interpolation-defined L1–2 conclusion uses SP-02/TM-01 and does not validate the inconsistent printed recurrence.

TM-01 first proves a standalone sharpness result for a smooth solution with nonzero smooth forcing. AUD-01 gives a different, homogeneous solution with an initial fractional singularity. Their comparison with the intended regularity class of Theorem 3.2 remains qualified. A quadrature counterexample alone is not a PDE convergence counterexample, and these two solution classes cannot be combined into one smooth homogeneous example.

## Inspect and reproduce the evidence

| Evidence | Where to start |
| --- | --- |
| Detailed mathematics | [Accepted 37-page PDF](reviews/AUD-01/revision-01/mathematical-verification-aud01-r1.pdf), [unchanged accepted source](reviews/AUD-01/revision-01/mathematical-verification-aud01-r1.tex) |
| Original claims and related work | [Source paper](../../../YS_SS_PD_NM_25_Calcolo.pdf), [literature qualifications](literature/README.md) |
| Formal subclaims | [Lean overview](lean/README.md), [42-name catalogue and 41-group convention](reviews/AUD-01/revision-01/LEAN_CATALOGUE.md) |
| Actual-library regressions | [Julia test entry point](../../../test/runtests.jl), [proof audit](../../../studies/legendre/test/proof_audit.jl) |
| Independent diagnostics | [Supplied AUD-01 programs](../../../AUD01_review_package/aud01/README.md), [existing regressions](scripts/check_counterexamples.py), [ten unavailable original groups](reviews/AUD-01/revision-01/DIAGNOSTIC_INVENTORY.md) |
| Execution scope and current replay | [AUD-01 integration validation](results/checkpoint-aud01/VALIDATION.md), [reproduction guide](REPRODUCE.md) |

The homogeneous finite-grid rate is **0.7498**, not numerical confirmation of the analytical half-order limit. The 42 named Lean certificates form 41 nonduplicate identity groups under the catalogue's explicit telescoping-overlap convention. They cover finite algebra, summation, exact quadrature and oscillator calculus, not complete PDE proofs.

## Sources and archival evidence

The accepted revision is the current mathematical source. [Supplied AUD-01 inputs](../../../AUD01_review_package/aud01/README.md), the [original independent review](reviews/AUD-01/REVIEW.md), and [revision-01 closure](reviews/AUD-01/revision-01/README.md) are preserved with their original context. Historical workspace-specific integrity checks are archival; current clean-tree checks are documented in the integration validation report.

Earlier sources remain available: [ST-04 LaTeX](mathematical-verification.tex), [ST-04 PDF](sources/legendre_spectral_verification_notes_st04.pdf), [ST-03 transcription](sources/mathematical-verification-st03-transcription.tex), and the [ST-04 validation report](results/VALIDATION.md). The ST-04 commit `80788d324e2c607119ac6585cf832994bcf1e823` remains in this branch's ancestry.

Detailed commands, outputs, failed attempts, environments and hashes belong to the [ST-04 archive](results/checkpoint-st04/), [AUD-01 review evidence](reviews/AUD-01/results/), [revision-01 replay evidence](reviews/AUD-01/revision-01/results/) and [clean-tree integration evidence](results/checkpoint-aud01/). These support the manuscripts and summaries; they are not the primary reading path.

## Outstanding mathematical questions

Recover the ten missing original diagnostic groups and verify the related-work primary locators. Clarify the original theorem's intended temporal regularity and forcing class before attributing a broader refutation. The accepted estimates retain fixed-order, regularity, uniform-grid and weighted-norm limitations; their constants and spatial regularity quantities require control for simultaneous limits. ST-04 remains separate from the analytical ST-05 construction. No new numerical method or further theorem is introduced by this integration.
