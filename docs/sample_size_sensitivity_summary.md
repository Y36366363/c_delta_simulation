# Sample-Size Sensitivity Summary

This run studies whether the lower-target calibrated findings change
substantially as sample size increases. The practical concern is whether larger
samples simply improve power under matched structure, or whether the procedure
starts to over-reject under independent-null conditions.

## Design

```text
target correlation = 0.35
sample sizes = 20, 40, 80, 160
k = 1, 2, 3
kinds = l2, l1
backgrounds = normal, t3, lognormal
scenarios = matched, independent_null
calibration repetitions = 120
evaluation repetitions = 300
n_perm = 499
alpha = .05
```

The target correlation `0.35` is used because earlier lower-target calibration
showed that `0.55` and `0.65` were still close to ceiling under the normal
background.

## Matched Power by Sample Size

```text
kind   background   k   n=20   n=40   n=80   n=160   first saturation
l2     normal       1   .350   .630   .973   1.000   80
l2     normal       2   .540   .667   .937   1.000   160
l2     normal       3   .633   .787   .990   1.000   80
l2     t3           1   .310   .513   .733   .750    none <= 160
l2     t3           2   .383   .573   .787   .953    160
l2     t3           3   .407   .700   .720   .940    none <= 160
l2     lognormal    1   .153   .390   .920   .997    160
l2     lognormal    2   .460   .677   .787   1.000   160
l2     lognormal    3   .187   .457   .997   1.000   80
l1     normal       1   .380   .660   .853   1.000   160
l1     normal       2   .587   .687   .950   1.000   80
l1     normal       3   .610   .800   .843   1.000   160
l1     t3           1   .293   .513   .847   .757    none <= 160
l1     t3           2   .373   .590   .793   .957    160
l1     t3           3   .400   .573   .873   .957    160
l1     lognormal    1   .180   .373   .887   1.000   160
l1     lognormal    2   .190   .703   .987   1.000   80
l1     lognormal    3   .227   .487   .997   1.000   80
```

## Independent-Null Calibration

Most independent-null rejection rates remain close to alpha `.05`. Two rows
are worth monitoring:

```text
kind   background   n     k   rejection rate   Wilson interval
l1     lognormal    20    2   .0233            [.0113, .0474]
l1     lognormal    160   1   .0767            [.0516, .1124]
```

The second row is the more relevant warning sign because the rejection rate is
above `.05` and the Wilson interval barely excludes `.05`. This should be
treated as a possible over-sensitivity point under the `l1` lognormal large-n
setting, not as a final conclusion.

Follow-up note: after the normalization correction, this flagged condition was
re-run with 1,000 replications and 999 permutations. The empirical size at
alpha `.05` was `0.053`, with Wilson interval `[0.0407, 0.0687]`, so the
earlier warning is less concerning.

## Interpretation

- Larger sample sizes strongly increase matched power even after calibrating
  the mean divergence-vector correlation to `0.35`.
- Saturation often appears by `n = 80` or `n = 160`, especially under normal and
  lognormal backgrounds.
- The heavy-tailed `t3` background delays saturation, especially for `k = 1`.
  This supports the earlier observation that natural heavy-tailed variation can
  blur sparse co-divergence signals.
- Most independent-null checks remain near nominal size, so the main large-n
  pattern looks more like increased statistical power than generic overfitting.
- The earlier potential over-sensitivity region was large-n lognormal data
  under `l1`, especially `n = 160, k = 1`, where independent-null rejection
  reached `.0767`. A higher-replication follow-up reduced this to `.053`.

## Practical Boundary

For the current simulation design, the most useful reporting boundary is:

```text
At target correlation 0.35, n = 20 to 40 remains a genuinely finite-sample
region, n = 80 is a transition region where several matched conditions begin
to saturate, and n = 160 is often a high-power or saturated region. We do not
yet see broad null over-rejection, but the l1/lognormal/n=160 case should be
checked with more replications and possibly more permutations.
```

## Next Check

The next check can shift from this flagged case to regenerating selected raw
tables under the corrected scale, or to adding a rank-based variant.
