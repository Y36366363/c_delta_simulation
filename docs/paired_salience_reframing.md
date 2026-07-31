# Paired-Salience Reframing

Date: 2026-07-31

This note examines Professor Hoorn's proposed reinterpretation:

> `c_delta` is not a new general correlation of internal structures, but a test
> of whether the same paired observations stand out from their respective
> groups in both datasets.

The main conclusion is that this is substantially correct for the current
one-dimensional implementation. A precise version should use
**paired observation-level salience profiles** rather than imply that the test
only detects a few binary outliers.

## Exact Meaning of One-Dimensional L2 Divergence

For

```text
D_i^2 = (1 / (n - 1)) sum_{j != i} (x_i - x_j)^2,
```

let

```text
x_bar = mean(x)
s_x^2 = (1 / n) sum_j (x_j - x_bar)^2.
```

Then

```text
sum_j (x_i - x_j)^2
    = n (x_i - x_bar)^2 + n s_x^2,
```

so

```text
D_i^2
    = n / (n - 1) * ((x_i - x_bar)^2 + s_x^2).
```

Therefore:

- `D_i` is a strictly increasing function of `|x_i - x_bar|`;
- the L2 divergence ranking is exactly the absolute-deviation-from-mean
  ranking;
- the full `n x n` pairwise distance matrix is compressed into `n`
  observation-level outlyingness or salience scores.

Together with the earlier identity,

```text
c_delta = 1 + corr(D_x, D_y) CV(D_x) CV(D_y),
```

the one-sided permutation test is exactly a test of positive Pearson
association between the two paired salience vectors.

For L1,

```text
D_i = (1 / (n - 1)) sum_{j != i} |x_i - x_j|,
```

which is the average absolute distance of observation `i` from the group. It
does not have the same quadratic closed form, but it is still a row-level
centrality/outlyingness summary, minimized near the sample median and
increasing toward the tails.

## Information Lost by Row Aggregation

The mapping

```text
full pairwise distance matrix -> row divergence vector
```

is many-to-one. Different pairwise configurations can produce the same or very
similar row summaries. The current coefficient therefore does not compare
general pairwise internal geometry.

This distinction is central:

- full internal relational structure concerns all `n(n-1)/2` pairwise
  distances;
- `c_delta` uses only `n` row aggregates;
- the permutation test asks whether large and small row aggregates are aligned
  at corresponding observation indices.

## Simulation Design

The paired-salience validation uses:

- `n = 80`;
- 500 repetitions and 499 permutations;
- L2 and L1 divergence;
- independent signs so raw Pearson association is approximately zero;
- unique continuous magnitudes so observation-level exchangeability is
  preserved.

Scenarios:

1. `diffuse_aligned`: all magnitudes lie in `[0.8, 1.2]` and the continuous
   salience profile is aligned with small noise;
2. `diffuse_null`: the same narrow profile is randomly paired;
3. `diffuse_reverse`: high salience in one dataset is paired with low salience
   in the other;
4. `full_profile_aligned`: a wider continuous profile is aligned;
5. `top_pair_only`: only the two largest moderate magnitudes are aligned and
   the rest are shuffled;
6. `profile_null`: the wider profile is randomly paired;
7. `sparse_extreme_aligned`: two magnitude-4 observations are aligned.

The null scenarios reject at `0.044-0.050`, supporting the observation-level
permutation calibration in this design.

## Main Results

| Kind | Scenario | Rejection | Divergence corr. | Raw Pearson | Full distance-matrix corr. | Max/median abs. dev. |
|---|---|---:|---:|---:|---:|---:|
| L2 | diffuse aligned | 0.976 | 0.6158 | -0.0013 | 0.0099 | 1.3025 |
| L2 | diffuse null | 0.046 | -0.0017 | 0.0051 | 0.0005 | 1.3023 |
| L2 | full profile aligned | 1.000 | 0.9231 | -0.0003 | 0.1674 | 1.8828 |
| L2 | top pair only | 0.186 | 0.0909 | 0.0004 | 0.0178 | 1.8558 |
| L2 | sparse extreme aligned | 1.000 | 0.9616 | 0.0275 | 0.3202 | 4.0490 |
| L1 | diffuse aligned | 0.800 | 0.4042 | -0.0053 | 0.0090 | 1.3060 |
| L1 | diffuse null | 0.050 | -0.0047 | 0.0000 | -0.0012 | 1.3037 |
| L1 | full profile aligned | 1.000 | 0.8752 | 0.0030 | 0.1676 | 1.8796 |
| L1 | top pair only | 0.220 | 0.1115 | -0.0038 | 0.0165 | 1.8627 |
| L1 | sparse extreme aligned | 1.000 | 0.9559 | -0.0072 | 0.3208 | 4.0497 |

## Interpretation

### The teacher's central correction is supported

The coefficient is not a general dependence measure or a general correlation
of full internal structures. It detects whether corresponding observations
have aligned divergence salience relative to their own groups.

### "Stand out" need not mean a few extreme outliers

In the diffuse-aligned scenario:

- no observation is extremely separated;
- the maximum absolute deviation is only about `1.30` times the median;
- raw Pearson correlation is approximately zero;
- full pairwise-distance-matrix correlation is approximately zero;
- L2 rejection is `0.976` and L1 rejection is `0.800`.

Thus, the test can detect a distributed continuous salience profile even when
there is no small extreme subgroup.

### A few aligned moderate standouts are not sufficient by themselves

When only the two largest moderate observations are aligned and the rest of
the profile is shuffled:

- L2 power is `0.186`;
- L1 power is `0.220`.

When two much stronger magnitude-4 observations are aligned, power is `1.000`
under both versions. Detection depends on both the number of aligned
observations and their leverage relative to the rest of the salience profile.

### Raw c_delta values near 1 can still be significant

For diffuse L2 alignment:

```text
mean c_delta = 1.0033
mean divergence correlation = 0.6158
rejection rate = 0.976.
```

The raw coefficient remains close to `1` because the divergence vectors have
low coefficients of variation. This reinforces the need to report the
divergence correlation or permutation p-value, rather than interpreting raw
distance from `1` without the CV factor.

### The test is one-sided in the current implementation

The diffuse-reverse scenario produces strongly negative divergence
correlation but zero upper-tail rejection. A separate lower-tail or two-sided
test would be needed if negative salience alignment were scientifically
meaningful.

## Position Relative to Existing Methods

### Distance correlation

Distance covariance/correlation uses double-centered full distance matrices
and is a general dependence measure; under its conditions, zero distance
correlation characterizes independence. The current coefficient instead
correlates row-level divergence summaries and does not characterize general
independence.

Reference:
Székely, Rizzo, and Bakirov (2007), *The Annals of Statistics*,
DOI `10.1214/009053607000000505`.

### HSIC

HSIC measures dependence through the Hilbert-Schmidt norm of an RKHS
cross-covariance operator. It is also designed as a general independence
criterion, not a paired-salience test.

Reference:
Gretton et al. (2005), *Algorithmic Learning Theory*,
DOI `10.1007/11564089_7`.

### Energy distance and MMD

Energy distance and MMD compare probability distributions in two-sample
problems. Pairing of observation indices is not their defining target. They
answer whether distributions differ, not whether the same observations are
relatively salient within their own groups.

References:

- Székely and Rizzo (2013), *Journal of Statistical Planning and Inference*,
  DOI `10.1016/j.jspi.2013.03.018`;
- Gretton et al. (2012), *Journal of Machine Learning Research*, 13,
  723-773.

### Mantel-type distance-matrix correlation

A Mantel-type statistic correlates corresponding entries of two full distance
matrices and is closer to a literal comparison of internal pairwise structure.
The current `c_delta` collapses each row before correlation, so it is a
different and more compressed target.

Reference:
Mantel (1967), *Cancer Research*, 27, 209-220.

## Recommended Reframing

Preferred concise description:

> In its current one-dimensional form, `c_delta` is a permutation-calibrated
> measure of positive alignment between paired observation-level divergence
> salience profiles. It tests whether observations that are relatively
> peripheral or central in one dataset tend to be similarly peripheral or
> central in the other.

Avoid:

- "a new general correlation of internal structures";
- "a general dependence measure";
- "a test only for shared outliers";
- "near zero means unrelated."

## Consequences for the Paper

1. The title, abstract, and introduction may require substantial reframing.
2. The primary estimand should be described as paired divergence salience
   alignment.
3. The one-dimensional L2 closed form should be stated explicitly.
4. Claims of novelty should focus on the chosen salience construction,
   interpretation, extensions, or applications rather than general
   correlation.
5. Distance correlation, HSIC, energy distance, MMD, and Mantel methods should
   be separated by the statistical question they answer.
6. A multivariate extension may be more interesting, but row aggregation still
   cannot retain general pairwise geometry.
7. Negative alignment requires a lower-tail or two-sided alternative if it is
   scientifically relevant.

## Suggested Next Checks

1. Repeat diffuse-salience validation across `n`, noise level, and profile
   width.
2. Compare one-sided, lower-tail, and two-sided permutation alternatives.
3. Quantify information loss by constructing distance matrices with similar
   row summaries but different pairwise entries.
4. Compare directly with a full distance-matrix statistic under matched
   geometry and matched-salience alternatives.
