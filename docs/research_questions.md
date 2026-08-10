# Research Questions and Next Checks

This note keeps the simulation work aligned with Professor Hoorn's latest
feedback and separates mathematical claims from empirical checks.

## Active Questions

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
- The current simplification uses symmetric margins. Skewed mixed paths would
  require restoring the Huber-location/MAD nuisance derivative from the full
  functional-delta calculation.

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
| Where does profile-versus-Mantel power change under mixed signals? | Real applications may contain both node salience and dyadic geometry. | Crossovers are mapped over 16 strength cells. Local derivatives show that both powers can fall near crossover while profile falls faster; the weak-both slope remains unresolved. | Extend the derivative only to skewed paths if needed, restoring the Huber/MAD nuisance terms; do not select a test post hoc from the observed mixture. |
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
3. Formalise within-building permutation validity and define the observational
   unit before cross-building application.
4. Treat the completed pure-path and external-grid result as a mechanistic
   approximation; pursue mixed-path local power theory only if needed for the
   report, not as a post-hoc method-selection rule.
5. Add MRQAP only for a concrete multi-predictor distance-matrix question.
