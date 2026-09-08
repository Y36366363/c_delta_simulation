# Prespecified active-nuisance validation (2026-09-07)

Written before inspecting the new Monte Carlo outcomes. This is one existing
law, not a new distribution grid or a method-selection exercise.

- Reuse the 2026-09-03 benchmark: `(log X, log Y)` has marginal SD 0.60,
  zero means, and latent Gaussian correlation 0.40.
- The target is the population median/MAD-scaled Huber profile correlation,
  with `k=1.4826`, `c=1.345`. It is not the latent Gaussian correlation.
- Before coverage simulation, independently establish population truth using
  truncated-lognormal analytic moments and split adaptive quadrature. Check
  complete IF variance by tensor quadrature split at every nuisance knot,
  with increasing orders. Retain the old Gauss--Hermite output unchanged and
  explicitly report any quadrature discrepancy.
- Run `n=160,640,2560`, 2,000 paired IID replications per size, fixed root seed
  `2026090701`. Each replication has its own SeedSequence `[root,n,rep]`.
  No optional stopping or additional scenario selection from the results.
- Compare (i) public-API complete KDE plug-in IF, (ii) the same fitted-profile
  estimate but an intentionally incomplete direct-only IF SE, and (iii) an
  oracle estimator with both population locations fixed and its correct
  direct IF SE. The oracle is an infeasible benchmark, not a new recommendation.
- Keep the sample variance correction `n/(n-1)` and ordinary untruncated
  two-sided 95% Wald intervals. No Fisher transform, permutation, HC tuning,
  or post hoc interval adjustment.
- Save replication-level values, errors, seeds and paired coverage indicators;
  report bias with MCSE, empirical SD, mean SE, SE/SD, interval width, coverage
  with Wilson intervals, studentized tails, and paired coverage differences
  with MCSE. Failures remain explicit, not silently replaced or resimulated.
- Numerical correctness tests must not assert that full inference has higher
  finite-sample coverage than the ablation. First-order necessity need not
  imply a large practical advantage in this particular law.
- A passing study supports only this fixed regular law. It cannot establish
  a universal minimum sample size, global robustness, permutation validity,
  or a diagnostic cutoff.

In parallel, incorporate the report's mechanism/scope corrections into active
manuscript text: distinguish nonregular median/MAD fitting from flat Huber
curvature, qualify the imposed-offset binary identity, and distinguish an
unexplained-by-index family residual from a proved higher-order decomposition.
