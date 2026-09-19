# Retained-evidence reproduction protocol — 2026-09-18

Recorded before generating reproduction outcomes. Scope is the September 15
single-file author manuscript's retained tables, not the entire historical grid.
No new simulation cells, methods, seeds, repetitions or permutation counts.

- Six August 23 regular-null cells: 1,000 datasets each, original sequential
  cell RNG streams, all stored aggregate fields.
- S2.1: 24 August 17 bridge-family cells, 150 datasets, 99 permutations and
  199 bootstrap reference fits per margin per dataset.
- S2.2: four original matched-index cells, 500 datasets with the same settings.
  Their first 150 datasets overlap the corresponding pilot cells: do not call
  these independent confirmations or add the two sample sizes together.
- S2.3: six August 25 prospective-family cells, 200 datasets, 99 permutations,
  no bootstrap diagnostics. Refit the old-family predictor from the reproduced
  training summaries and checked population Jacobian indices.
- Recalculate the retained population indices, September 7 quadrature orders
  24/48/72 and contamination checks, September 8 stored-draw tail diagnostics
  and 18 root replays. Reconcile every retained LaTeX table separately.

Use a temporary source/results snapshot and the existing isolated environment.
Replace the snapshot core with the archived historical source; hash all copied
Python sources and original result inputs. Parallelize independent cells only;
preserve each original within-cell RNG call order, including bootstrap fits.
Read original outputs for comparison; never overwrite frozen files. Reuse the
September 16 comparator at scaled absolute tolerance 1e-10; exact count, seed,
decision and rejection-rate comparisons are additionally required. NaN status,
row identities and columns must agree. Record any discrepancy before deciding
whether a tolerance or scientific change is justified. No silent hash refresh.

The September 16 completed two-study reproduction is complementary evidence,
not rerun here. Historical aggregate-only panels cannot establish equality of
every per-dataset decision because the original decisions were not all stored.
Successful reproduction is neither independent code reimplementation nor
independent mathematical review, and does not establish finite-sample calibration.
