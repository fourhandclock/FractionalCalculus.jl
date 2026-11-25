# AUD-01 independent mathematical review

This review examines the supplied AUD-01 manuscript against its equations, the original Sabawi et al. paper, and new Lean certificates. It does not take the preceding internal audit or successful finite tests as proof. The supplied manuscripts, programs, outputs, and production numerical library are preserved.

**Overall judgment.** The principal analytical chains withstand the checks described below under their explicit strong hypotheses. SP-02 supplies a finite-time bound rather than contractivity; TM-01 and AUD-01 give different sharpness examples; ST-05 gives an analytically supported all-fine-grid challenge to the sufficiently-fine-grid interpretation of Theorem 3.1. There is a repair needed in SP-01's weaker nodal-coefficient formulation, and important qualifications remain in comparing the error examples with the paper's temporal regularity assumptions. Numerical replay is separately reported below; it is not inferred from historical outputs.

## Sources, locators, and classifications

The principal source is [the supplied AUD-01 TeX](../../../../../AUD01_review_package/aud01/legendre_spectral_verification_notes_aud01.tex), with [its PDF](../../../../../AUD01_review_package/aud01/legendre_spectral_verification_notes_aud01.pdf). The separate [addendum](../../../../../AUD01_review_package/aud01/audit_addendum.tex) duplicates §14, and the [earlier ST-05 audit](../../../../../AUD01_review_package/aud01/ST05_proof_audit.md) is historical supporting material, not independent confirmation. Locators below give manuscript sections, labels, and TeX line numbers. Published-paper locators refer to [the original 46-page PDF](../../../../../YS_SS_PD_NM_25_Calcolo.pdf), not the notes.

- **Accepted on review:** the analytical derivation checks under the stated scope. This is a review judgment, not a Lean certificate or external peer review.
- **Repair required:** a hypothesis, interpretation, or reproducibility statement needs the specified correction before the broader claim is used.
- **Unresolved:** the available source or evidence does not decide the question.
- **Formally certified:** the exact listed Lean proposition compiled and its axioms were audited. This label does not extend to its surrounding analytical proof chain.

All seven entries in the supplied `SHA256SUMS` match. The review records hashes of all package files, including those outside that manifest. An existing repository discrepancy predates this review: the ST-04 PDF is missing at its manifest path, while `sources/legendre_spectral_verification-3.pdf` is present. Neither is restored, renamed, or treated as interchangeable here.

## Result register

| Result | Classification | Scope and dependencies |
| --- | --- | --- |
| SP-02 stationary convolution and startup correction | Accepted on review | Exact interpolation-defined recurrence, uniform grid; genuine first step retained |
| SP-02 positive-real symbol and two-sided estimates | Accepted on review; polynomial numerator/bracket formally certified | Fixed $0<\alpha<1$; integral and complex estimates remain analytical |
| SP-02 weighted resolvent and coefficient extraction | Accepted on review | Nonnegative self-adjoint $A$, uniform in its spectrum; timestep-weighted norm |
| SP-02 initial data and finite-time absorption | Accepted on review | Bounded nonnegative self-adjoint $K_n$, fixed finite $T$, sufficiently small $\tau$ |
| TM-01 smooth memory asymptotic and accumulated residual | Accepted on review | Smooth amplitude, consistently forced scheme, fixed parameters |
| TM-01 solution-error lower bound | Accepted on review | Maximum over time; uses summed error equation, not the disputed contraction theorem |
| TM-01 general initial-layer upper bound | Accepted on review | Stated derivative bounds and SP-02/L1 analogue; no automatic PDE regularity theorem |
| AUD-01 homogeneous Neumann solution and positivity | Accepted on review | Fixed constant kernel and small final time; rational contraction inequality formally certified |
| AUD-01 homogeneous $\Theta(\tau^{1/2})$ error | Accepted on review | Natural initial layer; not a classically time-smooth homogeneous example |
| Comparison with Theorem 3.2 under unstated regularity | Unresolved | Forced smooth and homogeneous initially singular examples do not share all hypotheses |
| ST-05 endpoint oscillator and smoothing | Accepted on review; listed oscillator identities formally certified | Exact endpoint is intermediate, not the admissible fractional example |
| ST-05 fractional perturbation and regularity | Accepted on review | Exact fixed orders $1-2^{-600},2^{-600}$; constants may be enormous |
| ST-05 independent L1 convergence and fine-grid transfer | Accepted on review | Does not use SP-02 or Theorem 3.1; uses the verified interpolation residual bounds |
| ST-05 interpolation-defined L1-2 conclusion | Accepted on review | Additionally depends on SP-02/TM-01; excludes the inconsistent printed collection |
| Literal existential reading of Theorem 3.1 | Unresolved as a theorem comparison | The accepted challenge addresses “sufficiently large number of partitions,” not a bare existence of one mesh |
| SP-01 projection, residual, fixed-grid estimate, L1 propagation | Accepted on review | Strong spatial/product regularity, consistent forcing, continuous Sobolev representatives |
| SP-01 weaker `L∞` nodal formulation | Repair required | Specify pointwise representatives and nodal bounds; see R1 |
| Historical SP-02/TM-01/ST-05 diagnostic claims | Unresolved as independently replayed results | Several named companion scripts/outputs are absent; see R3 |
| Supplied symbolic and homogeneous diagnostics | Unresolved pending local dependency acquisition | Exact versions absent; historical outputs are preserved, not counted as fresh runs |

## SP-02: convolution, resolvent, and finite-time stability

**Locators:** §11, `prop:sp02-stability`; `eq:sp02-start`, `eq:sp02-RHS`, `eq:sp02-symbol`, `eq:sp02-positive`, `eq:sp02-symbol-bounds`, `eq:sp02-green`, `eq:sp02-volterra-bound`; TeX lines 1035–1141. The spatial application is `prop:sp02-spatial`, lines 1144–1159.

### Startup is part of the scheme

With $c_{-1}=0$ and $a_r=b_r+c_r-c_{r-1}$, the stationary convolution contributes an extra $c_{n-1}\Delta u^1$ compared with the true linear-first-panel rule. Subtracting it gives

$$
\alpha_0D_{\tau,L12}u^n=\sum_{j=1}^n a_{n-j}\Delta u^j-c_{n-1}\Delta u^1.
$$

At $n=1$, $a_0-c_0=1$, so startup remains L1. For $X(z)=\sum_{n\ge1}u^nz^{n-1}$, the convolution of increments is $\delta X-A(z)u^0$. Thus the initial-data term on the inverted equation's right side is **plus** $a_{n-1}u^0$, and the correction is **plus** $c_{n-1}\Delta u^1$. The sign and index in the manuscript are correct. This calculation is formal in the power-series sense; it does not require the solution sequence to have an analytic generating function.

### Positive real part and quantitative symbol bounds

The Laplace density is positive and finite, behaving as $x^{\alpha-1}$ near zero and $x^{\alpha-2}$ at infinity. The panel-weight ratio satisfies $0\le q(x)\le1/2$ by pairing $v$ and $1-v$ in its defining integral. The unit-circle numerator is

$$
(1-\cos\theta)\{1+\rho+2q(\rho-\cos\theta)\}.
$$

Its bracket minus $2\rho$ equals $(1-2q)(1-\rho)+2q(1-\cos\theta)\ge0$. The corrected cross-term sign is essential. Both polynomial identities are now Lean-certified; the extension from each fixed integrand to the symbol uses the analytical harmonic minimum principle and integrability.

For $s=|1-z|$, the denominator obeys $|1-\rho z|\gtrsim x+s$ on $0<x\le1$. Integrating $x^{\alpha-1}/(x+s)$ gives the claimed $s^{\alpha-1}$ upper bound, and differentiating adds one denominator. For the lower bound, restricting $\operatorname{Re}B$ to $x\in[s,2s]$ when $s\le1/2$ gives $c_\alpha s^{\alpha-1}$. The positive real part of $(1-z)C$ prevents its cancellation. The large-$s$ range is handled on a fixed positive interval of $x$. Consequently the two-sided $|\delta|\asymp s^\alpha$ estimate and $|\delta'|\lesssim s^{\alpha-1}$ are justified throughout the open unit disk. “Moments” here should be read as the exponential moments defining $b_r,c_r$, rather than arbitrary polynomial moments in $x$.

### Weighted resolvent and Cauchy extraction

For every spectral value $y\ge0$, positivity of $\operatorname{Re}\delta$ gives

$$
|\delta+y|\ge (|\delta|+y)/\sqrt2.
$$

Applying this to $G=(\delta I+\alpha_0A)^{-1}$ and $Q=(I+\alpha_0A)^{1/2}G$ yields the stated uniform spectral bounds. In particular, $Q'=-\delta'QG$ has size $O(s^{-1-\alpha})$. The weighted bound is necessary: a scalar symbol estimate alone would not establish the spatial-energy conclusion. No commutation of $K_n$ with $A$ is used.

On the circle $r=e^{-1/k}$, integration by parts in Cauchy's angular coefficient integral supplies the factor $1/k$. The remaining integral is $O(k^\alpha)$ because $|1-re^{i\theta}|\gtrsim k^{-1}+|\theta|$. Therefore $\|G_kv\|_\tau\lesssim(k+1)^{\alpha-1}\|v\|$. The periodic boundary term vanishes. The zeroth coefficient must, and does, receive its separate estimate. For unbounded $A$, positivity and the resolvent identity justify the bounded weighted resolvent; the finite triangular recursion supplies the coefficient identity on the operator domain.

### Initial data and memory absorption

The true first-step energy estimate bounds $\Delta u^1$ by the unweighted initial norm and forcing, without assuming initial spatial energy. The initial-data convolutions are controlled by the discrete beta-type sum

$$
\sum_{j=1}^n(n-j+1)^{\alpha-1}j^{-\alpha}\le C_\alpha.
$$

Bounding memory by $L\max_{i\le j}E_i$ is valid from its nonnegative scalar weights and bounded multiplier. The short-block estimate absorbs the current block after choosing its physical length independently of $\tau$. The number of blocks is bounded independently of $N$. This establishes the finite-time constant $C_{\alpha,T,L}$, not the constant one, a bound uniform in $T$, an $\alpha$-robust estimate, or a uniform ordinary-$H^1$ bound. It is compatible with ST-05 amplification.

## TM-01: accumulated residual and temporal lower bound

**Locators:** §12, `eq:tm01-quad`, `eq:tm01-res-sum`, `prop:tm01-sharp`, `eq:tm01-error`, `prop:tm01-singular`, `eq:tm01-layer`; TeX lines 1178–1273.

### Leading memory error and forcing

For a $C^2$ amplitude, subtracting $a(t_n)$ from each panel isolates the positive constant-input defect. The remainder has second derivative bounded by $C[(t_n-s)^{-1-\beta}+(t_n-s)^{-\beta}]$. Its old-panel errors sum to $O(\tau^{2-\beta}+\tau^2)$, and its final-panel error is $O(\tau^{2-\beta})$. Since $0<\beta<1$, the claimed uniform expansion follows:

$$
Q_\tau^n[a]-J[a]\,(t_n)=\tau^{1-\beta}C_{\beta,n}a(t_n)+O(\tau^{2-\beta}).
$$

For the flat amplitude $a(t)=\exp(1-1/t)$, extended by zero at the origin, moving derivatives through the forcing integrals creates no endpoint terms: all derivatives of the integrands vanish at zero. The forcing is smooth, but is **nonzero**. The counterexample concerns a consistently forced extension, not automatically the literal homogeneous equations (19)/(37). The added §14 correctly makes this qualification.

The Caputo residual is uniformly $O(\tau^{2-\alpha})$ for the stated smoothness; retaining the first linear panel in L1-2 is necessary. This is $o(\tau^{1-\beta})$. Restricting the Riemann sum first to $t\ge\epsilon$ justifies uniform convergence of $C_{\beta,n}$ there; uniform boundedness controls the omitted short interval. The resulting positive **signed integrated residual** is stronger evidence for the lower-bound argument than a pointwise maximum of local defects.

### Finite summation and the error equation

The L1 summation-by-parts identity retains the initial boundary term, which disappears only because $e^0=0$. For the quadratic correction, writing $v_j=\Delta e^{j+1}$ gives the exact all-length identity

$$
\sum_{n=0}^{m-1}\sum_{j=0}^n c_{n-j}(v_{j+1}-v_j)
=\sum_{j=0}^{m-1}c_{m-1-j}v_{j+1}
 -\left(\sum_{r=0}^{m-1}c_r\right)v_0.
$$

This identity, previously tested only at finitely many lengths, is now Lean-certified for every $m\in\mathbb N$. Its coefficient absolute sum is $2P_{N-2}$, and $|\Delta e^j|\le2E$ gives the manuscript's conservative factor three for the complete L1-2 derivative. Nonnegative bounded-mass memory weights then give the summed error-equation bound. No stability theorem is required to deduce $E\ge c\tau^{1-\beta}$ from the positive accumulated residual. The weighted eigenmode norm is at least the scalar amplitude error. Flatness makes the first-step error superalgebraically small, so excluding startup does not remove this lower bound.

The matching smooth upper bound does depend on SP-02 (or its L1 analogue). It proves a maximum-over-time $\Theta$ statement, not a lower bound at every fixed positive time.

### Initial layers

The residual estimate $\|r_D^n\|\lesssim\tau^{\gamma-\alpha}(n^{-1-\alpha}+n^{\gamma-2})$ is justified with only the two stated derivative bounds. Endpoint interpolation errors vanish in the integration by parts; the final-panel error must use its extra factor $t_n-s$. Splitting the old-panel sum controls both summable powers for fixed $0<\alpha,\gamma<1$.

The Green factor is at most one before summing this residual. The direct derivative-error contribution is therefore $O(\tau^\gamma)$, while the memory residual gives $O(\tau^\gamma+\tau^{1-\beta})$. The genuine first step controls the additional L1-2 startup source. Applying the same block absorption proves the claimed upper bound. This is conditional regularity-to-error propagation, not a proof that every PDE solution has those derivative bounds. Its constants can depend on fixed orders and regularity; it is not a graded-grid result.

## AUD-01: homogeneous sharpness and the constant-kernel reference

**Locators:** §14, `prop:aud01-homogeneous`, TeX lines 1424–1476; standalone addendum lines 8–57.

For $\alpha=3/4$, $\beta=1/2$, $T=2^{-10}$, $K=\lambda=1$, the commuting fractional integrals yield the stated double Neumann series with exponent $\ell\alpha+k(1-\beta)$ and denominator $\Gamma(1+\ell\alpha+k(1-\beta))$. The binomial coefficient and power $\Gamma(1-\beta)^k$ are correct. The supremum-norm contraction bound uses

$$
T^\alpha<1/128,\quad\Gamma(7/4)>4/21,\quad\sigma<3,\quad2\sqrt T=1/16.
$$

The rational comparison of these bounds with $1/4$ is certified. The gamma lower bound follows by integrating on $(0,1)$ and using $e<3$. Thus the Neumann remainder has the stated geometric amplitude bound and $a\ge2/3$. That supremum-norm truncation estimate alone is not a bound for truncated derivatives; the regularity argument and numerical residual checks have separate roles.

The differentiated constant-coefficient series gives $|a^{(j)}(t)|\lesssim t^{\alpha-j}$ and $\alpha$-Hölder continuity. Freezing each ordinary-panel value incurs $O(\tau^\alpha)$ times bounded total kernel mass. Replacing frozen values by $a(t_n)$ adds a convergent sum $\tau^{1-\beta+\alpha}\sum r^\alpha c_{\beta,r}$. Hence the leading memory defect has the asserted positive sign. The derivative residual satisfies $\tau\sum|r_D^n|=O(\tau)$, which is smaller than $\tau^{1/2}$. Positivity of $a$ then prevents cancellation of the limiting signed accumulated residual.

The finite summation bound gives the lower solution-error order without SP-02. The upper order uses TM-01/SP-02. The first-step error is $O(\tau^{3/4})=o(\tau^{1/2})$, so restricting L1-2 to $n\ge2$ preserves the lower bound. The standalone homogeneous $\Theta(\tau^{1/2})$ statement is accepted on review.

This is an initially singular homogeneous solution. The smooth forced TM-01 example and this example cannot be combined into one classically smooth homogeneous counterexample. With bounded $u_t$ near zero and continuous $Au(t)$ at zero, the homogeneous equation would force $Au(0)=0$; for the Dirichlet Laplacian this gives zero initial data. Comparison with a smooth-solution interpretation of Theorem 3.2 therefore remains conditional; see R2.

### Finite-grid observations

The **supplied historical output**, not a fresh replay, reports rates `0.7498` at the last doubling for both methods. At $N=4096$ it reports errors `5.0190267127e-06` and `4.8350130274e-06`, with negative normalized total residuals but positive normalized memory residuals near `3.8361747868e-05`. This is compatible with dominance of the initial-layer contribution on the tested range. It does not numerically establish an exponent of $0.5$. The positive limiting signed residual is an analytical conclusion, not an observed sign on these grids.

## ST-05: endpoint, smoothing, fractional perturbation, and transfer

**Locators:** §13, `eq:st05-endpoint`, `eq:st05-K`, `eq:st05-smoothing`, `eq:st05-contraction`, `eq:st05-orders`, `eq:st05-reg`, `eq:st05-convergence`, `prop:st05`; TeX lines 1302–1401.

### Exact oscillator and logistic smoothing

In the critically damped first interval, $y=te^{-\gamma t}$ gives $y(t_*)=e^{-1}/\gamma$ and $a(t_*)=0$. Differentiating the second-interval formula at its quarter-period gives exactly

$$
a_*(t_a)=-(16+1/16)e^{-1-\pi/32}.
$$

The position/velocity identities and differentiation are certified in Lean. The further numerical inequality $a_*(t_a)<-4$ is accepted analytically using the manuscript's elementary $\pi$ and exponential bounds; it is not one of the formal certificates.

For the dimensionless system, the energy identity is $d(\kappa X_1^2+X_2^2)/dr=-4X_2^2$ on a constant-coefficient interval. This gives a Euclidean propagator bound at most $\sqrt{257}<17$ after the switch; intervals crossing it introduce no additional factor beyond the product of the two interval bounds. The logistic-tail integral is at most $512\log2/m<512/m$. Variation of constants relative to the switched propagator gives the denominator $1-Dd_0$, and the stated rational estimates imply an amplitude change below $1/4$. The fixed smooth endpoint solution is therefore below $-15/4$ at $t_a$.

### Fractional perturbation uses fixed, admissible orders

The weighted norm with $p=256$ gives the uniform contraction factor $31/128<1/4$ on $\alpha\in[3/4,1]$, $\beta\in[0,1/4]$. The multiplication by $K$ is bounded before convolution, so commutation with fractional integration is not assumed for variable $K$.

The kernel order derivative estimate follows from $1/\Gamma(q)<3$ and $|\Gamma'(q)|/\Gamma(q)^2<27$, yielding $3/q^2+27/q<50$. The unnormalized memory-kernel derivative has integral $(1-\beta)^{-2}<2$. These imply the conservative $30000\varepsilon$ operator perturbation bound and $720000e^{256}\varepsilon$ solution bound after norm conversion.

For the exact rational $\varepsilon=2^{-600}$, the estimate using $e^{256}<2^{512}$ is below $2^{-68}$. The coefficient and both fractional orders are fixed before letting $N\to\infty$. Ordinary binary64 would round $1-2^{-600}$ to one; none of the numerical decimal-pair evidence certifies this exact analytic parameter pair. The rational inequalities are certified; the gamma/exponential kernel bounds remain analytical.

### Regularity and the independent L1 convergence argument

The fixed-simplex representation of each Neumann word separates the factor $t^\nu$ from bounded derivatives of $K(t\theta)$. Differentiating twice creates polynomial factors in word length, while gamma denominators dominate the exponentially many words. This justifies local uniform differentiation for $t>0$ and the bounds $|a^{(j)}(t)|\lesssim t^{\alpha-j}$. Absolute continuity and the fractional semigroup identity then recover the Caputo equation. Classical differentiability at zero is neither obtained nor used.

For L1, the inverse coefficients are nonnegative and at most one because $b_j$ decreases. Their convolution with $b_j$ equals one, giving $\sum_{j<k}p_j\le k^\alpha/(1-\alpha)$. The derivative residual is summable for the fixed order. These two different inverse-coefficient bounds control the derivative and memory residuals respectively. A physical block length chosen after the fixed parameters absorbs the remaining diffusion/memory error, including the current error term. Constants and the sufficient grid threshold may be extremely large; their uniformity as $\alpha\uparrow1$ is not required.

Thus the L1 convergence proof is independent of SP-02. L1-2 additionally uses SP-02/TM-01. A nearest-grid-point sequence converges to the strict continuous amplitude below $-11/4$, so every sufficiently fine grid has amplitude greater than two in modulus. The timestep-dependent spatial norm factor is at least one. This is a valid transfer to the time-semidiscrete PDE eigenmode, without invoking a spatial spectral approximation.

The conclusion challenges constant-one contractivity for the permitted time-dependent positive coefficient. It does not imply unbounded growth, failure of a problem-dependent finite-time bound, or a result for constant/nonincreasing kernels. The original ST-04 kernel and practical decimal pairs remain numerical examples distinct from this analytic construction.

## SP-01: spatial projection and quadrature consistency

**Locators:** §10, `eq:sp-proj`, `eq:sp-quad`, `eq:sp-error`, `eq:sp-R`, `prop:sp-fixed`, `prop:sp-l1`; TeX lines 926–1029. The SP-02 application is lines 1144–1159. OB-04's all-degree construction is §9, `prop:ob04-allM`, lines 792–832.

The derivative Ritz projection is constructed correctly by projecting $u'$ onto $\mathbb P_{M-1}$ and integrating. Projection preserves its zero mean, so both endpoint conditions hold. The resulting $H^1$ approximation uses the standard Legendre approximation estimate. Exactness for the product of a degree-$M-1$ approximant with a degree-$M$ test polynomial yields the stated quadrature bound through the one-dimensional $H^1\hookrightarrow C^0$ embedding and positive GLL weights.

Ritz orthogonality cancels stiffness, not mass quadrature. The residual identity retains the forcing quadrature error, the derivative of the projection error, and all coefficient-weighted histories. Its bound genuinely requires product regularity and $A_\tau=\max\|D_\tau U^n\|_{H^m}$, not just unweighted spatial regularity of $U^n$.

The absolute-history induction gives a finite constant on a fixed temporal grid; it does not become uniform merely by being finite. The L1 comparison barrier uses positivity of the L1 history weights and the lower kernel bound over a short time block. Its iteration gives the stated timestep-independent prefactor with the displayed $\tau^{-\alpha}$ factor. For L1-2, SP-02 supplies propagation; monotonicity of $c_r$ bounds the collected second-difference correction and gives $\alpha_0 A_\tau\le(2+4c_0)S$.

The replacement estimates are conditional on their stronger product/forcing assumptions. They apply to the exact-derivative weighted norm, and to ordinary $H^1$ only at fixed $\tau$. A literal nodal evaluation of the nonpolynomial derivative requires $m>3/2$, as the manuscript recognizes. A joint limit still requires control of $S,F,A_\tau$ or a compatible refinement relation.

The OB-04 all-degree defect is also accepted: $(1-x^2)(P'_M)^2$ vanishes at every GLL node, and its leading coefficient and exact positive integral give the stated $D_M$. The polynomials vary with $M$ and the defect decays exponentially; this does not refute a convergence rate for one fixed smooth solution. The updated admissible mass coefficient $1+\eta(1+cx)$ is important; mere positivity of $1+cx$ did not by itself give $1+\eta K$ with $K>0$.

## Repairs and unresolved source comparisons

### R1 — `L∞` data do not determine nodal multiplication

**Locator:** §10.1, line 931, the “more generally” clause; consequences for `eq:sp-quad`, `eq:sp-R`, `prop:sp-fixed`, `prop:sp-l1`, and the spatial application of SP-02.

An $L^\infty$ function is an equivalence class, and changing it at finitely many quadrature nodes changes neither its essential bound nor weak product Sobolev norms. Yet such changes alter nodal multiplication. For example, on the $M=2$ Lobatto grid let $u=v=1-x^2$, and let $K_L=1$ except $K_L(0)=L>0$. Then $K_L=1$ almost everywhere and its Sobolev product class with $u$ is unchanged, but

$$
Q_2[K_Luv]-\int_{-1}^1K_Luv
=\frac43L-\frac{16}{15}.
$$

It is unbounded as $L$ grows despite the unchanged essential and Sobolev-class bounds. This illustrates a representative ambiguity, not a counterexample under the original smooth-kernel hypothesis.

**Required repair:** specify continuous representatives where the regularity permits them, or explicitly assume pointwise nonnegative nodal values bounded uniformly in $M,n$ and identify the sampled product with its intended Sobolev representative. The concrete $W^{m,\infty}$ case with its continuous representative and integer $m\ge2$ satisfies the needed convention. The abstract SP-02 theorem assumes an actual bounded operator $K_n$ and is unaffected. The weak SP-01 generalization must not inherit uniform nodal constants from an essential supremum without this clarification. ST-05 uses a smooth spatially constant coefficient and is unaffected.

### R2 — Theorem matching requires two separate qualifications

Paper p.5 expressly sets $f=0$ in the temporal construction, while discussing general forcing for full discretization. Theorem 3.2 on p.16 names (19)/(37). Its displayed statement does not enumerate bounded classical time derivatives, but its consistency argument uses solution-dependent smoothness bounds. The smooth forced TM-01 example and initially singular homogeneous AUD-01 example each answer a different version of the question. Neither alone proves failure for a classically time-smooth homogeneous solution class. The AUD-01 addendum correctly recognizes this; any summary claiming a single example meets both sets of assumptions requires repair.

Paper Theorem 3.1, p.15, says “for a sufficiently large number of partitions” but then says “there exists one Δt > 0.” ST-05 establishes a violation for **every sufficiently large integer $N$**, so it refutes the intended fine-grid nonamplification interpretation. It does not negate the logically weaker bare existential claim that one isolated mesh contracts. An assessment of the theorem should quote both wordings and state the interpretation used.

The spatial comparison also uses consistently scaled, unscaled-PDE forcing in SP-01. This should not be identified automatically with the general-source forms printed in paper Eqs. (49)–(53), whose source scaling/indexing is ambiguous. The homogeneous and explicitly consistently forced statements should remain separate.

### R3 — Missing companion programs limit reproducibility

The package supplies `check_exact_aud01.py` and `verify_aud01_homogeneous.py`. Programs named for SP-02, TM-01, ST-05, OB-03, and OB-04 in the manuscript are not present in the searched repository/package. In particular, `verify_sp02_resolvent.py`, `verify_l12_startup_obs03.py`, and `verify_gll_variable_coefficient_obs04.py` cannot be replayed from these inputs. References to the earlier failed TM-01 diagnostic and corrected source/output likewise lack their actual files here. These manuscript cross-references need a complete source/output manifest for local replay.

The manuscript's matrix, symbol-grid, sharpness-control, and practical ST-05 decimal-pair numbers therefore remain **historical reported evidence**, not independently replayed results of this review. This does not invalidate the analytical arguments, but it prevents those numerical claims from being counted as reproduced. The Canuto–Quarteroni Theorem 2.3 locator and precise ETNA related-work statements also have not been independently checked against supplied primary texts; they are not imported as formal dependencies of the new certificates.

## Formal certificates

The existing Lean 4.19.0/mathlib v4.19.0 project and dependency lock are reused. The supplied aggregate `import Mathlib.Tactic` has no compiled aggregate cache locally. [AuditConstants.lean](../../lean/AuditConstants.lean) therefore narrows imports to cached modules; every supplied theorem statement and proof body from its namespace onward is unchanged. The package original is preserved. No dependency update or full mathlib build was performed.

All 19 new propositions compiled, and [Aud01Axioms.lean](../../lean/Aud01Axioms.lean) printed their dependencies. Every output lists only `propext`, `Classical.choice`, and `Quot.sound`. No `sorry`, `admit`, `sorryAx`, or new unsupported axiom is accepted. Failed development attempts and their exact sources remain in the new results directory.

| Module/theorem | Precisely certified claim |
| --- | --- |
| `AuditConstants.symbol_numerator` | The stated real-polynomial numerator equals $(1-x)(1+\rho+2q(\rho-x))$ whenever $y^2=1-x^2$ |
| `symbol_bracket` | $2\rho\le1+\rho+2q(\rho-x)$ for $0\le\rho\le1$, $0\le q\le1/2$, $x\le1$ |
| `smoothing_denominator` | $1-17(512/10^6)>0$ in $\mathbb Q$ |
| `smoothing_amplitude` | $17/[1-17(512/10^6)]<18$ |
| `smoothing_difference` | $17^2(512/10^6)/[1-17(512/10^6)]<1/4$ |
| `weighted_contraction` | $(3+800/64)/64<1/4$ |
| `homogeneous_contraction` | $(1/128)(21/4)(3+1/16)<1/4$ |
| `fractional_parameter_bound` | $720000\,2^{512}2^{-600}<2^{-68}$ |
| `fractional_parameter_admissibility` | $0<2^{-600}\le1-2^{-600}<1$ |
| `Aud01FiniteSums.finite_summation_by_parts` | For any real sequences $w,u$ and $N\in\mathbb N$, $\sum_{j=0}^Nw_j(u_{j+1}-u_j)=w_Nu_{N+1}-w_0u_0+\sum_{j=0}^{N-1}(w_j-w_{j+1})u_{j+1}$ |
| `quadratic_history_collection` | The all-length triangular quadratic-history identity displayed in the TM-01 review above, for arbitrary real sequences and $m\in\mathbb N$, including zero |
| `reversed_difference_sum` | $\sum_{j=0}^{N-1}(b_{N-j}-b_{N-1-j})=b_N-b_0$ for any real sequence $b$ |
| `Aud01Oscillator.pre_derivative` | $d[te^{-\gamma t}]/dt=e^{-\gamma t}(1-\gamma t)$ for all real $\gamma,t$ |
| `critical_position` | At $t=1/\gamma$, position is $e^{-1}/\gamma$ if $\gamma\ne0$ |
| `critical_velocity` | At the same time, velocity is zero |
| `post_derivative` | The derivative of the stated post-switch position is $-y_0(\omega+\gamma^2/\omega)e^{-\gamma s}\sin(\omega s)$ for $\omega\ne0$ |
| `quarter_velocity` | At $s=\pi/(2\omega)$, the preceding velocity equals $-y_0(\omega+\gamma^2/\omega)e^{-\gamma\pi/(2\omega)}$ |
| `st05_endpoint_identity` | Substituting $\omega=16\gamma$, $y_0=e^{-1}/\gamma$ gives exactly $-(16+1/16)e^{-1-\pi/32}$ for $\gamma\ne0$ |
| `oscillator_energy_algebra` | $2\kappa xy+2y(-\kappa x-2y)=-4y^2$ for all real $\kappa,x,y$ |

Names in the table are in namespace `LegendreAudit.AUD01`; module prefixes identify their files rather than extra namespace components. The certificates do not establish the complex-analytic resolvent bounds, gamma estimates, propagator norm, logistic smoothing theorem, fractional regularity, or convergence transfer. Their precise role is algebra, rational constants, finite summation, and the listed calculus identities.

## Execution and reproduction status

The supplied symbolic program requires SymPy 1.14.0. The homogeneous program requires NumPy 2.3.5, SciPy 1.17.0, and mpmath 1.3.0. These exact versions are absent in the available environment. Workspace-only acquisition has been requested and remains pending; **neither supplied numerical/symbolic program is counted as freshly replayed**. No acceptance criterion was relaxed. The supplied finite-grid results remain labeled historical throughout this report.

The new Lean run records are under [results/](results/): constants attempt 01, finite sums attempt 02, oscillator attempt 02, and axiom audit attempt 01 pass. Initial finite-sum and oscillator proof attempts failed with explicit tactic errors; their sources and logs are retained, and the final statements were not weakened to obtain compilation.

From the existing Lean project, with its pinned toolchain and populated local cache, run these serially:

```bash
mkdir -p .lake/build/lib/lean
lake env lean -j1 -o .lake/build/lib/lean/AuditConstants.olean AuditConstants.lean
lake env lean -j1 -o .lake/build/lib/lean/Aud01FiniteSums.olean Aud01FiniteSums.lean
lake env lean -j1 -o .lake/build/lib/lean/Aud01Oscillator.olean Aud01Oscillator.lean
lake env lean -j1 Aud01Axioms.lean
```

Use the existing bounded runner for retained output, with a new label and output directory per attempt. Recorded runs use one CPU affinity/Lean worker, 120 s wall and 90 s CPU deadlines, 8 GiB per-process address-space limits, and sampled descendant RSS ceilings of 2.25 GiB for algebra and 3.5 GiB for oscillator/combined imports. The wrapper uses process-group cleanup; these are sampled/per-process controls, not cgroup aggregate isolation or a guarantee for deliberately detached children. No numerical workload has been launched while dependency acquisition is pending.

The original source paper was inspected locally at PDF pp.5–8, 15–17, and 22–25. The text extractor reported CFF font-encoding warnings; the quoted theorem/model wording and forcing convention are legible in the extracted text. PDF pp.15–16 were also rendered and visually inspected: the theorem quantifiers, norms, and Eq. (42) match the comparison above. No new primary related-work article was acquired.

## Consequences and next review actions

1. Retain SP-02 as a conditional finite-time estimate and the two temporal sharpness examples as distinct results. Do not present either as a uniform classical-$H^1$ estimate or combine their forcing/regularity hypotheses.
2. Repair R1's nodal representative convention before using the weak SP-01 formulation. The strong smooth-kernel case, abstract SP-02 stability, and ST-05 coefficient are unaffected.
3. State the sufficiently-fine-grid interpretation explicitly when comparing ST-05 with Theorem 3.1. Keep the independent L1 route visible: it gives the main challenge without relying on the L1-2 resolvent.
4. Supply the missing older diagnostic sources/outputs and primary-reference locators. Replay the two supplied programs at their exact versions once acquisition is approved, preserving any failures. Do not demand a finite-grid exponent of $0.5$ from the homogeneous data.
5. Keep practical decimal parameters, the exact $2^{-600}$ construction, and the original ST-04 candidate separate. The formal certificates close only the listed finite subclaims; the analytical chains remain subject to further mathematical review.
