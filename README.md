# c_delta Simulation Pilot

This is a small first-stage project for studying the finite-sample behavior of the
correlation-of-divergency coefficient, `c_delta`.

## Updates 07/19/2026

- **Tail-factor comparison** — Added
  `scripts/run_tail_factor_comparison.py` to test a finer Student-t tail
  gradient across `l1/l2`, `n = 40, 80, 160`, `k = 1, 2, 3`, magnitudes
  `4, 6, 8`, and matched versus independent-null settings.
- **Tail-gradient results** — Added
  `results/tail_df_factor_grid_20260719.tsv`,
  `results/tail_df_background_noise_20260719.tsv`, and
  `results/tail_df_null_validation_20260719.tsv`; matched power decreases
  gradually as tails become heavier, while higher-replication null validation
  remains close to alpha `.05`.
- **Visual summaries** — Added tail-gradient power, null-validation, and
  background-divergence-noise plots in `figures/`.
- **Interpretation summary** — Added
  `docs/tail_factor_comparison_summary.md`; the main interpretation is that
  heavy-tailed backgrounds reduce power by increasing background divergence
  noise, not by clearly inflating type-I error.

## Updates 07/18/2026

- **Follow-up stable diagnostics** — Added
  `scripts/run_followup_stable_diagnostics.py` to combine high-replication
  independent-null checks, normal-background power curves, and a heavy-tail
  gradient study under the corrected reporting scale.
- **High-replication null checks** — Added
  `results/flagged_null_high_replication_20260718.tsv`; previously flagged
  independent-null rows mostly return to the nominal `.05` level with 1,200
  repetitions, suggesting the earlier `.08-.09` values were likely Monte Carlo
  fluctuations.
- **Power and tail-gradient outputs** — Added
  `results/power_curve_stable_20260718.tsv`,
  `results/heavy_tail_gradient_20260718.tsv`, and summary plots in
  `figures/`; power increases with subgroup size, while Student `t2` remains
  the clearest hard background.
- **Follow-up summary** — Added
  `docs/followup_stable_diagnostics_summary.md` to summarize the null
  calibration, power-curve thresholds, and heavy-tail interpretation.

## Updates 07/17/2026

- **Extended stable simulations** — Added
  `scripts/run_extended_stable_simulations.py` to test calibrated matched and
  independent-null behavior across target correlations `.25` and `.35`, `l2`
  and `l1`, normal, `t3`, `t2`, and lognormal backgrounds, and
  `n = 40, 80, 160`.
- **Extended simulation results** — Added
  `results/extended_stable_simulations_20260717.tsv` and
  `docs/extended_stable_simulation_summary.md`; normal and lognormal
  backgrounds often saturate at larger `n`, while Student `t2` remains the
  hardest background and several independent-null rows are marked for
  higher-replication follow-up.
- **Stable reporting table** — Added
  `scripts/build_stable_reporting_tables.py` to generate a report-friendly table
  that excludes old raw-scale columns and keeps permutation p-values, rejection
  rates, Wilson intervals, divergence-vector correlations, pairing-normalized
  values, and independent-null calibration summaries.
- **Report-ready metrics** — Added
  `results/stable_reporting_metrics_20260717.tsv` with 198 stable-metric rows
  combining lower-target calibration and sample-size sensitivity summaries.
- **Reporting guidelines** — Added `docs/stable_reporting_guidelines.md` to
  document which quantities should be emphasized after the `1 / n`
  normalization correction and which older raw-scale columns should be avoided.

## Updates 07/16/2026

- **Numerator normalization correction** — Updated the raw `c_delta`
  implementation to include the missing `1 / n` factor in the numerator, so
  raw values are now on the corrected scale and the permutation mean is `1`
  rather than `n`.
- **Revision note** — Added `docs/normalization_revision_note.md` to document
  the formula correction, expected effects on previous outputs, and the
  original-paper revision item.
- **Corrected-scale verification** — Added
  `results/normalization_feedback_checks_20260716.tsv`; exact enumeration now
  confirms the corrected permutation mean is `1.0`, while p-values and
  rejection-rate conclusions are unchanged by the constant scale correction.
- **Normalization follow-up checks** — Added
  `scripts/run_normalization_followup_checks.py`,
  `results/normalization_followup_checks_20260716.tsv`, and
  `docs/normalization_followup_summary.md`; the previously flagged
  `l1/lognormal/n=160/k=1` null setting returns to empirical size `0.053` with
  1,000 replications.
- **Sample-size sensitivity** — Added `scripts/run_sample_size_sensitivity.py`
  to test lower-target calibrated behavior across `n = 20, 40, 80, 160` for
  both `l2` and `l1`.
- **Large-n sensitivity results** — Added
  `results/sample_size_sensitivity_20260716.tsv` and
  `docs/sample_size_sensitivity_summary.md`; matched power often saturates by
  `n = 80` or `n = 160`, while independent-null behavior remains mostly close
  to alpha `.05`.
- **Lower-target L1 calibration** — Added
  `scripts/run_lower_target_l1_calibration.py` to repeat the non-ceiling
  `target_corr = 0.35` subgroup calibration with the absolute-difference (`l1`)
  divergence definition.
- **L1 calibration results** — Added
  `results/lower_target_l1_calibration_20260716.tsv` and
  `docs/lower_target_l1_calibration_summary.md`; the subgroup-size pattern
  broadly persists under `l1`, while heavy-tailed backgrounds remain flatter
  across `k`.

## Updates 07/15/2026

- **Calibrated subgroup simulation** — Added
  `calibrated_subgroup_simulation()` and
  `scripts/run_calibrated_subgroup_simulations.py` to compare `k = 1, 2, 3`
  after first matching approximate divergence-vector correlation.
- **Calibrated subgroup results** — Added
  `results/calibrated_subgroup_simulation_20260715.tsv` and
  `docs/calibrated_subgroup_summary.md`; normal backgrounds show a ceiling
  effect, while heavy-tailed backgrounds show that subgroup-size effects cannot
  be explained by permutation resolution alone.
- **Research tracker update** — Updated `docs/research_questions.md` to mark
  calibrated alternatives as started and to identify lower-target calibration as
  the next refinement.
- **Lower-target calibration** — Added
  `scripts/run_lower_target_calibration.py`,
  `results/lower_target_calibration_20260715.tsv`, and
  `docs/lower_target_calibration_summary.md`; target correlation `0.35` avoids
  the normal-background ceiling effect better than `0.55` or `0.65`.

## Updates 07/14/2026

- **L1/L2 variant comparison** — Added `variant_comparison_simulation()` and
  `scripts/run_variant_comparison.py` to compare squared-divergence (`l2`) and
  absolute-divergence (`l1`) versions under matched, negative-control, and
  independent-null settings.
- **Variant comparison results** — Added
  `results/variant_comparison_20260714.tsv` and
  `docs/variant_comparison_summary.md`; the matched sparse co-divergence signal
  remains strong under both `l2` and `l1`, while independent-null behavior stays
  close to alpha `.05`.
- **Research question tracker** — Added `docs/research_questions.md` to track
  Professor Hoorn's feedback items, including calibrated alternatives,
  overlap-layer interpretation, independent-null calibration, rank-based
  variants, and background-scale interpretation.

## Updates 07/13/2026

- **High-replication validation** — Added
  `scripts/run_high_replication_checks.py` for 1,000-replication independent-null
  size checks and 100,000-permutation overlap-layer diagnostics.
- **Monte Carlo uncertainty reporting** — Independent-null summaries now include
  rejection counts, Wilson intervals, and p-value quantiles.
- **High-replication result summary** — Added
  `docs/high_replication_checks_summary.md` and
  `results/high_replication_checks_20260713.tsv`.
- **Feedback response checks** — Added `scripts/run_feedback_checks.py` to test
  Professor Hoorn's latest points: the old unnormalized permutation mean issue,
  permutation statistics by extreme-index overlap layer, and independent-null
  calibration with chance overlap.
- **Response plan** — Added `docs/feedback_response_plan.md` to track which
  simulation claims need correction before the next report.
- **Feedback check results** — Added `docs/feedback_checks_summary.md` and
  `results/feedback_checks_20260713.tsv`; the historical check exposed the
  missing `1 / n` normalization, and overlap-layer diagnostics support treating
  `1 / choose(n, k)` as a layer size rather than a p-value.

## Updates 07/12/2026

- **Large-scale simulation architecture** — Optimized `permutation_test()` by
  computing divergence vectors once and permuting `D_y` directly, making larger
  sample-size simulations feasible.
- **Large-scale simulation script** — Added `scripts/run_large_scale_simulations.py`
  to test `n = 100, 250, 500` under normal, heavy-tailed, and log-normal
  backgrounds.
- **Large-scale result summary** — Added `docs/large_scale_simulation_summary.md`
  and `results/large_scale_simulation_20260712.tsv`; fixed-magnitude matched
  extremes remain detectable at large `n`, but heavy-tailed backgrounds require
  stronger subgroup structure.
- **Near-zero divergence boundary notation** — Added
  `docs/near_zero_divergence_notation.md` to document the preferred notation
  `\bar D_x \bar D_y \to 0^+` and the report wording "undetermined due to data
  limitations."
- **Boundary behavior simulation** — Added `scripts/run_near_zero_boundary.py`
  and `near_zero_divergence_simulation()` to show that `c_delta` remains stable
  for positive shrinking divergence scales and becomes undetermined only at the
  empirical zero-divergence boundary.
- **Update log order** — README updates are now listed newest first.

## Updates 07/11/2026

- **Multi-extreme all-star subgroup simulations** — Added
  `scripts/run_multi_extreme_simulations.py` to compare one, two, and three
  co-occurring extreme pairs across small and larger sample sizes.
- **Finite-sample permutation resolution note** — Added
  `docs/finite_sample_permutation_resolution.md` to summarize why a single
  dominant extreme pair can be limited by the permutation test's finite-sample
  resolution, especially when `n` is small.

## Updates 07/10/2026

- **Follow-up power and size simulations** — Added `scripts/run_followup_simulations.py`
  to map matched-extreme power curves across smaller sample sizes, test normal,
  heavy-tailed, and log-normal backgrounds, and check nominal size at alpha
  `.05` and `.01`.
- **Simulation results** — Added
  `results/followup_power_background_size_20260710.tsv` with the first follow-up
  tables for Professor Hoorn's suggested next steps.
- **Testing coverage** — Added a power-curve sanity test; the current test suite
  runs 8 unit tests.

## Goal

The first deliverable is a reproducible simulation baseline:

- implement `c_delta` and its divergence vectors;
- report raw `c_delta`, a sample-dependent pairing-normalized version, and the
  Pearson correlation between divergence vectors;
- run permutation tests for the null hypothesis that the pairing between `x`
  and `y` carries no divergence-structure signal;
- run paired bootstrap confidence intervals;
- compare behavior under normal, heavy-tailed, skewed, and contaminated data.

This keeps the first phase close to Professor Hoorn's suggestion that simulation
studies are most urgent, while leaving room for later h-star screening, robust
variants, weighting schemes, and machine-learning examples.

## Files

- `src/cdelta.py`: statistic, permutation test, bootstrap CI, and data generators.
- `scripts/run_pilot.py`: example simulation run.
- `scripts/run_outlier_influence.py`: matched/unmatched extreme-value pilot.
- `scripts/run_outlier_repeated.py`: repeated extreme-value alignment study.
- `scripts/run_followup_simulations.py`: power curves, non-normal backgrounds,
  and nominal size checks.
- `scripts/run_multi_extreme_simulations.py`: one-vs-subgroup extreme-value
  simulations for finite-sample permutation resolution.
- `scripts/run_near_zero_boundary.py`: near-zero divergence boundary behavior.
- `scripts/run_large_scale_simulations.py`: larger-n multi-extreme simulations
  using the optimized permutation test.
- `scripts/run_feedback_checks.py`: algebraic and null-calibration checks from
  Professor Hoorn's feedback.
- `scripts/run_high_replication_checks.py`: higher-replication validation with
  Wilson intervals and p-value quantiles.
- `scripts/run_variant_comparison.py`: L1/L2 divergence variant comparison.
- `scripts/run_calibrated_subgroup_simulations.py`: calibrated subgroup-size
  comparison.
- `scripts/run_lower_target_calibration.py`: lower-target calibrated subgroup
  comparison.
- `scripts/run_lower_target_l1_calibration.py`: lower-target L1 calibrated
  subgroup comparison.
- `scripts/run_sample_size_sensitivity.py`: sample-size sensitivity comparison
  for lower-target calibrated simulations.
- `scripts/run_normalization_followup_checks.py`: corrected-scale verification
  and flagged large-n null recheck.
- `scripts/build_stable_reporting_tables.py`: generate report-friendly stable
  metrics without raw-scale columns.
- `docs/finite_sample_permutation_resolution.md`: summary note on the
  small-sample permutation issue.
- `docs/near_zero_divergence_notation.md`: notation and reporting note for
  vanishing empirical divergence.
- `docs/large_scale_simulation_summary.md`: larger-n result interpretation.
- `docs/feedback_response_plan.md`: checklist for the July 13 feedback.
- `docs/feedback_checks_summary.md`: results of the July 13 feedback checks.
- `docs/high_replication_checks_summary.md`: higher-replication validation
  summary with Wilson intervals.
- `docs/variant_comparison_summary.md`: L1/L2 variant comparison summary.
- `docs/calibrated_subgroup_summary.md`: calibrated subgroup-size simulation
  summary.
- `docs/lower_target_calibration_summary.md`: lower-target calibrated subgroup
  summary.
- `docs/lower_target_l1_calibration_summary.md`: lower-target L1 calibrated
  subgroup summary.
- `docs/sample_size_sensitivity_summary.md`: sample-size sensitivity summary.
- `docs/normalization_revision_note.md`: formula correction note for the
  missing `1 / n` numerator factor.
- `docs/normalization_followup_summary.md`: corrected-scale follow-up summary.
- `docs/stable_reporting_guidelines.md`: guidance for report-stable quantities
  after the normalization correction.
- `docs/research_questions.md`: active research questions and next checks.
- `tests/test_cdelta.py`: minimal unit tests using Python's built-in `unittest`.

## Quick Start

From this folder:

```bash
python3 -m unittest discover -s tests
python3 scripts/run_pilot.py
python3 scripts/run_outlier_influence.py
python3 scripts/run_outlier_repeated.py
python3 scripts/run_followup_simulations.py
python3 scripts/run_multi_extreme_simulations.py
python3 scripts/run_near_zero_boundary.py
python3 scripts/run_large_scale_simulations.py
python3 scripts/run_feedback_checks.py
python3 scripts/run_high_replication_checks.py
python3 scripts/run_variant_comparison.py
python3 scripts/run_calibrated_subgroup_simulations.py
python3 scripts/run_lower_target_calibration.py
python3 scripts/run_lower_target_l1_calibration.py
python3 scripts/run_sample_size_sensitivity.py
python3 scripts/build_stable_reporting_tables.py
```

If using the Codex bundled runtime on this machine:

```bash
/Users/jialiangyao/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m unittest discover -s tests
/Users/jialiangyao/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/run_pilot.py
/Users/jialiangyao/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/run_outlier_influence.py
/Users/jialiangyao/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/run_outlier_repeated.py
/Users/jialiangyao/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/run_followup_simulations.py
/Users/jialiangyao/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/run_multi_extreme_simulations.py
/Users/jialiangyao/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/run_near_zero_boundary.py
/Users/jialiangyao/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/run_large_scale_simulations.py
/Users/jialiangyao/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/run_feedback_checks.py
/Users/jialiangyao/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/run_high_replication_checks.py
/Users/jialiangyao/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/run_variant_comparison.py
/Users/jialiangyao/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/run_calibrated_subgroup_simulations.py
/Users/jialiangyao/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/run_lower_target_calibration.py
/Users/jialiangyao/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/run_lower_target_l1_calibration.py
/Users/jialiangyao/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/run_sample_size_sensitivity.py
/Users/jialiangyao/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_stable_reporting_tables.py
```

## First Simulation Questions

1. How stable is raw `c_delta` as a function of sample size?
2. Does pairing-normalization reduce sample-specific scale effects?
3. How often does the permutation test reject under null, aligned, inverted,
   nonlinear, heavy-tailed, skewed, and contaminated settings?
4. How wide are bootstrap intervals across these settings?
5. Which scenarios separate `c_delta` from Pearson/Spearman-style association?
6. When does a single extreme value define a shared divergence structure rather
   than merely destabilizing the statistic?

## Next Extensions

- Add h-star based outlier assessment before robustifying `c_delta`.
- Treat zero-divergence cases as "undetermined due to data limitations" in
  reports rather than as computational errors.
- Compare matched, mismatched, and one-sided extreme observations to study when
  a single observation defines shared divergence structure.
- Map power curves across smaller sample sizes and test heavy-tailed or skewed
  background distributions.
- Study whether multiple co-occurring extreme observations reduce the
  small-sample permutation resolution problem observed for a single dominant
  matched pair.
- Add L1/Gini and rank-based variants.
- Add weighted pairwise distances after defining a principled weight function.
- Add comparisons with energy distance and MMD.
- Add machine-learning examples, such as comparing dispersion structures in
  embedding dimensions, model residuals, or representation clusters.
