# AUD-02 revision 01: research closure

**Analytical verdict: ACCEPT WITH LIMITATIONS.** The GR-01–07 programme is closed within its existing scope. The three moment findings now have explicit repairs or a justified representability restriction. No new discretization, theorem or optimization is introduced. Numerical, formal and manuscript validation pass; all six offline-built PDFs and their 30 pages have been visually inspected. Actual results are recorded in the [validation report](VALIDATION.md).

The problem couples Caputo subdiffusion to weakly singular Volterra memory. The shifted Alikhanov–PI-L/PI-Q research methods are separate from the L1/L1-2 reproduction of Sabawi et al. The conditional smooth and graded ordinary-H1 estimates assume the stated spatial-temporal regularity, a fixed self-adjoint diffusion operator and continuous coefficient representatives with pointwise nodal bounds. They do not establish that arbitrary PDE data possess that regularity.

## Read the checkpoint

| Component | Entry point |
| --- | --- |
| Research implementation and all 156 experiments | [GR-07 revision-01 study guide](../../../../studies/legendre/gr07/revision-01/README.md) |
| Revised mathematical sources and compiled PDFs | [Six manuscripts](../../../../studies/legendre/gr07/revision-01/manuscripts/) |
| Exact boundary inputs, mechanisms and correction mapping | [Repairs and manuscript corrections](REPAIRS.md) |
| Independent analytical review and dependency graph | [Original AUD-02 mathematical review](../MATHEMATICAL_REVIEW.md) |
| Formal scope and exact 54 typed statements | [Certificate explanation](../LEAN_CERTIFICATES.md), [exact current catalogue](evidence/theorem-catalogue.json), [integrated pinned project](../../verification/lean/) |
| Literature/novelty and source limitations | [Literature closure](LITERATURE.md) |
| Actual test results and replay commands | [Validation](VALIDATION.md) |

The tiny-product input has a repaired representable M0 but unrepresentable positive M1/M2. Its full tuple is deliberately rejected rather than silently returning zero. The subnormal-step and near-zero-order tuples pass unchanged relative tolerances against the high-precision oracle. All 7,941 original experimental assertions remain, with 21 additional boundary/conversion assertions.

## What remains limited

All orders and grading exponents are fixed; no order-uniform estimate is claimed. The uniform-grid resolvent and graded physical-time argument have different hypotheses. Fine-grid restrictions are sufficient, not necessary. Ordinary H1 estimates are distinct from timestep-weighted stability. The 54 compiled certificates cover finite subclaims, not complete PDE arguments.

GR-04's exact novelty remains unresolved despite further primary-source comparison. The blocked Canuto–Quarteroni locator is still unverified; GR-05 now supplies an independent projection derivation. Neither limitation is hidden or recast as independent confirmation.

The original ST-04 finite-grid candidate remains a candidate. The ST-05 eventual-contractivity conclusion does not exclude every coarse grid, and the forcing/regularity qualifications for comparison with Theorem 3.2 remain. The homogeneous observed rate near 0.7498 is not relabelled as a half-order asymptotic observation. Published-table agreement is still incomplete. No intrinsic performance benefit or new timing admission is claimed for changed code.

## Preservation and publication preparation

This prepared tree is a separate workspace based on the completed AUD-02 audit and AUD-01 commit `bf43fd0e78bcbcaae94d4c95fd9e43fd562ba477`. Its [input manifest](evidence/input-manifest.json) records 1,393 files before revision. Original GR-01–06 manuscripts, original GR-07 sources/results, AUD-02 evidence and the original development checkout remain unchanged. The [integrity report](evidence/integrity.json) identifies the five intentional navigation/tracking/Lean-root edits in the prepared copy; production source, Julia dependencies and Lean/mathlib pins are preserved.

The intended checkpoint consists of the separate GR-07 revision and manuscripts, this closure area, the preserved AUD-02 review, the integrated unchanged certificate sources and the narrow navigation/tracking changes. Runtime caches, private acquisition caches and scratch outputs under `.checkpoint-tools` are outside publication scope. Raw provenance, failed attempts and original/fresh outputs stay in the evidence directories; they are not the primary reading path. Downloaded primary papers remain local review material, distinct from the scientific source publication scope.

The [intended file list](FILES.txt), [full-tree checksums](SHA256SUMS) and [checkpoint manifest](evidence/checkpoint-manifest.json) describe the prepared tree. Local downloaded review papers and runtime caches are explicitly outside that publication inventory. Publication is authorized on the dedicated `research/legendre-verification-aud02` branch, based on the preserved AUD-01 commit. The existing development checkouts remain untouched. No merge, force-push or pull request is part of this checkpoint.
