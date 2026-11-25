# AUD-01 revised research checkpoint

**Verdict: ACCEPT WITH LIMITATIONS.** The reviewed analytical results are acceptable with the corrected hypotheses and theorem interpretations below. All available identified original Python diagnostics pass unchanged. Missing older programs still limit numerical reproducibility; the complete PDE arguments are not Lean-certified.

Read the [revised mathematical manuscript (PDF)](mathematical-verification-aud01-r1.pdf), with its [LaTeX source](mathematical-verification-aud01-r1.tex), for the proofs. The [independent review](REVIEW.md) explains the corrections and their consequences. The [numerical replay](NUMERICAL_REPLAY.md), [diagnostic inventory](DIAGNOSTIC_INVENTORY.md), and [Lean catalogue](LEAN_CATALOGUE.md) describe the different kinds of evidence.

## Mathematical status

The study concerns a Caputo time-fractional diffusion equation with weakly singular Volterra memory. It separates the published formulas from the interpolation-defined L1–2 scheme and asks whether consistency, stability, and convergence claims follow under their stated assumptions.

| Investigation | Current conclusion |
| --- | --- |
| VQ-01 / Observation 8 | Verified discrepancy: the printed Volterra quadrature has sharp general order $1-\beta$, rather than the claimed $2-\beta$. This alone does not decide full PDE convergence. |
| CF-02 / Observation 2 | Verified algebraic discrepancy in the printed L1–2 coefficient collection; post-startup $d_0>1$ and some historical coefficients are negative. |
| ST-03 | Verified gap in the signed-history contraction argument. Mixed signs alone do not establish instability. |
| ST-04 | Finite-grid amplification candidate, reproduced for both derivative schemes and both memory rules; its own all-fine-grid claim remains unproved. |
| OB-03 / OB-04 | Verified startup consistency and variable-coefficient GLL exactness defects, within their explicit example classes. Neither alone refutes the complete convergence theorem. |
| SP-01 / SP-02 | Conditional spatial convergence and finite-time stability accepted on review. Nodal applications now require continuous coefficient representatives and uniform pointwise bounds. The finite-time constant is not a contraction factor of one. |
| TM-01 | Standalone smooth **forced** temporal sharpness and an initial-layer upper bound accepted on review. |
| AUD-01 | Standalone **homogeneous, initially singular** half-order sharpness accepted analytically. Tested grids show approximately 0.75, not 0.5. |
| ST-05 | Analytical all-fine-grid failure of eventual contractivity accepted for its fixed smooth positive kernel and fixed admissible orders. This separate construction does not exclude contraction on every possible coarse grid. |

The smooth forced and homogeneous initially singular examples do not constitute a single smooth homogeneous counterexample. Their comparison with the intended regularity class of Theorem 3.2 remains qualified. ST-05 addresses the eventual fine-grid interpretation of Theorem 3.1; the paper also contains a weaker, isolated-existence wording. [The review](REVIEW.md#theorem-interpretation-and-temporal-sharpness) gives both quantifiers.

## Evidence and reproduction

The four available identified originals and the existing independent 10-test suite pass in an isolated environment with NumPy 2.3.5, SciPy 1.17.0, mpmath 1.3.0, and SymPy 1.14.0. All executions were serial and bounded. [Reproduction instructions](NUMERICAL_REPLAY.md#reproduction) and complete command/output records are retained separately from the mathematical source.

The pinned Lean project retains 23 ST-04 and 19 AUD-01 named certificates. A fresh combined type and axiom inspection covers all **42 declarations**. Accounting for one repeated telescoping identity gives **41 nonduplicate identity groups**, under the catalogue's stated counting convention. This counts finite propositions, not independently proved PDE theorems.

The revised manuscript compiles offline to **37 pages**. An initial missing-font failure and the successful build are both retained. Ten referenced original program groups remain unavailable or unauthenticated after the documented search; related starter programs have not been substituted for them.

## Preservation and scope

This revision is a new document, not an overwrite of the supplied manuscript. The [provenance record](revision-provenance.json) and [patch](manuscript-changes.patch) identify its changes. The [previous review](../REVIEW.md) remains an archival snapshot: its dependency-pending statements are superseded by the fresh replay report here.

Both the **294-file original inventory** and the **49-file review/Lean guard** match byte-for-byte (335 distinct paths; eight occur in both inventories); see [integrity checks](INTEGRITY.json) and the [preserved-input manifest](preserved-inputs.json). Existing navigation work, production algorithms, historical outputs, and the pinned Lean project are preserved. The preexisting missing ST-04 PDF at its old manifest path remains unresolved. No Julia experiments were rerun for this documentation correction. No commit, push, merge, or pull request was made.

From the repository root, the new [documentary integrity validator](validate_checkpoint.py) checks source/output hashes, certificate bindings, unchanged assertions, original numbered equations, and new Markdown links without running the experiments:

```bash
python3 -B research/legendre/verification/reviews/AUD-01/revision-01/validate_checkpoint.py
```

The [checkpoint summary](CHECKPOINT.json) records the current verdict and limitations. The remaining work is recovery of missing diagnostics and primary-reference locators, and clarification of the original theorem's intended solution class. This checkpoint introduces no new numerical method or stability theorem.
