# Normalization Revision Note

Professor Hoorn reported that the apparent non-unity boundedness issue likely
comes from a missing numerator normalization. The numerator should include a
`1 / n` factor before the paired divergence-product sum.

## Corrected Formula

Let

```text
D_x = (D_{x,1}, ..., D_{x,n})
D_y = (D_{y,1}, ..., D_{y,n})
bar D_x = n^{-1} sum_i D_{x,i}
bar D_y = n^{-1} sum_i D_{y,i}
```

The historical implementation used:

```text
c_delta_old = sum_i D_{x,i} D_{y,i} / (bar D_x bar D_y)
```

The corrected raw statistic is:

```text
c_delta = (1 / n) sum_i D_{x,i} D_{y,i} / (bar D_x bar D_y)
```

Equivalently,

```text
c_delta = c_delta_old / n
```

The same `1 / n` factor must be applied to the sample-dependent maximum pairing
anchor used in this simulation code. Therefore the pairing-normalized value is
unchanged because both numerator and maximum-pairing anchor are divided by `n`.

## Immediate Code Changes

- `c_delta()` now computes the numerator using `mean(D_x * D_y)`.
- `_raw_from_divergences()` now computes the same corrected scale.
- `permutation_mean_check()` now expects the permutation mean to be `1`, not
  `n`.
- Unit tests now check that the corrected raw statistic equals the old raw
  statistic divided by `n`.
- Unit tests also check that the permutation p-value is unchanged by the
  constant `1 / n` scaling.

## What Changes

The following quantities change numerically:

- raw `c_delta`;
- raw bootstrap intervals;
- raw permutation statistics;
- raw means in result tables;
- any statement that said the permutation mean of raw `c_delta` is `n`.

The corrected statement is:

```text
Conditional on D_x and D_y, the mean raw c_delta over all permutations is 1.
```

Older result files generated before this revision should be read as using the
old raw scale. Their raw values should be divided by `n` for the corrected raw
scale.

## What Should Remain Unchanged

The following conclusions should remain unchanged because the correction is a
positive constant scaling within each fixed sample size:

- permutation p-values;
- permutation rejection indicators;
- matched vs. independent-null qualitative comparisons;
- overlap-layer ordering and tail shares;
- divergence-vector Pearson correlation;
- pairing-normalized `c_delta`, because the max-pairing anchor is scaled by the
  same `1 / n` factor.

The sample-size sensitivity conclusions based on rejection rates should remain
valid. However, raw-scale interpretations in large-sample summaries should be
updated if raw values are reported directly.

## Revision Item for the Paper

The original paper should revise the numerator normalization in the definition
of `c_delta`. A concise revision note could be:

```text
The numerator should be normalized by 1/n. Without this factor, the raw
coefficient is inflated by sample size, which explains the apparent non-unity
boundedness issue. The corrected numerator is the empirical mean of the paired
divergence products rather than their unnormalized sum.
```

## Next Verification Step

The next step is to re-run a compact set of summaries after the correction:

1. exact and Monte Carlo permutation mean checks;
2. one lower-target calibrated subgroup check;
3. one L1/L2 comparison check;
4. the flagged `l1/lognormal/n=160/k=1` independent-null check.

The main purpose is not to rediscover the same rejection rates, but to ensure
all reported raw-scale quantities are on the corrected scale.

## Follow-up Result

The flagged `l1/lognormal/n=160/k=1` independent-null condition was re-run with
1,000 replications and 999 permutations. The empirical size at alpha `.05` was
`0.053`, with Wilson interval `[0.0407, 0.0687]`. This suggests that the earlier
`0.0767` value was likely simulation variability rather than stable
over-rejection.
