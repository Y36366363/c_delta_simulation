# Externalized validation of the three claims

Date: 2026-08-25

## Purpose

This update asks whether the mechanisms assigned to the three claims remain
distinct under interventions that were not used to construct the original
evidence. Claim 1 fixes the population robust reference, Claim 2 varies only
cross-margin sign coupling, and Claim 3 prospectively evaluates a fifth bridge
family.

## Claim 1: strong-skew distortion is not reference-estimation distortion

For the independent lognormal--gamma weak null, the population Huber centres
were obtained by distribution-level numerical integration:

\[
T_X=1.23196,
\qquad
T_Y=0.52955.
\]

The ordinary full-IF test was paired with an oracle version fixing these
centres and omitting their nuisance-estimation contribution.

| n | Reference | Rejection | z SD | z 2.5% | z 97.5% |
|---:|---|---:|---:|---:|---:|
| 640 | refitted | `.120` | `1.258` | `-3.341` | `1.738` |
| 640 | fixed population | `.125` | `1.264` | `-3.331` | `1.744` |
| 2560 | refitted | `.092` | `1.127` | `-2.702` | `1.703` |
| 2560 | fixed population | `.090` | `1.127` | `-2.723` | `1.682` |

The oracle reference does not improve the skew calibration. At an independent
weak null, the population location-nuisance coefficient vanishes at first
order; the simulation now shows that removing reference estimation also leaves
the observed higher-order tail distortion essentially unchanged. The slow
convergence belongs to the skewed radius-correlation/studentization problem,
not to near-degenerate Huber reference fitting.

This cleanly separates Claim 1's finite-sample limitation from Claim 2's
mechanism.

## Claim 2: a cross-margin switching dose response

Both margins retain independent lognormal radii with zero fixed-reference
profile correlation. Only the sign construction changes. With probability
`q`, the second margin uses the first margin's sign; otherwise it receives an
independent sign. Thus `q` controls common mode-selection pressure without
creating radial concordance at the symmetry reference.

| q | Refit effect, n=80 | Refit rejection, n=80 | Refit effect, n=640 | Refit rejection, n=640 |
|---:|---:|---:|---:|---:|
| `.00` | `-.006` | `.025` | `.001` | `.018` |
| `.25` | `.047` | `.397` | `.027` | `.378` |
| `.50` | `.137` | `.687` | `.128` | `.392` |
| `.75` | `.358` | `.693` | `.302` | `.432` |
| `1.00` | `.806` | `.740` | `.626` | `.555` |

Mean fitted-centre products and mean refitted effects increase monotonically
with `q` at both sample sizes. The fixed-zero procedure remains far closer to
the null, with rejection between `.042` and `.100` across the ten cells.

The rejection curve itself need not be strictly monotone because it combines
the probability of a reference switch, effect magnitude, and unstable
studentization. The monotone centre-product and effect gradients are the
mechanism evidence. Even modest cross-margin coupling can be damaging because
the centre gap turns small sign-count perturbations into nonlocal reference
movement.

## Claim 3: prospective fifth-family prediction

A hyperexponential bridge was chosen before its rejection simulations were
run:

\[
R \sim \tfrac12\operatorname{Exp}(0.5)
       +\tfrac12\operatorname{Exp}(1.5).
\]

Its right density at zero is exactly

\[
f_R(0)=\tfrac12(0.5)+\tfrac12(1.5)=1,
\]

matching the four training bridge families, while its heavier tail supplies a
new higher-order shape. The logit model was fitted only to the original 24
cells, and its predictions were compared with six new 200-repetition cells.

| n | epsilon | conditioning index | Predicted rejection | Observed rejection |
|---:|---:|---:|---:|---:|
| 80 | `.05` | `.223` | `.566` | `.460` |
| 80 | `.10` | `.446` | `.307` | `.195` |
| 80 | `.20` | `.890` | `.131` | `.075` |
| 320 | `.05` | `.447` | `.307` | `.210` |
| 320 | `.10` | `.892` | `.131` | `.050` |
| 320 | `.20` | `1.780` | `.049` | `.030` |

The index correctly predicts the coarse recovery order across conditioning
levels. Two nearly duplicate index values (`.446/.447`) have observed rates
`.195/.210`, so the six cells are not strictly pointwise monotone; their Wilson
intervals overlap widely. Relative to the old-family intercept-only baseline,
MAE improves by `47.6%` and log loss by `14.5%`. This is prospective support
for gross first-order organization, not exact ordering of near-tied cells.

However, every prediction is too high, with absolute errors `.019--.112`.
This systematic miss is equally important: the conditioning index transports
the ordering better than the level. The fifth family therefore strengthens
Claim 3 and the higher-order-family limitation at the same time.

## Refined separation of claims

- **Claim 1:** regular IID pointwise theory can converge slowly for skewed
  radius correlation even with the population reference fixed.
- **Claim 2:** centre-gap reference fitting creates a separate failure when
  mode-selection perturbations are coupled across margins.
- **Claim 3:** the nuisance index transports the coarse recovery order to a new
  matched-density family, but family shape changes the rejection level beyond
  first order.

No universal conditioning cutoff, uniform finite-sample theorem, or complete
family-invariant transition law follows from these results.
