# Unequal Buildings, Covariates, and Adaptive Omnibus Validation

Date: 2026-08-13

## Decision Boundary

This is a pre-decision validation. It does not promote an adaptive omnibus to
the primary method and does not change the definition of `c_delta_star`. The
work asks whether the current adaptive rule has earned that discussion and
which alternative omnibus, if any, deserves a later definition-level choice.

## Design

The total number of rooms is fixed at 72 while the six-building allocation is
changed:

| Design | Room counts | Size CV |
| --- | --- | ---: |
| Balanced | 12, 12, 12, 12, 12, 12 | 0 |
| Moderately unequal | 6, 8, 10, 12, 16, 20 | .397 |
| Severely unequal | 5, 5, 6, 8, 16, 32 | .809 |

The application-style portfolio contains fixed building covariates resembling
log floor area, age, centrality, and retrofit status. They affect building
centres, heteroscedastic scale, marginal sign prevalence, and local radial or
dyadic signal. The covariates and room counts are design information and are
held fixed by within-building permutations.

Five scenarios were used:

1. a conditional null with covariate-driven centres and scales;
2. a size-only radial control with identical building distributions;
3. covariate-linked radial node signal;
4. covariate-linked dyadic signal; and
5. a mixed covariate-dependent node/dyad signal.

Each design-scenario cell has two independent 300-dataset runs and 199 common
within-building permutations. A separate restriction check has two 800-
dataset seeds. Temperatures `0, .1, .25, .5, 1, 2, 4, 8, 16` and three
building aggregation targets were compared:

- equal weight per building;
- weight proportional to `sqrt(n_b)`; and
- weight proportional to `n_b`, corresponding to equal room weight.

These are different estimands under unequal sizes, not interchangeable
computational choices.

## Size Imbalance Alone

When centre, scale, prevalence, and signal strength were identical across
buildings, changing only room allocation did not cause systematic failure:

| Method | Balanced | Moderate | Severe |
| --- | ---: | ---: | ---: |
| Profile | .670 | .722 | .688 |
| Mantel | .642 | .675 | .665 |
| Standardized max | .660 | .700 | .685 |

Thus unequal building size alone is not the explanation for the larger power
changes in the application model. Those changes arise because building size
co-varies with floor area and other signal/nuisance characteristics. This is
the realistic difficulty: informative cluster size, not merely unequal
cluster size.

## Application Covariates

In the mixed scenario, the generated portfolio had centre correlations near
`.89`, scale ratios about `1.80-2.58`, and increasing room-weighted positive
prevalence (`.500`, `.540`, `.566`) as the size allocation became more
unequal. The same size distributions also changed the room-weighted radial and
dyadic signal because large buildings contributed more observations.

At equal building aggregation and temperature zero where relevant, average
power over the three size designs was:

| Scenario | Profile | Mantel | Nested max | Standardized max | Raw CV | Standardized CV |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Size-only radial | .693 | .661 | .694 | .682 | .530 | .576 |
| Covariate radial | .395 | .363 | .396 | .387 | .305 | .402 |
| Dyadic | .147 | .241 | .156 | .218 | .128 | .132 |
| Covariate mixed | .374 | .408 | .376 | .400 | .286 | .357 |

No method dominates each scientifically distinct alternative. The
standardized maximum is close to the better fixed test across alternatives,
whereas learned mixtures lose substantial dyadic power.

## Why the Original Adaptive Weight Failed

The original LOO learner compares the raw within-building profile and Mantel
correlations. Although both lie on `[-1,1]`, their blockwise null variability
differs and Mantel dyads are internally dependent. At temperature 4 the learner
assigned a mean profile weight near `.53` under radial-node signal but `.55`
under dyadic signal: the direction was opposite to the intended scientific
interpretation. Severe imbalance amplified sensitivity to whether buildings
or rooms were the aggregation target.

An orbit-standardized version centres and scales every block-method score by
its permitted permutation distribution before learning. This is a fairer
evidence scale and is finite-sample rank-valid when the full orbit is used; all
`3!^2=36` permutations passed the exact small-orbit check. Nevertheless, its
weights still ran in the wrong scientific direction (`~.45` profile weight
under radial versus `~.57` under dyadic at temperature 4). Local block scores
are therefore not reliable learners of which global statistic is better.

## Temperature Sensitivity

For orbit-standardized CV, mean alternative power over designs decreased as
temperature increased:

| Aggregation | T=0 | .1 | .25 | .5 | 1 | 2 | 4 | 8 | 16 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Building equal | .298 | .297 | .298 | .291 | .284 | .256 | .233 | .219 | .213 |
| sqrt rooms | .329 | .329 | .330 | .325 | .320 | .293 | .267 | .254 | .247 |
| Room equal | .335 | .334 | .335 | .331 | .323 | .300 | .278 | .263 | .259 |

Temperature zero is exactly a fixed 50/50 mixture, not adaptive learning. The
flat optimum at `0-.25` and subsequent decline show that the data do not
support aggressive building-level method learning. Choosing a higher
temperature for interpretive adaptivity would pay a reproducible power cost.

## Null Calibration and Permutation Restriction

Across the full grid, conditional-null rejection ranges were approximately
`.030-.063`. The largest cells had Wilson intervals containing `.05`; there
was no resolved inflation after two 300-dataset seeds, although some methods
were conservative. In the higher-replication severe-imbalance restriction
check:

| Method | Unrestricted | Within building |
| --- | ---: | ---: |
| Profile | .143 | .044 |
| Mantel | .314 | .045 |
| Nested max | .160 | .044 |
| Standardized max | .299 | .044 |
| Raw CV | .001 | .043 |
| Standardized CV | .018 | .046 |

The unrestricted reference can be liberal or extremely conservative,
depending on the statistic, because it destroys the covariate- and building-
conditioned orbit. Within-building permutation calibrated every method. This
supports the previous theorem and shows that covariates do not need to be put
into a regression merely to obtain validity when they are building-constant;
they define the conditioning blocks. Room-level covariates would require finer
strata, residual randomization, or a model-based scheme.

## Standardized Maximum

For each method `j`, define a permutation-standardized evidence score

```text
Z_j = (T_j - mean_G(T_j)) / sd_G(T_j),
T_omnibus = max_j Z_j.
```

The same centring, scaling, and maximum are recomputed symmetrically on the
permutation orbit. The standardized maximum averaged `.422` power over the
four alternatives, versus `.402` for profile, `.418` for Mantel, `.405` for
raw nested max, `.312` for raw CV, and `.367` for standardized CV. These
averages are descriptive and depend on the chosen scenario mix. More
importantly, standardized max remained close to the stronger fixed method in
each alternative and avoided the learned-weight direction failure.

It is an omnibus test, not a new `c_delta` coefficient. It provides no single
population effect size and does not answer whether radial salience or dyadic
geometry generated the rejection. Component statistics and adjusted evidence
must therefore be reported with it.

## Decision Assessment

### Learned adaptive mixture

It does **not** meet the threshold for a primary method:

- learned weights have the wrong construct direction;
- temperature zero or nearly zero is best;
- results depend on the chosen building-versus-room aggregation target; and
- dyadic power is substantially below Mantel.

Further tuning would risk optimizing to the current simulation family rather
than resolving the estimand problem.

### Permutation-standardized maximum

It has earned a definition-level discussion as an omnibus candidate because
it is design-respecting, null-calibrated, and robust across the tested
alternative types. It has **not** yet earned automatic promotion to primary
method because:

1. it is a decision rule rather than a unified effect parameter;
2. the profile/Mantel family must be declared prospectively;
3. multiplicity grows if future components are added; and
4. real or externally calibrated application scenarios are still absent.

The present recommendation is therefore to retain robust profile
`c_delta_star` as the labelled-salience estimand, Mantel as the dyadic estimand,
and standardized max as a promising predeclared omnibus sensitivity test.
Promoting it to the main inferential rule requires an explicit scientific
decision about whether the primary question is “any supported internal-
structure concordance” rather than a particular estimand.

## Files

- `scripts/run_unequal_building_adaptive_validation_20260813.py`
- `scripts/summarize_unequal_building_adaptive_20260813.py`
- `results/unequal_building_adaptive_combined_20260813.tsv`
- `results/unequal_building_adaptive_decision_20260813.tsv`
- `results/unequal_building_restriction_combined_20260813.tsv`
