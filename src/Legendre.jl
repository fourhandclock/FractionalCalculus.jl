"""
    legendre_lobatto(M::Integer)

Construct the Legendre–Gauss–Lobatto rule with polynomial degree `M >= 2`
on `[-1, 1]`. The result contains `M + 1` ascending `nodes`, quadrature
`weights`, the nodal differentiation matrix `D`, the diagonal quadrature
`mass`, and the weak Laplacian `stiffness = D' * mass * D`.

The quadrature is exact through degree `2M - 1`. The mass is the quadrature
mass used by the nodal Galerkin method; it is not the exact continuous
mass matrix for products of degree-`M` polynomials. Boundary conditions
have not yet been imposed on either matrix.
"""
function legendre_lobatto(M::Integer)
    M >= 2 || throw(ArgumentError("the Legendre degree M must be at least 2"))
    degree = Int(M)

    # P'_M is proportional to the Jacobi polynomial P_{M-1}^{(1,1)}.
    # Its roots are the eigenvalues of this symmetric Jacobi matrix.
    n = degree - 1
    offdiagonal = [sqrt(k * (k + 2) / ((2k + 1) * (2k + 3))) for k in 1:(n - 1)]
    roots = eigvals(SymTridiagonal(zeros(n), offdiagonal))
    nodes = vcat(-1.0, roots, 1.0)

    # Three-term recurrence for P_M at the quadrature nodes.
    previous = ones(degree + 1)
    values = copy(nodes)
    for k in 2:degree
        next = ((2k - 1) .* nodes .* values .- (k - 1) .* previous) ./ k
        previous, values = values, next
    end
    weights = 2.0 ./ (degree * (degree + 1) .* values .^ 2)

    # The barycentric weights at Lobatto nodes are proportional to 1/P_M.
    D = zeros(degree + 1, degree + 1)
    for i in eachindex(nodes)
        for j in eachindex(nodes)
            i == j && continue
            D[i, j] = values[i] / (values[j] * (nodes[i] - nodes[j]))
        end
        D[i, i] = -sum(@view D[i, :])
    end

    mass = Diagonal(weights)
    stiffness = Matrix(Symmetric(transpose(D) * mass * D))
    return (; nodes, weights, D, mass, stiffness)
end

"""
    legendre_space(M::Integer)
    legendre_space((Mx, My))

Build the one- or two-dimensional Legendre nodal Galerkin space on
`[-1, 1]` or `[-1, 1]^2`. Each degree must be at least two. The returned
named tuple contains `points`, quadrature `weights`, `mass`, `stiffness`,
the indices `interior` for homogeneous Dirichlet boundary conditions,
full nodal `derivatives`, and the nodal array `shape`.

In two dimensions the x index varies fastest, matching `vec(U)` for a
Julia array `U` with size `(Mx + 1, My + 1)`. The stiffness represents
the sum of the x and y weak Laplacians. The matrices retain boundary
rows and columns; select `[space.interior, space.interior]` when
imposing homogeneous Dirichlet data.
"""
function legendre_space(M::Integer)
    rule = legendre_lobatto(M)
    points = [(x,) for x in rule.nodes]
    interior = collect(2:(length(rule.nodes) - 1))
    derivatives = (rule.D,)
    shape = (length(rule.nodes),)
    return (; rule..., points, interior, derivatives, shape)
end

function legendre_space(M::Tuple{Integer, Integer})
    x = legendre_lobatto(M[1])
    y = legendre_lobatto(M[2])
    nx, ny = length(x.nodes), length(y.nodes)

    points = [(ξ, η) for η in y.nodes for ξ in x.nodes]
    weights = kron(y.weights, x.weights)
    mass = Diagonal(weights)
    stiffness = kron(y.mass, x.stiffness) + kron(y.stiffness, x.mass)
    Ix = Matrix{Float64}(I, nx, nx)
    Iy = Matrix{Float64}(I, ny, ny)
    derivatives = (kron(Iy, x.D), kron(y.D, Ix))
    interior = [i + (j - 1) * nx for j in 2:(ny - 1) for i in 2:(nx - 1)]
    shape = (nx, ny)
    nodes = (x.nodes, y.nodes)
    return (; nodes, points, weights, mass, stiffness, interior, derivatives, shape)
end
