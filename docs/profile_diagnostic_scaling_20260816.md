# Sample-size scaling of profile-regularity diagnostics

## Purpose

The previous pilot showed that fully recomputed studentization cannot repair a
Huber/MAD reference that selects between two tight modes.  This follow-up asks
whether that failure and three possible warnings are stable across sample
size.  It does **not** change the primary statistic or declare a formal gate.

For each margin, the study compares:

1. **Spacing:** the largest interior (central 80%) order-statistic spacing
   divided by the sample IQR.  The paired diagnostic is the worse margin.
2. **Central density:** the minimum Gaussian-KDE density on a 21-point grid
   from the 40th to the 60th percentile, multiplied by the IQR.  The paired
   diagnostic is the lower-density margin.  Density only at the empirical
   median was also recorded, but can miss a valley when an even-sample median
   lands near one mode.
3. **Resampled-reference stability:** for each margin, bootstrap the complete
   fixed-MAD Huber location and calculate

   \[
   B_n=\sqrt n\,\frac{\operatorname{IQR}_*\{T_H^*\}}
                         {\operatorname{IQR}(X)}.
   \]

   The pair-level value is the larger of the two margins.  The `sqrt(n)`
   factor removes the ordinary root-n contraction expected for a stable
   reference.

The path uses the true profile weak-null model

\[
X=S\exp(\sigma U),\qquad Y=S\exp(\sigma V),
\]

with common random sign `S` and independent standard-normal `U,V`.  Each cell
has 150 datasets, 99 permutations, and 79 bootstrap samples per margin.
Sample sizes are 40, 80, 160, and 320 for `sigma=.10,.20,.40,.80`, with an
additional `n=640` check for `.10,.20,.40`.  Four external null scenarios use
the same sample-size grid: independent `t_5`, independent strong skewness, a
regular-behaving `t_5` sign-link profile null, and affine near-constant
continuous margins.

## Sample-size results

| sigma | n | rejection | spacing/IQR | central density x IQR | scaled bootstrap spread |
| ---: | ---: | ---: | ---: | ---: | ---: |
| .10 | 40 | .887 | .856 | .243 | 2.53 |
| .10 | 80 | .753 | .827 | .156 | 3.41 |
| .10 | 160 | .767 | .801 | .085 | 3.86 |
| .10 | 320 | .647 | .779 | .038 | 4.37 |
| .10 | 640 | .553 | .760 | .013 | 5.22 |
| .20 | 40 | .393 | .732 | .273 | 1.77 |
| .20 | 80 | .147 | .684 | .194 | 1.75 |
| .20 | 160 | .107 | .645 | .126 | 1.49 |
| .20 | 320 | .040 | .612 | .072 | .97 |
| .20 | 640 | .013 | .583 | .035 | .84 |
| .40 | 40 | .093 | .531 | .359 | 1.05 |
| .40 | 80 | .013 | .462 | .303 | .93 |
| .40 | 160 | .033 | .426 | .251 | .89 |
| .40 | 320 | .020 | .368 | .202 | .84 |
| .40 | 640 | .033 | .335 | .151 | .84 |
| .80 | 40 | .047 | .338 | .391 | 1.18 |
| .80 | 80 | .053 | .235 | .404 | 1.14 |
| .80 | 160 | .033 | .174 | .421 | 1.15 |
| .80 | 320 | .067 | .138 | .431 | 1.09 |

The severe `.10` path does not recover merely by increasing sample size.  Its
rejection rate remains `.553` at `n=640`, while `B_n` increases rather than
stabilising.  The empirical median continues selecting a mode, the MAD can
collapse to the within-mode scale, and the fitted Huber reference remains
bootstrap-unstable.

The `.20` path behaves differently.  Rejection falls from `.393` at `n=40` to
`.040/.013` at `n=320/640`, and `B_n` falls below 1.  Nevertheless, spacing
remains above `.50` and central density tends toward zero.  Thus a structural
low-density warning is not equivalent to evidence that the finite-sample test
is currently invalid.  It can mark failure of a convenient influence-function
regularity condition even when the fitted statistic is empirically stable.

## External cross-validation

Across all 16 external cells, studentized rejection ranged from `.0267` to
`.0667`.  The scaled bootstrap-spread medians were remarkably stable:

- affine near-constant: `1.08-1.13`;
- independent `t_5`: `1.12-1.21`;
- strong skew: `1.36-1.39`;
- `t_5` sign-link profile null: `1.03-1.12`.

The largest external 90th percentile was `1.69`, from strong skewness at
`n=40`.  In contrast, every severe `.10` cell had median `B_n > 2.5`.

Spacing separated the tight radial path but did not support a fixed cutoff
across sample sizes.  Under strong skewness its median was `.540` and its 90th
percentile was `1.012` at `n=40`, but the median fell to `.131` at `n=320`.
Therefore the former `.50` rule over-warns small skewed samples and becomes
increasingly permissive as `n` grows.

Central valley density was more stable in the ordinary continuous controls:
external medians ranged from `.387` to `.474`, and the smallest external 10th
percentile was `.258`.  A value below about `.25` cleanly describes a sparse
centre in this grid.  However, it also warns on the `.20` path after the test
has recovered, so it should be interpreted as a structural/theorem warning,
not a direct finite-sample error predictor.

## Bootstrap Monte Carlo precision

A nested-prefix experiment compared 39, 79, and 199 bootstrap draws with a
399-draw reference over 100 datasets at `n=80` and `n=320`.

| B | correlation with B=399 | median absolute error range | agreement for exploratory `B_n > 2` |
| ---: | ---: | ---: | ---: |
| 39 | .382-.916 | .130-.379 | .80-1.00 |
| 79 | .533-.961 | .085-.319 | .90-1.00 |
| 199 | .784-.990 | .039-.149 | .95-1.00 |

Seventy-nine draws are adequate for this pilot's coarse comparison, but not
for reporting a precise continuous stability score.  Future confirmatory
tables should use at least 199 draws.  The value `B_n > 2` is only an
exploratory warning boundary: it had useful separation here, but has not been
externally calibrated as a formal test or gate.

## Current assessment

- **Best gross geometry diagnostic:** spacing, but its threshold must depend
  on sample size and distributional shape.
- **Best regularity-condition diagnostic:** central valley density, because it
  directly describes the low-density centre; it is conservative for actual
  finite-sample validity.
- **Best operational estimator-stability diagnostic:** root-n scaled bootstrap
  Huber-reference spread.  It tracks the persistent `.10` failure while
  remaining stable across the external controls.
- **Not recommended:** density only at the empirical median, or the bootstrap
  large-shift frequency based on a hard `0.25*IQR` event.  Both are too
  discontinuous and can have misleading within-cell rankings.

The evidence supports a two-tier report rather than a single automatic rule:
report central density/spacing as assumptions diagnostics and bootstrap spread
as fitted-reference stability.  Promoting `B_n > 2`, combining the diagnostics,
or refusing inference based on either tier is a key theoretical decision and
requires a new independent calibration grid first.

## Reproducible artifacts

- `scripts/run_profile_diagnostic_scaling_20260816.py`
- `scripts/run_bootstrap_reference_precision_20260816.py`
- `results/profile_diagnostic_scaling_path_pilot_20260816.tsv`
- `results/profile_diagnostic_external_cv_pilot_20260816.tsv`
- `results/bootstrap_reference_precision_pilot_20260816.tsv`
- `tests/test_profile_diagnostic_scaling_20260816.py`

