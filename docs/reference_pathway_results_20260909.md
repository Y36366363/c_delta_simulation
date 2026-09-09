# Staged reference pathway: supervisor-directed completion

Date: 2026-09-09. Primary estimand rho_P; historical C is secondary. The
protocol was written before the new simulation outcomes. No distribution
grid expansion, new resampling method, or clustered-data theory was added.

## 1. Answer to the mechanism question

**Both pathways are present, but their roles differ.** In the severe tau=.10
construction, fixed-population-scale Huber fitting already creates strongly
linked reference errors and positive profile bias. It does **not** reproduce
all of the much larger full-fit effect and stage-aware rejection distortion.
Estimating the MAD with the true median fixed adds essentially nothing in
these concentrated samples. Estimating the median and then MAD about that
median substantially contracts the fitted scale and amplifies reference
movement. This last comparison is evidence for the **additional joint
median/MAD fitting pathway**, not a decomposition that assigns all failure
to the median alone.

Rejection comparisons depend strongly on the studentizer. At n=640,
fixed-scale fitting has mean rho=.11165 but stage-aware rejection .033;
the direct-only studentizer rejects .4875 on those same profiles. Thus low
rejection does not establish absence of reference-induced bias, and direct-
only rejection cannot be reported as though it were the complete procedure.

## 2. Prespecified design

- X=S exp(tau U), Y=S exp(tau V); population T=0, raw MAD=1, scaled MAD=k.
- Same four old cells: tau=.10/.40 and n=80/640; 2,000 samples each.
- 8,000 IID paired datasets, 32,000 stage records, no invalid fit/SE returns.
- All stages evaluated on identical draws. Root seed 2026090901 with
  SeedSequence [root,round(100*tau),n,replication]. No replaced failures.
- Stage 1 fixes population references. Stage 2 fixes population scale and
  estimates Huber location. Stage 3 fixes population median and estimates
  MAD/Huber. Stage 4 uses the public complete median/MAD/Huber API.
- Each estimated profile receives its stage-aware and direct-only plug-in
  SE. These are empirical null rejection experiments; the complete median
  regularity assumption fails in this family. No finite-sample validity
  certificate or permutation remedy is inferred.

Stage-2 IF_T=s psi/A. Stage-3 MAD influence omits the median-estimation term;
its IF_T additionally propagates -(B/A)k IF_d. Stage 4 uses the public full
IF. The direct-only track omits location IF terms at every stage. Both use
the same five-moment target and ordinary sample-variance correction. The
stage-aware formula also matches an independently assembled five-moment
gradient calculation in regression tests.

## 3. Severe shared-sign results, tau=.10

| n | Stage | Mean rho_P | Stage-aware empirical null rejection | Direct-only rejection | Reference RMSE X / Y | Corr(T_X,T_Y) |
|---|---|---|---|---|---|---|
| 80 | Population references | .00064 | .0720 | .0720 | 0 / 0 | NA |
| 80 | Population scale | .38042 | .2235 | .6785 | .11434 / .11481 | .99030 |
| 80 | Population median | .38042 | .2235 | .6785 | .11434 / .11481 | .99030 |
| 80 | Full fit | .82067 | .7550 | .9035 | .50555 / .50593 | .98468 |
| 640 | Population references | -.00061 | .0525 | .0525 | 0 / 0 | NA |
| 640 | Population scale | .11165 | .0330 | .4875 | .04013 / .04014 | .98990 |
| 640 | Population median | .11165 | .0330 | .4875 | .04013 / .04014 | .98990 |
| 640 | Full fit | .63059 | .5510 | .8270 | .27897 / .27872 | .98671 |

NA means an undefined correlation between constant references, not zero
correlation. All stage-wise Wilson intervals, RMSE delta-method MCSE,
reference-correlation delta-method MCSE, and effect MCSE are stored in
`results/reference_pathway_summary_20260909.tsv`.

Selected stage-aware 95% Wilson intervals:

- n=80: fixed references [.0615,.0842], fixed scale [.2058,.2423],
  full fit [.7357,.7733]. The fixed-reference baseline is not assumed to
  be perfectly calibrated at this small n.
- n=640: fixed references [.0436,.0632], fixed scale [.0260,.0418],
  full fit [.5291,.5727]. Fixed-scale rejection is conservative here, not
  evidence that the profile estimate has no bias.

The paired fixed-scale-to-full increase in mean rho is .44025 at n=80 and
.51894 at n=640. The corresponding stage-aware rejection increments are
.5315 and .5180. The n=80 increment has paired MCSE .01116; complete paired
MCSE for both sizes, adjacent stages, and squared reference errors is retained
in `results/reference_pathway_paired_20260909.tsv`.

### Why the stages behave differently

For tau=.10 all stage-2/3 fitted observations in this run are inside the
Huber clipping interval. Their references equal sample means to numerical
precision, with RMS discrepancies below 4e-17. The sample-mean correlation
formula exp(-tau^2) gives .99005, consistent with the empirical cross-reference
correlations near .99. This directly supports the professor's warning that
linked reference errors can arise even with the true scale held fixed.

Stage 3 keeps mean scaled MAD near 1.4826. Full fitting reduces mean X scale
to .53545 at n=80 and .61788 at n=640, with corresponding mean active Huber
fractions across margins .47326 and .37186. The full reference no longer
tracks the sample mean closely: RMS differences are .39872 and .23989.
Reference RMSE grows by about 4.4 and 7.0 times relative to fixed-scale fitting.
This supports additional amplification through empirical median/MAD fitting
in the severe cells. It does not identify a universal causal fraction or
prove a switching-probability law.

## 4. Diffuse control, tau=.40

| n | Stage | Mean rho_P | Stage-aware rejection | Direct-only rejection |
|---|---|---|---|---|
| 80 | Population references | -.00346 | .0755 | .0755 |
| 80 | Population scale | .06160 | .0490 | .1605 |
| 80 | Population median | .06155 | .0485 | .1610 |
| 80 | Full fit | .06934 | .0430 | .1780 |
| 640 | Population references | .00070 | .0615 | .0615 |
| 640 | Population scale | .01023 | .0505 | .0785 |
| 640 | Population median | .01022 | .0505 | .0785 |
| 640 | Full fit | .01009 | .0505 | .0770 |

The large full-fit amplification is absent in this control. Nevertheless its
median density at zero is also zero: apparent empirical calibration is not
proof that the complete regular theorem applies. The unbridged population J
has minimum singular value zero at both tau values; I_n cannot distinguish
these severe/diffuse regimes. Positive-density bridge results have a separate
role and do not turn I_n into a universal rule.

## 5. Numerical accuracy and reproducibility

The primary production estimator was not changed. All full-stage roots were
compared with an independent bracketed root at the same fitted scale. Two
of 8,000 full fits exceeded a diagnostic difference of 1e-7 scale units:
tau=.10,n=640,replications 70 and 1622. The maximum gap is 1.411e-5.
Recomputing both profiles and the matching full studentizer at the bracketed
roots changes estimates by less than 4.7e-7 and SEs by less than .0031%.
Neither rejection decision changes in either track. Original outcomes are
retained, and the sensitivity is disclosed in a separate table. Thus there
are zero invalid returns but **two numerical accuracy flags**, not a claim
that every original root met a strict convergence tolerance.

This finding warrants solver-status reporting before a software release,
not silently rewriting frozen simulations. A post-run correction to the
protocol also distinguishes population-root uniqueness from empirical-root
uniqueness: rare balanced, fully clipped samples can have an interval of
empirical roots. No zero-active/invalid stage return occurred in this run;
the stronger almost-sure uniqueness assertion is withdrawn, not used as a
theoretical guarantee.

The run used Python 3.12.3, NumPy 1.26.4, and SciPy 1.16.3. The complete
regression suite passes **269 tests**. These checks verify code, stored-result
accounting, algebra, and declared scope; they are not independent external
mathematical peer review. Reproduction:

```bash
/opt/anaconda3/bin/python scripts/run_reference_pathway_20260909.py
/opt/anaconda3/bin/python scripts/run_reference_pathway_20260909.py --summarize-only
/opt/anaconda3/bin/python -m pytest -q
```

The summary-only path reuses stored draws. Source/output hashes are in
`results/reference_pathway_manifest_20260909.tsv`. Historical canonical
sources and the completed nonzero-skew study are unchanged.

## 6. Manuscript consequences

1. Use the title and scope **Robust-reference profile correlation: pointwise
   inference and finite-sample limits**. The regular theorem is the core;
   failure and effective local conditioning are supporting contributions.
2. Replace a single-cause account with a two-pathway explanation: direct
   shared-sign reference error exists at fixed scale, while empirical
   median/MAD fitting supplies major additional amplification in the severe
   full-fit cells. Distinguish effect bias from studentizer-dependent rejection.
3. The short result in `docs/shared_sign_model_result_20260909.md` proves the
   population target, nonregular median, and nonflat Huber slope. Its
   fourth-root rate is only a conditional balance argument; no full boundary
   theorem or clustered extension is added.
4. Ordinary re-pairing does not change marginal medians, MADs, or Huber
   references. Recomputed quantities are the joint profile moments and the
   studentized statistic. Permutation remains empirical supporting evidence;
   do not label its stress rejection rates as validated Type I error for the
   weak profile-correlation null. The larger results can move to a supplement.
5. The nonzero-skew comparison is complete; full coverage .858/.9115/.927
   and asymmetric misses remain limitations, not reasons to search another
   favorable model. A short real application is optional only after verifying
   a defensible paired IID design. The proof/reproducibility review remains
   the next safe completion task.
