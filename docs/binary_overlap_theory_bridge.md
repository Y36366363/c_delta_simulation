# Binary-Overlap Theory and Continuous Divergence

Date: 2026-08-01

## Purpose

This note translates the phrase "the same paired observations stand out" into
a simple theoretical model and checks how the model carries over to continuous
L1/L2 divergence scores.

## Binary Salience Model

Let `A_i` and `B_i` be binary indicators that observation `i` stands out in
datasets X and Y. Suppose each dataset has exactly `k` standouts among `n`
paired observations, and exactly `m` indices are standouts in both.

Then

```text
mean(A) = mean(B) = k / n
mean(A B) = m / n,
```

and their Pearson correlation is

```text
r_binary = (n m - k^2) / (k (n - k)).
```

Consequences:

- full overlap, `m = k`, gives `r_binary = 1`;
- chance overlap has expectation `m = k^2 / n`, giving expected correlation 0;
- disjoint standouts, `m = 0`, give `r_binary = -k / (n - k)`;
- overlap above chance produces positive salience association.

For `n = 80` and `k = 4`, the theoretical correlations for `m = 0,...,4`
are `-0.0526, 0.2105, 0.4737, 0.7368, 1.0000`.

This provides a direct theoretical version of Professor Hoorn's
interpretation. The actual divergence vectors are continuous, so the binary
formula is an idealized upper-reference curve rather than an exact formula for
the observed statistic.

## Simulation Bridge

Settings:

- `n = 80`, `k = 4`;
- overlap `m = 0, 1, 2, 3, 4`;
- planted magnitudes `4, 6, 8, 12` after sample-MAD scaling;
- normal, `t3`, and `t2` backgrounds;
- L1 and L2 divergence;
- 200 repetitions and 199 permutations per cell;
- 120 cells and 24,000 simulated datasets.

Across the full grid, the correlation between the binary theoretical curve and
the mean continuous divergence correlation is:

- L2: `0.7065`;
- L1: `0.7213`.

Thus paired overlap remains a strong organizing variable, but continuous
background salience attenuates the idealized binary signal.

## Representative Magnitude-8 L2 Curves

| Background | Overlap | Binary theory | Mean divergence corr. | Rejection |
|---|---:|---:|---:|---:|
| normal | 0/4 | -0.0526 | -0.0451 | 0.005 |
| normal | 1/4 | 0.2105 | 0.1782 | 0.185 |
| normal | 2/4 | 0.4737 | 0.4047 | 1.000 |
| normal | 3/4 | 0.7368 | 0.6337 | 1.000 |
| normal | 4/4 | 1.0000 | 0.8493 | 1.000 |
| t3 | 0/4 | -0.0526 | -0.0424 | 0.005 |
| t3 | 1/4 | 0.2105 | 0.1139 | 0.105 |
| t3 | 2/4 | 0.4737 | 0.2494 | 0.585 |
| t3 | 3/4 | 0.7368 | 0.3976 | 0.900 |
| t3 | 4/4 | 1.0000 | 0.5465 | 0.945 |
| t2 | 0/4 | -0.0526 | -0.0093 | 0.050 |
| t2 | 1/4 | 0.2105 | 0.0696 | 0.095 |
| t2 | 2/4 | 0.4737 | 0.1317 | 0.190 |
| t2 | 3/4 | 0.7368 | 0.2041 | 0.430 |
| t2 | 4/4 | 1.0000 | 0.2716 | 0.500 |

At the same binary overlap, heavier tails move the continuous divergence
correlation further below the theoretical curve. The reason is that the
non-planted observations also acquire large continuous salience values.

## Magnitude as Convergence Toward the Binary Model

For full overlap, increasing planted magnitude moves the continuous salience
profile closer to a clean two-level standout/background profile.

L2 full-overlap mean divergence correlation and power:

| Background | Magnitude 4 | Magnitude 6 | Magnitude 8 | Magnitude 12 |
|---|---:|---:|---:|---:|
| normal corr. | 0.3905 | 0.7040 | 0.8493 | 0.9530 |
| normal power | 0.915 | 1.000 | 1.000 | 1.000 |
| t3 corr. | 0.1045 | 0.3492 | 0.5465 | 0.7676 |
| t3 power | 0.160 | 0.760 | 0.945 | 0.985 |
| t2 corr. | 0.0427 | 0.1296 | 0.2716 | 0.5101 |
| t2 power | 0.080 | 0.215 | 0.500 | 0.800 |

This gives a unified interpretation:

```text
paired standout overlap
        x standout/background separation
        / background salience noise
        -> continuous divergence alignment
        -> permutation power.
```

## Practical Interpretation

The binary model should not replace the continuous statistic. It is useful as:

1. a transparent theoretical explanation of the paired-overlap target;
2. an interpretable limiting case when standouts are sharply separated;
3. a diagnostic showing why identical overlap can yield different power under
   different magnitudes and tail backgrounds.

Recommended statement:

> The paired-index overlap of salient observations is a central signal
> component, while the continuous divergence contrast determines how strongly
> that overlap is expressed in the statistic.
