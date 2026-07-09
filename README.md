# c_delta Simulation Pilot

This is a small first-stage project for studying the finite-sample behavior of the
correlation-of-divergency coefficient, `c_delta`.

## Goal

The first deliverable is a reproducible simulation baseline:

- implement `c_delta` and its divergence vectors;
- report raw `c_delta`, a sample-dependent pairing-normalized version, and the
  Pearson correlation between divergence vectors;
- run permutation tests for the null hypothesis that the pairing between `x`
  and `y` carries no divergence-structure signal;
- run paired bootstrap confidence intervals;
- compare behavior under normal, heavy-tailed, skewed, and contaminated data.

This keeps the first phase close to Professor Hoorn's suggestion that simulation
studies are most urgent, while leaving room for later h-star screening, robust
variants, weighting schemes, and machine-learning examples.

## Files

- `src/cdelta.py`: statistic, permutation test, bootstrap CI, and data generators.
- `scripts/run_pilot.py`: example simulation run.
- `scripts/run_outlier_influence.py`: matched/unmatched extreme-value pilot.
- `scripts/run_outlier_repeated.py`: repeated extreme-value alignment study.
- `tests/test_cdelta.py`: minimal unit tests using Python's built-in `unittest`.

## Quick Start

From this folder:

```bash
python3 -m unittest discover -s tests
python3 scripts/run_pilot.py
python3 scripts/run_outlier_influence.py
python3 scripts/run_outlier_repeated.py
```

If using the Codex bundled runtime on this machine:

```bash
/Users/jialiangyao/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m unittest discover -s tests
/Users/jialiangyao/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/run_pilot.py
/Users/jialiangyao/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/run_outlier_influence.py
/Users/jialiangyao/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/run_outlier_repeated.py
```

## First Simulation Questions

1. How stable is raw `c_delta` as a function of sample size?
2. Does pairing-normalization reduce sample-specific scale effects?
3. How often does the permutation test reject under null, aligned, inverted,
   nonlinear, heavy-tailed, skewed, and contaminated settings?
4. How wide are bootstrap intervals across these settings?
5. Which scenarios separate `c_delta` from Pearson/Spearman-style association?
6. When does a single extreme value define a shared divergence structure rather
   than merely destabilizing the statistic?

## Next Extensions

- Add h-star based outlier assessment before robustifying `c_delta`.
- Treat zero-divergence cases as "undetermined due to data limitations" in
  reports rather than as computational errors.
- Compare matched, mismatched, and one-sided extreme observations to study when
  a single observation defines shared divergence structure.
- Add L1/Gini and rank-based variants.
- Add weighted pairwise distances after defining a principled weight function.
- Add comparisons with energy distance and MMD.
- Add machine-learning examples, such as comparing dispersion structures in
  embedding dimensions, model residuals, or representation clusters.
