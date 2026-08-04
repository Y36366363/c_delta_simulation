# Cap Loss Function and Diffuse-Tradeoff Decision

Date: 2026-08-05

## Bottom Line

The evidence now supports a relatively stable two-profile specification:

```text
Primary profile:
    R_zi = |z_i - T_z| / s_z,
    with Huber location constant 1.345.

Bounded sensitivity profile:
    R_zi^(6) = min(R_zi, 6).

Formal inference:
    based on the primary profile.

Sensitivity interpretation:
    whether the paired-salience conclusion survives after limiting the
    direct leverage of one observation to six robust scale units.
```

Cap 6 is not claimed to be a universal mathematical constant. In this project
it is the solution of a pre-specified constrained loss: maximise masking
resistance while allowing no more than three percentage points of worst-case
absolute power loss over the defined core alternatives. The cap must be
calibrated again if the scientific alternatives, contamination model, or loss
tolerance changes.

The small-sample diffuse-power loss of the primary profile should be accepted
for the present paired-exceptional-salience objective, but explicitly reported.
Attempts to recover it by increasing the Huber location constant transfer a
similar or larger loss to bimodal salience. For diffuse alignment as the main
scientific target, the old L2 statistic should remain a comparator rather than
silently changing the robust primary definition.

## 1. Literature Cross-Validation

### Huber contamination and efficiency

Huber's location paper treats robustness as optimisation under approximate
distributional knowledge and contaminated-normal neighbourhoods. Its
M-estimators interpolate between the sample mean and median rather than
declaring one estimator universally best:

- Peter J. Huber (1964), *Robust Estimation of a Location Parameter*:
  <https://projecteuclid.org/journals/annals-of-mathematical-statistics/volume-35/issue-1/Robust-Estimation-of-a-Location-Parameter/10.1214/aoms/1177703732.full>

For a standard normal location model, the asymptotic efficiency of the Huber
score with clipping constant `k` is

```text
eff(k) = P(|Z| <= k)^2 / E[min(Z^2, k^2)].
```

This gives:

| Huber location constant | Normal-model efficiency |
|---:|---:|
| 1.345 | .9500 |
| 2 | .9897 |
| 3 | .9996 |
| 4 | .99999 |

Thus increasing the centre constant is expected to improve ideal-model
efficiency while weakening clipping. The simulations below show that in this
problem the practical loss is not merely outlier resistance: a more mean-like
centre also loses power for an unbalanced finite-sample bimodal structure.

Adaptive Huber regression provides a modern nonasymptotic example where the
robustification parameter adapts to sample size, dimension, and moment
conditions to balance bias and robustness. Its regression theory does not
directly determine the c_delta cap, but it supports a calibration protocol over
a universal constant:

- Q. Sun, W.-X. Zhou, and J. Fan, *Adaptive Huber Regression*:
  <https://arxiv.org/abs/1706.06991>

### Robust dependence measures

Leyder, Raymaekers, and Rousseeuw distinguish influence function, finite-sample
sensitivity, and breakdown for distance correlation. They show that a bounded
population influence function can coexist with zero breakdown and unbounded
finite-sample sensitivity, then introduce a bounded/redescending transformation.
They also argue that comparing classical and robust versions can reveal how
outliers affect the conclusion:

- S. Leyder, J. Raymaekers, and P. J. Rousseeuw, *Robust Distance Covariance*:
  <https://onlinelibrary.wiley.com/doi/full/10.1111/insr.70005>
- Open preprint, *Is Distance Correlation Robust?*:
  <https://arxiv.org/abs/2403.03722>

That distinction is directly relevant here. Robustly fitting `T_z` does not
bound the uncapped final score. Applying cap 6 changes the final influence and
therefore defines a sensitivity estimand, not a cosmetic implementation detail.

The h-star paper explicitly treats exceptional observations as phenomena to
evaluate rather than automatically remove. This supports keeping the uncapped
score-all profile as primary while using a bounded version to assess leverage:

- J. F. Hoorn and J. K. W. Ho, *A test statistic, h-star, for outlier
  analysis*: <https://arxiv.org/abs/2508.06792>

The archived c_delta paper defines the original internal-divergence target and
acknowledges sensitivity to outliers:

- J. F. Hoorn, *Correlation of divergency: c-delta*:
  <https://arxiv.org/abs/2510.16717>

## 2. Direct-Influence Interpretation of a Cap

Let `A = R_x`, `B = R_y`, with positive population means `mu_A` and `mu_B`,
and write

```text
C = E[A B] / (mu_A mu_B).
```

If the fitted marginal references are temporarily held fixed, the direct
influence of contamination with scores `(a, b)` is

```text
IF_direct(a, b)
    = a b / (mu_A mu_B)
      - C a / mu_A
      - C b / mu_B
      + C.
```

For the uncapped profile, `a` and `b` can grow without bound. For the cap-`c`
profile, `0 <= a,b <= c`, so this direct component is bounded whenever the
profile means remain positive. The full influence also contains the effects of
estimating the Huber location and MAD scale; these are bounded under the usual
regularity conditions but require a separate formal derivation for a complete
influence-function theorem.

This calculation explains why cap selection is a robustness-policy decision:
smaller `c` lowers the maximum direct contribution but also compresses genuine
matched exceptional observations.

## 3. Constrained Cap Loss

### Definition

For each candidate cap `c`, define

```text
size_max(c)
    = maximum null rejection rate,

loss_core(c)
    = maximum over core settings of
      max(0, power_uncapped - power_c),

gain_mask(c)
    = mean over masking settings of
      (power_c - power_uncapped).
```

The core alternatives were:

- matched 1% magnitude-8 salience;
- t2 matched salience;
- diffuse aligned salience;
- bimodal aligned salience.

The training rule was

```text
choose c maximising gain_mask(c), subject to
    size_max(c) <= .065,
    loss_core(c) <= .03.
```

The `.065` training filter is a Monte Carlo screening tolerance, not the final
nominal level. Final null calibration is assessed on an independent evaluation
seed with Wilson intervals. The `.03` power tolerance is the substantive loss
policy: no core alternative should lose more than three absolute percentage
points relative to the uncapped profile.

### Three-seed training results

The fine grid used caps `4.5, 5, 5.5, 6, 6.5, 7, 8`, three independent seeds,
`n = 20, 40, 80`, 1,200 repetitions per seed and condition, and 499
permutations.

| Cap | Maximum null | Worst core loss | Mean core loss | Mean masking gain | Feasible at `.03` |
|---:|---:|---:|---:|---:|---:|
| 4.5 | .0508 | .0908 | .0251 | .4450 | No |
| 5 | .0511 | .0567 | .0117 | .4327 | No |
| 5.5 | .0508 | .0319 | .0052 | .3970 | No |
| 6 | .0503 | .0158 | .0023 | .3519 | Yes, selected |
| 6.5 | .0506 | .0050 | .0008 | .3047 | Yes |
| 7 | .0503 | .0022 | .0002 | .2561 | Yes |
| 8 | .0500 | .0000 | .0000 | .1725 | Yes |

Cap 6 is the first grid value comfortably inside the three-point core-loss
constraint and has the largest masking gain among feasible values.

### Dependence on the declared tolerance

| Allowed worst core loss | Selected cap |
|---:|---:|
| .005 | 7 |
| .010 | 6.5 |
| .020 | 6 |
| .030 | 6 |
| .040-.050 | 5.5 |
| .060 | 5 |
| .100 | 4.5 |

This table should accompany any recommendation of cap 6. It makes the policy
transparent: cap 6 corresponds to a two-to-three-point core-power tolerance.

### Independent cap-6 evaluation

The evaluation used a new seed, `n = 20, 40, 80, 160`, 5,000 repetitions, and
999 permutations.

| `n` | Scenario | Uncapped | Cap 6 |
|---:|---|---:|---:|
| 20 | clean null | .0488 | .0490 |
| 20 | 10% contaminated null | .0500 | .0524 |
| 160 | clean null | .0514 | .0514 |
| 160 | 10% contaminated null | .0548 | .0556 |
| 20 | matched 1%, magnitude 8 | .9352 | .9238 |
| 20 | t2 matched | .4734 | .4510 |
| 40 | t2 matched | .6672 | .8368 |
| 80 | t2 matched | .7834 | .9912 |
| 20 | unmatched masking | .0016 | .1442 |
| 40 | unmatched masking | .0308 | .4412 |
| 80 | unmatched masking | .0716 | .5952 |
| 160 | unmatched masking | .1390 | .5800 |

The largest independent core loss was `.0224` in the `n = 20` t2 setting,
inside the declared `.03` tolerance. The largest observed null rejection was
`.0556`; its Monte Carlo uncertainty remains compatible with a near-.05 test.

## 4. Diffuse-Loss Mechanism

### Centre-constant scan

Huber location constants `1.345, 2, 3, 4` and an exploratory tail-triggered
choice between `1.345` and `4` were tested over `n = 12, 20, 40, 80`, 2,500
repetitions, and 499 permutations.

At `n = 20`:

| Scenario | `c=1.345` | `c=2` | `c=3` | `c=4` | Adaptive |
|---|---:|---:|---:|---:|---:|
| Diffuse noise .15 | .587 | .713 | .769 | .780 | .770 |
| Diffuse noise .30 | .563 | .663 | .702 | .711 | .705 |
| Diffuse noise .50 | .438 | .508 | .532 | .534 | .532 |

Larger constants recover diffuse power by making the centre more mean-like.
However, at `n = 80` bimodal aligned power was `.905`, `.788`, `.695`, and
`.692` for constants `1.345`, `2`, `3`, and `4`. The adaptive rule was `.694`
because the simple tail trigger does not reliably distinguish meaningful
bimodality from a clean diffuse distribution.

### Independent joint validation

An independent seed compared `c=1.345`, `c=2`, and both cap-6 versions across
four sample sizes, nine scenarios, 4,000 repetitions, and 999 permutations.

- Null rejection ranges were `.0425-.0522` for all four methods.
- At `n = 20`, changing to `c=2` raised diffuse-noise-.15 power from `.596` to
  `.723` and diffuse-noise-.50 power from `.429` to `.492`.
- At `n = 40`, it reduced bimodal power from `.875` to `.851`.
- At `n = 80`, it reduced bimodal power from `.912` to `.792`.
- At `n = 160`, the bimodal loss was `.138`.
- Sparse matched, t2, and unmatched-masking behavior changed little between the
  two centre constants; the cap, rather than the centre constant, controlled
  masking resistance.

The candidate `c=2` therefore moves the tradeoff rather than solving it. The
data-triggered version adds two more constants and loses the bimodal advantage,
so it is not justified as the primary definition.

## 5. Decision on the Diffuse Tradeoff

For the present project, accept the diffuse tradeoff subject to explicit scope:

1. The intended target is paired exceptional salience relative to a robust
   marginal reference, not optimal detection of every diffuse dependence form.
2. The loss is most material for small samples (`n <= 40`) and becomes small
   by roughly `n = 60-80` in the tested diffuse family.
3. Increasing the Huber constant recovers diffuse power but loses a distinctive
   advantage under bimodal salience, especially at moderate and large `n`.
4. Cap 6 does not create the diffuse loss and should not be tuned to repair it.
5. When a study has small `n` and diffuse magnitude alignment is a primary
   scientific alternative, report old L2 or another diffuse-oriented comparator
   alongside the robust primary and state that the tests answer different
   robustness questions.

This is a conditional acceptance, not a claim of uniform superiority. A paper
should include the diffuse power curve as a limitation and should avoid saying
that non-rejection by the robust statistic rules out all forms of aligned
internal variation.

## 6. Recommended Version for a First Formal Report

### Primary c_delta

For each margin `z`:

```text
m_z = median(z),
s_z = 1.4826 median_i |z_i - m_z|,
T_z solves sum_i psi_1.345((z_i - T_z) / s_z) = 0,
R_zi = |z_i - T_z| / s_z.
```

Then

```text
c_delta^HR
    = mean(R_xi R_yi) / (mean(R_x) mean(R_y)).
```

Use the exchangeability-respecting permutation p-value for formal inference.

### Bounded sensitivity

```text
R_zi^(6) = min(R_zi, 6),
c_delta^HR,6
    = mean(R_xi^(6) R_yi^(6))
      / (mean(R_x^(6)) mean(R_y^(6))).
```

Report this as a pre-specified sensitivity analysis. Do not define formal study
significance as the unadjusted union of the two p-values.

### Required disclosure

- `1.345` targets a conventional robustness/normal-efficiency compromise for
  the marginal reference centre.
- `6` is calibrated under a declared `.03` worst-core-power tolerance in the
  project's reference grid.
- The uncapped primary has unbounded final score influence.
- The capped statistic answers a different leverage-limited question.
- Small-sample diffuse power can be lower than old L2.
- Neither variant is a general independence test on the original values.
