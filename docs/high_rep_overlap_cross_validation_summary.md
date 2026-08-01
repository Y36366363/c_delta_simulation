# High-Replication Paired-Overlap Cross-Validation

Date: 2026-08-01

## Purpose

This validation strengthens the empirical basis for Professor Hoorn's claim
that the statistic responds to whether the same paired observations stand out.
It also distinguishes a deliberately disjoint negative control from the proper
random-pairing null in which chance overlap is allowed.

## Design

### Forced-overlap cross-validation

- `n = 80`, `k = 4`, planted magnitude `8` after sample-MAD scaling;
- overlap `m = 0, 1, 2, 3, 4`;
- normal, `t3`, and `t2` backgrounds;
- L1 and L2 divergence;
- 1,000 repetitions and 199 permutations per cell;
- 30,000 simulated datasets with seeds independent of the earlier grid.

### Random-set null

- both datasets contain four magnitude-8 standouts;
- the two sets of standout indices are selected independently;
- 3,000 repetitions per L1/L2 and background cell;
- 18,000 simulated datasets.

## Forced-Overlap Results

### L2 rejection rates

| Background | 0/4 | 1/4 | 2/4 | 3/4 | 4/4 |
|---|---:|---:|---:|---:|---:|
| normal | 0.000 | 0.175 | 1.000 | 1.000 | 1.000 |
| t3 | 0.016 | 0.129 | 0.604 | 0.842 | 0.924 |
| t2 | 0.030 | 0.066 | 0.224 | 0.433 | 0.540 |

### L1 rejection rates

| Background | 0/4 | 1/4 | 2/4 | 3/4 | 4/4 |
|---|---:|---:|---:|---:|---:|
| normal | 0.000 | 0.194 | 1.000 | 1.000 | 1.000 |
| t3 | 0.017 | 0.117 | 0.565 | 0.853 | 0.937 |
| t2 | 0.038 | 0.071 | 0.201 | 0.422 | 0.586 |

Every background and divergence construction shows a monotone rejection
gradient. The independent rerun closely reproduces the earlier 200-repetition
results. For example, full-overlap `t2` power is `0.540` for L2 with a Wilson
interval `[0.5090, 0.5707]`, and `0.586` for L1 with interval
`[0.5552, 0.6161]`.

The divergence correlations also increase monotonically. Under L2 they move:

- normal: `-0.0423` to `0.8558`;
- t3: `-0.0275` to `0.5210`;
- t2: `-0.0159` to `0.2766`.

This confirms that tail background attenuates the continuous expression of a
fixed overlap signal.

## Random-Set Null and Chance Overlap

If two sets of `k` indices are independently selected from `n`, their overlap
`M` is hypergeometric:

```text
P(M = m) = choose(k, m) choose(n-k, k-m) / choose(n, k),
E(M) = k^2 / n.
```

For `n = 80`, `k = 4`, the theoretical probabilities are:

| m | 0 | 1 | 2 | 3 | 4 |
|---:|---:|---:|---:|---:|---:|
| Probability | 0.8112 | 0.1778 | 0.0108 | 0.0002 | 0.000001 |

The simulated mean overlaps were `0.1963-0.2103`, close to the theoretical
expectation `0.2`. Observed layer frequencies were also close to the
hypergeometric probabilities.

Overall random-set-null rejection rates:

| Kind | normal | t3 | t2 |
|---|---:|---:|---:|
| L2 | 0.0460 | 0.0453 | 0.0377 |
| L1 | 0.0463 | 0.0493 | 0.0437 |

All are close to the nominal level. Mean divergence correlations range only
from `-0.0016` to `0.0036`.

Conditional rejection rises with realized chance overlap. For example, under
L2-normal it is `0.0004` when `M=0`, `0.1776` when `M=1`, and `1.000` among the
45 simulations with `M=2`. This does not indicate type-I inflation: the rare
overlap layers are real finite-sample salience alignment events within the
random-set mixture, and their hypergeometric frequency keeps the unconditional
permutation test calibrated.

## Interpretation

The results distinguish three cases:

1. **Disjoint negative control:** both groups have standouts, but none are
   paired; upper-tail rejection is conservative and near zero.
2. **Random-set null:** both groups have standouts and chance overlap is
   allowed; unconditional rejection remains near `.05`.
3. **Above-chance overlap alternative:** rejection rises monotonically with the
   number of shared paired indices, with attenuation under heavy tails.

This is a stronger and more precise version of the teacher's interpretation:

> The sparse-signal component of `c_delta` responds to paired salience overlap
> above its random-pairing expectation, while the continuous divergence
> contrast determines how detectable that overlap is.

## Meeting-Relevant Point

A useful question for Professor Hoorn is whether the revised paper should
explicitly distinguish:

- the estimand: continuous paired divergence-salience alignment;
- the binary-overlap model: an interpretable limiting case;
- the randomization null: chance pairing of the observed salience profiles.

Making these three layers explicit would prevent the method from being
misdescribed either as a general internal-structure correlation or merely as a
test for the presence of outliers in both samples.
