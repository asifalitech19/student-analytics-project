"""
======================================================================
AI STUDENT ANALYTICS DASHBOARD
TARGET CLEANING PIPELINE - FEATURE SET B+
======================================================================

Purpose:
    Rebuild the training-cleaned CSV from the ORIGINAL IUBAT dataset
    while preserving the new academic-context features required by
    Feature Set B+:

        - Current Semester
        - Average attendance on class (Percentage )
        - How many Credit did you have completed?

Target:
        What is your current CGPA?

Rules:
    - Missing/non-numeric CGPA -> remove
    - CGPA < 0 or CGPA > 4 -> remove
    - CGPA == 0 -> treat as unavailable and remove
    - Do NOT remove Current Semester / Attendance / Credits here
    - Preserve all original columns so Dashboard / Analytics remain safe

Output:
    backend/dataset/IUBAT_CGPA_Training_Cleaned.csv
======================================================================
"""

from pathlib import Path

import numpy as np
import pandas as pd


# ======================================================================
# PATHS
# ======================================================================

BASE_DIR = Path(__file__).resolve().parents[2]
DATASET_DIR = BASE_DIR / "dataset"

OUTPUT_PATH = (
    DATASET_DIR / "IUBAT_CGPA_Training_Cleaned.csv"
)

ORIGINAL_CANDIDATES = [
    DATASET_DIR / "IUBAT_Student_Performance_Dataset(1).csv",

    DATASET_DIR / "IUBAT_Student_Performance_Dataset.csv",
    DATASET_DIR / "classified_dataset.csv",
]

# Exact columns required by the final B+ preprocessing pipeline.
TARGET = "What is your current CGPA?"

NEW_ACADEMIC_CONTEXT_FEATURES = [
    "Current Semester",
    "Average attendance on class (Percentage )",
    "How many Credit did you have completed?",
]

# Existing 14 features.
EXISTING_FEATURES = [
    "Age (Years)",
    "Gender",
    "What is your relationship status?",
    "With whom you are living with?",
    "Do you have any health issues?",
    "Do you have any physical disabilities?",
    "University Admission year",
    "H.S.C passing year",
    "Do you have meritorious scholarship ?",
    "Status of your English language proficiency",
    "How many hour do you study daily? (Hours )",
    "How many times do you seat for study in a day?",
    "How many hour do you spent daily in social media? (Hours)",
    "How many hour do you spent daily on your skill development? (Hours )",
]

REQUIRED_COLUMNS = (
    EXISTING_FEATURES
    + NEW_ACADEMIC_CONTEXT_FEATURES
    + [TARGET]
)


# ======================================================================
# HELPERS
# ======================================================================

def find_original_dataset() -> Path:
    """Find the original CSV that still contains completed credits."""

    for path in ORIGINAL_CANDIDATES:
        if path.exists():
            return path

    raise FileNotFoundError(
        "Could not find the original IUBAT CSV. Expected one of:\n"
        + "\n".join(f"- {p}" for p in ORIGINAL_CANDIDATES)
        + "\n\nDo NOT use IUBAT_CGPA_Training_Cleaned.csv as the source."
    )


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Strip column-name whitespace and text-value whitespace."""

    df = df.copy()

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    for column in df.columns:
        if (
            df[column].dtype == "object"
            or pd.api.types.is_string_dtype(df[column])
        ):
            df[column] = (
                df[column]
                .astype("string")
                .str.strip()
            )

    return df


def validate_columns(df: pd.DataFrame) -> None:
    missing = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            "Required Feature Set B+ columns are missing:\n"
            + "\n".join(f"- {column}" for column in missing)
        )


def print_numeric_summary(df: pd.DataFrame) -> None:
    print()
    print("=" * 70)
    print("ACADEMIC CONTEXT FEATURES PRESERVED")
    print("=" * 70)

    for column in NEW_ACADEMIC_CONTEXT_FEATURES:
        values = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        print(f"\n{column}")
        print(f"  Non-null : {int(values.notna().sum())}")
        print(f"  Missing  : {int(values.isna().sum())}")

        if values.notna().any():
            print(f"  Min      : {values.min():.3f}")
            print(f"  Max      : {values.max():.3f}")
            print(f"  Mean     : {values.mean():.3f}")


def clean_target(df: pd.DataFrame) -> pd.DataFrame:
    """Apply the locked target-cleaning policy."""

    df = df.copy()

    raw_target = pd.to_numeric(
        df[TARGET],
        errors="coerce"
    )

    missing_or_non_numeric = int(raw_target.isna().sum())
    zero_count = int((raw_target == 0).sum())
    below_zero = int((raw_target < 0).sum())
    above_four = int((raw_target > 4).sum())

    print()
    print("=" * 70)
    print("TARGET CLEANING")
    print("=" * 70)

    print(f"Total rows              : {len(df)}")
    print(f"Missing / non-numeric   : {missing_or_non_numeric}")
    print(f"CGPA = 0                : {zero_count}")
    print(f"Below 0                 : {below_zero}")
    print(f"Above 4                 : {above_four}")

    # Locked rule from the previous audit:
    # 0.0 is considered unavailable, not a valid training target.
    invalid_mask = (
        raw_target.isna()
        | (raw_target == 0)
        | (raw_target < 0)
        | (raw_target > 4)
    )

    removed_count = int(invalid_mask.sum())

    print()
    print(f"Removing invalid target rows: {removed_count}")

    cleaned = df.loc[~invalid_mask].copy()
    cleaned[TARGET] = raw_target.loc[
        ~invalid_mask
    ].astype(float)

    print()
    print("Final target range:")
    print(
        f"Minimum CGPA : {cleaned[TARGET].min():.3f}"
    )
    print(
        f"Maximum CGPA : {cleaned[TARGET].max():.3f}"
    )
    print(
        f"Mean CGPA    : {cleaned[TARGET].mean():.3f}"
    )

    return cleaned


# ======================================================================
# MAIN
# ======================================================================

def main():

    print()
    print("=" * 70)
    print("AI STUDENT ANALYTICS DASHBOARD")
    print("TARGET CLEANING - FEATURE SET B+")
    print("=" * 70)

    DATASET_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # ------------------------------------------------------------------
    # 1. Find ORIGINAL dataset
    # ------------------------------------------------------------------

    source_path = find_original_dataset()

    print()
    print("=" * 70)
    print("LOADING ORIGINAL DATASET")
    print("=" * 70)
    print(f"Source: {source_path}")

    df = pd.read_csv(
        source_path
    )

    print(f"Rows    : {len(df)}")
    print(f"Columns : {len(df.columns)}")

    # ------------------------------------------------------------------
    # 2. Normalize
    # ------------------------------------------------------------------

    print()
    print("=" * 70)
    print("TEXT NORMALIZATION")
    print("=" * 70)

    df = normalize_columns(df)

    print("✓ Column and text whitespace normalized.")

    # ------------------------------------------------------------------
    # 3. Validate B+ fields BEFORE cleaning target
    # ------------------------------------------------------------------

    print()
    print("=" * 70)
    print("FEATURE SET B+ VALIDATION")
    print("=" * 70)

    validate_columns(df)

    print(
        f"✓ All {len(REQUIRED_COLUMNS)} required B+ columns exist."
    )

    # ------------------------------------------------------------------
    # 4. Preserve the academic-context features
    # ------------------------------------------------------------------

    # Convert these to numeric where appropriate, but do not delete rows
    # based on missingness. The final preprocessing pipeline will impute.
    for column in [
        "Current Semester",
        "Average attendance on class (Percentage )",
        "How many Credit did you have completed?",
    ]:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    print_numeric_summary(df)

    # ------------------------------------------------------------------
    # 5. Target cleaning
    # ------------------------------------------------------------------

    cleaned = clean_target(df)

    # ------------------------------------------------------------------
    # 6. Final validation
    # ------------------------------------------------------------------

    print()
    print("=" * 70)
    print("FINAL TRAINING DATA VALIDATION")
    print("=" * 70)

    remaining_missing = int(
        cleaned[TARGET].isna().sum()
    )

    remaining_zero = int(
        (cleaned[TARGET] == 0).sum()
    )

    remaining_invalid = int(
        (
            (cleaned[TARGET] < 0)
            | (cleaned[TARGET] > 4)
        ).sum()
    )

    print(f"Training-ready rows : {len(cleaned)}")
    print(f"Missing target      : {remaining_missing}")
    print(f"CGPA = 0            : {remaining_zero}")
    print(f"Out-of-range CGPA   : {remaining_invalid}")

    if (
        remaining_missing
        or remaining_zero
        or remaining_invalid
    ):
        raise RuntimeError(
            "Final target validation failed."
        )

    # Verify the B+ columns still exist after cleaning.
    validate_columns(cleaned)

    print()
    print("✓ Target quality passed.")
    print("✓ Feature Set B+ columns preserved.")
    print("✓ Current Semester preserved.")
    print("✓ Attendance preserved.")
    print("✓ Completed Credits preserved.")

    # ------------------------------------------------------------------
    # 7. Save ALL columns
    # ------------------------------------------------------------------

    # Keep all original columns. This prevents Dashboard / Analytics /
    # chatbot from losing useful descriptive fields. preprocessing.py
    # will select only the final 17 model features.
    cleaned.to_csv(
        OUTPUT_PATH,
        index=False,
        encoding="utf-8-sig"
    )

    print()
    print("=" * 70)
    print("CLEANED DATASET SAVED")
    print("=" * 70)
    print(f"Output: {OUTPUT_PATH}")

    print()
    print("Final B+ model fields:")
    for index, column in enumerate(
        EXISTING_FEATURES
        + NEW_ACADEMIC_CONTEXT_FEATURES,
        start=1
    ):
        print(f"  {index:02d}. {column}")

    print(f"\nTarget: {TARGET}")

    print()
    print("=" * 70)
    print("TARGET CLEANING COMPLETE")
    print("=" * 70)

    print()
    print("NEXT STEP:")
    print("→ Run: python -m app.ml.preprocessing")
    print("→ Then: python -m app.ml.model_training")


if __name__ == "__main__":
    main()