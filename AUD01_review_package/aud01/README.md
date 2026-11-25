# AUD-01 — Internal proof audit revision

## What this revision contains

The 35-page manuscript is a successor to the original ST-05 snapshot, not a replacement for its historical evidence. Section 14 records the TM-01 forcing qualification, a homogeneous initial-layer sharpness proof, and a constant-kernel reference solution. The earlier audit record is retained separately.

- `legendre_spectral_verification_notes_aud01.{tex,pdf}`: complete manuscript.
- `audit_addendum.tex`: new section for inspection.
- `ST05_proof_audit.md`: preceding audit, unchanged.
- `verify_aud01_homogeneous.py`, `homogeneous_results.txt`: newly executed independent reference/evolution diagnostic, 12 configurations.
- `check_exact_aud01.py`, `exact_results.txt`: newly executed symbolic and rational checks.
- `AuditConstants.lean`: uncompiled Lean draft; polynomial/rational targets only.

The homogeneous test uses alpha=3/4, beta=1/2, T=2^-10, and K=lambda=1. Finite grids through N=4096 show approximately 0.75 convergence and negative signed integrated residuals; the normalized memory defect is positive. Do not claim these tests establish the asymptotic 0.5 exponent. The analytic asymptotic lower bound and finite tests have separate evidentiary roles. The homogeneous example has an initial layer; the smooth forced example is not a homogeneous theorem counterexample by itself.

## Local replay and formalization

From this directory, run `python3 -B check_exact_aud01.py` (SymPy), and `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B verify_aud01_homogeneous.py` (NumPy, SciPy, mpmath). Reference environment: NumPy 2.3.5, SciPy 1.17.0, mpmath 1.3.0, SymPy 1.14.0. Use new output filenames to preserve the retained evidence.

Compile the complete TeX in a separate output directory with `pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error`, repeated until references stabilize.

Use the existing pinned Lean 4.19.0/mathlib project from the ST-04 checkpoint. Review the draft, compile with `lake env lean` in the project, and write an axiom-audit driver for every accepted theorem. Do not treat any draft as a certificate. Check all theorem statements against the mathematical targets; no `sorry`, `admit`, or new axioms. Separately attempt a general finite summation-by-parts lemma and oscillator algebra. Do not attempt to replace the analytic infinite-sequence or fractional PDE proof with numeric assertions.

## Independent review gates before repository integration

Ask a fresh reviewer to try to refute the proofs, not to confirm them. Check these specifically:

1. SP-02: stationary startup correction; positive-real integrand; two-sided symbol estimate and derivative; uniform-in-spatial-spectrum weighted resolvent; Cauchy integration by parts; initial data and short-block bounds.
2. TM-01: exact sign and leading asymptotic of memory error; summed Caputo residual; discrete summation by parts; homogeneous versus forced scope, initial regularity, and post-startup index range. Check both proof and numerical reference.
3. ST-05: endpoint oscillator, logistic smoothing, quantitative order perturbation, Neumann derivative regularity, independent L1 inverse convolution, and all-fine-grid transfer. Check the exact paper hypotheses and the quantifiers of Theorem 3.1. Do not round the exact fractional orders to machine precision.
4. SP-01: spatial product regularity, Ritz projection, forcing consistency, nodal vs continuous weighted norms and uniformity of the constants.

Record each outcome as accepted, repair required, or unresolved with reasons. Separate human/external review, internal analytical review, numerical execution, and Lean-certified statements. Preserve all original notes, failed attempts, and numeric outputs. Do not modify the production numerical baseline. Use a new research branch only after local review, not a direct main edit; do not automatically merge or push. The present package contains no new Lean/Julia compilation, external peer review, or GitHub changes.

During preparation, an initial draft real-part expansion used the wrong sign for the imaginary cross term. The exact polynomial check rejected it; the corrected draft and corresponding check are supplied. The manuscript's original complex identity was correct and unchanged.
