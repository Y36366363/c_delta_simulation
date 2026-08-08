# Current Framework and the Node--Dyad Mixture Transition

Date: 2026-08-08

## Current Framework

The project now contains five related but distinct quantities:

| Quantity | Primary target | Current role |
| --- | --- | --- |
| Original L2 `c_delta` | Exact-set concordance of labelled units' overall L2 divergence | Preserve when every member of the observed group is substantively part of the target |
| Huber `c_delta_star` | Robust-reference concordance of labelled-unit salience | Candidate descriptive coefficient for typical or transferable salience structure |
| Pearson Huber-profile correlation | Standardized concordance of the same robust salience profiles | Same permutation evidence as `c_delta_star`; cleaner direct effect scale |
| Cap-6 `c_delta_star` | Salience concordance with bounded final leverage | Pre-specified sensitivity estimand, not a second primary definition |
| Mantel/QAP | Concordance of the complete labelled dyadic distance geometry | Use when the research question concerns all pairwise distances |

Three inference rules are already supported:

1. the corrected unrestricted random-pairing reference of a profile ratio is
   1, but a block-restricted reference need not be 1;
2. Huber `c_delta_star` and Huber-profile Pearson have identical one-sided
   permutation ordering and p-values; and
3. building data require within-building permutations whenever label
   exchangeability is conditional on building.

The two main unresolved definition questions are whether `CV_X CV_Y` belongs
to the intended robust-salience construct and how profile versus dyadic
methods behave when both signal types occur simultaneously.

## Continuous Mixture Design

The mixture study retains four buildings with twelve rooms per building and
scale ratios from 1 to 2.5. Within each building it independently generates:

- a standardized node-salience component with correlated absolute radii but
  pairwise sign rewiring; and
- a standardized dyadic component with correlated signed room values.

For dyadic variance weight (w\in[0,1]), the observed values are

```text
X = sqrt(1-w) Node_X + sqrt(w) Dyad_X,
Y = sqrt(1-w) Node_Y + sqrt(w) Dyad_Y.
```

The square-root coefficients make (w) an approximate within-building
variance share rather than an arbitrary amplitude interpolation. Every test
uses the same 399 within-building permutations. The coarse grid contains 500
datasets at weights `0,.1,...,1`. A `.10-.40` refined grid with spacing `.025`
uses 1,200 datasets per weight and is repeated with an independent seed.

## Coarse Power Shape

| Dyadic weight | Huber profile | Mantel | Huber minus Mantel |
| ---: | ---: | ---: | ---: |
| .0 | .862 | .706 | +.156 |
| .1 | .598 | .500 | +.098 |
| .2 | .382 | .362 | +.020 |
| .3 | .270 | .312 | -.042 |
| .4 | .214 | .294 | -.080 |
| .6 | .260 | .400 | -.140 |
| .8 | .400 | .732 | -.332 |
| 1.0 | .750 | .956 | -.206 |

Power is not monotone. Both procedures enter a broad detection valley in the
middle because neither component remains individually dominant and the two
signed components can partially mask one another. The crossover must
therefore be interpreted as a target-composition boundary in this generator,
not as a universal signal-strength constant.

## Refined Paired Comparison

The two refined runs are combined below, giving 2,400 datasets per weight.
The confidence interval uses the paired rejection difference from the same
datasets and the same permutations.

| Dyadic weight | Huber power | Mantel power | Difference | Paired 95% interval |
| ---: | ---: | ---: | ---: | ---: |
| .150 | .474 | .416 | +.058 | [.043, .073] |
| .175 | .440 | .391 | +.048 | [.033, .063] |
| .200 | .386 | .373 | +.013 | [-.002, .027] |
| .225 | .361 | .368 | -.008 | [-.021, .006] |
| .250 | .327 | .335 | -.008 | [-.022, .006] |
| .275 | .293 | .325 | -.032 | [-.045, -.019] |
| .300 | .290 | .330 | -.040 | [-.053, -.027] |

For Huber `c_delta_star`, the adjacent-grid linear crossover estimate is

```text
w_dyad = 0.216.
```

The first refined run estimated `.213` and the independent replication
estimated `.225`. In both runs the weights whose paired confidence intervals
included zero were exactly `.20-.25`. Thus a more defensible conclusion than
one point estimate is:

- Huber profile has a reproducible advantage through (w=.175);
- neither method has a resolved advantage over (w=.20-.25); and
- Mantel has a reproducible advantage from (w=.275) onward in the refined
  region.

## Original L2 and Cap 6

The combined crossover estimate for original L2 is `.137`, with a zero-
difference interval band of `.10-.175`. Huber therefore retains a node-
salience advantage farther into the mixed region than original L2 in this
model.

Cap 6 and uncapped Huber both cross at `.216` and have effectively identical
power curves. The standardized mixture contains no severe leverage event, so
the cap is mostly inactive. This is consistent with its intended role as a
separate extreme-leverage sensitivity rather than a routine power enhancer.

Huber `c_delta_star` and Huber-profile Pearson again had exactly identical
permutation p-values at every weight and in every dataset. The mixture study
therefore does not resolve the separate `CV_X CV_Y` construct decision.

## Interpretation

The results support a three-region description for the present generator:

1. **node-dominant region (`w <= .175`)**: robust profile inference is more
   efficient;
2. **transition region (`w = .20-.25`)**: the data do not distinguish method
   advantage reliably; and
3. **dyad-dominant region (`w >= .275`)**: Mantel is more efficient.

These are diagnostic regions, not universal cutoffs. Their locations depend
on the node-radius correlation `.55`, dyadic value correlation `.70`, sample
size 48, four balanced buildings, scale heterogeneity, and the chosen
permutation design.

## Next Research Step

The immediate result is sufficiently clear; simply adding more repetitions at
the same settings has low value. The next useful study would vary the node and
dyadic signal strengths as a two-dimensional surface and ask whether the
transition is governed approximately by a signal-to-signal ratio. After that,
one can formalize method selection as estimand-first rather than selecting the
test from observed data, which would otherwise create post-selection error.

Detailed outputs:

- `results/node_dyad_mixture_coarse_20260808.tsv`
- `results/node_dyad_mixture_coarse_comparison_20260808.tsv`
- `results/node_dyad_mixture_refined_20260808.tsv`
- `results/node_dyad_mixture_refined_comparison_20260808.tsv`
- `results/node_dyad_mixture_replication_20260808.tsv`
- `results/node_dyad_mixture_replication_comparison_20260808.tsv`
- `results/node_dyad_mixture_combined_comparison_20260808.tsv`
- `results/node_dyad_mixture_crossover_20260808.tsv`

Implementation:

- `scripts/run_node_dyad_mixture_20260808.py`
- `scripts/summarize_node_dyad_mixture_20260808.py`
