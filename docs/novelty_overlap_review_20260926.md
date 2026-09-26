# Bounded novelty and overlap review — 2026-09-26

This is an internal, AI-assisted source review for the September 25 author
draft and the subsequent September 26 revision. It is not an exhaustive
priority search, independent mathematical peer review, or a recommendation
that the manuscript is ready to submit. The date suffix distinguishes this
pass; work began on September 25 local time. No experiment, implementation,
or author source was changed by this review.

## Decision

The defensible contribution is substantially narrower than introducing a
correlation of fitted distances. Magnitude correlation is established, and
Fout and Fosdick explicitly consider a centered, normalized correlation of
distances to estimated Fréchet means. In the Euclidean scalar case, that
construction is the sample correlation of distances to sample means.
Consequently, neither the absolute-value operation nor fitting marginal
centers before correlating radii can carry a novelty claim.

The present paper supplies a specific median/MAD-scaled Huber reference
construction, its paired influence expansion and pointwise inference under
stated conditions, and a worked failure mechanism with bounded empirical
evidence. Quantile linearization, estimated-center propagation, Z-estimation,
the delta method, and sandwich variance are established tools. The useful
scientific question is whether their complete specialization and the worked
finite-sample limitations are sufficiently informative, not whether the
individual tools are new.

Among the sources checked, no source was identified that supplies the exact
median -> raw MAD -> scaled Huber -> five paired moments -> uncapped Pearson
radius correlation chain together with this shared-sign failure analysis.
That statement describes this finite search; it does not establish that no
such prior work exists. Specifying a new combination of familiar components
does not by itself establish a substantial contribution.

## Closest-source matrix

| Source and inspected location | Supported overlap | What remains different or unverified |
|---|---|---|
| Afuecheta, Nadarajah and Chan (2023), *Folded Bivariate Distributions as Models for Magnitude Correlation*, REVSTAT 21(1), 21–38, DOI 10.57805/revstat.v21i1.395. Full published text: p.22 definition; p.24 Eq.(2.1); pp.28–35 applications. | Defines Corr(|X|,|Y|) and studies folded bivariate parametric families. With references fixed, our target is magnitude correlation of translated variables. | This paper's parametric models and likelihood fitting do not supply the present estimated median/MAD/Huber reference expansion. Its application diagnostics are not an IID design justification for our work. |
| Fout and Fosdick (2023), *Fréchet Covariance and MANOVA Tests for Random Objects in Multiple Metric Spaces*, arXiv:2306.12066v1, submitted June 21, 2023. Primary-source verification supplied by the root review: Eqs.(22)–(27), Theorem 1 and Section 5.3. | Centered covariance and normalized correlation of distances to Fréchet means are explicitly defined, including empirical counterparts with fitted means. In scalar Euclidean space the centered correlation is Corr(|X−E X|,|Y−E Y|), with sample means in its empirical version. This is a direct fitted-center radius-correlation antecedent. | Fréchet means differ from the present robust references. Theorem 1 treats consistency of their uncentered covariance; Lemma 1 concerns positive semidefiniteness, not consistency. Section 5.3 identifies missing asymptotic results for the particular proposed test contrasts. Do not broaden that sentence into a claim that every estimator in the paper lacks theory. No publication beyond the arXiv v1 record was verified in this pass. |
| Holzmann and Klar (2025; online 2024), *Lancaster correlation: A new dependence measure linked to maximum correlation*, Scandinavian Journal of Statistics 52(1), 145–169, DOI 10.1111/sjos.12733. Published full text, definitions and Theorem 1/Remark 1. | Correlations after transformations with estimated marginal ingredients already have moment/rank-based inference. The linear version is max(|Corr(X,Y)|, |Corr(check X²,check Y²)|), with marginal standardization; the rank version uses normal scores. Their maximum operation has distinct tied-component limit cases. | This is not a single radius-covariance target or the present robust-center chain. Gaussian agreement with |r| differs from our radius-correlation formula. Their confidence interval or independence-testing evidence cannot rank our weak-null procedure without aligning targets. |
| Segers (2014), *On the asymptotic distribution of the mean absolute deviation about the mean*, ISBA Discussion Paper 2014/26; arXiv:1406.4151. Full text, Lemma 2.1 and Corollary 3.2, with Eq.(3.4). | Already derives an absolute-moment expansion with an estimated center, including the joint direct/center fluctuation and a boundary-atom term. For continuous F at μ, IF for E|X−μ| is |x−μ|−θ + {P(X<μ)−P(X>μ)}(x−μ). The covariance of these terms is retained. An atom at μ contributes a nonlinear absolute-normal term to the limit. | It treats a univariate mean absolute deviation about the mean, not the median absolute deviation or paired radius correlation. Its atom-driven nonnormality is not our continuous zero-center-density shared-sign construction. No journal publication was verified; cite as a discussion paper if used. |
| Falk (1997), *On MAD and comedians*, Annals of the Institute of Statistical Mathematics 49, 615–644. Primary abstract and initial definitions inspected; detailed theorem pages were not reliably retrieved in this pass. | The comedian is med((X−med X)(Y−med Y)); robust covariance/correlation and empirical asymptotic normality with estimated medians are established topics. The abstract explicitly notes that knowing the population median need not improve MAD asymptotic efficiency. Thus neither estimated-median covariance propagation nor nuisance/direct cancellation is a new general idea. | A median of signed products is not Pearson correlation of unsigned radii. This review does not claim an exact theorem-to-assumption match or full-text certification. This is a high-value source for targeted human/full-text follow-up before making stronger comparisons. |
| Collins (2000), *Robustness comparisons of some classes of location parameter estimators*, Annals of the Institute of Statistical Mathematics 52, 351–366. Primary abstract inspected; full theorem/formula pages not verified. | Studies scale-invariant M-estimators using preliminary MAD or IQR, as well as Huber Proposal 2, under asymmetric contamination; asymptotic bias and variance effects of these location/scale constructions predate this project. | It does not establish the present paired radius-correlation target or failure construction on the evidence inspected. Do not cite a supposedly matching Huber IF formula without checking the exact normalization and full text. |

### Primary source links and retrieval levels

- Afuecheta et al., publisher: https://revstat.ine.pt/index.php/REVSTAT/article/view/395
- Fout and Fosdick, current inspected record and v1 text:
  https://arxiv.org/abs/2306.12066 and https://arxiv.org/html/2306.12066v1
- Holzmann and Klar, published author-hosted PDF:
  https://publikationen.bibliothek.kit.edu/1000172416/153641019
- Segers, full text: https://arxiv.org/pdf/1406.4151 ; institutional record:
  https://dial.uclouvain.be/pr/boreal/object/boreal%3A145260
- Falk, publisher-hosted PDF/abstract extraction:
  https://www.ism.ac.jp/editsec/aism/pdf/049_4_0615.pdf
- Collins, primary abstract: https://www.ism.ac.jp/editsec/aism/52/351.html

The Fout source assessment above incorporates the root review's direct reading
of the primary v1 text. It is not a claim that a second person independently
reviewed that theorem. A batch request to download further historical PDFs
was interrupted; those attempted downloads are not counted as completed
full-text checks.

## What is already covered by general theory

The existing manuscript's Hahn–Ridder and Ichimura–Newey citations correctly
acknowledge first-step influence propagation. For the present finite-dimensional
system, one may stack the median, MAD, Huber and moment equations. Subject to
the required nonsmooth linearizations and empirical-process conditions,
the influence is the usual inverse-Jacobian score expression, followed by a
smooth correlation delta method. Its covariance must be computed for intact
paired observations. Block-diagonal marginal derivative structure never
justifies deleting cross-margin score covariance.

The appendix's value is the explicit verification for the stated conventions,
moments, moving boundaries and implementation—not a new generic IF principle.
The reduced-moment weak-null empirical-norm argument is a particularly useful
specific obligation because a blanket five-moment population-L2 argument
would be invalid with infinite fourth moments. This bounded literature search
has not certified novelty of that argument.

The already cited Mazumder–Serfling median/MAD linearization and standard
empirical-process tools remain core antecedents. Einmahl–Mason (2005),
Theorem 1/Remarks 2 and 7, directly covers uniform-in-bandwidth methods and
data-dependent bandwidths. This supports context for S1.5; its global density
assumptions do not silently replace the local Gaussian-KDE argument in this
manuscript. Neither KDE consistency nor numerical root residual checks are
novelty claims on their own.

## Permutation and nonregularity boundaries

The DiCiccio–Romano and Yu–Hutson antecedents already establish that
studentization can matter for correlation permutation inference. The present
paper has not completed a matching weak-null conditional permutation CLT for
its generated profiles. The retained permutation results therefore remain
empirical stress evidence, not a new proved weak-null permutation method.

Nonregular quantile limits and failures of routine asymptotics are established
phenomena. Sharipov and Wendler (2013), *Normal limits, nonnormal limits, and
the bootstrap for quantiles of dependent data*, Statistics & Probability
Letters 83(4), 1028–1035, DOI 10.1016/j.spl.2012.12.017, is a relevant primary
preprint lead (https://arxiv.org/abs/1204.5633). Its abstract was checked; its
theorem assumptions were not matched to the shared-sign law in this pass.
Do not call the observation f(m)=0 or generic non-root-n median behavior new.

What may be distinctive here is the linked worked construction: a dependent
signed pair with independent population radii, correlated fitted location
errors even with population scale fixed, additional full-fit amplification,
and a sample covariance identity that retains empirical cross terms. The
four-stage intervention separates these paths empirically. It is more
specific than the generic statement that bad nuisance estimation can harm
inference. No source inspected in this pass supplied that exact construction,
but no global originality claim follows. The conditional n^(-1/4) heuristic
is still not a local-to-degeneracy theorem for the full median/MAD estimator.

## Reference-chain follow-up and stopping rule

Afuecheta et al. cite Hämäläinen's *Correlation in the Magnitude of Financial
Returns* (2015, University of Turku) and Psarakis–Panaretos (2001), *On some
bivariate extensions of the folded normal and the folded-t distributions*,
Journal of Applied Statistical Science 10, 119–136. The former's institutional
thesis search extract confirms magnitude-correlation and Gaussian-formula
discussion; its detailed inference section was not inspected. The latter is
a folded-distribution antecedent identified from the published reference list.
These are leads, not verified claims about a missing complete IF theorem.

Adding every such antecedent would dilute the paper. The immediate minimal
revision should cite Fout–Fosdick explicitly, retain Afuecheta and Lancaster,
and qualify the Section 3 derivation as a problem-specific application of
established inference principles. Segers is useful in a technical overlap
note or appendix if the estimated-center absolute-value argument is being
presented as novel. Falk and Collins warrant focused full-text follow-up only
if the manuscript claims priority for their already established ingredients.

Suggested contribution wording:

> We study pointwise inference for an established type of radius association
> when the radii are generated by median/MAD-scaled Huber references. We give
> an explicit paired influence expansion with implementation-matched
> regularity conditions, and a worked construction showing how correlated
> reference errors and further fitting amplification can distort finite-sample
> behavior. The contribution is this problem-specific theory and mechanism
> analysis, rather than a new correlation operation or a new general
> nuisance-adjustment method.

Independent expert review is still required for proof correctness and the
strength of the remaining contribution. No amount of citation expansion,
passing code tests, or additional favorable simulation cells replaces that
assessment.
