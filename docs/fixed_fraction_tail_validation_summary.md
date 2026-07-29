# Fixed-k versus Fixed-Proportion Tail Validation

Date: 2026-07-29

This update extends the earlier sample-size comparison across a finer
heavy-tail gradient. The purpose is to distinguish a genuine sample-size
effect from dilution caused by holding the matched subgroup size fixed as
`n` increases.

## Design

The script `scripts/run_fixed_fraction_tail_validation.py` compares:

- divergence definitions `l2` and `l1`;
- normal, `t5`, `t4`, `t3`, `t2.5`, `t2.2`, and `t2` backgrounds;
- sample sizes `n = 40, 80, 160`;
- fixed `k = 2` versus fixed subgroup proportion `k / n = 0.05`;
- matched magnitude `6`;
- 300 repetitions and 299 permutations per setting.

The two designs share seeds within each `kind/background/n` setting. At
`n = 40`, both designs have `k = 2` and therefore provide an exact internal
check: their results are identical.

## Main Result

The distinction between fixed `k` and fixed proportion persists across the
tail gradient and under both divergence definitions.

For the more informative heavy-tail settings:

| Kind | Background | Fixed-k power, n=40 | Fixed-k power, n=160 | Fixed-proportion power, n=40 | Fixed-proportion power, n=160 |
|---|---|---:|---:|---:|---:|
| l2 | t3 | 0.8067 | 0.7067 | 0.8067 | 0.9633 |
| l2 | t2.5 | 0.6867 | 0.3767 | 0.6867 | 0.8833 |
| l2 | t2.2 | 0.5500 | 0.1800 | 0.5500 | 0.6833 |
| l2 | t2 | 0.3833 | 0.1233 | 0.3833 | 0.4700 |
| l1 | t3 | 0.8633 | 0.6633 | 0.8633 | 0.9633 |
| l1 | t2.5 | 0.6833 | 0.3567 | 0.6833 | 0.8900 |
| l1 | t2.2 | 0.5267 | 0.1867 | 0.5267 | 0.7233 |
| l1 | t2 | 0.3900 | 0.1267 | 0.3900 | 0.5300 |

At `n = 160`, the fixed-proportion minus fixed-k power gap ranges from
`0.2566` to `0.5366` for `t3` through `t2` backgrounds. The pattern is
similar for `l2` and `l1`.

For example, under a `t2` background:

- `l2` fixed-`k` power decreases from `0.3833` at `n = 40` to `0.1233`
  at `n = 160`, while fixed-proportion power changes from `0.3833` to
  `0.4700`;
- `l1` fixed-`k` power decreases from `0.3900` to `0.1267`, while
  fixed-proportion power increases from `0.3900` to `0.5300`.

The `n = 160`, `t2` Wilson intervals also separate clearly:

- `l2`: fixed `k`, `[0.0908, 0.1654]`; fixed proportion,
  `[0.4143, 0.5265]`;
- `l1`: fixed `k`, `[0.0937, 0.1691]`; fixed proportion,
  `[0.4735, 0.5857]`.

Normal and moderately heavy `t5` settings remain near ceiling under both
designs. They are therefore less informative about sample-size trends.

## Interpretation

The results support a more precise statement:

> Increasing sample size is not inherently harmful to detection. When the
> matched subgroup size remains fixed, its fraction of the sample decreases
> and the sparse co-divergence signal can be diluted. Holding the subgroup
> proportion fixed changes this pattern and generally preserves or increases
> power.

The heavy-tail and sparse-signal effects also interact. Fixed-proportion
power remains lower under the heaviest backgrounds than under normal or
moderately heavy backgrounds, consistent with the earlier
signal-to-background-divergence-noise explanation. Increasing the subgroup
size offsets part, but not all, of the heavy-tail power loss.

## Reporting Recommendation

Future sample-size simulations should always state whether `k` or `k / n` is
held fixed. A fixed-`k` decline should be described as sparse-signal dilution,
not as evidence that larger samples make `c_delta` less reliable.
