# Reproducible 156-case GR-07 scientific experiment. No package installation.
using LinearAlgebra, Printf
include("GR07.jl")
using .GR07
BLAS.set_num_threads(1)

function argument(name,default)
    p=findfirst(x->startswith(x,name*"="),ARGS)
    isnothing(p) ? default : split(ARGS[p],'=',limit=2)[2]
end
out=abspath(argument("--output-dir",joinpath(@__DIR__,"results","fresh")))
mkpath(out)
file=joinpath(out,"julia_results.csv")
isfile(file) && error("refusing to overwrite $file")
cases=canonical_cases()
open(file,"w") do io
    println(io,"alpha,beta,case,variant,grading,N,M,l2_max,h1_max,h1_final,scaled_residual,assembly_s,spatial_s,solve_s,total_s,time_weight_bytes,history_bytes,initialization,h1_rate")
    previous=Dict{Tuple,Float64}()
    for c in cases
        row=trial(c.a,c.b,c.N,c.M,c.kind,c.variant,c.grading)
        row.scaled_residual<1e-9 || error("full-equation residual failed: $c $(row.scaled_residual)")
        all(isfinite,(row.l2_max,row.h1_max,row.h1_final)) || error("nonfinite error norms")
        key=(c.a,c.b,c.kind,c.variant,c.grading,c.M)
        # The final 12 entries are a spatial sweep, not a temporal doubling.
        temporal=c.M==14
        rate=temporal && haskey(previous,key) ? log2(previous[key]/row.h1_max) : NaN
        temporal && (previous[key]=row.h1_max)
        print(io,join(string.(values(row)),','),',')
        println(io,isfinite(rate) ? string(rate) : "")
        flush(io)
        @printf("%s %s a=%.2f b=%.2f g=%.5g N=%d M=%d H1=%.9e residual=%.3e\n",row.variant,row.case,row.alpha,row.beta,row.grading,row.N,row.M,row.h1_max,row.scaled_residual)
    end
end
println("PASS: $(length(cases)) Julia configurations; continuous max-in-time norms include level zero; no rate assertions.")
