# Pareto (2024): full-text formula comparison and citation decision

Source: Adriano Pareto, *On a correlation coefficient based on the L1-norm*,
Statistical Papers 65, 5851–5871. DOI: 10.1007/s00362-024-01616-3.
The supplied 22-page PDF contains the complete 21-page article and a rights
page. Its hash is recorded in `results/pareto_formula_check_20260918.json`.
Formula pages 5853–5855 and example page 5862 were checked visually as well
as in extracted text. The full article, including conclusions, was read.
The publisher page was checked on September 18, 2026:
https://link.springer.com/article/10.1007/s00362-024-01616-3

## Formula, not a title-based identification

Write h for the regression slope (the article uses m; here m remains the
project's marginal median), and define

    p(h) = median_i(y_i - h x_i),
    A(h) = sum_i |y_i - h x_i - p(h)|,
    q(h) = A(h)/A(-h).

Equations (5)–(8), pp.5854–5855, optimize this ratio over slopes. For an
appropriate minimizing slope h*, the signed absolute-ratio coefficient is
1-q(h*) for h* >= 0 and q(h*)-1 for h* < 0. The corresponding lines are
the best-fitting median line and the opposite-slope counterline. Equation
(2), p.5853, is the equivalent piecewise SAE-positive/SAE-negative definition.
This is a joint regression optimization. It is **not** a Pearson correlation
of two separately fitted marginal radii, and its numerator is not E(ab).

The article's Table 1 data and reported optimum h*=1.5 give p(h*)=-0.5,
p(-h*)=8.5, A(h*)=7.25 and A(-h*)=23.25. Hence r'=0.6881720430,
matching the printed 0.69. A finite candidate-slope calculation verifies this
example only; it is not a general implementation or certification of the
paper's optimization algorithm. The deterministic audit is reproducible with
`scripts/check_pareto_formulas_20260918.py`.

## A decisive target distinction

Pareto's affine transformation property changes the coefficient's sign when
one margin is reflected (pp.5856–5858). Our equivariant reference distances
are invariant to a reflection of either margin. For nonconstant symmetric X
with nonconstant |X| and Y=-X, the reference locations are zero: Pareto's
coefficient is -1, whereas rho_P=1. A five-point symmetric sample checks the
same algebra. This endpoint example separates definitions; it is outside the
positive target-IF-variance assumptions for our Wald theorem.

| Question | Pareto (2024) | Present paper |
|---|---|---|
| Target | Signed relationship summarized by opposing median regression lines | Association of paired distances to marginal robust references |
| Fitting | Joint slope and residual-median intercepts | Two marginal median/MAD/Huber references, then paired moments |
| Main technical contribution | Coefficient properties, computational algorithm, illustrative robustness comparisons | Complete generated-reference IF and pointwise inference; worked finite-sample failure |
| Finite-sample evidence | Means, SEs and RMSEs; selected contamination comparisons (§4) | Null rejection, CI coverage, fitted-reference pathways, bounded conditioning evidence |
| Inferential connection | No matching full IF/Wald theorem is supplied for our target | Requires our own quantile/Z-estimation and empirical-process verification |

Its discussion of symmetry in §2.3(4) explicitly uses reflection of one
coordinate, not merely joint central symmetry. Do not import the latter
interpretation into the shared-sign model. Its numerical SE summaries do not
constitute validated plug-in confidence intervals for our estimator.

## Value and limits

**Retain a concise citation and formula-level distinction in Section 2.**
It is directly relevant adjacent work because it constructs correlation from
absolute deviations, but answers a different scientific question. This closes
the earlier full-text access/formula-comparison obligation. It does not make
the paper a missing foundation for our theorem, nor justify adding a new
head-to-head simulation against methods with different estimands.

Useful lessons are to state the target before comparing methods, distinguish
coefficient construction from its numerical computation, and give exact
invariance properties. These sharpen exposition without changing our method.
Do not transfer the article's selected contamination advantages to uncapped
profile correlation, which remains a robust reference rather than a globally
robust correlation. Do not borrow its cross-country application as evidence
that our paired-IID design requirements have been met.

The publisher displayed 3 citations on this visit; the user's count of 1 can
reflect another database or update date. Neither number measures whether the
formula is the closest prior construction. Recent publication does not by
itself justify a citation, and low citation count does not justify omission.
No citation quota, universal superiority claim, or new simulation is needed.

The planned addition is outside the Introduction awaiting Hoorn. The source
PDF is not copied into the repository or the external proof-review package.
