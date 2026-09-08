# High-standard methodological referee review

Date: 2026-09-08. Internal AI-assisted critical review, **not independent peer
review**, an editorial decision, or an acceptance-probability assessment.

## Overall judgement

There is a coherent methodological research question and a substantial
reproducible evidence base. The manuscript is **not submission-ready for a
high-selectivity methodological journal**. The main gap is not simulation
volume: it is demonstrating that the problem-specific insight is sufficiently
important beyond an application of established IF machinery, and stating
exactly what practitioners can and cannot learn from it.

The defensible current paper is an analysis of reliability and failure of a
generated-reference profile target. It is not yet a paper establishing a
generally effective finite-sample inference method. Negative calibration
results are not disqualifying for a critical methodological paper, but become
a central contradiction if the title or abstract promises calibrated safety.
The provisional title should be discussed, not silently changed: for example,
*Inference for Robust-Reference Profile Correlation: Regularity and
Finite-Sample Failure* would communicate the present scope more directly.

## External benchmark, not a chosen submission destination

JRSS B's current instructions emphasize methodological understanding and
practical relevance. They explicitly warn that correctness alone does not
suffice when a paper is a straightforward special case, disproportionate in
length, or dominated by routine computation. Critical evaluations are within
scope; a new broadly useful procedure is not the only possible contribution.
The instructions also require disclosure of relevant AI assistance. These
are a demanding comparator, not a recommendation that this project is already
competitive there. Sources checked on 2026-09-08:

- [JRSS B author instructions](https://academic.oup.com/jrsssb/pages/general-instructions).
- [JRSS C author instructions](https://academic.oup.com/jrsssc/pages/general-instructions):
  an applied-paper route makes a genuine motivating application central.
- [Morris, White and Crowther (2019)](https://doi.org/10.1002/sim.8086):
  ADEMP planning and Monte Carlo uncertainty distinguish clear simulation
  questions from accumulating favorable numerical examples.

## Priority review concerns and closure criteria

| Priority | Referee question | Present evidence / shortfall | Required response |
|---|---|---|---|
| P0 | What is the paper's nonroutine contribution? | Complete generated-reference IF is technically useful but follows established methods. Stavig separation is not an exhaustive novelty proof. | State one transferable insight, closest same-target predecessors, and exactly what is not implied by existing theory. Do not equate a long derivation with major methodological novelty. |
| P0 | In what sense is inference trustworthy? | At the active-nuisance regular law, 95% coverage remains .927 at n=2560; all three full-coverage Wilson intervals exclude .95. | Lead with pointwise scope and measured finite-sample limits. If calibrated practical intervals are essential to the chosen paper, open a separately prespecified development phase. |
| P0 | Is the theorem fully justified, not merely asserted through A8? | Appendix supplies a plausible empirical-process route and detailed IF. Audit tests mostly verify algebra, source consistency, and examples. | Obtain independent mathematical review of assumptions, topology, joint paired Z-expansion, entropy closures, weak-null relaxation, and plug-in empirical variance. Record unresolved points explicitly. |
| P1 | Does Claim 2 prove a stochastic failure mechanism? | Strong paired interventions; nonregular median at each tau in the unbridged example; imposed-offset identity only. | Clearly distinguish algebra, intervention evidence, and an unproved switching law. A local-to-degeneracy theorem is optional for the bounded paper but may be the most valuable strengthening for a more ambitious one. |
| P1 | Does nuisance conditioning explain the target, or merely a nuisance? | J can be singular while the target projection annihilates the weak direction. Omega and the projection are not fixed by matching the scalar index. | Explicitly retain this distinction; do not claim universal necessity, sufficiency, or higher-order-only residuals. A stronger target-specific diagnostic is a new theoretical project, not a relabelling. |
| P1 | Is the method scientifically needed? | Estimand and classical target table are clear; no genuine application has been chosen. | Justify discarding sign, pairing, group-reference choice, and sampling units. For an applied route obtain a genuine application; for a theory route justify general relevance without pretending simulations are data. |
| P1 | Are comparisons fair and informative? | Same-target direct-only ablation and infeasible reference oracle exist; full/direct variance nearly cancels in the selected law. | Separate same-target inference comparisons from different-target coefficients. Do not claim broad superiority. Any further comparator must answer an explicit open claim. |
| P1 | Does the implemented algorithm approximate the theorem's estimator? | Public API uses 100 IRLS iterations and a fixed tolerance without a general convergence certificate. | Report root residual diagnostics; exact/asymptotically negligible numerical error belongs in theorem-to-software mapping. Harden solver diagnostics in a separate scoped change before a software release, without rewriting frozen results. |
| P1 | Can a referee reproduce the final paper independently? | Fixed seeds, hashes, retained draws, and tests are strong. No consolidated dependency specification or single clean manuscript build has been demonstrated. | Supply dependency/environment specification, one-command paper display build, and an independently rerun clean environment. Preserve algorithm versions and failed-replication reporting. |
| P2 | Is submission governance complete? | Section 7, final title/journal, abstract, supplement assembly, and AI disclosure are not final. | Confirm with the supervisor; disclose actual assistance accurately and retain author responsibility. Do not infer agreement from silence. |

P0 means a potential obstacle to the central submission argument; P1 means a
substantial obligation whose exact remedy depends on scope. These are review
priorities, not mathematical proof that the paper is false.

## Targeted proof-review questions

1. **Empirical-root approximation.** A6 states consistency/conventions but
   should explicitly require the fitted Huber score residual to be
   o_P(n^{-1/2}). A fixed tolerance is a numerical approximation, not a proof
   of that asymptotic condition. This condition is now stated in Appendix A;
   the production algorithm is unchanged.
2. **Tangent-space precision.** The appendix mentions weighted variation and
   a continuous empirical-process tangent. Specify the actual normed domain
   and topology before claiming an infinite-dimensional Hadamard theorem;
   an empirical distribution need not approach a continuous law in total
   variation. A finite-dimensional joint estimating-equation/Bahadur route
   may suffice for the IID result. This is a proof-presentation obligation,
   not a finding that the stated IF formula is incorrect.
3. **Paired stacking.** The displayed generic marginal Z-expansion should be
   read as a six-dimensional paired system for X and Y. Cross-margin score
   covariances must survive through the moments and target projection.
4. **Class closure.** Verify the sign-times-radius piecewise class, coefficient
   localization, squared-envelope integrability, and random density plug-ins.
   A8 is an assumption; citing it is not an independent proof that every
   intended law/implementation satisfies it.
5. **Weak-null relaxation.** Verify that consistency, rather than root-n
   convergence, of the squared moments is enough at rho=0 and that the
   unrestricted plug-in terms remain negligible under the stated lower
   moment conditions. Numerical tests cannot certify this over the law class.
6. **Population symmetry and singular J.** Nuisance weakness is not equivalent
   to target weakness. The proof and explanatory narrative must not turn a
   matrix-norm upper amplification scale into a universal stochastic rate
   or guaranteed target effect.

The current turn does not certify these six obligations as resolved. A
source-level or AI-assisted reread cannot be labelled independent review.

## Additional checks performed today: no new grid

### A. Frozen coverage decomposition

The 2026-09-07 draws were reanalysed after seeing their undercoverage. This is
explicitly **post hoc diagnosis**, not a preregistered confirmation or a new
interval proposal. The complete estimator was evaluated with its reported
plug-in SE and the separately integrated, infeasible population asymptotic SE.

| n | Reported coverage | Below-truth / above-truth misses | Population-SE diagnostic coverage | Population-SE below / above |
|---|---|---|---|---|
| 160 | .8580 | .1115 / .0305 | .9675 | .0080 / .0245 |
| 640 | .9115 | .0695 / .0190 | .9590 | .0100 / .0310 |
| 2560 | .9270 | .0595 / .0135 | .9580 | .0195 / .0225 |

"Below truth" means the entire interval is too low: estimate + critical*SE
is below the population target. The two one-sided nominal miss rates are
.025, not .05. All coverage and tail rates retain Wilson intervals in the
machine-readable table. Error/estimated-SE correlations are .597, .591, and
.550 across sizes. The same qualitative pattern appears for the
fixed-reference oracle.

The diagnostic changes both random SE variation and its association with
the estimator, as well as average interval scale. It therefore cannot isolate
a unique causal component. It suggests that studentization contributes
materially; it does not prove a KDE-only problem, prove asymptotic normality,
or make population-SE intervals usable. Favorable total coverage can coexist
with unequal tails or conservatism.

An exact identity, not a new asymptotic theorem, supplements this diagnosis:
with U=error/population-SE and delta=estimated-SE/population-SE-1,
Z=U-U*delta+U*delta^2/(1+delta). The n=2560 empirical mean components are
-.02444, -.10102, and .00435, giving -.12111. The stored table verifies the
identity for every finite positive SE to below 1e-12. This localizes the mean
shift to its algebraic components, not coverage error to unique causes.
It supplies no permission to drop the remainder or use population SE in data.

### B. Numerical-root replay

For the first three already simulated replications at each of the three
sample sizes, compare both fitted margins against a bracketed Huber root at
the same empirical MAD scale: 18 fits in total. The maximum difference is
2.35e-11 scale units (rounded upper bound). This provides no evidence that
solver error explains the observed regular-law undercoverage, but is not an
arbitrary-distribution convergence guarantee. It does not test pathological
nonregular fits or replace an algorithm-level failure indicator.

### C. Manuscript consistency

The active skeleton still contained a flat-reference shorthand, an
unqualified higher-order residual label, and overly optimistic submission
gates. Those are revised rather than left to conflict with Sections 3--6.
Section 8 now explicitly separates theorem, finite-sample failure,
post hoc studentization diagnosis, and future scope decisions. Older dated
experimental logs are historical records, not current readiness statements.

## Work sequence while awaiting the supervisor

1. **Completed today:** Discussion draft; targeted frozen-draw diagnostics;
   root replays; readiness-language repair; numerical/provenance regression
   tests. No new distribution family, interval tuning, or revised primary
   estimand.
2. **Next safe work:** assemble a reviewer-facing theorem/assumption checklist
   with precise source locations and an independently runnable reproduction
   recipe; prepare, but do not claim completion of, external proof review.
3. **Supervisor decisions:** paper identity, journal level, need for real
   application, and whether one stronger local theorem or a genuinely
   practical interval is essential. Do not pursue all extensions at once.

The project remains worth developing. The justified conclusion is that it
has a focused working-paper foundation, not that a high-tier publication is
secured or that only cosmetic polishing remains.

## Reproduce today's diagnostics

```bash
/opt/anaconda3/bin/python scripts/audit_referee_readiness_20260908.py
/opt/anaconda3/bin/python -m pytest -q
```

The audit reads the frozen September 7 replications and numerical population
variance, replays only the declared existing samples, and writes diagnostic
tables plus an LF-normalized source/output hash manifest. It does not alter
the primary API, September 7 results, or the canonical simulation sources.
