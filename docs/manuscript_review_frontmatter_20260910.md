# Robust-reference profile correlation: pointwise inference and finite-sample limits

Jialiang Yao and Johan F. Hoorn

Internal first-draft reading entry, 2026-09-10. Provisional abstract and
assembly order for author review, not a submission-ready manuscript or an
approved replacement for Hoorn's Introduction. No real application is claimed.

## Provisional abstract

Paired observations can be associated through their magnitudes of departure
from marginal reference locations, even when signed association is not the
scientific target. We study profile correlation defined from absolute
deviations about median/MAD-scaled Huber references. Because the references
are estimated from the same pairs used to form the profiles, inference must
account jointly for reference fitting and profile moments. Under fixed
regular IID laws, we derive a complete influence-function expansion and
consistent studentization, yielding pointwise asymptotic Wald inference.
A shared-sign construction has independent profiles at the population
references but can exhibit severe fitted-profile bias and empirical null
rejection distortion. A staged comparison separates correlated location
errors that persist at fixed population scale from additional amplification
under complete median/MAD fitting. A short model-specific result identifies
the failure of median regularity despite a nonzero population Huber slope.
A standardized local conditioning index organizes part of the empirical
bridge transition, but does not determine finite-sample behavior or provide
a universal cutoff. A regular nonzero-effect skew example also exhibits
slow convergence and undercoverage, including with population references
fixed. The contribution is a pointwise inferential foundation and a worked
analysis of finite-sample limits, not a generally calibrated finite-sample
procedure, a weak-null permutation theorem, or globally robust correlation.

## Ordered working draft

1. [Introduction and estimand, Sections 1--2](manuscript_draft_sections_1_2_20260830.md).
   Introduction is provisional pending Hoorn's revision.
2. [Theory, failure and local conditioning, Sections 3--5](manuscript_draft_sections_3_5_20260904.md).
3. [Evidence and displays, Section 6](manuscript_draft_section_6_20260905.md).
   Legacy display numbering is retained pending the proposed supplement move.
4. Section 7: optional; omitted unless the paired-IID application gate passes.
   If omitted in the final manuscript, renumber Discussion at typesetting.
5. [Discussion, currently Section 8](manuscript_draft_section_8_20260908.md).
6. [Regular inference Appendix A](appendix_asymptotic_theory_20260819.md)
   and [short shared-sign model proof](shared_sign_model_result_20260909.md).

This entry collects the existing manuscript into one reading sequence rather
than duplicating chapter text that could drift out of sync. It is not a
compiled or typeset PDF. [Completion review and decisions](manuscript_completion_review_20260910.md)
record the proposed S1--S3 allocation and unresolved mathematical/software
review gates. The next author-facing deliverable is a continuously edited
integrated draft, not another general simulation grid.
