# Comparator Testing and Profile-Regularity Gate

Date: 2026-08-16

## Decision Summary

The closest horizontal analogues support the project's current use of fully
recomputed studentized permutation for a weak zero-correlation null. They do
not support replacing the profile statistic with a generic independence test.

A new continuous boundary path shows where studentization helps and where it
cannot help. It corrects most of the naive-permutation distortion once the
Huber/MAD reference becomes regular, but both procedures fail when the
population median/reference lies in a low-density gap. A scale-free largest
interior-spacing/IQR diagnostic is useful as a warning gate. The `.50` value
tested here is deliberately provisional: it identifies the failed path while
retaining nearly all regular heavy-tail cases, but it marks about 20% of the
strong-skew samples as undetermined.

## 1. Lessons from Comparable Parameters

### Pearson and concordance correlation

DiCiccio and Romano show that an ordinary permutation correlation test can be
invalid when the variables are dependent but uncorrelated, and that an
appropriately studentized permutation statistic is exact under independence
and asymptotically valid for the weaker zero-correlation null. Chung and
Romano give the broader exact-under-strong-null/asymptotically-robust-under-
parameter-null framework. Hutson and Yu obtain the same lesson for the
concordance correlation coefficient: the naive permutation test can inflate
Type-I error, while a statistic-specific studentizer repairs the regular
weak-null problem.

This is directly analogous to `c_delta_star`. Because its permutation ordering
equals the ordering of Pearson correlation between fitted salience profiles,
the profile influence function must be recomputed on every orbit member. A
fixed-profile or unstudentized reference is not enough for the weak null.

### Distance correlation and kernel tests

Distance correlation is zero if and only if the variables are independent
under its moment conditions. Its null is therefore stronger and scientifically
different from zero profile concordance. Under independence, its statistic is
a degenerate V-statistic with a non-Gaussian quadratic-form limit. Kernel
independence tests have the same strong-null degeneracy issue; wild bootstrap
methods are used for dependent processes when naive permutation breaks the
sampling dependence.

These methods suggest useful resampling principles, but they cannot be used as
drop-in p-values for the profile or Mantel weak-null components. In particular,
a distance-correlation rejection can coexist with a true profile null because
the observations may share sign or another dependence mechanism while their
salience radii remain uncorrelated.

### Mantel under structured sampling

Guillot and Rousset show that ordinary Mantel permutations can have severe
false-positive inflation when they destroy spatial autocorrelation. This
matches the project's building simulations: unrestricted or room-iid
permutations are not repaired by calling the statistic ``distance based.'' The
randomization group must preserve the building/spatial structure, or the
cluster functional and resampling law must be derived explicitly.

## 2. Continuous Nonregularity Path

The simulation used

```text
X = S exp(sigma U),
Y = S exp(sigma V),
```

where `S` is a common balanced random sign and `U,V` are independent standard
normal variables. The population Huber reference is zero by symmetry and the
two population radius profiles are independent, so the profile weak null is
true for every `sigma`. The common sign nevertheless makes `X` and `Y`
dependent, providing a genuine weak-null rather than an independence null.

Each row used `n=80`, 300 datasets, and 199 permutations.

| Radial log-SD | Mean fitted profile effect | Studentized reject | Naive reject | Median max-gap/IQR | Mean distance correlation |
|---:|---:|---:|---:|---:|---:|
| `.03` | `.9044` | `.9467` | `.9067` | `.9448` | `.9997` |
| `.10` | `.8432` | `.8400` | `.9033` | `.8262` | `.9961` |
| `.20` | `.3269` | `.2033` | `.5200` | `.6799` | `.9842` |
| `.40` | `.0795` | `.0300` | `.1567` | `.4640` | `.9386` |
| `.80` | `.0143` | `.0167` | `.0533` | `.2369` | `.7702` |

The comparison separates three facts.

1. Studentization is materially useful: at `.20` it reduces rejection from
   `.520` to `.203`, and at `.40` from `.157` to `.030`.
2. Studentization is not a cure for nonregular nuisance fitting. At `.03` and
   `.10`, the sample median/MAD/Huber reference selects between separated
   modes and the fitted profile no longer behaves like a regular expansion
   around the population reference.
3. Distance correlation remains large (`.770-.9997`) throughout even though
   the population profile correlation is zero. It is detecting dependence,
   not answering the salience-profile weak-null question.

## 3. Candidate Empirical Warning

For sorted observations, define

```text
G = largest adjacent spacing among the central 80% / IQR.
```

`G` is invariant to location and nonzero scale transformations. Large values
warn that an empirical margin contains a central low-density gap relative to
its ordinary spread. The pairwise diagnostic is `max(G_X,G_Y)`.

On the radial path, a provisional `.50` gate classified all `.03`, `.10`, and
`.20` samples as undetermined, retained `.760` of the `.40` samples, and
retained `.987` of the `.80` samples. Among retained `.40/.80` samples,
studentized rejection was `.0307/.0169`.

The same gate was then cross-validated on regular comparators:

| Comparator | Studentized reject | Naive reject | Median max-gap/IQR | `.50` pass rate | Studentized reject among pass |
|---|---:|---:|---:|---:|---:|
| Independent `t_5` | `.0433` | `.0500` | `.1998` | `.9967` | `.0435` |
| Independent strongly skew margins | `.0367` | `.0533` | `.3513` | `.7967` | `.0377` |
| Profile-null `t_5` sign link | `.0367` | `.0733` | `.3117` | `.9967` | `.0368` |
| Independent affine near-constant margins | `.0333` | `.0433` | `.1694` | `1.000` | `.0333` |

The last row is important: multiplying ordinary continuous variation by
`10^{-12}` does not create the failure. Correlation and the gap diagnostic are
scale invariant. The problematic case is low-density/separated reference
geometry, not a small raw measurement unit by itself.

## 4. Current Recommendation

1. Keep fully recomputed studentized permutation as the leading regular-iid
   local candidate. The naive profile permutation is rejected for weak-null
   use.
2. Add `max interior spacing / IQR` to routine simulation diagnostics. For
   now, use `.50` only as a conservative warning/sensitivity threshold, not a
   universal theorem or automatic data-analysis rule.
3. Report a failed gate as ``profile reference weakly identified under the
   declared regularity diagnostic.'' Do not reinterpret it as evidence for or
   against profile concordance.
4. Do not substitute distance correlation for the profile component. It is a
   valuable additional independence comparator when that broader question is
   scientifically intended.
5. Next test sample-size scaling and alternative gap/density diagnostics
   before fixing a reporting threshold. Building-level resampling remains a
   separate estimand problem.

## 5. Sources Used for Horizontal Validation

- DiCiccio, C. J., and Romano, J. P. (2017), ``Robust permutation tests for
  correlation and regression coefficients.''
  <https://doi.org/10.1080/01621459.2016.1202117>
- Chung, E., and Romano, J. P. (2013), ``Exact and asymptotically robust
  permutation tests.'' <https://doi.org/10.1214/13-AOS1090>
- Hutson, A. D., and Yu, H. (2021), ``A robust permutation test for the
  concordance correlation coefficient.'' <https://doi.org/10.1002/pst.2101>
- Szekely, G. J., Rizzo, M. L., and Bakirov, N. K. (2007), ``Measuring and
  testing dependence by correlation of distances.''
  <https://doi.org/10.1214/009053607000000505>
- Chwialkowski, K., Sejdinovic, D., and Gretton, A. (2014), ``A wild bootstrap
  for degenerate kernel tests.''
  <https://papers.neurips.cc/paper/5452-a-wild-bootstrap-for-degenerate-kernel-tests>
- Guillot, G., and Rousset, F. (2013), ``Dismantling the Mantel tests.''
  <https://doi.org/10.1111/2041-210X.12018>

## Reproducibility

- `scripts/run_profile_regularity_comparison_20260816.py`
- `tests/test_profile_regularity_comparison_20260816.py`
- `results/profile_regularity_comparison_pilot_20260816.tsv`
- `results/profile_regularity_gate_cv_pilot_20260816.tsv`
