# Background-Masking Diagnostics Summary

Date: 2026-07-30

This update directly tests Professor Hoorn's proposed masking mechanism. The
question is whether heavy-tailed backgrounds produce large divergence scores
at indices that are not aligned across `x` and `y`, and whether those random
background products weaken detection of the planted matched subgroup.

## Design

The diagnostic uses:

- `n = 80`, `k = 2`, and signal magnitude `8`;
- `l2` and `l1` divergence definitions;
- normal, `t5`, `t4`, `t3`, `t2.5`, `t2.2`, and `t2` backgrounds;
- common scale-parameter and common-MAD designs;
- 500 repetitions and 299 permutations per setting.

Because the planted subgroup is known in simulation, the script compares:

- the indices of the largest background divergence scores in `D_x` and `D_y`;
- the largest background divergence with the mean planted divergence;
- planted paired products with background paired products;
- planted paired products with their random-pairing expectation;
- rejection rates conditional on a pre-specified masking event.

The masking event is:

```text
maximum background paired product
    >
mean planted paired product.
```

This is an explanatory simulation diagnostic, not a statistic available when
the subgroup is unknown.

## Unmatched Background Extremes

The largest background divergence increasingly outranks the planted subgroup
as tails become heavier.

Under the common scale-parameter design, the probability that at least one
side has its largest divergence at a background index is:

| Kind | Normal | t3 | t2 |
|---|---:|---:|---:|
| L2 | 0.000 | 0.540 | 0.904 |
| L1 | 0.000 | 0.460 | 0.912 |

After common-MAD scaling, the corresponding `t2` probabilities decrease but
remain high:

- L2: `0.840`;
- L1: `0.830`.

The top-two background divergence indices in `D_x` and `D_y` overlap only
about `0.02-0.03` on average across the tail settings. This is close to the
chance overlap `k / (n-k) = 2 / 78 = 0.0256`.

Thus, heavy tails produce strong background divergence extremes, but those
extremes usually occur at different indices in the two vectors. They do not
form a competing matched subgroup; instead, they add unmatched leverage.

## Paired-Product Masking

The probability that the largest background paired product exceeds the mean
planted paired product also increases with tail heaviness.

For `t2`:

| Kind | Scale design | Masking probability |
|---|---|---:|
| L2 | common scale parameter | 0.248 |
| L2 | common MAD | 0.162 |
| L1 | common scale parameter | 0.192 |
| L1 | common MAD | 0.112 |

Masking is strongly associated with failure to reject. For the original `t2`
scale-parameter design:

| Kind | Rejection with masking | Rejection without masking |
|---|---:|---:|
| L2 | 0.1935 | 0.6649 |
| L1 | 0.3438 | 0.5941 |

After common-MAD scaling:

| Kind | Rejection with masking | Rejection without masking |
|---|---:|---:|
| L2 | 0.2222 | 0.7852 |
| L1 | 0.3393 | 0.7950 |

The same direction appears in the conditional masking probabilities. Under
common-MAD `t2`, the L2 masking probability is `0.0519` among rejected runs
and `0.4118` among non-rejected runs. For L1, the corresponding values are
`0.0511` and `0.2891`.

## Mechanism-Specific Product Contrast

The planted paired products remain larger than both background and
random-pairing products, but their relative advantage decreases as tails
become heavier.

Under the common scale-parameter design, the median planted-to-background
product ratio changes from:

- L2: `18.4666` under normal backgrounds to `6.9563` under `t2`;
- L1: `36.3715` under normal backgrounds to `12.4597` under `t2`.

The median planted-to-random-pairing ratio changes from:

- L2: `3.9772` to `2.5640`;
- L1: `5.3441` to `3.3746`.

Common-MAD scaling restores part of this contrast, consistent with the earlier
scale validation, but it does not return the heavy-tail settings to the normal
background level.

## Interpretation

The results support a more direct version of the masking explanation:

> Heavy-tailed backgrounds increasingly produce large divergence scores at
> indices that are not aligned across the two divergence vectors. These
> unmatched extremes reduce the planted subgroup's paired-product advantage.
> When a background paired product overtakes the planted mean product,
> rejection is substantially less likely.

This remains simulation evidence rather than a causal theorem. However, it
goes beyond the earlier maximum-to-mean ratio by locating the extremes,
checking their cross-vector index overlap, and relating a pre-specified
paired-product masking event to detection.

## Next Step

The next natural extension is a pre-specified sparse-signal comparator, such
as a top-k or scan-style statistic. It should be calibrated independently and
compared with the global statistic under both fixed `k` and fixed `k / n`
designs.
