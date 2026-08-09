# Pure-Path Approximation and External Signal-Strength Validation

## Purpose

The original nine-cell surface suggested that the profile-versus-Mantel
crossover was driven mainly by node strength, but it did not establish a
mechanism and used the same cells for fitting and assessment. This update does
two things:

1. derives population approximations on the pure node and pure dyadic paths;
2. treats a new intermediate node row (`0.65`) and a new lower dyad column
   (`0.30`) as a seven-cell external validation set.

The crossover remains a property of this generator and comparison, not an
observed-data rule for choosing a test.

## Pure dyadic path

Let `(X,Y)` be standard bivariate normal with correlation `rho`, and define

\[
A(\rho)=\sqrt{1-\rho^2}+\rho\arcsin(\rho).
\]

For the absolute profile radii,

\[
E|X|=\sqrt{2/\pi},\qquad
E(|X||Y|)=\frac{2}{\pi}A(\rho),
\]

so the population profile ratio and correlation are

\[
C_D(\rho)=A(\rho),\qquad
\operatorname{Corr}(|X|,|Y|)
=\frac{(2/\pi)A(\rho)-2/\pi}{1-2/\pi}.
\]

If `(X',Y')` is an independent copy, then the standardized differences
`(X-X',Y-Y')` are again bivariate normal with correlation `rho`. Therefore

\[
\operatorname{Corr}(|X-X'|,|Y-Y'|)
=\operatorname{Corr}(|X|,|Y|).
\]

Thus, on the ideal pure dyadic path, the profile correlation and population
Mantel correlation have exactly the same strength curve. Increasing dyadic
correlation can raise both methods' signal without producing an equally large
first-order change in their *difference*.

## Pure node path

Write the paired radii as

\[
R_X=\exp(\sigma U),\qquad
R_Y=\exp\{\sigma(\rho U+\sqrt{1-\rho^2}V)\},
\]

where `U,V` are independent standard normals and `sigma=0.55`. Then

\[
C_N(\rho)=\frac{E(R_XR_Y)}{E(R_X)E(R_Y)}
=\exp(\sigma^2\rho)
\]

and

\[
\operatorname{Corr}(R_X,R_Y)
=\frac{\exp(\sigma^2\rho)-1}{\exp(\sigma^2)-1}.
\]

The generator attaches balanced, randomly rewired signs to these correlated
radii. This preserves the labelled-room radius signal used by the profile,
but it deliberately weakens agreement of complete pairwise distances. The
Mantel expression is not reduced to the same closed form here, so it was
evaluated by a population Monte Carlo approximation.

Each row below uses 20 batches of 50,000 independent dyads (one million total).

| path | rho | analytic profile r | MC Mantel r | profile minus Mantel |
| --- | ---: | ---: | ---: | ---: |
| node | .35 | .3162 | .1066 | .2094 |
| node | .55 | .5124 | .1842 | .3283 |
| node | .65 | .6151 | .2298 | .3863 |
| node | .75 | .7210 | .2761 | .4453 |
| dyad | .30 | .0794 | .0802 | .0019 |
| dyad | .45 | .1806 | .1816 | -.0016 |
| dyad | .65 | .3852 | .3844 | -.0002 |
| dyad | .80 | .5989 | .5993 | -.0008 |

The analytic `C` and profile formulas agreed with Monte Carlo within `.0027`
in every row. The dyadic profile-minus-Mantel differences were all within
`.002`, whereas the node-path gap increased monotonically from `.209` to
`.445`. This gives the population-level reason for expecting node strength to
be the larger crossover direction.

## Seven-cell external validation

The external cells were not used in the original nine-cell fits:

- node `0.65` crossed with dyad `.30,.45,.65,.80`;
- dyad `0.30` crossed with node `.35,.55,.65,.75`.

The coarse search used 250 datasets per point. Local estimates combined two
independent 400-dataset runs per point. The unbracketed `(0.65,0.30)` cell was
extended with two further 400-dataset runs. Because both methods had nearly
equal power at `(0.35,0.30)`, that cell received two additional 800-dataset
boundary checks. All inference used 199 within-building permutations and
paired rejection differences.

| node | dyad | crossover | zero-difference band |
| ---: | ---: | ---: | ---: |
| .35 | .30 | .225 | .075-.250 |
| .55 | .30 | .289 | .250-.350 |
| .65 | .30 | .362 | .275-.400 |
| .65 | .45 | .304 | .275-.350 |
| .65 | .65 | .258 | .250-.275 |
| .65 | .80 | .242 | .225-.250 |
| .75 | .30 | .371 | .375-.450 |

At fixed dyad `.30`, the crossover rose from `.225` to `.371` as node strength
rose from `.35` to `.75`, with evidence of saturation above `.65`. At fixed
node `.65`, it fell from `.362` to `.242` as dyad strength rose from `.30` to
`.80`. Node strength is the larger direction, but lower dyadic strength has a
real and monotone effect in the expanded range.

## Predictive model check

The models fitted only to the original nine cells were evaluated on the seven
new cells. The raw node/dyad ratio generalized better than the original
nine-cell comparison suggested:

| model trained on 9 cells | external crossover RMSE | maximum error |
| --- | ---: | ---: |
| raw ratio | .0247 | .0320 |
| Fisher-z ratio | .0287 | .0408 |
| separate Fisher-z strengths | .0576 | .0972 |

After refitting all 16 cells, the raw-ratio model reached logit-crossover
`R-squared=.803` and LOOCV RMSE `.171`. The separate-strength model improved
these to `.903` and `.136`. Its coefficients were `+.785` for log Fisher-z
node strength and `-.360` for log Fisher-z dyad strength. The node coefficient
is about 2.2 times the dyad coefficient in absolute magnitude, rather than the
equal-and-opposite values required by a strict ratio law.

This revises the nine-cell conclusion. A signal ratio is a useful low-
dimensional approximation and predicted the new cells well, but the more
flexible surface still supports unequal node and dyad contributions.

## Interpretation and limitations

- The population derivation explains the dominant direction: dyadic strength
  is largely common signal for both targets, while node-radius strength is
  preferentially retained by the profile statistic after sign rewiring.
- The mechanism does not imply zero dyad effect in finite mixtures. Component
  mixing, standardization, block scaling, finite room count, and permutation
  power all depart from the ideal pure paths.
- The `(0.35,0.30)` power difference is flat near zero, so its `.225` point
  estimate is less informative than its broad `.075-.250` uncertainty band.
- Crossover regression is a design-stage description. It must not be used to
  inspect a dataset and select whichever test appears more favorable.
- A next theoretical step would approximate local slopes of the two power
  functions under mixtures. It is not necessary for preserving the current
  estimand-first reporting recommendation.

## Reproducible files

- `scripts/run_pure_path_approximation_20260809.py`
- `scripts/run_signal_strength_external_grid_20260809.py`
- `results/pure_path_population_approximation_20260809.tsv`
- `results/signal_strength_external_crossovers_20260809.tsv`
- `results/signal_strength_external_model_validation_20260809.tsv`
- `results/signal_strength_expanded_models_20260809.tsv`
