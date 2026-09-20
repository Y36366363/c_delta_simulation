# One moderate regular benchmark and solver comparison — 2026-09-20

Internal protocol fixed before numerical truth or simulation outcomes are
computed. This is not third-party preregistration. The user's September 20
request authorizes one bounded complementary check, not outcome-selected
search for a calibrated example.

## Design and reporting commitment

Let (Z1,Z2) be standard bivariate normal with correlation .4 and let
X=exp(.3 Z1), Y=exp(.3 Z2). The log SD .3 is fixed at half the previous .6
stress study, retaining its dependence structure. No candidate grid or
coverage pilot is used. All marginal densities required by the theorem are
positive at the relevant interior boundaries and all moments exist. Verify
nonzero target and nuisance coefficient numerically before simulation. If
either verification or quadrature fails, stop and report; do not switch laws.

Sample sizes 160,640,2560; 2,000 datasets each; root seed 2026092001;
PCG64/SeedSequence([root,n,rep]). Draw an n-by-2 standard-normal array, set
X=exp(.3*z[:,0]), Y=exp(.3*(.4*z[:,0]+sqrt(1-.4**2)*z[:,1])). Use midpoint
median/MAD, k=1.4826, c=1.345, default Gaussian KDE, sample variance correction,
and two-sided untransformed 95% Wald intervals.

Primary complete IF uses the existing `score_checked` mode. Direct-only uses
the same checked references, removing their influence terms only. Oracle
fixes population references and uses the matching direct variance. No new
solver implementation or default change. Record all failures and denominators.

Primary summary: complete coverage and Wilson interval at n=2560, reported
alongside both smaller sizes. A Wilson interval containing .95 means compatible
with nominal coverage at this MC resolution, not proof of calibration. Report
all cells regardless of outcome. Also report bias, empirical SD, mean SE,
SE/SD, interval width, tail misses and paired complete-minus-direct coverage
with MCSE. Active nuisance does not guarantee an appreciable variance gap or
superiority of the complete interval in any single finite sample design.

Use independent conditional adaptive integration for target moments and
knot-split tensor quadrature at 48 and 72 nodes for IF variance. Require
cross-moment discrepancy <1e-8, relative variance discrepancy <1e-7,
abs(target)>1e-4 and abs(reference coefficient)>1e-4. The numerical formulas
are copied from the existing audited September 7 engine, with declared
parameter changes; do not modify that historical engine or its outputs.

## Prospective numerical equivalence check

On every dataset also run legacy complete IF at the same KDE/settings.
Record estimate differences in checked-SE units, relative SE differences,
reference differences in fitted-scale units, sqrt(n) legacy score residual,
all checked residual diagnostics and coverage-decision differences.
Numerical comparison thresholds, fixed now: |estimate delta|/checked SE <1e-4,
|relative SE delta|<1e-4. Report breaches and every changed coverage decision;
neither thresholds nor zero changed decisions establish an asymptotic theorem.
This is prospective with respect to these data, not independent implementation.

## Limited constant sensitivity

For the existing .6 log-SD law only, numerically recompute population T and
rho for c=1.0 and c=1.5 with k unchanged, alongside c=1.345. No Monte Carlo
grid or comparison of coverage against an unchanged target. Huber's location
equation depends on c and k through c*k because psi_c(u)=c*psi_1(u/c).
Explain that alternative constants generally define different reference-profile
targets under asymmetry. Sensitivity here concerns population targets, not a
universal statement about calibration or robustness.

New outputs use September 20 names. Preserve all frozen inputs; report source
hashes, environment and protocol hash. Manuscript inclusion is bounded and
must retain the previous skew failure evidence irrespective of new results.
