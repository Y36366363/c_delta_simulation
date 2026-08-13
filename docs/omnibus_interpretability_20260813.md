# Interpretable Standardized-Max Follow-up

Date: 2026-08-13

## Purpose

The unequal-building study identified permutation-standardized max as a more
promising omnibus candidate than learned profile/Mantel mixtures. This follow-
up asks whether it can be explained after rejection, how much power it loses
relative to the best component, and how many permutations are needed for
stable decisions and attribution.

This work does not promote the omnibus to the primary method and does not
change `c_delta_star`.

## Simultaneous Evidence Construction

Let `T_P` be the robust-profile statistic and `T_M` the Mantel statistic. For
each permitted within-building permutation orbit, compute

```text
Z_j = (T_j - mean_G T_j) / sd_G T_j,
Q = max(Z_P, Z_M).
```

The omnibus p-value is the permutation upper-tail probability of `Q`. For
component `j`, define the maxT-adjusted evidence value

```text
p_j,adj = P_G(Q_g >= Z_j,observed).
```

Because the same survival function is evaluated at the two observed
component scores,

```text
p_omnibus = min(p_P,adj, p_M,adj).
```

The output can therefore report:

- the standardized winner `argmax(Z_P,Z_M)` as a descriptive evidence ranking;
- profile-only adjusted evidence;
- Mantel-only adjusted evidence;
- adjusted evidence from both components; or
- no adjusted component evidence when the omnibus does not reject.

The adjusted component values are never smaller than their corresponding
unadjusted permutation p-values in the implementation, and the exact
small-orbit rank checks remain valid.

## Important Interpretation Boundary

The construction controls the joint profile/Mantel family under the global
within-building random-pairing null. Strong family-wise control for arbitrary
partial nulls would additionally require subset pivotality or a valid partial-
null randomization law. That condition has not been proved here. A signal in
one structure can also change the finite-sample distribution of the other
statistic because both are computed from the same rooms.

Accordingly, `profile adjusted evidence` and `Mantel adjusted evidence` are
the correct current terms. They should not be described as causal mechanism
identification or proof that exactly one latent structure generated the data.

## Strength and Permutation Grid

Two unequal-building designs were evaluated at signal multipliers `.6, 1,
1.4` for covariate radial, dyadic, and mixed alternatives. Each cell has two
independent 50-dataset seeds. The same pool of 999 within-building
permutations was truncated to 199 and 499, so stability comparisons are paired.

Across all 18 alternative design-strength cells:

| Permutations | Mean omnibus power | Mean regret | Worst regret | Decision agreement with 999 | Winner agreement | Attribution agreement |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 199 | .387 | .019 | .050 | .962 | .971 | .932 |
| 499 | .401 | .017 | .050 | .984 | .988 | .968 |
| 999 | .405 | .017 | .060 | 1.000 | 1.000 | 1.000 |

Regret is `power(best fixed component) - power(omnibus)` in the same cell. It
can be negative when the standardized combination rejects datasets missed by
either individual unadjusted rule. The worst positive values occurred in
strong radial or dyadic cells; the omnibus is robust, not costless.

The focused null rows had rejection `.030`, `.045`, and `.030` at 199, 499,
and 999 permutations. Their 100-dataset intervals are broad, so primary size
evidence still comes from the previous 600-per-cell and 1,600-dataset
conditional-null studies. Nothing in this follow-up contradicts those results.

The stability result supports 499 as the routine simulation default. Use 999
for final weak-signal or near-threshold reporting when attribution itself is a
substantive conclusion. At 199, decisions were mostly stable but adjusted
attribution changed in about seven percent of alternative cells.

## Why the Covariate Radial Label Was Not a Truth Label

At 999 permutations, the covariate radial scenario gave nearly equal average
standardized profile and Mantel evidence and selected profile as winner only
about `.48` of the time. Adjusted evidence was often present in both
components. This is not a failed attribution: correlated room radii alter both
observation salience and multiple pairwise distances. Calling the generator a
pure profile alternative would overstate its construct separation.

The dyadic scenario was more distinct. Mantel was the standardized winner
about `.78` of the time, increasing from `.64` at strength `.6` to `.88` at
strength `1.4`. Its mean 999-permutation omnibus regret was `.033`.

## Focused Construct-Separation Check

The original four-building target-separation generator provides more explicit
profile-oriented and dyadic-oriented alternatives. Each row below combines two
300-dataset seeds and 499 permutations.

| Scenario | Profile power | Mantel power | Omnibus power | Regret | Expected winner | Adjusted evidence given rejection |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Conditional null | .045 | .045 | .038 | .010 | -- | unstable small null count |
| Node salience/sign rewiring | .825 | .702 | .812 | .013 | Profile `.735` | P-only `.172`, M-only `.033`, both `.795` |
| Shared dyadic geometry | .790 | .958 | .952 | .007 | Mantel `.998` | P-only `.000`, M-only `.235`, both `.765` |

The evidence ranking identifies the intended stronger component well,
especially for dyadic geometry. Exclusive adjusted attribution is uncommon
because the alternatives are not mathematically orthogonal: node salience
changes some distances, and shared geometry can induce aligned room radii.
Reporting `both` is therefore often scientifically more honest than forcing a
single mechanism label.

## Decision Update

1. Learned adaptive mixtures remain rejected as primary candidates.
2. Standardized max remains a defensible predeclared omnibus sensitivity test.
3. It is now interpretable through standardized winner and maxT-adjusted
   component evidence, provided the global-null/partial-null distinction is
   stated.
4. It should always be accompanied by both raw effect estimates, both
   unadjusted component permutation p-values, and both adjusted evidence
   values.
5. It still should not replace `c_delta_star` or Mantel as an effect parameter.
6. Promotion to a primary decision rule still requires the scientific target
   to be explicitly changed to “evidence for either declared internal-
   structure concordance.”

## Next Theoretical Check

Before any promotion, construct exact or asymptotically valid partial-null
models and determine whether subset pivotality is plausible. If it fails, use
closed testing or report adjusted component evidence only descriptively after
the globally valid omnibus decision.

## Files

- `scripts/run_omnibus_interpretability_20260813.py`
- `scripts/summarize_omnibus_interpretability_20260813.py`
- `results/omnibus_interpretability_combined_20260813.tsv`
- `results/omnibus_target_attribution_combined_20260813.tsv`
