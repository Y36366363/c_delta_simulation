# Research Questions and Next Checks

This note keeps the simulation work aligned with Professor Hoorn's latest
feedback and separates mathematical claims from empirical checks.

## Active Questions

### Update after the 2026-08-13 unequal-building and covariate study

- Unequal building size alone did not systematically damage power at fixed
  total `n`; the important complication is informative size, where room count
  co-varies with building covariates, nuisance scale, and signal strength.
- Building-equal, square-root-room, and room-equal aggregation define distinct
  targets. Adaptive results were materially sensitive to this choice under
  severe imbalance.
- Raw and orbit-standardized LOO learners failed the construct-direction check:
  they did not give relatively more profile weight to radial alternatives or
  more Mantel weight to dyadic alternatives. Temperature `0-.25` was best,
  showing little support for actual weight learning.
- A permutation-standardized maximum is now the leading omnibus candidate. It
  stayed close to the stronger component and calibrated under conditional
  permutation, but it has no single effect-size interpretation.
- Do not promote learned adaptive mixture to primary. Whether standardized max
  becomes a primary test or a sensitivity test is now an explicit scientific
  decision about “any internal-structure concordance” versus a named estimand.

### Update after the 2026-08-13 omnibus interpretability follow-up

- Standardized max can be accompanied by simultaneous maxT-adjusted profile
  and Mantel evidence; its p-value is the minimum adjusted component value.
- In explicit target-separation alternatives, the standardized winner selected
  profile `.735` under node salience and Mantel `.998` under dyadic geometry.
  Most rejecting datasets still supported both components, correctly exposing
  construct overlap rather than forcing an exclusive mechanism label.
- Across 18 unequal-building alternative cells, mean 999-permutation regret
  was `.017` and worst observed regret `.060`. Thus robustness has a finite but
  bounded empirical power cost in the current grid.
- 499 permutations reproduced 999-permutation decisions `.984`, winners `.988`,
  and adjusted attribution `.968`; use 999 for final weak-signal claims.
- The component evidence has weak/global-null family-wise validity. Strong
  component discovery needs subset pivotality or partial-null validation and
  remains the main theoretical obstacle to promoting the omnibus.

### Update after the 2026-08-12 application-mechanism study

- `Node strength` is now decomposed into marginal sign prevalence, directional
  sign agreement, shared radial heterogeneity, and block-centre displacement.
  The joint Bernoulli generator varies prevalence and agreement independently.
  Sign agreement helped Mantel more, so it should not be equated with unsigned
  node salience.
- Correlated building centres are a block-level nuisance for within-building
  inference. They may reduce power, but the conditional test does not count
  their fixed between-building agreement as within-building evidence.
- A continuous leave-one-building-out profile weight was calibrated only as a
  method-preference diagnostic. It is not an estimate of latent node/dyad
  mixture weight and is not ready to replace predeclared estimands.
- The within-building finite-sample theorem is now explicit. Any adaptive
  learner is allowed if the complete statistic, including weight refitting, is
  reapplied to every permitted permutation. Frozen observed-data weights need
  a group-invariance, external-training, or held-out-test justification.

### Update after the 2026-08-11 skew-mechanism audit

- The `.131/.043` crossover shift is not a general marginal-skewness result.
  A 2x2 decomposition attributes an average `-.277` shift to node positive-
  sign prevalence, versus `+.009` for dyadic lognormal skew.
- A balanced-sign node margin with larger absolute skewness moved crossover
  only `-.035` or `+.022`, depending on the dyadic margin. The prevalence
  mechanism changed sign agreement and node geometry, not just the third
  marginal moment.
- Huber-location and MAD indirect derivatives remain validated. The revision
  concerns power attribution, not the functional calculation.
- Further generic skew grids are low priority unless an application supplies a
  realistic sign/magnitude model.

### Update after the 2026-08-10 mixed-path derivative study

- The interior mixture tangent and generic correlation derivative are now
  explicit. Pathwise and `.001` numerical effect derivatives agreed within
  `.000166` across four profile/Mantel configurations.
- At the tested crossover points, both effect and power curves generally
  decline as dyadic variance weight increases; profile declines faster. Thus
  crossover reflects loss of node-profile advantage rather than requiring a
  monotone increase in Mantel power.
- Independent power seeds and `.025/.05` half-widths preserved the direction.
  The weak-both difference slope remained unresolved, consistent with its
  broad crossover uncertainty band.
- Skewed mixed paths have now restored the Huber-location/MAD nuisance
  derivative. Complete-refit validation shows that total Huber movement can
  reverse an individual profile slope; the MAD-only indirect term is smaller
  but reproducibly nonzero.
- The two composite generators have power crossovers `.131` and `.043`.
  The 08/11 audit shows that the early shift is mainly sign prevalence rather
  than a monotone skewness effect. Relative profile advantage still declines
  within those paths, while individual slopes can have different signs.

### Update after the 2026-08-09 strength-surface study

- The initial nine-cell result was not sufficient to reject a useful signal-
  ratio approximation. Its raw-ratio model predicted seven new intermediate-
  node/lower-dyad cells with crossover RMSE `.0247`; the 16-cell ratio model
  reached logit-crossover R-squared `.803`.
- Separate Fisher-z strengths still fit better (`R-squared=.903`), with node
  and dyad coefficients `+.785` and `-.360`. Node is the larger surface
  direction, but the lower-dyad extension shows a meaningful monotone effect.
- Pure-path theory explains the asymmetry: under a Gaussian dyadic path,
  profile and Mantel population correlations are equal, whereas sign-rewired
  node salience creates a profile-minus-Mantel gap that grows with node
  strength.
- No observed-data test-selection threshold is supported. Mixed scientific
  questions should pre-specify and separately report profile and dyadic
  estimands when both are substantively relevant.

### Update after the 2026-08-08 target-separation study

- A common four-building simulation now separates node-salience and dyadic-
  geometry alternatives. Huber profile methods are more sensitive to the
  former; Mantel is more sensitive to the latter. This supports estimand-first
  method choice rather than a universal comparison.
- The exact permutation equivalence of Huber `c_delta_star` and Pearson robust-
  profile correlation also holds under within-building restrictions.
- The unresolved definition question is now narrower: whether the
  `CV_X CV_Y` weighting is scientifically part of robust salience concordance.
  At fixed Pearson concordance `.30`, it changes the population coefficient
  from `1.019` to `3.546` and produces slow high-CV convergence.
- A continuous variance mixture locates the Huber-versus-Mantel transition at
  about `.216` in the current generator, with a reproducible unresolved band
  `.20-.25`. This is a diagnostic boundary, not a universal decision rule.

| Question | Why it matters | Current status | Next check |
| --- | --- | --- | --- |
| What is the right notation for the zero-divergence boundary? | The statistic should not be described as a computational error when empirical divergence vanishes. | Use `\bar D_x \bar D_y \to 0^+` and report "undetermined due to data limitations" at the empirical boundary. | Keep notation consistent in the next report. |
| Is the subgroup-size effect only a permutation-resolution effect? | Larger `k` increases both signal strength and changes the permutation overlap layers. | Added lower-target calibrated alternatives at target correlations `0.35`, `0.55`, and `0.65`; then repeated the non-ceiling `0.35` setting under `l1`. The pattern broadly persists under `l1`, while t3 remains flatter across `k`. | Add a rank-based variant or compare exact overlap layers at target `0.35`. |
| Is `1 / choose(n, k)` a p-value? | Professor Hoorn clarified that it is a layer probability, not the permutation p-value. | Overlap-layer diagnostics now report overlap count, layer probability, and share above the observed statistic. | Extend the layer diagnostic across magnitudes and backgrounds. |
| Is the mismatched condition a valid null? | A deliberately disjoint condition is a negative control, not a genuine null distribution. | Independent-null simulation now samples extreme indices independently and allows chance overlap. | Use independent-null results for Type-I statements; use disjoint mismatch only as a negative control. |
| Does raw `c_delta` have a zero-centered permutation null? | It does not; after adding the missing `1 / n` numerator factor, the mean raw statistic across permutations equals `1`. | Exact enumeration confirms the corrected permutation mean equals `1`; the previous value `n` reflected the unnormalized numerator. | Update formulae, raw-scale interpretations, and the original-paper revision note. |
| Are the findings specific to squared divergence? | Squared divergence can amplify sparse extremes. | L1/L2 comparison shows the qualitative matched-vs-null pattern survives under `l1`. | Add a rank-based divergence-vector comparison. |
| Do heavy-tailed or skewed backgrounds change detectability? | Backgrounds with natural extremes may make sparse structural signals harder to separate. | `t3` weakens power relative to normal/lognormal in the L1/L2 variant comparison. | Run calibrated power curves under `t2`, `t3`, and lognormal backgrounds. |
| Do unmatched background extremes mask the planted subgroup? | The maximum-to-mean ratio does not show where extremes occur or whether they interfere with detection. | Direct diagnostics show that heavy-tail background extremes usually occur at different indices in `D_x` and `D_y`; paired-product masking is substantially more common among non-rejected runs. | Compare the global statistic with a pre-specified top-k or scan-style sparse-signal comparator. |
| Does larger sample size create over-sensitivity? | Large samples may make weak structural signals detectable, but true over-sensitivity would show up as inflated independent-null rejection. | Higher-replication null checks returned close to `.05`. The fixed-`k` versus fixed-proportion tail validation shows that declining power with larger `n` is mainly sparse-signal dilution when `k / n` decreases, not an inherent large-sample problem. | Keep fixed `k` and fixed `k / n` separate in future sample-size reporting. |
| What does magnitude `8` mean relative to background scale? | Magnitude should be interpreted relative to the background distribution, not as a free-standing number. | Current simulations use standardized or unit-scale backgrounds. | Add a table showing where magnitude `8` falls in each background's empirical quantiles. |
| Is `c_delta` a general correlation of internal structures? | Row aggregation may discard most pairwise geometric information. | In one-dimensional L2, divergence ranking is exactly absolute-deviation ranking. An exact construction has identical divergence vectors but full distance-matrix correlation `-0.04018`. | Reframe the method as paired observation-level divergence salience; compare against full-matrix methods under deliberately different alternatives. |
| Does the CV weighting belong in robust `c_delta_star`? | Pearson and `c_delta_star` give identical permutation evidence, but only `c_delta_star` amplifies concordance by marginal heterogeneity. | At fixed population Pearson `.30`, the coefficient ranged `1.019-3.546`; the highest-CV setting remained variable at `n=2000`. | Ask whether heterogeneity amplification is part of the construct; otherwise prefer Pearson as the direct effect scale. |
| Do profile and Mantel methods target different alternatives in the same design? | Separate simulations cannot establish construct-specific sensitivity. | Two independent building runs show Huber advantage for node salience and Mantel advantage for shared dyadic geometry. | Vary the node/dyad mixture continuously and add MRQAP only when multiple dyadic predictors are present. |
| Where does profile-versus-Mantel power change under mixed signals? | Real applications may contain both node salience and dyadic geometry. | Symmetric and skew derivatives are explicit. The `.131/.043` composite-generator crossovers are mainly sign-prevalence effects; balanced magnitude skew caused only modest shifts. | Add another skew family only if it matches the application; do not promote generator-specific crossover values to a selection rule. |
| Is the crossover determined by node/dyad signal ratio? | A stable ratio could simplify design-stage method choice. | Pure paths now explain the stronger node direction. On seven external cells, the nine-cell raw-ratio model had RMSE `.0247`; over all 16 cells, ratio R-squared was `.803` versus `.903` for separate strengths. A ratio is useful but not exact. | Derive local mixed-path power slopes only if a design-stage approximation is needed; do not promote either fit to an observed-data decision rule. |
| Should the test be upper-tail, lower-tail, or two-sided? | The original implementation only tested positive alignment. | All three alternatives are null-calibrated in the focused simulation. Directional tests have higher power when direction is pre-specified. | Retain greater as the primary default; treat less/two-sided as scientifically motivated extensions. |
| Can the paired-standout interpretation be expressed theoretically? | A verbal description alone does not identify how overlap enters the signal. | For equal-size binary standout sets, `r = (n m - k^2) / (k (n-k))`; continuous simulations follow this ordering but are attenuated by background salience. | Decide whether to present the binary model as an explanatory limiting case in the revision. |
| Does chance overlap inflate rejection when both datasets contain strong standouts? | Deliberately disjoint sets are not a proper random-set null. | With independently selected size-4 standout sets, overlap follows the exact hypergeometric law and rejection remains `.0377-.0493` across L1/L2 and normal/`t3`/`t2`. | Explain conditional overlap signal separately from unconditional null calibration. |

## Suggested Priority

1. Ask whether `CV_X CV_Y` is part of the intended robust-salience construct;
   this determines whether Pearson or raw `c_delta_star` is the cleaner effect
   scale.
2. Confirm whether the substantive target is labelled-room salience, complete
   dyadic geometry, or both as separately reported questions.
3. Decide with Professor Hoorn whether a primary test should target a named
   profile/dyadic estimand or the standardized-max union question. Retain the
   latter as sensitivity until that scientific choice is explicit.
4. Partial-null profile-only and dyadic-only laws now reject subset
   pivotality. Complete local influence functions and jackknife studentizers
   are now implemented. Fully recomputed studentized permutation plus Holm
   passed the first iid `n=80/160` gate, but not a uniform theorem. Six-
   building room-iid and sign-flip rules failed, and skew-scale cluster-t Holm
   remained anti-conservative. Derive the declared building-level estimand and
   its cluster U-projection before formal component inference in the current
   application.
4. Treat the completed pure-path and external-grid result as a mechanistic
   approximation; pursue mixed-path local power theory only if needed for the
   report, not as a post-hoc method-selection rule.
5. Add MRQAP only for a concrete multi-predictor distance-matrix question.
