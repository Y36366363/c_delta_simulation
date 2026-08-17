# Complete median/MAD/Huber nuisance Jacobian

## Estimating system

For one marginal distribution, define

\[
m=\operatorname{Med}(X),\qquad
d=\operatorname{Med}|X-m|,\qquad
s=k d,\quad k=1.4826,
\]

and let the Huber centre `T` solve

\[
E\left[\psi_c\left(\frac{X-T}{s}\right)\right]=0,
\qquad c=1.345.
\]

The three population estimating equations are

\[
\begin{aligned}
G_1(m)&=F(m)-\frac12,\\
G_2(m,d)&=F(m+d)-F(m-d)-\frac12,\\
G_3(d,T)&=E\left[\psi_c\left(\frac{X-T}{kd}\right)\right].
\end{aligned}
\]

Write

\[
f_0=f(m),\quad f_-=f(m-d),\quad f_+=f(m+d),
\]

and, with `U=(X-T)/s`, define

\[
A=P(|U|<c),\qquad B=E\{U\mathbf 1(|U|<c)\}.
\]

Using nuisance perturbations measured in units of the population MAD, the
dimensionless Jacobian is

\[
\boxed{
J=
\begin{pmatrix}
d f_0 & 0 & 0\\
d(f_+-f_-) & d(f_++f_-) & 0\\
0 & -B & -A/k
\end{pmatrix}.
}
\]

This matrix simultaneously contains centre identification, both MAD boundary
densities, MAD asymmetry, Huber score curvature, and the MAD-to-Huber scale
coupling.  It was computed by analytic density/CDF formulas plus adaptive
quadrature.  A central finite-difference calculation of the complete estimating
system independently reproduced every entry; the largest error over all 13
distributions was below `5e-6`.

## Matched symmetric bridge families

For the four symmetric bridge families, `m=T=0`, `f_+=f_-`, and `B=0`.
The Jacobian is therefore diagonal at first order.  Population results were:

| epsilon | d*f(0) range | d*(f_-+f_+) range | A/k range | condition-number range |
| ---: | ---: | ---: | ---: | ---: |
| .05 | .02484-.02496 | 3.808-3.832 | .6699-.6745 | 152.6-154.3 |
| .10 | .04933-.04982 | 3.625-3.656 | .6652-.6745 | 72.8-74.1 |
| .20 | .09705-.09919 | 3.234-3.255 | .6558-.6745 | 32.8-33.4 |

The minimum singular value is the centre-density entry `d*f(0)` in every
matched bridge model.  The natural sample-size identification index is thus

\[
I_n=\sqrt n\,\sigma_{\min}(J)
   \simeq \sqrt n\,d f(0),
\]

which is the Jacobian version of the earlier `n*epsilon^2` scaling.

| design pair | I_n range | earlier rejection range |
| --- | ---: | ---: |
| `n=80, epsilon=.05` | .222-.223 | .500-.567 |
| `n=80, epsilon=.10` | .441-.446 | .293-.407 |
| `n=320, epsilon=.05` | .444-.446 | .233-.380 |
| `n=80, epsilon=.20` | .868-.887 | .107-.153 |
| `n=320, epsilon=.10` | .882-.891 | .060-.147 |
| `n=320, epsilon=.20` | 1.736-1.774 | .027-.053 |

Pairs with nearly equal `I_n` have overlapping rejection ranges even when
`n` and `epsilon` differ.  Nominal behavior in the current grid appears only
once `I_n` is comfortably above one, but `1` is not proposed as a formal
universal threshold.

Across all 24 matched-family cells, smaller `I_n` had risk-oriented Spearman
correlation `.971` with rejection (`p=3.3e-15`).  A logit model using only
`log(I_n)` reached R-squared `.932`.  Adding the MAD endpoint-density sum and
Huber curvature raised this only to `.938`.

The complete first-order Jacobians are almost identical across families at
fixed `epsilon`, whereas the targeted `n=320, epsilon=.05` confirmation still
found rejection `.232-.356`.  The residual family effect is therefore not a
missing first-order nuisance derivative.  It is a higher-order/nonlocal effect
of the finite-sample median/MAD selection and the distribution of clipped
scores.

## Why the MAD endpoint density cannot be read separately

In these tight two-mode models, `d(f_-+f_+)` is large because the MAD
boundaries lie inside dense modes.  It decreases as the centre bridge becomes
stronger, even while inference improves.  Consequently, treating a larger
MAD endpoint-density sum as automatically safer gives the wrong ordering.
The Jacobian must be evaluated jointly: the weak centre-density direction is
the binding singular direction here.

Likewise, `B=0` under symmetry, so the MAD-to-Huber indirect derivative
vanishes at the regular population solution.  The empirical MAD collapse seen
in simulations is a nonlocal switch between modes, not a small first-order
perturbation around that solution.  This explains why adding a first-order
bootstrap MAD-spread term did not repair the diagnostic gate.

## Skew benchmark

For a lognormal margin with log-SD `1.1`, the numerical solution was

\[
m=1,quad d=.6435,quad T=1.2320,quad A=.7991,quad B=-.2702.
\]

Its dimensionless Jacobian was

\[
J_{\mathrm{skew}}\approx
\begin{pmatrix}
.2334 & 0 & 0\\
-.2935 & .5500 & 0\\
0 & .2702 & -.5390
\end{pmatrix}.
\]

Thus skewness restores both mechanisms that vanish in the bridge models:
unequal MAD endpoint densities and a nonzero MAD-to-Huber scale path.  The
condition number was `3.74`, and `I_80=1.74`, consistent with the earlier
well-calibrated strong-skew external tests despite visible nuisance coupling.

## Current theoretical conclusion

1. The full Jacobian confirms that `sqrt(n)*d*f(m)`, not raw centre density
   alone, is the binding first-order identification scale on the symmetric
   bridge path.
2. MAD endpoint density and Huber curvature remain necessary regularity
   components, especially under skewness, but are not independently monotone
   risk scores.
3. A small singular value provides a coherent joint warning, but a universal
   cutoff is not established and cannot conditionally validate selected
   p-values.
4. The residual matched-family difference lies beyond the first-order
   functional delta method.  The next safe theoretical step is to compare the
   second moments and tail shape of the complete nuisance influence vector,
   followed by a second-order remainder check; no change to the statistic is
   currently justified.

## Reproducible artifacts

- `scripts/run_nuisance_jacobian_20260817.py`
- `scripts/summarize_nuisance_jacobian_20260817.py`
- `results/nuisance_jacobian_population_20260817.tsv`
- `results/nuisance_jacobian_joined_cells_20260817.tsv`
- `results/nuisance_jacobian_diagnostic_associations_20260817.tsv`
- `results/nuisance_jacobian_models_20260817.tsv`

