# Skew Mixed Paths: Huber Location and MAD Derivatives

> **Retrospective clarification (2026-08-11):** the `moderate_skew` and
> `strong_skew` names below identify composite generators. A later 2x2 audit
> found that their early power crossover was driven mainly by positive-sign
> prevalence and its change to node geometry, not by marginal skewness alone.
> The Huber/MAD derivative validation is unchanged. See
> `docs/skew_mechanism_factorial_20260811.md`.

## Scope

The symmetric mixed-path calculation set the population Huber location and its
path derivative to zero. This note removes that simplification. It derives the
median, MAD, and Huber-location derivatives under a smooth mixture-weight path,
propagates them through profile correlation and `c_delta_star`, and validates
the result against complete population refitting and finite-sample permutation
power.

The result is specific to continuous interior mixture paths. It does not claim
differentiability at weights `0` or `1`, at density zeros, at tied quantiles, or
when probability mass lies on a Huber knot.

## 1. Transport path

As before,

\[
X_w=\sqrt{1-w}N_X+\sqrt wD_X,
\qquad
V_X=\dot X_w=-\frac{N_X}{2\sqrt{1-w}}
                 +\frac{D_X}{2\sqrt w}.
\]

For a continuously transported margin, define the boundary velocity

\[
v_w(x)=E(V_X\mid X_w=x).
\]

The continuity equation gives

\[
\partial_w F_w(x)=-f_w(x)v_w(x).
\]

This conditional average is essential. The velocity of the single observation
occupying the empirical median order is an exact fixed-sample derivative, but
it is not a consistent population estimate when `V` remains random given `X`.
The first implementation exposed this distinction and was therefore replaced
by boundary kernel regression for the population calculation.

## 2. Median and MAD derivatives

Let `m(w)` be the median. Differentiating `F_w(m)=1/2` gives

\[
\boxed{\dot m=v_w(m)}.
\]

Let `d(w)` be the unscaled MAD, with upper and lower boundaries
`u=m+d` and `l=m-d`. Differentiating

\[
F_w(m+d)-F_w(m-d)=\frac12
\]

gives

\[
\boxed{
\dot d=
\frac{f(u)\{v(u)-\dot m\}-f(l)\{v(l)-\dot m\}}
     {f(u)+f(l)}
}.
\]

For the normal-consistent MAD scale `s=k d`,

\[
\dot s=k\dot d,qquad k=1.4826.
\]

The formulas correctly reduce to `dot m=c` and `dot d=0` under a pure
translation velocity `V=c`; this was added as a unit test.

## 3. Huber-location derivative

Let

\[
U=\frac{X_w-T(w)}{s(w)},qquad
E\{\psi_c(U)\}=0,qquad c=1.345,
\]

and define

\[
A=E\{\psi'_c(U)\},qquad
B=E\{U\psi'_c(U)\}.
\]

Implicit differentiation along the transport path gives

\[
\boxed{
\dot T=
\frac{E\{\psi'_c(U)V_X\}}{A}
-\frac{B}{A}\dot s
}.
\]

The first term is the direct movement of observations through the Huber
equation. The second is the MAD-to-Huber indirect path. Under symmetry `B=0`;
under skewness it generally remains nonzero.

This formula differs from the earlier contamination influence function. The
contamination path has a direct point-mass score `s psi/A`; the current smooth
transport path has `E(psi' V)/A`.

## 4. Effect derivatives

For raw profile radii

\[
R_X=|X_w-T_X(w)|,qquad
\dot R_X=\operatorname{sgn}(X_w-T_X)(V_X-\dot T_X),
\]

and analogously for `Y`. Marginal MAD division cancels exactly from both
profile Pearson correlation and the ratio

\[
C(w)=\frac{E(R_XR_Y)}{E(R_X)E(R_Y)}.
\]

MAD nevertheless affects both statistics indirectly through `dot T`. The
correlation derivative uses the covariance/variance formula from the symmetric
study. For `C`,

\[
\dot C=
\frac{\dot\nu}{\mu_X\mu_Y}
-C\left(\frac{\dot\mu_X}{\mu_X}
        +\frac{\dot\mu_Y}{\mu_Y}\right),
\]

where `mu_X=E(R_X)`, `mu_Y=E(R_Y)`, and `nu=E(R_XR_Y)`.

Mantel uses

\[
R^M_X=|X_w-X'_w|,qquad
\dot R^M_X=\operatorname{sgn}(X_w-X'_w)(V_X-V'_X),
\]

and has no Huber/MAD nuisance path.

## 5. Skew generators

Both configurations retain node-radius correlation `.55` and latent dyadic
correlation `.70` at weight `.216`.

- **Moderate skew:** positive node signs with probability `.70`, node
  log-radius sigma `.55`, and lognormal dyadic sigma `.55`.
- **Strong skew:** positive node signs with probability `.80`, node
  log-radius sigma `.70`, and lognormal dyadic sigma `.80`.

Components are population-standardized before mixing. The finite-building
power experiment additionally standardizes each component within each block,
then applies the existing four-building scale pattern and within-building
permutations.

## 6. Three-level derivative validation

### 6.1 Formula and implementation checks

Unit tests verified:

1. exact fixed-sample order-statistic derivatives;
2. the Huber implicit derivative against complete location refitting;
3. the pure-translation identities;
4. profile, `c_delta_star`, and Mantel derivatives against complete refitting.

### 6.2 Independent population runs

Two independent seeds used ten batches of 100,000 observations per skew
configuration. Boundary velocities used Gaussian kernel regression. Across
`epsilon=.0002,.0005,.001`, the complete-refit discrepancies were small and
stable, but finite-difference quantile noise remained visible.

Bandwidth multipliers `.75,1,1.25` and batch sizes 100,000 and 400,000 retained
all substantive slope directions. The largest sensitivity-table discrepancy
was `.00376` in one six-batch moderate-skew row. This was not hidden: it
motivated the higher-precision check below.

### 6.3 High-precision independent check

The final check used eight batches of 500,000 observations for each skew
configuration. At `epsilon=.0005`:

| configuration | method | full derivative | complete refit | difference |
| --- | --- | ---: | ---: | ---: |
| moderate | profile correlation | -.135824 | -.135761 | .000063 |
| moderate | `c_delta_star` | -.065890 | -.065878 | .000012 |
| moderate | Mantel | .070069 | .070070 | .000001 |
| strong | profile correlation | .053018 | .053078 | .000060 |
| strong | `c_delta_star` | -.001617 | -.001553 | .000063 |
| strong | Mantel | .094310 | .094306 | -.000004 |

The same agreement held at `epsilon=.001`; the largest absolute mean error
among the profile and `c_delta_star` rows was `.000217`, below its Monte Carlo
SE. The smaller `.0002` step was noisier for quantile refits and is retained as
a sensitivity result rather than the preferred validation step.

## 7. Nuisance-path decomposition

At high precision:

| configuration | effect | fixed-location slope | full slope | MAD indirect component | total location component |
| --- | --- | ---: | ---: | ---: | ---: |
| moderate | profile correlation | -.21262 | -.13582 | .00388 | .07679 |
| moderate | `c_delta_star` | -.10406 | -.06589 | .00193 | .03817 |
| strong | profile correlation | -.02865 | .05302 | .00162 | .08167 |
| strong | `c_delta_star` | -.10020 | -.00162 | .00196 | .09858 |

The MAD indirect contribution is reproducible and nonzero, but it is not the
main driver. Direct movement of the Huber location is much larger. Under strong
skewness it reverses the profile-correlation slope from negative to positive.

The raw `c_delta_star` slope does not follow profile correlation: in the strong
skew case it is almost zero while profile correlation is clearly positive.
This is another consequence of the `CV_X CV_Y` weighting and reinforces the
recommendation to report profile Pearson as the direct concordance effect.

## 8. Finite-sample permutation power

A 300-dataset coarse grid was followed by two independent 800-dataset local
runs. Strong skew required two further independent 800-dataset low-weight
extensions rather than extrapolation.

| configuration | crossover | zero-difference band |
| --- | ---: | ---: |
| moderate skew | .131 | .100-.150 |
| strong skew | .043 | .000-.075 |

Near these crossovers, finite-difference slopes of profile power minus Mantel
power were approximately `-.413` and `-.350`, respectively. Profile/
`c_delta_star` and profile-Pearson permutation p-values were identical in all
72 simulated grid rows.

These composite configurations move crossover substantially earlier than the
symmetric default value near `.216`, especially in the configuration named
`strong_skew`. The later mechanism audit shows that this is mainly a node
sign-prevalence/geometry effect rather than a general monotone effect of
skewness. It does not reverse the local decline in profile's relative power
advantage within these generators.

## 9. Conclusions

- The Huber and MAD nuisance paths can be restored coherently on skew mixed
  paths and agree with complete refitting at high precision.
- Ignoring all Huber-location movement is unsafe under skewness and can reverse
  the sign of a profile derivative.
- Ignoring only the MAD indirect term causes a smaller but systematic error;
  it is most consequential when the full `c_delta_star` derivative is near
  zero.
- Individual effect curves need not share the symmetric-path direction.
  Moderate skew gives a declining profile effect and rising Mantel effect;
  strong skew gives both effects rising, with Mantel rising faster.
- The robust conclusion is relative: profile's advantage decreases as dyadic
  mixture weight increases in all tested symmetric and skew paths.
- Crossover values remain generator-specific and cannot be used for post-hoc
  method selection.

## Reproducible files

- `scripts/run_skew_mixed_path_derivatives_20260810.py`
- `tests/test_skew_mixed_path_derivatives_20260810.py`
- `results/skew_mixed_path_derivatives_combined_20260810.tsv`
- `results/skew_mixed_path_derivative_sensitivity_20260810.tsv`
- `results/skew_mixed_path_derivatives_high_precision_20260810.tsv`
- `results/skew_mixed_path_power_combined_20260810.tsv`
- `results/skew_mixed_path_power_crossovers_20260810.tsv`
