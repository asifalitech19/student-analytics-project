"""
AI STUDENT ANALYTICS DASHBOARD
CGPA = 0.0 SEMANTIC INVESTIGATION

Purpose:
    Investigate whether CGPA = 0.0 represents:
    1. Genuine academic performance
    2. Missing/unavailable CGPA
    3. Data-entry / encoding artifact

IMPORTANT:
    This script DOES NOT modify the original dataset.
    It only produces an investigation report.
"""

from pathlib import Path
import pandas as pd


# ============================================================================
# CONFIGURATION
# ============================================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATASET_PATH = (
    BASE_DIR
    / "dataset"
    / "IUBAT_CGPA_Cleaned.xlsx"
)

TARGET_COLUMN = "What is your current CGPA?"

OUTPUT_DIR = BASE_DIR / "ml_reports"

OUTPUT_CSV = OUTPUT_DIR / "zero_cgpa_records.csv"
SUMMARY_CSV = OUTPUT_DIR / "zero_cgpa_summary.csv"


# ============================================================================
# DISPLAY
# ============================================================================

def section(title: str):
    print()
    print("=" * 80)
    print(title)
    print("=" * 80)


# ============================================================================
# LOAD DATASET
# ============================================================================

def load_dataset():

    section("LOADING DATASET")

    print(f"Dataset: {DATASET_PATH}")

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"\nDataset not found:\n{DATASET_PATH}\n"
        )

    df = pd.read_excel(DATASET_PATH)

    print(f"Rows    : {df.shape[0]}")
    print(f"Columns : {df.shape[1]}")

    return df


# ============================================================================
# TARGET VALIDATION
# ============================================================================

def validate_target(df):

    section("TARGET VALIDATION")

    if TARGET_COLUMN not in df.columns:
        raise ValueError(
            f"Target column not found:\n{TARGET_COLUMN}"
        )

    print("✓ Target found:")
    print(f"  {TARGET_COLUMN}")

    return df


# ============================================================================
# IDENTIFY ZERO CGPA
# ============================================================================

def get_zero_records(df):

    section("IDENTIFYING CGPA = 0 RECORDS")

    numeric_cgpa = pd.to_numeric(
        df[TARGET_COLUMN],
        errors="coerce"
    )

    zero_mask = numeric_cgpa == 0

    zero_df = df.loc[zero_mask].copy()

    print(f"CGPA = 0 records : {len(zero_df)}")

    if len(zero_df) == 0:
        print("\n✓ No CGPA = 0 records found.")
        return zero_df

    print("\n⚠ CGPA = 0 records detected.")

    return zero_df


# ============================================================================
# IMPORTANT COLUMNS
# ============================================================================

def find_column(df, keywords):

    """
    Find the first dataset column containing one of the keywords.
    """

    for column in df.columns:

        column_lower = str(column).lower()

        for keyword in keywords:

            if keyword.lower() in column_lower:
                return column

    return None


def get_academic_columns(df):

    """
    Identify useful academic/context columns automatically.
    """

    patterns = {

        "age": [
            "age"
        ],

        "gender": [
            "gender"
        ],

        "admission_year": [
            "university admission year"
        ],

        "hsc_year": [
            "h.s.c passing year",
            "hsc passing year"
        ],

        "semester": [
            "current semester"
        ],

        "program": [
            "program"
        ],

        "scholarship": [
            "meritorious scholarship"
        ],

        "attendance": [
            "attendance"
        ],

        "probation": [
            "probation"
        ],

        "suspension": [
            "suspension"
        ],

        "consultancy": [
            "teacher consultancy"
        ],

        "relationship": [
            "relationship status"
        ],

        "health": [
            "health issues"
        ],
    }

    found = {}

    for name, keywords in patterns.items():

        column = find_column(
            df,
            keywords
        )

        if column is not None:
            found[name] = column

    return found


# ============================================================================
# DISPLAY ZERO RECORDS
# ============================================================================

def display_zero_records(zero_df, academic_columns):

    section("ZERO CGPA RECORD DETAILS")

    if zero_df.empty:
        return

    selected_columns = []

    # Target first
    if TARGET_COLUMN in zero_df.columns:
        selected_columns.append(TARGET_COLUMN)

    # Important columns
    for name, column in academic_columns.items():

        if column in zero_df.columns:
            selected_columns.append(column)

    # Remove duplicates while preserving order
    selected_columns = list(
        dict.fromkeys(selected_columns)
    )

    print(
        f"\nShowing {len(selected_columns)} relevant columns:\n"
    )

    if selected_columns:

        print(
            zero_df[selected_columns]
            .to_string(index=False)
        )

    else:

        print(
            zero_df.to_string(index=False)
        )


# ============================================================================
# ZERO CGPA DISTRIBUTION
# ============================================================================

def analyze_column_distribution(
    zero_df,
    column,
    label
):

    if column is None:
        return

    if column not in zero_df.columns:
        return

    section(f"ZERO CGPA DISTRIBUTION: {label}")

    series = (
        zero_df[column]
        .fillna("MISSING")
        .astype(str)
        .str.strip()
    )

    counts = series.value_counts(
        dropna=False
    )

    print(counts.to_string())


# ============================================================================
# COMPARE ZERO VS NON-ZERO
# ============================================================================

def compare_zero_vs_nonzero(
    df,
    zero_df,
    academic_columns
):

    section("ZERO CGPA VS NON-ZERO CGPA COMPARISON")

    numeric_cgpa = pd.to_numeric(
        df[TARGET_COLUMN],
        errors="coerce"
    )

    nonzero_df = df.loc[
        numeric_cgpa > 0
    ].copy()

    print(f"Zero CGPA students    : {len(zero_df)}")
    print(f"Non-zero CGPA students: {len(nonzero_df)}")

    print()

    comparison_rows = []

    for name, column in academic_columns.items():

        if column not in df.columns:
            continue

        zero_values = zero_df[column]
        nonzero_values = nonzero_df[column]

        zero_missing = zero_values.isna().mean() * 100
        nonzero_missing = nonzero_values.isna().mean() * 100

        comparison_rows.append({
            "feature": column,
            "zero_cgpa_missing_%": round(
                zero_missing,
                2
            ),
            "nonzero_cgpa_missing_%": round(
                nonzero_missing,
                2
            ),
            "zero_unique_values": zero_values.nunique(
                dropna=True
            ),
            "nonzero_unique_values": nonzero_values.nunique(
                dropna=True
            ),
        })

    if comparison_rows:

        comparison_df = pd.DataFrame(
            comparison_rows
        )

        print(
            comparison_df.to_string(
                index=False
            )
        )


# ============================================================================
# NUMERICAL PATTERN ANALYSIS
# ============================================================================

def analyze_numeric_patterns(
    zero_df,
    academic_columns
):

    section("NUMERICAL PATTERN ANALYSIS")

    for name in [
        "age",
        "admission_year",
        "hsc_year",
    ]:

        column = academic_columns.get(name)

        if column is None:
            continue

        values = pd.to_numeric(
            zero_df[column],
            errors="coerce"
        )

        print()
        print(f"Feature: {column}")

        print(
            f"  Missing : {values.isna().sum()}"
        )

        if values.notna().any():

            print(
                f"  Minimum : {values.min()}"
            )

            print(
                f"  Maximum : {values.max()}"
            )

            print(
                f"  Mean    : {values.mean():.2f}"
            )


# ============================================================================
# CGPA ZERO SEMANTIC SIGNALS
# ============================================================================

def investigate_semantic_signals(
    zero_df,
    academic_columns
):

    section("SEMANTIC SIGNAL INVESTIGATION")

    signals = []

    # --------------------------------------------------------
    # Current Semester
    # --------------------------------------------------------

    semester_column = academic_columns.get(
        "semester"
    )

    if semester_column:

        values = (
            zero_df[semester_column]
            .fillna("MISSING")
            .astype(str)
            .str.strip()
        )

        print(
            f"\nCurrent Semester: {semester_column}"
        )

        print(
            values.value_counts(
                dropna=False
            ).to_string()
        )

        signals.append(
            "Current semester distribution inspected."
        )

    else:

        print(
            "\nCurrent Semester column not available."
        )

    # --------------------------------------------------------
    # Probation
    # --------------------------------------------------------

    probation_column = academic_columns.get(
        "probation"
    )

    if probation_column:

        values = (
            zero_df[probation_column]
            .fillna("MISSING")
            .astype(str)
            .str.strip()
        )

        print(
            f"\nProbation: {probation_column}"
        )

        print(
            values.value_counts(
                dropna=False
            ).to_string()
        )

        signals.append(
            "Probation status distribution inspected."
        )

    # --------------------------------------------------------
    # Suspension
    # --------------------------------------------------------

    suspension_column = academic_columns.get(
        "suspension"
    )

    if suspension_column:

        values = (
            zero_df[suspension_column]
            .fillna("MISSING")
            .astype(str)
            .str.strip()
        )

        print(
            f"\nSuspension: {suspension_column}"
        )

        print(
            values.value_counts(
                dropna=False
            ).to_string()
        )

        signals.append(
            "Suspension status distribution inspected."
        )

    # --------------------------------------------------------
    # Scholarship
    # --------------------------------------------------------

    scholarship_column = academic_columns.get(
        "scholarship"
    )

    if scholarship_column:

        values = (
            zero_df[scholarship_column]
            .fillna("MISSING")
            .astype(str)
            .str.strip()
        )

        print(
            f"\nScholarship: {scholarship_column}"
        )

        print(
            values.value_counts(
                dropna=False
            ).to_string()
        )

        signals.append(
            "Scholarship distribution inspected."
        )

    return signals


# ============================================================================
# SAVE INVESTIGATION FILE
# ============================================================================

def save_investigation(
    zero_df,
    df,
    academic_columns
):

    section("SAVING INVESTIGATION REPORT")

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # Save zero records
    # --------------------------------------------------------

    zero_df.to_csv(
        OUTPUT_CSV,
        index=False,
        encoding="utf-8-sig"
    )

    print(
        f"✓ Zero CGPA records saved:\n"
        f"  {OUTPUT_CSV}"
    )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    numeric_cgpa = pd.to_numeric(
        df[TARGET_COLUMN],
        errors="coerce"
    )

    total_records = len(df)

    zero_count = int(
        (numeric_cgpa == 0).sum()
    )

    valid_positive_count = int(
        (
            (numeric_cgpa > 0)
            &
            (numeric_cgpa <= 4)
        ).sum()
    )

    missing_count = int(
        numeric_cgpa.isna().sum()
    )

    invalid_high_count = int(
        (numeric_cgpa > 4).sum()
    )

    summary = pd.DataFrame([
        {
            "metric": "total_records",
            "value": total_records
        },
        {
            "metric": "zero_cgpa_records",
            "value": zero_count
        },
        {
            "metric": "valid_positive_cgpa_records",
            "value": valid_positive_count
        },
        {
            "metric": "missing_cgpa_records",
            "value": missing_count
        },
        {
            "metric": "above_4_cgpa_records",
            "value": invalid_high_count
        },
    ])

    summary.to_csv(
        SUMMARY_CSV,
        index=False,
        encoding="utf-8-sig"
    )

    print(
        f"✓ Summary saved:\n"
        f"  {SUMMARY_CSV}"
    )


# ============================================================================
# FINAL RECOMMENDATION
# ============================================================================

def final_recommendation(zero_df):

    section("FINAL INVESTIGATION STATUS")

    count = len(zero_df)

    if count == 0:

        print(
            "✓ No CGPA = 0 records exist."
        )

        print(
            "\nTarget rule can use:"
        )

        print(
            "0 < CGPA <= 4.0"
        )

        return

    print(
        f"CGPA = 0 records investigated: {count}"
    )

    print()
    print(
        "⚠ DO NOT automatically delete CGPA = 0."
    )

    print()
    print(
        "The investigation report has been generated."
    )

    print()
    print(
        "NEXT DECISION:"
    )

    print(
        "1. Review zero_cgpa_records.csv"
    )

    print(
        "2. Determine whether 0 means genuine CGPA"
    )

    print(
        "3. Determine whether 0 means missing/unavailable CGPA"
    )

    print(
        "4. Determine whether 0 is a data-entry artifact"
    )

    print()
    print(
        "Only after this decision should the target-cleaning"
    )

    print(
        "rule be permanently locked."
    )


# ============================================================================
# MAIN PIPELINE
# ============================================================================

def main():

    print()
    print("=" * 80)
    print(
        "AI STUDENT ANALYTICS DASHBOARD"
    )
    print(
        "CGPA = 0.0 SEMANTIC INVESTIGATION"
    )
    print("=" * 80)

    # --------------------------------------------------------
    # Load
    # --------------------------------------------------------

    df = load_dataset()

    # --------------------------------------------------------
    # Validate
    # --------------------------------------------------------

    df = validate_target(df)

    # --------------------------------------------------------
    # Zero records
    # --------------------------------------------------------

    zero_df = get_zero_records(df)

    if zero_df.empty:

        final_recommendation(
            zero_df
        )

        return

    # --------------------------------------------------------
    # Find important columns
    # --------------------------------------------------------

    academic_columns = get_academic_columns(
        df
    )

    section("DETECTED ACADEMIC / CONTEXT COLUMNS")

    for name, column in academic_columns.items():

        print(
            f"✓ {name:20} : {column}"
        )

    # --------------------------------------------------------
    # Display records
    # --------------------------------------------------------

    display_zero_records(
        zero_df,
        academic_columns
    )

    # --------------------------------------------------------
    # Distribution analysis
    # --------------------------------------------------------

    for name, column in academic_columns.items():

        analyze_column_distribution(
            zero_df,
            column,
            name
        )

    # --------------------------------------------------------
    # Numerical patterns
    # --------------------------------------------------------

    analyze_numeric_patterns(
        zero_df,
        academic_columns
    )

    # --------------------------------------------------------
    # Semantic signals
    # --------------------------------------------------------

    investigate_semantic_signals(
        zero_df,
        academic_columns
    )

    # --------------------------------------------------------
    # Zero vs non-zero
    # --------------------------------------------------------

    compare_zero_vs_nonzero(
        df,
        zero_df,
        academic_columns
    )

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    save_investigation(
        zero_df,
        df,
        academic_columns
    )

    # --------------------------------------------------------
    # Recommendation
    # --------------------------------------------------------

    final_recommendation(
        zero_df
    )

    print()
    print("=" * 80)
    print(
        "ZERO CGPA INVESTIGATION COMPLETE"
    )
    print("=" * 80)


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    main()