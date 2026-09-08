# Supervisor discussion brief: current Yao--Hoorn paper status

Date: 2026-09-06

> Follow-up qualification, 2026-09-07: this is the dated pre-meeting brief,
> not an unconditional readiness certification. The active-nuisance study in
> `docs/active_nuisance_validation_20260907.md` adds a nonzero-effect coverage
> boundary and corrects the mechanism/residual language used below. The
> complete theorem draft still needs independent mathematical review.

This is an internal meeting brief rather than an email or submission draft. It
summarizes the paper that now exists, the evidentiary status of each claim, and
the decisions that still require discussion with Professor Hoorn.

## 1. Current paper in one paragraph

The original Hoorn \(c_d\) paper asks whether two groups exhibit similar
all-to-all internal divergence patterns. The separate Yao--Hoorn paper retains
the paired-salience motivation but studies profiles around fitted robust
marginal references. Its primary estimand is

\[
\rho_P=\operatorname{Corr}(|X-T_X|,|Y-T_Y|),
\]

where each \(T\) is a median/MAD-scaled Huber location functional. The paper's
main question is inferential: when is inference for this generated profile
correlation trustworthy, how can unstable reference fitting create
finite-sample distortion, and how much of that transition is organized by
nuisance conditioning?

## 2. What is already mature

- The scientific scope and old/new construct separation are fixed.
- \(\rho_P\) is the primary estimand; the historical normalized cross-moment
  \(C\) is secondary.
- Sections 1--6 have working manuscript drafts.
- Appendix A contains the regular IID influence-function and studentization
  theory, including the median, MAD, Huber, five-moment, and paired covariance
  paths.
- The sample MAD convention, stochastic equicontinuity route, plug-in
  \(L_2\) consistency, and endpoint-density sign have received targeted
  mathematical audits.
- The public implementation of \(\rho_P\) and its complete Wald standard error
  passes equivalence, centering, identity, and affine-invariance checks.
- Table 2 and Figures 1--3 are built from frozen fixed-seed sources with
  source hashes and Monte Carlo uncertainty.
- Theorem-aligned Wald evidence, finite-sample mechanism interventions, and
  empirical fully recomputed permutation evidence are now visibly separated.
- The Stavig and classical robust-correlation positioning has been checked:
  the contribution is not the first use of absolute deviations, medians,
  MADs, robust correlation, generated-nuisance influence functions, or
  singular Jacobians.

## 3. The three claims and their present status

### Claim 1: regular IID inference

Under fixed regular IID laws satisfying the stated uniqueness, density,
moment, nonsingularity, and empirical-process conditions, the complete
influence-function expansion yields pointwise asymptotic normality, consistent
plug-in variance, and studentized Wald inference.

Status: theorem-level under declared assumptions.

Supporting evidence:

- at \(n=640\), the normal-margin shared-sign weak-null rejection rate is .044 and the
  independent-\(t_5\) rate is .059; both Wilson intervals contain .05;
- their studentized standard deviations are .993 and 1.037;
- the strong-skew rejection rate falls from .122 at \(n=640\) to .082 at
  \(n=2560\), but remains elevated and asymmetric.

Required wording: pointwise, not uniform. Strong skew can converge slowly even
when unstable reference fitting is not the explanation.

### Claim 2: nonlocal reference switching

In the studied near-degenerate separated-mode construction, sample
fluctuations can move the fitted robust references nonlocally and manufacture
strong profile correlation even though the fixed-reference population profile
correlation is zero.

Status: an exact proposition for the idealized two-mode geometry plus
triangulated empirical finite-sample evidence for the continuous construction.

Supporting evidence:

- fixing the symmetry reference reduces rejection by .723 at \(n=80\) and
  .491 at \(n=640\);
- in the diffuse control, the largest absolute refit--fixed difference is
  .018;
- exact sign balance reduces rejection by .709 at \(n=80\) and .475 at
  \(n=640\);
- at \(n=640\), increasing shared-sign coupling from zero to one increases the
  mean refitted profile effect by about .625, while fixed-reference effects
  remain within .0021 of zero.

Required wording: unstable fitting can cause severe distortion in this
construction, not that every multimodal or low-density law fails.

### Claim 3: nuisance conditioning

The standardized nuisance Jacobian motivates

\[
I_n=\sqrt n\,\sigma_{\min}(J)
\]

because first-order nuisance error is amplified at order \(1/I_n\) along the
least-identified standardized direction. The index is dimensionless and
positively affine invariant.

Status: first-order theoretical motivation plus strong empirical ordering, but
not an operational theorem.

Supporting evidence:

- leave-one-family-out, cross-sample-size, and held-conditioning-level
  predictions improve MAE over their intercept baselines by at least 72.2%;
- a prospectively selected hyperexponential family retains a 47.6% MAE
  improvement;
- all six prospective predictions are nevertheless too high;
- four families with nearly matched \(I_n\approx.445\) have rejection rates
  from .232 to .356.

Required wording: first-order organizer, not a universal cutoff. Family
residuals remain unexplained by the index; they are not proved purely higher
order without also matching score covariance and target projection.

## 4. Defensible novelty statement

The defensible contribution is the linked, problem-specific package:

1. complete inference for a profile correlation generated by two
   median/MAD-scaled Huber reference fits;
2. isolation of nonlocal reference switching as a source of finite-sample
   spurious profile correlation; and
3. use of a dimensionless nuisance-conditioning index to organize the
   transition while displaying its family-specific residual.

The paper should not claim invention of absolute-deviation correlation,
general robust correlation, the functional delta method, generated-regressor
corrections, or weak-identification diagnostics.

## 5. Decisions to discuss with Professor Hoorn

### Decision A: application

Should the paper include:

- one scientifically genuine paired dataset;
- a clearly labelled synthetic illustration; or
- no application, with the paper positioned as a theory-and-simulation
  methods article?

This is the largest remaining presentation decision. A convenient dataset
should not be added unless its pairing and sampling units are scientifically
defensible.

### Decision B: level of local theory

Is the current pointwise theorem plus explicit nonuniform boundary sufficient,
or should the paper derive a formal local-to-degeneracy limit? The latter
would strengthen the bridge between Claims 1 and 2, but is not needed to state
the current bounded three-claim paper.

### Decision C: role of permutation

Should the fully recomputed studentized-permutation results remain empirical
supporting evidence, as currently written? If permutation inference becomes a
headline procedure under the weak null, a conditional permutation CLT becomes
a substantive missing theorem and should receive its own section.

### Decision D: role of \(I_n\)

Should \(I_n\) remain a population explanatory diagnostic? Turning it into a
sample-level accept/reject gate would require estimating its uncertainty,
calibrating a decision rule, and validating that rule prospectively. The
current results do not authorize that interpretation.

### Decision E: paper destination and framing

The target journal, final title, permitted appendix length, and expectation for
an applied illustration will determine how much material belongs in the main
paper versus the online supplement.

## 6. Additional validation: necessary versus conditional

Necessary before submission:

- consolidate Sections 1--6 into one journal-formatted source;
- perform a final notation and bibliography consistency pass;
- conduct a systematic final novelty search without claiming exhaustive
  priority;
- verify the complete manuscript and display build in a clean dependency
  environment;
- write the abstract and bounded Discussion after the application decision.

Conditional on the supervisor's choice:

- real application selected: justify the sampling unit and use
  design-respecting or cluster-level inference;
- permutation promoted to a weak-null inferential method: prove the conditional
  studentized permutation limit;
- \(I_n\) promoted to an operational diagnostic: develop a sample estimator,
  uncertainty assessment, and prospective calibration;
- stronger theoretical bridge requested: develop local-to-degeneracy or
  switching-limit theory.

No additional general distribution grid is presently justified. New
computation should answer one of these explicit decisions rather than search
for another anomaly.

## 7. Recommended meeting outcome

The most useful outcome is to freeze four points:

1. the three-claim contribution and its bounded wording;
2. whether the current theory level is sufficient;
3. whether the paper needs a real application;
4. whether permutation and \(I_n\) remain supporting evidence or become
   headline methods.

Once these are fixed, the remaining work becomes manuscript consolidation,
targeted validation, and submission preparation rather than open-ended method
exploration.
