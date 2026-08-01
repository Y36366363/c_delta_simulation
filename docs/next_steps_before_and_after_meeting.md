# Prioritized Next Steps Around the 2026-08-03 Meeting

Date: 2026-08-01

## Before the Meeting

### 1. Consolidate the estimand

Use one working description consistently:

> positive alignment between paired observation-level divergence salience
> profiles.

Keep the binary-overlap formula as an explanatory limiting case, not as the
definition of the continuous statistic.

### 2. Prepare three figures, only if useful for discussion

1. rejection rate against paired-overlap fraction by background;
2. binary theoretical correlation against observed divergence correlation;
3. random-set-null overlap frequencies against the exact hypergeometric PMF.

These would communicate signal, attenuation, and calibration without requiring
the professor to inspect large tables.

### 3. Decide the questions that require the professor's judgment

- Is the revised target explicitly paired salience alignment?
- Is the binary model helpful, or does it overemphasize outliers?
- Does negative salience alignment have an intended application?
- Should a full-distance-matrix comparator be included?
- In the intended application, what makes observation pairing scientifically
  meaningful?

Further broad simulations should wait until these choices are discussed.

## Work That Can Start Now

### Exact random-overlap reference

Implement and test

```text
P(M=m) = choose(k,m) choose(n-k,k-m) / choose(n,k)
```

for independently selected equal-size standout sets. This connects the binary
model to the proper random-set null and distinguishes it from a deliberately
disjoint negative control.

Status: implemented and unit-tested on 2026-08-01.

### Meeting-oriented record

Maintain the concise meeting note separately from the cumulative technical
record so conclusions, limitations, and questions can be retrieved quickly.

Status: completed in `docs/meeting_discussion_20260803.md` and
`docs/meeting_addendum_high_rep_20260801.md`.

## After the Meeting: Highest-Value Branches

### Branch A: Manuscript reframing

If the professor accepts the paired-salience target:

1. rewrite the definition and estimand section;
2. state the L2 absolute-deviation identity;
3. state the `c_delta`/divergence-correlation identity;
4. introduce binary overlap as intuition;
5. distinguish row salience from full pairwise geometry.

### Branch B: Full-matrix comparator

If general internal structure remains an intended claim, compare `c_delta`
with a pre-specified full-distance-matrix statistic under:

- salience-aligned but geometry-misaligned alternatives;
- geometry-aligned alternatives;
- ordinary dependence without salience alignment;
- random-set nulls.

This would identify which information is gained or lost by row aggregation.

### Branch C: Application-driven validation

If the professor identifies a target application, design simulations around
its actual pairing mechanism and scientifically meaningful standouts. This is
more valuable than adding arbitrary distributions.

### Branch D: Alternative direction

If negative salience alignment is meaningful, expand lower-tail and two-sided
validation across sample sizes and tails. Otherwise retain upper-tail as the
primary analysis and avoid unnecessary scope.

## Lower-Priority Work

- additional generic distribution grids;
- robust/rank variants before the estimand is settled;
- more permutation counts in already stable cells;
- manuscript-scale raw tables before reporting conventions are finalized.

The current empirical claims already have high-replication support. The next
major gain should come from conceptual decisions and application specificity,
not simulation volume alone.
