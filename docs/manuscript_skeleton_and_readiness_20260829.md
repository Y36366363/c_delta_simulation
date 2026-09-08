# Manuscript skeleton and readiness map

Date: 2026-08-29

Readiness and scope revision: 2026-09-08. This map is current working guidance,
not an independent peer-review certification. See
`docs/referee_readiness_review_20260908.md` for unresolved submission issues.

## Working identity

### Working title

**Trustworthy Inference for Robust-Reference Divergence Profiles**

Possible subtitle: **Regularity, Reference Instability, and Nuisance
Conditioning**

The title is provisional. It deliberately leads with inference rather than a
new coefficient name.

### One-sentence contribution

The paper defines paired similarity through correlation of observation-level
distances from fitted robust marginal references, proves pointwise IID
inference under regular identification, constructs severe finite-sample
failure under unstable reference fitting, and studies a dimensionless
nuisance-conditioning index that organizes—but does not fully explain—the
transition.

### Abstract logic

The abstract should contain exactly these six moves:

1. motivate the original question of matched internal divergence;
2. explain the shift from all-to-all divergence to robust-reference profiles;
3. identify \(\rho_P\) as the primary estimand;
4. state the regular pointwise IID inference result;
5. state the near-degenerate failure and the role of
   \(\sqrt n\sigma_{\min}(J)\);
6. end with the unexplained-family residual and observed finite-sample
   undercoverage, not an assurance of practical calibration.

No sentence should claim uniform validity, a universal diagnostic cutoff, or
a proved weak-null permutation theorem.

## Proposed main-text structure

### 1. Introduction: from similarity of divergence to reliability of inference

Purpose:

- cite Hoorn (2025), arXiv:2510.16717, as the motivating predecessor and
  distinguish its currently archived v2 from the planned normalization update;
- retain the substantive question of whether matched observations stand out
  similarly inside their respective groups;
- state that the robust-reference construction changes the estimand;
- make trustworthiness, failure, and diagnosis the three contributions;
- preview that \(\rho_P\) is primary and \(C\) secondary.

The introduction should not claim that the new method dominates the original
coefficient. The papers answer related but different questions.

### 2. Robust-reference divergence profiles

Define for a paired observation \(Z=(X,Y)\)

\[
r_X(X)=|X-T_X|,\qquad r_Y(Y)=|Y-T_Y|,
\]

where each \(T\) is the population Huber location fitted with an MAD-based
scale. Define the primary estimand

\[
\rho_P=\operatorname{Corr}\{r_X(X),r_Y(Y)\}
\]

and the secondary historical scale

\[
C=\frac{E\{r_X(X)r_Y(Y)\}}{E\{r_X(X)\}E\{r_Y(Y)\}}.
\]

State and interpret

\[
C=1+\rho_PCV(r_X)CV(r_Y).
\]

This section should also display the old one-dimensional L2 identity

\[
D_i^2=\frac{n}{n-1}\{(X_i-\bar X)^2+s_X^2\}
\]

to show precisely why the old all-to-all and new robust-reference profiles
share a paired-salience lineage without being the same functional.

Evidence source: `results/estimand_choice_audit_20260819.tsv` and
`results/scope_decision_audit_20260829.tsv`.

### 3. Estimation and inference under regular identification

Give the sample median, midpoint sample MAD convention, normal-consistency
factor, Huber estimating equation, fitted profiles, \(\widehat\rho_P\), and
\(\widehat C\). Then state:

- the median/MAD/Huber influence functions;
- the joint five-moment influence representation;
- Theorem A.1 for pointwise IID asymptotic normality;
- plug-in \(L_2\) consistency and studentized Wald inference;
- reference orthogonality under global independence;
- the weaker moment requirement at \(\rho_P=0\).

The main text should give a compact theorem and interpretation. Proofs remain
in Appendix A and Supplement S1.

Theory source: `docs/appendix_asymptotic_theory_20260819.md`.

Validation source: `results/claim1_wald_validation_20260823.tsv` and
`results/claim1_oracle_reference_validation_20260825.tsv`.

### 4. A constructive failure from unstable robust references

Introduce the separated-mode weak-null family. Its unbridged signed-lognormal
median is nonregular at every positive radial spread; its population Huber
score at the declared MAD scale is not flat. Explain the nonlocal empirical
median/MAD-to-reference pathway without treating it as a regular first-order
scale derivative at symmetry.

The evidence sequence should be causal rather than catalogued:

1. severe rejection under fitted references;
2. disappearance under paired fixed-reference analysis;
3. disappearance under exact sign-balance intervention;
4. monotone return under increasing shared-sign coupling;
5. binary-profile correlations \(+1\) and \(-1\) conditional on imposed
   nonzero offsets, not a fitted-switching probability theorem; the binary
   zero-reference target is undefined.

Primary sources:

- `results/claim2_reference_mechanism_validation_20260823.tsv`;
- `results/claim2_sign_balance_intervention_validation_20260824.tsv`;
- `results/claim2_sign_coupling_validation_20260825.tsv`;
- `results/claim_theory_audit_20260826.tsv`.

The section must say “can cause,” not “always causes.” Fixed references and
forced balance are mechanism interventions, not proposed general remedies.

### 5. Nuisance conditioning as a first-order diagnostic

Define the dimensionless standardized nuisance Jacobian

\[
J=
\begin{pmatrix}
df(m)&0&0\\
d\{f(m+d)-f(m-d)\}&d\{f(m+d)+f(m-d)\}&0\\
0&-B&-A/k
\end{pmatrix}
\]

and

\[
I_n=\sqrt n\,\sigma_{\min}(J).
\]

Explain the natural scaling through

\[
\|\widehat\theta-\theta\|_{\mathrm{standardized}}=O_P(1/I_n)
\]

as a local linear amplification rationale, not a uniform stochastic rate
along arbitrary degenerating laws. Score covariance and target projection
also matter. State positive affine invariance under the declared equation
normalization. Then report bridge ordering, leave-one-family-out prediction,
stricter grouped validation, and prospective hyperexponential validation.

Primary sources:

- `results/claim3_conditioning_lofo_summary_validation_20260823.tsv`;
- `results/claim3_stricter_cv_summary_validation_20260824.tsv`;
- `results/claim3_prospective_family_summary_validation_20260825.tsv`;
- `results/claim_theory_audit_20260826.tsv`.

Current decision: \(I_n\) is an explanatory and cautionary diagnostic. It is
not yet a data-driven accept/reject gate or a universally calibrated cutoff.

### 6. Simulation design and consolidated evidence

The main simulations should be organized by claim rather than chronology.

#### 6.1 Regular IID Wald behavior

Use the normal-margin shared-sign weak null, independent t5 convergence, and the
strong-skew slow-convergence stress. These directly align with Theorem A.1.

Primary source: `results/claim1_wald_validation_20260823.tsv`.

Also retain the existing-law nonzero-effect validation:
`results/active_nuisance_summary_20260907.tsv`. Its complete 95% coverage
remains .927 at n=2560. This is a calibration limitation, not a passed
finite-sample safety gate.

#### 6.2 Near-degenerate failure and intervention

Use the paired fitted-versus-fixed reference table at \(n=80,640\), supported
by sign balance and coupling as mechanism checks.

Primary source: `results/claim2_reference_mechanism_validation_20260823.tsv`.

#### 6.3 Conditioning transition

Use the bridge grid to plot rejection against \(I_n\), but mark these panels
as empirical fully recomputed studentized-permutation evidence rather than
direct theorem validation.

Primary source: `results/canonical_evidence_20260819.tsv`.

#### 6.4 Family residual unexplained by the index

Use the matched-\(J\) family comparison and prospective fifth family to show
both first-order transport and systematic residual error. Similar J does not
match score covariance or the target projection; the residual is not proved
entirely higher order.

Primary sources: `results/canonical_evidence_20260819.tsv` and
`results/claim3_prospective_family_validation_20260825.tsv`.

### 7. Applied illustration

Status: not yet frozen for the paper.

The existing building simulations are useful design stress tests but are not
automatically a real-data application. Before submission, decide with
Professor Hoorn whether the paper needs:

- one genuine paired dataset illustrating profile construction and the
  diagnostic;
- a clearly labelled synthetic illustration; or
- no application, with the paper positioned as a methodological theory and
  simulation article.

This is the largest remaining presentation decision. It should not be filled
with a convenient dataset whose scientific pairing or sampling design is
unclear.

### 8. Discussion

The discussion should separate:

- what is proved pointwise;
- what is demonstrated constructively in finite samples;
- what \(I_n\) explains empirically;
- strong-skew slow convergence outside the reference-switching mechanism;
- family residuals not explained by the scalar conditioning index;
- the boundary between weak-null Wald inference and exact randomization under
  group invariance;
- extensions to clustered buildings, multidimensional profiles, and formal
  weak-null permutation theory as future work rather than current claims.

Working text: `docs/manuscript_draft_section_8_20260908.md`. It includes
the active-nuisance coverage limitation and the explicitly post hoc
population-SE diagnostic; neither is a new inferential recommendation.

## Proposed main displays

1. **Table 1:** old all-to-all versus new robust-reference construct and
   estimand.
2. **Table 2:** theorem-aligned regular IID Wald calibration and strong-skew
   convergence boundary.
3. **Figure 1:** fitted-reference failure versus paired fixed-reference
   intervention.
4. **Figure 2:** rejection versus \(I_n\) across bridge levels, visually
   separated by family and sample size.
5. **Figure 3:** matched-\(J\) family residual plus prospective-family
   prediction error.
6. **Optional Table 3:** practical interpretation and assumptions for the
   diagnostic, only if an applied illustration is included.

The four historical canonical panels remain frozen evidence, but their final
manuscript display may be reorganized so that Wald and permutation tracks are
not visually conflated.

## Appendix and supplement map

- **Appendix A:** assumptions, nuisance derivatives, complete influence
  functions, asymptotic normality, plug-in variance consistency,
  orthogonality, affine invariance, and nonuniform boundary.
- **Supplement S1:** class-by-class entropy ledger, sample MAD convention,
  KDE/analytic-density details, and source-level derivative checks.
- **Supplement S2:** fixed-margin permutation equivalence, exact group
  invariance, weak-null boundary, and building-resampling cautions.
- **Supplement S3:** full simulation designs, seeds, Monte Carlo uncertainty,
  sensitivity tables, and prospective-family validation.

## Readiness assessment

| Component | Status | What remains |
|---|---|---|
| Scientific question and authorship direction | Closed | Confirm final title and terminology during manuscript review |
| Old/new construct separation | Ready | Convert the scope map into concise introduction prose |
| Primary estimand | Closed | Use \(\rho_P\) consistently throughout all active manuscript material |
| Functional delta-method theory | Full draft, independent review open | Resolve precise topology, joint Z-expansion, entropy and numerical-root interface; not merely typesetting |
| Claim 1 validation | Evidence assembled; practical calibration not established | Lead with Wald evidence; retain active-nuisance undercoverage and slow skew convergence |
| Claim 2 mechanism | Algebra plus intervention evidence | Distinguish imposed offsets from a switching-probability theorem and nonregular median from flat Huber curvature |
| Claim 3 first-order explanation | Ready as explanatory evidence | Do not turn \(I_n\) into a cutoff without a new calibration decision |
| Family residual limitation | Explicit | Do not infer purely higher-order effects from matching J or the scalar index |
| Inference-track presentation | Section 6 display separation audited | Maintain the separation in final journal typesetting and captions |
| Applied illustration | Unresolved | Decide with Professor Hoorn whether a genuine application is required |
| Literature positioning | Core comparator pass complete | Final review must remain open to additional related work; do not claim exhaustive priority |
| Reproducibility | Strong in the current environment | Dependency specification and independent clean build remain unverified |
| Main manuscript prose | Sections 1--6 and 8 drafted | Consolidate sources; Section 7 and abstract remain scope-dependent |

The archive and Section 3 preparation audit is complete in
`docs/archive_and_section3_readiness_20260831.md`; it found no blocking
mathematical issue for the main-text theorem.

## Maturity gates before submission

1. **Scope gate — passed.** Separate paper, primary estimand, and three claims
   are agreed.
2. **Theory gate — independent review open.** The full proof draft exists;
   mathematical review and theorem-to-implementation obligations remain.
3. **Evidence gate — assembled with limitations.** No broad simulation is
   needed. Practical nonzero-effect Wald calibration is not established.
   Section 6 keeps theorem-aligned Wald cells,
   finite-sample mechanism interventions, and empirical permutation cells in
   distinct displays.
4. **Diagnostic gate — limited pass.** \(I_n\) is defensible as a first-order
   organizer, not yet as a formal decision rule.
5. **Application gate — open.** The need and choice of an application require
   a scientific decision.
6. **Presentation gate — progressing.** Sections 1--6, Table 2, three main
   figures, and reproducible display scripts are assembled. Journal-style
   typesetting, abstract, and the application decision remain.

## Immediate next action

Sections 1--2 are in `docs/manuscript_draft_sections_1_2_20260830.md`, the
integrated regularity--switching--conditioning argument for Sections 3--5 is
in `docs/manuscript_draft_sections_3_5_20260904.md`, and the frozen displays
and Section 6 text are in `docs/manuscript_draft_section_6_20260905.md`.
Section 8 is drafted in `docs/manuscript_draft_section_8_20260908.md`.
Next prepare independent mathematical review and a clean reproduction recipe.
Section 7 remains open. The scientific decisions for Professor Hoorn include
whether a genuine application, stronger local theory, or practically calibrated
intervals are essential to the intended paper. Promoting
\(I_n\) from a population explanation to an operational warning rule would be
a separate theoretical decision and is not assumed by the current draft.
