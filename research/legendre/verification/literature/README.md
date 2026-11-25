# Literature and mathematical context

The original method combines three numerical ingredients: L1/L1-2 approximation of a Caputo derivative, weakly singular Volterra quadrature, and Legendre spectral discretization. The present audit asks whether their stated coefficient identities and consistency estimates support the combined stability and convergence analysis.

## Original method and related analyses

Sabawi et al. is the source of the claims being tested. Gao, Sun, and Zhang provide background on L1-2 differentiation. The Ramezani–Mokhtari–Haase analysis is relevant to the treatment of exceptional L-type coefficients, but concerns subdiffusion without the additional Volterra term in this project. A stability argument for that model cannot be imported as a proof for the combined scheme.

The independent verification notes report an energy/discrete-Grönwall treatment in the ETNA article. Its precise theorem locators and interpretation have **not been checked against the primary text**. The distinction between a reported related result and independently verified source content is retained below.

| Source | Provenance and verification | What may be used here |
| --- | --- | --- |
| Y. A. Sabawi, S. Santra, P. Das, N. A. Mohammad, *H¹ stability and convergence analysis of the L1/L1-2 Legendre spectral method for non-local weakly singular integro-PDEs*, Calcolo **62**, 42 (2025). [DOI](https://doi.org/10.1007/s10092-025-00671-y) | [Local full paper](../../../../YS_SS_PD_NM_25_Calcolo.pdf); relevant equations/theorems checked; [locator table](../PROVENANCE.md#checked-source-locators) | Published claims being audited, explicitly distinct from our derivations |
| M. Ramezani, R. Mokhtari, G. Haase, *Analysis of stability and convergence for L-type formulas combined with a spatial finite element method for solving subdiffusion problems*, Electronic Transactions on Numerical Analysis **55** (2022), 568–584. [DOI](https://doi.org/10.1553/etna_vol55s568) | Supplied notes §6.4 reports Section 3.2, Theorems 3.4–3.6; primary text **not supplied or found locally**. Those locators and the energy/discrete-Grönwall interpretation require source verification | Preserve the reported exceptional-coefficient discussion as source-reported related work. Its subdiffusion model has no additional Sabawi Volterra term; it does not prove Theorem 3.1 for the present model |
| G. Gao, Z. Sun, H. Zhang, *A new fractional numerical differentiation formula to approximate the Caputo fractional derivative and its applications*, Journal of Computational Physics **259** (2014), 33–50. [DOI](https://doi.org/10.1016/j.jcp.2013.11.017) | Already cited in `research/THEORY.md`; bibliographic identity matches Sabawi reference [52], p.45. The independent article itself was not checked here | Original L1-2 background; do not attribute a specific stability theorem or additional assumptions to it without checking its text |
| Hardik Bisht, *Verification notes on the L1/L1-2 Legendre spectral method*, November 2026 | Supplied [11-page PDF](../sources/legendre_spectral_verification_notes_st03.pdf), retained byte-for-byte | Independent derivations VQ-01, CF-02, ST-03; provisional observations; historical numerical reports; research protocol |

## Independent findings and possible extensions

The [accepted AUD-01 manuscript](../reviews/AUD-01/revision-01/mathematical-verification-aud01-r1.tex) contains the earlier investigations and the OB-03/OB-04, SP-01/SP-02, TM-01, ST-05 and AUD-01 analyses. These are our independent derivations, not independently published confirmation. The [review](../reviews/AUD-01/revision-01/REVIEW.md) records their assumptions and qualifications. The [original ST-04 source](../sources/legendre_spectral_verification_notes_st04.tex) and [supplied PDF](../sources/legendre_spectral_verification_notes_st04.pdf) extend the earlier notes; their references do not independently verify the cited articles.

Product integration interpolates the smooth function while integrating the singular weight exactly. Manuscript §4.6 derives a candidate operator-level $O(\tau^2)$ bound under its stated smoothness assumptions. It is a different quadrature from paper Eq. (6), and appears as a control in the supplied ST-04 diagnostic. No replacement production solver is introduced. The manuscript gives conditional smooth-data propagation using positive bounded memory weights; this is separate from validating the published quadrature or its proof.

Discrete fractional or memory Grönwall inequalities may help control accumulated history once an appropriate combined estimate has been derived. They are a possible route, rather than an existing justification for the signed-history contraction step. The original paper's references [46]–[48] are likewise not treated as independent verification of its Eq. (8).

## Source coverage

The bibliography preserves the supplied references and their existing source-verification qualifications. No new literature search is represented here. Links identify cited works; checked source content is described in the table. Missing primary texts should be consulted before attributing precise theorems, coefficient assumptions, or independent confirmation to them.

The spatial analysis cites Canuto and Quarteroni, *Approximation results for orthogonal polynomials in Sobolev spaces*, Math. Comp. 38 (1982), 67–86, Theorem 2.3, as recorded in manuscript §10.2. That precise primary-source locator has not been independently checked. It remains a source-verification qualification, rather than a Lean dependency or a claim of independent confirmation. No new literature was acquired for this integration.
