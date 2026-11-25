import Mathlib.Tactic

/-!
AUD-01 draft: algebraic and rational proof targets only.
NOT compiled in the preparation environment. Do not count as certificates
until checked with the pinned Lean/mathlib project and audited for axioms.
-/
namespace LegendreAudit.AUD01

theorem symbol_numerator (x y rho q : ℝ) (h : y^2 = 1 - x^2) :
    ((1-x) + q*((1-x)^2-y^2))*(1-rho*x) +
      (y+2*q*(1-x)*y)*(rho*y) =
      (1-x)*(1+rho+2*q*(rho-x)) := by
  calc
    _ = (1-x)*(1+rho+2*q*(rho-x)) +
          (y^2 - (1-x^2)) * (-q*rho*x+2*q*rho-q+rho) := by ring
    _ = _ := by rw [h]; ring

theorem symbol_bracket (rho q x : ℝ) (hr : 0 ≤ rho) (hr' : rho ≤ 1)
    (hq : 0 ≤ q) (hq' : q ≤ 1/2) (hx : x ≤ 1) :
    2*rho ≤ 1+rho+2*q*(rho-x) := by
  have h1 : 0 ≤ (1-2*q)*(1-rho) :=
    mul_nonneg (by linarith) (by linarith)
  have h2 : 0 ≤ 2*q*(1-x) :=
    mul_nonneg (by linarith) (by linarith)
  calc
    2*rho ≤ 2*rho+(1-2*q)*(1-rho)+2*q*(1-x) := by linarith
    _ = _ := by ring

theorem smoothing_denominator : (0 : ℚ) < 1-17*(512/1000000) := by norm_num

theorem smoothing_amplitude : (17 : ℚ)/(1-17*(512/1000000)) < 18 := by norm_num

theorem smoothing_difference :
    (17 : ℚ)^2*(512/1000000)/(1-17*(512/1000000)) < 1/4 := by norm_num

theorem weighted_contraction : ((3 : ℚ)+800/64)/64 < 1/4 := by norm_num

theorem homogeneous_contraction : (1 : ℚ)/128*(21/4)*(3+1/16) < 1/4 := by norm_num

theorem fractional_parameter_bound :
    (720000 : ℚ)*2^512*(1/2^600) < 1/2^68 := by norm_num

theorem fractional_parameter_admissibility :
    (0 : ℚ) < 1/2^600 ∧ (1 : ℚ)/2^600 ≤ 1-1/2^600 ∧ (1 : ℚ)-1/2^600 < 1 := by
  norm_num

end LegendreAudit.AUD01
