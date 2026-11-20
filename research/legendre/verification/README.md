# Legendre verification checkpoint through ST-04

This record preserves the mathematical audit of Sabawi et al. (2025), independent numerical regressions, and a small Lean 4/mathlib project. Start with the [original-author LaTeX document](mathematical-verification.tex), [supplied ST-04 PDF](sources/legendre_spectral_verification_notes_st04.pdf), and [checkpoint report](CHECKPOINT_REPORT.md). The main TeX is byte-identical to the original supplied ST-04 source. The earlier [ST-03 transcription](sources/mathematical-verification-st03-transcription.tex) and [historical integration report](INTEGRATION_SUMMARY.md) remain available.

| Item | Mathematical status |
| --- | --- |
| Observation 1 / ST-03 | Established gap in the signed-history contraction induction; Theorem 3.1 unresolved |
| Observation 2 / CF-02 | Verified algebraic discrepancy in printed L1-2 coefficients, indexing, and normalization |
| Observation 3 | Provisional explicit startup test case; early-index and fixed-time estimates must be distinguished |
| Observation 4 | Provisional spatial-proof qualification; the concrete M=3 polynomial example is isolated from the full theorem |
| Observation 5 | Timestep-dependent norm interpretation caveat |
| Observation 6 | Numerical error-normalization check |
| Observation 7 | Kernel-sign assumptions check |
| Observation 8 / VQ-01 | Verified inconsistency of Eq. (8)'s claimed order for printed Eq. (6); sharp general order 1−β |
| ST-04 | Strong finite-grid numerical counterexample candidate with a smooth positive time-dependent kernel; no all-fine-grid theorem refutation |

“Verified” distinguishes exact mathematical discrepancies from numerical observations and unresolved theorem questions. Small Lean certificates cover only their explicitly stated algebraic/integral claims. They do not formalize Theorem 3.1, the full PDE, or an arbitrarily-fine-grid ST-04 counterexample.

| Record | Contents |
| --- | --- |
| [Checkpoint report](CHECKPOINT_REPORT.md) | Release scope, actual validation, mathematical limits, and complete changed-file list |
| [Reproduction instructions](REPRODUCE.md) | Pinned tools, commands, caches, limits, and failure handling |
| [ST-04 provenance and implementation audit](ST04_PROVENANCE.md) | Original source comparison, exact parameters, residual scope, and actual library behavior |
| [Observation dossier](observations/README.md) | Claims, hypotheses, derivations, computations, results, limitations, and dependencies |
| [Lean certificates](lean/README.md) | Exact theorem statements and current machine-check status |
| [Validation report](results/VALIDATION.md) | Actual run results, preserved failures, and remaining limitations |
| [Input manifest](sources/inputs.json) | Portable names and SHA-256 identifiers for supplied/historical inputs |
| [Literature boundaries](literature/README.md) | Published claims, source-reported independent work, and our derivations |
| [Commit scope](CHECKPOINT_SCOPE.md) | Narrow tracking exception and exclusion of unrelated pending changes |
| [Run evidence](results/checkpoint-st04/) | Complete command/output records, exact attempted sources, parameters, and printed observations |

The fresh numerical checks passed: **669 Julia assertions**, **10 independent Python regression tests**, **432 ST-03 parameter cases**, and **24 ST-04 configurations**. The original LaTeX compiled to **13 pages**, and **23 Lean theorems** compiled with an axiom audit containing only standard Lean/mathlib axioms. Full results, warnings, failed attempts, and precise certificate scope are in the validation report.

The production Caputo weights, Volterra quadrature, PDE solver, examples, error definitions, published targets, and earlier numerical results are preserved. L1-2 already follows the interpolation-defined two sums, while singular memory follows printed Eq. (6). Product integration exists only in the supplied independent ST-04 control and is not inserted into the reproduction library. The actual-library regressions are in [proof_audit.jl](../../../studies/legendre/test/proof_audit.jl).

The existing ignore rules now expose only this verification subtree. Toolchains, `.lake`, TeX build outputs, prior private integration inventories, and other research remain excluded. The checkpoint is built from the intended Legendre tree; pre-existing metric-graph work and line-ending-only changes remain local and unstaged.
