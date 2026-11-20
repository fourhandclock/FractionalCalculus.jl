# ST-04 checkpoint validation

Fresh validation was performed on 2026-11-20 UTC / 2026-11-21 IST. This report supersedes the historical ST-03 integration's tool-availability statements. Historical inputs and earlier local evidence are preserved; they are not relabeled as executions in this session.

| Required check | Actual result | Evidence in `checkpoint-st04/` |
| --- | --- | --- |
| Julia Legendre suite, including `proof_audit.jl` | **669/669 assertions pass**, 12 test sets | `julia-legendre-01.{json,stdout.log,stderr.log}` |
| Independent Python regressions | **10/10 pass**: Volterra sign/rate/table checks, printed vs corrected coefficients, signed histories, exact-rational GLL calculation | `python-counterexamples-01.*` |
| Supplied ST-03 diagnostic | **432 cases pass**, maximum representation discrepancy `3.77e-15` against tolerance `2e-11` | `python-st03-01.*` |
| Supplied ST-04 diagnostic | **24 configurations pass**, L1/L1-2, printed quadrature/product integration, N=128…4096 | `python-st04-01.*`, `st04-parameters.json`, `st04-observations.csv` |
| Original ST-04 LaTeX | **Compiles to 13 pages**, automatically repeated passes; no undefined commands/references or overfull boxes | `latex-checkpoint-01.*`, `latex-final.log`, `latex-artifact.json` |
| Lean coefficient/history module | **17 theorems compile** | `lean-coefficients-06.*` |
| Lean GLL/integral module | **6 theorems compile**, including the actual real interval integral | `lean-quadrature-02.*` |
| Lean axiom audit | **23/23 printed**, only `propext`, `Classical.choice`, `Quot.sound`; no `sorryAx` | `lean-coefficient-axioms-01.*`, `lean-quadrature-axioms-01.*` |

The final static integrity replay passed **37 checks**, including links, source preservation, protected library/result hashes, executed-source bindings, and all 23 axiom records (`static-validation-02.json`). The initial 36-check replay also passed; the final replay adds the test-entrypoint check. Exact commands, source hashes, timestamps, limits, exit codes, and complete stdout/stderr are in the JSON run records and logs. Failed proof sources retained as `.source.txt` are **not certificates**. Final sources are tied to passing records by SHA-256. The [Lean catalogue](../lean/README.md) specifies each certified statement; the [replay guide](../REPRODUCE.md) gives clean-checkout commands.

## Numerical scope

Julia 1.12.6 loaded the actual package from the intended checkpoint snapshot. Its entry module and dependencies came from `a01b208d13e25800da623dcf053b32bcc2eeb0b6`; Legendre operators/cases were unchanged. This excludes unrelated unfinished metric-graph imports and dependencies. The original 645 assertions plus 24 audit assertions passed: 13 coefficient/history, 8 ST-04, and 3 GLL assertions. Tests call library functions; independent Python formulas do not replace them.

The Julia ST-04 subset uses both actual Caputo matrices and the printed memory matrix at N=128. It checks finite values, weighted peaks above two, rounded supplied amplitudes at absolute tolerance `5e-8`, and the **full residual vector** at `5e-10`. The standalone Python ST-04 script checks six residual levels per trajectory. Its fixed defaults, optional-argument limitation, and shared memory-assembly checker are documented in [ST04_PROVENANCE.md](../ST04_PROVENANCE.md).

Python 3.13.16 / NumPy 2.2.6 reproduced all 24 ST-04 configurations. At N=4096 printed-rule weighted peaks are `2.98087371` (L1) and `2.98488050` (L1-2); product-integration controls give `2.98092560` and `2.98493258`. The sampled residual tolerance is `5e-10`; the script asserts weighted peaks greater than two for N≥1024. Rounded output is not an interval enclosure. ST-03's largest weighted amplification `1.08601376` uses `(α,β,σ,λ,N)=(.25,.8,10,10,16)`, with β>α. This is not a theorem counterexample. Freely assigned signed-history states are not scheme trajectories.

No production formula, target, initial value, error norm, historical CSV, or figure was adjusted. [Protected hashes](checkpoint-st04/protected-files.json) cover 48 intended baseline files. [Workspace preservation](checkpoint-st04/workspace-preservation.json) compares all 105 initially inventoried files and reports no unexpected changes, including preservation of unrelated work.

## TeX and source preservation

The main source is **byte-identical** to supplied original ST-04 TeX (SHA-256 `4024424fbf27c58661180ef652103b0bba98dbae7bc013733e0c302ff004d1a8`). Eight sections, eight observations, five propositions, the earlier 22 numbered equations, and seven new ST-04 equations are retained. The earlier manual ST-03 transcription remains a separate historical source; its original LaTeX was not recovered.

Tectonic 0.15.0 produced 13 pages. Rebuildable PDF/auxiliary files stay ignored; the final compiler log and PDF hash are retained. Rendered pages 4, 7, 9, 11, 12, and 13 were inspected for long formulae, tables, and qualifications; no clipping was observed. Warnings retained: UTF-8 `inputenc` ignored, math tokens removed from PDF bookmarks, one underfull paragraph (badness 3302, source lines 508–512), and host Fontconfig warnings. No unresolved-reference or overfull-box warning remains. Source equality protects transcription; rendering is not an independent proof of every formula.

## Setup and failed attempts

[Environment metadata](checkpoint-st04/environment.json) records versions and archive hashes. Julia/NumPy digests were checked against official metadata. Lean/Tectonic hashes identify local downloads; no independent metadata digest check is claimed for them. All tools, depots, sources, and caches are workspace-local and ignored; global environments were unchanged.

All attempts are retained:

- `julia-setup-01` failed precompiling Pkg under the initial 8 MiB file cap; `julia-setup-02` exhausted its 180 s CPU budget with interpreted Pkg. `julia-setup-03` succeeded with a 256 MiB per-file allowance and normal native precompilation. Dependency versions were not changed to obtain a pass; the stale registry PID warning remains in the log.
- `lean-setup-01/02` failed full-history fetches beyond the file budget. The shallow helper then checked out all nine locked revisions. The first cache/widget attempts failed because ProofWidgets lacked its release tag; fetching **that same revision's** `v0.0.57` tag resolved it. `lean-cache-02` downloaded 2347 precompiled files. Only the small cache utility was built locally, not the whole mathlib library.
- `lean-proofs-01` exited 139; `lean-proofs-02` was executor-interrupted with no final wrapper record. Its recovery record confirms zero matching surviving task processes. `lean-proofs-03/04` timed out. Import/prefix diagnostics exposed memory exceptions. Initial split algebra attempts hit memory/`max_memory` option problems. Lean's `-M` flag was removed while external bounds were retained. The next three algebra attempts reported tactic errors. Proofs were corrected without changing their statements; `normalized_history` was added to state normalization explicitly. Attempt 06 passes.
- The first split GLL run hit its sampled RSS ceiling. Its next run passes with a finite 3.5 GiB sampled descendant ceiling; successful peak process RSS was about 2.0 GiB. The final algebra ceiling was 2.25 GiB. Both axiom drivers passed.

Runs are serial with one CPU affinity and single-thread settings. The wrapper applies wall/CPU deadlines, per-process virtual-memory and per-file limits, output monitoring, optional sampled descendant RSS limits, and process-group cleanup. Sampled RSS can count shared pages repeatedly. These controls are **not cgroup aggregate isolation**, and cannot cover deliberately detached children. They implement the user's task-specific execution safeguards, not the older skill's stronger default containment policy. No task processes remain unaccounted for.

Public logs normalize only local path prefixes. Original bytes remain in ignored `.checkpoint-tools/raw-evidence/`; the normalization manifest records raw/public SHA-256 hashes and substitution categories. No numbers, error lines, or failure outcomes are removed. Supplied inputs are never normalized or overwritten.

## Remaining limits

Observations 2 and 8 establish the algebraic and quadrature discrepancies. ST-03 establishes a contraction-proof gap. ST-04 remains a strong **finite-grid numerical counterexample candidate**, not an all-fine-grid refutation or proof of instability. Stability of the corrected L1-2 recurrence and propagation of the Volterra defect into PDE solution error remain open. The exact M=3 calculation does not resolve every hypothesis of Theorem 4.1. The abstract weighted-energy certificate is not a Sobolev theorem; the β=1/2 near-panel certificate is not the full Volterra estimate.

Original VQ-01/CF-02 companions and the original Lean draft remain unavailable. New regressions reproduce named analytical outcomes, not absent code executions. The independent ETNA primary source remains unchecked and its locators source-reported. No new literature search, stability theorem, or production method belongs to this checkpoint.

The final full `git diff --cached --check` reports whitespace in verbatim supplied TeX, retained output/source snapshots, and the generated CSV’s CRLF endings. Those bytes are preserved intentionally. The same check restricted to authored documentation/code/tests and scoped root edits passes. The complete formatting diagnostics and qualification are recorded in `checkpoint-st04/release-preflight.json`; this is not a failed numerical, TeX, or Lean validation.
