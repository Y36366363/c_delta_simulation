# Functional delta method and studentized inference for Huber c_delta

## Status and scope

This note gives a first-order derivation for the **uncapped, one-dimensional,
continuous-margin** Huber-reference statistic

\[
C(F)=\frac{E\{r_X(X)r_Y(Y)\}}
{E\{r_X(X)\}E\{r_Y(Y)\}},\qquad
r_X(x)=|x-T_X|,
\]

where each marginal centre is a Huber location fitted with a
normal-consistent MAD scale. It also implements a plug-in sandwich standard
error, normal and log-normal intervals, and a Wald test. This is a serious
working derivation, but not yet a complete theorem: formal Hadamard
differentiability and uniform remainder control still need to be written down.

The construction follows the influence-curve view of statistical functionals
introduced by Hampel and the functional delta method described by van der
Vaart. Unknown-scale Huber theory confirms that scale estimation must be
included rather than silently treated as fixed. Stacked estimating-equation
theory provides the corresponding empirical sandwich interpretation.

## 1. Marginal nuisance functionals

For one margin, write

\[
m=\operatorname{Med}(X),\quad
d=\operatorname{Med}|X-m|,\quad s=k d,\quad k=1.4826,
\]

and define the Huber centre by

\[
E\left[\psi_c\left(\frac{X-T}{s}\right)\right]=0,
\qquad \psi_c(u)=\max(-c,\min(u,c)).
\]

Assume a continuous density `f`, positive at `m`, `m-d`, and `m+d`, no
probability mass at the Huber knots, and finite moments needed below. Under the
contamination path \(F_\epsilon=(1-\epsilon)F+\epsilon\Delta_z\),

\[
\operatorname{IF}_m(z)=
\frac{1/2-\mathbf 1(z\le m)}{f(m)}.
\]

Implicit differentiation of
\(P(m-d\le X\le m+d)=1/2\) gives

\[
\operatorname{IF}_d(z)=
\frac{
1/2-\mathbf 1(|z-m|\le d)
-\{f(m+d)-f(m-d)\}\operatorname{IF}_m(z)
}{f(m+d)+f(m-d)},
\]

and \(\operatorname{IF}_s(z)=k\operatorname{IF}_d(z)\). The term multiplying
\(\operatorname{IF}_m\) is essential for an asymmetric distribution.

Let \(U=(X-T)/s\),

\[
A=E\{\psi'_c(U)\}=P(|U|<c),\qquad
B=E\{U\psi'_c(U)\}.
\]

Differentiating the Huber equation yields

\[
\boxed{
\operatorname{IF}_T(z)=
\frac{s}{A}\psi_c\left(\frac{z-T}{s}\right)
-\frac{B}{A}\operatorname{IF}_s(z)
}.
\]

Thus the MAD affects `C` only indirectly through `T` for the uncapped primary
statistic. The explicit scale in \(|X-T|/s\) cancels from the ratio defining
`C`. For a symmetric margin, \(B=0\), so the MAD-to-centre term vanishes to
first order. It does not generally vanish for skewed margins.

## 2. Joint numerator and denominator influence

Set

\[
a=|X-T_X|,\quad b=|Y-T_Y|,\quad
\mu_X=E(a),\quad\mu_Y=E(b),\quad\nu=E(ab),
\]

so \(C=\nu/(\mu_X\mu_Y)\). Define

\[
g_X=E\{\operatorname{sign}(X-T_X)\},\quad
h_X=E\{\operatorname{sign}(X-T_X)b\},
\]

and analogously \(g_Y,h_Y\). For a contaminated **pair** \(z=(x,y)\),

\[
\begin{aligned}
\operatorname{IF}_{\mu_X}(z)
 &=a_x-\mu_X-g_X\operatorname{IF}_{T_X}(x),\\
\operatorname{IF}_{\mu_Y}(z)
 &=b_y-\mu_Y-g_Y\operatorname{IF}_{T_Y}(y),\\
\operatorname{IF}_{\nu}(z)
 &=a_xb_y-\nu-h_X\operatorname{IF}_{T_X}(x)
                    -h_Y\operatorname{IF}_{T_Y}(y).
\end{aligned}
\]

The ordinary multivariate delta method for \(q(\nu,\mu_X,\mu_Y)) then gives

\[
\boxed{
\operatorname{IF}_C(z)=
\frac{\operatorname{IF}_\nu(z)}{\mu_X\mu_Y}
-C\frac{\operatorname{IF}_{\mu_X}(z)}{\mu_X}
-C\frac{\operatorname{IF}_{\mu_Y}(z)}{\mu_Y}
}.
\]

An equivalent and computationally useful decomposition is

\[
\operatorname{IF}_C(z)=D(z)+\Gamma_X\operatorname{IF}_{T_X}(x)
                             +\Gamma_Y\operatorname{IF}_{T_Y}(y),
\]

where

\[
D(z)=\frac{a_xb_y}{\mu_X\mu_Y}
-C\frac{a_x}{\mu_X}-C\frac{b_y}{\mu_Y}+C,
\]

\[
\Gamma_X=C\frac{g_X}{\mu_X}-\frac{h_X}{\mu_X\mu_Y},\qquad
\Gamma_Y=C\frac{g_Y}{\mu_Y}-\frac{h_Y}{\mu_X\mu_Y}.
\]

This single paired influence value is important. Estimating separate marginal
variances and then adding them would omit covariance induced by the observed
pairing. The variance of the *sum* above automatically includes all
numerator-denominator, X-Y, and nuisance/direct cross-covariances.

## 3. Sandwich variance, interval, and test

Under iid pairs and the stated regularity conditions,

\[
\sqrt n(\widehat C-C)\ \Rightarrow\ N(0,V),\qquad
V=E\{\operatorname{IF}_C(X,Y)^2\}.
\]

The implemented empirical sandwich estimate is

\[
\widehat V=\frac1{n-1}\sum_{i=1}^n
\{\widehat{\operatorname{IF}}_{C,i}-
\overline{\widehat{\operatorname{IF}}_C}\}^2,
\qquad
\widehat{SE}=\sqrt{\widehat V/n}.
\]

It estimates the three density values required by the median/MAD influence
functions with a one-dimensional Gaussian KDE. The two reported intervals are

\[
\widehat C\pm z_{1-\alpha/2}\widehat{SE}
\]

and the positivity-preserving log-Wald interval

\[
\exp\left\{\log\widehat C\pm z_{1-\alpha/2}
\frac{\widehat{SE}}{\widehat C}\right\}.
\]

For \(H_0:C=C_0\), the current test uses
\(Z=(\widehat C-C_0)/\widehat{SE}\), with one- or two-sided normal-tail
p-values. For the scientific positive-salience alternative, the natural
default is \(C_0=1\) and `alternative="greater"`. This Wald test is not a
replacement for exact or design-respecting permutation inference in small,
discrete, tied, clustered, or nearly degenerate samples.

## 4. Closed-form symmetric benchmark

For

\[
X=S_Xe^{\sigma U},\qquad Y=S_Ye^{\sigma V},
\]

with balanced independent random signs and correlated standard-normal
\((U,V)\) having correlation \(\rho\), symmetry gives
\(T_X=T_Y=0\) and \(\Gamma_X=\Gamma_Y=0\). Therefore

\[
C=\exp(\sigma^2\rho)
\]

and, putting \(t=\sigma^2\),

\[
\begin{aligned}
V={}&e^{2t+4t\rho}+2e^{t+2t\rho}-4e^{t+3t\rho}\\
   &+2e^{3t\rho}-e^{2t\rho}.
\end{aligned}
\]

At \(\rho=0\), this reduces to \((e^t-1)^2\). A 250,000-draw Monte Carlo
check agreed with this expression within `0.01` absolute variance.

## 5. Numerical derivative validation

The analytic influence function was compared with
\([C\{(1-\epsilon)F+\epsilon\Delta_z\}-C(F)]/\epsilon\) using a 300,000-pair
reference sample.

| Margin model | contamination point | analytic IF | finite difference at 0.0001 | location contribution |
|---|---:|---:|---:|---:|
| symmetric signed lognormal | matched high | 1.3394 | 1.3384 | -0.0013 |
| symmetric signed lognormal | unmatched X high | -1.1606 | -1.1603 | 0.0000 |
| skew lognormal | matched high | 16.9904 | 16.9820 | -0.7568 |
| skew lognormal | unmatched X high | -5.2015 | -5.1873 | -0.3226 |

For the symmetric model, the maximum scaled discrepancy over all tested points
and epsilon values was `0.0043`. In the skewed model the high-leverage checks
were also close, and the nonzero location contributions confirmed the nuisance
path. Central contamination points had up to about `0.025` scaled discrepancy,
consistent with finite-sample empirical-quantile and KDE roughness; a
distribution-level quadrature check is still desirable.

## 6. Studentized coverage results

The main grid used 1,200 datasets per row, `n=40,80,160`, and
`rho=0,.2,.5`. Across all nine rows:

| SE/interval method | mean 95% coverage | mean SE / empirical SD |
|---|---:|---:|
| fixed-profile direct, log | .9198 | .9134 |
| full plug-in sandwich, log | .9415 | .9668 |
| full-refit jackknife, log | .9511 | 1.0335 |
| closed-form oracle, log | .9357 | .9386 |

These averages again conceal effect-dependent behavior. For `rho=.5`, the
full sandwich log interval covered `.9258`, `.9142`, and `.9108` at
`n=40,80,160`; its SE/empirical-SD ratios were `.9045`, `.9369`, and `.9066`.
The full influence formula therefore improves the overall direct-profile
diagnostic but does **not** yet yield dependable 95% finite-sample coverage.

An independent 3,000-dataset focused replication already showed that the
closed-form oracle interval covered about `.95` at `rho=.5,n=80,160`. This
supports the first-order variance derivation itself. The remaining failure is
mainly plug-in/studentization behavior, including variable nuisance and moment
estimation, rather than evidence that the analytic population variance is
wrong. The jackknife improves scale estimation but still covered only about
`.923-.927` in that focused strong-effect setting.

## 7. Present conclusion and next theory tests

1. The full paired influence function is now explicit and numerically
   supported. The MAD-to-Huber path matters under asymmetry and can be ignored
   only under justified symmetry conditions.
2. The natural asymptotic variance is the empirical variance of the complete
   paired influence contribution. It is not the variance of the numerator
   alone and not the sum of two marginal variances.
3. The closed-form symmetric benchmark supports asymptotic normality, but the
   current plug-in Wald interval is not ready to replace permutation inference.
4. The next narrow tests should target studentization rather than more broad
   power grids: analytic or cross-fitted density estimates, finite-sample
   sandwich corrections, a bootstrap-t interval based on the complete IF, and
   distribution-level quadrature for skewed margins.
5. A formal theorem must state continuity/positive-density conditions,
   positive radius moments, finite second moment of the complete IF, treatment
   of Huber knots, and the exact iid-pair or cluster-level sampling unit.

## References

- Hampel, F. R. (1974). *The Influence Curve and Its Role in Robust
  Estimation*. Journal of the American Statistical Association.
  https://doi.org/10.1080/01621459.1974.10482962
- van der Vaart, A. W. (1998). *Asymptotic Statistics*, Chapter 20:
  Functional Delta Method.
  https://www.cambridge.org/core/books/asymptotic-statistics/functional-delta-method/734EE290B8542CECFD7D4B981F458C4B
- Rieder, H. (1991). *Min-max asymptotic variance of M-estimates of location
  when scale is unknown*. Statistics & Probability Letters.
  https://doi.org/10.1016/0167-7152(91)90131-A
- Fay, M. P., and Graubard, B. I. (2001). *Small-Sample Adjustments for
  Wald-Type Tests Using Sandwich Estimators*. Biometrics.
  https://doi.org/10.1111/j.0006-341X.2001.01198.x

