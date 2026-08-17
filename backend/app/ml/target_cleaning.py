import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# AI STUDENT ANALYTICS DASHBOARD
# TARGET CLEANING PIPELINE
# ============================================================

TARGET_COLUMN = "What is your current CGPA?"

MIN_CGPA = 0.0
MAX_CGPA = 4.0

# IMPORTANT:
# Treat CGPA = 0 as unavailable/invalid for supervised training.
ZERO_CGPA_IS_INVALID = True


# ============================================================
# DATASET PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATASET_PATH = (
    BASE_DIR
    / "dataset"
    / "IUBAT_CGPA_Cleaned.xlsx"
)


# ============================================================
# LOAD DATASET
# ============================================================

def load_dataset():

    print("=" * 70)
    print("LOADING DATASET")
    print("=" * 70)

    print(f"Dataset: {DATASET_PATH}")

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found:\n{DATASET_PATH}"
        )

    df = pd.read_excel(DATASET_PATH)

    print(f"Rows    : {len(df)}")
    print(f"Columns : {len(df.columns)}")

    return df


# ============================================================
# NORMALIZE COLUMN NAMES
# ============================================================

def normalize_columns(df):

    df = df.copy()

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    return df


# ============================================================
# CLEAN TARGET
# ============================================================

def clean_target(df):

    print("\n" + "=" * 70)
    print("TARGET CLEANING")
    print("=" * 70)

    df = df.copy()

    if TARGET_COLUMN not in df.columns:

        raise ValueError(
            f"Target column not found:\n{TARGET_COLUMN}"
        )

    # --------------------------------------------------------
    # Convert target to numeric
    # --------------------------------------------------------

    df[TARGET_COLUMN] = pd.to_numeric(
        df[TARGET_COLUMN],
        errors="coerce"
    )

    # --------------------------------------------------------
    # Original statistics
    # --------------------------------------------------------

    total_rows = len(df)

    missing_before = df[TARGET_COLUMN].isna().sum()

    zero_count = (
        df[TARGET_COLUMN]
        .eq(0)
        .sum()
    )

    below_zero = (
        df[TARGET_COLUMN] < MIN_CGPA
    ).sum()

    above_four = (
        df[TARGET_COLUMN] > MAX_CGPA
    ).sum()

    print(f"Total rows              : {total_rows}")
    print(f"Missing / non-numeric   : {missing_before}")
    print(f"CGPA = 0                : {zero_count}")
    print(f"Below 0                 : {below_zero}")
    print(f"Above 4                 : {above_four}")

    # --------------------------------------------------------
    # Remove invalid CGPA > 4
    # --------------------------------------------------------

    invalid_range_mask = (
        (df[TARGET_COLUMN] < MIN_CGPA)
        |
        (df[TARGET_COLUMN] > MAX_CGPA)
    )

    invalid_range_count = invalid_range_mask.sum()

    if invalid_range_count > 0:

        print(
            f"\n❌ Removing out-of-range values: "
            f"{invalid_range_count}"
        )

        df.loc[
            invalid_range_mask,
            TARGET_COLUMN
        ] = np.nan

    # --------------------------------------------------------
    # Handle CGPA = 0
    # --------------------------------------------------------

    if ZERO_CGPA_IS_INVALID:

        zero_mask = (
            df[TARGET_COLUMN] == 0
        )

        zero_removed = zero_mask.sum()

        if zero_removed > 0:

            print(
                f"⚠ Treating CGPA = 0 as unavailable: "
                f"{zero_removed}"
            )

            df.loc[
                zero_mask,
                TARGET_COLUMN
            ] = np.nan

    # --------------------------------------------------------
    # Remove missing target rows
    # --------------------------------------------------------

    missing_after_cleaning = (
        df[TARGET_COLUMN].isna().sum()
    )

    print(
        f"\nMissing target after cleaning : "
        f"{missing_after_cleaning}"
    )

    rows_before_drop = len(df)

    df = df.dropna(
        subset=[TARGET_COLUMN]
    ).copy()

    rows_removed = (
        rows_before_drop - len(df)
    )

    print(
        f"Rows removed                 : "
        f"{rows_removed}"
    )

    print(
        f"Rows remaining               : "
        f"{len(df)}"
    )

    # --------------------------------------------------------
    # Final range verification
    # --------------------------------------------------------

    if len(df) > 0:

        min_value = df[TARGET_COLUMN].min()
        max_value = df[TARGET_COLUMN].max()

        print("\nFinal target range:")
        print(f"Minimum CGPA : {min_value:.3f}")
        print(f"Maximum CGPA : {max_value:.3f}")

        if (
            min_value < MIN_CGPA
            or max_value > MAX_CGPA
        ):

            raise ValueError(
                "Target cleaning failed. "
                "Invalid CGPA values remain."
            )

    return df


# ============================================================
# TARGET QUALITY REPORT
# ============================================================

def target_quality_report(df):

    print("\n" + "=" * 70)
    print("FINAL TARGET QUALITY REPORT")
    print("=" * 70)

    target = df[TARGET_COLUMN]

    print(
        f"Training-ready rows : {len(df)}"
    )

    print(
        f"Target minimum      : {target.min():.3f}"
    )

    print(
        f"Target maximum      : {target.max():.3f}"
    )

    print(
        f"Target mean         : {target.mean():.3f}"
    )

    print(
        f"Target median       : {target.median():.3f}"
    )

    print(
        f"Target std          : {target.std():.3f}"
    )

    print(
        f"Remaining missing   : {target.isna().sum()}"
    )

    print(
        f"Remaining zeros     : {(target == 0).sum()}"
    )

    # --------------------------------------------------------
    # Final assertions
    # --------------------------------------------------------

    assert target.notna().all(), (
        "Missing target values remain."
    )

    assert (target >= 0).all(), (
        "CGPA below 0 remains."
    )

    assert (target <= 4).all(), (
        "CGPA above 4 remains."
    )

    if ZERO_CGPA_IS_INVALID:

        assert not (target == 0).any(), (
            "CGPA = 0 remains despite "
            "ZERO_CGPA_IS_INVALID=True."
        )

    print("\n✓ No missing target values.")
    print("✓ No CGPA below 0.")
    print("✓ No CGPA above 4.")

    if ZERO_CGPA_IS_INVALID:
        print("✓ No CGPA = 0 values.")

    print("\n✓ TARGET QUALITY PASSED")


# ============================================================
# SAVE CLEANED TRAINING DATA
# ============================================================

def save_cleaned_dataset(df):

    output_path = (
        BASE_DIR
        / "dataset"
        / "IUBAT_CGPA_Training_Cleaned.csv"
    )

    df.to_csv(
        output_path,
        index=False
    )

    print("\n" + "=" * 70)
    print("CLEANED DATASET SAVED")
    print("=" * 70)

    print(f"Output: {output_path}")

    return output_path


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n")
    print("=" * 70)
    print("AI STUDENT ANALYTICS DASHBOARD")
    print("CGPA TARGET CLEANING PIPELINE")
    print("=" * 70)

    # Load
    df = load_dataset()

    # Normalize
    df = normalize_columns(df)

    # Clean target
    df = clean_target(df)

    # Report
    target_quality_report(df)

    # Save
    save_cleaned_dataset(df)

    print("\n" + "=" * 70)
    print("TARGET CLEANING COMPLETE")
    print("=" * 70)

    print("\nNEXT STEP:")
    print("→ Update preprocessing.py to use")
    print("  IUBAT_CGPA_Training_Cleaned.csv")
    print("→ Run preprocessing again")
    print("→ Retrain regression models")
    print("→ Compare MAE / RMSE / R²")


if __name__ == "__main__":
    main()