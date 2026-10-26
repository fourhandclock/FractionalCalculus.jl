"""Uniform or graded mesh `T*(n/N)^grading`, including zero and T."""
function time_mesh(N::Integer; T::Real=1.0, grading::Real=1.0)
    N >= 1 || throw(ArgumentError("N must be positive"))
    isfinite(T) && T > 0 || throw(ArgumentError("T must be finite and positive"))
    isfinite(grading) && grading >= 1 || throw(ArgumentError("grading must be finite and >= 1"))
    times = Float64(T) .* ((0:N) ./ N) .^ Float64(grading)
    _check_times(times)
    times
end

function _check_times(times)
    length(times) >= 2 || throw(ArgumentError("at least two time nodes are required"))
    all(isfinite, times) && times[1] == 0 && all(diff(times) .> 0) ||
        throw(ArgumentError("time nodes must be finite, strictly increasing, and start at zero"))
end

# Centered kernel moments. High precision prevents subtractive cancellation on
# graded meshes when an old interval is tiny relative to its distance from t_n.
function _kernel_moments(left, right, alpha)
    p = one(alpha) - alpha
    i0 = (left^p - right^p) / p
    i1 = (left + right) * i0 / 2 - (left^(p + 1) - right^(p + 1)) / (p + 1)
    i0, i1
end

"""
    caputo_weights(times, alpha; scheme=:L1)

Return A with `D_C^alpha u(t_n) ≈ sum(A[n,j+1]*u(t_j), j=0:n)`.
L1 integrates piecewise linear interpolation. L1-2 uses linear interpolation on
the first interval and backward quadratic interpolation on subsequent intervals
(paper Eq. 20-23). Both accept nonuniform nodes. The graded L1-2 rule is an
explicit interpolation-based extension; the paper only derives uniform weights.
"""
function caputo_weights(times::AbstractVector, alpha::Real; scheme::Symbol=:L1)
    _check_times(times)
    0 < alpha < 1 || throw(ArgumentError("Caputo order must satisfy 0 < alpha < 1"))
    scheme in (:L1, :L12) || throw(ArgumentError("scheme must be :L1 or :L12"))
    N = length(times) - 1
    A = zeros(N, N + 1)
    h = times[2] - times[1]
    if all(hj -> isapprox(hj, h; rtol=1e-12, atol=0), diff(times))
        # On uniform grids, O(N) high-precision kernel evaluations suffice.
        b, c = setprecision(BigFloat, 256) do
            ab = BigFloat(alpha)
            bb = [(BigFloat(j+1)^(1-ab)-BigFloat(j)^(1-ab)) for j in 0:N-1]
            cc = [(BigFloat(j+1)^(2-ab)-BigFloat(j)^(2-ab))/(2-ab) -
                  (BigFloat(j+1)^(1-ab)+BigFloat(j)^(1-ab))/2 for j in 0:N-1]
            Float64.(bb), Float64.(cc)
        end
        scale = h^(-alpha)/gamma(2-alpha)
        for n in 1:N, j in 1:n
            lag = n-j
            A[n,j] -= scale*b[lag+1]
            A[n,j+1] += scale*b[lag+1]
            if scheme == :L12 && j >= 2
                A[n,j-1] += scale*c[lag+1]
                A[n,j] -= 2scale*c[lag+1]
                A[n,j+1] += scale*c[lag+1]
            end
        end
        return A
    end
    # Build from local slopes and second divided differences rather than the
    # inconsistent d_j recurrence printed after Eq. 23.
    setprecision(BigFloat, 256) do
        tb = BigFloat.(times)
        ab = BigFloat(alpha)
        invgamma = inv(BigFloat(gamma(1 - Float64(alpha))))
        for n in 1:N
            row = zeros(BigFloat, n + 1)
            for j in 1:n
                h = tb[j + 1] - tb[j]
                i0, i1 = _kernel_moments(tb[n + 1] - tb[j], tb[n + 1] - tb[j + 1], ab)
                row[j] -= i0 / h
                row[j + 1] += i0 / h
                if scheme == :L12 && j >= 2
                    hp = tb[j] - tb[j - 1]
                    # p'(s) = slope_j + 2(s-mid_j)/(hp+h)
                    #                         * (slope_j-slope_{j-1}).
                    correction = 2i1 / (hp + h)
                    row[j - 1] += correction / hp
                    row[j] -= correction * (inv(h) + inv(hp))
                    row[j + 1] += correction / h
                end
            end
            A[n, 1:n+1] .= Float64.(row .* invgamma)
        end
    end
    A
end

"""Evaluate the discrete Caputo derivative of values supplied at the time nodes."""
function caputo_derivative(values::AbstractVector, times::AbstractVector, alpha::Real; scheme::Symbol=:L1)
    length(values) == length(times) || throw(DimensionMismatch("values and time nodes must have equal lengths"))
    caputo_weights(times, alpha; scheme) * values
end

"""
    memory_weights(times; beta=nothing, kernel=(t,s)->1.0)

Return Q for the paper's unnormalized Volterra integral. For `0 < beta < 1`,
use the literal Eq. 6: trapezoids of `(t-s)^(-beta)u(s)` on old intervals and
`h^(1-beta)*(u_{n-1}+u_n)/(2*(1-beta))` on the final interval. For a smooth
kernel pass `beta=nothing` and `kernel(t,s)` for composite trapezoids everywhere.
The singular rule generally has order 1-beta, despite the paper's claimed 2-beta.
"""
function memory_weights(times::AbstractVector; beta::Union{Nothing,Real}=nothing,
                        kernel=(t, s) -> 1.0)
    _check_times(times)
    isnothing(beta) || 0 < beta < 1 || throw(ArgumentError("beta must be nothing or lie in (0,1)"))
    N = length(times) - 1
    Q = zeros(N, N + 1)
    for n in 1:N
        tn = times[n + 1]
        last_regular = isnothing(beta) ? n : n - 1
        for j in 1:last_regular
            h = times[j + 1] - times[j]
            kl = isnothing(beta) ? kernel(tn, times[j]) : (tn - times[j])^(-beta)
            kr = isnothing(beta) ? kernel(tn, times[j + 1]) : (tn - times[j + 1])^(-beta)
            Q[n, j] += h * kl / 2
            Q[n, j + 1] += h * kr / 2
        end
        if !isnothing(beta)
            q = (tn - times[n])^(1 - beta) / (2(1 - beta))
            Q[n, n] += q
            Q[n, n + 1] += q
        end
    end
    Q
end
