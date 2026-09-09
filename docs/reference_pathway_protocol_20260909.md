# Prespecified staged reference-pathway check (2026-09-09)

Design below written before inspecting this experiment's outcomes, following Professor
Hoorn's September 9 request. This is an internal prespecification, not an
external preregistration.

## Design and stopping rule

Reuse X=S exp(tau U), Y=S exp(tau V), independent standard normal U,V and
one shared independent Rademacher S per pair. Reuse the severe tau=.10 and
diffuse control tau=.40, each at n=80 and n=640. Run 2,000 repetitions per
cell with root seed 2026090901, and PCG64 SeedSequence
[root, round(100*tau), n, replication]. Compare all stages on identical pairs.
Do not choose additional families, sizes, seeds, or replications after seeing
the outcomes. The population target at every positive tau is rho_P=0, C=1.

## Four stages

1. `population_reference`: T_X=T_Y=0 fixed at population values; no fitted
   location influence. Population raw MAD=1 and s=k=1.4826.
2. `population_scale`: s=k fixed; fit both Huber locations with c=1.345.
3. `population_median`: m=0 fixed; estimate each raw MAD as median(abs(W));
   s=k*d_hat; fit both Huber locations.
4. `full_fit`: estimate median, raw MAD about that median, and Huber location
   using the public procedure. Do not silently replace its algorithm. Compare
   its score residual and root with a bracketed solution for diagnostics.

Use brentq for stages 2--3; roots are unique almost surely for these draws.
Record stage-4 solver discrepancies instead of silently replacing the fit.
Population-reference RMSE is zero and cross-reference correlation is **NA**,
not zero, because neither reference varies across repetitions.

## Studentization and interpretation

Keep intact pairs and the ordinary sample-variance correction. For each
stage report two explicitly distinguished empirical-null rejection rates:

- `stage_aware`: the stage's five-moment IF plus the appropriate fitted-
  reference path. At stage 2 IF_T=s psi/A. At stage 3
  IF_d=(.5-1(abs(W)<=d))/(f(d)+f(-d)); IF_T=s psi/A-(B/A)k IF_d.
  Stage 4 uses the public full median/MAD/Huber plug-in IF. Stage 1 is the
  direct profile IF. KDE endpoints are used consistently with the public API.
- `direct_only`: the same fitted profiles, omitting all fitted-location IF
  terms. This is a common computational standardization formula, not a valid
  general fixed-reference approximation for stages 2--4.

Use two-sided |Z|>1.959963984540054. Stage 4 violates regular median
identification in this law, so its IF-based test is an empirical stress
calculation, not a theorem-validated level-.05 test. Do not label these as
validated Type I error rates or compare differently studentized statistics
without showing which one is used. Rejection is only one mechanism outcome:
also report mean rho_P, mean C, reference RMSEs, cross-reference correlation,
sample-mean tracking, median/MAD summaries, sign-imbalance association, active
Huber fractions, numerical failures, and root residuals.

Show paired adjacent-stage changes in rejection with MCSE, and differences
in mean effect and squared reference error with paired MCSE. Compare stage 2
directly with stage 4 as well. Estimate RMSE MCSE by the delta method on the
mean squared errors; correlation is descriptive, with a paired-repetition
delta-method MCSE when nondegenerate, not a normal-bivariate assumption.

Retain every repetition, both successful and failed. Do not resimulate failed
draws. Report valid denominators, per-stage failure reasons and complete-case
paired denominators. No permutation simulation is needed for this task.

## Short model result

Prove population m=T=0, d=1, rho_P=0 and C=1 for tau>0; give f(0)=0 and
the nonzero population Huber slope. Distinguish nonregular median fitting
from nonunique median or flat Huber fitting. Explain the imposed-offset
covariance identity and its sample-dependent-reference limitation. Treat
tau approximately n^(-1/4) only as a conditional rate-balance heuristic
under root-n reference errors and an appropriate local profile approximation,
not a proved boundary for the complete nonregular estimator.

The existing nonzero-skew study is complete and is not rerun or tuned. Do not
add clustered-data theory, a universal threshold, a new resampling method,
or an application without a verified sampling design.

## Post-run mathematical correction (2026-09-09)

The original sentence claiming almost-sure uniqueness of empirical roots
above is too strong and is retained only as protocol history. Population
uniqueness does not imply uniqueness in every finite sample: at a fixed scale,
an exactly sign-balanced sample separated beyond the clipping intervals can
have an interval of empirical Huber roots, with positive (possibly extremely
small) probability. The stage-aware calculation requires a positive empirical
active fraction and records an invalid return otherwise. No such invalid
return occurred in the declared run. This correction changes neither the
design, stored outcomes, nor population uniqueness proof; no replacement
draws or new simulation cells were introduced.
