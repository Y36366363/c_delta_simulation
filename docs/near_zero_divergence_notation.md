# Near-Zero Divergence Notation

The notation question concerns how to describe the boundary case where empirical
divergence vanishes. The most precise object in the current implementation is
not a generic scalar `x`, but the empirical divergence scale in the denominator:

```text
Dbar_x * Dbar_y -> 0+
```

In LaTeX form:

```tex
\bar D_x \bar D_y \to 0^+
```

This is preferable to writing only `x approx 0`, because `x approx 0` is
descriptive but not mathematically specific. It is also preferable to writing
the boundary as a literal `0/x` limit, because the statistic is scale invariant
for positive divergence scales. If both samples retain the same internal
divergence shape while their scale shrinks by a positive factor epsilon, both
the numerator and denominator shrink together and the ratio remains stable.

The problem occurs at the empirical boundary where the data no longer contain
observable internal divergence. At that point, the comparison is not a
meaningful numerical `c_delta` value. It should be reported as:

```text
undetermined due to data limitations
```

Suggested prose for the report:

```text
When the empirical divergence scale approaches zero, i.e.,
\bar D_x \bar D_y \to 0^+, c_delta reaches a resolution-limited boundary case
rather than a meaningful numerical comparison.
```

The accompanying boundary simulation confirms the intended interpretation:
for positive epsilon, `c_delta` remains stable as the divergence scale approaches
zero; at epsilon equal to zero, the implementation reports the result as
undetermined due to data limitations.
