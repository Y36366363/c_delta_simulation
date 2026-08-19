# Appendix: asymptotic theory for robust paired-salience concordance

Date: 2026-08-19
Audit revision: 2026-08-19

## A.1 Scope and notation

This appendix treats the one-dimensional, uncapped, continuous-margin
statistic. The Huber-profile correlation is the primary estimand and the
historical c_delta scale is a smooth secondary estimand.

Let \(Z_i=(X_i,Y_i)\), \(i=1,\ldots,n\), be iid from \(P\). For a generic
margin \(W\), define

\[
m=\operatorname{Med}(W),\qquad
d=\operatorname{Med}|W-m|,\qquad s=kd,
\]

where \(k>0\) is fixed. Let \(T\) be the unique solution of

\[
E\left[\psi_c\left(\frac{W-T}{s}\right)\right]=0,
\qquad
\psi_c(u)=\max(-c,\min(u,c)).
\]

For the two margins, put

\[
a=|X-T_X|,\qquad b=|Y-T_Y|,
\]

and define

\[
\mu_a=E(a),\quad \mu_b=E(b),\quad \nu=E(ab),
\quad q_a=E(a^2),\quad q_b=E(b^2).
\]

The two effect scales are

\[
C(P)=\frac{\nu}{\mu_a\mu_b}
\]

and

\[
\rho_P(P)=
\frac{\nu-\mu_a\mu_b}
{\{(q_a-\mu_a^2)(q_b-\mu_b^2)\}^{1/2}}.
\]

Whenever both profile variances are positive,

\[
C=1+\rho_PCV(a)CV(b).
\]

## A.2 Assumptions

Assume:

**A1 (iid sampling).** The pairs \(Z_i\) are iid. If buildings are the
independent units, the theorem requires a separate cluster-level formulation
and does not authorize room-level iid inference.

**A2 (regular median and MAD).** For each margin, the median \(m\) is unique,
\(d>0\), and the marginal cdf has a density \(f\) that is continuous and
strictly positive in neighbourhoods of \(m\), \(m-d\), and \(m+d\).

**A3 (regular Huber root).** The Huber equation has a unique root \(T\),

\[
A=P(|U|<c)>0,\qquad U=(W-T)/(kd),
\]

and the distribution has no mass at \(T\) or \(T\pm ckd\).

**A4 (profile nondegeneracy).** The means \(\mu_a,\mu_b\) and variances

\[
v_a=q_a-\mu_a^2,\qquad v_b=q_b-\mu_b^2
\]

are strictly positive. The asymptotic variance of the estimand under
consideration is also strictly positive.

**A5-C (moments for \(C\)).** For some \(\eta>0\),

\[
E\{a^{2+\eta}+b^{2+\eta}+(ab)^{2+\eta}\}<\infty.
\]

For asymptotic normality of \(C\), the corresponding second moments suffice;
the \(2+\eta\) margin is retained for plug-in uniform integrability.

**A5-\(\rho\) (moments for \(\rho_P\)).** For some \(\eta>0\),

\[
E\{a^{4+\eta}+b^{4+\eta}+(ab)^{2+\eta}\}<\infty.
\]

This stronger condition is used for inference at a general, possibly nonzero
\(\rho_P\), because \(IF_\rho\) then contains \(a^2-q_a\) and
\(b^2-q_b\). A generic \(2+\eta\) marginal moment with arbitrarily small
\(\eta\) is not enough for that general \(IF_\rho\in L_2(P)\) claim. At the
weak null \(\rho_P=0\), both squared-moment gradient coefficients vanish and
the moment condition can be relaxed; see Corollary A.2.

**A6 (empirical roots).** The selected empirical medians, MADs, and Huber
roots are measurable and consistent. Generalized empirical quantile roots
satisfy their estimating equations up to \(o_P(n^{-1/2})\).

**A7 (density plug-in).** The density estimators used at the median and the
two MAD boundaries are uniformly consistent on fixed neighbourhoods of those
points. For a kernel estimator, one sufficient route is local uniform
continuity and boundedness of \(f\), a kernel whose translation/scale class
satisfies the standard uniform-entropy conditions, a regular bandwidth with
\(h_n\to0\), and \(nh_n/\log(1/h_n)\to\infty\) in one dimension. Uniform
consistency makes evaluation at the random consistent median and MAD
boundaries legitimate.

**A8 (local empirical-process classes).** With probability tending to one,
the fitted nuisance vector lies in a fixed compact neighbourhood
\(\Theta_0\) of the population value on which all denominators in the
influence formula are bounded away from zero. For inference on \(C\), use the
class below without the last two squared-moment functions; for inference on
\(\rho_P\), use the full class. The relevant class is \(P\)-Donsker where
used at root-\(n\) scale, and its finite linear influence-function closure and
squared closure are \(P\)-Glivenko–Cantelli where used for variance
consistency:

\[
\begin{aligned}
\mathcal F_1
=\{&
1(w\le t),\
1(|w-m|\le d),\
\psi_c((w-T)/(kd)),\\
&1(|u|<c),\ u1(|u|<c),\
\operatorname{sign}(w-T),\ w-T,\\
&|x-T_X|,\ |y-T_Y|,\
|x-T_X||y-T_Y|,\\
&\operatorname{sign}(x-T_X)|y-T_Y|,\
\operatorname{sign}(y-T_Y)|x-T_X|,\\
&(x-T_X)^2,\ (y-T_Y)^2:
(m,d,T_X,T_Y)\in\Theta_0\}.
\end{aligned}
\]

Here \(u=(w-T)/(kd)\). The indicator, sign, active-score, and clipped-score
subclasses are VC-type or bounded transformations of VC-type classes. The
moment subclasses and their displayed products are finite-dimensional
Lipschitz/Euclidean classes with envelopes controlled by

\[
1+|X|+|Y|+X^2+Y^2+|XY|.
\]

A5-C makes the reduced-class envelopes integrable for \(C\), and
A5-\(\rho\) does so for the full class. Thus A8 may be verified from standard
VC/Euclidean-class closure results rather than treated as an independent
modelling restriction; it is stated explicitly to expose the
stochastic-equicontinuity and in-sample variance steps.

For a pathwise statement, let \(\mathcal T\) consist of signed tangent
measures \(h\) with total mass zero, the weighted variation required by the
relevant moment assumption, and marginal cdf perturbations continuous at
\(m\) and \(m\pm d\). This excludes an atom inserted exactly at a quantile
boundary, where a convention-dependent one-sided derivative can occur. The
continuous iid empirical-process tangent is covered.

## A.3 Marginal nuisance derivative

For a marginal tangent \(h\), write

\[
H(t)=\int 1(w\le t)\,dh(w).
\]

### Lemma A.1 (median and MAD)

Under A2, the median and MAD maps are Hadamard differentiable tangentially to
\(\mathcal T\), with

\[
\dot m[h]=-\frac{H(m)}{f(m)}
\]

and

\[
\dot d[h]=-
\frac{
H(m+d)-H(m-d)+\{f(m+d)-f(m-d)\}\dot m[h]
}{f(m+d)+f(m-d)}.
\]

#### Proof

The median satisfies \(F(m)=1/2\). For a differentiable path
\(F_t=F+tH+o(t)\) and \(m_t=m+t\dot m+o(t)\),

\[
0=H(m)+f(m)\dot m.
\]

The MAD is the positive solution of

\[
F(m+d)-F(m-d)=1/2.
\]

Expansion of the two moving boundaries gives

\[
0=H(m+d)-H(m-d)
+\{f(m+d)-f(m-d)\}\dot m
+\{f(m+d)+f(m-d)\}\dot d.
\]

The denominator is positive by A2. The quantile Hadamard-differentiability
theorem makes these expansions uniform on the declared tangent set. ∎

For the contamination tangent \(h=\Delta_z-P\),

\[
IF_m(z)=\frac{1/2-1(z\le m)}{f(m)}
\]

and

\[
IF_d(z)=
\frac{
1/2-1(|z-m|\le d)
-\{f(m+d)-f(m-d)\}IF_m(z)
}{f(m+d)+f(m-d)}.
\]

### Lemma A.2 (Huber location with MAD scale)

Under A2–A3, let

\[
B=E\{U1(|U|<c)\}.
\]

Then

\[
\dot T[h]
=\frac{s}{A}\int\psi_c\left(\frac{w-T}{s}\right)dh(w)
-\frac{B}{A}\dot s[h],
\qquad \dot s[h]=k\dot d[h].
\]

Consequently,

\[
IF_T(z)=
\frac{s}{A}\psi_c\left(\frac{z-T}{s}\right)
-\frac{B}{A}IF_s(z).
\]

#### Proof

Let

\[
\Psi(P,T,s)=P\psi_c\{(W-T)/s\}.
\]

The absence of mass at the Huber knots permits differentiation under the
integral. At the population solution,

\[
\partial_T\Psi=-A/s,\qquad \partial_s\Psi=-B/s.
\]

The derivative in the distribution direction is

\[
\partial_P\Psi[h]
=\int\psi_c\{(w-T)/s\}\,dh(w).
\]

Because \(A>0\), the implicit-function theorem applied to
\(\Psi(P,T(P),s(P))=0\), followed by Lemma A.1, gives the result. ∎

### Nuisance Jacobian

For the unscaled parameter \((m,d,T)\), the derivative of the three estimating
equations is

\[
J_0=
\begin{pmatrix}
f(m)&0&0\\
f(m+d)-f(m-d)&f(m+d)+f(m-d)&0\\
0&-B/d&-A/(kd)
\end{pmatrix}.
\]

Measuring nuisance perturbations in units of \(d\) gives

\[
J=J_0\operatorname{diag}(d,d,d)=
\begin{pmatrix}
df(m)&0&0\\
d\{f(m+d)-f(m-d)\}&d\{f(m+d)+f(m-d)\}&0\\
0&-B&-A/k
\end{pmatrix}.
\]

A2–A3 make this triangular matrix nonsingular pointwise. They do not impose a
uniform lower bound on its smallest singular value.

## A.4 Joint moment derivatives

Define

\[
g_X=E\{\operatorname{sign}(X-T_X)\},\quad
h_X=E\{\operatorname{sign}(X-T_X)b\},
\]

with analogous \(g_Y,h_Y\). For a joint tangent \(h\),

\[
\dot\mu_a[h]=\int a\,dh-g_X\dot T_X[h],
\]

\[
\dot\mu_b[h]=\int b\,dh-g_Y\dot T_Y[h],
\]

and

\[
\dot\nu[h]=\int ab\,dh-h_X\dot T_X[h]-h_Y\dot T_Y[h].
\]

The second moments satisfy

\[
\dot q_a[h]=\int a^2\,dh-2E(X-T_X)\dot T_X[h],
\]

and analogously for \(q_b\).

For point contamination \(z=(x,y)\), these derivatives give the complete
moment influence functions. In particular,

\[
IF_C(z)=
\frac{IF_\nu(z)}{\mu_a\mu_b}
-C\frac{IF_{\mu_a}(z)}{\mu_a}
-C\frac{IF_{\mu_b}(z)}{\mu_b}.
\]

This is one paired influence value. Its variance includes X–Y,
numerator–denominator, direct–nuisance, and cross-nuisance covariances.

## A.5 Profile-correlation derivative

Let

\[
u=\nu-\mu_a\mu_b,\quad
v_a=q_a-\mu_a^2,\quad v_b=q_b-\mu_b^2,
\quad D=(v_av_b)^{1/2}.
\]

For moment order \((\nu,\mu_a,\mu_b,q_a,q_b)\),

\[
\nabla\rho_P=
\left(
\frac1D,
-\frac{\mu_b}{D}+\rho_P\frac{\mu_a}{v_a},
-\frac{\mu_a}{D}+\rho_P\frac{\mu_b}{v_b},
-\frac{\rho_P}{2v_a},
-\frac{\rho_P}{2v_b}
\right).
\]

Combining this gradient with the complete five-moment influence vector gives

\[
IF_{\rho}(z)=\nabla\rho_P^\top IF_M(z).
\]

## A.6 Stochastic equicontinuity

The earlier proof draft asserted stochastic equicontinuity without identifying
the relevant classes. The required statement is the following.

### Lemma A.3 (random-nuisance empirical-process remainder)

Under A1–A6 and A8, for each component moment function
\(f_\theta\in\mathcal F_1\), if
\(\widehat\theta-\theta_0=O_P(n^{-1/2})\), then

\[
\mathbb G_n(f_{\widehat\theta}-f_{\theta_0})=o_P(1),
\qquad
\mathbb G_n=\sqrt n(P_n-P).
\]

#### Proof

Consistency localizes \(\widehat\theta\) to \(\Theta_0\). The indicator
subclasses indexed by median and MAD boundaries are VC and are
\(L_2(P)\)-continuous because the marginal cdfs are continuous at the
population boundaries. The clipped Huber subclass is bounded and
finite-dimensional Lipschitz away from a \(P\)-null set of knots.

For the moment functions, on \(\Theta_0\),

\[
\left||x-T|-|x-T'|\right|\le |T-T'|,
\]

\[
\left|(x-T)^2-(x-T')^2\right|
\le |T-T'|\{2|x|+|T|+|T'|\},
\]

and

\[
\begin{aligned}
&\left||x-T_X||y-T_Y|
-|x-T_X'||y-T_Y'|\right|\\
&\quad\le
|T_X-T_X'|\{|y|+M\}
+|T_Y-T_Y'|\{|x|+M\}
+|T_X-T_X'||T_Y-T_Y'|,
\end{aligned}
\]

for a finite neighbourhood bound \(M\). The Lipschitz coefficients are in
\(L_2(P)\) under A5-\(\rho\). These are therefore Euclidean, hence
\(P\)-Donsker, local classes with \(L_2(P)\)-continuous semimetric. Asymptotic
equicontinuity of a Donsker empirical process yields the display. ∎

Lemma A.3 supplies the missing justification for substituting fitted Huber
locations into the five empirical moments. It also clarifies that mere
consistency of the fitted nuisance is not sufficient without local
empirical-process control.

## A.7 Main asymptotic theorem

### Theorem A.1 (asymptotic linearity and normality)

Under A1–A6 and A8, using A5-\(\rho\) for \(\rho_P\) and A5-C for \(C\),

\[
\sqrt n\{\widehat\rho_P-\rho_P\}
=\frac1{\sqrt n}\sum_{i=1}^n IF_\rho(Z_i;P)+o_P(1),
\]

and

\[
\sqrt n\{\widehat C-C\}
=\frac1{\sqrt n}\sum_{i=1}^n IF_C(Z_i;P)+o_P(1).
\]

Therefore

\[
\sqrt n\{\widehat\rho_P-\rho_P\}\Rightarrow N(0,V_\rho),
\qquad
\sqrt n\{\widehat C-C\}\Rightarrow N(0,V_C),
\]

where \(V_\rho=E(IF_\rho^2)\) and \(V_C=E(IF_C^2)\).

#### Proof

Lemmas A.1–A.2 and the VC quantile expansions give the stacked nuisance
representation

\[
\sqrt n(\widehat\theta-\theta)
=-J_0^{-1}\frac1{\sqrt n}\sum_{i=1}^n g(W_i;\theta)+o_P(1).
\]

Lemma A.3 removes the empirical-process remainder created by replacing
\(\theta\) with \(\widehat\theta\) in the five moment functions. The ordinary
population Taylor terms in that substitution are exactly the nuisance terms
displayed in Section A.4. Hence the five moments have the complete joint
asymptotic linear representation \(n^{-1/2}\sum_i IF_M(Z_i)+o_P(1)\).

Under A4, both finite-dimensional maps from the moment vector to \(C\) and
\(\rho_P\) are continuously differentiable near the population moments. The
multivariate delta method gives the two influence functions. A5-C places
\(IF_C\) in \(L_2(P)\); A5-\(\rho\) places \(IF_\rho\) in \(L_2(P)\). The iid
CLT completes the proof. ∎

## A.8 Plug-in \(L_2\) consistency

Pointwise convergence of \(\widehat{IF}(z)\) is not, by itself, enough to
justify an in-sample empirical variance. The proof requires both function-norm
and empirical-process control.

### Lemma A.4 (function-norm consistency)

Under A1–A8,

\[
\|\widehat{IF}_\rho-IF_\rho\|_{P,2}=o_P(1)
\]

under A5-\(\rho\), and

\[
\|\widehat{IF}_C-IF_C\|_{P,2}=o_P(1)
\]

under A5-C.

#### Proof

All fitted scalar coefficients in the influence formulas converge: the
nuisance roots by A6, density values by A7, and expectations such as
\(A,B,g_X,h_X\) and the five moments by the Glivenko–Cantelli part of A8.
A2–A4 keep their limiting denominators away from zero.

The only discontinuous observation-level terms are threshold indicators and
signs. Moving their consistent thresholds changes them only on intervals
whose \(P\)-probability tends to zero; continuity and absence of mass at the
boundaries therefore give their \(L_r(P)\) convergence for every finite
\(r\). Huber scores are bounded and converge outside a \(P\)-null knot set.
The remaining moment terms are continuous in the nuisance parameters and are
dominated by the A8 envelopes. A5-C or A5-\(\rho\), as appropriate, makes the
squared influence envelope uniformly integrable. Truncation followed by
dominated convergence gives the displayed \(L_2(P)\) result. ∎

### Lemma A.5 (in-sample empirical second moment)

Under the same conditions,

\[
P_n\widehat{IF}_\rho^{\,2}\to_P PIF_\rho^2
\]

and analogously for \(C\).

#### Proof

Decompose

\[
\begin{aligned}
P_n\widehat{IF}^{\,2}-PIF^2
=&(P_n-P)(\widehat{IF}^{\,2}-IF^2)\\
&+P(\widehat{IF}^{\,2}-IF^2)
+(P_n-P)IF^2.
\end{aligned}
\]

The last term is \(o_P(1)\) by the ordinary law of large numbers. Lemma A.4
and Cauchy–Schwarz give

\[
|P(\widehat{IF}^{\,2}-IF^2)|
\le
\|\widehat{IF}-IF\|_{P,2}
\{\|\widehat{IF}\|_{P,2}+\|IF\|_{P,2}\}
=o_P(1).
\]

For the first term, A8 makes the localized squared plug-in influence class
\(P\)-Glivenko–Cantelli. Both \(\widehat{IF}^{\,2}\) and \(IF^2\) belong to
that class with probability tending to one, so the term is \(o_P(1)\).
This is the step missing from the earlier “pointwise convergence plus uniform
integrability” argument. ∎

### Corollary A.1 (studentized Wald inference)

Let

\[
\widehat V_\rho=
\frac1{n-1}\sum_{i=1}^n
(\widehat{IF}_{\rho,i}-\overline{\widehat{IF}_\rho})^2,
\]

and similarly for \(C\). Lemma A.5 also gives
\(P_n\widehat{IF}=o_P(1)\), so under A1–A8,

\[
\widehat V_\rho\to_P V_\rho,\qquad
\widehat V_C\to_P V_C.
\]

Consequently,

\[
\frac{\sqrt n(\widehat\rho_P-\rho_P)}
{\sqrt{\widehat V_\rho}}
\Rightarrow N(0,1),
\]

with the analogous conclusion for \(C\).

### Corollary A.2 (moment relaxation at the profile weak null)

Suppose \(\rho_P=0\). Then

\[
\frac{\partial\rho_P}{\partial q_a}
=-\frac{\rho_P}{2v_a}=0,\qquad
\frac{\partial\rho_P}{\partial q_b}
=-\frac{\rho_P}{2v_b}=0.
\]

Consequently, the first-order null influence contains no
\(a^2-q_a\) or \(b^2-q_b\) term. Under A1–A4, A5-C, A6–A8, where the
squared-moment functions need only be Glivenko–Cantelli for denominator
consistency rather than Donsker with square-integrable squares,

\[
\sqrt n\,\widehat\rho_P
\Rightarrow N(0,V_{\rho,0}).
\]

A null-restricted plug-in influence function sets the two squared-moment
gradient coefficients to zero and is consistent under these weaker moments.
The unrestricted plug-in coefficients are also asymptotically negligible.
Indeed, \(\widehat\rho_P=O_P(n^{-1/2})\), and, for example,

\[
\widehat\rho_P^{\,2}P_n a^4
=O_P(1)\frac{P_n a^4}{n}=o_P(1),
\]

because \(E(a^2)<\infty\) implies

\[
\frac{P_n a^4}{n}
\le
\frac{\max_i a_i^2}{n}P_n a^2
\to_P0.
\]

The same argument applies to \(b\) and the cross terms. Thus fourth marginal
moments are required for the general-\(\rho_P\) confidence theorem, but not
for the first-order test of \(H_0:\rho_P=0\).

## A.9 Permutation statements

### Proposition A.1 (fixed-margin equivalence)

For observed nonconstant positive profile vectors \(a,b\), and any
permutation \(\pi\),

\[
C_\pi=1+\rho_\pi CV_n(a)CV_n(b).
\]

The CV factors are positive and fixed over the orbit. Thus \(C_\pi\) and
\(\rho_\pi\) have identical ranks and corresponding permutation p-values when
centred at \(1\) and \(0\), respectively.

### Proposition A.2 (finite-sample randomization validity)

If the conditional joint law of the labels is invariant under the declared
permutation group and the complete statistic is recomputed on every orbit
element, the randomization p-value is finite-sample valid, up to Monte Carlo
randomization resolution.

This group-invariance result does not follow merely from \(\rho_P=0\) or
\(C=1\).

### Weak-null studentized permutation boundary

Theorem A.1 and Corollary A.1 establish the sampling limit of the observed
studentized statistic under a regular weak null. A proof that its conditional
permutation distribution has the same standard-normal limit additionally
requires a combinatorial triangular-array CLT and conditional consistency of
the fully recomputed orbit studentizer. This appendix does not claim that
result.

## A.10 Why the theorem is not uniform near degeneracy

The nuisance expansion is schematically

\[
\widehat\theta-\theta
\approx-J^{-1}(P_n-P)g.
\]

Its least-identified dimensionless direction has size

\[
O_P\{1/(\sqrt n\,\sigma_{\min}(J))\}.
\]

A1–A8 ensure pointwise nonsingularity but do not bound
\(\sigma_{\min}(J)\) uniformly over a sequence \(P_n\). Theorem A.1 therefore
makes no claim when

\[
\sqrt n\,\sigma_{\min}(J(P_n))=O(1).
\]

In that region, curvature and nonlocal median/MAD selection can be of the same
order as the nominal first-order term.

## A.11 Audited proof status

The audit corrected the marginal moment requirement for general
\(\rho_P\), recorded its weak-null relaxation, replaced the unsupported
stochastic-equicontinuity sentence with Lemma A.3, and replaced the invalid
pointwise-to-empirical-\(L_2\) shortcut with Lemmas A.4–A.5.

The remaining publication-level tasks are:

1. map each displayed A8 class to a precise VC/Euclidean closure theorem and
   record the envelope calculation in the final proof;
2. decide whether A8 will remain an explicit high-level assumption or be
   replaced entirely by primitive entropy and envelope conditions;
3. obtain an independent check of the joint MAD-with-estimated-median
   Bahadur remainder;
4. add a separate conditional combinatorial-CLT proof only if weak-null
   studentized permutation is promoted to a formal theorem.

Primary sources supporting these remaining mappings are:

- van der Vaart and Wellner, *Empirical processes indexed by estimated
  functions*, for replacing a random estimated function by its population
  limit under Donsker/equicontinuity conditions:
  https://arxiv.org/abs/0709.1013
- Giné and Guillou, *Rates of strong uniform consistency for multivariate
  kernel density estimators*, for uniform KDE control under regular bandwidth
  and kernel-class conditions:
  https://numdam.org/item/AIHPB_2002__38_6_907_0/
- Mazumder and Serfling, *Bahadur representations for the median absolute
  deviation and its modifications*, for weak and strong sample-MAD
  representations with an estimated median:
  https://doi.org/10.1016/j.spl.2009.05.006
