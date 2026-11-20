> Historical ST-03 integration report. The current ST-04 checkpoint is described in [CHECKPOINT_REPORT.md](CHECKPOINT_REPORT.md). Statements below about unavailable tools and local-only work describe that earlier session.

# Integration deliverables

The mathematical audit has been integrated into the existing `research/legendre/verification/` directory, alongside its two earlier source-page images. This follows the repository's study layout and local-research convention. The [entry point](README.md), [complete LaTeX transcription](sources/mathematical-verification-st03-transcription.tex), and [observation dossier](observations/README.md) can be reviewed independently of the lost conversation. No numerical method was replaced, no old result was deleted, and no Git or remote operation was performed.

## A. Integration and provenance

All 11 pages of the supplied verification PDF were read. The original PDF, ST-03 Python file, and supplied stdout were copied byte-for-byte, with hashes. The new TeX document preserves sections 1–7, all eight observations, five propositions and their proofs, 22 numbered equations, both numerical tables, source references, and the original qualifications. It explicitly identifies new transcription/evidence notices and does not claim recovery of original LaTeX. A page-by-page [coverage and locator record](PROVENANCE.md) connects the text to both the supplied notes and published source.

The existing implementation already uses interpolation-defined L1-2 coefficients and literal Eq. (6) memory quadrature. It remains useful as the reproduction baseline; the preserved discrepancies are not silently repaired. Printed coefficient alternatives and corrected collections remain separate in the new regression sources. Product integration remains a documented candidate only.

## B. Complete file changes

Only these pre-existing files were modified:

| Project-relative path | Change |
| --- | --- |
| `README.md` | Added one paragraph linking the verification record; the protected opening and all other original bytes are preserved |
| `studies/legendre/test/runtests.jl` | Added only `include("proof_audit.jl")` |

Created outside the verification directory:

| Project-relative path | Purpose |
| --- | --- |
| `studies/legendre/test/proof_audit.jl` | Coefficient/sign/index regressions against the actual Julia library and the M=3 variable-coefficient LGL example |

Every other created file is listed below relative to `research/legendre/verification/`:

| File | Purpose |
| --- | --- |
| `README.md` | Audit entry point, status overview, navigation, and compilation instructions |
| `INTEGRATION_SUMMARY.md` | This deliverables and change record |
| `PROVENANCE.md` | Repository reconnaissance, input provenance, full source coverage, exact locators, and missing-source qualifications |
| `mathematical-verification.tex` | Full mathematical transcription, with original logical order and evidence notices |
| `observations/README.md` | Claim, hypotheses, derivation locator, computation, result, limits, and dependencies for all eight observations; prioritized next research |
| `literature/README.md` | Citation provenance and limits on independent confirmation |
| `scripts/verify_l12_stability.py` | Unchanged supplied ST-03 diagnostic |
| `scripts/check_counterexamples.py` | Newly authored deterministic standard-library regressions; separate printed and corrected formulas |
| `scripts/check_integration.py` | Reproducible static syntax, links, TeX-structure, and integrity audit; executes no numerical code |
| `sources/legendre_spectral_verification_notes_st03.pdf` | Original supplied notes PDF, preserved byte-for-byte |
| `sources/st03_verification_results.txt` | Original supplied historical output, preserved byte-for-byte |
| `sources/input-manifest.json` | Input paths, byte counts, hashes, and original-TeX availability |
| `sources/verification-notes-extracted.txt` | Secondary Poppler text extraction; source PDF remains authoritative |
| `results/TEST_PLAN.md` | Parameters, domains, tolerances, predictions, replay commands, and preflight requirements |
| `results/VALIDATION.md` | Actual checks, initial static failures, unavailable execution, and historical evidence boundaries |
| `results/integration-2026-11-20/baseline-inventory.json` | SHA-256 inventory of all 83 pre-integration project files, excluding `.git` and runtime cache directories |
| `results/integration-2026-11-20/execution-preflight.json` | Actual executable availability, read-only cgroup inspection, and blocked-before-launch numerical decision |
| `results/integration-2026-11-20/static-validation-01.json` | Initial static audit, retaining two documentation-check failures |
| `results/integration-2026-11-20/static-validation-02.json` | Corrected static audit: all 18 checks passed |
| `results/integration-2026-11-20/static-validation-03.json` | Final static replay after adding the completed documentation/index |
| `results/integration-2026-11-20/file-changes.json` | Final project-relative created/modified/deleted list and file hashes; explicitly excludes a recursive self-hash |

The pre-existing `page39.png` and `page42.png` are unchanged. No files in `src/`, cases, the original test bodies, dependency configuration, CSVs, figures, earlier research notes, license, ignore configuration, or source papers were altered. The machine-readable change record is generated after final validation; no numerical output is generated in that step.

## C. Observation status

| Observation | Preserved finding | Limit |
| --- | --- | --- |
| 1 / ST-03 | Established gap in coefficient-based contraction induction for signed histories | Theorem 3.1 remains unresolved; assigned states are not an evolution trajectory |
| 2 / CF-02 | Verified coefficient/indexing/normalization discrepancy; post-startup `d₀=1+α/[2(2−α)]`, negative coefficient at α=3/4 | Does not imply instability; authors' implementation remains unknown |
| 3 | Provisional explicit startup test: nonzero `τ^(2−α)` first-panel contribution at t₂ for `u=t²` | Uniform early-index and fixed-positive-time statements must be distinguished |
| 4 | Provisional exactness qualification; positive variable-coefficient example with mass discrepancy `32c/525` retained | Full variable-coefficient spatial proof audit incomplete |
| 5 | Provisional interpretation caveat on timestep-dependent H¹-type norm | Fixed-τ equivalence does not provide uniform standard-H¹ control |
| 6 | Numerical reproduction check on the extra spatial-node normalization | Reported and conventional quadrature metrics remain distinct |
| 7 | Assumptions check: `K=x` in Example 6.2 changes sign | No extension of positive-kernel theory is inferred |
| 8 / VQ-01 | Verified quadrature-estimate inconsistency for Eq. (6); constant-input error Θ(τ^(1−β)), sharp smooth-input upper order 1−β | Does not determine the global PDE solution rate or disprove the full convergence theorem |

These are analytical statuses from the supplied notes, checked at the relevant local-paper formula level. No result is described as Lean-certified or freshly reproduced numerically. Observations 3–7 retain their supplied provisional/check/caveat status.

## D. Validation results

The corrected static audit passed all 18 checks: unchanged-baseline integrity, minimality of the two existing-file edits, input hashes, Python syntax parsing without evaluation, local links, and TeX delimiter/environment/reference/section/equation structure. The initial report is retained: a checker limitation around doubled backslashes and a link to the not-yet-created report were resolved without changing a mathematical formula or numerical expectation. All 83 original files remain present; 81 retain their original hashes, and the other two are exactly the documented insertions.

Relevant source-paper pages and source-note mathematical pages were rendered with installed local Poppler/Cairo libraries and inspected; the [validation record](results/VALIDATION.md) lists them. No independent article was downloaded or consulted. No numerical data were regenerated.

LaTeX compilation was unavailable because no TeX engine was installed. Julia tests were unavailable because Julia was absent. Lean/mathlib were absent and the mentioned draft was missing, so there is no formal machine-check claim. Python numerical checks were **not run**: the applied local skill requires verified aggregate resource/containment/cleanup controls, and no qualifying backend was available. The numerical preflight stopped before any payload launch. The supplied `3.77e-15`/432-case output and PDF tables remain clearly labeled historical evidence. Full commands and fixed expectations are in the [test plan](results/TEST_PLAN.md).

## E. Outstanding issues

- Original LaTeX and original VQ-01/CF-02 Python companions, the CF-02 Julia counterpart, and the Lean draft were not supplied or found. The historical CF-02 direct-integration test lacks retained precision, tolerances, and raw output; it cannot be reconstructed as an executed result from the notes alone.
- Ramezani–Mokhtari–Haase Section 3.2 / Theorems 3.4–3.6 are preserved as source-reported locators requiring primary-source verification. Their memory-free model cannot establish the present theorem.
- The published scaled residual conventions and missing λ in an early shorthand need reconciliation. The notes' qualification is retained rather than resolved by assumption.
- The paper's true implemented L1-2 recurrence and any unstated singular quadrature are unknown. The repository already chooses interpolation for L1-2 while retaining the printed Volterra quadrature; this distinction is explicit.
- New LaTeX rendering, numerical runs, and any Lean compilation remain outstanding. Historical table reproduction and H¹/2D conventions were not repaired. The full PDE stability/convergence questions and provisional observations remain open.
- `research/` remains intentionally excluded by the existing ignore rules. All deliverables are present locally for manual review; no upload/version-control change was made.

## F. Recommended next research steps

First establish a stability estimate for the corrected, step-dependent L1-2 recurrence with **both fractional and Volterra signed histories**, using the actual newest coefficient and explicit parameter/timestep assumptions. The L1 signed-history inference also needs its own valid estimate. Only then derive how the proven Volterra discrepancy propagates into the PDE solution, distinguishing unscaled consistency, α₀-scaled residual, startup accumulation, and global error.

Recover the missing companion sources and verify the cited independent analysis. Complete the provisional startup, variable-coefficient quadrature, norm, normalization, and kernel-assumption audits. Run the documented checks and compile the transcription in a configured local environment, preserving every failure and its exact inputs. Investigating product integration or repairing the theorems is a subsequent research task, not part of this integration.
