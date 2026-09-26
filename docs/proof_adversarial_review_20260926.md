# Adversarial internal mathematical review — 2026-09-26

Status: internal AI-assisted analytical review, not independent mathematical
peer review, referee approval, or statistical calibration evidence.

Reviewed baseline: commit `cb04f78ef02ae29925685ff014e74bad67b7aaf2` and the
September 25 author LaTeX at
`/Users/jialiangyao/.codex/visualizations/2026/09/11/01a08f53-8ee3-7dc0-87fd-0a3628d3098f/rho_p_minimal_20260925/main.tex`.
Line numbers below refer to that unchanged source. This review does not edit
the author file, production estimator, historical scripts, or frozen evidence.
No new simulation is required by these findings.

## 1. Actual-error covariance is stronger than the proved distributional limit

**Locations:** Section 5, lines 786–795; S1.2, line 1579.

The paired expansion proves a Gaussian limit for the scaled error. It does
not, from probability-order assumptions alone, prove convergence of the actual
second moments of that error. The displayed `Var(error) approximately Sigma/n`
is conventional first-order shorthand, but should be explicitly labeled as
such instead of being read as a further consequence of the theorem.

This distinction is logically necessary under R5, not merely stylistic.
Consider a regular normal law, retaining the prescribed sample median/MAD.
Let Tstar be an exact empirical Huber root. Replace it by n^2 on an event
E_n determined by the first observation with P(E_n)=1/n, and keep Tstar
otherwise. The modified reference remains consistent and has the same
root-n weak limit as Tstar. Its score is zero off E_n and bounded by c on
E_n, so its score residual is still o_P(n^-1/2). Nevertheless its second
moment includes n^4 P(E_n)=n^3. Because the exact root lies between the
sample extrema, its normal-law second moment is O(log n); the squared
mean of the modified root is only O(n^2+log n). The modified reference
therefore has diverging variance. This is an artificial logical witness,
not a statement about the implemented legacy or checked solver.

**Exact replacement for the Section 5 passage starting
`However, nuisance covariance also depends...` and ending the display:**

```latex
However, the limiting nuisance covariance also depends on the score
covariance $\Omega$. Under the regular conditions,
\[
\sqrt n\,\widehat\theta_{\mathrm{std}}
\ \Rightarrow\ N(0,\Sigma_W),\qquad
\Sigma_W=J^{-1}\Omega J^{-\top}.
\]
The matrix $\Sigma_W/n$ is a first-order covariance approximation;
convergence of the actual error covariance would additionally require
moment control, such as uniform integrability of the scaled squared errors.
```

**Exact replacement in S1.2 for the sentence beginning
`Then \(J_W=d_WJ_{0W}\) and ...`:**

```latex
Then $J_W=d_WJ_{0W}$ and
$\sqrt n e_W\Rightarrow N(0,J_W^{-1}\Omega_WJ_W^{-\top})$,
where $\Omega_W=E(\xi_W\xi_W^\top)$.
This specifies the covariance of the limiting distribution, not an
additional assertion of convergence of actual second moments.
```

No added moment assumption is needed if the manuscript makes this more
precise distributional statement. The local-conditioning interpretation
continues unchanged.

## 2. Complete the weak-null empirical-norm argument for the entire IF

**Locations:** S1.6, lines 1721–1749, with the compact counterpart in
Appendix A lines 1365 onward.

The existing maximum inequality and fitted-radius bound are correct. They
control the problematic quadratic terms. A complete unrestricted plug-in
IF also contains rho-hat-weighted linear and reference terms. These are
harmless under the stated regularity, but the present text skips their
explicit incorporation. The following decomposition closes that local
interface analytically; it does not add a fourth-moment CLT or a population
L2 assertion for the unrestricted influence.

Here all fitted moment influences mean the displayed Section 3 formulas
evaluated at the fitted parameters and moments. They need not individually
sum to zero; empirical centering is subsequently handled by contraction.

**Insert after the paragraph at line 1728, before `For the unrestricted
empirical studentizer...`:**

```latex
For this weaker-moment argument, retain R1--R3 and R5 and use the reduced
moment and empirical-process conditions just stated in place of R4
and the full five-moment requirement. Put
$\widehat D=\sqrt{\widehat v_a\widehat v_b}$ and write the unrestricted
plug-in influence exactly as
\[
\widehat{\IF}_\rho=\widehat H+\rhophat\widehat K,
\]
where
\[
\begin{aligned}
\widehat H
&=\{\widehat{\IF}_\nu-\widehat\mu_b\widehat{\IF}_{\mu_a}
       -\widehat\mu_a\widehat{\IF}_{\mu_b}\}/\widehat D,\\
\widehat K
&=\frac{\widehat\mu_a}{\widehat v_a}\widehat{\IF}_{\mu_a}
 +\frac{\widehat\mu_b}{\widehat v_b}\widehat{\IF}_{\mu_b}
 -\frac{\widehat{\IF}_{q_a}}{2\widehat v_a}
 -\frac{\widehat{\IF}_{q_b}}{2\widehat v_b}.
\end{aligned}
\]
The reduced class argument gives consistency of the empirical variance
of $\widehat H$ for the null IF variance; the denominator moments are
used only as consistent scalar coefficients. On the localized event,
the marginal reference influences are uniformly bounded and their
coefficients are bounded in probability. Consequently, for some
$L_n=O_P(1)$,
\[
P_n\widehat K^2
\le L_n\{1+P_n\widehat a^4+P_n\widehat b^4\}.
\]
This bound includes the linear-profile terms and all reference terms,
not only the two quadratic-profile components.
```

The notation `L_n` avoids using `C`, which already denotes the secondary
scientific parameter.

**Replace the start of line 1749 through
`This establishes empirical-norm negligibility of the extra quadratic terms.`
with:**

```latex
For fitted radii, $\widehat a_i\le a_i+|\widehat T_X-T_X|$ gives
$P_n\widehat a^4\le8P_na^4+8|\widehat T_X-T_X|^4$, and similarly
for $b$. Hence $\rhophat^2P_n\widehat K^2=o_P(1)$.
Empirical centering cannot increase this norm, and empirical
Cauchy--Schwarz controls its cross term with $\widehat H$.
Thus the unrestricted empirical studentizer has the same null variance
limit as the reduced influence.
```

Retain the following infinite-fourth-moment population-L2 warning and t3
example verbatim. R3's positive target IF variance still applies at the null.

## 3. Make the R6 envelope distinction literal

**Location:** lines 1243–1248.

R6 currently mentions IF and squared-IF GC closure, then speaks collectively
of `integrable squared envelopes`. Read literally for the square closure,
this could ask for an eighth moment, contrary to S1.3. The intended argument
needs an L2 envelope for the component/IF classes and an L1 envelope for their
squares. This is a wording ambiguity, not a failure of the supplied truncation
proof.

**Replace the two sentences from `Their localized finite influence-function
closure...` through `...integrable squared envelopes.` with:**

```latex
The component and finite influence-function classes have square-integrable
envelopes and are continuous in the required $L_2(P)$ semimetric at the
population nuisance values. Their localized influence-function closure
and squared closure are Glivenko--Cantelli where used for empirical
variance consistency; the squared closure requires only an integrable
envelope.
```

## 4. Checked reference coefficient and chain-rule representation

**Location:** Section 3 joint moment influences, immediately after the
five-moment gradient, if a compact explicit representation helps readers.

With the paper's existing g_X, h_X, mu_a, mu_b, v_a, v_b and D,

```latex
\[
\IF_\rho=\IF_{\rho,\mathrm{direct}}
 +\gamma_X\IF_{T_X}+\gamma_Y\IF_{T_Y},\qquad
\gamma_X=\frac{-h_X+\mu_b g_X}{D}
 +\rhop\frac{\E(X-T_X)-\mu_a g_X}{v_a},
\]
```

and gamma_Y is obtained by exchanging X/a and Y/b. This is verified by
collecting the reference coefficients in the five moment influences:

- the cross-moment term contributes -h_X/D;
- the mean-a term contributes mu_b g_X/D - rho mu_a g_X/v_a;
- the square-a term contributes rho E(X-T_X)/v_a.

It is an explicit instance of the existing chain rule, not a new general
influence-function technique. A globally independent law makes h_X=g_X mu_b
and rho=0, so gamma_X vanishes. Merely setting rho=0 does not force the first
term to vanish under a general dependent paired law.

## 5. Align local-density assumptions with the quantile and KDE arguments

R2 can naturally be read as local absolute continuity near the three
quantile boundaries, not global absolute continuity. That is sufficient,
but the proof should not silently import a stronger global domain.

**S1.1 replacement for the two sentences beginning `For continuous marginal
samples...` and ending `...that bound's constant).`:**

```latex
By consistency, with probability tending to one the fitted median and
the two fitted MAD boundaries lie in their respective atom-free density
neighborhoods. On this event the midpoint quantile indicator scores
have residuals of order $n^{-1}$; the possible midpoint-induced tie
between central absolute deviations changes only the bound's constant.
```

The local statement is enough: observations outside those neighborhoods
may include atoms, but cannot create an empirical mass jump at a fitted
boundary lying inside an atom-free neighborhood. For the MAD, coincident
opposite-side deviations involve affine equality of continuous coordinates;
apart from the deterministic central-pair tie they have probability zero.

**S1.5 replacement for the bias paragraph from `For the bias, choose...`
through `...uniform bias convergence on I.`:**

```latex
For the bias, choose $\delta>0$ with the closed $\delta$-enlargement of
$I$ inside the local density neighborhood. On $|w-t|\le\delta$,
uniform continuity bounds $|f(w)-f(t)|$. Outside this interval, the
kernel contribution is integrated against the marginal probability
law $P_W$ and is bounded by
\[
\sup_{t\in I,\,h\in[h_-,h_+]}
\int_{|w-t|>\delta}g_{t,h}(w)\,dP_W(w)
\le\sup_{h\in[h_-,h_+]}h^{-1}\phi(\delta/h).
\]
The remaining term is bounded by $\sup_I f$ times the corresponding
Gaussian tail probability. Both tail bounds vanish. Letting $n$ grow
and then $\delta$ decrease proves uniform bias convergence on $I$,
without requiring a density away from the local neighborhoods.
```

These replacements retain the existing local regularity and do not need
new tests or a new simulation study.

## 6. Remaining checked interfaces and why no further local change is needed

| Interface | Analytical check and its limit |
|---|---|
| R2/sample-MAD uniqueness | A positive continuous density near m and m±d supplies local quantile identification; positive derivative of P(|W−m|≤d) rules out a median plateau at d. R5 already requires consistency. The midpoint convention is retained. |
| S1.1 midpoint residuals | In continuous marginal samples the ordinary quantile residual is O(1/n); equal central deviations can increase its constant but not order. Locally continuous laws with remote atoms can instead restrict to the high-probability event that the fitted median/MAD boundaries lie in their continuous neighborhoods. A global no-atoms assumption need not be silently added. |
| S1.2 Huber derivative | Derivatives −A/s and −B/s have the correct signs and scaling. Bounded Huber score plus local positive scale supplies uniform Lipschitz bounds. No independence of marginal fits is used. |
| S1.3 signs/active knots | September 25's strict-half-line decomposition includes equality exactly. The active score's knot pieces include their zero boundary values. Finite Boolean combinations of half-spaces supply the stated VC route. |
| Moving weighted boundaries | The displayed uniform bound 2δ²+8E[b²1{|X−T|≤δ}] vanishes by integrability and the null limiting boundary. No factorization across margins is needed. |
| Random coefficients | Each consistent scalar can be included in a deterministic compact set with interior containing its limit. Finite cover products control the finite sum. There is no use of arbitrary unbounded-product Donsker closure. |
| S1.4 product remainder | Each radius shift is bounded by its location shift; the second-order product term is at most |h_X h_Y|. Weighted first-order remainder is o(|h|) by dominated convergence. |
| S1.5 random bandwidth | The Gaussian grid's O(n^4) cardinality and O(h_-^-2) derivative bounds give the stated deliberately crude rate. The bandwidth band follows from sample-SD consistency. Evaluation points and bandwidth may depend on the same sample. |
| Local density versus remote atoms | If R2 is interpreted as requiring a density only locally, the Gaussian bias tail can be written as an integral against P, bounded by sup h^-1 phi(δ/h) because P has total mass one. Thus remote atoms do not invalidate that argument; the current density notation is sufficient for globally absolutely continuous margins. |
| S1.6 t3 witness | Independent t3 margins satisfy the reduced moments for 0<eta<1; the nonzero fitted quadratic coefficient gives infinite population squared norm. The empirical norm route remains distinct. |
| S1.7 exact-root equivalence | Monotonicity, strict population signs, scale consistency and local positive active mass give consistency and an O_P(n^-1) gap under the real-arithmetic residual rule. The fixed precision/budget implementation boundary remains explicit. |
| S1.7 reflection at sample equality | The stored deterministic witness is explained by the <= median score at an observed median. For a unique observed median, the centered correction has empirical squared norm O_P(1/n) under localized coefficients. This does not justify a universal O_P(1/n) SE-gap rate. |
| Shared-sign proposition | Unique median zero, MAD one and Huber reference zero follow as written. Unbalanced sign samples place the absolute midpoint median above the minimum radius. The union bound then implies sqrt(n)|mhat|→infinity. |
| Shared-sign Gaussian tail | Writing a_n=(0.5 log n−log M)/tau, log{n Phi(−a_n)}≤log n−a_n²/2+O(log log n)→−infinity. This makes the lower-tail step explicit without an additional theorem. |
| Sample covariance identity | Expanding Cov_n(R_X−S T_X,R_Y−S T_Y) gives exactly the four terms printed, even when fitted offsets depend on the sample. The no-crossing condition is necessary for that representation. |
| n^-1/4 heuristic | It is labeled conditional and does not claim control of the full median/MAD estimator or domination over all omitted terms. No new local-to-degeneracy theorem is implied. |

## 7. Literature matching and external handoff

Theorem 2.1 of van der Vaart and Wellner (2007), *Empirical processes indexed
by estimated functions*, p.236, matches the substitution step: localization
to a fixed Donsker class with probability tending to one and population L2
continuity permit estimated-index substitution. The author's hosted primary
source was checked in the preceding focused review:
https://sites.stat.washington.edu/jaw/JAW-papers/NR/jaw-vdv-07LNMS.pdf

The local proofs, not the citation by itself, establish the claimed classes
and envelopes. A renewed literature search is not needed to resolve the two
analytical repairs above. No additional Monte Carlo coverage run would prove
them. The external reviewer should still check the paired midpoint-MAD
linearization, entropy/measurability of the exact classes, the now-complete
weak-null decomposition, and the estimator-to-software precision boundary.
This document records identified local repairs and checked limits, not a
certificate that no further mathematical issue can exist.
