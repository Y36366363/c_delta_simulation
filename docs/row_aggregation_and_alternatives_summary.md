# Row Aggregation and Salience Alternatives

Date: 2026-07-31

## Main Conclusion

The current one-dimensional statistic tests paired divergence-salience
alignment. It is not an injective comparison of full internal geometry.

## Exact Information-Loss Counterexample

Consider

```text
x = (-1, -2, -3, -4,  5,  5)
y = ( 1, -2, -3,  4,  5, -5).
```

Both vectors have mean zero and identical corresponding absolute deviations.
Their L2 divergence vectors are therefore exactly equal, although their
pairwise geometries differ:

- maximum paired divergence difference: `0`;
- divergence correlation: `1.0000`;
- corrected `c_delta`: `1.03375`;
- raw Pearson correlation: `-0.0500`;
- full distance-matrix correlation: `-0.04018`.

This exact many-to-one counterexample shows that perfect salience alignment
does not imply aligned full pairwise structure. Row aggregation retains how
peripheral each observation is, but loses which particular observations it is
near to or far from.

## Directional Alternative Validation

Settings: `n = 80`, 400 repetitions, 399 permutations, L2/L1 divergence, and
positive diffuse alignment, random-pairing null, and negative diffuse
alignment.

| Kind | Signal | Mean divergence corr. | Greater | Less | Two-sided |
|---|---|---:|---:|---:|---:|
| L2 | positive | 0.6171 | 0.9725 | 0.0000 | 0.9550 |
| L2 | null | -0.0040 | 0.0425 | 0.0400 | 0.0450 |
| L2 | negative | -0.6423 | 0.0000 | 0.9800 | 0.9650 |
| L1 | positive | 0.3959 | 0.8100 | 0.0000 | 0.7775 |
| L1 | null | -0.0079 | 0.0325 | 0.0475 | 0.0400 |
| L1 | negative | -0.3503 | 0.0000 | 0.7425 | 0.6900 |

All alternatives remain close to the nominal 0.05 level under the null. A
directional test has higher power when its direction is scientifically
pre-specified; the two-sided test detects either sign with a modest power cost.

## Interpretation and Recommendation

- `greater` tests whether peripheral/central observations align in the same
  direction across datasets;
- `less` tests whether peripheral observations in one dataset systematically
  correspond to central observations in the other;
- `two-sided` tests either positive or negative salience alignment.

For the current common-standout motivation, `greater` remains the natural
primary analysis and backward-compatible default. The scientific meaning of
negative alignment should be justified before making `less` or `two-sided` a
primary target. Two-sided analysis is nevertheless a coherent extension and a
useful sensitivity analysis.
