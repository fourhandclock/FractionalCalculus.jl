"""
Numerical building blocks and paper-specific fractional-calculus studies.
Study cases, tests, and results are organized under studies/; see README.md.
"""
module FractionalCalculus

using LinearAlgebra
using SpecialFunctions: gamma, beta

include("Legendre.jl")
include("TimeDiscretization.jl")
include("../studies/legendre/cases.jl")
include("Solver.jl")

export legendre_lobatto, legendre_space, time_mesh
export caputo_weights, caputo_derivative, memory_weights
export paper_example, solve_tfide, error_norms

end
