# Finite-Sample Permutation Resolution

The small-sample simulations suggest a finite-sample issue that is not a failure
of `c_delta` itself, but a property of permutation testing when a single
dominant paired extreme value defines most of the divergence structure.

If one extreme pair dominates both divergence vectors, then a random permutation
of `y` has roughly `1/n` probability of accidentally placing the extreme `y`
value back at the same index as the extreme `x` value. When this happens, the
permuted statistic can be close to the observed statistic. This creates a
finite-sample resolution floor for the permutation p-value: even when the
observed co-divergence is structurally strong, the permutation null may contain
a nontrivial fraction of similarly strong alignments.

This helps explain why, for small samples such as `n = 15` or `n = 20`, increasing
the magnitude of a single matched extreme value does not necessarily push the
rejection rate all the way to one. The divergence-vector correlation can become
very high, while the permutation test still has limited resolution because the
dominant pair can be recreated by chance under permutation.

The multi-extreme setting tests whether this limitation changes when the group
structure is defined by a small subgroup rather than a single observation. If
there are `k` co-occurring extreme observations, then the probability of a
random permutation preserving the whole extreme subgroup is approximately
`1 / choose(n, k)`, which is much smaller than `1/n` once `k` is two or three.
In the basketball analogy, this is the difference between one Michael Jordan and
a small all-star subgroup. The latter may define a more stable structural
pattern under permutation testing because the entire subgroup is much less
likely to be accidentally reconstructed by a random re-pairing.

The current interpretation is therefore:

1. `c_delta` can detect a single dominant co-divergent observation.
2. In small samples, the permutation p-value may be limited by the chance that
   permutation recreates the dominant pair.
3. Multiple matched extreme observations should reduce this permutation
   resolution problem because accidental reconstruction becomes combinatorially
   less likely.
4. Mismatched extreme subgroups remain an important control: both datasets may
   contain an all-star subgroup, but if those observations do not occur at the
   same paired indices, there is no co-divergence structure.
