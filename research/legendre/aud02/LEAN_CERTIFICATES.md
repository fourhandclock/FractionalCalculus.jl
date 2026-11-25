# Lean certificate catalogue and scope

All **42 existing AUD-01 named certificates** were recompiled from the preserved
five source modules. Their established count remains **41 nonduplicate identity
groups**, grouping the previously identified telescoping repetition. No prior
statement or proof changed. AUD-02 adds **12 named finite certificates** in
[Aud02Finite.lean](lean/Aud02Finite.lean), for **54 named certificates** in the
combined audit catalogue. This is a declaration count, not a count of logically
independent mathematical results. The old identity-group convention is not
extended into a claim that every new algebraic rearrangement is independent.

The useful formal coverage is finite: row-tail summation, ordered-vector
comparison, products of noncommuting positive operators under explicit cone
hypotheses, exact stencil moment algebra, and polarized energy algebra.
Continuous fractional integrals, gamma/beta analysis, infinite Neumann limits,
Sobolev approximation and the fully discrete PDE theorems remain analytical.

## Pinned environment and compiler results

The unchanged project uses Lean **4.19.0** and mathlib revision
`c44e0c8ee63ca166450922a373c7409c5d26b00b` (v4.19.0), with the existing
transitive lockfile. Existing precompiled caches were reused read-only. No
`lake update`, dependency download, pin change or full mathlib rebuild occurred.
Local modules were compiled serially with `-j1`; exact commands and finite
limits are in [the execution records](evidence/runs/).

Every accepted declaration has a successful `#print axioms` result. Only
`propext`, `Classical.choice` and `Quot.sound`, the standard Lean/mathlib
foundations, appear. No new unsupported axiom, `sorryAx`, `sorry` or `admit`
is accepted. See [the machine-readable inventory](evidence/lean-audit.json),
[the new audit output](evidence/runs/aud02-lean-aud02axioms-01.stdout.log), and
the three existing audit outputs:
[coefficients](evidence/runs/aud02-lean-coefficientsaxioms-01.stdout.log),
[quadrature](evidence/runs/aud02-lean-quadratureaxioms-01.stdout.log),
[AUD-01](evidence/runs/aud02-lean-aud01axioms-01.stdout.log).

Two unsuccessful new-proof compilations are retained as attempts 01 and 03.
Attempt 01 lacked the finite ring-sum import. Attempt 03 had an incomplete
tactic sequence for the unchanged forward mass identity. Attempt 02 compiled
the initial nine statements; attempt 04 compiles all 12 final statements.
The two nonfatal tactic-style warnings in attempt 04 are recorded. They do
not bypass proof checking. No failed draft is described as certified.

## Exact meaning of the new certificates

All scalars are real. The finite sets and all explicit hypotheses are part
of the statements, not computational observations. The namespace is
`LegendreAudit.AUD02`.

| Name | Statement certified |
| --- | --- |
| `row_tail_identity` | For finite $S\subset\mathbb N$, arbitrary $w,dv$: the row sum $\sum_{k\in S} w_k\sum_{m\in S,m\le k}dv_m$ equals $\sum_{m\in S}dv_m\sum_{k\in S,m\le k}w_k$ |
| `ordered_vector_domination` | Under $dv_m\ge0$ and every tail of $w$ bounded by the corresponding tail of $d$, the preceding row sum for $w$ is no larger than the row sum for $d$ |
| `increment_reconstruction` | For every $n\ge0$, $\sum_{j<n}(v_{j+1}-v_j)=v_n-v_0$ |
| `finite_word_domination` | For finite-dimensional pointwise-ordered vectors, monotone maps $B_i$, maps $D_i$ preserving an explicitly supplied cone, $B_iv\le D_iv$ on that cone, and initial $v$ in the cone: every finite ordered B-word applied to $v$ is bounded by the same D-word |
| `cumulative_weights` | For all $m,n\in\mathbb N,C\in\mathbb R$, $\sum_{j<n}C[f(m+j+1)-f(m+j)]=C[f(m+n)-f(m)]$ |
| `shifted_energy_identity` | For arbitrary finite $h_j,v_j,v_n,v_*$, $2\sum h_j(v_n-v_j)v_*-\sum h_j(v_n^2-v_j^2)=\sum h_j(v_*-v_j)^2-(\sum h_j)(v_n-v_*)^2$ |
| `linear_absolute_basis` | On $0\le x\le1$, $\lvert1-x\rvert+\lvert x\rvert=1$ |
| `quadratic_absolute_basis` | On $0\le x\le1$, the absolute sum of the three forward uniform Lagrange basis polynomials is $1+x(1-x)\le5/4$ |
| `quadratic_negative_weight` | The exact rational GR-03 initial-weight bracket with $D=31/20,r=1/10$ equals $-17/231$ |
| `forward_moment_identities` | For $R>0$, the coefficients of the nonuniform forward stencil $0,1,1+R$, defined from arbitrary $M_0,M_1,M_2$, satisfy $f_0+f_1+f_2=M_0, f_1+(1+R)f_2=M_1, f_1+(1+R)^2f_2=M_2$ |
| `backward_moment_identities` | For $\rho>0$, the coefficients of the backward stencil $-\rho,0,1$ satisfy $f_0+f_1+f_2=M_0, -\rho f_0+f_2=M_1, \rho^2f_0+f_2=M_2$ |
| `complementary_composition` | For finite $S$, assuming $\sum_{j\in S}P_jA_{jk}=1$ for every $k\in S$, $\sum_jP_j\sum_kA_{jk}dv_k=\sum_kdv_k$ |

The row-tail identity plus increment reconstruction represents any nonnegative
nondecreasing finite vector starting from zero before its first component.
The ordered-vector theorem does not assert domination on arbitrary vectors.
The word theorem takes positivity/monotonicity and cone invariance as explicit
hypotheses; it does not itself prove the Toeplitz construction, commutation,
or an infinite resolvent bound. `cumulative_weights` becomes the Toeplitz
row-tail identity on substituting $f(j)=(j\tau)^s$; no real-power monotonicity
theorem is certified here.

The moment identities certify the coefficient collection for both nonuniform
stencils; the integral evaluation of $M_j$ is not formalized. The scalar
energy identity extends componentwise to finite Euclidean sums analytically,
but no arbitrary Hilbert-space energy theorem is claimed as a new Lean result.
The complementary theorem is conditional on column identities; positivity and
the recursive construction of the actual Alikhanov complementary kernels remain
analytical arguments. None of these distinctions is removed by compilation.

## Preserved earlier coverage

The complete [AUD-01 exact-statement catalogue](../verification/reviews/AUD-01/revision-01/LEAN_CATALOGUE.md)
and [original project README](../verification/lean/README.md) remain the
human-readable statement source for the earlier 42 declarations. The new
machine-readable inventory lists every old and new theorem name, source module
and actual axiom dependencies, so none is hidden by the summary below.

| Preserved source module | Named declarations | Certified scope |
| --- | ---: | --- |
| `Coefficients.lean` | 17 | Endpoint L1-2 coefficient algebra, real-power sign witness, signed-history statements, telescoping and norm/Volterra constants |
| `Quadrature.lean` | 6 | Concrete M=3 GLL polynomial, exact integral, positivity and discrepancy |
| `AuditConstants.lean` | 9 | Symbol polynomial algebra and rational perturbation constants |
| `Aud01FiniteSums.lean` | 3 | All-length finite summation and quadratic history identities |
| `Aud01Oscillator.lean` | 7 | Exact oscillator derivatives, endpoint identities and energy algebra |

Earlier certificates do not prove the complete AUD-01 analytical arguments,
the GR-01–06 PDE programme, a numerical trajectory's correctness, or a novelty
claim. Recompilation preserves that scope.
