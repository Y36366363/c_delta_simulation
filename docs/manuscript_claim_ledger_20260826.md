# Manuscript claim ledger and stopping rule (2026-08-26)

## Frozen paper question

Professor Hoorn's 2026-08-29 scope decision separates the projects. The
corrected original \(c_d\) paper retains the broad all-to-all divergence
coefficient on arXiv. The new Yao--Hoorn paper cites that work but studies a
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
| 2 | Near-degenerate robust-reference fitting can create severe finite-sample distortion through nonlocal reference switching. | Mechanism proposition only for the idealized binary switching limit; the broad finite-sample statement is empirical. | Centre-gap versus diffuse controls, paired fixed-reference intervention, exact sign-balance intervention, and shared-sign coupling dose response. | Do not claim that every small density or every multimodal law fails. Do not present fixed reference or forced balance as a general correction. |
| 3 | The dimensionless quantity \(I_n=\sqrt n\,\sigma_{\min}(J)\) is a natural first-order organizer of the transition because nuisance error is amplified at order \(1/I_n\). | First-order expansion plus Proposition A.3: the standardized \(J\), \(\sigma_{\min}(J)\), and \(I_n\) are invariant to shift and positive units. Predictive adequacy remains empirical. | Monotone conditioning bands, leave-one-family-out and cross-size prediction, stricter grouped validation, and the prospective hyperexponential family. | It is not a universal scalar law or calibrated cutoff. Systematic family residuals show that curvature, switching geometry, tail shape, and other higher-order terms remain. |

## What is theorem, proposition, or observation

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
   correlation \(+1\), and opposite modes induce correlation \(-1\).
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
2 instead concerns a nonuniform sequence in which the nuisance map becomes
poorly conditioned and sample fluctuations can select different modes.

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
