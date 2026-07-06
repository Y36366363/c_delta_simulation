Dear Professor Hoorn,

Thank you for your last message. I apologize that my reply has been a little
slow; over the past two weeks I have been revisiting the relevant parts of the
`c_delta` paper more carefully, especially the sections on normalization,
outlier sensitivity, permutation testing, bootstrap intervals, and the suggested
reporting items. I also started turning my understanding into a small
reproducible simulation framework.

I agree that I should now make a concrete choice rather than keep all possible
extensions open. I would like to start with the simulation studies as the first
project stage, since they seem most urgent and can also clarify several of the
other issues. My initial plan is to build a reproducible simulation framework
for the finite-sample behavior of `c_delta` under normal, heavy-tailed, skewed,
and contaminated settings. For each setting, I would report the raw `c_delta`,
the sample-dependent normalized value, the correlation between divergence
vectors, permutation-based p-values, and bootstrap confidence intervals.

Before treating outliers as something to remove or down-weight, I will first
study your `h*` paper and use it to think about whether an extreme observation is
itself informative. This should help separate meaningful exceptional values from
values that merely destabilize the statistic.

The current prototype includes a first implementation of `c_delta`, a
sample-dependent pairing normalization, a permutation test, paired bootstrap
intervals, several basic data-generating mechanisms, and sanity tests such as
scale invariance and zero-divergence behavior. My next step will be to expand
this into repeated simulation tables and then use those results to decide which
robust or weighted variant is sensible.

For the machine-learning framing, my current thought is that `c_delta` may be
useful when the object of interest is not direct prediction agreement but
similarity of internal dispersion structures, for example in model residuals,
embedding spaces, representation clusters, or human-AI response patterns. I will
keep this framing in mind while building the simulations, but I will first focus
on getting the statistical behavior clear.

Please let me know if this is a reasonable first direction, or if you would
prefer me to prioritize a different simulation setting.

Sincerely,
Jialiang Yao
