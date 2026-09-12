# Bounded manuscript-interface work

Recorded before the new numerical replay on 2026-09-12. Internal protocol,
not third-party preregistration. The authoritative manuscript is the user's
approved `rho_p_minimal_preview.pdf` and its matching single-file LaTeX at
`/private/tmp/rho_p_minimal_20260911/main.tex`. The September 11 integrated
Markdown/PDF is an evidence source, not the current editing base.

## Scope and predetermined replay

No new generating laws, sample sizes, seeds, simulation cells or permutations.
Retain frozen outputs and the public algorithm unchanged. For the existing
nonzero skew study replay replications 0, 1, 2, 10, 100, 500, 1000, 1500, 1999
at each of n=160,640,2560 (27 datasets). For the existing pathway study replay
replications 0,1,1999 at each of the four tau/n cells, plus the two previously
flagged tau=.10,n=640 replications 70 and 1622 (14 datasets). The added flags
are explicitly post hoc; the other IDs are fixed before this replay.

Compare all three skew methods and all four pathway stages against the saved
rows. For each dataset also compare the default full fit with a bracketed
Huber root at the same sample midpoint median and MAD, recomputing the entire
IF and both full/direct SEs. Record score residuals, scale-normalized root
gaps, estimate/SE changes and matching interval or rejection decisions.
Replay agreement is numerical provenance evidence, not calibration evidence.

Use a fresh Python 3.12 environment with NumPy 1.26.4, SciPy 1.16.3 and
pytest 7.4.4; report actual versions and environment isolation. Reconstruct
the displayed evidence from frozen sources. A bounded replay does not count
as rerunning all original Monte Carlo or permutation studies.

## Mathematical work

Supply an elementary uniform-on-band consistency argument for the exact
Gaussian KDE in the API, avoiding an unverified transfer from fixed to random
bandwidth results. Specify the paired quantile/Z route, closure operations,
and empirical versus population norms. Record remaining independent-review
obligations without describing internal checks as peer review.

## LaTeX and delivery

Add source-to-final-LaTeX table validation, with negative controls for changed
coverage, seed, missing/duplicated tables, and NA. Preserve the baseline
preamble, original four tables, theorem statement and original Introduction
paragraphs. New literature prose is a short integration input, pending Hoorn.
Compile the revised single-file manuscript and check layout. Keep manuscript
artifacts outside the scientific repository; only research audit materials
and scripts belong here. No push or overwrite of frozen files.
