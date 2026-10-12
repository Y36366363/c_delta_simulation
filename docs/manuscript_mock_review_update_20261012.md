# Manuscript revision after the simulated questioning — 12 October 2026

The user requested incorporation of valuable corrections from the simulated
questioning, a short report email to Professor Hoorn, and guidance on obtaining
independent review. The questioning and the internal AI-assisted checks are
not independent mathematical review.

## Author artifacts

The new author version is stored outside the repository at:

`/Users/jialiangyao/.codex/visualizations/2026/09/11/01a08f53-8ee3-7dc0-87fd-0a3628d3098f/rho_p_review_revision_20261012/`

It contains standalone `main.tex`, the final `rho_p_review_revision_20261012.pdf`,
an Overleaf source ZIP, `INDEPENDENT_REVIEW.md`, and a separate candidate
fixed-tau review note. The October 2 source is preserved as found at the start
of this revision, including the abstract sentences inserted on October 12.
Its old PDF predates that abstract edit and is not the current deliverable.

## Implemented changes

| Location | Change |
|---|---|
| Abstract | Retained the user's exact two-sentence limitation; identified the counterexample as signed-lognormal to distinguish the regular normal-margin shared-sign control. |
| Introduction and model | Separated fixed regular-law results from nonregular empirical evidence; stated that signs are shared within IID pairs and independent radii do not imply independent fitted references. |
| S1.3 | Added the global clipped-score Lipschitz bound, explicit entropy integral, a random-index substitution lemma and proof, and the separate regular empirical-boundary localization argument. |
| S1.5 | Made empirical cross-margin reference covariance consistency explicit, with fitted coefficient hats and the n−1 sample-covariance convention. |
| S1.6 | Displayed the required weighted empirical Cauchy–Schwarz bound; did not demand an unweighted cross term converge to zero. |
| S1.7 | Distinguished exact residual checks, endpoint active fractions and complete segment-slope certificates. No certificate replay is claimed. |
| S1.9 and Discussion | Kept the alternative fixed-tau analysis outside the established manuscript results; no new CLT or nonregular full-IF validity claim was inserted. |
| Main/S3 simulation prose and notes | Specified the normal cutoff, stage-aware full-IF and direct-only SEs, and their distinction from population-reference oracle and constant-SE procedures. Rejection frequencies are not established test sizes in the nonregular model. |

Hoorn's six-section structure is retained. Frozen numerical table bodies,
production algorithms and solver defaults are unchanged. The candidate
location/correlation expansions, dependent reference influences, model-specific
constant SE, and fixed-tau root-slope argument remain separately labelled in
the internal dependency note and accompanying review materials.

## Validation scope

- Native desktop LaTeX compilation succeeded; a final PDF was also exported
  using the existing local TeX installations (no packages installed).
- The existing retained-table/source audit checked 23 tables / 1,270 cells,
  references, six main sections, historical audit conditions and frozen-file
  hashes. See `results/manuscript_mock_review_audit_20261012.json`.
- The audit ran with `/opt/anaconda3/bin/python`; it is not a newly isolated
  dependency reproduction. Initial system/bundled Python attempts lacked
  dependencies and did not complete the audit.
- Final PDF build, page inspection and artifact hashes are recorded in
  `results/manuscript_mock_review_delivery_20261012.json`.
- No broad test suite, new simulation grid, or root-certificate replay was
  run. Internal mathematical spot checks do not certify the proofs.

## Independent review request

The accompanying English guide asks a reviewer with expertise in asymptotic
statistics, empirical processes or robust estimation to examine specific
S1 claims and report Pass / Gap / Needs an additional assumption / Not reviewed,
with source locations. The first request should be scoped to regular S1,
especially random-index substitution and the reduced-moment studentizer.
Candidate fixed-tau work and code reproduction are separate review tasks.

The email is drafted for the user in chat; nothing is sent to Professor Hoorn.
