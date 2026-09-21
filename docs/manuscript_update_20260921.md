# Integrated author draft and complete replay of the additional study

Date: 2026-09-21. The user requested an integrated LaTeX/PDF and a short
supervisor email. Initial Git state was clean at 768ecfa, main equal to
origin/main. No push, external message or production-method change is made.
Email text is delivered in the conversation, not saved in this repository.

## What was closed locally

The September 20 study was rerun at its original seeds, using an isolated
source snapshot of commit 768ecfa and the existing isolated Python 3.12.3 /
NumPy 1.26.4 / SciPy 1.16.3 environment. All six output TSVs agree cell for
cell, including 18,000 method records and 6,000 solver records from 6,000
datasets, as well as population, summary, paired and constant-sensitivity
results. This adds zero design cells. All pre-existing result TSV hashes
remain unchanged. This is source-based reproduction, not independent
reimplementation or mathematical peer review.

Report: `results/moderate_reproduction_20260921.json`. It records the exact
snapshot, source archive hash, runner command, environment, source hashes,
row/column accounting and normalized output hashes. The dated original
runner is unchanged. No new simulation search, enlarged sample size or
alternative seed was used to improve the outcome.

The three complete coverages remain .9045/.9355/.9365, and all corresponding
Wilson intervals exclude .95. Active nuisance is present, but its variance
largely cancels with direct--reference covariance. The new evidence does not
supply a calibrated positive example or establish full-IF finite-sample
superiority. Checked-versus-legacy agreement remains a numerical finding.

## Local manuscript changes

The September 18 single-file author LaTeX is the base. The new candidate is
outside the research repository, in `rho_p_minimal_20260921` under the existing
artifact directory. Its preamble is unchanged except for the date.

| Location | Integrated change | Evidentiary status |
|---|---|---|
| Draft status and S3 opening | Remove stale statement that retained-evidence reproduction is outstanding; distinguish original studies, the new study and its replay | Completed computational reproduction, bounded scope |
| Section 2.1 | Explain normal-calibration constants and their estimand dependence under asymmetry | Exact score identity and defined target; not a coverage guarantee |
| Section 2.4 | Recommend explicit checked mode for future analyses; add a small target comparison and focused literature links | Software recommendation and source-based positioning; no API default change |
| Section 6.3 | Briefly report the additional undercoverage, with full comparison referred to S3.10 | Empirical observation, no favorable-design selection |
| S1.7 | Add complete prospective numerical comparison, retaining fixed-precision qualifications | Numerical evidence, not a replacement for R5 |
| S3.10 | Full DGM, RNG mapping, methods, numerical truth, two new tables, solver checks, constant sensitivity, replay and source paths | Existing September 20 evidence plus September 21 reproduction |
| References/checklist | Add the five previously checked relevant sources and update completion wording | Author review and editorial approval still open |

The Introduction, complete IF/theorem section, Appendices A and B,
S1.1--S1.6 and S2 are text-identical to the accepted September 18 source.
All 19 historical table blocks are preserved verbatim. Historical root flags
remain. The target table is unnumbered, preserving main Tables 1--4;
new results are Tables S3.13--S3.14. The old source ledger is preserved,
and the new study carries its source ledger in S3.10.

The full PDF is 40 pages, compared with 37 previously. Main text ends on
page 13. The principal additions to read are Section 2 (especially the
comparison on page 5), the short Section 6.3 addition on page 11, and S3.10
on pages 37--38. No competing Introduction or separate long report is added.

## Validation and delivery

- The integrated LaTeX audit verifies 21 numerical tables / 1,182 cells,
  including all 19 old tables / 1,047 cells and 2 new tables / 135 cells.
- It also verifies 172 historical provenance checks, eight September 20
  evidence hashes, citation/reference keys, selected scope qualifications,
  and unchanged proof/Introduction blocks. It does not certify every prose
  number or prove the mathematics.
- Twenty-one focused tests pass, including negative controls for altered
  old/new result cells, changed proof text and misleading calibration wording.
  The full test suite was not rerun; production estimator code is unchanged.
- Final pdfLaTeX compilation has no warnings, unresolved citations/references,
  or overfull/underfull boxes. All-page visual inspection and enlarged review
  of the target comparison and added supplement support layout checking.
- The Overleaf package is a single main.tex with embedded references; no
  bibliography engine or local source path is required to compile it.
  Dates, hashes and final package integrity are in the delivery record.

Actual independent mathematical review remains open. Hoorn's Introduction,
final supplement placement, affiliations/venue and availability/AI disclosures
still require author input. The old independent-review package is retained;
its mathematical text remains applicable because the proof blocks are
unchanged. No independent review or reviewer contact is claimed.
