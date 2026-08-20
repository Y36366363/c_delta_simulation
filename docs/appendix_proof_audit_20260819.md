# Independent audit of the asymptotic appendix

Date: 2026-08-19

## Verdict

The derivative chain and finite-dimensional delta method are internally
consistent, but the pre-audit appendix was not yet a complete proof of the
primary \(\rho_P\) theorem or of the in-sample sandwich variance. The audit
found two substantive gaps:

1. the moment condition inherited from the \(C\) proof was too weak for
   \(\rho_P\);
2. pointwise plug-in convergence was incorrectly used as if it implied
   convergence of the empirical second moment.

Both gaps are repaired in the revised appendix through separate moment
conditions, an explicit local empirical-process assumption, and three new
lemmas. The revised result is a defensible high-level theorem. It is not yet a
fully primitive entropy proof suitable for publication without citations and
an external mathematical check.

## Finding 1: the old moment condition was insufficient

The influence function for \(C\) contains direct terms of orders

\[
ab,\quad a,\quad b,
\]

plus bounded median/MAD/Huber nuisance contributions. Its finite variance
therefore requires the corresponding second moments.

The influence function for \(\rho_P\) additionally contains

\[
a^2-q_a,\qquad b^2-q_b.
\]

Squaring these terms requires \(E(a^4)\) and \(E(b^4)\). The previous
assumption

\[
E(a^{2+\eta}+b^{2+\eta}+(ab)^{2+\eta})<\infty
\]

did not guarantee this when \(0<\eta<2\).

### Resolution

The revised appendix separates:

\[
\text{A5-C:}\quad
E\{a^{2+\eta}+b^{2+\eta}+(ab)^{2+\eta}\}<\infty
\]

from

\[
\text{A5-}\rho:\quad
E\{a^{4+\eta}+b^{4+\eta}+(ab)^{2+\eta}\}<\infty.
\]

This matters scientifically: choosing the bounded effect scale \(\rho_P\)
does not make its ordinary sample-correlation influence bounded. Estimating
the two profile variances still introduces fourth-moment requirements.

There is an important weak-null refinement. At \(\rho_P=0\), the gradient
coefficients on \(q_a\) and \(q_b\) are zero. Corollary A.2 therefore uses
A5-C-type moments for the first-order zero-correlation test. Fourth marginal
moments remain the clean condition for confidence intervals at arbitrary
nonzero \(\rho_P\), but they are not imposed as an unnecessary universal
requirement on the main weak-null test.

## Finding 2: stochastic equicontinuity had been asserted, not shown

Replacing a fixed centre by \(\widehat T\) creates terms such as

\[
\mathbb G_n\{f_{\widehat\theta}-f_{\theta_0}\}.
\]

Consistency or even root-\(n\) consistency of \(\widehat\theta\) does not by
itself make these terms negligible. A local Donsker condition and
\(L_2(P)\)-continuity are needed.

### Resolution

Lemma A.3 now identifies the relevant classes:

- threshold indicators for median and MAD;
- bounded Huber score translations and rescalings;
- translated absolute residuals;
- their paired product;
- squared residuals for the profile-correlation denominator.

The indicator classes are VC-type. The moment classes are
finite-dimensional Lipschitz/Euclidean classes. Explicit inequalities show
that their local \(L_2(P)\) semimetric goes to zero with the nuisance
parameter. Under the strengthened moments, asymptotic equicontinuity gives

\[
\mathbb G_n(f_{\widehat\theta}-f_{\theta_0})=o_P(1).
\]

## Finding 3: pointwise plug-in convergence was not enough

The earlier proof effectively argued:

\[
\widehat{IF}(z)\to IF(z)
\quad+\quad\text{uniform integrability}
\quad\Longrightarrow\quad
P_n\widehat{IF}^{\,2}\to PIF^2.
\]

That implication skips the fact that \(\widehat{IF}\) is random and evaluated
on the same empirical sample \(P_n\).

### Resolution

The revised proof separates two steps:

1. function-norm convergence,

   \[
   \|\widehat{IF}-IF\|_{P,2}=o_P(1);
   \]

2. a Glivenko–Cantelli result for the localized squared influence class.

It then uses

\[
\begin{aligned}
P_n\widehat{IF}^{\,2}-PIF^2
=&(P_n-P)(\widehat{IF}^{\,2}-IF^2)\\
&+P(\widehat{IF}^{\,2}-IF^2)
+(P_n-P)IF^2.
\end{aligned}
\]

The local squared-class GC property controls the first term, \(L_2\)
convergence controls the second, and the ordinary law of large numbers
controls the third.

## Finding 4: random density evaluation needed an explicit route

The median and MAD-boundary density estimates are evaluated at random
consistent points. Pointwise KDE consistency at fixed population points does
not automatically justify this substitution.

### Resolution

A7 now assumes local uniform density consistency. It also records a standard
sufficient bandwidth route:

\[
h_n\to0,\qquad nh_n/\log(1/h_n)\to\infty,
\]

together with local uniform continuity and boundedness of the density and the
standard kernel-class entropy conditions.
Then

\[
\sup_{t\in N}|\widehat f(t)-f(t)|=o_P(1)
\]

implies consistency at \(\widehat m\) and
\(\widehat m\pm\widehat d\).

## Finding 5: 2026-08-20 closure update

The three proof-completion items identified by the audit have now been
resolved at draft level. Every A8 subclass is mapped to an explicit
VC-subgraph or compact finite-dimensional Lipschitz theorem; Theorem 2.1 of
van der Vaart and Wellner (2007) is used for the random estimated index; and
the code's exact NumPy midpoint median/MAD convention is recorded. Its
difference from the generalized-inverse convention is O_P(n^{-1}) by the
central-spacing argument and is confirmed by a fixed-seed normal/skew audit.

An external mathematical review remains appropriate, especially for the
estimated-centre MAD spacing step and the piecewise VC decompositions. The
conditional combinatorial CLT is a separate theorem, not a missing line in
the iid Wald argument, and is not required under the current paper scope.
See `entropy_mad_permutation_decision_20260820.md`.

## Primary-source cross-check

The audit was checked against:

- van der Vaart and Wellner, *Empirical processes indexed by estimated
  functions*, which treats conditions under which an estimated index can be
  replaced by its population limit:
  https://arxiv.org/abs/0709.1013
- Giné and Guillou, *Rates of strong uniform consistency for multivariate
  kernel density estimators*, which supplies uniform stochastic KDE rates
  under explicit bandwidth and kernel-class assumptions:
  https://numdam.org/item/AIHPB_2002__38_6_907_0/
- Mazumder and Serfling, *Bahadur representations for the median absolute
  deviation and its modifications*, which proves weak and strong Bahadur
  representations for sample MAD with an estimated sample median:
  https://doi.org/10.1016/j.spl.2009.05.006

## Claim boundary after audit

Safe:

> Under the revised regularity, moment, and local empirical-process
> conditions, the iid Huber-profile correlation and \(C\) estimators are
> asymptotically linear and normal, and their complete plug-in influence
> variances are consistent.

Not yet safe:

> The displayed primitive density and moment assumptions alone imply every
> entropy condition automatically in all allowed distributions.

Also not yet safe:

> Fully recomputed studentized permutation is theorem-level valid under every
> regular weak null.
