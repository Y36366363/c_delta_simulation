# Feedback Response Plan

Professor Hoorn's July 13 feedback identifies several points that need to be
tightened before the simulation results can be treated as report-ready.

## Immediate Corrections

1. Separate permutation resolution from signal strength.
   Increasing the number of extreme observations from `k = 1` to `k = 2` or
   `k = 3` changes both the combinatorial permutation layers and the strength of
   the simulated alternative. The next report should not attribute all power
   gains to the `1 / choose(n, k)` argument.

2. Treat deliberately disjoint subgroups as negative controls, not as genuine
   Type-I nulls.
   A deliberately mismatched design excludes overlap in the observed
   arrangement, while the permutation distribution allows overlap. A valid null
   calibration should generate X and Y extreme indices independently and allow
   chance overlap.

3. Check the algebraic permutation mean.
   The historical implementation had mean raw `c_delta` equal to `n`, which
   exposed the missing `1 / n` factor in the numerator. With the corrected
   normalization, the mean raw `c_delta` over all permutations should be `1`.

4. Classify permutations by extreme-index overlap.
   The p-value is not equal to `1 / choose(n, k)`. That quantity is the size of
   one permutation layer. The permutation statistic should be examined
   conditional on overlap count.

5. Keep raw `c_delta`, normalized `c_delta`, divergence-vector correlation, and
   permutation p-value conceptually separate.

6. Add a revision note for the original paper.
   The numerator should be normalized as
   `(1 / n) * sum_i D_xi D_yi`; otherwise the raw statistic is inflated by a
   factor of `n`.

## Next Simulation Tasks

- Add calibrated alternatives where `k = 1, 2, 3` have comparable descriptive
  signal strength, such as comparable divergence-vector correlations.
- Add p-value quantiles and binomial confidence intervals for rejection rates.
- Repeat main experiments using the absolute-difference version and, later, a
  rank-based version.
- Report what magnitude 8 means relative to each background distribution.
