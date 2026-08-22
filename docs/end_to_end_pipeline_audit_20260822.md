# End-to-end pipeline and inference-track audit

Date: 2026-08-22

## Verdict

The core statistic, complete influence-function implementation, nuisance
Jacobian, appendix proof, and frozen source files remain internally
consistent. No sign, normalization, MAD-convention, or source-data corruption
was found.

One substantive presentation problem was found and corrected: the formal
appendix establishes pointwise iid Wald/sandwich inference, whereas all four
frozen 2026-08-19 evidence panels use fully recomputed studentized
permutation. Those panels are useful empirical evidence for finite-sample
behavior and the conditioning mechanism, but they are not direct simulation
validation of the Wald theorem. Their table now carries an explicit
`inference_track` and theorem-alignment warning.

## 1. The two inference tracks

Appendix Theorem A.1 and Corollary A.1 concern the complete plug-in influence
function and iid Wald studentization under A1--A8. The fixed-seed audit in
`results/wald_convergence_audit_20260822.tsv` targets this procedure directly.

Panels A--D in `results/canonical_evidence_20260819.tsv` use fully recomputed
studentized permutation. Such a procedure is exact under a declared
group-invariance null. Under an arbitrary weak null, the project has not
proved the conditional permutation CLT. The panels therefore must not be
called a formal validation of Appendix Theorem A.1 or a proof of weak-null
permutation validity.

## 2. Wald convergence audit

Each cell uses 600 independent repetitions, a two-sided nominal level of
`.05`, and a deterministic cell-specific seed derived from root seed
`2026082201`. Monte Carlo uncertainty is recorded by both MCSE and 95% Wilson
intervals.

| Model | n=80 | n=160 | n=320 | n=640 |
|---|---:|---:|---:|---:|
| independent t5 | `.087` | `.083` | `.057` | `.075` |
| independent strong skew | `.147` | `.165` | `.135` | `.102` |
| normal margins, shared sign, independent radii | `.073` | `.052` | `.052` | `.047` |

The last model is a genuinely dependent weak null with standard-normal
margins: the common sign creates dependence, while independent half-normal
radii give population profile correlation zero. Unlike the older
shared-sign-t5 model with a positive radial offset, it has a unique regular
centre and positive density there. Its studentized-z SD is essentially one
from `n=160` onward.

The independent-t5 path broadly approaches nominal behavior but is not
monotone at 600 repetitions. The Wilson interval at `n=640` is
`[.057,.099]`, so the observed `.075` should not be interpreted as proof of a
persistent asymptotic error.

Strong skew is a real finite-sample warning. Rejection remains `.092` at
`n=1280` and `.082` at `n=2560`; the corresponding studentized-z SDs are
`1.109` and `1.127`. This is consistent with slow convergence under unbounded
skew profiles and does not contradict the pointwise theorem, but the present
audit does not isolate a single second-order cause. The paper can claim
asymptotic validity under its assumptions, but cannot claim that regularity
alone guarantees accurate moderate-sample Wald calibration.

## 3. Regularity-label correction

The old frozen Panel A row `profile_null_t5_sign_link` uses radii
`.25 + |t5|`. Its margins have no probability mass near zero, so the median
is not locally identified by a positive centre density. The row happened to
have rejection `.053` under studentized permutation, but it is not a regular
model under A2. It is retained in the historical frozen panel with corrected
language; it cannot be used as theorem-aligned regular evidence.

The separated lognormal-radius comparator reinforces this distinction. At
radial log-SD `.10`, Wald rejection is `.783` at `n=80` and still `.588` at
`n=640`. At log-SD `.40`, the corresponding rates are `.057` and `.050`.
Both paths violate the positive-centre-density condition, so this contrast is
a finite-sample mechanism check, not an in-assumption convergence theorem.

## 4. Reproducibility and integrity checks

The audit now checks more than the length of a SHA string:

- every stored canonical SHA-256 digest is recomputed from its current source;
- all 34 canonical rows are regenerated and compared with the stored table;
- every result TSV is checked for a nonempty body; the current claim-chain
  tables are additionally required to have a unique header and rectangular
  schema;
- current claim-chain files and the explicit inference-track label are
  checked automatically.

Ten July exploration tables predate the common rectangular writer and contain
scenario-specific trailing fields. They are retained as historical artifacts
and inventoried by the audit, but are not current manuscript evidence.

The machine-readable result is
`results/pipeline_integrity_audit_20260822.tsv`.

## 5. Claim ledger after review

Safe theorem claim: pointwise iid asymptotic linearity, normality, consistent
plug-in variance, and Wald studentization under A1--A8.

Safe empirical claims: severe near-degenerate distortion exists; the tested
transition is strongly organized by `sqrt(n) sigma_min(J)`; a residual bridge
family effect remains; and finite-sample Wald convergence can be slow under
strong skew.

Not safe: uniform validity near degeneracy, a universal Jacobian cutoff,
general weak-null permutation validity, moderate-sample Wald reliability from
regularity alone, or building-level inference based on an ordinary iid CLT.

## 6. Scope decision

No new paper branch is warranted. The correct next step is to present the two
inference tracks separately and use the skew result as a limitation or
finite-sample caution. Further computation should be undertaken only if the
paper chooses Wald inference as an operational recommendation and therefore
needs a correction for the strong-skew regime.
