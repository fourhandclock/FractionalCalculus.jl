# Sabawi et al.: Legendre spectral reproduction study

This study reproduces and independently audits Sabawi et al. (2025), *H¹ stability and convergence analysis of the L1/L1-2 Legendre spectral method for non-local weakly singular integro-PDEs*. Read the [source paper](../../YS_SS_PD_NM_25_Calcolo.pdf) alongside the [mathematical verification dashboard](../../research/legendre/verification/README.md).

The problems combine diffusion with a fractional Caputo time derivative and a Volterra integral over the preceding solution history. The examples include smooth and weakly singular memory kernels. The implementation supports homogeneous Dirichlet conditions on `(-1,1)` and `(-1,1)²`, using L1/L1-2 time discretization and Legendre–Gauss–Lobatto (GLL) spatial quadrature. Examples 6.1–6.4 cover spatial regularity, singular memory, an initial time layer, and a tensor-product 2D problem.

## Post-reproduction analysis and research methods

Start with [AUD-02 revision 01](../../research/legendre/aud02/revision-01/README.md) for the closed GR-01–07 programme: six revised manuscripts, the separate [Alikhanov–PI-L/PI-Q module](gr07/revision-01/README.md), 54 finite Lean certificates and reproducible evidence. These shifted methods are research alternatives; they do not replace the production reproduction or establish full agreement with Sabawi’s tables. The AUD-01 summary below retains its original scope.

## Reproduction and verification status

The current AUD-01 checkpoint has verdict **ACCEPT WITH LIMITATIONS**, an accepted 37-page manuscript, and **42 named Lean certificates / 41 nonduplicate identity groups**. The [clean-tree validation report](../../research/legendre/verification/results/checkpoint-aud01/VALIDATION.md) records actual Julia, Python, Lean and LaTeX executions. The earlier [ST-04 record](../../research/legendre/verification/results/VALIDATION.md) remains historical evidence.

Full numerical reproduction remains open: the saved [comparison](results/comparison.csv) covers **231 configurations** across Tables 1–21, with **194/546 reported error values** agreeing within printed rounding. Tables 15 and 16 match completely; discrepancies remain in L1-2, H1 errors, and 2D results. Test success and agreement with the published tables are separate assessments.

The mathematical audit distinguishes **confirmed coefficient and Volterra-order discrepancies** (Observations 2 and 8), an **established contraction-proof gap** (ST-03), and a **finite-grid numerical counterexample candidate** (ST-04). Later SP-01/SP-02 supply conditional replacement estimates; TM-01/AUD-01 distinguish smooth forced from initially singular homogeneous sharpness. ST-05 analytically contradicts eventual contractivity for fixed admissible data, while the isolated-mesh reading of Theorem 3.1 and the temporal regularity comparison with Theorem 3.2 remain qualified.

## Find the implementation and results

| Component | Start here |
| --- | --- |
| Caputo and Volterra weights | [TimeDiscretization.jl](../../src/TimeDiscretization.jl) |
| GLL operators and 1D/2D spaces | [Legendre.jl](../../src/Legendre.jl) |
| Galerkin solve and error definitions | [Solver.jl](../../src/Solver.jl) |
| Problems with known exact solutions | [cases.jl](cases.jl), via `paper_example` |
| Published targets and saved comparisons | [reference_tables.csv](reference_tables.csv), [comparison.csv](results/comparison.csv), [rates.csv](results/rates.csv) |
| Library tests and mathematical regressions | [study test runner](test/runtests.jl), [proof_audit.jl](test/proof_audit.jl) |
| Figures and their parameters/data | [figures/](figures/), [export_figures.jl](export_figures.jl), [plot_results.py](plot_results.py) |

L1-2 follows the interpolation definition where the printed recurrence disagrees; its first step is L1. Singular memory retains the paper's printed quadrature. The numerical error definitions and graded-grid reconstruction choices are documented in the [implementation audit](../../research/legendre/verification/ST04_PROVENANCE.md#implementation-inspected-before-release). Product integration is separate from this production reproduction: it appears in the independent ST-04 control and the explicitly separate GR-07 research methods.

## Reproduce or investigate

Run these commands from the repository root after [Julia setup](../../README.md#setup):

```bash
# Run this study's tests, including proof_audit.jl.
julia --project=. studies/legendre/test/runtests.jl

# Compare selected published tables in a separate output directory.
julia --project=. studies/legendre/run.jl --tables=12,13 --output-dir=research/legendre/check-results
```

The [table runner](run.jl) accepts `--tables` and `--output-dir`; omitting `--tables` selects all tables. Its default output directory contains the saved baseline, so use a separate directory for new comparisons. The [reproduction guide](../../research/legendre/verification/REPRODUCE.md) pins toolchains and covers Python, Lean, LaTeX, and execution limits. The root [test runner](../../test/runtests.jl) discovers every available study; the command above runs only Legendre.

For mathematical work, start with the [full independent manuscript](../../research/legendre/verification/reviews/AUD-01/revision-01/mathematical-verification-aud01-r1.tex), [observation dossier](../../research/legendre/verification/observations/README.md), and [Lean certificate catalogue](../../research/legendre/verification/lean/README.md). The [dashboard's open questions](../../research/legendre/verification/README.md#outstanding-mathematical-questions) identify the next research steps. Historical command logs support the dated validation report. Its checkpoint is `80788d324e2c607119ac6585cf832994bcf1e823`, a message-only replacement of `84cb923` with an identical committed file tree.

[Repository overview](../../README.md#research-framework) · [Research workflow and documentation plan](../../docs/RESEARCH_WORKFLOW.md)
