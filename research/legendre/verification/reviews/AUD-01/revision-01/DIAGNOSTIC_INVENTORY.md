# Diagnostic source inventory

**Four referenced programs are available and replayed; ten referenced originals remain unavailable or unauthenticated.** Some references give no filename. The inventory distinguishes exact recovery from related implementations and does not infer provenance from a shared equation or paper citation.

The search covered repository sources and retained snapshots, Downloads research materials, and five related starter ZIP archives. Archive members were inspected without extraction or execution. [The search record](search-record.json) lists names, matches, archive hashes, and program-member identities. Dependency caches and Git internals were excluded.

| Reference | Original program | Result |
| --- | --- | --- |
| VQ-01-original — §4 numerical check, TeX 285 | `unnamed original Python checker` | unavailable |
| CF-02-python — §5 reproducibility/formalization, TeX 430–448 | `unnamed original CF-02 Python program` | unavailable |
| CF-02-julia — §5 reproducibility/formalization, TeX 447 | `unnamed standard-library Julia counterpart` | unavailable |
| CF-02-lean — §5 reproducibility/formalization, TeX 447 | `unnamed original mathlib Lean draft` | unavailable |
| ST-03 — §6 numerical diagnostic, TeX 550 | `verify_l12_stability.py` | available |
| ST-04 — §7 numerical record, TeX 654 | `verify_time_variable_kernel_st04.py` | available |
| OB-03 — §8 numerical checks, TeX 735 | `verify_l12_startup_obs03.py` | unavailable |
| OB-04 — §9 reproducibility, TeX 887 | `verify_gll_variable_coefficient_obs04.py` | unavailable |
| SP-02 — §11 numerical diagnostics, TeX 1163–1165 | `verify_sp02_resolvent.py` | unavailable |
| TM-01-failed — §12 numerical diagnostics, TeX 1285 | `unnamed original failed sharpness diagnostic and output` | unavailable |
| TM-01-revised — §12 numerical diagnostics, TeX 1275–1285 | `unnamed corrected smooth/initial-layer/PI diagnostic` | unavailable |
| ST-05 — §13 numerical corroboration, TeX 1404–1413 | `unnamed 36-configuration ST-05 trajectory checker` | unavailable |
| AUD-01-exact — §14 diagnostics and package README | `check_exact_aud01.py` | available |
| AUD-01-homogeneous — §14 diagnostics and package README | `verify_aud01_homogeneous.py` | available |

## Recovery and provenance qualifications

**VQ-01-original.** Later check_counterexamples.py and starter-package reference checks are independently sourced checks, not authenticated originals.

**CF-02-python.** The described direct panel-integration companion is not identified by a filename/hash.

**CF-02-julia.** Existing Julia study tests and starter projects are not established as this original companion.

**CF-02-lean.** The later ST-04 Coefficients module and AUD-01 constants draft have explicit independent provenance.

**ST-03.** Repository and Downloads copies have identical hashes; replayed unchanged.

**ST-04.** Repository and Downloads copies agree; this uses the original ST-04 kernel, not ST-05. The manuscript output filename st04_numerical_results.txt differs from the supplied st04_recheck_2026-11-20.txt.

**OB-03.** No exact-name or authenticated content-equivalent original found.

**OB-04.** Existing M=3 checks are not the described all-degree rational/high-precision program.

**SP-02.** Neither symbol/768-coefficient grids nor the noncommuting matrix checker was recovered.

**TM-01-failed.** The text says the failed source/output were retained separately; they are absent from the searched materials.

**TM-01-revised.** The related temporal-residual starter tests operator residuals, not this flat forced solution-error experiment; not substituted.

**ST-05.** The ST-04 script has a different kernel and is not this program.

**AUD-01-exact.** Supplied exact symbolic/rational checks; replayed unchanged.

**AUD-01-homogeneous.** Supplied 12-case constant-kernel program; replayed unchanged.

## Related materials are not original recoveries

The caputo-L1, caputo-L1-2, weak-Volterra, and temporal-residual starter archives contain related Julia/reference experiments. The temporal-residual README explicitly targets combined operator consistency, with no spatial Galerkin solution-error solver. Its Python smoke checks do not implement the manuscript’s flat forced TM-01 or the steep logistic ST-05 trajectory experiment. The generic research-lab archive is execution infrastructure. None provides an authenticated replacement for the missing original programs.

The existing `check_counterexamples.py` has explicit provenance as a later independent regression suite. Its fresh 10-test result is useful supplementary evidence, but it is not a recovery of the original VQ-01/CF-02 companions. No new reconstructed numerical replacement was introduced.

Missing source/output files prevent replay of the corresponding historical numerical claims. They do not, by themselves, refute the separate analytical proofs. New experimental reconstruction would require a separate scope and provenance record.
