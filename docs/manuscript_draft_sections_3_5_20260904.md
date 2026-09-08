# Trustworthy Inference for Robust-Reference Divergence Profiles

## Regularity, Reference Instability, and Nuisance Conditioning

Working manuscript draft, Sections 3--5  
Date: 2026-09-04; mechanism and scope review: 2026-09-07

> Editorial note: this text continues
> `manuscript_draft_sections_1_2_20260830.md`. It integrates only frozen theory
> and claim-directed evidence. Numerical tables remain assigned to Section 6;
> the values cited here are signposts for those displays, not a new simulation
> grid.

## 3. Estimation and inference under regular identification

### 3.1 The generated-reference problem

Although \(\widehat\rho_P\) is computed as a Pearson correlation after the two
fitted radius vectors have been formed, its sampling uncertainty is not the
usual fixed-vector correlation uncertainty. Every fitted radius depends on a
marginal reference estimated from the same sample. A perturbation of one
paired observation can change its own two radii, the five empirical profile
moments, both marginal medians and MADs, and all radii through the two fitted
Huber locations. Valid first-order inference must propagate these paths
jointly while retaining \((X_i,Y_i)\) as the independent sampling unit.

For a generic margin \(W\), retain the notation

\[
m=\operatorname{Med}(W),\qquad
d=\operatorname{Med}|W-m|,\qquad s=kd,
\]

and let \(T\) solve \(E\{\psi_c((W-T)/s)\}=0\). Put

\[
A=P\{|(W-T)/s|<c\},\qquad
B=E\left[\frac{W-T}{s}1\{|(W-T)/s|<c\}\right].
\]

At a regular continuous marginal law, the nuisance influence functions are

\[
IF_m(w)=\frac{1/2-1(w\le m)}{f(m)},
\]

\[
IF_d(w)=
\frac{1/2-1(|w-m|\le d)
-\{f(m+d)-f(m-d)\}IF_m(w)}
{f(m+d)+f(m-d)},
\]

and

\[
IF_T(w)=\frac{s}{A}\psi_c\left(\frac{w-T}{s}\right)
-\frac{B}{A}kIF_d(w).
\]

The last term is the indirect MAD-to-Huber path. It disappears for a
symmetric law with \(B=0\), but not generally.

### 3.2 Complete profile-correlation influence function

Let \(a=|X-T_X|\), \(b=|Y-T_Y|\), and order the profile moments as

\[
M=(\nu,\mu_a,\mu_b,q_a,q_b)^\top.
\]

Define

\[
g_X=E\{\operatorname{sign}(X-T_X)\},\qquad
h_X=E\{\operatorname{sign}(X-T_X)b\},
\]

with \(g_Y,h_Y\) defined analogously. The complete paired moment influences
include

\[
\begin{aligned}
IF_{\mu_a}(Z)
  &=a-\mu_a-g_XIF_{T_X}(X),\\
IF_{\mu_b}(Z)
  &=b-\mu_b-g_YIF_{T_Y}(Y),\\
IF_\nu(Z)
  &=ab-\nu-h_XIF_{T_X}(X)-h_YIF_{T_Y}(Y),\\
IF_{q_a}(Z)
  &=a^2-q_a-2E(X-T_X)IF_{T_X}(X),\\
IF_{q_b}(Z)
  &=b^2-q_b-2E(Y-T_Y)IF_{T_Y}(Y).
\end{aligned}
\]

Writing \(D=(v_av_b)^{1/2}\), the gradient of \(\rho_P\) with respect to
the ordered moment vector is

\[
\nabla\rho_P=
\left(
\frac1D,
-\frac{\mu_b}{D}+\rho_P\frac{\mu_a}{v_a},
-\frac{\mu_a}{D}+\rho_P\frac{\mu_b}{v_b},
-\frac{\rho_P}{2v_a},
-\frac{\rho_P}{2v_b}
\right)^\top.
\]

Hence

\[
IF_\rho(Z;P)=\nabla\rho_P^\top IF_M(Z;P).
\]

This is one influence value per observed pair. Its variance automatically
contains the direct cross-moment covariance, numerator--denominator
covariances, direct--reference covariances, and cross-margin dependence. It
must not be calculated by treating the two margins, or pairwise edges derived
from them, as independent observations.

### 3.3 Pointwise regular IID theorem

The main result uses five groups of conditions. The observed pairs are IID;
the marginal medians, MADs, and Huber roots are uniquely and regularly
identified; the profile means, profile variances, and target influence
variance are positive; the required profile moments are finite; and the
localized nuisance, density, moment, and influence-function plug-ins satisfy
the consistency and empirical-process conditions stated in Appendix A. For a
general nonzero \(\rho_P\), the marginal fourth-plus moments in Appendix A are
used. The weak-null test admits the relaxation described below.

**Theorem 1 (regular robust-reference profile inference).** Under the regular
IID conditions of Appendix A,

\[
\sqrt n(\widehat\rho_P-\rho_P)
=\frac1{\sqrt n}\sum_{i=1}^n IF_\rho(Z_i;P)+o_P(1)
\ \Rightarrow\ N(0,V_\rho),
\qquad
V_\rho=E\{IF_\rho(Z;P)^2\}.
\]

If \(\widehat{IF}_{\rho,i}\) substitutes consistent nuisance, density, and
moment estimates into the complete influence function, then

\[
\widehat V_\rho=
\frac1{n-1}\sum_{i=1}^n
(\widehat{IF}_{\rho,i}-\overline{\widehat{IF}}_\rho)^2
\ \longrightarrow_P\ V_\rho,
\]

and therefore

\[
\frac{\sqrt n(\widehat\rho_P-\rho_P)}{\sqrt{\widehat V_\rho}}
\Rightarrow N(0,1).
\]

Appendix A proves the result through the median and MAD derivatives, the
implicit Huber derivative, a joint five-moment expansion, stochastic
equicontinuity for the random nuisance substitution, the functional delta
method, plug-in \(L_2(P)\) consistency, and empirical second-moment
consistency. The result is pointwise at each fixed regular law; it does not
provide uniform control as the nuisance Jacobian approaches singularity.

Three corollaries clarify its scope. First, at \(H_0:\rho_P=0\), the gradient
coefficients on \(q_a\) and \(q_b\) vanish. The first-order null test therefore
does not require the general-confidence-interval fourth-moment condition.
Second, if \(X\) and \(Y\) are independent, the coefficients multiplying both
marginal reference influences cancel exactly. Independence is sufficient,
not necessary: cancellation also occurs in the symmetric shared-sign radial
weak-null calibration design used here. It does not hold at every dependent
weak null or at a general nonzero profile correlation. Third, the theorem
does not cover sequences satisfying
\(\sqrt n\,\sigma_{\min}\{J(P_n)\}=O(1)\); Sections 4 and 5 study that boundary.

### 3.4 Numerical derivative and calibration checks

The analytic expression was checked directly for the primary estimand, not
only for the secondary \(C\) scale. In one fixed regular correlated-lognormal
law, a fixed Gauss--Hermite discretization was used to evaluate contamination
derivatives along four directions. At contamination weight \(10^{-6}\), the largest scaled difference
between the analytic complete influence and the finite-difference derivative
was \(1.58\times10^{-5}\). The largest fitted-reference component was 0.314
and the largest indirect MAD component was 0.0587, so the check exercises the
nuisance path rather than relying on independence orthogonality. This is a
within-quadrature derivative check, not by itself a bound on integration error.
The 2026-09-07 independent split-integration check and active-nuisance coverage
study are reported in `docs/active_nuisance_validation_20260907.md`; the old
numerical source is retained for provenance, not treated as exact population
truth.

The theorem-aligned simulations are deliberately limited. At \(n=640\), a
normal-margin shared-sign profile weak null rejected in 0.044 of 1,000 repetitions and
an independent \(t_5\) null rejected in 0.059; both Wilson intervals contain
0.05, and their studentized standard deviations were 0.993 and 1.037. In the
strong-skew stress design, rejection decreased from 0.122 at \(n=640\) to
0.082 at \(n=2560\), but remained asymmetric. Fixing the population Huber
references did not improve that skew behavior. The evidence is consistent
with pointwise convergence and demonstrates why the paper does not claim
uniformly accurate moderate-sample Wald inference.

## 4. A constructive failure from unstable robust references

### 4.1 A separated-mode profile null

To isolate reference fitting from the intended profile target, let

\[
X=S\exp(\tau U),\qquad Y=S\exp(\tau V),
\]

where \(S\) is a common Rademacher sign and \(U,V\) are independent standard
normal variables independent of \(S\). At the symmetry reference zero,
\(|X|=\exp(\tau U)\) and \(|Y|=\exp(\tau V)\) are independent, so their
population profile correlation is zero. The common sign does not itself
create radial concordance at that fixed reference.

For every \(\tau>0\), this marginal law has \(m=T=0\), raw MAD \(d=1\),
and \(f(0)=0\). Its median is uniquely defined but nonregular: it fails the
positive-center-density assumption in Theorem 1. For the declared defaults,
the population Huber equation is not nearly flat at its reference. In fact,

\[
A=\Phi\{\log(ck)/\tau\},\qquad
\partial_T E\psi_c((X-T)/k)=-A/k,
\]

which is approximately \(-0.6745\) at \(\tau=0.10\). The instability must
therefore be described at the level of the complete fitted nuisance system,
not attributed to a weak population Huber root alone.

When the outer modes are concentrated, IID sign-count fluctuations can move
the sample median and its associated MAD nonlocally; the resulting fitted
scale changes the empirical Huber solution. Since the same \(S_i\) enters
both margins, their fitted-reference movements tend to align. They change
many radii simultaneously and can manufacture strong profile correlation
although the population fixed-reference radial target remains zero. At the
symmetric population law \(B=0\); this finite-sample propagation is not a
nonzero first-order MAD-to-Huber derivative at that law. The interventions
below support this nonlocal mechanism, not a regular IF expansion there.

The limiting geometry can be seen without asymptotics. If observations occupy
two radius levels, choosing the same reference mode in both margins makes the
two fitted binary profiles perfectly correlated; choosing opposite modes
makes them perfectly anticorrelated. This identity is conditional on imposed
nonzero reference offsets, not a theorem that the fitted algorithm selects
these offsets with any specified probability. At the exact symmetric binary
law with zero reference, the radii are constant and \(\rho_P\) is undefined.
The continuous positive-\(\tau\) construction supplies the nondegenerate
profile-null example; the binary geometry supplies only an algebraic
illustration of the potentially \(O(1)\) target response.

### 4.2 Paired mechanism interventions

The central comparison refits the robust references and then repeats the
analysis on exactly the same samples with the symmetry reference fixed at
zero. For \(\tau=0.10\), fitted-reference rejection was 0.777 at \(n=80\) and
0.541 at \(n=640\), compared with 0.054 and 0.050 under the fixed reference.
The paired reductions were 0.723 (MCSE 0.0145) and 0.491 (MCSE 0.0171). When
the radial log standard deviation increased to \(\tau=0.40\), the largest
absolute refit--fixed difference across the two sample sizes was only 0.018.
The contrast is therefore specific to the separated, weak-reference geometry
in this construction rather than a generic difference between fitted and
fixed profiles.

A second intervention removes the empirical sign-count fluctuation while
retaining the same bimodal radial construction. Under IID signs at
\(\tau=0.10\), rejection was 0.766 at \(n=80\) and 0.535 at \(n=640\). With
exactly balanced signs, it fell to 0.058 and 0.060, and the mean maximum
absolute fitted Huber centre fell from 0.491 to 0.0127 at \(n=80\) and from
0.239 to 0.00459 at \(n=640\). Forced balance is not a proposed correction;
it is a controlled intervention on the hypothesized switching trigger.

Finally, a coupling parameter \(q\) determines whether the second margin
inherits the first margin's sign or receives an independent sign, while the
fixed-reference radial profiles remain uncorrelated. At \(n=640\), the mean
refitted profile effect increased from 0.001 at \(q=0\) to 0.626 at \(q=1\),
and the mean fitted-centre product increased from -0.003 to 0.080. The fixed
zero-reference effect stayed within 0.002 of zero. The rejection curve need
not be pointwise monotone because effect size, switching probability, and
studentization all contribute, but the monotone centre/effect dose response
provides the predicted mechanism gradient.

### 4.3 Scope of the failure claim

The exact two-mode result is an imposed-reference algebraic identity about
idealized geometry, not a fitted-switching probability theorem. The rejection
rates and interventions are empirical evidence for a
continuous finite-sample construction. Together they establish that unstable
reference fitting **can cause** severe spurious profile correlation and
inferential distortion. They do not establish that every multimodal law,
every small central density, or every low-curvature Huber equation fails. Nor
do they establish fixed references, sign balancing, truncation, or bootstrap
as universal remedies. The problem is a failure of local approximation under
nonlocal nuisance movement, not evidence that the robust-reference estimand
is undefined in every difficult distribution.

## 5. Nuisance conditioning as a first-order diagnostic

### 5.1 Standardized nuisance Jacobian

For one margin, stack the median, MAD, and Huber equations in the parameter
\(\theta=(m,d,T)^\top\). After measuring all three parameter perturbations in
units of \(d\), their population Jacobian is

\[
J=
\begin{pmatrix}
df(m)&0&0\\
d\{f(m+d)-f(m-d)\}&d\{f(m+d)+f(m-d)\}&0\\
0&-B&-A/k
\end{pmatrix}.
\]

The first-order nuisance expansion is schematically

\[
\widehat\theta-\theta\approx-J^{-1}(P_n-P)g.
\]

Because \(\|J^{-1}\|_2=1/\sigma_{\min}(J)\), sampling noise in the least
identified standardized direction has a local linear amplification scale

\[
\frac{1}{\sqrt n\,\sigma_{\min}(J)}.
\]

This motivates

\[
I_n=\sqrt n\,\sigma_{\min}(J).
\]

The standardized construction matters. If \(W^*=a+bW\) with \(b>0\), then
the transformed median, MAD, and Huber reference change location and units,
but \(J^*=J\). Consequently \(I_n\) is dimensionless and positively affine
invariant. The corresponding statement would not hold for the unscaled
Jacobian. It does not make the index invariant to arbitrary rescaling of
the estimating equations; their stated normalization must remain fixed.
Nor is this linear amplification argument a uniform error bound along an
arbitrary degenerating sequence.

### 5.2 What the index explains

The bridge construction varies the amount of central probability connecting
two outer modes and evaluates several bridge shapes at two sample sizes. A
binomial logit using only \(\log I_n\) was trained on three bridge families and
used to predict the fourth. Across all 24 held-out cells, it improved weighted
mean absolute error by 74.7% and binomial log loss by 13.9% relative to an
intercept-only prediction; every fitted log-index slope was negative. More
demanding checks that held out an entire sample size or a conditioning level
improved MAE by 77.6% and 72.2%, respectively.

A hyperexponential bridge was then selected before its rejection experiments
were run. Across its six cells, the rank correlation between \(I_n\) and the
observed rejection rate was -0.943. Relative to the old-family intercept
baseline, the old-family index model improved MAE by 47.6% and log loss by
14.5%. These results support a coarse first-order organization of recovery,
not an exact response curve.

### 5.3 What the index does not explain

Every prospective hyperexponential prediction exceeded the observed rejection
rate, with absolute errors from 0.019 to 0.112. Earlier matched-J comparisons
also retained family-specific rejection differences. These are family
residuals unexplained by \(I_n\), not proof that all remaining differences
are higher order. Even equal \(J\) need not imply an equal first-order
stochastic law: with score covariance \(\Omega=\operatorname{Var}\{g(Z)\}\),
the local nuisance covariance is \(n^{-1}J^{-1}\Omega J^{-\top}\), and its
effect on the target also depends on the target's nuisance projection. Both
must be considered before claiming a matched complete first-order experiment.
Curvature, the distance of competing fitted-reference regions, tail behavior,
and nonlocal switching/studentization are additional plausible contributors,
not an established higher-order decomposition of the residual.

Accordingly, \(I_n\) is a **first-order organizer, not a universal cutoff**.
The current results do not calibrate a threshold, prove necessity or
sufficiency for failure, or authorize a data-dependent gate that suppresses
inference. Moreover, the present \(I_n\) values are population quantities
used to explain simulation regimes. A sample stability diagnostic would need
its own estimation error, operating rule, and prospective validation before
it could be recommended in applications.

### 5.4 Connection to the regular theorem

Sections 3--5 describe one coherent boundary rather than three unrelated
experiments. At any fixed regular law, \(\sigma_{\min}(J)>0\), so
\(I_n\to\infty\) and the pointwise expansion supports Wald inference. Along a
sequence for which \(I_n=O(1)\), the nuisance error need not remain local and
Theorem 1 makes no uniform claim. Section 4 demonstrates one way this loss of
locality can generate severe distortion. Section 5 shows that \(I_n\) orders
much of the transition while the family residual prevents reduction of the
whole phenomenon to a single scalar law.

This connection fixes the manuscript's inferential language: **pointwise,
not uniform**; near-degenerate fitting **can cause, not always causes** the
failure; \(I_n\) is a **first-order organizer, not a universal cutoff**; and
the procedure uses a **robust reference, not a globally robust correlation**.

## References introduced in Sections 3--5

- Forneron, J.-J. *Detecting Identification Failure in
  Moment Condition Models*. <https://arxiv.org/abs/1907.13093>
- Clark, D. I. (1985). *The Mathematical Structure of Huber's M-Estimator*.
  <https://doi.org/10.1137/0906017>
- Hahn, J., and Ridder, G. (2013). *Asymptotic Variance of Semiparametric
  Estimators With Generated Regressors*.
  <https://doi.org/10.3982/ECTA9609>
- Shevlyakov, G. L., and Vilchevski, N. O. (2002). *Minimax Variance
  Estimation of a Correlation Coefficient for Epsilon-Contaminated Bivariate
  Normal Distributions*.
  <https://doi.org/10.1016/S0167-7152(02)00058-5>
- Stavig, G. R. (1982). *The Absolute Deviation Correlation Coefficient*.
  <https://doi.org/10.2466/pms.1982.54.1.164>
