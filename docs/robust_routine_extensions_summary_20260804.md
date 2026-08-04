# Robust c_delta Routine Extension Pilots

Date: 2026-08-04

## Scope

These pilots screen four questions raised after the stage-2 validation:

1. whether cap 6 should enter formal reporting and how a cap could be selected
   prospectively;
2. whether the definition should be extended to multivariate observations;
3. how large the small-sample diffuse-power loss is;
4. whether the primary and bounded profiles should be combined into one
   decision rule.

The results below narrow the choices but do not freeze a final estimand,
multivariate definition, cap constant, or manuscript decision rule.

## 1. Prospective Cap Calibration

### Training rule

Caps `3, 4, 5, 6, 8` were compared on a training grid with independent random
seed, `n = 40, 80`, 1,500 repetitions, and 499 permutations. A cap was declared
feasible only when:

```text
maximum training null rejection <= .065,
minimum sparse-power retention versus uncapped Huber >= .95.
```

Among feasible caps, the rule selected the cap with the largest mean
unmatched-masking power. These thresholds were written before examining the
independent evaluation run.

| Cap | Maximum null | Minimum sparse retention | Mean t2 power | Mean masking power | Feasible |
|---:|---:|---:|---:|---:|---:|
| 3 | .0580 | .3407 | .5623 | .3667 | No |
| 4 | .0573 | .7787 | .8037 | .5377 | No |
| 5 | .0600 | .9740 | .9040 | .5823 | Yes, selected |
| 6 | .0613 | .9947 | .9210 | .5117 | Yes |
| 8 | .0627 | 1.0000 | .8947 | .2813 | Yes |

The selected cap was `5`, not `6`. This is important evidence against placing
cap 6 into the formal definition merely because it performed well in the
earlier grid.

### Independent evaluation

The selected cap 5 was evaluated with a new seed across `n = 20, 40, 80, 160`,
5,000 repetitions, and 999 permutations.

| `n` | Scenario | Uncapped Huber | Preselected cap 5 |
|---:|---|---:|---:|
| 20 | clean null | .0422 | .0426 |
| 20 | 10% contaminated null | .0468 | .0510 |
| 160 | clean null | .0548 | .0548 |
| 160 | 10% contaminated null | .0522 | .0520 |
| 20 | matched 1%, magnitude 8 | .9356 | .8928 |
| 40 | matched 1%, magnitude 8 | 1.0000 | .9794 |
| 80 | matched 1%, magnitude 8 | .9998 | .9756 |
| 40 | t2 matched | .6648 | .8050 |
| 80 | t2 matched | .7720 | .9828 |
| 40 | unmatched masking | .0250 | .5528 |
| 80 | unmatched masking | .0676 | .6182 |

Cap 5 passed this preliminary independent calibration and strongly improved
masking resistance. It nevertheless reduced small-sample sparse and t2 power.
The selected constant depends on the pre-specified retention constraint and
utility criterion; changing those scientific priorities can legitimately
select cap 6 or 8. The supported conclusion is therefore a calibration
protocol, not a universal constant.

Current wording for a report should be "a prospectively calibrated bounded
sensitivity profile," with the training rule and evaluation split disclosed.

## 2. Multivariate Feasibility

### Candidates

Three profiles were compared for vector observations:

1. original multivariate pairwise L2 divergence;
2. Euclidean aggregation of separately fitted coordinatewise Huber scores;
3. distance from the spatial median divided by the median radial distance.

The coordinatewise construction is easy to implement but depends on the
coordinate axes. The spatial-median radius is translation, orthogonal-rotation,
and global-scale invariant.

### Rotation diagnostic

| Method | Maximum score change after rotation | Profile correlation |
|---|---:|---:|
| Original multivariate L2 | `1.78e-15` | 1.0000 |
| Coordinatewise Huber | .8481 | .9884 |
| Spatial-median radius | `7.35e-12` | 1.0000 |

Coordinatewise Huber should therefore not be the formal multivariate extension
unless coordinate axes have an intrinsic scientific meaning.

### Preliminary simulation

The pilot used dimensions `1, 2, 5, 10`, `n = 40, 80`, 1,500 repetitions, and
499 permutations. Spatial-median null rejection ranged from `.0360` to `.0587`
with mean `.0483`. The low and high rows are compatible with a preliminary
multiple-condition Monte Carlo grid; higher replication is needed before a
strong multivariate calibration claim.

At `n = 80`:

| Dimension | Scenario | Original multivariate L2 | Spatial-median radius |
|---:|---|---:|---:|
| 1 | t3 matched | .964 | .973 |
| 2 | t3 matched | .880 | .900 |
| 5 | t3 matched | .541 | .565 |
| 10 | t3 matched | .225 | .247 |
| 1 | unmatched masking | .263 | .801 |
| 2 | unmatched masking | .223 | .664 |
| 5 | unmatched masking | .181 | .495 |
| 10 | unmatched masking | .126 | .363 |

The decreasing t3 power with dimension reflects a fixed planted radial
magnitude against increasing-dimensional background noise; it is not evidence
that larger dimension intrinsically invalidates the method.

### Recommendation

Do not add multivariate machinery to the current one-dimensional definition
unless vector-valued observations are part of the intended application.
If they are, develop the spatial-median or spatial-Huber radius as a separately
labelled extension and calibrate signal magnitude and robust radial scale by
dimension. Do not use the coordinatewise Huber shortcut as the general default.

## 3. Small-Sample Diffuse Power

The diffuse pilot used independently random signs with shared magnitude
profiles, six sample sizes, three noise levels, 2,500 repetitions, and 499
permutations.

| `n` | Noise | Original L2 | Huber radius | Difference |
|---:|---:|---:|---:|---:|
| 12 | .15 | .456 | .332 | -.124 |
| 20 | .15 | .764 | .603 | -.161 |
| 30 | .15 | .928 | .800 | -.128 |
| 40 | .15 | .969 | .906 | -.063 |
| 60 | .15 | .997 | .978 | -.019 |
| 80 | .15 | 1.000 | .997 | -.003 |
| 20 | .50 | .490 | .429 | -.061 |
| 40 | .50 | .856 | .798 | -.058 |
| 80 | .50 | .991 | .978 | -.013 |

The loss is reproducible rather than a one-seed anomaly. It is material for
roughly `n <= 40` in this constructed family and small by `n = 60-80`. Whether
this is acceptable depends on the intended estimand:

- if small-sample diffuse magnitude alignment is central, the loss must be
  treated as a substantive limitation and old L2 should remain an explicit
  comparator;
- if resistance to centre displacement and unmatched extremes is central, the
  loss is a quantifiable tradeoff rather than automatic grounds for rejection.

The earlier robust L2-floor tests did not recover this loss consistently, so
adding a radial-floor tuning parameter is not currently supported.

## 4. Primary Plus Sensitivity Versus a Single Rule

The pilot compared five rules at `n = 40, 80`, using 4,000 repetitions and 999
common permutations:

```text
primary only:       p_HR < .05
cap-6 only:         p_cap < .05
unadjusted union:   p_HR < .05 or p_cap < .05
Bonferroni union:   p_HR < .025 or p_cap < .025
intersection:       p_HR < .05 and p_cap < .05
```

Across four null rows, rejection-rate ranges were:

| Rule | Minimum | Maximum | Mean |
|---|---:|---:|---:|
| Primary only | .0405 | .0508 | .0476 |
| Cap-6 only | .0405 | .0510 | .0476 |
| Unadjusted union | .0405 | .0595 | .0508 |
| Bonferroni union | .0173 | .0330 | .0272 |
| Intersection | .0405 | .0488 | .0444 |

At `n = 80`, unmatched-masking rejection was `.075` for primary only, `.583`
for cap 6, `.584` for the unadjusted union, `.400` for the Bonferroni union,
and `.075` for the intersection. For t2 matched signal the corresponding rates
were `.785`, `.990`, `.992`, `.976`, and `.783`.

The unadjusted union has no general level-.05 guarantee and showed preliminary
inflation under contaminated null pairing. Bonferroni controls multiplicity but
is conservative under the highly correlated profiles. Intersection largely
discards the masking advantage.

### Working recommendation

Use one primary inferential rule based on uncapped Huber radius. Report the
pre-specified bounded profile as a sensitivity analysis that describes whether
the conclusion survives leverage limitation. Do not define study significance
as the unadjusted union of the two p-values. If a formal dual-test rule is ever
required, its joint null distribution should be calibrated directly rather
than defaulting to either an unadjusted union or a conservative Bonferroni rule.

## Decision Status

The routine tests support the following provisional structure:

```text
primary definition:
    uncapped Huber robust-reference c_delta

secondary sensitivity:
    prospectively calibrated bounded profile

multivariate extension:
    deferred unless vector observations are required;
    spatial, rotation-invariant centre preferred

formal rejection decision:
    based on the primary statistic alone for now
```

Still requiring a substantive discussion are the cap calibration loss
function, the scientific importance of small-sample diffuse alignment, and
whether future applications require a multivariate estimand.
