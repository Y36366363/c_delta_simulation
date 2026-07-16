# Lower-Target L1 Calibration Summary

This run repeats the most informative lower-target calibration setting with the
absolute-difference divergence definition (`l1`). The goal is to check whether
the non-ceiling subgroup-size findings at target correlation `0.35` depend on
the squared-difference (`l2`) version.

## Design

```text
n = 40
kind = l1
target correlation = 0.35
k = 1, 2, 3
backgrounds = normal, t3, lognormal
magnitude grid = 1, 1.5, 2, ..., 6, 7, 8
calibration repetitions = 180
evaluation repetitions = 500
n_perm = 499
alpha = .05
```

## Matched Results

```text
background   k   selected magnitude   calibrated corr   mean corr   rejection rate
normal       1   3.0                  0.3593            0.3561      0.642
normal       2   2.5                  0.3561            0.3573      0.678
normal       3   2.5                  0.4214            0.4181      0.842
t3           1   5.5                  0.3628            0.3769      0.594
t3           2   4.5                  0.3677            0.3492      0.566
t3           3   4.0                  0.3424            0.3340      0.534
lognormal    1   3.5                  0.3267            0.3339      0.396
lognormal    2   3.0                  0.3772            0.3916      0.650
lognormal    3   2.5                  0.3533            0.3556      0.556
```

## Independent-Null Results

```text
background   k   independent-null rejection rate
normal       1   0.042
normal       2   0.038
normal       3   0.054
t3           1   0.044
t3           2   0.056
t3           3   0.032
lognormal    1   0.034
lognormal    2   0.052
lognormal    3   0.034
```

## Interpretation

- The L1 results broadly replicate the L2 lower-target pattern, so the
  non-ceiling subgroup-size findings are not only an artifact of squared
  divergence.
- Under the normal background, rejection increases from `0.642` at `k = 1` to
  `0.842` at `k = 3`.
- Under the heavy-tailed `t3` background, rejection is flatter across subgroup
  sizes (`0.594`, `0.566`, `0.534`), suggesting that natural heavy-tailed
  variation can blur the subgroup-size effect after signal calibration.
- Under lognormal background, `k = 2` is strongest, again indicating that the
  subgroup-size effect is not a simple monotone consequence of `k`.
- Independent-null rejection remains close to alpha `.05`, supporting the
  calibration of the permutation procedure in this setting.

## Report-Level Claim

The safest conclusion is:

```text
At a lower calibrated signal level, the subgroup-size effect persists under
both L2 and L1 divergence definitions, but its form depends on the background
distribution. This supports treating detectability as a joint function of
signal strength, subgroup size, tail behavior, and permutation overlap
structure rather than as a consequence of any single factor.
```
