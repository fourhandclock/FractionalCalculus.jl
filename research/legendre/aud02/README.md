# AUD-02: independent review of the GR-01–GR-07 programme

**Overall verdict: ACCEPT WITH LIMITATIONS.** The conditional analytical
results survive this adversarial review under their stated strong assumptions.
The admitted numerical experiments reproduce. Three extreme-input failures in
the generic moment API require repair or a narrower supported domain before
broader use. No complete PDE theorem is Lean-certified, and GR-04 novelty
remains unresolved.

The problem is a Caputo subdiffusion equation with a weakly singular Volterra
memory term and homogeneous Dirichlet diffusion. GR-01–06 analyze shifted
Alikhanov time differentiation with linear or quadratic product integration,
including smooth and initially singular solutions. GR-07 implements those
methods separately from the published-scheme reproduction. The main review
question is whether positive comparison and residual propagation genuinely
support ordinary H1 stability/convergence, especially on graded meshes.

## Read the findings

| Document | Purpose |
| --- | --- |
| [Mathematical review](MATHEMATICAL_REVIEW.md) | Exact manuscript locators, result classifications, independent proof-chain checks, dependency graph, counterexamples and correction requirements |
| [Implementation review](IMPLEMENTATION_REVIEW.md) | Formula correspondence, independent probes, three moment failures, continuous error norms and performance scope |
| [Lean catalogue](LEAN_CERTIFICATES.md) | Preserved 42 certificates, 12 new finite certificates, precise statements and axiom audits |
| [Literature comparison](LITERATURE.md) | Primary-source locators, prior methods, access limitations and unresolved novelty |
| [Validation and reproduction](VALIDATION.md) | Actual test results, exact environments, failures, safeguards and replay commands |

The row-tail theorem is accepted with its **ordered-vector** hypothesis and
commutation only of the Toeplitz majorants. The graded bound in ordinary H1 is
accepted under the written Hm-valued temporal regularity, continuous coefficient
representatives, Ritz initialization and fixed-operator assumptions. It is not
an existence/regularity result for arbitrary input data. Finite-grid rates and
implementation timings do not prove asymptotic convergence or intrinsic
algorithmic superiority.

The original ST-04/AUD-01 qualifications remain intact: signed-history proof
gaps are not instability proofs, finite-grid candidates are not all-grid
theorem refutations, and forcing/regularity and theorem-quantifier distinctions
must be retained. The observed homogeneous rate near 0.7498 is not relabelled
as confirmation of a half-order regime.

## Evidence and preservation

The input is the completed local `research/legendre-gr07` worktree at AUD-01
baseline `bf43fd0e78bcbcaae94d4c95fd9e43fd562ba477`, including uncommitted GR-07
work. Before review, **1,041 source/evidence files** were inventoried and copied
to this isolated workspace. They remain byte-for-byte unchanged in both copies.
The prior 481-file guard for the original development checkout also passes,
including its navigation and metric-graph work. See the [source manifest](evidence/SOURCE_MANIFEST.json)
and [final integrity record](evidence/integrity.json).

Fresh raw evidence is in [evidence/runs/](evidence/runs/), independent probe and
matrix outputs in [evidence/targeted/](evidence/targeted/), and approved primary
paper downloads in [literature/](literature/). Historical GR-07 evidence stays
in its [original study directory](../../../studies/legendre/gr07/), including
the explicitly invalid initial reference run. Detailed execution metadata is
kept behind those links rather than serving as the reading order.

Only this new review area and disposable local runtime/cache links were added
to the isolated copy. Production algorithms, the Julia project, Lean pins,
original manuscripts/results and the original checkout were not changed.
No commit, push, merge, publication or checkpoint integration was performed.
The [review plan](PLAN.md) records the criteria fixed before numerical probes.
