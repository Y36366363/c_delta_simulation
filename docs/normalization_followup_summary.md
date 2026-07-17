# Normalization Follow-up Summary

This follow-up checks the project after adding the missing `1 / n` numerator
factor to the raw `c_delta` statistic.

## Corrected Permutation Mean

The corrected raw statistic is:

```text
c_delta = (1 / n) sum_i D_xi D_yi / (bar D_x bar D_y)
```

The exact and Monte Carlo checks confirm that the permutation mean is now `1`,
not `n`.

```text
method        n_statistics   mean_permuted_raw   expected_mean   absolute_error
exact         40320          1.000000            1.000000        0.000000
monte_carlo   5000           1.000402            1.000000        0.000402
```

This confirms the normalization revision suggested by Professor Hoorn's postdoc.

## Compact Corrected-Scale Check

A compact lower-target check under the corrected scale was run for:

```text
background = normal
n = 40
target correlation = 0.35
k = 1, 2, 3
kind = l2, l1
evaluation repetitions = 150
n_perm = 299
```

The rejection-rate pattern remains qualitatively consistent with the previous
reports. Raw values are now close to `1` under independent-null settings, as
expected.

```text
kind   k   scenario           rejection   mean_raw   mean_corr
l2     1   matched            0.5400      1.0335     0.3329
l2     1   independent_null   0.0267      0.9994    -0.0065
l2     2   matched            0.6400      1.0320     0.3462
l2     2   independent_null   0.0667      1.0005     0.0069
l2     3   matched            0.8133      1.0373     0.4105
l2     3   independent_null   0.0467      1.0010     0.0083
l1     1   matched            0.5867      1.0539     0.3506
l1     1   independent_null   0.0200      0.9994    -0.0053
l1     2   matched            0.6467      1.0492     0.3611
l1     2   independent_null   0.0533      1.0007     0.0069
l1     3   matched            0.8467      1.0561     0.4235
l1     3   independent_null   0.0600      1.0019     0.0103
```

## Flagged Large-n Independent-Null Recheck

The earlier sample-size sensitivity run flagged the condition:

```text
kind = l1
background = lognormal
n = 160
k = 1
```

The earlier exploratory rejection rate was `0.0767`. A higher-replication
follow-up was run with:

```text
repetitions = 1000
n_perm = 999
alpha = .05 and .01
```

Results:

```text
alpha   reject_count   empirical_size   Wilson interval
.05     53             0.053            [0.0407, 0.0687]
.01     11             0.011            [0.0062, 0.0196]
```

The flagged condition no longer shows clear over-rejection. The previous
`0.0767` appears consistent with simulation variability rather than a stable
large-sample calibration problem.

## What Can Be Reported Now

- The formula correction has been implemented.
- Corrected raw `c_delta` has permutation mean `1`.
- Raw-scale values in old tables need reinterpretation or division by `n`.
- Permutation p-values, rejection rates, correlation patterns, and
  pairing-normalized values remain valid because the correction is a constant
  positive rescaling for each fixed sample size.
- The earlier flagged large-n lognormal `l1` null issue is less concerning
  after higher-replication checking.

## Suggested Next Step

Future report tables should either:

1. regenerate raw-scale columns under the corrected formula, or
2. focus on rejection rates, p-values, normalized values, and divergence-vector
   correlations, which are not changed by the `1 / n` scaling.
