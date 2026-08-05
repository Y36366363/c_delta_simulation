"""Independent replication of strong-effect studentized interval coverage."""

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.robust_extension_utils import write_tsv
from scripts.run_studentized_inference_validation import run


if __name__ == "__main__":
    write_tsv(
        PROJECT_ROOT
        / "results"
        / "studentized_focused_replication_20260805.tsv",
        run(
            repetitions=3000,
            seed=20260915,
            sample_sizes=(80, 160),
            latent_correlations=(0.5,),
        ),
    )
