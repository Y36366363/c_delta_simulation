# Accuracy Audit of the Paired-Overlap Results

Date: 2026-08-01

## Scope

This audit rechecked the results used in the meeting figures and paired-
standout interpretation at four levels: deterministic reproducibility,
permutation implementation, mathematical identities, and reporting accuracy.

## Reproducibility

The high-replication forced-overlap simulation, random-set null, conditional
overlap layers, and binary-overlap bridge were independently rerun from their
stored seeds. The recomputed rows matched the saved TSV values exactly after
the same reporting conversion:

- 30 forced-overlap summary rows;
- 6 random-set-null summary rows;
- 18 conditional overlap-layer rows;
- 120 binary-overlap bridge rows.

## Permutation Implementation

The simulation helper computes permutation p-values from standardized
divergence-vector correlation, while the core implementation uses corrected
raw `c_delta`. Their permutation order should be identical because

```text
c_delta = 1 + corr(D_x, D_y) CV(D_x) CV(D_y),
```

and the positive CV product is fixed during permutation. In 120 direct checks
across L1/L2, normal/`t3`/`t2`, and all five overlap levels, the helper and core
implementation returned identical p-values. Mismatch count: `0`.

## Mathematical Checks

The binary-overlap identity was compared directly with Pearson correlations of
constructed indicator vectors in 24 settings:

```text
r_binary = (n m - k^2) / (k (n-k)).
```

All checks passed. The exact hypergeometric overlap PMF was checked for
normalization and expectation under four `(n,k)` settings:

```text
sum_m P(M=m) = 1,
E(M) = k^2 / n.
```

All checks passed.

## Confidence Intervals

All six random-set-null Wilson intervals were independently recomputed and
matched the stored four-decimal endpoints. The project helper uses `z=1.96`
and the simulation helper uses `z=1.9599639845`; their unrounded endpoints
differ by less than `2e-7` and produce identical reported values.

## Finite Monte Carlo Resolution

The reported p-value is

```text
p = (exceedances + 1) / (n_perm + 1),
```

with rejection defined by `p < .05`. The attainable randomization level is
therefore slightly below `.05`:

| Permutations | Effective attainable level |
|---:|---:|
| 199 | 0.0450 |
| 399 | 0.0475 |
| 499 | 0.0480 |

This is not a defect, but it should be stated when interpreting null rejection
rates. In particular, the random-set-null rates `.0377-.0493` are consistent
with the effective `.045` reference at 199 permutations. Earlier wording that
said only "near nominal `.05`" is directionally correct but less precise.

## Interpretation Boundaries

The audit supports the numerical conclusions, subject to these qualifications:

1. Forced-disjoint standout sets are a conservative negative control, not a
   formal independent null.
2. The random-set null is the appropriate calibration design when both samples
   contain standouts but their index sets are independently selected.
3. Conditional rejection can be high in rare chance-overlap layers while the
   unconditional test remains calibrated.
4. Heavy-tail attenuation is an empirical conclusion for the simulated
   settings, not a universal theorem.
5. The binary-overlap model is an explanatory limiting case, not the definition
   of continuous `c_delta`.
6. The descriptive upper-triangle distance-matrix correlation is not itself a
   fully developed general-structure test or formal Mantel analysis.

## Audit Conclusion

No numerical or implementation error was found in the meeting results. The
main correction is reporting precision: for 199-permutation runs using strict
`p < .05`, compare null rejection with `.045` as well as the nominal `.05`
label. This refinement does not change the paired-overlap gradient, heavy-tail
attenuation, binary-overlap identity, or random-set-null calibration
conclusions.
