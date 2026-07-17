# Stable Reporting Guidelines After the Normalization Correction

This note defines which simulation quantities should be emphasized in future
reports after adding the missing `1 / n` numerator factor to raw `c_delta`.

## Recommended Reporting Quantities

Future reports should emphasize:

- permutation p-values;
- rejection rates at pre-specified alpha levels;
- Wilson intervals for rejection rates;
- divergence-vector correlations;
- pairing-normalized values;
- independent-null calibration summaries;
- overlap-layer probabilities and tail shares.

These quantities are stable under the `1 / n` correction. The correction is a
positive constant scaling for each fixed sample size, so permutation orderings
and rejection decisions do not change.

## Quantities to De-emphasize

Raw `c_delta` should not be central in the next reports unless the table is
explicitly regenerated under the corrected formula. Old raw values were on the
unnormalized scale and should be divided by the corresponding sample size `n`
before being interpreted as corrected raw values.

Avoid using older `mean_raw` columns directly in text unless the corrected scale
is clearly stated.

## New Stable Reporting Table

The script

```text
scripts/build_stable_reporting_tables.py
```

creates:

```text
results/stable_reporting_metrics_20260717.tsv
```

This table removes raw-scale columns and keeps only reporting-stable quantities.
It combines:

- lower-target `L2` calibration at target correlation `0.35`;
- lower-target `L1` calibration at target correlation `0.35`;
- sample-size matched-power summaries;
- sample-size independent-null summaries.

## Current Interpretation

The normalization correction changes raw scale but not the main simulation
interpretation:

- lower-target calibration remains the preferred way to avoid ceiling effects;
- the subgroup-size pattern persists under both `L2` and `L1`, but depends on
  background distribution;
- sample-size increases matched power, often saturating by `n = 80` or `160`;
- independent-null behavior is mostly close to nominal size;
- the previously flagged `L1/lognormal/n=160/k=1` independent-null row was
  rechecked with 1,000 replications and returned empirical size `0.053`.

## Suggested Wording for Reports

```text
Because the normalization correction rescales raw c_delta by 1/n, I avoid
emphasizing old raw-scale values in the main report. The stable conclusions are
reported using permutation p-values, rejection rates, divergence-vector
correlations, pairing-normalized values, and independent-null calibration.
```
