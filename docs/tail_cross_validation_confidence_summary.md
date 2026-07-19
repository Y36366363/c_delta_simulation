# Tail Cross-Validation Confidence Summary

Date: 2026-07-19

This note checks whether the current heavy-tail conclusions are sufficiently
stable. The earlier factor grid was broad but used moderate repetition per
cell. The new cross-validation focuses on the key claims with higher
replication and independent seeds.

## Validation Design

Three targeted checks were added in `scripts/run_tail_cross_validation.py`:

1. matched tail-power validation for the central slice `n = 80`, `k = 2`,
   magnitudes `4`, `6`, and `8`, using `500` repetitions and `399`
   permutations;
2. independent-null tail-size validation for `n = 80`, `k = 2`, magnitude `8`,
   using `1000` repetitions and `499` permutations;
3. a fixed-`k` versus fixed-proportion comparison across `n = 40, 80, 160`,
   with normal, `t_3`, and `t_2` backgrounds.

## Confidence Judgment

The main heavy-tail conclusion is now strong:

- matched power decreases clearly as tails become heavier;
- the decrease is repeated under independent seeds;
- the effect is visible under both `l2` and `l1`;
- the effect persists across magnitudes, although larger magnitudes partially
  compensate for heavier tails.

For example, at `n = 80`, `k = 2`, magnitude `8`:

| Kind | Normal | t5 | t4 | t3 | t2.5 | t2.2 | t2 |
|---|---:|---:|---:|---:|---:|---:|---:|
| l2 | 1.000 | 1.000 | .992 | .950 | .840 | .704 | .560 |
| l1 | 1.000 | 1.000 | 1.000 | .974 | .834 | .710 | .558 |

The Wilson intervals for the heavier-tail settings are well separated from the
normal and moderate-tail settings. For `l2`, magnitude `8`, the interval for
`t_3` is `[.9272, .9659]`, while the interval for `t_2` is `[.5162, .6029]`.
This is a large and stable separation, not a borderline simulation artifact.

The null-calibration conclusion is also strong for the central slice. With
`1000` repetitions, the independent-null rejection rates remain close to alpha
`.05`:

| Kind | Normal | t5 | t4 | t3 | t2.5 | t2.2 | t2 |
|---|---:|---:|---:|---:|---:|---:|---:|
| l2 | .040 | .046 | .052 | .048 | .063 | .043 | .054 |
| l1 | .049 | .054 | .042 | .050 | .049 | .050 | .047 |

This supports the interpretation that heavy tails mainly reduce power rather
than obviously inflating the type-I rejection rate.

## Fixed k versus Fixed Proportion

The previous sample-size result looked counterintuitive because power decreased
from `n = 40` to `n = 160` in some fixed-`k` settings. The cross-validation
clarifies this.

When `k` is fixed at `2`, the matched subgroup becomes sparser as `n` grows.
For example, under `l2`, `t_2`, magnitude `8`, power decreases from `.648` at
`n = 40` to `.348` at `n = 160`.

When the subgroup proportion is fixed near `5%`, the pattern changes. Under
the same `l2`, `t_2`, magnitude `8` setting, power is `.672` at `n = 40`,
`.632` at `n = 80`, and `.776` at `n = 160`.

This supports a more careful statement: large `n` is not inherently harmful,
but a fixed-size sparse subgroup can be diluted as `n` grows. Future sample-size
studies should distinguish fixed `k` from fixed `k / n`.

## What Is Now Well Supported

The following claims are now sufficiently supported for a progress report:

1. The heavy-tail power decline is real and stable in the simulated settings.
2. The `t_2` result is part of a continuous tail-heaviness pattern.
3. The power decline is not explained by an obvious independent-null
   calibration failure.
4. Increasing magnitude or subgroup size can compensate for heavier
   background tails.
5. Fixed-`k` sample-size comparisons should not be interpreted without also
   considering subgroup proportion.

## What Still Needs Careful Wording

The current evidence is simulation-based. It is strong enough for reporting,
but not yet a theorem. The best wording is therefore:

> In these simulation settings, heavy-tailed backgrounds reduce the power of
> detecting matched co-divergence structures, while independent-null rejection
> rates remain close to the nominal level.

Avoid saying that heavy tails always reduce power in all possible settings.
Also avoid saying that type-I error is proven exact under all heavy-tailed
backgrounds.

## Suggested Next Step

The most useful next methodological step is to define a
signal-to-background-divergence-noise ratio. The current simulations suggest
that this ratio may explain why power decreases as tails become heavier.
