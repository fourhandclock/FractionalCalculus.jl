"""New integration regressions for the supplied mathematical notes.

Standard library only. This is not a recovered VQ-01/CF-02 companion script.
See ../results/TEST_PLAN.md for the fixed domain, tolerances, and run status.
No PDE solver, data rewriting, new quadrature scheme, or file output is used.
The supplied verify_l12_stability.py is imported unchanged and never auto-run.
"""

from decimal import Decimal
from fractions import Fraction
import math
import unittest

from verify_l12_stability import recurrence, weights


def b(alpha, r):
    return (r + 1.0) ** (1 - alpha) - r ** (1 - alpha)


def bstar(alpha, r):
    return (
        ((r + 1.0) ** (2 - alpha) - r ** (2 - alpha)) / (2 - alpha)
        - ((r + 1.0) ** (1 - alpha) + r ** (1 - alpha)) / 2
    )


def interpolatory_two_sum(alpha, values):
    """Notes (5.1), without its common tau^(-alpha)/Gamma(2-alpha)."""
    k = len(values) - 2
    increments = [values[j + 1] - values[j] for j in range(k + 1)]
    return math.fsum(b(alpha, k - j) * increments[j] for j in range(k + 1)) + math.fsum(
        bstar(alpha, k - j) * (increments[j] - increments[j - 1])
        for j in range(1, k + 1)
    )


def corrected_collected_sum(alpha, values):
    """Notes (5.3)-(5.4), using the unchanged supplied coefficient function."""
    k = len(values) - 2
    ds = weights(alpha, k)
    return math.fsum(
        ds[r] * (values[k + 1 - r] - values[k - r]) for r in range(k + 1)
    )


def defining_panel_moments(alpha, values):
    """Integrate the defining local affine derivatives analytically.

    Unit mesh; multiply the integral by (1-alpha), giving the same
    dimensionless bracket as the two sums. This is an analytical moment
    evaluation, not a numerical integration or high-precision experiment.
    """
    n = len(values) - 1
    p = 1 - alpha
    panels = []
    for j in range(n):
        left, right = n - j, n - j - 1
        zeroth = (left ** p - right ** p) / p
        panel = (values[j + 1] - values[j]) * zeroth
        if j >= 1:
            centered = (n - j - 0.5) * zeroth - (
                left ** (p + 1) - right ** (p + 1)
            ) / (p + 1)
            panel += (values[j + 1] - 2 * values[j] + values[j - 1]) * centered
        panels.append((1 - alpha) * panel)
    return math.fsum(panels)


def published_eq23_final_sum_k1(alpha, values):
    """Literal reversed last-line indexing of paper (23), only at k=1.

    At k=1 the printed newest/oldest cases are both defined. For k>=2 the
    printed middle range omits r=1, so no completion of that formula is
    invented here. This differs from corrected_collected_sum intentionally.
    """
    if len(values) != 3:
        raise ValueError("The unambiguous printed diagnostic is restricted to k=1")
    d0 = b(alpha, 0) + bstar(alpha, 0)
    d1 = b(alpha, 1) - bstar(alpha, 0)
    # sum_j Delta u^(k-j) d_(k-j), k=1, as actually printed.
    return (values[2] - values[1]) * d1 + (values[1] - values[0]) * d0


def corrected_diffusion_step(d0, d1, mu):
    u1 = 1 / (1 + mu)
    return ((d0 - d1) * u1 + d1) / (d0 + mu)


def published_d0_one_diffusion_step(d1, mu):
    """Paper (30)'s d0=1 substitution with no rescaling, lambda=0 only."""
    u1 = 1 / (1 + mu)
    return ((1 - d1) * u1 + d1) / (1 + mu)


def printed_volterra_constant(beta, n):
    """Literal Eq. (6), T=K=u=1, using original time nodes."""
    tau = 1 / n
    old = tau / 2 * math.fsum(
        (1 - j * tau) ** (-beta) + (1 - (j + 1) * tau) ** (-beta)
        for j in range(n - 1)
    )
    return old + tau ** (1 - beta) / (1 - beta)


def exact_panel_error_sum(beta, n):
    """Notes (4.4), Q-I; an equivalent identity, not a modified scheme."""
    return (1 / n) ** (1 - beta) * math.fsum(
        ((r - 1) ** (-beta) + r ** (-beta)) / 2
        - (r ** (1 - beta) - (r - 1) ** (1 - beta)) / (1 - beta)
        for r in range(2, n + 1)
    )


class CoefficientAudit(unittest.TestCase):
    def test_exact_leading_identity_and_negative_coefficient_argument(self):
        for alpha in (Fraction(1, 4), Fraction(1, 2), Fraction(3, 4)):
            star0 = 1 / (2 - alpha) - Fraction(1, 2)
            self.assertEqual(star0, alpha / (2 * (2 - alpha)))
            self.assertGreater(star0, 0)
        self.assertEqual(1 + Fraction(3, 4) / (2 * (2 - Fraction(3, 4))), Fraction(13, 10))
        # Since both are positive, this exactly proves 2^(1/4) < 13/10.
        self.assertGreater(Fraction(13, 10) ** 4, 2)

    def test_step_dependent_collection_and_panel_moments(self):
        # Same small coefficient/polynomial domain reported in notes section 5.5.
        for alpha in (0.25, 0.5, 0.75):
            for k in (0, 1, 2, 4):
                for degree in range(4):
                    with self.subTest(alpha=alpha, k=k, degree=degree):
                        values = [float(j ** degree) for j in range(k + 2)]
                        reference = interpolatory_two_sum(alpha, values)
                        self.assertAlmostEqual(corrected_collected_sum(alpha, values), reference, delta=2e-11)
                        self.assertAlmostEqual(defining_panel_moments(alpha, values), reference, delta=2e-11)
                ds = weights(alpha, k)
                history = [ds[r] - ds[r + 1] for r in range(k)] + [ds[k]]
                self.assertAlmostEqual(math.fsum(history), ds[0], delta=2e-14)
                self.assertAlmostEqual(ds[0], 1 if k == 0 else 1 + alpha / (2 * (2 - alpha)), delta=2e-14)

    def test_printed_index_reversal_is_a_separate_formula(self):
        values = [0.0, 0.0, 1.0]
        corrected = interpolatory_two_sum(0.75, values)
        printed = published_eq23_final_sum_k1(0.75, values)
        self.assertAlmostEqual(corrected, 1.3, delta=2e-14)
        self.assertAlmostEqual(printed, 2 ** 0.25 - 1.3, delta=2e-14)
        self.assertLess(printed, 0)
        self.assertGreater(corrected, 0)

    def test_signed_history_refutes_norm_bound_inference_only(self):
        d0, d1 = weights(0.75, 1)
        h0, h1 = d0 - d1, d1
        self.assertLess(d1, 0)
        self.assertGreater(abs(h0) + abs(h1), d0)
        # Assigned states (U0,U1)=(-1,+1) are not a scheme trajectory.
        self.assertGreater(abs(h0 * 1 + h1 * (-1)), d0)
        ds = weights(0.5, 2)
        self.assertGreater(ds[2], ds[1])
        self.assertLess(ds[1] - ds[2], 0)

    def test_d0_substitution_changes_the_reduced_recurrence(self):
        d0, d1 = weights(0.75, 1)
        correct = corrected_diffusion_step(d0, d1, 0.3)
        printed = published_d0_one_diffusion_step(d1, 0.3)
        self.assertAlmostEqual(correct, 0.6090202570, delta=5e-10)
        self.assertAlmostEqual(printed, 0.5720486003, delta=5e-10)
        self.assertGreater(abs(correct - printed), 1e-3)

    def test_supplied_scalar_representations_on_named_reductions(self):
        # Includes the published-note coarse diagnostic, with no contractivity
        # assertion and no attempt to infer a PDE theorem from finite tests.
        cases = ((0.75, 0.5, 1.0, 0.0, 16), (0.25, 0.8, 10.0, 10.0, 16))
        for alpha, beta, sigma, lam, n in cases:
            with self.subTest(parameters=(alpha, beta, sigma, lam, n)):
                collected, _ = recurrence(alpha, beta, n, sigma, lam, "collected")
                increments, _ = recurrence(alpha, beta, n, sigma, lam, "increments")
                self.assertTrue(all(math.isfinite(v) for v in collected + increments))
                self.assertLess(max(abs(x - y) for x, y in zip(collected, increments)), 2e-11)


class VolterraAudit(unittest.TestCase):
    def test_positive_near_panel_and_finite_sum_identity(self):
        for beta in (0.2, 0.5, 0.8):
            c_beta = (1 + 2 ** (-beta)) / 2 - (2 ** (1 - beta) - 1) / (1 - beta)
            self.assertGreater(c_beta, 0)
            for n in (16, 256, 512, 1024):
                with self.subTest(beta=beta, n=n):
                    error = printed_volterra_constant(beta, n) - 1 / (1 - beta)
                    self.assertGreaterEqual(error + 2e-12, c_beta * (1 / n) ** (1 - beta))
                    self.assertAlmostEqual(error, exact_panel_error_sum(beta, n), delta=2e-12)

    def test_reported_table_rounding_and_order(self):
        # Transcribed historical predictions, not integration execution results.
        targets = {
            0.2: ("1.90147e-4", "1.09293e-4", "6.27930e-5"),
            0.5: ("2.47721e-3", "1.75194e-3", "1.23888e-3"),
            0.8: ("2.06036e-2", "1.79371e-2", "1.56153e-2"),
        }
        for beta, strings in targets.items():
            errors = []
            for n, target in zip((256, 512, 1024), strings):
                error = printed_volterra_constant(beta, n) - 1 / (1 - beta)
                errors.append(error)
                decimal = Decimal(target)
                rounding = float(Decimal(10) ** decimal.as_tuple().exponent) / 2
                self.assertAlmostEqual(error, float(decimal), delta=rounding + 2e-12)
            self.assertGreater(errors[0], errors[1])
            self.assertGreater(errors[1], errors[2])
            self.assertAlmostEqual(math.log2(errors[1] / errors[2]), 1 - beta, delta=0.0015)

    def test_existing_beta_half_counterexample(self):
        self.assertAlmostEqual(printed_volterra_constant(0.5, 16) - 2, 0.00974865205936, delta=5e-14)


class SpatialAudit(unittest.TestCase):
    def test_lgl_variable_coefficient_example_exact_rationals(self):
        c = Fraction(1, 2)  # Explicitly satisfies 0<c<1.
        # (1+c*x) * (1-x^2) * x*(1-x^2).
        coefficients = {1: Fraction(1), 2: c, 3: Fraction(-2), 4: -2 * c, 5: Fraction(1), 6: c}
        exact = sum((coefficient * Fraction(2, degree + 1) if degree % 2 == 0 else Fraction(0))
                    for degree, coefficient in coefficients.items())
        # Endpoints vanish; the two interior nodes are +/-1/sqrt(5),
        # each of weight 5/6. Odd contributions cancel exactly.
        quadrature = Fraction(5, 3) * sum(coefficient * Fraction(1, 5) ** (degree // 2)
                                        for degree, coefficient in coefficients.items() if degree % 2 == 0)
        self.assertEqual(exact, Fraction(16, 105) * c)
        self.assertEqual(quadrature, Fraction(16, 75) * c)
        self.assertEqual(abs(quadrature - exact), Fraction(32, 525) * c)


if __name__ == "__main__":
    unittest.main(verbosity=2)
