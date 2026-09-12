# Supplement S1. Regular inference: a paired Bahadur and Z-estimation proof

This supplement supplies the proof details used by Appendix A of the integrated
author draft. It concerns the uncapped profiles and a fixed regular IID law.
It is an author-level mathematical argument, not independent mathematical
peer review. The proof uses finite-dimensional quantile and Z-estimation
expansions; it does not require empirical measures to converge in total
variation, or assert a joint Hadamard theorem on an unspecified domain.

## S1.1 Conditions and conventions

Use Conditions R1–R5 in Appendix A: intact IID pairs; unique median and positive
raw MAD; continuous positive densities near the median and both MAD boundaries;
a unique Huber root with positive active probability and no boundary atoms;
positive profile variances and target IF variance; the stated moments;
consistent measurable empirical roots and negligible Huber score residual;
and locally uniformly consistent density estimates. All statements below are
pointwise at that law. Local parameter sets are deterministic and compact,
with scales and limiting denominators bounded away from zero.

For even sample size the median is the average of the two central order
statistics. The MAD applies that same convention to deviations from the
sample midpoint median. For odd size the middle order statistic is used.
There is no finite-sample correction to the raw MAD; the fixed factor
\(k=1.4826\) is applied afterward. This is the sample construction treated
by Mazumder and Serfling (2009). The proof uses its weak Bahadur expansion,
not a claim that sample quantiles solve indicator equations exactly.

Write \(P_n\) for the empirical law of intact pairs and
\(\mathbb G_n=\sqrt n(P_n-P)\). For a margin put
\(f_0=f(m)\), \(f_+=f(m+d)\), and \(f_-=f(m-d)\).
The paired versions of the marginal Bahadur expansions are

\[
\begin{aligned}
\sqrt n(\widehat m-m)
&=\frac{1}{\sqrt n}\sum_{i=1}^n
\frac{1/2-1\{W_i\le m\}}{f_0}+o_P(1),\\
\sqrt n(\widehat d-d)
&=\frac{1}{\sqrt n}\sum_{i=1}^n
\frac{1/2-1\{|W_i-m|\le d\}-(f_+-f_-)IF_m(W_i)}{f_++f_-}
+o_P(1).
\end{aligned}
\]

Each marginal remainder is negligible jointly because there are only two
margins. Their leading sums are paired and may be correlated.
Positive continuous boundary densities supply the local quantile
identification needed for these expansions. The midpoint convention is not
silently replaced by a lower empirical quantile.

## S1.2 Huber equation and the paired score system

Use the following fixed estimating-equation normalization, with
\(\theta_W=(m_W,d_W,T_W)^\top\):

\[
\xi_W(w;\theta_W)=
\begin{pmatrix}
1\{w\le m_W\}-1/2\\
1\{|w-m_W|\le d_W\}-1/2\\
\psi_c\{(w-T_W)/(kd_W)\}
\end{pmatrix}.
\]

Let \(U=(W-T)/(kd)\), \(A=P(|U|<c)\), and
\(B=P\{U1(|U|<c)\}\). The population derivative in the unscaled coordinates is

\[
J_{0W}=\begin{pmatrix}
f_0&0&0\\
f_+-f_-&f_++f_-&0\\
0&-B/d&-A/(kd)
\end{pmatrix}.
\]

The Huber equation is differentiable in \((T,s)\) at the population values:
\(\partial_T P\psi_c=-A/s\) and \(\partial_s P\psi_c=-B/s\).
The score is bounded and locally Lipschitz in location and positive scale.
Boundary no-mass conditions justify the displayed derivatives. Consistency,
local stochastic equicontinuity (S1.3), the MAD expansion, and
\(P_n\psi_c\{(W-\widehat T)/(k\widehat d)\}=o_P(n^{-1/2})\)
first give the root-n rate from the nonzero location derivative, then

\[
\sqrt n(\widehat T-T)=\frac{1}{\sqrt n}\sum_i
\left[\frac{s}{A}\psi_c\{(W_i-T)/s\}
-\frac{B}{A}kIF_d(W_i)\right]+o_P(1).
\]

Define \(\xi_{XY}(Z)=(\xi_X(X)^\top,\xi_Y(Y)^\top)^\top\) and
\(\Omega_{XY}=E(\xi_{XY}\xi_{XY}^\top)\). The mean score is zero.
The derivative is \(J_{0,XY}=\operatorname{diag}(J_{0X},J_{0Y})\), but
\(\Omega_{XY}\) is generally not block diagonal. Thus

\[
\sqrt n(\widehat\theta_{XY}-\theta_{XY})
=-J_{0,XY}^{-1}\frac{1}{\sqrt n}\sum_i\xi_{XY}(Z_i)+o_P(1).
\]

For a margin, standardize the *error* as
\(e_W=(\widehat\theta_W-\theta_W)/d_W\), using the population raw MAD.
Then \(J_W=d_WJ_{0W}\) and
\(\operatorname{Var}(e_W)\approx J_W^{-1}\Omega_WJ_W^{-\top}/n\),
where \(\Omega_W=E(\xi_W\xi_W^\top)\). This standardizes a local
perturbation; it is not the derivative of the nonlinear coordinate map
\((m/d,d/d,T/d)\). Arbitrary rescaling of the score equations changes the
singular values of \(J_W\). Positive affine changes of data units leave the
declared standardized derivative unchanged. Target projection and paired
score covariance remain necessary for the target variance.

## S1.3 Verification of the local empirical-process classes

Here is the class verification used for R6, under R1–R5. Use a compact
neighborhood with \(|T_X|,|T_Y|\le M\) and \(d\ge d_0>0\).
Measurable versions (or the usual separable versions of these finite-parameter
classes) are understood. Norms in this section are population norms unless
\(P_n\) is written explicitly.

**Indicators and signs.** Half-lines and intervals are VC set classes. The
classes \(1\{w\le t\}\), \(1\{|w-m|\le d\}\), and
\(1\{|w-T|<ckd\}\) therefore have polynomial covering numbers with envelope
one. Signs are affine transformations of half-line indicators, with the
value at equality treated separately on a probability-zero boundary.

**Clipped and active scores.** The clipped Huber score is bounded by \(c\).
On \(d\ge d_0\), its location derivative is bounded and its scale derivative
is bounded because an active standardized residual has magnitude at most
\(c\). It is a finite-dimensional Lipschitz class with a constant envelope.
The active score \(u1\{|u|<c\}\) is bounded by \(c\) but jumps at its knots.
On each of the finitely many regions separated by \(T\pm ckd\), its
subgraph inequalities become linear inequalities after multiplication by
the positive \(kd\). Their finite unions and intersections have finite VC
dimension. No mass at the limiting knots gives \(L_2(P)\) continuity.

**Translated radii and moments.** The following pointwise bounds establish
Euclidean parameter covers with the indicated envelopes:

\[
\begin{aligned}
\big||x-t|-|x-t'|\big|&\le |t-t'|,\\
|(x-t)^2-(x-t')^2|&\le |t-t'|(2|x|+2M),\\
\big||x-t||y-u|-|x-t'||y-u'|\big|
&\le |t-t'|(|y|+M)+|u-u'|(|x|+M).
\end{aligned}
\]

Envelopes are \(|X|+M\), \((|X|+M)^2\), and
\((|X|+M)(|Y|+M)\), respectively. The general-correlation moments in R4
make these square integrable. For the reduced three-moment vector used for
\(C\), omit the squared-radius classes; the reduced moments in S1.6 suffice.

**Weighted moving signs.** For example,
\(\operatorname{sign}(x-t)|y-u|\) has envelope \(|Y|+M\).
Partition its subgraph by \(x\le t\) and \(y\le u\).
On each of four regions the function equals one of
\(y-u,u-y,-(y-u),-(u-y)\). The subgraph is a finite Boolean combination of
half-spaces in \((x,y,z)\); consequently the class has polynomial VC covers.
Its continuity at \((T_X,T_Y)\) follows from dominated convergence: the
squared difference is bounded by a constant times \(1+Y^2\), and pointwise
convergence fails only at the probability-zero moving-sign boundary.
The other margin is identical with X and Y interchanged. Dependence within
a pair does not invalidate domination.

**Finite IF closure and random coefficients.** Treat every fitted scalar
coefficient (density evaluations, A, B, moments, and smooth ratios) as an
additional coordinate in a deterministic compact set containing its limit.
Denominators are bounded away from zero on that set. Finite sums of the
classes above and multiplication by bounded scalar coefficients retain
polynomial entropy: cover each summand at accuracy proportional to the
desired total accuracy and take the product of the finitely many covers.
This argument does not assert that arbitrary products of unbounded Donsker
classes are Donsker.

For the full IF an envelope is
\(H=K(1+|X|+|Y|+X^2+Y^2+|XY|)\); for the reduced IF omit X-squared and
Y-squared. The appropriate moment condition gives \(PH^2<\infty\).
Polynomial entropy and the square-integrable envelope give the needed
Donsker conclusion. They also give Glivenko–Cantelli control. To handle the
squared IF class, truncate all influences to \([-L,L]\), use the Lipschitz
square map there, and bound the discarded tails uniformly by
\(H^2 1\{H>L\}\). Its population expectation tends to zero; for each fixed
L its empirical mean converges by the ordinary law of large numbers.
Letting L grow proves the squared-class GC assertion with an integrable
envelope, without requiring an eighth moment.

These are the VC/Euclidean entropy and closure routes of van der Vaart and
Wellner (1996) and van der Vaart (1998). After localization and the displayed
\(L_2(P)\) continuity, estimated-function stochastic equicontinuity gives
\(\mathbb G_n(f_{\widehat\theta}-f_{\theta_0})=o_P(1)\)
(van der Vaart and Wellner, 2007). Thus R6 is connected to concrete classes
and envelopes rather than left as an unexplained assumption. Independent
review of this verification remains outstanding.

## S1.4 Joint moments and the population Taylor remainder

Put \(a=|X-T_X|\), \(b=|Y-T_Y|\). Away from an atom at the reference,
the population derivative of \(P|X-t|\) at \(T_X\) is
\(-P\operatorname{sign}(X-T_X)\). One useful remainder bound is

\[
\big||x-T-h|-|x-T|+h\operatorname{sign}(x-T)\big|
\le 2|h|1\{|x-T|\le |h|\}.
\]

Its expectation is \(o(|h|)\). In the paired product the corresponding
bound is weighted by b (or a); integrability and no boundary atom imply
\(P[b1\{|X-T_X|\le |h|\}]\to0\). The product of the two residual changes
is bounded by \(|h_Xh_Y|\). The squared-radius expansion is algebraically
exact up to the shift squared. With root-n nuisance errors these give
\(o_P(n^{-1/2})\) population remainders. S1.3 controls the empirical
random-index remainders. Therefore

\[
\sqrt n(\widehat M-M)=n^{-1/2}\sum_i IF_M(Z_i)+o_P(1),
\quad M=(\nu,\mu_a,\mu_b,q_a,q_b)^\top,
\]

with the complete influences in Section 3. The finite-dimensional
correlation map is differentiable at positive profile variances. Its
gradient gives \(IF_\rho=\nabla\rho_P^\top IF_M\); R4 makes its variance
finite. The IID CLT then proves the unstudentized conclusion of Theorem 1.

## S1.5 Density plug-ins and empirical variance consistency

Uniform density consistency near \(m,m\pm d\), combined with consistent
random evaluation points and continuity of f, yields consistency of every
plug-in boundary density. For the implemented Gaussian KDE,

\[
\widehat f_h(t)=\frac1{nh}\sum_i\phi\{(W_i-t)/h\},\qquad
\widehat h=1.06\widehat\sigma_W n^{-1/5},
\]

\(\widehat\sigma_W\) is the ordinary sample standard deviation with divisor
\(n-1\). Finite nonzero variance gives
\(\widehat h/(1.06\sigma_W n^{-1/5})\to_P1\). On a probability-tending-to-one
event h lies in a deterministic band \([c_1n^{-1/5},c_2n^{-1/5}]\).
Gaussian translation/scale entropy yields a uniform stochastic bound over
that band tending to zero, since \(nh/\log n\to\infty\).
Local uniform continuity controls kernel bias on a slightly smaller compact
neighborhood; the Gaussian tails and integrability of the density control
the outside contribution. This supplies a route to R5 for the default KDE,
with the uniform kernel-density theory of Giné and Guillou (2002).
Consistency at random boundaries is not deduced solely from fixed-point KDE
consistency. Analytic and cross-fit options exist in the software; they are
not the default method in the main studies and require their own matching
conditions if used.

Localize the fitted scalar coefficients as in S1.3. Pointwise convergence
outside null boundaries and domination by H give
\(\|\widehat{IF}_\rho-IF_\rho\|_{P,2}=o_P(1)\). For the in-sample variance,

\[
\begin{aligned}
P_n\widehat{IF}_\rho^2-PIF_\rho^2
={}&(P_n-P)(\widehat{IF}_\rho^2-IF_\rho^2)\\
&+P(\widehat{IF}_\rho^2-IF_\rho^2)+(P_n-P)IF_\rho^2.
\end{aligned}
\]

The terms vanish by squared-class GC, Cauchy–Schwarz and function-norm
consistency, and the ordinary LLN, respectively. The first-moment argument
justifies empirical centering. Thus the sample variance of the paired
plug-in influences is consistent; Slutsky yields the Wald conclusion.

## S1.6 Secondary C and the weaker-moment null route

For C use only \(M_C=(\nu,\mu_a,\mu_b)^\top\) and
\(E\{a^{2+\eta}+b^{2+\eta}+(ab)^{2+\eta}\}<\infty\) for some \(\eta>0\).
The reduced class, Taylor expansion and variance argument give

\[
IF_C=\frac{IF_\nu}{\mu_a\mu_b}
-C\frac{IF_{\mu_a}}{\mu_a}-C\frac{IF_{\mu_b}}{\mu_b}.
\]

No root-n CLT for \(q_a,q_b\) is imported under these reduced conditions.
At \(\rho_P=0\), the correlation numerator uses the same three-moment
expansion and its denominator needs only consistency. The squared-moment
gradient coefficients vanish at the null, giving the reduced null influence.

For the unrestricted empirical studentizer, \(\widehat\rho_P=O_P(n^{-1/2})\).
Finite second moments imply

\[
\frac{P_na^4}{n}\le\frac{\max_i a_i^2}{n}P_na^2=o_P(1),\qquad
\widehat\rho_P^2P_na^4=o_P(1).
\]

For fitted radii use \(\widehat a_i\le a_i+|\widehat T_X-T_X|\), hence
\(P_n\widehat a^4\le8P_na^4+8|\widehat T_X-T_X|^4\); the same control
applies. Empirical Cauchy–Schwarz controls cross terms with the reduced IF.
This establishes empirical-norm negligibility of the extra quadratic terms.
When fourth moments are infinite it does **not** establish population
\(L_2(P)\) consistency of an unrestricted plug-in IF having a nonzero
squared-profile coefficient. This null argument is not a general nonzero
effect confidence theorem.

## S1.7 Software boundary

The mathematical procedure requires exact or sufficiently accurate empirical
Huber roots. The public API implements iteratively reweighted location updates
from the sample median, at most 100 iterations, stopping when the location
change is below \(10^{-10}\max(1,\widehat s)\). It does not enforce an
n-dependent score-residual bound. Neither a fixed tolerance nor these finite
replays prove the asymptotic root condition. Section S3.6 records the two
flagged full fits and their bracketed sensitivity checks. The public solver
and its defaults have not been changed during manuscript integration.

This closes the presentation of the proof route, local classes, moving
boundaries, random coefficients, and density evaluation. It does not certify
independent mathematical acceptance or a uniform software convergence theorem.
