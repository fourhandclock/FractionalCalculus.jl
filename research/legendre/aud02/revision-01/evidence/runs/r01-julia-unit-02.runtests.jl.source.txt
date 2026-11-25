using Test, LinearAlgebra, Random
using SpecialFunctions: gamma
import FractionalCalculus as FC
include("../GR07.jl")
using .GR07
BLAS.set_num_threads(1)

function oracle_path()
    i=findfirst(x->startswith(x,"--oracles="),ARGS)
    isnothing(i) ? joinpath(@__DIR__,"../../evidence/oracles/moments.csv") : split(ARGS[i],'=',limit=2)[2]
end

# Generic Lagrange evaluation; no local-weight coefficient formula is reused.
function interp(xs,vs,x;derivative=false)
    ans=0.0
    for j in eachindex(xs)
        v=derivative ? vs[j]-vs[1] : vs[j]
        if derivative
            for p in eachindex(xs)
                p==j && continue
                z=1/(xs[j]-xs[p])
                for q in eachindex(xs)
                    q in (j,p) && continue
                    z *= (x-xs[q])/(xs[j]-xs[q])
                end
                ans+=v*z
            end
        else
            z=1.0
            for p in eachindex(xs)
                p==j && continue
                z*=(x-xs[p])/(xs[j]-xs[p])
            end
            ans+=v*z
        end
    end
    ans
end

const XG,WG=GR07.gauss_rule(64)
const XF,WF=GR07.gauss_rule(512)
function integrate_panel(fun,t,star,n,k,r,sigma;derivative=false)
    h=t[k+1]-t[k]
    if k==n
        H=sigma
        x=H.*(1 .- ((XF.+1)./2).^(1/r))
        return (h*H)^r/gamma(1+r)*sum(WF.*fun.(x))/2
    end
    d=(star-t[k])/h; x=(XG.+1)./2
    h^r/gamma(r)*sum(WG.*(d.-x).^(r-1).*fun.(x))/2
end

function direct_rows(t,a,b,n,quadratic)
    sig=1-a/2; star=t[n]+sig*(t[n+1]-t[n]); A=zeros(n); W=zeros(n+1)
    for k in 1:n
        h=t[k+1]-t[k]
        di=k<n ? collect(k:k+2) : collect(k:k+1)
        dx=(t[di].-t[k])./h
        for ell in 1:n
            vals=Float64.((di.-1).>=ell)
            fun=x->interp(dx,vals,x;derivative=true)/h
            A[ell]+=integrate_panel(fun,t,star,n,k,1-a,sig)
        end
        mi=(!quadratic || n==1) ? collect(k:k+1) : (k<n ? collect(k:k+2) : collect(k-1:k+1))
        mx=(t[mi].-t[k])./h
        for j in eachindex(mi)
            vals=zeros(length(mi)); vals[j]=1
            fun=x->interp(mx,vals,x)
            W[mi[j]]+=integrate_panel(fun,t,star,n,k,1-b,sig)
        end
    end
    A,W
end

@testset "GR-07 parameter and convention guards" begin
    for a in (-.1,0.,1.,NaN,Inf)
        @test_throws ArgumentError time_operators([0.,1.],a,.5)
        @test_throws ArgumentError time_operators([0.,1.],.5,a)
    end
    for t in ([0.,0.,1.],[0.,.7,1.],[.1,1.],[0.,Inf],[0.])
        @test_throws ArgumentError time_operators(t,.5,.5)
    end
    @test_throws ArgumentError time_operators([0.,1.],.5,.5;variant=:unknown)
    @test_throws ArgumentError local_moments(0.,.5,1.)
    @test_throws ArgumentError local_moments(1.,1.,1.)
    @test_throws ArgumentError local_moments(1.,.5,.5,1.)
    @test_throws ArgumentError mesh(0)
    @test_throws ArgumentError mesh(4;grading=.5)
    @test length(canonical_cases())==156
end

@testset "Independent high-precision local moments" begin
    path=oracle_path(); @test isfile(path)
    for line in readlines(path)[2:end]
        v=parse.(Float64,split(strip(line),','))
        h,r,d,H=v[1:4]; got=local_moments(h,r,d,H)
        for j in 1:4
            @test isapprox(got[j],v[j+4];rtol=5e-12,atol=1e-300)
        end
    end
end

@testset "Direct interpolation-integral rows, including nonuniform stencils" begin
    for (a,b,g) in ((.5,.25,1.),(.75,.5,2/.75),(.9,.9,1.),(.75,.5,8.))
        t=mesh(4;grading=g)
        for variant in (:Alikhanov_PI_L,:Alikhanov_PI_Q)
            op=time_operators(t,a,b;variant)
            for n in 1:4
                A,W=direct_rows(t,a,b,n,variant==:Alikhanov_PI_Q)
                for k in eachindex(A)
                    @test isapprox(op.A[n,k],A[k];rtol=5e-10,atol=2e-12)
                end
                for k in eachindex(W)
                    @test isapprox(op.W[n,k],W[k];rtol=5e-10,atol=2e-12)
                end
            end
        end
    end
end

@testset "Independent uniform closed forms and polynomial exactness" begin
    for a in (.05,.5,.75,.99)
        N=16; t=mesh(N); sig=1-a/2
        op=time_operators(t,a,.5)
        aa,bb=setprecision(BigFloat,256) do
            ab=BigFloat(a); sb=1-ab/2
            av=[sb^(1-ab); [(j+sb)^(1-ab)-(j-1+sb)^(1-ab) for j in 1:N-1]]
            bv=[((j+sb)^(2-ab)-(j-1+sb)^(2-ab))/(2-ab)-((j+sb)^(1-ab)+(j-1+sb)^(1-ab))/2 for j in 1:N-1]
            Float64.(av),Float64.(bv)
        end
        for n in 1:N,k in 1:n
            lag=n-k
            c=n==1 ? aa[1] : lag==0 ? aa[1]+bb[1] : lag==n-1 ? aa[lag+1]-bb[lag] : aa[lag+1]-bb[lag]+bb[lag+1]
            @test isapprox(op.A[n,k],c*N^a/gamma(2-a);rtol=2e-11,atol=2e-12)
        end
        for degree in 0:2
            got=op.A*diff(t.^degree)
            want=degree==0 ? zeros(N) : gamma(1+degree)/gamma(1+degree-a).*op.star.^(degree-a)
            @test maximum(abs.(got-want))<2e-11
        end
    end
end

@testset "Signs, complementary kernels, tail bounds and shifted energy" begin
    rng=MersenneTwister(707)
    for (a,b,g) in ((.05,.1,1.),(.5,.25,1.),(.5,.25,4.),(.75,.5,2/.75),(.9,.8,2/.9),(.75,.5,12.))
        N=16; t=mesh(N;grading=g); sig=1-a/2; r=1-b
        for variant in (:Alikhanov_PI_L,:Alikhanov_PI_Q)
            op=time_operators(t,a,b;variant); A,W=op.A,op.W
            @test all(A[n,k]>0 for n in 1:N for k in 1:n)
            @test all(all(diff(A[n,1:n]).>0) for n in 2:N)
            @test all((2sig-1)*A[n,n]>sig*A[n,n-1] for n in 2:N)
            P=complementary(A)
            @test minimum(P)>=-2e-12
            @test maximum(abs.(P*A-tril(ones(N,N))))<2e-10
            d=(g==1 ? .5 : 4/11)/gamma(1-a)
            rho=min(1/(2.0^g-1),3.0^(1-g))
            Lq=variant==:Alikhanov_PI_L ? 1.0 : 1+1/(2rho*(1+rho))
            Cq=variant==:Alikhanov_PI_L ? 1.0 : Lq*2^r
            H=abs.(W); PH=P*H[:,2:end]
            for n in 1:N
                mass=op.star[n]^r/gamma(1+r)
                @test isapprox(sum(W[n,:]),mass;rtol=2e-10,atol=2e-12)
                @test sum(H[n,:]) <= Lq*mass*(1+2e-10)+2e-12
                for m in 1:n
                    ell=t[n+1]-t[m]
                    @test A[n,m]>=d*ell^(-a)*(1-2e-10)
                    @test sum(P[n,m:n])<=ell^a/d*(1+2e-10)+2e-12
                    @test sum(H[n,m+1:n+1])<=Cq*ell^r/gamma(1+r)*(1+2e-10)+2e-12
                    @test sum(PH[n,m:n])<=Cq*ell^(a+r)/(d*gamma(1+r))*(1+2e-10)+2e-12
                end
            end
            for degree in (0,1,2)
                err=W*(t.^degree).-gamma(1+degree)/gamma(1+degree+r).*op.star.^(degree+r)
                keep=degree==2 && variant==:Alikhanov_PI_Q ? (2:N) : (1:N)
                if degree<2 || variant==:Alikhanov_PI_Q
                    @test maximum(abs.(err[keep]))<2e-10
                end
            end
            v=randn(rng,N+1,3); dv=A*diff(v,dims=1); vs=sig.*v[2:end,:].+(1-sig).*v[1:end-1,:]
            energy=2 .* vec(sum(dv.*vs,dims=2))-A*diff(vec(sum(abs2.(v),dims=2)))
            scale=1 .+ 2 .* vec(sum(abs.(dv.*vs),dims=2))+abs.(A)*abs.(diff(vec(sum(abs2.(v),dims=2))))
            @test all(energy .>= -1e-11.*scale)
        end
    end
    op=time_operators(mesh(2),.9,.9;variant=:Alikhanov_PI_Q)
    @test isapprox(op.W[2,1]/(op.star[2]^.1/gamma(1.1)),-17/231;rtol=5e-12,atol=5e-13)
    @test op.W[2,1]<0
    t=mesh(8); op=time_operators(t,.75,.5;variant=:Alikhanov_PI_Q)
    @test op.W[1,:]==time_operators(t,.75,.5;variant=:Alikhanov_PI_L).W[1,:]
    @test (op.W*t.^2)[1]>2/gamma(3.5)*op.star[1]^2.5
end

function block_solution(op,space,lambda,K,F,u0)
    N=size(op.A,1); m=length(u0); C=zeros(N,N+1)
    for n in 1:N,k in 1:n
        C[n,k]-=op.A[n,k]; C[n,k+1]+=op.A[n,k]
    end
    B=zeros(N*m,N*m); rhs=zeros(N*m); eye=Matrix{Float64}(I,m,m); lg=lambda*gamma(1-op.beta)
    for n in 1:N
        row=(n-1)*m+1:n*m
        rhs[row]=F[:,n]-(C[n,1].*eye+lg*op.W[n,1].*Diagonal(K[:,n])+(n==1 ? (1-op.sigma).*space.L : zeros(m,m)))*u0
        for k in 1:n
            col=(k-1)*m+1:k*m
            B[row,col]=C[n,k+1].*eye+lg*op.W[n,k+1].*Diagonal(K[:,n])
            n==k && (B[row,col].+=op.sigma.*space.L)
            k==n-1 && (B[row,col].+=(1-op.sigma).*space.L)
        end
    end
    reshape(B\rhs,m,N)
end

@testset "GLL energy, Ritz initialization and independent equation checks" begin
    space=spatial_operators(7)
    @test isapprox(Diagonal(space.mass)*space.L,space.S;atol=2e-13,rtol=2e-13)
    @test isapprox(transpose(space.dB)*(space.wz.*space.dB),space.S;atol=2e-12,rtol=2e-12)
    @test norm(space.rule.D*ones(8),Inf)<2e-13
    p=manufactured(.75,.5,:singular); u0=project_initial(space,p.initial,p.initial_gradient)
    @test norm(space.S*u0-transpose(space.dB)*(space.wz.*p.initial_gradient.(space.z)),Inf)<2e-13
    small=spatial_operators(3)
    @test norm(project_initial(small,p.initial,p.initial_gradient)-project_initial(small,p.initial,p.initial_gradient;initialization=:interpolation))>1e-5
    for N in (1,4), variant in VARIANTS
        op=time_operators(mesh(N;grading=2/.75),.75,.5;variant)
        signedK=(x,t)->(-.7+.3x)*(1+.2sin(t))
        sol=advance(op,space;lambda=.4,coefficient=signedK,forcing=p.forcing,initial=p.initial,initial_gradient=p.initial_gradient)
        @test equation_residual(op,space,sol)<1e-9
        other=block_solution(op,space,.4,sol.K,sol.F,sol.U[:,1])
        @test isapprox(sol.U[:,2:end],other;atol=3e-11,rtol=3e-11)
    end
    # Exactly represented nonzero initial polynomial and linear time factor.
    for variant in (:L12_PI_L,:Alikhanov_PI_L,:Alikhanov_PI_Q)
        a=.75; b=.5; r=1-b; op=time_operators(mesh(8;grading=4),a,b;variant)
        phi=x->1-x^2; K=(x,t)->(1+.3x)*(1+.2sin(t))
        F=(x,t)->phi(x)*t^(1-a)/gamma(2-a)+2*(1+t)+0.4*gamma(r)*K(x,t)*phi(x)*(t^r/gamma(1+r)+t^(1+r)/gamma(2+r))
        sol=advance(op,space;lambda=.4,coefficient=K,forcing=F,initial=phi,initial_gradient=x->-2x)
        want=[phi(x)*(1+t) for x in space.nodes,t in op.times]
        @test maximum(abs.(sol.U-want))<4e-11
    end
    op=time_operators(mesh(8),.75,.5)
    @test_throws ArgumentError advance(op,space;lambda=NaN,coefficient=p.coefficient,forcing=p.forcing,initial=p.initial,initial_gradient=p.initial_gradient)
    @test_throws ArgumentError advance(op,space;lambda=.4,coefficient=(x,t)->NaN,forcing=p.forcing,initial=p.initial,initial_gradient=p.initial_gradient)
    @test_throws ArgumentError project_initial(space,x->1.,x->0.)
    @test_throws ArgumentError project_initial(space,p.initial,p.initial_gradient;initialization=:unknown)
end

@testset "Actual production controls and independent norm quadrature" begin
    M=7; N=8; space=spatial_operators(M); p=manufactured(.75,.5,:singular)
    u0=project_initial(space,p.initial,p.initial_gradient)
    V,_=GR07.legendre_table(space.rule.nodes,M)
    coefficients=V\vcat(0.,u0,0.)
    init=point->dot(GR07.legendre_table([point[1]],M)[1][1,:],coefficients)
    problem=(;dimensions=1,alpha=.75,beta=.5,lambda=.4,kernel=(t,s)->1.,initial=init,
        coefficient=(point,t)->p.coefficient(point[1],t),forcing=(point,t)->p.forcing(point[1],t))
    for (variant,scheme) in ((:L1_printed,:L1),(:L12_printed,:L12))
        op=time_operators(mesh(N),.75,.5;variant)
        @test op.state==FC.caputo_weights(op.times,.75;scheme)
        @test op.W*gamma(.5)≈FC.memory_weights(op.times;beta=.5)
        sol=advance(op,space;lambda=.4,coefficient=p.coefficient,forcing=p.forcing,initial=p.initial,initial_gradient=p.initial_gradient)
        actual=FC.solve_tfide(problem;M,N,scheme)
        @test isapprox(sol.U,actual.values[2:M,:];atol=3e-11,rtol=3e-11)
    end
    op=time_operators(mesh(8),.75,.5)
    sol=advance(op,space;lambda=.4,coefficient=p.coefficient,forcing=p.forcing,initial=p.initial,initial_gradient=p.initial_gradient)
    e80=continuous_errors(op,space,sol,p.exact,p.gradient)
    e120=continuous_errors(op,spatial_operators(M;quadrature_order=120),sol,p.exact,p.gradient)
    @test abs(e80.h1_max-e120.h1_max)<2e-12
    @test abs(e80.l2_max-e120.l2_max)<2e-12
end

@testset "Final-panel quadrature refinement and exact shifted cancellation" begin
    x256,w256=GR07.gauss_rule(256)
    for r in (.01,.1,.5,.75,.99), j in 0:2
        H=.55
        f=x->x^j
        q256=H^r/gamma(1+r)*sum(w256.*f.(H.*(1 .- ((x256.+1)./2).^(1/r))))/2
        q512=H^r/gamma(1+r)*sum(WF.*f.(H.*(1 .- ((XF.+1)./2).^(1/r))))/2
        @test isapprox(q256,q512;atol=2e-12,rtol=5e-10)
    end
    @test local_moments(.25,.1,.55,.55)[4]==0.0
end

@testset "AUD-02 revision 01 exact boundary regressions" begin
    p=findfirst(x->startswith(x,"--boundary-oracle="),ARGS)
    path=isnothing(p) ? joinpath(@__DIR__,"../../../../../research/legendre/aud02/revision-01/evidence/results/boundary.csv") : split(ARGS[p],'=',limit=2)[2]
    @test isfile(path)
    for line in readlines(path)[2:end]
        row=split(strip(line),',')
        name=row[1];h,r,H=parse.(Float64,row[2:4]);expected_big=parse.(BigFloat,row[6:9]);expected=Float64.(expected_big)
        if row[5]=="reject"
            # M0 is representable and repaired. M1 and M2 are not representable;
            # the entire tuple API must reject rather than silently return zeros.
            @test isapprox(GR07.final_panel_mass(h,r,H),expected[1];rtol=5e-12,atol=0)
            @test expected[1]>floatmin(Float64)
            @test 0<expected_big[2]<BigFloat(nextfloat(0.))
            @test 0<expected_big[3]<BigFloat(nextfloat(0.))
            err=try local_moments(h,r,H,H); nothing catch e; e end
            @test err isa DomainError
            @test occursin("M0, M1 and M2",sprint(showerror,err))
        else
            got=local_moments(h,r,H,H)
            for j in 1:4
                @test isapprox(got[j],expected[j];rtol=5e-12,atol=0)
            end
        end
    end
    setprecision(BigFloat,2048) do
        @test_throws ArgumentError time_operators([0.,1.],1-big(2.0)^(-600),.5)
        @test_throws ArgumentError local_moments(big"1e400",.5,1.)
        @test_throws ArgumentError local_moments(big"1e-400",.5,1.)
        @test_throws ArgumentError time_operators(BigFloat[0,1,1+big(2.0)^(-1000)],.5,.5)
    end
    @test_throws ArgumentError time_operators([0.,nextfloat(0.)],.9,.5)
    @test_throws DomainError local_moments(1.,.5,1e-200,1e-200)
end
