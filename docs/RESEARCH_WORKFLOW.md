# Research workflow and documentation ownership

This framework keeps reusable numerical operators in `src/`, paper-specific reproduction studies in `studies/`, and mathematical investigations in `research/`. Start with the [repository overview](../README.md#research-framework), then a study's own guide. The [Legendre study](../studies/legendre/README.md) is the first study with a completed, validated research checkpoint; its remaining numerical mismatches and theorem questions stay explicit.

## Reading and working sequence

1. **Understand the paper and implemented problem.** Read the study guide, source paper, named cases, and implementation map.
2. **Assess reproduction.** Compare saved targets, computed values, error definitions, and rates. Use the study tests for implementation checks; use a separate output directory for new comparisons.
3. **Audit the mathematics.** Use the verification dashboard to reach the full manuscript, observation dossiers, theorem certificates, independent experiments, and literature qualifications.
4. **Reproduce a claim.** Follow the current replay guide for its assumptions, parameters, toolchain, and commands. Read the dated validation report before interpreting a historical count as a current execution.
5. **Trace the evidence.** Consult retained inputs and checkpoint logs when a source identity, failure, or numerical observation needs inspection. Keep new execution records separate from existing evidence.

For Legendre, the [study guide](../studies/legendre/README.md), [verification dashboard](../research/legendre/verification/README.md), [replay guide](../research/legendre/verification/REPRODUCE.md), and [dated validation report](../research/legendre/verification/results/VALIDATION.md) provide this sequence.

## Proposed directory architecture

The long-term architecture standardizes these roles for future papers while retaining the existing Legendre paths:

```text
README.md                              Framework purpose, study catalogue, shared setup
docs/
  RESEARCH_WORKFLOW.md                  Workflow and documentation ownership
src/                                   Reusable numerical operators and solvers
test/runtests.jl                        Discovers study test entry points
studies/<paper>/
  README.md                            Problem, implementation, reproduction status, navigation
  cases.jl                             Paper-specific problems
  test/runtests.jl                      Study checks
  run.jl                               Experiment/table runner
  reference_tables.csv                 Published targets, when applicable
  results/                             Saved numerical comparisons and rates
  figures/                             Figures with parameters and underlying data
research/<paper>/verification/
  README.md                            Current research dashboard
  mathematical-verification.tex        Preserved ST-04 manuscript
  sources/                             Supplied inputs and provenance manifests
  reviews/AUD-01/revision-01/           Accepted current manuscript and review closure
  observations/                        Claims, hypotheses, findings, limitations
  lean/                                Pinned proof project and theorem catalogue
  scripts/                             Independent mathematical/numerical checks
  literature/                          References and source-verification boundaries
  REPRODUCE.md                         Current commands, versions, parameters, limits
  results/VALIDATION.md                 Dated validation summary
  results/<checkpoint>/                Immutable execution evidence
```

This is a documentation convention and a proposal for future studies. No directories have been moved. Paper-specific needs can adapt the template. Additional research material should enter tracking through a deliberate narrow scope; the present ignore exception publishes only Legendre verification. Shared `src/` code should be described as reusable according to its actual capabilities, with each study recording its own assumptions and reconstruction choices.

## Documentation ownership and consolidation plan

The following recommendations identify overlap; historical reports remain in place.

| Overlap | Preferred ongoing responsibility | Recommended later consolidation |
| --- | --- | --- |
| Root README and detailed Legendre descriptions | Root: framework catalogue and shared setup. [Study guide](../studies/legendre/README.md): paper-specific problem, implementation, results, and entry points | Replace duplicated root study detail with a short catalogue entry and link after a separate review. Preserve the protected opening and unrelated study sections |
| [Dashboard](../research/legendre/verification/README.md), [checkpoint report](../research/legendre/verification/CHECKPOINT_REPORT.md), [ST-03 integration summary](../research/legendre/verification/INTEGRATION_SUMMARY.md) | Dashboard: current status and next questions. Reports: dated integration/release history | Update status in the dashboard; retain reports as historical records with their original scope |
| [REPRODUCE.md](../research/legendre/verification/REPRODUCE.md) and [TEST_PLAN.md](../research/legendre/verification/results/TEST_PLAN.md) | Replay guide: current supported commands. Historical plan: original predictions and tolerances | Link the historical plan where needed; avoid copying obsolete environment statements into current instructions |
| [VALIDATION.md](../research/legendre/verification/results/VALIDATION.md), dashboard counts, and raw logs | Dated validation report: what ran and its limitations. Dashboard: short attributed checkpoint summary | Record future runs separately and link their summaries; retain the ST-04 evidence unchanged |
| [ST04_PROVENANCE.md](../research/legendre/verification/ST04_PROVENANCE.md), [PROVENANCE.md](../research/legendre/verification/PROVENANCE.md), [CHECKPOINT_SCOPE.md](../research/legendre/verification/CHECKPOINT_SCOPE.md) | Current provenance: supplied inputs and implementation comparison. Historical provenance: ST-03 source locators. Scope: original release boundaries | Create one provenance index if further checkpoints accumulate; link dated records instead of merging away their history |
| Dashboard summaries and [Lean catalogue](../research/legendre/verification/lean/README.md) | Catalogue: exact certified statements and toolchain. Dashboard: certificate scope and links | Maintain theorem details in the catalogue; keep broader PDE questions explicitly separate |

The manuscript's retained supplied copy, earlier transcription, and attempted-source snapshots serve distinct provenance roles. They are intentional preservation, rather than candidates for deduplication. Likewise, the 165 ST-04 evidence files and later AUD-01 review/integration records include successes, failures, source snapshots, and metadata. Keep them behind their dated validation reports in the reading path. Directory browsing and historical logs should not replace the manuscript, tests, or certificate catalogue as scientific entry points.

## Source material and execution evidence

| Material | Interpretation |
| --- | --- |
| Source paper | Published claims under investigation |
| Independent manuscript and observation dossiers | Our derivations, exact assumptions, and qualified mathematical findings |
| Lean source and theorem catalogue | Precisely stated certificates; compilation status belongs to a recorded toolchain/run |
| Julia/Python sources | Reproducible experiments and checks; source presence alone is not an execution |
| Supplied inputs and manifests | Provenance, including author-supplied historical outputs |
| Dated validation reports and checkpoint directories | What was actually executed, with hashes, failures, warnings, and observed results |

Keep confirmed discrepancies, proof gaps, numerical candidates, and unresolved questions distinct. The first completed checkpoint does not imply that the paper's tables, stability theorem, or convergence theory have all been reproduced.
