# Claim-directed validation

Date: 2026-08-23

## Scope

This update tests the three frozen paper claims rather than opening another
simulation branch. All new Monte Carlo cells use 1,000 repetitions and
independent deterministic seeds. Claim 3 reuses the frozen 24-cell bridge
experiment but evaluates it out of family rather than refitting and evaluating
on the same cells.

## Claim 1: pointwise regular iid Wald inference

The theorem-aligned full-influence-function Wald test was independently
repeated under three regular weak-null designs.

| Design | n | Rejection | 95% Wilson interval | SD of z |
|---|---:|---:|---:|---:|
| dependent normal sign-link | 160 | `.052` | `[.040,.068]` | `1.011` |
| dependent normal sign-link | 640 | `.044` | `[.033,.059]` | `.993` |
| independent t5 | 320 | `.075` | `[.060,.093]` | `1.068` |
| independent t5 | 640 | `.059` | `[.046,.075]` | `1.037` |
| independent strong skew | 640 | `.122` | `[.103,.144]` | `1.280` |
| independent strong skew | 2560 | `.082` | `[.067,.101]` | `1.136` |

The regular dependent weak null is well calibrated and the t5 path moves
toward nominal behavior. Strong skew independently reproduces slow
finite-sample convergence. This supports the theorem's **pointwise** claim,
but it also makes a general moderate-sample accuracy claim untenable.

## Claim 2: near-degenerate reference fitting causes distortion

The shared-sign model has independent lognormal radii, so its intended
symmetry reference is zero and the population radius correlation is zero. On
each simulated dataset, two tests were paired:

1. the actual procedure, which re-estimates the median/MAD/Huber reference;
2. a counterfactual test fixing the symmetry reference at zero.

| Radial log-SD | n | Refit rejection | Fixed-centre rejection | Paired difference |
|---:|---:|---:|---:|---:|
| `.10` | 80 | `.777` | `.054` | `.723` (MCSE `.0145`) |
| `.10` | 640 | `.541` | `.050` | `.491` (MCSE `.0171`) |
| `.40` | 80 | `.060` | `.078` | `-.018` (MCSE `.0080`) |
| `.40` | 640 | `.049` | `.055` | `-.006` (MCSE `.0051`) |

This is the cleanest current mechanism evidence for Claim 2. In the severe
path, fixing the reference removes almost all distortion on the same data;
once radial variation recovers, refitting and fixing behave similarly. The
result is constructive and model-specific: it establishes that unstable
reference fitting **can** generate the failure, not that every
near-degenerate law must fail in the same way.

## Claim 3: the conditioning index organizes the transition

For each of the four bridge families, a binomial logit model using only
`log(sqrt(n) sigma_min(J))` was trained on the other three families and used to
predict the six held-out cells. An intercept-only training prediction is the
comparison.

| Held-out family | LOFO MAE | Baseline MAE | MAE improvement |
|---|---:|---:|---:|
| exponential | `.055` | `.145` | `62.1%` |
| half-normal | `.030` | `.166` | `81.8%` |
| scaled beta(1,2) | `.034` | `.154` | `77.8%` |
| uniform | `.040` | `.166` | `75.8%` |
| pooled | `.040` | `.158` | `74.7%` |

Pooled binomial log loss improves by `13.9%`, and the fitted log-index slope is
negative in every fold. Thus the first-order index retains substantial gross
transition information when an entire bridge shape is withheld; its strength
is not only an in-sample R-squared artifact.

The residual limitation remains visible. Held-out MAE ranges from `.030` to
`.055`, with exponential the least accurately predicted family. Therefore the
result strengthens “organizes much of the transition” but does not support
“fully explains the transition,” a universal cutoff, or transport beyond the
tested bridge construction.

## Claim decision after this update

- Claim 1 remains theorem-level only with pointwise and iid qualifiers;
  finite-sample calibration must be shown by regime.
- Claim 2 is now supported by a direct paired mechanism contrast in addition
  to the original rejection curves.
- Claim 3 is strengthened from in-sample association to within-design,
  leave-one-family-out predictive evidence.
- The higher-order family residual remains an explicit limitation rather than
  a new research branch.

Machine-readable outputs are
`results/claim1_wald_validation_20260823.tsv`,
`results/claim2_reference_mechanism_validation_20260823.tsv`, and the two
`results/claim3_conditioning_lofo_*_validation_20260823.tsv` tables.
