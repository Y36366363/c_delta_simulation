# Feedback Checks Summary

This update responds to Professor Hoorn's July 13 feedback.

## 1. Permutation Mean Check

Conditional on `D_x` and `D_y`, the mean raw `c_delta` over permutations should
be `n`. The exact enumeration check for `n = 8` confirms this:

```text
exact mean = 8.0
expected mean = 8.0
```

The Monte Carlo version with 5,000 sampled permutations gives:

```text
Monte Carlo mean = 8.002016
```

This confirms that raw `c_delta` should not be interpreted relative to zero.
The permutation test is about upper-tail extremity relative to the permutation
distribution, not a zero-centered statistic.

## 2. Overlap-Layer Diagnostic

For `n = 15`, `k = 3`, and magnitude 8, permutations were classified by how
many of the three extreme `y` observations landed on the three extreme `x`
indices.

```text
overlap  layer probability  mean statistic  share >= observed
0        0.4854             14.653067       0.000000
1        0.4336             15.236571       0.000000
2        0.0789             15.815094       0.000000
3        0.0021             16.389214       0.523810
```

The complete-overlap layer probability is approximately 0.0021, consistent with
`1 / choose(15, 3) = 0.002198`. This supports Professor Hoorn's correction: the
combinatorial quantity describes the size of a permutation layer, not the
p-value itself.

## 3. Independent-Null Calibration

The deliberately disjoint mismatched condition should be described as a negative
control, not as a genuine Type-I null. A separate independent-null check was
therefore added, where X and Y extreme indices are generated independently and
chance overlap is allowed.

For `n = 40`, `k = 2`, magnitude 8, 200 replications, and 499 permutations:

```text
background   alpha=.05 size   alpha=.01 size
normal       0.035            0.005
t3           0.055            0.010
lognormal    0.045            0.020
```

These exploratory checks are broadly consistent with nominal behavior, though
more replications should be used before making a final claim.

## Reporting Correction

Future reports should use:

- independent-null calibration for Type-I error;
- deliberately disjoint subgroups as negative controls;
- overlap-layer diagnostics to explain permutation-resolution behavior;
- raw `c_delta`, normalized `c_delta`, divergence-vector correlation, and
  permutation p-values as separate quantities.
