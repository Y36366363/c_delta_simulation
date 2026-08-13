# Studentized Permutation and Small-Building Validation

Date: 2026-08-14

## Decision Summary

Fully recomputed studentized permutation is the first local weak-null method
in this project to give broadly satisfactory pointwise calibration across both
global-null and partial-null iid models.  Holm applied to these local p-values
is therefore a promising iid component-discovery candidate.

It is **not** promoted for the current six-building application.  Treating
rooms as iid is severely anti-conservative, cluster-summed `t_5` inference
still fails under skew building scales, and a linearized building sign-flip is
invalid.  The iid candidate and the six-building problem must remain separate.

## 1. Fully Recomputed Studentized Permutation

For each random pairing \(\pi\), the method uses

\[
Z_P^\pi=\frac{\widehat\rho_P^\pi}{\widehat{SE}_P^\pi},
\qquad
Z_M^\pi=\frac{\widehat\rho_M^\pi}{\widehat{SE}_M^\pi}.
\]

The two-sided local p-value is the Monte Carlo rank

\[
p_j=\frac{1+\sum_{r=1}^R
I(|Z_{j,r}^\pi|\ge |Z_{j,obs}|)}{R+1}.
\]

### Profile recomputation

The marginal Huber/MAD fits and their marginal location influence values are
invariant to permutation of the second-margin labels, so they are fitted once.
For every orbit member the implementation nevertheless recomputes every
pairing-dependent part:

- the five joint profile moments;
- the correlation gradient;
- both Huber-location nuisance coefficients;
- the paired ordering of the second location influence;
- the complete paired influence variance;
- the studentized score.

This is a fully recomputed studentizer in the relevant mathematical sense; it
does not waste computation refitting permutation-invariant marginal
functionals.

### Mantel recomputation

Every orbit member recomputes:

- the paired distance-kernel five moments;
- the correlation gradient;
- all node-conditional kernel means;
- the first-order Hájek projection;
- the node-level influence variance;
- the studentized score.

No edge-independence approximation is used.

## 2. Iid Confirmatory Results

At `n=80`, 600 datasets per cell and 499 permutations gave:

| Scenario | Profile local reject | Mantel local reject | Holm true-null FWER | Profile Holm reject | Mantel Holm reject |
|---|---:|---:|---:|---:|---:|
| Signed-lognormal global null | `.0650` | `.0550` | `.0500` | `.0483` | `.0367` |
| Profile null, Mantel alternative | `.0483` | `.9317` | `.0417` | `.0417` | `.8583` |
| Calibrated-mixture global null | `.0367` | `.0383` | `.0300` | `.0217` | `.0233` |
| Mantel null, profile alternative | `.6433` | `.0467` | `.0367` | `.5233` | `.0367` |
| Both positive alternatives | `.9833` | `.9983` | n/a | `.9833` | `.9983` |

The signed-lognormal Holm FWER estimate `.0500` had a 95% Wilson interval
`.0352-.0705`.  The two independently constructed partial-null FWER values
were below `.05`.  Compared with the previous normal/jackknife p-values, the
new permutation reference removed the most serious distribution-dependent
inflation.

An `n=160` extension used 400 datasets and 199 permutations:

| Scenario | Profile local reject | Mantel local reject | Holm true-null FWER |
|---|---:|---:|---:|
| Signed-lognormal global null | `.0500` | `.0550` | `.0225` |
| Profile null, Mantel alternative | `.0325` | `.9925` | `.0325` |
| Calibrated-mixture global null | `.0525` | `.0700` | `.0350` |
| Mantel null, profile alternative | `.9275` | `.0275` | `.0225` |
| Both positive alternatives | `1.000` | `1.000` | n/a |

The individual `.070` Mantel row shows that local finite-sample behavior is
not uniformly exact.  Holm remained conservative in all tested `n=160` rows.
These simulations support pointwise candidacy, not a uniform validity theorem.

## 3. Multiplicity Consequence

Holm/closed-Bonferroni was previously blocked because its local p-values were
not adequately calibrated.  With fully recomputed studentized-permutation
p-values, the iid simulations now pass the first practical calibration gate.

Accordingly:

1. for a future genuinely iid application, predeclared profile and Mantel
   weak-null hypotheses plus Holm are a defensible **candidate**;
2. the candidate still needs heavy-tail, skew, near-degenerate, unequal-
   variance and one-sided/directional-error stress tests;
3. it does not inherit finite exactness under a weak zero-correlation null;
   the evidence is asymptotic and simulation-based;
4. the old global exchangeability omnibus remains a different inferential
   question and is not used as a gate.

## 4. Six-Building Validation

The building experiment used six independent buildings with 20 rooms each.
It compared:

- room-iid normal p-values;
- building-summed influence with a `t_5` reference;
- a linearized wild sign-flip over building scores;
- Holm adjustment of each pair of local p-values.

Confirmatory results used 2,000 datasets:

| Scenario | Room-iid raw FWER | Cluster-t Holm FWER | Sign-flip Holm FWER | Profile cluster-t | Mantel cluster-t |
|---|---:|---:|---:|---:|---:|
| Gaussian building null | `.2450` | `.0405` | `.1800` | `.0400` | `.0515` |
| Skew-scale building null | `.3685` | `.0735` | `.2360` | `.0910` | `.0875` |
| Correlated building alternative | n/a | both reject `.3975` | both reject `.6630` | power `.4640` | power `.5905` |

The skew-scale null mean effects were close to zero (`-.00070` profile and
`.01114` Mantel), so its failure cannot be dismissed as a strongly non-null
generator.  At `B=6`, the largest building contributed on average about
`.34-.35` of total absolute cluster score, leaving inference sensitive to one
building.

### Why the sign-flip failed

The linearized score sign-flip assumes a sufficiently symmetric cluster-score
law and treats estimated influence values as fixed.  Neither property is
guaranteed here.  It produced extreme FWER inflation even under the Gaussian
building model and is rejected.

### Building-count extension

A 300-dataset extension at `B=12,24` did not rescue the skew-scale model:

| Buildings | Gaussian cluster-t Holm | Skew-scale cluster-t Holm | Skew mean profile effect | Skew mean Mantel effect |
|---:|---:|---:|---:|---:|
| 12 | `.0467` | `.0933` | `-.00607` | `.00107` |
| 24 | `.0333` | `.0933` | `-.00154` | `.00118` |

This suggests more than a simple degrees-of-freedom problem.  Full global
Mantel geometry contains cross-building dyads, and a room-level node
projection summed by building may not adequately capture all finite-cluster
U-statistic structure under heterogeneous building scales.  A cluster-level
functional or multiway U-statistic derivation is needed before further
calibration claims.

## 5. Current Recommendation

### Can proceed

- Retain the full asymptotic local derivations.
- Retain fully recomputed studentized permutation as the leading iid weak-null
  candidate.
- Continue testing Holm/closed-Bonferroni only with those studentized local
  p-values.

### Cannot proceed yet

- Do not treat rooms as iid in building applications.
- Do not use the tested linearized building sign-flip.
- Do not promote building-summed `t_5` inference under heterogeneous scales.
- Do not claim formal component discovery for the current six-building case.

### Next narrow theory

1. Define whether the building estimand is an average of within-building
   profile/Mantel functionals or one global cross-building functional.
2. For the former, calculate one effect vector per building and use a small-
   sample multivariate procedure; cross-building dyads are then excluded by
   definition.
3. For the latter, derive the cluster-level projection of the order-two
   distance U-functional, including cross-building dyads, before resampling.
4. Stress-test iid studentized permutation under heavy tails, skewness,
   near-degeneracy, and directional alternatives before any promotion.

## Files

- `scripts/run_studentized_permutation_weak_null_20260814.py`
- `scripts/run_small_building_weak_null_20260814.py`
- `tests/test_studentized_permutation_weak_null_20260814.py`
- `tests/test_small_building_weak_null_20260814.py`
- `results/studentized_permutation_weak_null_confirmatory_20260814.tsv`
- `results/studentized_permutation_weak_null_n160_extension_20260814.tsv`
- `results/small_building_weak_null_confirmatory_20260814.tsv`
- `results/small_building_weak_null_count_extension_20260814.tsv`
