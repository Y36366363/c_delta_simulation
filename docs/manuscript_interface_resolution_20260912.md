# Literature positioning and bounded interface resolution

Date: 2026-09-12. Internal author work, not independent mathematical peer
review. Editing base: the user-approved `rho_p_minimal_preview.pdf` and its
matching `/private/tmp/rho_p_minimal_20260911/main.tex` (SHA-256
`dd7d01bc717b2f3e35d14de958fed0e8f91c90aa339571d2d9ec171ec353f66f`).
The earlier integrated Markdown remains a source of evidence; it is not the
authoritative current manuscript. The revised single-file LaTeX and PDF are
delivered outside the scientific repository, with a baseline diff.

## What existing theory establishes, and what this paper adds

| Existing contribution | Connection to this paper | Defensible additional contribution / boundary |
|---|---|---|
| Standard multistep/Z-estimation and influence propagation; Hahn and Ridder's generated-regressor calculations | First-stage uncertainty is not a new statistical principle. Their multistep nonparametric-regression problem is not this finite-dimensional marginal reference problem. | Derive the median-to-MAD-to-Huber terms and their projection into the paired five-moment correlation, and verify the local classes and variance consistency for this construction. Do not claim a new general nuisance-propagation theorem. |
| Robust signed-correlation constructions, including median/MAD and clipped-score methods surveyed by Shevlyakov and Smirnov | Ingredient overlap does not imply the same target. Robust correlation estimators often address signed association or a model correlation parameter. | Target unsigned reference-distance association; explicitly retain unbounded radii and the qualification “robust reference, not globally robust correlation.” No superiority or global novelty priority is asserted. |
| DiCiccio and Romano's studentized permutation theory for correlation of IID observed pairs | Fixed-population-reference radii are IID pairs and provide a connection to ordinary correlation theory. | Shared fitted references require a separate conditional argument before transferring their result to this generated-profile statistic. Our permutation panels remain empirical stress evidence; weak-null permutation inference is not declared impossible in general. |
| Quantile Bahadur expansions and empirical processes indexed by estimated functions | These supply the mathematical foundation, including the same-sample random-index issue. | Connect them to the actual midpoint convention, paired covariance, moving boundaries, default KDE, and empirical studentizer. Their existence is not itself a novelty claim. |
| Standard first-order conditioning analysis | Singular values organize local amplification under a fixed score normalization. | Work out the median direction, score covariance and target-projection limitations in this example. No universal scalar cutoff follows. |

The proposed contribution is a *construction-specific inferential result plus
a worked finite-sample failure analysis*. It includes a fixed-scale
location-error pathway, extra full-fit amplification, and the distinction
between correct first-order propagation and slow finite-sample convergence.
The skew example is not claimed to show a large coverage gain from full IF
terms: nonzero coefficients coexist with covariance cancellation.

Primary literature checked for this integration:

- Hahn and Ridder (2013), *Econometrica* 81, 315–340,
  [publisher record](https://onlinelibrary.wiley.com/doi/abs/10.3982/ECTA9609)
  and [2011 author version](https://www.princeton.edu/~erp/erp%20seminar%20pdfs/papersFall2011/GenRegHahnRidder.pdf).
- Shevlyakov and Smirnov (2011), *Austrian Journal of Statistics* 40, 147–156,
  [original article](https://www.stat.tugraz.at/AJS/ausg111%2B2/111%2B2Shevlyakov.pdf),
  especially Sections 1–2. No assertion that its MAD correlation equals our target.
- DiCiccio and Romano (2017), *JASA* 112, 1211–1220,
  [publisher abstract/record](https://www.tandfonline.com/doi/abs/10.1080/01621459.2016.1202117)
  and [author report record](https://statistics.stanford.edu/technical-reports/robust-permutation-tests-correlation-and-regression-coefficients).
  No theorem-number or detailed condition transfer is asserted from the abstract.
- van der Vaart and Wellner (2007),
  [author-hosted published article](https://sites.stat.washington.edu/jaw/JAW-papers/NR/jaw-vdv-07LNMS.pdf),
  Theorem 2.1, p. 236: a fixed localized Donsker class and population-L2
  convergence give the estimated-index replacement. These are exactly the
  two conditions verified locally in S1.3; no root-n rate is required just
  for that replacement step.

## Proof interface: resolved exposition and outstanding review

| Obligation | Current resolution | Status / what still needs review |
|---|---|---|
| Functional domain/topology | Explicit paired IID Bahadur/Z route; no unspecified global Hadamard/Fréchet claim | Presentation resolved; regularity assumptions remain explicit |
| Midpoint median and MAD | Quantile scores have O(1/n) residuals for continuous samples; expand G(m,d) with derivative (f_plus-f_minus, f_plus+f_minus) before solving the MAD equation | Actual convention retained; independent check of the joint expansion requested |
| Moving boundaries | Half-lines/intervals and piecewise subgraphs; no atoms at limiting boundaries; weighted L2 domination using the other margin's second moment | Existing class verification retained, not replaced by a generic citation |
| Random coefficients and squared IF | Deterministic compact localization; finite covers for sums and scalar multiplication; truncate then control H-squared tails to establish GC | No assertion that arbitrary unbounded Donsker products are Donsker; no eighth-moment assumption introduced |
| Random KDE bandwidth and fitted evaluation points | New self-contained Gaussian-kernel argument in S1.5: bounded-variable grid bound, parameter derivative extension, local bias control, then random-band and random-point substitution | Author-level sufficient proof supplied; independent mathematical review remains open |
| Weak-null lower moments | Retain reduced three-moment route and empirical-norm negligibility of fitted quadratic terms | Population L2 consistency of an unrestricted plug-in IF is not asserted with infinite fourth moments |
| Numerical root condition | New deterministic residual-to-location bound under an active-fraction lower bound along the root segment; direct full-IF bracketed comparison on 41 existing datasets | Does not prove that fixed tolerance/100 iterations satisfies o_P(n^-1/2) for every regular law |

For the new KDE argument, on a compact evaluation interval and
`h in [c1 n^(-1/5), c2 n^(-1/5)]`, the Gaussian density summand is bounded
by K/h_min and its two parameter derivatives by K/h_min^2. A mesh n^(-2)
grid has polynomial cardinality. Hoeffding plus a union bound gives the
crude stochastic order `sqrt(log n)/(sqrt(n) h_min)`, which tends to zero;
the off-grid error is `O(n^(-2) h_min^(-2))`. Local continuity handles the
near-field bias, and Gaussian decay together with total density mass one
handles the far field. This proof needs no global density bound and no
independence of the fitted bandwidth/evaluation points. It is a sufficient
consistency proof, not an optimal-rate result or new general KDE theorem.

The deterministic root bound integrates the continuous piecewise-linear
empirical Huber score. Its active-fraction lower bound must hold along the
whole segment almost everywhere, not just at one endpoint. Without that
condition, the bound must not be used as a general accuracy certificate.

Independent mathematical acceptance is still outstanding. A reviewer should
specifically assess the localization/measurability choices, midpoint residual
argument, Gaussian grid-and-bias proof, and weak-null empirical-norm route.
No new broad simulations are needed to answer these mathematical questions.

## Numerical and final-LaTeX interfaces

The protocol in `manuscript_interface_protocol_20260912.md` preceded this
bounded replay. A fresh virtual environment without system-site-packages
installed Python-3.12-compatible NumPy 1.26.4, SciPy 1.16.3, pytest 7.4.4,
and Matplotlib 3.9.2 (the last is imported by the historical display audit).
`requirements-manuscript-audit-lock.txt` records all installed audit packages.
A separate snapshot of the current scripts, sources, evidence and tests at
`/private/tmp/rho_interface_snapshot_20260912` was used for the final runs.
It includes authorized uncommitted integration files; it is not a claim of
reproduction from a published Git release.

- 27 skew and 14 pathway datasets; 137 saved method/stage rows and 193 saved
  coverage/rejection decisions checked. Maximum saved-value discrepancy,
  normalized by max(1,abs(saved)), was 1.491862189340054e-16.
- Recomputed bracketed-root complete IF: maximum correlation changes were
  1.2190852887981776e-10 original-SE units for skew and
  1.6203795470922866e-6 for pathway; maximum relative full-SE changes were
  7.08988423525625e-12 and 3.022980213540638e-5 respectively. No full/direct
  decision changed. The two historical flags are retained.
- The final LaTeX audit checks 19 actual table bodies, 1,047 cells, row
  identities and citation/reference keys. Source reconstruction includes the
  earlier bounded 2,000-dataset replay at stored references for CV summaries.
  It does not verify all prose numbers, every caption, or the mathematics.
- Negative controls modify coverage, seed and NA, or remove/duplicate a
  table. They must fail. The six final-LaTeX tests and eleven existing
  completion/integration tests passed (17 total). Matplotlib emitted 14
  dependency deprecation warnings; these are distinct from LaTeX diagnostics.
- No new simulation cell, permutation study or coverage recalibration was
  performed. Core algorithms, constants and frozen scientific outputs remain
  unchanged. This is bounded clean-environment reproduction, not a complete
  rerun of all historical studies or the entire test suite.

Machine-readable details: `results/manuscript_numerical_replay_20260912.json`
and `results/manuscript_final_latex_audit_20260912.json`. The latter records
the hash of the exact final LaTeX it checked.

## Repeat the bounded checks

In an isolated snapshot/check-out with the selected manuscript exported from
Overleaf to `main.tex`, create a Python 3.12 environment and run:

```sh
python -m pip install -r requirements-manuscript-audit-lock.txt
python scripts/audit_final_latex_20260912.py /path/to/main.tex --report /tmp/final-latex-audit.json
python scripts/replay_manuscript_interfaces_20260912.py --report /tmp/bounded-replay.json
RHOP_MANUSCRIPT_PATH=/path/to/main.tex python -m pytest -q tests/test_final_latex_20260912.py tests/test_manuscript_integration_20260911.py tests/test_manuscript_completion_20260910.py
```

The lock specifies packages for this audit, not every historical project
runner. Preserve the original RNG call order, including diagnostic draws,
when undertaking a later full permutation-study reproduction. Do not use an
older fixed-output runner in the live scientific repository.

## Publication boundary after this work

Literature distinctions and concrete proof/KDE/solver/source interfaces are
now incorporated into the minimally revised author manuscript. Independent
proof review, a full historical-study rerun if claimed in the final release,
Hoorn's Introduction integration, final supplement placement and submission
metadata remain open. No blanket ready-to-submit claim is made.
