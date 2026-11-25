# AUD-01 clean-tree validation

**Verdict: ACCEPT WITH LIMITATIONS.** This integration replays the accepted research against a clean branch while preserving its analytical qualifications. Numerical and formal checks support the particular statements below; they do not certify the complete PDE theory.

## Actual executions

| Check | Result | Retained record |
| --- | --- | --- |
| Julia 1.12.6 root regression suite | **669/669 pass**, including actual-library `proof_audit.jl` | [Julia output](julia-regression-01.stdout.log), [command and source hashes](julia-regression-01.json) |
| Supplied AUD-01 exact checker | Pass; identical stdout to the previous replay and supplied exact output | [Output](python-exact-01.stdout.log), [record](python-exact-01.json) |
| Supplied homogeneous checker | **12 configurations pass** unchanged | [Output](python-homogeneous-01.stdout.log), [record](python-homogeneous-01.json) |
| Original ST-03 recurrence diagnostic | **432 cases pass**, maximum representation discrepancy 3.77e-15 | [Output](python-st03-01.stdout.log), [record](python-st03-01.json) |
| Original ST-04 variable-kernel diagnostic | **24 configurations pass**: both derivative schemes, printed quadrature/product-integration control | [Output](python-st04-01.stdout.log), [record](python-st04-01.json) |
| Later independent regression suite | **10 tests pass**; not a recovered original companion | [Output](python-regressions-01.stderr.log), [record](python-regressions-01.json) |
| Lean source compilation | All **five proof modules** compile serially, preserving 23+19 named certificates | [Coefficients](lean-coefficients-01.json), [quadrature](lean-quadrature-01.json), [constants](lean-constants-01.json), [finite sums](lean-finite-sums-01.json), [oscillator](lean-oscillator-01.json) |
| Complete Lean type/axiom audit | **42 names** checked; only `propext`, `Classical.choice`, `Quot.sound` | [Full audit](lean-all-axioms-01.stdout.log), [record](lean-all-axioms-01.json) |
| Accepted LaTeX source | Successful offline **37-page** rebuild | [Record](latex-aud01-01.json), [engine log](latex-aud01-01.engine.log) |
| Documentation and integrity | Local links, source/evidence identities, unchanged assertions and configuration scope checked separately | [Integrated checks](integrity.json), [checker](../../scripts/check_aud01_checkpoint.py) |

All scientific execution attempts in this integration pass. Earlier unsuccessful builds, proof drafts and validator attempts remain in their original archives; none is erased or counted as a success. The first integration link check misread `J[a](t_n)` inside an indented code block as a Markdown link. The parser now excludes code blocks/spans; the failed check and exact attempted source are retained, and no scientific assertion changed. The exact commands, durations and resource limits are in the individual records above. The [complete staged whitespace check](staged-whitespace-check.txt) returns 2 for retained source/log whitespace and snapshot EOFs; [the review](whitespace-review.json) records these warnings. Current authored documentation/configuration/checker whitespace checks pass. Original manuscripts and execution output were not normalized to silence this lint result.

## What the numerical data show

The homogeneous last-doubling rates remain **0.7498 for both L1 and L1–2**, with negative normalized total signed residual and positive memory residual on the tested range. This is not numerical confirmation of the asymptotic half-order regime. The standalone half-order theorem is analytical and has an initial-layer hypothesis; it is not a smooth homogeneous example.

The four original-program stdout files are byte-identical to their revision-01 replay counterparts; [summary.json](summary.json) records their hashes. The older supplied homogeneous output differs at roundoff-sized printed fields, as retained in the [earlier replay comparison](../../reviews/AUD-01/revision-01/replay-comparison.json). Neither historical nor fresh output was overwritten. All acceptance assertions/tolerances are unchanged.

ST-04 remains its own finite-grid candidate. The separate ST-05 analytical construction concerns every sufficiently fine grid for fixed data; it does not exclude every coarse mesh. No unavailable ST-05 trajectory program was represented as executed.

## Formal and manuscript scope

The **42 named Lean declarations** form **41 nonduplicate identity groups**, grouping only the repeated telescoping identity under index reversal/rearrangement. This is not a count of logically independent results. [The catalogue](../../reviews/AUD-01/revision-01/LEAN_CATALOGUE.md) gives exact statements and the analytical arguments outside their scope. Fresh compilation and axiom inspection bind the unchanged source statements to this pinned project; no theorem, axiom or dependency revision changed.

The accepted source and supplied PDFs remain byte-identical to the review inputs. The rebuilt PDF stays in ignored scratch space, with its hash recorded in [summary.json](summary.json); it does not overwrite the accepted PDF. The final engine log has no undefined references, undefined commands or overfull boxes. Six underfull paragraph warnings and host Fontconfig warnings remain. The accepted revision's visual review is preserved in its [artifact record](../../reviews/AUD-01/revision-01/manuscript-artifact.json); this integration changes no typeset mathematical source.

## Preservation and limitations

[The integration input manifest](inputs.json) protects **243 base files**, **141 transferred archival inputs** and **eight Lean source files**. It includes the original numerical algorithms, dependencies, historical results, ST-04 evidence and all earlier proofs. The accepted revision and its failed-attempt/source snapshots are transferred unchanged. The main branch base and exclusions are recorded in [SCOPE.md](SCOPE.md).

[Workspace preservation](workspace-preservation.json) confirms all **440 pre-integration paths**, the original Git index and status are unchanged, including unrelated metric-graph work and pending navigation/data edits. Its 294-file historical audit is not the identity of this clean checkout: the clean branch deliberately excludes unrelated local additions and retains the ST-04 PDF from Git. The archived workspace-specific validator therefore remains historical; the new release checker verifies the actual integration scope without changing its assertions.

Ten referenced original diagnostic groups remain unavailable or unauthenticated. Related-work primary theorem locators are still unverified. Spatial applications require compatible continuous representatives and pointwise nodal bounds; the replacement estimates retain their product-regularity, fixed-order, uniform-grid and timestep-weighted-norm assumptions. Theorem 3.2's intended forcing/regularity class and Theorem 3.1's isolated-existence wording remain qualified. Complete PDE stability and convergence arguments remain analytical rather than Lean-certified.

## Environment and safeguards

[environment.json](environment.json) records the reused binaries and exact Python versions. Julia project/manifest and Lean/mathlib pins are unchanged. No additional dependencies were acquired; no global environment was modified. The first Julia depot is isolated and writable; an existing depot supplies cached dependencies. Lean reuses cached mathlib packages and writes newly compiled local modules only to the worktree's ignored build directory.

Runs were serial, with one CPU affinity and Julia/BLAS/Lean worker. Julia used 300 s wall / 240 s CPU, 8 GiB per-process address space and 3 GiB sampled RSS; Lean modules used 120 s / 90 s, 8 GiB address space and 3.5 GiB sampled RSS. Python and LaTeX limits are retained per record. Log/file ceilings and process-group cleanup apply. These safeguards are resource-conscious per-process/sampled controls, not cgroup aggregate isolation. [Reproduction instructions](../../REPRODUCE.md) explain safe replay without rewriting historical outputs.
