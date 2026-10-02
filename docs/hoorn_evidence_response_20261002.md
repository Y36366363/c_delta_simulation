# Evidence retained in the six-section Hoorn revision

Date: 2 October 2026. Starting repository commit: `f694b1e`.
Starting author source is the 2 October definition-integration version recorded
in `results/manuscript_delivery_20261002.json` (SHA-256
`4ef70ad6645d17f7ffbbccc3d42a305aa72c0a05da4a2b320856b3c425413493`).

This revision changes how the existing evidence is presented. It does not add
a scientific design, replace an unfavorable law, alter either solver, or turn
internal review into independent mathematical certification.

## Two selected main-text tables

### Reference pathway: eight rows

Use all four stages at tau=.10 for n=80 and 640, preserving the same 2,000
datasets per cell. Report mean fitted rho, stage-aware empirical null rejection,
its Wilson interval, and direct-only rejection. The stage definition is fixed
population locations; fixed population scale with fitted locations; fixed
population medians with fitted MAD/locations; and complete median/MAD/Huber fit.

Source: `results/reference_pathway_summary_20260909.tsv` fields `mean_rho`,
`stage_aware_rate`, `stage_aware_wilson_low`, `stage_aware_wilson_high`, and
`direct_only_rate`. Rates are not validation of a regular-law theorem for the
nonregular full fit. Stages 2 and 3 agree in these realized severe cells because
their fitted observations lie inside the Huber linear regime; the stored-data
check of all 16,000 marginal fits is in `results/evidence_interfaces_20260926.json`.

Optional concise paired contrast in prose: at n=80, full minus fixed-scale
stage-aware rejection is .5315 (paired MCSE .01116); mean fitted rho increases
.44025 (paired MCSE .00574). At n=640 the respective increases are .5180
(.01122) and .51894 (.00658). These come from the stored within-dataset contrasts,
not independent-method standard errors. One such contrast suffices in the body;
all contrasts remain in S3.

### Regular checks: four null rows and six coverage rows

The compact regular table contains the same four selected null rows previously
in the main text plus complete-IF coverage at every sample size of both
prespecified nonzero lognormal studies. Separate the two rate meanings clearly:
null rejection nominal .05 (1,000 datasets per row), interval coverage nominal
.95 (2,000 datasets per row). Give Wilson uncertainty for every displayed row.

| Law | n | Rejection or coverage | 95% Wilson |
|---|---:|---:|---|
| Normal shared sign, null rejection | 640 | .0440 | [.0329,.0586] |
| Independent t5, null rejection | 640 | .0590 | [.0460,.0754] |
| Independent strong skew, null rejection | 640 | .1220 | [.1031,.1437] |
| Independent strong skew, null rejection | 2560 | .0820 | [.0666,.1006] |
| Lognormal SD .6, coverage | 160 | .8580 | [.8420,.8726] |
| Lognormal SD .6, coverage | 640 | .9115 | [.8983,.9232] |
| Lognormal SD .6, coverage | 2560 | .9270 | [.9148,.9376] |
| Lognormal SD .3, coverage | 160 | .9045 | [.8908,.9166] |
| Lognormal SD .3, coverage | 640 | .9355 | [.9239,.9455] |
| Lognormal SD .3, coverage | 2560 | .9365 | [.9250,.9464] |

Sources: `claim1_wald_validation_20260823.tsv`,
`active_nuisance_summary_20260907.tsv`, and
`moderate_benchmark_summary_20260920.tsv`. The two smaller null cells, all
direct-only/oracle intervals, empirical SD/SE summaries, tails, flags, constants,
and failure accounting remain in the retained supplement tables.

## Interpretive obligations that shortening must retain

1. **All three original null laws have inactive population reference terms.**
   Independence gives zero reference coefficients in t5 and strong skew;
   shared-sign symmetry gives them in the normal-margin law. This does not make
   finite-sample fitted coefficients identically zero.
2. **Both nonzero laws activate nuisance, but cancellation is substantial.**
   At log SD .6, rho=.19347511885804566 and each reference coefficient is about
   -.14981377; full/direct population IF variances are 2.93034404/2.93512545.
   At log SD .3, rho=.1625386847281758 and the coefficient is about -.28971150;
   variances are 1.76932513/1.77747949. These are not strong demonstrations of
   complete-studentizer superiority. Do not treat similar coverage as permission
   to omit reference terms in other laws.
3. **Neither nonzero study supplies successful nominal calibration.** Every
   displayed complete-coverage Wilson interval excludes .95. Moderate-skew
   n=640 versus 2560 does not establish continuing monotone improvement.
   Oracle undercoverage rules out reference estimation as the sole cause.
4. **Pointwise asymptotics do not give a sample-size rule.** The null cells
   compatible with .05 may be described as compatible, not as proof that all
   regular distributions are calibrated by n=640.
5. **The staged intervention supports two pathways.** Fixed-scale location
   error is already present; full fitting further amplifies it. The shared-sign
   population Huber slope is nonzero. It is incorrect to attribute all failure
   to a nearly flat population Huber equation or a nonzero symmetric first-order
   scale derivative.
6. **Conditioning and permutation remain supporting material.** The index is
   an explanatory first-order organizer, not a gate. Matched indices do not match
   score covariance or target projection. S2 rates are for the B=99 procedure
   and do not prove weak-null permutation exactness or a conditional CLT.

## Reconciliation and scope

`scripts/audit_hoorn_restructure_20261002.py` independently assembles the two
selected displays directly from the frozen result fields. It reconciles all
21 retained tables (1,182 cells) and the two selected tables (88 cells):
23 tables and 1,270 cells in total. It permits moving tables and changing
captions while requiring all scientific data bodies to remain identical.
Only three semantic display pointers in the S3.12 source ledger are changed:
W to `Table~\ref{tab:regular}; S3.1`, PS to
`Tables~\ref{tab:stages}--\ref{tab:references}; S3.2--3`, and AS to
`Table~\ref{tab:coverage}; S3.5--6`. All other source-ledger cells are preserved.
The six-section main body must contain only the two selected tables; the
original 21 identities must occur in the supplement portion. Citation and
equation references are checked by key, not by old printed numbering.

The former main-table identities in the source ledger are replaced by the
three explicit label-based references above. Relocation is not permission to
leave misleading references to the new Table 1 or 2.

The temporary September 25 verified environment is no longer present on
2 October. This round's deterministic assembly/source audit uses the available
Anaconda interpreter and makes no new isolated-environment reproduction claim.
All previously recorded clean-environment evidence and its limitations remain
intact. No new Monte Carlo run is required for a structural revision.

### Final author-source audit

The final source reconciliation passed and is recorded in
`results/manuscript_restructure_audit_20261002.json`. It binds the restructured
`main.tex` to SHA-256
`a04efba49a0693c5b260733f78bd6ae0eef81b65fb1d0a116efcf042edf7fefc`
and the audit script to
`aef065a0c7df1dc1c60777d9bbf11bd1edff6cbabfac2208bca9546b81659345`.
All 23 tables and 1,270 cells passed: the 20 retained data-table bodies are
identical, and the retained source ledger differs only in the three declared
display pointers. The main text has six sections and its two selected tables;
the supplement retains all 21 earlier table identities. All 172 historical
provenance checks and eight moderate-study frozen-file hashes passed. All 25
bibliography keys are cited, and the 37 labels and 23 referenced keys contain
no duplicates or unresolved references.

A separate targeted prose review corrected the cancellation reference to
S3.4, the population-SE diagnostic reference to S3.6, and the description of
the archived severe-cell displays (two sample sizes at tau=.10, not two spread
settings). The main text now explicitly calls the six uncertainty intervals
Monte Carlo Wilson intervals for complete-IF coverage. The fixed-offset radial
variances use distinct notation from the five-moment derivative vectors.
These are source and interpretation checks, not independent mathematical
review or a new Monte Carlo experiment; the report records zero new design
cells. PDF compilation and visual quality assurance are recorded separately
by the author-artifact delivery step.

## Genuine remaining dependencies

Hoorn's assessment of the shorter narrative, final section placement and journal
fit remains an author decision. Independent mathematical review of the full
regular proof and nonregular proposition remains a substantive external task.
Availability wording, actual AI assistance disclosure and author details must
match the intended submission. None of these is closed by additional simulation
or by making the main text shorter.
