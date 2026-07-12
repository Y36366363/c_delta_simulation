# Large-Scale Simulation Summary

The large-scale simulation extends the multi-extreme setting to `n = 100, 250,
500` under normal, Student-t with 3 degrees of freedom, and log-normal
backgrounds. The permutation test was optimized by computing the divergence
vectors once and permuting `D_y` directly. This makes larger sample-size runs
feasible without changing the statistical null: the test still breaks the
pairing between `D_x` and `D_y`.

Main observations:

1. Matched extreme subgroups remain detectable in large samples under normal
   and log-normal backgrounds. With magnitude 8, rejection rates were 1.0 across
   `n = 100, 250, 500` for `k = 1, 2, 3` matched extremes.
2. Heavy-tailed backgrounds reduce the contrast of a single fixed-magnitude
   extreme value. Under the `t3` background at `n = 500`, one matched extreme had
   rejection rate 0.425, while two and three matched extremes increased the
   rejection rates to 0.900 and 0.975.
3. Mismatched extreme subgroups remain close to nominal null behavior. This
   supports the interpretation that `c_delta` targets co-occurring internal
   divergence structure, not merely the presence of large values in both
   samples.
4. As `n` increases with fixed magnitude, the mean divergence-vector correlation
   can decrease because a fixed number of extreme observations becomes a smaller
   part of the total group. This suggests that future power curves should vary
   both sample size and either magnitude or subgroup size.

The practical implication is that large-sample behavior depends on how the
structural signal scales. A single fixed-magnitude extreme may be enough under
normal or skewed backgrounds, but under heavy-tailed backgrounds a small
co-occurring subgroup is more reliable.
