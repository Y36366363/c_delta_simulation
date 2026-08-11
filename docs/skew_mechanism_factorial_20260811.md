# Audit of Skew Mechanisms in the Mixed-Path Crossover

## Why this audit was needed

The 2026-08-10 skew-path study validated the Huber/MAD transport derivative,
but its two finite-sample generators changed several features simultaneously:

- the probability of a positive node sign;
- node log-radius tail strength;
- the dyadic margin from Gaussian to lognormal.

Consequently, the early crossovers `.131` and `.043` could not be attributed
to marginal skewness alone. This update separates the mechanisms while keeping
node correlation `.55`, dyadic latent correlation `.70`, node log-radius sigma
`.70`, dyadic lognormal sigma `.80`, the building design, and the permutation
scheme fixed.

## Primary 2x2 design

The factorial crosses:

1. balanced node signs (`P(+)=.50`) versus positive-sign prevalence
   (`P(+)=.80`);
2. Gaussian versus standardized lognormal dyadic margins.

The two sign sequences remain independently generated across `X` and `Y`.
Thus changing `P(+)` changes both the marginal distribution and sign-agreement
geometry: independent signs agree with probability `.50` when balanced but
`.68` when `P(+)=.80`.

Analytic marginal skewness confirms that the labels must not be conflated:

| node signs | dyad margin | node skewness | dyad skewness |
| --- | --- | ---: | ---: |
| balanced | Gaussian | .000 | .000 |
| prevalent positive | Gaussian | .072 | .000 |
| balanced | lognormal | .000 | 3.689 |
| prevalent positive | lognormal | .072 | 3.689 |

The positive-sign-prevalence node margin is only mildly skew by its third
standardized moment. Its larger structural change is the altered sign
composition and agreement probability.

## Population derivative study

Two independent seeds used six batches of 250,000 observations in each cell,
or three million observations per cell. Complete-refit errors at
`epsilon=.0005` were below `.00015` in every displayed effect.

| node signs | dyad margin | profile slope | `c_delta_star` slope | Mantel slope |
| --- | --- | ---: | ---: | ---: |
| balanced | Gaussian | -.491 | -.380 | -.186 |
| prevalent positive | Gaussian | -.122 | -.377 | -.072 |
| balanced | lognormal | -.251 | .010 | .021 |
| prevalent positive | lognormal | .051 | -.004 | .095 |

For profile correlation, the factorial contrasts were:

- node sign-prevalence main effect: `+.335`;
- dyadic-lognormal main effect: `+.206`;
- interaction: `-.067`.

For Mantel they were `+.093`, `+.187`, and `-.040`. Dyadic marginal skew
therefore changes both effect slopes in a similar direction. Node sign
prevalence acts more selectively on the profile slope and on the starting
node geometry.

The Huber/MAD theory remains supported. In the balanced Gaussian cell the
MAD and total location components were numerically zero. They became nonzero
when either margin mechanism induced asymmetry, and the complete derivative
continued to agree with complete refitting.

## Finite-sample crossover study

A 250-dataset coarse grid was followed by two independent 600-dataset local
runs in each cell. All tests used 199 within-building permutations and common
weights/permutations within each dataset.

| node signs | dyad margin | combined crossover | zero-difference band |
| --- | --- | ---: | ---: |
| balanced | Gaussian | .280 | .275-.300 |
| balanced | lognormal | .300 | .275-.325 |
| prevalent positive | Gaussian | .014 | .000-.125 |
| prevalent positive | lognormal | .013 | .000-.100 |

The factorial crossover contrasts were:

- node sign-prevalence main effect: `-.277`;
- dyadic-lognormal main effect: `+.009`;
- interaction: `-.021`.

Although the sign-prevalence zero-difference bands are broad near the endpoint,
both independent seeds put their crossover near `.012-.018`, far from the two
balanced-sign cells. The dyadic-lognormal change alone did not move crossover
earlier; its combined point estimate moved from `.280` to `.300`.

## Balanced-sign magnitude-skew control

To distinguish marginal node skewness from sign prevalence, a second control
kept `P(+)=.50` and sign agreement `.50`, but multiplied positive radii by `.80`
and negative radii by `1.00`. Its node marginal skewness was `-.432`, much
larger in absolute value than the `.072` sign-prevalence cell.

| node construction | dyad margin | crossover | zero-difference band | shift from balanced reference |
| --- | --- | ---: | ---: | ---: |
| magnitude skew | Gaussian | .245 | .225-.250 | -.035 |
| magnitude skew | lognormal | .322 | .300-.375 | +.022 |

The lognormal magnitude-control seeds were noisy (`.308` versus a boundary
estimate near `.400`), so the broad uncertainty band is more informative than
the combined point estimate. Even that range remains qualitatively different
from the sign-prevalence cells near zero.

## Corrected interpretation

The evidence does **not** support the general statement “stronger skewness
makes profile-versus-Mantel crossover earlier.” Instead:

1. The mathematical result is robust: under genuinely asymmetric margins,
   Huber-location movement and the MAD indirect path must be included.
2. Dyadic lognormal skew strongly changes individual effect slopes but had
   little crossover main effect in this factorial.
3. The extremely early crossover was driven primarily by positive-sign
   prevalence, which changes node sign geometry as well as the margin.
4. Balanced-sign magnitude skew produced only modest and direction-dependent
   crossover shifts.

The previous labels `moderate_skew` and `strong_skew` remain reproducible
configuration names, but their power results should now be described as
**composite sign-imbalanced/lognormal generators**, not as a monotone skewness
gradient.

## Consequences for the c_delta project

- The Huber/MAD functional and transport derivatives remain valid and useful.
- Generator-specific crossover values should not be generalized by a single
  skewness coefficient.
- Profile Pearson remains the cleaner direct concordance scale; raw
  `c_delta_star` again showed slopes different from profile correlation because
  of its marginal-CV weighting.
- More abstract skew grids are now low priority. A further skew study should
  use an application-matched sign/magnitude mechanism, not an arbitrary third
  moment target.
- The higher-priority unresolved decisions remain the scientific status of the
  `CV_X CV_Y` weighting and formal design-respecting permutation validity.

## Reproducible files

- `scripts/run_skew_mechanism_factorial_20260811.py`
- `tests/test_skew_mechanism_factorial_20260811.py`
- `results/skew_mechanism_population_combined_20260811.tsv`
- `results/skew_mechanism_power_crossovers_20260811.tsv`
- `results/skew_mechanism_factorial_contrasts_20260811.tsv`
- `results/skew_mechanism_marginal_skewness_20260811.tsv`
- `results/skew_mechanism_magnitude_population_20260811.tsv`
- `results/skew_mechanism_magnitude_power_crossovers_20260811.tsv`
- `results/skew_mechanism_magnitude_comparisons_20260811.tsv`
