# Teacher-Feedback Validation Summary

Date: 2026-07-30

This update addresses the main mathematical and simulation questions in
Professor Hoorn's response to Follow-up Note 1. The priorities are the
algebraic relationship between corrected `c_delta` and divergence-vector
correlation, scale confounding in the tail gradient, and the separation
between matched and null statistic distributions.

## Algebraic Identity

Let `D_x` and `D_y` be the two divergence vectors, with positive means and
nonzero standard deviations. Using population covariance and standard
deviations,

```text
c_delta
  = mean(D_x D_y) / (mean(D_x) mean(D_y))
  = 1 + cov(D_x, D_y) / (mean(D_x) mean(D_y))
  = 1 + corr(D_x, D_y) CV(D_x) CV(D_y).
```

This confirms that the random-pairing reference is `1`, not `0`. During a
permutation of `D_y`, its mean and standard deviation do not change.
Therefore, `CV(D_x) CV(D_y)` is a fixed positive factor, and corrected
`c_delta` is an increasing affine transformation of the Pearson correlation
between the divergence vectors.

Across 12,000 simulated matched and independent-null datasets and 299
permutations per dataset:

- the maximum numerical identity error was below the reported
  `1e-14` precision;
- the one-sided permutation p-value mismatch count was `0`.

The divergence-vector correlation is therefore mathematically central rather
than an optional diagnostic.

## Common-Scale Tail Validation

The central setting uses `n = 80`, `k = 2`, signal magnitude `8`, 300
repetitions, and 299 permutations. Three background designs were compared:

1. common scale parameter, matching the earlier simulations;
2. common population MAD, using the normal MAD as the reference;
3. common theoretical variance for distributions with degrees of freedom
   greater than `2`.

Under the common scale-parameter design, matched power decreases from normal
to `t2`:

| Kind | Normal | t3 | t2.5 | t2.2 | t2 |
|---|---:|---:|---:|---:|---:|
| L2 | 1.0000 | 0.9267 | 0.8100 | 0.6500 | 0.5433 |
| L1 | 1.0000 | 0.9800 | 0.8433 | 0.7067 | 0.5133 |

After common-MAD scaling, the decline remains but is attenuated:

| Kind | Normal | t3 | t2.5 | t2.2 | t2 |
|---|---:|---:|---:|---:|---:|
| L2 | 1.0000 | 0.9733 | 0.9400 | 0.8033 | 0.7000 |
| L1 | 1.0000 | 1.0000 | 0.9067 | 0.8367 | 0.7433 |

This suggests that the earlier power loss reflects both effective
signal-to-background scale and residual tail-shape effects. The common-MAD
comparison does not remove the tail pattern completely.

The common-variance comparison, excluding `t2`, gives near-ceiling power
through `t2.2`. This requires careful interpretation. Scaling a low-degree
Student-t distribution to unit theoretical variance strongly contracts its
central bulk because much of its variance is carried by rare extremes. A
fixed signal magnitude of `8` then becomes very large relative to typical
finite-sample observations. The result is informative about scale
sensitivity, but it should not be treated as evidence that tail shape is
irrelevant.

Independent-null rejection rates remain broadly compatible with the nominal
`.05` level. The Wilson intervals describe Monte Carlo uncertainty in these
estimated rates; they do not describe uncertainty about whether the
simulation models represent real data.

## Statistic-Distribution Separation

The complete matched and independent-null empirical distributions are
retained in
`results/teacher_feedback_statistic_distributions_20260730.tsv`.

Under the common scale-parameter design, the median matched-minus-null-95th
percentile gap for corrected `c_delta` becomes smaller as the tails become
heavier:

| Kind | Normal | t3 | t2 |
|---|---:|---:|---:|
| L2 | 0.175810 | 0.060001 | 0.001736 |
| L1 | 0.441922 | 0.118644 | 0.015104 |

After common-MAD scaling, the corresponding `t2` gaps increase to `0.027511`
for L2 and `0.054643` for L1, but remain much smaller than under normal
backgrounds.

The same conclusion appears when the matched median is compared with the
median conditional permutation 95th percentile. Under the original scale
design, the gap decreases from `0.183904` to `0.009407` for L2 and from
`0.379873` to `0.013741` for L1 between normal and `t2`.

These distribution-level results are consistent with random background
extremeness, unevenness, and leverage obscuring the planted alignment. They
also show that common robust scaling only partly removes the loss of
separation.

## Reporting Implications

- Mark `1` as the random-pairing reference in plots of corrected `c_delta`, or
  report `c_delta - 1`.
- Treat divergence-vector Pearson correlation as mathematically equivalent
  for one-sided permutation ordering, not as an unrelated secondary metric.
- Regenerate old raw `c_delta` values before a final report.
- Describe Wilson intervals only as Monte Carlo uncertainty intervals.
- Limit current permutation-calibration claims to independent and
  exchangeable settings.
- Keep fixed `k` and fixed `k / n` in separate tables, with exact integer `k`
  values and Wilson intervals.
- Defer Huberized and rank-based variants until their questions and
  calibration plans are pre-specified.
