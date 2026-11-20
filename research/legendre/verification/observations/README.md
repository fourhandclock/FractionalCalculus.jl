# Observation dossier

Earlier execution-availability statements refer to the historical ST-03 integration. The current [validation report](../results/VALIDATION.md) records fresh checkpoint runs and explicitly scoped certificates.

The [original ST-04 LaTeX](../mathematical-verification.tex) contains the complete proofs, not condensed replacements. Its equation and section numbers below match the supplied [notes PDF](../sources/legendre_spectral_verification_notes_st03.pdf). Published locators refer instead to the local [Sabawi paper](../../../../YS_SS_PD_NM_25_Calcolo.pdf). Mathematical statuses and computational execution statuses are separate.

## Observation 1 / ST-03

- **Published claim:** Theorem 3.1, paper pp.15–16, asserts `||U^{k+1}_{(q)}||₁ ≤ ||U⁰_{(q)}||_{L²}` for a sufficiently fine temporal mesh, `q=1,2`. The p.16 coefficient argument combines signed histories inside one absolute value; the L1-2 case is asserted by analogy using Eq. (29).
- **Hypotheses:** Real homogeneous evolution, zero forcing and homogeneous Dirichlet conditions; `0<α,β<1`, positive sufficiently smooth kernel factor, positive memory coupling in the paper. The norm uses `α₀=Γ(2−α)τ^α`. The arbitrary-state demonstration and the zero-memory diagnostic are explicitly reductions, not complete theorem-admissible trajectories.
- **Independent derivation:** Notes §6, Eqs. (6.2)–(6.6), Proposition 6.1. With `h_r=d_r−d_{r+1}`, `h_k=d_k`, the signed sum telescopes to `d₀`, but the absolute sum need not. At `α=3/4,k=1`, `d₀=13/10`, `d₁=2^(1/4)−13/10<0`, and `|h₀|+|h₁|=d₀−2d₁>d₀`. States `U⁰=−1,U¹=1` refute the inference from norm bounds alone. They are **not asserted to solve the recurrence**. At `α=1/2,k=2`, another negative historical coefficient occurs even with positive increment coefficients. Notes (6.5) retains all Volterra contributions and the correct current-state coefficient.
- **Computational verification:** Unmodified [ST-03 script](../scripts/verify_l12_stability.py), [supplied output](../sources/st03_verification_results.txt), new [Python checks](../scripts/check_counterexamples.py), and [Julia regression](../../../../studies/legendre/test/proof_audit.jl). The supplied output reports 432 cases and maximum representation discrepancy `3.77e-15`; the fresh run reproduces all 432 cases (see the current validation report). The cited amplification `1.08601376` is a finite coarse-grid observation, with `β>α`, not a theorem counterexample.
- **Result:** Established proof gap in the proposed coefficient-based contraction induction, including its extension to the corrected L1-2 rule. Cauchy–Schwarz itself is not the invalid step.
- **Limitations:** Neither instability nor falsity of Theorem 3.1 is proved. Notes §6.5 actually gives a contractive reduced two-step zero-memory trajectory. Kernel positivity alone cannot justify replacing `Σ|c_j|` by `|Σc_j|`; a valid combined memory estimate is still needed.
- **Dependencies:** CF-02's corrected coefficients; the proof strategy for Theorem 3.1 and later temporal error induction in Theorem 3.2; any full convergence argument importing those estimates.

## Observation 2 / CF-02

- **Published claim:** Two-sum and single-sum equivalence in Eq. (23), correction weights Eq. (24), coefficient identities Eq. (29), and recurrence Eqs. (28)–(32), paper pp.11–13.
- **Hypotheses:** Uniform mesh, `0<α<1`, linear interpolation on the first panel and backward quadratic interpolation afterwards; `Δu^j=u^{j+1}−u^j`. At `t_{k+1}`, `k=0` is startup.
- **Independent derivation:** Notes §5, Propositions 5.1–5.2. Startup is `d₀^[0]=1`. For `k≥1`, use exactly `d₀^[k]=b₀+b₀*`, `d_r^[k]=b_r+b_r*−b_{r−1}*` for **1≤r≤k−1**, and `d_k^[k]=b_k−b_{k−1}*`; the middle case is empty when `k=1`. The oldest coefficient is step-dependent. Thus `d₀=1+α/[2(2−α)]`. The exact negative coefficient and rational fourth-power sign proof are notes (5.6). Nodal data `(0,0,1)` expose the independent reversed-index error. Both missing `j=1` ranges are recorded; no completion of the undefined printed middle case is silently assumed. Telescoping gives `d₀`, not one, and normalizing must rescale diffusion and the whole history.
- **Computational verification:** Existing [uniform-increment tests](../../../../studies/legendre/test/time_and_solver.jl) and implementation already follow interpolation. New checks keep the printed index reversal and `d₀=1` diffusion diagnostic separate from the corrected formulas. The PDF's original CF-02 Python/Julia/Lean companions are missing; its reported polynomial/direct-integral run was not reproduced.
- **Result:** Verified algebraic discrepancy in the printed coefficient representation and blanket coefficient assertions, independent of spatial and memory discretization.
- **Limitations:** Negative coefficients alone do not establish instability. Authors' actual implementation is unavailable. No inference is made that their code used either conflicting formula. No whole-scheme repair is performed.
- **Dependencies:** The elliptic coefficient in (31), historical RHS (32), normalization (29), and L1-2 stability/convergence arguments based on them. Startup (34) is unaffected by this post-startup coefficient discrepancy.

## Observation 3

- **Published claim:** Post-startup `3−α` Caputo consistency component, notably paper Eq. (26), p.12.
- **Hypotheses:** Smooth `u=t²`, uniform mesh, `0<α<1`; investigate the fixed early index `n=2` as `τ→0`, separately from fixed positive physical time.
- **Independent derivation:** Notes observation 3 retains the complete first-panel integral `τ^(2−α)/Γ(1−α) ∫₀¹(2z−1)(2−z)^(−α)dz`, which is nonzero; the quadratic second panel is exact.
- **Computational verification:** Existing Julia startup-error tests compare the full interpolatory derivative with analytical first-panel moments. They were not rerun here. New Python checks compare panel moments and both coefficient collections on the stated small polynomial grid; they do not replace a uniform-in-time proof.
- **Result:** **Provisional, explicit test case available**, as in the supplied PDF. The proposed uniform early-step claim needs a startup qualification.
- **Limitations:** No newly completed audit of global PDE convergence or a fixed-time asymptotic rate; the PDF's status is not promoted by adding regression code.
- **Dependencies:** Eq. (26), startup treatment, and post-startup temporal convergence claims. Further analysis must retain startup error propagation.

## Observation 4

- **Published claim:** `B(R_M,ρ_M)=B_M(R_M,ρ_M)` for `R_M∈P^0_{M−1}`, Theorem 4.1 proof immediately before Eq. (55), paper p.23.
- **Hypotheses:** `M+1` LGL nodes, exactness through `2M−1`; `M=3`, `R_M=1−x²`, `ρ_M=x(1−x²)`, positive variable factor `R̂=1+cx`, **0<c<1**. Both test polynomials vanish at the endpoints.
- **Independent derivation:** Notes observation 4 gives the absolute mass-quadrature discrepancy `32c/525`. The degree-six even term lies beyond degree-five exactness. The derivative product is of admissible degree and does not remove this discrepancy. The complete supplied observation remains in §2 of the TeX file.
- **Computational verification:** New exact-rational Python check uses mass integral `16c/105` and four-point Lobatto sum `16c/75`; Julia checks the same construction with actual nodes/weights at `c=1/2`. These are new, unexecuted integration regressions, not historical results. Existing spatial tests already check the declared constant-coefficient exactness range.
- **Result:** **Provisional: exactness claim requires qualification.** The explicit polynomial calculation is preserved without upgrading the full spatial-proof audit.
- **Limitations:** Need a complete variable-coefficient consistency estimate or stronger assumptions. A constant-coefficient exactness result does not settle the variable-coefficient form.
- **Dependencies:** Theorem 4.1's cancellation and the combined spatial/temporal estimates of Theorem 4.2.

## Observation 5

- **Published claim:** The theoretical norm in Eq. (2), paper p.5, with α₀ defined on p.8.
- **Hypotheses:** Fixed positive timestep and `0<α<1`; `||v||₁²=||v||²+α₀||v_x||²`, `α₀=Γ(2−α)τ^α`.
- **Independent derivation:** Notes observation 5: equivalence to standard H¹ holds for fixed τ, with constants degenerating as τ decreases. The spatial-gradient weight tends to zero.
- **Computational verification:** An analytical interpretation issue. No empirical run is offered as a proof. The implementation's reported H¹ error uses a different, unweighted spatial gradient, already described in `error_norms` and the theory guide.
- **Result:** **Provisional interpretation caveat**, retained as such.
- **Limitations:** No uniform standard-H¹ theorem is established or refuted by translating a weighted estimate alone.
- **Dependencies:** Interpretation of all stability and convergence estimates using this norm; comparisons with the numerical section's H¹ columns.

## Observation 6

- **Published claim:** Section 6 discrete error definitions, paper p.28, including the extra `(M+1)^{-1}` spatial averaging factor.
- **Hypotheses:** LGL weights already approximate spatial integration; paper metrics average over sampled time levels as well. Graded time samples are not automatically a time-integral quadrature.
- **Independent derivation:** Notes observation 6: omitting the distinction adds a resolution-dependent scale and can affect apparent spatial rates. The original observation does not prescribe a replacement metric.
- **Computational verification:** Existing `error_norms` retains the printed `L2` and `H1`, and also reports `space_time_L2` without the extra spatial-node divisor. Existing tests use a known constant offset to check normalization. Existing CSVs are preserved. No new error values or table reproduction claim is made.
- **Result:** **Numerical reproduction check**, unresolved interpretation, not an established error in all reported tables.
- **Limitations:** Published H¹ gradient evaluation and the 2D normalization convention remain ambiguous; do not tune them to fit targets.
- **Dependencies:** Table comparisons, inferred spatial rates, and the interpretation of a numerical H¹ column versus the theoretical weighted norm.

## Observation 7

- **Published claim:** Strictly positive smooth kernel factor in the model, paper p.5 and Theorem 3.1 proof; compare Example 6.2, p.33.
- **Hypotheses:** Positivity throughout the domain is required by the cited proof; the example uses `K=x` on `(-1,1)` and λ=1.
- **Independent derivation:** Notes observation 7 identifies the negative-x part of the domain. Computing that example does not make it a test under the theorem's positivity assumptions.
- **Computational verification:** `paper_example(2)` already sets `coefficient=(p,t)->p[1]`; source inspection confirms this without altering the example. The earlier theory guide also discusses Example 6.1's `sin x` factor; that is existing repository context, not an additional result promoted by this integration.
- **Result:** **Assumptions check**, retaining provisional status.
- **Limitations:** Neither an instability result for sign-changing kernels nor an extension of the theorem to them is supplied.
- **Dependencies:** Which manufactured examples can be used as evidence under the positive-kernel stability assumptions.

## Observation 8 / VQ-01

- **Published claim:** Singular Volterra quadrature Eq. (6) and `O(τ^(2−β))` estimate in Eq. (8)/Remark 1, paper p.7. The combined L1 simplification in (8) assumes β≤α; the quadrature discrepancy itself is independent of α.
- **Hypotheses:** Uniform `t_n=nτ`, `τ=T/N`; separable singular kernel; `0<β<1`. Lower bound: `T=1`, `K=u=1`, `n=N≥2`. Upper bound: `u∈C²([0,T])`, bounded kernel factor; constant may depend on T, β, its supremum, and the stated derivatives of u, not N.
- **Independent derivation:** Notes §4, Propositions 4.1–4.2, all proofs retained. The special last panel is exact for constants. The previous ordinary trapezoid has strictly positive error `c_β τ^(1−β)`; convexity prevents cancellation. The positive panel-error series converges, giving `|Φ_T^N|∼C_β τ^(1−β)`. The upper bound sums all ordinary panels and the final-panel error, yielding uniform `Cτ^(1−β)`. Therefore the constant-input error is **Θ(τ^(1−β))**, and the general smooth-input order is sharp. The homogeneous-Dirichlet embedding and scaled `τ^(1+α−β)` residual are retained with the original sign/scaling qualification.
- **Computational verification:** Full historical β=.2,.5,.8 table from notes §4.4 is in TeX. The repository already retains a β=.5 [memory diagnostic](../../../../studies/legendre/figures/memory_diagnostic.csv) and tests β=.2,.5,.8 refinement. Its original VQ-01 Python checker is missing; new Python checks separately implement the printed rule and exact panel-error identity, with analytical sign and rate expectations and rounded-PDF comparisons. The new independent 10-test suite reproduces these sign, table-rounding, and order checks; the original VQ-01 companion remains missing.
- **Result:** Verified inconsistency of the claimed quadrature remainder for the formula **as printed**, with sharp general consistency order `1−β`.
- **Limitations:** Does not establish the global PDE solution-error rate or disprove the full convergence theorem. Authors' possible unstated quadrature is unknown. Notes §4.6 product integration and its `Cτ²` operator estimate are an explicitly different candidate; no weights, scheme, stability proof, or replacement solver have been implemented.
- **Dependencies:** Eqs. (8), (26), and scaled residual estimates; Theorem 3.2's consistency inputs; combined convergence arguments in Theorem 4.2. A solution-error statement additionally needs a valid discrete evolution estimate.

## ST-04

- **Published claim:** Theorem 3.1, paper pp.15–16, claims nonamplification in its timestep-dependent norm for a sufficiently fine mesh. The source allows a smooth strictly positive time-dependent coefficient; no time-monotonicity condition is imposed by the cited statement.
- **Hypotheses:** Exact eigenmode `φ(x)=cos(πx/2)` on `(-1,1)`, unit L² norm, eigenvalue `σ=(π/2)²`; homogeneous boundary conditions, zero forcing, initial amplitude one; α=.95, β=.05, λ=1, T=.8, `K(t)=.05+500/(1+exp(-45(t-.3)))`. Thus `0<β≤α<1`, and K is bounded, smooth, and strictly positive. No spatial approximation is involved.
- **Independent derivation:** Original supplied ST-04 TeX §7 reduces the PDE and time-semidiscrete schemes to the scalar fractional Volterra recurrence, with weighted amplitude `sqrt(1+σα₀)|a_n|`. The limiting α=1,β=0 switched oscillator is an explanatory calculation outside the open parameter range; its smoothing, parameter-continuity, and convergence arguments remain to be certified.
- **Computational verification:** The unchanged supplied [ST-04 script](../scripts/verify_time_variable_kernel_st04.py) runs L1 and interpolation-defined L1-2 at N=128,256,512,1024,2048,4096, for both the printed Eq. (6) and the supplied product-integration control. All 24 configurations passed in the fresh run. At N=4096 the printed-rule weighted peaks are about 2.98087 and 2.98488 respectively. The residual check samples six levels per trajectory; it does not test every level or supply rounding enclosures. The supplied historical output and fresh output are retained separately.
- **Result:** **Strong numerical counterexample candidate** to the published contractivity estimate for a smooth positive time-dependent kernel. Both derivative formulas and both memory rules show amplification on the tested meshes.
- **Limitations:** Finite grids do not establish a violation for all sufficiently small timesteps. ST-04 is not a formal theorem refutation, a proof of instability, or a disproof of a weaker finite-time bound. Product integration is a control in the supplied diagnostic and was not inserted into the reproduction solver. Small floating-point residuals do not certify continuum convergence.
- **Dependencies:** Correct coefficient collection, exact eigenmode reduction, the printed-memory interpretation, and the weighted-norm definition. An all-fine-grid counterexample still needs a justified convergence argument or a direct parameter-valid discrete certificate.

The original source, complete parameter provenance, and implementation audit are in [ST04_PROVENANCE.md](../ST04_PROVENANCE.md). Current run/certificate statuses are in [VALIDATION.md](../results/VALIDATION.md); earlier statements above that tests were not rerun describe the historical ST-03 integration and are superseded by that dated checkpoint record.

## Next research steps

1. Derive an energy or resolvent estimate for the **corrected step-dependent L1-2 coefficients and the combined Volterra history**, retaining signed coefficients and the actual newest-step coefficient. Identify admissible α, β, λ, kernel hypotheses, and any timestep restriction. Recheck the L1 signed-history argument separately. A discrete Grönwall argument can only be applied after establishing the needed combined estimate.
2. Propagate the proven Volterra consistency error through that evolution estimate. Separate unscaled operator error, α₀-scaled local residual, startup accumulation, and global PDE solution error; do not identify their exponents without proof.
3. Recover the missing CF-02/VQ-01 companions and Lean draft, plus authors' code or clarification of conflicting recurrences if available. Check the independent 2022 literature against its primary text before importing any technical result. No new search or acquisition was performed here.
4. Complete the provisional startup and variable-coefficient quadrature audits, preserving their current scope and statuses; reconcile weighted theoretical and reported numerical norms and the sign-changing examples.
5. Complete the unavailable validation steps in a configured environment and retain raw outputs separately. Consider product integration only as a later, separately labeled scheme investigation, after the reproduction and proof audit have been assessed.
