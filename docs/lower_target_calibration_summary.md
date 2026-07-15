# Lower-Target Calibration Summary

This run extends the calibrated subgroup simulation by using explicit lower
targets for the matched-condition divergence-vector correlation. The purpose is
to avoid the ceiling effect observed when the target was based on
`k = 1, magnitude = 8`.

## Design

```text
n = 40
kind = l2
target correlations = 0.35, 0.55, 0.65
k = 1, 2, 3
backgrounds = normal, t3, lognormal
magnitude grid = 1, 1.5, 2, ..., 6, 7, 8
calibration repetitions = 180
evaluation repetitions = 500
n_perm = 499
alpha = .05
```

For each target correlation and subgroup size, the simulation selects the
magnitude whose matched-condition mean correlation is closest to the target.
It then evaluates matched, negative-control, and independent-null conditions.

## Main Matched Results

```text
target   background   k   selected magnitude   mean corr   rejection rate
0.35     normal       1   3.0                  0.3459      0.638
0.35     normal       2   2.5                  0.3433      0.678
0.35     normal       3   2.5                  0.3923      0.796
0.35     t3           1   5.5                  0.3593      0.544
0.35     t3           2   4.5                  0.3470      0.564
0.35     t3           3   4.0                  0.3424      0.572
0.35     lognormal    1   3.5                  0.3372      0.396
0.35     lognormal    2   3.0                  0.3871      0.668
0.35     lognormal    3   2.5                  0.3197      0.452

0.55     normal       1   4.0                  0.5658      0.986
0.55     normal       2   3.5                  0.6080      1.000
0.55     normal       3   3.0                  0.5520      0.984
0.55     t3           1   8.0                  0.5889      0.856
0.55     t3           2   6.0                  0.5313      0.814
0.55     t3           3   5.5                  0.5615      0.860
0.55     lognormal    1   5.0                  0.5948      0.934
0.55     lognormal    2   3.5                  0.5046      0.952
0.55     lognormal    3   3.5                  0.5987      0.996

0.65     normal       1   4.5                  0.6484      1.000
0.65     normal       2   3.5                  0.6037      1.000
0.65     normal       3   3.5                  0.6708      1.000
0.65     t3           1   8.0                  0.5921      0.864
0.65     t3           2   7.0                  0.6194      0.894
0.65     t3           3   7.0                  0.7087      0.952
0.65     lognormal    1   5.5                  0.6593      0.978
0.65     lognormal    2   4.5                  0.6913      1.000
0.65     lognormal    3   3.5                  0.5973      1.000
```

## Independent-Null Calibration

Across the lower-target runs, independent-null rejection rates mostly remain
near alpha `.05`, with Wilson intervals generally covering or close to `.05`.
This supports using the independent-null design as the Type-I calibration check.

Examples:

```text
target   background   k   independent-null rejection rate
0.35     normal       1   0.052
0.35     normal       2   0.042
0.35     normal       3   0.042
0.35     t3           1   0.054
0.35     t3           2   0.064
0.35     t3           3   0.026
0.35     lognormal    1   0.046
0.35     lognormal    2   0.038
0.35     lognormal    3   0.042
```

## Interpretation

- A target correlation of `0.55` is still too strong for the normal background:
  matched rejection rates remain approximately `0.984` to `1.000`.
- A target correlation of `0.65` is clearly saturated for normal and mostly
  saturated for lognormal.
- A target correlation of `0.35` gives a more informative non-ceiling comparison.
  Under normal background, rejection increases from `0.638` for `k = 1` to
  `0.796` for `k = 3`; under t3, rejection is more stable across `k`; under
  lognormal, the pattern is less monotone.
- These results support a cautious claim: after approximate signal calibration,
  subgroup size can still affect detectability, but the effect depends on the
  background distribution and is not reducible to the combinatorial overlap
  probability alone.
- The calibrated results also show why fixed-magnitude comparisons are not
  enough: changing `k` changes both the overlap structure and the strength of
  the alternative.

## Recommended Reporting Sentence

In the next report, the safest wording is:

```text
Lower-target calibrated simulations suggest that the apparent subgroup-size
effect is not solely a finite-sample permutation-resolution artifact. When the
matched divergence-vector correlation is calibrated to a lower, non-saturated
level, independent-null rejection remains close to nominal size, while matched
power varies by subgroup size and background distribution.
```
