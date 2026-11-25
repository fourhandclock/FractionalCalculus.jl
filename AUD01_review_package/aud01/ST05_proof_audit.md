# Mathematical proof audit through ST-05

Audit of `legendre_spectral_verification_notes_st05.tex` (Sections 4–13), the four standalone proof sections, and the local source paper `YS_SS_PD_NM_25_Calcolo.pdf`. The source manuscript is unchanged. This is a fresh internal mathematical review, not external peer review or Lean certification. No production code, historical evidence, or GitHub state was changed.

## Verdicts

| Result | Review outcome |
|---|---|
| VQ-01 | Valid sharp uniform quadrature order for Eq. (6) as printed, under its stated smoothness assumptions. |
| CF-02 | Valid corrected step-dependent interpolation coefficients and exact sign/index counterexamples. |
| ST-03 | Valid counterexample to the signed-history inference, not independently a counterexample to an evolution theorem. |
| OB-03 | Valid startup Caputo operator counterexample. The combined residual example is forced, and its forcing is not classically smooth to arbitrary order at zero. |
| OB-04 | Valid all-degree GLL exactness counterexample. Does not refute a spatial error rate. |
| SP-01 | Ritz residual identity and fixed-grid estimate hold under the stated stronger product regularity and consistent forcing. L1 block comparison holds. |
| SP-02 | Convolution, positive-real symbol, weighted Green bound and finite-time block argument check out; applies to uniform grids and fixed fractional order. |
| TM-01 | Smooth forced sharpness proof and initial-layer bound check out. Qualify the claim about the literal homogeneous Theorem 3.2; see extension below. |
| ST-05 | Endpoint, smoothing, order-continuity, regularity and all-fine-grid steps check out. L1 conclusion is independent of SP-02; L1-2 refers to interpolation-defined rule. |

## Main scope correction (TM-01)

Source paper pp. 5–6 explicitly introduces temporal schemes with f=0. Theorem 3.2 (p. 16, Eq. 42) names problems (19) and (37), while describing the exact solution of (1). The original TM-01 smooth flat manufactured amplitude has nonzero forcing. Its lower bound establishes failure of the claimed rate for the consistently forced extension, not automatically for every interpretation of the strictly homogeneous theorem. The manuscript should explicitly state this distinction. OB-03 already notes its forced scope; additionally, its manufactured forcing includes t^(2-alpha), so it is not C^infinity at zero even though the amplitude is polynomial. Its Caputo operator counterexample is unaffected.

### Homogeneous extension (new argument)

Fix alpha=3/4, beta=1/2, K=lambda=1, T=2^(-10), sigma=pi^2/4. Use the normalized Dirichlet eigenfunction cos(pi x/2) with initial amplitude a(0)=1 and f=0. The scalar integral equation is a=1+Va with V=-I^alpha(sigma I+J_beta). In the unweighted supremum norm,

    ||V|| <= T^alpha/Gamma(1+alpha) * (sigma+2 sqrt(T)) < 1/4.

Indeed T^alpha<1/128, Gamma(7/4)>4/21 (integrate on [0,1], using e<3), sigma<3, and 2 sqrt(T)=1/16. Thus ||a-1||<=1/3 and a(t)>=2/3. The constant-coefficient special case of ST-05's Neumann-series regularity argument gives |a^(j)(t)|<=C t^(alpha-j), j=1,2, and alpha-Holder continuity. All parameters are fixed independently of the mesh.

For the memory quadrature, freeze the amplitude at the left endpoint of each old panel. The resulting difference in exact and numerical integrals is bounded by C tau^alpha times their uniformly bounded total kernel mass. Each constant-panel trapezoid defect is tau^(1-beta)c_(beta,r), where c_(beta,r)>0 and c_(beta,r)=O(r^(-beta-2)), as in VQ-01. Replacing the frozen amplitude by a(t_n) changes the sum by at most C tau^(1-beta+alpha) sum_(r>=2) r^alpha c_(beta,r), which is finite. The last panel is exact for constants and its remainder is O(tau^(1-beta+alpha)). Hence, uniformly in n,

    Q_tau^n[a]-J[a](t_n) = tau^(1-beta) C_(beta,n) a(t_n) + O(tau^alpha).

As alpha>1-beta, the remainder is little-o(tau^(1-beta)). TM-01's initial-layer Caputo bound with gamma=alpha gives |r_D^n|<=C(n^(-1-alpha)+n^(alpha-2)), so tau sum |r_D^n|=O(tau). Therefore

    tau^(-(1-beta)) tau sum_n r^n -> C_beta integral_0^T a(t)dt > 0.

The same discrete summation-by-parts estimate as TM-01 holds on general fixed T: for L1 the derivative contribution is at most T^(1-alpha)E/Gamma(2-alpha); for L1-2 it is at most three times this, with E=max|e^n| and e^0=0. The diffusion and memory contributions are bounded by T(sigma+W)E. Consequently E>=c tau^(1-beta). TM-01's initial-layer upper bound yields E<=C(tau^alpha+tau^(1-beta)). Thus the actual homogeneous maximum weighted solution error is Theta(tau^1/2) for both interpolation-defined schemes (L1 and L1-2), and the first-step error O(tau^alpha) cannot account for the lower bound. This is an analytical extension; no new trajectory simulation or formal certificate is claimed.

This resolves the forcing objection for ordinary initially singular homogeneous solutions. If the convergence theorem is interpreted with additional bounded classical time-derivative hypotheses at t=0, this homogeneous example need not satisfy those stronger hypotheses. The original flat forced example covers smooth solutions of the consistently forced scheme. Do not combine the two into a claim that one example satisfies both sets of assumptions.

## SP-02 detailed audit

- Corrected stationary increment coefficients a_r=b_r+c_r-c_(r-1), c_(-1)=0, require subtracting c_(n-1)Delta u^1. The first step remains L1. The generating-function initial term a_(n-1)u^0 has the correct sign and index.
- The positive Laplace measure and 0<=q<=1/2 follow from the defining panel moments. Exact expansion of the real-part numerator on the unit circle gives (1-cos theta)[1+rho+2q(rho-cos theta)]. The bracket is >=2rho. For each fixed x>0, the integrand is analytic across the closed unit disk, so the harmonic minimum principle is applicable before integrating.
- The split x~|1-z| in the positive measure gives |B|+|C|<=C|1-z|^(alpha-1), the analogous derivative bound, and Re B>=c|1-z|^(alpha-1). Re((1-z)C)>=0 prevents cancellation in the lower bound. Therefore |delta| is comparable to |1-z|^alpha, with |delta'|<=C|1-z|^(alpha-1).
- Spectral calculus uses |delta+y| >= (|delta|+y)/sqrt(2), y>=0. The weighted resolvent and derivative estimates are uniform in the spectrum. Cauchy coefficient extraction at r=exp(-1/k), followed by integration by parts, gives the claimed (k+1)^(alpha-1) Green bound. The integral of (k^(-1)+|theta|)^(-1-alpha) is O(k^alpha); division by k supplies the required power.
- The true first-step energy inequality controls Delta u^1 without requiring initial spatial energy. The initial-data convolution is bounded by the discrete beta-type sum, and current-block memory contributions can be absorbed. The number of blocks is uniform in tau. No appeal to Theorem 3.1 or positivity of the signed history is made.
- Limitations: fixed alpha; uniform time mesh; bounded positive memory multiplier; weighted, not unweighted H1, norm. Constants may depend on T, alpha and the kernel bound. No graded-grid or alpha-robust theorem follows.

## SP-01 and OB-04

The all-degree counterexample reduces to the leading coefficient of H_M=(1-x^2)(P_M')^2, which vanishes on GLL nodes. Its exact integral is 2M(M+1)/(2M+1), giving the stated positive defect. The Ritz projection cancels diffusion exactly, not the mass quadrature. The residual uses the H^m regularity of coefficient-weighted histories and forcing, as required. The H^1 embedding controls the nodal approximation error in 1D. The fixed-grid induction uses absolute history coefficients and is finite, and the L1 block argument uses positivity of L1 coefficients only. SP-02 closes the L1-2 propagation under the same regularity assumptions. Do not claim exact recovery of the original theorem's hypotheses, arbitrary dimension, or a timestep-uniform ordinary H1 estimate. A joint limit must control S, F and A_tau or enforce a compatible refinement relation.

## ST-05 detailed audit

The critically damped initial interval gives y(t*)=exp(-1)/gamma and a(t*)=0. At quarter-period in the second interval the derivative is -(16+1/16)exp(-1-pi/32)<-4. The switched propagator is bounded by 17 from the constant-coefficient energy on each interval. The logistic-tail L1 perturbation is <512/10^6; the relative variation-of-constants bound is 17^2 d/(1-17d)<1/4. This gives the smooth endpoint amplitude <-15/4. The weighted Volterra operator contraction is (3+800/64)/64=31/128<1/4. The kernel order derivative bounds and perturbation constant 720000 exp(256) are conservative but sufficient: epsilon=2^(-600) yields an error below 2^(-68). The exact pair must not be rounded into a double-precision endpoint. The differentiated Neumann series is justified by fixed-simplex scaling and factorial/gamma decay, giving the initial-layer derivative bounds. The L1 inverse convolution is positive, bounded by one, and its partial sums are <=k^alpha/(1-alpha). Together with the summable Caputo residual this supplies all-fine-grid convergence without SP-02. L1-2 uses SP-02/TM-01. Nearest-grid-point convergence transfers the strict continuous amplification to every sufficiently fine grid. The L1 counterexample is enough to refute the claimed fine-grid contractivity; no need to resolve the inconsistent literal L1-2 collected recurrence first. This does not disprove stability with a larger constant or claim a result for constant/nonincreasing K. The original Theorem 3.1 wording on p. 15 is slightly awkward ('there exists one Delta t>0'); the result addresses its stated sufficiently-large-number-of-partitions interpretation.

## Executed audit checks

Exact symbolic expansion of the SP-02 real-part numerator; exact rational inequalities for ST-05's smoothing and order perturbation constants and the new homogeneous small-time contraction; exact finite summation-by-parts coefficient checks for N=2,...,15. These checks supplement, but do not replace, the analytical derivations. The prior numerical suites and Lean proofs were not rerun. No claim of independent human review or formalization of SP-01 through ST-05.

## Before publication or merge

1. Add the TM-01 scope correction and homogeneous extension to a new manuscript revision; preserve the original ST-05 snapshot.
2. Make the weighted norm, forcing convention, uniform-grid scope, and coefficient/product regularity assumptions explicit in all summary tables.
3. Obtain a truly independent review of SP-02's complex-analysis estimates, TM-01's initial-layer bound, and ST-05's regularity and convergence transfer.
4. Formalize bounded algebraic identities, rational inequalities, finite summation identities and explicit oscillator algebra in Lean as tractable targets. Do not claim Lean proves the entire PDE theorem without a complete formalization.
5. Only then integrate the new research into a dedicated branch, preserving prior numerical evidence and distinguishing any new executed tests from historical logs.
