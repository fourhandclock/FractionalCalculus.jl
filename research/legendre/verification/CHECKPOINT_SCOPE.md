> Archival ST-04 release scope. Authorization, staging, and environment details below describe the original release procedure. The current research entry points are the [overview](README.md) and [reproduction guide](REPRODUCE.md).

# Intended ST-04 checkpoint scope

This task authorizes inspection, a dedicated research branch, coherent commits, and a normal push to `origin`. It does not authorize merging, force-pushing, pull requests, or inclusion of unrelated unfinished work. Initial branch: `main`; initial commit: `a01b208d13e25800da623dcf053b32bcc2eeb0b6`; repository: `fourhandclock/FractionalCalculus.jl`. The initial index was empty.

The working tree already contains a metric-graph implementation, corresponding dependency/module/README changes, and line-ending-only changes to several existing files. Those are preserved locally and excluded from this checkpoint. In particular, the pending `Project.toml`, `Manifest.toml`, `src/FractionalCalculus.jl`, metric-graph files, license, figures, and numerical CSV changes are not staged by this task.

The intended commit includes:

- A narrow `.gitignore` exception for `research/legendre/verification/`, with toolchains, caches, build outputs, prior private integration evidence, and other research excluded.
- Only the verification-guide paragraph and its research-tracking qualification in the root README. Other pending README edits belong to the metric-graph study and remain unstaged.
- `studies/legendre/test/proof_audit.jl` and its single study-runner include, plus the current task's documented ST-04 actual-library regression if validated.
- Mathematical documentation through ST-04, supplied original LaTeX/PDF/script/output, retained ST-03 sources, portable input manifests, independent regressions, reproducibility instructions, and full bounded validation logs.
- A pinned Lean 4/mathlib project, its source proofs, dependency lock, exact theorem statements, and compiler/axiom-audit output. Dependency sources and compiled caches are excluded.

Validation uses a local snapshot of the exact intended checkpoint: tracked `HEAD` library/project files plus these scoped changes. This is necessary because the working module currently imports the unrelated uncommitted graph study. The Legendre operators in that snapshot are the actual package implementations, not copied mathematical replacements. Snapshot hashes and commands are retained. Neither the working source nor historical numerical results are rewritten to make a test pass.

The task-specific execution policy is serial, resource-conscious local validation: finite wall and CPU deadlines, per-process address-space/file-size limits where supported, one Julia/BLAS/Lean worker, bounded log files, and process-group termination on timeout or cancellation. These are not claimed to provide cgroup-level aggregate isolation. The user authorized local toolchain downloads after being informed that the tools were absent. Tools, package depots, and acquisition caches stay in `.checkpoint-tools/`; global environments are unchanged.

Before any commit, all required Julia/Python/LaTeX validations and Lean certificates must succeed for the intended snapshot. Failures remain in the evidence directory. If a required validation remains unresolved, no verified release is committed or pushed.

ST-04 remains a strong finite-grid numerical counterexample candidate for the stated contractivity estimate with a smooth positive time-dependent kernel. No claim about every sufficiently fine mesh, a new stability theorem, or a replacement production scheme is made.
