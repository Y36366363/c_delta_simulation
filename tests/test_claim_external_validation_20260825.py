import csv

import numpy as np

from scripts.run_claim_external_validation_20260825 import PROJECT_ROOT
from scripts.run_nuisance_jacobian_20260817 import bridge_cdf, bridge_pdf
from scripts.run_profile_bridge_family_validation_20260817 import (
    sample_unit_origin_density_radius,
)


def _read(name: str) -> list[dict[str, str]]:
    with (PROJECT_ROOT / "results" / name).open(newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def test_hyperexponential_bridge_has_matched_origin_density_and_expected_mean():
    assert bridge_pdf(0.0, "hyperexponential") == 1.0
    assert bridge_cdf(0.0, "hyperexponential") == 0.0
    rng = np.random.default_rng(2026082502)
    sample = sample_unit_origin_density_radius(rng, 200_000, "hyperexponential")
    assert abs(float(np.mean(sample)) - 4.0 / 3.0) < 0.02


def test_claim1_oracle_reference_does_not_remove_strong_skew_distortion():
    rows = _read("claim1_oracle_reference_validation_20260825.tsv")
    assert len(rows) == 4
    for n in (640, 2560):
        subset = {row["reference_fit"]: row for row in rows if int(row["n"]) == n}
        assert abs(
            float(subset["refitted"]["rejection_rate"])
            - float(subset["oracle_fixed_population"]["rejection_rate"])
        ) < 0.01
        assert abs(
            float(subset["refitted"]["q025_z"])
            - float(subset["oracle_fixed_population"]["q025_z"])
        ) < 0.03
    assert all(float(row["wilson_95_low"]) > 0.05 for row in rows)


def test_claim2_shared_sign_coupling_has_monotone_effect_dose_response():
    rows = _read("claim2_sign_coupling_validation_20260825.tsv")
    for n in (80, 640):
        subset = sorted(
            (row for row in rows if int(row["n"]) == n),
            key=lambda row: float(row["shared_sign_coupling"]),
        )
        effects = [float(row["mean_refitted_profile_effect"]) for row in subset]
        centre_products = [float(row["mean_huber_center_product"]) for row in subset]
        assert effects == sorted(effects)
        assert centre_products == sorted(centre_products)
        assert effects[-1] - effects[0] > 0.60
        assert max(float(row["fixed_zero_rejection_rate"]) for row in subset) <= 0.10


def test_claim3_fifth_family_preserves_order_but_exposes_family_residual():
    rows = _read("claim3_prospective_family_validation_20260825.tsv")
    summary = _read("claim3_prospective_family_summary_validation_20260825.tsv")[0]
    # Near-duplicate indices (.446/.447 and .890/.892) need not order their
    # Monte Carlo rates exactly. Coarse conditioning bands must recover.
    bands = (
        (0.0, 0.30),
        (0.30, 0.70),
        (0.70, 1.20),
        (1.20, 2.00),
    )
    band_means = []
    for lower, upper in bands:
        selected = [
            float(row["observed_rejection_rate"])
            for row in rows
            if lower <= float(row["conditioning_index"]) < upper
        ]
        band_means.append(float(np.mean(selected)))
    assert band_means == sorted(band_means, reverse=True)
    assert float(summary["mae_improvement_fraction"]) > 0.40
    assert float(summary["log_loss_improvement_fraction"]) > 0.10
    # Systematic overprediction is prospective evidence that first-order
    # conditioning does not absorb the fifth family's higher-order shape.
    assert all(
        float(row["old_family_model_prediction"]) > float(row["observed_rejection_rate"])
        for row in rows
    )
