"""Environment check for Week 1-5 customer intent repo."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path


REQUIRED_PACKAGES = [
    ("pandas", "pandas"),
    ("sklearn", "scikit-learn"),
    ("ipykernel", "jupyter kernel"),
]

REQUIRED_FILES = [
    "data/customer_intent_demo.csv",
    "notebooks/week01_baseline.ipynb",
    "notebooks/week04_baseline.ipynb",
    "notebooks/week05_ml_experiment.ipynb",
    "evidence/week04_baseline_report.md",
    "evidence/week04_solution_choice_note.md",
    "evidence/week05_ml_experiment.md",
    "outputs/week05_results.csv",
    "outputs/week05_top3_failures.csv",
]


def main() -> int:
    print("Python:", sys.version.split()[0])

    missing: list[str] = []
    for module_name, display_name in REQUIRED_PACKAGES:
        try:
            module = importlib.import_module(module_name)
        except ImportError:
            missing.append(display_name)
            print(f"[missing] {display_name}")
            continue

        version = getattr(module, "__version__", "installed")
        print(f"[ok] {display_name}: {version}")

    root = Path(__file__).resolve().parent
    missing_files = []
    for rel_path in REQUIRED_FILES:
        if (root / rel_path).exists():
            print(f"[ok] file: {rel_path}")
        else:
            missing_files.append(rel_path)
            print(f"[missing] file: {rel_path}")

    if missing or missing_files:
        print()
        print("Some packages or files are missing.")
        print("Run: pip install -r requirements.txt")
        return 1

    print()
    print("Environment check passed.")
    print("Open notebooks/week05_ml_experiment.ipynb for Week 5.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
