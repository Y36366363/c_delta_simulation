# Follow-up Stable Diagnostics Summary

Date: 2026-07-18

This update follows the stable-reporting direction after the corrected
normalization. The main reported quantities are permutation p-values, rejection
rates, Wilson intervals, divergence-vector correlations, pairing-normalized
values, and independent-null summaries.

## What Was Tested

The script `scripts/run_followup_stable_diagnostics.py` adds three follow-up
checks:

1. high-replication checks for the independent-null settings that were flagged
   in the extended simulation;
2. normal-background power curves across sample size, matched subgroup size,
   and magnitude;
3. a heavy-tail gradient comparing normal, Student `t_5`, Student `t_3`,
   Student `t_2`, and lognormal backgrounds.

The script also generates three visual summaries in `figures/`.

## High-Replication Independent-Null Checks

The previous extended simulation produced several monitoring flags around
rejection rates `.08` to `.09`. These were re-tested with `1200` repetitions
and `799` permutations per repetition.

The main result is reassuring: most flags return to approximately the nominal
`.05` level.

| Kind | Background | n | k | Magnitude | Rejection Rate | Wilson Interval |
|---|---:|---:|---:|---:|---:|---:|
| l2 | normal | 160 | 1 | 2.5 | .0542 | [.0427, .0685] |
| l2 | normal | 160 | 2 | 4.0 | .0525 | [.0412, .0666] |
| l2 | normal | 160 | 3 | 3.5 | .0542 | [.0427, .0685] |
| l1 | normal | 160 | 2 | 3.5 | .0475 | [.0368, .0610] |
| l1 | normal | 160 | 3 | 3.5 | .0467 | [.0361, .0601] |
| l2 | t2 | 40 | 1 | 10.0 | .0492 | [.0383, .0629] |
| l1 | t2 | 40 | 1 | 10.0 | .0617 | [.0494, .0767] |
| l1 | lognormal | 40 | 3 | 4.5 | .0367 | [.0274, .0489] |

This suggests that the earlier `.08` to `.09` rates were probably Monte Carlo
fluctuations rather than stable evidence of size inflation. The only setting
that remains slightly above `.05` is `l1/t2/n=40/k=1`, but its Wilson interval
still contains `.05`.

## Power Curves

The normal-background power curve was tested across `n = 20, 40, 80, 160`,
`k = 1, 2, 3`, magnitudes from `1.5` to `8.0`, and both `l2` and `l1`.

For a single matched extreme pair (`k = 1`), the first magnitude reaching
approximately `.80` power is:

| Kind | n=20 | n=40 | n=80 | n=160 |
|---|---:|---:|---:|---:|
| l2 | 4.0 | 3.5 | 3.5 | 4.0 |
| l1 | 4.0 | 3.5 | 3.5 | 4.0 |

For matched subgroups (`k = 2` or `k = 3`), the threshold is usually lower,
often around magnitude `3.0`. This continues the earlier finite-sample
interpretation: one dominant matched pair can define a strong structure, but a
small matched subgroup makes the co-divergence signal easier for the
permutation test to distinguish from chance re-pairing.

The slightly higher threshold at `n = 160` for `k = 1` is consistent with a
sparsity effect: with one extreme pair and many background observations, the
single co-divergence structure can be diluted unless its magnitude is large
enough.

## Heavy-Tail Gradient

The heavy-tail gradient used `n = 80`, `k = 2`, magnitude `8.0`, and compared
matched and independent-null behavior.

Matched rejection rates:

| Kind | Normal | t5 | t3 | t2 | Lognormal |
|---|---:|---:|---:|---:|---:|
| l2 | 1.0000 | 1.0000 | .9500 | .5200 | 1.0000 |
| l1 | 1.0000 | 1.0000 | .9667 | .5367 | 1.0000 |

Independent-null rejection rates remain close to the nominal `.05` level. The
largest independent-null rate in this gradient is `l1/lognormal`, `.0767`, with
Wilson interval `[.0516, .1124]`, so it should be treated as a future monitoring
case rather than a conclusion.

The most important substantive result is the Student `t_2` background. It
substantially lowers matched power even when the matched subgroup is present.
This supports the interpretation that power depends not only on whether a
co-occurring extreme structure exists, but also on whether that structure
stands out from the background divergence noise.

## Interpretation

Today's results strengthen three points:

1. The independent-null behavior appears broadly calibrated after
   higher-replication checking.
2. The power curve depends jointly on sample size, matched subgroup size, and
   magnitude. Multi-extreme matched subgroups generally require less magnitude
   than a single matched extreme pair.
3. Heavy-tailed backgrounds, especially Student `t_2`, are not merely another
   null condition. They create a genuine power challenge because the background
   itself can produce large internal divergence.

## Suggested Next Step

The next useful extension is to repeat the heavy-tail gradient with a finer
degree-of-freedom grid, such as Student `t_8`, `t_5`, `t_4`, `t_3`, `t_2.5`,
and `t_2`, while keeping independent-null calibration checks beside matched
power. This would turn the current qualitative tail effect into a more
continuous power curve over tail heaviness.
