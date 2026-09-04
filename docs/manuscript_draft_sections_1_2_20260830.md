# Trustworthy Inference for Robust-Reference Divergence Profiles

## Regularity, Reference Instability, and Nuisance Conditioning

Working manuscript draft, Sections 1--2  
Date: 2026-08-30

> Editorial note: the original paper is archived as Hoorn (2025),
> arXiv:2510.16717. The online version inspected on 2026-08-31 was v2, revised
> 2026-03-08. Its Eq. 4 still lacks the planned \(1/n\) numerator correction,
> so version-specific wording must be checked again after the next arXiv
> revision. Targeted methodological citations remain for the literature pass.

## 1. Introduction

Many paired-data questions concern more than whether two measurements move in
the same direction. In some applications, the scientifically relevant pattern
is whether the same observational units are internally unusual in two domains:
if unit \(i\) is far from the other observations in group or variable \(X\),
is its matched observation also far from the other observations in \(Y\)? A
statistic for this question should preserve the labels linking the two
datasets while summarizing how strongly each labelled observation stands out
inside its own marginal distribution.

The correlation-of-divergency coefficient \(c_d\) was introduced for this
purpose by constructing an all-to-all within-group divergence score for every
observation and comparing the two resulting labelled profiles [Hoorn (2025),
arXiv:2510.16717]. This construction asks whether
two groups are internally divergent in a similar way. It is distinct from an
ordinary correlation between the raw measurements, because observations may
occupy very different numerical positions while retaining similar relative
salience within their respective groups. It is also distinct from comparing
two complete distance matrices: the all-to-all distances are first compressed
to one divergence score per labelled observation.

The present paper studies a related but different construction. Instead of
forming each observation's divergence from every other observation, we fit a
robust marginal reference and define the profile by the observation's distance
from that reference. Specifically, the reference is a Huber location whose
scale is obtained from the median absolute deviation (MAD). The resulting
profiles preserve the original paired-salience question—whether the same
labels are relatively far from their respective groups—but replace the
all-to-all profile by a robust-reference radial profile. This replacement
changes the statistical functional and its interpretation; it is not merely a
new computational formula for the original \(c_d\).

That change also shifts the main purpose of the paper. Our primary question is
not how to introduce another general-purpose coefficient. It is when inference
for robust-reference profile similarity can be trusted. The reference is
estimated from the same observations used to construct the profiles. Under
regular marginal identification, this generated-reference step can be handled
by a complete functional delta method. When the marginal distribution has a
thin central bridge, separated modes, or another geometry that weakly
identifies the reference, however, small empirical fluctuations can move the
fitted location nonlocally. The fitted profiles may then appear strongly
aligned even when the population profile correlation is zero. Robustness of a
location equation to ordinary contamination does not by itself prevent this
reference-selection failure.

This distinction is also necessary relative to established correlation
methods. Stavig's (1982) interval absolute-deviation coefficient is a
normalized \(L_1\) discrepancy between *signed* marginal standard scores, and
its ranked version is a Spearman-footrule form. Robust median/MAD correlation
estimators instead obtain signed raw-value association from robust scales of
principal sums and differences (Shevlyakov and Vilchevski, 2002). Neither
targets correlation between two *unsigned* marginal radius profiles. We do
not claim novelty for applying an absolute-value transform, using MAD/Huber
ingredients, or propagating estimated nuisance parameters in general. The
contribution is the problem-specific combination of a robust-reference
profile estimand, its complete inference, an isolated reference-switching
failure, and a conditioning diagnostic for that failure.

We take the population correlation of the two robust-reference radius
profiles as the primary estimand,

\[
\rho_P
=\operatorname{Corr}\{|X-T_X|,|Y-T_Y|\},
\]

where \(T_X\) and \(T_Y\) are marginal Huber location functionals fitted with
MAD-based scales. This quantity lies in \([-1,1]\) and directly represents
standardized concordance of labelled profile salience. We retain the
normalized cross-moment scale

\[
C
=\frac{E\{|X-T_X||Y-T_Y|\}}
{E|X-T_X|\,E|Y-T_Y|}
\]

as a secondary effect measure and as a link to the historical \(c_d\) scale.
The identity

\[
C=1+\rho_P\,CV(|X-T_X|)CV(|Y-T_Y|)
\]

shows why the two quantities should not be interpreted interchangeably.
Whereas \(\rho_P\) isolates profile concordance, \(C-1\) additionally weights
that concordance by the marginal heterogeneity of both radius profiles. The
two statistics have identical fixed-margin permutation rankings, but they are
different population effect scales and need not have identical Wald
uncertainty statements.

The paper makes three main contributions. First, for fixed regular IID laws,
we derive the complete influence function of \(\widehat\rho_P\), including the
effects of the marginal medians, both MAD boundaries, the MAD-to-Huber scale
path, and the covariance induced by observing \((X,Y)\) as a pair. Under the
stated density, moment, uniqueness, and nondegeneracy conditions, this yields
pointwise asymptotic normality and consistent plug-in studentization. At the
global independence null, the first-order contribution of marginal reference
estimation cancels, although higher-order skewness and self-normalization can
still cause slow finite-sample convergence.

Second, we construct a continuous weak-null family in which the
robust-reference system is nearly degenerate. In that family, empirical mode
imbalance moves the fitted references and can create severe finite-sample
distortion. Paired interventions that fix the population reference or enforce
exact sign balance isolate reference fitting as the mechanism in this
construction. These examples establish that near-degenerate reference fitting
*can* invalidate ordinary first-order approximations in finite samples; they
do not imply that every multimodal distribution fails or that the distortion
must always have the same sign.

Third, we study the dimensionless nuisance-conditioning quantity

\[
I_n=\sqrt n\,\sigma_{\min}(J),
\]

where \(J\) is the standardized Jacobian of the median/MAD/Huber estimating
system. Linearization suggests that error in the least-identified standardized
nuisance direction is amplified at order \(1/I_n\). Across matched bridge
families and sample sizes, \(I_n\) organizes much of the observed transition
from severe distortion toward calibration and transports to a prospectively
held-out family. It does not fully determine finite-sample behavior: families
with nearly identical first-order Jacobians retain different rejection rates.
We therefore treat \(I_n\) as an explanatory and cautionary diagnostic, not as
a universal cutoff or a data-driven accept/reject gate.

These contributions give a precise meaning to a “safer” development of the
original idea. Safety does not mean that a robust reference automatically
prevents misleading inference. It means that the estimand is explicit, the
regularity conditions are stated, a concrete failure mechanism is exhibited,
and proximity to weak reference identification is studied rather than hidden.
The theory is pointwise and IID. Exact randomization inference additionally
requires invariance under the declared permutation group; the weak null
\(\rho_P=0\) alone does not supply that invariance. A conditional weak-null
permutation central limit theorem is outside the claims of this paper.

The remainder of the paper is organized as follows. Section 2 defines the
robust-reference profiles, the primary and secondary estimands, their sample
versions, and their relation to the original all-to-all construction. Section
3 gives regular IID influence-function inference. Section 4 develops the
near-degenerate reference-switching example. Section 5 introduces nuisance
conditioning and the index \(I_n\). Section 6 consolidates the simulations by
claim rather than chronology. The final sections discuss practical reporting,
the boundary of randomization claims, and higher-order and structured-data
extensions.

## 2. Robust-reference divergence profiles

### 2.1 Paired observations and marginal robust references

Let \(Z=(X,Y)\sim P\), where \(X\) and \(Y\) are measurements on the same
labelled observational unit under two variables, domains, or conditions. The
pairing is scientifically meaningful: relabelling \(Y\) changes the
cross-profile association even though it leaves both marginal distributions
unchanged. Let \(P_X\) and \(P_Y\) denote the two marginal laws.

For a generic marginal variable \(W\), define

\[
m_W=\operatorname{Med}(W),\qquad
d_W=\operatorname{Med}|W-m_W|,\qquad
s_W=k d_W,
\]

where \(k>0\) is fixed. The implementation uses the normal-consistency
constant \(k=1.4826\). Given a fixed clipping constant \(c>0\), the population
Huber reference \(T_W=T(P_W)\) is the selected solution of

\[
E\left[
\psi_c\left(\frac{W-T_W}{s_W}\right)
\right]=0,
\qquad
\psi_c(u)=\max\{-c,\min(u,c)\}.
\]

Our default implementation uses \(c=1.345\). The theory treats \(c\) and
\(k\) as fixed constants and requires the median, MAD, and Huber roots to be
uniquely and regularly identified. These requirements matter: a bounded Huber
score controls the response of its estimating equation to large residuals,
but it does not guarantee uniqueness or strong curvature of the population
reference equation.

Define the two nonnegative population radius profiles

\[
a_P(X)=|X-T_X|,\qquad
b_P(Y)=|Y-T_Y|,
\]

where \(T_X=T(P_X)\) and \(T_Y=T(P_Y)\). Dividing either profile by its own
positive marginal scale does not change the correlation or the normalized
cross-moment below. We therefore use unscaled radii in the notation while
retaining the MAD scale in the definition of each Huber reference.

### 2.2 Primary profile-correlation estimand

Write

\[
\mu_a=E_P\{a_P(X)\},\qquad
\mu_b=E_P\{b_P(Y)\},
\]

\[
q_a=E_P\{a_P(X)^2\},\qquad
q_b=E_P\{b_P(Y)^2\},\qquad
\nu=E_P\{a_P(X)b_P(Y)\},
\]

and let

\[
v_a=q_a-\mu_a^2,qquad v_b=q_b-\mu_b^2.
\]

Whenever \(v_a>0\) and \(v_b>0\), the primary estimand is

\[
\rho_P(P)
=\frac{\nu-\mu_a\mu_b}{\sqrt{v_av_b}}
=\operatorname{Corr}_P\{a_P(X),b_P(Y)\}.
\]

A positive value means that labels far from the robust reference in one
margin tend also to be far from the reference in the other; labels close to
one reference likewise tend to be close to the other. A negative value means
that high salience in one profile tends to coincide with low salience in the
other. The value zero is a weak profile-covariance null. It does not imply
independence of \(X\) and \(Y\), equality of their marginal distributions, or
exchangeability of pairing labels.

The use of correlation is deliberate. It separates alignment of the two
labelled profiles from their marginal units and heterogeneity, provides the
familiar range \([-1,1]\), and answers the direct scientific question of
whether the profiles are similar. It is not intended as a general dependence
coefficient: nonlinear dependence may remain when \(\rho_P=0\), and different
joint distributions can share the same profile correlation.

### 2.3 Secondary normalized cross-moment scale

For continuity with the original correlation-of-divergency scale, define

\[
C(P)=\frac{\nu}{\mu_a\mu_b},
\]

provided \(\mu_a\mu_b>0\). Since the profiles are nonnegative, \(C\) compares
the observed paired radius product with the product expected from the two
marginal mean radii. Let

\[
CV(a_P)=\frac{\sqrt{v_a}}{\mu_a},\qquad
CV(b_P)=\frac{\sqrt{v_b}}{\mu_b}.
\]

Then

\[
\begin{aligned}
C
&=\frac{\mu_a\mu_b+\operatorname{Cov}\{a_P(X),b_P(Y)\}}
        {\mu_a\mu_b}\\
&=1+\rho_P\,CV(a_P)CV(b_P).
\end{aligned}
\]

Consequently, \(C=1\) and \(\rho_P=0\) describe the same weak-null boundary
when both profile means and variances are positive. Their effect
interpretations differ away from that boundary. At the same \(\rho_P\), \(C\)
moves as either marginal profile becomes more heterogeneous. In the frozen
estimand audit, holding population \(\rho_P=0.30\) fixed while changing only
the marginal profile variation moved \(C\) from \(1.019\) to \(3.546\).
Accordingly, we report \(C\) only as a secondary or historically linked
effect and accompany it with both marginal profile coefficients of variation.

### 2.4 Sample construction

For paired IID observations \(Z_i=(X_i,Y_i)\), \(i=1,\ldots,n\), fit each
marginal reference separately. Let \(\widehat m_X\) be the sample median and

\[
\widehat d_X=\operatorname{Med}_n|X_i-\widehat m_X|,
\qquad \widehat s_X=k\widehat d_X.
\]

The implementation uses the midpoint convention: for even \(n\), the median
is the average of the two central order statistics, and the same convention is
applied to the absolute deviations when calculating the MAD. Select
\(\widehat T_X\) as the empirical Huber root

\[
\frac1n\sum_{i=1}^n
\psi_c\left(\frac{X_i-\widehat T_X}{\widehat s_X}\right)=0,
\]

and define \(\widehat T_Y\) analogously. The fitted profiles are

\[
\widehat a_i=|X_i-\widehat T_X|,
\qquad
\widehat b_i=|Y_i-\widehat T_Y|.
\]

With \(\bar a=n^{-1}\sum_i\widehat a_i\) and
\(\bar b=n^{-1}\sum_i\widehat b_i\), the sample profile correlation is

\[
\widehat\rho_P
=\frac{\sum_{i=1}^n(\widehat a_i-\bar a)
                         (\widehat b_i-\bar b)}
       {\left\{\sum_{i=1}^n(\widehat a_i-\bar a)^2
                    \sum_{i=1}^n(\widehat b_i-\bar b)^2\right\}^{1/2}},
\]

and the secondary estimator is

\[
\widehat C
=\frac{n^{-1}\sum_{i=1}^n\widehat a_i\widehat b_i}
       {\bar a\bar b}.
\]

If a marginal mean radius or profile variance is zero, the corresponding
estimand is undetermined from those data rather than evidence of no profile
association. The regular theory therefore assumes positive population means
and variances and consistent selection of the empirical nuisance roots.

### 2.5 Relation to the original all-to-all profile

The robust-reference construction retains the original labelled-salience
motivation but is not algebraically identical to the all-to-all profile. To
make the distinction explicit, consider the implemented one-dimensional L2
row divergence

\[
D_i
=\left\{\frac{1}{n-1}\sum_{j\ne i}(X_i-X_j)^2\right\}^{1/2}.
\]

If \(\bar X=n^{-1}\sum_iX_i\) and
\(s_X^2=n^{-1}\sum_i(X_i-\bar X)^2\), then

\[
D_i^2
=\frac{n}{n-1}\{(X_i-\bar X)^2+s_X^2\}.
\]

Thus, although \(D_i\) is computed from all pairwise differences involving
unit \(i\), in one dimension it is a nonlinear transform of distance from the
sample mean with a common variance floor. The new profile instead uses direct
distance from an explicitly fitted robust location. Replacing \(\bar X\) by a
Huber reference and removing the variance floor changes both the sample
profile and the population target. Neither construction is a uniformly
superior representation: the appropriate question depends on whether the
scientific target is all-to-all internal divergence or salience relative to a
robust marginal reference.

Both constructions compress within-group geometry to one score per labelled
observation. Neither, by itself, establishes similarity of the complete
pairwise distance matrices. Claims about full relational geometry require a
matrix-level target and inference procedure rather than a profile
correlation.

### 2.6 Fixed-margin permutation ordering and inference boundary

For any fixed nonconstant fitted profile vectors \(\widehat a\) and
\(\widehat b\), and any permutation \(\pi\) of the second profile,

\[
\widehat C_\pi
=1+\widehat\rho_{P,\pi}\,
CV_n(\widehat a)CV_n(\widehat b).
\]

The two CV factors are positive and unchanged over the permutation orbit.
Here \(CV_n\) denotes the empirical coefficient of variation using the same
population-denominator convention as the displayed sample moments.
Therefore \(\widehat C_\pi\) and \(\widehat\rho_{P,\pi}\) have identical
one-sided ranks when centred at \(1\) and \(0\), respectively. This explains
why selecting \(\rho_P\) as the primary effect does not discard the historical
fixed-margin permutation evidence.

This algebraic ordering is not itself an inference theorem. Exact
randomization validity requires the conditional joint law of the labels to be
invariant under the declared permutation group. The weak null
\(\rho_P=0\), equivalently \(C=1\), does not generally imply that invariance.
Moreover, when the reference is recomputed after relabelling, the statistic
and its studentizer must be treated as complete orbit-specific quantities.
Section 3 therefore uses full influence-function Wald inference for the
regular IID weak null; later permutation results are labelled according to
their empirical or group-invariance status.

### 2.7 Interpretation carried forward

The remainder of the paper uses “profile similarity” to mean association of
the labelled robust-reference radii, not raw-value correlation, marginal
distributional equality, independence, or complete distance-matrix
agreement. We use \(\rho_P\) as the lead scientific effect because it isolates
that association. We retain \(C\) to preserve contact with the original
correlation-of-divergency scale and to describe settings in which weighting by
marginal salience heterogeneity is scientifically intentional.

This separation also clarifies the inferential problem. Estimating
\(\rho_P\) is not merely calculating a Pearson correlation of two observed
vectors: both vectors depend on estimated marginal functionals. Section 3
derives the complete first-order effect of that generated-reference step and
states the conditions under which the resulting studentized inference is
valid.
