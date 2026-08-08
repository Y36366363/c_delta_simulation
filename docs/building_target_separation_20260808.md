# Building-Style Separation of Salience and Dyadic Targets

Date: 2026-08-08

## Purpose

Professor Hoorn's latest questions imply that the next comparison should not
ask which statistic wins on one generic alternative. It should ask whether
each statistic is most sensitive to the structure it claims to measure. This
focused study therefore compares observation-level salience concordance with
complete dyadic-distance concordance in one common building-style design.

## Design

Each dataset contains four buildings and twelve labelled rooms per building.
The buildings have common scale heterogeneity with ratios from 1 to 2.5. Five
conditions are generated:

1. a conditional null with independent room values given building;
2. shared room salience with pairwise signs rewired between systems;
3. shared dyadic geometry from correlated room values;
4. one matched, structurally meaningful extreme room per building; and
5. deliberately unmatched extremes as a negative control.

The methods are original L2 `c_delta`, uncapped Huber `c_delta_star`, Pearson
correlation of the same Huber profiles, cap-6 `c_delta_star`, and the ordinary
standardized Mantel correlation. Each run uses 800 datasets and 399 common
permutations. A second 800-dataset run uses an independent seed. Alternatives
use within-building label permutations. The conditional null is tested with
both unrestricted and within-building permutations.

## Main Results

The following rates average the two independent 800-dataset runs.

| Condition | Original L2 | Huber `c_delta_star` | Huber Pearson | Cap 6 | Mantel |
| --- | ---: | ---: | ---: | ---: | ---: |
| Conditional null, unrestricted | .222 | .239 | .239 | .239 | .229 |
| Conditional null, within building | .044 | .042 | .042 | .041 | .046 |
| Node salience, signs rewired | .749 | .823 | .823 | .824 | .713 |
| Shared dyadic geometry | .722 | .797 | .797 | .797 | .959 |
| Matched structural extreme | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Unmatched-extreme negative control | .000 | .000 | .000 | .001 | .000 |

In the first run, the node-salience power intervals were `.775-.830` for
Huber `c_delta_star` and `.666-.730` for Mantel. Under shared dyadic geometry,
the corresponding intervals were `.768-.824` and `.941-.969`. The intervals
are separated in opposite directions. The independent run reproduced both
directions (`.843` versus `.728`, then `.796` versus `.960`).

The results do not imply that one method dominates. They support construct
alignment:

- profile methods are more sensitive when labelled rooms preserve atypicality
  but not all pairwise directions;
- Mantel is more sensitive when the complete distance geometry is shared; and
- a very strong matched exceptional room changes both node salience and many
  dyads, so every method detects it.

## Pearson and `c_delta_star`

The Huber `c_delta_star` and Huber-profile Pearson tests had identical
permutation p-values in every dataset under both unrestricted and
within-building permutation. The maximum recorded difference was zero at
floating-point precision. This extends the earlier algebraic result to the
design-respecting building setting.

Their reported effect scales remain different. The mean Huber `c_delta_star`
was about `1.285` under node salience and `1.383` under shared dyadic geometry,
while mean Pearson correlations were `.622` and `.512`. A larger raw
`c_delta_star` is therefore not evidence that its concordance is stronger;
the CV product also contributes.

## Fixed-Correlation CV Experiment

For lognormal positive profiles, the population values satisfy

```text
c_delta_star = 1 + r CV_X CV_Y.
```

Holding population Pearson profile correlation at `.30` produced:

| Sigma X | Sigma Y | CV product | Population `c_delta_star` |
| ---: | ---: | ---: | ---: |
| .25 | .25 | .064 | 1.019 |
| .50 | .50 | .284 | 1.085 |
| 1.00 | 1.00 | 1.718 | 1.515 |
| 1.50 | 1.50 | 8.488 | 3.546 |
| .50 | 1.50 | 1.553 | 1.466 |

Thus two samples with the same population concordance can have radically
different `c_delta_star` values. Under the most heterogeneous symmetric row,
the mean estimate was `2.904` at `n=100` (relative bias `-18.1%`) and `3.422`
at `n=2000` (relative bias `-3.5%`), with sample SD still `1.464`. Low and
moderate CV rows were essentially stable by `n=500`.

The CV term is therefore both a scientific weighting choice and a source of
finite-sample instability under highly heterogeneous profiles. The raw
coefficient should not be compared across groups or studies without also
reporting Pearson concordance and the two marginal CVs.

## Current Recommendation

No main-definition decision should be made from power alone. The evidence
supports the following provisional reporting structure:

1. state whether the scientific target is labelled-unit salience or complete
   dyadic geometry;
2. use within-building permutations whenever exchangeability is conditional
   on building;
3. report Pearson robust-profile correlation as the direct concordance effect;
4. report `c_delta_star` and `CV_X CV_Y` together only if amplification by
   marginal salience heterogeneity is scientifically desired; and
5. retain original L2 for the exact-set question and cap 6 as a separately
   declared leverage-limited sensitivity.

The next definition-level decision for discussion with Professor Hoorn is
whether `CV_X CV_Y` belongs to the intended construct. If it does not, Pearson
robust-profile correlation is the simpler primary concordance parameter. If
it does, cross-sample comparisons require explicit CV reporting and a warning
about slow convergence under high heterogeneity.

## Limitations and Next Checks

- This is a scalar-room model with four balanced buildings; it is not yet a
  real-data validation.
- The alternatives were selected to distinguish targets, so power values are
  diagnostic rather than universal benchmarks.
- The Mantel comparison uses one distance matrix and one predictor. MRQAP is
  still needed for multiple dyadic predictors or building interactions.
- A formal finite-sample proof of within-building permutation validity remains
  desirable even though two independent simulations are calibrated.
- The next simulation should vary the node-versus-dyad mixture continuously
  rather than use only separated endpoint alternatives.

Detailed results:

- `results/building_target_separation_20260808.tsv`
- `results/building_target_separation_replication_20260808.tsv`
- `results/fixed_correlation_cv_weighting_20260808.tsv`

Implementation: `scripts/run_building_target_separation_20260808.py`.
