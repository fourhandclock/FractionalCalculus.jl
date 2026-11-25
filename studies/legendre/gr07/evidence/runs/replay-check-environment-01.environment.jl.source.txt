using LinearAlgebra, SpecialFunctions, SHA, TOML, Libdl
BLAS.set_num_threads(1)
filehash(p)=isfile(p) ? bytes2hex(open(sha256,p)) : "unavailable"
binary=joinpath(Sys.BINDIR,"julia")
image=unsafe_string(Base.JLOptions().image_file)
libs=Dict{String,String}()
for lib in Libdl.dllist()
    if occursin("openblas",lowercase(lib)) || occursin("openspecfun",lowercase(lib))
        libs[lib]=filehash(lib)
    end
end
TOML.print(stdout,Dict("julia"=>string(VERSION),"specialfunctions"=>string(Base.pkgversion(SpecialFunctions)),
    "julia_threads"=>Threads.nthreads(),"blas_threads"=>BLAS.get_num_threads(),
    "blas"=>string(BLAS.get_config()),"cpu_name"=>Sys.CPU_NAME,"machine"=>Sys.MACHINE,
    "kernel"=>string(Sys.KERNEL),"word_size"=>Sys.WORD_SIZE,"binary_sha256"=>filehash(binary),
    "sysimage_sha256"=>filehash(image),"native_library_hashes"=>libs,
    "startup_disabled"=>true,"gcthreads"=>1,"additional_dependency_acquisition"=>false))
