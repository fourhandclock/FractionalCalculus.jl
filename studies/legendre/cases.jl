"""
    paper_example(number; alpha=0.5, beta=0.2, nu=2.3, lambda=1.0, no_memory_variant=false)

Manufactured problems of the Legendre paper's Section 6 on (-1,1) or (-1,1)^2, T=1, with zero
Dirichlet data. Exact solutions and analytic spatial gradients are included.
The memory integral is unnormalized (no reciprocal Gamma(1-beta)).
`no_memory_variant=true` selects the different zero-initial-data problem used
for Example 6.2 Tables 12-14: u=t^(3+alpha)*sin(pi*x), lambda=0.
"""
function paper_example(number::Integer; alpha::Real=0.5, beta::Real=0.2,
                       nu::Real=2.3, lambda::Real=1.0, no_memory_variant::Bool=false)
    0 < alpha < 1 || throw(ArgumentError("alpha must lie in (0,1)"))
    0 < beta < 1 || throw(ArgumentError("beta must lie in (0,1)"))
    isfinite(lambda) || throw(ArgumentError("lambda must be finite"))
    no_memory_variant && number != 2 && throw(ArgumentError("no_memory_variant applies only to Example 6.2"))
    a, b, v, lam = Float64.((alpha, beta, nu, lambda))
    smooth = (t, s) -> t - s
    if number == 1
        isfinite(v) && v >= 2 || throw(ArgumentError("Example 6.1 requires finite nu >= 2"))
        phi(x) = max(0.0, 1 - x^2)^v
        exact = (p, t) -> t^2 * phi(p[1])
        gradient = (p, t) -> (-2v * p[1] * t^2 * max(0.0, 1-p[1]^2)^(v-1),)
        coefficient = (p, t) -> sin(p[1])
        forcing = function(p, t)
            x = p[1]
            z = max(0.0, 1-x^2)
            2t^(2-a) / gamma(3-a) * phi(x) + 2v*t^2*z^(v-1) -
                4v*(v-1)*t^2*x^2*z^(v-2) + lam*t^4/12*sin(x)*phi(x)
        end
        return (; name="Example 6.1", number, alpha=a, beta=nothing, lambda=lam,
                coefficient, kernel=smooth, initial=p->0.0, forcing, exact, gradient, dimensions=1)
    elseif number == 2
        if no_memory_variant
            exact = (p, t) -> t^(3+a)*sinpi(p[1])
            gradient = (p, t) -> (t^(3+a)*pi*cospi(p[1]),)
            forcing = (p, t) -> (gamma(4+a)/gamma(4)*t^3 + pi^2*t^(3+a))*sinpi(p[1])
            return (; name="Example 6.2 (lambda=0 variant)", number, alpha=a, beta=b, lambda=0.0,
                    coefficient=(p,t)->p[1], kernel=smooth, initial=p->0.0,
                    forcing, exact, gradient, dimensions=1)
        end
        exact = (p, t) -> (1-t^(3+a))*sinpi(p[1])
        gradient = (p, t) -> ((1-t^(3+a))*pi*cospi(p[1]),)
        coefficient = (p, t) -> p[1]
        forcing = (p, t) -> (-gamma(4+a)/gamma(4)*t^3 + pi^2*(1-t^(3+a)) +
            lam*p[1]*(t^(1-b)/(1-b) - t^(4+a-b)*FractionalCalculus.beta(4+a,1-b))) * sinpi(p[1])
        return (; name="Example 6.2", number, alpha=a, beta=b, lambda=lam,
                coefficient, kernel=smooth, initial=p->sinpi(p[1]), forcing, exact, gradient, dimensions=1)
    elseif number == 3
        exact = (p, t) -> t^a*cospi(p[1]/2)
        gradient = (p, t) -> (-pi/2*t^a*sinpi(p[1]/2),)
        coefficient = (p, t) -> exp(p[1])
        forcing = (p, t) -> (gamma(1+a) + pi^2/4*t^a +
            lam*exp(p[1])*t^(a+0.5)*FractionalCalculus.beta(1+a,0.5))*cospi(p[1]/2)
        return (; name="Example 6.3", number, alpha=a, beta=0.5, lambda=lam,
                coefficient, kernel=smooth, initial=p->0.0, forcing, exact, gradient, dimensions=1)
    elseif number == 4
        exact = (p, t) -> t^a*sinpi(p[1])*sinpi(p[2])
        gradient = (p, t) -> (pi*t^a*cospi(p[1])*sinpi(p[2]), pi*t^a*sinpi(p[1])*cospi(p[2]))
        coefficient = (p, t) -> 1.0
        forcing = (p, t) -> (gamma(1+a) + 2pi^2*t^a +
            lam*t^(1+a-b)*FractionalCalculus.beta(1+a,1-b))*sinpi(p[1])*sinpi(p[2])
        return (; name="Example 6.4", number, alpha=a, beta=b, lambda=lam,
                coefficient, kernel=smooth, initial=p->0.0, forcing, exact, gradient, dimensions=2)
    end
    throw(ArgumentError("paper example must be 1, 2, 3, or 4"))
end
