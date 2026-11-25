# Alikhanov–product integration: audited revision 01

This is the separate GR-07 research implementation accompanying the revised GR-01–06 analysis. It approximates Caputo diffusion with weakly singular Volterra memory, using shifted Alikhanov differentiation and either linear or quadratic product integration (PI-L/PI-Q). Uniform and fixed-exponent graded meshes are supported. Production L1/L1-2 operators are unchanged.

The [closure guide](../../../../research/legendre/aud02/revision-01/README.md) connects the implementation, six revised manuscripts, analytical review, 54 finite Lean certificates and actual validation. The conditional mathematical verdict is **ACCEPT WITH LIMITATIONS**. Full PDE arguments remain analytical, and source-locator/novelty limitations remain explicit.

## Implementation and numerical contract

[GR07.jl](GR07.jl) retains increment coefficients for the derivative and state coefficients for normalized memory. The equation supplies Gamma(1-beta) once. Shifted times, actual nonuniform quadratic stencils, backward final memory panels and linear startup are preserved.

All three AUD-02 boundary inputs remain regressions. Final-panel mass uses separately scaled powers and Gamma(1+r), avoiding intermediate product underflow and reciprocal-Gamma overflow. For the tiny-panel input, M0 is representable but M1 and M2 are not; the complete tuple raises an informative DomainError.

The tuple API requires its three positive moments to be finite **normal Float64 values**. This is a conservative declared precision domain, not the claim that every nonzero subnormal value is unrepresentable. Subnormal panel steps themselves are allowed when the requested moments satisfy this contract. Full time meshes additionally require strictly increasing converted Float64 nodes and strictly interior representable shifted times. Conversion is checked after rounding; inputs are never clamped.

The [original module](../GR07.jl), tests and results remain archived. The [boundary analysis](../../../../research/legendre/aud02/revision-01/REPAIRS.md) gives exact inputs, oracle values, failure mechanisms and criteria. No discretization or optimization was added.

## Read the mathematics

The [revised manuscripts](manuscripts/) preserve all original theorem counts and historical numerical tables. All six PDFs compile offline and all 30 pages were visually inspected; failed attempts are retained. GR-04 gives the uniform-grid majorant; GR-05 the ordinary H1 smooth estimate; GR-06 the graded initial-layer estimate under strong Hm-valued regularity. Fixed-order estimates are not order-uniform estimates, and assumed regularity is not a theorem that arbitrary PDE data possess that regularity.

## Reproduce

From the prepared checkpoint root, use the existing pinned environment and approved containment described in the [validation guide](../../../../research/legendre/aud02/revision-01/VALIDATION.md). The bounded serial runner accepts a fresh identifier:

```bash
python3 -B research/legendre/aud02/revision-01/scripts/validate_checkpoint.py --run-id researcher01 --part numerics
python3 -B research/legendre/aud02/revision-01/scripts/validate_checkpoint.py --run-id researcher01 --part lean
python3 -B research/legendre/aud02/revision-01/scripts/validate_checkpoint.py --run-id researcher01 --part latex
```

[run.jl](run.jl) supplies all 156 scientific cases. The revised [tests](test/runtests.jl) retain the complete original suite and boundary regressions. Fresh outputs use separate run directories. The invalid initial GR-07 reference is not used. Original performance measurements belong to the original source identity; this changed implementation has no fresh timing admission or performance claim.
