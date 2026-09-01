"""Deterministic validation of the public robust-profile correlation API."""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import (
    c_delta_from_profiles,
    huber_profile_correlation_inference,
    huber_reference_profile,
)
from scripts.robust_extension_utils import write_tsv
from scripts.run_weak_null_local_tests_20260814 import profile_weak_null_test


RESULTS_PATH = PROJECT_ROOT / "results" / "public_rho_api_audit_20260901.tsv"


def _row(
    check: str,
    observed: float,
    threshold: float,
    passed: bool,
    interpretation: str,
) -> dict[str, object]:
    return {
        "check": check,
        "observed": observed,
        "criterion": "less_than_or_equal_to",
        "threshold": threshold,
        "passed": int(passed),
        "interpretation": interpretation,
    }


def public_rho_api_audit() -> list[dict[str, object]]:
    """Check one fixed regular sample without adding a distribution grid."""
    rng = np.random.default_rng(20260901)
    x = rng.normal(size=400)
    y = 0.35 * x + np.sqrt(1.0 - 0.35**2) * rng.normal(size=x.size)

    public = huber_profile_correlation_inference(x, y)
    compatibility = profile_weak_null_test(x, y)
    transformed = huber_profile_correlation_inference(
        3.7 * x + 11.0,
        0.8 * y - 4.0,
    )
    profile_x = huber_reference_profile(x)
    profile_y = huber_reference_profile(y)
    direct_rho = float(np.corrcoef(profile_x, profile_y)[0, 1])
    secondary_c = c_delta_from_profiles(profile_x, profile_y)
    cv_x = float(np.std(profile_x, ddof=0) / np.mean(profile_x))
    cv_y = float(np.std(profile_y, ddof=0) / np.mean(profile_y))
    identity_c = 1.0 + float(public["estimate"]) * cv_x * cv_y

    estimate_compatibility_error = abs(
        float(public["estimate"]) - float(compatibility["estimate"])
    )
    se_compatibility_error = abs(
        float(public["standard_error"]) - float(compatibility["standard_error"])
    )
    influence_compatibility_error = float(
        np.max(
            np.abs(
                np.asarray(public["influence"])
                - np.asarray(compatibility["influence"])
            )
        )
    )
    profile_estimate_error = abs(float(public["estimate"]) - direct_rho)
    affine_estimate_error = abs(
        float(public["estimate"]) - float(transformed["estimate"])
    )
    affine_se_error = abs(
        float(public["standard_error"]) - float(transformed["standard_error"])
    )
    influence_center_error = abs(float(np.mean(np.asarray(public["influence"]))))
    c_identity_error = abs(float(secondary_c["raw"]) - identity_c)

    return [
        _row(
            "legacy_wrapper_estimate_matches_public_api",
            estimate_compatibility_error,
            1e-14,
            estimate_compatibility_error <= 1e-14,
            "the existing simulation entry point delegates without changing rho_P",
        ),
        _row(
            "legacy_wrapper_se_matches_public_api",
            se_compatibility_error,
            1e-14,
            se_compatibility_error <= 1e-14,
            "the complete first-order standard error is shared by both paths",
        ),
        _row(
            "legacy_wrapper_influence_matches_public_api",
            influence_compatibility_error,
            1e-14,
            influence_compatibility_error <= 1e-14,
            "the empirical influence values cannot drift between code paths",
        ),
        _row(
            "public_estimate_matches_direct_profile_correlation",
            profile_estimate_error,
            1e-14,
            profile_estimate_error <= 1e-14,
            "the public estimate targets Corr(|X-T_X|, |Y-T_Y|)",
        ),
        _row(
            "public_estimate_positive_affine_invariance",
            affine_estimate_error,
            1e-12,
            affine_estimate_error <= 1e-12,
            "separate positive changes of origin and units preserve rho_P",
        ),
        _row(
            "public_se_positive_affine_invariance",
            affine_se_error,
            1e-12,
            affine_se_error <= 1e-12,
            "the complete plug-in standard error respects the same invariance",
        ),
        _row(
            "public_influence_empirically_centered",
            influence_center_error,
            1e-12,
            influence_center_error <= 1e-12,
            "the returned empirical influence representation is centered",
        ),
        _row(
            "secondary_C_identity_retained",
            c_identity_error,
            1e-12,
            c_identity_error <= 1e-12,
            "C remains a secondary scale linked by C=1+rho_P CV_X CV_Y",
        ),
    ]


def main() -> None:
    rows = public_rho_api_audit()
    write_tsv(RESULTS_PATH, rows)
    for row in rows:
        print(row)
    if not all(int(row["passed"]) for row in rows):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
