# Targeted proof and solver audit protocol — 2026-09-14

This is an internal protocol recorded before calculating new audit outcomes,
not third-party preregistration. It concerns manuscript completion, not a new
calibration study. The public API, constants, frozen results and sent PDFs are
not changed.

## Mathematical questions

1. Make the moving weighted-sign bound and localization of random coefficients
   explicit, including why within-pair dependence is allowed.
2. Supply the maximum-observation argument for weak-null empirical-norm
   consistency with finite second moments; explain the failure of unrestricted
   population L2 consistency when fourth moments are infinite.
3. Prove an n-dependent Huber score stopping rule in real arithmetic, and
   distinguish it from finite-machine success and from a positive local slope.

## Candidate numerical procedure

Keep the existing midpoint median, raw MAD, k=1.4826 and c=1.345. Use bracketed
bisection with acceptance threshold |q_n(t)| <= 1/(10^8 n). Check the returned
location in the original data units. Independently evaluate the clipped score
with exact rational arithmetic on the represented input floats, scale, clipping
constant and candidate location before accepting. A cap or adjacent floating
endpoints causes a reported failure, never a silent return or relaxed tolerance.
This is a diagnostic prototype, not a new public default.

In ideal arithmetic the prescribed threshold is o(n^-1/2). A rational check
certifies the residual for represented inputs, not rounding-free population
quantiles or success for every arbitrarily large IEEE floating-point dataset.

## Bounded numerical comparison

Reuse exactly the September 12 selection: 27 nonzero-skew datasets with
n=160,640,2560 and replication IDs 0,1,2,10,100,500,1000,1500,1999; plus 14
pathway datasets with tau=.1,.4, n=80,640 and IDs 0,1,1999, with the two known
flags 70 and 1622 added only to tau=.1,n=640. Inclusion of these flags is post hoc.
Use the existing generators and original random stream definitions.

For all 82 margins report legacy and candidate scores, exact residual checks,
root changes and iteration counts. Recompute the complete marginal IF and both
full and direct studentizers on each of the 41 intact datasets. Compare estimates,
standard errors and confidence/rejection decisions with the unchanged public API.
Report all failures. Do not estimate a new coverage rate from this selection.

## Deterministic tests and artifacts

Test a linear-region mean root, active clipping, a nonunique flat root,
translation/scaling, exhausted iteration budget, infeasible floating-point
resolution, invalid inputs, an exact-score acceptance false positive, and the
absolute-radius/weighted-sign bounds. These test algebra and implementation;
they cannot prove an empirical-process limit.

Write new audit outputs under their own dated names. Record source hashes and
environment. No frozen file, source hash, or original failure is overwritten.
