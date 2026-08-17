# Independent boundary and central-bridge calibration

## Aim and design

This update independently checks the diagnostic conclusions from August 16.
It does not alter the robust profile definition or promote a warning to a
formal gate.

The first design refines the shared-sign true profile weak-null path over
radial log-SD `.10,.12,.14,.16,.18,.20,.25,.30` at `n=80,320`.  The second
design fixes log-SD `.10` and replaces an independent fraction `epsilon` of
each margin's radii by `Uniform(0,1)` bridge radii.  The raw margins remain
dependent through a common sign, while the two radii and hence the population
profiles are independent.  For `epsilon>0`, the symmetric marginal density at
zero is positive:

\[
f_X(0)=f_Y(0)=\frac{\epsilon}{2}.
\]

Every cell uses 150 independently generated datasets, 99 fully recomputed
studentized permutations, and 199 bootstrap fits of each Huber reference.
Four external null scenarios at both sample sizes provide an independent
false-warning check.

## Refined radial boundary

| radial log-SD | rejection n=80 | median B_n n=80 | rejection n=320 | median B_n n=320 |
| ---: | ---: | ---: | ---: | ---: |
| .10 | .847 | 3.14 | .753 | 4.38 |
| .12 | .647 | 2.81 | .420 | 3.50 |
| .14 | .453 | 2.51 | .293 | 2.60 |
| .16 | .360 | 2.12 | .080 | 1.93 |
| .18 | .247 | 2.00 | .073 | 1.19 |
| .20 | .227 | 1.76 | .020 | .92 |
| .25 | .080 | 1.36 | .020 | .82 |
| .30 | .053 | .98 | .033 | .81 |

Here `B_n` is the root-n scaled bootstrap IQR of the fitted Huber centre,
divided by the data IQR.  The independent seed reproduces the previous broad
conclusion: tight radial mixtures remain severely anti-conservative, while
greater within-sign radial heterogeneity stabilises the reference.  The
finite-sample transition is gradual and sample-size dependent; it is not a
universal log-SD cutoff.

## Positive-density bridge

| epsilon | rejection n=80 | B_n n=80 | rejection n=320 | B_n n=320 |
| ---: | ---: | ---: | ---: | ---: |
| 0 | .773 | 3.15 | .607 | 4.64 |
| .01 | .693 | 3.30 | .613 | 4.31 |
| .025 | .647 | 3.11 | .413 | 3.92 |
| .05 | .487 | 2.93 | .313 | 3.45 |
| .10 | .273 | 2.47 | .147 | 2.61 |
| .20 | .173 | 1.75 | .033 | .71 |

Merely making `f(0)` positive does not deliver useful finite-sample
regularity.  Small bridge probabilities satisfy a pointwise asymptotic
condition but leave the empirical median/MAD vulnerable to mode selection.
At `n=320`, `epsilon=.20` finally restores nominal rejection, whereas
`epsilon=.05` still rejects `.313`.

The usual median expansion has standard-error scale

\[
\frac{1}{2f(0)\sqrt n}=\frac{1}{\epsilon\sqrt n},
\]

suggesting recovery should depend approximately on `n*epsilon^2`.  Matched
cells support this mechanism:

| n*epsilon^2 | rejection at n=80 | matched rejection at n=320 | absolute difference |
| ---: | ---: | ---: | ---: |
| .20 | .487 (`epsilon=.05`) | .413 (`epsilon=.025`) | .073 |
| .80 | .273 (`epsilon=.10`) | .313 (`epsilon=.05`) | .040 |
| 3.20 | .173 (`epsilon=.20`) | .147 (`epsilon=.10`) | .027 |

On the empirical-logit scale, a model based on `log(n*epsilon)` had
R-squared `.895`, versus `.919` for `log(n*epsilon^2)`.  Allowing the exponent
to be freely estimated gave `1.55` and R-squared `.926`.  Thus the theoretical
square scaling is directionally supported but not numerically established;
only two sample sizes and one bridge family were tested.

## Diagnostic comparison

### Spacing

Spacing responds quickly when bridge observations physically break the empty
interval, but that can occur before the Huber/MAD reference is stable.  At
`n=320, epsilon=.05`, its warning rate was only `.0067` although Type-I
rejection remained `.313`.  It is a gross gap diagnostic, not an estimator-
identification diagnostic.

### Central valley density

Central density correctly remains small when the bridge density is positive
but weak.  It warned in `.993` of the `n=320, epsilon=.20` samples even though
rejection was `.033`.  It therefore describes a conservative regularity
condition rather than the current test's finite-sample error.

### Bootstrap reference spread

The scaled bootstrap spread follows the recovery transition most closely.  In
the eight independent external-null cells, its median was `1.04-1.35`, every
90th percentile was below `1.54`, and the exploratory `B_n>2` warning rate was
zero.  The same warning occurred in `.69/.93` of the severe `.10` path at
`n=80/320` and declined as radial or bridge variation restored stability.

However, `B_n>2` is **not a valid screening gate**.  Conditional rejection
among the samples that passed remained `.537` at `n=80, sigma=.16`, and `.600`
at `n=320, epsilon=.05`; in still more severe rows, rare passing samples could
all reject.  The warning identifies instability at the population-of-samples
level but does not create a conditionally calibrated local test.

## Current judgement

1. The independent grid confirms that nonregular reference fitting, rather
   than raw scale, is the failure source.
2. A pointwise assumption `f(0)>0` is too weak for finite samples.  A useful
   theorem/reporting condition should quantify identification strength, for
   example a lower bound on `sqrt(n)*f(0)` relative to the profile scale.
3. Root-n bootstrap spread remains the most informative operational
   diagnostic, but its threshold must not be used to claim conditional Type-I
   validity.
4. Spacing and central density should remain descriptive assumption checks;
   neither should independently suppress or approve inference.
5. The next non-decisional validation should change the bridge distribution
   while holding `f(0)` and `n*f(0)^2` approximately fixed.  Only after that
   should the project decide whether a quantitative identification condition
   belongs in the formal theorem or only in reporting guidance.

## Reproducible artifacts

- `scripts/run_profile_bridge_calibration_20260817.py`
- `scripts/summarize_profile_bridge_calibration_20260817.py`
- `results/profile_sigma_calibration_pilot_20260817.tsv`
- `results/profile_bridge_calibration_pilot_20260817.tsv`
- `results/profile_external_calibration_pilot_20260817.tsv`
- `results/profile_bridge_collapse_models_20260817.tsv`
- `results/profile_bridge_matched_kappa_20260817.tsv`

