# Manuscript claim ledger and stopping rule (2026-08-26)

## Frozen paper question

Professor Hoorn's 2026-08-29 scope decision separates the projects. The
original \(c_d\) paper retains the broad all-to-all divergence coefficient on
arXiv, with a normalization revision planned after the currently archived v2.
The new Yao--Hoorn paper cites that work but studies a
different primary object: robust-reference profile correlation and the
reliability of its inference.

The paper is therefore not a search for every distribution on which a robust
distance coefficient behaves unusually, nor a second attempt to define a
general-purpose \(c_d\). Its focused question is:

> If similarity of internal divergence is represented by paired profiles
> around robust references, when is the resulting inference trustworthy, when
> can unstable reference fitting fool us, and how much of that transition is
> organized by nuisance conditioning?

The primary estimand is the profile correlation

\[
\rho_P=\operatorname{Corr}(|X-T_X|,|Y-T_Y|).
\]

The ratio

\[
C=\frac{E(|X-T_X||Y-T_Y|)}{E|X-T_X|E|Y-T_Y|}
\]

is retained as the original scientific scale and secondary estimand. The
identity linking the two makes their fixed-margin permutation rankings the
same, but it does not make their Wald intervals identical.

This preserves the scientific lineage without equating the constructs. The
original statistic compares all-to-all within-group divergences. In the
one-dimensional L2 case its row profile satisfies

\[
D_i^2=\frac{n}{n-1}\{(X_i-\bar X)^2+s_X^2\},
\]

whereas the new primary profile is \(|X_i-\widehat T_X|\), with
\(\widehat T_X\) obtained from the median/MAD/Huber system. Thus the old and
new papers ask related paired-salience questions through different reference
and profile constructions.

## Claim ledger

| Claim | Defensible manuscript statement | Mathematical status | Frozen evidence | Boundary |
|---|---|---|---|---|
| 1 | Under fixed regular IID laws satisfying the stated density, moment, nonsingularity, and empirical-process conditions, the plug-in estimator is asymptotically linear and the full-IF studentized Wald statistic is asymptotically standard normal. | Theorem A.1, Lemmas A.1--A.5, and Corollaries A.1--A.3. At global independence, marginal reference estimation is first-order orthogonal. | Regular dependent-normal calibration, independent t5 recovery, and strong-skew convergence diagnostics. The oracle-reference skew experiment agrees with the orthogonality corollary. | The result is pointwise, not uniform near degeneracy. Strong skew can converge slowly even when reference fitting is not the cause. It is not a weak-null conditional permutation theorem. |
| 2 | Near-degenerate robust-reference fitting can create severe finite-sample distortion through nonlocal reference switching. | An imposed-offset algebraic identity illustrates the geometry; the fitted-switching and finite-sample statements are empirical, not a selection-probability theorem. | Centre-gap versus diffuse controls, paired fixed-reference intervention, exact sign-balance intervention, and shared-sign coupling dose response. | The signed-lognormal example has a nonregular median, not a flat population Huber root. The binary zero-reference profile has zero variance. Neither fixed reference nor forced balance is a general correction. |
| 3 | The dimensionless quantity \(I_n=\sqrt n\,\sigma_{\min}(J)\) supplies a local linear amplification rationale at scale \(1/I_n\). | First-order expansion plus positive-unit invariance under the declared equation normalization. Predictive adequacy remains empirical; this is not a uniform bound along arbitrary degenerating sequences. | Monotone conditioning bands, grouped prediction, and the prospective hyperexponential family. | Not a scalar law or calibrated cutoff. Family residuals are unexplained by the index; equal J does not match score covariance or target projection, so the residual is not proved entirely higher order. |

**2026-09-07 active-nuisance qualification to Claim 1.** The existing regular
correlated-lognormal law has an independently integrated target
\(\rho_P=0.193475119\) and nonzero reference/MAD contributions. In 2,000
replications per size, complete-IF 95% Wald coverage is .858, .9115, and .927
at n=160,640,2560. All Wilson intervals exclude .95. An oracle fixed-reference
estimator also undercovers. This validates an implementation/formula path and
records a practical convergence boundary; it does not establish usable
finite-sample coverage or superiority over the direct-only ablation. See
`docs/active_nuisance_validation_20260907.md`.

## What is theorem, proposition, or observation

**2026-09-09 supervisor-directed qualification.** The main contribution is
pointwise regular inference with a worked finite-sample failure, not a broad
safe-use rule. In four existing shared-sign cells, fixed-population-scale
Huber fitting already links reference errors and biases the fitted profile
correlation; complete median/MAD fitting substantially amplifies the severe
cells. Thus Claim 2 must not name median/MAD as the exclusive cause. The short
model result proves m=T=0, raw MAD=1, independent true profiles (rho_P=0, C=1),
and sample-median root-n failure despite a nonzero Huber slope. This identifies
a failed sufficient assumption, not impossibility of alternative target
asymptotics. Its fourth-root boundary remains a conditional heuristic.

For Claim 3, the standardized full Jacobian is singular at every positive
tau in this unbridged family; I_n=0 cannot distinguish its severe and diffuse
cells. Positive-density bridge ordering is separate empirical evidence, not
a universal characterization. Re-pairing leaves all marginal references
unchanged; only joint moments and studentization change. The permutation
track supplies empirical null rejection, not established weak-null Type I
error. See `docs/reference_pathway_results_20260909.md` for stage-aware and
direct-only rejection, paired Monte Carlo uncertainty, and numerical flags.

### Theorem-level results under declared assumptions

1. The median, MAD, and MAD-scaled Huber functionals have the displayed
   derivatives.
2. The five moments and the two estimands have joint asymptotic linear
   representations, yielding pointwise IID asymptotic normality.
3. The plug-in influence variance is consistent under the stated localized
   Glivenko--Cantelli and moment conditions.
4. At the profile weak null, the fourth-moment requirement for the two
   variance moments relaxes in the first-order test.
5. At global independence, the marginal Huber-reference contribution to the
   profile-correlation influence function cancels exactly.

### Exact finite-dimensional propositions

1. Fixed-margin permutation rankings of \(C-1\) and \(\rho_P\) agree.
2. Randomization inference is finite-sample valid under the declared group
   invariance, not merely under \(\rho_P=0\).
3. In the two-radius binary construction, common reference modes induce
   correlation \(+1\), and opposite modes induce correlation \(-1\),
   conditional on imposed nonzero offsets. It does not prove fitted selection
   probabilities; at the binary zero-reference law the target is undefined.
4. The standardized nuisance Jacobian and \(I_n\) are positively affine
   invariant. Also, \(\|J^{-1}\|_2=1/\sigma_{\min}(J)\) whenever \(J\) is
   nonsingular.

### Empirical observations

- The selected regular calibration cells are close to nominal size.
- Strong-skew studentization has a persistent asymmetric finite-sample tail.
- Reference switching causes the severe centre-gap distortion in the studied
  family.
- \(I_n\) orders much of the bridge transition but leaves family-specific
  prediction error.

These observations support and delimit the claims; none is itself a universal
theorem over all regular or near-degenerate distributions.

## Logical separation of the three claims

Claim 1 and Claim 2 are not two strengths of the same defect. Under global
independence, reference fitting is first-order orthogonal, which explains why
oracle population centres did not cure the strong-skew tail imbalance. Claim
2 instead concerns nonlocal nuisance fitting. The severe unbridged
signed-lognormal example already violates regular median identification at
each positive radial spread; it is not itself a sequence of regular laws.
Regular bridge laws provide the separate approach-to-degeneracy comparison.

Claim 3 explains why this second transition is plausible at first order:
the least identified standardized nuisance direction is of order
\(1/\{\sqrt n\sigma_{\min}(J)\}\). It does not explain every Claim 1
higher-order skew effect, nor does it absorb the remaining bridge-family
residual.

## Claims that must not be written

- “The new procedure has valid finite-sample inference under every weak null.”
- “Studentized permutation is proved valid whenever \(\rho_P=0\).”
- “A small \(I_n\) is necessary and sufficient for failure.”
- “There is a universal calibrated cutoff for \(I_n\).”
- “Near-degenerate fitting always inflates size.”
- “The Jacobian index fully explains family effects.”
- “The unexplained family residual has been proved entirely higher order.”
- “The severe signed-lognormal construction has a flat population Huber root.”
- “The current nonzero-effect study establishes nominal 95% Wald coverage.”
- “Fixing the centre, forcing sign balance, or switching to bootstrap is an
  established general remedy.”
- “Six buildings are enough for a conventional cluster asymptotic argument.”

## Frozen evidence for the manuscript

The four canonical panels remain: regular calibration, near-degenerate
failure, bridge recovery, and family residual. The paired fixed-reference and
sign-balance experiments are mechanism checks. The prospective fifth family
is an external transport check. They should not be expanded into an open-ended
distribution catalogue.

All reported Monte Carlo cells retain fixed root seeds, repetition counts,
Wilson intervals where appropriate, and explicit inference-track labels. Wald
and fully recomputed permutation evidence must remain in separate columns or
panels.

## Stopping rule and next decision

The 2026-08-29 supervisor decision confirms the three-claim package and closes
the estimand and scope questions. New computation is justified only if it
closes one of these claims, checks reproducibility, or tests a stated boundary.
The next high-value task is manuscript assembly and alignment of the main
tables with this ledger, not another marginal scenario.

The 2026-08-26 deterministic audit records machine-precision cancellation for
independence orthogonality, exact binary-switching correlations, and numerical
positive-affine invariance of the standardized Jacobian. A source-level check
also protects the single-numerator MAD derivative and the new LaTeX escapes.
