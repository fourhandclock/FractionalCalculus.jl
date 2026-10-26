@testset "Time meshes and causal Caputo operators" begin
    @test time_mesh(4) == [0.0, 0.25, 0.5, 0.75, 1.0]
    @test time_mesh(2; T=2, grading=2) == [0.0, 0.5, 2.0]
    @test_throws ArgumentError time_mesh(0)
    @test_throws ArgumentError time_mesh(4; T=0)
    @test_throws ArgumentError time_mesh(4; grading=0.5)
    @test_throws ArgumentError caputo_weights([0.0, 0.2, 0.2], 0.5)
    @test_throws ArgumentError caputo_weights([0.1, 1.0], 0.5)
    @test_throws ArgumentError caputo_weights([0.0, 1.0], 1.0)
    @test_throws ArgumentError caputo_weights([0.0, 1.0], 0.5; scheme=:unknown)
    @test_throws DimensionMismatch caputo_derivative([0.0], [0.0, 1.0], 0.5)

    meshes = (time_mesh(8), time_mesh(12; T=1.2, grading=2.4),
              [0.0, 0.01, 0.03, 0.2, 1.2])
    for times in meshes, alpha in (0.2, 0.6, 0.9), scheme in (:L1, :L12)
        A = caputo_weights(times, alpha; scheme)
        N = length(times) - 1
        @test size(A) == (N, N + 1)
        @test A * ones(N + 1) ≈ zeros(N) atol = 2e-11
        exact = times[2:end] .^ (1 - alpha) ./ FractionalCalculus.gamma(2 - alpha)
        @test caputo_derivative(times, times, alpha; scheme) ≈ exact atol = 2e-12
        @test all(A[n, n + 2:end] == zeros(N - n) for n in 1:N)
        @test all(A[n, n + 1] > 0 for n in 1:N)
    end
end

@testset "Independent uniform L1 and L1-2 increment formulas" begin
    N, tau = 9, 0.125
    times = collect(0:N) .* tau
    values = @. exp(times / 3) + times^3 - 0.7times
    for alpha in (0.2, 0.5, 0.9)
        b(j) = (j + 1)^(1 - alpha) - j^(1 - alpha)
        c(j) = ((j + 1)^(2 - alpha) - j^(2 - alpha)) / (2 - alpha) -
               ((j + 1)^(1 - alpha) + j^(1 - alpha)) / 2
        scale = tau^(-alpha) / FractionalCalculus.gamma(2 - alpha)
        for scheme in (:L1, :L12)
            A = caputo_weights(times, alpha; scheme)
            for n in 1:N
                # This reference is the paper's b_j and b*_j increment sum,
                # independently of the implementation's integrated moments.
                reference = sum(b(n - j) * (values[j + 1] - values[j]) for j in 1:n)
                if scheme == :L12 && n >= 2
                    reference += sum(c(n - j) * (values[j + 1] - 2values[j] + values[j - 1])
                                     for j in 2:n)
                end
                @test dot(A[n, :], values) ≈ scale * reference atol = 5e-13
                d0 = scheme == :L12 && n >= 2 ? 1 + alpha / (2 * (2 - alpha)) : 1.0
                @test A[n, n + 1] / scale ≈ d0 atol = 5e-14
            end
        end
    end

    # A concrete counterexample to the paper's blanket positivity assertion.
    alpha = 0.9
    d1 = 2.0^(1 - alpha) - 1 - alpha / (2 * (2 - alpha))
    @test d1 < 0
    A = caputo_weights([0.0, 1.0, 2.0], alpha; scheme=:L12)
    @test -A[2, 1] * FractionalCalculus.gamma(2 - alpha) ≈ d1 atol = 2e-14
end

@testset "L1-2 quadratic exactness with its linear startup defect" begin
    for times in (time_mesh(12), time_mesh(12; grading=2.7)), alpha in (0.3, 0.8)
        computed = caputo_derivative(times .^ 2, times, alpha; scheme=:L12)
        exact = 2 .* times[2:end] .^ (2 - alpha) ./ FractionalCalculus.gamma(3 - alpha)
        h = times[2]
        startup_error = setprecision(BigFloat, 256) do
            a, hb = BigFloat(alpha), BigFloat(h)
            [begin
                tn = BigFloat(t)
                # Only the first interval uses h instead of the true 2s.
                integral_kernel = (tn^(1 - a) - (tn - hb)^(1 - a)) / (1 - a)
                integral_s_kernel = tn * integral_kernel -
                    (tn^(2 - a) - (tn - hb)^(2 - a)) / (2 - a)
                Float64((hb * integral_kernel - 2integral_s_kernel) /
                        FractionalCalculus.gamma(1 - alpha))
            end for t in times[2:end]]
        end
        @test computed - exact ≈ startup_error atol = 3e-12
        @test maximum(abs, computed - exact) > 1e-7
        @test abs(startup_error[end]) < abs(startup_error[1])
    end
end

@testset "Volterra quadrature and the literal singular-rule limitation" begin
    @test_throws ArgumentError memory_weights([0.0, 1.0]; beta=0.0)
    @test_throws ArgumentError memory_weights([0.0, 1.0]; beta=1.0)
    for times in (time_mesh(10), time_mesh(10; T=1.3, grading=2.5))
        N = length(times) - 1
        Q = memory_weights(times)
        @test Q * ones(N + 1) ≈ times[2:end] atol = 2e-14
        @test Q * times ≈ times[2:end] .^ 2 ./ 2 atol = 2e-14
        @test all(Q[n, n + 2:end] == zeros(N - n) for n in 1:N)

        # Integrating s^2 exposes the known exact trapezoid error on each cell.
        trapezoid_error = cumsum(diff(times) .^ 3) ./ 6
        @test Q * (times .^ 2) ≈ times[2:end] .^ 3 ./ 3 + trapezoid_error atol = 2e-14
        Qsmooth = memory_weights(times; kernel=(t, s) -> t - s)
        @test Qsmooth * ones(N + 1) ≈ times[2:end] .^ 2 ./ 2 atol = 2e-14
        @test Qsmooth * times ≈ times[2:end] .^ 3 ./ 6 - trapezoid_error atol = 2e-14
    end

    for beta in (0.2, 0.5, 0.8)
        errors = [begin
            Q = memory_weights(time_mesh(N); beta)
            @test all(Q .>= 0)
            abs(sum(Q[end, :]) - 1 / (1 - beta))
        end for N in (32, 64, 128)]
        @test errors[3] < errors[2] < errors[1]
        rate = log2(errors[2] / errors[3])
        @test abs(rate - (1 - beta)) < 0.015
        @test rate < 2 - beta - 0.9
    end
    # The beta=1/2 constant-input result is a reproducible paper counterexample.
    Q = memory_weights(time_mesh(16); beta=0.5)
    @test abs(sum(Q[end, :]) - 2) ≈ 0.00974865205936 atol = 5e-14
end

# Polynomial spatial factors remove spatial approximation error from the time
# refinement tests. This manufactured family also tests nonzero initial data.
function _polynomial_test_problem(dimensions; alpha=0.5, power=3.5, lambda=0.0)
    phi = dimensions == 1 ? p -> 1 - p[1]^2 : p -> (1 - p[1]^2) * (1 - p[2]^2)
    minuslaplacian = dimensions == 1 ? p -> 2.0 : p -> 2 * (2 - p[1]^2 - p[2]^2)
    exact = (p, t) -> t^power * phi(p)
    gradient = dimensions == 1 ?
        (p, t) -> (-2p[1] * t^power,) :
        (p, t) -> (-2p[1] * (1 - p[2]^2) * t^power,
                    -2p[2] * (1 - p[1]^2) * t^power)
    coefficient = (p, t) -> 1 + p[1] / 3
    derivative_coefficient = power == 0 ? 0.0 :
        FractionalCalculus.gamma(power + 1) / FractionalCalculus.gamma(power + 1 - alpha)
    forcing = (p, t) -> derivative_coefficient * t^(power - alpha) * phi(p) +
        t^power * minuslaplacian(p) + lambda * coefficient(p, t) * phi(p) * t^(power + 1) / (power + 1)
    initial = power == 0 ? phi : p -> 0.0
    (; dimensions, alpha, beta=nothing, lambda, coefficient, kernel=(t, s) -> 1.0,
       exact, gradient, forcing, initial)
end

@testset "Galerkin solver time convergence in one and two dimensions" begin
    for dimensions in (1, 2), scheme in (:L1, :L12)
        problem = _polynomial_test_problem(dimensions)
        M = dimensions == 1 ? 4 : (4, 3)
        errors = Float64[]
        for N in (16, 32, 64)
            sol = solve_tfide(problem; M, N, scheme)
            norms = error_norms(sol)
            push!(errors, norms.Linf)
            @test norms.residual < 2e-13
            @test norms.Linf > 0
            @test norms.H1 >= norms.L2
            @test norms.space_time_L2 ≈ norms.L2 * sqrt(length(sol.space.points)) atol = 2e-14
            boundary = setdiff(1:length(sol.space.points), sol.space.interior)
            @test all(iszero, sol.values[boundary, :])
            @test all(iszero, sol.values[:, 1])

            # Reconstruct the fully discrete PDE using the complete nodal history.
            A = caputo_weights(sol.times, problem.alpha; scheme)
            Q = memory_weights(sol.times; beta=problem.beta, kernel=problem.kernel)
            ii, w = sol.space.interior, sol.space.weights[sol.space.interior]
            for n in (1, N ÷ 2, N)
                t = sol.times[n + 1]
                f = [problem.forcing(sol.space.points[i], t) for i in ii]
                c = [problem.coefficient(sol.space.points[i], t) for i in ii]
                lhs = sol.space.stiffness[ii, ii] * sol.values[ii, n + 1] +
                      w .* (sol.values[ii, :] * A[n, :] +
                            problem.lambda .* c .* (sol.values[ii, :] * Q[n, :]))
                @test lhs ≈ w .* f atol = 3e-12
            end
        end
        @test errors[3] < errors[2] < errors[1]
        rate = log2(errors[2] / errors[3])
        expected_order = scheme == :L1 ? 1.5 : 2.5
        @test abs(rate - expected_order) < 0.18
    end

    # Exercise the actual paper no-memory variant in addition to polynomial data.
    problem = paper_example(2; alpha=0.5, no_memory_variant=true)
    @test problem.lambda == 0
    @test problem.initial((0.2,)) == 0
    for scheme in (:L1, :L12)
        errors = [error_norms(solve_tfide(problem; M=18, N, scheme)).Linf for N in (16, 32, 64)]
        rate = log2(errors[2] / errors[3])
        @test abs(rate - (scheme == :L1 ? 1.5 : 2.5)) < 0.18
    end
end

@testset "Initial data, boundaries, memory history, and reported norms" begin
    for dimensions in (1, 2), scheme in (:L1, :L12)
        problem = _polynomial_test_problem(dimensions; power=0.0, lambda=0.7)
        M = dimensions == 1 ? 4 : (4, 3)
        sol = solve_tfide(problem; M, N=10, scheme, grading=2.3)
        @test sol.values[:, 1] == problem.initial.(sol.space.points)
        @test error_norms(sol).Linf < 2e-12
        @test error_norms(sol).H1 < 2e-12
        @test sol.residual < 2e-13

        # A constant nodal offset has zero gradient error, so both normalizations
        # can be checked without relying on numerical solution accuracy.
        exact_values = [problem.exact(point, t) for point in sol.space.points, t in sol.times]
        offset = 0.125
        shifted = merge(sol, (; values=exact_values .- offset))
        norms = error_norms(shifted)
        domain_volume = 2.0^dimensions
        expected_L2 = offset * sqrt(domain_volume / length(sol.space.points))
        @test norms.L2 ≈ expected_L2 atol = 2e-14
        @test norms.H1 ≈ expected_L2 atol = 2e-14
        @test norms.Linf ≈ offset atol = 2e-14
        @test norms.space_time_L2 ≈ offset * sqrt(domain_volume) atol = 2e-14
    end

    problem = _polynomial_test_problem(1)
    @test_throws ArgumentError solve_tfide(problem; M=(3, 3))
    bad_initial = merge(problem, (; initial=p -> 1.0))
    @test_throws ArgumentError solve_tfide(bad_initial; M=4)
    @test_throws ArgumentError paper_example(0)
    @test_throws ArgumentError paper_example(1; no_memory_variant=true)
    @test_throws ArgumentError paper_example(1; nu=1.5)
end
