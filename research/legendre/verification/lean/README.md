# Small Lean certificates

Lean **4.19.0** and mathlib **v4.19.0**, pinned to `c44e0c8ee63ca166450922a373c7409c5d26b00b`, certify the statements below. The dependency lock pins all transitive packages. These are newly written proofs for this checkpoint, not recovered versions of the original missing CF-02 drafts. See [reproduction instructions](../REPRODUCE.md) and [actual compiler output](../results/checkpoint-st04/).

Both source modules compile successfully. The axiom drivers print the dependencies of all 23 theorems. Only Lean/mathlib's standard `propext`, `Classical.choice`, and `Quot.sound` are permitted; no `sorry`, `admit`, `sorryAx`, or new axioms are accepted. Style/unused-hypothesis linter warnings are retained in the compiler logs. They do not change the hypotheses or mathematical statements.

All theorem names below are prefixed by `LegendreAudit.`. Variables are real unless indicated otherwise. Define

\[
b_0^*(a)=\frac1{2-a}-\frac12,\quad d_0(a)=1+b_0^*(a),\quad
d_1(a)=2^{1-a}-d_0(a).
\]

The definitions are the evaluated zeroth correction and the step-2 historical coefficient from the notes. This project verifies their exact algebra and real powers; it does not formalize the derivation from fractional interpolation integrals.

| Theorem in `Coefficients.lean` | Exact certified statement |
| --- | --- |
| `bStarZero_identity` | For \(0<a<1\), \(b_0^*(a)=a/[2(2-a)]\) |
| `leading_identity` | Under the same hypotheses, \(d_0(a)=1+a/[2(2-a)]\) |
| `leading_gt_one` | Under the same hypotheses, \(d_0(a)>1\) |
| `leading_three_quarters` | \(d_0(3/4)=13/10\) |
| `fourthRootTwo_fourth` | \((2^{1/4})^4=2\), using real power, not a floating-point value |
| `fourthRootTwo_lt_thirteen_tenths` | \(2^{1/4}<13/10\) |
| `oldestSecond_three_quarters` | \(d_1(3/4)=2^{1/4}-13/10\) |
| `oldestSecond_three_quarters_neg` | \(d_1(3/4)<0\) |
| `history_abs_budget` | If \(d_0>0,d_1<0\), then \(\lvert d_0-d_1\rvert+\lvert d_1\rvert=d_0-2d_1>d_0\) |
| `signedHistory_triangle` | For any finite index set and real \(c_j,u_j\), \(\|\sum c_ju_j\|\le\sum |c_j||u_j|\) |
| `signed_sum_bound_false` | It is false that every real \(c_0,c_1,u_0,u_1\) with \(|u_i|\le1\) satisfies \(|c_0u_0+c_1u_1|\le|c_0+c_1|\). Exact witness: \((2,-1,1,-1)\) |
| `l12_assigned_state_counterexample` | For the exact \(d_0(3/4),d_1(3/4)\), \(d_0<|(d_0-d_1)\cdot1+d_1\cdot(-1)|\). These states are freely assigned, not a computed trajectory |
| `telescoping_history` | For every \(d:\mathbb N\to\mathbb R\), \(k\in\mathbb N\), \(\sum_{r=0}^{k-1}(d_r-d_{r+1})+d_k=d_0\), including \(k=0\) |
| `telescoping_not_one` | If \(d_0=d_0(a)\) with \(0<a<1\), that unnormalized sum is not one |
| `normalized_history` | If \(d_0\ne0\), dividing that sum by \(d_0\) gives one |
| `no_uniform_weighted_energy_bound` | No \(C>0\) bounds \(x^2+y^2\le C(x^2+w y^2)\) simultaneously for every \(0<w\le1\) and every real \(x,y\). This is an abstract energy statement, not a theorem about Sobolev spaces |
| `volterra_half_near_panel_positive` | \((1+1/\sqrt2)/2-2(\sqrt2-1)>0\), the exact near-panel coefficient for \(\beta=1/2\) |

For the concrete \(M=3\) example, define
\[
f_c(x)=(1+cx)(1-x^2)x(1-x^2),\qquad
Q[f]=\frac{f(-1)+f(1)}6+\frac56\bigl[f(-\sqrt{1/5})+f(\sqrt{1/5})\bigr].
\]
The weights and nodes are exact real algebraic quantities. The integral below is mathlib's real interval integral, proved using an explicit polynomial primitive and the fundamental theorem of calculus.

| Theorem in `Quadrature.lean` | Exact certified statement |
| --- | --- |
| `mass_polynomial` | \(f_c=x-2x^3+x^5+cx^2-2cx^4+cx^6\), for all real \(c,x\) |
| `gll3_mass` | \(Q[f_c]=16c/75\), for all real \(c\) |
| `mass_hasDerivAt` | \(F_c'=f_c\) at every real \(x\), where \(F_c=x^2/2-x^4/2+x^6/6+cx^3/3-2cx^5/5+cx^7/7\) |
| `mass_integral` | \(\int_{-1}^1 f_c(x)\,dx=16c/105\), for all real \(c\) |
| `positive_mass_coefficient` | If \(0<c<1\) and \(-1\le x\le1\), then \(1+cx>0\) |
| `gll3_variable_coefficient_counterexample` | If \(0<c<1\), then \(|Q[f_c]-\int_{-1}^1f_c|=32c/525\) and the two values differ |

The general \(M\) statement is not formalized. The norm certificate does not identify a PDE function space or establish its uniform norm equivalences. The near-panel certificate does not prove the full Volterra \(\Theta(\tau^{1-\beta})\) theorem; the full analytical argument remains in the supplied LaTeX. No formal certificate concerns ST-04, the numerical trajectories, a fractional derivative, or Theorem 3.1.
