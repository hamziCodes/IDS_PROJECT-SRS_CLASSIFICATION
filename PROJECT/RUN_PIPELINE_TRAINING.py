"""Launcher for the split requirement-classification pipeline.

Layman: Runs each numbered stage (0→6) in order using a fresh Python
process so each script stays small and independent.
"""

from pathlib import Path
import subprocess
import sys


BASE_DIR = Path(__file__).resolve().parent
STAGES = [
    "0_Outlier_Training.py",
    "1_Load_and_Merge.py",
    "2_Outlier_Gate.py",
    "3_EDA.py",
    "4_Data_Cleaning.py",
    "5_Feature_Engineering.py",
    "6_Model_Training_and_Export.py",
]


def run_stage(stage_name):
    # Run one stage in a fresh process so each script stays simple and isolated.
    stage_path = BASE_DIR / stage_name
    print(f"\n=== Running {stage_name} ===")
    subprocess.run([sys.executable, str(stage_path)], check=True)


if __name__ == "__main__":
    # Execute the pipeline in the same order as the original monolithic script.
    for stage_name in STAGES:
        run_stage(stage_name)

    # Tell the user the split pipeline finished without needing the old monolith.
    print("\n✓ Split pipeline completed.")