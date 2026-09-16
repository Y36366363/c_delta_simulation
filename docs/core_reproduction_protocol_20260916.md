# Core-study reproduction protocol — 2026-09-16

Internal execution protocol recorded before the reproduction outcomes, not
third-party preregistration. This closes part of an existing reproducibility
obligation; it is not new evidence from additional simulation designs.

- Reproduce all 6,000 September 7 skew datasets (18,000 method rows) and all
  8,000 September 9 pathway datasets (32,000 stage rows) using original seeds,
  generator order and repetitions. Do not use the new optional solver.
- Run in a separate source snapshot using the archived historical cdelta source
  whose SHA-256 is 32f0dd80097bb1a7c207b18edcb8b54069ea473291627e649a717705a23d5be7.
  Verify the two original runners against their frozen manifests. Use the
  existing isolated Python environment and record its package versions; do not
  describe the environment as newly created today.
- Invoke the runners' calculation functions, not their mains with fixed output
  paths. Write regenerated tables only beneath the temporary snapshot.
- Compare every replication field by intact row key, preserving error strings,
  categorical values, nonfinite status and exact seed/decision fields. Numeric
  tolerance is 1e-10 times max(1, absolute stored value). Report maximum gaps,
  any failures, missing/duplicate rows, and all threshold exceedances.
- Recompute summary tables and paired contrasts from the reproduced records;
  also recompute the pathway model checks and the two original root-sensitivity
  records. Compare them with their frozen counterparts. Do not revise hashes or
  replace frozen outputs if a mismatch appears.
- This run does not reproduce the six older regular-null cells, all permutation
  panels, or every post hoc diagnostic/population-integration convergence grid.
  Do not call a successful core-study run full project reproduction.
- Record a compact report, source hashes and environment in the repository.
  Keep the working PDF unchanged unless a substantive manuscript error is found.
