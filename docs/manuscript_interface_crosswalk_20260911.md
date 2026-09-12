# Manuscript integration: claim-to-proof-to-source crosswalk

Date: 2026-09-11. Internal author integration and evidence review, not an
independent mathematical review or a submission-readiness certificate.

## Deliverable and version boundary

The current editable reading source is
[the integrated manuscript](manuscript_integrated_20260911.md), with actual
[S1](supplement_S1_20260911.md), [S2](supplement_S2_20260911.md),
[S3](supplement_S3_20260911.md), and [references](manuscript_references_20260911.md).
[The combined PDF](../output/pdf/rho_p_integrated_20260911.pdf) contains all of
them. The original Downloads PDF and the historical dated chapter drafts,
simulation results, manifests, public algorithm and constants are unchanged.
The new manuscript is the maintained integrated version of the text; older
chapter files remain historical source documents, not parallel current drafts.

The Introduction retains the existing PDF's provisional prose, followed by
a clearly labelled short literature-integration input. It does not substitute
for Hoorn's forthcoming Introduction. The final journal placement of the
assembled supplements has not been approved by Hoorn.

## Claim and source matrix

| Main location and claim | Status of statement | Proof / actual supplement | Result and implementation sources |
|---|---|---|---|
| 2.2: C=1+rho CVx CVy | Exact same-profile identity | Algebra in 2.2; S2.1 for sample orbit | Public definitions in `src/cdelta.py`; C values individually checked in S3.5 |
| 2.3: L2 all-to-all variance floor | Exact sample identity | Expansion shown in 2.3 | Applies only to the stated one-dimensional implementation; no latest-preprint normalization claim |
| 3.1: full marginal and moment IFs | Fixed-regular-law derivation | S1.1–S1.4 | `src/cdelta.py`; active-nuisance derivative and population tables dated 20260907 |
| 3.2: pointwise CLT and consistent variance | Theorem under R1–R5 and verified local classes | Appendix A; S1.1–S1.5 | No simulation proves the theorem; software root condition remains qualified in S1.7 |
| 4.1: independent population radii, nonregular median | Model proposition | Appendix B | `docs/shared_sign_model_result_20260909.md`; pathway model checks |
| 4.2: location errors before MAD estimation | Exact mean moments plus empirical pathway evidence | 4.2 and S3.2–S3.3 | `reference_pathway_replications`, `summary`, `paired` dated 20260909 |
| 4.2: fitted sample covariance | Conditional exact sample identity | Full cross terms retained in 4.2 | No substitution of fitted offsets into a fixed-offset population covariance |
| 4.2: fourth-root boundary | Conditional rate heuristic | Assumptions and non-theorem status stated in 4.2 | No local-to-degeneracy theorem claimed |
| 5: index and covariance normalization | Local first-order explanation | Explicit score vector, Omega and error coordinates in S1.2 | `scripts/run_nuisance_jacobian_20260817.py`; population source indexes |
| 5: bridge transition and family residual | Empirical permutation evidence | Actual S2.1–S2.3 tables and legacy Figures 2–3 | September 5 display tables; source/seed ledger in S3.7–S3.8 |
| 6.2: regular null checks, including skew failure | Empirical Wald evidence | Table 1 and S3.1 | Six source rows in `claim1_wald_validation_20260823.tsv`; valid denominators retained |
| 6.3: slow nonzero-skew coverage convergence | Empirical coverage evidence | Table 2; S3.4 and S3.6 | September 7 summary/replications and September 8 diagnostic files |
| 6.4: four stages and extra full-fit amplification | Paired empirical mechanism evidence | Tables 3–4; S3.2–S3.3 | Complete 16-cell-stage summary, 32,000 records, paired contrasts and root flags |
| 6.4: supporting C with both CVs | Descriptive same-profile effects | Table 4; S3.5 | Frozen C records; bounded replay at stored references, 2,000 existing datasets / 8,000 stages |
| 7: unchanged references and permutation scope | Exact orbit identity; conditional validity boundary | S2.1–S2.2 | Existing permutation implementation; no new conditional weak-null CLT |

## Closure of the previous PDF interfaces

| Interface | Integration status | What is now present / remaining boundary |
|---|---|---|
| Accurate DGMs and parameters | Closed in text | All main laws, bridge mixtures and prospective family are explicit; no model labels alone |
| Density estimator, solver and studentizer | Closed in text | Gaussian bandwidth, sample variance correction, stage-specific influences, IRLS/brentq settings and root flags in S1.5/S1.7/S3.2/S3.6 |
| Seeds, RNG mapping and denominators | Closed in text | Six regular cell seeds; both September SeedSequence rules; exact 34-cell permutation seed ledger and call-order qualifications |
| Compact Appendix A / bare R6 | Proof route assembled; independent review open | Explicit paired Bahadur/Z route, local entropy, weighted boundaries, coefficient localization, KDE consistency and empirical variance argument in S1 |
| S2 empirical assertions without panels | Closed in reading package | Actual figures and all bridge, matched-index and prospective rows supplied |
| C defined but absent from results | Closed | Main Table 4 and S3.8 give actual mean C and separate marginal CVs; no product of means |
| vX/vY, Omega, normalization | Closed | Radius variances in 4.2; score stack and marginal/paired Omega, error-standardization definition in S1.2 |
| Closest literature distinction | Bounded integration completed; author review open | Stavig, robust signed-correlation and generated-regressor distinctions incorporated with bibliography; no global novelty-priority certification |
| Draft-status/checklist inside scientific narrative | Partly closed | Detailed internal checklist moved here; provisional Introduction and honest proof/software limitations retained in author draft |
| Section 6.4 table citations | Closed | Explicit Tables 3–4 reference with full S3 supporting tables |
| Existing mechanism figure | Optional, not required | Quantitative four-stage tables carry the mechanism; legacy conditioning figures supplied in S2 without launching a new experiment |

## Additional provenance finding

The old four-family pilot and matched-index confirmation use identical seeds,
permutation counts and diagnostic RNG consumption at their shared cell. The
first 150 datasets of the 500-dataset confirmation therefore overlap the
pilot. The current S2 describes a larger-run confirmation, not a wholly
independent replication, and warns against pooling the two as independent.
This is inferred from the saved settings and generator call order, not from
an expensive new permutation rerun. Their stored rejection rates and hashes
are retained. It does not affect the separate September 9 paired pathway run.

## Validation performed

- New table assembly: 19 actual display/ledger blocks checked against source
  tables; the same read-only command rejects an optimistic coverage edit.
- Bounded deterministic CV recovery: 2,000 existing tau=.10,n=640 datasets,
  no refits, 8,000 stored stage records; maximum rho discrepancy
  1.5543122344752192e-15, C discrepancy zero, identity discrepancy
  7.771561172376096e-16.
- Historical completion audit: 172 checks, 95 displayed numbers, all passing.
  That audit continues to target the old chapter sources; the new audit
  specifically targets the new manuscript tables.
- Full project suite after the scientific/table edits: 280 passed. These are
  software and evidence-consistency tests, not statistical calibration or
  independent proof review.
- The 27-page PDF was rendered and visually checked separately from the source
  audit, including equations, tables, figures and pagination. There were no
  overfull TeX boxes or extracted words outside the checked page bounds.
  The PDF is built from these exact Markdown files and bibliography.
- No new simulation cells, new inference method, or estimator-default change.

## Still open, rather than falsely marked complete

1. Hoorn's revised Introduction and approval of final supplement placement.
2. Independent mathematical review of the proof and the specific empirical
   process/KDE arguments. A normed-domain Hadamard theorem is not needed for
   the chosen paired Bahadur/Z proof and is not claimed.
3. A general software-to-theorem guarantee for the public fixed-iteration
   solver. Its observed flags and finite sensitivity checks remain visible.
4. Locked-environment, isolated-checkout reproduction of the original studies.
   Current-environment tests and bounded seed replay do not satisfy this.
5. Author affiliations, venue, availability statements and accurate disclosure
   of actual AI assistance. No real application has passed the design gate.

## Maintenance

Edit the new Markdown prose directly. If a table's presentation intentionally
changes, edit `scripts/integrate_manuscript_20260911.py`, review source fidelity,
then run it with `--write`. A plain invocation checks without writing.
Render with `python scripts/render_manuscript_20260911.py` and visually inspect
the PDF after any content change. Do not run old result-producing scripts in
the active repository to reproduce a frozen experiment.
