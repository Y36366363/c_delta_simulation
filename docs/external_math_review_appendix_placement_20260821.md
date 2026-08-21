# External mathematical review and final appendix placement

Date: 2026-08-21

## Verdict

The regular-iid theorem remains defensible after external source matching,
with one strengthening and one presentation correction:

1. the project's NumPy midpoint median and midpoint MAD are not merely
   first-order equivalent to the statistic in the principal MAD reference;
   they are exactly the sample convention defined by Mazumder and Serfling
   (2009);
2. the class-by-class entropy ledger is useful verification, but it is too
   technical for the main manuscript appendix. The main appendix should state
   the local empirical-process condition, give a concise verification
   proposition, and send the full Boolean/entropy and truncation ledger to an
   online supplement.

No theorem claim needs to be withdrawn. The remaining risk is ordinary
publication-level checking of measurability and piecewise-VC bookkeeping, not
a missing first-order argument.

## 1. External source audit

### Exact sample MAD convention

Mazumder and Serfling define, for ordered observations, the sample median as
the average of the two central indexed order statistics and define sample MAD
by applying the same average-of-two-central-values rule to

W_i^* = |X_i - Med_n|.

This is exactly numpy.median followed by numpy.median of the absolute
deviations. Their Assumption (W) requires continuity near the two MAD
boundaries, differentiability at the median and both boundaries, positive
median density, and positive sum of the two boundary densities. Their Theorem
2 gives an o_P(n^{-1/2}) weak Bahadur remainder. The project's A2 is at least
as strong locally, because it assumes a continuous strictly positive density
in neighbourhoods of all three points.

Therefore Lemma A.1 can cite that theorem directly for the actual estimator.
The lower-generalized-inverse comparison remains a useful software sensitivity
audit, but it is no longer part of the logical bridge to the Bahadur theorem.

### MAD asymmetry sign

For a contamination point z, differentiating

F(m+d) - F(m-d) = 1/2

gives

IF_d(z) = [1/2 - 1{|z-m| <= d}
           - {f(m+d)-f(m-d)} IF_m(z)]
          / {f(m+d)+f(m-d)}.

Because typography in extracted PDF text can obscure the sign and fraction
boundaries, the sign was checked independently against a population
contamination path under a skew lognormal distribution. At the 0.99
contamination quantile, the analytic MAD influence was approximately 0.65013
and the epsilon=10^-6 finite difference agreed within 2e-6. Reversing the
endpoint-density sign missed by approximately 0.46. The existing code and
appendix sign are therefore retained.

### Estimated-function replacement

Theorem 2.1 of van der Vaart and Wellner (2007) exactly matches Lemma A.3:
localize the estimated nuisance to a fixed set, require the joint class to be
P-Donsker, and verify

P(f_{theta,eta_hat} - f_{theta,eta_0})^2 -> 0.

The appendix supplies the last condition through explicit Lipschitz bounds
and no-boundary-mass arguments. Root-n consistency alone is not being used as
a substitute for stochastic equicontinuity.

### VC and Euclidean classes

The external theorem chain is internally consistent:

- van der Vaart and Wellner (1996), Theorem 2.6.7, supplies polynomial
  covering bounds for VC-subgraph classes;
- their uniform-entropy Donsker theorem and VC corollary supply Donsker
  conclusions under square-integrable envelopes;
- finite unions/intersections and negativity sets of finite-dimensional
  vector spaces cover half-lines, intervals, active Huber regions, and the
  four sign-times-radius pieces;
- compact finite-dimensional L2-Lipschitz parameter classes cover the
  translated radius, squared radius, paired product, and clipped Huber score.

The sign-times-radius identity was also checked numerically over 10,000 fixed-
seed draws by reconstructing its four affine pieces; maximum discrepancy was
zero. This is a safeguard against an algebraic partition mistake, not a
numerical proof of the VC theorem.

### Squared influence Glivenko--Cantelli step

The cleanest citation is the preservation result of van der Vaart and Wellner
for continuous transforms of finitely many Glivenko--Cantelli classes with an
integrable envelope. Squaring is continuous, and A5-C or A5-rho gives an
integrable squared influence envelope. Truncation is a transparent optional
proof device, but the appendix should not present Theorem 2.10.20 as if it
alone handled unbounded tails. The integrable-envelope preservation condition
is essential and is now stated explicitly.

## 2. Remaining claim boundary

Safe at theorem level:

- pointwise iid asymptotic linearity and normality under A1--A8;
- consistency of the complete plug-in influence variance under the stated
  moment and local GC conditions;
- the weaker moment route for the null-restricted rho_P test;
- exact randomization inference under the declared group-invariance null.

Still not safe:

- uniform validity as sqrt(n) sigma_min(J) remains bounded;
- a universal finite-sample cutoff for the conditioning index;
- weak-null permutation validity without the missing conditional CLT;
- room-level iid inference when buildings are the independent units;
- extending the continuous-margin MAD theorem to atoms or zero-density
  boundaries.

## 3. Final placement decision

### Main manuscript Appendix A

Keep only material required to support Main Claims 1 and 3:

1. scope, notation, and A1--A8;
2. median/MAD influence lemma, now with the exact Mazumder--Serfling
   convention citation;
3. Huber-location implicit derivative and nuisance Jacobian;
4. joint moment and rho_P/C influence formulas;
5. one concise empirical-process verification proposition;
6. asymptotic linearity, plug-in variance, and studentized Wald theorem;
7. the nonuniformity statement involving sqrt(n) sigma_min(J).

This appendix should be readable as a complete proof roadmap without forcing
the reader through every subgraph decomposition.

### Online Supplement S1

Move the technical proof ledger here:

1. exact class-by-class VC/Euclidean mapping and envelopes;
2. four-piece sign-times-radius decomposition;
3. detailed L2-continuity inequalities;
4. squared-influence GC preservation and truncation details;
5. exact sample convention quotation/formula and the lower-quantile
   sensitivity audit;
6. fixed-seed numerical safeguards in
   results/external_math_review_checks_20260821.tsv.

### Online Supplement S2 or a short methods note

Place the fixed-margin C/rho_P permutation equivalence and exact
group-invariance proposition here. Keep one sentence in the main text
distinguishing the weak null from the exchangeability null.

No conditional weak-null permutation CLT should be added under the current
paper scope. If permutation inference later becomes a headline method, it
should receive its own theoretical section rather than being inserted into
Appendix A.

## 4. Sources checked

- Mazumder, S., and Serfling, R. (2009), Bahadur representations for the
  median absolute deviation and its modifications:
  https://doi.org/10.1016/j.spl.2009.05.006
- van der Vaart, A. W., and Wellner, J. A. (1996), Weak Convergence and
  Empirical Processes:
  https://doi.org/10.1007/978-1-4757-2545-2
- van der Vaart, A. W., and Wellner, J. A. (2007), Empirical processes indexed
  by estimated functions:
  https://arxiv.org/abs/0709.1013
- van der Vaart, A. W., and Wellner, J. A. (2000), Preservation theorems for
  Glivenko--Cantelli and uniform Glivenko--Cantelli classes:
  https://doi.org/10.1007/978-1-4612-1358-1_9
- NumPy quantile documentation, for the implemented default interpolation
  convention:
  https://numpy.org/doc/stable/reference/generated/numpy.quantile.html
