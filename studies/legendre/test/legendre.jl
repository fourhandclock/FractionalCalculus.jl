@testset "Legendre–Gauss–Lobatto quadrature and differentiation" begin
    @test_throws ArgumentError legendre_lobatto(0)
    @test_throws ArgumentError legendre_lobatto(1)
    @test_throws ArgumentError legendre_space((3, 1))

    for M in (2, 3, 5, 8, 16)
        rule = legendre_lobatto(M)
        x, w, D = rule.nodes, rule.weights, rule.D
        @test length(x) == M + 1
        @test first(x) == -1.0
        @test last(x) == 1.0
        @test all(diff(x) .> 0)
        @test all(w .> 0)
        @test x ≈ -reverse(x) atol = 2e-14
        @test w ≈ reverse(w) atol = 2e-14
        @test sum(w) ≈ 2.0 atol = 2e-14
        @test rule.mass isa Diagonal
        @test diag(rule.mass) == w

        # Test the full stated quadrature precision, including odd powers.
        for k in 0:(2M - 1)
            integral = iseven(k) ? 2.0 / (k + 1) : 0.0
            @test dot(w, x .^ k) ≈ integral atol = 5e-14
        end

        # Every polynomial represented by the nodal space differentiates exactly.
        for k in 0:M
            derivative = k == 0 ? zeros(M + 1) : k .* x .^ (k - 1)
            @test D * (x .^ k) ≈ derivative atol = 2e-11
        end

        K = rule.stiffness
        @test K ≈ transpose(D) * rule.mass * D atol = 2e-12
        @test issymmetric(K)
        @test minimum(eigvals(Symmetric(K))) >= -2e-12
        @test K * ones(M + 1) ≈ zeros(M + 1) atol = 2e-12
        @test isposdef(Symmetric(K[2:M, 2:M]))

        # The discrete integration-by-parts identity fixes derivative signs
        # and both endpoint contributions independently of the Gram matrix.
        boundary = zeros(M + 1, M + 1)
        boundary[1, 1], boundary[end, end] = -1.0, 1.0
        @test rule.mass * D + transpose(D) * rule.mass ≈ boundary atol = 2e-12
    end
end

@testset "One-dimensional Legendre space" begin
    space = legendre_space(5)
    @test space.shape == (6,)
    @test space.interior == [2, 3, 4, 5]
    @test space.points == [(x,) for x in space.nodes]
    @test length(space.derivatives) == 1
    @test space.derivatives[1] == space.D
    @test space.mass * ones(6) == space.weights
    @test isposdef(Symmetric(space.stiffness[space.interior, space.interior]))
end

@testset "Tensor Legendre space and x-fastest indexing" begin
    # Unequal degrees expose accidental interchange of the two axes.
    space = legendre_space((4, 3))
    nx, ny = space.shape
    @test space.shape == (5, 4)
    @test length(space.points) == nx * ny
    @test size(space.mass) == (nx * ny, nx * ny)
    @test space.interior == [7, 8, 9, 12, 13, 14]
    @test sum(space.weights) ≈ 4.0 atol = 5e-14
    @test diag(space.mass) == space.weights

    x, y = space.nodes
    for j in 1:ny, i in 1:nx
        @test space.points[i + (j - 1) * nx] == (x[i], y[j])
    end
    @test all(abs(space.points[k][1]) < 1 && abs(space.points[k][2]) < 1
              for k in space.interior)

    Dx, Dy = space.derivatives
    f = [ξ^4 * η^3 for (ξ, η) in space.points]
    fx = [4ξ^3 * η^3 for (ξ, η) in space.points]
    fy = [3ξ^4 * η^2 for (ξ, η) in space.points]
    @test Dx * f ≈ fx atol = 2e-13
    @test Dy * f ≈ fy atol = 2e-13
    @test Dx * Dy ≈ Dy * Dx atol = 2e-13

    K = space.stiffness
    @test issymmetric(K)
    @test K ≈ transpose(Dx) * space.mass * Dx + transpose(Dy) * space.mass * Dy atol = 2e-12
    @test minimum(eigvals(Symmetric(K))) >= -2e-12
    @test K * ones(nx * ny) ≈ zeros(nx * ny) atol = 2e-12
    @test isposdef(Symmetric(K[space.interior, space.interior]))

    # The boundary-zero polynomial has analytic gradient energy 256/45.
    bubble = [(1 - ξ^2) * (1 - η^2) for (ξ, η) in space.points]
    @test dot(bubble, K * bubble) ≈ 256 / 45 atol = 2e-13
end
