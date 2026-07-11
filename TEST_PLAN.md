# Test Plan

## Phase 1: Mathematical Sanity Checks

These tests are already included in `tests/test_cdelta.py`.

1. Divergence vectors have the expected length and nonnegative entries.
2. Raw `c_delta` is invariant to location shifts and nonzero scale changes.
3. Zero-divergence inputs are reported as undetermined due to data limitations.
4. Pairing-normalized `c_delta` stays within the sample-dependent pairing range.
5. A clearly aligned sample gives a small permutation p-value.

## Phase 2: Simulation Calibration

Run repeated simulations across:

- sample sizes: `n = 10, 20, 50, 100, 250`;
- settings: null normal, aligned normal, nonlinear alignment, inverted divergence,
  heavy-tailed, skewed, contaminated aligned, contaminated unaligned, matched
  extreme, mismatched extreme, X-only extreme, Y-only extreme;
- repetitions: at least 1,000 per setting for a draft table;
- permutation counts: 999 for exploratory runs, 4,999 or 9,999 for final tables;
- bootstrap counts: 2,000 minimum, 10,000 preferred for final intervals.

Record:

- raw `c_delta`;
- sample-dependent normalized `c_delta`;
- divergence-vector correlation;
- permutation p-value;
- bootstrap CI width and empirical coverage when ground truth is simulated;
- sensitivity to single and multiple extreme observations.
- whether extreme observations are matched across groups or appear in only one
  group.
- how the shared divergence signal changes as the magnitude of a matched
  extreme observation increases.
- whether smaller samples require larger extreme values to reach the same
  rejection rate.
- whether null and mismatched controls maintain nominal size at alpha `.05` and
  `.01`.
- whether two or three co-occurring extreme pairs improve small-sample power by
  reducing the chance that a random permutation accidentally reconstructs the
  dominant structure.

## Phase 3: h-star Integration

Before removing or down-weighting outliers:

1. identify candidate global outliers;
2. apply h-star to assess whether the candidate value is stably exceptional;
3. compare `c_delta` results with the value included and excluded;
4. report whether the paired group contains a corresponding divergent value;
5. report whether the outlier changes the divergence-structure conclusion.

This follows Professor Hoorn's point that outliers may contain information and
should not automatically be removed.

The retained-outlier analysis is the primary analysis. Exclusion is only a
sensitivity comparison, because a single extreme value may define the structure
of the whole group.

## Phase 4: Robust and Weighted Variants

After Phase 1-3 are stable:

- compare L2 `c_delta` with the L1/Gini variant;
- add rank-based divergence vectors;
- define a principled weight function for pairwise differences;
- test whether weighting improves stability without erasing meaningful
  exceptional observations.

## Phase 5: Positioning Against Existing Methods

Add comparison baselines:

- Pearson/Spearman correlation of raw values;
- Pearson/Spearman correlation of divergence vectors;
- energy distance;
- maximum mean discrepancy;
- Kolmogorov-Smirnov distance for one-dimensional examples.

The purpose is not to show that `c_delta` replaces these methods, but to show
which question it answers differently.
