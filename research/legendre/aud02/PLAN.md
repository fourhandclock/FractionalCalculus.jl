# AUD-02 review plan and acceptance criteria

The sealed input is the completed local GR-07 workspace based on AUD-01
`bf43fd0e78bcbcaae94d4c95fd9e43fd562ba477`. All 1,041 source and
evidence files are copied and hashed before review. Originals and the copied
inputs remain unchanged. New work is confined to this audit directory and
disposable workspace-local scratch. No Git operation or dependency acquisition
is part of this review. Primary-literature search and downloads were explicitly
approved separately.

Analytical acceptance requires a derivation under the actual stated assumptions;
passing finite experiments cannot substitute for it. Findings are accepted on
review, repair required, unresolved, or formally certified for the precise Lean
statement only. Literature novelty remains unresolved without an equivalence
analysis; an unsuccessful search is not evidence of novelty.

## Targeted checks

- Exact rational row-tail comparison and arbitrary ordered products: no tolerance
  for inequalities, finite examples including noncommuting original matrices and
  failure of entrywise domination. Check mixed-product simplex shifts exactly
  for positive integer exponents. These test the abstract argument, not its
  infinite-dimensional generalization.
- Independent interpolation-integral oracle for nonuniform derivative and
  memory rows, using generic Lagrange polynomials and mpmath quadrature, not
  incomplete-beta moments or either existing assembly implementation. Compare
  scaled weights with tolerance `8e-11`; polynomial identities `1e-10` scaled.
- Probe moment evaluation at representable Float64 extremes and parameter
  conversion boundaries. Record discrepancies; do not repair the implementation
  or relax tolerances. Distinguish supported experiment range from broad API
  behavior and exact-arithmetic theory.
- Inspect the 7,941-assertion suite, 156 comparisons, 669 baseline assertions,
  oracle construction, continuous norms and benchmark protocol. Reuse sealed
  execution evidence with its exact scope; targeted replay is separately labelled.
- Compile existing 42 named Lean certificates and the feasible new finite
  identities serially with pinned Lean 4.19.0/mathlib revision. Print axioms of
  every accepted named theorem; reject placeholders or unsupported axioms.

## Execution safeguards

Use the existing bounded serial supervisor and GR-07 namespace launcher. Sources,
dependencies and evidence are read-only inside payloads. Each run has fresh
scratch, a finite wall/CPU limit, per-process address-space limit, sampled
descendant RSS threshold, bounded output, single Julia/BLAS worker and verified
PID-namespace cleanup, including detached descendants. This is the explicit
user-approved research exception; aggregate cgroup isolation is unavailable.
Failed and prelaunch attempts are retained. No new experiment starts before
cleanup is verified.
