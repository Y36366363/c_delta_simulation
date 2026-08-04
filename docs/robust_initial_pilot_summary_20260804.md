# Stage-1 Initial Pilot for Robust c_delta

Date: 2026-08-04

## Purpose

This is the first direct replacement test of the original pilot using the
Huber robust-reference profile. The design follows the project's original
`run_pilot.py` scenarios so that the direction of the old baseline remains
visible.

Methods:

- `original_l2`: existing pairwise RMS divergence;
- `huber_reference`: Huber centre, all-observation distance profile;
- `huber_reference_cap6`: same profile with a prospective `6 x MAD` cap;
- `iqr_reference`: earlier fit-without/score-all baseline.

Settings for the one-dataset pilot were `n = 60`, 499 permutations, and 500
bootstrap resamples. Repeated checks used 300 datasets per scenario and 199
permutations per dataset.

Outputs:

- `results/robust_initial_pilot_20260804.tsv`;
- `results/robust_initial_repeated_20260804.tsv`;
- `scripts/run_robust_initial_pilot.py`.

## Repeated Results

| Scenario | Original L2 | Huber reference | Huber cap6 | IQR reference |
|---|---:|---:|---:|---:|
| Null normal | .050 | .0367 | .0367 | .040 |
| Aligned normal | 1.000 | 1.000 | 1.000 | 1.000 |
| Inverted divergence | .060 | .000 | .000 | .000 |
| Heavy-tailed null | .0667 | .060 | .0567 | .060 |
| Skewed null | .0633 | .0567 | .050 | .0533 |
| Contaminated aligned | 1.000 | 1.000 | 1.000 | 1.000 |

The repeated null rates are Monte Carlo estimates from only 300 datasets. They
are compatible with the earlier high-replication calibration, but should not be
treated as final size estimates.

## Interpretation

### 1. Basic power direction is preserved

The new profiles retain full power in the aligned-normal and contaminated-
aligned scenarios. This confirms that robust centre fitting does not remove the
paired-salience signal in the first baseline settings.

### 2. The upper-tail test does not detect reverse salience alignment

The Huber and IQR profiles have zero upper-tail rejection for the
`inverted_divergence` scenario. This is expected: the current primary
alternative is positive salience alignment. If negative alignment becomes
scientifically relevant, use the already implemented `less` or `two-sided`
alternative rather than changing the centre definition.

### 3. Heavy-tail and skew null calibration remains close to nominal

The robust versions remain near `.05` in the preliminary heavy-tail and
skew-null checks. The cap6 version is slightly more conservative in this small
pilot. This agrees with the project's earlier conclusion that calibration
should be stated only for independent/exchangeable pairing.

### 4. Raw values are not comparable across profile definitions

In the one-dataset `aligned_normal` example, original L2 had raw value about
`1.084`, while Huber reference had raw value about `1.519`. Both had very high
profile correlation and identical rejection. The difference is caused by the
profile coefficient of variation, as predicted by

```text
c_delta = 1 + corr(S_x, S_y) CV(S_x) CV(S_y).
```

Therefore, stage-1 reports should emphasise profile correlation and permutation
p-values, with raw c_delta retained as a method-specific descriptive value.

## Stage-1 Decision

The Huber robust-reference profile is viable for the next stage and does not
require a new project. Keep the same project so historical baselines,
normalisation checks, and teacher-feedback simulations remain directly
comparable.

Next routine test (no theory decision required): repeat this baseline over
`n = 20, 40, 80, 160`, L1/L2-compatible profile choices, and contamination
fractions `0%, 1%, 5%, 10%`, while reserving Sol for any decision about changing
the estimand or making the bounded version primary.
