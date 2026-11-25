# Independent review of AUD-01 revision 1

**Verdict: ACCEPT WITH LIMITATIONS.** The representative ambiguity and theorem-interpretation findings are repaired in the new manuscript. Available original diagnostics pass without changes to their assertions. Missing diagnostic sources and the temporal regularity interpretation remain explicit limitations, rather than completed verifications.

This report closes findings R1–R3 from the [initial independent review](../REVIEW.md). It supplements that review's analytical checks; it does not replace the original manuscripts or count a successful numerical run as a proof. The [revised PDF](mathematical-verification-aud01-r1.pdf) and [source](mathematical-verification-aud01-r1.tex) are separate derived artifacts. Section, proposition, and page locators below refer to this revision unless a source-paper locator is specified.

**Accepted on review** means the analytical argument is accepted under its explicit hypotheses. **Formally certified** applies only to an exact compiled Lean statement. **Unresolved** identifies missing evidence or an undecided interpretation. No remaining repair is concealed by either acceptance label.

## R1: coefficient representatives and spatial applications

### Correction

SP-01 §10.1, TeX lines 934–938, now requires a chosen continuous representative $K_n\in C(\overline I)$ with uniform pointwise bounds $0\le K_n(x)\le K_*$. Products, solution values, and forcing values at nodes use their continuous Sobolev representatives; pointwise multiplication must agree with the product representative. The concrete sufficient case is integer $m\ge2$, with $K_n\in W^{m,\infty}$ and its continuous representative. The more general multiplier assumption retains continuity, pointwise bounds, and compatibility of sampled products, with $K_m\ge K_*$.

An essential bound on an equivalence class does not constrain arbitrarily reassigned nodal values. The earlier review's $M=2$ example makes this distinction concrete: $K_L=1$ almost everywhere, $K_L(0)=L$, and $u=v=1-x^2$ give

$$
Q_2[K_Luv]-\int_{-1}^1 K_Luv=\frac43L-\frac{16}{15}.
$$

The revised continuity requirement excludes that ambiguity. For a continuous representative on this interval, the supremum agrees with the essential supremum. The correction strengthens the weak formulation's hypotheses; it does not establish nodal bounds from an essential bound alone.

### Dependencies checked

| Application | Revision locator | Consequence |
| --- | --- | --- |
| OB-04 consistency repair | §9.4, Proposition 9.2, p.17 | The sampled $a,u,au$ use compatible continuous representatives. The explicit smooth counterexample is unchanged. |
| Projection, quadrature, and residual | §§10.2–10.3, Eqs. (10.4)–(10.7), pp.20–21 | The product approximation and nodal multiplication have the same intended representative. |
| Fixed-grid spatial propagation | Proposition 10.1, p.21 | Its nodal operator bound inherits the pointwise coefficient hypothesis. Constants are not inferred from arbitrary representatives. |
| L1 spatial propagation | Proposition 10.2, p.22 | The same convention applies to the nonnegative memory bound. |
| Abstract L1–2 stability | Proposition 11.1, p.23 | Unchanged abstract content: $K_n$ is already an actual bounded nonnegative self-adjoint operator. A GLL realization must satisfy the revised nodal convention. |
| L1–2 spatial consequence | Proposition 11.2, p.25 | Explicitly inherits §10.1 before applying the resolvent estimate. |
| Initial-layer and combined estimates | Proposition 12.2, pp.29–30; §12.7, p.30 | The abstract temporal statement is unchanged; a spatial GLL application and the combined estimate inherit §10.1. |

**Classification: accepted on review after repair.** This correction does not change the smooth spatially constant coefficients in ST-05 or AUD-01. It supplies no new spatial regularity theorem for general PDE solutions.

## Theorem interpretation and temporal sharpness

### ST-05: eventual contractivity and an isolated mesh

The source paper's Theorem 3.1 (PDF p.15) states:

> The semi-discretized problems (19) and (37) are stable for a sufficiently large number of partitions in time. That is, there exists one Δt > 0, such that

It then displays $\|U_{(q)}^{k+1}\|_1\le\|U_{(q)}^0\|$, for $q=1,2$ and $k=0,\ldots,N-1$. The exact quote and displayed bound are transcribed in revised §13.1, p.31. The source PDF pp.15–16 was visually checked in the initial review. The wording contains two different possible quantifiers:

$$
\text{Eventual:}\quad \exists N_0\ \forall N\ge N_0\ \forall n\in\{1,\ldots,N\},\quad
\|U_N^n\|_{\tau_N}\le\|U^0\|_{L^2}.
$$

$$
\text{Isolated existence:}\quad \exists N\ge1\ \forall n\in\{1,\ldots,N\},\quad
\|U_N^n\|_{\tau_N}\le\|U^0\|_{L^2}.
$$

For the fixed data of ST-05, Proposition 13.1 (p.34; TeX lines 1416–1428) instead establishes

$$
\exists N_1\ \forall N\ge N_1\ \exists n_N\in\{1,\ldots,N\},\quad
\|U_N^{n_N}\|_{\tau_N}>2\|U^0\|_{L^2}.
$$

The coefficient, fractional orders, and initial data are fixed before $N\to\infty$. The proof concerns L1 and the interpolation-defined L1–2 rule with the printed memory quadrature. It does not identify that L1–2 rule with the inconsistent printed single-sum collection. The independent L1 convergence route does not require SP-02; the L1–2 route uses SP-02/TM-01. Its strict continuous amplification transfers to a nearest grid point by convergence.

**Classification: accepted on analytical review for failure of eventual contractivity.** The isolated-existence interpretation remains unresolved as a comparison with the theorem: ST-05 does not exclude every possible coarse grid. Neither the intermediate endpoint pair $(1,0)$ nor binary64 decimal approximations replace the fixed admissible orders $(1-2^{-600},2^{-600})$. A finite-time bound with a larger constant remains compatible with amplification.

### TM-01 and AUD-01: two standalone results

Proposition 12.1 (§12.3, p.27) first states a standalone maximum-over-time $\Theta(\tau^{1-\beta})$ error for a smooth manufactured amplitude with **smooth nonzero forcing**. Its lower bound uses the signed accumulated residual and a finite summed error equation. The matching upper bound uses SP-02 or its L1 analogue. Only after this proof does §12.4 (p.28) discuss Theorem 3.2.

Proposition 14.1 (§14.2, p.35) separately states a **zero-forcing homogeneous** example with $\alpha=3/4$, $\beta=1/2$, $T=2^{-10}$ and natural initial fractional singularity. It has maximum-over-time $\Theta(\tau^{1/2})$ error. The Neumann series, positivity estimate, initial-layer bounds, and signed accumulated-residual argument retain their original scope. The lower bound does not use SP-02; the upper bound uses Proposition 12.2 and its stability dependencies. The forcing/regularity comparison follows the standalone proof in §14.3, p.36.

**Classification: both standalone results accepted analytically.** Their implications for the intended smooth homogeneous solution class of Theorem 3.2 remain qualified. The source temporal construction sets $f=0$ (paper pp.5–6), while its consistency estimates use solution-dependent regularity. A smooth forced example and an initially singular homogeneous example cannot be combined into one smooth homogeneous example. The revised manuscript states this limitation and preserves the separate consistently forced spatial formulations.

The replayed homogeneous grids have a last-doubling exponent **0.7498 for both schemes**, with negative signed total residual but positive memory residual. They do not demonstrate the half-order asymptotic regime. No half-order numerical acceptance criterion was added. [The replay report](NUMERICAL_REPLAY.md) records the actual values, unchanged checks, and roundoff-sized differences from historical printed output.

## R3: reproducibility closure and remaining gaps

Four identified original programs were recovered or supplied and replayed: ST-03, ST-04, the AUD-01 exact checker, and the AUD-01 homogeneous checker. All pass. The existing independent 10-test counterexample suite also passes and is explicitly identified as a later independent check.

The [source inventory](DIAGNOSTIC_INVENTORY.md) contains all 14 referenced program groups. Ten originals remain unavailable or unauthenticated, including the named OB-03, OB-04, and SP-02 programs, the failed and corrected TM-01 companions, and the distinct ST-05 trajectory program. Repository sources, retained snapshots, Downloads research materials, and five related archives were searched. Related implementations were not promoted to original sources, and no replacement numerical program was reconstructed.

**Classification: available replay accepted; missing historical replay unresolved.** R3 is closed as a source-accounting and disclosure requirement, not as recovery of all missing programs. Historical matrix/resolvent, corrected TM-01, and 36-configuration ST-05 numerical claims remain reported evidence. They are not included in the fresh success count. The precise Canuto–Quarteroni and ETNA primary-source locators remain unverified; no broader literature search was performed.

## Formal evidence and result register

All 19 AUD-01 certificates and 23 ST-04 certificates are preserved. A fresh combined inspection checks their types and prints their axioms. The 42 names represent 41 nonduplicate identity groups when the two index-reversed telescoping statements are grouped. This is an explicit identity-counting convention, not a claim of logical independence. The [catalogue](LEAN_CATALOGUE.md) supplies exact statements, source hashes, successful source-compilation records, and all axiom dependencies.

| Proof chain | Classification and scope |
| --- | --- |
| SP-02 symbol, weighted resolvent, Cauchy extraction, startup and finite-time memory absorption | Accepted on review for fixed orders, uniform grids and the stated operator hypotheses. The numerator/bracket algebra is formally certified; complex analysis and operator estimates remain analytical. |
| TM-01 memory expansion, accumulated residual, solution lower bound, initial-layer propagation | Accepted on review with separate forcing and regularity hypotheses. Finite summation identities are formally certified; asymptotic error propagation remains analytical. |
| AUD-01 homogeneous series, positivity and sharpness | Accepted analytically for the explicit small-time problem. Rational contraction constants are formally certified; positivity, fractional regularity and asymptotics are analytical. |
| ST-05 oscillator, smoothing, order perturbation, regularity and fine-grid transfer | Accepted analytically within the explicit fixed-data construction. Listed oscillator calculus and rational constants are formally certified; the full counterexample theorem is not. |
| SP-01 projection, quadrature, norm and constants | Accepted with the representative repair and stated product regularity. The concrete GLL example is formally certified; general spatial convergence and approximation-source checks are not. |
| Earlier VQ-01 / CF-02 / ST-03 / OB-03 / OB-04 | Their formula-level discrepancies and proof gaps retain the scope described in the manuscript. The ST-04 finite-grid candidate remains distinct from ST-05. |

Every fresh axiom list is limited to `propext`, `Classical.choice`, and `Quot.sound`; no unsupported axiom or incomplete proof was accepted. Source hashes match the prior successful compilation records. This turn inspected the combined compiled modules rather than recompiling all 42 source proofs or changing the pinned project.

## Validation and remaining limitations

The revised manuscript compiles offline to 37 pages, with no undefined references or overfull boxes. Six underfull paragraph warnings remain. Missing-font and output-directory setup failures are preserved; the successful revision uses cached script sizes without altering the mathematics. Final PDF pages 20, 31, and 37 were visually inspected. [Artifact metadata](manuscript-artifact.json) locates every principal proposition and records all build attempts.

The original 294-file inventory and the additional 49-file review/Lean guard compare byte-for-byte unchanged. Original manuscripts, numerical outputs, proof sources, navigation edits, and production algorithms are preserved. No Julia rerun is claimed. [Integrity and documentation checks](INTEGRITY.json) record the final comparison and link checks.

The first documentary validator run found a formatting mismatch in its comparison of recorded unittest calls: deparsed AST text normalized parentheses and decimal literals. The validator now extracts exact source text, matching the criteria inventory. The initial failure is retained; no numerical assertion or acceptance threshold was changed.

Acceptance is limited to the corrected statements and reproduced programs. It does not resolve the original theorem's regularity interpretation, recover the ten missing program groups, certify all analytical arguments in Lean, provide an order-uniform or ordinary-$H^1$ estimate, or establish the homogeneous asymptotic rate from the finite data. These limitations belong in any subsequent presentation of the checkpoint.
