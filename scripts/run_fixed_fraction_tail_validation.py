from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from scripts.run_tail_cross_validation import run_repeated_setting
from scripts.run_tail_factor_comparison import write_tsv


RESULTS_DIR = PROJECT_ROOT / "results"


def run_fixed_fraction_tail_validation() -> list[dict]:
    rows = []
    repetitions = 300
    n_perm = 299
    df_labels = ["normal", "t5", "t4", "t3", "t2.5", "t2.2", "t2"]
    n_values = [40, 80, 160]

    for kind_offset, kind in enumerate(["l2", "l1"]):
        for df_offset, df_label in enumerate(df_labels):
            for n_offset, n in enumerate(n_values):
                for design in ["fixed_k", "fixed_proportion"]:
                    k = 2 if design == "fixed_k" else max(1, round(0.05 * n))
                    rowspec = {
                        "validation": "fixed_k_vs_fixed_proportion_tail_gradient",
                        "design": design,
                        "kind": kind,
                        "df_label": df_label,
                        "n": n,
                        "k_extremes": k,
                        "k_fraction": round(k / n, 4),
                        "magnitude": 6.0,
                        "scenario": "matched",
                    }
                    rows.append(
                        run_repeated_setting(
                            rowspec=rowspec,
                            repetitions=repetitions,
                            n_perm=n_perm,
                            seed_base=(
                                20260729
                                + kind_offset * 100_000_000
                                + df_offset * 10_000_000
                                + n_offset * 100_000
                            ),
                        )
                    )
    return rows


def summarize_design_contrasts(rows: list[dict]) -> list[dict]:
    by_key = {
        (row["kind"], row["df_label"], row["n"], row["design"]): row
        for row in rows
    }
    out = []
    for kind in ["l2", "l1"]:
        for df_label in ["normal", "t5", "t4", "t3", "t2.5", "t2.2", "t2"]:
            fixed_rows = [
                by_key[(kind, df_label, n, "fixed_k")] for n in [40, 80, 160]
            ]
            proportion_rows = [
                by_key[(kind, df_label, n, "fixed_proportion")]
                for n in [40, 80, 160]
            ]
            out.append(
                {
                    "kind": kind,
                    "df_label": df_label,
                    "magnitude": 6.0,
                    "fixed_k": 2,
                    "fixed_proportion": 0.05,
                    "fixed_k_power_n40": fixed_rows[0]["rejection_rate"],
                    "fixed_k_power_n80": fixed_rows[1]["rejection_rate"],
                    "fixed_k_power_n160": fixed_rows[2]["rejection_rate"],
                    "fixed_k_change_n40_to_n160": round(
                        fixed_rows[2]["rejection_rate"]
                        - fixed_rows[0]["rejection_rate"],
                        4,
                    ),
                    "fixed_prop_power_n40": proportion_rows[0]["rejection_rate"],
                    "fixed_prop_power_n80": proportion_rows[1]["rejection_rate"],
                    "fixed_prop_power_n160": proportion_rows[2]["rejection_rate"],
                    "fixed_prop_change_n40_to_n160": round(
                        proportion_rows[2]["rejection_rate"]
                        - proportion_rows[0]["rejection_rate"],
                        4,
                    ),
                    "design_gap_at_n160": round(
                        proportion_rows[2]["rejection_rate"]
                        - fixed_rows[2]["rejection_rate"],
                        4,
                    ),
                }
            )
    return out


def main() -> None:
    RESULTS_DIR.mkdir(exist_ok=True)
    rows = run_fixed_fraction_tail_validation()
    write_tsv(
        RESULTS_DIR / "fixed_fraction_tail_validation_20260729.tsv",
        rows,
    )
    write_tsv(
        RESULTS_DIR / "fixed_fraction_tail_contrasts_20260729.tsv",
        summarize_design_contrasts(rows),
    )


if __name__ == "__main__":
    main()
