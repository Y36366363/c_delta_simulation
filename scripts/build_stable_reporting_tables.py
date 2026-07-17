from pathlib import Path
import csv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS = PROJECT_ROOT / "results"


STABLE_FIELDS = [
    "section",
    "source_file",
    "kind",
    "background",
    "n",
    "k_extremes",
    "scenario",
    "target_corr",
    "selected_magnitude",
    "alpha",
    "repetitions",
    "n_perm",
    "reject_count",
    "rejection_rate",
    "wilson_low",
    "wilson_high",
    "mean_norm",
    "mean_corr",
    "mean_p",
    "p05",
    "p50",
    "p95",
    "mean_index_overlap",
]


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def project_row(row: dict[str, str], *, section: str, source_file: str) -> dict[str, str]:
    projected = {field: "" for field in STABLE_FIELDS}
    projected["section"] = section
    projected["source_file"] = source_file
    for field in STABLE_FIELDS:
        if field in row:
            projected[field] = row[field]
    if not projected["repetitions"] and "evaluation_repetitions" in row:
        projected["repetitions"] = row["evaluation_repetitions"]
    return projected


def main() -> None:
    rows = []

    l2_path = RESULTS / "lower_target_calibration_20260715.tsv"
    for row in read_tsv(l2_path):
        if row["target_corr"] == "0.35":
            rows.append(
                project_row(
                    row,
                    section="lower_target_l2_target_0.35",
                    source_file=l2_path.name,
                )
            )

    l1_path = RESULTS / "lower_target_l1_calibration_20260716.tsv"
    for row in read_tsv(l1_path):
        rows.append(
            project_row(
                row,
                section="lower_target_l1_target_0.35",
                source_file=l1_path.name,
            )
        )

    sample_path = RESULTS / "sample_size_sensitivity_20260716.tsv"
    for row in read_tsv(sample_path):
        if row["scenario"] == "matched":
            rows.append(
                project_row(
                    row,
                    section="sample_size_matched_power",
                    source_file=sample_path.name,
                )
            )
        elif row["scenario"] == "independent_null":
            rows.append(
                project_row(
                    row,
                    section="sample_size_independent_null",
                    source_file=sample_path.name,
                )
            )

    output_path = RESULTS / "stable_reporting_metrics_20260717.tsv"
    with output_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=STABLE_FIELDS, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)

    print(f"wrote {len(rows)} rows to {output_path}")


if __name__ == "__main__":
    main()
