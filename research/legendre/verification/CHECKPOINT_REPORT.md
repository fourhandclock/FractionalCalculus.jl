# Validated Legendre checkpoint through ST-04

Repository: `fourhandclock/FractionalCalculus.jl`. Starting branch/commit: `main`, `a01b208d13e25800da623dcf053b32bcc2eeb0b6`. The intended release branch is `research/legendre-verification-st04`. A normal push to `origin` is authorized only after validation; no main/master merge, force-push, or pull request is part of this task. The final Git commit and remote confirmation are reported separately after release, avoiding a self-referential commit hash in this document.

## Integration and file scope

The existing `research/legendre/verification/` layout is retained. The narrow tracking exception exposes this subtree while excluding other research, old private inventories, tools, caches, and generated builds. The existing numerical package remains a reproduction baseline. Unrelated pending metric-graph development and line-ending changes remain local and unstaged; the release uses the baseline module and dependencies already in HEAD.

The original supplied ST-04 TeX is the mathematical authority and is copied without modification to `mathematical-verification.tex`. Its PDF, script, and historical output are preserved separately with hashes. Earlier ST-03 transcription, propositions, observations, source references, and comments remain available; the original ST-04 source retains the earlier mathematical sections in order. [ST04_PROVENANCE.md](ST04_PROVENANCE.md) documents the comparison, filename differences, numerical parameters, and source/code discrepancies.

| Created or updated path | Purpose |
| --- | --- |
| `.gitignore` (repository root) | Expose only this research subtree; exclude local tools, `.lake`, and generated/private artifacts |
| `README.md` (repository root) | Link the validated checkpoint and its limitations; unrelated graph changes excluded from the commit |
| `studies/legendre/test/runtests.jl` | Include the audit tests |
| `studies/legendre/test/proof_audit.jl` | Actual-library coefficient/history, ST-04 scalar, and M=3 GLL regressions |
| `README.md`, `CHECKPOINT_SCOPE.md`, `CHECKPOINT_REPORT.md`, `REPRODUCE.md` | Entry point, commit boundaries, this report, replay instructions |
| `mathematical-verification.tex`, `sources/legendre_spectral_verification_notes_st04.{tex,pdf}` | Exact original ST-04 source and supplied PDF |
| `sources/mathematical-verification-st03-transcription.tex`, ST-03 PDF/extraction/output | Preserve the earlier reconstruction and supplied evidence |
| `ST04_PROVENANCE.md`, `PROVENANCE.md`, `INTEGRATION_SUMMARY.md` | Current source audit plus explicitly historical reconstruction reports |
| `observations/README.md`, `literature/README.md` | Status dossier and publication/source boundaries |
| `sources/inputs.json`, `sources/st04-input-manifest.json` | Portable input names, byte counts, and hashes |
| `scripts/verify_l12_stability.py`, `scripts/verify_time_variable_kernel_st04.py` | Supplied unchanged diagnostics; printed/corrected formulas remain distinct |
| `scripts/check_counterexamples.py` | Independent deterministic VQ-01/CF-02/ST-03/GLL regressions |
| `scripts/run_bounded.py`, `scripts/fetch_lean_sources.py`, `scripts/prepare_evidence.py`, `scripts/check_integration.py` | Bounded capture, shallow pinned dependencies, transparent path normalization, static integrity |
| `requirements.txt` | NumPy 2.2.6, required only by supplied ST-04 diagnostic |
| `lean/{lean-toolchain,lakefile.toml,lake-manifest.json}` | Pinned Lean/mathlib project and transitive lock |
| `lean/{Coefficients,Quadrature}.lean`, corresponding `*Axioms.lean`, `lean/README.md` | Compiled proof sources, axiom drivers, precise theorem catalogue |
| `results/VALIDATION.md`, `results/TEST_PLAN.md` | Fresh outcomes and historical fixed test plan |
| `results/checkpoint-st04/` | Complete successful/failed run logs, exact attempted sources, tool versions, parameters, observed CSV, protected hashes, static report, and complete file inventory |

The machine-readable [checkpoint file inventory](results/checkpoint-st04/checkpoint-files.json) enumerates every intended path individually. It excludes rebuildable binaries and caches. No production source, dependency version, earlier CSV, or figure is changed by this checkpoint.

## Mathematical status

| Item | Established result and remaining limit |
| --- | --- |
| Observation 1 / ST-03 | Established gap in the mixed-sign historical-coefficient contraction induction. Theorem 3.1 remains unresolved; assigned states are not a trajectory |
| Observation 2 | Verified algebraic discrepancy between interpolation and the printed single-sum coefficients. Exact d0=1+α/[2(2−α)]>1 after startup; α=3/4 has a negative historical coefficient |
| Observation 3 | Explicit startup consistency test retained; early-step and fixed-positive-time estimates require separate treatment |
| Observation 4 | Exact M=3 positive variable-coefficient quadrature discrepancy 32c/525 is machine-checked. The general spatial proof qualification remains unresolved |
| Observation 5 | Weighted H1-type norm depends on τ; an abstract two-component nonuniformity statement is certified, without a Sobolev-space formalization |
| Observation 6 | Error-normalization qualification remains; production definitions preserved and inspected |
| Observation 7 | Kernel positivity/sign-assumption question retained; ST-04's kernel is smooth and positive |
| Observation 8 | Verified sharp general Volterra consistency order 1−β for the printed rule, contradicting the stated 2−β estimate. This alone does not disprove the PDE convergence theorem |
| ST-04 | Strong finite-grid counterexample candidate for published contractivity under a positive time-dependent kernel, reproduced for L1/L1-2 and both supplied quadrature variants. No rigorous arbitrarily-fine-grid refutation |

## Validation and implementation comparison

All required numerical/build checks passed: **669 Julia assertions**, **10 Python regression tests**, **432 ST-03 cases**, **24 ST-04 configurations**, **13-page LaTeX build**, and **23 Lean theorems with successful axiom audits**. The [validation report](results/VALIDATION.md) retains exact bounds, warnings, failed attempts, and certificate limitations. Static source/link/evidence checks are recorded separately; they are not numerical or formal proof executions.

The implementation already uses interpolation-derived L1-2 coefficients and the correct historical collection. It preserves the printed singular Volterra rule. Its reported numerical H1 error is not the timestep-weighted theoretical norm, and the additional spatial-node normalization is retained. The test suite exercises actual library functions. The intended snapshot excludes unrelated graph imports/dependencies present in the working tree; no automatic mathematical repair was made.

## Outstanding work and priorities

1. Determine stability of the corrected interpolation recurrence under clearly stated kernel and parameter hypotheses. Establish an appropriate replacement for the mixed-sign contraction step before relying on it downstream. Do not infer instability from the gap alone.
2. For ST-04, turn the candidate into a rigorous question about trajectories and fine timesteps: justify any limiting/smoothing/continuity/convergence steps or derive certified finite-parameter bounds. The α=1,β=0 switched-oscillator illustration is outside the open parameter range and is not that proof.
3. Analyze how the verified Volterra τ^(1−β) defect propagates through the full discrete PDE and scaled residual. Independent product integration remains a supplied control/future direction, not a production replacement.
4. Resolve startup consistency and the variable-coefficient spatial proof assumptions, norm uniformity, error normalization, and kernel-sign examples. Keep the concrete certified calculations separate from broader theorem claims.
5. Recover missing original VQ-01/CF-02 companions and Lean drafts if available; check the cited ETNA article at primary-source level before using its theorem locators. No missing source or independent confirmation is fabricated.

Historical private integration evidence, source-page PNGs, unrelated research, downloaded tools, raw private-path logs, `.lake`, and TeX build products remain local and ignored. Pending metric-graph work and line-ending-only tracked changes remain uncommitted. They are not part of the validated release.
