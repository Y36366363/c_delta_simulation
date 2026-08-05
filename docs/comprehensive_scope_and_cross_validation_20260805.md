# Comprehensive Scope, Original-Definition Comparison, and Cap-6 Cross-Validation

Date: 2026-08-05

## Decision

The robust-reference definition has enough evidence to justify continued
development. The evidence does **not** support calling it a universally better
replacement for every use of the original L2 definition. It supports a
moderately broad method for a clearly stated target:

> positive alignment of paired observation-level salience relative to robustly
> fitted marginal references, under an exchangeable or design-respecting
> pairing null.

Within that target, the new definition is usable across normal, heavy-tailed,
skewed, contaminated, and globally multimodal marginals. Its central
limitations are mainly restrictions on the scientific target and permutation
design, not reasons to abandon the method. It should not be presented as a
general correlation, general independence, causal, or full-geometry statistic.

The recommended reporting structure remains:

```text
formal primary: uncapped Huber-reference c_delta
robustness sensitivity: pre-calibrated cap-6 c_delta
diffuse comparator when scientifically pre-specified: original L2 c_delta
```

The unadjusted union of their p-values is not a single level-.05 decision rule.

## 1. Definitions Being Compared

For paired scalar observations `(x_i, y_i)`, the corrected coefficient for any
two nonnegative profiles `A` and `B` is

```text
C(A, B) = mean(A_i B_i) / (mean(A_i) mean(B_i)).
```

The unrestricted random-pairing reference is exactly `1` conditional on fixed
profiles. For restricted permutations, use the group-specific reference
derived in `docs/inference_boundaries_and_local_power_20260805.md`.

### Original L2 profile

The original one-dimensional L2 divergence satisfies

```text
D_zi^2 = n / (n - 1) [(z_i - mean(z))^2 + variance_population(z)].
```

It uses the non-robust sample mean, contains a common variance floor, and gives
quadratic leverage to remote values before the square root. It can be highly
efficient for clean diffuse magnitude alignment, but an unmatched remote value
can move the centre, inflate the common scale, and dominate the profile.

### Robust-reference primary

Let

```text
s_z = 1.4826 median_i |z_i - median(z)|,
sum_i psi_1.345((z_i - T_z) / s_z) = 0,
R_zi = |z_i - T_z| / s_z.
```

Then

```text
c_delta^HR = C(R_x, R_y).
```

This is a fit-robustly/score-all construction. It protects the marginal
reference from remote points while retaining them as possible scientific
signals. The final uncapped score remains unbounded.

### Bounded cap-6 sensitivity

```text
R_zi^(6) = min(R_zi, 6),
c_delta^HR,6 = C(R_x^(6), R_y^(6)).
```

This limits direct final-score leverage. It is a different, leverage-limited
estimand and is not silently interchangeable with the primary statistic.

## 2. Comprehensive Comparison Design

The new benchmark used:

- sample sizes `n = 20, 40, 80, 160`;
- 18 scenarios;
- 1,500 independently generated datasets per condition;
- 499 common permutations for all methods within a dataset;
- original L2, original L1, Huber primary, and Huber cap 6.

The scenarios covered six exchangeable nulls, eight core alternatives, partial
overlap, unmatched masking, reverse salience, and a deliberately invalid
unrestricted-permutation design with a shared heteroskedastic scale pattern.
The benchmark contains 108,000 generated paired datasets.

With 1,500 repetitions, the binomial Monte Carlo standard error is about
`.0056` near a rejection rate of `.05` and `.0129` near `.50`. Differences of
one or two percentage points in isolated rows should therefore not be treated
as stable rankings without replication.

## 3. Calibration and Average Performance

### Exchangeable nulls

Across 24 null conditions per method:

| Method | Minimum | Maximum | Mean |
|---|---:|---:|---:|
| Original L2 | .0400 | .0593 | .0476 |
| Original L1 | .0367 | .0580 | .0475 |
| Huber primary | .0380 | .0587 | .0482 |
| Huber cap 6 | .0387 | .0620 | .0485 |

There is no evidence of systematic size inflation for the new profiles under
the tested exchangeable nulls. The maximum `.0620` is one Monte Carlo row, not
evidence that the population size is `.062`.

### Core-alternative averages

| `n` | Original L2 | Original L1 | Huber primary | Huber cap 6 |
|---:|---:|---:|---:|---:|
| 20 | .7709 | .7382 | .7609 | .7571 |
| 40 | .8863 | .8658 | .9033 | .9258 |
| 80 | .9108 | .9256 | .9428 | .9681 |
| 160 | .9128 | .9406 | .9506 | .9680 |

The Huber primary is not better at `n = 20` on average; it is stronger from
`n = 40` onward in this grid. Averaged over all sample sizes and core
alternatives, rejection was `.8702` for old L2, `.8894` for the Huber primary,
and `.9047` for cap 6.

### Alternative-family averages across sample sizes

| Scenario | Original L2 | Huber primary | Huber cap 6 | Primary minus L2 |
|---|---:|---:|---:|---:|
| Diffuse, low noise | .9378 | .8797 | .8795 | -.0582 |
| Diffuse, high noise | .8213 | .7992 | .7993 | -.0222 |
| Sparse matched 5%, magnitude 6 | .9727 | .9697 | .9665 | -.0030 |
| Sparse matched 1%, magnitude 8 | .9732 | .9733 | .9708 | +.0002 |
| t2 matched 5%, magnitude 8 | .6405 | .6900 | .8182 | +.0495 |
| Balanced shared bimodality | .6225 | .8083 | .8083 | +.1858 |

The new method preserves sparse matched-salience detection, improves
heavy-tail and balanced-bimodal performance, and pays a real diffuse-alignment
cost. There is no uniform dominance theorem hiding in these averages.

### Masking and partial overlap

For the unmatched-masking alternative, average rejection was `.0410` for old
L2, `.0612` for the uncapped Huber primary, and `.4308` for cap 6. Robust centre
fitting alone is therefore insufficient when a remote unmatched score remains
in the final product; limiting final leverage is what creates most of the
masking resistance.

For the half-overlap alternative, the methods were essentially tied
(`.6723-.6747`). This is useful evidence that the redefinition does not obtain
its gains by changing the basic paired-index-overlap mechanism.

## 4. What Can and Cannot Be Generalised

### Supported moderately broad use

The new definition can be used beyond a narrow normal/outlier toy model when:

1. observations are paired scalar units;
2. global marginal salience relative to one robust reference is meaningful;
3. the null permits unrestricted re-pairing, or permutations are restricted to
   the actual randomisation/block/cluster design;
4. the scientific alternative is positive salience alignment;
5. marginal robust scale is non-degenerate.

The tested evidence covers heavy tails, skewness, independent contamination,
shared sparse salience, partial overlap, diffuse salience, and global
bimodality. This is meaningfully broader than an outlier-only method.

### Conditions requiring qualification or modification

- **Small-sample clean diffuse alignment.** Old L2 can be materially stronger.
- **Multimodality.** A global robust centre tests global salience, including
  shared cluster membership. If the target is within-cluster exceptionality,
  cluster-conditional references must be defined and validated separately.
- **Clustered, longitudinal, or matched-set data.** The profile may remain
  useful, but unrestricted permutation is invalid; block- or design-respecting
  permutation is required.
- **Multivariate observations.** A rotation-invariant spatial centre and robust
  radial scale are needed. Coordinatewise Huber scoring is not a general
  solution.
- **Near-zero marginal spread.** The statistic becomes unstable or
  scientifically undefined and needs an explicit degeneracy rule.

### Claims that remain unsupported

The statistic should not be described as a general test of raw-value
independence, linear correlation, causal dependence, or equality of full
pairwise-distance geometry. A shared heteroskedastic scale pattern produced
rejection increasing from roughly `.31` at `n = 20` to `.96` at `n = 160` for
the robust methods. That scenario is a genuine paired-salience alternative but
is a design violation if one calls it a null and permutes without respecting
the scale strata. This distinction must be explicit.

## 5. Expanded Cap-6 Cross-Validation

An expanded grid independently compared caps `5.5`, `6`, and `6.5` using:

- 36 independently contaminated null conditions;
- 48 clean matched-core conditions;
- 96 unmatched-masking conditions;
- `n = 20, 40, 80, 160`;
- normal, t2, and t3 backgrounds;
- contaminant magnitudes `10, 20, 50`;
- 1,000 repetitions and 499 common permutations.

This contributes 180,000 further generated datasets.

| Candidate | Null range | Worst clean-core loss | Mean clean-core loss | Mean masking gain |
|---|---:|---:|---:|---:|
| Cap 5.5 | .036-.063 | .029 | .0058 | .2516 |
| Cap 6 | .035-.062 | .024 | .0025 | .2319 |
| Cap 6.5 | .036-.060 | .009 | .0011 | .2114 |

Cap 6 remains the most defensible compromise under the declared maximum
three-point core-loss policy. Cap 5.5 touched `.029` in this evaluation but had
already reached `.0319` in the earlier three-seed training study; it sits on an
unstable boundary. Cap 6.5 provides a larger clean-power safety margin but
gives up about two percentage points of average masking gain relative to cap 6.

Mean masking rejection for uncapped versus cap 6 was:

| `n` | Uncapped | Cap 6 |
|---:|---:|---:|
| 20 | .0086 | .0565 |
| 40 | .0706 | .3022 |
| 80 | .2097 | .5616 |
| 160 | .3592 | .6555 |

Cap 6 is therefore cross-validated as a project-specific policy, not a
universal constant. A new application with a different contamination model or
loss tolerance should repeat the prospective calibration.

## 6. Expanded Diffuse Tradeoff

The diffuse boundary expansion used 80 conditions formed by:

- `n = 12, 20, 40, 80, 160`;
- noise `.15` or `.50`;
- balanced signs or a `.65` positive-sign probability;
- uniform or lognormal shared magnitudes;
- no contamination or independent 5% magnitude-20 contamination;
- 1,500 repetitions and 499 common permutations.

It contributes 120,000 generated datasets.

### Clean diffuse alternatives

Mean rejection by sample size was:

| `n` | Original L2 | Huber primary | Difference |
|---:|---:|---:|---:|
| 12 | .3657 | .2953 | -.0704 |
| 20 | .5992 | .4938 | -.1055 |
| 40 | .8325 | .7288 | -.1037 |
| 80 | .9462 | .8682 | -.0781 |
| 160 | .9902 | .9454 | -.0447 |

Across all 40 clean conditions, the primary was more than three points worse
than old L2 in 27 and within three points in 13; it was never more than three
points better. The largest observed deficit was `.2827` for `n = 80`, low
noise, uniform magnitudes, and sign probability `.65`.

This expansion corrects the earlier shorthand that the diffuse difference is
always negligible by `n = 80`. Absolute power often approaches one at large
`n`, but meaningful gaps persist in sign-imbalanced or harder diffuse families.
The limitation is structural, not only a small-sample phenomenon.

### Independently contaminated diffuse alternatives

At 5% independent magnitude-20 contamination, mean rejection stayed near the
nominal level for old L2 and the uncapped primary at every sample size. Cap 6
rose from `.0707` at `n = 12` to `.1238` at `n = 160`; in the strongest
lognormal/sign-imbalanced row it reached `.2893` at `n = 160`, versus `.0533`
uncapped.

Thus cap 6 partly restores diffuse detection under severe unmatched
contamination, but does not solve it generally. The correct conclusion is not
that the capped method dominates; rather, severe independent contamination can
erase a diffuse signal for all tested global statistics, and cap 6 recovers a
limited portion by preventing a few observations from monopolising leverage.

## 7. Final Assessment of Research Value

Continued exploration is justified for four reasons:

1. the population target and exact conditional permutation reference are
   interpretable;
2. calibration is stable across a broad exchangeable-null grid;
3. the robust primary improves important heavy-tail and multimodal regimes
   without sacrificing sparse matched-salience power;
4. cap 6 now has a transparent loss policy and independent neighbouring-cap
   cross-validation.

The method can be made moderately broad by stating its target precisely and
using design-respecting permutations. Its limitations do not force use only in
one narrow distribution. However, no parameter adjustment found so far makes
it an omnibus dependence test or removes the clean-diffuse tradeoff.

The next decisive evidence should come from real or realistically structured
datasets and from restricted-permutation designs. A multivariate extension is
worth a separate phase only when the scientific data require vector-valued
observations. A cluster-conditional extension should likewise be treated as a
new estimand, not a hidden preprocessing option.

## 8. Reporting Recommendation

For a first formal report:

1. define the Huber-reference profile with constant `1.345` as the primary;
2. use its design-respecting one-sided permutation p-value for formal
   inference;
3. report cap 6 as a pre-specified leverage-limited sensitivity analysis;
4. state the `.03` worst-clean-core-power calibration policy for cap 6;
5. include original L2 as a historical comparator and, when diffuse alignment
   is scientifically central, as a pre-specified secondary analysis;
6. do not combine unadjusted p-values into one reject-if-any rule;
7. report profile correlation, the two marginal profiles, and c_delta relative
   to the correct permutation-group reference so that leverage and disagreement
   are visible.

Detailed raw outputs:

- `results/comprehensive_scope_benchmark_20260805.tsv`;
- `results/cap6_expanded_cross_validation_20260805.tsv`;
- `results/diffuse_boundary_expansion_20260805.tsv`.
