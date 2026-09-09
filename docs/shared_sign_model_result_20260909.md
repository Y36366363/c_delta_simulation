# A short result for the shared-sign construction

Date: 2026-09-09. Model-specific algebra and regularity analysis, not a
general local-to-degeneracy theorem. Let k=1.4826 and c=1.345 throughout.

## Proposition: population target and failed median regularity

Let S be Rademacher, U,V independent standard normal, and S independent of
(U,V). For a fixed tau>0 put X=S R_X, Y=S R_Y with
R_X=exp(tau U), R_Y=exp(tau V). For each margin the unique median is m=0,
the raw MAD is d=1, the scaled MAD is s=k, and the unique population Huber
location is T=0. Consequently,

\[
\rho_P=\operatorname{Corr}(|X|,|Y|)=0,\qquad
C=\frac{E(|X||Y|)}{E|X|E|Y|}=1.
\]

The marginal density extends continuously to f(0)=0; thus Appendix A's
positive-center-density assumption A2 fails. The midpoint sample median
does not have an ordinary root-n limit about zero. This is not a claim that
the population median is nonunique or that the population Huber root is flat.

### Proof

Let G_tau be the lognormal radial CDF. For x>0,
F_X(x)=1/2+G_tau(x)/2>1/2; for x<0,
F_X(x)=(1-G_tau(-x))/2<1/2. Continuity yields the unique median zero.
The median of |X|=R_X is exp(tau*0)=1. Symmetry and oddness of psi_c imply
E psi_c(X/k)=0. For any finite T the interval (T-ck,T+ck) has positive
probability, making the Huber score strictly decreasing in T; the root is
unique. The joint fixed-reference profiles are independent positive
lognormal variables with nonzero variances, which gives rho_P=0 and C=1.

For x not equal to zero,

\[
f_X(x)=\frac{1}{2\tau|x|}\phi\{\log|x|/\tau\}.
\]

Writing a=-log|x| shows f_X(x) is proportional to
exp(-a^2/(2 tau^2)+a), which tends to zero as x tends to zero.
The densities at both MAD boundaries, -1 and 1, are positive. All polynomial
moments exist, the profiles have positive variance for tau>0, and there are
no atoms at the reference or clipping boundaries. It is specifically the
median identification condition that fails; the full theorem is not invoked
by selectively retaining the other conditions.

To see the root-n failure directly, fix M>0. For an unbalanced sample of
signs, the sample median (including the midpoint convention for even n)
lies on one side of zero and its absolute value is at least the minimum
sample radius. Therefore

\[
P(\sqrt n|\widehat m|\le M)
\le P(\text{exact sign balance})
   + nG_\tau(M/\sqrt n)\longrightarrow0.
\]

The balance probability is O(n^(-1/2)) for even n and zero for odd n.
The second term tends to zero because the Gaussian lower tail has exponent
of order -(log n)^2/(8 tau^2), dominating log n. Thus sqrt(n)|m_hat|
diverges in probability even though the sample median is consistent. This
proves nonregularity for the implemented convention without assuming a
particular switching-probability approximation.

Failure of A2 is failure of a sufficient assumption of the present theorem,
not proof that no alternative asymptotic result for the fitted Huber reference
or profile correlation is possible. Nonregularity of the median does not by
itself establish nonregularity of every functional that uses it.

## Huber curvature and the local index

At T=0 and s=k,

\[
A=P(R_X<ck)=\Phi\{\log(ck)/\tau\},\quad B=0,\quad
\partial_T E\psi_c((X-T)/k)\big|_{T=0}=-A/k.
\]

At tau=.10 the clipping radius ck is about 1.9941 and the slope is about
-.67449, not close to zero. Analytic truncated-moment evaluation and central
finite differences verify this in the accompanying numerical table.

In the declared standardized (m,d,T) coordinates, the population Jacobian is

\[
J=\operatorname{diag}\left(0,\frac{1}{\tau\sqrt{2\pi}},-A/k\right).
\]

It is singular for **every** positive tau in this unbridged family, so its
effective local conditioning index I_n is zero at both tau=.10 and tau=.40.
It cannot explain the difference between those two cells by itself. The
positive-density bridge evidence is a separate experiment that varies local
conditioning; this unbridged example must not be called a sequence of fixed
regular models. Weakness of the nuisance system also does not imply that its
weak direction has a nonzero first-order target projection.

## Direct shared-sign reference errors need not involve estimating the scale

At small tau, magnitudes lie near one while ck is about two. If all fitted
residuals lie inside the Huber clipping interval at the population scale,
the fitted reference equals the sample mean exactly. This is a conditional
sample identity, not a guarantee that every sample is unclipped.

For the sample means themselves, the following formulas are exact:

\[
E(\bar X\bar Y)=e^{\tau^2}/n,\quad
E(\bar X^2)=E(\bar Y^2)=e^{2\tau^2}/n,\quad
\operatorname{Corr}(\bar X,\bar Y)=e^{-\tau^2}.
\]

This follows from E X=E Y=0, E(XY)=E(R_X)E(R_Y)=exp(tau^2),
and E X^2=exp(2 tau^2). Shared-sign linkage is therefore already present
before estimating a median or MAD. Whether this pathway accounts for most
of the observed distortion is answered by the staged experiment, not by
the identity alone.

## Fixed-offset covariance identity and its sample version

For fixed offsets t_X,t_Y and positive radii satisfying R_X>|t_X| and
R_Y>|t_Y| almost surely,

\[
|SR_X-t_X|=R_X-St_X,\qquad
\operatorname{Cov}(R_X-St_X,R_Y-St_Y)=t_Xt_Y,
\]

because the radii are independent of one another and of the symmetric sign.
The profile correlation is

\[
\frac{t_Xt_Y}{\sqrt{(v_X+t_X^2)(v_Y+t_Y^2)}}.
\]

Lognormal radii have support down to zero, so the no-crossing condition is
not literally true for nonzero fixed offsets at the population level. It
is a local approximation in concentrated regimes, not an exact identity
over the whole lognormal law.

On a sample with no crossings, the algebraic identity remains exact for
data-dependent fitted offsets, but the **sample covariance** has extra terms:

\[
\widehat{Cov}_n(a,b)=\widehat{Cov}_n(R_X,R_Y)
-t_X\widehat{Cov}_n(S,R_Y)-t_Y\widehat{Cov}_n(R_X,S)
+t_Xt_Y\widehat{Var}_n(S).
\]

Using a fitted offset in the population fixed-offset formula as if it were
independent of its own sample would omit these terms. The product of linked
reference errors is the candidate leading mechanism, not an exact
finite-sample bias formula for the full fitted estimator.

## Fourth-root boundary: a conditional rate-balance heuristic

Suppose reference errors are O_P(n^(-1/2)) with a nonnegligible shared product,
the profiles are sufficiently local for the above approximation, and radial
variance v_tau=exp(tau^2)(exp(tau^2)-1) is of order tau^2. Then the
induced correlation contribution has size O_P(1/(n tau^2)). Relative to an
ordinary n^(-1/2) correlation fluctuation, the standardized contribution has
size O_P(1/(sqrt(n) tau^2)). Equating this scale to order one suggests

\[
\tau\asymp n^{-1/4}.
\]

This calculation explains the proposed rate; it is **not** a proved local
limit, a universal boundary, or a result for the full nonregular median/MAD
estimator. Uniform remainder control, clipping/crossing probabilities,
reference fitting rates, and the limiting studentizer would all require
separate proof. In particular, nonregularity of the median prohibits simply
assuming root-n behavior for the whole fitted nuisance vector. This short
result deliberately stops before that additional theory.
