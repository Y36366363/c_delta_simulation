# Calibrated Subgroup Simulation Summary

This update addresses Professor Hoorn's point that increasing the number of
matched high-divergence observations changes two things at once:

1. the permutation overlap structure, and
2. the strength of the simulated alternative.

The new simulation first calibrates the magnitude for each subgroup size
`k = 1, 2, 3` so that the matched condition has approximately comparable
divergence-vector correlation. It then evaluates matched, negative-control, and
independent-null behavior at those selected magnitudes.

## Design

```text
n = 40
kind = l2
reference condition = k = 1, magnitude = 8
magnitude grid = 2, 3, 4, 5, 6, 7, 8, 10, 12
calibration repetitions = 120
evaluation repetitions = 250
n_perm = 499
alpha = .05
backgrounds = normal, t3
```

For each background, the calibration target is the mean matched-condition
divergence-vector correlation under `k = 1, magnitude = 8`.

## Selected Magnitudes

```text
background   target_corr   k   selected_magnitude   calibrated_mean_corr
normal       0.9035        1   8                   0.9035
normal       0.9035        2   7                   0.9179
normal       0.9035        3   6                   0.9043
t3           0.5804        1   8                   0.5804
t3           0.5804        2   6                   0.5736
t3           0.5804        3   6                   0.5984
```

## Evaluation Results

```text
background   k   scenario             rejection_rate   mean_corr
normal       1   matched              1.0000           0.8990
normal       1   negative_control     0.0280          -0.0181
normal       1   independent_null     0.0400           0.0008
normal       2   matched              1.0000           0.9209
normal       2   negative_control     0.0000          -0.0460
normal       2   independent_null     0.0440          -0.0000
normal       3   matched              1.0000           0.9058
normal       3   negative_control     0.0000          -0.0733
normal       3   independent_null     0.0440           0.0007
t3           1   matched              0.8720           0.5982
t3           1   negative_control     0.0360          -0.0088
t3           1   independent_null     0.0520          -0.0006
t3           2   matched              0.8160           0.5397
t3           2   negative_control     0.0120          -0.0317
t3           2   independent_null     0.0440          -0.0035
t3           3   matched              0.9000           0.6005
t3           3   negative_control     0.0120          -0.0501
t3           3   independent_null     0.0320          -0.0060
```

## Interpretation

- The calibrated design partially separates subgroup size from signal strength.
  This is a better basis for discussing finite-sample permutation resolution
  than the earlier fixed-magnitude comparison.
- Under the normal background, the calibrated matched signals are already very
  strong, so all three subgroup sizes reach rejection rate `1.0000`. This is a
  ceiling-effect setting rather than a sensitive comparison of `k`.
- Under the heavy-tailed `t3` background, the calibrated matched rejection rates
  are high but not saturated. They range from `0.8160` to `0.9000`, while
  independent-null rates remain near alpha `.05`.
- The `t3` results suggest that subgroup size alone does not create a simple
  monotone power curve once approximate signal strength is controlled. This
  supports the more careful claim that detectability depends jointly on signal
  strength, background tail behavior, and the permutation overlap structure.
- The negative-control condition remains low, reinforcing that high-divergence
  observations in both samples are not enough; the signal comes from
  co-occurring internal divergence structure.

## Next Check

The next useful refinement is to repeat this calibration at a lower target
correlation so the normal background avoids the ceiling effect. A second target,
for example around `0.55` or `0.65`, would make the comparison across subgroup
sizes more informative.
