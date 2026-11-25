# GR-07: Alikhanov product integration in Julia

GR-07 implements and tests the proposed GR-01–06 discretizations in a separate **1D research module**, using audited AUD-01 commit `bf43fd0e78bcbcaae94d4c95fd9e43fd562ba477` as the baseline. Production algorithms, dispatch, dependency pins and previous reproduction data are unchanged. The analytical manuscripts remain proposals for AUD-02; these numerical checks are not a complete theorem audit or a formal proof.

Read [VALIDATION.md](VALIDATION.md) for actual results and limitations, then [GR07.jl](GR07.jl), [tests](test/runtests.jl), and the [supplied handoff](reference/GR07_JULIA_HANDOFF.md). The original package, including its invalid initial comparison, is preserved under [reference/](reference/README.md).

## Mathematical problem and conventions

The forced Dirichlet problem on $(-1,1)$ is

$$
{}^CD_t^\alpha u-u_{xx}+\lambda K(x,t)\int_0^t(t-s)^{-\beta}u(x,s)\,ds=f(x,t).
$$

Let $r=1-\beta$, $\sigma=1-\alpha/2$, and $t_*^n=t_{n-1}+\sigma\tau_n$. The new methods use

$$
(\mathcal D_\tau^\alpha U)^n=\sum_{k=1}^n A_{nk}(U^k-U^{k-1}),
\qquad Q_X^n[U]=\sum_{k=0}^nW_{n,k+1}U^k\approx I^rU(t_*^n).
$$

Here **A contains increment coefficients**, unlike production `caputo_weights`, which returns state coefficients. **W is normalized by $1/\Gamma(r)$**; the equation multiplies it by $\lambda\Gamma(r)$ exactly once. The production memory routine is unnormalized. The endpoint controls retain their actual production state matrix, and tests compare their evolution with the actual production solver under matching initial values.

Alikhanov differentiates forward quadratics on completed panels and a full-panel linear interpolant integrated only to the shifted point on the final panel. PI-L integrates linear interpolation at that same shifted point. PI-Q uses forward quadratics on completed panels, a backward quadratic on the final partial panel, and linear startup at $n=1$. On nonuniform meshes the stencils use the actual adjacent step ratios. The known final-panel ratio is set exactly to $\sigma$.

Spatial operators reuse actual library GLL mass and stiffness, with $L=M_{\rm mass}^{-1}S$. The current-level matrix is

$$
A_{nn}I+\sigma L+\lambda\Gamma(r)W_{n,n+1}\operatorname{diag}K(t_*^n).
$$

All prior increments, shifted diffusion and memory columns—including the initial column—remain in the right-hand side. No commutation with spatially varying multiplication is assumed. Initial values are the **derivative Ritz projection**; interpolation is available only as an explicitly labeled control. Coefficient callbacks supply continuous representatives whose finite nodal values are sampled.

## Methods and experiment domain

| Variant | Derivative/evaluation | Memory |
| --- | --- | --- |
| `:L1_printed` | Actual-library endpoint L1 | Printed unnormalized rule, explicitly normalized in the research wrapper |
| `:L12_printed` | Actual-library interpolation-defined endpoint L1–2 | Printed rule |
| `:L12_PI_L` | Same endpoint L1–2 | Separate endpoint PI-L control |
| `:Alikhanov_PI_L` | Shifted Alikhanov increments | Shifted PI-L |
| `:Alikhanov_PI_Q` | Shifted Alikhanov increments | Shifted PI-Q with linear startup |

The 156 configurations reproduce the corrected Python reference: $T=1$, $\lambda=.4$, $K=(1+.3x)(1+.2\sin t)$, and $u=\cos(\pi x/2)t^2$ or $\cos(\pi x/2)(1+t^\alpha)$ with exact consistent forcing. Orders are $(.5,.25),(.75,.5),(.9,.8)$; $N=32,64,128,256$, $M=14$. The singular Alikhanov cases additionally use grading $2/\alpha$. Twelve spatial refinements use $M=3,5,7,9,12,16$, $N=256$, $(\alpha,\beta)=(.75,.5)$ on the graded singular problem.

Errors are continuous $L^2$ and ordinary $H^1$ norms from separate Gauss quadrature, maximized over **all time levels including zero**. They are not the original paper's extra-node-normalized sampled errors. Uniform and nondecreasing-step graded grids are supported; decreasing steps, duplicate/nonfinite nodes and invalid parameters are rejected. No 2D implementation or arbitrary-mesh theorem is claimed.

## Use and reproduce

The module is included explicitly rather than registered with production dispatch:

```julia
using LinearAlgebra
include("studies/legendre/gr07/GR07.jl")
using .GR07
p = manufactured(.75, .5, :singular)
t = mesh(128; grading=2/p.alpha)
op = time_operators(t, p.alpha, p.beta; variant=:Alikhanov_PI_L)
space = spatial_operators(14)
sol = advance(op, space; lambda=p.lambda, coefficient=p.coefficient,
    forcing=p.forcing, initial=p.initial, initial_gradient=p.initial_gradient)
continuous_errors(op, space, sol, p.exact, p.gradient)
```

From the repository root, [the reproduction controller](scripts/reproduce.py) runs independent oracles, the complete baseline/final regression suite, the new tests, all final supplied diagnostics, the Python/Julia case matrix and comparison. Each new run ID preserves earlier evidence:

```bash
python3 -B studies/legendre/gr07/scripts/reproduce.py --run-id new-replay
# Include controlled timings and figures only after all correctness gates pass:
python3 -B studies/legendre/gr07/scripts/reproduce.py --run-id new-performance --performance
```

Prerequisites are existing Julia **1.12.6 / SpecialFunctions 2.9.0** under the unchanged project/manifest; the isolated Python environment with NumPy **2.3.5**, SciPy **1.17.0**, mpmath **1.3.0**, SymPy **1.14.0**; and local bubblewrap. The recorded interpreter is CPython **3.13.16**, whereas the supplied reference reports 3.13.5. Runtime/depot paths expected by the controller are `.checkpoint-tools/julia-1.12.6`, `.checkpoint-tools/python-aud01` and `.checkpoint-tools/shared-julia-depot`. Provision missing tools/dependencies only after separate approval; the controller installs or downloads nothing. Figures are standalone SVGs generated from CSVs without additional packages.

The [execution policy](evidence/execution-policy.json) records the user's explicit bounded-process exception. Workloads run serially with one Julia/BLAS thread, finite wall/CPU deadlines, per-process memory/file limits, sampled descendant RSS and bounded logs. A namespace mounts host sources read-only, supplies fresh writable scratch/private temporary mounts, and checks PID-namespace cleanup. These controls **are not aggregate cgroup resource isolation**. Review that policy and the actual local namespace capabilities before replay on another machine.

## Evidence and performance interpretation

- [Julia matrix](results/julia_results.csv), [fresh Python reference](results/python_reference.csv), and [norm comparison](results/julia_reference_comparison.json).
- [Finite-window rates](results/convergence_windows.csv), [five-repeat timing summary](results/timing_summary.csv), [raw samples](results/timing_repeats.csv), and [separate warmups](results/warmups.csv).
- [Error versus N](figures/error_N_a0.75_smooth.svg), [graded/singular refinement](figures/error_N_a0.75_singular.svg), [error versus runtime](figures/error_runtime_smooth.svg), [spatial refinement](figures/spatial_refinement.svg), and [stored arrays versus N](figures/stored_arrays_N.svg). Other order pairs and singular runtime are also plotted.
- [Predeclared plan](evidence/PLAN.md), [correctness admissions](evidence/admission/candidate.json), [runtime identities](evidence/environment.json), [raw execution records](evidence/runs/), and [preserved input hashes](evidence/supplied-inputs.json).

Timings cover time-weight assembly, spatial assembly/projection preparation, stepping and their instrumented total. They exclude package loading, fixed manufactured-callback construction, residual/error postprocessing and file I/O. Actual callback evaluation and Ritz projection are included in stepping. Every measured solve has fresh arrays; explicit pre-sample GC is outside the timed region. Five repeats follow a specialization warmup, with rotated variant order. Runtime variability, allocated bytes, stored array bytes and sampled process RSS are reported separately.

The controls use the actual library's high-precision weight construction and retain both state and converted increment matrices for diagnostics; new weights use stabilized Float64 moments. Storage and timings describe these research implementations, not minimum possible storage or intrinsic scheme complexity. No cross-language or general production speedup is claimed. PI-Q's higher memory consistency need not improve the overall convergence order or the singular-case error.

The supplied `invalid_initial_results.csv` and its adapter/log are **INVALID scientific evidence** and are not used by any comparison or figure. A separate new high-precision-oracle attempt encountered an exact-zero relative-error issue; its source, failure and correction are retained. The analytical GR-01–06 results remain pending AUD-02, regardless of passing finite tests.
