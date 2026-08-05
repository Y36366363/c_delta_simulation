# c_delta Simulation Pilot

This is a small first-stage project for studying the finite-sample behavior of the
correlation-of-divergency coefficient, `c_delta`.

## Updates 08/05/2026

- **Full functional-delta derivation** - Derived the Huber-centre influence,
  including median/MAD scale coupling, then propagated the numerator and both
  denominator moments through one complete paired influence function.
- **Sandwich implementation** - Added plug-in asymptotic variance, normal and
  log-normal studentized intervals, and one-/two-sided Wald tests for the
  uncapped continuous-margin primary statistic.
- **Theory validation** - A closed-form symmetric lognormal benchmark matched
  a 250,000-draw variance check; 300,000-pair contamination derivatives also
  confirmed the nonzero MAD/centre nuisance path under skewness.
- **Finite-sample boundary** - Across the 1,200-repetition coverage grid, the
  full log-sandwich interval improved mean coverage from `.9198` for the
  fixed-profile approximation to `.9415`, but still covered only
  `.9108-.9258` for `rho=.5`. It is not yet a formal replacement for
  permutation inference.
- **New theory note** - See
  `docs/functional_delta_and_studentized_inference_20260805.md` and the
  corresponding `results/studentized_*` and
  `results/general_influence_validation_20260805.tsv` files.
- **Next-phase decision** - Broad calibration grids are no longer the main
  bottleneck. Prioritise the primary statistic's full influence function,
  asymptotic variance, studentized interval, and a formal restricted-
  permutation theorem.
- **Huber bootstrap implementation** - Added paired profile-refitting
  percentile, basic, BCa, and bootstrap-SE normal intervals, including
  leave-one-pair-out BCa acceleration and affine-invariance tests.
- **Analytic-truth coverage test** - Against
  `C=exp(.2025*rho)`, ordinary bootstrap intervals overcovered severely at
  `n=20` but undercovered stronger effects at `n=80-160`; overall averages hid
  this pattern.
- **Focused coverage replication** - With 800 independent datasets per row at
  `rho=.5`, coverage was only `.934-.939` at `n=80` and `.919-.933` at
  `n=160`. No tested bootstrap interval is ready as a formal 95% interval.
- **Independent core replication** - A new 3,000-repetition seed reproduced
  block correction (`.6610` unrestricted versus `.0453` within-block), binary
  conservatism (`.0240`), clean local power (`.4350`), and contaminated local
  masking (`.0693`).
- **Theory roadmap** - See
  `docs/next_theory_and_interval_validation_20260805.md` and the corresponding
  `results/huber_bootstrap_*` and
  `results/inference_independent_replication_20260805.tsv` files.
- **Design-respecting inference** - Added within-block profile permutation and
  an exact restricted-reference formula. Under a shared-scale conditional
  null, unrestricted rejection averaged `.44-.52`; within-block permutation
  restored `.047-.048` calibration while retaining high matched-signal power.
- **Restricted reference** - The random-pairing reference is exactly `1` only
  for unrestricted permutations. With blocks, between-block salience is held
  fixed and the exact conditional reference can differ substantially from `1`.
- **Discrete and degenerate validation** - Across Bernoulli, ordinal, Poisson,
  zero-inflated, quantized, and near-constant margins, null rejection was
  conservative-to-calibrated. An exactly constant margin is reported as
  undetermined; ties must not be confused with evidence of no raw association.
- **Local weak-signal map** - In a balanced lognormal diffuse family, Huber
  primary exceeded old L2 for weak-to-moderate latent salience correlations.
  This refines the diffuse limitation: performance depends on signal geometry,
  not merely whether the signal is sparse or distributed.
- **Severe diffuse masking** - Independent 5% magnitude-20 contamination left
  every method with low diffuse power even at `n=320`; cap 6 improved detection
  but did not solve the problem.
- **Inference-boundary documentation** - See
  `docs/inference_boundaries_and_local_power_20260805.md` and the corresponding
  `results/design_respecting_*`, `results/discrete_degeneracy_*`, and
  `results/local_salience_power_*` files.
- **Comprehensive old-versus-new benchmark** - Compared original L2/L1,
  Huber primary, and Huber cap 6 across 18 scenarios, four sample sizes,
  108,000 datasets, and common permutations. Exchangeable-null mean rejection
  remained `.0475-.0485` across methods.
- **Scope decision** - Continue development as a moderately broad test of
  positive paired salience under exchangeable or design-respecting pairing;
  do not market it as a general correlation, independence, causal, or
  full-distance-geometry statistic.
- **Comparative performance** - Huber-primary average core power exceeded old
  L2 from `n=40` onward and was substantially stronger for balanced bimodality
  and moderate-to-large-sample t2 signals, while preserving sparse matched
  power. Old L2 retained a genuine clean-diffuse advantage.
- **Expanded cap-6 cross-validation** - Across 180 additional conditions, cap
  6 kept worst clean-core loss at `.024` and delivered `.2319` mean masking
  gain over uncapped Huber. Cap 5.5 remained too close to the declared `.03`
  loss boundary; cap 6.5 was safer but less resistant to masking.
- **Expanded diffuse boundary** - Across 80 conditions, clean diffuse power
  loss sometimes persisted beyond `n=80`, especially with sign imbalance.
  Independent 5% magnitude-20 contamination erased most diffuse power for all
  uncapped methods; cap 6 recovered only part of it.
- **Final reporting structure** - Use uncapped Huber as the formal primary,
  cap 6 as a pre-specified leverage-limited sensitivity, and old L2 as a
  pre-specified comparator when diffuse alignment is scientifically central;
  do not use an unadjusted reject-if-any rule.
- **Comprehensive documentation** - See
  `docs/comprehensive_scope_and_cross_validation_20260805.md` and
  `results/comprehensive_scope_benchmark_20260805.tsv`,
  `results/cap6_expanded_cross_validation_20260805.tsv`, and
  `results/diffuse_boundary_expansion_20260805.tsv`.
- **Cap loss formalisation** - Defined a constrained loss that maximises
  unmatched-masking gain subject to null calibration and at most `.03`
  worst-case absolute power loss over matched, t2, diffuse, and bimodal core
  alternatives.
- **Cap-6 selection** - A fine `4.5-8` grid across three training seeds selected
  cap `6`; independent 5,000-repetition evaluation kept the largest core loss
  at `.0224` and greatly improved masking power.
- **Tolerance map** - Cap `6` corresponds to accepting roughly `.02-.03`
  worst-core-power loss; stricter tolerances select `6.5-7`, while looser ones
  select `4.5-5.5`. It is a declared robustness policy, not a universal constant.
- **Diffuse mechanism** - Increasing the Huber centre constant recovers
  small-sample diffuse power but transfers substantial loss to bimodal
  salience. An exploratory tail-triggered rule did not resolve this conflict.
- **Definition recommendation** - Retain Huber centre constant `1.345` for the
  primary score-all profile, accept and disclose the small-sample diffuse
  limitation, and use cap `6` only as a pre-specified bounded sensitivity
  profile.
- **Literature cross-validation** - Connected the decision to Huber
  contamination/efficiency theory, adaptive robustification, robust distance
  covariance influence analysis, h-star, and the archived c_delta target.
- **Documentation** - See
  `docs/cap_loss_and_diffuse_decision_20260805.md` and the corresponding
  `results/cap_loss_*`, `results/center_*`, and
  `results/joint_candidate_validation_20260805.tsv` files.

## Updates 08/04/2026

- **Robust-definition study** - Formalised centre-radius, fit-without/score-all,
  bounded-influence, and h-star-inspired salience profiles after the 08/03
  discussion.
- **First validation** - Across six 500-repetition scenarios, the provisional
  IQR-fit/all-score profile preserved matched-outlier, diffuse-profile, and
  heavy-tail paired-signal power, but did not bound final outlier leverage.
- **Robustness tradeoff** - A three-robust-scale cap improved power under huge
  unmatched masking (`.272` versus original L2 `.052`) but reduced genuine
  matched-outlier power (`.314` versus `1.000`).
- **h-star bridge** - A leave-one-out h-star-style profile was effective for a
  single matched candidate but suffered multiple-outlier denominator masking.
- **Recommendation** - Treat robust-reference/all-observation scoring as the
  main redefinition candidate and bounded scoring as a separate sensitivity
  estimand; do not use ordinary k-means as a one-centre robustness device.
- **Expanded robustness grid** - Added trimmed-mean and Huber centres,
  independent contamination nulls, t2, skewed, bimodal, masking, sample-size,
  and parameter-sensitivity checks. Huber reference scoring was the strongest
  uncapped candidate in heavy-tail and bimodal settings.
- **Bounded sensitivity** - A prospective `6 x MAD` cap preserved nearly all
  matched-signal power while substantially improving unmatched-masking power;
  it remains a separate estimand, not a post-hoc universal constant.
- **Stage-1 initial pilot** - Replayed the original six pilot scenarios at
  `n=60`; Huber robust-reference preserved aligned and contaminated-aligned
  power (`1.000`), gave zero upper-tail rejection for inverted salience, and
  kept heavy-tail/skew null rejection near `.05`.
- **Stage-2 structural theory** - Derived the population target, affine
  invariance, exact permutation reference, and the distinction between robust
  centre fitting and bounded final influence. Tested robust L2-like radial
  floors to separate centre robustness from the old variance-floor geometry.
- **High-replication validation** - Completed 864,000 datasets across four
  sample sizes and nine scenarios with 999 permutations per method. Huber
  radius null rejection stayed in `.0462-.0509`, preserved sparse matched
  power, and improved t2 and bimodal power for moderate-to-large `n`.
- **Independent-seed audit** - The 3,000- and 24,000-repetition runs differed
  by only `.00323` on average across 180 matched rows and reproduced the same
  main directional conclusions.
- **Definition refinement** - L2-like radial floors added no consistent value;
  retain the pure Huber radius as the primary candidate and cap `6` as a
  separate masking-resistance sensitivity estimand.
- **Cap pre-calibration pilot** - A prospective training rule selected cap `5`
  rather than cap `6`; independent evaluation preserved calibration and
  improved masking power but exposed a small-sample power cost. Treat the
  calibration protocol, not a universal cap constant, as the supported result.
- **Multivariate feasibility** - Spatial-median radius was rotation invariant
  and promising across dimensions `1, 2, 5, 10`; coordinatewise Huber was not
  rotation invariant and should not be the general multivariate default.
- **Diffuse tradeoff map** - The robust-radius power loss was material in the
  constructed diffuse family for roughly `n <= 40` and small by `n = 60-80`.
- **Dual-reporting pilot** - An unadjusted union of primary and bounded p-values
  lacked level-.05 protection, while Bonferroni was conservative. Retain one
  primary inferential rule and report the bounded profile as sensitivity.
- **Documentation** - See `docs/robust_cdelta_redefinition_20260804.md` and
  `docs/robust_definition_stage2_summary_20260804.md`,
  `results/robust_cdelta_grid_20260804.tsv`,
  `results/robust_cdelta_null_high_rep_20260804.tsv`, and
  `results/robust_parameter_sensitivity_20260804.tsv`, plus
  `results/robust_definition_highrep_validation_20260804.tsv`. Routine
  extension results are summarised in
  `docs/robust_routine_extensions_summary_20260804.md`.

## Updates 08/01/2026

- **Teacher-claim overlap validation** — Added a 27,000-dataset factorial
  simulation holding standout number and magnitude fixed while varying only
  paired-index overlap across L1/L2, three sample sizes, and three backgrounds.
- **Overlap gradient** — Average rejection rose from about `.02` at disjoint
  standouts to `.81-.84` at full overlap, directly supporting the paired-
  standout interpretation.
- **High-replication null follow-up** — A preliminary L1-normal flag disappeared
  at 5,000 repetitions (`.0466`, Wilson interval `[.0411, .0528]`).
- **Binary-overlap theory bridge** — Derived
  `r = (n m - k^2) / (k (n - k))` for equal-size binary standout sets and
  compared it with continuous divergence across 24,000 additional datasets.
- **Meeting preparation** — Added `docs/meeting_discussion_20260803.md` with
  concise findings, qualifications, and questions for Professor Hoorn.
- **High-replication overlap cross-validation** — Repeated the magnitude-8
  overlap gradient with 1,000 repetitions per condition; all L1/L2 and
  normal/`t3`/`t2` curves remained monotone.
- **Random-set null** — Added 18,000 simulations in which both datasets contain
  four strong standouts with independently selected indices; rejection stayed
  between `.0377` and `.0493` while observed overlap followed its exact
  hypergeometric distribution.
- **Next-step roadmap** — Added `docs/next_steps_before_and_after_meeting.md`
  and implemented the exact chance-overlap PMF with unit tests.
- **Independent accuracy audit** — Recomputed all meeting-result tables,
  matched the fast and core permutation implementations in 120 checks, and
  clarified that strict `p < .05` gives effective levels `.045`, `.0475`, and
  `.048` for 199, 399, and 499 permutations.
- **Audited meeting figures** — Added a reproducible figure builder using the
  1,000-repetition overlap results and the exact random-set overlap reference.

## Updates 07/31/2026

- **Paired-salience reframing** — Added the exact one-dimensional L2 identity
  showing that divergence ranks observations by absolute deviation from their
  sample mean, so the current statistic aligns observation-level salience
  profiles rather than general full internal structures.
- **Salience validation** — Added
  `scripts/run_paired_salience_validation.py` and
  `results/paired_salience_*_20260731.tsv` to compare diffuse alignment,
  sparse alignment, partial alignment, reverse alignment, and calibrated null
  scenarios under L1 and L2.
- **Reframing summary** — Added `docs/paired_salience_reframing.md`; diffuse
  salience alignment is detectable even without strong outliers, while full
  pairwise-distance correlation can remain near zero.
- **Literature positioning** — Distinguished the current row-summary target
  from distance correlation, HSIC, energy distance, MMD, and Mantel-type
  full-distance-matrix correlation.
- **Exact information-loss example** — Added a construction with identical L2
  divergence vectors (`r = 1`) but almost unrelated full distance matrices
  (`r = -0.0402`), proving that row aggregation is many-to-one.
- **Directional alternatives** — Extended `permutation_test()` with
  `greater`, `less`, and `two-sided` alternatives and retained `greater` as the
  default. Focused null rejection rates remained between `0.0325` and `0.0475`.
- **Alternative validation** — Added
  `scripts/run_row_aggregation_and_alternatives.py`, two result tables, and
  `docs/row_aggregation_and_alternatives_summary.md`.

## Key Findings Index

The cumulative record of mathematical identities, stable simulation findings,
representative numerical results, reporting cautions, and open questions is
maintained in `docs/key_findings.md`. Update this file after each material
simulation or theoretical revision.

## Updates 07/30/2026

- **Cumulative findings record** — Added `docs/key_findings.md` as the central
  retrieval document for stable conclusions, representative values, reporting
  rules, open questions, and the reverse-chronological research log.
- **Direct background-masking diagnostics** — Added
  `scripts/run_background_masking_diagnostics.py` to locate large background
  divergence scores, measure their cross-vector index overlap, and compare
  planted paired products with background and random-pairing products.
- **Masking results** — Added
  `results/background_masking_diagnostics_20260730.tsv` and
  `results/background_masking_summary_20260730.tsv`; heavy-tail background
  extremes usually occur at unmatched indices, and a background-product
  masking event is substantially more common when the permutation test does
  not reject.
- **Mechanism summary** — Added
  `docs/background_masking_diagnostics_summary.md`; common-MAD scaling restores
  part of the planted product advantage, but unmatched background leverage
  remains under the heaviest tails.
- **Algebraic identity validation** — Added the exact decomposition
  `c_delta = 1 + corr(D_x, D_y) CV(D_x) CV(D_y)` and tests confirming that
  corrected `c_delta` and divergence-vector Pearson correlation rank
  permutations identically.
- **Teacher-feedback scale checks** — Added
  `scripts/run_teacher_feedback_validation.py` to compare the earlier common
  scale-parameter tail design with common-MAD and common-variance designs.
- **Distribution-level results** — Retained 12,000 matched and
  independent-null statistic pairs and added separation, power, and identity
  summaries in `results/teacher_feedback_*_20260730.tsv`.
- **Interpretation summary** — Added
  `docs/teacher_feedback_validation_summary.md`; common-MAD scaling attenuates
  but does not remove heavy-tail power loss, while matched-null separation
  narrows as tails become heavier.

## Updates 07/29/2026

- **Fixed-k versus fixed-proportion tail validation** — Added
  `scripts/run_fixed_fraction_tail_validation.py` to compare fixed `k = 2`
  with fixed `k / n = .05` across `l1/l2`, seven tail settings, and
  `n = 40, 80, 160`.
- **Sample-size design results** — Added
  `results/fixed_fraction_tail_validation_20260729.tsv` and
  `results/fixed_fraction_tail_contrasts_20260729.tsv`; fixed-`k` power
  declines as the subgroup becomes sparser under heavy tails, while
  fixed-proportion power is generally preserved or increases.
- **Interpretation update** — Added
  `docs/fixed_fraction_tail_validation_summary.md` and updated the research
  tracker; larger `n` is not inherently harmful, and future sample-size
  studies should distinguish fixed subgroup size from fixed subgroup
  proportion.

## Updates 07/26/2026

- **Broad signal/noise validation** — Added
  `scripts/run_signal_noise_broad_validation.py` to test whether signal/noise
  diagnostics explain power across 486 matched settings covering `l1/l2`,
  tail settings, `n = 40, 80, 160`, `k = 1, 2, 3`, and magnitudes `4, 6, 8`.
- **Broad validation results** — Added
  `results/signal_noise_broad_validation_20260726.tsv` and
  `results/signal_noise_broad_correlations_20260726.tsv`; the strongest metric,
  `signal_over_topk_noise`, has overall Spearman correlation `0.9399` with
  rejection rate and remains strongly positive across kinds, sample sizes,
  subgroup sizes, and magnitudes.
- **Broad validation summary** — Added
  `docs/signal_noise_broad_validation_summary.md`; background divergence noise
  is consistently negatively associated with power, supporting the mechanism
  that heavy tails reduce signal-to-background-divergence-noise contrast.
- **Signal-to-noise diagnostics** — Added
  `scripts/run_signal_noise_diagnostics.py` to quantify the proposed mechanism
  behind heavy-tail power loss using matched subgroup prominence and
  background-only divergence noise.
- **Signal/noise results** — Added
  `results/signal_noise_diagnostics_20260726.tsv` and
  `results/signal_noise_metric_correlations_20260726.tsv`; signal-over-noise
  metrics correlate strongly with matched rejection rates, while background
  max-to-mean divergence is negatively associated with power.
- **Mechanism summary** — Added
  `docs/signal_noise_diagnostics_summary.md`; the current interpretation is
  that heavy-tailed backgrounds reduce power by lowering the matched
  subgroup's signal-to-background-divergence-noise contrast.

## Updates 07/19/2026

- **Tail cross-validation** — Added
  `scripts/run_tail_cross_validation.py` with higher-replication checks for the
  central tail-power slice, independent-null tail-size validation, and a
  fixed-`k` versus fixed-proportion sample-size comparison.
- **Confidence summary** — Added
  `docs/tail_cross_validation_confidence_summary.md`; the heavy-tail power
  decline is now stable under independent seeds, while null rejection rates
  remain close to alpha `.05`.
- **Cross-validation results** — Added
  `results/tail_power_cross_validation_20260719.tsv`,
  `results/tail_null_cross_validation_20260719.tsv`, and
  `results/fixed_k_vs_fixed_proportion_20260719.tsv`.
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
- `scripts/run_robust_center_validation.py`: first centre/cap/h-star robust
  profile comparison.
- `scripts/run_robust_cdelta_grid.py`: contamination, tail, skew, bimodal, and
  sample-size validation for robust-reference profiles.
- `scripts/run_robust_parameter_sensitivity.py`: Huber, trimming, hard-cap,
  and soft-cap sensitivity grid.
- `scripts/run_robust_initial_pilot.py`: stage-1 replay of the original pilot
  scenarios for the new profile definitions.
- `scripts/run_studentized_inference_validation.py`: oracle, direct-profile,
  full-sandwich, and jackknife studentized coverage comparison.
- `scripts/run_studentized_focused_replication.py`: independent strong-effect
  studentized interval replication.
- `scripts/run_general_influence_validation.py`: point-contamination finite-
  difference validation of the complete influence function.
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
- `docs/functional_delta_and_studentized_inference_20260805.md`: full Huber
  functional-delta derivation, sandwich variance, and interval validation.
- `docs/research_questions.md`: active research questions and next checks.
- `tests/test_cdelta.py`: minimal unit tests using Python's built-in `unittest`.

## Quick Start

From this folder:

```bash
python3 -m unittest discover -s tests
python3 scripts/run_pilot.py
python3 scripts/run_outlier_influence.py
python3 scripts/run_outlier_repeated.py
python3 scripts/run_robust_center_validation.py
python3 scripts/run_robust_cdelta_grid.py
python3 scripts/run_robust_parameter_sensitivity.py
python3 scripts/run_robust_initial_pilot.py
python3 scripts/run_studentized_inference_validation.py
python3 scripts/run_general_influence_validation.py
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
