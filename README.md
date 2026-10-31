# Reliable Inference for Robust-Reference Profile Correlation

Research code and manuscript support for studying when inference on paired
robust-reference divergence profiles is reliable—and when finite-sample
behavior can be misleading.

## Project at a Glance

| Item | Description |
|---|---|
| Research question | When can inference for correlation between paired robust-reference divergence profiles be trusted? |
| Primary estimand | Profile correlation, \(\rho_P\) |
| Secondary scale | The historical \(C\) scale, reported with profile coefficients of variation when used |
| Current stage | Active manuscript development and reproducibility audit |
| Role | Independent research project and implementation |
| Main methods | Complete influence-function inference, model-specific failure analysis, paired simulations, and local conditioning diagnostics; permutation/resampling studies are supporting historical evidence |

This repository began as a finite-sample simulation study of the
correlation-of-divergency coefficient, `c_delta`. It now supports a separate
Yao–Hoorn methodological manuscript focused on inference reliability for
profiles defined around robust references.

The motivating all-to-all coefficient remains associated with the earlier
[arXiv predecessor](https://arxiv.org/abs/2510.16717). The current project does
not claim that robust-reference profiles are universally superior; it studies
the conditions under which their inferential behavior is reliable or unstable.

## Current Evidence

The current theoretical and simulation work supports four bounded conclusions:

1. **Pointwise inference for the specified reference chain.**
   At a fixed regular IID paired law, the complete median/MAD/Huber and
   profile-moment expansion supports a consistent paired studentizer. A
   separate reduced-moment weak-null result uses empirical-norm control.
   These are asymptotic statements, not finite-sample calibration guarantees.

2. **Correlated location errors and additional full-chain amplification.**
   The shared-sign counterexample has zero population profile correlation.
   Correlated fitted-location errors can appear even with population scale
   fixed; full median/MAD/Huber fitting can amplify the distortion. The
   stage-2-to-stage-4 contrast does not separately identify a MAD effect.

3. **Persistent undercoverage in the examined regular skew studies.**
   Some regular null cells are compatible with nominal rejection, but have
   population nuisance cancellation. Both nonzero skew studies have active
   reference coefficients, near-cancellation in total variance, and
   persistent undercoverage over the examined sample sizes. They do not
   establish a mathematical convergence rate or successful practical
   calibration with materially active nuisance variance.

4. **Supplementary diagnostics have limited explanatory scope.**
   The standardized nuisance-Jacobian index organizes some bridge behavior;
   it is not a universal cutoff. Permutation results remain supporting
   empirical evidence, without a proved conditional weak-null limit for
   this generated-profile statistic.

These statements deliberately separate theorem-level results, exact
finite-dimensional calculations, and empirical simulation evidence.

## Repository Guide

| Location | Purpose |
|---|---|
| [`src/`](src/) | Core statistical implementation |
| [`scripts/`](scripts/) | Simulation, diagnostic, and audit entry points |
| [`tests/`](tests/) | Regression, mathematical-consistency, and pipeline tests |
| [`results/`](results/) | Stored simulation outputs and reporting tables |
| [`figures/`](figures/) | Generated figures used in analysis and reporting |
| [`docs/`](docs/) | Public research notes, audits, and research decisions |
| [`TEST_PLAN.md`](TEST_PLAN.md) | Testing strategy and planned validation |

## Local-only author materials

Supervisor correspondence and working-paper sources are kept locally and are
excluded from Git. Store future private emails and author packages in `private/`;
the existing local draft paths are also ignored. Generated PDFs remain ignored.
This repository distributes research code and simulation evidence, not the
working paper or private correspondence.

Historical manuscript-rendering scripts and document-specific tests require
these local-only inputs and cannot all run from a public clone alone. Their
presence in the repository does not publish the associated author materials.

## Key Research Documents

- [Closest-prior overlap and bounded novelty review](docs/novelty_overlap_review_20260926.md)
- [Adversarial internal proof review and local repairs](docs/proof_adversarial_review_20260926.md)
- [Retained-evidence interfaces and targeted checks](docs/evidence_adversarial_review_20260926.md)
- [Focused target table and literature checks](docs/target_literature_review_20260920.md)
- [Retained-evidence reproduction, Pareto formula comparison and independent review package](docs/manuscript_update_20260918.md)
- [Current manuscript review and complete reproduction of two core studies](docs/manuscript_review_20260916.md)
- [S1 proof integration and optional residual-checked API](docs/score_checked_integration_20260915.md)
- [Interface closure and claim/proof/source crosswalk](docs/manuscript_interface_crosswalk_20260911.md)
- [Manuscript skeleton and readiness audit](docs/manuscript_skeleton_and_readiness_20260829.md)
- [Archive and Section 3 readiness audit](docs/archive_and_section3_readiness_20260831.md)
- [Paper-level claim ledger](docs/manuscript_claim_ledger_20260826.md)
- [End-to-end pipeline audit](docs/end_to_end_pipeline_audit_20260822.md)
- [Active-nuisance validation and claim refinement](docs/active_nuisance_validation_20260907.md)
- [High-standard referee review and open issues](docs/referee_readiness_review_20260908.md)
- [Supervisor-directed four-stage reference-pathway results](docs/reference_pathway_results_20260909.md)
- [Short shared-sign model result and bounded rate heuristic](docs/shared_sign_model_result_20260909.md)
- [Completion review, proof/evidence reconciliation and placement decisions](docs/manuscript_completion_review_20260910.md)

## Reproducibility

Run the test suite from the repository root:

~~~bash
python3 -m pytest -q
~~~

Individual simulations and audits are available in [`scripts/`](scripts/).
The repository is currently research code rather than a packaged software
release. The primary \(\rho_P\) inference API is now public in `src/cdelta.py`;
a consolidated dependency specification for all historical runners remains
part of the software-readiness work. The bounded manuscript audit has its own
tested [package lock](requirements-manuscript-audit-lock.txt). Author-document
audits additionally require local-only materials.
