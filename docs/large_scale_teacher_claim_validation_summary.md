# Large-Scale Validation of the Paired-Standout Interpretation

Date: 2026-07-31

## Question

Professor Hoorn proposed that `c_delta` is not a general correlation of
internal structures, but a test of whether the same paired observations stand
out from their respective groups in both datasets.

This validation holds the number and magnitude of planted standouts fixed in
both datasets and changes only their paired-index overlap.

## Design

- L1 and L2 divergence;
- `n = 40, 80, 160`;
- normal, `t3`, and `t2` backgrounds;
- planted subgroup size `k / n` approximately `0.05`;
- both backgrounds standardized by their sample MAD;
- planted magnitude `8` on that scale;
- target overlap fractions `0, .25, .50, .75, 1`;
- 300 repetitions and 199 permutations per grid cell;
- 90 grid cells and 27,000 simulated datasets.

The zero-overlap condition is not an ordinary independent null. Both datasets
contain the same number and strength of planted standouts, but they occur at
disjoint paired indices. It directly separates "both groups have standouts"
from "the same paired observations stand out."

## Overall Overlap Gradient

Averaged across sample sizes and backgrounds:

| Kind | 0 overlap | .25 overlap | .50 overlap | .75 overlap | Full overlap |
|---|---:|---:|---:|---:|---:|
| L2 rejection | 0.021 | 0.166 | 0.518 | 0.784 | 0.814 |
| L2 mean divergence corr. | -0.029 | 0.066 | 0.262 | 0.461 | 0.554 |
| L1 rejection | 0.016 | 0.154 | 0.528 | 0.801 | 0.841 |
| L1 mean divergence corr. | -0.032 | 0.066 | 0.263 | 0.458 | 0.550 |

The rejection rate and divergence correlation rise with paired-index overlap.
At zero overlap, rejection is low even though both datasets contain equally
strong planted standouts. This strongly supports the paired-standout
interpretation.

For `n = 40`, `k = 2`, so requested quarter-overlap increments round to only
three distinct realized overlap levels. Small differences between duplicated
rounded levels are Monte Carlo variation rather than a non-monotone mechanism.

## Representative `n = 80` Results

For L2:

| Background | 0 | .25 | .50 | .75 | 1.00 |
|---|---:|---:|---:|---:|---:|
| normal | 0.000 | 0.170 | 1.000 | 1.000 | 1.000 |
| t3 | 0.013 | 0.140 | 0.563 | 0.847 | 0.927 |
| t2 | 0.037 | 0.080 | 0.207 | 0.417 | 0.597 |

For L1:

| Background | 0 | .25 | .50 | .75 | 1.00 |
|---|---:|---:|---:|---:|---:|
| normal | 0.003 | 0.167 | 1.000 | 1.000 | 1.000 |
| t3 | 0.010 | 0.133 | 0.577 | 0.863 | 0.923 |
| t2 | 0.030 | 0.077 | 0.183 | 0.447 | 0.613 |

Thus overlap is the primary signal dimension, while heavy-tailed background
divergence noise moderates the mapping from overlap to power. Full overlap is
not sufficient for uniformly high power under `t2`.

## Independent-Null Calibration

An additional validation used 1,000 repetitions and 499 permutations for each
L1/L2 and background combination at `n = 80`.

- L2 rejection ranged from `0.049` to `0.061`;
- L1 rejection ranged from `0.044` to `0.071`.

The L1-normal cell initially returned `0.071`, with a Wilson interval slightly
above `.05`. A separate 5,000-repetition rerun with a new seed gave:

- L2-normal: `0.0464`, Wilson interval `[0.0409, 0.0526]`;
- L1-normal: `0.0466`, Wilson interval `[0.0411, 0.0528]`.

The initial L1-normal flag is therefore consistent with Monte Carlo
fluctuation rather than stable type-I inflation.

## Large-Scale Row-Aggregation Information Loss

For each repetition, paired observations were assigned exactly the same
absolute magnitudes but independently flipped signs in balanced pairs. The L2
divergence vectors are therefore exactly equal in all repetitions, while the
full pairwise distance matrices differ.

| n | Divergence corr. | Mean matrix corr. | Matrix corr. 2.5% | Median | 97.5% |
|---:|---:|---:|---:|---:|---:|
| 40 | 1.000 | 0.1983 | 0.0570 | 0.1830 | 0.4281 |
| 80 | 1.000 | 0.1795 | 0.0862 | 0.1710 | 0.3237 |
| 160 | 1.000 | 0.1721 | 0.1053 | 0.1681 | 0.2618 |

Perfect salience alignment repeatedly coexists with only weak full-matrix
alignment. The positive residual matrix correlation is expected because both
datasets share the same magnitude profile; sign-dependent relational geometry
is nevertheless discarded by row aggregation.

## Conclusion

The large-scale results support a precise version of the teacher's statement:

> In its current one-dimensional form, `c_delta` tests whether the same paired
> observations have aligned relative divergence salience within their
> respective datasets.

Two qualifications remain important:

1. "stand out" is continuous rather than necessarily a binary outlier label;
2. paired salience alignment is not equivalent to general full internal
   structure alignment.

The next manuscript revision should make paired-index overlap the central
signal concept and treat background tail behavior as a modifier of the
signal-to-background-salience contrast.
