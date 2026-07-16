# Research Questions and Next Checks

This note keeps the simulation work aligned with Professor Hoorn's latest
feedback and separates mathematical claims from empirical checks.

## Active Questions

| Question | Why it matters | Current status | Next check |
| --- | --- | --- | --- |
| What is the right notation for the zero-divergence boundary? | The statistic should not be described as a computational error when empirical divergence vanishes. | Use `\bar D_x \bar D_y \to 0^+` and report "undetermined due to data limitations" at the empirical boundary. | Keep notation consistent in the next report. |
| Is the subgroup-size effect only a permutation-resolution effect? | Larger `k` increases both signal strength and changes the permutation overlap layers. | Added lower-target calibrated alternatives at target correlations `0.35`, `0.55`, and `0.65`; then repeated the non-ceiling `0.35` setting under `l1`. The pattern broadly persists under `l1`, while t3 remains flatter across `k`. | Add a rank-based variant or compare exact overlap layers at target `0.35`. |
| Is `1 / choose(n, k)` a p-value? | Professor Hoorn clarified that it is a layer probability, not the permutation p-value. | Overlap-layer diagnostics now report overlap count, layer probability, and share above the observed statistic. | Extend the layer diagnostic across magnitudes and backgrounds. |
| Is the mismatched condition a valid null? | A deliberately disjoint condition is a negative control, not a genuine null distribution. | Independent-null simulation now samples extreme indices independently and allows chance overlap. | Use independent-null results for Type-I statements; use disjoint mismatch only as a negative control. |
| Does raw `c_delta` have a zero-centered permutation null? | It does not; the mean raw statistic across permutations equals `n`. | Exact enumeration confirms the permutation mean equals `n` for small `n`. | Report raw `c_delta`, normalized pairing, correlation, and p-value separately. |
| Are the findings specific to squared divergence? | Squared divergence can amplify sparse extremes. | L1/L2 comparison shows the qualitative matched-vs-null pattern survives under `l1`. | Add a rank-based divergence-vector comparison. |
| Do heavy-tailed or skewed backgrounds change detectability? | Backgrounds with natural extremes may make sparse structural signals harder to separate. | `t3` weakens power relative to normal/lognormal in the L1/L2 variant comparison. | Run calibrated power curves under `t2`, `t3`, and lognormal backgrounds. |
| Does larger sample size create over-sensitivity? | Large samples may make weak structural signals detectable, but true over-sensitivity would show up as inflated independent-null rejection. | Sample-size sensitivity at target correlation `0.35` shows power often saturating by `n = 80` or `160`, while independent-null behavior mostly remains close to `.05`. The main flagged row is `l1/lognormal/n=160/k=1`, with rejection `.0767`. | Re-run the flagged large-n lognormal null setting with more replications and more permutations. |
| What does magnitude `8` mean relative to background scale? | Magnitude should be interpreted relative to the background distribution, not as a free-standing number. | Current simulations use standardized or unit-scale backgrounds. | Add a table showing where magnitude `8` falls in each background's empirical quantiles. |

## Suggested Priority

1. Calibrate alternatives across `k = 1, 2, 3` so that subgroup-size comparisons
   are not confounded by signal strength.
2. Add rank-based checks after the L1/L2 comparison.
3. Extend overlap-layer diagnostics across magnitude and background.
4. Add a short table translating fixed magnitudes into background quantiles.
