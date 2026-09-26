# Focused review, provenance correction and target positioning

Date: 2026-09-25. Current baseline: author draft of September 21 and commit
d4ae9c6. The user authorized local revision and supporting tests while Hoorn
reviews the draft. No new Monte Carlo design was introduced, and no push is
authorized or performed. Mathematical comments below are internal AI-assisted checks,
not independent mathematical peer review.

## Findings that justify a local revision

1. **A closer target antecedent was missing.** Afuecheta, Nadarajah and Chan
   (2023), *Folded Bivariate Distributions as Models for Magnitude Correlation*,
   REVSTAT 21(1),21–38, explicitly defines Corr(|X|,|Y|) on p.22; Eq.(2.1)
   gives the folded density. For fixed references, our coefficient is magnitude
   correlation of centered variables. The manuscript now acknowledges this
   directly. The contribution concerns estimated robust references, full
   inference and finite-sample mechanisms, not the absolute-value operation.
   Its parametric fitting/applications do not supply our theorem or an IID
   design justification. Source: https://revstat.ine.pt/index.php/REVSTAT/article/view/395

2. **Lancaster correlation is a useful recent comparator.** Holzmann and Klar
   (2025; online 2024), Scandinavian Journal of Statistics 52(1), 145–169,
   DOI 10.1111/sjos.12733. Equations (4), (6) distinguish normal-score and linear
   versions; the latter combines absolute raw correlation with absolute
   correlation of standardized squares. It has a different target and its
   own moment-based inference. We add one formula comparison, not a power
   competition under different nulls. Published author-hosted source:
   https://publikationen.bibliothek.kit.edu/1000172416/153641019

3. **S1.3 should retain exact equality pieces.** The original 'affine transform
   of half-line indicator, probability-zero boundary' shorthand was insufficient
   for a data-selected boundary. We now use sign(w−t)=1{w>t}−1{w<t}, and include
   the x=t zero piece in the weighted-sign class. The subsequent VC/entropy and
   local L2 bounds continue unchanged. No IF formula or estimator is altered.

4. **The random-bandwidth source can be more precise.** Einmahl and Mason
   (2005), Annals of Statistics 33(3), 1380–1403, DOI 10.1214/009053605000000129,
   Theorem 1/Remarks 2, 7 address bandwidth ranges and data-driven bandwidths.
   This is context for S1.5; its global assumptions do not replace our local
   Gaussian-kernel grid argument. Source: https://arxiv.org/abs/math/0507431

5. **Dependency isolation was overstated.** Historical September18,20,21
   reports explicitly record isolated_venv=false, while some prose called the
   runtime isolated. Separate source snapshots and identical NumPy/SciPy
   versions support the recorded replays, but do not prove package isolation.
   The old environment path now lacks pyvenv.cfg; its name and Python -I were
   insufficient checks. No cause or time of that filesystem change is known.
   The manuscript corrects the claim, retains original reports, and adds a
   new verified-environment replay. September12/16 reports record isolation.

6. **Record identity checks were incomplete.** The old audit accepted an
   in-memory wrong solver replication and root seed because it checked counts
   rather than the complete planned key set. The new audit joins every method
   and solver record to the exact grid, seed and truth, with negative controls.
   The existing outcomes pass; this finding does not show their corruption.

7. **Do not claim exact finite-sample studentizer reflection symmetry.** With
   an odd sample, one observed value equals the sample median. The <= median
   IF convention does not negate at equality. A deterministic 95-observation
   skewed example gives an SE difference of 9.55e-9; the derived centered IF
   correction explains it to 1.06e-14. Reference/point-estimate equivariance is
   distinct. Under regularity the correction vanishes in empirical norm, but
   no universal O_P(n^-1) SE-gap rate is asserted. The default is unchanged.

## Supporting checks and limits

The deterministic Gaussian comparison checks five parameter points by
conditional adaptive integration, with maximum formula/quadrature difference
4.44e-16. At |r|=.4, magnitude/profile correlation is .1421205, squared
correlation is .16, and linear Lancaster correlation is .4. These are target
values, not comparative quality scores. Gaussian reference derivatives vanish;
this is not an active-nuisance or calibration study. See
`results/target_comparison_20260925.json`.

The new identity audit checks 18,000 method rows, 6,000 solver rows and 12,000
exact residual inequalities. Twenty-four negative-control/property tests
cover wrong or missing identities, metadata, failure flags and affine/equality
behavior. See `results/record_identity_audit_20260925.json`.

The old runner's exception bookkeeping can leave a partial method group if a
later method fails, and an empty AssertionError message is not a robust error
encoding. We do not rewrite the already executed runner or relabel its frozen
outputs. Current complete records have no such failures; the new exact-grid
and finite-value audit rejects partial/malformed groups. Any future extended
runner should explicitly append one status row per scheduled method. There
is no planned new study requiring that implementation change now.

The current test plan replaces active exploratory-grid instructions with
manuscript checks, runtime verification, exact record identity, and a clear
separation of numerical tests from proof. The old plan remains verbatim in
an inactive historical section.

## Environment replay and remaining obligations

The new replay uses a fresh venv with system-site packages disabled, distinct
prefix/base_prefix, no user site, and NumPy/SciPy loaded from that venv.
Runtime probes are preserved before and after execution. The first strict
bitwise comparison found tiny floating differences; this is reported, not
silently called exact. The follow-up uses the existing scaled tolerance 1e-10
for numerical fields while requiring record IDs, seeds, decisions, errors and
exact rational residual fields to agree exactly. Original files are untouched.
The result and actual maxima are in
`results/environment_reproduction_20260925.json`.

All 6,000 distinct scheduled datasets were replayed, producing 18,000 method
records and 6,000 solver records without errors. The first completed execution
and the final execution total 12,000 dataset executions; this is not 12,000
independent datasets. Three of six tables match exactly; the other three have
maximum scaled difference 6.661338147750939e-16 and maximum absolute difference
8.881784197001252e-16. IDs, seeds, all 18,000 coverage decisions, 6,000 solver
decision-change flags, 24,000 exact-fraction integers and 12,000 residual-pass
flags match exactly. All 292 pre-existing TSV files remain unchanged. The
two new executions agree exactly with each other. Python 3.12.3 is recorded;
the wrapper guards NumPy/SciPy versions and isolation, not the Python patch
version. No calibration outcome has improved through this reproduction.

## Completed regression and manuscript checks

- The verified environment initially lacked the additional manuscript-audit
  dependencies (Pillow and matplotlib); test collection failed before tests
  executed. After the replay's final environment probe was saved, the existing
  `requirements-manuscript-audit-lock.txt` was installed. Scientific-library
  versions stayed unchanged. The following tests use that expanded audit
  environment, not the smaller pre/post replay environment.
- Full suite: **379 passed, 18 skipped**. The 18 skips require an external
  version-specific manuscript path. Each was then run against its matching
  author source: six historical 19-table checks on September 18, six integrated
  checks on September 21, and six new checks on September 25, all passed.
  Thus **397 distinct tests passed** across the full and version-specific runs.
  Third-party matplotlib/pyparsing deprecation warnings remain; no scientific
  test failure remains.
- The manuscript audit passes 172 historical provenance checks and reconciles
  all **21 numerical tables / 1,182 cells**. Every numerical table block is
  unchanged from September 21. Introduction, main IF/theorem, Appendices A/B
  and S2 remain unchanged. S1 changes are limited to the recorded boundary,
  KDE-context and finite-sample equality qualifications.
- The new PDF remains **40 pages**; the LaTeX package compiles without final
  warnings or unresolved references. The delivery manifest records the final
  source and package hashes, visual checks and extracted-package compile.

Independent proof review remains open. Internal review found no counterexample
to the checked moving-boundary, weak-null empirical-norm, KDE, R5 ideal-root or
shared-sign arguments, but this is not a certification. The new bibliography
does not confer global novelty or finite-sample reliability. Hoorn's
Introduction, editorial placement and submission decisions remain pending.
