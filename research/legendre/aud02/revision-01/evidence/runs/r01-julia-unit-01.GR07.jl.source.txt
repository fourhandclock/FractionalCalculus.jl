"""Experimental GR-07 methods. Include explicitly; production dispatch is unchanged.

A acts on increments; W acts on states and approximates normalized I^(1-beta).
All methods are 1D with homogeneous Dirichlet endpoints. Revision 01 repairs
the AUD-02 moment boundary findings; the original module remains archival.
"""
module GR07
using LinearAlgebra
using SpecialFunctions: gamma, beta_inc
import FractionalCalculus as FC

export mesh, local_moments, time_operators, complementary, spatial_operators,
       project_initial, advance, equation_residual, continuous_errors,
       manufactured, trial, VARIANTS, canonical_cases

const VARIANTS = (:L1_printed, :L12_printed, :L12_PI_L, :Alikhanov_PI_L, :Alikhanov_PI_Q)
const LABELS = Dict(:L1_printed=>"L1-printed", :L12_printed=>"L12-printed",
    :L12_PI_L=>"L12-PI-L", :Alikhanov_PI_L=>"Alikhanov-PI-L", :Alikhanov_PI_Q=>"Alikhanov-PI-Q")

function check_order(order)
    isfinite(order) && 0 < order < 1 || throw(ArgumentError("fractional orders must be finite and in (0,1)"))
    value=Float64(order)
    isfinite(value) && 0 < value < 1 || throw(ArgumentError("fractional order is not representable in Float64 inside (0,1)"))
    value
end

function check_times(t)
    t isa AbstractVector && length(t)>=2 || throw(ArgumentError("at least two time nodes required"))
    all(isfinite,t) && t[1]==0 && all(diff(t).>0) || throw(ArgumentError("finite strictly increasing nodes starting at zero required"))
    h=diff(Float64.(t))
    all(x->isfinite(x) && x>0,h) || throw(ArgumentError("time nodes must remain finite and strictly increasing after Float64 conversion"))
    # Uniform and nondecreasing-step grids only. Account for representation of uniform nodes.
    all(h[2:end] .>= h[1:end-1].*(1-64eps(Float64))) || throw(ArgumentError("decreasing steps are outside the supported grid class"))
    all(isfinite,h[2:end]./h[1:end-1]) || throw(ArgumentError("unrepresentable adjacent step ratio"))
    h
end

mesh(N::Integer; T::Real=1.0, grading::Real=1.0) = FC.time_mesh(N;T,grading)

"""Normalized panel moments M_0,M_1,M_2 and stable 2M_1-M_0.

Local x=(s-left)/h, d=(tstar-left)/h, integration x in [0,H]. The fourth
entry is stabilized for completed panels H=1; it matters when d is enormous.
For H/d<=1/4 a convergent positive kernel expansion avoids power subtraction
and cancellation in 2M_1-M_0. Other panels use existing incomplete-beta code;
the final panel uses its exact d=H value, never a subtraction of time nodes.
"""
function local_moments(h::Real,r::Real,d::Real,H::Real=1.0)
    all(isfinite,(h,r,d,H)) && h>0 && 0<r<1 && 0<H<=d || throw(ArgumentError("require h>0, 0<r<1, 0<H<=d, all finite"))
    hf,rf,df,Hf=Float64.((h,r,d,H))
    all(isfinite,(hf,rf,df,Hf)) && hf>0 && 0<rf<1 && 0<Hf<=df || throw(ArgumentError("panel parameters leave the supported domain after Float64 conversion"))
    ig=inv(gamma(rf))
    ig==0 && (ig=rf/gamma(1+rf))
    _moments(hf,rf,df,Hf,ig)
end

# Rescale before exponentiation: h*H can underflow although its power is normal.
final_panel_mass(h,r,H)=h^r*H^r/gamma(1+r)

function checked_moments(values)
    # This tuple API requires all three positive moments to carry normal
    # Float64 precision. Signed centered moments may vanish exactly.
    all(x->isfinite(x) && x>=floatmin(Float64),values[1:3]) ||
        throw(DomainError(values,"M0, M1 and M2 must be finite positive normal Float64 values; panel moments underflow or overflow, so use a representable panel scale"))
    isfinite(values[4]) || throw(DomainError(values,"centered panel moment overflows Float64"))
    values
end

function _moments(h,r,d,H,ig)
    if d == H
        m0=final_panel_mass(h,r,H)
        m1=m0*H/(1+r)
        m2=m1*2H/(2+r)
        return checked_moments((m0,m1,m2,m0*(2H-(1+r))/(1+r)))
    elseif H/d <= 0.25
        z=H/d; term=1.0; s0=1.0; s1=0.5; s2=1/3; sc=H-1.0
        converged=false
        for k in 1:256
            term *= (k-r)/k*z
            s0 += term/(k+1); s1 += term/(k+2); s2 += term/(k+3)
            sc += term*(2H/(k+2)-1/(k+1))
            if term <= eps(Float64)*s2
                converged=true; break
            end
        end
        converged || error("panel series failed its convergence guard")
        scale=h^r*d^(r-1)*H*ig
        return checked_moments((scale*s0,scale*H*s1,scale*H^2*s2,scale*sc))
    end
    m0=h^r*d^r*beta_inc(1.0,r,H/d)[1]*ig/r
    m1=h^r*d^(r+1)*beta_inc(2.0,r,H/d)[1]*ig/(r*(r+1))
    m2=h^r*d^(r+2)*beta_inc(3.0,r,H/d)[1]*2ig/(r*(r+1)*(r+2))
    checked_moments((m0,m1,m2,2m1-m0))
end

function state_to_increments(S)
    N=size(S,1); A=zeros(N,N)
    for n in 1:N
        z=0.0
        for k in n:-1:1
            z+=S[n,k+1]; A[n,k]=z
        end
    end
    A
end

"""Assemble time weights separately from spatial assembly and evolution.

For printed controls the actual production state-weight and memory functions
are called. Their unnormalized memory is divided by Gamma(1-beta) here. The
state matrix is retained for faithful control stepping and diagnostic checks.
"""
function time_operators(times::AbstractVector,alpha::Real,beta::Real;variant::Symbol=:Alikhanov_PI_L)
    a=check_order(alpha); b=check_order(beta); h=check_times(times)
    variant in VARIANTS || throw(ArgumentError("unknown variant $variant"))
    t=Float64.(times); N=length(h); shifted=variant in (:Alikhanov_PI_L,:Alikhanov_PI_Q)
    sigma=shifted ? 1-a/2 : 1.0
    star=t[1:end-1].+sigma.*h
    if shifted
        0.5<sigma<1 && all(t[1:end-1].<star) && all(star.<t[2:end]) ||
            throw(ArgumentError("shifted evaluation times must be representable strictly inside each Float64 timestep"))
    end
    A=zeros(N,N); W=zeros(N,N+1); state=nothing
    if !shifted
        state=FC.caputo_weights(t,a;scheme=variant==:L1_printed ? :L1 : :L12)
        A=state_to_increments(state)
        if variant in (:L1_printed,:L12_printed)
            W=FC.memory_weights(t;beta=b)./gamma(1-b)
        end
    end
    r=1-b; igd=inv(gamma(1-a)); igm=inv(gamma(r)); quadratic=variant==:Alikhanov_PI_Q
    for n in 1:N
        for k in 1:n
            H=k==n ? sigma : 1.0
            d=k==n ? sigma : (star[n]-t[k])/h[k]
            if shifted
                m0,m1,m2,center=_moments(h[k],1-a,d,H,igd)
                A[n,k]+=m0/h[k]
                if k<n
                    R=h[k+1]/h[k]
                    correction=center/(h[k]*(1+R))
                    A[n,k]-=correction
                    A[n,k+1]+=correction/R
                end
            end
            if shifted || variant==:L12_PI_L
                m0,m1,m2,_=_moments(h[k],r,d,H,igm)
                if !quadratic || n==1
                    W[n,k]+=m0-m1; W[n,k+1]+=m1
                elseif k<n
                    R=h[k+1]/h[k]
                    W[n,k]+=(m2-(2+R)*m1+(1+R)*m0)/(1+R)
                    W[n,k+1]+=((1+R)*m1-m2)/R
                    W[n,k+2]+=(m2-m1)/(R*(1+R))
                else
                    rho=h[n-1]/h[n]
                    W[n,n-1]+=(m2-m1)/(rho*(1+rho))
                    W[n,n]+=m0+((1-rho)*m1-m2)/rho
                    W[n,n+1]+=(m2+rho*m1)/(1+rho)
                end
            end
        end
    end
    all(isfinite,A) && all(isfinite,W) && all(>(0),diag(A)) || error("invalid assembled time coefficients")
    (;A,W,state,times=t,star,sigma,alpha=a,beta=b,variant)
end

"""Analysis-only P such that P*A=J. Never assembled by the evolution solver."""
function complementary(A::AbstractMatrix)
    N=size(A,1); size(A,2)==N || throw(DimensionMismatch("square A required"))
    Matrix(transpose(UpperTriangular(transpose(A))\transpose(tril(ones(N,N)))))
end

function gauss_rule(n)
    n>=2 || throw(ArgumentError("Gauss order >=2 required"))
    E=eigen(SymTridiagonal(zeros(n),[k/sqrt(4k^2-1) for k in 1:n-1]))
    E.values,2 .* E.vectors[1,:].^2
end

function legendre_table(x,M)
    V=ones(length(x),M+1); dV=zeros(length(x),M+1)
    V[:,2].=x; dV[:,2].=1
    for k in 2:M
        V[:,k+1].=((2k-1).*x.*V[:,k].-(k-1).*V[:,k-1])./k
        dV[:,k+1].=((2k-1).*(V[:,k].+x.*dV[:,k]).-(k-1).*dV[:,k-1])./k
    end
    V,dV
end

function spatial_operators(M::Integer; quadrature_order::Integer=max(80,2M+10))
    rule=FC.legendre_lobatto(M); ii=2:M
    S=rule.stiffness[ii,ii]; mass=rule.weights[ii]; L=Diagonal(1 ./mass)*S
    z,wz=gauss_rule(quadrature_order)
    V,_=legendre_table(rule.nodes,M); C=V\Matrix{Float64}(I,M+1,M+1)
    G,dG=legendre_table(z,M); B=G*C; dB=dG*C
    (;M,rule,nodes=rule.nodes[ii],S,mass,L,z,wz,B=B[:,ii],dB=dB[:,ii],quadrature_order)
end

function project_initial(space,initial,initial_gradient;initialization::Symbol=:ritz)
    initialization in (:ritz,:interpolation) || throw(ArgumentError("initialization must be :ritz or explicitly labeled :interpolation"))
    all(isfinite,[initial(-1.0),initial(1.0)]) && max(abs(initial(-1.0)),abs(initial(1.0)))<=1e-12 || throw(ArgumentError("initial data must satisfy zero Dirichlet endpoints"))
    values=initialization==:ritz ? space.S\(transpose(space.dB)*(space.wz.*initial_gradient.(space.z))) : initial.(space.nodes)
    all(isfinite,values) || throw(ArgumentError("nonfinite initial projection"))
    values
end

"""Dense full-history solve using preassembled time and spatial operators.

Callbacks coefficient(x,tstar), forcing(x,tstar) use continuous representatives.
State controls use the production state matrix; shifted methods use increments.
"""
function advance(op,space;lambda::Real,coefficient,forcing,initial,initial_gradient,initialization::Symbol=:ritz)
    isfinite(lambda) || throw(ArgumentError("finite lambda required"))
    N=size(op.A,1); m=length(space.nodes); U=zeros(m,N+1); du=zeros(m,N)
    U[:,1]=project_initial(space,initial,initial_gradient;initialization)
    K=zeros(m,N); F=zeros(m,N); lg=Float64(lambda)*gamma(1-op.beta); theta=1-op.sigma
    for n in 1:N
        K[:,n].=coefficient.(space.nodes,op.star[n]); F[:,n].=forcing.(space.nodes,op.star[n])
        all(isfinite,@view(K[:,n])) && all(isfinite,@view(F[:,n])) || throw(ArgumentError("nonfinite nodal coefficient/forcing"))
        rhs=copy(@view F[:,n])
        if isnothing(op.state)
            rhs .+= op.A[n,n].*U[:,n]
            n>1 && (rhs .-= (@view du[:,1:n-1])*(@view op.A[n,1:n-1]))
        else
            rhs .-= (@view U[:,1:n])*(@view op.state[n,1:n])
        end
        rhs .-= theta.*(space.L*U[:,n])
        rhs .-= lg.*K[:,n].*((@view U[:,1:n])*(@view op.W[n,1:n]))
        mat=op.sigma.*space.L+Diagonal(op.A[n,n].+lg*op.W[n,n+1].*K[:,n])
        U[:,n+1]=mat\rhs
        all(isfinite,@view U[:,n+1]) || error("nonfinite solution")
        du[:,n]=U[:,n+1]-U[:,n]
    end
    (;U,K,F,lambda=Float64(lambda),initialization)
end

function equation_residual(op,space,sol)
    lg=sol.lambda*gamma(1-op.beta); du=diff(sol.U,dims=2)
    V=op.sigma.*sol.U[:,2:end].+(1-op.sigma).*sol.U[:,1:end-1]
    residual=op.A*transpose(du)+transpose(V)*transpose(space.L)+lg.*transpose(sol.K).*(op.W*transpose(sol.U))-transpose(sol.F)
    scale=1 .+ abs.(op.A)*transpose(abs.(du))+transpose(abs.(V))*transpose(abs.(space.L))+abs(lg).*transpose(abs.(sol.K)).*(abs.(op.W)*transpose(abs.(sol.U)))+transpose(abs.(sol.F))
    maximum(abs.(residual)./scale)
end

function continuous_errors(op,space,sol,exact,gradient)
    exact_values=[exact(x,t) for x in space.z,t in op.times]
    exact_grad=[gradient(x,t) for x in space.z,t in op.times]
    e=space.B*sol.U-exact_values; ex=space.dB*sol.U-exact_grad
    l2=sqrt.(vec(transpose(space.wz)*abs2.(e)))
    h1=sqrt.(vec(transpose(space.wz)*(abs2.(e)+abs2.(ex))))
    (;l2_max=maximum(l2),h1_max=maximum(h1),h1_final=last(h1),l2,h1)
end

function manufactured(alpha::Real,beta::Real,kind::Symbol;lambda::Real=0.4)
    a=check_order(alpha); b=check_order(beta); kind in (:smooth,:singular) || throw(ArgumentError("unknown case"))
    p=kind==:smooth ? 2.0 : a; base=kind==:smooth ? 0.0 : 1.0; r=1-b
    phi=x->cospi(x/2); dphi=x->-pi/2*sinpi(x/2)
    exact=(x,t)->phi(x)*(base+t^p); gradient=(x,t)->dphi(x)*(base+t^p)
    coefficient=(x,t)->(1+0.3x)*(1+0.2sin(t))
    forcing=(x,t)->(gamma(1+p)/gamma(1+p-a)*t^(p-a)+pi^2/4*(base+t^p))*phi(x)+lambda*gamma(r)*coefficient(x,t)*(base*t^r/gamma(1+r)+gamma(1+p)/gamma(1+p+r)*t^(p+r))*phi(x)
    (;alpha=a,beta=b,kind,lambda=Float64(lambda),coefficient,forcing,initial=x->base*phi(x),initial_gradient=x->base*dphi(x),exact,gradient)
end

function trial(a,b,N,M,kind,variant,grading;initialization=:ritz,quadrature_order=max(80,2M+10))
    p=manufactured(a,b,kind)
    time0=time_ns(); times=mesh(N;grading)
    t0=time_ns(); op=time_operators(times,a,b;variant); assembly=(time_ns()-t0)/1e9
    t0=time_ns(); space=spatial_operators(M;quadrature_order); spatial=(time_ns()-t0)/1e9
    t0=time_ns(); sol=advance(op,space;lambda=p.lambda,coefficient=p.coefficient,forcing=p.forcing,initial=p.initial,initial_gradient=p.initial_gradient,initialization=initialization); stepping=(time_ns()-t0)/1e9
    total=(time_ns()-time0)/1e9
    residual=equation_residual(op,space,sol)
    err=continuous_errors(op,space,sol,p.exact,p.gradient)
    (;alpha=Float64(a),beta=Float64(b),case=String(kind),variant=LABELS[variant],grading=Float64(grading),N,M,
      l2_max=err.l2_max,h1_max=err.h1_max,h1_final=err.h1_final,scaled_residual=residual,
      assembly_s=assembly,spatial_s=spatial,solve_s=stepping,total_s=total,
      time_weight_bytes=sizeof(op.A)+sizeof(op.W)+(isnothing(op.state) ? 0 : sizeof(op.state)),
      history_bytes=sizeof(sol.U),initialization=String(initialization))
end

function canonical_cases()
    cases=NamedTuple[]
    for (a,b) in ((0.5,0.25),(0.75,0.5),(0.9,0.8)), kind in (:smooth,:singular), variant in VARIANTS
        for grading in (kind==:singular && variant in (:Alikhanov_PI_L,:Alikhanov_PI_Q) ? (1.0,2/a) : (1.0,))
            for N in (32,64,128,256)
                push!(cases,(;a,b,N,M=14,kind,variant,grading))
            end
        end
    end
    for variant in (:Alikhanov_PI_L,:Alikhanov_PI_Q), M in (3,5,7,9,12,16)
        push!(cases,(;a=0.75,b=0.5,N=256,M,kind=:singular,variant,grading=2/0.75))
    end
    cases
end
end
