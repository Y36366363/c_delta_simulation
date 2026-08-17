# Matched-density bridge-family and MAD-identification validation

## Question

The first bridge pilot suggested that finite-sample recovery is largely
controlled by `n*epsilon^2`, because every Uniform bridge gives marginal
centre density `f(0)=epsilon/2`.  This update asks whether that conclusion
survives changes in the bridge distribution while holding `f(0)` exactly
fixed.

Four positive-radius bridge families were constructed with the same right
density `g(0)=1`:

- `Uniform(0,1)`;
- `Exponential(rate=1)`;
- half-normal with scale `sqrt(2/pi)`;
- `2*Beta(1,2)`.

Consequently every symmetric margin has the same `f(0)=epsilon/2` at a given
bridge probability.  The population profiles remain independent despite the
raw variables sharing a sign.  The pilot used `n=80,320`,
`epsilon=.05,.10,.20`, four families, 150 datasets per cell, 99 permutations,
and 199 bootstrap reference fits.

## Matched-family comparison

| n | epsilon | n*epsilon^2 | rejection range | median bootstrap-spread range | Holm family p |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 80 | .05 | .20 | .500-.567 | 2.83-2.92 | 1.000 |
| 80 | .10 | .80 | .293-.407 | 2.48-2.58 | .548 |
| 80 | .20 | 3.20 | .107-.153 | 1.77-2.00 | 1.000 |
| 320 | .05 | .80 | .233-.380 | 3.38-3.56 | .279 |
| 320 | .10 | 3.20 | .060-.147 | 2.22-2.75 | .482 |
| 320 | .20 | 12.80 | .027-.053 | .70-.80 | 1.000 |

The main recovery ordering is common to all four families.  A logit model
using only `log(n*epsilon^2)` reached R-squared `.931`.  Family intercepts
increased this to `.949`, and family-specific slopes to `.956`.  Thus centre
identification strength explains most, but not all, of the between-cell
variation.

The largest pilot family difference occurred at `n=320, epsilon=.05`.  A new
500-dataset confirmation at that single preselected cell gave:

| bridge family | rejection | median scaled location spread |
| --- | ---: | ---: |
| exponential | .232 | 3.52 |
| half-normal | .310 | 3.56 |
| scaled Beta(1,2) | .356 | 3.52 |
| uniform | .334 | 3.46 |

The family homogeneity test was `p=.00013`, with Cramer's V `.101`.  The
effect is therefore reproducible but modest.  Importantly, it appears despite
nearly identical centre densities and bootstrap-location spreads.  Neither
`f(0)` nor location stability alone fully specifies finite-sample behavior in
the transition region.

## Comparison of the three earlier diagnostics

Across the 24 matched-family pilot cells, Spearman correlations with rejection
were:

| risk-oriented diagnostic | Spearman correlation | p-value |
| --- | ---: | ---: |
| median continuous spacing/IQR | .880 | `1.4e-8` |
| spacing warning rate | .821 | `9.1e-7` |
| bootstrap warning rate | .788 | `4.7e-6` |
| median scaled bootstrap location spread | .749 | `2.6e-5` |
| low central valley density | .108 | .616 |

Spacing gives the best *cell-level ordering* in this matched experiment, but
this does not rescue its fixed `.50` gate.  In the earlier bridge path it
stopped warning before Type-I error recovered, and within a cell it does not
certify a passing sample.  Central KDE density cannot rank cells whose true
`f(0)` is deliberately matched, confirming that it is an assumption
descriptor rather than an operational validity score.

## Reintroducing the MAD nuisance

The fitted Huber profile uses a fixed scale

\[
s=1.4826\operatorname{median}|X-\operatorname{median}(X)|.
\]

A separate 300-dataset nuisance audit at `n=320, epsilon=.05` bootstrapped both
the Huber location and this MAD scale.  Within every family, the strongest
dataset-level association with rejection was a **small full-sample
`s/IQR` ratio**: risk-oriented Spearman correlations were `.726-.777`.
Location-spread correlations were only `.008-.223`.

Bootstrap log-MAD spread had correlations `-.625` to `-.664`, in the opposite
direction from a simple instability interpretation.  Samples near a scale-
selection boundary can have highly variable bootstrap scales without being
the samples with the largest observed profile distortion.  Bootstrap scale
spread should therefore not be added mechanically to the location spread.

The cheap quantity

\[
R_s=\min\left\{\frac{s_X}{IQR_X},\frac{s_Y}{IQR_Y}\right\}
\]

directly detects collapse of the MAD toward a within-mode scale.  A 2,000-
dataset cross-validation produced:

| scenario | n | median R_s | rate R_s < .40 |
| --- | ---: | ---: | ---: |
| independent `t_5` | 80 / 320 | .735 / .737 | 0 / 0 |
| affine near-constant | 80 / 320 | .734 / .737 | 0 / 0 |
| regular-behaving `t_5` sign link | 80 / 320 | .739 / .747 | 0 / 0 |
| strong skew | 80 / 320 | .550 / .570 | .028 / 0 |
| severe radial `.10` | 80 / 320 | .202 / .258 | .909 / .961 |
| regular radial `.40` | 80 / 320 | .736 / .782 | .014 / 0 |
| bridge `.20` | 80 / 320 | .481 / .655 | .380 / .049 |

The `.40` boundary is a promising descriptive collapse warning, with much
lower small-skew cost than a `.50` boundary.  It is not a gate: the threshold
was not designed to deliver conditional Type-I error, and the preceding
bootstrap analysis shows why sample selection cannot automatically validate
the retained p-values.

## Updated judgement

1. `n*f(0)^2` captures the primary identification scale, but higher-order
   bridge shape has a small reproducible effect in the transition region.
2. Continuous spacing is useful for ordering simulation cells, not for a
   universal sample-level decision.
3. Central KDE density remains a conservative theorem-assumption diagnostic.
4. Bootstrap Huber-location spread remains a useful broad instability flag,
   but omits MAD collapse and cannot certify individual p-values.
5. The full-sample `MAD-scale/IQR` ratio is the most useful new complement: it
   is affine invariant, computationally cheap, closely tied to the actual
   nuisance fit, and externally stable in this grid.
6. No diagnostic is promoted to a formal screening rule.  The next theoretical
   calculation should evaluate the complete nuisance Jacobian—centre density,
   MAD endpoint densities, and Huber score curvature—across the four matched
   families.  This can explain the residual family effect without changing the
   statistic.

## Reproducible artifacts

- `scripts/run_profile_bridge_family_validation_20260817.py`
- `scripts/summarize_profile_bridge_family_validation_20260817.py`
- `scripts/run_profile_bridge_family_nuisance_20260817.py`
- `scripts/run_mad_ratio_crossvalidation_20260817.py`
- `results/profile_bridge_family_validation_pilot_20260817.tsv`
- `results/profile_bridge_family_validation_confirmatory_20260817.tsv`
- `results/profile_bridge_family_confirmatory_contrast_20260817.tsv`
- `results/profile_bridge_family_nuisance_confirmatory_20260817.tsv`
- `results/mad_ratio_crossvalidation_20260817.tsv`

