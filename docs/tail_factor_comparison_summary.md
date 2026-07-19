# Tail-Factor Comparison Summary

Date: 2026-07-19

This update extends the previous heavy-tail check into a broader factor grid.
The goal is to determine whether the low power under Student `t_2` is an
isolated result or part of a continuous tail-heaviness pattern.

## Design

The main simulation grid varies:

- divergence definition: `l2` and `l1`;
- tail setting: normal, Student `t_10`, `t_8`, `t_5`, `t_4`, `t_3`,
  `t_2.5`, `t_2.2`, and `t_2`;
- sample size: `n = 40, 80, 160`;
- matched subgroup size: `k = 1, 2, 3`;
- extreme magnitude: `4`, `6`, and `8`;
- scenario: matched and independent-null;
- repetitions: `120` per grid cell;
- permutations: `299` per repetition.

Because the full grid uses moderate repetition per cell, a separate
higher-replication independent-null validation was run for the central slice
`n = 80`, `k = 2`, magnitude `8`, with `800` repetitions and `499`
permutations per repetition.

## Main Finding

The power decline under heavy tails is continuous rather than isolated. As the
Student degrees of freedom decrease, matched rejection rates decrease
systematically.

For the central slice `n = 80`, `k = 2`, the matched rejection rates are:

| Kind | Magnitude | Normal | t10 | t8 | t5 | t4 | t3 | t2.5 | t2.2 | t2 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| l2 | 4 | 1.000 | .983 | .975 | .717 | .508 | .275 | .158 | .133 | .158 |
| l2 | 6 | 1.000 | 1.000 | 1.000 | .992 | .958 | .750 | .467 | .383 | .267 |
| l2 | 8 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | .942 | .783 | .692 | .483 |
| l1 | 4 | 1.000 | .975 | .967 | .825 | .592 | .292 | .142 | .125 | .067 |
| l1 | 6 | 1.000 | 1.000 | 1.000 | 1.000 | .967 | .792 | .567 | .367 | .292 |
| l1 | 8 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | .950 | .850 | .733 | .533 |

This supports the interpretation that heavy-tailed background variation can
mask a real matched co-divergence structure. In other words, the issue is not
only whether a matched subgroup exists, but whether it separates from the
background divergence noise.

## Horizontal Factor Comparison

Across all matched settings in the grid:

- mean matched power decreases from `.995` under normal backgrounds to `.278`
  under `t_2`;
- mean matched power increases with subgroup size: `k = 1` gives `.596`,
  `k = 2` gives `.729`, and `k = 3` gives `.785`;
- mean matched power increases with magnitude: magnitude `4` gives `.505`,
  magnitude `6` gives `.743`, and magnitude `8` gives `.862`;
- `l1` and `l2` are broadly similar overall: `.707` for `l1` and `.700` for
  `l2`.

The sample-size pattern is more subtle in this sparse-extreme grid. Mean
matched power is `.755` for `n = 40`, `.708` for `n = 80`, and `.647` for
`n = 160`. This is consistent with a sparsity dilution effect: if `k` is fixed,
the same small matched subgroup occupies a smaller fraction of the sample as
`n` grows.

## Independent-Null Validation

The higher-replication validation for `n = 80`, `k = 2`, magnitude `8` shows
that the independent-null rejection rates remain close to the nominal `.05`
level across the tail gradient.

For `l2`, rejection rates range from `.041` to `.056`. For `l1`, they range
from `.040` to `.064`. The intervals are compatible with nominal size, so the
power decline under heavier tails should not be interpreted as a type-I
calibration failure.

## Background Divergence Noise

The background-only divergence noise increases as tails become heavier. For
`n = 80`, the average max-to-mean divergence ratio increases:

| Kind | Normal | t10 | t8 | t5 | t4 | t3 | t2.5 | t2.2 | t2 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| l2 | 2.12 | 2.38 | 2.46 | 2.84 | 3.04 | 3.45 | 4.16 | 4.46 | 4.76 |
| l1 | 2.39 | 2.75 | 2.85 | 3.39 | 3.69 | 4.35 | 5.69 | 6.29 | 7.08 |

This gives a possible mechanism for the power pattern: as the background itself
produces larger divergence-vector extremes, the inserted matched subgroup has a
lower effective signal-to-background-noise contrast.

## Interpretation

Today's update strengthens the heavy-tail finding:

1. The `t_2` result is not an isolated anomaly; power decreases gradually as
   the tail becomes heavier.
2. The independent-null behavior remains broadly calibrated in the central
   higher-replication validation.
3. The power loss is plausibly driven by increasing background divergence
   noise, not by a simple failure of the permutation test.
4. Fixed-size sparse subgroups can be diluted as `n` increases, so sample-size
   studies should distinguish fixed `k` from fixed subgroup proportion.

## Suggested Next Questions

- Define and test a signal-to-background-divergence-noise ratio.
- Repeat the sample-size comparison with fixed subgroup proportions, such as
  `k / n = .025, .05, .10`, rather than fixed `k`.
- Compare raw divergence-vector noise with rank-based or Huberized divergence
  variants as sensitivity checks, while keeping the original statistic as the
  main version.
- Consider whether a paper section should explicitly state that heavy-tailed
  backgrounds may reduce power without inflating type-I error.
