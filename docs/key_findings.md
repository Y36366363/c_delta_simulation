# c_delta Project: Key Findings

Last updated: 2026-07-31

This is the central, cumulative record of the project's most important
findings. It is intended for quick retrieval when preparing emails, follow-up
notes, presentations, and the final report.

## Maintenance Rules

- Add new entries to the dated update log in reverse chronological order.
- Change the main findings only after independent checking or material
  refinement.
- Keep mathematical identities separate from simulation interpretations.
- Record representative values and the detailed source document.
- Preserve the limitations and reporting language when reusing conclusions.

## Evidence Labels

- **Mathematical identity**: follows algebraically from the corrected
  definition.
- **Strong simulation evidence**: replicated with independent seeds, higher
  repetitions, multiple settings, or both L1 and L2.
- **Focused simulation evidence**: supported in a targeted diagnostic but not
  yet broadly validated.
- **Working interpretation**: consistent with the evidence, but not a theorem
  or established causal mechanism.

## Executive Summary

> In its current one-dimensional form, `c_delta` measures positive alignment
> between paired observation-level divergence salience profiles, not general
> correlation of full internal structures. After the numerator correction, it
> is an affine rescaling of the Pearson correlation between the divergence
> vectors for a fixed sample. Alignment may be sparse or distributed.
> Heavy-tailed backgrounds weaken detection by generating large, usually
> unmatched background divergence scores.

## Main Findings

### 1. Corrected Formula and Reference Value

**Evidence: Mathematical identity**

```text
c_delta = mean(D_x D_y) / (mean(D_x) mean(D_y)).
```

The missing `1 / n` in the original numerator inflated old raw values by `n`:

```text
c_delta_corrected = c_delta_old / n.
```

The corrected random-pairing reference is `1`, not `0`. Plots should mark `1`
or report `c_delta - 1`.

The correction changes raw values and raw intervals. It does not change
within-sample permutation ordering, permutation p-values, rejection decisions,
or pairing-normalized values.

Source: `docs/normalization_revision_note.md`.

### 2. Exact Relationship with Divergence Correlation

**Evidence: Mathematical identity and numerical verification**

```text
c_delta
  = 1 + corr(D_x, D_y) CV(D_x) CV(D_y).
```

During permutation of `D_y`, the CV product remains fixed and positive.
Corrected `c_delta` and the Pearson correlation of the divergence vectors
therefore rank all permutations identically and give the same one-sided
permutation p-value.

Across 12,000 matched and independent-null datasets with 299 permutations:

- maximum reported identity error: below `1e-14`;
- permutation p-value mismatch count: `0`.

The divergence-vector correlation is mathematically central rather than an
optional secondary diagnostic.

Source: `docs/teacher_feedback_validation_summary.md`.

### 3. What the Statistic Detects

**Evidence: Strong simulation evidence**

`c_delta` detects positive alignment of paired observation-level divergence
salience rather than ordinary raw association or general full-matrix internal
structure.

- A matched extreme or subgroup increases divergence alignment and rejection.
- A deliberately mismatched subgroup does not produce the same behavior.
- Independent-null designs allowing chance overlap should be used for type-I
  statements.
- Deliberately disjoint mismatch is a negative control, not a genuine null.

Recommended wording:

> The statistic tests whether observations that are relatively peripheral or
> central in one dataset tend to be similarly peripheral or central in the
> other.

For one-dimensional L2 divergence,

```text
D_i^2 = n / (n - 1) * ((x_i - x_bar)^2 + s_x^2).
```

The divergence ranking is therefore exactly the absolute-deviation-from-mean
ranking. The full distance matrix has been compressed to an observation-level
salience vector.

Source: `docs/paired_salience_reframing.md`.

### 4. Single Extreme and Finite-Sample Resolution

**Evidence: Strong simulation evidence**

A single dominant matched observation can define a strong co-divergence
structure. In small samples, its test is limited because a random permutation
can reconstruct the pairing with probability approximately `1 / n`.

For a subgroup of size `k`, exact reconstruction belongs to a layer of
probability approximately:

```text
1 / choose(n, k).
```

This is a permutation-layer probability, not the p-value. Subgroups with
`k = 2` or `k = 3` are generally more stable than a single pair.

Source: `docs/finite_sample_permutation_resolution.md`.

### 5. L1 and L2 Give Similar Qualitative Results

**Evidence: Strong simulation evidence**

The matched-versus-null pattern and heavy-tail power decline appear under:

- `l2`: root-mean-squared pairwise divergence;
- `l1`: mean absolute pairwise divergence.

The phenomenon is therefore broader than the squaring operation. The corrected
original statistic should remain primary, with L1 as the first pre-specified
sensitivity analysis.

### 6. Heavy-Tail Power Decline

**Evidence: Strong simulation evidence**

At `n = 80`, `k = 2`, signal magnitude `8`:

| Kind | Normal | t5 | t4 | t3 | t2.5 | t2.2 | t2 |
|---|---:|---:|---:|---:|---:|---:|---:|
| L2 | 1.000 | 1.000 | 0.992 | 0.950 | 0.840 | 0.704 | 0.560 |
| L1 | 1.000 | 1.000 | 1.000 | 0.974 | 0.834 | 0.710 | 0.558 |

For L2:

```text
t3 Wilson interval: [0.9272, 0.9659]
t2 Wilson interval: [0.5162, 0.6029]
```

The decline is continuous across tail heaviness, not an isolated `t2` anomaly.
It remains a simulation finding rather than a universal theorem.

Source: `docs/tail_cross_validation_confidence_summary.md`.

### 7. Heavy Tails Mainly Reduce Power, Not Null Calibration

**Evidence: Strong simulation evidence in independent/exchangeable settings**

Independent-null rejection rates with 1,000 repetitions:

| Kind | Normal | t5 | t4 | t3 | t2.5 | t2.2 | t2 |
|---|---:|---:|---:|---:|---:|---:|---:|
| L2 | 0.040 | 0.046 | 0.052 | 0.048 | 0.063 | 0.043 | 0.054 |
| L1 | 0.049 | 0.054 | 0.042 | 0.050 | 0.049 | 0.050 | 0.047 |

Recommended wording:

> In these independent and exchangeable simulation settings, heavy-tailed
> backgrounds reduce matched power while independent-null rejection rates
> remain close to the nominal level.

Do not extend this calibration claim to clustered, longitudinal, or dependent
data without an appropriate permutation scheme.

### 8. Scale Confounding Explains Part of the Tail Effect

**Evidence: Strong focused simulation evidence**

At `n = 80`, `k = 2`, magnitude `8`:

| Kind | Design | Normal | t3 | t2.5 | t2.2 | t2 |
|---|---|---:|---:|---:|---:|---:|
| L2 | Common scale parameter | 1.0000 | 0.9267 | 0.8100 | 0.6500 | 0.5433 |
| L2 | Common MAD | 1.0000 | 0.9733 | 0.9400 | 0.8033 | 0.7000 |
| L1 | Common scale parameter | 1.0000 | 0.9800 | 0.8433 | 0.7067 | 0.5133 |
| L1 | Common MAD | 1.0000 | 1.0000 | 0.9067 | 0.8367 | 0.7433 |

Common-MAD scaling attenuates but does not remove the decline. The original
effect reflects both unequal effective scale and residual tail-shape/masking
effects.

Same-variance comparisons near two degrees of freedom require caution because
unit-variance scaling strongly contracts the central bulk.

### 9. Matched-Null Separation Narrows

**Evidence: Strong focused simulation evidence**

Matched median minus independent-null 95th percentile:

| Kind | Normal | t3 | t2 |
|---|---:|---:|---:|
| L2 | 0.175810 | 0.060001 | 0.001736 |
| L1 | 0.441922 | 0.118644 | 0.015104 |

Matched median minus median conditional-permutation 95th percentile:

| Kind | Normal | t3 | t2 |
|---|---:|---:|---:|
| L2 | 0.183904 | 0.062147 | 0.009407 |
| L1 | 0.379873 | 0.135322 | 0.013741 |

Common-MAD scaling restores part of the separation but does not return
heavy-tail results to the normal-background level.

### 10. Signal-to-Background Diagnostics Explain Power

**Evidence: Strong broad simulation association**

Across 486 matched settings, `signal_over_topk_noise` had:

```text
Spearman correlation with rejection rate = 0.9399
bootstrap interval = [0.9277, 0.9484]
```

The association remains strongly positive across L1/L2, all tested sample
sizes, subgroup sizes, and magnitudes.

This is an explanatory simulation diagnostic, not yet a proposed inferential
statistic.

Source: `docs/signal_noise_broad_validation_summary.md`.

### 11. Direct Evidence for Unmatched Background Masking

**Evidence: Strong focused simulation evidence**

Probability that at least one side's maximum divergence occurs at a background
index under the common scale-parameter design:

| Kind | Normal | t3 | t2 |
|---|---:|---:|---:|
| L2 | 0.000 | 0.540 | 0.904 |
| L1 | 0.000 | 0.460 | 0.912 |

The top-two background indices in `D_x` and `D_y` overlap only `0.02-0.03`,
close to the chance value `2 / 78 = 0.0256`. Heavy tails create strong but
usually unmatched leverage rather than a competing matched subgroup.

Masking event:

```text
maximum background paired product
    >
mean planted paired product.
```

Original `t2` design:

| Kind | Rejection with masking | Rejection without masking |
|---|---:|---:|
| L2 | 0.1935 | 0.6649 |
| L1 | 0.3438 | 0.5941 |

Common-MAD `t2`:

| Kind | Rejection with masking | Rejection without masking |
|---|---:|---:|
| L2 | 0.2222 | 0.7852 |
| L1 | 0.3393 | 0.7950 |

Working interpretation:

> Heavy-tailed backgrounds produce large divergence scores at indices that are
> usually not aligned across the two vectors. These unmatched extremes reduce
> the planted subgroup's paired-product advantage.

Source: `docs/background_masking_diagnostics_summary.md`.

### 12. Fixed k and Fixed Proportion Are Different Alternatives

**Evidence: Strong simulation evidence**

For `t2`, signal magnitude `6`:

| Kind | Design | n=40 | n=80 | n=160 |
|---|---|---:|---:|---:|
| L2 | Fixed `k = 2` | 0.3833 | 0.2633 | 0.1233 |
| L2 | Fixed `k/n = .05` | 0.3833 | 0.4467 | 0.4700 |
| L1 | Fixed `k = 2` | 0.3900 | 0.2400 | 0.1267 |
| L1 | Fixed `k/n = .05` | 0.3900 | 0.4767 | 0.5300 |

At `n = 160`:

```text
L2 fixed k:           [0.0908, 0.1654]
L2 fixed proportion:  [0.4143, 0.5265]
L1 fixed k:           [0.0937, 0.1691]
L1 fixed proportion:  [0.4735, 0.5857]
```

Recommended wording:

> Larger sample size is not inherently harmful. When `k` remains fixed, the
> affected proportion decreases and a global averaging statistic can dilute
> the sparse signal.

Source: `docs/fixed_fraction_tail_validation_summary.md`.

### 13. Salience Alignment Can Be Distributed, Not Only Sparse

**Evidence: Mathematical identity and strong focused simulation evidence**

In a diffuse-aligned design with no strong outliers:

- maximum/median absolute deviation: about `1.30`;
- mean raw Pearson: approximately `0`;
- mean full distance-matrix correlation: approximately `0.01`;
- L2 divergence correlation: `0.6158`;
- L2 rejection rate: `0.976`;
- L1 divergence correlation: `0.4042`;
- L1 rejection rate: `0.800`.

Thus, "the same observations stand out" should be understood as continuous
paired salience, not only a shared extreme subgroup.

When only two moderately high observations are aligned and the remainder of
the profile is shuffled, power is only `0.186` for L2 and `0.220` for L1.
When two much stronger magnitude-4 observations are aligned, power is `1.000`.

The test responds to the strength and distribution of alignment across the
salience profile.

Source: `docs/paired_salience_reframing.md`.

## Reporting Rules

1. Use the corrected raw formula everywhere.
2. Mark `1` as the random-pairing reference or report `c_delta - 1`.
3. Treat divergence Pearson correlation as mathematically equivalent for
   one-sided permutation ordering.
4. Describe Wilson intervals as Monte Carlo uncertainty intervals only.
5. Use independent-null results for type-I statements.
6. Limit calibration claims to independent/exchangeable settings.
7. Call `1 / choose(n, k)` a permutation-layer probability, not a p-value.
8. Write `normal, t10, t8, t5, ...`; do not imply `t10` is normal.
9. Use "signal magnitude," not "scale," for the planted value.
10. Keep fixed `k` and fixed `k / n` in separate tables.
11. Describe heavy tails as increasing background extremeness, unevenness, and
    unmatched leverage, not simply variance.
12. Label planted-subgroup diagnostics as simulation-only.

## Open Questions

### High Priority

1. Compare the global statistic with a pre-specified top-k or scan-style
   comparator under fixed `k` and fixed `k / n`.
2. Regenerate all older raw `c_delta` summaries before the final report.
3. Extend direct masking diagnostics beyond `n = 80`, `k = 2`, magnitude `8`.

### Later Sensitivity Work

4. Implement a pre-specified Huberized divergence after robust scaling.
5. Clarify the intended rank-based question.
6. Give every variant its own permutation calibration and independent-null
   validation under normal, heavy-tailed, and contamination-mixture settings.

### Theory and Framing

7. Develop connections to energy statistics, distance covariance, HSIC, MMD,
   and related distance/kernel methods.
8. Investigate whether a sparse comparator can improve fixed-handful detection
   while preserving the structural interpretation.

## Dated Update Log

### 2026-07-31

- Derived the exact one-dimensional L2 salience formula.
- Reframed the estimand as paired observation-level divergence salience.
- Validated distributed, sparse, null, and reverse salience alternatives.
- Compared the compressed salience target with full distance-matrix
  correlation.
- Positioned the method relative to distance correlation, HSIC, energy
  distance, MMD, and Mantel-type matrix correlation.

### 2026-07-30

- Confirmed the exact identity and identical permutation ordering.
- Added common-MAD and common-variance tail comparisons.
- Retained complete matched and null statistic distributions.
- Added systematic fixed-`k` versus fixed-proportion validation.
- Added direct unmatched-background and paired-product masking diagnostics.

### 2026-07-26

- Added signal-to-background-divergence-noise diagnostics.
- Validated the top-k signal/noise relationship across 486 settings.

### 2026-07-19

- Cross-validated the continuous heavy-tail power decline.
- Confirmed independent-null rejection rates remain near `.05`.
- Introduced fixed `k` versus fixed proportion.

### 2026-07-16 to 2026-07-18

- Corrected the missing numerator `1 / n`.
- Changed the permutation reference mean from `n` to `1`.
- Established stable reporting quantities.
- Rechecked flagged null settings with higher replication.

### 2026-07-11 to 2026-07-15

- Established the finite-sample permutation-resolution interpretation.
- Extended from a single pair to matched subgroups.
- Added L1/L2 comparisons and calibrated subgroup simulations.

### 2026-07-09 to 2026-07-10

- Established matched, mismatched, x-only, y-only, and independent-null
  scenarios.
- Formed the central interpretation of co-occurring internal divergence
  structure.
