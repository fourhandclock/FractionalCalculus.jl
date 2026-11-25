# Controlled Julia measurements; admission is mandatory and sources are checked.
using LinearAlgebra, SHA, TOML, Printf
include("GR07.jl")
using .GR07
BLAS.set_num_threads(1)

function arg(name,default)
    i=findfirst(x->startswith(x,name*"="),ARGS)
    isnothing(i) ? default : split(ARGS[i],'=',limit=2)[2]
end
function admission(path)
    data=TOML.parsefile(path)
    get(data,"status","")=="admitted" || error("successful matching correctness admission required")
    for (file,digest) in data["files"]
        actual=bytes2hex(sha256(read(joinpath(@__DIR__,file))))
        actual==digest || error("admitted source/input changed: $file")
    end
    data
end

function measurement(N,kind,variant,grading)
    a=.75; b=.5; M=14; p=manufactured(a,b,kind)
    all=@timed begin
        times=mesh(N;grading)
        tw=@timed time_operators(times,a,b;variant)
        sp=@timed spatial_operators(M)
        so=@timed advance(tw.value,sp.value;lambda=p.lambda,coefficient=p.coefficient,
            forcing=p.forcing,initial=p.initial,initial_gradient=p.initial_gradient)
        (tw,sp,so)
    end
    tw,sp,so=all.value
    # Correctness checks outside the timed region, on every fresh sample.
    residual=equation_residual(tw.value,sp.value,so.value)
    residual<1e-9 || error("measured output failed residual criterion")
    e=continuous_errors(tw.value,sp.value,so.value,p.exact,p.gradient)
    phases=(tw,sp,so,all)
    times=[p.time for p in phases]; bytes=[p.bytes for p in phases]
    allocs=[Base.gc_alloc_count(p.gcstats) for p in phases]
    op=tw.value; weights=sizeof(op.A)+sizeof(op.W)+(isnothing(op.state) ? 0 : sizeof(op.state))
    (;times,bytes,allocs,h1=e.h1_max,l2=e.l2_max,residual,weights,history=sizeof(so.value.U),
      compile_s=all.compile_time,recompile_s=all.recompile_time,gc_s=all.gctime)
end

admitted=admission(arg("--admission",joinpath(@__DIR__,"evidence/admission.toml")))
function check_sample(result,N,kind,variant)
    key=string(N,"|",kind,"|",GR07.LABELS[variant])
    expected=admitted["expected"][key]
    for (value,name) in ((result.h1,"h1_max"),(result.l2,"l2_max"))
        abs(value-expected[name])<=5e-11+2e-6*abs(expected[name]) || error("measured sample disagrees with admitted reference: $key $name")
    end
end
out=abspath(arg("--output-dir",joinpath(@__DIR__,"results/performance")))
mkpath(out); raw=joinpath(out,"timing_repeats.csv"); warm=joinpath(out,"warmups.csv")
(ispath(raw)||ispath(warm)) && error("refusing to overwrite timing output")
header="alpha,beta,case,variant,grading,N,M,repeat,phase,seconds,allocation_count,allocated_bytes,h1_max,l2_max,scaled_residual,time_weight_bytes,history_bytes,total_compile_s,total_recompile_s,total_gc_s"
function writerow(io,N,kind,variant,grading,rep,result)
    for (i,phase) in enumerate(("time_weights","spatial","stepping","total"))
        println(io,join((.75,.5,String(kind),GR07.LABELS[variant],grading,N,14,rep,phase,
            result.times[i],result.allocs[i],result.bytes[i],result.h1,result.l2,result.residual,
            result.weights,result.history,result.compile_s,result.recompile_s,result.gc_s),','))
    end
    flush(io)
end
open(warm,"w") do io
    println(io,header)
    for N in (64,128,256),kind in (:smooth,:singular)
        variants=kind==:smooth ? VARIANTS : VARIANTS[4:5]
        grading=kind==:smooth ? 1.0 : 2/.75
        for v in variants
            result=measurement(N,kind,v,grading)
            check_sample(result,N,kind,v)
            writerow(io,N,kind,v,grading,0,result)
        end
    end
end
println("Warmup complete: 21 configurations; measurements use five fresh-input evaluations each.")
open(raw,"w") do io
    println(io,header)
    for repeat in 1:5
        for N in (iseven(repeat) ? (256,128,64) : (64,128,256)), kind in (iseven(repeat) ? (:singular,:smooth) : (:smooth,:singular))
            variants=collect(kind==:smooth ? VARIANTS : VARIANTS[4:5])
            variants=circshift(variants,repeat-1)
            grading=kind==:smooth ? 1.0 : 2/.75
            for v in variants
                GC.gc() # same pre-sample reset policy, outside the timed operation
                result=measurement(N,kind,v,grading)
                check_sample(result,N,kind,v)
                writerow(io,N,kind,v,grading,repeat,result)
                @printf("repeat=%d N=%d %s %s total=%.6f s alloc=%d H1=%.8e\n",repeat,N,String(kind),GR07.LABELS[v],result.times[4],result.bytes[4],result.h1)
            end
        end
    end
end
admission(arg("--admission",joinpath(@__DIR__,"evidence/admission.toml")))
println("PASS: 105 measured fresh solves, four phase records each; 21 separate warmups retained.")
