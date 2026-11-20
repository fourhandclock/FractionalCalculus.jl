# Regression examples from the supplied mathematical verification notes.
# These checks concern formulas and a proof-step inference, not PDE instability.
@testset "CF-02 and ST-03: corrected coefficients and signed histories" begin
    alpha = 0.75
    scale = inv(FractionalCalculus.gamma(2 - alpha)) # unit time step
    A = caputo_weights([0.0, 1.0, 2.0], alpha; scheme=:L12)
    d0, d1 = 13 / 10, 2.0^(1 / 4) - 13 / 10
    @test A[1, 2] / scale ≈ 1.0 atol=2e-14 # L1 startup remains separate
    @test A[2, 3] / scale ≈ d0 atol=2e-14
    @test -A[2, 1] / scale ≈ d1 atol=2e-14
    @test d1 < 0
    @test (13 // 10)^4 > 2 # exact rational sign argument in notes (5.6)

    # The coefficient of U^(k-r) on the history side is -A[n,k-r+1]/scale.
    h = -reverse(A[2, 1:2]) / scale
    @test h ≈ [d0 - d1, d1] atol=2e-14
    @test sum(h) ≈ d0 atol=2e-14
    @test sum(abs, h) > d0
    # U0=-1, U1=+1 are freely assigned states, not a recurrence trajectory.
    @test abs(dot(h, [1.0, -1.0])) > d0

    # Literal final-line indexing of paper (23) differs on data (0,0,1).
    interpolatory = dot(A[2, :], [0.0, 0.0, 1.0]) / scale
    printed_reversed_k1 = d1
    @test interpolatory ≈ d0 atol=2e-14
    @test printed_reversed_k1 < 0 < interpolatory

    # At alpha=1/2,k=2, a negative history coefficient also occurs.
    alpha = 0.5
    A = caputo_weights([0.0, 1.0, 2.0, 3.0], alpha; scheme=:L12)
    scale = inv(FractionalCalculus.gamma(2 - alpha))
    h = -reverse(A[3, 1:3]) / scale
    @test h[2] < 0
    @test sum(h) ≈ 1 + alpha / (2 * (2 - alpha)) atol=2e-14
end

@testset "ST-04: supplied eigenmode diagnostic using actual library weights" begin
    # Finite-grid candidate only. No spatial discretization or PI replacement.
    alpha, beta, T, N = 0.95, 0.05, 0.8, 128
    sigma = (pi / 2)^2
    kernel(t) = 0.05 + 500 / (1 + exp(-45 * (t - 0.3)))
    times = time_mesh(N; T)
    Q = memory_weights(times; beta)
    K = kernel.(times[2:end])
    for (scheme, expected_peak) in ((:L1, 2.83648192), (:L12, 2.95543966))
        A = caputo_weights(times, alpha; scheme)
        u = zeros(N + 1)
        u[1] = 1
        for n in 1:N
            history = dot(A[n, 1:n], u[1:n]) + K[n] * dot(Q[n, 1:n], u[1:n])
            u[n + 1] = -history / (A[n, n + 1] + sigma + K[n] * Q[n, n + 1])
        end
        @test all(isfinite, u)
        @test maximum(abs, u[2:end]) ≈ expected_peak atol=5e-8
        residual = A * u + sigma * u[2:end] + K .* (Q * u)
        @test maximum(abs, residual) < 5e-10
        alpha0 = FractionalCalculus.gamma(2 - alpha) * (T / N)^alpha
        @test sqrt(1 + sigma * alpha0) * maximum(abs, u[2:end]) > 2
    end
end

@testset "Observation 4: variable-coefficient LGL mass exactness example" begin
    # Status remains the PDF's provisional exactness qualification.
    # M=3 integrates through degree 5, while this mass product has degree 6.
    rule = legendre_lobatto(3)
    x, w = rule.nodes, rule.weights
    c = 0.5 # 0<c<1 ensures a strictly positive coefficient on [-1,1]
    RM = 1 .- x.^2
    rhoM = x .* RM
    Rhat = 1 .+ c .* x
    mass_quadrature = dot(w, Rhat .* RM .* rhoM)
    mass_integral = 16c / 105
    @test mass_quadrature ≈ 16c / 75 atol=3e-14
    @test abs(mass_quadrature - mass_integral) ≈ 32c / 525 atol=3e-14
    @test minimum(Rhat) > 0
end
