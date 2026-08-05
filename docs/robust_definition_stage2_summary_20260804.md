# Robust-Reference c_delta: Stage-2 Theory and High-Replication Validation

Date: 2026-08-04

## Project Decision

The new definition should remain in the existing `c_delta_simulation` project.
It retains the same paired-salience research question, corrected normalisation,
and permutation engine as the archived method. Keeping the old and new profile
definitions together provides direct historical controls and prevents the
evidence for a redefinition from being separated from the evidence that
motivated it. A separate project would become useful only if the target changes
from paired salience to a different object, such as full distance-matrix
dependence, clustering, or a multivariate spatial-outlier test.

## Leading Definition

For one marginal sample `z_1, ..., z_n`, define

```text
m_z = median(z),
s_z = 1.4826 median_i |z_i - m_z|,
```

with a documented nonzero-scale fallback. Holding `s_z` fixed, estimate the
Huber location `T_z` from

```text
sum_i psi_1.345((z_i - T_z) / s_z) = 0,
psi_c(u) = sign(u) min(|u|, c).
```

Score every observation, including remote observations, by

```text
R_zi = |z_i - T_z| / s_z.
```

For paired margins `x` and `y`, the leading candidate is

```text
c_delta^HR
    = mean(R_xi R_yi) / (mean(R_x) mean(R_y)).
```

This is a fit-robustly/score-all construction. Remote observations have bounded
contribution to fitting the reference location, but their final salience is
retained. It therefore does not equate robustness with deleting the
observations that may carry the scientific signal.

## Population Target and Null

Let `T(F)` and `s(F)` denote the Huber-location and MAD-scale functionals of a
marginal distribution `F`, and let

```text
r_F(x) = |x - T(F)| / s(F).
```

For a paired population `(X, Y)` with marginal laws `F` and `G`, the population
target is

```text
C_HR(F, G, P_XY)
    = E[r_F(X) r_G(Y)] / (E[r_F(X)] E[r_G(Y)]).
```

When the paired salience variables are independent, this target equals `1`.
The sample permutation null is slightly more general: conditional on any two
fixed positive profiles, a uniformly random re-pairing gives

```text
E_perm[c_delta^HR] = 1
```

exactly. The stage-2 exact enumeration checked all `6! = 720` pairings for
each candidate and found absolute numerical error at most `1.11e-16`.

The test is therefore a test of positive paired-salience alignment under an
exchangeable pairing null. It is not a general test of independence between
the original measurements. Longitudinal, clustered, or matched-set designs
need design-respecting permutations.

## Structural Properties

The proposed profile has the following useful properties.

1. **Label symmetry.** Marginal fitting does not depend on observation order.
2. **Translation, reflection, and nonzero-scale invariance.** The
   dimensionless profile is unchanged by `z -> a z + b` for `a != 0`.
3. **Separate marginal fitting.** The `x` profile is fitted without using `y`
   and vice versa, so no paired signal is introduced during preprocessing.
4. **Exact unrestricted conditional permutation reference.** The corrected
   statistic has reference `1` for fixed profiles under unrestricted re-pairing.
   Within-block permutations have a group-specific reference; see the
   2026-08-05 inference-boundary follow-up.
5. **Correlation identity.** As for the previous definition,

   ```text
   c_delta^HR
       = 1 + corr(R_x, R_y) CV(R_x) CV(R_y).
   ```

   Thus the one-sided permutation ordering is the Pearson ordering of the two
   robust salience profiles.
6. **Robust reference, not bounded final influence.** The Huber fit protects
   the ordinary observations from centre displacement, but an uncapped remote
   score still grows without bound. Claims about a positive breakdown point
   for the complete statistic would therefore be inappropriate.

## Why a Second L2-Like Candidate Was Tested

The original one-dimensional L2 divergence satisfies

```text
D_i^2
    = n / (n - 1) [(x_i - mean(x))^2 + population_variance(x)].
```

Consequently, changing from the old L2 divergence to a pure robust radius does
two things: it robustifies the centre and removes the common variance floor.
To separate these mechanisms, stage 2 tested

```text
R_zi(lambda)
    = sqrt(((z_i - T_z) / s_z)^2 + lambda^2)
```

with `lambda = 0.5` and `1`. These are robust analogues of the old L2 geometry.
The floor variants remained calibrated but provided no consistent power gain;
their largest absolute rejection-rate difference from the pure radius version
was `.0334`, and the pure radius was generally better for diffuse, heavy-tail,
and unmatched-masking alternatives. The additional `lambda` parameter is not
currently justified. The pure radius remains the leading candidate.

## Bounded Sensitivity Definition

A second, explicitly different estimand caps the dimensionless score:

```text
R_zi^(6) = min(R_zi, 6).
```

This asks whether paired salience remains after limiting the leverage of any
one observation. It is useful when an unmatched remote contaminant would
otherwise dominate the global statistic, but it must be reported as a
sensitivity analysis rather than silently substituted for the score-all
definition.

## High-Replication Design

The formal stage-2 run used:

- sample sizes `n = 20, 40, 80, 160`;
- nine scenarios per sample size;
- 24,000 independently generated datasets per condition;
- 999 Monte Carlo permutations per dataset;
- strict upper-tail `p < .05` rejection;
- common permutation indices across methods within each dataset;
- five methods: original L2, Huber radius, Huber floors `.5` and `1`, and
  Huber radius capped at `6`.

This totals 864,000 simulated paired datasets, 4.32 million fitted method
comparisons, and approximately 4.32 billion permuted statistic evaluations.
The run took 43.7 minutes. The complete output is
`results/robust_definition_highrep_validation_20260804.tsv`.

An independent-seed 3,000-repetition run was retained as
`results/robust_definition_long_validation_20260804.tsv`. Across its 180 rows
that match the formal run, the mean absolute rejection-rate difference was
`.00323` and the corresponding mean across null rows was `.00299`. All three
central directional findings reproduced: Huber radius exceeded old L2 in
every bimodal condition, exceeded it in every t2 condition with `n >= 40`, and
cap 6 exceeded uncapped Huber radius in every unmatched-masking condition. The
largest individual difference was `.0261` in a small-sample t2 row; numerical
claims therefore use the 24,000-repetition estimates.

## Main Results

### Null calibration

Across clean, 5% independently contaminated, and 10% independently
contaminated nulls at all four sample sizes, rejection-rate ranges were:

| Method | Minimum | Maximum | Mean |
|---|---:|---:|---:|
| Original L2 | .0460 | .0519 | .0489 |
| Huber radius | .0462 | .0509 | .0485 |
| Huber floor `.5` | .0459 | .0514 | .0488 |
| Huber floor `1` | .0458 | .0513 | .0489 |
| Huber radius cap `6` | .0460 | .0519 | .0488 |

The new profile therefore shows no detectable systematic type-I inflation in
this grid. These are exchangeable independent-null results, not a guarantee
for dependent designs.

### Selected rejection rates

| `n` | Scenario | Original L2 | Huber radius | Huber cap `6` |
|---:|---|---:|---:|---:|
| 20 | matched 1%, magnitude 8 | .9375 | .9369 | .9247 |
| 80 | matched 1%, magnitude 8 | 1.0000 | 1.0000 | .9995 |
| 20 | diffuse aligned | .7448 | .5992 | .5990 |
| 40 | diffuse aligned | .9726 | .9062 | .9062 |
| 80 | diffuse aligned | .9997 | .9958 | .9958 |
| 40 | t2 matched | .6268 | .6665 | .8452 |
| 80 | t2 matched | .7003 | .7841 | .9908 |
| 160 | t2 matched | .7781 | .8753 | 1.0000 |
| 40 | bimodal aligned | .7213 | .8790 | .8790 |
| 80 | bimodal aligned | .6881 | .9071 | .9071 |
| 160 | bimodal aligned | .6456 | .8860 | .8860 |
| 40 | unmatched masking | .0192 | .0284 | .4441 |
| 80 | unmatched masking | .0408 | .0718 | .5980 |
| 160 | unmatched masking | .0914 | .1361 | .5785 |

### Interpretation

- The Huber radius preserves the old method's sparse matched-outlier power.
- It is substantially stronger under the shared bimodal structure and becomes
  stronger than old L2 under the tested t2 signal for `n >= 40`.
- Old L2 retains a small-sample advantage for the constructed diffuse-aligned
  alternative. The difference becomes negligible by `n = 80`.
- Robust centre fitting alone only partly solves unmatched masking. The cap-6
  sensitivity version is much stronger in that scenario.
- Cap 6 is not uniformly superior: at `n = 20` it slightly reduces sparse
  matched and t2 power. Its scientific question remains different.

## Current Recommendation

Promote the uncapped Huber radius to the leading candidate definition:

```text
primary:     c_delta^HR based on |z_i - T_z| / s_z
sensitivity: c_delta^HR,6 based on min(|z_i - T_z| / s_z, 6)
```

Do not add an L2 radial-floor parameter at this stage. Do not claim that the
uncapped statistic has bounded total influence. Report profile correlation and
permutation p-value as the primary inferential quantities and raw c_delta as a
secondary effect-scale description.

## Next Decision Gate

The next work can remain routine until one of the following choices is needed:

1. whether `6` should be frozen, calibrated from a separate training grid, or
   omitted from the formal definition;
2. whether the definition must cover multivariate observations, which would
   require choosing a spatial Huber/geometric-median and robust-scatter
   construction;
3. whether small-sample diffuse power is part of the primary scientific target
   or an acceptable tradeoff for robustness;
4. whether the manuscript should present one primary statistic plus a
   sensitivity statistic, or a single composite decision rule.

These are substantive theoretical decisions and should be discussed before
they are fixed.
