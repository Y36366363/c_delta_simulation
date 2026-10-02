# Supervisor-directed six-section reconstruction — 2 October 2026

This update implements the full structural guidance supplied by Professor
Hoorn in the current conversation. It revises the existing October 2 author
source, preserving that version. The input is not an instruction to broaden
the experiments. No simulation design was added, no scientific result was
replaced, no public algorithm/default changed, and nothing was pushed.

## Manuscript and hierarchy

The new title is **Pointwise inference for median-MAD-Huber distance-profile
correlation, with a finite-sample counterexample**. The abstract uses Hoorn's
proposed paragraph. The main text occupies seven pages; S1–S4 and the shared
bibliography follow in the complete 41-page author PDF. The original LaTeX
preamble and standalone Overleaf workflow are retained.

| Hoorn's instruction | Implemented location and disposition |
|---|---|
| Scientific question, closest three antecedents, explicit contribution, scope | §1: paired unsigned reference distances; Afuecheta et al., Fout–Fosdick, Segers; specific reference-chain inference rather than a new magnitude-correlation target |
| Compact estimator definition | §2: midpoint median/raw MAD, Huber root, fixed c/k, population and empirical radius correlation |
| One sentence distinguishing all-to-all target | §2; full privately communicated definition and variance-floor derivation moved to S4.2 |
| Correct/clarify reference influence | §3.1 and S1.2: raw/scaled coordinates and score derivatives displayed explicitly; current k factor retained after verification |
| Compact joint-moment influence | §3.1: five-moment vector, two reference-derivative vectors, correlation gradient, paired variance |
| R6 logical status | Theorem 1 is explicitly conditional on R1–R6; Lemma 1 in S1.3 verifies classes; Corollary 1 and S1.8 derive R5/R6 applicability for midpoint/Gaussian-KDE/sufficient-root procedure |
| Reduced-moment null result | Corollary 2 in §3.2; three-moment numerator and unrestricted empirical-norm proof in S1.6, without importing general fourth-moment inference |
| Shared-sign proposition, nonzero Huber slope | §4 Proposition 1; full proof in S1.9, including diverging root-n median displacement |
| Correlated sample-mean errors | §4 exact identities; elementary calculation in S1.9 |
| Sample covariance identity | §4 retains all empirical cross terms and states the no-crossing condition |
| Two pathways; stage 2→4 wording | §4/§5.1 explicitly distinguish location-error pathway and **additional full-chain amplification**, not a separately identified MAD effect |
| Compact staged table | Main Table 1, tau=.10, n=80/640; stage-aware Wilson intervals and direct-only rejection; full tau=.40 and secondary panels retained in S3 |
| Small regular/skew panel | Main Table 2: four selected old null rows and all six nonzero-law complete-IF coverage rows; distinguish rejection from coverage |
| Missing favorable active-nuisance evidence | §5.2 explicitly acknowledges the gap; no selected successful outcome or new broad grid substitutes for it |
| Skew interpretation | **Persistent undercoverage over the examined sample sizes**; no simulation-based mathematical convergence-rate claim |
| Discussion scope | §6: pointwise inference, no finite-sample calibration certificate, no independence interpretation, bounded future work |
| C identity and all-to-all derivation | S4.1–S4.2; supporting C/CV summaries remain S3.5 |
| Stavig/Pareto/Lancaster/broad comparison and Gaussian formula | S4.3; three closest antecedents remain in §1 |
| Conditions, class/KDE/root arguments and theorem proofs | S1.0–S1.9; proof details removed from main text |
| Conditioning index and bridge results | S2.0, S2.3–S2.4; no operational threshold claim |
| Permutation section | S2.1–S2.5; only a scope sentence remains in Discussion |
| Designs, MCSE, seeds, solver diagnostics, secondary tables | S3.0–S3.11; old table bodies retained with corrected cross-reference pointers |

## Factor k: clarification, not a false correction

For raw MAD d, scale s=kd, U=(W−T)/s and B=E[U 1(|U|<c)], the score
partials are q_T=−A/(kd) and q_d=−B/d. Hence

    IF_T = (s/A) psi − (k B/A) IF_d
         = (s/A) psi − (B/A) IF_s,    IF_s = k IF_d.

The input main formula, unscaled and standardized Jacobians, S3.2,
production API and staged implementation already agreed. Removing k would
introduce a coordinate error. The revision makes both coordinate systems
explicit. The new deterministic check on the existing skew marginal gives
maximum correct contamination-derivative error 2.14e−7; omitting k gives
errors from approximately .019 to .065. This corroborates the algebra,
not a proof certification or a new simulation study.

Detailed algebra, source locations, primitive-condition proof route and
internal review record:
[mathematical response](hoorn_math_response_20261002.md).
Reproducible check:
[`check_huber_scale_coordinates_20261002.py`](../scripts/check_huber_scale_coordinates_20261002.py),
[result](../results/huber_scale_coordinates_20261002.json).

## What is and is not established

- **Theorem / corollaries:** fixed-law asymptotic linearity and complete
  studentization under explicit conditions. The ideal-arithmetic estimator
  corollary does not guarantee termination of a fixed-precision solver.
- **Exact model statements:** independent population radii, median
  nonregularity, nonzero Huber slope and sample-mean identities. The fitted
  covariance identity is conditional on the explicitly stated no-crossing event.
- **Empirical observations:** nonregular fitting distortion and additional
  full-chain amplification; persistent regular-skew undercoverage. Every
  old null design has population reference cancellation; both nonzero
  laws have active coefficients but near-cancellation in total variance.
- **Heuristic:** the conditional tau~n^(-1/4) balance is only in S2.6;
  it is not a local-to-degeneracy theorem for the full estimator.
- **Outstanding:** independent mathematical expert review, especially class
  closure/moving boundaries, reduced-moment empirical norm, random-bandwidth
  density estimation, root precision and Proposition 1. Internal AI-assisted
  review is not external certification. Author/venue and disclosure details
  still require their respective decisions; no new empirical claim is needed
  merely to fill the time before that review.

## Validation and artifacts

The retained-table audit validates 23 numerical displays / 1,270 cells:
21 existing tables / 1,182 cells plus two selected main tables / 88 cells.
Twenty scientific table bodies are unchanged; the source ledger changes
only three declared table-reference cells. The 172 historical audit checks
and frozen moderate-study hashes remain part of this audit. The two new
main tables reuse stored results, not new Monte Carlo outcomes.

Source-reconciliation scope is explicit: table rows, references, relocation
inventory and provenance; it does not certify every prose claim, literature
exhaustiveness or the mathematical proofs. The full software suite was not
rerun for this manuscript restructuring. Current targeted checks are not
claimed to be a new package-isolated reproduction.

See [evidence response](hoorn_evidence_response_20261002.md),
[final table audit](../results/manuscript_restructure_audit_20261002.json),
and [delivery manifest](../results/manuscript_restructure_delivery_20261002.json).
The latter records final source/PDF/ZIP hashes, build/visual checks, baseline
hash and outside-repository paths. The author artifacts contain no external
image or bibliography dependency and no generated PDF is added to Git.
