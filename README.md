# c_delta Simulation Pilot

This is a small first-stage project for studying the finite-sample behavior of the
correlation-of-divergency coefficient, `c_delta`.

## Updates 08/19/2026

- **Independent appendix audit completed** - The earlier moment assumption was
  sufficient for the C influence but not for profile correlation, whose
  general nonzero-effect variance terms require marginal fourth moments. The
  revision separates A5-C from the stronger general A5-rho, while proving a
  weaker-moment corollary specifically at the profile weak null.
- **Empirical-process gaps repaired explicitly** - A local
  VC/Euclidean-class condition and stochastic-equicontinuity lemma now control
  random nuisance substitution. Plug-in variance consistency is proved through
  population L2 convergence plus a Glivenko-Cantelli squared influence class,
  rather than pointwise convergence alone.
- **Remaining proof boundary recorded** - Precise entropy citations, an
  independent estimated-median MAD Bahadur check, and any conditional weak-null
  permutation CLT remain publication tasks. See
  docs/appendix_proof_audit_20260819.md.
- **Primary estimand recommendation resolved** - Use Huber-profile correlation
  `rho_P` as the direct concordance estimand and retain historical `C` as a
  secondary CV-weighted scale. Existing checks give identity error below
  `4.5e-16` and exactly equal permutation p-values, while fixed `rho_P=.30`
  allows population `C` to range from `1.019` to `3.546` as marginal CVs vary.
- **Formal appendix proof drafted** - The median, MAD, Huber, five joint
  moments, profile correlation, and c_delta derivatives are assembled into an
  iid asymptotic theorem and studentized Wald corollary. Exact randomization
  validity is separated from the still-incomplete conditional proof for
  studentized permutation under arbitrary weak nulls.
- **Four canonical evidence panels frozen** - Regular calibration,
  near-degenerate failure, 24-cell bridge recovery, and the confirmatory
  family residual are now selected from existing fixed-seed results. The
  34-row canonical table records source hashes, seeds, counts, Monte Carlo SEs,
  and Wilson intervals.
- **No anomaly expansion** - Today's computation only audited and froze
  existing evidence. See `docs/appendix_asymptotic_theory_20260819.md` and
  `docs/estimand_and_canonical_evidence_20260819.md`.

## Updates 08/18/2026

- **Project moved to paper-definition phase** - The core narrative is now
  regular iid validity, severe finite-sample distortion under near-degenerate
  robust-reference fitting, and the first-order explanatory role of
  `sqrt(n)*sigma_min(J)`. New simulations should serve one of these claims
  rather than open unrelated anomaly branches.
- **Evidence boundaries frozen** - Pointwise iid asymptotic normality is kept
  separate from exact permutation invariance; the Jacobian formula is
  analytic, while the predictive strength and lack of a universal cutoff for
  the conditioning index are empirical conclusions.
- **Higher-order family effects retained as the main limitation** - Matched
  first-order Jacobians do not remove the confirmed family residual. Curvature,
  influence-tail shape, and nonlocal median/MAD switching are future focused
  theory, not a reason for another broad simulation grid.
- **Conceptual and claim audit added** - The proposed paper structure, ten
  required conceptual explanations, evidence ledger, forbidden claims, and
  decisions for Professor Hoorn are in
  `docs/paper_architecture_and_conceptual_guide_20260818.md`.

## Updates 08/17/2026

- **Complete nuisance Jacobian computed and numerically verified** - The
  standardized median/MAD/Huber Jacobian includes centre density, both MAD
  endpoint densities, MAD asymmetry, Huber active-score curvature, and scale
  coupling. Central finite differences reproduced all entries within `5e-6`.
- **Smallest Jacobian singular value unifies the bridge scaling** - Across 24
  matched-family cells, smaller `sqrt(n)*sigma_min(J)` correlated `.971` with
  rejection and gave logit `R-squared=.932`. The binding direction was
  `d*f(m)`; nominal rows appeared only after the sample-scaled value was well
  above one, although no universal cutoff is claimed.
- **Residual family effect is beyond first order** - Adding MAD endpoint
  density and Huber curvature increased R-squared only to `.938`, while the
  matched-family Jacobians were nearly identical. The confirmed family
  difference is therefore a higher-order/nonlocal median-MAD selection effect,
  not a missing term in the functional delta derivative.
- **Skew benchmark restored the full coupling** - For lognormal log-SD `1.1`,
  the standardized MAD density difference was `-.294`, Huber scale coupling
  was `-.270`, and the Jacobian condition number was `3.74`, confirming the
  implemented indirect MAD-to-location path outside symmetry.

- **Matched-density bridge families refined the identification claim** - Four
  bridge laws with identical `f(0)=epsilon/2` preserved the main
  `n*epsilon^2` ordering (`R-squared=.931`). Family terms raised R-squared only
  to `.949`, but a targeted 500-dataset transition cell confirmed a modest
  residual family effect (`p=.00013`, Cramer's V `.101`). Centre density alone
  is therefore not a complete finite-sample condition.
- **MAD collapse added to the diagnostic audit** - Within the confirmed
  transition cell, small fixed-MAD-scale/IQR had risk-oriented Spearman
  correlations `.726-.777` with rejection, stronger and more consistent than
  bootstrap location spread. Bootstrap MAD spread itself had the wrong
  directional interpretation and is not recommended as a risk score.
- **External MAD-ratio check passed a conservative warning boundary** - In
  2,000-dataset external cells, `MAD-scale/IQR < .40` never warned for `t_5`,
  affine near-constant, or the regular-behaving sign-link path, and warned
  `.028/0` under strong skew at `n=80/320`. It remains descriptive, not a
  conditional-validity gate.

- **Independent boundary calibration reproduced the failure transition** - At
  `n=80`, studentized rejection fell from `.847` to `.053` as radial log-SD
  increased `.10` to `.30`; at `n=320` it fell from `.753` to `.033`.
  Root-n bootstrap reference spread moved with this transition, whereas fixed
  spacing and density warnings remained too structural to determine validity.
- **Positive centre density is not enough at finite n** - Adding independent
  Uniform bridge radii makes `f(0)=epsilon/2>0`, yet `epsilon=.05` still gave
  rejection `.487/.313` at `n=80/320`. Recovery approximately followed
  `n*epsilon^2`, as predicted by the median error scale
  `1/(epsilon*sqrt(n))`; the constrained collapse R-squared was `.919`.
- **Bootstrap warning remains diagnostic, not a gate** - The exploratory
  scaled-spread threshold `2` had zero warnings in eight external-null cells
  and tracked the broad recovery path, but samples passing the warning could
  still have strongly inflated conditional rejection. It must not be used to
  certify local p-values.
- **Project audit** - New boundary, bridge, collapse, and external validation
  artifacts are documented in `docs/profile_bridge_calibration_20260817.md`;
  after the nuisance-Jacobian extension, the full suite now passes 171 tests.

## Updates 08/16/2026

- **Sample-size diagnostic comparison completed** - Across `n=40-640`, the
  severe radial `.10` profile null remained invalid (`.887` to `.553`
  rejection), while root-n scaled bootstrap Huber-reference spread increased
  from `2.53` to `5.22`. The `.20` path recovered to nominal rejection even
  though spacing and central density still warned, separating assumption
  diagnostics from operational estimator stability.
- **Bootstrap reference stability is the leading operational warning** - In
  16 external null cells its scaled median stayed `1.03-1.39` and its largest
  90th percentile was `1.69`. A provisional value above `2` separates the
  severe path in this grid, but remains an exploratory warning rather than a
  formal gate. At least 199 bootstrap draws are recommended for reportable
  continuous scores.
- **Fixed spacing gate not promoted** - The `.50` spacing rule over-warned
  small strongly skewed samples, whereas central valley density described the
  theoretical low-density boundary but also warned after finite-sample
  rejection recovered. Current reporting should retain two tiers rather than
  combine them automatically.

- **Horizontal testing comparison completed** - Pearson/CCC weak-null theory
  supports fully recomputed studentization; distance correlation/HSIC target
  independence and have different degenerate-null resampling theory; spatial
  Mantel work reinforces structure-preserving permutations rather than
  unrestricted room labels.
- **Continuous regularity path located the recovery region** - Under a true
  profile weak null with shared signs, ordinary profile permutation rejected
  `.907/.903/.520/.157/.053` as radial log-SD increased
  `.03/.10/.20/.40/.80`; studentization reduced this to
  `.947/.840/.203/.030/.017`. It helps materially but cannot repair a
  nonregular Huber/MAD reference.
- **Scale-free gap diagnostic piloted** - Largest central spacing divided by
  IQR fell from median `.945` at the severe boundary to `.237` in the regular
  endpoint. A provisional `.50` warning gate removed the failed `.03-.20`
  path, retained `.997` of `t_5`, `.997` of the regular profile partial null,
  and `.797` of strong-skew samples. It is a conservative diagnostic, not a
  universal cutoff.
- **Small raw scale separated from nonregular geometry** - Independent
  continuous margins scaled by `10^-12` passed the `.50` gate in every
  replication and retained rejection `.033`, confirming that affine scale
  alone is not the failure mechanism.
- **Project audit** - The comparison is documented in
  `docs/comparator_testing_and_regularity_gate_20260816.md` with canonical
  result tables and reproducible code; after the diagnostic-scaling extension,
  the full suite now passes 152 tests.

## Updates 08/15/2026

- **Iid stress test sharpened the promotion boundary** - A new `n=80`,
  300-dataset, 199-permutation pilot tested fully recomputed studentized
  permutation under `t_5`, `t_3`, strong skewness, and both partial-null
  directions. Regular-row Holm true-null error ranged from `.0200` to `.0533`,
  strengthening its status as a pointwise iid candidate.
- **Near-degenerate profile inference rejected** - When population radii had
  SD only `.03` inside separated sign mixtures, unstable median/MAD reference
  fitting dominated the genuine profile variation: mean estimated profile
  correlation was `.9123` and true-null rejection was `.9533`. A stable
  Huber/MAD fit and profile variances bounded away from zero are now explicit
  reporting requirements; failure should yield ``weakly identified'' or
  ``undetermined'', not an ordinary local p-value.
- **Technical reporting note** - Added the focused interpretation in
  `docs/studentized_permutation_stress_20260815.md`; email and LaTeX drafts
  are delivered in conversation rather than stored in the project.
- **Project audit** - The full Anaconda test suite now passes 139 tests.

## Updates 08/14/2026

- **Fully recomputed studentized permutation passed its first iid gate** - On
  every permutation, the profile method recomputes all pairing-dependent
  complete-IF terms and Mantel recomputes its node-level Hájek variance. At
  `n=80`, Holm true-null FWER was `.050/.030` under two global nulls and
  `.0417/.0367` under the two partial nulls.
- **Larger-iid extension remained conservative after Holm** - At `n=160`,
  global/partial-null Holm FWER ranged from `.0225` to `.0350`, while both-
  alternative Holm power was `1.000`. One individual Mantel null row reached
  `.070`, so the evidence is pointwise rather than a uniform guarantee.
- **Six-building room-iid inference rejected** - Treating 120 rooms as iid
  produced family error `.2450` under Gaussian clusters and `.3685` under
  skew-scale clusters.
- **Small-building corrections remain unresolved** - Building-summed `t_5`
  plus Holm reduced FWER to `.0405` under Gaussian clusters but remained
  `.0735` under skew scales. A linearized building sign-flip was severely
  invalid (`.180/.236`) and was rejected. Increasing to 12/24 buildings did
  not repair the skew-scale cluster-t row, indicating that the global Mantel
  cross-building U-structure needs a separate cluster-level derivation. See
  `docs/studentized_permutation_and_small_building_20260814.md`.
- **Weak-null local tests derived** - Added the complete functional-delta
  influence function for the Huber-radius profile correlation and the
  order-two Hájek-projection influence function for the Mantel distance
  correlation. Both test `correlation = 0` without assuming label
  exchangeability.
- **Proper Mantel sampling unit** - The `n(n-1)/2` edges are not treated as
  independent. The sandwich uses node-level U-statistic projections, and the
  alternative jackknife deletes one node and all incident edges.
- **Iid partial-null confirmation** - Replaced fixed templates with genuinely
  iid weak-null laws. At `n=80/160`, Mantel-null/profile-alternative jackknife
  rejection was `.055/.047`; profile-null/Mantel-alternative rejection was
  `.053/.064`.
- **Finite-sample boundary remains** - Full-refit/delete-node jackknife improved
  on the raw sandwich, but global-null local rejection still reached `.075`
  for profile and `.097` for Mantel. The local tests are theoretically
  motivated research implementations, not report-ready defaults.
- **Multiplicity decision deferred** - Holm equals closed Bonferroni for the
  two component nulls and does not require subset pivotality, but it does
  require valid local p-values. Confirmatory global-null Holm FWER remained as
  high as `.080` at `n=80` and `.073` at `n=160`; neither Holm nor closed
  testing is promoted. See
  `docs/weak_null_local_tests_and_multiplicity_20260814.md`.

## Updates 08/13/2026

- **Subset pivotality rejected for weak component nulls** - Constructed
  independently calibrated profile-null/Mantel-alternative and Mantel-null/
  profile-alternative laws at `n=60`. The true-null standardized component
  distribution changed materially when the other component was non-null.
- **Partial-null behavior quantified** - Under profile-null/Mantel-alternative
  data, raw/maxT profile rejection was `.056/.038`, close to the matched
  global-null `.056/.044`. Under the reverse path, the null Mantel score SD
  collapsed from `1.083` to `.075` (KS `.596`) and rejected `0`. No inflation
  appeared in these cleaned paths, but the distributional change disproves a
  general subset-pivotality claim.
- **Interpretation boundary tightened** - Standardized max remains valid for
  the joint random-pairing omnibus null. Adjusted component p-values and winner
  labels remain descriptive rather than strong partial-null discoveries.
  Closed testing cannot be used until valid local weak-null tests are derived.
  See `docs/partial_null_subset_pivotality_20260813.md`.
- **Omnibus interpretation validated** - Added permutation maxT-adjusted
  profile/Mantel evidence and a standardized winner. The omnibus p-value is
  exactly the minimum of the two adjusted component values.
- **Focused attribution check** - In two 600-dataset target-separation rows,
  profile was the standardized winner `.735` under node salience and Mantel
  was winner `.998` under shared dyadic geometry. Omnibus regret was only
  `.013` and `.007`, respectively.
- **Construct overlap made explicit** - Most significant datasets supported
  both adjusted components because node salience and dyadic geometry are not
  orthogonal. Winner/evidence describe relative support; they do not identify
  a unique causal mechanism.
- **Permutation resolution** - Relative to 999 permutations, 499 achieved
  `.984` decision, `.988` winner, and `.968` attribution agreement across 18
  alternative cells; 499 is suitable for routine simulation and 999 remains
  preferable for final near-threshold attribution.
- **Theoretical boundary** - maxT controls the declared family under the joint
  random-pairing null. Strong component discovery still requires subset-
  pivotality or partial-null validation, so standardized max remains an
  interpretable omnibus sensitivity rather than the primary method. See
  `docs/omnibus_interpretability_20260813.md`.
- **Project audit** - The completed project passes 125 tests; all new omnibus
  result files and conditional attribution shares passed consistency checks.
- **Unequal building sizes separated from informative size** - Held total
  `n=72` fixed across balanced, moderately unequal, and severely unequal
  allocations. Size imbalance alone did not cause systematic power loss;
  larger changes arose when building size co-varied with floor area, age,
  heteroscedasticity, prevalence, and signal strength.
- **Temperature learning did not validate** - Scanned temperatures
  `0,.1,.25,.5,1,2,4,8,16`. Orbit-standardized CV power was flat near
  `0-.25` and then declined; temperature zero is a fixed 50/50 mixture. Learned
  weights also moved in the wrong radial-versus-dyadic direction.
- **Aggregation is an estimand choice** - Equal-building, square-root-room,
  and equal-room weights gave materially different adaptive results under
  severe imbalance; they cannot be selected as a technical afterthought.
- **Standardized-max candidate** - Permutation-standardized max stayed close
  to the better fixed method and averaged `.422` over four alternatives,
  versus `.402` profile and `.418` Mantel. It is an omnibus test without a
  unified effect size, so it is retained as a promising sensitivity candidate,
  not promoted to primary method.
- **Covariate-conditioned inference confirmed** - In the severe-imbalance
  null, unrestricted rejection ranged from `.001` to `.314`, while every
  within-building method calibrated at `.043-.046`.
- **Earlier project audit** - The project passed 121 tests at the end of the
  unequal-building stage. See
  `docs/unequal_building_covariate_adaptive_20260813.md`.

## Updates 08/12/2026

- **Application mechanism model added** - Separately controlled marginal
  positive-sign prevalence, directional sign agreement, shared radial
  heterogeneity, correlated building-centre offsets, and a declared dyadic
  component in a six-building generator.
- **Node terminology refined** - Across two 400-dataset seeds per factorial
  cell, sign agreement helped Mantel more (`+.524` average power effect versus
  `+.381` for Huber profile), whereas radial heterogeneity helped profile more
  (`+.157` versus `+.103`). Positive prevalence and correlated block centres
  acted as power-reducing distribution/nuisance axes rather than equivalent
  measures of within-building node signal.
- **Adaptive weighting calibrated conditionally** - Four null designs with
  2,000 datasets each placed fully retrained CV at `.043-.045` and nested-max
  at `.038-.049`. The adaptive weight is a method-preference diagnostic, not
  a latent node/dyad mixture estimate.
- **Within-building theorem completed** - Stated the product-permutation-group
  orbit proof and verified all `3!^2=36` permutations in a small example.
  Data-driven weights require pre-specification, group invariance, independent
  training, or complete refitting under every permutation.
- **Environment audit** - The project passes 112 tests in the Anaconda
  scientific Python environment. The system Python lacks NumPy/SciPy, so its
  import failure is an environment issue rather than a project regression.
  See `docs/application_node_decomposition_and_permutation_20260812.md`.

## Updates 08/11/2026

- **Project audit clean** - All 103 pre-existing tests passed before the study;
  the completed project now passes 106 tests and compiles without errors.
- **Skew attribution audited** - Decomposed node positive-sign prevalence and
  dyadic lognormal margins in a 2x2 study with two population and two local-
  power seeds per cell.
- **Sign structure, not skew magnitude, drove the early transition** - Node
  sign prevalence shifted crossover by about `-.277`; dyadic lognormal skew
  shifted it only `+.009` on average.
- **Balanced magnitude-skew control** - A node margin with skewness `-.432`
  but unchanged sign agreement moved crossover only `-.035` with Gaussian
  dyads and `+.022` with lognormal dyads. The prevalence cell had skewness only
  `.072` yet moved crossover by `-.266` to `-.288`.
- **Prior wording corrected** - The `.131/.043` configurations remain valid
  composite-generator results, but no longer support “greater skew implies an
  earlier crossover.” Huber/MAD derivative conclusions are unchanged. See
  `docs/skew_mechanism_factorial_20260811.md`.

## Updates 08/10/2026

- **Skew-path nuisance theory** - Derived transport derivatives for the median,
  MAD, and Huber location, including the nonzero MAD-to-Huber indirect term,
  then propagated them through profile correlation and `c_delta_star`.
- **Population derivative confirmed** - In the final eight-by-500,000 check,
  preferred-step complete-refit errors were at most `.000217` and below their
  Monte Carlo SE; two seeds, three steps, three boundary bandwidths, and two
  sample sizes preserved the substantive directions.
- **Huber movement matters more than MAD alone** - MAD indirect profile terms
  were `.0016-.0039`, while total location terms were about `.077-.082` and
  could reverse the profile slope under strong skewness.
- **Composite skew-generator crossover replicated** - Two independent local
  power runs placed the two composite configurations at `.131` and `.043`.
  The 08/11 mechanism audit attributes the early values mainly to node sign
  prevalence, not marginal skewness alone. All profile-ratio/Pearson
  permutation p-values stayed identical. See
  `docs/skew_mixed_path_huber_mad_derivatives_20260810.md`.
- **Prior logic independently reproduced** - A new eight-million-dyad seed
  reproduced the growing pure-node profile-minus-Mantel gap within `.00131`
  and the near-zero pure-dyad gap within `.00150`; all 95 pre-existing tests
  also passed before the new work.
- **Mixed-path tangent derived** - For the square-root variance mixture,
  derived the component tangent and propagated it through profile-radius and
  pair-distance correlations using the full covariance/variance derivative.
- **Pathwise formula verified** - Across four configurations and eight method
  rows, the analytic/pathwise effect slope agreed with a `.001` central
  difference to maximum error `.000166`.
- **Power slopes independently repeated** - Two 800-dataset seeds showed that
  both methods' power generally falls near the crossover, but profile power
  falls faster. The combined profile-minus-Mantel slopes ranged from `-.094`
  to `-.538`; only the weak-both path remained unresolved.
- **Mechanism refined** - Crossover is caused locally by faster loss of the
  node-specific profile advantage, not necessarily by Mantel power increasing.
  See `docs/mixed_path_local_slopes_20260810.md`.

## Updates 08/09/2026

- **Pure-path theory** - Derived closed forms for lognormal node salience and
  Gaussian dyadic signals. On the pure dyad path, profile and Mantel population
  correlations are exactly equal; on the sign-rewired node path, their Monte
  Carlo gap increased from `.209` at node correlation `.35` to `.445` at `.75`.
- **External row-and-column validation** - Added intermediate node strength
  `.65` and lower dyad strength `.30`, producing seven new cells with refined,
  independently repeated crossover estimates.
- **Ratio conclusion revised** - The original raw-ratio model predicted the
  seven new crossovers with RMSE `.0247`. Across all 16 cells it achieved
  `R-squared=.803`; separate strengths improved this to `.903`, with node and
  dyad coefficients `+.785` and `-.360`.
- **Qualified node dominance** - Node strength remains the larger crossover
  direction, consistent with the pure-path mechanism, but lower dyad strength
  has a non-negligible monotone effect. See
  `docs/pure_paths_and_external_strength_validation_20260809.md`.
- **Clean project baseline** - All 85 pre-existing tests passed, all Python
  sources compiled, and the working tree was clean before the new study.
- **Two-dimensional strength surface** - Crossed node-radius correlations
  `.35,.55,.75` with dyadic-value correlations `.45,.65,.80`, estimating a
  locally refined profile-versus-Mantel crossover for every cell.
- **Initial nine-cell result** - Raw and Fisher-z strength-ratio models explained
  only `.686` and `.644` of logit-crossover variation. Allowing node and dyad
  strengths to enter separately increased R-squared to `.938` and reduced
  leave-one-cell-out RMSE from `.202-.215` to `.118`; the new external grid
  above shows this was too small a basis for rejecting a ratio approximation.
- **Node strength dominates the surface** - Crossovers were `.148-.170` for
  node strength `.35`, `.211-.234` for `.55`, and `.253-.304` for `.75`.
  Dyad strength produced a smaller, nonmonotone within-row adjustment.
- **Interpretation boundary** - The separate model is descriptive and does not
  support post-hoc method selection. Profile versus Mantel choice remains
  estimand-first. See `docs/signal_strength_surface_20260809.md`.

## Updates 08/08/2026

- **Common-target building simulation** - Compared original L2 `c_delta`,
  Huber `c_delta_star`, Huber-profile Pearson, cap 6, and Mantel in one
  four-building design with node-salience and dyadic-geometry alternatives.
- **Construct-specific power** - Across two independent 800-dataset runs,
  Huber `c_delta_star` exceeded Mantel for sign-rewired node salience (`.823`
  versus `.713` combined), while Mantel exceeded Huber for shared dyadic
  geometry (`.959` versus `.797`). Neither method universally dominates.
- **Building restriction replicated** - Conditional-null rejection averaged
  about `.222-.239` under unrestricted permutations and `.041-.046` under
  within-building permutations.
- **Pearson equivalence extended** - Huber `c_delta_star` and Huber-profile
  Pearson had identical p-values in every unrestricted and block-restricted
  permutation test.
- **CV weighting boundary** - At fixed population Pearson concordance `.30`,
  theoretical `c_delta_star` ranged from `1.019` to `3.546` solely because the
  marginal CV product changed. The highest-CV row still had `-3.5%` relative
  bias and SD `1.46` at `n=2000`.
- **Interpretation update** - Report Pearson as the direct profile-concordance
  effect and report `c_delta_star` together with both CVs only when marginal
  heterogeneity weighting is scientifically intentional. See
  `docs/building_target_separation_20260808.md`.
- **Continuous node--dyad mixture** - Interpolated standardized node-salience
  and dyadic components over weights `0-1`, then refined the crossover region
  with two independent 1,200-dataset runs per grid point.
- **Transition region** - Combined paired-power analysis estimates the Huber-
  versus-Mantel crossover at dyadic variance weight `.216`. Huber has a
  resolved advantage through `.175`, neither has a resolved advantage over
  `.20-.25`, and Mantel has a resolved advantage from `.275` onward in this
  generator.
- **Comparator distinction** - Original L2 crosses earlier at `.137`; cap 6
  and uncapped Huber both cross at `.216`, confirming that the cap is mostly
  inactive without a severe leverage event.
- **Non-universality** - The transition is conditional on the selected node
  and dyadic correlations, sample size, building design, and permutation
  scheme. It is not a data-driven rule for choosing a test. See
  `docs/node_dyad_mixture_transition_20260808.md`.

## Updates 08/07/2026

- **Two estimands, not one replacement** - Professor Hoorn's distinction is
  now explicit: original L2 `c_delta` describes concordance of overall
  divergence for every member of the exact observed set, whereas
  `c_delta_star` describes robust-centre salience-profile concordance for a
  typical or generalisable structure.
- **Exact Pearson identity** - For nondegenerate robust radius profiles,
  `c_delta_star = 1 + corr(r_x,r_y) CV(r_x) CV(r_y)`. Consequently, Pearson
  profile correlation and `c_delta_star` have exactly the same one-sided
  permutation ordering and p-value; MAD scaling cancels from both.
- **Mantel information boundary** - Mantel compares the complete dyadic
  distance matrices. Original `c_delta` first compresses each matrix to one
  row-RMS divergence per labelled observation and therefore cannot establish
  equality of the complete pairwise geometry. Cross-building claims must be
  stated at the observation-salience level unless Mantel/QAP/MRQAP is used.
- **Reference robustness is not bounded influence** - The Huber centre protects
  ordinary observations from centre displacement, but an uncapped matched
  extreme can still dominate the final numerator. At planted magnitude 32 its
  median numerator share was `.965` for uncapped `c_delta_star`, `.474` for old
  L2, and `.497` for cap 6.
- **Design-respecting inference confirmed** - Reanalysis of the existing
  18,000-dataset conditional-null experiment gave unrestricted rejection
  `.442-.520`, versus `.047-.048` after within-building permutation.
- **Teacher-response package** - See the copyable LaTeX text in
  `docs/cdelta_response_hoorn_20260807.tex` and the proposed reply in
  `docs/email_reply_prof_hoorn_20260807.md`. The final PDF is intentionally
  left for the author's established R/LaTeX rendering workflow.

## Updates 08/06/2026

- **Distribution-level validation** - Replaced empirical contamination checks
  with analytic lognormal margins and Gaussian-Hermite joint quadrature. At
  regular points the full influence derivative matched finite differences to
  scaled error below `1.2e-5`.
- **Boundary clarification** - A contaminating atom exactly at the median is a
  nondifferentiable quantile direction. This is probability-zero for continuous
  sampling but must be excluded or treated directionally in the theorem.
- **Density diagnosis** - Across 2,500 skew-lognormal datasets per row,
  ordinary KDE, five-fold cross-fitted KDE, and the known true density changed
  mean sandwich SE by at most `0.2%`. KDE is not the main coverage bottleneck.
- **HC-style corrections** - HC1 and HC3-style scalar inflation improved
  coverage but remained inadequate; skew-model HC3-style coverage ranged only
  from `.8544` to `.8976` over `n=40-160`.
- **Bootstrap-t result** - In 600 outer datasets per condition, complete-refit
  bootstrap-t did not improve coverage and the skew log-pivot could produce
  very wide intervals.
- **Formal theorem** - Stated auditable regularity conditions, asymptotic
  linearity, paired asymptotic normality, sandwich consistency requirements,
  and the boundary of the studentized claim.
- **Inference decision** - Retain permutation inference as formal default;
  treat the complete-IF interval as asymptotic and exploratory. See
  `docs/studentization_refinement_and_theorem_20260806.md`.

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
- `scripts/run_population_skew_influence_validation.py`: distribution-level
  quadrature validation under skew lognormal margins.
- `scripts/run_density_hc_studentization_validation.py`: KDE, cross-fit, true-
  density, and HC-style standard-error comparison.
- `scripts/run_bootstrap_t_validation.py`: focused complete-IF bootstrap-t
  coverage experiment.
- `scripts/run_teacher_feedback_20260807.py`: exact profile/Pearson checks,
  Mantel information-loss construction, exact-set versus typical-set outlier
  estimands, and cross-building reanalysis prompted by the August 7 feedback.
- `scripts/run_building_target_separation_20260808.py`: common building-style
  comparison of salience-profile and dyadic targets, plus fixed-correlation CV
  weighting and convergence diagnostics.
- `scripts/run_node_dyad_mixture_20260808.py`: coarse, refined, and replicated
  power curves over a continuous node-to-dyad variance mixture.
- `scripts/summarize_node_dyad_mixture_20260808.py`: combine paired rejection
  counts and estimate method crossover locations without rerunning simulation.
- `scripts/run_signal_strength_surface_20260809.py`: coarse and refined
  node-strength by dyad-strength crossover surface and ratio-model comparison.
- `scripts/run_signal_strength_extension_20260809.py`: targeted independent
  extension for the one cell whose refined grid missed its coarse bracket.
- `scripts/summarize_signal_strength_surface_20260809.py`: assemble the final
  complete surface and refit ratio and separate-strength models.
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
- `docs/studentization_refinement_and_theorem_20260806.md`: distribution-level
  validation, studentization refinements, and formal first-order theorem.
- `docs/cdelta_response_hoorn_20260807.tex`: copyable LaTeX text for the
  technical response to Professor Hoorn; generate the final PDF through the
  author's established R workflow rather than treating a locally compiled PDF
  as the deliverable.
- `docs/email_reply_prof_hoorn_20260807.md`: proposed concise email reply.
- `docs/building_target_separation_20260808.md`: two-seed target-separation,
  building-permutation, and CV-weighting findings.
- `docs/node_dyad_mixture_transition_20260808.md`: current framework, mixture
  construction, paired transition estimates, and interpretation limits.
- `docs/signal_strength_surface_20260809.md`: two-dimensional crossover
  surface, ratio-hypothesis test, validation, and limitations.
- `docs/application_node_decomposition_and_permutation_20260812.md`:
  application-oriented mechanism decomposition, adaptive weighting, and the
  finite-sample within-building permutation theorem.
- `docs/unequal_building_covariate_adaptive_20260813.md`: unequal-size versus
  informative-size validation, temperature sensitivity, covariate-conditioned
  inference, and the adaptive-omnibus decision assessment.
- `docs/omnibus_interpretability_20260813.md`: maxT component evidence,
  construct attribution, power regret, permutation stability, and the
  global-null/partial-null interpretation boundary.
- `docs/studentized_permutation_stress_20260815.md`: heavy-tail, skewness,
  partial-null, and near-degenerate stress-test interpretation.
- `docs/comparator_testing_and_regularity_gate_20260816.md`: horizontal
  parameter-test comparison, continuous recovery path, and provisional
  profile-regularity warning gate.
- `docs/profile_diagnostic_scaling_20260816.md`: sample-size scaling,
  spacing-versus-density-versus-bootstrap comparison, external validation, and
  bootstrap Monte Carlo precision.
- `docs/profile_bridge_calibration_20260817.md`: independent fine-grid
  replication, positive-density bridge scaling, and diagnostic-gate audit.
- `docs/profile_bridge_family_validation_20260817.md`: matched-centre-density
  bridge families, targeted family confirmation, MAD nuisance audit, and
  external scale-ratio validation.
- `docs/nuisance_jacobian_20260817.md`: complete nuisance estimating system,
  finite-difference verification, singular-value identification scale, and
  skew benchmark.
- `docs/research_questions.md`: active research questions and next checks.
- `tests/test_cdelta.py`: minimal unit tests using Python's built-in `unittest`.

## Quick Start

For the complete test suite on this machine, use the Anaconda scientific
environment; the default system Python does not contain NumPy/SciPy:

```bash
/opt/anaconda3/bin/python -m pytest -q
```

From an environment with the scientific dependencies installed:

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
python3 scripts/run_population_skew_influence_validation.py
python3 scripts/run_density_hc_studentization_validation.py
python3 scripts/run_bootstrap_t_validation.py
python3 scripts/run_teacher_feedback_20260807.py
python3 scripts/run_building_target_separation_20260808.py
python3 scripts/run_node_dyad_mixture_20260808.py
python3 scripts/summarize_node_dyad_mixture_20260808.py
python3 scripts/run_signal_strength_surface_20260809.py
python3 scripts/run_signal_strength_extension_20260809.py
python3 scripts/summarize_signal_strength_surface_20260809.py
python3 scripts/run_application_node_decomposition_20260812.py
python3 scripts/summarize_application_node_decomposition_20260812.py
python3 scripts/run_unequal_building_adaptive_validation_20260813.py
python3 scripts/summarize_unequal_building_adaptive_20260813.py
python3 scripts/run_omnibus_interpretability_20260813.py
python3 scripts/summarize_omnibus_interpretability_20260813.py
python3 scripts/run_partial_null_subset_pivotality_20260813.py --phase confirmatory
python3 scripts/run_weak_null_local_tests_20260814.py --phase confirmatory
python3 scripts/run_studentized_permutation_weak_null_20260814.py --phase confirmatory
python3 scripts/run_small_building_weak_null_20260814.py --phase confirmatory
python3 scripts/run_studentized_permutation_stress_20260814.py --phase pilot
python3 scripts/run_profile_regularity_comparison_20260816.py --phase pilot
python3 scripts/run_profile_regularity_comparison_20260816.py --phase pilot --design gate_cv
python3 scripts/run_profile_diagnostic_scaling_20260816.py --phase pilot --design path --n 80 --radial-log-sd 0.2
python3 scripts/run_profile_diagnostic_scaling_20260816.py --phase pilot --design external --n 80 --scenario independent_t5
python3 scripts/run_bootstrap_reference_precision_20260816.py --phase pilot --n 80 --scenario radial_0p1
python3 scripts/run_profile_bridge_calibration_20260817.py --phase pilot --design bridge --n 80 --bridge-probability 0.1
python3 scripts/summarize_profile_bridge_calibration_20260817.py
python3 scripts/run_profile_bridge_family_validation_20260817.py --phase pilot --n 80 --bridge-probability 0.1 --bridge-family half_normal
python3 scripts/summarize_profile_bridge_family_validation_20260817.py
python3 scripts/run_profile_bridge_family_nuisance_20260817.py --phase confirmatory --bridge-family uniform
python3 scripts/run_mad_ratio_crossvalidation_20260817.py --design external --n 80 --scenario independent_t5
python3 scripts/run_nuisance_jacobian_20260817.py
python3 scripts/summarize_nuisance_jacobian_20260817.py
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
