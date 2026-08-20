# Entropy mapping, sample-MAD convention, and permutation-theorem decision

Date: 2026-08-20

## Executive decision

The iid Wald appendix can now be completed without treating A8 as an opaque
appeal to a single standard result. Each class has a direct VC-subgraph or
finite-dimensional Lipschitz route, and random-nuisance substitution is an
application of Theorem 2.1 of van der Vaart and Wellner (2007).

The implementation uses the NumPy midpoint convention for both the sample
median and the median of absolute deviations. This is not exactly the
generalized-inverse empirical quantile when n is even, but under A2 their
difference is of central-spacing order, hence O_P(n^{-1}) and
o_P(n^{-1/2}). The same first-order median/MAD influence representation
therefore applies. A fixed-seed audit checks the predicted scale under normal
and skewed continuous distributions.

A conditional weak-null permutation CLT is not required for the present
three-claim paper. The paper should use the iid studentized Wald result for the
weak null and reserve finite-sample permutation validity for the strong
group-invariance null. The conditional CLT becomes necessary only if
fully-recomputed studentized permutation is promoted to a headline weak-null
theorem or the primary reported inferential procedure.

## 1. Class-by-class theorem matching

The references below are van der Vaart and Wellner (1996), abbreviated VW,
unless otherwise stated. The common route is:

1. establish VC-subgraph structure or a polynomial Euclidean covering bound;
2. use VW Theorem 2.6.7 for polynomial covering numbers of VC-subgraph
   classes and the uniform-entropy Donsker theorem, VW Theorem 2.5.2 and its
   VC corollary Theorem 2.6.8, with an L2 envelope;
3. use van der Vaart (1998), Example 19.7, for compact finite-dimensional
   parameter classes satisfying an L2 Lipschitz bound;
4. use VW Section 2.10, in particular Theorem 2.10.20, for the finite sums,
   differences, and compositions appearing in the influence formula;
5. invoke Theorem 2.1 of van der Vaart and Wellner (2007) after proving
   L2-continuity at the estimated nuisance.

| Displayed subclass | Exact route | Envelope and continuity |
|---|---|---|
| half-line indicator 1(w <= t) | Half-lines form a VC set class; VW 2.6.7 plus 2.5.2/2.6.8 | Envelope 1; L2 distance is the probability mass between thresholds |
| interval indicator 1(abs(w-m) <= d) | Intervals form a VC set class; equivalently intersect two half-lines using VW VC closure | Envelope 1; continuity follows from no mass at m plus or minus d |
| sign(w-T) | Affine transformation of a half-line indicator; VW Section 2.10 closure | Envelope 1; continuity follows from no mass at T |
| clipped Huber score psi_c((w-T)/(kd)) | On a compact parameter set with d bounded below, this is a bounded finite-dimensional Lipschitz class; van der Vaart (1998), Example 19.7 | Constant envelope c; the parameter Lipschitz coefficient is bounded because clipping restricts scale sensitivity |
| active indicator 1(abs(u) < c) | Indicator of an interval with endpoints T plus or minus ckd; a two-parameter VC set class | Envelope 1; A3 excludes mass at both knots |
| active score u 1(abs(u) < c) | Piecewise-linear finite-dimensional VC-subgraph class: split at the two Huber knots and apply VW Lemmas 2.6.17-2.6.18 | Envelope c; A3 provides L2 continuity despite the jump at the knots |
| w-T and abs(w-T) | Compact one-parameter Lipschitz classes; van der Vaart (1998), Example 19.7 | Envelope abs(w)+M in L2 |
| squared radius (w-T)^2 | Compact one-parameter Lipschitz class with coefficient 2 abs(w)+2M | L2 envelope requires a fourth marginal moment for general-rho Donsker use |
| paired radius abs(x-T_X) abs(y-T_Y) | Compact two-parameter Lipschitz class; Example 19.7 | An L2 envelope is controlled by 1+abs(xy)+abs(x)+abs(y) |
| sign-times-radius classes | Split into x <= T_X and x > T_X and the two linear pieces of abs(y-T_Y); the subgraphs are finite unions/intersections of negativity sets of finite-dimensional affine functions, hence VC by VW Lemmas 2.6.17-2.6.18 | Envelope abs(y)+M, or its x analogue; boundary mass exclusions give L2 continuity |
| finite influence-function closure | Finite scalar sums, differences, products with convergent scalar coefficients, and smooth denominator maps; VW 2.10.20 supplies the entropy closure | Denominators are bounded away from zero on Theta_0 |
| squared influence class | First truncate the influence envelope at K, apply the Lipschitz square map and VW 2.10.20, then let K grow | The tail is uniformly bounded by P[I^2 1(I>K)], which vanishes because the squared influence envelope is integrable |

This mapping is deliberately local. It does not claim that every unbounded
product of arbitrary Donsker classes is Donsker. The displayed piecewise
finite-dimensional form and the stated moment envelopes are doing essential
work.

### Random estimated functions

Theorem 2.1 of van der Vaart and Wellner (2007) states the needed replacement
result directly: if the localized joint class is P-Donsker and

P(f_{theta,eta_hat} - f_{theta,eta_0})^2 -> 0

in probability, the empirical process indexed by the estimated function may
be replaced by the population-indexed process. The inequalities in Lemma A.3
and the boundary no-mass conditions establish precisely this L2 condition.

Consequently, root-n consistency is useful for the nuisance expansion, but
consistency plus local L2 continuity and Donsker control is what removes the
random-index empirical-process remainder.

## 2. Exact sample median and MAD convention

The two production paths, huber_reference_profile and
_huber_location_influence, both calculate

median_np = numpy.median(W_1,...,W_n)

and

mad_np = numpy.median(abs(W_i - median_np)).

Thus, for n=2r without ties,

median_np = (W_(r) + W_(r+1))/2.

The second median uses the same midpoint rule on the ordered deviations from
that midpoint centre. For odd n it is the central order statistic. No finite
sample consistency multiplier is applied to MAD itself; k=1.4826 is applied
afterward to form the normal-consistent Huber scale.

By contrast, the generalized-inverse empirical median is W_(r) for n=2r.
The two conventions are genuinely different. For the sample
(0,1,4,10), the NumPy and lower medians are 2.5 and 1, and the corresponding
MADs are 2 and 1.

### First-order equivalence

Under a positive continuous density at m, the central spacing
W_(r+1)-W_(r) is O_P(n^{-1}). Therefore the midpoint and lower empirical
medians differ by O_P(n^{-1}). Under positive continuous densities at the two
MAD boundaries, the induced change in the empirical absolute-deviation
distribution and its central spacing give

mad_np - mad_lower = O_P(n^{-1}).

Both differences are o_P(n^{-1/2}); hence they have the same Bahadur linear
term and influence functions in Lemma A.1. This is consistent with Mazumder
and Serfling (2009), who establish weak and strong Bahadur representations for
sample MAD with an estimated sample median. The convention equivalence here
is an additional central-spacing argument, not a claim that their finite
sample statistic must use NumPy's interpolation rule.

There is also no estimating-equation conflict. With continuous data and even
n, both the midpoint and lower median satisfy the empirical half-mass equation
exactly under the less-than-or-equal convention; with odd n, the discrepancy
is only 1/(2n). The analogous statement holds for the deviation median.

### Fixed-seed numerical audit

The script scripts/audit_mad_convention_20260820.py compares the NumPy pair
with the generalized-inverse lower-quantile pair at n=40,80,160,320,640,
using 6,000 repetitions per cell, seed 20260820, under standard normal and
lognormal log-SD 1.1 sampling. It reports Monte Carlo uncertainty for the mean
absolute convention gap and both root-n and n-scaled summaries.

The numerical audit is a diagnostic confirmation of the rate argument, not
the proof of it. It cannot validate discrete or near-degenerate cases, which
are intentionally outside A2.

The predicted separation is clear. From n=40 to n=640, the median of the
root-n-scaled absolute MAD convention gap fell from 0.128 to 0.032 under the
normal law and from 0.171 to 0.044 under the lognormal law. In contrast, the
n-scaled median absolute MAD gap stayed approximately stable: 0.80--0.83 for
normal sampling and 1.08--1.10 for lognormal sampling. The mean absolute gaps
at n=640 were 0.00170 (MCSE 0.000020) and 0.00214 (MCSE 0.000023),
respectively. This is the numerical signature of O_P(n^{-1}), hence confirms
that the convention difference disappears on the root-n theorem scale.

## 3. Decision on a weak-null conditional permutation CLT

### What is already proved

- The iid estimator has an asymptotically linear, studentized Wald limit under
  the regular weak null.
- A fully recomputed permutation test is finite-sample exact when the joint
  law is invariant under the chosen permutation group.
- Existing simulations suggest that full recomputation and studentization can
  repair much of the ordinary weak-null permutation distortion in regular
  settings, but not near nonregular reference fitting.

### What the missing theorem would add

It would show, conditional on the observed triangular array, that the orbit
distribution of the fully recomputed studentized statistic converges to the
same standard normal law under rho_P=0 without full exchangeability. This
requires both a combinatorial CLT and uniform conditional consistency of the
recomputed nuisance fit and studentizer. It is not a corollary of the iid
functional delta method.

### Scope decision

Do not complete that theorem for the current manuscript unless Professor
Hoorn decides that weak-null permutation inference itself is a main claim.
Under the frozen paper architecture it would create a fourth contribution and
would not strengthen the central explanation of near-degenerate failure by
sqrt(n) sigma_min(J).

The safe reporting rule is:

1. use the influence-function Wald statistic for formal regular-iid weak-null
   inference;
2. call permutation exact only under the stated random-pairing or conditional
   group-invariance null;
3. retain fully recomputed studentized weak-null permutation as empirical
   sensitivity evidence, explicitly without theorem-level validity;
4. reopen the conditional CLT only if permutation becomes the primary method,
   the title or abstract promises robust weak-null permutation validity, or a
   reviewer makes that result necessary.

DiCiccio and Romano (2017) confirms that this is a genuine theorem category:
ordinary correlation permutation can fail under zero correlation, while a
properly studentized version can attain asymptotic validity. Their result
supports feasibility, but it does not automatically cover the estimated
Huber/MAD salience profiles used here.

## Sources

- van der Vaart, A. W., and Wellner, J. A. (1996), Weak Convergence and
  Empirical Processes, especially Theorems 2.5.2, 2.6.7, 2.6.8 and 2.10.20,
  and Lemmas 2.6.17-2.6.18.
- van der Vaart, A. W. (1998), Asymptotic Statistics, Example 19.7.
- van der Vaart, A. W., and Wellner, J. A. (2007), Empirical processes indexed
  by estimated functions: https://arxiv.org/abs/0709.1013
- Mazumder, S., and Serfling, R. (2009), Bahadur representations for the
  median absolute deviation and its modifications:
  https://doi.org/10.1016/j.spl.2009.05.006
- DiCiccio, C. J., and Romano, J. P. (2017), Robust permutation tests for
  correlation and regression coefficients:
  https://doi.org/10.1080/01621459.2016.1202117
