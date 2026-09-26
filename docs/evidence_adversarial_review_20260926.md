# Retained empirical evidence review, 26 September 2026

## Scope and baseline

The reviewed source is the 25 September single-file manuscript, specifically
Sections 5--7 and Supplements S2--S3. Baseline commit: `cb04f78`.
This is an internal evidence/implementation review, not independent mathematical
peer review. No new scientific design, family grid, sample-size cell, estimator,
solver default or frozen outcome was introduced.

The execution environment was checked before use: distinct virtual-environment
and base prefixes; NumPy 1.26.4 and SciPy 1.16.3 imported from the verified
25 September environment. The 18--21 September environment correction remains
explicit in the manuscript and in its historical records.

## Findings requiring local wording refinement

### E1: All three older regular-null laws have inactive population reference terms

Section 6.2 currently explains cancellation in the symmetric calibration
design. The statement is true but incomplete: the independent t5 and independent
strong-skew laws also have both population reference coefficients equal to zero.
For independent margins, the reference derivative of the profile covariance is
minus `Cov(sign(X-T_X), |Y-T_Y|)`, which vanishes; the profile-variance
derivative is multiplied by the null correlation and also vanishes. For the
normal shared-sign law, independent radii and the symmetric shared sign give
the corresponding cancellation without raw independence.

Suggested replacement:

> All three regular-null designs have zero population reference coefficients:
> independence gives this cancellation in the t5 and strong-skew laws, and the
> joint sign symmetry gives it in the normal shared-sign law. Estimated
> coefficients need not vanish in a finite sample. The nonzero-effect study
> below therefore supplies a separate check with active population nuisance
> contributions.

This does not assert that the estimated reference never affects finite-sample
behavior; the independent strong-skew undercoverage remains informative.

### E2: State the finite-permutation target of S2 rates

The displayed S2 rates use the actual randomized procedure with B=99 and the
plus-one rule. The minimum p-value is .01, and rejection at .05 corresponds
to at most four sampled permutation statistics as or more extreme than the
observed statistic. The independent-trial Wilson denominator is the number of
generated datasets, as already stated, and incorporates both sampling and the
99 sampled permutations.

Suggested extra sentence in S2.2:

> These rates describe the procedure with 99 randomly sampled pairings,
> including its permutation Monte Carlo randomness and discrete p-value grid;
> they do not estimate a separately implemented exhaustive-permutation rule.

The existing seed/call-order ledger is correct. Increasing B would change the
retained procedure and its random-number streams and is not needed to support
the manuscript's bounded empirical claims.

### E3: Distinguish prospective outcome uncertainty from prediction uncertainty

The S2.3/S2.4 prospective predictions come from a binomial-logit fit to the
four-family pilot. The displayed Wilson intervals concern the fifth family's
observed rejection rates. They are not prediction intervals and do not include
training-fit uncertainty. No text currently establishes a formal residual test;
the following caption clarification prevents an unintended reading:

> Predictions are conditional on the fitted pilot model; Wilson intervals
> describe Monte Carlo uncertainty in the prospective observed rates only.

The statements that all six point predictions exceed observed rates and that
the scalar index is not a universal cutoff are supported. An uncertainty model
for cross-family transport is outside scope and unnecessary for those statements.

## Separately implemented targeted verification

The new runner `scripts/audit_evidence_interfaces_20260926.py` creates only
`results/evidence_interfaces_20260926.json` and checks the following interfaces.

1. **Symmetry-reduced population Jacobians.** For each retained bridge radius
   CDF G, solve G(d)=1/2 and independently calculate
   `J = diag(d*epsilon/2, d*g(d), -G(c*k*d)/k)`.
   The historical three-equation numerical Jacobian routine is not called.
   All 24 pilot, four matched-index and six prospective displayed indices agree
   within 1e-10. Analytic pure-bridge median/density anchors provide five small
   regression tests of this separate calculation.
2. **All severe realized linear fits.** Regenerate the 4,000 original
   tau=.10 datasets at n=80/640 and evaluate stored Stage 2/3 references, without
   refitting. All 8,000 stage records (16,000 marginal fits) have active fraction
   one. The maximum standardized residual is 1.164230054953371 < 1.345; the
   largest location-minus-sample-mean gap is 1.1449174941446927e-16. The fixed-scale
   location IF equals the centered observation to 4.440892098500626e-16.
   This establishes the realized linearity claim across the full stated severe
   cells; it is not an assertion about all possible draws or local sequences.
3. **Permutation implementation cross-check.** For replication zero of each of
   four original bridge cells, compare the cached marginal-reference method on
   the first three sampled pairings with complete public-API refitting on each
   permuted raw pair. An independent centered-moment reconstruction explicitly
   uses `gamma_X=(-h_X+mu_b*g_X)/D + rho*(mean(X-T_X)-mu_a*g_X)/v_a`
   and the margin-swapped gamma_Y, adding both reference IF terms to the direct
   centered correlation IF. It agrees with the five-moment API IF and coefficients.
   Marginal references agree within 1e-12 and studentized statistics within 1e-9.
   No new p-value or rejection-rate estimate is reported.

All checks passed; five new deterministic tests passed. All existing frozen TSV
bytes were unchanged. The machine-readable report retains actual discrepancies
and source hash. This adds implementation checks, not evidence of a conditional
permutation CLT or independent proof certification.

## Source-to-manuscript interfaces inspected

| Interface | Source checked | Finding |
|---|---|---|
| Six older regular-null DGMs/seeds | `audit_wald_convergence_20260822.py`, `run_claim_validation_20260823.py` | Normal-sign, independent t5, exp(1.1U)/Gamma(.7,1), six cell seeds and n values match. |
| Complete null studentizer | `run_weak_null_local_tests_20260814.py`, `src/cdelta.py` | Compatibility wrapper uses complete IF, KDE, sample variance divisor n-1 and legacy reference solver. |
| Nonzero DGM/RNG/three methods | `validate_active_nuisance_20260907.py` | n-by-2 normal ordering, reference sharing for direct ablation, fixed-population oracle and paired differences match. |
| Four-stage pathway | `run_reference_pathway_20260909.py` | Fixed scales/medians, endpoint KDE, full median propagation, brentq xtol and root flags match. |
| S2 cached marginal references | `run_studentized_permutation_weak_null_20260814.py` | Y IF is permuted with Y; joint moments, target derivatives and empirical IF variance are recomputed. |
| Bridge distributions/call order | `run_profile_bridge_family_validation_20260817.py`, `run_profile_diagnostic_scaling_20260816.py` | Five bridge distributions, common sign, independent radii, 199 bootstrap fits per margin and seed consumption match. |
| Prospective fifth family | `run_claim_external_validation_20260825.py` | Pilot logit training precedes fifth-family outcomes; seed mapping and absence of bootstrap stream consumption match. |
| C/CV summaries | S3.5 and original pathway records | Correctly identified as robust-reference C; mean C is not reconstructed from products of summary means. |
| Reproduction claims | September 16/18/21/25 reports and S3.9--S3.10 | Source isolation versus dependency isolation and exact versus tolerant agreement are distinguished in current text. |

## Limitations retained rather than repaired by simulation

- Historical permutation cells retain aggregate outputs, so aggregate replay
  cannot verify unrecorded historical per-dataset decisions. Current manuscript
  states this; new seed replay cannot reconstruct a missing original ledger.
- The two lognormal laws have active nuisance terms but substantial covariance
  cancellation. They validate the formula and expose undercoverage; they do not
  demonstrate a large practical advantage of complete over direct-only SEs.
- Internal mathematics, software tests and exact simulation reproduction do not
  replace external mathematical review of the theorem and nonregular proposition.
- The existing evidence supports retaining the stated finite-sample limitations.
  There is no justified need for another favorable distribution search, bigger
  family grid, new resampling procedure or more recent citations solely by date.

## Execution

```
/private/tmp/rho_verified_20260925/bin/python scripts/audit_evidence_interfaces_20260926.py --report results/evidence_interfaces_20260926.json
/private/tmp/rho_verified_20260925/bin/python -m pytest -q tests/test_evidence_interfaces_20260926.py
```
