# Six proposed completion tasks: decisions and bounded results

Date: 2026-09-20. The September 18 working paper remains the canonical author
draft. Today supplies tested evidence and short proposed LaTeX blocks, not a
longer replacement paper or a competing Introduction. Initial Git state was
clean at a149241, main equal to origin/main; no push is performed here.

## Decisions

| Proposal | Action now | Status / next dependency |
|---|---|---|
| Independent mathematical review | Reuse the versioned September 18 review package; prioritize a focused technical review rather than asking for a general reading of 37 pages | External review remains open; authors must identify/approach a suitable reviewer |
| Positive nonzero active-nuisance benchmark | Run one prespecified moderate law, retaining results irrespective of coverage | Completed as a bounded check; **did not yield a nominal-coverage success example** |
| Theory versus legacy solver | Compare checked and legacy modes on every new dataset; draft explicit method/release wording | Numerical comparison completed; fixed-precision asymptotic success still unproved |
| Constants c and k | Explain normal-model conventions and exact product dependence; two population-only alternatives | Completed; alternative targets differ; no coverage sensitivity grid |
| Target distinction table | Correct the proposed yes/no reference column to estimated ingredients; give population null meanings | Short LaTeX block ready; current working paper unchanged |
| Closest literature | Verify bounded roles for the suggested sources, including published robust distance covariance | Citation-ready text prepared; no survey expansion |

## One-law benchmark, without selecting a favorable result

The internal protocol was fixed before truth integration or outcomes. It uses
the previous lognormal-pair structure with log SD halved to .3 and latent
correlation fixed at .4. The root seed is 2026092001; sample sizes are
160/640/2560 with 2,000 replications each. Checked complete IF, direct-only
with those same fitted references, and population-reference oracle give
18,000 method rows from 6,000 datasets. There are no error returns.

Numerical truth is rho_P=0.1625386847281758, Huber T=1.0208816124782667,
raw MAD=.200080494777416, reference coefficient=-.2897114962006473
per margin. The full IF variance is 1.7693251308084323; direct variance is
1.7774794886234. Nuisance variance .023559222346506 and twice the
direct–nuisance covariance -.031713580161474 substantially cancel. Thus
active nuisance is verified, but this is not a design in which omission must
produce a large variance difference. Coefficients carry inverse data units;
their magnitudes should not be compared across scales without normalization.

| n | Complete coverage | 95% Wilson | Direct | Oracle | Complete SE/SD |
|---:|---:|---|---:|---:|---:|
| 160 | .9045 | [.89083,.91662] | .8990 | .9050 | .91025 |
| 640 | .9355 | [.92388,.94545] | .9345 | .9355 | .98246 |
| 2560 | .9365 | [.92495,.94637] | .9370 | .9375 | .96809 |

All complete Wilson intervals exclude .95. Coverage improves from n=160,
but the upper two sizes do not establish continuing monotone improvement.
All results remain on record. No additional law, seed or larger n is searched
to obtain a success example. The oracle also undercovers, so reference
estimation cannot be the sole explanation. The paired complete-minus-direct
coverage differences are .0055/.001/-.0005, MCSE .001933/.000707/.000500;
there is no basis for a general finite-sample superiority claim.

The user-proposed *positive* benchmark remains an unmet aspiration, not a
condition for the present pointwise-plus-failure paper. A new design should
require a substantive question or supervisor agreement, not a desire to fill
that narrative slot. The new study can instead support the numerical solver
comparison and, if included later, an honestly described supplementary check.

## Complete prospective solver comparison

Every dataset was evaluated with the existing checked and legacy APIs. All
12,000 marginal exact-rational residual checks passed; zero checked/legacy
coverage decisions changed. Maximum absolute estimate difference divided by
checked SE was 6.148e-10; maximum absolute relative SE difference was
7.467e-11; maximum sqrt(n) legacy score residual was 2.621e-9. Both
prespecified numerical thresholds, 1e-4, were satisfied throughout.

The comparison is prospective for this law and seed, and complete for all
6,000 scheduled datasets. It is not an independent implementation. It rules
out a material discrepancy between these two solvers in this checked sample,
not every source of statistical error or all possible root failures.

For future analyses, explicitly request `reference_solver="score_checked"`
and retain/report failures. Keep the current API default legacy for backward
compatibility until a deliberate versioned release decision. This recommendation
does not relabel historical results or turn successful return into a regularity
certificate. The theoretical estimator remains an exact/sufficiently accurate
empirical root; finite-precision success probability is a separate obligation.

## Constants are part of the target

k=1/Phi^{-1}(.75), rounded to 1.4826, normalizes the population MAD to the
normal SD. c=1.345 gives approximately .95 normal-model asymptotic efficiency
for Huber location at consistent scale; this is not efficiency or coverage
of the resulting profile correlation. The normal efficiency was separately
computed as A^2/E psi_c(Z)^2=.9500002597.

The identity psi_c(u)=c psi_1(u/c) means the location root depends on c and k
through c*k when raw MAD is fixed. In asymmetric laws, changing that product
generally changes T and hence rho_P. At a symmetric law with unique root,
T remains its symmetry center; this does not guarantee unchanged finite-sample
fitting or calibration. This exact fact avoids an unnecessary two-dimensional
tuning grid.

For the existing .6-log-SD, .4-latent-correlation law, at fixed k=1.4826:

| c | Population T | Population rho_P |
|---:|---:|---:|
| 1.0 | 1.049022985 | .202799971 |
| 1.345 | 1.079808861 | .193475119 |
| 1.5 | 1.093192473 | .189487657 |

Positive association persists in these two alternatives; numerical target
equality does not. These are population-target checks, not evidence that
coverage or the shared-sign failure rate is insensitive to c or k.

## Independent-review agenda and communication burden

The existing external-review package already asks the six substantive
questions. First request focused scrutiny of S1.3 (entropy, random coefficients,
moving boundaries), S1.6 (empirical versus population L2), and Proposition 1.
Then check S1.5 and S1.7 together with the precise R5 wording and source code.
All assumptions and main IF equations must accompany excerpts; do not send
isolated inequalities without context. One qualified reviewer can cover both
passes; a second specialist is useful only if necessary expertise is missing.

Reviewer disposition must say valid as written / local gap / added assumption /
false / not reviewed, with exact locations. Neither the present checks nor a
second AI reading will be described as independent mathematical review.
This is an ordered agenda, not a booked appointment or a background automation.
No reviewer or supervisor has been contacted.

At the next natural author follow-up, a one-page progress summary and three
decisions would be easier to digest than another full attachment: (i) scope
and Introduction; (ii) who can review the proof; (iii) whether to include this
additional supplementary check. There is no need to ask Hoorn to adjudicate
every local software detail or to send another long paper immediately.

## Verification

Conditional integration and 48/72-node tensor quadrature agree under the
protocol tolerances. A post-run four-direction contamination check has maximum
scaled discrepancy 1.230e-5 at epsilon=1e-6. All replication identities,
coverage decisions, summaries, paired differences, tail counts and 12,000
exact rational inequalities were audited. Original TSV hashes remain unchanged.
Fifteen focused tests pass, including residual negative controls and a check
that copied function defaults use sigma=.3 rather than the old .6. No production
estimator source was changed. Full-suite testing was not repeated.

The protocol, full replication and solver records, population calculations,
paired summaries and audit metadata use `moderate_benchmark_*_20260920` names.
The proposed LaTeX blocks are outside the research repository. Independent
review, final placement and any future default change remain open.
