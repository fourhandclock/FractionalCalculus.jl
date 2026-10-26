# Legendre spectral method

This is a fork of FractionalCalculus.jl, tailored around the method developed in , *H1 stability and convergence analysis of the L1/L1-2 Legendre spectral method for non-local weakly singular integro-PDEs*, Calcolo 62:42 (2025), [DOI](https://doi.org/10.1007/s10092-025-00671-y). The supplied PDF is [here](YS_SS_PD_NM_25_Calcolo.pdf).

However I plan to extend this framework for future studies.

The natural objective is to understand the method, implement its defined operators, and compare the computations with the published results. New methods and improvements are deferred until this baseline is understood. **However, implementing the equations does not establish the fact that the published tables or stability proof have been reproduced.** See the generated comparison report for the numerical status.
<!-- keep everything above as it is -->

## Study layout

The numerical components stay in `src/`; each paper keeps its cases, tests, runners, and results in its own directory under `studies/`.

```text
src/                         Numerical operators and solver
studies/
  legendre/
    cases.jl                 First paper's manufactured problems
    test/                    First paper's validation suite
    run.jl                   Published-table comparison
    export_figures.jl        Figure data generation
    plot_results.py          Figure rendering
    reference_tables.csv     Published error values and parameters
    results/                 Computed comparisons and rates
    figures/                 Plots, nodal data, and parameters
test/runtests.jl            Runs each study's test entry point
```

The README is the public study guide. Detailed working notes remain local in the excluded `research/` directory; generated prose reports are also excluded from uploads. The numerical CSVs and figures remain with their study.

## Setup

Use Julia 1.10 or later. The current environment was exercised with Julia 1.12.6 and uses `LinearAlgebra` and `SpecialFunctions`. From this library directory:

```powershell
julia --project=. -e 'using Pkg; Pkg.instantiate()'
```

The manifest was recorded with Julia 1.12.6; an older Julia version may need to resolve a compatible environment. Add `--compiled-modules=no` if the execution environment blocks precompilation. Figure rendering additionally requires Python with NumPy and Matplotlib.

## L1/L1-2 Legendre spectral method

All cases and outputs for the Calcolo paper above are grouped in [`studies/legendre/`](studies/legendre/). `paper_example` remains this paper's case constructor; its existing call signature is unchanged.

### Test cases and results

| Case | Problem | Published tables |
| --- | --- | --- |
| Example 6.1 | 1D problem with a smooth memory kernel and varying spatial regularity | 1-5 |
| Example 6.2 | 1D weakly singular memory; separate zero-initial, no-memory variant | 6-14 |
| Example 6.3 | 1D initial time layer on uniform and graded meshes | 15-18 |
| Example 6.4 | 2D tensor-product spatial discretization | 19-21 |

The existing baseline contains **645 passing checks**, **231 table configurations**, and **194/546 published error values matching within their printed rounding**. Tables 15 and 16 match completely. Differences remain in L1-2, the reported H1 errors, and the 2D results; full numerical reproduction is not yet established.

| Data | Location |
| --- | --- |
| Published parameters and error values | [`reference_tables.csv`](studies/legendre/reference_tables.csv) |
| Computed errors, targets, rounding checks, and solve residuals | [`results/comparison.csv`](studies/legendre/results/comparison.csv) |
| Computed and reference convergence rates | [`results/rates.csv`](studies/legendre/results/rates.csv) |
| Validation checks | [`test/`](studies/legendre/test/) |

The comparison retains the paper's extra spatial-node normalization in L2 and H1. H1 uses the analytic spatial gradient minus the derivative of the numerical interpolant; the 2D denominator uses the product of the spatial node counts. Time errors are averaged over sampled levels, including on graded grids. `space_time_L2` is also saved without the extra spatial-node divisor. A match requires agreement within half of the last printed digit, rather than a fitted tolerance. CPU timings are local diagnostics and are not compared with the authors' hardware timings.

### Run this study

```powershell
# Run every study's validation suite (currently the Legendre study).
julia --project=. test/runtests.jl

# Run only the first paper's checks.
julia --project=. studies/legendre/test/runtests.jl

# Compare all 21 published tables.
julia --project=. studies/legendre/run.jl

# Compare selected tables without changing the saved baseline.
julia --project=. studies/legendre/run.jl --tables=12,13 --output-dir=research/legendre/check-results

# Generate the first paper's figure data and render its plots.
julia --project=. studies/legendre/export_figures.jl
python studies/legendre/plot_results.py
```

Input and default output paths are anchored to the study directory, so commands can also be launched from another working directory with absolute script and `--project` paths. `run.jl` and `export_figures.jl` accept `--output-dir=<path>` to write a separate run; an explicit relative output directory is resolved from the working directory. Each study supplies `test/runtests.jl`, which the root test runner discovers automatically.

```julia
using FractionalCalculus

# Isolate time stepping and spatial assembly: Tables 12-14.
p = paper_example(2; alpha=0.4, no_memory_variant=true)
s = solve_tfide(p; M=9, N=16, scheme=:L12)
error_norms(s)

# Weakly singular memory: Example 6.2.
p = paper_example(2; alpha=0.5, beta=0.2)
s = solve_tfide(p; M=9, N=16, scheme=:L1)

# Tensor 2D space and graded time mesh: Example 6.4.
p = paper_example(4; alpha=0.6, beta=0.3)
s = solve_tfide(p; M=(9,9), N=16, scheme=:L1, grading=(2-0.6)/0.6)
```

`M` is polynomial degree (M+1 nodes), `N` is the number of time intervals, and `:L12` denotes L1-2. The current solver supports homogeneous Dirichlet conditions on (-1,1) or (-1,1)^2. It is a dense reference implementation with full memory history and direct linear solves.

### Implementation map

| Paper component | Implementation |
|---|---|
| Caputo L1, Eqs. 4-5 | `src/TimeDiscretization.jl`: `caputo_weights`, `caputo_derivative` |
| L1-2 interpolation definition, Eqs. 20-24 | Same file, `scheme=:L12`; L1 first step |
| Volterra quadrature, Eq. 6 | Same file, `memory_weights`; literal old-interval trapezoids |
| Legendre-Gauss-Lobatto nodal weak form, Sections 4-5 | `src/Legendre.jl`: diagonal quadrature mass, D'WD stiffness |
| Tensor 2D extension, Example 6.4 | `legendre_space((Mx,My))` |
| Linear systems, Eq. 59 | `src/Solver.jl`: unscaled PDE assembly |
| Four exact solutions and sources | `studies/legendre/cases.jl`: `paper_example` |
| Discrete errors, p. 28 | `error_norms`; analytic spatial gradients |
| Numerical Tables 1-21 | `studies/legendre/reference_tables.csv` and `studies/legendre/run.jl` |

The code follows the interpolation definition when the paper's later L1-2 recurrence contradicts it. The unscaled PDE assembly retains the required forcing scale. Graded-grid weights are explicitly reconstructed because the article supplies only the graded mesh, rather than their full formulas. The singular Volterra rule is kept as printed; the constant-input check demonstrates a disagreement with its claimed order. These choices remain part of the first paper's baseline.

### Figures,raw data and what they mean

The plots are local numerical reconstructions, with CSVs for their parameters and nodal values. PNG and SVG versions are saved in [`figures/`](studies/legendre/figures/); they do not assert identity with the published graphics.

| Figure | Output |
| --- | --- |
| 1 | [Example 6.1, L1, alpha=.55, nu=2.5](studies/legendre/figures/figure1.png) |
| 2 | [Example 6.1, L1-2, alpha=.7, nu=2.9](studies/legendre/figures/figure2.png) |
| 3 | [Temporal convergence, alpha=.5, nu=2.3, M=9](studies/legendre/figures/figure3.png) |
| 4 | [Example 6.2, singular memory](studies/legendre/figures/figure4.png) |
| 5 | [Example 6.3, initial layer and graded meshes](studies/legendre/figures/figure5.png) |
| 6 | [Example 6.4, two spatial dimensions](studies/legendre/figures/figure6.png) |
| Diagnostic | [Constant-input memory quadrature](studies/legendre/figures/memory_diagnostic.png) |
| Diagnostic | [Published and computed convergence for Tables 1-2](studies/legendre/figures/table_convergence_diagnostic.png) |

Figure 3 uses N=4,8,16 and scaled N^-1.5 slope guides matching the printed labels; the guides are not error bounds. The memory diagnostic retains the literal quadrature and measures a rate approaching .5 for beta=.5, rather than the claimed 1.5.

## Future plans

- Resolve the first paper's outstanding L1-2, H1, and 2D discrepancies while preserving the current baseline for comparison.
- I want to add another paper namely [fractional
diffusion equations on metric graphs](Kaust_Fractionaldiffusionequationsonmetricgraphs.pdf) as a separate study with its own cases, tests, reference data, and results using the now forked repo. Its implementation is planned for a later stage.
- Extend the numerical library as new studies require it, keeping reusable operators in `src/` and paper-specific choices in their study directories.
- maybe have improved experiments after the corresponding theory and more reproduction checks, and then compare accuracy, convergence, and computational cost etc etc. within each study.