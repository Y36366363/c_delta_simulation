# Novelty and classical-alternative positioning (2026-09-02)

## Purpose and search boundary

This update answers one manuscript question: where does

\[
\rho_P=\operatorname{Corr}(|X-T_X|,|Y-T_Y|)
\]

sit relative to Stavig's absolute-deviation correlation and the main classical
alternatives?  It is a source-level positioning audit plus deterministic
target-separation checks, not another general distribution grid.  The search
is deliberately finite and is **not an exhaustive proof of absence** of every
related statistic.

## What Stavig (1982) actually defines

Stavig gives two coefficients.  For paired ranks with differences
\(d_i=R_{Xi}-R_{Yi}\),

\[
r_{ad}=1-\frac{\sum_i |d_i|}{(n^2-1)/3}.
\]

The paper identifies this ranked statistic with Spearman's footrule form.  For
interval-level observations, let \(z_{Xi}\) and \(z_{Yi}\) be the separately
standardized marginal scores.  Stavig defines

\[
r_{AD}
=1-\frac{\sum_i |z_{Xi}-z_{Yi}|}
{\{4(n^2-1)/3\}^{1/2}}.
\]

Thus the interval coefficient measures an \(L_1\) discrepancy between
**signed standardized paired values**.  It uses the sample mean and standard
deviation through the z scores.  It is not the Pearson correlation between
absolute distances from marginal robust references.

## Decisive target distinction

The naming overlap is real, but the estimands are different:

| Feature | Stavig interval \(r_{AD}\) | Yao--Hoorn \(\rho_P\) |
|---|---|---|
| Input after marginal fitting | signed z scores | unsigned robust-reference radii |
| Pairing operation | normalized \(\sum |z_X-z_Y|\) | Pearson correlation of the two profiles |
| Reference | mean and SD | median/MAD-scaled Huber location |
| Direction | retained | deliberately removed |
| Scientific question | do standardized paired values agree? | do paired observations become unusual together relative to their own robust references? |

Three deterministic witnesses make the difference executable.  When
\(Y=X\), both coefficients equal one.  When \(Y=-X\), the radial profiles are
identical and \(\rho_P=1\), whereas Stavig's coefficient is negative.  A
within-radius sign rewiring also leaves \(\rho_P=1\) but materially changes
Stavig's coefficient.  These are target-separation examples, not performance
claims and not Monte Carlo evidence.

The complete eleven-row positioning table is stored in
`results/classical_alternative_positioning_20260902.tsv`; the witness values
and pass/fail audit are in `results/stavig_target_separation_20260902.tsv` and
`results/stavig_positioning_audit_20260902.tsv`.

## Defensible novelty position

The paper should not argue that correlating absolute deviations is itself a
new algebraic operation.  Once two profiles are fixed,
\(\operatorname{Corr}(|X-t_X|,|Y-t_Y|)\) is ordinary Pearson correlation
after a prespecified transformation.  Nor should the title similarity with
Stavig be ignored.  The established MAD/median principal-variable correlation
family also shows that robust marginal centering and scaling are not by
themselves novel.  Instead, the defensible contribution is the combined
methodological problem:

1. define a scientifically interpretable, generated robust-reference profile
   for Hoorn's divergence-similarity question;
2. derive complete first-order inference when median/MAD-scaled Huber
   references are estimated;
3. show that near-degenerate reference fitting **can cause, not always
   causes**, nonlocal switching and serious finite-sample distortion; and
4. establish \(I_n=\sqrt n\,\sigma_{\min}(J)\) as a **first-order organizer,
   not a universal cutoff**, while retaining the observed higher-order family
   residual as a limitation.

This is an inference-and-reliability contribution for a generated profile
estimand.  It is not a claim that \(\rho_P\) is a broadly new dependence
coefficient.  Its theory is **pointwise, not uniform**, and its robustification
is a **robust reference, not a globally robust correlation**.

## Manuscript-ready positioning paragraph

Stavig's (1982) absolute-deviation correlation is an important terminological
and technical comparator, but it does not target robust-reference profile
correlation.  Its interval version scores agreement through the normalized
absolute difference of signed marginal z scores; its ranked version is a
Spearman-footrule coefficient.  By contrast, our estimand correlates unsigned
distances from separately fitted median/MAD-scaled Huber locations.  The
novelty claimed here therefore does not rest on the absolute-value transform
or on introducing another general-purpose correlation coefficient.  It rests
on inference for a generated robust-reference profile, the finite-sample
failure induced by unstable reference fitting, and a conditioning diagnostic
that organizes that transition to first order.

## Claims not supported by the current evidence

- Do not call \(\rho_P\) the first absolute-deviation correlation.
- Do not claim that Stavig tests the same null or answers the same scientific
  question.
- Do not describe \(\rho_P\) as a globally robust correlation coefficient.
- Do not claim uniform Wald validity near degeneracy.
- Do not turn \(I_n\) into a universal operational gate or cutoff.
- Do not claim the source audit proves that no prior related construction
  exists.

## Primary sources

- Stavig, G. R. (1982). *The Absolute Deviation Correlation Coefficient*.
  Perceptual and Motor Skills, 54(1), 164--166.
  <https://doi.org/10.2466/pms.1982.54.1.164>
- Hoorn, J. F. (2025/2026). *Correlation of Divergence*.
  <https://arxiv.org/abs/2510.16717>
- Devlin, S. J., Gnanadesikan, R., & Kettenring, J. R. (1975). Robust
  estimation and outlier detection with correlation coefficients.
  <https://doi.org/10.1093/biomet/62.3.531>
- Shevlyakov, G. L., & Vilchevski, N. O. (2002). Minimax variance estimation
  of a correlation coefficient for epsilon-contaminated bivariate normal
  distributions. <https://doi.org/10.1016/S0167-7152(02)00058-5>
- Schechtman, E., & Yitzhaki, S. (1987). A measure of association based on
  Gini's mean difference. <https://doi.org/10.1080/03610928708829359>
- Székely, G. J., Rizzo, M. L., & Bakirov, N. K. (2007). Measuring and testing
  dependence by correlation of distances.
  <https://doi.org/10.1214/009053607000000505>
- Mantel, N. (1967). The detection of disease clustering and a generalized
  regression approach.
  <https://aacrjournals.org/cancerres/article/27/2_Part_1/209/476508/>
