# Supplement S2. Permutation scope and empirical conditioning evidence

This supplement supplies the evidence cited in Sections 5 and 7. All
permutation rejection frequencies below are **empirical null rejection rates**,
not a demonstrated weak-null Type I error guarantee. The figures retain their
legacy Figure 2 and Figure 3 identifiers; including them here does not record
supervisor approval of their eventual journal placement.

## S2.1 Exact fixed-margin identities

For fixed nonconstant nonnegative profile vectors a,b with positive means,
use empirical variances with divisor n. Permuting b preserves both means,
variances and CVs. Expanding the empirical covariance gives

\[
\widehat C_\pi
=\frac{\bar a\bar b+\operatorname{Cov}_n(a,b_\pi)}{\bar a\bar b}
=1+\widehat\rho_{P,\pi}CV_n(a)CV_n(b).
\]

The multiplier is positive. Thus one-sided ranks agree, as do two-sided
ranks based on absolute distance from the respective null values 1 and 0.
This is an unstudentized identity, not an equivalence for arbitrary
studentizers or tail definitions. Re-pairing raw X and Y also leaves each
marginal sample unchanged, so the median, MAD and Huber fit are unchanged.
The Y-indexed marginal IF vector is permuted along with Y; joint moments,
target reference coefficients and empirical IF variance are recomputed.

Under a permutation-invariant null law, the rank of the observed statistic
on its orbit supplies a valid randomization test with the declared tie
convention. IID pairs with independent X and Y supply such pairing invariance.
The larger null \(\rho_P=0\) does not. In particular, shared signs can make
raw variables dependent despite independent population radii. This manuscript
does not prove a conditional permutation CLT for its weak null. The observed
Wald CLT in Theorem 1 is a different statement. Multiplicity adjustment cannot
repair an invalid local p-value; Holm does not require subset pivotality.

## S2.2 Empirical permutation method

The frozen method uses complete five-moment profile influences with Gaussian
KDE boundary estimates and the same median/MAD/Huber constants as the main
text. For each of B sampled pairings it recomputes joint moments and the
complete studentized statistic \(Z_\pi\). It reports

\[
p_{MC}=\frac{1+\sum_{j=1}^B1\{|Z_{\pi_j}|\ge|Z_{obs}|\}}{B+1},
\]

and rejects when \(p_{MC}\le.05\). Here B=99. This formula describes the
calculation, not a proof of weak-null calibration. Wilson intervals use the
number of independent generated datasets, not B as the denominator.
The function is `profile_studentized_permutation_test` in
`scripts/run_studentized_permutation_weak_null_20260814.py`.

## S2.3 Bridge generating laws and evidence

Let \(X=SR_X,Y=SR_Y\). S is a symmetric sign independent of two independent
radii. Each radius is independently drawn from

\[
(1-\epsilon)\mathcal L\{\exp(.10U)\}+\epsilon Q_f,
\qquad U\sim N(0,1).
\]

The bridge distributions \(Q_f\) are Uniform(0,1), Exponential(rate=1),
\(|N(0,2/\pi)|\) (normal variance \(2/\pi\)), and \(2\operatorname{Beta}(1,2)\).
All have right density one at zero, giving symmetric marginal
\(f(0)=\epsilon/2\). Their independent radii give population
\(T_X=T_Y=0\), \(\rho_P=0,C=1\). Their MADs and Huber active fractions
are evaluated for each mixture; the standardized Jacobian is not replaced
by the median density alone.

The 24-cell panel uses four families, n=80,320 and
epsilon=.05,.10,.20. Each cell has 150 datasets, 99 permutations and 199
bootstrap reference fits per margin for historical diagnostics. The bootstrap fits
are not used to define the displayed population index. Their RNG consumption
must nevertheless be retained to reproduce the original cell stream.
S3.7 gives exact cell seeds and implementation sources.

![Legacy Figure 2. Bridge transition: empirical studentized-permutation evidence only. Whiskers are Wilson intervals across datasets.](../figures/manuscript_figure2_conditioning_bridge_20260905.png)

**Table S2.1. Full bridge panel.** Index is population \(I_n\). Rates and
intervals describe empirical permutation rejection. These rows are the actual
data behind legacy Figure 2, not a proposed future display.

<!-- table:bridge -->
| Family | n | epsilon | Index | Rejection | 95% Wilson |
| --- | --- | --- | --- | --- | --- |
| Exp | 80 | 0.05 | 0.2232 | 0.5000 | [0.4210, 0.5790] |
| Half-normal | 80 | 0.05 | 0.2228 | 0.5667 | [0.4867, 0.6433] |
| Beta | 80 | 0.05 | 0.2229 | 0.5267 | [0.4471, 0.6049] |
| Uniform | 80 | 0.05 | 0.2222 | 0.5267 | [0.4471, 0.6049] |
| Exp | 80 | 0.1 | 0.4456 | 0.2933 | [0.2264, 0.3706] |
| Half-normal | 80 | 0.1 | 0.4437 | 0.4067 | [0.3313, 0.4867] |
| Beta | 80 | 0.1 | 0.4442 | 0.4000 | [0.3250, 0.4800] |
| Uniform | 80 | 0.1 | 0.4412 | 0.3933 | [0.3188, 0.4732] |
| Exp | 80 | 0.2 | 0.8872 | 0.1067 | [0.0667, 0.1662] |
| Half-normal | 80 | 0.2 | 0.8787 | 0.1467 | [0.0989, 0.2121] |
| Beta | 80 | 0.2 | 0.8809 | 0.1533 | [0.1044, 0.2196] |
| Uniform | 80 | 0.2 | 0.8681 | 0.1200 | [0.0773, 0.1817] |
| Exp | 320 | 0.05 | 0.4464 | 0.2333 | [0.1728, 0.3072] |
| Half-normal | 320 | 0.05 | 0.4455 | 0.3000 | [0.2324, 0.3776] |
| Beta | 320 | 0.05 | 0.4458 | 0.3333 | [0.2629, 0.4121] |
| Uniform | 320 | 0.05 | 0.4443 | 0.3800 | [0.3062, 0.4598] |
| Exp | 320 | 0.1 | 0.8912 | 0.0600 | [0.0319, 0.1101] |
| Half-normal | 320 | 0.1 | 0.8873 | 0.1067 | [0.0667, 0.1662] |
| Beta | 320 | 0.1 | 0.8883 | 0.1267 | [0.0826, 0.1894] |
| Uniform | 320 | 0.1 | 0.8824 | 0.1467 | [0.0989, 0.2121] |
| Exp | 320 | 0.2 | 1.7744 | 0.0533 | [0.0273, 0.1017] |
| Half-normal | 320 | 0.2 | 1.7574 | 0.0267 | [0.0104, 0.0666] |
| Beta | 320 | 0.2 | 1.7618 | 0.0533 | [0.0273, 0.1017] |
| Uniform | 320 | 0.2 | 1.7361 | 0.0400 | [0.0185, 0.0845] |
<!-- /table:bridge -->

Across the displayed bridge cells rejection generally declines as the
population index increases. This is an empirical ordering, not direct Wald
theorem validation, a universal cutoff, or a reliability certificate.

## S2.4 Matched-index and prospective family residuals

The matched-index confirmation uses n=320, epsilon=.05, 500 datasets per
family and 99 permutations. The family comparison was selected after the
pilot and uses a larger replication run. In the original implementation the
pilot and confirmation share a cell seed; their first 150 datasets overlap.
Accordingly this is a larger-run confirmation, not an entirely independent
replication of the pilot. It remains separate from the September 9 Wald
pathway study. The source scripts and seed ledger make that overlap explicit.

**Table S2.2. Matched-index confirmation.**

<!-- table:matched -->
| Family | Index | Rejection | 95% Wilson |
| --- | --- | --- | --- |
| Exp | 0.4464 | 0.2320 | [0.1971, 0.2710] |
| Half-normal | 0.4455 | 0.3100 | [0.2710, 0.3519] |
| Beta | 0.4458 | 0.3560 | [0.3153, 0.3989] |
| Uniform | 0.4443 | 0.3340 | [0.2941, 0.3765] |
<!-- /table:matched -->

The scalar index does not determine the rejection rate. Even exact equality
of J would not equate score covariance, target projection, profile variability,
or direct–reference covariance; differences are not identified as purely
higher order.

The prospective fifth bridge is the mixture
\(Q_H=.5\operatorname{Exp}(.5)+.5\operatorname{Exp}(1.5)\), with rates
in parentheses. Its right density at zero is also one. The predictor is a
binomial-logit model with intercept and log population index, fitted on the
old bridge panel before simulating the fifth family's outcomes. It uses six
cells (n=80,320; epsilon=.05,.10,.20), each with 200 datasets and 99
permutations. No bootstrap-reference diagnostic is consumed in this fifth
family's stream.

**Table S2.3. Prospective predictions and observed rejection.**

<!-- table:prospective -->
| n | epsilon | Index | Predicted | Observed | 95% Wilson |
| --- | --- | --- | --- | --- | --- |
| 80 | 0.05 | 0.2234 | 0.5663 | 0.4600 | [0.3923, 0.5292] |
| 80 | 0.1 | 0.4462 | 0.3074 | 0.1950 | [0.1461, 0.2554] |
| 80 | 0.2 | 0.8898 | 0.1314 | 0.0750 | [0.0460, 0.1200] |
| 320 | 0.05 | 0.4467 | 0.3070 | 0.2100 | [0.1593, 0.2716] |
| 320 | 0.1 | 0.8923 | 0.1309 | 0.0500 | [0.0274, 0.0896] |
| 320 | 0.2 | 1.7795 | 0.0489 | 0.0300 | [0.0138, 0.0639] |
<!-- /table:prospective -->

All six predictions exceed the observations. This supports transport of
coarse ordering while preserving a family residual; it does not calibrate
the levels or produce an operational rule.

![Legacy Figure 3. Family residuals unexplained by the index. Both panels use empirical studentized-permutation evidence.](../figures/manuscript_figure3_family_residual_20260905.png)

Figure 3's homogeneity p-value and Cramér's V describe the legacy family
comparison. They are not weak-null validity results for profile correlation.
The accompanying table sources are the frozen September 5 display tables;
their underlying source hashes are verified by the existing display audit.
No family grid has been expanded in assembling this supplement.
