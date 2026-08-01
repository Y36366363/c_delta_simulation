# High-Replication Meeting Addendum

## Short update to say aloud

I reran the paired-overlap experiment with 1,000 repetitions per condition and
independent seeds. The overlap-power gradient was monotone under L1 and L2 and
under normal, t3, and t2 backgrounds. I also added a proper random-set null in
which both datasets contain four strong standouts but their indices are chosen
independently. Its rejection rates remained between `.0377` and `.0493`.

## Why this matters

The disjoint case is a useful negative control, but it is not the formal null
because it suppresses chance overlap. Under the proper null, overlap follows a
hypergeometric distribution with expected value `k^2/n`. Rare chance-overlap
samples can reject, but the unconditional test remains calibrated.

## Possible formulation

> The statistic responds to paired salience overlap above the level expected
> under random pairing, with detection strength determined by the continuous
> contrast between aligned salience and background divergence noise.

## Question for Professor Hoorn

Would it help the revision to separate the binary overlap intuition from the
continuous estimand and from the permutation null, perhaps in a short theory or
interpretation subsection?
