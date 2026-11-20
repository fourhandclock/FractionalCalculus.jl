> Historical ST-03 reconstruction, retained for its source locators. The current original ST-04 source and checkpoint provenance are recorded in [ST04_PROVENANCE.md](ST04_PROVENANCE.md). Earlier statements about missing original LaTeX and unexecuted checks refer to the earlier session.

# Provenance and reconstruction

Reconnaissance and integration date: 2026-11-20. No version-control commands, remote queries, dependency installations, or changes outside this workspace were performed. Temporary extraction and page-rendering scratch files were written under `/tmp`.

## Repository state reconstructed before editing

The root README is the current study guide. `src/TimeDiscretization.jl` implements uniform and graded L1, the linear-first/quadratic-later L1-2 interpolants, smooth-kernel trapezoids, and the printed singular Volterra quadrature. Uniform weights use 256-bit intermediate `BigFloat` evaluations before conversion to `Float64`; nonuniform weights reconstruct kernel moments. `src/Legendre.jl` provides LGL nodes, diagonal quadrature mass, `D'WD` stiffness, and one- and two-dimensional spaces. `src/Solver.jl` assembles unscaled PDE systems with direct solves and calculates the paper-normalized errors plus `space_time_L2`.

`studies/legendre/` contains the four manufactured problems and no-memory variant, study tests, table runner, reference-table transcription, figure exporter, Python plotting, comparison/rate CSVs, and figure data. The root test entry point discovers study suites. The metric-graph implementation and study are a separate later project and were preserved.

`Project.toml` specifies Julia ≥1.10, `LinearAlgebra`, `SparseArrays`, `SpecialFunctions` 2, and `BaryRational` 1. `Manifest.toml` records Julia 1.12.6. Plotting uses Python, NumPy, and Matplotlib. The supplied ST-03 diagnostic needs only Python's standard library. No Lean files, `lean-toolchain`, Lake project, original verification `.tex`, or CF-02/VQ-01 companions were found, including in ignored local research files.

`research/THEORY.md`, `STATUS.md`, `LIBRARY_AUDIT.md`, `research/legendre/REPRODUCTION.md`, and `FIGURES.md` already document reconstruction choices and historical work. Before integration this verification directory contained only `page39.png` and `page42.png`, retained source-paper images used for table transcription. Existing reproduction reports and root README record 645 Legendre checks and 194/546 published-cell matches; the root README also records 270 later graph checks. These are historical claims, not tests rerun here. Older status/audit files describe earlier dependencies and architecture and remain preserved rather than rewritten.

The source paper is `YS_SS_PD_NM_25_Calcolo.pdf` at the project root (46 PDF pages). References and equation locators already existed in the README and theory guide. Numerical evidence stays under each study's `results/` and `figures/`. The chosen extension of `research/legendre/verification/` follows that separation without reorganizing either study.

## Supplied inputs

The [input manifest](sources/inputs.json) records exact byte counts and SHA-256 hashes, including the pre-existing source paper. These three supplied files were copied without alteration:

| Supplied basename | Retained location | Evidence meaning |
| --- | --- | --- |
| `legendre_spectral_verification_notes_st03.pdf` | [PDF](sources/legendre_spectral_verification_notes_st03.pdf) | Primary audit source: all 11 pages read |
| `verify_l12_stability.py` | [Script](scripts/verify_l12_stability.py) | Supplied ST-03 implementation, byte-identical |
| `st03_verification_results.txt` | [Output](sources/st03_verification_results.txt) | Supplied historical stdout; execution date, command, and environment were not supplied |

The PDF identifies Hardik Bisht as author and November 2026 as its date. Its metadata reports LaTeX/pdfTeX production. This establishes that the input is a compiled PDF, not that its original source was available. [mathematical-verification.tex](sources/mathematical-verification-st03-transcription.tex) is a new manual transcription, not recovered author source. Only integration/evidence notices and navigation have been added; these are labeled. Original sections 1–7, observations 1–8, propositions 4.1/4.2/5.1/5.2/6.1, equation numbering, tables, and mathematical qualifications are retained.

## Full PDF coverage

| Supplied PDF page | Material retained in the TeX transcription |
| ---: | --- |
| 1 | Title, author/date, §1, model (1.1)–(1.2), purpose and status distinctions; §2 and start of observation 1 |
| 2 | Signed-sum inequality; observations 2–5 with coefficient, startup integral, LGL example, and weighted norm |
| 3 | Observations 6–7; §3 observation 8; §4.1 and integral (4.1) |
| 4 | Rule (4.2), error sign, Proposition 4.1 and full lower-bound proof; positive series (4.4), asymptotic (4.5) |
| 5 | Proposition 4.2 and upper-bound proof, (4.6); §4.4 complete historical table; IBVP embedding and unscaled residual |
| 6 | Scaled residual qualification, established/not-established distinction; product-integration candidate and bound; §5.1, (5.1)–(5.2), correction moment |
| 7 | Proposition 5.1 and proof, (5.3)–(5.4); Proposition 5.2 and proof, (5.5)–(5.6); independent index reversal and omitted indices |
| 8 | §5.4 telescoping (5.7), current-state coefficient and rescaling qualification; §5.5 historical experiment, full coefficient table and formalization status; §6.1 and (6.1) |
| 9 | Zero-forcing/real-valued reduction; history (6.2), state recurrence (6.3), telescoping (6.4), full memory recurrence (6.5); Proposition 6.1, (6.6), full proof |
| 10 | Historical numerical coefficient budget; α=1/2, k=2 example; signed-sum inequality; full independent literature discussion; two-step eigenmode (6.7), contractive bound and `d0=1` diagnostic |
| 11 | §6.6 scalar equation, reported 432 cases, coarse amplification and refinement qualification; ST-03 verdict; §7 protocol and proposed next task |

The [secondary extraction](sources/verification-notes-extracted.txt) was made using installed Poppler libraries. It is a reading aid with degraded math ordering, not authoritative equation source. An independent `pypdf` extraction was used during reading; the published paper triggered missing-`fontTools` encoding warnings in that extractor. Poppler text and rendered pages were used to resolve notation. No extractor output was treated as original LaTeX. Rendered page inspections and remaining limits are recorded in [validation](results/VALIDATION.md).

## Checked source locators

Page numbers below are one-based PDF pages in the local 46-page paper, not equation numbers in our notes.

| Audit item | Published source checked | Finding / transcription constraint |
| --- | --- | --- |
| Positive separable kernel | Model (1), pp.4–5 | `0<α,β<1`; smooth strictly positive spatial/time factor; theory concerns homogeneous zero-forcing evolution for stability |
| Weighted norm | Eq. (2), p.5; α₀ definition p.8 | Preserve timestep dependence; displayed variable typo in source does not change the norm interpreted in the notes |
| L1 and Volterra | Eqs. (4)–(8), pp.6–7 | Old panels use trapezoids of the whole singular integrand; error `Φ_T=I−Q`; Eq. (8)'s combined simplification assumes β≤α; Remark 1 discusses the other ordering |
| L1-2 interpolation | Eqs. (20)–(24), pp.10–11 | Two-sum construction, reversed last-line indexing, and missing `j=1` in both printed ranges are present |
| L1-2 truncation | Eq. (26), p.12 | Separate startup and post-startup claims; retain the early-index distinction |
| L1-2 recurrence | Eqs. (28)–(34), pp.13–14 | Eq. (29) asserts normalization/positivity; (30)–(31) substitute `d0=1`; startup (34) is separate |
| Residual scaling | Eq. (35), p.14; (7)–(8), p.7 | (35) includes α₀ and λ; the shorthand before (8) omits λ. General sign/normalization reconciliation remains open as the notes require |
| Stability | Theorem 3.1, pp.15–16, Eqs. (38)–(41) | Fine temporal mesh qualification; coefficient modulus `C_x` appears on p.16; L1-2 proof asserted by analogy to (29) |
| Later time analysis | Theorem 3.2, pp.16–20 | Depends on a valid recurrence, stability reasoning, and the truncation estimates under audit |
| Variable-coefficient exactness | Theorem 4.1, pp.22–23, passage immediately before Eq. (55) | Equality asserted for `R_M ∈ P^0_{M−1}`; mass factor can raise the degree |
| Error metrics | Section 6, p.28 | Additional `(M+1)^{-1}` factor present; H¹ metric here is distinct from the α₀-weighted theoretical norm |
| Sign-changing example | Example 6.2, p.33 | `K=x`, domain `(-1,1)`, λ=1; source positivity is not satisfied everywhere |
| L1-2 reference already cited locally | Reference [52], p.45 | Gao, Sun, Zhang (2014), JCP 259, 33–50; no new literature search |

Theorems in the independent Ramezani–Mokhtari–Haase article were **not** checked at primary-source level. Its Section 3.2 / Theorems 3.4–3.6 locators are preserved as reported in the PDF and marked as requiring source verification in the [literature record](literature/README.md). No missing theorem, equation, or hypothesis has been guessed.

## Missing companion sources and evidence boundaries

The PDF §4.4 refers to a companion VQ-01 Python checker. Section 5.5 refers to a CF-02 Python checker, a standard-library Julia counterpart, and a mathlib Lean draft. None was supplied alongside the three named inputs or found in the workspace. The §5.5 direct-integral experiment has no retained tolerances, precision configuration, raw output, or original source here. Its report remains historical and cannot be upgraded to independently reproduced evidence.

The supplied ST-03 script's structural print heading says “Exact structural checks,” but its computations use ordinary Python floating point. The exact sign argument is the rational fourth-power comparison in Proposition 5.2. The script's assertion tolerance for recurrence agreement is `2e-11`, while `3.77e-15` is the supplied output's reported observed maximum. The script reports only finite trajectories when choosing its largest amplification; it does not assert that every trajectory is finite. The new regression checker includes finite-value assertions on its explicitly listed reduced cases, without altering the supplied file.

The PDF reports that refinement reduces the cited coarse amplification below one; the supplied output reports only the largest value across the grid. No per-refinement output was supplied, so the refinement statement remains a source-reported observation. Likewise `4e-15` in the PDF is a rounded historical observation, not a universal test tolerance.

New regression sources are identified as new integration work and are not substitutes claimed to be original companions. No Lean draft has been invented. No formal machine-check claim is made.
