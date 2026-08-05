"""Focused independent replication of weak Huber c_delta interval coverage."""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.robust_extension_utils import write_tsv
from scripts.run_huber_bootstrap_coverage import run


if __name__ == "__main__":
    write_tsv(
        PROJECT_ROOT
        / "results"
        / "huber_bootstrap_focused_replication_20260805.tsv",
        run(
            repetitions=800,
            n_boot=399,
            seed=20260911,
            sample_sizes=(80, 160),
            latent_correlations=(0.5,),
        ),
    )
