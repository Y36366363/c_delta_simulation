# Studentization refinement and asymptotic theorem for Huber c_delta

## Executive conclusion

The complete influence function derived on 08/05 survives a substantially
stronger check. Distribution-level quadrature for a skew-lognormal joint law
matches its point-contamination derivative to scaled error below `1.2e-5` at
all regular test points. The apparent discrepancy seen in the earlier
empirical check is now localized: a contaminating atom placed exactly at the
population median is a nondifferentiable boundary direction, not evidence that
the regular influence formula is wrong.

The finite-sample interval problem is also better diagnosed. Replacing KDE by
cross-fitted KDE or by the known population lognormal density changes the mean
sandwich SE by less than `0.2%`. HC-style scalar corrections improve coverage
but do not repair it. A complete-refit bootstrap-t interval also undercovers
and its log version can be extremely wide under skewness. Consequently:

- the point functional and its first-order asymptotic theory remain viable;
- density estimation is not the main bottleneck in the tested model;
- the generic finite-sample Wald or bootstrap-t interval is not ready;
- permutation inference remains the formal default for pairing evidence.

## 1. Distribution-level skew validation

The validation law is

\[
X=\exp(0.6U),\qquad Y=\exp(0.6V),\qquad
\operatorname{Corr}(U,V)=0.4,
\]

with bivariate standard-normal \((U,V)\). Marginal medians and densities are
analytic. The MAD and Huber equation are solved at population level, while
joint radius moments are evaluated by 160-node Gaussian-Hermite quadrature.
For every \(\epsilon\), the contaminated median, MAD, Huber centre, numerator,
and both denominator moments are all recomputed under
\((1-\epsilon)P+\epsilon\Delta_{(x,y)}\).

The population quantities are

\[
C=1.2223616,\qquad T_X=T_Y=1.0791670,\qquad
\operatorname{MAD}=0.3871215,
\]

and the quadrature complete-IF variance is approximately `4.9854`.
Across quadrature orders `80-200`, `C` ranged from `1.2210` to `1.2224` and
the IF variance from `4.9331` to `4.9854`; the regular-point derivative error
remained below `1.2e-5` at every checked order. Thus the derivative conclusion
is stable even though nonsmooth absolute-value integrands make the last few
digits of the population moments order-sensitive.

At \(\epsilon=10^{-6}\):

| contamination direction | analytic IF | finite difference | scaled error | MAD indirect component |
|---|---:|---:|---:|---:|
| matched 0.99 quantiles | 16.7612 | 16.7610 | 0.0000116 | -0.1502 |
| X 0.99, Y 0.60 | -5.2404 | -5.2404 | 0.0000044 | -0.0622 |
| X 0.55, Y 0.45 | 1.0310 | 1.0310 | 0.0000008 | 0.0921 |
| X 0.01, Y 0.99 | 1.0082 | 1.0082 | 0.0000075 | -0.0921 |

The MAD pathway is therefore not merely formal: its contribution can be around
`0.09-0.15` in this skewed law. Removing it would produce a visibly wrong
derivative.

### Quantile-boundary exception

For an atom inserted exactly at the population median, the scaled discrepancy
is about `0.0253` and does not vanish as epsilon decreases. The distributional
quantile map is Hadamard differentiable tangentially to continuous empirical-
process directions when the density is positive, but a point-mass direction
at the quantile lies on the indicator's jump. Its one-sided contamination
derivative depends on the quantile convention. This exceptional point has
probability zero under a continuous sampling law and does not change the iid
asymptotic-linear representation, but it must be acknowledged when presenting
the influence curve pointwise.

## 2. Density estimator comparison

The skew-lognormal coverage experiment used 2,500 datasets per row. It
compared ordinary KDE, five-fold cross-fitted KDE, and the **known true
lognormal density**, all evaluated in the complete IF calculation.

| n | method | 95% log-Wald coverage | mean SE / empirical SD |
|---:|---|---:|---:|
| 40 | KDE, sample correction | .8032 | .6588 |
| 40 | cross-fitted KDE | .8036 | .6589 |
| 40 | true analytic density | .8056 | .6601 |
| 80 | KDE, sample correction | .8124 | .7326 |
| 80 | cross-fitted KDE | .8124 | .7326 |
| 80 | true analytic density | .8132 | .7334 |
| 160 | KDE, sample correction | .8552 | .7981 |
| 160 | cross-fitted KDE | .8552 | .7981 |
| 160 | true analytic density | .8552 | .7987 |

Relative to ordinary KDE, cross-fitting changed the mean SE by at most about
`0.01%`, and using the true density changed it by at most about `0.20%`.
Therefore density bias or own-observation reuse is not the operative cause of
the severe underestimation in this model.

The likely mechanism is finite-sample underrepresentation of the rare, large
values in the **squared complete influence contribution**. Robustifying the
centre bounds the centre's local influence, but the uncapped product
\(|X-T_X||Y-T_Y|\) still gives an unbounded direct IF. A finite sample can
estimate \(C\) reasonably while materially underestimating
\(E(\operatorname{IF}_C^2)\).

## 3. HC-style correction results

The tested corrections apply scalar analogues to the empirical IF meat. With
effective estimating-equation dimension `p=9`:

\[
\text{HC0 factor}=1,\quad
\text{sample factor}=\frac n{n-1},\quad
\text{HC1 factor}=\frac n{n-p},\quad
\text{HC3-style factor}=\left(\frac n{n-p}\right)^2.
\]

These are explicitly **HC-style analogues**, not the observation-specific
regression-leverage HC2/HC3 estimator of MacKinnon and White.

| n | HC0 | sample | HC1 | HC3-style |
|---:|---:|---:|---:|---:|
| 40 | .7976 | .8032 | .8508 | .8976 |
| 80 | .8088 | .8124 | .8300 | .8544 |
| 160 | .8544 | .8552 | .8628 | .8712 |

The correction helps most at `n=40`, as expected from its degrees-of-freedom
factor, but no fixed parameter-count multiplier can replace missing tail
information. HC3-style is useful as a diagnostic upper adjustment, not a
validated confidence interval.

For reference, the interval using the population quadrature variance covered
`.9588`, `.9568`, and `.9560` at `n=40,80,160`. This supports the population
variance formula while showing that it can be conservative relative to the
finite-sample estimator SD.

## 4. Complete-IF bootstrap-t

The bootstrap-t experiment used 600 outer datasets per condition and 99 paired
bootstrap refits per dataset. Every refit recomputed median, MAD, Huber centre,
all moments, KDE density values, and the complete IF standard error. All outer
datasets produced valid intervals.

| scenario | n | sandwich log | HC3-style log | bootstrap-t normal | bootstrap-t log |
|---|---:|---:|---:|---:|---:|
| symmetric, rho=.5 | 80 | .9250 | .9450 | .8983 | .8983 |
| symmetric, rho=.5 | 160 | .9100 | .9283 | .9017 | .9017 |
| skew, rho=.4 | 80 | .8217 | .8600 | .8133 | .8067 |
| skew, rho=.4 | 160 | .8700 | .8883 | .8717 | .8700 |

Bootstrap-t did not improve coverage. Under skewness at `n=80`, its average
log-scale interval width was `2.808`, compared with `0.628` for the ordinary
log-sandwich interval, yet coverage remained only `.8067`. Rare bootstrap
samples can produce a highly unstable studentizing denominator and extreme
pivot quantiles. Increasing the number of inner bootstrap draws would estimate
that unstable pivot more precisely; it would not address the observed
structural failure.

## 5. Formal first-order theorem

Let \(Z_i=(X_i,Y_i)\), \(i=1,\ldots,n\), be iid from a joint distribution
\(P\). For margin \(j\in\{X,Y\}\), let \(F_j\), \(m_j\), \(d_j\),
\(s_j=k d_j\), and \(T_j\) denote its cdf, median, MAD, scaled MAD, and Huber
location. Define

\[
a(x)=|x-T_X|,\quad b(y)=|y-T_Y|,
\quad C(P)=\frac{P\{a(X)b(Y)\}}{P a(X)\,P b(Y)}.
\]

### Assumptions

**A1 (sampling).** The pairs \(Z_i\) are iid. If the sampling unit is a
cluster, the theorem must instead be applied to independent clusters with a
cluster-summed influence contribution.

**A2 (regular marginal quantiles).** Each margin has unique \(m_j\) and
\(d_j>0\). Its density is continuous and strictly positive in neighborhoods
of \(m_j\), \(m_j-d_j\), and \(m_j+d_j\).

**A3 (regular Huber equation).** The fixed \(c\in(0,\infty)\) Huber equation
has a unique solution \(T_j\),

\[
A_j=P\left(\left|\frac{X_j-T_j}{s_j}\right|<c\right)>0,
\]

and the margin assigns zero probability to \(T_j\), \(T_j-cs_j\), and
\(T_j+cs_j\). The last condition avoids derivative ambiguity at the absolute-
value and Huber knots.

**A4 (nondegeneracy).** \(\mu_X=P a(X)>0\), \(\mu_Y=P b(Y)>0\), and the
complete influence variance \(V\) is strictly positive.

**A5 (moments).**

\[
P\{a(X)^2+b(Y)^2+a(X)^2b(Y)^2\}<\infty.
\]

Because the Huber, median, and MAD influence contributions are bounded under
A2-A3, this joint product condition is sufficient for
\(P\operatorname{IF}_C^2<\infty\). A slightly stronger
\(2+\eta\) moment is useful for uniform integrability and bootstrap arguments.

**A6 (empirical solutions).** The empirical median, MAD, and selected Huber
root are measurable and consistent for their unique population counterparts.

### Theorem

Under A1-A6, the empirical uncapped Huber c_delta satisfies

\[
\sqrt n\{C(P_n)-C(P)\}
=\frac1{\sqrt n}\sum_{i=1}^n
\operatorname{IF}_C(Z_i;P)+o_P(1),
\]

where \(\operatorname{IF}_C\) is the complete paired influence function in
`functional_delta_and_studentized_inference_20260805.md`. Consequently,

\[
\sqrt n\{C(P_n)-C(P)\}\Rightarrow N(0,V),
\qquad V=P\{\operatorname{IF}_C^2\}.
\]

If, additionally, the three required density estimates in each margin are
consistent at the corresponding random sample quantiles, all other plug-in
moments are consistent, and \(\widehat V\to_P V\), then

\[
\frac{\sqrt n\{C(P_n)-C(P)\}}{\sqrt{\widehat V}}
\Rightarrow N(0,1).
\]

Thus the normal and log-Wald intervals are **pointwise asymptotically valid**.
This theorem does not claim uniform finite-sample validity over heavy-tail,
near-degenerate, discrete, or contamination neighborhoods.

### Proof sketch

1. Positive continuous densities give the usual tangential Hadamard
   derivatives for the median and for the radius median defining MAD.
2. Apply the implicit-function theorem to the Huber score. A3 makes its
   derivative in `T` nonzero; composing with the MAD derivative yields the
   complete \(\operatorname{IF}_{T_j}\).
3. Differentiate \(P|X-T_X|\), \(P|Y-T_Y|\), and
   \(P\{|X-T_X||Y-T_Y|\}\). A3 removes mass at the absolute-value knots.
4. Apply the ordinary finite-dimensional delta method to
   \(q(\nu,\mu_X,\mu_Y)=\nu/(\mu_X\mu_Y)\). A4 keeps its gradient finite.
5. A5 places the resulting influence function in \(L_2(P)\), so the iid CLT
   gives asymptotic normality. Consistency of the empirical IF variance and
   Slutsky's theorem give the studentized conclusion.

This is now a theorem-level statement with an auditable proof route. A journal
appendix should still specify the exact tangent space and prove the empirical
remainder terms rather than citing composition informally.

## 6. Inferential recommendation after today's tests

1. Retain uncapped Huber c_delta as the primary **point statistic**.
2. Retain unrestricted or design-respecting permutation as the primary test of
   paired salience.
3. Label the complete-IF sandwich interval as asymptotic/exploratory. Do not
   describe HC3-style or bootstrap-t as a solved 95% interval.
4. Do not spend the next stage tuning KDE bandwidth or cross-fitting; today's
   true-density comparison rules that out as the principal bottleneck.
5. The next targeted inference work should compare:
   - tail-stabilized estimation of the IF second moment;
   - an `m`-out-of-`n` bootstrap or subsampling method under explicit moment
     conditions;
   - the cap-6 sensitivity estimand's bounded direct IF, kept separate from the
     uncapped primary estimand;
   - larger `n` to measure the onset of the asymptotic regime.

## References

- Hampel, F. R. (1974). *The Influence Curve and Its Role in Robust
  Estimation*. https://doi.org/10.1080/01621459.1974.10482962
- van der Vaart, A. W. (1998). *Asymptotic Statistics*, Chapter 20,
  Functional Delta Method.
  https://www.cambridge.org/core/books/asymptotic-statistics/functional-delta-method/734EE290B8542CECFD7D4B981F458C4B
- Beutner, E., and Zähle, H. (2016). *Functional delta-method for the bootstrap
  of quasi-Hadamard differentiable functionals*.
  https://arxiv.org/abs/1510.06207
- Arachchige, C. N. P. G., and Prendergast, L. A. (2024).
  *Confidence intervals for median absolute deviations*.
  https://doi.org/10.1080/03610918.2024.2376198
- MacKinnon, J. G., and White, H. (1985). *Some heteroskedasticity-consistent
  covariance matrix estimators with improved finite sample properties*.
  https://doi.org/10.1016/0304-4076(85)90158-7
- Hall, P., and Martin, M. A. (1988). *On bootstrap resampling and iteration*.
  https://doi.org/10.1093/biomet/75.4.661
