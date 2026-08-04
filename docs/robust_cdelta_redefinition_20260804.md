# Robust Redefinition of c_delta: Theory and First Validation

Date: 2026-08-04

## Bottom Line

The proposed changes solve two different problems and should not be conflated.

1. **Robust centre, retained outlier signal.** Estimate the ordinary-group
   centre without flagged extremes, then score every observation, including
   the flagged values. This prevents an extreme value from moving the reference
   centre while preserving its scientific role as a standout.
2. **Bounded final influence.** In addition, cap or smoothly downweight large
   distances. This prevents one matched extreme from dominating the final
   paired-salience statistic, but necessarily reduces power for scientifically
   meaningful matched extremes.

For the project's current estimand - whether the same paired observations are
relatively salient in their respective groups - the first should be the main
candidate. The second should be a pre-specified robustness analysis rather than
an automatic replacement.

The expanded grid favours a Huber-fitted centre for the first candidate. A
Huber centre has a clear M-estimation objective and bounded score contribution
during centre fitting; it was more stable than IQR fitting in the tested t2
and bimodal settings. This is robust-reference estimation, not a claim that
the complete c_delta statistic has a positive finite-sample breakdown point.

## Formal Huber Robust-Reference Definition

For each margin (z \in \{x,y\}), compute a preliminary robust scale

```text
s_z = 1.4826 median_i |z_i - median(z)|,
```

with a documented nonzero-scale fallback. Fit the centre as the Huber
M-estimate

```text
T_z = argmin_t sum_i rho_1.345((z_i - t) / s_z),
```

where the derivative is

```text
psi_c(u) = sign(u) min(|u|, c).
```

The primary robust-reference profile is then

```text
S_zi = |z_i - T_z| / s_z,
c_delta^Huber = mean(S_x S_y) / (mean(S_x) mean(S_y)).
```

The division by `s_z` is optional for the uncapped c_delta value because the
ratio is separately scale invariant, but it is required to make a cap have a
common interpretation across margins. The Huber fitting constant `1.345` and
the optional final cap constant (for example `6`) are different parameters and
must not be conflated.

## Inferential Statement

After the two marginal profiles have been fitted, the robust statistic tests

```text
H0: the pairing between S_x and S_y is exchangeable
    (no positive paired-salience alignment),
H1: E[S_xi S_yi] > E[S_xi] E[S_yi].
```

For fixed profiles and a uniformly random permutation of `S_y`,

```text
E_perm[c_delta^Huber] = 1
```

exactly. Enumerating all `n!` permutations gives a finite-sample exact test;
Monte Carlo permutations use the plus-one correction. This is the main
inferential advantage over treating the robust score as an uncalibrated
descriptive index. The proof requires only positive finite profile means and
does not require normality of the original observations.

The centre, scale, and any marginal screen must be computed separately within
`x` and `y`, before looking at their alignment. Under clustered, longitudinal,
or otherwise dependent pairing, ordinary permutations are not valid and must
be replaced by a block- or design-respecting permutation scheme. At an
empirical zero profile mean, report "undetermined due to data limitations".

## What the Archived Formula Shows

The arXiv record for Hoorn's c_delta paper contains version 1 (2025-10-19) and
version 2 (2026-03-08):

- <https://arxiv.org/abs/2510.16717>
- <https://arxiv.org/pdf/2510.16717v1>
- <https://arxiv.org/pdf/2510.16717v2>

Both archived versions write the numerator as a **sum** of paired divergence
products and the denominator as a product of **mean** divergences. The project
has already established that the coherent corrected statistic requires a mean
in the numerator:

```text
c_delta = mean(S_x S_y) / (mean(S_x) mean(S_y)).
```

This gives random-pairing reference 1. Without the extra `1/n`, the reference
is `n`. Any new definition should start from the corrected profile formula,
not reproduce the archived normalisation error.

Version 2 explicitly describes the L2 version as having quadratic outlier
influence and breakdown point near zero, and recommends L1 or a rank-based
version when known outliers are present. This agrees with the project's
simulation evidence. There is also an internal wording inconsistency: the text
calls squared differences robust, whereas its comparison table correctly says
that squaring amplifies outliers.

## General Profile Form

Let `S_x = (S_x1, ..., S_xn)` and `S_y = (S_y1, ..., S_yn)` be any nonnegative,
separately computed salience profiles. Define

```text
c_delta(S_x, S_y)
    = mean(S_xi S_yi) / (mean(S_x) mean(S_y)).
```

The existing identity still holds:

```text
c_delta
    = 1 + corr(S_x, S_y) CV(S_x) CV(S_y).
```

Therefore, for a fixed sample, the upper-tail permutation ordering remains
exactly the Pearson ordering of the two new salience profiles. The inferential
engine does not need to change merely because the marginal score definition
changes.

Under the random-pairing null, the conditional permutation expectation remains
1 for every fixed pair of positive profiles. Calibration still requires that
the score construction be symmetric in observation labels and computed from
each marginal sample separately. A joint x-y screening rule would require
recomputation under every permutation and is not recommended.

## Candidate A: Distance to a Geometric Centre

The direct centre proposal is

```text
S_i = ||x_i - T(X)||_2.
```

In one dimension this is simply `|x_i - T(X)|`.

### Why ordinary k-means does not solve the problem

- With `k = 1`, k-means returns the arithmetic mean. Its breakdown point is
  zero, so a remote outlier moves the centre.
- With `k > 1`, the estimand changes from global group salience to distance
  from a selected local cluster. An extreme can receive its own singleton
  cluster and distance zero, reversing its intended interpretation.
- The chosen `k`, initialisation, and cluster-label structure become additional
  model assumptions.

For a single global centre, use a robust location estimator instead. In
multiple dimensions, the geometric median is the natural rotation-equivariant
analogue. In one dimension it reduces to the median, although the simulation
below shows that a raw sample median can be inefficient or unstable for some
diffuse symmetric profiles.

### Remote-outlier limit

Suppose `n-1` ordinary observations remain bounded and one value tends to
`M -> infinity`.

- Original pairwise L2 gives ordinary scores of order `M/sqrt(n)` and an
  outlier score of order `M`; the relative contrast approaches order
  `sqrt(n)`.
- Distance to the arithmetic mean gives ordinary scores of order `M/n` and an
  outlier score of order `M`; the relative contrast approaches `n-1`.

Thus, changing from pairwise RMS to distance from the ordinary centroid does
not make the final profile less outlier-dominated. It can make the outlier's
relative leverage larger.

## Candidate B: Fit Without Flagged Values, Score Everyone

Let `I_x` be a marginally selected ordinary subset, and let

```text
T_x = location({x_i: i in I_x}).
```

Then score all observations:

```text
S_xi = |x_i - T_x|,  for every i = 1, ..., n.
```

The flagged observations are excluded only from fitting the reference centre;
they are not deleted from the salience profile or from c_delta.

This cleanly implements the second proposal. A remote outlier no longer moves
the ordinary observations' reference centre. However, its own score still
grows without bound. This is not a defect if the scientific target is a
meaningful shared standout; it is not a bounded-influence estimator.

The prototype uses a 1.5-IQR marginal screen followed by the mean of retained
observations. This is intentionally simple, not a final recommendation. A
final paper should compare a pre-specified trimmed mean, Huber M-location, and
in multivariate work a geometric median or high-breakdown scatter estimator.

Hard screening must be treated carefully under skewness, multimodality, and
small samples. The rule and its tuning constant must be selected before seeing
the x-y alignment result.

## Candidate C: Bounded-Influence Distance

To protect the final statistic rather than only the centre, define a robust
scale `s_x` on the ordinary subset and use

```text
S_xi = min(|x_i - T_x|, c s_x).
```

This is the score induced by the Huber weight

```text
w(r) = min(1, c/r),
S = w(r) r.
```

This distinction matters for the proposed "distance weighting": an increasing
weight amplifies far points, while a decreasing weight with bounded `w(r)r`
limits their influence. Merely applying an L2 norm or squaring again moves in
the wrong direction if robustness is the goal.

The earlier illustrative cap `c = 3` is too aggressive for the tested signal
sizes. A parameter grid found that `c = 6` retained nearly all single matched
outlier power while materially reducing unmatched masking. This is a design
tradeoff, not a universal constant: `6` must be frozen before evaluation or
replaced by an explicitly calibrated null-quantile rule.

## Connection to h_star

The h-star paper is:

- Hoorn and Ho, *A test statistic, h-star, for outlier analysis*:
  <https://arxiv.org/abs/2508.06792>
- PDF: <https://arxiv.org/pdf/2508.06792>

For one pre-selected candidate `i`, its core construction is

```text
h_i =
  RMS(distance from candidate i to all other observations)
  --------------------------------------------------------.
  RMS(pairwise distance among observations excluding i)
```

This is conceptually close to "fit ordinary structure without the candidate,
then evaluate the candidate against it." It also treats an outlier as a
possible phenomenon of interest rather than automatically deleting it.

The present validation creates an exploratory `h_i` for every observation and
correlates the resulting profiles. This is **not** the h-star inferential test:

- h-star is formulated for a selected global extreme and uses a
  distribution-specific reference calculation;
- applying leave-one-out h-star to every point creates a dependent profile;
- with multiple outliers, the denominator for one candidate contains the other
  outliers, producing masking;
- calling h-star non-normality-compatible does not make it distribution-free;
  its reference distribution still depends on the assumed or fitted ordinary
  distribution.

The paper's worked example `{3, 4, 5, 8}` contains an arithmetic inconsistency.
It writes `(3-5)^2` as 2 and reports approximately 3.54. Following Definition 1,
the ordinary squared-distance sum is `1 + 4 + 1 = 6`, so

```text
h_8 = sqrt(50/3) / sqrt(6/3) = 2.88675.
```

The implementation and tests follow the formal definition, not the worked
example's arithmetic.

## First Validation Design

Settings:

- `n = 80`;
- 500 repetitions per scenario;
- 199 permutations per dataset;
- strict `p < .05` upper-tail rejection;
- methods: original pairwise L2, arithmetic-centroid radius, median radius,
  IQR-fit/all-score radius, capped IQR-fit/all-score radius, and h-star-style
  L2/L1 profiles.

Scenarios:

1. clean independent normal null;
2. independent normal null with one randomly located outlier in each margin;
3. one genuinely matched magnitude-8 outlier;
4. diffuse aligned salience without a sparse extreme;
5. two matched magnitude-8 observations in a Student-t2 background;
6. two matched magnitude-6 observations plus one magnitude-20 contaminant on
   each side at different indices.

Full output:

- `results/robust_center_validation_20260804.tsv`;
- `results/robust_center_influence_20260804.tsv`.

The expanded grid is in `results/robust_cdelta_grid_20260804.tsv`, its
2,000-repetition null check is in
`results/robust_cdelta_null_high_rep_20260804.tsv`, and the tuning scan is in
`results/robust_parameter_sensitivity_20260804.tsv`.

## Representative Results

| Scenario | Original L2 | Centroid | Median | IQR fit/all | Capped IQR | h-star L2 | h-star L1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Clean null | .050 | .050 | .050 | .054 | .054 | .048 | .050 |
| Random-outlier null | .050 | .058 | .062 | .054 | .058 | .062 | .058 |
| Matched outlier | 1.000 | 1.000 | 1.000 | 1.000 | .314 | 1.000 | .998 |
| Diffuse salience | 1.000 | 1.000 | .412 | 1.000 | 1.000 | 1.000 | .980 |
| t2 matched pair | .488 | .470 | .490 | .492 | .200 | .462 | .480 |
| Unmatched masking | .052 | .062 | .082 | .074 | .272 | .024 | .044 |

Wilson intervals for the random-outlier-null rates all include `.05`; the
differences among `.050-.062` should not be overinterpreted.

### What these results say

- The IQR-fit/all-score proposal preserves the original method's strong
  matched-outlier and diffuse-profile power in these settings.
- Robust centre estimation alone does not solve final-statistic domination;
  the uncapped IQR version behaves much like the original under extreme
  matched signals.
- Capping helps when huge unmatched contaminants mask a moderate paired
  signal (`.272` versus `.052`), but substantially sacrifices meaningful
  matched-outlier power (`.314` versus `1.000`) and t2 matched-pair power
  (`.200` versus about `.49`).
- The raw median is not uniformly preferable. In the constructed diffuse
  signed profile, small sign imbalance can place the sample median on one side
  of a central gap, distorting the salience ranking.
- The h-star profile is strong for one matched candidate but weak under
  multiple-outlier masking, as predicted by its leave-one-candidate-out
  denominator.

The influence path reinforces the distinction. As the remote value grows from
8 to 1024, ordinary-score means remain about 1.01 for median and IQR-fit/all
profiles, but the remote score grows without bound. The capped version fixes
the remote score at about 4.45. The original pairwise L2 ordinary-score mean
grows from 1.85 to 113.79 because the remote point enters every row divergence.

## Expanded Systematic Validation

The expanded grid used `n = 40, 80, 160`, 300 repetitions, and 199
permutations. It added 1%, 5%, and 10% independent contamination nulls,
matched 1% and 5% signals, Student-t2, skewed lognormal, a shared bimodal
structure, and unmatched masking. The method order below is original L2 / IQR
/ trimmed 10% / Huber / IQR cap 3 / Huber cap 3.

At `n = 80`, rejection rates were:

| Scenario | Original | IQR | Trim | Huber | IQR cap3 | Huber cap3 |
|---|---:|---:|---:|---:|---:|---:|
| Clean null | .070 | .053 | .063 | .053 | .050 | .063 |
| 5% contaminated null | .053 | .067 | .067 | .070 | .067 | .073 |
| 1% matched magnitude-8 | 1.000 | 1.000 | 1.000 | 1.000 | .280 | .310 |
| t2 matched | .737 | .827 | .810 | .837 | .533 | .707 |
| Bimodal aligned | .690 | .700 | .750 | .907 | .707 | .903 |
| Unmatched masking | .047 | .063 | .080 | .073 | .267 | .287 |

The clean-null `n = 80` fluctuation disappears in the higher-replication check:
with 2,000 repetitions, original L2, IQR, trimmed, and Huber rates were
`.0445`, `.0465`, `.0495`, and `.0480`. Under 5% independent contamination
they were `.0430`, `.0500`, `.0480`, and `.0445`. The corresponding Wilson
intervals are compatible with the nominal .05 level.

### Parameter sensitivity

At `n = 80` with 300 repetitions, the key tuning results were:

| Method | Matched 1% | t2 matched | Bimodal aligned | Unmatched masking |
|---|---:|---:|---:|---:|
| Huber, no cap, `c=1.345` | 1.000 | .750 | .910 | .067 |
| Hard cap `3s` | .317 | .697 | .913 | .357 |
| Hard cap `4s` | .757 | .933 | .910 | .540 |
| Hard cap `6s` | .997 | .997 | .910 | .590 |
| Soft cap `6s` | .983 | .983 | .917 | .373 |

The `6s` values are promising as a robustness sensitivity analysis, but the
grid is not a license to optimise the constant on the final dataset. A formal
version should either freeze `6` prospectively or determine the cap from a
training/reference null distribution.

## Recommendation

### Main candidate: Huber robust-reference c_delta

Use a robustly fitted marginal reference, but score all observations:

```text
R_xi = ||x_i - T_x||,
R_yi = ||y_i - T_y||,

c_delta^R = mean(R_xi R_yi) / (mean(R_x) mean(R_y)).
```

Use a pre-specified Huber M-location with `c = 1.345`, estimate the robust scale
with MAD, and score all observations. Retain IQR-fit/all and trimmed centres as
transparent sensitivity baselines. This definition best matches the current
paired-salience estimand and the h-star philosophy of evaluating rather than
deleting exceptional observations.

### Required sensitivity analysis: bounded version

Report a capped profile in parallel, with `c = 6` frozen prospectively or
calibrated from a reference null:

```text
R_xi^(c) = min(R_xi / s_x, c),
R_yi^(c) = min(R_yi / s_y, c).
```

This answers a different question: whether the paired salience pattern remains
after limiting any one observation's leverage. It should not silently replace
the retained-outlier statistic. A soft cap can be reported as a third
sensitivity analysis when continuity is important.

### Keep h-star separate

Use h-star to evaluate pre-specified candidate outliers or to motivate the
signal-versus-ordinary-noise construction. Do not directly call the
all-observation h-star profile a new c_delta definition until collective
outlier masking, candidate selection, and its reference distribution are
resolved.

## Next Validation Needed Before a Definition Change

1. Replace the provisional IQR centre with trimmed and Huber M-locations;
   compare contamination fractions `0%, 1%, 5%, 10%, 20%`.
2. Separate aligned meaningful standouts from independently placed contaminants
   in the same dataset and vary both magnitudes independently.
3. Validate skewed, multimodal, clustered, and multivariate settings; do not
   treat a multimodal cluster as contamination by default.
4. Tune the cap on a training grid or under pre-specified loss, then freeze it
   for evaluation to avoid power-driven cherry-picking.
5. Refit screening, centre, and scale inside every bootstrap resample.
6. Compare fixed `k` and fixed contamination proportion as sample size changes.
7. Report profile correlation and permutation p-value as primary quantities;
   raw distance from 1 remains confounded by profile CVs.
8. State the robust-reference estimand separately from the bounded-influence
   estimand in the manuscript; they answer different scientific questions.
