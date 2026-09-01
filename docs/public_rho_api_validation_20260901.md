# Public robust-profile correlation API validation

Date: 2026-09-01

## Single deliverable

The validated primary estimator and pointwise Wald procedure are now exposed
as `huber_profile_correlation_inference` in `src/cdelta.py`. Its target is

\[
\rho_P=\operatorname{Corr}(|X-T_X|,|Y-T_Y|),
\]

with each \(T\) defined by the median/MAD-scaled Huber functional. The older
simulation function is retained as a compatibility wrapper that delegates to
the public implementation. This closes the nonblocking software gap identified
by the Section 3 readiness audit without creating another simulation branch.

## Deterministic validation

One fixed regular paired sample (`n=400`, seed `20260901`) is used as an
implementation audit, not as a new distribution grid. The checks require:

1. exact agreement of the public and compatibility paths for the estimate,
   complete plug-in standard error, and empirical influence values;
2. agreement of the public estimate with the direct Pearson correlation of
   the two fitted absolute-deviation profiles;
3. invariance of both the estimate and complete standard error to separate
   positive affine transformations;
4. empirical centering of the returned influence values; and
5. preservation of the secondary-scale identity
   \(C=1+\rho_P CV_XCV_Y\).

The machine-readable audit is
`results/public_rho_api_audit_20260901.tsv`. These are implementation
equivalence and invariance checks; they are not additional evidence for
finite-sample calibration.

## Interpretation boundary

The public docstring and validation preserve the paper's frozen language:

- inference is **pointwise, not uniform** over near-degenerate sequences;
- unstable reference fitting **can cause**, but does not always cause,
  finite-sample distortion;
- \(\sqrt n\,\sigma_{\min}(J)\) remains a **first-order organizer, not a
  universal cutoff**; and
- robust marginal references do **not** turn \(\rho_P\) into a globally robust
  correlation coefficient.

## Consequence for the next manuscript task

The API gap is closed. The next work should therefore return to a paper-level
deliverable rather than another general simulation grid: precise novelty and
classical-comparator positioning, followed by the Section 3--8 prose. Whether
to develop local-to-degeneracy theory or an operational sample-stability
diagnostic remains a supervisor-level scope decision.
