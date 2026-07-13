# L1/L2 Variant Comparison Summary

This update responds to the concern that the current sparse co-divergence
results may be driven mainly by the squared-difference divergence definition.
The comparison repeats the same design using both:

- `l2`: root mean squared pairwise divergence,
- `l1`: mean absolute pairwise divergence.

## Design

```text
n = 40
k = 2 retained high-divergence observations
magnitude = 8
repetitions = 300
n_perm = 499
alpha = .05
backgrounds = normal, t3, lognormal
scenarios = matched, negative_control, independent_null
```

The `negative_control` condition has high-divergence observations in both
samples, but not at the same paired indices. It is not treated as a true null.
The `independent_null` condition independently samples the high-divergence
indices in `x` and `y`, allowing chance overlap, and is the better calibration
check for Type-I behavior.

## How to Read the Results

If both `l2` and `l1` show high rejection for the matched condition and near
nominal rejection for the independent-null condition, then the main qualitative
finding is not merely an artifact of quadratic amplification. If `l2` is much
stronger than `l1`, that would indicate that squared divergence is more
sensitive to sparse extremes and should be reported explicitly as a design
choice of the statistic.

## Current Interpretation

Results:

```text
kind   background   scenario             rejection   mean_corr
l2     normal       matched              1.0000      0.9456
l2     normal       negative_control     0.0000     -0.0468
l2     normal       independent_null     0.0500      0.0029
l2     t3           matched              0.9500      0.7085
l2     t3           negative_control     0.0100     -0.0372
l2     t3           independent_null     0.0467     -0.0096
l2     lognormal    matched              1.0000      0.9358
l2     lognormal    negative_control     0.0000     -0.0442
l2     lognormal    independent_null     0.0333     -0.0072
l1     normal       matched              1.0000      0.9307
l1     normal       negative_control     0.0000     -0.0540
l1     normal       independent_null     0.0533      0.0040
l1     t3           matched              0.9367      0.6832
l1     t3           negative_control     0.0200     -0.0292
l1     t3           independent_null     0.0500     -0.0010
l1     lognormal    matched              1.0000      0.8796
l1     lognormal    negative_control     0.0000     -0.0514
l1     lognormal    independent_null     0.0567      0.0036
```

Interpretation:

- The main qualitative finding survives the change from `l2` to `l1`.
  Co-occurring high-divergence observations are detected strongly, while
  negative-control and independent-null settings remain near nominal behavior.
- The heavy-tailed `t3` background weakens power for both variants, which is
  expected because the background itself more often produces large divergences.
- The `l1` version is still sensitive to the sparse matched structure, so the
  result is not only a consequence of quadratic amplification in the `l2`
  definition.
- This remains a variant check rather than a final robustness proof. A
  rank-based version is still useful because it would test whether only the
  ordering of divergence structure is sufficient, rather than the divergence
  magnitudes themselves.
