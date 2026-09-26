# Retained-evidence reproduction, Pareto comparison and review package

> **September 25 provenance correction:** this dated note originally overstated
> dependency-environment isolation. The recorded source-snapshot replay and
> numeric agreement remain valid, but the execution report records
> `isolated_venv=false`. See [the dated correction and verified rerun](review_and_positioning_20260925.md).
> Original result/audit files are preserved; no mathematical certification is implied.

Date: 2026-09-18. Authorized manuscript-completion update. No new simulation
designs, changed frozen results, default-method changes or push.

## Reproduction closed for the listed retained evidence

The September 16 core reproduction remains valid: 14,000 datasets and
50,000 replication records, with their summaries and root checks. Today's
complement uses the existing isolated Python 3.12.3 / NumPy 1.26.4 / SciPy
1.16.3 environment and separate historical-source/results snapshot.

| Retained evidence rerun today | Original settings | Result |
|---|---|---|
| Six regular-null cells | 1,000 datasets per cell | All saved aggregate fields match |
| S2.1 four-family bridge panel | 24 cells, 150 datasets, 99 permutations | All saved aggregate fields match |
| S2.2 matched-index panel | 4 cells, 500 datasets, 99 permutations | All saved aggregate fields match |
| S2.3 prospective fifth family | 6 cells, 200 datasets, 99 permutations | All saved aggregate fields match |
| Population bridge indices | 24 retained pilot cells | All indices match; predictor retrained from reproduced summaries |
| Nonzero-skew numerical benchmarks | Original 24/48/72 quadrature and contamination directions | All fields match |
| Post hoc skew diagnostics and regular roots | Stored draws; 18 root records | All fields match |

There are 12,800 dataset executions but 12,200 distinct datasets: the first
150 in each matched-index run overlap the corresponding pilot. There are
673,200 permutation evaluations and 2,228,800 historical bootstrap reference
fits. Bootstrap fits preserve the original RNG call order, even though those
diagnostics are not the displayed population index. Independent cells were
parallelized; within-cell order was unchanged.

Across nine comparisons, 109 rows and 2,165 fields were checked. Maximum
scaled numeric difference was zero; all declared exact fields agreed and
nonfinite status was retained. All 286 pre-existing TSV hashes remained
unchanged. This does not establish equality of every unrecorded historical
per-dataset decision, nor reproduce every old project experiment.

The retained S3 C/CV summary was separately recalculated at stored references
by the final LaTeX audit. With September 16, this closes the original-seed
reproduction task for the current retained evidence. It does not improve the
observed skew coverage or establish statistical calibration.

Protocol: `docs/retained_reproduction_protocol_20260918.md`.
Report: `results/retained_history_reproduction_20260918.json`.
Runner: `scripts/reproduce_retained_history_20260918.py`.
The first harness attempt stopped before simulations because the Python
namespace path did not support list insertion. Explicit snapshot-path binding
fixed it. The completed run took approximately 235 seconds. The final
comparison wrapper was also reapplied to all eight saved replay tables after
refactoring exact-field checks for isolated negative tests; all passed.

## Pareto full text and local manuscript revision

The supplied paper is the complete Pareto (2024) article. Equations (2),
(5)–(8), transformation properties, algorithm, examples and conclusion now
support an actual formula-level comparison. Its signed opposite-line residual
ratio differs from marginal robust-reference radius correlation. The Table 1
example reproduces r'=0.688172, printed as 0.69. Reflection and a perfect
negative-line example separate the targets without a new simulation.

The article is worth citing as adjacent construction/positioning, not as a
foundation for our IF/Wald theorem or a general robustness endorsement.
The full comparison and limits are in `docs/pareto_formula_comparison_20260918.md`.

The new September 18 author candidate makes only local changes to the accepted
September 15 LaTeX: a Section 2 formula comparison and reference; the completed
reproduction record in S3.9; and corresponding status/checklist wording.
The original preamble (apart from date), Introduction, main theorem, S1 proof
and all 19 tabular data bodies are preserved. No competing Introduction was
written. Existing historical root flags remain. The PDF is 37 pages.

## Independent review prepared, not performed

An English review package outside the repository contains the exact author
LaTeX/PDF, source-line claim/proof/evidence map, five priority proof interfaces,
model/scope checks, a blank reviewer response template, selected implementation
sources, internal notes, environment locks and numerical audit reports.
Its manifest records content hashes. It explicitly discloses local AI assistance
and does not call previous internal or literature checks independent review.
The licensed Pareto PDF is not redistributed. No email or request was sent.

The priority questions are joint quantile/Z-expansion; entropy, moving
boundaries and random coefficients; weaker-moment empirical-norm reasoning;
uniform random-bandwidth KDE; and R5 versus the optional finite-precision
solver. The model proposition and conditional heuristic are separately typed.
The code subset is for inspection; full experiment runners require the full
repository, as explained in the package.

## Checks and remaining dependencies

- All 19 tables / 1,047 cells, citation keys and cross-references reconcile.
- 32 targeted tests pass: manuscript completion, final LaTeX, existing
  reproduction comparator and nine new exact-field negative controls.
- Deterministic Pareto formula check repeats successfully.
- pdfLaTeX stabilizes after three passes, with no final warnings, unresolved
  references or overfull/underfull boxes. All-page contact sheets and enlarged
  changed pages were inspected. The local microtype temporary dependency was
  missing and restored from CTAN; no preamble workaround was introduced.
- The full test suite was not rerun; no production estimator code changed.

Still open: actual independent mathematical review; Hoorn's Introduction and
editorial decisions; author/venue facts and final availability/AI disclosures.
The fixed-machine solver does not acquire a universal asymptotic success
guarantee from these checks. No further grid or method extension is needed
merely to keep updating while awaiting the supervisor's response.

Artifact paths, hashes and package verification are recorded in
`results/manuscript_delivery_20260918.json`.
