# Revision-01 validation and reproduction

**All required validation passes.** The six revised manuscripts compile offline and all 30 pages have been visually inspected. The analytical verdict remains **ACCEPT WITH LIMITATIONS**. Numerical/Lean results below retain their executed source identities; no algorithm or proof source changed during final typesetting. The checkpoint is prepared for publication on its dedicated research branch.


## Executed results

| Check | Actual result | Evidence |
| --- | --- | --- |
| Original failing inputs replay | All three original mechanisms reproduced against the unchanged original module | [original values](evidence/results/original-extremes.csv), [captured run](evidence/runs/r01-original-boundaries-01.stdout.log) |
| Independent complete-beta oracle | All four moments evaluated at 400/500 digits; relative stabilization below 1e-80; impossible tuple components shown strictly below the minimum positive Float64 | [oracle](evidence/runs/r01-boundary-oracle-01.stdout.log) |
| Existing Julia suite | 669/669 pass | [baseline](evidence/runs/r01-final-baseline.stdout.log) |
| Revised GR-07 suite | 7,962/7,962 pass: all 7,941 original assertions plus 21 boundary/conversion regressions | [experimental suite](evidence/runs/r01-final-unit.stdout.log) |
| Original independent moment oracle | 24 panels, 96 polynomial integrals; original 120/180-digit stabilization and tolerances retained | [moment replay](evidence/runs/r01-final-moments.stdout.log) |
| Final supplied Python diagnostics | GR-02–06 pass, including the 60-case graded diagnostic without a rate assertion | [run records](evidence/runs/) |
| Complete Julia/Python scientific matrix | All 156 cases pass original tolerances; largest H1 difference 3.437441303821842e-14 | [comparison](evidence/runs/r01-final-julia-python.stdout.log) |
| Revised versus preserved Julia norms | Largest H1 change 1.9506965487359196e-15, within the original criterion; old results untouched | [comparison](evidence/runs/r01-final-preserved-julia.stdout.log) |
| Independent generic interpolation oracle | 156 coefficient comparisons pass, maximum scaled difference 4.311681156648209e-15 | [repaired independent replay](evidence/runs/r01-repaired-independent-01.stdout.log) |
| Repaired boundary M0 values | Relative errors about 4.76e-17, 1.07e-17 and zero at displayed precision; the tiny-product full tuple is rejected separately | [same independent replay](evidence/runs/r01-repaired-independent-01.stdout.log) |
| Lean | All six proof modules and four audit drivers compile; all 54 named statements report only standard Lean/mathlib axioms | [exact catalogue](evidence/theorem-catalogue.json) |
| Historical manuscript data | Theorem-environment counts and all original tabular blocks unchanged in six revised sources | [preservation check](evidence/manuscript-preservation.json) |
| Revised LaTeX/PDFs | Six offline builds, 30 pages visually inspected; no undefined references, missing citations, TeX errors or box warnings | [final manuscript checks](evidence/final-manuscript-validation.json) |
| Documentation | Nine entry-point/closure Markdown files: all 151 local paths and fragments resolve, balanced fences/math, consistent tables | [link checks](evidence/documentation-checks-05.json) |
| Preservation | 1,393 original audit files and the 481-file original-development guard unchanged; only five documented existing-file edits in prepared copy | [integrity](evidence/integrity.json) |

The first independent-row replay reused the original diagnostic's archived boundary CSV as an explicitly historical input. The later `r01-repaired-independent-01` run supplies newly exported repaired M0 values and is the current boundary evidence. Its tiny-product row evaluates the internal repaired mass helper only; the full tuple's justified rejection is tested in Julia. No failed case is discarded or reported as a successful full tuple.

## Failures retained

The first new Julia regression failed in the **test reader**, which tried to parse the oracle's nonrepresentable values directly as Float64. The corrected reader uses BigFloat and asserts positivity and the representability bound. Original tolerance 5e-12 remains unchanged. A controller prelaunch stopped on Boolean grouping of its existing preservation allowlist before launching a workload; the narrow intended edit list did not expand to cover an unexpected source change. The original offline TeX failure at missing `article.cls` and two subsequent font-cache failures are preserved. The authorized acquisition engine succeeded; its first cache-promotion helper attempted to overwrite unchanged read-only entries. Recovery verified the acquired delta and skipped identical entries, without reacquisition. A resource-inventory helper also needed its local import path corrected; neither helper failure was a scientific test. A documentation prelaunch also stopped at a report-path conversion in the checker; only its path-label calculation was repaired before the successful link check. The [three complete failed TeX logs](evidence/failed-offline-logs.json) are archived without alteration alongside stdout/stderr. All attempted sources and outputs remain in [evidence/runs/](evidence/runs/), with the [prelaunch record](evidence/prelaunch-01.json).

## TeX acquisition and visual inspection

Before acquisition, the private bundle index and cache manifest identified `article.cls` (20,144 bytes), `size11.clo` (8,464 bytes) and `booktabs.sty` (6,078 bytes) as missing. Their exact pre-acquisition record and cache hashes are [preserved](evidence/tex-resources-before-acquisition.json). Subsequent offline failures identified title/body fonts. Required transitive resources were requested only by manuscript package/font fixtures and the six manuscript sources; all acceptance builds then ran with `--only-cached`.

The [complete acquired-resource catalogue](evidence/tex-final-resources.json) records 39 TeX files totalling 1,140,982 bytes, their names and SHA-256 hashes. Acquisition used the existing engine and fixed bundle in this revision's private cache. No global environment, Julia dependency or Lean pin was changed. Acquisition outputs are separate from the accepted offline PDFs. Final stderr retains host Fontconfig warnings about existing configuration attributes; the TeX logs have no warnings, and the rendered pages show the intended fonts.

Every page was rendered using already installed Poppler/Cairo and visually inspected for legible mathematics, tables, headings and bibliography, overlaps, clipping and page breaks. The [render record](evidence/pdf-render-record.json) identifies all PDF hashes and pages. The original failed offline attempt and all fresh attempts remain in the run archive.

## Environment and execution

Existing versions are retained: Julia 1.12.6, SpecialFunctions 2.9.0, Python 3.13.16, NumPy 2.3.5, SciPy 1.17.0, mpmath 1.3.0, SymPy 1.14.0, Lean 4.19.0 and mathlib revision `c44e0c8ee63ca166450922a373c7409c5d26b00b`. Julia project/manifest and formal version pins are unchanged. No numerical dependency acquisition or new performance experiment occurred.

Runs use the existing approved bounded serial policy: one CPU affinity, one Julia/BLAS worker, finite wall/CPU deadlines, per-process address-space limits, sampled descendant RSS, bounded logs, read-only source/evidence mounts and verified PID-namespace cleanup. This is **not strict aggregate cgroup isolation**. The new preflight blocked write/chmod/rename/unlink and verified detached-child teardown. Exact commands, versions, source capsules and cleanup records are retained per run.

Default Julia limits are 300/240 wall/CPU seconds with 8-GiB address-space and 2-GiB sampled RSS bounds; the full matrix has 600/540 seconds. Python scientific jobs have 2-GiB address-space/1-GiB sampled RSS limits. Lean uses 120/90 seconds, 8-GiB address-space/3.5-GiB sampled RSS and `-j1`. TeX uses 120/90 seconds, 2-GiB address-space/1-GiB sampled RSS, untrusted mode and cached resources only. No assertion, rate criterion or residual tolerance was relaxed.

## Reproduce without overwriting evidence

Use a fresh identifier from the prepared workspace root:

```bash
python3 -B research/legendre/aud02/revision-01/scripts/validate_checkpoint.py --run-id researcher01 --part numerics
python3 -B research/legendre/aud02/revision-01/scripts/validate_checkpoint.py --run-id researcher01 --part lean
python3 -B research/legendre/aud02/revision-01/scripts/validate_checkpoint.py --run-id researcher01 --part latex
```

The runner records fresh results under its run identifier and preserves frozen PDFs if they already exist. It requires the locally provisioned pinned runtimes, caches, sealed audit baseline and namespace capability used for this checkpoint. On another machine, provision/adapt those paths through a separately approved setup, or run the included Julia/Python entrypoints with equivalent bounded containment. The controller does not install or update dependencies.

The main Julia entrypoints are [run.jl](../../../../studies/legendre/gr07/revision-01/run.jl) and [test/runtests.jl](../../../../studies/legendre/gr07/revision-01/test/runtests.jl). The [boundary oracle generator](scripts/boundary_oracle.py) and [manuscript generator](scripts/revise_manuscripts.py) preserve the exact source of their respective artifacts. A validation replay never uses the invalid initial reference. Old timings are historical evidence for old source hashes, not a performance admission for revision 01.

## Publication scope

The dedicated branch is `research/legendre-verification-aud02`, based directly on audited AUD-01 commit `bf43fd0e78bcbcaae94d4c95fd9e43fd562ba477`. Publication uses a new isolated Git worktree. The existing development, GR-07 and AUD-01 worktrees are guarded separately; their source files, uncommitted changes and branch heads remain unchanged.

The commit includes the complete GR-07 study with its original and repaired revisions, original/revised GR-01–06 manuscripts, figures and results, the AUD-02 review and closure evidence, and the unchanged 12 additional finite certificate sources integrated with the preserved 42 AUD-01 declarations. Only five previously tracked files change: three navigation READMEs, the narrow audit-directory ignore exception and the Lean root list. Production Julia sources, dependency manifests, old mathematical statements and historical results are byte-identical to the AUD-01 baseline.

All 173 local links in the 17 study/audit guides also resolve; see the [integrated link check](evidence/integrated-study-links.json). The checkpoint checksums identify every included source and artifact. Runtime caches, scratch renders and revision-01 local literature downloads are excluded from publication. Historical downloaded sources already sealed with the original AUD-02 review are preserved. Fresh TeX acquisition is isolated from numerical environments and is represented by its resource/hash catalogue, not bundled toolchain binaries.
