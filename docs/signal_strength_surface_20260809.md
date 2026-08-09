# Node-Strength by Dyad-Strength Crossover Surface

Date: 2026-08-09

## Pre-Experiment Project Check

Before adding this study, all 85 existing unit tests passed, all Python files
under `src`, `scripts`, and `tests` compiled, `git diff --check` was clean, and
the working tree contained no uncommitted changes. The surface experiment was
therefore built on the verified 2026-08-08 specification.

## Question

The previous one-dimensional mixture fixed latent node-radius correlation at
`.55` and dyadic signed-value correlation at `.70`, producing a Huber-profile
versus Mantel crossover near dyadic variance weight `.216`. The present study
asks whether the crossover (w^\star) is approximately determined by a ratio
of node and dyadic signal strengths.

The simple candidate is

```text
logit(w*) = a + b log(node strength / dyad strength).
```

A Fisher-z ratio is also tested. A less restrictive comparison model allows
log Fisher-z node and dyad strengths to enter separately. Under a genuine
ratio-only relationship, the two separate coefficients should be similar in
magnitude and opposite in sign.

## Design

The surface contains nine signal cells:

- latent node-radius correlations `.35, .55, .75`; and
- latent dyadic-value correlations `.45, .65, .80`.

Each cell uses the same four-building, twelve-room design and within-building
permutation scheme as the earlier mixture study. The coarse phase scans twelve
dyadic variance weights from 0 to 1 with 300 datasets and 199 permutations per
point. Each estimated crossover is then locally refined at `.025` resolution
with two independent 400-dataset runs. The combined local results contain 800
datasets per ordinary cell and weight.

One cell (`node=.35`, `dyad=.65`) did not retain the coarse bracket after the
two refined seeds were combined. It was not silently omitted. A targeted
extension over weights `0-.175` used two further 600-dataset runs, giving
1,200 datasets per extension point and a valid final crossover.

## Final Crossover Surface

| Node strength | Dyad strength | Strength ratio | Crossover (w^\star) | Zero-difference band |
| ---: | ---: | ---: | ---: | ---: |
| .35 | .45 | .778 | .150 | [.125, .200] |
| .35 | .65 | .538 | .170 | [.125, .175] |
| .35 | .80 | .438 | .148 | [.100, .150] |
| .55 | .45 | 1.222 | .228 | [.200, .325] |
| .55 | .65 | .846 | .234 | [.175, .250] |
| .55 | .80 | .688 | .211 | [.175, .225] |
| .75 | .45 | 1.667 | .304 | [.275, .350] |
| .75 | .65 | 1.154 | .253 | [.225, .300] |
| .75 | .80 | .938 | .280 | [.250, .300] |

The dominant surface pattern is vertical by node strength:

- node `.35`: crossovers `.148-.170`;
- node `.55`: `.211-.234`; and
- node `.75`: `.253-.304`.

Changing dyad strength within a node row does not create a stable monotone
shift. For example, at node `.35`, increasing dyad strength from `.45` to
`.65` moves the estimate upward before it returns to `.148` at dyad `.80`.
This alone contradicts a deterministic one-ratio ordering.

## Ratio-Model Test

The response is the logit of the estimated crossover.

| Model | In-sample R-squared | Logit RMSE | LOOCV logit RMSE | Maximum LOOCV error |
| --- | ---: | ---: | ---: | ---: |
| Raw strength ratio | .686 | .176 | .202 | .431 |
| Fisher-z strength ratio | .644 | .187 | .215 | .457 |
| Separate Fisher-z strengths | .938 | .078 | .118 | .197 |

The separate model is

```text
logit(w*) = -0.940
             + 0.756 log(atanh(node strength))
             - 0.093 log(atanh(dyad strength)).
```

The coefficient sum is `.663`, far from the zero implied by equal-and-
opposite ratio coefficients. Leave-one-cell-out prediction remains materially
better for the separate model, so its improvement is not explained only by
adding one predictor.

## Conclusion

The tested hypothesis is not supported in its simple form. The crossover is
not well described by node/dyad signal ratio alone. In the current parameter
range, absolute node strength moves the transition substantially, whereas the
incremental dyad-strength effect is smaller and nonmonotone.

This result is plausible because the mixture weight already directly controls
the variance allocated to the dyadic component. Increasing dyadic latent
correlation then changes Mantel power, but profile statistics also respond to
correlated signed values and Mantel also responds to node-induced star dyads.
The two signals are not orthogonal in the observable statistics, so a simple
balance-of-two-independent-signals formula is too restrictive.

The fitted separate model is descriptive, not a new decision rule. Nine cells
are insufficient for a general response-surface theorem, and using an
estimated mixture to select the test after observing data would create
post-selection error.

## Implications for the Definition Discussion

1. Method choice should remain estimand-first: node salience suggests a
   profile method; complete dyadic geometry suggests Mantel/QAP.
2. There is no supported universal strength-ratio threshold for choosing
   between them.
3. Huber `c_delta_star` and Huber-profile Pearson remained permutation-
   equivalent throughout the surface, so the `CV_X CV_Y` construct question
   remains separate.
4. A mixed scientific question may justify reporting both pre-specified
   estimands rather than using simulation to choose one after seeing results.

## Next Useful Checks

- Add one intermediate node strength and one lower dyad strength to determine
  whether the weak dyad coefficient is specific to the current grid.
- Repeat a reduced surface at `n=96` to separate sample-size effects from the
  signal geometry.
- Derive population or large-sample approximations for the pure node and pure
  dyad effect paths before fitting a larger empirical surface.
- Do not expand to MRQAP until a concrete multi-predictor dyadic research
  question is specified.

Detailed outputs:

- `results/signal_strength_surface_coarse_20260809.tsv`
- `results/signal_strength_surface_refined_20260809.tsv`
- `results/signal_strength_surface_replication_20260809.tsv`
- `results/signal_strength_surface_extension_combined_20260809.tsv`
- `results/signal_strength_surface_final_combined_20260809.tsv`
- `results/signal_strength_surface_crossovers_20260809.tsv`
- `results/signal_strength_ratio_models_20260809.tsv`
- `results/signal_strength_ratio_predictions_20260809.tsv`

Implementation:

- `scripts/run_signal_strength_surface_20260809.py`
- `scripts/run_signal_strength_extension_20260809.py`
- `scripts/summarize_signal_strength_surface_20260809.py`
