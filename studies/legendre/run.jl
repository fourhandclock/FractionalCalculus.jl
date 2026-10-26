#!/usr/bin/env julia
# Run with --project=<this package>. All data/output paths are anchored here.
using FractionalCalculus
using Printf

const REPRODUCTION_DIR = @__DIR__
const PACKAGE_ROOT = normpath(joinpath(REPRODUCTION_DIR, "..", ".."))
const EXPECTED_SOURCE = joinpath(PACKAGE_ROOT, "src", "FractionalCalculus.jl")
normpath(pathof(FractionalCalculus)) == EXPECTED_SOURCE || error(
    "Loaded a different FractionalCalculus package. Start Julia with --project=$PACKAGE_ROOT.")

const METRICS = (:L2, :Linf, :H1)
const SPATIAL_TABLES = Set((3, 4, 10, 11, 18, 21))

optional(::Type{T}, value) where {T} = isempty(value) ? nothing : parse(T, value)

function read_reference(path)
    lines = readlines(path)
    names = Symbol.(split(strip(lines[1]), ','))
    result = NamedTuple[]
    for (line_number, line) in enumerate(lines[2:end])
        isempty(strip(line)) && continue
        values = split(strip(line), ','; keepempty=true)
        length(values) == length(names) || error("Malformed reference CSV at line $(line_number+1)")
        d = Dict(zip(names, values))
        refs = Dict(metric => optional(Float64, d[metric]) for metric in METRICS)
        # Half of the last printed digit, using the original decimal spelling.
        tolerances = Dict{Symbol,Union{Nothing,Float64}}()
        for metric in METRICS
            if refs[metric] === nothing
                tolerances[metric] = nothing
            else
                matched = match(r"^\d+\.(\d+)[eE]([+-]?\d+)$", d[metric])
                matched === nothing && error("Expected scientific notation for published $metric")
                tolerances[metric] = 0.5 * 10.0^(parse(Int, matched.captures[2]) - length(matched.captures[1]))
            end
        end
        push!(result, (; table=parse(Int,d[:table]), example=parse(Int,d[:example]),
                       scheme=Symbol(d[:scheme]), alpha=parse(Float64,d[:alpha]),
                       beta=optional(Float64,d[:beta]), nu=optional(Float64,d[:nu]),
                       lambda=parse(Float64,d[:lambda]), M1=parse(Int,d[:M1]),
                       M2=optional(Int,d[:M2]), N=parse(Int,d[:N]),
                       grading=parse(Float64,d[:grading]), source_page=parse(Int,d[:source_page]),
                       refs, tolerances))
    end
    result
end

function csv_cell(value)
    value === nothing && return ""
    s = string(value)
    occursin(r"[,\"\r\n]", s) ? "\"" * replace(s, "\"" => "\"\"") * "\"" : s
end

function write_csv(path, header, rows)
    open(path, "w") do io
        println(io, join(csv_cell.(header), ','))
        for row in rows
            println(io, join(csv_cell.(row), ','))
        end
    end
end

function configuration_key(row)
    (row.example, row.scheme, row.alpha, row.beta, row.nu, row.lambda,
     row.M1, row.M2, row.N, row.grading)
end

function compute_configuration(row)
    try
        problem = paper_example(row.example; alpha=row.alpha,
            beta=something(row.beta, 0.2), nu=something(row.nu, 2.3),
            lambda=row.lambda, no_memory_variant=(row.example == 2 && row.lambda == 0))
        degree = row.M2 === nothing ? row.M1 : (row.M1, row.M2)
        metrics = nothing
        elapsed = @elapsed begin
            solution = solve_tfide(problem; M=degree, N=row.N, scheme=row.scheme, grading=row.grading)
            metrics = error_norms(solution)
        end
        all(isfinite, values(metrics)) || error("Nonfinite computed metrics")
        (; status="computed", metrics, elapsed, message="")
    catch err
        (; status="failed", metrics=nothing, elapsed=nothing,
           message=replace(sprint(showerror,err), '\n'=>' ', '\r'=>' '))
    end
end

function comparison(row, computed, metric)
    reference = row.refs[metric]
    reference === nothing && return (; relative=nothing, matches=nothing)
    computed.status == "computed" || return (; relative=nothing, matches=false)
    actual = getproperty(computed.metrics, metric)
    # Numerical roundoff is negligible beside the precision of printed tables.
    half_unit = row.tolerances[metric]
    matches = abs(actual-reference) <= half_unit + 8eps(reference)
    (; relative=(actual-reference)/reference, matches)
end

function median_value(values)
    isempty(values) && return nothing
    sorted = sort(values)
    n = length(sorted)
    isodd(n) ? sorted[(n+1)÷2] : (sorted[n÷2]+sorted[n÷2+1])/2
end

function write_rates(path, references, runs)
    groups = Dict{Tuple,Vector{Int}}()
    for (i,row) in enumerate(references)
        spatial = row.table in SPATIAL_TABLES
        fixed_grid = spatial ? row.N : (row.M1,row.M2)
        key = (row.table,row.example,row.scheme,row.alpha,row.beta,row.nu,
               row.lambda,row.grading,fixed_grid)
        push!(get!(groups,key,Int[]),i)
    end
    rate_rows = Vector{Any}[]
    ordered_groups = sort(collect(values(groups)); by=ids->minimum(ids))
    for ids in ordered_groups
        spatial = references[first(ids)].table in SPATIAL_TABLES
        axis(row) = spatial ? row.M1 : row.N
        sort!(ids; by=i->axis(references[i]))
        for k in 1:length(ids)-1
            i,j = ids[k],ids[k+1]
            coarse,fine = references[i],references[j]
            ratio = axis(fine)/axis(coarse)
            for metric in METRICS
                coarse.refs[metric] === nothing && continue
                fine.refs[metric] === nothing && continue
                reference_rate = log(coarse.refs[metric]/fine.refs[metric])/log(ratio)
                local_rate = if runs[i].computed.status == "computed" && runs[j].computed.status == "computed"
                    ec = getproperty(runs[i].computed.metrics,metric)
                    ef = getproperty(runs[j].computed.metrics,metric)
                    ec > 0 && ef > 0 ? log(ec/ef)/log(ratio) : nothing
                else
                    nothing
                end
                push!(rate_rows, Any[coarse.table,coarse.example,coarse.scheme,coarse.alpha,
                    coarse.beta,coarse.nu,coarse.lambda,coarse.grading,spatial ? "M" : "N",
                    axis(coarse),axis(fine),metric,reference_rate,local_rate])
            end
        end
    end
    write_csv(path, ["table","example","scheme","alpha","beta","nu","lambda","grading",
        "axis","coarse_resolution","fine_resolution","metric","rate_from_printed_errors","local_rate"], rate_rows)
end

function write_summary(path, references, runs, cache, all_reference_count)
    tables = sort(unique(row.table for row in references))
    failures = count(run->run.computed.status == "failed", runs)
    matches = count(comparison(row,run.computed,metric).matches === true
                    for (row,run) in zip(references,runs) for metric in METRICS)
    reported = count(row.refs[metric] !== nothing for row in references for metric in METRICS)
    open(path,"w") do io
        println(io,"# Legendre study: comparison with the published tables\n")
        println(io,"Selected **$(length(references)) of $all_reference_count reference configurations**, covering tables $(join(tables,", ")). ",
                "Computed $(length(cache)) distinct configurations; $failures failed solves. ",
                "**$matches of $reported published error cells agree within their printed rounding.**\n")
        println(io,"A cell matches only when the computed value lies within half of its last printed decimal digit ",
                "(at most about 5e-5 relative for these entries). A numerical mismatch remains a mismatch; ",
                "no weights, norms, data, or reference values are fitted to obtain agreement.\n")
        println(io,"| Table | Configurations | Matching / printed cells | Median absolute relative deviation L2 | Linf | H1 | Failed solves |")
        println(io,"| ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
        for table in tables
            ids = findall(row->row.table == table,references)
            table_matches = 0
            table_reported = 0
            medians = String[]
            for metric in METRICS
                deviations = Float64[]
                for i in ids
                    row,run = references[i],runs[i]
                    row.refs[metric] === nothing && continue
                    table_reported += 1
                    comp = comparison(row,run.computed,metric)
                    table_matches += comp.matches === true
                    comp.relative === nothing || push!(deviations,abs(comp.relative))
                end
                middle = median_value(deviations)
                push!(medians,middle === nothing ? "not reported / unavailable" : @sprintf("%.4g%%",100middle))
            end
            failed = count(i->runs[i].computed.status == "failed",ids)
            println(io,"| $table | $(length(ids)) | $table_matches / $table_reported | $(join(medians," | ")) | $failed |")
        end
        println(io,"\n## Interpreting disagreements\n")
        println(io,"- `comparison.csv` preserves each published target, computed metric, signed relative deviation, ",
                "and rounding check. Blank reference metrics were not published and are never manufactured.")
        println(io,"- L2 and H1 use the literal extra spatial-node normalization printed on paper p.28. ",
                "Time is averaged over sampled nodes, including on graded grids. `space_time_L2` is also saved ",
                "without that extra spatial-node divisor; the difference is a norm convention, not a tuned comparison.")
        println(io,"- H1 uses the analytic exact spatial gradient minus the derivative of the computed polynomial. ",
                "The paper does not clearly disambiguate this from differentiating the interpolated nodal error. ",
                "The 2D denominator is the documented product-node extension, which the paper does not explicitly specify.")
        println(io,"- Tables 12-14 use the changed-data zero-initial, no-memory Example 6.2 variant. ",
                "Tables 15-21 use their captioned graded or uniform grids. The graded-grid formulas are documented ",
                "implementation choices because the article does not supply every nonuniform coefficient.")
        println(io,"- The weakly singular memory quadrature is kept as documented, including its consistency issue. ",
                "A complete numerical match is not assumed, and a small solve residual verifies only the assembled linear solve.")
        println(io,"- `rates.csv` recomputes reference rates from printed error pairs and records local rates. ",
                "It does not copy erroneous printed rate placements; Table 20 reverses adjacent L2 rates in its alpha=.4 block.")
        println(io,"\n## Local runtime\n")
        times = [value.elapsed for value in values(cache) if value.elapsed !== nothing]
        total = sum(times;init=0.0)
        println(io,"Unique solves and error evaluation took ",@sprintf("%.6g",total),
                " local seconds in total. Each cached configuration retains its original runtime in `comparison.csv`. ",
                "First-use compilation may be included; these are diagnostic timings, not benchmark repetitions. ",
                "The paper's MATLAB/hardware CPU seconds are not compared.\n")
        println(io,"Julia version: `",VERSION,"`. Package source: `",EXPECTED_SOURCE,"`.")
        if failures > 0
            println(io,"\n## Solve failures\n")
            for (i,run) in enumerate(runs)
                run.computed.status == "failed" || continue
                println(io,"- Reference row $i, Table$(references[i].table): ",run.computed.message)
            end
        end
    end
end

function main(args)
    selected_tables = Set(1:21)
    output_dir = joinpath(REPRODUCTION_DIR,"results")
    limit = typemax(Int)
    for argument in args
        if startswith(argument,"--tables=")
            selected_tables = Set(parse.(Int,split(split(argument,'=';limit=2)[2],',')))
            all(table->1 <= table <= 21,selected_tables) || error("Tables must be in 1:21")
        elseif startswith(argument,"--output-dir=")
            output_dir = abspath(split(argument,'=';limit=2)[2])
        elseif startswith(argument,"--limit=")
            limit = parse(Int,split(argument,'=';limit=2)[2])
            limit > 0 || error("--limit must be positive")
        elseif argument in ("--help","-h")
            println("Usage: julia --project=<package> studies/legendre/run.jl [--tables=12,13] [--limit=1] [--output-dir=<path>]")
            return 0
        else
            error("Unknown argument: $argument")
        end
    end
    all_references = read_reference(joinpath(REPRODUCTION_DIR,"reference_tables.csv"))
    references = filter(row->row.table in selected_tables,all_references)
    references = references[1:min(limit,length(references))]
    isempty(references) && error("No reference rows selected")
    mkpath(output_dir)
    cache = Dict{Tuple,Any}()
    runs = NamedTuple[]
    last_table = 0
    for row in references
        if row.table != last_table
            println("Computing Table $(row.table)...")
            flush(stdout)
            last_table = row.table
        end
        key = configuration_key(row)
        cache_hit = haskey(cache,key)
        computed = get!(()->compute_configuration(row),cache,key)
        push!(runs,(; computed,cache_hit))
    end
    header = Any["table","example","scheme","alpha","beta","nu","lambda","M1","M2","N",
        "grading","source_page","status","cache_hit","local_seconds","residual","space_time_L2"]
    for metric in METRICS
        append!(header,["$(metric)_reference","$(metric)_computed","$(metric)_relative_deviation","$(metric)_matches_rounding"])
    end
    push!(header,"failure_message")
    output_rows = Vector{Any}[]
    for (row,run) in zip(references,runs)
        computed = run.computed
        ok = computed.status == "computed"
        values = Any[row.table,row.example,row.scheme,row.alpha,row.beta,row.nu,row.lambda,
            row.M1,row.M2,row.N,row.grading,row.source_page,computed.status,run.cache_hit,
            computed.elapsed,ok ? computed.metrics.residual : nothing,
            ok ? computed.metrics.space_time_L2 : nothing]
        for metric in METRICS
            comp = comparison(row,computed,metric)
            append!(values,Any[row.refs[metric],ok ? getproperty(computed.metrics,metric) : nothing,
                            comp.relative,comp.matches])
        end
        push!(values,computed.message)
        push!(output_rows,values)
    end
    write_csv(joinpath(output_dir,"comparison.csv"),header,output_rows)
    write_rates(joinpath(output_dir,"rates.csv"),references,runs)
    write_summary(joinpath(output_dir,"REPORT.md"),references,runs,cache,length(all_references))
    println("Saved comparison.csv, rates.csv and REPORT.md in $output_dir")
    any(run->run.computed.status == "failed",runs) ? 1 : 0
end

exit(main(ARGS))
