# Weak-Null Local Tests and Multiplicity

Date: 2026-08-14

## Status

This update derives studentized local tests for the two elementary weak nulls

\[
H_P:\rho_P=0,\qquad H_M:\rho_M=0,
\]

where \(\rho_P\) is the Huber-radius profile correlation and \(\rho_M\) is
the population correlation of paired absolute distances.  The derivations are
first-order valid under iid continuous observations and nondegeneracy.  The
finite-sample validation does **not** yet support making these tests, closed
testing, or Holm-adjusted component discovery primary procedures.

The motivation agrees with the correlation warning in
[DiCiccio and Romano (2017)](https://doi.org/10.1080/01621459.2016.1202117):
an unstudentized permutation correlation test can fail under a dependent but
uncorrelated weak null.  General studentized randomization theory is developed
by [Chung and Romano (2013)](https://doi.org/10.1214/13-AOS1090).  The Mantel
derivation below uses the order-two U-statistic projection originating with
[Hoeffding (1948)](https://doi.org/10.1214/aoms/1177730196).

## 1. Profile-Only Weak Null

Let

\[
a=|X-T_X|,\qquad b=|Y-T_Y|,
\]

with the marginal Huber locations \(T_X,T_Y\) fitted using normal-consistent
MAD scales.  The scale factors in `huber_reference_profile` cancel exactly
from Pearson correlation, although MAD estimation still affects the statistic
indirectly through each Huber centre.  Define

\[
\mu_a=E(a),\quad \mu_b=E(b),\quad \nu=E(ab),\quad
q_a=E(a^2),\quad q_b=E(b^2),
\]

\[
u=\nu-\mu_a\mu_b,\quad v_a=q_a-\mu_a^2,\quad
v_b=q_b-\mu_b^2,
\]

so

\[
\rho_P=\frac{u}{\sqrt{v_av_b}}.
\]

For moment order \((\nu,\mu_a,\mu_b,q_a,q_b)\), the gradient is

\[
\nabla\rho_P=
\left(
\frac1d,
-\frac{\mu_b}{d}+\rho_P\frac{\mu_a}{v_a},
-\frac{\mu_a}{d}+\rho_P\frac{\mu_b}{v_b},
-\frac{\rho_P}{2v_a},
-\frac{\rho_P}{2v_b}
\right),
\quad d=\sqrt{v_av_b}.
\]

The fixed-centre direct influence is the gradient multiplied by

\[
(ab-\nu,\ a-\mu_a,\ b-\mu_b,\ a^2-q_a,\ b^2-q_b)^\top.
\]

To restore centre fitting, write

\[
g_X=E\{\operatorname{sign}(X-T_X)\},\quad
h_X=E\{\operatorname{sign}(X-T_X)b\},\quad
e_X=E(X-T_X).
\]

Then

\[
\partial_{T_X}u=-h_X+g_X\mu_b,
\qquad
\partial_{T_X}v_a=-2e_X+2\mu_ag_X,
\]

and

\[
\Gamma_X=
\frac{-h_X+g_X\mu_b}{d}
-\frac{\rho_P}{2v_a}(-2e_X+2\mu_ag_X).
\]

The analogous \(\Gamma_Y\) follows by exchanging margins.  Therefore

\[
\boxed{
IF_P(Z)=IF_{P,\mathrm{direct}}(Z)
+\Gamma_XIF_{T_X}(X)+\Gamma_YIF_{T_Y}(Y)
}.
\]

The already validated Huber-location influence contains the median, MAD, and
MAD-to-Huber indirect terms.  The local Wald statistic is

\[
Z_P=\frac{\widehat\rho_P}{
\sqrt{n^{-1}\widehat{\operatorname{Var}}(IF_P)}}.
\]

The implementation also recomputes both Huber/MAD fits in every delete-one
sample and uses the full-refit jackknife SE.

## 2. Mantel-Only Weak Null

Let \(Z=(X,Y)\), let \(Z'\) be an independent copy, and define

\[
A(Z,Z')=|X-X'|,\qquad B(Z,Z')=|Y-Y'|.
\]

The same five-moment correlation map gives

\[
\rho_M=
\operatorname{Corr}\{A(Z,Z'),B(Z,Z')\}.
\]

Each moment is an order-two U-functional with kernel vector

\[
h(Z,Z')=(AB,A,B,A^2,B^2)^\top.
\]

If \(\theta=E\{h(Z,Z')\}\), its first-order Hájek projection is

\[
IF_\theta(z)=2[E\{h(z,Z')\mid z\}-\theta].
\]

Consequently,

\[
\boxed{IF_M(z)=\nabla\rho_M(\theta)^\top IF_\theta(z)}.
\]

This is the essential correction to an edge-wise analysis: the
\(n(n-1)/2\) distances are not independent observations.  The effective CLT
unit is the node, and the standard error is

\[
\widehat{SE}_M=
\sqrt{n^{-1}\widehat{\operatorname{Var}}(IF_M)}.
\]

The alternative delete-one-node jackknife removes all \(n-1\) edges incident
to one observation, recomputes the five U-moments, and studentizes the original
Mantel effect estimate.

## 3. Regularity Conditions

For the profile result, require the earlier median/MAD/Huber regularity
conditions, positive profile variances, and a square-integrable complete
influence function.  For Mantel, require iid observations,
finite second moments of the projected five-kernel vector, positive distance
variances, and a nondegenerate first-order projection.  Under these conditions
the functional delta method and U-statistic CLT give

\[
\sqrt n(\widehat\rho_j-\rho_j)\Rightarrow N(0,V_j),
\qquad j\in\{P,M\},
\]

and consistent studentization gives asymptotic standard normal local tests.

These results are pointwise.  They do not cover discrete/near-degenerate
margins, heavy-tail sequences with vanishing moments, or a fixed small number
of buildings.  With clustered rooms the independent unit is the building and
the influence contributions must be summed within building before estimating
variance.  Six buildings are not enough to rely comfortably on a cluster CLT.

## 4. Iid Partial-Null Validation

Two genuinely iid partial-null laws replaced yesterday's fixed-template
diagnostic:

1. **Profile null, Mantel alternative:** independent lognormal radii with a
   shared random sign.  Population radial profiles are independent, while
   the sign partition creates distance association.
2. **Mantel null, profile alternative:** \(X\sim U(-1,1)\), with \(Y=X\) for
   a calibrated fraction of observations and
   \(Y=1/(0.1+|X|)+\epsilon\) otherwise.  A 500,000-pair independent
   calibration selected probability `.640502`, giving Mantel effect
   `1.59e-6` and a separate profile-effect check `-.3782`.

Each confirmatory cell used 1,000 independent datasets.

### Local null rejection

| Scenario | n | Profile sandwich | Profile jackknife | Mantel sandwich | Mantel jackknife |
|---|---:|---:|---:|---:|---:|
| Independent signed-lognormal null | 80 | `.086` | `.062` | `.085` | `.066` |
| Independent signed-lognormal null | 160 | `.071` | `.058` | `.111` | `.097` |
| Profile null, Mantel alternative | 80 | `.071` | `.053` | alternative | alternative |
| Profile null, Mantel alternative | 160 | `.073` | `.064` | alternative | alternative |
| Independent calibrated-mixture null | 80 | `.099` | `.075` | `.109` | `.085` |
| Independent calibrated-mixture null | 160 | `.074` | `.065` | `.068` | `.054` |
| Mantel null, profile alternative | 80 | alternative | alternative | `.063` | `.055` |
| Mantel null, profile alternative | 160 | alternative | alternative | `.058` | `.047` |

The jackknife is consistently better than the plug-in sandwich.  It is close
to nominal on the two partial-null paths, but it is not uniformly calibrated
over the matched global-null distributions.  In particular, the signed-
lognormal Mantel row remains anti-conservative at `n=160`.  A generic
delete-one bias correction was also tested in the pilot; it increased
dispersion in several rows and was rejected rather than tuned.

### Power and Holm behavior

- Profile-null/Mantel-alternative jackknife Mantel power was `.942` at `n=80`
  and `.990` at `n=160`; Holm power was `.911` and `.982`.
- Mantel-null/profile-alternative profile power was `.731` and `.964`; Holm
  power was `.658` and `.946`.
- When both effects were positive, both Holm-adjusted tests rejected in `.982`
  and `.999` of datasets.
- Global-null Holm FWER ranged from `.059-.080` at `n=80` and `.053-.073` at
  `n=160`.  Partial-null FWER was `.050/.063` for the profile-null path and
  `.048/.044` for the Mantel-null path.

## 5. Multiplicity Decision

If \(p_P,p_M\) are valid marginal weak-null p-values, the two-test Holm rule
provides strong FWER control without subset pivotality
([Holm, 1979](https://doi.org/10.2307/4615733)).  For two hypotheses it is
equivalent to closed testing with the Bonferroni intersection p-value

\[
p_{P\cap M}=\min\{1,2\min(p_P,p_M)\}.
\]

Thus a separate complex closed-testing implementation would add no benefit at
this stage.  More importantly, multiplicity adjustment cannot repair invalid
local p-values.  Because the current jackknife p-values remain mildly to
materially anti-conservative in some global-null rows, neither Holm nor closed
testing is ready for formal component discovery.

The old global permutation omnibus cannot be used as a gate that legitimizes
unadjusted local weak-null tests.  It tests joint label exchangeability, not
the intersection \(\rho_P=\rho_M=0\) under arbitrary dependence.

## 6. Recommendation

1. Retain the existing standardized-max permutation result only for the joint
   random-pairing omnibus null.
2. Retain adjusted component evidence as descriptive.
3. Keep today's profile and Mantel local tests as theoretically motivated
   research implementations, not report-ready defaults.
4. Do not activate Holm or closed testing for formal component discovery yet.
5. Next test studentized permutation calibration inspired by DiCiccio–Romano,
   recomputing the complete profile or U-projection variance on each orbit.
   For small building counts, also compare building-level wild bootstrap or
   subsampling; do not treat rooms as iid when buildings are the sampling unit.

## Files

- `scripts/run_weak_null_local_tests_20260814.py`
- `tests/test_weak_null_local_tests_20260814.py`
- `results/weak_null_local_calibration_confirmatory_20260814.tsv`
- `results/weak_null_local_tests_confirmatory_20260814.tsv`
