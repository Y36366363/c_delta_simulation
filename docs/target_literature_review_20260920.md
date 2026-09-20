# Target distinctions and focused literature decisions — 2026-09-20

These are targeted source checks, not an exhaustive novelty search or an
independent proof review. The draft Introduction awaiting Hoorn is untouched.

## Corrected comparison table

All zero statements below concern population quantities under the corresponding
existence/nondegeneracy assumptions, not a sample test result. For Spearman,
use continuous margins; tied-data extensions need their stated conventions.

| Measure | Target | Reflect one margin | Meaning of zero | Estimated ingredients |
|---|---|---|---|---|
| Pearson | Signed standardized covariance | Sign reverses | Cov(X,Y)=0 | Marginal means and variances |
| Spearman | Corr(F_X(X),F_Y(Y)) | Sign reverses | Zero rank covariance | Empirical ranks / marginal CDFs |
| Distance correlation | General dependence | Invariant | Independence, for Euclidean variables with finite first moments | Double-centered pairwise distances |
| Pareto L1 | Signed fit relative to opposite-slope median line | Sign reverses for the corresponding selection | Equal optimal opposite-line absolute-error sums | Joint slope and residual-median intercepts |
| rho_P | Association of distances to robust marginal references | Invariant | Zero covariance of the two radii | Median/MAD/Huber references and paired moments |

The proposed 'reference estimated: no' for Pearson is misleading: means are
estimated. Pairwise distance centering is not a marginal robust-reference
fit. The revised last column identifies the ingredients without pretending
that all methods have the same nuisance problem. A zero Pearson, Spearman,
Pareto or profile coefficient does not generally imply independence.

## Source-specific decisions

**Devlin, Gnanadesikan and Kettenring (1975).** *Robust estimation and outlier
detection with correlation coefficients*, Biometrika 62(3), 531–545,
DOI 10.1093/biomet/62.3.531. Publisher metadata and abstract verified. They
study robust correlation construction, influential observations and Monte
Carlo comparisons. Useful historical context in one citation; no detailed
formula or theorem is claimed from an inaccessible full text.
https://academic.oup.com/biomet/article-abstract/62/3/531/256768

**Croux and Dehon (2010).** *Influence functions of the Spearman and Kendall
correlation measures*, Statistical Methods & Applications 19, 497–515,
DOI 10.1007/s10260-010-0142-z. Publisher abstract/publication details and
institutional discussion-paper full text inspected. Equation (2) defines the
raw Spearman target Corr(F(X),G(Y)); equation (3) separately calibrates it to
the Gaussian Pearson parameter. This directly supports target separation.
Their IF/gross-error-sensitivity analysis is pertinent prior work; it does
not supply the generated median/MAD/Huber-profile IF developed here.
https://link.springer.com/article/10.1007/s10260-010-0142-z
https://repository.tilburguniversity.edu/bitstreams/2cd1fe38-9ef0-4c22-89c5-f89af23d6de2/download

**Rousseeuw and Croux (1993).** *Alternatives to the Median Absolute
Deviation*, JASA 88(424), 1273–1283, DOI 10.1080/01621459.1993.10476408.
The author-hosted scanned PDF's first two pages were visually read. Page
1273 gives the normal calibration 1.4826 and midpoint convention. Pages
1273–1274 discuss efficiency and MAD's symmetric treatment of dispersion.
This supports interpreting MAD as a defined reference scale under asymmetry,
not a universal SD estimate. It does not say MAD is unusable for skewed laws,
nor justify replacing it with S_n/Q_n without changing our nuisance analysis.
https://wis.kuleuven.be/statdatascience/robust/papers/publications-1993/rousseeuwcroux-alternativestomedianad-jasa-1993.pdf

**Leyder, Raymaekers and Rousseeuw (2026; online 2025).** *Robust Distance
Covariance*, International Statistical Review 94(1), 1–25,
DOI 10.1111/insr.70005. Publisher full text and April 2026 issue verified.
Their usual-distance-covariance result distinguishes bounded influence from
zero breakdown and unbounded finite-sample sensitivity. This is a directly
relevant recent reminder that robustness claims require a specified criterion.
Their transformation-based dependence method answers a different question
from reference-radius correlation. Cite this connection briefly; do not import
their robustness or independence-testing conclusions to our statistic.
https://onlinelibrary.wiley.com/doi/full/10.1111/insr.70005
https://onlinelibrary.wiley.com/toc/17515823/2026/94/1

**Székely, Rizzo and Bakirov (2007).** *Measuring and testing dependence by
correlation of distances*, Annals of Statistics 35(6), 2769–2794,
DOI 10.1214/009053607000000505. The authors' archived abstract and the
definitions/finite-first-moment qualification in the Leyder et al. primary
article support the distance-correlation row. This independence target differs
from a zero unsigned-radius covariance.
https://arxiv.org/abs/0803.4101

Pareto (2024) was already checked against full text on September 18; use
`docs/pareto_formula_comparison_20260918.md`, not a new title-based inference.

## Proposed integration

Replace or condense existing target-comparison prose with the small table,
retaining one Pareto formula cross-reference if desired. Add at most one short
paragraph relating existing robust correlation and rank IF work to this target,
one sentence on MAD calibration, and one recent robustness distinction.
Do not append an independent literature-review section or duplicate Hoorn's
Introduction. Publication years follow the final issue year where verified;
Leyder et al. is therefore cited as 2026, noting its 2025 online publication
only where useful. These citation choices are based on direct relevance.
