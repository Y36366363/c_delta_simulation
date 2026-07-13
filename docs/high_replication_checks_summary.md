# High-Replication Checks Summary

This run increases the credibility of the July 13 feedback checks by using
1,000 simulation replications for independent-null calibration and 100,000
sampled permutations for the overlap-layer diagnostic.

## Independent-Null Calibration

Setting:

```text
n = 40
k = 2
magnitude = 8
repetitions = 1000
n_perm = 999
backgrounds = normal, t3, lognormal
```

Results:

```text
background   alpha   reject_count   empirical_size   Wilson interval
normal       .05     57             0.057            [0.0443, 0.0731]
normal       .01     6              0.006            [0.0028, 0.0130]
t3           .05     51             0.051            [0.0390, 0.0664]
t3           .01     10             0.010            [0.0054, 0.0183]
lognormal    .05     53             0.053            [0.0407, 0.0687]
lognormal    .01     15             0.015            [0.0091, 0.0246]
```

Interpretation:

- At alpha `.05`, all three empirical sizes are close to nominal and their
  Wilson intervals contain `.05`.
- At alpha `.01`, normal and t3 are close to nominal. The lognormal case is
  slightly higher at `0.015`, but with 1,000 replications this should be treated
  as a mild signal to monitor rather than a final conclusion.
- The p-value medians are near 0.5 across backgrounds, which supports broad
  calibration under the independent-null design.

## Overlap-Layer Diagnostic

Setting:

```text
n = 15
k = 3
magnitude = 8
n_perm = 100000
```

Results:

```text
overlap   layer_probability   mean_stat   share_ge_observed
0         0.48184             14.651709   0.000000
1         0.43659             15.232320   0.000000
2         0.07924             15.811696   0.000000
3         0.00233             16.391677   0.562232
```

Interpretation:

- The complete-overlap layer probability is `0.00233`, close to
  `1 / choose(15, 3) = 0.002198`.
- This strengthens the corrected interpretation: the combinatorial value is a
  layer probability, not a p-value.
- Only the complete-overlap layer contributes meaningfully to the upper tail in
  this specific configuration, but that need not hold universally.
