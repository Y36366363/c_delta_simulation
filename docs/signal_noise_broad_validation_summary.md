# Broad Signal-to-Noise Validation Summary

Date: 2026-07-26

This update expands the signal-to-background-divergence-noise check beyond the
central slice. The previous diagnostic used `n = 80`, `k = 2`, and magnitudes
`4`, `6`, and `8`. The purpose here is to test whether the signal/noise
interpretation remains stable across many more simulated settings.

## Design

The script `scripts/run_signal_noise_broad_validation.py` uses all matched
settings from the tail-factor grid:

- divergence definitions: `l2` and `l1`;
- tail settings: normal, `t10`, `t8`, `t5`, `t4`, `t3`, `t2.5`, `t2.2`, `t2`;
- sample sizes: `n = 40, 80, 160`;
- subgroup sizes: `k = 1, 2, 3`;
- magnitudes: `4`, `6`, `8`.

This gives 486 matched settings. For each setting, the script estimates matched
subgroup prominence using 220 repetitions. For each `kind/background/n`
combination, it estimates background-only divergence noise using 700
repetitions. Rejection rates are taken from the existing tail-factor grid.

The script then computes Pearson and Spearman correlations between rejection
rate and several diagnostic metrics. Bootstrap intervals are included to check
stability.

## Main Result

The signal/noise explanation remains stable across the broad grid.

Overall correlations with rejection rate:

| Metric | Pearson | Spearman |
|---|---:|---:|
| signal over q90 noise | 0.6037 | 0.6729 |
| signal over q95 noise | 0.6626 | 0.7555 |
| signal over top-k noise | 0.8209 | 0.9399 |
| signal over max noise | 0.7602 | 0.8874 |
| matched extreme prominence | 0.5973 | 0.6715 |
| background top-k noise | -0.6509 | -0.6784 |
| background max noise | -0.6336 | -0.6917 |
| divergence-vector correlation | 0.8507 | 0.8933 |

The strongest signal/noise metric is `signal_over_topk_noise`, where the
background noise anchor uses the average of the largest `k` background
divergence values. This is natural because the matched signal is also defined
by a subgroup of size `k`.

## Stability Across Groups

The Spearman correlation between `signal_over_topk_noise` and rejection rate is
stable across several cross-sections:

| Group | Spearman correlation | Bootstrap interval |
|---|---:|---:|
| all settings | 0.9399 | [0.9277, 0.9484] |
| l2 | 0.9422 | [0.9233, 0.9540] |
| l1 | 0.9405 | [0.9228, 0.9523] |
| n = 40 | 0.9249 | [0.8901, 0.9476] |
| n = 80 | 0.9526 | [0.9312, 0.9648] |
| n = 160 | 0.9539 | [0.9384, 0.9629] |
| k = 1 | 0.9696 | [0.9560, 0.9766] |
| k = 2 | 0.9585 | [0.9397, 0.9683] |
| k = 3 | 0.9419 | [0.9173, 0.9577] |
| magnitude = 4 | 0.9506 | [0.9284, 0.9606] |
| magnitude = 6 | 0.9387 | [0.9119, 0.9549] |
| magnitude = 8 | 0.8949 | [0.8480, 0.9230] |

This is the strongest evidence so far that the signal/noise interpretation is
not a one-setting artifact.

The more generic `signal_over_q95_noise` metric is weaker but still consistently
positive. Its Spearman correlation is `0.7555` overall, with positive
correlations in both `l2` and `l1`, all sample sizes, all subgroup sizes, and
all magnitudes.

## Background Noise Alone

Background divergence noise is consistently negatively related to power. For
`background_max_to_mean`, the overall Spearman correlation with rejection rate
is `-0.6917`, with bootstrap interval `[-0.7341, -0.6433]`.

This negative association also persists across groups:

| Group | Spearman correlation |
|---|---:|
| all settings | -0.6917 |
| l2 | -0.7281 |
| l1 | -0.7521 |
| n = 40 | -0.7356 |
| n = 80 | -0.7621 |
| n = 160 | -0.7661 |
| k = 1 | -0.7163 |
| k = 2 | -0.7124 |
| k = 3 | -0.7230 |

This supports the mechanism suggested by the heavy-tail simulations: as the
background produces stronger natural divergence extremes, matched structures
are harder to separate from the background.

## Interpretation

The broad validation supports the following refined statement:

> Across a broad simulation grid, the power of detecting matched co-divergence
> structures is strongly associated with the matched subgroup's prominence
> relative to background divergence noise. Heavy-tailed backgrounds reduce power
> because they increase natural background divergence extremes, thereby lowering
> the signal-to-background-noise contrast.

This remains a simulation-based interpretation rather than a theorem, but it is
now supported across many settings.

## Reporting Recommendation

For future reports, two signal/noise quantities are useful:

1. `signal_over_topk_noise`: strongest empirical association with power and
   naturally matches subgroup size `k`.
2. `signal_over_q95_noise`: more generic and less dependent on knowing the
   subgroup size, but somewhat weaker.

The top-k version may be best for simulation diagnostics, while the q95 version
may be easier to present as a general background-noise summary.
