# Stress validation and refinement of the three claims

Date: 2026-08-24

## Scope

This update tests failure modes of the three existing claims. It does not add
a fourth claim or change the primary estimand. Claim 1 and Claim 2 use 800
fixed-seed repetitions per cell. Claim 3 reuses the frozen 24 bridge cells and
applies stricter out-of-sample splits.

## Claim 1: what remains wrong under strong skew?

The audit compares the empirical sampling SD of the estimator with the root
mean squared reported sandwich SE. It also examines the two tails of the
studentized statistic.

| Model | n | SE / empirical SD | z SD | z 2.5% | z 97.5% | Rejection |
|---|---:|---:|---:|---:|---:|---:|
| dependent normal weak null | 160 | `1.007` | `1.020` | `-1.962` | `1.975` | `.055` |
| dependent normal weak null | 640 | `1.014` | `.996` | `-1.960` | `1.984` | `.051` |
| independent t5 | 320 | `.929` | `1.123` | `-2.443` | `1.815` | `.086` |
| independent t5 | 640 | `1.000` | `1.021` | `-2.075` | `1.974` | `.059` |
| independent strong skew | 640 | `.956` | `1.267` | `-3.279` | `1.726` | `.108` |
| independent strong skew | 2560 | `.980` | `1.138` | `-2.741` | `1.705` | `.083` |

The regular normal model behaves as predicted, and t5 largely recovers by
`n=640`. Under strong skew, the average reported scale is already close to the
empirical estimator SD, especially by `n=2560`, but the studentized law remains
left-heavy and asymmetric. Therefore the remaining distortion is not well
described as a single constant variance-underestimation problem. Dataset-level
dependence between the estimate and its estimated scale, skewed higher-order
terms, and tail behavior are more plausible targets. A uniform scalar HC
inflation is unlikely to address this pattern completely.

This refines Claim 1 without weakening its pointwise theorem: regular IID
asymptotics work in the regular examples, but the approach to the limit is
distribution-specific and can be strongly asymmetric.

## Claim 2: sign imbalance as the switching trigger

The severe separated-mode model with radial log-SD `.10` was repeated under
two sign designs. The IID design samples shared signs independently. The
intervention fixes exactly half positive and half negative signs, then
randomizes their positions. Radii remain independently generated in both
margins.

| n | Sign design | Mean max absolute Huber centre | Rejection |
|---:|---|---:|---:|
| 80 | IID signs | `.491` | `.766` |
| 80 | exactly balanced | `.013` | `.058` |
| 640 | IID signs | `.239` | `.535` |
| 640 | exactly balanced | `.005` | `.060` |

Exact sign balance nearly removes both reference displacement and rejection
distortion. Within the IID samples, rank-quartiles of absolute sign imbalance
also show a steep monotone rejection gradient. At `n=640`, rejection rises
from `.005` in the lowest imbalance quartile to `.205`, `.930`, and `1.000`.
The corresponding mean maximum absolute Huber centres rise from `.033` to
`.173`, `.304`, and `.444`.

This identifies a concrete finite-sample pathway:

1. the centre-density gap makes the reference weakly or non-uniquely
   identified;
2. ordinary binomial sign-count noise selects a side of the gap;
3. the fitted Huber centres move together because the margins share signs;
4. the resulting fitted radius profiles acquire artificial concordance.

The exactly balanced design is a mechanism intervention, not an IID sampling
law and not a proposed inferential correction. The imbalance quartiles are
post-simulation descriptive strata, not pre-specified diagnostic cutoffs.

## Claim 3: stricter transport tests for the conditioning index

The logit predictor based only on

\[
I_n=\sqrt n\,\sigma_{\min}(J)
\]

was tested under two more demanding schemes.

| Validation scheme | MAE | Baseline MAE | MAE gain | Log-loss gain |
|---|---:|---:|---:|---:|
| train at one n, predict the other n | `.045` | `.201` | `77.6%` | `23.7%` |
| leave one `(n, epsilon)` level out | `.052` | `.186` | `72.2%` | `18.0%` |

Every training slope remains negative. The index therefore preserves the
gross ordering of the transition when sample size is withheld and when all
four families at one conditioning level are withheld. This is stronger than
the earlier leave-one-family-out result.

The evidence remains internal to the bridge construction and does not erase
family residuals. It supports the wording that the conditioning index
``organizes much of the transition at first order,'' not a universal cutoff or
a complete transport theorem.

## Updated boundaries

- Claim 1 remains a pointwise IID theorem plus distribution-specific
  finite-sample evidence. Strong-skew distortion is asymmetric and higher
  order, not merely a constant SE bias.
- Claim 2 now has a more specific demonstrated mechanism: reference switching
  is triggered by ordinary sign-count imbalance in a centre-gap model.
- Claim 3 now has leave-family-out, cross-sample-size, and
  leave-conditioning-level-out evidence.
- Higher-order family effects and external transport remain the explicit
  limitations.
