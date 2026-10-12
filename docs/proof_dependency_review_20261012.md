# Proof dependencies and review boundaries — 12 October 2026

Internal review note. This records the current discussion, not independent
mathematical certification. The initial note left the October 2 manuscript
unchanged. A subsequent October 12 revision integrates selected proof and
reporting clarifications; see manuscript_mock_review_update_20261012.md.
No new
simulation cells, root replays, algorithm changes, or frozen-result changes
accompany this note. The fixed-tau argument below is a candidate supplement,
not an established result of the current manuscript.

## Three separate result lines

| Line | Dependencies | Scope and outstanding work |
|---|---|---|
| Regular inference | Fixed paired IID law; quantile and Huber identification; nuisance consistency and linearization; local classes; paired joint moments; delta method; plug-in empirical variance | Current S1 contains proofs, including reduced-moment null empirical-norm control. Independent expert review remains outstanding. Does not depend on the new fixed-tau argument. |
| Candidate fixed-tau shared-sign point-estimator limit | Median/MAD consistency; Huber consistency; local score Donsker lemma below; exact population symmetry; root-n Huber expansion; profile oracle equivalence; oracle CLT | Fixed tau > 0 and exact/sufficiently accurate empirical roots. Candidate conclusion sqrt(n) rho_hat -> N(0,1). Not yet integrated or independently reviewed. No regular-form full-IF studentizer theorem or triangular-array conclusion. |
| Finite-sample mechanism evidence | Frozen paired designs; population truth; staged fits; estimator summaries; reference errors; specified rejection rules | Point-estimate distortion is independent of the studentizer. Stage 2 to 4 is additional full-chain amplification, not an isolated MAD effect. Numerical observations do not prove a limit or a rate. |

The existing shared-sign Proposition 1 and exact covariance calculations are
distinct from the new candidate point-estimator CLT. Do not relabel the latter
as already established by the existing proposition.

## Lemma RI: local random-index substitution

Let Z_i be IID with law P. Let G = {g_theta: theta in Theta_0} be a
measurable/separable P-Donsker class, with theta_0 in Theta_0. Suppose

    omega(delta) = sup_{||theta-theta_0|| <= delta}
                   ||g_theta-g_theta_0||_{P,2} -> 0.

Then, for every deterministic delta_n -> 0,

    sup_{||theta-theta_0|| <= delta_n}
        |G_n(g_theta-g_theta_0)| ->_P 0.

If theta_hat ->_P theta_0 and P(theta_hat in Theta_0) -> 1, the same conclusion
holds at theta_hat, without independence between theta_hat and the sample.
Use outer probability if separability/measurability has not been established.

Proof. A P-Donsker class is asymptotically equicontinuous in the canonical
semimetric d_P(f,g) = [Var_P(f-g)]^(1/2). This semimetric is bounded above by
||f-g||_{P,2}. Therefore, for every epsilon > 0,

    lim_{delta -> 0} limsup_n P*(sup_{||theta-theta_0|| <= delta}
       |G_n(g_theta-g_theta_0)| > epsilon) = 0.

For fixed delta > 0, eventually delta_n <= delta; bound the shrinking
supremum by the fixed-delta supremum and then let delta -> 0. For a random
index, add P(||theta_hat-theta_0|| > delta) and the probability of leaving
Theta_0 to this bound. First let n -> infinity, then delta -> 0. Alternatively
select a sufficiently slow deterministic delta_n containing theta_hat with
probability tending to one. No delta_n sqrt(n) condition is needed.

The estimated-index specialization is also covered by van der Vaart and
Wellner (2007), Theorem 2.1, p. 236, with their outer target-index set a
singleton, eta = theta, H_0 = Theta_0, and their condition (3) supplied by
L2 consistency. Source: https://doi.org/10.1214/074921707000000382
and https://sites.stat.washington.edu/jaw/JAW-papers/NR/jaw-vdv-07LNMS.pdf .
Theorem 2.1 does not itself establish that the proposed class is Donsker.

### Huber-score application

Take g_(t,s)(w) = psi_c((w-t)/s) on
Theta_0 = [-r,r] x [s_min,s_max], with 0 < s_min < k < s_max.
An envelope is the constant c. Uniformly in w,

    |g_(t,s)(w)-g_(t',s')(w)|
      <= |t-t'|/s_min + c |s-s'|/s_min.

For the scale term, take s <= s' and split |w-t'| into the regions below cs,
between cs and cs', and above cs'. The bound holds in all three regions,
including knots. No classical differentiability at a knot is needed.
Parameter grids give N(epsilon ||c||_{Q,2}, G, L2(Q)) <= (C/epsilon)^2
for 0 < epsilon < 1, uniformly in finite-support Q, with constants depending
on the fixed parameter rectangle and c. The uniform entropy integral is
finite, proving Donsker under the usual measurability conditions. Parameter
continuity gives a countable separable version. Lemma RI now applies.

## Candidate shared-sign proof order

1. Specify IID triples (S_i,U_i,V_i); only X_i and Y_i share S_i. Fix tau > 0.
2. Establish midpoint median consistency and raw MAD consistency at 0 and 1.
   A zero density at the median prevents the usual root-n median expansion,
   not consistency. Establish consistent Huber roots separately by score
   uniform LLN, monotonicity, and strict population signs around zero.
3. Apply Lemma RI to the bounded score class, using only scale consistency.
4. Symmetry gives q(0,s)=0 for every positive s. The identity
   q(t,s) = -integral_0^t P(|W-v|<cs)/s dv gives
   q(T_hat,s_hat)=-(A/k+o_P(1))T_hat. Combining this with the empirical
   score residual o_P(n^-1/2) first proves root-n T_hat and then its expansion
   sqrt(n) T_hat = (k/A) G_n psi_c(W/k) + o_P(1).
5. For h_(t,u)=(|X-t||Y-u|,|X-t|,|Y-u|,(X-t)^2,(Y-u)^2), all first
   derivatives of P h at zero vanish. In particular |Y| is independent of X
   because V is independent of (S,U); likewise |X| is independent of Y.
6. A locally bounded marginal density and the absolute-value remainder bound
   give ||P h_(t,u)-P h_(0,0)|| <= C_tau(t^2+u^2+|tu|), uniformly on a fixed
   small neighborhood. For the paired product, use
   |Y| Delta_X + |X| Delta_Y + Delta_X Delta_Y and |Delta_X| <= |t|.
7. Local moment classes are Donsker under their square-integrable envelopes.
   Lemma RI controls their empirical difference. Step 4 controls the
   population second-order term. Hence sqrt(n)(M_hat-M_oracle)=o_P(1).
8. Smoothness at positive profile variances gives correlation oracle
   equivalence. Independent nondegenerate radii with finite fourth moments
   give the oracle influence (a-Ea)(b-Eb)/sqrt(Var(a)Var(b)), of variance 1.

The explicit paired-product envelope check is

    E[(|X|+M)^2(|Y|+M)^2]
      = [exp(2 tau^2) + 2M exp(tau^2/2) + M^2]^2 < infinity.

Squared-radius envelopes require E(|W|+M)^4 < infinity, which follows from
E|W|^r = exp(r^2 tau^2/2). None of these are uniform-in-tau claims.

### Scale convergence: what has and has not been established

Let d_tilde be the sample midpoint median of |W_i|. Order statistics and
midpoint medians are 1-Lipschitz under coordinatewise sup-norm perturbations,
so |d_hat-d_tilde| <= |m_hat|. Since the population radius median has positive
density, d_tilde-1=O_P(n^-1/2). Consequently

    |s_hat-k| <= k |m_hat| + k |d_tilde-1|.

This proves consistency and gives a rate bound in terms of median error; it
does not identify the exact MAD rate, its sign, or its limiting distribution.
No exp(-C sqrt(log n)) rate is claimed here. Deriving a sharp rate would
require a separate quantile/order-statistic analysis. The Huber argument
does not require that rate because q(0,s) vanishes identically in s.
An O_P(n^-1/2) statement is about a sequence, not a finite-n accuracy bound.

## Frozen finite-sample evidence, not a limit validation

Source: ../results/reference_pathway_summary_20260909.tsv . All rows below
have tau=.1, root seed 2026090901, and 2,000 replications per cell.

| n | Mean rho, fixed reference | Mean rho, fixed scale | Mean rho, full fit | Mean fitted scale X, full fit | Median RMSE X | Reference RMSE X, full fit |
|---|---:|---:|---:|---:|---:|---:|
| 80 | .0006351 | .3804208 | .8206744 | .5354496 | .8225149 | .5055524 |
| 640 | -.0006059 | .1116500 | .6305944 | .6178805 | .8088261 | .2789732 |

Population scale is k=1.4826. These summaries directly demonstrate that the
examined full-fit samples do not have small scale errors. Two sample sizes
do not establish an eventual rate, monotonicity, or entry into an asymptotic
regime. No extra sample sizes were generated for this note. Other historical
designs must not be spliced into this table as one common simulation design.
If the candidate consistency/CLT is proved, boundedness |rho_hat|<=1 implies
E rho_hat -> 0 (with a bounded convention on asymptotically negligible
undefined samples), but it does not imply sqrt(n) E rho_hat -> 0 without
additional uniform integrability. No finite sample size threshold follows.

## Empirical moving windows: a separate auxiliary lemma

For IID (X_i,Z_i), E|Z|<infinity, P(X=t0)=0, T_hat ->_P t0 and b_n>=0
with b_n ->_P 0, P_n[|Z|1{|X-T_hat|<=b_n}] ->_P 0. The window and centre
may depend on the full sample. On |T_hat-t0|+b_n<=epsilon dominate by the
fixed-window integrable function |Z|1{|X-t0|<=epsilon}; apply LLN for fixed
epsilon, then dominated convergence as epsilon decreases to zero.

This lemma is useful for regular fitted moving-sign coefficients: the
weighted sign difference is bounded by |u_hat-u0| plus
2|Y-u0|1{|X-t0|<=|t_hat-t0|}. With squared weights it supports analogous
empirical-norm controls. It belongs with S1.3 class/coefficient verification
and S1.5 plug-in consistency if explicitly included. The population L2
continuity argument there uses P, not P_n.

It is NOT a required additional step in the candidate shared-sign proof
above: that proof uses deterministic population remainder bounds and
Donsker random-index substitution. Do not conflate these two routes.

## Reporting and implementation boundaries

The candidate point-estimator CLT does not establish n SE_full^2 ->_P 1.
The regular-form full-IF Wald limit under shared-sign is not established
here; no claim of universal impossibility is intended. Report rejection
rates as empirical behavior of specified procedures, not evidence of their
asymptotic validity. Place this boundary in abstract scope, the shared-sign
numerical discussion and table note, as well as Discussion, if revising the
manuscript. Point-estimate and staged intermediate-reference comparisons
support the mechanism without any studentizer.

Root certificates are a proposed supplementary reproducibility addition,
not a completed output of this note. Existing exact score checks certify
residuals for represented float inputs, not every location-error bound.
The 6,000-dataset/12,000-margin September 20 log lacks segmentwise active
fractions. If raw arrays are unavailable, replay would regenerate the same
draws using the recorded generator and seeds, not add Monte Carlo cells.
Scope a future certificate pass first to that regular benchmark and the
two retained September 9 root flags; expand only if claiming certification
of all displayed main cells. A complete-main-evidence claim would also
require the remaining retained designs, not just these selected checks.

Save per fit: input provenance, fitted scale, certified root bracket and
endpoint score signs, returned location, exact residual, active-fraction
lower bound on the segment containing the bracket and returned location,
and a bracket-width or slope-based location-error bound. A zero conservative
active lower bound must be reported, not replaced by an endpoint fraction.
Recompute target and complete IF for numerical sensitivity comparisons;
location certificates alone do not certify SE accuracy or statistical size.

Under fixed regular-law slope and scale conditions, o_P(n^-1/2) score
residual gives negligible first-order location error. Finite certificates
document selected computations and are not the proof of that asymptotic
statement. No certificate replay has been run in this update.

## Remaining review decisions

- Independently review current S1, especially class closure, coefficient
  localization and weak-null empirical norms.
- Review the candidate fixed-tau steps separately before theorem promotion.
- Do not infer finite-sample performance from an O_P bound or weak limit.
- Do not label an unproved limit a numerical observation.
- Decide manuscript placement with Hoorn; no restructuring is enacted here.

## Follow-up corrections and disposition in the revised draft

The October 12 manuscript preserves the six-section structure and strengthens
the regular proof exposition and reporting boundaries. It does not promote
the candidate fixed-tau CLT to a manuscript theorem. The independent-review
guide prioritizes the formal regular results; the candidate remains separate.

### Location and correlation expansions are different

The expression (k/A) G_n psi_c(W/k) is the leading term for sqrt(n) T_hat,
not sqrt(n) rho_hat. The latter requires profile-oracle equivalence and the
separate radius-correlation CLT. If that proof is completed, the constant SE
1/sqrt(n) is sufficient for pointwise calibration in this fixed model family.
It needs no nontrivial variance-estimator consistency theorem. A fitted
oracle-form plug-in SE would require its own explicit consistency argument.
The target is identically zero in this family; this is not a general
confidence-interval theorem for unknown nonzero correlations.

### Shared signs induce dependent fitted reference errors

Put R=exp(tau U), A=P(R<ck), and L(r)=(k/A) psi_c(r/k). Under the candidate
location expansions, the two reference influences are S L(R_X) and
S L(R_Y). Their limiting covariance is (E L(R))^2 > 0, while each limiting
variance is E L(R)^2. Independent radii do not imply asymptotically independent
fitted locations. Oracle equivalence uses root-n marginal rates and zero
target derivatives, not independence of the fitted references: their product
is still O_P(n^-1). The empirical-process class is indexed by intact pairs.

### Root accuracy at a fixed tau

For this model, p_tau=P(|W|<ck/2)>0 at each fixed tau>0. On s_hat>3k/4
and |t|<ck/8, all observations with |W|<ck/2 are active at t. Thus the
LLN bounds the empirical active fraction uniformly below on this local
segment by p_tau/2 with probability tending to one. Together with scale
consistency this gives s_hat/alpha=O_P(1) for consistent computed/exact
roots on the segment. No lower bound on f(0) is required here. This is a
fixed-law argument, not uniform in tau or a stored numerical certificate.

The statement must continue to assume exact or sufficiently accurate
consistent empirical roots. Finite residual records do not by themselves
establish every root-location error or solver success for arbitrarily large n.

### Simulation procedures and audit boundary

The pathway code uses the two-sided cutoff 1.959963984540054. Full fitting
uses the regular-form full-IF SE; direct-only uses the empirical direct IF
at the same fitted references. The population-reference oracle is a separate
stage. No frozen table reports the candidate constant-SE 1/sqrt(n) procedure.
These procedures must not be relabelled to match a new theorem.

Pathway records contain active fractions at returned locations, but these
are not segmentwise lower-bound certificates. The September 20 12,000-fit
residual log does not store such segmentwise bounds. No new certificate
replay or simulation was run for this revision.
