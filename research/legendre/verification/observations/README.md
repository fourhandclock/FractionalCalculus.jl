# Mathematical investigations

These investigations examine the discretizations and estimates in the [Sabawi paper](../../../../YS_SS_PD_NM_25_Calcolo.pdf). VQ-01 concerns Volterra quadrature, CF-02 concerns L1-2 coefficients, and ST-03/ST-04 examine stability. The identifiers are retained so that claims can be traced through the manuscript, programs, and recorded results.

The [verification overview](../README.md#verification-status) defines the research statuses. Full proofs and exact qualifications are in the [accepted manuscript](../reviews/AUD-01/revision-01/mathematical-verification-aud01-r1.tex): VQ-01 in §4, CF-02 in §5, ST-03 in §6, ST-04 in §7, OB-03/OB-04 in §§8–9, SP-01/SP-02 in §§10–11, TM-01 in §12, ST-05 in §13 and AUD-01 in §14. Equation numbers below refer to that manuscript unless explicitly identified as paper equations. Current execution results are in the [AUD-01 integration validation](../results/checkpoint-aud01/VALIDATION.md); the [ST-04 record](../results/VALIDATION.md) remains historical.

| Investigation | Question |
| --- | --- |
| [VQ-01 / Observation 8](#vq-01-volterra-quadrature-observation-8) | What consistency order does the printed memory quadrature attain? |
| [CF-02 / Observation 2](#cf-02-l1-2-coefficients-observation-2) | Do the printed coefficients represent the stated interpolation? |
| [ST-03 / Observation 1](#st-03-the-contraction-argument-observation-1) | Does the signed-history estimate justify contraction? |
| [ST-04](#st-04-amplification-with-a-positive-time-dependent-kernel) | Can an admissible time-dependent kernel produce amplification? |
| [OB-03 / OB-04](#ob-03-and-ob-04-startup-and-spatial-exactness) | Which startup and spatial exactness claims fail? |
| [SP-01 / SP-02](#sp-01-and-sp-02-conditional-spatial-convergence-and-stability) | What conditional replacement estimates hold? |
| [TM-01](#tm-01-smooth-forced-sharpness-and-initial-layers) | How does the memory defect propagate for smooth forced solutions? |
| [ST-05](#st-05-eventual-contractivity) | Can eventual contraction fail for fixed admissible data? |
| [AUD-01](#aud-01-homogeneous-temporal-sharpness-and-independent-review) | What changes for homogeneous initially singular solutions? |
| [Observations 3–7](#remaining-observations) | What norm, normalization and model qualifications remain? |

## VQ-01: Volterra quadrature (Observation 8)

### Research question

Does the printed quadrature resolve the weak singularity accurately enough to support the claimed consistency order? Fix a spatial point and write

$$
I^n[u]=K(t_n)\int_0^{t_n}(t_n-s)^{-\beta}u(s)\,ds,
\qquad t_n=n\tau,\quad \tau=T/N,\quad 0<\beta<1.
$$

### Published claim

Paper Eq. (6) uses ordinary trapezoids on every panel except the final one, where an endpoint average is multiplied by the exact integral of the singular weight. Paper Eq. (8) and Remark 1 (p.7) give an $O(\tau^{2-\beta})$ quadrature remainder. The combined L1 simplification assumes $\beta\le\alpha$; the quadrature question itself is independent of $\alpha$.

### Independent finding

**Confirmed discrepancy.** Take $T=1$, $K=u=1$, and $n=N\ge2$. The last panel is exact. The immediately preceding ordinary trapezoid overestimates its integral by

$$
c_\beta\tau^{1-\beta},\qquad
c_\beta=\frac{1+2^{-\beta}}2-
\frac{2^{1-\beta}-1}{1-\beta}>0.
$$

Convexity makes every earlier trapezoidal error positive, so cancellation cannot restore the claimed order. The exact panel-error sum converges after division by $\tau^{1-\beta}$ to a positive constant. Thus the constant-input error is $\Theta(\tau^{1-\beta})$.

Propositions 4.1–4.2 and Eqs. (4.3)–(4.5) give the lower bound, exact sum, and asymptotic result. For $u\in C^2([0,T])$ and bounded $K$, the general estimate is

$$
\max_{1\le n\le N}\lvert I^n[u]-Q_\tau^n[u]\rvert
\le C\tau^{1-\beta}.
$$

Here $C$ may depend on $T$, $\beta$, the supremum of $K$, and the stated derivative bounds on $u$, but not on $N$. The constant-input example makes this general order sharp.

### Mathematical significance

The inconsistency is in the remainder claimed for the formula **as printed**. The manuscript also embeds the example in a homogeneous-Dirichlet problem. Multiplication by $\alpha_0=\Gamma(2-\alpha)\tau^\alpha$ gives a contribution of order $\tau^{1+\alpha-\beta}$, subject to the stated residual sign/scaling qualification.

The affected consistency inputs include paper Eqs. (8) and (26), Theorem 3.2, and the combined estimates of Theorem 4.2. A global PDE solution-error rate additionally needs a valid estimate for the discrete evolution; the quadrature counterexample does not itself disprove that convergence theorem.

### Evidence

The manuscript's §4.4 table uses $\beta=.2,.5,.8$. The [independent Python regressions](../scripts/check_counterexamples.py) check the printed rule, exact panel-error identity, sign, rounded table values, and rates. The [Julia suite](../../../../studies/legendre/test/time_and_solver.jl) checks memory refinement; a saved $\beta=.5$ [memory diagnostic](../../../../studies/legendre/figures/memory_diagnostic.csv) provides earlier evidence. The Lean theorem `volterra_half_near_panel_positive` certifies the exact near-panel constant only for $\beta=1/2$.

### Remaining questions

How does this consistency defect propagate through the full PDE scheme? Could a separately analyzed quadrature improve that result? Manuscript §4.6 gives a piecewise-linear product-integration operator bound of $C\tau^2$ under its smoothness assumptions. This is a different rule, used as a control in ST-04; TM-01 gives conditional smooth-data propagation, while a broader improved-order analysis remains open. The original VQ-01 companion program and any unpublished quadrature used by the authors remain unavailable.

## CF-02: L1-2 coefficients (Observation 2)

### Research question

Does collecting the linear-first, quadratic-later interpolation formula give the paper's stated coefficients? Assume a uniform mesh, $0<\alpha<1$, and increments $\Delta u_j=u^{j+1}-u^j$. The evaluation time is $t_{k+1}$; $k=0$ is startup.

### Published claim

Paper Eq. (23) equates a two-sum interpolatory formula to a single sum. Eq. (24) defines the correction weights, Eq. (29) asserts coefficient identities including $d_0=1$, and Eqs. (28)–(32) use them in the recurrence (pp.11–13).

### Independent finding

**Confirmed algebraic discrepancy.** Proposition 5.1 collects the increments exactly. Startup has $d_0^{[0]}=1$. For $k\ge1$,

$$
d_r^{[k]}=
\begin{cases}
b_0+b_0^*, & r=0,\\
b_r+b_r^*-b_{r-1}^*, & 1\le r\le k-1,\\
b_k-b_{k-1}^*, & r=k.
\end{cases}
$$

The middle range is empty for $k=1$; the oldest coefficient depends on the current step. The weights $b_r,b_r^*$ are defined in manuscript Eqs. (5.1)–(5.2). In particular,

$$
b_0^*=\frac{\alpha}{2(2-\alpha)},\qquad
d_0^{[k]}=1+\frac{\alpha}{2(2-\alpha)}>1.
$$

At $\alpha=3/4$, $k=1$, Proposition 5.2 gives $d_0^{[1]}=13/10$ and $d_1^{[1]}=2^{1/4}-13/10<0$. The sign follows from the exact rational comparison $2<(13/10)^4$.

There is also an independent index reversal in the final line of paper Eq. (23): nodal values $(0,0,1)$ give different results in the two expressions. The printed correction-weight range and middle coefficient case both omit a needed $j=1$ entry. The audit records these omissions rather than guessing a completion of an undefined formula.

### Mathematical significance

The history coefficients telescope to $d_0^{[k]}$, rather than one. Dividing the whole equation by this coefficient also rescales diffusion and every history term. Setting only $d_0=1$ defines a different recurrence.

This affects the elliptic coefficient in paper Eq. (31), the history in Eq. (32), normalization in Eq. (29), and subsequent L1-2 stability and convergence arguments. Startup, including paper Eq. (34), is unaffected by the post-startup discrepancy.

### Evidence

The [Julia uniform-increment tests](../../../../studies/legendre/test/time_and_solver.jl) and [coefficient regressions](../../../../studies/legendre/test/proof_audit.jl) exercise the library's interpolation-derived rows. The [Python regressions](../scripts/check_counterexamples.py) keep the printed index-reversal test, corrected collection, analytical panel moments, and unrescaled $d_0=1$ diffusion diagnostic distinct. The [Lean catalogue](../lean/README.md) records exact identities, the negative coefficient, and telescoping results.

The manuscript reports an earlier polynomial/direct-integral comparison whose original Python/Julia/Lean companions are unavailable. The later programs have their own recorded results and are not represented as executions of those missing companions.

### Remaining questions

The authors' implementation is unavailable, so the discrepancy does not identify which conflicting formula their code used. SP-02 supplies conditional finite-time stability of the interpolation-defined recurrence; a negative coefficient alone does not establish instability.

## ST-03: The contraction argument (Observation 1)

### Research question

Can norm bounds on previous states justify contraction when the collected history coefficients have mixed signs?

### Published claim

Theorem 3.1 (pp.15–16) claims $\lVert U_{(q)}^{k+1}\rVert_1\le\lVert U_{(q)}^0\rVert_{L^2}$ for a sufficiently fine temporal mesh, $q=1,2$. The setting is real homogeneous evolution with zero forcing, homogeneous Dirichlet conditions, $0<\alpha,\beta<1$, a positive sufficiently smooth kernel factor, and positive memory coupling. The norm has weight $\alpha_0=\Gamma(2-\alpha)\tau^\alpha$.

The written coefficient induction combines signed histories inside one absolute value; the L1-2 extension is asserted by analogy using paper Eq. (29).

### Independent finding

**Established proof gap.** At a fixed step, suppress $[k]$ and define $h_r=d_r-d_{r+1}$ for $r<k$, $h_k=d_k$. Although $\sum h_r=d_0$, the valid general bound is

$$
\left\lVert\sum_r h_rU^{k-r}\right\rVert
\le\sum_r\lvert h_r\rvert\,\lVert U^{k-r}\rVert.
$$

At $\alpha=3/4$, $k=1$, the CF-02 coefficients give $\lvert h_0\rvert+\lvert h_1\rvert=d_0-2d_1>d_0$. Choosing scalar states $U^0=-1$, $U^1=1$ disproves the inference from norm bounds alone. These are freely assigned states, not a numerical solution trajectory. At $\alpha=1/2$, $k=2$, a negative history coefficient occurs even with positive increment coefficients. Manuscript Eqs. (6.2)–(6.6) and Proposition 6.1 contain the full calculation; Eq. (6.5) retains the Volterra contributions and correct newest-state coefficient.

### Mathematical significance

The signed sum and the sum of absolute values cannot be substituted for one another. Cauchy–Schwarz is not the disputed step, and kernel positivity alone does not supply the missing sign information for the combined coefficients. The same issue occurs in the published L1 argument.

The gap affects the proposed Theorem 3.1 proof and any later temporal error induction, including Theorem 3.2, that relies on it. It does not establish instability or decide the theorem's truth. Indeed, manuscript §6.5 gives a contractive, exactly solved two-step zero-memory reduction.

### Evidence

The [ST-03 script](../scripts/verify_l12_stability.py) compares collected and increment recurrences. The recorded 432 cases have maximum discrepancy `3.77e-15`, against tolerance `2e-11`. Its largest reported weighted amplification, `1.08601376`, is a coarse-grid case with $\beta>\alpha$ and is not a counterexample to the stated fine-grid theorem. The [supplied historical output](../sources/st03_verification_results.txt) and [validation record](../results/VALIDATION.md) distinguish the two executions. Julia regressions test actual library rows; Lean certifies the signed-history inequality, its algebraic counterexample, and normalization identities.

### Remaining questions

SP-02 now provides a finite-time estimate for the corrected coefficients and full Volterra history. It does not justify the original contraction induction. The zero-memory calculation isolates an algebraic issue and does not satisfy all positive-coupling hypotheses of the theorem. Independent L1-2 energy analysis is relevant, but its precise source statements still require verification; see the [literature discussion](../literature/README.md).

## ST-04: Amplification with a positive time-dependent kernel

### Research question

Does a computed trajectory challenge contractivity when the kernel coefficient is smooth and positive but varies with time?

### Published claim

Theorem 3.1 asserts nonamplification in the timestep-dependent norm for sufficiently fine meshes. The cited model assumption allows $K(x,t)>0$ without imposing temporal monotonicity or a time-constant coefficient.

### Independent finding

**Strong finite-grid numerical counterexample candidate.** Manuscript §7 uses the exact Dirichlet eigenmode $\varphi(x)=\cos(\pi x/2)$ on $(-1,1)$, with unit $L^2$ norm and eigenvalue $\sigma=(\pi/2)^2$. Zero forcing and initial amplitude one reduce the PDE and its time-semidiscretizations to a scalar fractional Volterra problem, without spatial approximation. The fixed parameters are

$$
\alpha=.95,\quad\beta=.05,\quad\lambda=1,\quad T=.8,
\qquad K(t)=.05+\frac{500}{1+\exp[-45(t-.3)]}.
$$

Thus $0<\beta\le\alpha<1$, and $K$ is bounded, smooth, and strictly positive. The claimed norm bound becomes $\sqrt{1+\sigma\alpha_0}\lvert a_n\rvert\le1$. Both L1 and interpolation-defined L1-2 exceed it on the tested meshes, using either the printed quadrature or the supplied product-integration control.

### Mathematical significance

Unlike ST-03's freely assigned states, these are recurrence trajectories under the stated parameter and kernel conditions. At $N=4096$, the printed-rule weighted peaks are approximately `2.98087` (L1) and `2.98488` (L1-2). The control indicates that amplification on these meshes is not explained solely by the VQ-01 order defect.

A finite set of meshes cannot refute a theorem asserted only for sufficiently small timesteps. The evidence concerns contractivity; it does not rule out a weaker finite-time stability bound.

### Evidence

The [unchanged ST-04 script](../scripts/verify_time_variable_kernel_st04.py) runs both derivative formulas and both memory rules for $N=128,256,512,1024,2048,4096$: 24 configurations. Its residual check samples six levels per trajectory and provides no rounding enclosures. Julia [library-weight regressions](../../../../studies/legendre/test/proof_audit.jl) independently reproduce the printed-rule case at $N=128$ and check the full residual vector. The [source audit](../ST04_PROVENANCE.md#st-04-parameters-and-evidence) records parameters and checker limitations; supplied historical and later outputs remain separate.

### Remaining questions

An arbitrarily-fine-grid result requires a justified convergence argument or a direct parameter-valid discrete certificate. The manuscript's switched-oscillator calculation at $\alpha=1$, $\beta=0$ is outside the paper's open range. For this original ST-04 construction those steps remain proof obligations. ST-05 treats a separate smooth coefficient and fixed admissible orders; its analytical result is not a proof for the original ST-04 parameters. Small floating-point residuals do not establish convergence to the continuum problem.

## OB-03 and OB-04: startup and spatial exactness

**Research question and published claims.** Can the post-startup Caputo estimate in paper Eq. (26), and the variable-coefficient bilinear equality before Eq. (55), be used uniformly as printed?

**Independent finding.** Proposition 8.1 gives a positive $\Theta(\tau^{2-\alpha})$ error at the second time level for $u=t^2$. This differs from refinement at a fixed positive time. Proposition 9.1 gives an admissible positive smooth spatial coefficient and an explicit nonzero GLL defect for every degree $M\ge3$.

**Mathematical significance.** The startup contribution and spatial quadrature defect must be propagated, rather than omitted. Neither discrepancy alone settles global convergence.

**Evidence and remaining questions.** The exact arguments are in §§8–9. The concrete startup and $M=3$ calculations below are checked by existing library regressions; the latter has exact Lean certificates. The original all-degree/startup companion programs remain unavailable. Higher-order startup and simultaneous-limit conclusions require their own hypotheses.

## SP-01 and SP-02: conditional spatial convergence and stability

**Research question and published claim.** Can spatial and temporal residuals be propagated without the contraction step disputed in Theorems 3.1 and 4.1?

**Independent finding.** SP-01 (§10) retains the quadrature defect and gives fixed-grid spatial propagation, plus a finite-time L1 estimate. SP-02 (§11) proves a uniform finite-time bound for the actual interpolation-defined L1–2 startup and memory rule, using the positive-real convolution symbol and a weighted resolvent. Proposition 11.2 applies it to spatial error.

**Mathematical significance.** These are replacement conditional estimates with constants independent of sufficiently small timesteps, not contraction with constant one. They use a timestep-weighted norm and do not establish uniform standard-$H^1$ stability. Spatial applications require compatible continuous coefficient/product representatives and uniform pointwise nodal bounds; an essential bound alone is insufficient.

**Evidence and remaining questions.** The analytical chain and representative repair were accepted in the [independent review](../reviews/AUD-01/revision-01/REVIEW.md#r1-coefficient-representatives-and-spatial-applications). Lean certifies the symbol numerator/bracket algebra, not the complex resolvent proof. The original numerical SP-02 program is unavailable. Order-uniform constants, simultaneous limits and the cited primary approximation theorem require further qualification.

## TM-01: smooth forced sharpness and initial layers

**Research question and published claim.** Does the solution inherit the lower consistency order, and how should this be compared with Theorem 3.2?

**Independent finding.** Proposition 12.1 proves maximum-over-time $\Theta(\tau^{1-\beta})$ error for a smooth flat manufactured solution with nonzero smooth forcing. Its lower bound uses the signed accumulated residual and a finite summed error equation; its upper bound uses SP-02 or its L1 analogue. Proposition 12.2 separately propagates stated initial-layer derivative bounds.

**Mathematical significance.** This is a standalone consistently forced result. The paper's temporal equations take zero forcing, and the intended smoothness class in Theorem 3.2 is not fully explicit. The comparison is qualified after the standalone theorem, not incorporated as an unproved extra conclusion.

**Evidence and remaining questions.** The analysis is accepted on review; the finite summation identities are Lean-certified. The original failed and corrected TM-01 numerical programs are unavailable, so their printed tables remain historical. Applying the initial-layer bound to a PDE requires its derivative hypotheses, not merely an error experiment.

## ST-05: eventual contractivity

**Research question and published claim.** Theorem 3.1 says both “a sufficiently large number of partitions” and “there exists one” timestep. These differ logically.

**Independent finding.** For the fixed smooth positive kernel and exact fractional orders in §13, Proposition 13.1 proves

$$
\exists N_1\ \forall N\ge N_1\ \exists n_N\in\{1,\ldots,N\}:\quad
\|U_N^{n_N}\|_{\tau_N}>2\|U^0\|_{L^2}.
$$

**Mathematical significance.** This excludes eventual constant-one contractivity, while allowing that an isolated coarse mesh might contract. The L1 convergence argument is independent of SP-02; interpolation-defined L1–2 uses SP-02/TM-01. The printed inconsistent recurrence is not substituted for that scheme. The construction is separate from ST-04 and compatible with finite-time boundedness using a larger constant.

**Evidence and remaining questions.** The exact oscillator calculation, smoothing, fixed-order perturbation and convergence transfer were accepted analytically. Lean covers the listed oscillator calculus and rational constants, not the complete transfer argument. The distinct 36-configuration ST-05 program remains unavailable. Practical decimal-pair observations do not certify the exact orders $1-2^{-600},2^{-600}$ or eliminate all coarse grids.

## AUD-01: homogeneous temporal sharpness and independent review

**Research question and published claim.** Can a zero-forcing problem show the memory order at solution level, and does this settle the smooth homogeneous interpretation of Theorem 3.2?

**Independent finding.** Proposition 14.1 gives homogeneous initial-layer sharpness $\Theta(\tau^{1/2})$ for $\alpha=3/4$, $\beta=1/2$, $T=2^{-10}$. The positive constant-kernel Neumann solution and accumulated residual establish the standalone result. Its upper bound retains the TM-01/SP-02 dependencies.

**Mathematical significance.** This solution is initially singular. It must remain separate from TM-01's smooth forced solution; together they do not make one smooth homogeneous counterexample.

**Evidence and remaining questions.** The unchanged supplied exact and homogeneous programs pass their original criteria. The homogeneous tested grids show last-doubling rates **0.7498**, negative total signed residuals and positive memory residuals. They do not numerically establish the half-order asymptotic regime. The [accepted review](../reviews/AUD-01/revision-01/REVIEW.md) and [source inventory](../reviews/AUD-01/revision-01/DIAGNOSTIC_INVENTORY.md) retain the analytical, finite-grid and missing-source distinctions. Full formal verification of these PDE arguments is not claimed.

## Remaining observations

### Observation 3: L1-2 startup consistency

**Research question.** Does linear interpolation on the first panel limit a claimed higher-order estimate at early steps?

**Published claim.** Paper Eq. (26), p.12, includes a post-startup Caputo consistency component of order $3-\alpha$.

**Independent finding.** The verified OB-03 calculation uses $u(t)=t^2$, a uniform mesh, and $0<\alpha<1$. At the fixed early index $n=2$, the first-panel error is

$$
\frac{\tau^{2-\alpha}}{\Gamma(1-\alpha)}
\int_0^1(2z-1)(2-z)^{-\alpha}\,dz.
$$

The integral is nonzero, while interpolation on the quadratic second panel is exact.

**Mathematical significance.** A uniform early-step estimate needs a startup qualification; refining at $n=2$ differs from refining at a fixed positive physical time. Subsequent temporal estimates must account for startup propagation.

**Evidence.** The Julia suite's startup tests compare the full interpolatory derivative with analytical moments; Python regressions compare panel moments and collected coefficients. These are included in the recorded checkpoint checks.

**Remaining questions.** Proposition 8.1 proves the early-step discrepancy; this is not by itself a global solution-error result. TM-01 handles startup within its separate smooth and initial-layer assumptions.

### Observation 4: Variable-coefficient spatial quadrature

**Research question.** Does the polynomial exactness of GLL quadrature justify the mass-form equality when a coefficient varies in space?

**Published claim.** Theorem 4.1, immediately before paper Eq. (55), p.23, uses $B(R_M,\rho_M)=B_M(R_M,\rho_M)$ for $R_M\in P^0_{M-1}$. An $(M+1)$-node GLL rule is exact through degree $2M-1$.

**Independent finding.** For $M=3$, take $R_M=1-x^2$, $\rho_M=x(1-x^2)$, and $K=1+cx$, with mass coefficient $\widehat R=1+\eta(1+cx)$, $0<c<1$, $\eta>0$. This has the required positive-kernel form. Both test functions vanish at the endpoints. The exact mass integral is $16\eta c/105$, whereas four-point GLL quadrature gives $16\eta c/75$: an absolute difference $32\eta c/525$. The constant part integrates to zero in both rules. The degree-six even term exceeds the rule's degree-five exactness; the admissible-degree derivative product does not remove this discrepancy.

**Mathematical significance.** The concrete polynomial calculation is certified. Proposition 9.1 extends the analytical exactness discrepancy to every $M\ge3$; SP-01/SP-02 supply conditional spatial estimates with an explicit defect. It concerns a cancellation used by Theorem 4.1 and the combined estimates of Theorem 4.2.

**Evidence.** Exact-rational Python calculations, Julia tests of actual nodes and weights at $c=1/2$, and the [Lean integral certificate](../lean/README.md) establish this example. These checks were executed in the ST-04 record; they are distinct from the original manuscript's earlier program descriptions.

**Remaining questions.** The replacement estimates require spatial/product regularity and continuous coefficient representatives with uniform nodal bounds. Their hypotheses and constants must be checked in each PDE application; they do not validate the original cancellation.

### Observation 5: The timestep-dependent norm

**Research question.** How should stability in the paper's weighted norm be interpreted as the timestep tends to zero?

**Published claim.** Paper Eq. (2), p.5, uses

$$
\lVert v\rVert_1^2=\lVert v\rVert_{L^2}^2+
\alpha_0\lVert v_x\rVert_{L^2}^2,
\qquad\alpha_0=\Gamma(2-\alpha)\tau^\alpha,
$$

with $\alpha_0$ defined on p.8.

**Independent finding.** For fixed $\tau>0$, $0<\alpha<1$, this norm is equivalent to the standard $H^1$ norm, but its equivalence constants degenerate as $\tau\downarrow0$.

**Mathematical significance.** A weighted estimate cannot automatically be read as a uniform standard-$H^1$ estimate. This remains an interpretation caveat for stability, convergence, and comparisons with numerical H1 errors.

**Evidence.** The manuscript gives the norm argument. Lean certifies an abstract two-component energy statement; the library's reported H1 metric uses an unweighted gradient, as documented in [error_norms](../../../../src/Solver.jl).

**Remaining questions.** The abstract certificate does not formalize a Sobolev-space theorem. A uniform standard-$H^1$ result must be established on its own hypotheses.

### Observation 6: Numerical error normalization

**Research question.** Are the reported errors directly comparable to conventional spatial norms?

**Published claim.** Section 6, p.28, uses Lobatto weights and an additional spatial averaging factor $(M+1)^{-1}$, with averaging over sampled time levels.

**Independent finding.** The quadrature weights already account for spatial integration. The extra factor introduces a resolution-dependent scale; samples on a graded time mesh are not automatically a quadrature for a time integral.

**Mathematical significance.** Normalization affects comparisons and apparent spatial rates. This is a reproduction/interpretation check, not an established error in all reported tables.

**Evidence.** The library retains the printed L2 and H1 definitions, reports `space_time_L2` without the extra spatial-node divisor, and tests normalization using a known constant offset. Existing CSVs preserve the original comparisons.

**Remaining questions.** The paper's H1 gradient evaluation and 2D normalization convention remain ambiguous. The observation prescribes no fitted replacement metric; the numerical H1 column must also be distinguished from the theoretical weighted norm.

### Observation 7: Kernel positivity and the examples

**Research question.** Which numerical examples satisfy the positivity assumptions of the stability proof?

**Published claim.** The model on p.5 and Theorem 3.1 require a strictly positive smooth factor. Example 6.2, p.33, uses $K=x$ on $(-1,1)$ with $\lambda=1$.

**Independent finding.** That factor is negative on part of the domain. The example therefore does not test the theorem under its positivity assumptions. This retains the status of an assumptions check.

**Mathematical significance.** The scope of the theorem and the scope of the computed examples must be assessed separately.

**Evidence.** The [case definition](../../../../studies/legendre/cases.jl) preserves `coefficient=(p,t)->p[1]`. Earlier repository notes also discuss Example 6.1's $\sin x$ factor; that context is separate from this observation.

**Remaining questions.** No stability extension to sign-changing kernels, or instability result for them, is established here.

## Next research steps

Recover the unavailable original companions and check the cited primary-reference locators. Clarify the original theorem's forcing, regularity and quantifier interpretation before making broader comparisons. Existing replacement estimates retain fixed-order, uniform-grid, product-regularity and weighted-norm assumptions. ST-04's own all-fine-grid question remains distinct from the accepted ST-05 construction; numerical agreement alone cannot settle it.
