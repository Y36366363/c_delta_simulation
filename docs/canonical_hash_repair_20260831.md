# Canonical evidence hash repair (2026-08-31)

## Finding

The four source tables behind `results/canonical_evidence_20260819.tsv` were
scientifically unchanged, but their byte-level SHA-256 values depended on line
endings. Python's `csv` writer materialized CRLF, whereas Git or another
checkout could materialize the same tabular text with LF. A raw-byte hash could
therefore mark all four sources stale without any change to a data value.

## Repair

Canonical source hashes now use a text-transport convention: replace CRLF and
lone CR with LF, then compute SHA-256. The freeze script, integrity audit, and
tests all call the same implementation. The frozen hashes are:

| Source table | Normalized SHA-256 |
|---|---|
| `studentized_permutation_stress_pilot_20260814.tsv` | `3bf7fabb1e4c9bd01d4dab943fc2e4ffd915762af96b9f58da16a29b799667b4` |
| `profile_regularity_comparison_pilot_20260816.tsv` | `174f5ae6cb3702936304cd97c9bccb312783221750a20bb8bd965d1918c1f951` |
| `profile_bridge_family_validation_pilot_20260817.tsv` | `1b176122b54f052b90ef1e515a230081c02d5cc3f689a44d75eecd8bcf10ddf9` |
| `profile_bridge_family_validation_confirmatory_20260817.tsv` | `ab537b63a9be503edfa0cef2612c525062851fb91bc8974e978a1cd0e428cd03` |

This convention remains sensitive to every tabular content change, including
field values, ordering, delimiters, and whitespace other than the line-ending
representation.

## Scientific invariants

Comparison with the preceding frozen table confirms that all 34 rows are
identical after excluding `source_sha256`. In particular, the evidence-group
labels, scenarios, sample sizes, fixed root seeds, rejection counts, Monte
Carlo standard errors, Wilson intervals, conditioning quantities, and notes did
not change. This is a reproducibility repair, not a rerun or reinterpretation
of the simulations.

## Guardrail

`test_canonical_hash_is_invariant_to_lf_and_crlf` constructs equivalent LF and
CRLF tables and requires their canonical hashes to match. The pipeline audit
also recomputes every source hash through the normalized implementation.
