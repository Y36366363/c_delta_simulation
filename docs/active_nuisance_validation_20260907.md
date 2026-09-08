# Active-nuisance inference and claim refinement (2026-09-07)

## Deliverable and decision

This closes the first post-review task: exercise the full primary-estimand IF
in the **existing** skewed nonzero-effect law, independently establish its
population target, and correct the active manuscript's mechanism language.
There is no new distribution grid, permutation theorem, operational gate,
interval tuning, or application choice. The prespecified protocol is
`docs/active_nuisance_validation_protocol_20260907.md`.

**Outcome:** the complete formula and implementation receive additional
support; adequate 95% finite-sample coverage does not. This distinction must
remain visible in the paper. Software success is not calibration success.

## 1. Population truth and full nuisance verification

Reuse `(log X, log Y)` jointly normal with means zero, marginal SD .60 and
latent correlation .40, with `k=1.4826`, `c=1.345`. Analytic truncated
lognormal moments determine the MAD and Huber score. Conditional analytic
radius moments plus adaptive one-dimensional integration determine the joint
cross-moment. An independent bivariate Gaussian tensor integration is split
at the median, both MAD endpoints, the Huber clipping points, and the radius
origin. Orders 24, 48, and 72 are used **per interval**; Gaussian tails are
truncated at 12 SD. These are numerical checks, not symbolic exactness.

| Quantity | Value |
|---|---:|
| Population raw MAD | .387121537597268 |
| Population Huber location | 1.079808860961767 |
| Population rho_P | .193475118858046 |
| Reference coefficient, either margin | -.149813768489134 |
| Complete IF variance | 2.930344036192 |
| Direct-only IF variance | 2.935125447075 |
| Nuisance contribution variance | .029924671347 |
| Twice direct--nuisance covariance | -.034706082231 |
| RMS indirect MAD contribution | .035593370612 |

The last two quadrature orders agree on complete IF variance within 2e-14;
cross-moment agreement between conditional and tensor integration is within
7e-15. Both IF means are numerically centered. Four contamination directions
were checked at epsilon 1e-4, 1e-5 and 1e-6 with roots and moments recomputed.
The largest scaled derivative error at 1e-6 is 1.596e-5; every direction's
error decreases with epsilon. Reference and MAD components are nonzero.

### Correction to the old numerical benchmark

The frozen 2026-09-03 Gauss--Hermite calculation reported rho_P approximately
.193218. Its self-consistent contamination derivative check remains useful,
but does not establish integration accuracy for the continuous law. The new
target is larger by about .000257. We retain the old table and its hashes;
the new study uses the independently checked value above. Section 3.4 now
explicitly distinguishes a within-quadrature derivative check from population
integration validation. This correction is small compared with the sampling
SDs here, but should not be hidden by using approximate truth as exact truth.

### Why an active nuisance path need not yield a large variance change

Write IF_full = IF_direct + IF_nuisance. Then

\[
V_{full}=V_{direct}+V_{nuisance}
 +2\operatorname{Cov}(IF_{direct},IF_{nuisance}).
\]

Here the two added terms nearly cancel. The net change in variance is about
-0.163%; the standard-error difference at first order is about -0.0815%.
The estimated reference changes the IF, but it does not substantially change
the total variance in this particular law. This does not license dropping
the correction elsewhere, and it prevents claiming large practical
superiority from this benchmark.

## 2. Prespecified Monte Carlo results

Root seed `2026090701`; PCG64 with separate SeedSequence `[root,n,rep]` for each
replication. Sizes 160,640,2560; 2,000 replications each. Complete KDE plug-in
uses the public API and its sample-variance correction. The direct-only
ablation uses the same fitted profile estimate. The oracle fixes both true
Huber references and has its own direct-profile estimator/SE. There are
6,000 IID datasets, 18,000 method records, and **zero failed fits**.

| n | Full coverage (95% Wilson) | Direct-only coverage | Oracle coverage | Full SE/SD | Full bias (MCSE) |
|---|---|---|---|---|---|
| 160 | .8580 [.8420,.8726] | .8535 | .8485 | .8397 | -.007823 (.002778) |
| 640 | .9115 [.8983,.9232] | .9110 | .9050 | .8999 | -.002474 (.001495) |
| 2560 | .9270 [.9148,.9376] | .9265 | .9290 | .9664 | -.000827 (.000746) |

Full mean interval widths: .40899, .23580, .12645. Full studentized SDs:
1.33756, 1.15613, 1.05727. Its 2.5%/97.5% studentized quantiles are
(-3.2784,2.0503), (-2.5976,1.8839), and (-2.3440,1.6654). A scalar variance
comparison alone therefore misses the asymmetric tails.

Paired full-minus-direct coverage differences are .0045 (MCSE .001800),
.0005 (.000500), and .0005 (.000866). At n=160 this is a modest improvement,
not a recovery to .95; at the two larger sizes the practical difference is
very small. The point estimates agree to below 6e-16, as intended.

All three full-coverage Wilson intervals exclude .95. Larger samples improve
performance but do not establish a safe sample-size threshold. The oracle
also undercovers, so a substantial part of the problem persists without
generated-reference estimation. These observations are consistent with slow
skewed-profile/self-normalized convergence, not a proof of a full higher-order
error decomposition. Do not infer that a density change or HC factor will
repair it without a separate justified study.

## 3. Mechanism and claim corrections

### Claim 2: identify the unstable subsystem correctly

In the earlier signed-lognormal construction X=S exp(tau U), tau>0,
the median and Huber location are zero and the raw MAD is one. The median is
unique but has density zero at its root. Thus the full regular theorem does
not apply. At tau=.10 the population Huber slope is instead

\[
-\Phi\{\log(ck)/\tau\}/k\approx-.67449,
\]

which is not nearly flat. Analytic truncated moments and numerical score
differences verify this. The correct interpretation is nonregular median
fitting and nonlocal sample MAD changes propagating through the fitted scale
to the empirical Huber reference. At symmetry the first-order scale coupling
B is zero; the explanation is explicitly nonlocal, not a nonzero regular
first-order MAD derivative. Existing refit/fixed and balance interventions
remain intact, but do not prove a full stochastic switching law.

With fixed offsets tx,ty and independent radii exceeding their magnitudes,

\[
|SR_X-t_X|=R_X-St_X,\qquad
\operatorname{Corr}(R_X-St_X,R_Y-St_Y)
=\frac{t_Xt_Y}{\sqrt{(v_X+t_X^2)(v_Y+t_Y^2)}}.
\]

An exact finite product-law check verifies this identity. It is conditional
on imposed offsets; it does not establish their fitted selection probability.
At an exact binary zero-reference law the radii are constant and rho_P is
undefined. The continuous positive-spread example supplies the nondegenerate
target, not this binary boundary.

### Claim 1: independence is not necessary for orthogonality

The shared-sign, independent-radius null has E(S)=E(SR_X)=E(SR_Y)=0,
so the reference coefficients cancel despite dependence of X,Y. An algebraic
check verifies this, explaining why the main symmetric dependent null does
not itself exercise the complete nuisance contribution. Appendix A now
records this qualification without treating the nonregular signed-lognormal
law as an application of the regular theorem.

### Claim 3: a scalar index does not match the full first-order law

Equal J need not give equal score covariance Omega or target projection.
Local nuisance covariance contains J^{-1} Omega J^{-T}/n. Thus an
unexplained-by-I_n family residual is not automatically a proved higher-order
effect. Curvature and switching remain plausible contributors; a decomposition
has not been identified. The index also depends on the declared equation
normalization despite its invariance to positive changes of data units.

The primary-source authorship of *Detecting Identification Failure in Moment
Condition Models* was rechecked against
[arXiv:1907.13093](https://arxiv.org/abs/1907.13093) on 2026-09-07. The author
is Jean-Jacques Forneron; the prior Andrews--Mikusheva attribution in the
active manuscript and novelty note has been corrected. The precedent concerns
identification analysis, not a theorem validating this project's scalar gate.

## 4. What is now ready, and what is not

- Ready to integrate: accurate continuous-law target, active-nuisance IF
  verification, covariance decomposition, honest coverage table, refined
  Claim 2/3 language, and reproducible source/output hashes.
- Not established: practical nominal Wald coverage for this law at the tested
  sizes, a general advantage over classical/direct-profile methods, a
  switching-probability theorem, uniform inference, or a purely higher-order
  family-residual explanation.
- Next safe task: integrate these bounded findings into the Discussion and
  limitations, then obtain independent mathematical review of the full proof.
  If Professor Hoorn wants a practically calibrated interval as a headline
  method, that is a separate scoped inference-development decision; do not
  keep trying corrections until this table looks favorable.

Application choice, a conditional weak-null permutation CLT, stronger
local-to-degeneracy theory, and a sample operational diagnostic remain subject
to supervisor scope decisions. No email or LaTeX attachment has been stored
in the project.

## 5. Reproduction

```bash
/opt/anaconda3/bin/python scripts/validate_active_nuisance_20260907.py
/opt/anaconda3/bin/python scripts/validate_active_nuisance_20260907.py --summarize-only
/opt/anaconda3/bin/python -m pytest -q
```

The first command regenerates the prespecified study. The second recomputes
tables from retained replications without new simulation. Population,
derivative, mechanism-scope, paired-comparison, and replication tables all
have the prefix `results/active_nuisance_` and suffix `_20260907.tsv`.
The manifest hashes LF-normalized text and records software versions and
the source base commit. Original canonical simulation sources remain frozen.
