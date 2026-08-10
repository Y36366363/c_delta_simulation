# Mixed-Path Local Effect and Power Slopes

## Question

The previous strength-surface study located profile-versus-Mantel crossovers
and showed that node strength was the larger surface direction. This update
asks what happens locally when the *mixture weight itself* changes near a
crossover.

Two derivatives must be kept separate:

1. the derivative of a smooth population or sample effect statistic;
2. the derivative of rejection probability, or power.

The second is not obtained by differentiating a dataset's reject/not-reject
indicator. It is estimated as a finite difference of probabilities.

## Mixture path and tangent

Let the standardized node and dyadic components be `N` and `D`. The simulation
path is

\[
X_w=\sqrt{1-w}\,N_X+\sqrt w\,D_X,
\qquad
Y_w=\sqrt{1-w}\,N_Y+\sqrt w\,D_Y.
\]

For `0<w<1`, its pathwise tangent is

\[
\dot X_w=-\frac{N_X}{2\sqrt{1-w}}
          +\frac{D_X}{2\sqrt w},
\qquad
\dot Y_w=-\frac{N_Y}{2\sqrt{1-w}}
          +\frac{D_Y}{2\sqrt w}.
\]

The derivative becomes singular at the endpoints because `w` is a variance-
share parameter. The present result is therefore local to interior weights,
not an endpoint differentiability claim.

## Generic correlation derivative

For paired paths `A_w,B_w`, write

\[
M_{11}=\operatorname{Cov}(A_w,B_w),\quad
M_{20}=\operatorname{Var}(A_w),\quad
M_{02}=\operatorname{Var}(B_w),
\]

and

\[
T(w)=\frac{M_{11}}{\sqrt{M_{20}M_{02}}}.
\]

Provided the moments are differentiable and the variances are positive,

\[
\dot T(w)=\frac{1}{\sqrt{M_{20}M_{02}}}
\left[
\dot M_{11}-\frac{M_{11}}{2}
\left(\frac{\dot M_{20}}{M_{20}}
     +\frac{\dot M_{02}}{M_{02}}
\right)
\right].
\]

The required moment derivatives follow from centered `A,B` and their centered
tangents:

\[
\dot M_{11}=E(\dot A_c B_c+A_c\dot B_c),\quad
\dot M_{20}=2E(A_c\dot A_c),\quad
\dot M_{02}=2E(B_c\dot B_c).
\]

## Profile and Mantel specializations

For the profile target,

\[
A_w=|X_w-\theta_X(w)|,qquad
\dot A_w=\operatorname{sgn}(X_w-\theta_X)
          \{\dot X_w-\dot\theta_X(w)\},
\]

and similarly for `Y`. The simulated margins are symmetric, so the population
Huber locations satisfy `theta_X=theta_Y=0` throughout the path and their
path derivatives are zero. Marginal MAD division also cancels from Pearson
correlation. Consequently the current symmetric-generator derivative reduces
to `sgn(X_w) dot X_w`.

This simplification is not a general asymmetric-distribution theorem. Under
skewness, the implicit Huber-location derivative and the MAD-to-Huber nuisance
path derived in the earlier functional-delta work must be restored.

For the population Mantel target, take an independent copy `(X'_w,Y'_w)` and
set

\[
A_w=|X_w-X'_w|,qquad
\dot A_w=\operatorname{sgn}(X_w-X'_w)
          (\dot X_w-\dot X'_w),
\]

with the analogous expression for `B_w`. Substitution into the generic
correlation derivative gives the local Mantel effect slope.

## Population derivative validation

Four configurations were evaluated at their previously estimated crossover
weights. Each method/configuration row used 20 batches of 50,000 independent
dyads. The pathwise derivative was checked against a common-random-number
central difference with half-width `.001`.

| configuration | node rho | dyad rho | w | profile slope | Mantel slope | slope difference |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| default | .55 | .70 | .216 | -.581 | -.096 | -.485 |
| weak both | .35 | .30 | .225 | -.440 | -.131 | -.309 |
| strong node, low dyad | .65 | .30 | .362 | -.586 | -.236 | -.350 |
| balanced strong | .65 | .65 | .258 | -.623 | -.141 | -.482 |

The maximum absolute difference between the pathwise formula and numerical
derivative was `.000166`. All eight effect slopes were negative, and the
profile slope was more negative in every configuration.

This is an important refinement. Near these crossovers, increasing dyadic
variance weight does not necessarily make Mantel's raw effect increase
immediately. It can initially dilute the remaining node-derived geometry in
both methods. The crossover occurs because the profile statistic loses its
node-specific advantage faster than Mantel, not because one curve must rise
while the other falls.

## Finite-sample power slopes

For each configuration, two independent seeds used 800 datasets each, 199
within-building permutations, and the same latent components/permutations at
all five weights. Slopes were calculated at half-widths `.025` and `.05`.

The `.05` combined estimates are:

| configuration | profile power slope | Mantel power slope | difference slope | SE of difference |
| --- | ---: | ---: | ---: | ---: |
| default | -1.325 | -.788 | -.538 | .103 |
| weak both | -.744 | -.650 | -.094 | .085 |
| strong node, low dyad | -.969 | -.638 | -.331 | .089 |
| balanced strong | -1.263 | -.744 | -.519 | .098 |

The default, strong-node/low-dyad, and balanced-strong difference slopes are
resolved below zero. The weak-both difference is not resolved, consistent with
the broad zero-difference band found on 2026-08-09. Both independent seeds gave
negative individual method slopes in every configuration. Half-width `.025`
gave the same direction throughout; its largest change from the `.05` estimate
was `.188`, comparable to the Monte Carlo uncertainty of the noisier power
derivatives.

At each center, the newly simulated profile-minus-Mantel power difference was
small: `+.014,-.016,-.011,-.007` in the table order. These new seeds therefore
support the previous crossover locations without requiring exact equality of
two Monte Carlo power estimates.

## Noncentral approximation

If a one-sided standardized test satisfies approximately

\[
Z_j(w)\sim N\{\lambda_j(w),1\},
\]

then

\[
\pi_j(w)\approx
\Phi\{\lambda_j(w)-z_{1-\alpha}\},
\qquad
\dot\pi_j(w)\approx
\phi\{\lambda_j(w)-z_{1-\alpha}\}\dot\lambda_j(w).
\]

A local probit transformation of the endpoint powers reproduced the direct
finite-difference power slopes to maximum absolute discrepancy `.0187`. This
is a useful consistency diagnostic, but it is partly algebraic and does not
prove asymptotic normality of the finite-sample permutation statistic.

## Independent check of the previous pure-path logic

The eight one-million-dyad pure-path rows were repeated with a new seed. Node
profile-minus-Mantel gaps differed from the earlier run by at most `.00131` and
again increased monotonically from about `.211` to `.446`. Dyad gaps changed by
at most `.00150` and remained close to zero. Thus the pure-path mechanism is
stable and agrees in sign with the new mixed-path slopes.

## Conclusions and boundaries

- The previous claim that node strength is the larger crossover direction is
  supported by an explicit local tangent calculation and new simulation.
- Dyad strength remains non-negligible. “Node driven” means preferential loss
  of node-profile information along `w`, not independence from the dyadic
  component.
- Changing dyad correlation `rho_D` and changing mixture weight `w` are
  different paths and can have different derivative signs.
- Local effect slopes are mathematically smoother and more stable than power
  slopes. Power derivatives should be reported with their half-width and Monte
  Carlo SE.
- These slopes explain a pre-specified simulation design. They do not authorize
  post-hoc selection between profile and Mantel tests.

## Reproducible files

- `scripts/run_mixed_path_local_slopes_20260810.py`
- `tests/test_mixed_path_local_slopes_20260810.py`
- `results/mixed_path_population_slopes_20260810.tsv`
- `results/mixed_path_power_slopes_slope_seed1_20260810.tsv`
- `results/mixed_path_power_slopes_slope_seed2_20260810.tsv`
- `results/mixed_path_power_slopes_combined_20260810.tsv`
- `results/pure_path_population_replication_20260810.tsv`
