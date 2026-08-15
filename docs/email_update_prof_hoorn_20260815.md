Subject: Update on c_delta*: component inference and the building-level boundary

Dear Professor Hoorn,

I have continued the simulations by separating two questions more explicitly: whether the same observations are salient across the two measurements, and whether the complete pairwise distance geometry is similar. I use the Huber/MAD profile statistic for the first question and Mantel for the second. A combined maximum statistic can test whether either type of agreement is present, but its “winner” should only be interpreted as stronger relative evidence, not as proof of a unique mechanism.

The main recent progress concerns inference for the two components. I implemented a fully recomputed studentized permutation procedure: for every permutation, all pairing-dependent influence-function and variance terms are recalculated. In iid simulations, the resulting local p-values, followed by Holm adjustment, were well calibrated under the tested global and partial nulls. At n = 80, the familywise error ranged from .030 to .050 in the main confirmatory models. A new stress test with heavy-tailed and strongly skewed margins gave familywise error between .020 and .053 in the regular scenarios. This is encouraging, although I would still describe it as a pointwise iid candidate rather than a general theorem.

The stress test also found a useful boundary. When the robust radius profiles had almost no genuine variation, estimation error in the Huber/MAD reference dominated the profile itself. In that near-degenerate setting, the nominal profile test failed badly. I therefore think the method needs an explicit regularity screen: if the profile variance is too small or the robust centre/scale fit is unstable, the profile component should be reported as weakly identified or undetermined rather than assigned an ordinary p-value.

The building application remains a separate problem. Treating rooms as iid produced familywise error of .245 under Gaussian clusters and .369 under skewed building scales. Building-summed t inference improved the Gaussian case but still reached .074 under skewed scales, and the tested linearized sign-flip was invalid. I do not think we should claim formal component discovery for six buildings yet.

The next theoretical choice seems to be the building-level estimand. Should the target be an average of separate within-building profile/Mantel effects, or one global functional that includes cross-building dyads? The first is easier to interpret and permits one effect vector per building; the second is closer to the current pooled geometry but requires a new cluster-level U-statistic derivation. I would appreciate your view on which question is scientifically closer to the intended application.

I have attached a short technical note with the definitions, calibration results, failure boundary, and the precise decision that remains.

Kind regards,

Jialiang
