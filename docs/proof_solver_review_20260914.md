# Local proof and numerical-root review — 2026-09-14

Status: internal AI-assisted mathematical review and targeted implementation
audit. This is neither independent mathematical peer review nor a proof of
finite-sample calibration. The editing reference is the September 14 candidate
derived from the September 12 working paper. No manuscript PDF is replaced by
this review.

## 1. What can be closed locally

The existing S1 already uses a paired Bahadur/Z-estimation route. Its proof does
not need an unspecified topology on all probability laws. The local tasks are
to expose the steps below for scrutiny, verify their match to the source
theorem, and test the numerical implementation against deterministic identities
and failure examples. Independent review remains a separate external task.

Theorem 2.1 of van der Vaart and Wellner (2007), *Empirical processes indexed by
estimated functions*, assumes localization to a fixed Donsker class with
probability tending to one and L2(P) convergence. It then permits the estimated
index substitution. These are the obligations addressed in S1.3; citing the
theorem alone would not verify them. Author-hosted source, p.236:
https://sites.stat.washington.edu/jaw/JAW-papers/NR/jaw-vdv-07LNMS.pdf

### 1.1 Moving boundaries with dependent pairs

Write b=|Y-u0|, |t-t0|<=delta and |u-u0|<=delta. Pointwise,

    |sign(X-t)|Y-u| - sign(X-t0)|Y-u0||
       <= |u-u0| + 2 b 1{|X-t0|<=|t-t0|}.

Consequently its squared population L2 norm is at most

    2 delta^2 + 8 E[b^2 1{|X-t0|<=delta}].

Finite E b^2 and P(X=t0)=0 make this bound tend to zero by dominated
convergence. No factorization into marginal probabilities is used: X and Y
may be dependent. The same pointwise inequality gives uniform control over
the shrinking deterministic parameter neighborhood. This closes the gap
between checking continuity along one sequence and applying localization
to random fitted locations. The boundary equality cases satisfy the bound
under sign(0)=0; their population mass vanishes at the limiting reference.

The half-line/interval classes are VC. A weighted moving-sign subgraph is a
finite union of intersections of half-spaces after partitioning by signs of
x-t and y-u. The unbounded weight has square-integrable envelope |Y|+M.
Translated products use the explicit Lipschitz bounds in S1.3 and an L2
envelope, rather than an unjustified closure under arbitrary products of
unbounded Donsker classes.

### 1.2 Random coefficients and squared influences

All boundary-density values, A, B and moment ratios converge in probability
to finite constants, with limiting denominators strictly positive. Put them
in a deterministic compact coefficient set whose interior contains those
limits. The event that all fitted coefficients belong to the set has
probability tending to one. They need not be independent of the data.

For a finite sum F=sum_j c_j f_j, component covers and coefficient covers give
a product cover; errors are bounded by the sum of component errors. A common
envelope H with PH^2<infinity controls coefficient perturbations. Combining
this with the preceding uniform boundary bound gives the L2(P) continuity
required for random-index substitution. The finite-dimensional localization
applies to the default KDE, whose density estimates are scalar coefficients;
it does not silently establish validity for every cross-fit option.

For the square class, truncate each influence at +/-L. Squaring on this
bounded interval is Lipschitz. The omitted contribution is bounded by
H^2 1{H>L}. First take n to infinity for fixed L using GC/LLN; then take
L to infinity by integrability of H^2. This establishes the squared-class GC
step without requiring an eighth moment. Merely proving pointwise convergence
of a fitted influence would not suffice for its in-sample variance.

### 1.3 Weak null with infinite fourth moments

Keep all reference regularity/nondegeneracy conditions and the reduced moment
assumptions E[a^(2+eta)+b^(2+eta)+(ab)^(2+eta)]<infinity for some eta>0.
The three-moment expansion gives a root-n numerator under rho_P=0; consistency
of the squared-moment denominator gives rho_hat=O_P(n^-1/2).

Here is the missing explicit tail step. If E a^2<infinity, for epsilon>0,

    P(max_i a_i^2 > n epsilon)
      <= n P(a^2 > n epsilon)
      <= E[a^2 1{a^2>n epsilon}]/epsilon -> 0.

The ordinary LLN gives P_n a^2=O_P(1). Therefore

    (P_n a^4)/n <= (max_i a_i^2/n) P_n a^2 = o_P(1),
    rho_hat^2 P_n a^4 = (n rho_hat^2) (P_n a^4/n) = o_P(1).

No independence between rho_hat and P_n a^4 is required for the last product.
For fitted radii, a_hat<=a+|T_hat-T| gives
P_n a_hat^4<=8 P_n a^4+8|T_hat-T|^4. Empirical centering does not enlarge
the norm of a squared-radius component: P_n(a_hat^2-P_n a_hat^2)^2
<=P_n a_hat^4. Positive limiting profile variances keep denominators bounded
away from zero. Thus the two quadratic components of the unrestricted IF
are negligible in the empirical norm. Their cross terms with the reduced
IF vanish by empirical Cauchy--Schwarz. Additional rho_hat-weighted scalar
coefficients multiplying reference IFs also vanish after coefficient
localization and the reference IF's empirical L2 bound.

This argument does not imply population L2 consistency of the unrestricted
plug-in function. A concrete scope witness is independent t3 margins: they
have positive regular boundary densities, finite moments below order 3,
independent population radii, and infinite fourth moments. The reduced
conditions hold for 0<eta<1. Conditional on any fitted coefficients with
nonzero rho_hat, the unrestricted IF as a function of a fresh x contains
a nonzero quadratic term. Its squared integral in x is infinite: the t3
density has order |x|^-4, while the squared leading term has order x^4.
Other terms have at most linear growth in x when y is fixed; bounded
reference IF terms cannot cancel this quadratic term. Fubini then gives
infinite joint second moment. The empirical sample still has a finite norm.
This is an analytic example, not a newly simulated t3 study.

## 2. A constructive route to R5

Let the same fitted median/MAD produce s_hat>0, and define the empirical score

    q_n(t)=n^-1 sum_i psi_c((W_i-t)/s_hat).

Prescribe eta_n=1/(10^8 n). Accept t_tilde only if |q_n(t_tilde)|<=eta_n.
Then sqrt(n)|q_n(t_tilde)|<=1/(10^8 sqrt(n))->0. The constant 10^-8 is
an engineering precision choice; any fixed positive constant times n^-1
has the required asymptotic order. It is not a calibration tuning parameter.

### 2.1 Existence and termination in ideal arithmetic

For finite observations the clipped score is continuous and nonincreasing,
with q_n(min W)>=0 and q_n(max W)<=0. Hence the bracket contains a root,
possibly a root interval. It is globally 1/s_hat-Lipschitz. If a root-containing
bracket has width L, its midpoint therefore has |q_n(t)|<=L/(2 s_hat).
After j exact bisections, width L0/2^j suffices. A finite j with

    L0 / (2^(j+1) s_hat) <= eta_n

always exists. No lower score slope is needed for this residual bound, and
neither uniqueness nor a valid IF follows from it. A fixed maximum iteration
count is not part of this ideal-arithmetic termination theorem.

### 2.2 Consistency and equivalence to exact roots at a regular law

Suppose the sample scale is consistent, the population root T is unique and
the remaining regular reference conditions hold. For any fixed epsilon>0,
population monotonicity/uniqueness give q(T-epsilon)>0>q(T+epsilon).
The bounded score LLN and scale substitution preserve these strict signs
with probability tending to one. Since eta_n->0, any accepted approximate
root must lie between those endpoints on that event. Thus t_tilde->P T.

With A=P(|(W-T)/s|<c)>0, choose a fixed strict inner active interval with
positive probability. Consistency of s_hat and both reference locations,
together with the interval-class LLN, gives a positive lower empirical
active fraction alpha along the entire local segment with probability
tending to one. Integrating the score slope gives, for any local exact root,

    |t_tilde-t_exact| <= s_hat eta_n/alpha = O_P(n^-1).

Thus the approximate and exact reference fits are first-order equivalent.
The existing paired moment expansion and empirical variance argument then
transfer the pointwise result, under their own conditions. This proof adds
no uniform guarantee near a weak slope, and does not establish regularity of
the shared-sign sample median.

### 2.3 What is implemented and what remains conditional

The dated diagnostic script implements bracketed numerical search and accepts
only after exact rational evaluation of the score on the represented input
floats, stored fitted scale, clipping constant and returned location. This
catches floating-point cancellation that a floating mean alone can hide.
It is a certificate for that particular residual inequality, not a
statistical-validity certificate.

The candidate retains a 512-iteration failure guard; exhausting it or reaching
adjacent floating endpoints raises an error. This differs explicitly from the
uncapped ideal-arithmetic argument. Exact rational acceptance does not prove
that a floating candidate always exists, that the routine succeeds with
probability tending to one as n grows without bound at fixed machine precision,
or that rounded median/MAD calculations themselves have negligible asymptotic
error. A general computational asymptotic theorem would require matching
precision and iteration budgets. The bounded study can check neither limit.

The public source remains unchanged. Consequently the historical simulations
still use the original fixed-tolerance estimator. Successful checks cannot
retroactively claim that its stopping rule enforces R5. The practical options
are to retain the present theorem/software qualification, or later adopt an
explicit optional residual-checked mode with clear failure behavior and its
own validation. Changing a default requires a separate review of callers,
runtime cost and numerical compatibility; it is not done here.

## 3. Independent-review handoff

An external reviewer should receive the complete S1, this clarification,
the theorem statement and the implementation correspondence, and be asked to
check the following specific propositions:

1. Joint midpoint-median/MAD Bahadur expansion with paired dependence.
2. Local entropy/measurability and all moving weighted-boundary classes.
3. Random coefficient localization and squared-class GC under the stated moments.
4. Weak-null empirical-norm studentization without importing a five-moment CLT.
5. The real-arithmetic stopping-rule result and its stated software boundary.

No person has independently reviewed or approved these arguments as part of
this local audit. Deterministic tests can reject an incorrect algebraic bound
or implementation; their passing is not mathematical peer review.

## 4. Numerical results

All 41 existing datasets completed, with all 82 candidate margins passing
the exact represented-input residual inequality and zero reported failures.
Twenty-seven new deterministic tests and 14 existing public-API/pathway tests
passed (41 targeted tests total). The complete historical test suite was not
rerun. No new simulation cell was generated.

| Existing selection | Skew | Pathway |
|---|---:|---:|
| Datasets / margins | 27 / 54 | 14 / 28 |
| Legacy margins outside the new engineering tolerance | 19 | 8 |
| Maximum absolute legacy score | 2.07246e-11 | 1.01405e-6 |
| Maximum absolute candidate score | 6.23812e-11 | 1.00509e-10 |
| Maximum candidate iterations | 41 | 37 |
| Maximum absolute correlation change | 1.06787e-11 | 4.68160e-7 |
| Maximum absolute relative full-SE change | 2.01288e-11 | 3.02300e-5 |
| Changed full/direct decisions | 0 / 0 | 0 / 0 |

The new tolerance depends on n; the maximum score across different n is not
a test of the acceptance rule. The candidate is not necessarily more accurate
than an already adequate legacy root on every dataset. In particular, the
aggregate maximum skew score is larger for the candidate, while every exact
candidate check passes its own declared threshold. The 27 legacy threshold
exceedances are not new scientific failure flags, invalid p-values, or evidence
that those observations fail an asymptotic condition. This is an engineering
criterion that was not enforced by the historical algorithm.

The pathway full-SE change is approximately 0.003023 percent. No checked
decision changed, agreeing with the bounded September 12 bracketing result.
This targeted selection cannot support a new coverage estimate, a general
reliability claim, or a claim that numerical refinement fixes skew undercoverage.

See `results/proof_solver_audit_20260914.json` for every attempted dataset,
per-margin exact scores, full-IF comparisons, failures and source hashes.
These results are separate from the mathematical arguments above.

Reproduction commands from the project root (choose a fresh report path):

```bash
python -m pytest -q tests/test_proof_solver_20260914.py tests/test_public_rho_api_20260901.py tests/test_reference_pathway_20260909.py
python scripts/audit_proof_solver_20260914.py --report /tmp/proof_solver_recheck.json
```

The recorded run used the existing isolated Python environment with
Python 3.12.3 and NumPy 1.26.4; see the machine-readable report for its
executable and source hashes. The report command refuses to overwrite an
existing file. The primary implementation and frozen source hashes were
rechecked after the audit.
