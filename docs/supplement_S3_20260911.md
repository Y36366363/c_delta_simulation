# Supplement S3. Designs, studentizers, numerical diagnostics and sources

This supplement supplies the reproducibility material behind Section 6.
No fresh Monte Carlo cells were generated for this integration. A bounded
deterministic replay of 2,000 existing September 9 datasets is used only to
recover marginal profile CVs at stored references; S3.5 reports its checks.
Numerical summaries below are generated from existing result files, rather
than manually transcribed into independent tables.

## S3.1 Main generating laws and random-number mapping

All main studies use independent units, one intact X/Y pair per unit.
Within-pair dependence is specified explicitly. The population effects are
the uncapped robust-reference effects in Section 2.

1. **Normal-margin shared-sign null:** independently generate a Rademacher
   sign S and U,V standard normal; set X=S|U| and Y=S|V|. Both margins are
   standard normal; the raw pair is dependent and population radii are
   independent. n=160,640, 1,000 datasets each.
2. **Independent t5 null:** X,Y are independent standard t distributions with
   five degrees of freedom. n=320,640, 1,000 datasets each.
3. **Independent strong-skew null:** X=exp(1.1U), U standard normal, and
   independent Y is Gamma(shape=.7, scale=1). n=640,2560, 1,000 datasets each.
   These first three laws have rho=0 and use the complete IF Wald test.
4. **Nonzero correlated lognormal:** independently across units generate
   (log X,log Y) centered bivariate normal with marginal SD .6 and correlation
   .4. n=160,640,2560, 2,000 paired datasets each, root seed 2026090701.
   Each replication uses PCG64 with SeedSequence([root,n,rep]), rep=0,...,1999.
   Full, direct-only and population-reference oracle methods share the draw.
5. **Four-stage shared-sign:** X=S exp(tau U), Y=S exp(tau V), with independent
   standard U,V and independent common symmetric S. tau=.10,.40 and n=80,640,
   2,000 datasets per cell. PCG64 uses SeedSequence([2026090901,round(100*tau),n,rep]).
   Within a draw the sign vector is generated first, then the X normal vector,
   then the Y normal vector. All four stages use the same pair array.

**Table S3.1. Exact cell seeds for the six regular-null cells.** The original
run uses one sequential NumPy default_rng/PCG64 stream per cell, not the
September 7 replication-level SeedSequence mapping. The seed is
`2026082301+100000*j+n`, where j=1,...,6 is the row order below.

<!-- table:wald_seeds -->
| j | Law | n | Cell seed |
| --- | --- | --- | --- |
| 1 | Normal/sign | 160 | 2026182461 |
| 2 | Normal/sign | 640 | 2026282941 |
| 3 | t5 | 320 | 2026382621 |
| 4 | t5 | 640 | 2026482941 |
| 5 | Strong skew | 640 | 2026582941 |
| 6 | Strong skew | 2560 | 2026684861 |
<!-- /table:wald_seeds -->

The reference generator is `generate_regular_scenario` in
`scripts/audit_wald_convergence_20260822.py`; the six-cell selection is
`run_claim1` in `scripts/run_claim_validation_20260823.py`.
The nonzero study uses `simulate` in
`scripts/validate_active_nuisance_20260907.py`. It draws an n-by-2 standard
normal array z, then sets `X=exp(.6*z[:,0])` and
`Y=exp(.6*(.4*z[:,0]+sqrt(1-.4**2)*z[:,1]))`. Replacing this with a different
bivariate-normal sampler need not preserve the frozen stream.
The four-stage generator is `generate` in
`scripts/run_reference_pathway_20260909.py`.

The September 7 manifest records Python 3.12.3, NumPy 1.26.4 and SciPy 1.16.3.
These are provenance entries, not a claim that a clean environment with those
versions has been exercised here. A seed alone is insufficient to reproduce
a different RNG call order or changed numerical libraries.

## S3.2 Exact studentizers and numerical methods

For arbitrary reference values tX,tY, define centered profiles ac=a-mean(a),
bc=b-mean(b), divisor-n variances va,vb and D=sqrt(va*vb). The direct
correlation IF is

\[
\ell_{0i}=\frac{a_{ci}b_{ci}}D-
\frac{\widehat\rho_P}{2}\left(\frac{a_{ci}^2}{v_a}+\frac{b_{ci}^2}{v_b}\right).
\]

With fitted sample gX=mean(sign(X-tX)) and hX=mean(sign(X-tX)b), put

\[
\widehat\lambda_X=
\frac{-\widehat h_X+\widehat g_X\bar b}{D}
+\frac{\widehat\rho_P}{v_a}\{P_n(X-t_X)-\bar a\widehat g_X\},
\]

and define lambdaY by interchanging margins. The stage-aware IF is
\(\ell_i=\ell_{0i}+\widehat\lambda_X\widehat{IF}_{T_X,i}
+\widehat\lambda_Y\widehat{IF}_{T_Y,i}\). The two studentizers are sample
SD(ell)/sqrt(n) and sample SD(ell0)/sqrt(n), both with variance divisor n-1.
The stage-aware label describes the formula, not theorem validity for the
nonregular full fit.

- **Stage 1, population reference:** tX=tY=0; location influences are zero.
  The scale k is recorded descriptively; no Huber score equation is fitted.
- **Stage 2, population scale:** s=k fixed. Fit the Huber location and use
  \(IF_T=(s/A)\psi_c\). Plug in the empirical active fraction A.
- **Stage 3, population median:** fix m=0 and estimate d=median(abs(W));
  fit the location at s=kd. Use
  \(IF_d=\{.5-1(|W|\le d)\}/\{f(d)+f(-d)\}\), then
  \(IF_T=(s/A)\psi_c-(B/A)kIF_d\). The absent median term is not estimated.
- **Stage 4, full fit:** use the complete median/MAD/Huber IF in Section 3
  with all empirical joint moments and coefficients.

Stages 2–3 use SciPy brentq on [min(W),max(W)] with xtol=1e-13. Stage 4
uses the unchanged public API. The default Gaussian KDE uses the sample SD
bandwidth in S1.5 and evaluations at the fitted median and its two MAD
boundaries (stage 3: at plus/minus d). The full solver starts at the midpoint
median and performs at most 100 reweighted updates. The default c and k are
1.345 and 1.4826. Zero MAD, a degenerate active fraction or profile variance,
or invalid SE is not interpreted as a valid zero effect. The saved error
fields retain invalid returns; no replacements occurred.

Tests use two-sided |rho/SE|>1.959963984540054 in the pathway study; the
regular API uses its corresponding normal p-value and nominal .05. The
nonzero study covers truth when the ordinary untruncated 95% interval includes
.19347511885804566. Direct-only methods omit reference IF terms but retain
the fitted estimator; the oracle uses population locations and the direct
IF matching those fixed profiles. No permutation, bootstrap correction,
Fisher transform or tuned coverage adjustment is used in the main studies.

## S3.3 Full four-stage results

Every row has 2,000 valid records and zero failures. R denotes population
reference, S population scale, M population median, and F full fitting.
Both tau values remain nonregular at the median.

**Table S3.2. Profile effects and stage-aware rejection.** The interval is
the 95% Wilson interval for stage-aware empirical null rejection.

<!-- table:pathway_all -->
| tau | n | Stage | Mean rho | Rejection | 95% Wilson |
| --- | --- | --- | --- | --- | --- |
| 0.1 | 80 | R | 0.0006 | 0.0720 | [0.0615, 0.0842] |
| 0.1 | 80 | S | 0.3804 | 0.2235 | [0.2058, 0.2423] |
| 0.1 | 80 | M | 0.3804 | 0.2235 | [0.2058, 0.2423] |
| 0.1 | 80 | F | 0.8207 | 0.7550 | [0.7357, 0.7733] |
| 0.1 | 640 | R | -0.0006 | 0.0525 | [0.0436, 0.0632] |
| 0.1 | 640 | S | 0.1117 | 0.0330 | [0.0260, 0.0418] |
| 0.1 | 640 | M | 0.1117 | 0.0330 | [0.0260, 0.0418] |
| 0.1 | 640 | F | 0.6306 | 0.5510 | [0.5291, 0.5727] |
| 0.4 | 80 | R | -0.0035 | 0.0755 | [0.0647, 0.0879] |
| 0.4 | 80 | S | 0.0616 | 0.0490 | [0.0404, 0.0594] |
| 0.4 | 80 | M | 0.0616 | 0.0485 | [0.0399, 0.0588] |
| 0.4 | 80 | F | 0.0693 | 0.0430 | [0.0350, 0.0528] |
| 0.4 | 640 | R | 0.0007 | 0.0615 | [0.0518, 0.0729] |
| 0.4 | 640 | S | 0.0102 | 0.0505 | [0.0417, 0.0610] |
| 0.4 | 640 | M | 0.0102 | 0.0505 | [0.0417, 0.0610] |
| 0.4 | 640 | F | 0.0101 | 0.0505 | [0.0417, 0.0610] |
<!-- /table:pathway_all -->

**Table S3.3. Direct-only rejection and reference errors.** Reference
correlation is across replications. Constant-reference correlation is NA.

<!-- table:pathway_refs -->
| tau | n | Stage | Direct rate | RMSE X | RMSE Y | Corr(TX,TY) |
| --- | --- | --- | --- | --- | --- | --- |
| 0.1 | 80 | R | 0.0720 | 0.00000 | 0.00000 | NA |
| 0.1 | 80 | S | 0.6785 | 0.11434 | 0.11481 | 0.99030 |
| 0.1 | 80 | M | 0.6785 | 0.11434 | 0.11481 | 0.99030 |
| 0.1 | 80 | F | 0.9035 | 0.50555 | 0.50593 | 0.98468 |
| 0.1 | 640 | R | 0.0525 | 0.00000 | 0.00000 | NA |
| 0.1 | 640 | S | 0.4875 | 0.04013 | 0.04014 | 0.98990 |
| 0.1 | 640 | M | 0.4875 | 0.04013 | 0.04014 | 0.98990 |
| 0.1 | 640 | F | 0.8270 | 0.27897 | 0.27872 | 0.98671 |
| 0.4 | 80 | R | 0.0755 | 0.00000 | 0.00000 | NA |
| 0.4 | 80 | S | 0.1605 | 0.13323 | 0.13266 | 0.86889 |
| 0.4 | 80 | M | 0.1610 | 0.13317 | 0.13248 | 0.86926 |
| 0.4 | 80 | F | 0.1780 | 0.14508 | 0.14539 | 0.89306 |
| 0.4 | 640 | R | 0.0615 | 0.00000 | 0.00000 | NA |
| 0.4 | 640 | S | 0.0785 | 0.04785 | 0.04763 | 0.87410 |
| 0.4 | 640 | M | 0.0785 | 0.04784 | 0.04762 | 0.87384 |
| 0.4 | 640 | F | 0.0770 | 0.04766 | 0.04736 | 0.86932 |
<!-- /table:pathway_refs -->

**Table S3.4. Paired stage contrasts.** Difference means the later stage
minus the earlier stage, using the same 2,000 datasets. Entries show
difference (paired MCSE); rejection is stage-aware. Direct-only and reference
MSE contrasts remain in the source ledger for exact machine-readable use.

<!-- table:pathway_pairs -->
| tau | n | Contrast | Delta rejection (MCSE) | Delta rho (MCSE) |
| --- | --- | --- | --- | --- |
| 0.1 | 80 | R to S | 0.1515 (0.01050) | 0.3798 (0.00639) |
| 0.1 | 80 | S to M | 0.0000 (0.00000) | -0.0000 (0.00000) |
| 0.1 | 80 | M to F | 0.5315 (0.01116) | 0.4403 (0.00574) |
| 0.1 | 80 | S to F | 0.5315 (0.01116) | 0.4403 (0.00574) |
| 0.1 | 640 | R to S | -0.0195 (0.00621) | 0.1123 (0.00277) |
| 0.1 | 640 | S to M | 0.0000 (0.00000) | 0.0000 (0.00000) |
| 0.1 | 640 | M to F | 0.5180 (0.01122) | 0.5189 (0.00658) |
| 0.1 | 640 | S to F | 0.5180 (0.01122) | 0.5189 (0.00658) |
| 0.4 | 80 | R to S | -0.0265 (0.00574) | 0.0651 (0.00177) |
| 0.4 | 80 | S to M | -0.0005 (0.00112) | -0.0001 (0.00004) |
| 0.4 | 80 | M to F | -0.0055 (0.00165) | 0.0078 (0.00053) |
| 0.4 | 80 | S to F | -0.0060 (0.00187) | 0.0077 (0.00053) |
| 0.4 | 640 | R to S | -0.0110 (0.00338) | 0.0095 (0.00031) |
| 0.4 | 640 | S to M | 0.0000 (0.00000) | -0.0000 (0.00000) |
| 0.4 | 640 | M to F | 0.0000 (0.00000) | -0.0001 (0.00001) |
| 0.4 | 640 | S to F | 0.0000 (0.00000) | -0.0001 (0.00001) |
<!-- /table:pathway_pairs -->

The original protocol's statement of almost-sure empirical-root uniqueness
was corrected after the run: a separated, exactly balanced sample can have
an interval of Huber roots. Population uniqueness remains valid. The
correction and the original outcomes are both retained. No invalid return
occurred in these runs; that does not establish all-sample uniqueness.

## S3.4 Nonzero-effect results and numerical truth

The population target is from split adaptive quadrature and analytic
truncated-lognormal moments, not the earlier coarse .193218 benchmark.
The variance quadrature splits at the nuisance knots and was checked at
24,48,72 nodes per interval. At the highest order the full variance is
2.930344036191777, direct-only variance 2.935125447074918, nuisance variance
.029924671347371, and twice the direct–nuisance covariance -.034706082230512.
The last two explain the small net variance difference without justifying
omission of nuisance terms. Four contamination directions at epsilon=1e-6
give maximum scaled derivative discrepancy about 1.596e-5.

**Table S3.5. Full nonzero-study summaries.** F=complete IF, D=direct-only
ablation, O=population-reference oracle. Each row has 2,000 valid estimates
and zero failures. Bias is estimate minus population truth. SE is mean
estimated standard error; SD is empirical sampling SD.

<!-- table:skew_full -->
| n | Method | Bias | Bias MCSE | SD | Mean SE | SE/SD |
| --- | --- | --- | --- | --- | --- | --- |
| 160 | F | -0.00782 | 0.00278 | 0.12425 | 0.10434 | 0.8397 |
| 160 | D | -0.00782 | 0.00278 | 0.12425 | 0.10342 | 0.8323 |
| 160 | O | -0.00918 | 0.00280 | 0.12502 | 0.10336 | 0.8268 |
| 640 | F | -0.00247 | 0.00149 | 0.06684 | 0.06015 | 0.8999 |
| 640 | D | -0.00247 | 0.00149 | 0.06684 | 0.06010 | 0.8991 |
| 640 | O | -0.00244 | 0.00150 | 0.06699 | 0.06006 | 0.8967 |
| 2560 | F | -0.00083 | 0.00075 | 0.03338 | 0.03226 | 0.9664 |
| 2560 | D | -0.00083 | 0.00075 | 0.03338 | 0.03227 | 0.9669 |
| 2560 | O | -0.00088 | 0.00075 | 0.03355 | 0.03227 | 0.9620 |
<!-- /table:skew_full -->

**Table S3.6. Coverage uncertainty and widths.** Widths refer to the original
Wald interval. These are coverage probabilities, not null rejection rates.

<!-- table:skew_uncertainty -->
| n | Method | Coverage | MCSE | 95% Wilson | Mean width |
| --- | --- | --- | --- | --- | --- |
| 160 | F | 0.8580 | 0.00780 | [0.8420, 0.8726] | 0.4090 |
| 160 | D | 0.8535 | 0.00791 | [0.8373, 0.8683] | 0.4054 |
| 160 | O | 0.8485 | 0.00802 | [0.8321, 0.8635] | 0.4052 |
| 640 | F | 0.9115 | 0.00635 | [0.8983, 0.9232] | 0.2358 |
| 640 | D | 0.9110 | 0.00637 | [0.8977, 0.9227] | 0.2356 |
| 640 | O | 0.9050 | 0.00656 | [0.8914, 0.9171] | 0.2354 |
| 2560 | F | 0.9270 | 0.00582 | [0.9148, 0.9376] | 0.1264 |
| 2560 | D | 0.9265 | 0.00584 | [0.9142, 0.9371] | 0.1265 |
| 2560 | O | 0.9290 | 0.00574 | [0.9169, 0.9395] | 0.1265 |
<!-- /table:skew_uncertainty -->

**Table S3.7. Paired complete-minus-direct coverage.**

<!-- table:skew_pairs -->
| n | Paired R | Coverage difference | Paired MCSE | Full only | Direct only |
| --- | --- | --- | --- | --- | --- |
| 160 | 2000 | 0.0045 | 0.001800 | 11 | 2 |
| 640 | 2000 | 0.0005 | 0.000500 | 1 | 0 |
| 2560 | 2000 | 0.0005 | 0.000866 | 2 | 1 |
<!-- /table:skew_pairs -->

## S3.5 Supporting C and marginal profile CVs

The saved pathway records include each fitted C and rho but not both
marginal CVs. For the existing tau=.10,n=640 cell only, the integration
script deterministically regenerates each of the 2,000 original arrays
using its recorded seed mapping and evaluates distances at the *stored*
references. It performs no reference refitting, simulation expansion or
rejection recalibration. It checks all 8,000 stage records against saved C
and rho and verifies C=1+rho*CVx*CVy per replication before summarizing.

**Table S3.8. Secondary C and CV summaries.** Each entry is mean (MCSE).
The three means do not reconstruct mean C when multiplied by mean rho.

<!-- table:c_summaries -->
| Stage | C (MCSE) | CVx (MCSE) | CVy (MCSE) |
| --- | --- | --- | --- |
| R | 0.999994 (0.000009) | 0.100108 (0.000064) | 0.100172 (0.000062) |
| S | 1.001573 (0.000051) | 0.107351 (0.000223) | 0.107407 (0.000223) |
| M | 1.001573 (0.000051) | 0.107351 (0.000223) | 0.107407 (0.000223) |
| F | 1.079550 (0.001963) | 0.265546 (0.003200) | 0.265044 (0.003204) |
<!-- /table:c_summaries -->

The CVs use divisor n, not n-1. C comes from the original stored
`historical_C` field, which here denotes robust-reference C, not original
all-to-all c-delta. The generated integration audit records maximum replay
gaps, record counts and source hashes. This verifies the bounded summary;
it is not a fresh Monte Carlo run or independent clean reproduction.

## S3.6 Post hoc diagnostics and root flags

**Table S3.9. Nonzero-skew tail and population-SE diagnostics.** These
use the same frozen replications. P=reported plug-in SE; V=infeasible
population asymptotic SE. All rows use the complete estimator and 2,000
replications. Below means the interval is wholly below truth; above means
it is wholly above truth. Wilson intervals are retained in the source file.

<!-- table:skew_diagnostics -->
| n | SE | Coverage | Below | Above | Coverage delta | Paired MCSE |
| --- | --- | --- | --- | --- | --- | --- |
| 160 | P | 0.8580 | 0.1115 | 0.0305 | 0.0000 | 0.00000 |
| 160 | V | 0.9675 | 0.0080 | 0.0245 | 0.1095 | 0.00750 |
| 640 | P | 0.9115 | 0.0695 | 0.0190 | 0.0000 | 0.00000 |
| 640 | V | 0.9590 | 0.0100 | 0.0310 | 0.0475 | 0.00618 |
| 2560 | P | 0.9270 | 0.0595 | 0.0135 | 0.0000 | 0.00000 |
| 2560 | V | 0.9580 | 0.0195 | 0.0225 | 0.0310 | 0.00525 |
<!-- /table:skew_diagnostics -->

The population-SE substitution changes random scale and its dependence on
the estimate simultaneously. It is not a practical remedy or unique causal
decomposition. Eighteen regular-study reference replays had maximum
scale-normalized discrepancy about 2.35e-11; those fits do not suggest an
obvious solver explanation for this undercoverage.

**Table S3.10. The two flagged pathway full fits.** Both are tau=.10,n=640.
The flag compares stored and bracketed roots in fitted-scale units against
1e-6. Delta rho is bracketed minus original; relative delta SE is a fraction,
not a percentage. Neither studentizer's rejection changed.

<!-- table:root_flags -->
| Rep | Root gap / scale | Delta rho | Relative delta SE | Decisions changed |
| --- | --- | --- | --- | --- |
| 70 | 1.410854e-05 | -4.572481e-07 | -3.02298e-05 | 0 / 0 |
| 1622 | 1.790506e-06 | -4.681389e-07 | -1.397699e-05 | 0 / 0 |
<!-- /table:root_flags -->

The recorded score residual at Stage 1 need not be zero: those references
are fixed at population values and are not empirical roots. It must not
be counted as a fitting failure. The public full-fit solver has not been
silently replaced by the bracketed solver; no flagged record was removed.

## S3.7 Permutation seed ledger and execution order

The full bridge DGM and methods are in S2. The four-family seed formula is
`2026081750+n+round(10000*epsilon)+100000*f`, with zero-based family order
uniform, exponential, half-normal, scaled_beta12. Each replication consumes
the draw, 99 permutation index vectors, then the historical diagnostic
bootstrap calls (199 reference fits per margin) before the next draw. Pilot and larger
confirmation use the same cell seed and call order, so the pilot is a prefix
of the larger confirmation; they are not independent datasets to be pooled.
For the prospective family the seed is
`2026082581+100000*i+10000*j+n`, with i=1,2 for n=80,320 and j=1,2,3 for
epsilon=.05,.10,.20; the stream has no diagnostic bootstrap step.

**Table S3.11. Exact permutation cell ledger.** P=24-cell pilot,
C=larger matched-index confirmation, H=prospective hyperexponential.
All have 99 permutations per dataset. R is number of datasets.

<!-- table:permutation_seeds -->
| Panel | Family | n | epsilon | R | Cell seed |
| --- | --- | --- | --- | --- | --- |
| P | Exp | 80 | 0.05 | 150 | 2026182330 |
| P | Half-normal | 80 | 0.05 | 150 | 2026282330 |
| P | Beta | 80 | 0.05 | 150 | 2026382330 |
| P | Uniform | 80 | 0.05 | 150 | 2026082330 |
| P | Exp | 80 | 0.1 | 150 | 2026182830 |
| P | Half-normal | 80 | 0.1 | 150 | 2026282830 |
| P | Beta | 80 | 0.1 | 150 | 2026382830 |
| P | Uniform | 80 | 0.1 | 150 | 2026082830 |
| P | Exp | 80 | 0.2 | 150 | 2026183830 |
| P | Half-normal | 80 | 0.2 | 150 | 2026283830 |
| P | Beta | 80 | 0.2 | 150 | 2026383830 |
| P | Uniform | 80 | 0.2 | 150 | 2026083830 |
| P | Exp | 320 | 0.05 | 150 | 2026182570 |
| P | Half-normal | 320 | 0.05 | 150 | 2026282570 |
| P | Beta | 320 | 0.05 | 150 | 2026382570 |
| P | Uniform | 320 | 0.05 | 150 | 2026082570 |
| P | Exp | 320 | 0.1 | 150 | 2026183070 |
| P | Half-normal | 320 | 0.1 | 150 | 2026283070 |
| P | Beta | 320 | 0.1 | 150 | 2026383070 |
| P | Uniform | 320 | 0.1 | 150 | 2026083070 |
| P | Exp | 320 | 0.2 | 150 | 2026184070 |
| P | Half-normal | 320 | 0.2 | 150 | 2026284070 |
| P | Beta | 320 | 0.2 | 150 | 2026384070 |
| P | Uniform | 320 | 0.2 | 150 | 2026084070 |
| C | Exp | 320 | 0.05 | 500 | 2026182570 |
| C | Half-normal | 320 | 0.05 | 500 | 2026282570 |
| C | Beta | 320 | 0.05 | 500 | 2026382570 |
| C | Uniform | 320 | 0.05 | 500 | 2026082570 |
| H | Hyperexp | 80 | 0.05 | 200 | 2026192661 |
| H | Hyperexp | 80 | 0.1 | 200 | 2026202661 |
| H | Hyperexp | 80 | 0.2 | 200 | 2026212661 |
| H | Hyperexp | 320 | 0.05 | 200 | 2026292901 |
| H | Hyperexp | 320 | 0.1 | 200 | 2026302901 |
| H | Hyperexp | 320 | 0.2 | 200 | 2026312901 |
<!-- /table:permutation_seeds -->

The code paths are `run_family_cell` in
`scripts/run_profile_bridge_family_validation_20260817.py` and
`claim3_prospective_family_validation` in
`scripts/run_claim_external_validation_20260825.py`. The index calculations
and original source links are preserved in the September 5 display tables.

## S3.8 Source ledger and reproducibility status

All paths below are relative to the repository root. Raw and normalized
SHA-256 hashes of these inputs are stored in the new integration audit,
alongside the old manifest verification. The old result files and manifests
are unchanged. An unexpected old hash failure must be investigated, not
repaired by updating the expected hash.

<!-- table:source_ledger -->
| ID | Used for |
| --- | --- |
| W | Main Table 1; S3.1 |
| W0 | Regular-null source/denominators |
| B | S2.1; legacy Figure 2 |
| F | S2.2–3; legacy Figure 3 |
| D | Legacy display source hashes |
| P | All 32,000 stage records |
| PS | Main Tables 3–4; S3.2–3 |
| PP | S3.4 paired contrasts |
| PR | S3.10 retained root flags |
| PM | Pathway provenance |
| A | 18,000 method records |
| AS | Main Table 2; S3.5–6 |
| AP | S3.7 paired coverage |
| AT | Population truth and IF variance |
| AD | Contamination derivative check |
| AM | Skew provenance |
| Q | S3.9 post hoc tail diagnostics |
| QR | 18 regular reference replays |
| QM | Post hoc provenance |

- W: `results/section6_display_table2_wald_20260905.tsv`.
- W0: `results/claim1_wald_validation_20260823.tsv`.
- B: `results/section6_display_figure2_bridge_20260905.tsv`.
- F: `results/section6_display_figure3_residual_20260905.tsv`.
- D: `results/section6_display_manifest_20260905.tsv`.
- P: `results/reference_pathway_replications_20260909.tsv`.
- PS: `results/reference_pathway_summary_20260909.tsv`.
- PP: `results/reference_pathway_paired_20260909.tsv`.
- PR: `results/reference_pathway_root_sensitivity_20260909.tsv`.
- PM: `results/reference_pathway_manifest_20260909.tsv`.
- A: `results/active_nuisance_replications_20260907.tsv`.
- AS: `results/active_nuisance_summary_20260907.tsv`.
- AP: `results/active_nuisance_paired_20260907.tsv`.
- AT: `results/active_nuisance_population_20260907.tsv`.
- AD: `results/active_nuisance_derivative_20260907.tsv`.
- AM: `results/active_nuisance_manifest_20260907.tsv`.
- Q: `results/referee_coverage_diagnostics_20260908.tsv`.
- QR: `results/referee_root_replay_20260908.tsv`.
- QM: `results/referee_diagnostics_manifest_20260908.tsv`.
<!-- /table:source_ledger -->

The deterministic table/replay check is
`python scripts/integrate_manuscript_20260911.py` from the repository root.
Its default mode is read-only and rejects changed displayed tables. Only
`--write` refreshes the new manuscript table blocks and dated integration
report. It never rewrites frozen scientific sources. The older completion
audit remains a separate check of the historical chapter files.

For a future clean reproduction, use an isolated checkout, an explicit
environment lock and a separate output directory. The September 7 script
accepts `--out-dir`; older runners write to fixed result paths and therefore
must only be run in that isolated checkout. Reproduction must compare
declared source versions, numeric tolerances, row accounting and retained
failures, not merely whether a script exits successfully. No clean-environment
Monte Carlo reproduction is claimed by the present table assembly.
