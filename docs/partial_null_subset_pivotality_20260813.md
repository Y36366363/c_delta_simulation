# Partial-Null and Subset-Pivotality Validation

Date: 2026-08-13

## Question

The standardized max statistic is exactly valid for the joint within-building
random-pairing null.  Can its maxT-adjusted profile and Mantel p-values also be
interpreted as strong component-level discoveries when only one component
null is true?

## Null-Hypothesis Boundary

Both component tests permute the same paired room labels.  Their exact
randomization null is therefore the same joint exchangeability statement.  A
profile association can be zero while Mantel geometry remains associated, but
then the labels are not exchangeable.  Such a profile null is a weak
effect-parameter null, not an exact randomization null.  The same distinction
applies in the opposite direction.

Subset pivotality would require the distribution of a true-null component
statistic to be invariant to whether the other component is null or non-null.
This was assessed directly rather than assumed.

## Calibrated Partial-Null Models

### Profile null, Mantel alternative

The two margins used 60 independent positive radii and the same randomly
ordered balanced sign skeleton (30 negative and 30 positive signs).  Their
population Huber centres are zero, so robust radius profiles are independent
in the population, while the shared sign partition induces a strong pairwise-
distance association.  No radii were duplicated.  The confirmatory empirical
effects were:

- mean profile correlation `-.00982`;
- mean Mantel correlation `.36925`.

### Mantel null, profile alternative

A 60-room template used common smoothly varying magnitudes and different
balanced sign geometries.  A small amount of the aligned geometry was mixed
into the low-Mantel template and independent Gaussian noise was added.  The
mixing coefficient was calibrated on 20,000 independent datasets, not on the
test samples:

- calibrated mixing coefficient `.052813`;
- calibration mean Mantel correlation `2.67e-8`;
- calibration mean Huber-profile correlation `.80461`.

The independent confirmatory samples had mean Mantel correlation `.0000585`
and mean profile correlation `.80382`.

## Confirmatory Design

- 500 independent datasets per global-null or partial-null condition;
- sample size 60;
- 499 Monte Carlo permutations per dataset;
- matched global-null controls retained the relevant marginal construction
  but independently permuted the second margin;
- comparison metrics: component effect, standardized null-component score,
  empirical KS distance from the matched global null, unadjusted rejection,
  maxT-adjusted rejection, omnibus rejection, 95% max-reference critical
  value, and permutation-reference component correlation.

## Results

| Path and scenario | Null effect | False effect | Null-z SD | KS vs global | Raw null reject | maxT null reject | False-component reject | Omnibus reject |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Profile path, global null | `.00516` | `.00115` | `.979` | `0` | `.056` | `.044` | `.050` | `.052` |
| Profile path, partial null | `-.00982` | `.36925` | `1.035` | `.076` | `.056` | `.038` | `.972` | `.970` |
| Mantel path, global null | `-.000031` | `-.00133` | `1.083` | `0` | `.052` | `.042` | `.046` | `.054` |
| Mantel path, partial null | `.000058` | `.80382` | `.075` | `.596` | `0` | `0` | `1.000` | `1.000` |

The independent-observation profile partial null showed only a modest
distributional difference (KS `.076`) and no rejection inflation: raw
rejection was `.056` under both matched global and partial nulls, while maxT
rejection was `.044` and `.038`.  An earlier paired-radius pilot appeared
anti-conservative, but that construction duplicated each radius and therefore
confounded partial-null behavior with pseudo-replication; it was replaced and
is not used for the conclusion.

The Mantel partial null demonstrates the opposite failure: its score collapses
toward zero, producing no false rejections.  Conservatism does not rescue
subset pivotality; the null-component distribution still changes drastically
(KS `.596`).  The failure therefore persists at `n=60` and is not merely the
discreteness of the original six-point counterexample.

Permutation-reference critical values and component dependence changed only
modestly within each matched path.  The failure is driven mainly by the
observed null-component distribution under the weak partial null, not by a
large shift in the max reference critical value.

## Decision

General subset pivotality is rejected for these weak, statistic-specific
partial nulls because the Mantel null-component distribution depends strongly
on the profile alternative.  The two cleaned confirmatory paths did not show
component Type-I inflation—the profile path was calibrated and the Mantel path
was strongly conservative—but finite simulation over two paths is not a proof
of strong control.  Consequently:

1. the standardized max p-value remains a valid global omnibus test of the
   joint within-building random-pairing null;
2. maxT-adjusted component p-values must not be reported as strong component-
   level discoveries under partial nulls;
3. winner labels, raw component effects, and adjusted component evidence may
   be reported descriptively after the omnibus result, with an explicit
   global-null interpretation;
4. closed testing is not yet a solution: it requires valid local tests for
   the profile-only and Mantel-only weak nulls, which the current shared-label
   permutation tests do not provide;
5. formal component claims would require separately derived weak-null tests,
   such as asymptotically studentized statistics with valid nuisance handling,
   followed by a multiplicity procedure whose assumptions are proved.

This result does not weaken the definition or inference developed for
`c_delta_star`.  It narrows only the interpretation of the exploratory
profile/Mantel standardized-max omnibus and its component attribution.

## Files

- `scripts/run_partial_null_subset_pivotality_20260813.py`
- `tests/test_partial_null_subset_pivotality_20260813.py`
- `results/partial_null_calibration_confirmatory_20260813.tsv`
- `results/partial_null_subset_pivotality_confirmatory_20260813.tsv`
