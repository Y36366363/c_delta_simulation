# Paper architecture and conceptual guide

Date: 2026-08-18

## Stage decision

The project is now in a **paper-definition and consolidation phase**.  New
simulations should be run only when they distinguish wording, assumptions, or
evidence for one of the three proposed main claims.  Unexplained anomalies are
recorded, but they no longer automatically generate a new branch of testing.

The most coherent current paper is not a universal comparison of profile,
Mantel, adaptive, and building-level procedures.  It is a focused paper about
when robust-reference paired-salience inference is regular, how it fails near
weak reference identification, and how the onset of failure can be organized
by the conditioning of the nuisance estimating system.

### Working one-sentence pitch

> Robust-reference paired-salience concordance has standard pointwise iid
> inference under regular nuisance identification, but near-degenerate
> median/MAD/Huber reference fitting can cause severe finite-sample distortion;
> a sample-scaled nuisance-Jacobian singular value explains much of this
> transition at first order while leaving identifiable higher-order family
> effects.

This wording deliberately says **pointwise**, **iid**, **much of**, and
**first order**.  Removing any of those qualifications would exceed the
current evidence.

## Proposed main claims and their evidence level

### Main Claim 1: regular iid theory

Let

\[
a_P(x)=|x-T_X(P_X)|,\qquad b_P(y)=|y-T_Y(P_Y)|,
\]

where each `T` is the Huber location fitted with a normal-consistent MAD
scale.  The robust c_delta functional is

\[
C(P)=\frac{E_P\{a_P(X)b_P(Y)\}}
{E_P\{a_P(X)\}E_P\{b_P(Y)\}}.
\]

Under the stated iid, continuity, uniqueness, positive-density,
nondegeneracy, and moment conditions, the complete functional delta method
gives

\[
\sqrt n\{C(P_n)-C(P)\}
=n^{-1/2}\sum_{i=1}^n IF_C(Z_i;P)+o_P(1),
\]

and hence pointwise asymptotic normality and consistent sandwich
studentization when the nuisance quantities are consistently estimated.

**Current status:** theorem-level statement with a complete influence formula,
distribution-level numerical derivative validation, and an auditable proof
route.  A publication proof must still spell out the tangent space and the
empirical remainder argument.  Fully recomputed studentized permutation under
a weak null is a theoretically motivated and empirically supported candidate,
not yet a uniform theorem in this project.

### Main Claim 2: finite-sample distortion near degeneracy

Continuous, true weak-null examples with separated sign modes and little
central radial variation show that estimated Huber/MAD references can switch
or drift enough to manufacture strong apparent profile concordance.  In the
tested paths, nominal 5% rejection reached roughly `.75-.95` in the most
severe cells and declined toward nominal as bridge mass or radial variation
increased.

**Current status:** reproducible constructive simulation evidence, supported
by the reference-fitting mechanism.  It is not a theorem that every
near-degenerate distribution is anti-conservative, nor that distortion must
have the same sign.

### Main Claim 3: first-order nuisance conditioning organizes the transition

For one margin, using nuisance perturbations scaled by the population MAD,
the median/MAD/Huber estimating system has Jacobian

\[
J=
\begin{pmatrix}
d f(m)&0&0\\
d\{f(m+d)-f(m-d)\}&d\{f(m+d)+f(m-d)\}&0\\
0&-B&-A/k
\end{pmatrix},
\]

where

\[
A=P(|U|<c),\qquad B=E\{U\,1(|U|<c)\},\qquad
U=(X-T)/(kd).
\]

The dimensionless identification index is

\[
I_n=\sqrt n\,\sigma_{\min}(J).
\]

Across 24 matched bridge cells, the risk-oriented Spearman correlation between
small `I_n` and rejection was `.971`; `log(I_n)` alone gave logit
`R-squared=.932`.  Adding the other first-order Jacobian components raised it
only to `.938`.

**Current status:** the Jacobian formula and its finite-difference check are
analytic/numerical facts; the choice of `I_n` follows naturally from the
linearized estimating equation; its observed predictive strength is
empirical.  There is no established universal cutoff, and `I_n>1` must not be
presented as a certificate of valid inference.

### Limitation: higher-order family effects remain

Matched families with nearly identical first-order Jacobians retained
different rejection rates in a 500-replication transition study
(`.232-.356`, homogeneity `p=.00013`, Cramer's `V=.101`).  First-order
conditioning therefore does not exhaust finite-sample behavior.

Plausible next layers are the curvature of the nuisance equations, the
second and higher moments of the complete nuisance influence vector,
empirical-process tail shape, and nonlocal median/MAD mode switching.  These
are a stated limitation and a targeted future-theory direction, not reasons
to start another broad simulation grid now.

## The ten concepts that must be explainable without code

### 1. What is the c_delta estimand?

For the current robust version, the estimand is `C(P)` above: normalized
cross-moment concordance between the **labelled observation-level radial
saliences** relative to fitted marginal Huber centres.  It is not a general
measure of independence and not a comparison of the entire pairwise geometry.

Writing

\[
\rho_P=\operatorname{Corr}\{a_P(X),b_P(Y)\},
\]

gives the identity

\[
C=1+\rho_P\,CV(a_P)CV(b_P).
\]

Thus `C=1` is the zero-covariance weak-null boundary, but `C-1` combines
salience correlation with marginal salience heterogeneity.  For fixed
marginal profiles, `C`, covariance, and Pearson profile correlation have the
same permutation ordering.  The paper must explicitly decide whether `C` or
`rho_P` is the primary scientific effect scale; that is a construct choice,
not a numerical choice.

### 2. How do the permutation null and weak null differ?

The **permutation null** is a distributional symmetry statement: conditional
on the observed marginal samples (or design strata), the pairing labels are
exchangeable under the declared permutation group.  Under that invariance, a
fully recomputed randomization test is exact in finite samples.

The **weak null** is only an effect restriction, such as

\[
H_P:\rho_P=0\quad\text{or equivalently}\quad C=1.
\]

It allows nonlinear dependence, heteroskedasticity, shared signs, and other
joint structure.  Zero covariance does not make the raw pairs exchangeable.
Consequently, an ordinary permutation distribution need not match the
sampling distribution under a weak null.  Studentization can give pointwise
asymptotic validity under regular conditions, but it does not turn the weak
null into an exact randomization null.

### 3. Why can subset pivotality fail?

For component statistics `T_P` and `T_M`, subset pivotality would require the
distribution of a true-null component to be unchanged by whether the other
component null is true or false.  A profile alternative changes the joint
node geometry and can therefore change the variance and shape of the Mantel
statistic even when its own population correlation is zero; the reverse can
also occur.  The project exhibited a Mantel-null distribution whose
standardized SD fell from `1.083` to `.075` and whose KS distance from its
matched global-null distribution was `.596`.

Therefore the joint-label maxT permutation reference is valid for the joint
exchangeability null, but its component-adjusted values are not automatically
strong-FWER discoveries under arbitrary partial weak nulls.  Holm avoids a
subset-pivotality assumption only if each local p-value is itself valid; it
cannot repair an invalid weak-null p-value.

### 4. Why can Mantel not treat pairwise edges as iid?

The distances `|X_i-X_j|` and `|X_i-X_k|` share node `i`, so they are normally
dependent.  Although there are `n(n-1)/2` edges, the leading sampling
fluctuation of the order-two U-statistic is its node-level Hájek projection,

\[
IF_\theta(z)=2\{E[h(z,Z')\mid z]-\theta\}.
\]

The effective first-order CLT has `n` independent node contributions, not
`n(n-1)/2` independent edge contributions.  Correct resampling deletes a node
and all incident edges, or uses the node-level projection.  With clustered
rooms, the independent contributions must instead respect buildings and the
cross-building U-structure; six buildings do not justify an ordinary cluster
CLT.

### 5. How do the Huber location and MAD enter the influence function?

For one margin,

\[
m=\operatorname{Med}(X),\quad d=\operatorname{Med}|X-m|,
\quad s=kd,
\]

and `T` solves `E psi_c((X-T)/s)=0`.  The median affects the MAD through both
MAD boundaries; the MAD affects the Huber equation through its scale.  With

\[
A=P(|U|<c),\qquad B=E\{U1(|U|<c)\},
\]

the location influence is

\[
IF_T(z)=\frac{s}{A}\psi_c\left(\frac{z-T}{s}\right)
-\frac{B}{A}IF_s(z).
\]

This `IF_T` then enters the influences of the numerator and both denominator
moments of `C`.  Because contamination occurs as an observed pair `(x,y)`, a
single paired `IF_C(x,y)` is required; its variance automatically includes
the X-Y and numerator-denominator covariances.  Under symmetry `B=0`, so the
MAD-to-Huber path vanishes at first order, but not necessarily in finite
samples or under skewness.

### 6. Why can the Jacobian be ill-conditioned?

The Jacobian records how strongly the population estimating equations react
to movements in median, MAD, and Huber centre.  If the density near the
median is very small, moving the median changes `F(m)-1/2` only weakly.  If
the MAD boundary density or Huber active-score probability is small, their
equations are similarly flat.  Coupling and cancellation under asymmetry can
create an additional weak direction.  A small singular value means that some
combination of nuisance parameters can move greatly while changing the
estimating equations very little.

In the symmetric bridge families, the binding direction is exactly
`d f(m)`: the central valley weakly identifies which side/mode anchors the
reference.  Large MAD endpoint density does not compensate for that weak
centre direction.

### 7. Why is sqrt(n) sigma_min(J) natural?

For nuisance parameter `theta`, the first-order estimating-equation expansion
is

\[
0\approx (P_n-P)g(\theta)+J(\widehat\theta-\theta),
\]

so

\[
\widehat\theta-\theta
\approx-J^{-1}(P_n-P)g(\theta).
\]

Empirical score noise is order `n^{-1/2}`, while the worst amplification by
the inverse system is `1/sigma_min(J)`.  Hence the least stable nuisance
direction has scale

\[
O_P\{1/(\sqrt n\,\sigma_{\min}(J))\}.
\]

The product `sqrt(n) sigma_min(J)` is therefore the natural dimensionless
signal-to-noise measure for local reference identification.  When it is not
large, a local linear approximation is being asked to describe nuisance
movement of nonlocal size.

### 8. What is the next layer after first-order family residuals?

A second-order expansion contains nuisance curvature terms schematically of
the form

\[
J^{-1}H[J^{-1}\mathbb G_n g,J^{-1}\mathbb G_n g],
\]

so two families with the same `J` can differ through the Hessian `H`, score
skewness/tails, or the probability of crossing a nonsmooth median/MAD
selection boundary.  The most useful future work is therefore a focused
second-order remainder comparison on already matched families, not a search
for unrelated anomalies.  Until that work is complete, the family residual
is a limitation rather than a fourth claim.

### 9. Which results are theorem and which are empirical?

| Statement | Current evidence class |
|---|---|
| `C=1+rho_P CV(a)CV(b)` and fixed-margin permutation ordering | Algebraic identity |
| One-dimensional L2 divergence reduces to radial salience ranking | Algebraic identity |
| Complete median/MAD/Huber and `C` influence formulas | Functional derivative, numerically validated |
| Pointwise iid asymptotic linearity/normality under A1-A6 | Theorem-level statement; final proof details still to write |
| Exact permutation validity under declared group invariance | Finite-sample randomization theorem |
| Mantel first-order variance uses node Hájek projections | U-statistic theorem |
| Complete nuisance Jacobian formula | Analytic derivative, finite-difference verified |
| Near-degenerate fitting can severely distort tested procedures | Constructive empirical observation |
| `I_n` strongly organizes the tested transition | Empirical observation with first-order rationale |
| A cutoff near one separates all future valid/invalid cases | Not established |
| Residual matched-family difference is beyond the measured first-order Jacobian | Empirical observation and logical diagnosis |
| Exact form or magnitude of the higher-order correction | Open problem |

### 10. Which claims absolutely cannot be written now?

Do not claim that:

- c_delta is a general measure of dependence or complete internal geometry;
- Huber/MAD fitting makes the uncapped statistic bounded-influence or immune
  to outliers;
- a permutation test is exact whenever `C=1` or `rho_P=0`;
- studentization always repairs a weak-null permutation test;
- `sqrt(n) sigma_min(J)>1` guarantees valid inference, or any current
  diagnostic provides a conditional-validity gate;
- centre density, spacing, MAD/IQR, or bootstrap reference spread alone is a
  universal failure criterion;
- first-order conditioning fully explains the residual family effect;
- subset pivotality holds for profile and Mantel component nulls;
- maxT component p-values have general strong-FWER meaning here;
- Holm or an omnibus gate can repair invalid local p-values;
- Mantel has `n(n-1)/2` iid observations;
- room-level iid or a standard cluster CLT is justified with approximately
  six buildings;
- the current method uniformly dominates Mantel, Pearson, distance
  correlation, or another dependence procedure;
- cap-6 and uncapped c_delta estimate the same parameter;
- current pointwise asymptotics are uniform over near-degenerate, discrete,
  heavy-tail, or contamination neighborhoods.

## Proposed paper structure

1. **Scientific target and estimand.**  Define labelled paired-salience
   concordance, distinguish it from full dyadic geometry, and settle `C`
   versus `rho_P` as the main reported effect.
2. **Regular iid inference.**  State assumptions, complete influence
   function, asymptotic theorem, and the exact-versus-weak-null distinction.
3. **A near-degenerate counterexample family.**  Show the reference-fitting
   mechanism and the finite-sample distortion with a small, predeclared set of
   figures/tables.
4. **Nuisance conditioning.**  Derive `J`, motivate `I_n`, and show the matched
   bridge transition without presenting a universal cutoff.
5. **What first order misses.**  Present the matched-family residual as an
   explicit limitation and point to second-order/nonlocal reference selection.
6. **Discussion.**  State scope, diagnostics as warnings rather than gates,
   and implications for regular iid applications.

The Mantel, adaptive omnibus, partial-null multiplicity, and small-building
results should not all remain in the main narrative.  Unless Professor Hoorn
identifies them as essential to the scientific application, they belong in a
brief contrast section, an appendix, or later work.

## Decisions to settle with Professor Hoorn

1. Is the paper's primary effect scale raw `C`, or the more direct profile
   correlation `rho_P`, with `C` reported as the historical parameter?
2. Is the main inferential target exact random-pairing evidence, weak-null
   inference, or a deliberate two-layer presentation of both?
3. Is the central contribution a regularity/failure paper about the existing
   robust c_delta, rather than another proposal for an adaptive omnibus?
4. Should the building application be only motivation/illustration until an
   adequate building-level estimand and sampling theory exist?
5. Is the higher-order family residual acceptable as a clearly quantified
   limitation, or is one focused second-order result required before writing?

## Remaining work that directly serves the paper

1. Freeze notation and the primary estimand after Professor Hoorn's response.
2. Turn the theorem proof sketch into a formal appendix proof, including the
   tangent set and empirical remainder conditions.
3. Select a minimal canonical simulation set: regular calibration,
   near-degenerate distortion, matched bridge recovery, and matched-family
   residual.
4. Rebuild only those canonical tables from fixed seeds and attach Monte Carlo
   uncertainty.
5. Audit every manuscript sentence against the evidence-class table above.

No additional broad power surface, anomaly family, adaptive weighting grid,
or diagnostic threshold search is currently justified by the proposed paper.
