# Lean proof certificates

The current project preserves **23 ST-04 and 19 AUD-01 named certificates**. They form **41 nonduplicate identity groups**, with one repeated telescoping identity grouped under index reversal and rearrangement. This is not a claim of logical independence. Read the [combined coverage and exact-statement catalogue](../reviews/AUD-01/revision-01/LEAN_CATALOGUE.md) before the earlier ST-04 inventory below.

The AUD-01 certificates add polynomial symbol algebra, rational perturbation constants, all-length finite summation identities and exact oscillator calculus. Their compiler output and axiom audits are preserved; the [clean-tree validation](../results/checkpoint-aud01/VALIDATION.md) records fresh compilation of all five proof modules and the combined audit. Complex resolvent estimates, fractional regularity and complete PDE arguments remain analytical.

The formal proofs isolate the exact algebra behind several disputed steps. They certify the post-startup L1-2 leading coefficient and a negative historical coefficient, distinguish signed-history bounds from contraction, and establish a concrete variable-coefficient quadrature discrepancy using an exact real integral. Real powers and algebraic nodes are handled exactly rather than through floating-point approximations.

| Mathematical role | What is certified |
| --- | --- |
| L1-2 coefficients and histories | Exact identities, the $\alpha=3/4$ sign example, the valid triangle inequality, an assigned-state counterexample, and telescoping/normalization identities |
| Spatial quadrature | For the specified $M=3$ GLL rule and $0<c<1$, the mass integral and quadrature differ by exactly $32c/525$ |
| Additional qualifications | An abstract weighted-energy nonuniformity statement and positivity of the Volterra near-panel constant at $\beta=1/2$ |

These propositions support the [mathematical investigations](../observations/README.md). They do not formalize fractional differentiation, a Sobolev-space PDE, the full Volterra error theorem, Theorem 3.1, or the ST-04 trajectories. In particular, the signed-state counterexample concerns an algebraic inference, not a computed solution.

## Compilation and proof dependencies

The clean AUD-01 integration compiled all five local proof modules and printed the dependencies of **all 42 named declarations**. The earlier ST-04 run compiled its original 23 declarations in two modules. The only reported axioms are the standard Lean/mathlib foundations `propext`, `Classical.choice`, and `Quot.sound`; there are no `sorry`/`admit` placeholders, `sorryAx` dependencies, or new unsupported axioms. Compiler style and unused-hypothesis warnings remain in the logs.

The pinned environment is **Lean 4.19.0**, with mathlib **v4.19.0** at `c44e0c8ee63ca166450922a373c7409c5d26b00b`. The lockfile fixes transitive dependencies. See the [Lean reproduction commands](../REPRODUCE.md#lean) and [current validation report](../results/checkpoint-aud01/VALIDATION.md) for compilation records. The [ST-04 report](../results/VALIDATION.md) remains archival evidence. These proof files are independent certificates; they are not recovered versions of the original missing CF-02 drafts.

## ST-04 theorem statements

All theorem names below are prefixed by `LegendreAudit.`. Variables are real unless indicated otherwise. Define

$$
b_0^*(a)=\frac1{2-a}-\frac12,\quad d_0(a)=1+b_0^*(a),\quad
d_1(a)=2^{1-a}-d_0(a).
$$

The definitions are the evaluated zeroth correction and the step-2 historical coefficient from the notes. This project verifies their exact algebra and real powers; it does not formalize the derivation from fractional interpolation integrals.

| Theorem in `Coefficients.lean` | Exact certified statement |
| --- | --- |
| `bStarZero_identity` | For $0<a<1$, $b_0^*(a)=a/[2(2-a)]$ |
| `leading_identity` | Under the same hypotheses, $d_0(a)=1+a/[2(2-a)]$ |
| `leading_gt_one` | Under the same hypotheses, $d_0(a)>1$ |
| `leading_three_quarters` | $d_0(3/4)=13/10$ |
| `fourthRootTwo_fourth` | $(2^{1/4})^4=2$, using real power, not a floating-point value |
| `fourthRootTwo_lt_thirteen_tenths` | $2^{1/4}<13/10$ |
| `oldestSecond_three_quarters` | $d_1(3/4)=2^{1/4}-13/10$ |
| `oldestSecond_three_quarters_neg` | $d_1(3/4)<0$ |
| `history_abs_budget` | If $d_0>0,d_1<0$, then $\lvert d_0-d_1\rvert+\lvert d_1\rvert=d_0-2d_1>d_0$ |
| `signedHistory_triangle` | For any finite index set and real $c_j,u_j$, $\Vert \sum c_ju_j\Vert \le\sum \vert c_j\vert \vert u_j\vert $ |
| `signed_sum_bound_false` | It is false that every real $c_0,c_1,u_0,u_1$ with $\vert u_i\vert \le1$ satisfies $\vert c_0u_0+c_1u_1\vert \le\vert c_0+c_1\vert $. Exact witness: $(2,-1,1,-1)$ |
| `l12_assigned_state_counterexample` | For the exact $d_0(3/4),d_1(3/4)$, $d_0<\vert (d_0-d_1)\cdot1+d_1\cdot(-1)\vert $. These states are freely assigned, not a computed trajectory |
| `telescoping_history` | For every $d:\mathbb N\to\mathbb R$, $k\in\mathbb N$, $\sum_{r=0}^{k-1}(d_r-d_{r+1})+d_k=d_0$, including $k=0$ |
| `telescoping_not_one` | If $d_0=d_0(a)$ with $0<a<1$, that unnormalized sum is not one |
| `normalized_history` | If $d_0\ne0$, dividing that sum by $d_0$ gives one |
| `no_uniform_weighted_energy_bound` | No $C>0$ bounds $x^2+y^2\le C(x^2+w y^2)$ simultaneously for every $0<w\le1$ and every real $x,y$. This is an abstract energy statement, not a theorem about Sobolev spaces |
| `volterra_half_near_panel_positive` | $(1+1/\sqrt2)/2-2(\sqrt2-1)>0$, the exact near-panel coefficient for $\beta=1/2$ |

For the concrete $M=3$ example, define

$$
f_c(x)=(1+cx)(1-x^2)x(1-x^2),\qquad
Q[f]=\frac{f(-1)+f(1)}6+\frac56\bigl[f(-\sqrt{1/5})+f(\sqrt{1/5})\bigr].
$$

The weights and nodes are exact real algebraic quantities. The integral below is mathlib's real interval integral, proved using an explicit polynomial primitive and the fundamental theorem of calculus.

| Theorem in `Quadrature.lean` | Exact certified statement |
| --- | --- |
| `mass_polynomial` | $f_c=x-2x^3+x^5+cx^2-2cx^4+cx^6$, for all real $c,x$ |
| `gll3_mass` | $Q[f_c]=16c/75$, for all real $c$ |
| `mass_hasDerivAt` | $F_c'=f_c$ at every real $x$, where $F_c=x^2/2-x^4/2+x^6/6+cx^3/3-2cx^5/5+cx^7/7$ |
| `mass_integral` | $\int_{-1}^1 f_c(x)\,dx=16c/105$, for all real $c$ |
| `positive_mass_coefficient` | If $0<c<1$ and $-1\le x\le1$, then $1+cx>0$ |
| `gll3_variable_coefficient_counterexample` | If $0<c<1$, then $\vert Q[f_c]-\int_{-1}^1f_c\vert =32c/525$ and the two values differ |

The general $M$ statement is not formalized. The norm certificate does not identify a PDE function space or establish its uniform norm equivalences. The near-panel certificate does not prove the full Volterra $\Theta(\tau^{1-\beta})$ theorem; the full analytical argument remains in the supplied LaTeX. No formal certificate concerns ST-04, the numerical trajectories, a fractional derivative, or Theorem 3.1.
