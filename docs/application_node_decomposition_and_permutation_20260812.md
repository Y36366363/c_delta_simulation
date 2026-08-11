# Application-Oriented Node Decomposition and Adaptive Permutation Validity

Date: 2026-08-12

## Questions

This study addresses four linked questions left by the skew-mechanism audit:

1. can the synthetic building model separate interpretable node mechanisms;
2. which mechanisms are actually node-profile signals rather than dyadic or
   nuisance structure;
3. what a data-driven profile/Mantel weight can legitimately mean; and
4. when within-building permutation remains finite-sample valid after method
   selection or weight fitting.

No definition of `c_delta_star` is changed here. The exercise concerns the
data-generating model and the inferential wrapper.

## Application-Oriented Generator

There are six buildings and ten labelled rooms per building. Building scales
vary geometrically from one to two. For room `i` in building `b`, the within-
building node component has the schematic form

```text
X_bi = mu_Xb + scale_b S_Xbi exp(sigma R_Xbi) / exp(sigma^2) + dyadic part,
Y_bi = mu_Yb + scale_b S_Ybi exp(sigma R_Ybi) / exp(sigma^2) + dyadic part.
```

The controls are deliberately distinct:

- `positive_probability = P(S_X=+1) = P(S_Y=+1)` controls the two marginal
  sign prevalences through a joint Bernoulli law;
- `sign_agreement = P(S_Y = S_X)` controls directional agreement;
- `magnitude_sigma` controls radial heterogeneity, while `magnitude_rho`
  controls whether the heterogeneous radii agree between margins;
- `center_sd` controls between-building centre displacement, and `center_rho`
  controls whether those block centres covary between margins; and
- `dyadic_weight` and `dyadic_rho` add a separately declared correlated-value
  component.

The normalization by `exp(sigma^2)` holds the second moment of the signed
lognormal node component fixed. Increasing `sigma` therefore changes radial
heterogeneity rather than merely increasing variance.

## Initial 2 x 2 x 2 x 2 Decomposition

The grid used positive-sign probability `.50/.70`, sign agreement `.50/.75`,
radial sigma `.35/.85`, and centre SD `0/1`, with magnitude correlation `.55`,
dyadic variance weight `.15`, and dyadic correlation `.50`. The joint sign law
holds both marginal positive probabilities fixed while varying agreement, so
prevalence and pairing are no longer confounded. Each cell used two independent
400-dataset runs and 199 within-building permutations.

Average power main effects, averaging the other two factors, were:

| Method | Positive prevalence | Sign agreement | Magnitude heterogeneity | Centre displacement |
| --- | ---: | ---: | ---: | ---: |
| Huber profile | -.090 | +.381 | +.157 | -.090 |
| Mantel | -.096 | +.524 | +.103 | -.057 |
| Nested maximum | -.091 | +.395 | +.152 | -.080 |
| Retrained LOO weight | -.113 | +.470 | +.174 | -.059 |

These effects are descriptive factorial contrasts, not structural causal
parameters. Nevertheless, their direction corrects an important naming
problem. Agreement of signed deviations preserves directional and pairwise
geometry, so it helps Mantel more than the unsigned Huber-radius profile.
Shared radial heterogeneity is the cleaner node-salience mechanism and helps
the profile relatively more. `Sign consistency` should therefore not be used
as a synonym for node salience.

Moving the common marginal positive probability from `.50` to `.70` reduced
power by about `.09-.11` for every method, after averaging the other factors.
Both seeds reproduced the direction. This prevalence parameter changes the
available negative-cell mass and robust-centre geometry even when pairwise
agreement is held fixed; it is therefore a distribution-shape/nuisance axis,
not a substitute for directional agreement.

Correlated building-centre displacement is held fixed by within-building
permutation. It is a stratification-level nuisance, not a within-building
node signal. It can reduce power by increasing marginal heterogeneity, but it
does not become evidence merely because the two margins have correlated
building centres. A global additive shift would disappear entirely because
the Huber profile and distance matrix are translation invariant.

## Data-Driven Weight Pilot

For each held-out building, the pilot computes profile and Mantel association
scores in the other buildings. Their difference is mapped to a continuous
profile weight by

```text
a_b = logistic(4 * (mean profile training score - mean Mantel training score)).
```

The held-out score is `a_b profile_b + (1-a_b) Mantel_b`, averaged over
buildings. The temperature `4` is predeclared in this pilot. It is not yet
calibrated as an optimal choice.

The resulting weight has a limited interpretation: it is an empirical
preference of this prediction/association rule for one score, not an estimate
of the latent node variance share, dyadic variance share, or the earlier
mixture parameter. Cross-validation reduces same-building reuse; it does not
turn a method-selection coefficient into a scientific construct parameter.

The retrained rule had the highest average power in this deliberately mixed
grid (`.579`, versus `.520` profile and `.576` Mantel), but this is not enough
to promote it to the new primary definition. Its temperature, block count,
and alternative family were used in its construction. A predeclared primary
estimand plus an adaptively calibrated omnibus sensitivity test remains the
safer reporting structure.

## Conditional-Null Stress Test

Four conditional-null designs were used: correlated building centres, high
radial heterogeneity, only three buildings, and a dyad-dominant independent
within-building mixture. Each design has 2,000 datasets across two seeds and
199 permutations.

| Null design | Profile | Mantel | Naive selection | Nested max | Frozen CV | Retrained CV |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Correlated centres | .039 | .046 | .046 | .038 | .039 | .044 |
| High heterogeneity | .042 | .044 | .043 | .042 | .044 | .045 |
| Three buildings | .051 | .045 | .056 | .049 | .040 | .043 |
| Dyad-dominant null | .045 | .042 | .046 | .045 | .046 | .045 |

There is no inflation signal for nested-max or retrained CV in these checks.
Some rows are mildly conservative. Naive selection reached `.056` with three
buildings; its Wilson interval still includes `.05`, so this is a warning, not
a demonstrated failure. Frozen CV also happened to calibrate in these four
designs, but simulation calibration in selected models cannot replace its
missing general permutation guarantee.

## Finite-Sample Within-Building Theorem

Let the observed data be `D=(X,Y,Z)`, where `Z` contains fixed building labels
and any variables on which exchangeability is conditioned. Let

```text
G = product_b S_(n_b)
```

be the direct product of all permutations within each building. Assume the
conditional null

```text
(X, Y, Z) has the same conditional law as (X, gY, Z)
for every g in G, conditional on the G-invariant information.
```

Equivalently, within each building the labels attached to the `Y` values are
exchangeable under the null. Buildings may have different locations, scales,
sizes, and centre offsets; these are conditioned on rather than permuted.

For any measurable statistic `T(D)`, define its full-orbit p-value by

```text
p(D) = |G|^(-1) sum_g 1{T(X,gY,Z) >= T(X,Y,Z)}.
```

Then, conditional on the orbit, `p(D)` is super-uniform:

```text
P(p <= alpha | orbit) <= alpha.
```

The proof is the ordinary orbit-rank argument: under the null the observed
labelling is uniform over its orbit, so the rank of its statistic among the
orbit values is uniform when there are no ties and conservative with ties.
The statistic may contain Huber/MAD fitting, Mantel distances, weight
selection, cross-validation, or other deterministic calculations. What
matters is that the same complete map `T` is applied to every orbit member.

For Monte Carlo permutations `g_1,...,g_M`, the plus-one value

```text
(1 + sum_m 1{T(X,g_m Y,Z) >= T(D)}) / (M+1)
```

is the appropriate conservative implementation. The current code was also
checked by exhaustive enumeration of all `3!^2=36` within-building
permutations in a two-building example; the complete retrained-CV orbit obeyed
the exact rank bound at alpha `.05`, `.10`, and `.20`.

## Consequences for Weight Learning

If `A(D)` learns a weight, the valid adaptive statistic is

```text
T(D) = T_(A(D))(D),
```

and each reference value must be

```text
T_(A(gD))(gD).
```

Learning `A(D_observed)` once and comparing
`T_(A(D_observed))(gD)` across permutations is not generally the same orbit
map. It is justified only when at least one of the following holds:

1. the weight is pre-specified;
2. the weight learner is invariant to every allowed within-building
   permutation;
3. the weight is trained on genuinely independent external data; or
4. a training/test split is used and only the untouched test labels are
   permuted, conditional on the trained weight.

Cross-fitting alone does not automatically provide exactness when all folds
are reused for testing. For the finite-sample guarantee, the complete foldwise
learner must be rerun for each permutation. Fold assignments themselves must
be fixed from design information or treated symmetrically.

## Current Recommendation

1. Rename the three mechanisms as directional sign agreement, shared radial
   heterogeneity, and block-centre nuisance; do not call all three node signal.
2. Keep within-building permutation as the formal default when building is the
   exchangeability unit.
3. Keep profile and Mantel effects separately interpretable. Do not interpret
   the adaptive CV weight as a physical node/dyad mixing fraction.
4. If an adaptive omnibus test is needed, use a predeclared nested-max or
   fully retrained cross-fitted statistic and recompute it under every
   permutation.
5. Before adopting the CV rule, vary its temperature, use unequal building
   sizes, and validate on a substantive building model or real pilot data.

## Files

- `scripts/run_application_node_decomposition_20260812.py`
- `scripts/summarize_application_node_decomposition_20260812.py`
- `results/application_node_decomposition_combined_20260812.tsv`
- `results/application_node_decomposition_effects_20260812.tsv`
- `results/adaptive_weight_null_combined_20260812.tsv`
