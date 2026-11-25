"""Produce six separate revisions from the frozen original TeX, without new theorems."""
from pathlib import Path
import json,re

ROOT=Path(__file__).resolve().parents[5]
SOURCE=ROOT/'studies/legendre/gr07/reference/theory'
DEST=ROOT/'studies/legendre/gr07/revision-01/manuscripts'
NOTICE=r"""
\noindent\textbf{Revision 01 (AUD-02 closure).}
The independent analytical review verdict is \emph{ACCEPT WITH LIMITATIONS}.
The results below are conditional on their stated hypotheses. Finite-grid
diagnostics are evidence for implementations, not proofs of the analytical
theorems. The numerical tables retain the original diagnostic values.
Lean certificates cover the explicitly identified finite algebraic subclaims,
not complete fractional PDE arguments. Original manuscripts and execution
evidence are preserved separately.
"""

ADDITIONS={
'GR01':r"""
\section*{Review qualifications}
The orders and final time are fixed. Constants need not remain bounded as a
fractional order approaches an endpoint. For bounded measurable equivalence
classes, the comparison is almost everywhere; a pointwise comparison requires
chosen representatives satisfying its hypotheses pointwise. In particular,
the nondecreasing initial majorant is interpreted with such a representative.
The continuous comparison and multinomial Mittag--Leffler representation are
established positive-kernel theory, not a novelty claim of this study.

The PDE estimate requires enough regularity for testing, the Caputo energy
identity and its fractional inverse. It is an a priori Hilbert-norm estimate,
not an ordinary $H^1$ theorem or a proof that arbitrary weak solutions have
the required regularity. It does not replace the original endpoint L1/L1-2
scheme by a shifted method without saying so.

The preliminary discrete comparison is conditional on its stated positive
complementary kernels and localized tails, on a possibly nonuniform mesh.
Its fine-mesh condition is sufficient for block absorption; it is not a
necessary stability condition. It does not assert an exact discrete semigroup.
The sharp constant-data continuous majorant concerns the abstract comparison
class, not a sharp energy trajectory of the PDE.
""",
'GR02':r"""
\section*{Review qualifications}
This note's explicit coefficient identities and consistency result use uniform
timesteps. Their nonuniform counterpart is used in GR-06 only with its separate
mesh hypotheses. All orders are fixed; order-uniform constants are not claimed.
The cited Alikhanov preprint locators are Lemmas 2 and 4 of version 3.

The matrix $A$ acts on increments; $PA=J$ has ones below and on the diagonal,
not an identity matrix. Neither this identity nor the localized complementary
mass estimate asserts a fractional semigroup. The positive-history energy
argument is distinct from the signed-history cancellation rejected in ST-03.

At step $n$, a completed quadratic stencil can use the current unknown $v^n$,
but never $v^{n+1}$. This is a causal implicit construction even though its
evaluation point precedes $t_n$. Quadratic exactness therefore uses no later
timestep value. The final-panel linear slope is taken over the full current
step, not just the integrated partial panel.

The AUD-02 Lean certificates establish finite summation, scalar polarized
energy and conditional complementary-composition identities. Positivity of
these fractional coefficients, Hilbert-space energy estimates and smooth
consistency remain analytical. The derivative order $3-\alpha$ does not imply
that the shifted diffusion scheme has that solution order.
""",
'GR03':r"""
\section*{Review qualifications}
These explicit coefficients and constants are for a uniform mesh and fixed
orders. GR-06 rederives the nonuniform stencil geometry and its
grading-dependent absolute-basis constant; the value $5/4$ must not be
transferred unchanged to an arbitrary backward nonuniform stencil.

The rule approximates normalized $I^r$; the equation includes
$\lambda\Gamma(r)$ exactly once. It is causal implicit: completed forward
stencils use levels at most $n$, and the final quadratic memory stencil is
backward. At startup both memory rules are linear. The final Caputo panel,
the final memory panel, and the shifted diffusion average have distinct roles.

The exact negative witness is the \emph{normalized factor}
$W^Q_{20}/[t_*^r/\Gamma(1+r)]=-17/231$, not the dimensional weight itself.
All later comparisons use $|W^Q|$, including its initial column.
Sharpness of the startup memory error, post-startup memory error and full
solution error are different statements. A memory estimate alone neither
proves nor refutes a PDE convergence theorem.

Nonpolynomial nodal coefficients in spatial applications require continuous
representatives with pointwise bounds at the nodes; an essential bound on an
arbitrarily modified equivalence class is insufficient.
The Lean certificates check finite moment collection, the uniform basis
bound and the rational witness. Gamma/beta integration, consistency and the
PDE energy application remain analytical.
""",
'GR04':r"""
\section*{Review qualifications and novelty boundary}
The quantitative Toeplitz resolvent argument is a uniform-grid result for
fixed exponents and coefficients. GR-06 uses a different physical-time block
argument on graded meshes. Row-tail domination applies to nonnegative
nondecreasing vectors, not arbitrary vectors or entrywise matrix comparison.
In a mixed word only the majorant intermediate vector must stay in that cone;
the original operators need not preserve it. Only the Toeplitz majorants
commute in the binomial expansion.

The diagonal condition $\rho_\tau<1$ proves finite triangular Neumann
convergence. The stronger $\xi$-condition is used separately for the
mesh-uniform shifted upper series and its limit. The upper simplex time is
$t_n+(h-1)\tau$ for word length $h$; dropping this shift is not justified.
Sharpness is over the abstract row-tail class with constant data, not the
subclass of actual PDE energies.

For the operator application $A$ is fixed, nonnegative and self-adjoint,
$U^0\in D(A)$ and $K_n:H\to H$ is uniformly bounded. The base resolvent
maps $H$ into $D(A)$, so the displayed bounded-perturbation factorization is
an operator from $D(A)$ onto $H$. No preservation of $D(A)$ by $K_n$ is
required. In collocation the bound concerns actual continuous representative
values at the nodes. Solvability and stability timestep restrictions are
sufficient, not necessary.

The result is in the underlying Hilbert norm. Ordinary diffusion-energy
stability is established separately in GR-05; no timestep-weighted norm is
silently identified with ordinary $H^1$.
Finite row-tail, mixed-word and composition algebra has Lean certificates;
infinite resolvent convergence, real-power bounds and PDE applications do not.
General positive-kernel resolvent comparison and monotone-kernel comparison
have established precedents. The novelty of this particular power-tail
majorant construction and uniform limit remains unresolved. No novelty claim
is made, and mathematical validity does not depend on establishing novelty.
""",
'GR05':r"""
\section*{Review completion: projection input and operator domains}
For $x,y\in D(A)$, $(x,Ay)=(A^{1/2}x,A^{1/2}y)$.
Finite temporal combinations of the existing $D(A)$ sequence therefore
justify testing by $Av_*$ without assuming $D(A^{3/2})$ regularity.
The operator must be fixed in time; a varying unbounded $A_n$ is not covered.
The complementary dissipation controls $\sum_jP_{nj}\|Av_*^j\|^2$,
not every $\|Av^n\|$ pointwise.

The standard Legendre approximation input can be checked independently.
For Legendre coefficients $a_k$ of $f$, weighted derivative orthogonality,
integration by parts and Bessel's inequality give, for integer $s\ge1$,
\[
 \sum_{k\ge s}\frac{2}{2k+1}\frac{(k+s)!}{(k-s)!}|a_k|^2
 \le \int_{-1}^1(1-x^2)^s|f^{(s)}(x)|^2\,dx.
\]
For smooth functions the boundary terms vanish because of $(1-x^2)^s$;
density extends this estimate to $H^s$. The reciprocal factorial ratio on
a degree-$L$ tail is bounded by $C_s(L+1)^{-2s}$. Hence
$\|f-\Pi_Lf\|_{L^2}\le C_s(L+1)^{-s}\|f\|_{H^s}$.
Taking $f=u_x$ or $g_x$ and $s=m-1$ gives the two integrated projection
estimates used above; finitely many small degrees are absorbed in $C_s$.
This is an independent justification, not a fabricated theorem locator in
Canuto--Quarteroni. The precise source-locator status is recorded with the
literature review accompanying this revision.

All nonpolynomial nodal quantities use continuous representatives; uniform
multiplier bounds refer to those pointwise values. The direct residual
decomposition uses a bounded $H^m$ derivative and integrates the shifted
stiffness residual by parts, so neither a $\tau^{-\alpha}$ projection loss
nor a polynomial-degree inverse factor is introduced. This is why no
time/space coupling is required under the stated strong hypotheses.

The temporal lower bound is for a consistently \emph{forced smooth} solution.
It uses the absolute value of the complementary-summed error equation, not
positivity of an actual solution-error trajectory. It is distinct from the
homogeneous initially singular AUD-01 sharpness example. Its implications for
Sabawi's Theorem 3.2 retain the forcing and regularity qualifications.

All orders and data norms are fixed. This is ordinary $H^1$ stability and
convergence, not equivalence to a timestep-weighted norm with a uniform
constant. It is conditional on the displayed regularity, fixed-operator,
pointwise nodal and initialization hypotheses. No theorem proving that
arbitrary PDE data produce this regularity is asserted. The complete
projection, residual and PDE arguments remain analytical.
""",
'GR06':r"""
\section*{Review qualifications}
The primary nonuniform source is specifically arXiv:1803.09873v4,
not the distinct SIAM discrete Gronwall paper. Its ratio is old step divided
by next step, $\rho_k=\tau_k/\tau_{k+1}\le7/4$.
The graded mesh also satisfies that source's M2 geometry, with constants
depending on the fixed $\gamma$. The sufficient fine-grid threshold need
not be necessary, uniform in $\gamma$, or uniform in the fractional orders.

The final conclusion concerns ordinary $H^1$, under the written $H^m$-valued
regularity and the continuous nodal multiplier/forcing assumptions inherited
from GR-05. It does not establish that arbitrary initial data and forcing
produce such a PDE solution. Replacing the regularity by only scalar or
$L^2$ consistency would not justify the displayed $H^1$ result.
No timestep/degree coupling is used under these strong hypotheses.

For $\gamma\alpha=2$, the weighted derivative exponent still exceeds or
equals the solution target since $3-\alpha>2$. The maximum-based bound has
no harmonic summation and introduces no endpoint logarithm.
The threshold $\gamma=2/\alpha$ is sufficient for order two here, not a
novel general grading principle. All of the Hilbert-valued consistency,
block absorption and fully discrete convergence remain analytical; the
finite Lean certificates do not formalize this theorem.
"""
}

ADDITIONS['GR04'] += r"""
Van Dijk and Sladky \cite{dijksladky}, Section 4, already give comparison
results for nonnegative matrix iterations and cumulative rewards. Their
written monotonicity-class and trajectory conditions are not identical to
our one-sided ordered-majorant construction; an equivalence for the complete
power-tail mixed-product and uniform-limit statement has not been established.
Thus the comparison mechanism has clear precedents while the exact novelty
question remains unresolved.
"""
ADDITIONS['GR05']=ADDITIONS['GR05'].replace(
    'literature review accompanying this revision.',
    'literature review accompanying this revision: publisher access remained blocked\n(HTTP 403), so the exact CQ theorem locator is still unverified. The\nindependent projection argument above supplies the required input without it.')

TRACE=r"""
The first-derivative bound is integrable in $H^m$, so $u$ is absolutely
continuous there. Beta integration gives a uniformly bounded exact Caputo
derivative. The zero boundary trace is preserved by differentiation at
positive times, finite temporal combinations and Bochner integration.
Consequently $R_D^j\in H^m\cap H_0^1$, and its Ritz projection is defined.
"""
ECS=r"""
\paragraph{Hilbert-valued consistency justification.}
The scalar error-convolution-structure proof extends at the integral-remainder
level. Replace each scalar third derivative by its Bochner norm; the bounding
kernels are nonnegative. Its local and history remainders then give
\[
 \|R_D^j\|_{H^m}\le A_{jj}G_{\rm loc}^j+
 \sum_{k<j}(A_{j,k+1}-A_{jk})G_{\rm his}^k.
\]
Multiply by nonnegative $P$ and use the exact column identities, precisely
as in the scalar estimate. At zero the weighted third-derivative integrands
are $O(s^{\alpha-1})$, hence integrable. Integral remainders can first be
used away from zero and then passed to the limit in norm. This uses no
vector mean-value theorem and no interchange of a supremum with a sum of
scalar consistency errors.

On the graded mesh the remaining maximum has the explicit bound
\[
 \frac{t_k^\alpha t_{k-1}^{\alpha-3}\tau_k^3}{\tau_{k-1}^\alpha}
 \le C N^{-\gamma\alpha}k^{\gamma\alpha-(3-\alpha)}.
\]
Its maximum, including equality of the exponents, gives the displayed rate
without a logarithm. Constants include the fixed-order factors of the
primary estimate and are not asserted order-robust.
"""
SPLIT=r"""
The $g$ term is a form pairing:
$(g,v_*+Av_*)=(g,v_*)+(A^{1/2}g,A^{1/2}v_*)$.
Thus it is bounded by $L\|g\|_V$ before multiplication by two.
For $h$ and the memory, reserve part of $2\|Av_*\|^2$ for Young
absorption. The remaining Hilbert pairings contribute only $CSE$,
$C\|h\|^2$ and $C\sum_kH_{nk}E_k$.
After complementary summation and physical blocks one has
\[
 L^2\le C\left(E_0+\max_j\|h_j\|^2+
 L\max_n\sum_{j\le n}P_{nj}\|g_j\|_V\right).
\]
Scalar Young absorption of this \emph{linear} $L$ term proves the bound.
The local singular Caputo residual is never squared or replaced by its
unweighted maximum.
"""

def main():
    records=[]
    for p in sorted(SOURCE.glob('*.tex')):
        s=p.read_text();key=p.name[:4]
        s=s.replace(r'\date{26 November 2026}',r'\date{26 November 2026 --- revision 01}')
        s=s.replace(r'\maketitle',r'\maketitle'+NOTICE,1)
        # Keep numbered sections and theorem numbering unchanged.
        first=s.index(r'\section{')
        s=s[:first]+ADDITIONS[key]+'\n'+s[first:]
        if key=='GR06':
            s=s.replace('With fixed orders, grading and operator bounds, for sufficiently fine grids,',
                'For $v^0\\in D(A)$ and the existing sequence in $D(A)$, with fixed orders, grading and operator bounds, for sufficiently fine grids,')
            s=s.replace(r'Let $R_D^j=',TRACE+'\n'+r'Let $R_D^j=',1)
            s=s.replace(r'Let $s=\min(2,\gamma\alpha)$.',ECS+'\n'+r'Let $s=\min(2,\gamma\alpha)$.',1)
            start=s.index(r'\begin{proof}',s.index('[Split-residual energy estimate]'))
            end=s.index(r'\end{proof}',start)
            s=s[:end]+SPLIT+s[end:]

        if key=='GR04':
            s=s.replace(r'\end{thebibliography}',r'\bibitem{dijksladky} N. M. van Dijk and K. Sladky, Monotonicity and comparison results for nonnegative dynamic systems. Part I: Discrete-time case, \emph{Kybernetika} 42 (2006), 37--56. Section 4, Results 4.1--4.2 and Corollary 4.1. \href{https://dml.cz/handle/10338.dmlcz/135698}{Primary archive}.'+'\n'+r'\end{thebibliography}')

        # End sections contain historical original diagnostic evidence.
        s=s.replace(r'\section{Finite-grid verification and next step}',r'\section{Historical finite-grid diagnostic}')
        s=s.replace(r'\section{Standalone diagnostic and remaining work}',r'\section{Historical graded diagnostic}')
        s=s.replace('No novelty claim, graded-grid estimate, independent audit or Lean certification is made.',
                    'No novelty claim, graded-grid estimate or full PDE formal certification is made in this note.')
        s=s.replace('The following argument is a proposed analytical extension pending independent review.',
                    'The following conditional analytical extension was accepted on review with the qualifications below.')
        s=s.replace('No production or repository modifications, independent proof audit or Lean compilation were performed.',
                    'These historical diagnostics predate AUD-02; the subsequent analytical audit and finite Lean coverage are distinguished above.')
        s=s.replace('No full independent proof audit, Lean compilation, or production integration has been performed.',
                    'These historical diagnostics are separate from the later AUD-02 analytical review and finite Lean certificates.')
        s=s.replace('No independent review, Lean compilation or repository modification has been performed.',
                    'The later independent review and finite Lean coverage do not turn these historical diagnostics into analytical proofs.')
        s=s.replace('No Lean, Julia, GitHub or independent audit work is claimed. GR-07 should implement and benchmark the new schemes, including a nonuniform GLL case; AUD-02 should independently review GR-01--06, in particular the Hilbert-valued consistency extension, mixed-residual proof and spatial regularity. Check relevant prior art before any novelty assertion.',
                    'GR-07 supplies the separate Julia implementation and AUD-02 reviews the analytical chain. This revision incorporates its consistency, mixed-residual and spatial-regularity qualifications. Novelty remains unresolved and is not needed for the conditional theorem.')

        s=s.replace('No source-code or repository modification, numerical replay, Lean compilation, or independent review is claimed for these notes.',
                    'Implementation validation and the exact scope of finite Lean certificates are documented separately in the AUD-02 revision-01 closure record.')
        s=s.replace('No production code, repository, or Lean project was modified.',
                    'The original production algorithms and historical evidence remain preserved separately.')
        s=s.replace(r'\section{Next steps}',r'\section{Relation to the graded analysis}')
        s=s.replace('GR-06 should relax temporal smoothness and derive residual propagation for initial layers and graded meshes;',
                    'GR-06 treats temporal initial layers and graded meshes under its separate regularity hypotheses;')
        s=s.replace('GR-03 will derive shifted product-integration weights, including the initial and final columns, and GR-04 will apply the two-kernel inequality',
                    'GR-03 derives shifted product-integration weights, including the initial and final columns, and GR-04 applies the two-kernel inequality')

        old=p.read_text()
        environments=lambda t:re.findall(r'\\begin\{(theorem|proposition|lemma)\}',t)
        tables=lambda t:re.findall(r'\\begin\{tabular\}.*?\\end\{tabular\}',t,re.S)
        assert environments(s)==environments(old),(key,'theorem count changed')
        assert tables(s)==tables(old),(key,'historical tables changed')
        q=DEST/p.name;q.write_text(s)
        records.append({'manuscript':p.name,'theorem_environments':environments(s),'historical_tables_unchanged':True})
    out=ROOT/'research/legendre/aud02/revision-01/evidence/manuscript-preservation.json'
    out.write_text(json.dumps(records,indent=2)+'\n')
    print('Six revised manuscripts; all theorem counts and historical tabular blocks preserved.')
if __name__=='__main__':main()
