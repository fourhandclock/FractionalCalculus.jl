#!/usr/bin/env julia
# Usage: julia --project=<package> studies/legendre/export_figures.jl [--output-dir=<path>]
using FractionalCalculus

const FIGURE_DIR = joinpath(@__DIR__, "figures")
const PACKAGE_ROOT = normpath(joinpath(@__DIR__, "..", ".."))
const FIGURE_SOURCE = joinpath(PACKAGE_ROOT, "src", "FractionalCalculus.jl")
normpath(pathof(FractionalCalculus)) == FIGURE_SOURCE || error("Load this research fork with --project=$PACKAGE_ROOT")

function figure_csv(path, header, rows)
    cell(x) = x === nothing ? "" : string(x)
    open(path, "w") do io
        println(io, join(header, ','))
        for row in rows
            println(io, join(cell.(row), ','))
        end
    end
end

function export_case(label, example; scheme=:L1, alpha, beta=0.2, nu=2.3, M, N, grading=1.0)
    problem = paper_example(example; alpha, beta, nu)
    sol = solve_tfide(problem; M, N, scheme, grading)
    metrics = error_norms(sol)
    rows = Vector{Any}[]
    for (n, t) in enumerate(sol.times), (i, point) in enumerate(sol.space.points)
        truth = problem.exact(point, t)
        push!(rows, Any[label, example, scheme, alpha, problem.beta, example == 1 ? nu : nothing, 1.0,
                       M isa Tuple ? M[1] : M, M isa Tuple ? M[2] : nothing,
                       N, grading, n-1, i-1, t, point[1], length(point) == 2 ? point[2] : nothing,
                       truth, sol.values[i,n], abs(truth-sol.values[i,n])])
    end
    params = Any[label, example, scheme, alpha, problem.beta, example == 1 ? nu : nothing, 1.0,
                 M isa Tuple ? M[1] : M, M isa Tuple ? M[2] : nothing, N, grading, 1.0,
                 metrics.L2, metrics.Linf, metrics.H1, sol.residual, "reconstruction"]
    println(label, ": Linf=", metrics.Linf, ", residual=", sol.residual)
    (; rows, params)
end

function main(args=ARGS)
    output_dir = FIGURE_DIR
    for argument in args
        if startswith(argument, "--output-dir=")
            output_dir = abspath(split(argument, '='; limit=2)[2])
        elseif argument in ("--help", "-h")
            println("Usage: julia --project=<package> studies/legendre/export_figures.jl [--output-dir=<path>]")
            return
        else
            error("Unknown argument: $argument")
        end
    end
    mkpath(output_dir)
    data_header = ["case","example","scheme","alpha","beta","nu","lambda","M1","M2","N","grading",
                   "time_index","point_index","t","x","y","exact","numerical","absolute_error"]
    parameter_header = ["case","example","scheme","alpha","beta","nu","lambda","M1","M2","N","grading","T",
                        "L2","Linf","H1","residual","status"]
    cases = [
        ("figure1", [("caption",1,(; scheme=:L1, alpha=0.55, nu=2.5, M=32, N=10))]),
        ("figure2", [("caption",1,(; scheme=:L12, alpha=0.7, nu=2.9, M=32, N=16))]),
        ("figure4", [("caption",2,(; scheme=:L1, alpha=0.7, beta=0.3, M=20, N=16))]),
        ("figure5", [("alpha$(a)",3,(; scheme=:L1, alpha=a, M=16, N=20, grading=(2-a)/a)) for a in (0.3,0.6,0.9)]),
        ("figure6", [("caption",4,(; scheme=:L1, alpha=0.6, beta=0.7, M=(9,9), N=8, grading=2*(2-0.6)/0.6))])]
    for (name, configurations) in cases
        output = [export_case(label, number; kwargs...) for (label,number,kwargs) in configurations]
        figure_csv(joinpath(output_dir,name*"_solution.csv"),data_header,
                   Iterators.flatten(case.rows for case in output))
        figure_csv(joinpath(output_dir,name*"_parameters.csv"),parameter_header,[case.params for case in output])
    end

    convergence_rows = Vector{Any}[]
    for scheme in (:L1,:L12), N in (4,8,16)
        problem = paper_example(1; alpha=0.5, nu=2.3)
        sol = solve_tfide(problem; M=9, N, scheme)
        metrics = error_norms(sol)
        push!(convergence_rows,Any["caption",1,scheme,0.5,nothing,2.3,1.0,9,nothing,N,1.0,1.0,
                                  metrics.L2,metrics.Linf,metrics.H1,sol.residual,"reconstruction"])
    end
    figure_csv(joinpath(output_dir,"figure3_convergence.csv"),parameter_header,convergence_rows)
    figure_csv(joinpath(output_dir,"figure3_parameters.csv"),parameter_header,convergence_rows)

    rows = Vector{Any}[]
    for N in (16,32,64,128,256,512,1024)
        times = time_mesh(N)
        estimate = sum(memory_weights(times; beta=0.5)[end,:])
        push!(rows,Any[N,1/N,0.5,2.0,estimate,abs(estimate-2.0)])
    end
    figure_csv(joinpath(output_dir,"memory_diagnostic.csv"),
               ["N","tau","beta","exact","approximation","absolute_error"],rows)
    figure_csv(joinpath(output_dir,"memory_diagnostic_parameters.csv"),
               ["case","beta","T","input","rule","expected_observed_order","paper_claimed_order"],
               [["constant-input counterexample",0.5,1.0,1.0,"literal Eq. 6",0.5,1.5]])
    println("Figure data written to ",output_dir)
end

main()
