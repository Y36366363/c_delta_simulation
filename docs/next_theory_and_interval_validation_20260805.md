# Next Theory Priorities and Huber c_delta Interval Validation

Date: 2026-08-05

## Decision

The project has reached the point where another broad distribution grid has
lower value than targeted theory. The primary definition, cap-6 policy,
exchangeable-null calibration, restricted-permutation design, discrete-data
boundary, and major power tradeoffs have all received substantial simulation
support.

The next main phase should derive the influence function, asymptotic variance,
and a studentized interval for the uncapped Huber-reference c_delta. Short
simulation studies should continue, but they should test consequences of that
theory rather than search for another centre or cap.

## 1. Current Unresolved Problems, in Priority Order

### 1. Full asymptotic distribution and valid interval estimation

The population primary target is

```text
C(F, G, P_XY)
  = E[r_F(X) r_G(Y)] / {E[r_F(X)] E[r_G(Y)]},

r_F(x) = |x - T(F)| / s(F).
```

For the uncapped coefficient, multiplication of either whole profile by a
positive constant cancels from `C`. Thus the MAD scale cancels directly from
the final ratio, although it still affects the fitted Huber location `T(F)`
through the standardised score equation. A full derivation must include:

- the influence of the marginal Huber locations;
- the influence of their scale functionals on those locations;
- the numerator and two denominator means;
- covariance induced by paired `(X,Y)` observations;
- conditions excluding zero profile means and nondifferentiable boundary
  cases.

The resulting influence function should yield an asymptotic variance and a
studentized statistic. This is now the highest-value theoretical task.

### 2. Formal restricted-permutation theorem

The project already has the exact fixed-profile block reference

```text
{(1/n) sum_b [sum(A_b) sum(B_b) / n_b]} / {mean(A) mean(B)}.
```

The remaining theory should state a finite-sample conditional-validity theorem:
if the pairing is exchangeable within each declared block under the null, the
within-block randomisation p-value is super-uniform, with equality after
appropriate randomisation for ties. This should distinguish clearly between:

- global salience alignment, including between-block structure;
- additional salience alignment conditional on blocks.

### 3. Full cap-6 influence and estimand statement

The fixed-profile direct influence is bounded under cap 6, but a complete
result must include the fitted centre and MAD scale. The cap also prevents
marginal scale cancellation and introduces kinks at the clipping boundary.
This should be handled after the primary influence derivation, not in parallel
with another cap search.

### 4. Practical degeneracy threshold

Exact constants are already reported as undetermined. The remaining question
is what counts as scientifically negligible spread. No universal numerical
threshold can be inferred from c_delta alone; it should depend on measurement
resolution or a pre-specified domain tolerance. Short sensitivity tests can
validate a proposed rule once an application supplies that tolerance.

### 5. Severe unmatched diffuse masking

Cap 6 does not recover weak distributed salience under 5% independently placed
magnitude-20 contamination. A trimmed product, winsorised product, or sparse
scan could help, but each changes the aggregation target and multiple-testing
structure. This is a substantive next-definition decision and should wait
until the primary theory is stable.

## 2. Why Bootstrap Coverage Was Tested Now

General bootstrap consistency results exist for broad classes of M-estimators,
and robust Huber estimators have Bahadur and normal-approximation theory. These
results support bootstrap exploration but do not automatically establish
finite-sample coverage for this ratio of fitted salience moments:

- Cheng and Huang, *Bootstrap consistency for general semiparametric
  M-estimation*: <https://arxiv.org/abs/0906.1310>;
- Zhou, Bose, Fan, and Liu, *A New Perspective on Robust M-Estimation*:
  <https://arxiv.org/abs/1711.05381>;
- Efron and Narasimhan, *The automatic construction of bootstrap confidence
  intervals*: <https://pmc.ncbi.nlm.nih.gov/articles/PMC7958418/>.

The implementation therefore refits both marginal Huber profiles in every
paired bootstrap sample and compares percentile, basic, BCa, and
bootstrap-standard-error normal intervals.

## 3. Analytic-Truth Coverage Design

Let

```text
X = S_x exp(sigma U),
Y = S_y exp(sigma V),
```

where signs are independent and balanced, `(U,V)` are standard normal with
correlation `rho`, and `sigma=.45`. By symmetry, the population Huber locations
are zero. Marginal positive scale factors cancel from c_delta, giving the exact
population target

```text
C = exp(sigma^2 rho) = exp(.2025 rho).
```

The study used:

- `rho = 0, .2, .5`;
- `n = 20, 40, 80, 160`;
- 300 datasets per condition;
- 399 paired bootstrap samples per dataset;
- full profile refitting in every bootstrap sample;
- leave-one-pair-out jackknife acceleration for BCa.

All 3,600 dataset fits and their bootstrap replications completed successfully.
With 300 repetitions, the Monte Carlo standard error of a `.95` coverage rate
is approximately `.0126`.

## 4. Coverage Results

### Overall summaries

| Interval | Mean coverage | Minimum | Maximum | Mean width |
|---|---:|---:|---:|---:|
| Percentile | .9719 | .9233 | 1.0000 | .2370 |
| Basic | .9719 | .9167 | 1.0000 | .2370 |
| BCa | .9531 | .9100 | .9833 | .2448 |
| Normal, bootstrap SE | .9750 | .9300 | 1.0000 | .2341 |

The overall mean is misleading. At `n=20`, percentile and normal coverage was
`1.000` in every tested effect setting, with average width about `.51`: these
intervals are overconservative rather than accurately calibrated. At moderate
and large `n`, stronger effects produced undercoverage.

### Initial weak rows

At `rho=.5`:

| `n` | Percentile | Basic | BCa | Normal |
|---:|---:|---:|---:|---:|
| 80 | .9367 | .9167 | .9233 | .9300 |
| 160 | .9233 | .9200 | .9100 | .9300 |

The estimator bias was small, so the problem is not explained by a large mean
bias alone.

## 5. Independent Focused Coverage Replication

The `rho=.5`, `n=80,160` rows were repeated with an independent seed, 800
datasets per sample size, and 399 bootstrap samples.

| `n` | Percentile | Basic | BCa | Normal |
|---:|---:|---:|---:|---:|
| 80 | .9338 | .9362 | .9388 | .9388 |
| 160 | .9238 | .9188 | .9325 | .9212 |

At `n=160`, BCa was best but its Wilson interval was `[.9130,.9479]`, still
slightly below `.95`. The undercoverage is therefore reproducible and not just
one 300-repetition fluctuation.

### Reporting consequence

No tested ordinary bootstrap interval should yet be presented as a validated
95% confidence interval for the primary c_delta. Until studentized theory is
derived and validated:

- permutation p-values remain the formal inferential output;
- bootstrap intervals may be reported only as exploratory uncertainty ranges;
- the interval method and number of resamples must be stated;
- a manuscript should not use interval exclusion of the reference as a second
  formal significance rule.

## 6. Independent Replication of Recent Core Results

Four newest findings were repeated with an independent seed, 3,000 datasets
per condition, and 499 permutations:

| Condition | Rejection rate | Wilson interval |
|---|---:|---:|
| Block null, unrestricted | .6610 | [.6439,.6777] |
| Block null, within block | .0453 | [.0385,.0534] |
| Bernoulli `.50` null | .0240 | [.0191,.0301] |
| Clean local `rho=.2, n=80` | .4350 | [.4174,.4528] |
| 5% contaminated `rho=.7, n=320` | .0693 | [.0608,.0790] |

These reproduce the restricted-permutation correction, conservative binary
ties, clean local power, and severe unmatched-masking limitation.

## 7. Recommended Next Sequence

### Main next phase: theory

1. derive the primary functional's influence function;
2. derive its paired asymptotic variance;
3. construct a studentized statistic and interval;
4. prove finite-sample restricted-permutation validity conditional on fixed
   profiles and blocks;
5. validate interval coverage under the analytic model, heavy tails, skewness,
   and contamination.

### Short tests that remain useful

- measurement-resolution sensitivity once a substantive resolution is known;
- studentized interval coverage after the variance formula exists;
- restricted-design interval coverage;
- frozen-specification real or realistically structured examples;
- independent-seed checks for any newly introduced inference formula.

### Tests that are currently low priority

- another broad normal/t/tail null grid;
- further tuning of Huber `1.345`;
- another cap search around 6;
- multivariate expansion without a concrete multivariate application;
- combining primary and cap p-values into a new single rule.

Raw outputs:

- `results/huber_bootstrap_coverage_20260805.tsv`;
- `results/huber_bootstrap_focused_replication_20260805.tsv`;
- `results/inference_independent_replication_20260805.tsv`.
