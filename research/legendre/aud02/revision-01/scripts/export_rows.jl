using LinearAlgebra
include(joinpath(@__DIR__,"../../../../../studies/legendre/gr07/revision-01/GR07.jl"))
using .GR07
BLAS.set_num_threads(1)
out=ARGS[1]
open(out,"w") do io
    println(io,"case,alpha,beta,variant,n,k,A,W,star")
    for (id,a,b,t) in [("irregular",.35,.82,[0.,.013,.041,.122,.379,1.]),
                       ("graded",.85,.17,mesh(5;grading=2/.85)),
                       ("startup",.02,.97,mesh(2;grading=7.))]
        for variant in (:Alikhanov_PI_L,:Alikhanov_PI_Q)
            op=time_operators(t,a,b;variant)
            for n in 1:length(t)-1,k in 0:n
                aa=k==0 ? 0. : op.A[n,k]
                println(io,join((id,a,b,variant,n,k,aa,op.W[n,k+1],op.star[n]),','))
            end
        end
    end
end
println("independent-oracle input rows written: ",out)


open(ARGS[2],"w") do io
    println(io,"case,h,r,d,H,m0,m1,m2,center")
    for (label,h,r,d,H) in [("tiny_product_M0_only",1e-200,.5,1e-200,1e-200),
                           ("subnormal_step",nextfloat(0.),.5,.55,.55),
                           ("near_zero_order",1.,1e-310,1.,1.)]
        if label=="tiny_product_M0_only"
            # The complete tuple rejects unrepresentable M1/M2. Only the
            # repaired representable M0 helper is evaluated for this CSV.
            m0=GR07.final_panel_mass(h,r,H)
            println(io,join((label,h,r,d,H,m0,"unrepresentable","unrepresentable","not requested"),','))
        else
            println(io,join((label,h,r,d,H,local_moments(h,r,d,H)...),','))
        end
    end
end
