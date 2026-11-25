using Test

# Each study supplies its own test entry point. Adding a study does not change
# this runner or require mixing its test cases with an existing paper's suite.
const STUDIES_DIR = normpath(joinpath(@__DIR__, "..", "studies"))
for study in sort(readdir(STUDIES_DIR))
    entry = joinpath(STUDIES_DIR, study, "test", "runtests.jl")
    isfile(entry) || continue
    @testset "$study" begin
        include(entry)
    end
end
