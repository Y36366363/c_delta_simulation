# Archived predecessor and Section 3 readiness audit

Date: 2026-08-31

## 1. Archived predecessor verified

The original paper has a stable arXiv record:

- Johan F. Hoorn;
- *Correlation of divergency: c-delta. Being different in a similar way or
  not*;
- arXiv:2510.16717, primary category `stat.ME`;
- first submitted 2025-10-19;
- current inspected version: v2, revised 2026-03-08, 17 pages;
- official record: <https://arxiv.org/abs/2510.16717>.

The stable manuscript citation may therefore use “Hoorn (2025),
arXiv:2510.16717.” If the bibliography records a version date, it should say
that v2 was revised in 2026. The arXiv identifier will remain stable when a new
version is uploaded.

### Normalization status of current v2

Visual and extracted-text review of page 3, Eq. 4, gives

\[
c_\delta^{(v2)}
=\frac{\sum_{i=1}^nD_{x,i}D_{y,i}}
{\left(n^{-1}\sum_iD_{x,i}\right)
 \left(n^{-1}\sum_iD_{y,i}\right)}.
\]

Thus the archived v2 exists, but the planned correction is not yet online.
The corrected numerator should be the empirical mean,

\[
c_\delta^{\mathrm{corrected}}
=\frac{n^{-1}\sum_{i=1}^nD_{x,i}D_{y,i}}
{\bar D_x\bar D_y}
=\frac{c_\delta^{(v2)}}{n}.
\]

This correction gives permutation expectation one conditional on the two
fixed divergence profiles. Until a later arXiv version appears, the new paper
should cite the archived predecessor but should not say that the online PDF
already contains the correction.

## 2. Section 3 purpose

Section 3 should establish the paper's first main claim and nothing broader:

> Under a fixed regular IID law, the robust-reference profile-correlation
> estimator is asymptotically linear, its complete paired influence variance
> can be estimated consistently, and the resulting Wald statistic is
> asymptotically standard normal.

It should not attempt to prove finite-sample validity, uniformity near a
degenerate reference, clustered-building inference, or a conditional
weak-null permutation CLT.

## 3. Main-text assumptions to retain

The eight Appendix assumptions can be compressed into five main-text groups:

1. **Paired IID sampling.** The independent units are the observed pairs
   \(Z_i=(X_i,Y_i)\). Rooms nested in buildings require a different theorem.
2. **Regular marginal references.** The median and MAD are unique, the three
   required density values are continuous and positive, and the Huber root is
   unique with positive score curvature and no mass at its knots.
3. **Profile nondegeneracy.** Both profile means and variances, and the target
   influence variance, are positive.
4. **Moments.** General confidence intervals for \(\rho_P\) use the stated
   fourth-plus marginal moments; testing \(\rho_P=0\) admits the weaker
   Corollary A.2 condition.
5. **Regular plug-in and empirical processes.** Nuisance roots and density
   estimates are consistent, and the localized moment/influence classes obey
   the Appendix Donsker and Glivenko--Cantelli conditions.

The main text should not reproduce the full entropy ledger. It belongs in
Appendix A and Supplement S1.

## 4. Recommended theorem block

After defining the complete paired influence function \(IF_\rho(Z;P)\) by
reference to the preceding nuisance and moment derivatives, state:

\[
\sqrt n(\widehat\rho_P-\rho_P)
=\frac1{\sqrt n}\sum_{i=1}^n IF_\rho(Z_i;P)+o_P(1)
\Rightarrow N(0,V_\rho),
\qquad
V_\rho=E\{IF_\rho(Z;P)^2\}.
\]

If \(\widehat{IF}_{\rho,i}\) uses consistent nuisance, moment, and density
plug-ins, then

\[
\widehat V_\rho
=\frac1{n-1}\sum_{i=1}^n
(\widehat{IF}_{\rho,i}-\overline{\widehat{IF}}_\rho)^2
\to_P V_\rho,
\]

and

\[
\frac{\sqrt n(\widehat\rho_P-\rho_P)}{\sqrt{\widehat V_\rho}}
\Rightarrow N(0,1).
\]

The main text should give interpretation rather than the full proof. The proof
chain is already audited in Appendix A: median/MAD and Huber derivatives,
joint moment influence, stochastic equicontinuity, functional delta method,
plug-in \(L_2\) consistency, and empirical second-moment consistency.

## 5. Corollaries worth retaining in the main text

1. At \(\rho_P=0\), the gradients with respect to the two squared profile
   moments vanish, allowing the weaker null moment condition.
2. Under global independence, the coefficients on both marginal Huber
   reference influences vanish at first order. This does not eliminate
   higher-order strong-skew distortion.
3. The theorem is pointwise. It is not uniform over sequences with
   \(\sqrt n\sigma_{\min}(J)=O(1)\).

These three statements connect Section 3 directly to the later regular,
strong-skew, and near-degenerate evidence.

## 6. Validation completed for Section 3

The deterministic 2026-08-31 audit found:

- positive-affine error of the primary estimate below \(5\times10^{-16}\);
- positive-affine error of its complete standard error below
  \(3\times10^{-17}\);
- empirical influence-centering error below \(2\times10^{-17}\);
- all theorem, studentization, weak-null, orthogonality, and non-overclaiming
  markers present in Appendix A;
- both 1,000-repetition regular dependent weak-null Wald intervals compatible
  with nominal 5% size (`.052` and `.044` rejection);
- strong-skew rejection decreasing from `.122` at \(n=640\) to `.082` at
  \(n=2560\), supporting a pointwise theorem with an explicit finite-sample
  warning rather than uniform calibration.

The reproducible values are in
`results/section3_readiness_audit_20260831.tsv`.

## 7. One nonblocking implementation gap

The validated primary \(\rho_P\) inference routine currently lives in
`scripts/run_weak_null_local_tests_20260814.py`, whereas the reusable public
module in `src/cdelta.py` still exposes its full general inference entry point
mainly on the secondary \(C\) scale. This does not block drafting Section 3 or
the mathematical theorem. Before a software release or replication package is
frozen, the \(\rho_P\) routine should be promoted to a public source API and
the simulation script should call that shared implementation.

## 8. Readiness decision

Section 3 is ready to draft. The safe next action is to write a concise main
text section with the five assumption groups, one theorem block, the three
corollary interpretations, and a clear nonuniformity boundary. HC corrections,
bootstrap-t intervals, full entropy verification, and weak-null permutation
theory should remain outside the main theorem section.
