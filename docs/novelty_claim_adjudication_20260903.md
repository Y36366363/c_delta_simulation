# Adjudication of the three-part novelty claim (2026-09-03)

## Decision

The three-part package is now sufficiently coherent and supported to serve as
the methodological contribution of the Yao--Hoorn paper, provided that it is
phrased as a **problem-specific contribution** rather than a priority claim
over functional delta methods, robust correlation, or weak-identification
diagnostics generally:

1. complete inference for a generated robust-reference profile correlation;
2. finite-sample distortion caused by nonlocal reference switching in a
   studied near-degenerate construction; and
3. \(I_n=\sqrt n\,\sigma_{\min}(J)\) as a dimensionless first-order organizer
   of that transition, with higher-order family residuals left explicit.

This judgment is stronger than saying that the three ideas are individually
new. They are not. Generated-regressor influence corrections are established
in general semiparametric theory; robust MAD/median correlations predate this
project; Huber-root structure and singular-Jacobian identification diagnostics
also have their own literatures. The defensible novelty lies in the particular
estimand, the full nuisance path required by it, the isolated switching
mechanism, and the linked diagnostic/evidence package.

## 1. Complete generated-profile inference

The primary estimand is

\[
\rho_P=\operatorname{Corr}(|X-T_X|,|Y-T_Y|),
\]

where each \(T\) is a median/MAD-scaled Huber functional. The phrase
"complete inference" means that the influence expansion includes all of the
following:

- the joint contribution of \(E(ab),E(a),E(b),E(a^2),E(b^2)\);
- the covariance created by observing \((X,Y)\) as intact pairs;
- both fitted Huber-location paths; and
- the indirect median/MAD contribution to each Huber location.

The previous distribution-level finite-difference audit concentrated on the
secondary \(C\) scale. Today's targeted calculation closes that alignment gap
for the primary \(\rho_P\). Under one fixed regular correlated-lognormal law,
four smooth contamination directions were evaluated at
\(\epsilon=10^{-6},10^{-5},10^{-4}\). At \(10^{-6}\), the maximum scaled
analytic-versus-numerical error was

\[
1.58\times 10^{-5}.
\]

The maximum fitted-reference component was \(0.314\), and the maximum indirect
MAD component was \(0.0587\). Thus the agreement is not produced by choosing a
case in which the nuisance path vanishes. For every contamination direction,
the error decreases approximately linearly as \(\epsilon\downarrow0\), as a
first-order derivative check should.

The frozen regular calibration remains compatible with the theorem: at
\(n=640\), both the dependent-normal profile null and independent-\(t_5\) null
have Wilson intervals containing 0.05, and the largest deviation of the
studentized standard deviation from one is 0.0366. The strong-skew cell still
rejects at 0.082 at \(n=2560\), preserving the essential limitation:
**pointwise, not uniform**.

The external theory boundary matters. Hahn and Ridder's generated-regressor
work explicitly shows that first-stage estimation can contribute to an
influence function. Therefore the generic idea of propagating nuisance
estimation is not new. Our narrower contribution is the complete derivation
for this generated robust-reference profile estimand, with its exact
median/MAD/Huber and five-moment structure.

## 2. Reference-switching distortion

The mechanism case is supported by three logically distinct interventions:

1. On the same severe near-degenerate samples, fixing the population symmetry
   reference reduces rejection by at least 0.491 across \(n=80,640\).
2. On the diffuse control path, the largest refit-versus-fixed difference is
   only 0.018.
3. Exact sign balance reduces rejection by at least 0.475, while the separate
   sign-coupling experiment produces a monotone fitted-centre/effect gradient.

Together these contrasts rule out a simple explanation based only on the
fixed radial profiles or a generic defect of the test statistic. They isolate
sample sign fluctuations, nonlocal movement of the fitted reference, and the
resulting common profile distortion in the studied construction.

This is probably the most distinctive part of the paper. Nevertheless, its
formal status remains mixed: the two-mode limit is an exact proposition, while
the broader finite-sample phenomenon is supported empirically. The correct
statement is that near-degenerate robust-reference fitting **can cause, not
always causes**, severe distortion. Clark's analysis of Huber M-estimator
structure and uniqueness confirms that root geometry is a classical topic; it
does not already establish this profile-correlation switching mechanism.

## 3. The conditioning diagnostic

The first-order expansion implies nuisance amplification of order

\[
\frac{1}{\sqrt n\,\sigma_{\min}(J)}=\frac{1}{I_n}.
\]

The standardized Jacobian and \(I_n\) are positively affine invariant. In the
frozen bridge evidence, a model based only on \(\log I_n\) improves pooled
leave-one-family-out MAE by 74.7% relative to an intercept-only baseline. The
stricter cross-size and held-conditioning-level validations improve MAE by at
least 72.2%. In the prospective hyperexponential family, the rank correlation
between \(I_n\) and rejection is \(-0.943\).

The same prospective experiment also prevents overclaiming: every old-family
prediction is too high, by 0.019 to 0.112. Hence \(I_n\) transports the coarse
ordering better than the level. General weak-identification work already uses
near-singular Jacobians to detect identification failure. The paper-specific
advance is the standardized, dimensionless \(I_n\) construction and its use to
organize this robust-reference profile transition. It remains a **first-order
organizer, not a universal cutoff**.

## Revised novelty boundaries after literature cross-check

The previous Stavig audit remains correct, but today's wider check adds an
important comparator. The MAD/median principal-variable correlations studied
by Pasman--Shevlyakov and Shevlyakov--Vilchevski already combine robust
marginal standardization with robust scales of signed sums and differences.
They target robust signed raw-value correlation, not correlation between
unsigned marginal radii. Consequently:

- Stavig does not preempt the estimand, but prevents an "absolute-deviation
  correlation is new" claim.
- MAD/median correlation does not preempt the estimand, but prevents a
  "median/MAD makes the correlation new" claim.
- General generated-regressor theory prevents claiming a new generic IF
  principle.
- General weak-identification theory prevents claiming that singular values
  are a new universal diagnostic principle.

The literature audit is finite and does not establish global priority. It
does support a careful claim of a new problem-specific theory-and-mechanism
package, subject to ordinary peer review and a final systematic reference
check.

## What can now be written

> We develop inference for a robust-reference profile correlation whose
> profiles are generated by median/MAD-scaled Huber functionals. Under fixed
> regular IID laws, a complete influence-function expansion yields pointwise
> plug-in Wald inference. In a near-degenerate construction, nonlocal
> reference switching can create severe finite-sample distortion. The
> dimensionless index \(I_n=\sqrt n\,\sigma_{\min}(J)\) organizes much of this
> transition at first order, although systematic family residuals show that it
> is not a universal cutoff.

## What still cannot be written

- that \(\rho_P\) is the first absolute-deviation or robust correlation;
- that the functional delta method or generated-nuisance correction is new;
- that every near-degenerate or multimodal reference fit fails;
- that \(I_n\) is necessary and sufficient, calibrated, or operational;
- that robust marginal references make \(\rho_P\) a globally robust
  correlation; or
- that the selected simulations establish uniform finite-sample validity.

The four permanent boundaries remain: **pointwise, not uniform**; **can cause,
not always causes**; **first-order organizer, not a universal cutoff**; and
**robust reference, not a globally robust correlation**.

## Immediate development decision

No further general distribution grid is warranted. The next work should be
manuscript integration: place the new \(\rho_P\) derivative check in the
appendix, compress the three interventions into the mechanism section, and
present the cross-validation plus prospective miss together so that the
diagnostic and its limitation cannot be separated. Local-to-degeneracy theory
is a possible later strengthening, not a prerequisite for drafting the current
three-claim paper unless Professor Hoorn requests it.

## Sources used for the boundary judgment

- Stavig (1982), *The Absolute Deviation Correlation Coefficient*:
  <https://doi.org/10.2466/pms.1982.54.1.164>
- Shevlyakov and Vilchevski (2002), minimax robust correlation and its median
  limit: <https://doi.org/10.1016/S0167-7152(02)00058-5>
- Shevlyakov and Oja (2016), *Robust Correlation: Theory and Applications*:
  <https://doi.org/10.1002/9781119264507>
- Hahn and Ridder (2013), generated-regressor contributions to influence
  functions: <https://doi.org/10.3982/ECTA9609>
- Clark (1985), Huber M-estimator structure and uniqueness:
  <https://doi.org/10.1137/0906017>
- Andrews and Mikusheva, identification failure and asymptotically singular
  Jacobians: <https://arxiv.org/abs/1907.13093>
