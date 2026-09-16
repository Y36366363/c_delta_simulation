# Working-paper review and core reproduction — 2026-09-16

## Review decision

The September 15 author draft remains the editing base. No immediate change
to its scientific claims was identified in the reviewed abstract, main theorem
and software qualifications, shared-sign proposition/proof, mechanism identities,
conditioning discussion, permutation scope and Discussion. This is an internal
scope/consistency review, not independent mathematical certification or a
submission-readiness decision. The LaTeX and delivered PDF hashes were verified
against the September 15 artifact record; neither artifact was edited today.

The manuscript distinguishes pointwise inference from finite-sample calibration,
the optional residual check from statistical regularity, and empirical permutation
evidence from a proved conditional weak-null limit. The generated-reference
terms remain relevant even though the selected skew example has strong variance
cancellation. Neither a new calibration claim nor another distribution grid
is justified by this review.

## A reproducibility obligation advanced without changing the paper

The two most recent core studies were fully reproduced at their original seeds,
sample sizes, repetitions and methods. This extends the earlier 41-dataset check
for these two studies only.

| Reproduced material | Dataset count | Replication rows | Result |
|---|---:|---:|---|
| Nonzero regular skew, September 7 | 6,000 | 18,000 | All fields match within declared tolerance |
| Four-stage shared-sign pathway, September 9 | 8,000 | 32,000 | All fields match within declared tolerance |

The three-method skew summaries/paired differences, all four-stage summaries/
paired contrasts, pathway model checks and both historical root-sensitivity
records also match. Across eight tables, 1,017,136 fields were checked, including
row identities, exact seed/decision fields, error strings and nonfinite status.
The largest scaled numeric discrepancy was 5.574393188047023e-16, below the
prespecified 1e-10 threshold. There were zero simulation error rows and no
missing or duplicate rows. Original frozen input hashes were unchanged.

The run used a separate temporary source snapshot with the archived historical
implementation, not the September 15 optional solver, and the existing isolated
Python environment (Python 3.12.3, NumPy 1.26.4, SciPy 1.16.3). Both runners were
verified against the original manifests. Every copied Python source is hashed
in the machine-readable report. Regenerated tables are only in the temporary
snapshot; frozen scientific outputs were not overwritten.

The first isolation check stopped before simulation because macOS resolved a
temporary-directory alias differently. Resolving the snapshot path before the
check corrected that harness issue; the recorded complete run then passed.
Nine new comparator tests cover changed decisions/seeds/errors, nonfinite status,
duplicate/missing rows and missing columns. Together with eight existing
manuscript-completion tests, 17 targeted tests pass with 14 dependency-deprecation
warnings. The full test suite was not rerun today; its last result remains
327 passed on September 15.

This is not full-project reproduction. The six older regular-null cells, all
permutation/bridge panels, and every post hoc or numerical-integration grid
remain outside today's run. It is also not new simulation evidence: the seeds
and datasets are those already reported. In particular, existing skew coverage
.8580/.9115/.9270 and severe pathway rejection .7550/.5510 are not improved by
successful reproduction.

## Literature access and relevance

A targeted renewed search for Pareto (2024), *On a correlation coefficient based
on the L1-norm*, did not yield an accessible full-text formula source. The
publisher still labels the page a subscription preview and states that its
implementation code is available on request:
https://link.springer.com/article/10.1007/s00362-024-01616-3

The formula comparison therefore remains open. The abstract, figure captions,
or the earlier related paper cannot establish identity or nonidentity of the
2024 coefficient with the present estimand. Institutional full-text access or
an author-provided copy is the next useful input; no message was sent and no
purchase was made. No citation was added merely for recency. The existing short
Ichimura--Newey (2022) and Yu--Hutson (2024) connections already have bounded
roles and do not supply missing theorems for this paper.

## Remaining work, separated by dependency

| Item | Status / appropriate next step |
|---|---|
| Main claims versus S1 and numerical implementation | Reviewed; no new contradiction identified in scope examined |
| Two core studies' full replication arrays and derived tables | Completed today, with explicit scope above |
| Remaining original regular-null and S2 reproduction | Can be done locally; sequence by final retained evidence, without new designs |
| Pareto formula comparison | Needs full text; not intrinsically dependent on Hoorn's reply |
| Independent mathematical review | Requires an external reviewer; local tests cannot close it |
| Hoorn's revised Introduction and positioning emphasis | Await his text/feedback; do not write a competing Introduction |
| Main/supplement placement, length and target journal | Author decisions; avoid disruptive restructuring before feedback |
| Real application | Optional; none has passed the paired-IID design gate, so do not add one to fill space |
| Affiliations, availability statements and AI disclosure | Prepare accurate factual records, finalize with authors and venue |

There is no need to issue another working-paper PDF solely for this audit.
At the next agreed revision, S3's reproducibility paragraph can report completion
of these two core studies while retaining the outstanding broader reproduction
and independent-review qualifications. No request for a new anomaly, resampling
method, clustered extension or universal conditioning threshold follows.

## Artifacts and rerun

- Protocol: `docs/core_reproduction_protocol_20260916.md`.
- Full comparison metadata: `results/core_reproduction_20260916.json`.
- Reproduction entry point: `scripts/reproduce_core_studies_20260916.py`.
- Comparator tests: `tests/test_core_reproduction_20260916.py`.

From the project root, with the recorded environment and a fresh report path:

```bash
python scripts/reproduce_core_studies_20260916.py --report /tmp/core_reproduction_recheck.json
python -m pytest -q tests/test_core_reproduction_20260916.py tests/test_manuscript_completion_20260910.py
```
