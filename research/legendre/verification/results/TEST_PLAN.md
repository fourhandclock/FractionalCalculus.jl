> Historical pre-execution ST-03 test plan. The current execution results and replay instructions are in [VALIDATION.md](VALIDATION.md) and [REPRODUCE.md](../REPRODUCE.md). Its previous execution restrictions are historical.

# Reproducibility plan and fixed expectations

This plan records theoretical predictions and historical evidence before any fresh numerical execution. None of the commands below was run during integration. A source file passing a static syntax check is not an executed regression, and supplied stdout is not a new result. See [VALIDATION.md](VALIDATION.md) for actual status.

## Formula identities and roles

`scripts/verify_l12_stability.py` is a byte-identical copy of the supplied ST-03 script. It implements the corrected interpolation-defined coefficients, with `k=current step−1`, unit final time, `τ=1/N`, `α₀=Γ(2−α)τ^α`, `μ=σα₀`, and the **literal printed Volterra rule**. Its `collected` and `increments` modes represent the same corrected scheme. Its `false_one` diffusion diagnostic is the unrescaled `d₀=1` alternative and remains separate.

The new `scripts/check_counterexamples.py` preserves separate named implementations of the interpolation two-sum, corrected collected sum, and analytical defining-panel moments. `published_eq23_final_sum_k1` implements only the unambiguous `k=1` printed index reversal; it deliberately refuses to guess the omitted middle coefficient for later steps. `published_d0_one_diffusion_step` and `corrected_diffusion_step` are different reduced recurrences. The two Volterra expressions are an implementation of Eq. (6) and its exact error identity, **not** two different quadrature methods. Product integration is documented in TeX only and has no implementation.

## Supplied ST-03 diagnostic

| Check | Inputs and expectation | Acceptance / evidence scope |
| --- | --- | --- |
| Negative increment and signed history | α=3/4, k=1: d₀=1.3, d₁=2^(1/4)−1.3<0; absolute history budget >d₀ | Supplied script asserts signs; the exact proof is Proposition 5.2, not its floating-point “Exact” print heading |
| Assigned-state proof gap | `(U⁰,U¹)=(-1,+1)` | Norm-bounds inference only; not a recurrence trajectory |
| Distinct reduced diffusion recurrences | α=.75, μ=.3, λ=0; u¹=1/1.3; corrected u²≈.6090202570 and unrescaled d₀=1 u²≈.5720486003 | Supplied assertion requires difference >1e-3; λ=0 diagnostic is outside the positive-memory setting |
| Representation agreement | α∈{.25,.5,.75,.9}, β∈{.2,.5,.8}, σ∈{.25,1,10}, λ∈{0,.1,1,10}, N∈{16,32,64}; 4×3×3×4×3=432 cases | Maximum state difference <2e-11, as in the unchanged source. This is the test criterion, not the supplied observed 3.77e-15 |
| Weighted amplification | max over n≥1 of `sqrt(1+μ)*|uⁿ|`, among finite trajectories | Diagnostic only, with no pass/fail contractivity threshold. Supplied output reports 1.08601376 at (.25,.8,10,10,16); no fine-grid theorem counterexample |

The supplied file uses binary floating point and `math.gamma`; no random seed is needed. It filters finite trajectories when computing its maximum rather than asserting that all cases are finite. Preserve that behavior. Historical stdout has no Python/platform identity or exact invocation attached; do not treat final printed digits as a portable exact-output acceptance test.

## Newly added Python regressions

All inputs are deterministic; standard library only (`math`, `unittest`, `decimal`, `fractions`), with unchanged ST-03 functions imported locally. The new checker writes only its test report to stdout/stderr.

| Check | Domain / expected outcome | Fixed tolerance |
| --- | --- | --- |
| Leading identity and sign proof | Exact rational α=1/4,1/2,3/4; `b₀*=α/[2(2−α)]`; `(13/10)^4>2` | Exact `Fraction` equality/inequality |
| Correct coefficient collection vs interpolation moments | α=.25,.5,.75; k=0,1,2,4; polynomial nodal values j^p, p=0,1,2,3; dimensionless unit-step brackets | Absolute 2e-11, conservative for finite small-degree polynomial sums and cancellation |
| Startup/newest and telescope | Same α,k; d₀=1 at k=0, otherwise 1+α/[2(2−α)]; Σh=d₀ | Absolute 2e-14 |
| Printed index reversal | α=.75, k=1, values (0,0,1); interpolation 1.3, printed last line 2^(1/4)−1.3<0 | Absolute 2e-14 |
| Signed history | α=.75,k=1 and α=.5,k=2 | Strict sign and budget inequalities; no PDE stability assertion |
| Reduced diffusion alternatives | α=.75, μ=.3, λ=0; values as supplied above | Absolute 5e-10 against printed historical values; difference >1e-3 |
| Two named scalar reductions | (.75,.5,1,0,16) and (.25,.8,10,10,16), ordered as α,β,σ,λ,N | All values finite on these named cases; state difference <2e-11; no amplification upper bound imposed |
| Volterra near-panel lower bound and exact error sum | T=K=u=1, β=.2,.5,.8, N=16,256,512,1024; c_β>0; Q−I≥c_βτ^(1−β) | Absolute 2e-12 allowance for cancellation in ordinary double precision; no proof inferred from tolerance checks |
| Historical VQ-01 table | β=.2,.5,.8, N=256,512,1024; compare every error to notes §4.4 | Half of the last displayed decimal place plus absolute 2e-12 roundoff allowance |
| Volterra rate | p₅₁₂=log₂(E₅₁₂/E₁₀₂₄), tending to 1−β | Absolute .0015 from 1−β at the stated resolutions; this does not test a claimed 2−β order |
| Existing β=.5 example | N=16, absolute error .00974865205936 | Absolute 5e-14, same criterion as the existing Julia regression |
| Variable-coefficient LGL | M=3, c=1/2; integral 16c/105, Lobatto sum 16c/75, difference 32c/525 | Exact rational arithmetic, exploiting symmetric nodes with squared interior coordinate 1/5 |

The new polynomial checks use **analytical panel moments**, not the missing original CF-02 numerical-integration oracle, and do not claim its unspecified high precision or integration tolerance. They cannot reconstruct that historical experiment's environment.

## Julia integration

The existing [Legendre suite](../../../../studies/legendre/test/runtests.jl) now includes `proof_audit.jl`. Existing files already test L1/L1-2 invariants, uniform formulas, startup moments, singular-memory order, manufactured-solution convergence, and error normalization. The new test file adds α=3/4 coefficient/history and reversed-index regressions, α=1/2,k=2 negative history, the exact rational fourth-power inequality, and the actual library's M=3,c=.5 LGL mass calculation. Coefficient comparisons use absolute 2e-14; spatial comparisons use 3e-14. These tolerances target the stated tiny Float64 problems, not a full parameter-domain theorem.

No existing test expectations were changed. Historical “645 passing Legendre checks” predates this added file and is not an expected new test count. The root suite also runs the separate graph study; neither suite could run without Julia. The metric-graph study is outside the numerical scope of this integration.

## Replay without overwriting evidence

From the project root, in a locally configured execution environment:

```bash
python3 -B research/legendre/verification/scripts/verify_l12_stability.py
python3 -B research/legendre/verification/scripts/check_counterexamples.py
julia --startup-file=no --project=. studies/legendre/test/runtests.jl
```

Use a new run directory when retaining stdout, stderr, exit status, environment versions, command, and source/input hashes. Keep failure outputs and failed tolerances; do not replace historical stdout, expected values, comparison CSVs, or figures. Do not run the table/figure generators with their default output directories to validate this documentation change. No numerical data need regeneration.

The applied local research skill requires verified process containment, finite deadlines, aggregate memory/CPU/task limits, bounded output/storage, source/evidence protection, network restrictions, and descendant cleanup before numerical execution. A reasonable initial plan for these small Python checks is at most 60 seconds, 256 MiB aggregate memory, one CPU, 30 aggregate CPU seconds, eight tasks, 64 KiB per output stream, and 4 MiB scratch; **none of those limits is claimed enforced here**. Julia needs a separately verified budget including loading and compiler workers. The historical preflight record (retained locally and excluded from this checkpoint) records that no qualified execution backend was available. The script launch was therefore withheld before any numerical payload started; no experimental cleanup was needed. No runner, capability trial, toolchain installation, or new scheme was introduced to work around that boundary.

## Lean and LaTeX

No Lean draft or mathlib project was supplied or found; `lean` and `lake` are unavailable. Consequently no Lean compilation was attempted, and no statement is labeled machine-checked. Recovering the mentioned draft is a missing-source task, not a reason to invent one.

The LaTeX source requires ordinary `amsart`, AMS math/theorem packages, `booktabs`, `geometry`, and `hyperref`. No TeX engine is available. The [verification README](../README.md) gives a two-pass `pdflatex` command for a separate build directory. Static delimiter/reference/numbering checks and source-page comparison do not substitute for compilation or rendered-output review.
