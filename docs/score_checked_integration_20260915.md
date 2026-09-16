# S1 and optional residual-checked API integration — 2026-09-15

This implements the authorized local manuscript-completion update. There are
no new simulation cells, revised frozen scientific results, or new calibration
claims. The supplementary proof remains an internal author-level argument,
pending independent mathematical review.

## Public interface

```python
result = huber_profile_correlation_inference(
    x, y, reference_solver="score_checked", solver_max_iterations=512
)
diagnostics = result["solver_diagnostics"]
```

The default `reference_solver="legacy"` retains the original fitting arithmetic
and return fields. The optional mode uses the September 14 bisection candidate,
requiring an exact rational represented-input score residual at most 1/(10^8 n).
It recomputes the full median/MAD/Huber IF, target coefficients and studentizer
at the accepted roots, using the existing density option and variance correction.
It returns x/y root diagnostics, including the exact residual numerator and
denominator, floating residual, tolerance and iteration count. Numerical budget
or resolution failures raise errors without fallback. Other degeneracy checks
continue to apply; a valid root residual is not a statistical-validity certificate.
The exact check adds computational cost and is explicitly opt-in.

The real-arithmetic R5 argument and the fixed-machine qualification are in
S1.7 and `docs/proof_solver_review_20260914.md`. Fixed-machine universal success
is not asserted. No historical result is relabelled as using the new mode.

## Manuscript changes

The single-file September 14 author candidate is the base. Its preamble, main
theorem, original Introduction and all 19 tabular data bodies remain intact.
S1.3 adds a uniform weighted-moving-sign bound and explicit random-coefficient
localization; S1.6 adds the maximum-observation tail argument and analytic t3
scope example; S1.7 adds the n-dependent residual rule, ideal-arithmetic proof,
public option and bounded integration check. Historical solver descriptions
are qualified as the default. The date is September 15. Manuscript artifacts
remain outside the research repository, as requested.

## Provenance resolution

Adding a public option necessarily changes `src/cdelta.py`. Original manifests
retain their original hash:
`32f0dd80097bb1a7c207b18edcb8b54069ea473291627e649a717705a23d5be7`.
An exact snapshot from commit `176248b9d62d012ad061421028232d0968b065ea`
is retained at `archive/source_snapshots/cdelta_20260914.py`.

`scripts/verify_frozen_sources.py` verifies the live path if its hash matches;
otherwise it resolves only this explicitly registered source/hash pair to the
snapshot and verifies the original hash there. Other mismatches fail. Negative
tests cover snapshot corruption and unregistered paths/hashes. The current
source is separately hashed and compared through the new integration audit.
This is a version distinction, not an update of the frozen expected hash.

The manuscript completion audit now writes its current version to
`results/manuscript_completion_audit_20260915.json`. The September 10 report
is preserved. A regression test requires every original scientific check to
remain identical after removing only the newly reported source-version metadata.

## Validation

- Complete suite, including the actual manuscript via `RHOP_MANUSCRIPT_PATH`:
  **327 passed**, no skips. Fourteen warnings are dependency deprecations from
  Matplotlib/Pyparsing. No test failure remains.
- Same 41 previously selected datasets, 82 margins: default return keys, scalars,
  intervals and influence arrays match the archived implementation exactly.
- Optional API matches the separate dated prototype; no checked two-sided Wald
  decision changes. Largest absolute rho change is 4.6815988479e-7; largest
  absolute relative complete-SE change is 3.0229966970e-5 (0.003023 percent).
- Original 172 completion checks and 95 displayed-number checks pass. Actual
  final LaTeX: 19 tables / 1,047 cells and reference/citation keys pass.
- pdfLaTeX produces 36 pages without LaTeX errors, warnings or box overflow.
  Final page images are reviewed separately; successful compilation alone
  is not proof of correct mathematical content or layout.

The first targeted run detected the anticipated live-source/frozen-hash mismatch;
the first full run additionally detected the outdated stored-audit comparison.
Both were resolved through the explicit version mapping above. The initial PDF
had one overlong code label; it was reworded before the final compilation.

## Reproduce

```bash
python scripts/audit_score_checked_api_20260915.py --legacy-source archive/source_snapshots/cdelta_20260914.py --report /tmp/score_checked_recheck.json
RHOP_MANUSCRIPT_PATH=/absolute/path/to/main.tex python -m pytest -q
python scripts/audit_final_latex_20260912.py /absolute/path/to/main.tex
```

Use a fresh audit output path. Exact software/environment details remain in
the prior clean-environment lock. These bounded comparisons do not replace a
full reproduction of all historical Monte Carlo and permutation studies.
