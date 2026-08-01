# Discussion Points for Meeting with Professor Hoorn

Prepared: 2026-08-01

## One-Sentence Update

The new simulations support the paired-standout interpretation: when both
datasets contain the same number and strength of standouts, rejection rises
primarily with the overlap of their paired indices, while heavy-tailed
background salience attenuates that signal.

## Three Results Worth Showing

### 1. Overlap, not merely the presence of standouts, drives detection

Across 27,000 datasets, average rejection increased from about `.02` at zero
paired overlap to about `.81-.84` at full overlap. Both datasets contained
equally many, equally strong standouts in every condition.

This is the most direct empirical support for:

> whether the same paired observations stand out from their respective groups.

### 2. There is a simple theoretical overlap formula

For binary standout indicators with `k` standouts in each dataset and `m`
shared paired indices,

```text
r_binary = (n m - k^2) / (k (n - k)).
```

Chance overlap corresponds to expected correlation zero; full overlap gives
one. This may offer a clean way to explain the estimand before introducing
continuous divergence scores.

### 3. Overlap alone is not the whole power story

At `n = 80`, `k = 4`, magnitude 8, and full overlap, L2 power was:

- normal: `1.000`;
- t3: `0.945`;
- t2: `0.500`.

The same paired observations stand out by construction, but natural heavy-tail
salience makes the planted subgroup less distinct. The method therefore
reflects paired overlap through a signal-to-background-salience contrast.

## Important Qualification

The phrase "stand out" should not be restricted to a binary outlier label.
Earlier diffuse-profile simulations detected continuous salience alignment
without a small extreme subgroup. A precise description is:

> paired observation-level divergence salience alignment.

Also, perfect salience alignment does not imply matching full pairwise
geometry; row aggregation discards relational information.

## Questions to Ask

1. Should the revised paper explicitly define its estimand as positive paired
   divergence-salience alignment?
2. Would the binary-overlap model be useful as an explanatory limiting case,
   or would it make the method sound too outlier-specific?
3. Is negative salience alignment scientifically meaningful, or should the
   paper retain only the upper-tail alternative?
4. Should the paper compare `c_delta` with a full distance-matrix method to
   make the information retained and discarded by row aggregation explicit?
5. Does the intended application view observations as inherently paired? If
   pairing is absent or arbitrary, the target changes fundamentally.

## Claims to Avoid

- a general correlation of internal structures;
- a general dependence measure;
- a test that merely checks whether both samples contain outliers;
- interpreting raw `c_delta - 1` without the divergence CV factor;
- claiming heavy tails invalidate calibration.

## Current Working Description

> In its current one-dimensional form, `c_delta` is a
> permutation-calibrated measure of positive alignment between paired
> observation-level divergence salience profiles. It tests whether observations
> that are relatively peripheral or central in one dataset tend to be similarly
> peripheral or central in the other.
