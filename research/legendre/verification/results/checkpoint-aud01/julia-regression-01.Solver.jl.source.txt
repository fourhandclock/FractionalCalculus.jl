"""
    solve_tfide(problem; M=9, N=16, scheme=:L1, grading=1, T=1)

Nodal Galerkin solve of D_C^alpha u - Delta u + lambda*J(u) = f. M is the
Legendre degree, or (Mx,My) in 2D. Only homogeneous Dirichlet data are supported.
Use unscaled Caputo weights to avoid source scaling and L1-2 d0 misprints.
General graded L1-2 interpolation and the nonuniform Eq. 6 extension are explicit
choices because the article does not give their full formulas.
"""
function solve_tfide(problem; M=9, N::Integer=16, scheme::Symbol=:L1,
                     grading::Real=1.0, T::Real=1.0)
    if problem.dimensions == 2 && M isa Integer
        M = (M, M)
    end
    problem.dimensions == (M isa Tuple ? 2 : 1) || throw(ArgumentError("M dimension does not match problem"))
    space = legendre_space(M)
    times = time_mesh(N; T, grading)
    A = caputo_weights(times, problem.alpha; scheme)
    Q = memory_weights(times; beta=problem.beta, kernel=problem.kernel)
    points, ii = space.points, space.interior
    U = zeros(length(points), N + 1)
    U[:, 1] .= problem.initial.(points)
    boundary = setdiff(1:length(points), ii)
    maximum(abs, U[boundary, 1]; init=0.0) <= 1e-12 ||
        throw(ArgumentError("initial data must satisfy homogeneous Dirichlet conditions"))
    U[boundary, 1] .= 0.0
    S = space.stiffness[ii, ii]
    w = space.weights[ii]
    residual = 0.0
    for n in 1:N
        t = times[n + 1]
        c = [problem.coefficient(points[i], t) for i in ii]
        f = [problem.forcing(points[i], t) for i in ii]
        derivative_history = U[ii, 1:n] * A[n, 1:n]
        memory_history = U[ii, 1:n] * Q[n, 1:n]
        mat = S + Diagonal(w .* (A[n, n + 1] .+ problem.lambda*Q[n, n + 1].*c))
        rhs = w .* (f .- derivative_history .- problem.lambda .* c .* memory_history)
        un = mat \ rhs
        U[ii, n + 1] .= un
        residual = max(residual, norm(mat*un-rhs, Inf) / max(1.0, norm(rhs, Inf)))
    end
    (; problem, space, times, values=U, scheme, grading=Float64(grading), residual)
end

"""
    error_norms(solution)

Paper p.28 discrete errors, including all nodes/time levels. `L2` divides the
quadrature-weighted sum by (#spatial nodes)*(#time nodes), as printed. `H1`
adds spatial-gradient errors inside the same normalization. Gradients use the
analytic exact gradient minus the derivative of the numerical interpolant.
`space_time_L2` omits the unusual spatial-node factor, for interpretation.
These are sample averages in time, including on graded grids, not time integrals.
"""
function error_norms(sol)
    p, space, times, U = sol.problem, sol.space, sol.times, sol.values
    exact = [p.exact(point,t) for point in space.points, t in times]
    E = exact - U
    weighted = sum(space.weights .* abs2.(E))
    gradient_error = 0.0
    for d in eachindex(space.derivatives)
        numerical_gradient = space.derivatives[d] * U
        exact_gradient = [p.gradient(point,t)[d] for point in space.points, t in times]
        gradient_error += sum(space.weights .* abs2.(exact_gradient - numerical_gradient))
    end
    denom = length(space.points) * length(times)
    (; L2=sqrt(weighted/denom), Linf=maximum(abs,E),
       H1=sqrt((weighted+gradient_error)/denom),
       space_time_L2=sqrt(weighted/length(times)), residual=sol.residual)
end
