# Design-Respecting Inference, Discrete Boundaries, and Local Power

Date: 2026-08-05

## Bottom Line

This phase adds three kinds of statistical support without changing the
recommended c_delta profile definition:

1. within-block permutation restores conditional-null calibration when global
   exchangeability is broken by strata with different scales;
2. tied and discrete data are generally conservative, while a constant margin
   is correctly treated as undetermined;
3. the diffuse tradeoff depends on signal geometry: the Huber profile can be
   stronger than original L2 for weak, balanced lognormal salience, although
   severe unmatched contamination defeats every tested global method.

The primary remains the uncapped Huber-reference profile, with cap 6 as a
separate sensitivity analysis. The main improvement is inferential: the
permutation group and its reference must now be stated as part of the method.

## 1. Why the Permutation Design Is Part of the Hypothesis

For unrestricted re-pairing of two fixed positive profiles `A` and `B`,

```text
E_perm[C(A, B)] = 1.
```

Suppose observations belong to exchangeability blocks `b`, and only pairings
within the same block are allowed. Conditional on the profiles and blocks,

```text
E_block[C(A, B)]
  = { (1/n) sum_b [sum(A_b) sum(B_b) / n_b] }
    / {mean(A) mean(B)}.
```

This is generally not `1`: between-block salience differences are deliberately
preserved by every allowed permutation. The p-value remains valid for the
within-block conditional null because the observed statistic is compared with
the correct restricted randomisation distribution. However, reports should
give the restricted reference above rather than interpret `c_delta - 1` as the
conditional effect. A two-sided restricted test must likewise measure both
tails around this group-specific reference rather than around `1`.

The implementation now supports optional block labels in
`permutation_test_profiles(..., blocks=...)` and returns both the Monte Carlo
and exact restricted-permutation reference means. Exact enumeration unit tests
verify the formula.

This is consistent with the broader permutation literature: exactness comes
from the relevant invariance/exchangeability group, and unrestricted
permutation can fail when heterogeneous populations are mixed. Blockwise
permutation preserves the exchangeability structure, while studentisation is
another route for particular heterogeneous-parameter problems. Relevant
primary references are:

- Winkler et al., *Permutation inference for the general linear model*:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC4010955/>;
- Zhou, Zwilling, and Calhoun, *Efficient Blockwise Permutation Tests
  Preserving Exchangeability*:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC4185212/>;
- Chung and Romano, *Exact and Asymptotically Robust Permutation Tests*:
  <https://arxiv.org/abs/1304.5939>.

The Chung-Romano studentisation results do not automatically prove validity for
c_delta. They reinforce the narrower point that a permutation distribution
must match the null being tested; the present project directly validates
within-block permutation for its conditional paired-salience null.

## 2. Design-Respecting Permutation Simulation

### Design

The simulation used:

- `n = 40, 80, 160`;
- two or four equal-size blocks;
- largest-to-smallest block scale ratios `2` and `4`;
- independent `x` and `y` within each block under the conditional null;
- matched 5% within-block signals of standardised magnitude `4` or `6`;
- unrestricted and within-block permutations;
- original L2, Huber primary, and Huber cap 6;
- 1,500 repetitions and 499 permutations per condition.

The 54,000 generated datasets use the same data and common randomisation draws
for method comparisons. At a true rejection probability near `.05`, the Monte
Carlo standard error is approximately `.0056`.

### Conditional-null calibration

| Permutation | Method | Minimum | Maximum | Mean |
|---|---|---:|---:|---:|
| Unrestricted | Original L2 | .1360 | .9060 | .4417 |
| Unrestricted | Huber primary | .1467 | .9847 | .5158 |
| Unrestricted | Huber cap 6 | .1467 | .9893 | .5201 |
| Within block | Original L2 | .0360 | .0580 | .0481 |
| Within block | Huber primary | .0380 | .0607 | .0474 |
| Within block | Huber cap 6 | .0380 | .0607 | .0473 |

Under scale ratio `2`, unrestricted mean rejection was `.2740` for old L2 and
`.3028` for the Huber primary. At scale ratio `4`, it rose to `.6094` and
`.7289`. Within-block means remained `.0460-.0487` across both ratios.

These unrestricted rejections are not ordinary numerical type-I failures. The
global profiles genuinely align because the same blocks are high-scale in both
margins. They are false positives only relative to the conditional question
“is there additional within-block paired salience?” The permutation design
determines which of these scientific questions is being tested.

### Restricted reference and power

Under the conditional null, the average observed and restricted-reference
values were:

| Method | Mean observed | Mean restricted reference |
|---|---:|---:|
| Original L2 | 1.0241 | 1.0241 |
| Huber primary | 1.1888 | 1.1892 |
| Huber cap 6 | 1.1879 | 1.1883 |

The unrestricted reference remained approximately `1`. The restricted
reference can be substantially above `1`, especially for the robust radius,
confirming the exact formula's practical importance.

Within-block matched-signal power averaged over block counts and scale ratios:

| `n` | Signal | Original L2 | Huber primary | Huber cap 6 |
|---:|---:|---:|---:|---:|
| 40 | 4 | .7510 | .7608 | .7022 |
| 40 | 6 | .9240 | .9393 | .8882 |
| 80 | 4 | .9505 | .9537 | .9190 |
| 80 | 6 | .9922 | .9955 | .9837 |
| 160 | 4 | .9977 | .9982 | .9907 |
| 160 | 6 | .9998 | 1.0000 | .9998 |

Correct conditional calibration therefore does not make the test unusably
weak. The cap again loses some power for genuine matched extremes, supporting
its role as sensitivity analysis rather than co-primary inference.

## 3. Discrete, Tied, and Degenerate Margins

### Design

The boundary study covered Bernoulli, three-level ordinal, Poisson,
zero-inflated, rounded-normal, near-constant, and exactly constant margins at
`n = 20, 40, 80`, plus shared rare-binary, ordinal, and zero-pattern
alternatives. It used 1,500 repetitions and 499 permutations, for 54,000
generated datasets.

### Null behaviour

Across all nondegenerate discrete null rows:

| Method | Minimum | Maximum | Mean |
|---|---:|---:|---:|
| Original L2 | .0187 | .0600 | .0433 |
| Huber primary | .0207 | .0580 | .0419 |
| Huber cap 6 | .0207 | .0580 | .0414 |

The lowest rejection rates occurred for Bernoulli margins. With strict
upper-tail comparison using `>=`, tied permutation statistics make the test
conservative. This is preferable to silently adding random jitter, which would
change the scientific data and the exact randomisation distribution.

For Bernoulli `.50`, the robust profiles were constant in about `.076` of
datasets and old L2 profiles in about `.234`. A constant positive profile has
no ordering information: its p-value is one rather than evidence of no raw
association. Binary raw agreement is not automatically a paired-salience
alternative.

Bernoulli `.20`, zero-inflated, and rare shared-pattern data were occasionally
fully constant, especially at `n = 20`. Across the shared-pattern alternatives,
mean power was `.8796` for the Huber primary at `n = 20`, `.9847` at `n = 40`,
and `.9998` at `n = 80`.

### Degeneracy and near-zero scale

When one margin was exactly constant, all three methods had determined rate
zero at every sample size. The correct report is “undetermined due to data
limitations,” not `c_delta = 1`, zero association, or a nonsignificant result.

Near-constant continuous margins with fluctuations of order `1e-12` retained
null rejection near `.0476` for the robust methods, consistent with affine
scale invariance. This is numerical evidence, not a recommendation to analyse
variation below measurement resolution. A scientific implementation should
pre-specify a minimum meaningful marginal spread based on instrument precision;
that threshold should not be estimated post hoc from the paired result.

## 4. Local Diffuse-Salience Power

### Design

The local-power study generated correlated lognormal magnitudes using a
Gaussian latent correlation `rho = 0, .1, .2, .3, .5, .7`, independent random
signs, `n = 20, 40, 80, 160, 320`, and either no contamination or independently
located 5% magnitude-20 contamination. It used 1,200 repetitions and 499
permutations, for 72,000 generated datasets.

At a true rejection probability near `.05`, the Monte Carlo standard error is
approximately `.0063`; near `.50` it is `.0144`.

### Calibration

At `rho = 0`, mean rejection across sample sizes was `.0463` for the clean
Huber primary, `.0473` for clean old L2, `.0480` for contaminated Huber, and
`.0475` for contaminated old L2. The local-power curves therefore start from a
well-calibrated null.

### Clean local power

Selected results:

| `rho` | `n` | Original L2 | Huber primary | Huber cap 6 |
|---:|---:|---:|---:|---:|
| .2 | 40 | .206 | .221 | .221 |
| .2 | 80 | .363 | .421 | .421 |
| .2 | 160 | .618 | .704 | .704 |
| .2 | 320 | .877 | .942 | .942 |
| .3 | 40 | .401 | .448 | .448 |
| .3 | 80 | .635 | .717 | .717 |
| .3 | 160 | .911 | .957 | .957 |
| .5 | 40 | .766 | .812 | .812 |

In this balanced, weak-to-moderate lognormal diffuse family, the Huber primary
is generally more powerful than old L2. This does not contradict the earlier
uniform/sign-imbalanced diffuse results where L2 was stronger. It shows that
“diffuse” is not a sufficient description of an alternative: sign balance,
magnitude distribution, centre displacement, tail shape, and contamination
all affect the profile geometry.

The approximate tested-grid requirements for `.80` power were:

- `rho=.5`: `n=40` for Huber; old L2 crossed `.80` at `n=80`;
- `rho=.3`: `n=160` for all methods;
- `rho=.2`: `n=320` for all methods;
- `rho=.1`: no method reached `.80` by `n=320`.

These are simulation planning anchors for this generator, not universal sample
size formulas.

### Severe unmatched contamination

With independently located 5% magnitude-20 contamination, no method approached
`.80` power anywhere in the grid. Even at `rho=.7`, `n=320`, rejection was
`.058` for old L2, `.079` for the Huber primary, and `.152` for cap 6.

This is strong evidence for a remaining limitation: a global average-product
statistic can be masked by a small number of unmatched high-leverage
observations even when its marginal centre is robust. Cap 6 helps but cannot
recover a weak signal distributed over the whole sample. A future sparse or
trimmed product aggregator could address this, but it would be a new decision
rule and should not be added without a separate theoretical decision.

## 5. Updated Supported Procedure

For one-dimensional paired data:

1. fit the Huber `1.345` location and MAD scale separately in each margin;
2. construct all-observation robust salience profiles;
3. declare the permutation group from the sampling or randomisation design;
4. use unrestricted permutations only under global exchangeability;
5. otherwise use pre-specified exchangeability blocks;
6. report the exact permutation reference for the chosen group;
7. treat an exact constant or scientifically negligible-spread margin as
   undetermined;
8. use cap 6 as a leverage sensitivity, not an unadjusted second primary;
9. retain old L2 as a pre-specified comparator when its clean diffuse geometry
   is scientifically important.

## 6. Remaining Evidence Priorities

The next strongest support would come from:

- frozen-specification analysis on real or realistically structured data;
- a measurement-resolution rule for practically degenerate margins;
- coverage evaluation for effect-size intervals relative to the correct
  unrestricted or restricted permutation reference;
- a formal influence-function derivation including fitted Huber location and
  MAD scale;
- only after a substantive decision, a sparse/trimmed aggregation comparator
  for severe unmatched contamination.

Raw outputs:

- `results/design_respecting_permutation_20260805.tsv`;
- `results/discrete_degeneracy_validation_20260805.tsv`;
- `results/local_salience_power_20260805.tsv`.
