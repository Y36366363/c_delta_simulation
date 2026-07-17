# Extended Stable Simulation Summary

Date: 2026-07-17

This simulation extends the post-normalization reporting workflow by using only
stable quantities: permutation p-values, rejection rates, Wilson intervals,
divergence-vector correlations, pairing-normalized values, and
independent-null calibration summaries. Old raw-scale values are intentionally
not emphasized.

## Design

The script `scripts/run_extended_stable_simulations.py` evaluates calibrated
matched-subgroup and independent-null settings across a wider grid:

- target divergence-vector correlations: `0.25` and `0.35`;
- divergence definitions: squared difference (`l2`) and absolute difference
  (`l1`);
- backgrounds: normal, Student `t_3`, Student `t_2`, and lognormal;
- sample sizes: `n = 40, 80, 160`;
- matched subgroup sizes: `k = 1, 2, 3`;
- evaluation repetitions: `220`;
- permutations per repetition: `399`;
- nominal alpha: `.05`.

Each setting first selects a magnitude from a fixed grid to approximately match
the target correlation, then evaluates matched and independent-null behavior
under the selected magnitude.

## Main Findings

The larger simulation supports the current reporting direction. Matched
co-divergence structures are detected much more often than independent-null
structures, while the null settings mostly remain close to the nominal `.05`
level.

The background distribution strongly affects power. Normal and lognormal
backgrounds become easy to detect as `n` increases, especially at target
correlation `.35`. For example, at target `.35`, both `l2` and `l1` reach
rejection rates near or equal to `1.0` for normal and lognormal backgrounds at
`n = 160`.

Heavy-tailed backgrounds are harder. The Student `t_2` background remains the
flattest case. At target `.35` and `n = 160`, the average matched rejection
rate across `k = 1, 2, 3` is about `.542` for both `l2` and `l1`, compared with
approximately `1.0` in normal and lognormal backgrounds. This suggests that a
sparse extreme structure can be partly masked when the background itself
naturally produces large divergences.

The lower target `.25` helps avoid the ceiling effect, but large sample sizes
can still make the matched signal highly detectable. At target `.25`,
normal-background matched rejection rates at `n = 160` average about `.895`
for `l2` and `.915` for `l1`; for `k = 3`, the rejection rates reach `.9864`
and `.9955`, respectively.

## Independent-Null Calibration

Most independent-null rejection rates remain near the nominal `.05` level.
Several rows are monitoring flags rather than final conclusions, because each
setting currently uses `220` evaluation repetitions:

- target `.25`, `l2`, normal, `n = 160`, `k = 1`: rejection rate `.0818`,
  Wilson interval `[.0524, .1256]`;
- target `.35`, `l2`, normal, `n = 160`, `k = 3`: rejection rate `.0864`,
  Wilson interval `[.0560, .1309]`;
- target `.35`, `l1`, normal, `n = 160`, `k = 3`: rejection rate `.0864`,
  Wilson interval `[.0560, .1309]`;
- target `.35`, `l2`, Student `t_2`, `n = 40`, `k = 1`: rejection rate
  `.0909`, Wilson interval `[.0596, .1362]`;
- target `.35`, `l1`, Student `t_2`, `n = 40`, `k = 1`: rejection rate
  `.0818`, Wilson interval `[.0524, .1256]`.

These flags should be treated as candidates for higher-replication follow-up.
They do not yet show a stable failure of the permutation calibration, but they
identify settings where Monte Carlo uncertainty should be reduced.

## Interpretation

The extended results suggest three useful reporting points:

1. `c_delta` responds to co-occurring internal divergence structure rather than
   simply to large values appearing somewhere in both samples.
2. Sample size and background tail behavior jointly determine power; increasing
   `n` can produce near-saturated detection in normal or lognormal backgrounds,
   while heavy-tailed backgrounds can still reduce power substantially.
3. Independent-null calibration remains a necessary companion to matched-power
   reporting, especially when `n` is large or when the background distribution
   already contains strong natural variation.

## Suggested Next Step

The most useful next check is a higher-replication validation of the monitoring
flags above, especially the `n = 160` normal-background settings and the
`n = 40`, Student `t_2`, `k = 1` settings. This can separate random Monte Carlo
variation from a real small null-calibration issue.
