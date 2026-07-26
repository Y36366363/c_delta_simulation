# Signal-to-Background-Divergence-Noise Diagnostics

Date: 2026-07-26

This update follows from the previous heavy-tail cross-validation. The earlier
results showed that heavy-tailed backgrounds reduce matched-power while
independent-null rejection rates remain close to the nominal level. The purpose
of this update is to make the proposed mechanism more quantitative.

## Question

The working interpretation is:

> Heavy-tailed backgrounds reduce power because the background itself produces
> larger divergence-vector extremes, making the matched subgroup less
> distinguishable from natural background divergence noise.

This note tests whether a simple signal-to-background-divergence-noise ratio is
aligned with the observed rejection rates.

## Design

The script `scripts/run_signal_noise_diagnostics.py` uses the central
tail-gradient setting:

- `n = 80`;
- `k = 2`;
- magnitudes `4`, `6`, and `8`;
- backgrounds: normal, `t5`, `t4`, `t3`, `t2.5`, `t2.2`, and `t2`;
- divergence definitions: `l2` and `l1`.

For each background and divergence definition, it estimates background-only
divergence noise using 1,000 repetitions. For each matched setting, it
estimates the divergence prominence of the inserted matched subgroup using 600
repetitions.

The diagnostic quantities include:

- matched extreme divergence divided by the sample mean divergence;
- background divergence coefficient of variation;
- background `q95 / mean`, `top2 / mean`, and `max / mean`;
- signal-over-noise ratios, such as
  `matched_extreme_to_mean / background_q95_to_mean`.

The rejection rates are taken from the higher-replication tail-power
cross-validation table.

## Main Result

The signal-to-noise diagnostics are strongly aligned with matched rejection
rates.

| Kind | Metric | Correlation with rejection rate |
|---|---|---:|
| l2 | matched extreme prominence | 0.8965 |
| l2 | signal over q95 noise | 0.8875 |
| l2 | signal over top2 noise | 0.8462 |
| l2 | signal over max noise | 0.8206 |
| l1 | matched extreme prominence | 0.8444 |
| l1 | signal over q95 noise | 0.8498 |
| l1 | signal over top2 noise | 0.8038 |
| l1 | signal over max noise | 0.7817 |

The background-only max-to-mean ratio is negatively associated with rejection
rate:

- `l2`: correlation `-0.7375`;
- `l1`: correlation `-0.7497`.

This supports the idea that natural background divergence extremes make the
matched subgroup harder to detect.

## Central Slice Example

For `n = 80`, `k = 2`, magnitude `8`, the `l2` signal-over-max-noise ratio
decreases as tails become heavier:

| Background | Rejection rate | Signal/max-noise | Matched extreme/mean | Background max/mean |
|---|---:|---:|---:|---:|
| normal | 1.000 | 1.8707 | 3.9697 | 2.1220 |
| t5 | 1.000 | 1.2782 | 3.5422 | 2.7711 |
| t4 | 0.992 | 1.1369 | 3.3884 | 2.9802 |
| t3 | 0.950 | 0.9157 | 3.1299 | 3.4181 |
| t2.5 | 0.840 | 0.7812 | 2.8800 | 3.6869 |
| t2.2 | 0.704 | 0.6649 | 2.6854 | 4.0386 |
| t2 | 0.560 | 0.6132 | 2.5234 | 4.1150 |

The same pattern appears under `l1`, where the signal-over-max-noise ratio
drops from `2.2597` under normal backgrounds to `0.5377` under `t2`.

## Interpretation

These results make the heavy-tail explanation more concrete:

1. The matched subgroup remains present under heavy-tailed backgrounds.
2. However, the background itself produces stronger divergence-vector extremes.
3. The matched subgroup therefore has lower signal-to-background-noise contrast.
4. Lower contrast is associated with lower rejection rate.

This does not prove a theoretical power law, but it provides a useful
simulation-based mechanism for why heavy-tailed backgrounds reduce power
without necessarily inflating independent-null rejection rates.

## Suggested Next Step

The next methodological step is to formalize the diagnostic into a small set of
pre-specified reporting quantities. A reasonable candidate is:

```text
signal_over_q95_noise =
    matched_extreme_to_mean / background_q95_to_mean
```

This version may be more stable than using the maximum, because the background
maximum is itself noisy under heavy tails. The max-based version is still useful
as a conservative stress check.
