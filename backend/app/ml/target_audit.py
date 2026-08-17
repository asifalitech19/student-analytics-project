import pandas as pd
from pathlib import Path

# ============================================================
# CONFIG
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATASET_PATH = BASE_DIR / "dataset" / "IUBAT_CGPA_Cleaned.xlsx"

TARGET_COLUMN = "What is your current CGPA?"


# ============================================================
# LOAD DATASET
# ============================================================

def load_dataset():

    print("=" * 80)
    print("AI STUDENT ANALYTICS DASHBOARD")
    print("CGPA TARGET QUALITY AUDIT")
    print("=" * 80)

    print("\n" + "=" * 80)
    print("LOADING DATASET")
    print("=" * 80)

    print(f"\nDataset: {DATASET_PATH}")

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found:\n{DATASET_PATH}"
        )

    df = pd.read_excel(DATASET_PATH)

    print(f"Rows    : {len(df)}")
    print(f"Columns : {len(df.columns)}")

    return df


# ============================================================
# TARGET COLUMN CHECK
# ============================================================

def check_target_column(df):

    print("\n" + "=" * 80)
    print("TARGET COLUMN CHECK")
    print("=" * 80)

    if TARGET_COLUMN not in df.columns:

        print("\n❌ TARGET COLUMN NOT FOUND")

        print("\nAvailable columns:")

        for column in df.columns:
            print(f"  - {column}")

        raise ValueError(
            f"Target column not found: {TARGET_COLUMN}"
        )

    print(f"\n✓ Target found:")
    print(f"  {TARGET_COLUMN}")


# ============================================================
# TARGET CONVERSION
# ============================================================

def convert_target(df):

    print("\n" + "=" * 80)
    print("TARGET CONVERSION")
    print("=" * 80)

    df = df.copy()

    df["_cgpa_numeric"] = pd.to_numeric(
        df[TARGET_COLUMN],
        errors="coerce"
    )

    missing = df["_cgpa_numeric"].isna().sum()

    print(f"\nMissing / non-numeric CGPA : {missing}")

    return df


# ============================================================
# TARGET DISTRIBUTION
# ============================================================

def target_distribution(df):

    print("\n" + "=" * 80)
    print("CGPA DISTRIBUTION")
    print("=" * 80)

    target = df["_cgpa_numeric"]

    print("\nDescriptive statistics:")

    print(
        target.describe()
        .to_string()
    )

    print("\nCGPA value counts:")

    counts = (
        target
        .value_counts(dropna=False)
        .sort_index()
    )

    for value, count in counts.items():

        print(
            f"  {value!s:>8} : {count}"
        )


# ============================================================
# ZERO CGPA AUDIT
# ============================================================

def zero_cgpa_audit(df):

    print("\n" + "=" * 80)
    print("CGPA = 0.0 AUDIT")
    print("=" * 80)

    zero_rows = df[
        df["_cgpa_numeric"] == 0
    ].copy()

    print(
        f"\nNumber of CGPA = 0 records : {len(zero_rows)}"
    )

    if len(zero_rows) == 0:

        print("\n✓ No CGPA = 0 records found.")

        return

    print("\n⚠ CGPA = 0 records detected.")

    print(
        "\nIMPORTANT:"
    )

    print(
        "We must determine whether 0.0 represents:"
    )

    print(
        "  1. A genuine academic CGPA"
    )

    print(
        "  2. Missing / unavailable CGPA"
    )

    print(
        "  3. Data-entry / encoding artifact"
    )

    print("\nSample records:")

    # Show useful columns if available

    preferred_columns = [
        "Age (Years)",
        "Gender",
        "University Admission year",
        "H.S.C passing year",
        "Do you have meritorious scholarship ?",
        "What is your current CGPA?",
    ]

    available = [
        column
        for column in preferred_columns
        if column in zero_rows.columns
    ]

    if available:

        print(
            zero_rows[available]
            .head(20)
            .to_string(index=False)
        )

    else:

        print(
            zero_rows.head(20)
            .to_string(index=False)
        )


# ============================================================
# INVALID TARGET RANGE
# ============================================================

def range_audit(df):

    print("\n" + "=" * 80)
    print("CGPA RANGE AUDIT")
    print("=" * 80)

    target = df["_cgpa_numeric"]

    below_zero = (target < 0).sum()

    above_four = (target > 4).sum()

    print(
        f"\nBelow 0.0 : {below_zero}"
    )

    print(
        f"Above 4.0 : {above_four}"
    )

    if below_zero == 0 and above_four == 0:

        print(
            "\n✓ All numeric CGPA values are within 0.0–4.0."
        )

    else:

        print(
            "\n❌ Invalid CGPA values detected."
        )


# ============================================================
# TARGET MISSINGNESS
# ============================================================

def missing_target_audit(df):

    print("\n" + "=" * 80)
    print("TARGET MISSINGNESS")
    print("=" * 80)

    missing = df["_cgpa_numeric"].isna().sum()

    total = len(df)

    percentage = (
        missing / total * 100
        if total > 0
        else 0
    )

    print(
        f"\nMissing target rows : {missing}"
    )

    print(
        f"Missing percentage  : {percentage:.2f}%"
    )


# ============================================================
# FINAL RECOMMENDATION
# ============================================================

def final_recommendation(df):

    print("\n" + "=" * 80)
    print("FINAL TARGET QUALITY RECOMMENDATION")
    print("=" * 80)

    target = df["_cgpa_numeric"]

    zero_count = (target == 0).sum()

    missing_count = target.isna().sum()

    invalid_count = (
        (target < 0).sum()
        +
        (target > 4).sum()
    )

    print("\nAUDIT SUMMARY")

    print(
        f"  Total records        : {len(df)}"
    )

    print(
        f"  Missing CGPA         : {missing_count}"
    )

    print(
        f"  CGPA = 0             : {zero_count}"
    )

    print(
        f"  Out-of-range CGPA    : {invalid_count}"
    )

    print("\n" + "-" * 80)

    if invalid_count > 0:

        print(
            "❌ INVALID TARGET VALUES REQUIRE CLEANING."
        )

    if zero_count > 0:

        print(
            "⚠ CGPA = 0 REQUIRES SEMANTIC VERIFICATION."
        )

        print(
            "DO NOT automatically delete these rows yet."
        )

    if missing_count > 0:

        print(
            "⚠ Missing CGPA rows cannot be used for supervised training."
        )

    print("\n" + "-" * 80)

    print(
        "NEXT DECISION:"
    )

    print(
        "→ Verify the meaning of CGPA = 0."
    )

    print(
        "→ Then lock the final target-cleaning rule."
    )

    print(
        "→ Then retrain and re-evaluate the regression models."
    )


# ============================================================
# MAIN
# ============================================================

def run_audit():

    df = load_dataset()

    check_target_column(df)

    df = convert_target(df)

    target_distribution(df)

    zero_cgpa_audit(df)

    range_audit(df)

    missing_target_audit(df)

    final_recommendation(df)

    print("\n" + "=" * 80)
    print("TARGET AUDIT COMPLETE")
    print("=" * 80)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    run_audit()