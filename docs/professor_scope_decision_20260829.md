# Supervisor scope decision and manuscript alignment

Date: 2026-08-29

## Decision received

Professor Hoorn decided to correct the normalization in the original
\(c_d\) paper, leave that paper on arXiv, and treat the robust-reference work
as a separate Yao--Hoorn paper with Yao as first author.

The original paper asks whether two groups are internally divergent in the
same way by comparing each labelled observation with the other observations
in its own group. The new paper retains the paired-divergence-profile idea but
changes the reference construction and the main scientific question. It asks
whether similarity of profiles around robust references can be inferred
reliably, especially when those references are weakly identified or unstable.

## Construct map

| Feature | Original arXiv \(c_d\) | New Yao--Hoorn paper |
|---|---|---|
| Observation profile | All-to-all within-group divergence | Radius around a median/MAD/Huber reference |
| Reference geometry | Empirical pairwise configuration; for 1D L2, reducible to a mean-centred radial transform | Explicit robust marginal location functional |
| Main scientific object | Broad normalized concordance of internal divergence profiles | Standardized robust-reference profile similarity |
| Main estimand | Historical \(c_d\) scale | \(\rho_P=\operatorname{Corr}(|X-T_X|,|Y-T_Y|)\) |
| Secondary quantity | Not applicable within the old paper's own framing | \(C=E(r_Xr_Y)/\{E(r_X)E(r_Y)\}\), as historical/effect scale |
| Main contribution | Define and motivate the coefficient | Establish when inference works, construct failures, and develop diagnostics |

## Exact mathematical relation and separation

For the implemented one-dimensional L2 all-to-all profile,

\[
D_i=\left\{\frac{1}{n-1}\sum_{j\ne i}(X_i-X_j)^2\right\}^{1/2}
\]

satisfies

\[
D_i^2=\frac{n}{n-1}\{(X_i-\bar X)^2+s_X^2\},
\qquad
s_X^2=\frac1n\sum_i(X_i-\bar X)^2.
\]

Thus the old all-to-all calculation is compressed to a nonlinear,
mean-centred radial profile with a group-wide variance floor. The new profile

\[
R_i=|X_i-\widehat T_X|
\]

uses a fitted robust location functional instead. MAD scaling can be used in
the fitting equation but cancels from within-margin Pearson profile
correlation. These constructions are scientifically related but are not the
same statistic or population functional.

For the new profiles,

\[
C=1+\rho_P\,CV(R_X)CV(R_Y).
\]

Therefore \(C\) and \(\rho_P\) have the same fixed-margin permutation
ordering, but \(C\) also changes with marginal profile heterogeneity. This is
why \(\rho_P\) is the clearer main effect and \(C\) should be secondary.

## Alignment with the three claims

1. **When can the result be trusted?** Under fixed regular IID laws, the
   complete influence-function expansion and plug-in studentization give
   pointwise asymptotically valid Wald inference.
2. **When can it fool us?** Near-degenerate robust-reference fitting can
   switch nonlocally and create severe finite-sample distortion even when the
   population profile effect is null.
3. **Can risk be diagnosed?**
   \(I_n=\sqrt n\,\sigma_{\min}(J)\) is a dimensionless first-order organizer
   of this transition, but not a universal cutoff; higher-order family effects
   remain.

Professor Hoorn's framing therefore confirms rather than replaces the frozen
claim package. It gives the three claims a single scientific narrative:
trustworthy regular inference, a constructive way it fails, and a principled
but incomplete diagnostic of proximity to failure.

## Manuscript consequences

- Lead with the substantive paired-profile question and \(\rho_P\), not with
  a new \(c_d\) definition.
- Introduce the original arXiv paper as the motivating predecessor, then state
  clearly where the robust-reference functional departs from it.
- Use the \(C\) scale only for historical continuity or when marginal
  heterogeneity weighting is itself scientifically intended.
- Keep the regular Wald theorem and empirical studentized-permutation panels
  visibly separate.
- Describe “safer” as theory plus diagnostics and explicit failure boundaries,
  not as a claim of universal robustness.
- Retain the four frozen evidence panels. No new distribution grid is needed
  in response to this decision.

## Immediate next work

The next work package should assemble a manuscript skeleton in this order:

1. original question and the robust-reference shift;
2. definition and interpretation of \(\rho_P\), with \(C\) secondary;
3. regular IID inference theorem;
4. near-degenerate constructive failure;
5. nuisance-conditioning diagnostic and higher-order limitation;
6. implications for practice and the boundary of permutation claims.
