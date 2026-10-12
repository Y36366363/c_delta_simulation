# Selective revision after external AI feedback — 12 October 2026

The user supplied another AI's review and requested useful changes rather
than automatic acceptance. The review is treated as suggestions to verify,
not independent expert certification. The previous author revision is preserved.

## Decisions

| Suggestion | Assessment and action |
|---|---|
| Ambiguous abstract opening | Accepted: prior magnitude/fitted-centre work is now explicitly antecedent work. |
| Keyword | Replaced `generated profiles` with `fitted-reference distance profiles`. |
| Finite-sample undercoverage | Added an abstract sentence and concise Discussion statement that no finite-sample calibration correction or higher-order explanation is provided. Kept the user's exact two-sentence regular/shared-sign limitation. |
| Local score slope | Existing S1.7 already had the argument; added the fixed inner-interval inequality and explicit high-probability bound to make it checkable. No new assumption or theorem scope. |
| KDE / class / squared-IF review | Existing proofs address these issues. No new flaw was demonstrated by the supplied review. Retained independent-review priorities rather than adding unsupported conditions or claiming review completion. |
| Oracle-form SE | Qualified: a proved unit-variance CLT immediately gives constant SE n^(-1/2); a data-dependent variance additionally requires consistency. Neither alternative full-fit procedure is evaluated here. |
| Formal pending fixed-tau proposition | Not adopted: the candidate remains separate, not a formal established manuscript theorem. |
| Afuecheta spelling | Alleged misspelling not found in source or PDF; existing spelling is correct. |
| S4.3 last row | No broken/missing row found. Improved row spacing, Reflection column width and final-row separation; clarified the reference ingredients. |
| Software prose | Neutralized internal terminology in main text. Moved API options and validation chronology from S1.7 to computational S3.9, retaining essential mathematical and finite-precision limits. |
| Main/supplement structure | Already matches most suggestions; kept Hoorn's six-section main structure and S1–S4. |

The explicit slope argument chooses epsilon with
p=P(|W−T|≤cs−3 epsilon)>0. Consistency makes the fitted scale and both
root endpoints close enough that the entire segment has active fraction
at least the fixed inner interval's empirical mass. The LLN gives p/2,
and scale boundedness turns C0/n residual into O_P(n^−1) location error.
This does not certify all numerical fits or fixed-precision termination.

## Artifacts and validation

New author folder, outside the repository:

`/Users/jialiangyao/.codex/visualizations/2026/09/11/01a08f53-8ee3-7dc0-87fd-0a3628d3098f/rho_p_review_refinement_20261012/`

Contains standalone source, PDF, Overleaf ZIP and the separate review notes.
The native compiler succeeded; the PDF was exported with the existing local
TeX installation. Source reconciliation was rerun with `/opt/anaconda3/bin/python`:
23 numerical tables / 1,270 cells, citation/label checks, six main sections,
172 historical checks, and frozen-file hashes passed. The qualitative target
comparison table is separately visually checked and is not counted among
the 23 numerical displays. The final delivery manifest records page count,
visual checks, artifacts and hashes.

- Audit: `results/manuscript_ai_feedback_audit_20261012.json`.
- Delivery: `results/manuscript_ai_feedback_delivery_20261012.json`.
- No new Monte Carlo study, root-certificate replay, production-code change,
  or dependency installation. This is not a newly isolated reproduction.
- Internal mathematical checks found no new issue in the added inequality
  or conditional SE wording; independent mathematical review remains pending.
