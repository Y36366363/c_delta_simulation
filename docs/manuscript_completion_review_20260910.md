# Manuscript completion review and editorial decision sheet

Date: 2026-09-10. Internal AI-assisted reconciliation, not independent
mathematical peer review. No new model, dataset, resampling method, or
distribution grid was introduced. Editorial allocation is a proposal,
**pending supervisor confirmation**, not an agreement communicated to Hoorn.

## 1. Ready to write is not ready to submit

There is enough material for an integrated first working draft now. Sections
1--6, Discussion, Appendix A, and the shared-sign model result already exist.
Waiting for another anomaly or for a general degeneracy theorem is not a
requirement of the bounded paper. The September 9 supervisor reply proposes
the title *Robust-reference profile correlation: pointwise inference and
finite-sample limits*, says the Introduction is being rewritten, and asks to
finish the nonzero skew study, staged pathway check, short model result, and
proof/code/Monte Carlo work. The first three bounded tasks are complete as
working research outputs. This is evidence of a move toward manuscript
completion, not acceptance of all proofs, a journal choice, or submission
authorization. The final exploratory sentence about extensions is not read
as commissioning all those extensions against the reply's repeated scope
limits.

`manuscript_review_frontmatter_20260910.md` supplies a provisional abstract
and ordered reading entry. Hoorn's forthcoming Introduction should be
integrated by the authors; the local Introduction is not a competing rewrite.

## 2. Reconciliation findings and changes

| Location | Finding | Resolution / remaining boundary |
|---|---|---|
| Section 2.2 | Missing backslash in qquad | Corrected the variance-definition display |
| Section 2.6 and Appendix A.9 | Stale re-pairing wording; rank identity could be overread | Marginal references are unchanged; only joint moments/studentizer vary; unstudentized ordering does not equate arbitrary studentized p-values |
| Appendix A.7 | One five-moment proof paragraph covered both estimands despite different moment requirements | Separate M_C=(nu,mu_a,mu_b) from the general-rho five-moment vector; no root-n expansion of squared moments under A5-C |
| Appendix A.7 | Generic marginal stack did not explicitly display the paired system | State six-dimensional stacking with block-diagonal derivative but potentially non-block-diagonal score covariance |
| Appendix A.8 / Corollary A.2 | Function-norm and empirical-norm claims needed clearer separation | Localize fitted scalar coefficients; justify weighted moving signs; identify the relaxed-moment unrestricted argument as empirical P_n norm, not population L2 with infinite fourth moments |
| Section 5.3 | Zero-index limitation lived mainly in the model note | State I_n=0 throughout the unbridged positive-tau family; bridge ordering is separate evidence |
| Section 6 | Old manifest described as covering all later material | September 5 displays and September 7/9 follow-ups retain separate manifests |
| Discussion / skeleton | Earlier open-ended scope language survived the supervisor decision | Pointwise inference and limits are the agreed direction; practical calibration and clustered/local-limit extensions are not default completion tasks |
| Appendix placement / historical source review | Working allocation described as final; source matching could be mistaken for external peer review | Explicitly provisional allocation and internal/external-source audit, not independent proof certification |

The C-proof distinction is substantive proof bookkeeping, not a new effect
definition or a change to the public estimator. For example independent t3
margins can meet the reduced moments with eta=.25 but lack fourth moments;
one cannot borrow a general five-moment CLT under that weaker assumption.
No claim of a new theorem is inferred from source-wording tests.

## 3. Evidence reconciliation

The read-only audit parses and compares the actual displayed numbers in
Section 6, not merely the presence of selected strings:

- Table 2: all six rows, sample sizes, repetitions, rates, MCSE, Wilson limits,
  and studentized standard deviations.
- Active-nuisance table: all three sizes, full/direct/oracle coverage,
  complete-IF Wilson limits and SE/SD ratios.
- Four-stage main summary: four cells, fitted effects and both studentizer
  tracks for fixed-scale versus full fitting.

It also recomputes stage-wise binomial Monte Carlo SE and Wilson intervals,
checks the existing display reconstruction, and verifies September 7--9
source manifests. The full regression suite separately replays stored-stage
examples and recomputes the September 8 tail accounting. No frozen simulation
table, display identifier, historical seed, or public estimator is changed.
The new audit is `results/manuscript_completion_audit_20260910.json`.

The evidence still says full nonzero-skew 95% coverage is .858/.9115/.927,
not adequate finite-sample calibration; shared-sign failure is a worked
nonregular example, not a uniform regular-law theorem; and the permutation
panels are empirical null rejection rather than a validated weak-null test.
Not every sentence or bibliography entry is mechanically certified by this
audit. Its finite list of checks is recorded in the JSON output.

## 4. Proposed main-text and supplement allocation

| Material | Proposed destination | Scientific role / caution |
|---|---|---|
| Estimand, complete IF, regular theorem, worked shared-sign model | Main Sections 2--4 | Core paper; C secondary; mathematical statements distinguished from empirical outcomes |
| Regular Wald evidence and active-nuisance skew coverage | Main Section 6 | Pointwise-theorem-aligned checks and a clearly disclosed slow-convergence limitation |
| Four-stage pathway table and concise intervention display | Main Sections 4/6 | Direct fixed-scale error plus additional full-fit amplification; include uncertainty and both reference RMSEs |
| Definition of standardized J and I_n, brief bridge/residual interpretation | Main Section 5 | Explanatory only; a short bounded summary can cite Supplement S2 |
| Full proof of the regular theorem and short shared-sign proposition | Appendix A; model proof as an adjoining appendix block | Required arguments remain accessible; the fourth-root discussion is explicitly a heuristic |
| Detailed entropy, MAD convention and KDE bookkeeping | Supplement S1 | Supporting proof details, not a replacement for stated assumptions in Appendix A |
| Legacy Figures 2--3, full bridge/permutation/residual comparisons, rank identity and group-invariance statement | Supplement S2 | Empirical permutation stress evidence; no weak-null conditional permutation CLT or remedy claim |
| Full Monte Carlo designs, seed/source ledger, paired contrasts, numerical-root flags, skew tail diagnostics | Supplement S3 | Reproducibility and sensitivity, with post hoc diagnostics labelled |

This proposal has not physically moved the legacy figures or renumbered
cross-references. Confirmation is needed on whether to keep a single compact
conditioning illustration in the main text or only a summary paragraph.
The empirical comparisons remain scientifically available if moved; moving
them does not strengthen their inferential validity.

## 5. Application gate: do not fill an empty section with convenient data

No dataset has passed this gate. The default working draft contains no claimed
real application. A candidate requires documented answers to all of:

1. What is the independent observational unit, and why are X and Y paired?
2. Is there one intact pair per independently sampled unit, without hidden
   person/building/site/repeated-measure or temporal/spatial clustering?
3. Is a common sampling population defensible, rather than an unexamined
   mixture of different sampling designs or selection mechanisms?
4. Why is unsigned distance from a fitted group reference scientifically
   meaningful, rather than signed association or distance from an external
   standard? What do missingness, exclusions and preprocessing change?
5. Are provenance, access/use conditions and variable definitions documented?
6. Are profile variability, root accuracy and the numerical CI reportable
   without asserting a finite-sample calibration certificate?

Design evidence is necessary; no independence test or sample-size threshold
proves IID. If these questions cannot be answered promptly, omit the
application. If they can, show one raw-pair plot and one profile-pair plot,
both fitted references, rho_P with full-IF interval, and C as secondary.
Any displayed I_n remains descriptive, never a reliable/unreliable label.
Existing building simulations do not pass this gate as real paired-IID data.

## 6. Proof and implementation obligations that remain open

- Independent review of the precise functional domain/topology, or a fully
  explicit paired Bahadur/Z-estimation proof route. An empirical process is
  not justified by treating empirical laws as convergent in total variation.
- Independent verification of the entropy-class closure, random density
  plug-ins and weak-null lower-moment argument. Today's clarifications do not
  substitute for that review.
- The theorem's negligible root-residual condition versus fixed solver
  tolerance/iteration cap. The two September 9 flags are disclosed, not
  erased; software-release diagnostics remain a separate bounded task.
- Consolidated environment specification and an independently exercised
  clean reproduction. Passing in the current environment is not this gate.
- Final novelty/bibliography check, author review of wording and actual AI
  assistance disclosure, target venue, and journal layout. These are not
  settled by the simulation counts.

## 7. Specific questions for the next supervisor discussion

1. Shall we use the existing theorem, completed skew study, four-stage failure
   evidence and short model result as the basis of the first integrated draft?
2. Is the proposed S2 allocation acceptable, with only a concise conditioning
   summary (or one compact illustration) in the main text?
3. May the first draft omit Section 7 unless a defensible paired-IID dataset
   becomes available, as suggested in the reply?
4. How should Hoorn's revised Introduction and the mathematical proof review
   be integrated into the next author-review cycle?

These questions clarify completion and presentation; they do not reopen a
broad search for anomalies or ask for all possible theoretical extensions.

## Reproduce this reconciliation

```bash
/opt/anaconda3/bin/python scripts/audit_manuscript_completion_20260910.py
/opt/anaconda3/bin/python -m pytest -q
```

Add `--write-report` only to refresh this dated audit JSON after intentional
source edits. It never regenerates simulated datasets.
