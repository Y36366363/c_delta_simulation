# Estimand decision and frozen canonical evidence

Date: 2026-08-19

## Decision

Use the Huber-profile correlation

\[
\rho_P=\operatorname{Corr}(|X-T_X|,|Y-T_Y|)
\]

as the **primary scientific estimand**.  Retain

\[
C=\frac{E\{|X-T_X||Y-T_Y|\}}
{E|X-T_X|E|Y-T_Y|}
\]

as the historical c_delta scale and a secondary estimand.  When (C) is
reported, also report both marginal profile CVs.

The reasons are:

1. `rho_P` directly measures standardized labelled-unit salience alignment
   and lies in `[-1,1]`.
2. `C=1+rho_P CV_X CV_Y`, so `C` additionally weights alignment by marginal
   salience heterogeneity.
3. Across five numerical identity checks, the largest identity error was
   `4.44e-16`, the largest permutation p-value difference was zero, and there
   was no permutation-rank disagreement.
4. At fixed population `rho_P=.30`, changing only marginal CVs moved
   population `C` from `1.019` to `3.546`.
5. In the highest-CV design, sample `C` still had SD `1.464` at `n=2000`.

Thus the decision changes the interpretation and reported effect scale, but
does not discard historical c_delta or alter its fixed-margin permutation
evidence.  Professor Hoorn can override this if the scientific construct is
explicitly intended to reward populations with more heterogeneous salience.

## Evidence-freezing rule

No new simulations were used for the four manuscript panels.  The script
`scripts/freeze_canonical_evidence_20260819.py` reads existing fixed-seed
tables, records the source SHA-256 hash and generating root seed, reconstructs
the integer rejection count, and adds Monte Carlo SE plus a 95% Wilson
interval.  The canonical long table contains 34 rows in
`results/canonical_evidence_20260819.tsv`.

## Panel A: regular calibration

These are `n=80`, 300-replication, 199-permutation profile tests with root seed
`2026081452`.

| Regular weak-null law | Rejection | MCSE | 95% Wilson interval |
|---|---:|---:|---:|
| independent `t5` | `.033` | `.010` | `[.018,.060]` |
| independent strong skew | `.040` | `.011` | `[.023,.069]` |
| shared-sign `t5`, independent radii | `.053` | `.013` | `[.033,.085]` |

These rows support pointwise feasibility, not uniform validity.  The last row
is especially important because it is a dependent weak null rather than a
full independence or exchangeability null.

## Panel B: near-degenerate failure

The sign-link path keeps the population profile effect at zero while reducing
radial variation.  All rows use `n=80`, 300 replications, 199 permutations,
and root seed `2026081612`.

| Radial log-SD | Rejection | MCSE | 95% Wilson interval |
|---:|---:|---:|---:|
| `.03` | `.947` | `.013` | `[.915,.967]` |
| `.10` | `.840` | `.021` | `[.794,.877]` |
| `.20` | `.203` | `.023` | `[.162,.252]` |

This is the constructive finite-sample failure panel.  It shows that complete
studentization is not a cure when reference fitting is nonlocal.

## Panel C: bridge recovery and first-order conditioning

The frozen bridge panel contains all 24 combinations of four matched-density
bridge families, `n in {80,320}`, and `epsilon in {.05,.10,.20}`.  Each cell
has 150 replications and 99 permutations, with a deterministic cell-specific
seed.  The compressed ordering is:

| Design pair | `sqrt(n) sigma_min(J)` | Rejection range |
|---|---:|---:|
| `n=80, epsilon=.05` | `.222-.223` | `.500-.567` |
| `n=80, epsilon=.10` | `.441-.446` | `.293-.407` |
| `n=320, epsilon=.05` | `.444-.446` | `.233-.380` |
| `n=80, epsilon=.20` | `.869-.887` | `.107-.153` |
| `n=320, epsilon=.10` | `.882-.891` | `.060-.147` |
| `n=320, epsilon=.20` | `1.736-1.774` | `.027-.053` |

The complete table, rather than only these ranges, carries each Wilson
interval and seed.  Across the 24 cells the risk-oriented Spearman correlation
between small identification index and rejection is `.971`; `log(I_n)` alone
has logit `R-squared=.932`.  This is strong empirical organization, not a
universal cutoff theorem.

## Panel D: higher-order family residual

The confirmatory transition panel uses `n=320`, `epsilon=.05`, 500
replications, and 99 permutations per family.

| Bridge family | Rejection | 95% Wilson interval | `sqrt(n) sigma_min(J)` |
|---|---:|---:|---:|
| exponential | `.232` | `[.197,.271]` | `.446` |
| half-normal | `.310` | `[.271,.352]` | `.446` |
| scaled beta(1,2) | `.356` | `[.315,.399]` | `.446` |
| uniform | `.334` | `[.294,.376]` | `.444` |

The family-homogeneity test gives `p=.0001305` and Cramer's `V=.1014`.
Because the first-order indices are nearly identical, the residual is a
quantified limitation pointing toward curvature, influence-tail shape, and
nonlocal reference selection.

## Manuscript use

The four panels now have distinct jobs:

- Panel A establishes that the proposed inference is not generically broken
  in regular iid examples.
- Panel B supplies the counterexample mechanism and magnitude of failure.
- Panel C provides the first-order organizing quantity.
- Panel D prevents overclaiming and states what first order misses.

Replacing these panels with a newly discovered anomaly requires an explicit
paper-level reason, not merely an unusual simulation result.
