import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Data.Real.Sqrt
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FunProp

noncomputable section
namespace LegendreAudit
open scoped Interval

def massIntegrand (c x : ℝ) : ℝ := (1 + c * x) * (1 - x ^ 2) * (x * (1 - x ^ 2))
def gll3 (f : ℝ → ℝ) : ℝ :=
  f (-1) / 6 + (5 / 6) * f (-Real.sqrt (1 / 5)) +
    (5 / 6) * f (Real.sqrt (1 / 5)) + f 1 / 6

theorem mass_polynomial (c x : ℝ) :
    massIntegrand c x = x - 2 * x ^ 3 + x ^ 5 + c * x ^ 2 - 2 * c * x ^ 4 + c * x ^ 6 := by
  unfold massIntegrand
  ring

theorem gll3_mass (c : ℝ) : gll3 (massIntegrand c) = 16 * c / 75 := by
  have h₂ : (Real.sqrt (1 / 5 : ℝ)) ^ 2 = 1 / 5 := Real.sq_sqrt (by norm_num)
  have h₄ : (Real.sqrt (1 / 5 : ℝ)) ^ 4 = 1 / 25 := by
    calc
      _ = ((Real.sqrt (1 / 5 : ℝ)) ^ 2) ^ 2 := by ring
      _ = _ := by rw [h₂]; norm_num
  have h₆ : (Real.sqrt (1 / 5 : ℝ)) ^ 6 = 1 / 125 := by
    calc
      _ = ((Real.sqrt (1 / 5 : ℝ)) ^ 2) ^ 3 := by ring
      _ = _ := by rw [h₂]; norm_num
  unfold gll3 massIntegrand
  ring_nf
  rw [h₂, h₄, h₆]
  ring

def massPrimitive (c x : ℝ) : ℝ :=
  x ^ 2 / 2 - x ^ 4 / 2 + x ^ 6 / 6 + c * x ^ 3 / 3 - 2 * c * x ^ 5 / 5 + c * x ^ 7 / 7

theorem mass_hasDerivAt (c x : ℝ) :
    HasDerivAt (massPrimitive c) (massIntegrand c x) x := by
  have h₂ := (hasDerivAt_pow 2 x).div_const (2 : ℝ)
  have h₄ := (hasDerivAt_pow 4 x).div_const (2 : ℝ)
  have h₆ := (hasDerivAt_pow 6 x).div_const (6 : ℝ)
  have h₃ := ((hasDerivAt_pow 3 x).const_mul c).div_const (3 : ℝ)
  have h₅ := ((hasDerivAt_pow 5 x).const_mul (2 * c)).div_const (5 : ℝ)
  have h₇ := ((hasDerivAt_pow 7 x).const_mul c).div_const (7 : ℝ)
  convert (((((h₂.sub h₄).add h₆).add h₃).sub h₅).add h₇) using 1 <;>
    dsimp [massPrimitive, massIntegrand] <;> ring

-- Exact real integral; its statement is unchanged from the combined draft.
theorem mass_integral (c : ℝ) :
    (∫ x in (-1 : ℝ)..1, massIntegrand c x) = 16 * c / 105 := by
  have hc : Continuous (massIntegrand c) := by unfold massIntegrand; fun_prop
  calc
    (∫ x in (-1 : ℝ)..1, massIntegrand c x) = massPrimitive c 1 - massPrimitive c (-1) :=
      intervalIntegral.integral_eq_sub_of_hasDerivAt (fun x _ => mass_hasDerivAt c x)
        (hc.intervalIntegrable (-1) 1)
    _ = _ := by norm_num [massPrimitive] <;> ring

theorem positive_mass_coefficient (c x : ℝ) (hc0 : 0 < c) (hc1 : c < 1)
    (hx0 : -1 ≤ x) (hx1 : x ≤ 1) : 0 < 1 + c * x := by
  nlinarith [mul_nonneg (le_of_lt hc0) (show 0 ≤ x + 1 by linarith)]

theorem gll3_variable_coefficient_counterexample (c : ℝ) (hc0 : 0 < c) (hc1 : c < 1) :
    |gll3 (massIntegrand c) - (∫ x in (-1 : ℝ)..1, massIntegrand c x)| = 32 * c / 525 ∧
      gll3 (massIntegrand c) ≠ (∫ x in (-1 : ℝ)..1, massIntegrand c x) := by
  rw [gll3_mass, mass_integral]
  constructor
  · rw [abs_of_pos (by linarith : 0 < 16 * c / 75 - 16 * c / 105)]
    ring
  · intro h
    linarith


end LegendreAudit
