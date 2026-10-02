# Mathematical response to the October 2 restructuring questions

Status: internal AI-assisted algebra and proof-structure review. This is not
independent mathematical peer review. The reviewed input is
`rho_p_minimal_20261002/main.tex`, the October 2 author artifact outside the
research repository. No original equation, estimator, default algorithm,
historical script or frozen result is changed by this note.

## 1. The factor k is required under the manuscript's definitions

**Finding:** no factor-k inconsistency was found in the current main formula,
S1.2, the standardized Jacobian, S3.2 or the production implementation.
Removing k from the displayed Huber IF while retaining the definitions of
raw MAD d and B would introduce an error.

The paper defines s=kd, U=(W−T)/s, A=P(|U|<c), and
B=E[U 1{|U|<c}]. Let

```latex
q(T,d)=P\psi_c\{(W-T)/(kd)\}.
```

Under the no-mass-at-clipping-boundaries assumption, differentiation gives

```latex
\[
\partial_T q=-\frac{A}{kd},\qquad
\partial_d q
=-\frac{1}{d}P\{U1(|U|<c)\}
=-\frac{B}{d}.
\]
```

For a point contamination, the score derivative is

```latex
\[
0=\psi_c\{(w-T)/(kd)\}
  -\frac{A}{kd}\IF_T(w)-\frac{B}{d}\IF_d(w).
\]
```

Hence

```latex
\[
\IF_T(w)=\frac{kd}{A}\psi_c\{(w-T)/(kd)\}
          -\frac{kB}{A}\IF_d(w).
\]
```

The alternative coordinate s has derivative ∂_s q=−B/s. In that coordinate
the correct expression is (s/A)psi−(B/A)IF_s, with IF_s=k IF_d.
The apparent difference is a coordinate conversion, not a choice between
two equivalent raw-MAD formulas.

| Coordinates / perturbation | Huber derivative row | Huber IF scale contribution |
|---|---|---|
| Physical theta=(m,d,T), d raw MAD | (0, −B/d, −A/(kd)) | −(kB/A) IF_d |
| Physical (m,s,T), s scaled MAD | (0, −B/s, −A/s) | −(B/A) IF_s |
| Error (theta_hat−theta)/d, fixed population d | d times first row = (0, −B, −A/k) | Same IF after converting back to physical units |

The manuscript's J0 uses the first row and its J uses the third. In
particular, replacing −B/d by −B/(kd) in J0 would incorrectly substitute the
scaled-MAD derivative for the raw-MAD coordinate. Standardizing data units
does not permit arbitrary score-equation rescaling.

### Exact locations checked

- Main influence display, label `eq:IFhuber`, input lines 554–559:
  `-(B/A) k IF_d` is correct.
- S1.2, input lines 1625–1642: J0 has `-B/d` and `-A/(kd)` and the expansion
  retains k; the subsequent derivative with respect to s is `-B/s`.
- Section 5, label `eq:J`, input lines 830–835: standardized third row
  `(0,-B,-A/k)` is correct.
- S3.2 Stage 3, input line 2228: population median fixed but raw MAD estimated;
  the Huber propagation must still multiply IF_d by k.
- `src/cdelta.py`, `_huber_location_influence`: `scale_if = 1.4826 * mad_if`
  and `location_if = scale/A * psi - B/A * scale_if` are correct.
- `scripts/run_reference_pathway_20260909.py`, `fit_margin`: the Stage 3
  implementation uses `it - b/a * K * id_`, consistently.
- `scripts/validate_active_nuisance_20260907.py`, `location_if`: the population
  calculation uses `direct - b/a * K * id_`, consistently.

### Minimal manuscript clarification

Keep the current formulas. Immediately after the Huber influence display add:

```latex
Here $d$ is the raw MAD, so $\IF_s=k\IF_d$.
For $q(T,d)=P\psi_c\{(W-T)/(kd)\}$,
$\partial_Tq=-A/(kd)$ and $\partial_dq=-B/d$.
Thus differentiating the empirical-reference equation gives
$\IF_T=(s/A)\psi_c-(B/A)\IF_s
       =(s/A)\psi_c-(kB/A)\IF_d$.
```

An author response can state politely that the suspected inconsistency was
checked but the factor is required by the current raw-MAD definition. It
should not say that k was removed or that an error was fixed when none was
found. Clearer notation is the appropriate response.

### Bounded numerical falsification of the no-k alternative

An independently written closed-form lognormal score check used the existing
log-SD .6 marginal, k=1.4826 and c=1.345. This was deterministic numerical
differentiation, not a simulation or a new population design. The current
runtime was Python 3.12.3 / NumPy 1.26.4 / SciPy 1.16.3; this check does not
claim a newly isolated dependency environment.

With m=1, d=.387121537597268, T=1.0798088609617673,
A=.8229760645580049 and B=−.17141146941370808:

| Quantity | Analytic value | Central difference, step 1e−6 |
|---|---:|---:|
| ∂d q at fixed T | .4427846367773824 | .4427846367061061 |
| ∂T q at fixed d | −1.433890127271249 | −1.433890126981141 |

The incorrectly substituted value −B/(kd) is .298654145944545. The check
does not rely on a symmetric law where B vanishes.

Re-solving the contaminated median, raw MAD and Huber score at epsilon=1e−7
gave:

| Contamination point w | IF with k | Finite-difference derivative | Absolute error if k is omitted |
|---:|---:|---:|---:|
| .3 | −.8794422939242038 | −.8794423900226889 | .0190634892 |
| .8 | −.5407558420024154 | −.5407558445469363 | .0653490712 |
| 1.3 | .20898931056046116 | .20898932362456435 | .0190635723 |
| 3 | 1.1387672022242343 | 1.1387674159202277 | .0653492823 |

The largest error of the correct formula was 2.14e−7. This corroborates the
algebra; neither numerical differentiation nor internal review is a proof
certification. No production defect was found, so no replacement estimator,
new simulator or scientific-result rewrite is warranted.

The deterministic calculation is reproducible with
`scripts/check_huber_scale_coordinates_20261002.py`; its successful report is
`results/huber_scale_coordinates_20261002.json`, which records the source hash,
runtime, score derivatives and all four contamination directions. The script
refuses to overwrite an existing report. To repeat, use a fresh report path:

```text
python scripts/check_huber_scale_coordinates_20261002.py --report /tmp/huber_scale_recheck.json
```

## 2. Make the logical role of R6 explicit instead of leaving a circular impression

The current theorem is validly conditional on R6, but the presentation can
better distinguish a conditional inference criterion from its verification
for the actual construction. The existing S1.3 supplies construction-specific
class arguments; R6 should not be advertised as an unexplained new assumption
that the implemented example happens to satisfy by assertion.

Recommended structure:

1. Retain the main theorem as a conditional pointwise theorem under R1–R6.
2. State a construction-specific verification lemma: primitive law and moment
   conditions give the listed entropy, continuity and integrable envelopes.
   Coefficient consistency then gives the high-probability localization.
3. State an implementation-matched corollary under R1–R4 using midpoint
   quantiles, the Gaussian sample-SD KDE, and a sufficiently accurate empirical
   Huber root **in ideal real arithmetic**. Prove the R5 fitting and density
   requirements instead of assuming them again inside that corollary.

This is a real logical separation, not a theorem obtained by renaming R6.
It leaves the finite-machine success limitation intact.

### Proposed construction-verification lemma

```latex
\begin{lemma}[Local classes for the robust-reference construction]
\label{lem:profileclasses}
Under R1--R4, on deterministic compact parameter sets with positive scales
and denominators bounded away from zero, the indicator, clipped-score,
radius, paired-product and weighted-sign classes used in the expansion
have the VC or finite-dimensional covering bounds and $L_2(P)$ continuity
described in S1.3. Their finite scalar influence-function closure has an
$L_2(P)$ envelope, and its squared closure is Glivenko--Cantelli with an
$L_1(P)$ envelope. Consistent fitted scalar coefficients can be localized
in these sets with probability tending to one. Thus R6 holds for this
construction whenever the fitted quantities in R5 are consistent.
\end{lemma}
```

The proof must cite the exact S1.3 pieces, rather than merely appeal to a
general empirical-process theorem: half-lines/intervals, clipped-score
Lipschitzness, active-score pieces, translated radius/product bounds,
weighted signs including equality, finite coefficient covers and squared
influence truncation. The proof must distinguish the L2 envelope of the IF
class from the L1 envelope of its squares.

### Proposed construction-specific inference corollary

```latex
\begin{corollary}[Midpoint and Gaussian-KDE implementation]
\label{cor:implementedregular}
Assume R1--R4 at a fixed paired law. Estimate the median and raw MAD by
the stated midpoint convention. At scale $k\widehat d$, choose a measurable
empirical Huber location with score residual at most $C_0/n$, where
$0<C_0<\infty$ is fixed, or an exact empirical root. Use the Gaussian KDE
with bandwidth $1.06\widehat\sigma_W n^{-1/5}$ for the boundary densities.
For the ideal-real-arithmetic procedure, the expansion, complete plug-in
variance consistency and studentized limit of Theorem~\ref{thm:regular}
hold pointwise.
\end{corollary}
```

Here C0 is an engineering bound, not the secondary target C. An exact root
is permitted as the zero-residual special case. This statement concerns
the mathematical estimator, not automatic success of a fixed floating-point
implementation. Denominators/scales are positive on an event whose probability
tends to one; define the mathematical statistic arbitrarily on its complement
if a total random-variable definition is needed. This mathematical completion
must not instruct software to hide failure records or return a zero effect.

### Proof of the corollary, avoiding circularity

- R2 gives consistency of the midpoint median and raw MAD and their local
  quantile identification; d>0 then makes the fitted scale positive with
  probability tending to one.
- First verify the deterministic classes and GC bounds from the law conditions,
  without using consistency of the selected Huber root. At fixed T±epsilon,
  score LLN plus scale substitution preserve the population strict signs.
  Monotonicity and the vanishing residual force every accepted location
  between those endpoints. Hence the chosen empirical location is consistent.
- The residual C0/n is o(n^-1/2). S1.1–S1.2 then give the joint paired
  quantile/Z expansion. The root construction is measurable; exact bisection
  with a growing budget is an explicit admissible selection.
- Finite nonzero marginal variance follows from R3/R4. The Gaussian KDE
  argument in S1.5 proves local uniform consistency with the sample-SD
  bandwidth and data-dependent boundary evaluations. Its remote tails are
  integrated against the probability law, allowing remote atoms.
- GC and continuous mapping give consistency of A, B, signed weights and
  moment/denominator coefficients. Population-positive limits place all
  fitted scalar coefficients in fixed compact sets with probability tending
  to one. S1.3's class lemma therefore supplies R6 for the fitted procedure.
- The conditional theorem now applies. No statement that the historical
  legacy stopping rule or fixed-precision checked implementation guarantees
  these conditions has been smuggled into the corollary.

## 3. State the weaker-moment weak-null conclusion separately

The full general-effect theorem cannot be reused with R4 simply deleted:
its squared-radius classes and unrestricted population-L2 assertion can fail.
The reduced-null result should be a separate corollary using the already
written S1.6 empirical-norm proof, not a stronger version of the five-moment
theorem.

Define the null influence, using the manuscript's D, g and h, by

```latex
\[
H_0(Z)=\frac{(a-\mu_a)(b-\mu_b)
 -(h_X-\mu_b g_X)\IF_{T_X}(X)
 -(h_Y-\mu_a g_Y)\IF_{T_Y}(Y)}{D}.
\]
```

Under rho_P=0 this has mean zero and is exactly the gradient-combined
three-moment influence. Set V0=P H0^2 and require 0<V0<infinity. The reduced
moment assumptions give finiteness; nondegeneracy still must be stated.

```latex
\begin{corollary}[Reduced-moment weak-null inference]
\label{cor:weaknull}
At a fixed law with $\rhop=0$, assume R1--R3, replacing the target variance
condition by $0<V_0=P H_0^2<\infty$, and suppose, for some $\eta>0$,
\[
P\{a^{2+\eta}+b^{2+\eta}+(ab)^{2+\eta}\}<\infty.
\]
Use the midpoint quantiles, Gaussian boundary-density estimator and
sufficiently accurate ideal-arithmetic empirical roots of
Corollary~\ref{cor:implementedregular}. Then
\[
\sqrt n\rhophat
=n^{-1/2}\sum_{i=1}^n H_0(Z_i)+o_P(1),\qquad
\widehat V_\rho\to_P V_0,
\]
where $\widehat V_\rho$ is the unrestricted complete empirical studentizer.
Consequently $\sqrt n\rhophat/\sqrt{\widehat V_\rho}\Rightarrow N(0,1)$.
\end{corollary}
```

The corollary refers to the estimator specification in the regular corollary,
not its stronger R4 assumption. If that distinction is hard to read, repeat
the estimator specification verbatim instead of using the cross-reference.

Proof route: the three-moment expansion and denominator consistency give
rhohat=O_P(n^-1/2). Write exactly fullIFhat=Hhat+rhohat Khat, including the
linear and bounded-reference terms in Khat. S1.6 establishes
rhohat² P_n Khat²=o_P(1) using max_i a_i²/n=o_P(1), the empirical fourth-power
bound and fitted-reference consistency. Centering contracts the empirical
norm, and empirical Cauchy–Schwarz removes the cross term with Hhat. The
reduced class supplies the variance limit for Hhat. No claim that the full
unrestricted plug-in function converges in population L2 is made; the t3
witness stays in S1.6. This is a weak-null result only, not general nonzero
confidence inference under the same lower moment condition.

## 4. Disposition

Locally resolved: coordinate/algebra clarification; a concrete route from
primitive construction conditions to R5/R6; separation of the weaker-moment
null corollary from the general theorem. No discovered factor-k defect
requires rerunning historical results. The proposed corollaries are
author-level proof statements for independent review, not an external
endorsement. The fixed-machine precision/iteration interface, actual reviewer
judgment, and editorial choice of main versus supplement placement remain
explicit rather than being erased by new theorem labels.

## 5. Read-only check of the restructured author draft

The subsequent review covered Section 3, R1–R6 and all of S1.1–S1.9 in
`rho_p_hoorn_restructured_20261002/main.tex` (snapshot SHA-256
`e75113c6d6966217fdefe72bbffe14b1f511aecb0e045c1d7f89eef13d21144c`).
This identifies the reviewed snapshot; the author may make subsequent
layout or wording edits. The review did not edit the author file.

No new substantive inconsistency was identified in the following integrated
steps:

- The physical raw-MAD derivative, scaled-MAD derivative, standardized
  Jacobian and Huber influence retain the required coordinate conversion.
- The conditional theorem explicitly assumes R6; the construction-specific
  corollary instead derives fitting consistency from deterministic score
  GC and strict endpoint signs, then obtains residual, density and scalar
  coefficient consistency before invoking the class lemma.
- The lemma's weighted moving-sign bound is uniform locally, retains
  sample equality conventions, and requires no independence of the two
  margins. The finite scalar closure uses an L2 envelope; its squared
  closure uses only the corresponding L1 envelope.
- The local Gaussian-KDE bias proof integrates the remote portion against
  the marginal probability law, so it does not silently impose global
  absolute continuity. Its random sample-SD bandwidth is contained in a
  deterministic band by finite-variance consistency.
- The weak-null influence H0 has the correct two reference coefficients.
  The proof applies the lower-moment class argument to the three moments,
  uses squared moments only for a consistent denominator, and controls
  the entire unrestricted empirical influence through Hhat+rhohat Khat.
  The bound on Khat includes its linear and reference terms. The maximum
  and empirical fourth-power argument needs no population fourth moment.
- The C0/n corollary and S1.7 distinguish an ideal-arithmetic estimator
  from a fixed-precision, finite-iteration implementation. A mathematical
  completion on vanishing-probability invalid events is explicitly not
  an instruction to hide software failures.
- The shared-sign proof supplies the stated nonregular median rate,
  positive Huber score slope and independent population radii. Its exact
  sample covariance identity keeps the empirical cross terms, and its
  rate heuristic remains explicitly conditional.

Two small notation clarifications were sent to the author integrator:

1. In S1.2, replace “Multiplying the first row” by “Multiplying the raw-MAD
   coordinate row” after displaying the two physical derivative rows.
   This avoids confusion with the first row of the three-by-three J0.
2. In S1.4, use delta_X and delta_Y for reference shifts in the bound for
   the product of radius changes. The symbols h_X and h_Y already denote
   weighted-sign expectations in Section 3.

These are notation fixes, not changes to a theorem or scientific result.
This review has not become independent mathematical review, and no
additional simulation cells were generated.
