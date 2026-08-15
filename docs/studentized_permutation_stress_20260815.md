# Studentized-Permutation Stress Test and Reporting Boundary

Date: 2026-08-15

## Purpose

The previous update identified fully recomputed studentized permutation as the
leading iid candidate for the profile and Mantel weak-null tests. This focused
pilot asks whether that conclusion survives heavy tails, strong skewness, and
partial nulls, and where the first clear regularity failure occurs.

Each row used `n=80`, 300 independently generated datasets, and 199
permutations per dataset. Every permutation recomputed all pairing-dependent
profile influence terms or the complete node-Hajek Mantel studentizer. The two
local p-values were adjusted by Holm. There were no numerical failures.

## Results

| Scenario | True local null(s) | Profile local reject | Mantel local reject | Holm true-null error |
|---|---|---:|---:|---:|
| Independent `t_5` | both | `.0333` | `.0367` | `.0200` |
| Independent `t_3` (infinite fourth moment) | both | `.0333` | `.0567` | `.0233` |
| Independent strongly skew margins | both | `.0400` | `.0667` | `.0300` |
| Profile-null, heavy-tail sign link | profile only | `.0533` | `.9267` | `.0533` |
| Profile-null, nearly constant radii | profile only | `.9533` | `1.0000` | `.9533` |
| Mantel-null, profile alternative | Mantel only | `.6500` | `.0333` | `.0300` |

The Wilson interval for the heavy-tail profile partial-null error was
`.0331-.0849`; the corresponding interval for the near-constant row was
`.9232-.9720`. Independent targeted reruns gave the same qualitative
separation: ordinary heavy-tail/skew/partial-null rows remained near the
nominal range, while the near-constant row failed overwhelmingly.

## Interpretation

### What improved

The iid candidate is not tied to Gaussian margins. Holm true-null error was
`.020-.030` in the three global-null stress rows and `.030` for the Mantel
partial null. The heavy-tail profile partial null was slightly above `.05`,
but its Monte Carlo interval includes `.05`. These results strengthen the
case for a pointwise iid candidate; they do not establish uniform validity.

### What failed

The nearly constant profile row deliberately approached a nonregular
boundary. Its two margins were symmetric, separated sign mixtures with
independent radii having standard deviation only `.03`. At the population
reference, the radius-profile correlation is zero. In a sample, however,
the median/MAD reference is unstable in the low-density gap and the
`O_p(n^{-1/2})` location error can dominate the tiny genuine radius variation.
Because the signs are shared, the two fitted reference errors move together,
creating a large apparent profile correlation (mean `.9123`). Studentization
cannot repair a statistic whose regular expansion is failing.

This row violates the intended regularity conditions: a locally unique
median/reference solution, adequate density near the median/MAD quantiles,
and profile variances bounded away from zero. It should therefore be treated
as a diagnostic boundary, not as evidence that all iid studentized
permutation inference is invalid.

## Reporting recommendation

1. Retain fully recomputed studentized permutation plus Holm as an **iid
   research candidate**, not a finished universal procedure.
2. Add a pre-analysis regularity screen for nontrivial profile variance and
   stable Huber/MAD fitting. If it fails, report the profile component as
   weakly identified or undetermined rather than force a p-value.
3. Keep the six-building problem separate. These iid results do not repair
   the previously observed cluster failures.
4. Ask Professor Hoorn to choose the building estimand before more cluster
   theory: an average of within-building functionals or one global functional
   containing cross-building dyads.

## Reproducibility

- `scripts/run_studentized_permutation_stress_20260814.py`
- `tests/test_studentized_permutation_stress_20260814.py`
- `results/studentized_permutation_stress_pilot_20260814.tsv`
