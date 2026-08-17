"""
AI Student Analytics Dashboard
================================

DATA QUALITY CHECK

Purpose
-------
Inspect the cleaned IUBAT CGPA dataset before building the
production machine-learning pipeline.

This module DOES NOT:
    - delete rows
    - delete columns
    - modify the original Excel file
    - train a model
    - perform imputation
    - encode categorical features

It only identifies data-quality issues.

Next stages:
    data_validation.py
        ↓
    data_leakage_audit.py
        ↓
    data_quality_check.py
        ↓
    feature_engineering.py
        ↓
    preprocessing.py
        ↓
    model training
"""


from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATASET_PATH = (
    BASE_DIR
    / "dataset"
    / "IUBAT_CGPA_Cleaned.xlsx"
)


# ============================================================
# TARGET
# ============================================================

TARGET_COLUMN = "What is your current CGPA?"


# ============================================================
# IMPORTANT NUMERICAL COLUMNS
# ============================================================

NUMERICAL_COLUMNS = [

    "Age (Years)",

    "H.S.C passing year",

    "University Admission year",

    "How many hour do you study daily? (Hours )",

    "How many times do you seat for study in a day?",

    "How many hour do you spent daily in social media? (Hours)",

    "How many hour do you spent daily on skill development? (Hours )",

]


# ============================================================
# EXPECTED NUMERICAL RANGES
# ============================================================

EXPECTED_RANGES = {

    "Age (Years)": (
        15,
        80
    ),

    "H.S.C passing year": (
        1950,
        2035
    ),

    "University Admission year": (
        1950,
        2035
    ),

    "How many hour do you study daily? (Hours )": (
        0,
        24
    ),

    "How many times do you seat for study in a day?": (
        0,
        30
    ),

    "How many hour do you spent daily in social media? (Hours)": (
        0,
        24
    ),

    "How many hour do you spent daily on skill development? (Hours )": (
        0,
        24
    ),

}


# ============================================================
# CATEGORICAL / HIGH CARDINALITY COLUMNS
# ============================================================

CATEGORICAL_COLUMNS = [

    "What is your monthly Family Income",

    "What is you interested area?",

    "What are the skills do you have ?",

    "What is your relationship status?",

    "Status of your English language proficiency",

    "What is your preferable learning mode?",

    "Gender",

]


# ============================================================
# LOAD DATASET
# ============================================================

def load_dataset():

    print()
    print("=" * 80)
    print("LOADING DATASET")
    print("=" * 80)

    print()
    print(
        f"Dataset location:\n{DATASET_PATH}"
    )

    if not DATASET_PATH.exists():

        raise FileNotFoundError(
            f"\nDataset not found:\n{DATASET_PATH}"
        )

    df = pd.read_excel(
        DATASET_PATH
    )

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    print()
    print(
        f"Rows    : {df.shape[0]}"
    )

    print(
        f"Columns : {df.shape[1]}"
    )

    return df


# ============================================================
# DATASET OVERVIEW
# ============================================================

def dataset_overview(df):

    print()
    print("=" * 80)
    print("DATASET OVERVIEW")
    print("=" * 80)

    print()

    print(
        f"Total rows    : {len(df)}"
    )

    print(
        f"Total columns : {len(df.columns)}"
    )

    print()

    print("Column names:")

    for index, column in enumerate(
        df.columns,
        start=1
    ):

        print(
            f"{index:02d}. {column}"
        )


# ============================================================
# MISSING VALUE CHECK
# ============================================================

def missing_value_check(df):

    print()
    print("=" * 80)
    print("MISSING VALUE CHECK")
    print("=" * 80)

    results = []

    for column in df.columns:

        missing = (
            df[column]
            .isna()
            .sum()
        )

        percentage = (
            missing
            / len(df)
            * 100
        )

        results.append(
            {
                "column": column,
                "missing": int(missing),
                "percentage": round(
                    percentage,
                    2
                ),
            }
        )

    report = pd.DataFrame(
        results
    )

    report = report[
        report["missing"] > 0
    ].sort_values(
        by="missing",
        ascending=False
    )

    print()

    if report.empty:

        print(
            "✓ No missing values found."
        )

    else:

        print(
            report.to_string(
                index=False
            )
        )

    return report


# ============================================================
# DUPLICATE CHECK
# ============================================================

def duplicate_check(df):

    print()
    print("=" * 80)
    print("DUPLICATE ROW CHECK")
    print("=" * 80)

    duplicate_count = (
        df.duplicated()
        .sum()
    )

    print()

    print(
        f"Duplicate rows: {duplicate_count}"
    )

    if duplicate_count == 0:

        print(
            "✓ No duplicate rows."
        )

    else:

        print(
            "⚠ Duplicate rows detected."
        )

        duplicates = df[
            df.duplicated(
                keep=False
            )
        ]

        print()

        print(
            duplicates.head(20)
            .to_string(
                index=True
            )
        )

    return duplicate_count


# ============================================================
# TARGET / CGPA CHECK
# ============================================================

def target_quality_check(df):

    print()
    print("=" * 80)
    print("CGPA TARGET QUALITY CHECK")
    print("=" * 80)

    if TARGET_COLUMN not in df.columns:

        raise ValueError(
            f"Target column not found:\n"
            f"{TARGET_COLUMN}"
        )

    target = pd.to_numeric(
        df[TARGET_COLUMN],
        errors="coerce"
    )

    missing_mask = target.isna()

    invalid_mask = (
        target.notna()
        & (
            (target < 0)
            | (target > 4)
        )
    )

    print()

    print(
        f"Missing CGPA values : "
        f"{missing_mask.sum()}"
    )

    print(
        f"Invalid CGPA values : "
        f"{invalid_mask.sum()}"
    )

    if invalid_mask.any():

        print()
        print(
            "INVALID CGPA RECORDS:"
        )

        invalid_rows = df.loc[
            invalid_mask,
            [TARGET_COLUMN]
        ].copy()

        invalid_rows.insert(
            0,
            "row_number",
            invalid_rows.index + 2
        )

        print(
            invalid_rows.to_string(
                index=False
            )
        )

    valid_target = target[
        ~missing_mask
        & ~invalid_mask
    ]

    if not valid_target.empty:

        print()
        print(
            "VALID CGPA STATISTICS:"
        )

        print(
            f"Minimum : "
            f"{valid_target.min():.3f}"
        )

        print(
            f"Maximum : "
            f"{valid_target.max():.3f}"
        )

        print(
            f"Mean    : "
            f"{valid_target.mean():.3f}"
        )

        print(
            f"Median  : "
            f"{valid_target.median():.3f}"
        )

        print(
            f"Std Dev : "
            f"{valid_target.std():.3f}"
        )

    return {
        "missing": int(
            missing_mask.sum()
        ),
        "invalid": int(
            invalid_mask.sum()
        ),
    }


# ============================================================
# NUMERICAL QUALITY CHECK
# ============================================================

def numerical_quality_check(df):

    print()
    print("=" * 80)
    print("NUMERICAL FEATURE QUALITY CHECK")
    print("=" * 80)

    all_results = []

    for column in NUMERICAL_COLUMNS:

        if column not in df.columns:

            print()
            print(
                f"⚠ Column not found: {column}"
            )

            continue

        numeric_values = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        minimum, maximum = (
            EXPECTED_RANGES[column]
        )

        invalid_mask = (
            numeric_values.notna()
            & (
                (numeric_values < minimum)
                | (numeric_values > maximum)
            )
        )

        invalid_count = (
            invalid_mask.sum()
        )

        print()
        print(
            f"FEATURE: {column}"
        )

        print(
            f"  Data type          : "
            f"{df[column].dtype}"
        )

        print(
            f"  Missing            : "
            f"{numeric_values.isna().sum()}"
        )

        print(
            f"  Unique values      : "
            f"{numeric_values.nunique(dropna=True)}"
        )

        if numeric_values.notna().any():

            print(
                f"  Minimum            : "
                f"{numeric_values.min()}"
            )

            print(
                f"  Maximum            : "
                f"{numeric_values.max()}"
            )

            print(
                f"  Mean               : "
                f"{numeric_values.mean():.3f}"
            )

        print(
            f"  Expected range     : "
            f"{minimum} - {maximum}"
        )

        print(
            f"  Invalid values     : "
            f"{invalid_count}"
        )

        if invalid_count > 0:

            print()
            print(
                "  ⚠ SUSPICIOUS RECORDS:"
            )

            invalid_data = df.loc[
                invalid_mask,
                [column]
            ].copy()

            invalid_data.insert(
                0,
                "row_number",
                invalid_data.index + 2
            )

            print(
                invalid_data.to_string(
                    index=False
                )
            )

        else:

            print(
                "  ✓ No range violations."
            )

        all_results.append(
            {
                "feature": column,
                "invalid_values":
                    int(invalid_count),
            }
        )

    return pd.DataFrame(
        all_results
    )


# ============================================================
# CATEGORICAL QUALITY CHECK
# ============================================================

def categorical_quality_check(df):

    print()
    print("=" * 80)
    print("CATEGORICAL FEATURE QUALITY CHECK")
    print("=" * 80)

    results = []

    for column in CATEGORICAL_COLUMNS:

        if column not in df.columns:

            continue

        series = (
            df[column]
            .dropna()
            .astype(str)
            .str.strip()
        )

        unique_count = (
            series.nunique()
        )

        results.append(
            {
                "feature": column,
                "unique_values":
                    unique_count,
            }
        )

        print()
        print(
            f"FEATURE: {column}"
        )

        print(
            f"Unique values: {unique_count}"
        )

        # ----------------------------------------------------
        # Show all values for manageable cardinality
        # ----------------------------------------------------

        if unique_count <= 20:

            print()

            value_counts = (
                series
                .value_counts()
            )

            print(
                value_counts.to_string()
            )

        # ----------------------------------------------------
        # Show sample for high cardinality
        # ----------------------------------------------------

        else:

            print()
            print(
                "⚠ High-cardinality feature."
            )

            print(
                "Sample values:"
            )

            sample_values = (
                series
                .drop_duplicates()
                .head(30)
                .tolist()
            )

            for value in sample_values:

                print(
                    f"  - {value}"
                )

    return pd.DataFrame(
        results
    )


# ============================================================
# FAMILY INCOME INSPECTION
# ============================================================

def inspect_family_income(df):

    column = (
        "What is your monthly Family Income"
    )

    print()
    print("=" * 80)
    print("FAMILY INCOME INSPECTION")
    print("=" * 80)

    if column not in df.columns:

        print(
            "⚠ Family Income column not found."
        )

        return None

    series = df[column]

    print()
    print(
        f"Data type: {series.dtype}"
    )

    print(
        f"Unique values: "
        f"{series.nunique(dropna=True)}"
    )

    print()
    print(
        "Sample raw values:"
    )

    sample = (
        series
        .dropna()
        .astype(str)
        .drop_duplicates()
        .head(50)
    )

    for value in sample:

        print(
            f"  - {value}"
        )

    # --------------------------------------------------------
    # Attempt numeric conversion
    # --------------------------------------------------------

    numeric_version = pd.to_numeric(
        series,
        errors="coerce"
    )

    numeric_success = (
        numeric_version.notna()
        & series.notna()
    ).sum()

    non_missing = (
        series.notna()
    ).sum()

    if non_missing > 0:

        conversion_rate = (
            numeric_success
            / non_missing
            * 100
        )

    else:

        conversion_rate = 0

    print()
    print(
        "Numeric conversion test:"
    )

    print(
        f"Successfully numeric: "
        f"{numeric_success}/{non_missing}"
    )

    print(
        f"Conversion rate: "
        f"{conversion_rate:.2f}%"
    )

    if conversion_rate >= 90:

        print()
        print(
            "✓ Strong indication that "
            "Family Income may be treated as numerical "
            "after proper cleaning."
        )

    else:

        print()
        print(
            "⚠ Family Income appears to contain "
            "non-numeric/category-style values."
        )

    return {
        "unique_values":
            int(series.nunique(dropna=True)),
        "numeric_conversion_rate":
            round(
                conversion_rate,
                2
            ),
    }


# ============================================================
# TEXT QUALITY CHECK
# ============================================================

def text_quality_check(df):

    print()
    print("=" * 80)
    print("TEXT QUALITY CHECK")
    print("=" * 80)

    text_columns = df.select_dtypes(
        include=[
            "object",
            "string"
        ]
    ).columns

    for column in text_columns:

        series = (
            df[column]
            .dropna()
            .astype(str)
        )

        if series.empty:
            continue

        leading_trailing_spaces = (
            series
            != series.str.strip()
        ).sum()

        empty_strings = (
            series
            .str.strip()
            == ""
        ).sum()

        print()
        print(
            f"{column}"
        )

        print(
            f"  Leading/trailing spaces: "
            f"{leading_trailing_spaces}"
        )

        print(
            f"  Empty strings: "
            f"{empty_strings}"
        )


# ============================================================
# POTENTIAL IDENTIFIER CHECK
# ============================================================

def identifier_check(df):

    print()
    print("=" * 80)
    print("POTENTIAL IDENTIFIER CHECK")
    print("=" * 80)

    for column in df.columns:

        unique_count = (
            df[column]
            .nunique(
                dropna=True
            )
        )

        non_missing = (
            df[column]
            .notna()
            .sum()
        )

        if (
            non_missing > 0
            and unique_count == non_missing
        ):

            print()
            print(
                f"⚠ Potential identifier: "
                f"{column}"
            )

            print(
                f"  Unique: "
                f"{unique_count}"
            )

            print(
                f"  Non-missing: "
                f"{non_missing}"
            )

        elif (
            non_missing > 0
            and unique_count / non_missing
            >= 0.95
        ):

            print()
            print(
                f"⚠ Very high uniqueness: "
                f"{column}"
            )

            print(
                f"  Unique ratio: "
                f"{unique_count / non_missing:.2%}"
            )

    print()
    print(
        "Identifier detection is diagnostic only."
    )


# ============================================================
# FINAL SUMMARY
# ============================================================

def print_final_summary(
    df,
    missing_report,
    duplicate_count,
    target_report,
    numerical_report,
    categorical_report,
):

    print()
    print("=" * 80)
    print("DATA QUALITY FINAL SUMMARY")
    print("=" * 80)

    print()

    print(
        f"Rows inspected       : {len(df)}"
    )

    print(
        f"Columns inspected    : {len(df.columns)}"
    )

    print(
        f"Duplicate rows       : {duplicate_count}"
    )

    print(
        f"Missing CGPA         : "
        f"{target_report['missing']}"
    )

    print(
        f"Invalid CGPA        : "
        f"{target_report['invalid']}"
    )

    numerical_invalid = (
        numerical_report[
            "invalid_values"
        ].sum()
        if not numerical_report.empty
        else 0
    )

    print(
        f"Numerical violations : "
        f"{numerical_invalid}"
    )

    if not missing_report.empty:

        print()
        print(
            "Features with missing values:"
        )

        for _, row in missing_report.iterrows():

            print(
                f"  ⚠ {row['column']} "
                f"→ {row['missing']} "
                f"({row['percentage']}%)"
            )

    print()
    print(
        "IMPORTANT:"
    )

    print(
        "No data has been modified."
    )

    print(
        "No rows have been deleted."
    )

    print(
        "No columns have been deleted."
    )

    print(
        "No imputation has been performed."
    )

    print(
        "No model has been trained."
    )

    print()
    print(
        "NEXT STEP:"
    )

    print(
        "Review the suspicious values above and "
        "then finalize the cleaning rules."
    )

    print("=" * 80)


# ============================================================
# MAIN QUALITY PIPELINE
# ============================================================

def run_quality_check():

    print()
    print("=" * 80)
    print("AI STUDENT ANALYTICS DASHBOARD")
    print("IUBAT CGPA DATA QUALITY PIPELINE")
    print("=" * 80)

    # --------------------------------------------------------
    # Load
    # --------------------------------------------------------

    df = load_dataset()

    # --------------------------------------------------------
    # Overview
    # --------------------------------------------------------

    dataset_overview(
        df
    )

    # --------------------------------------------------------
    # Missing values
    # --------------------------------------------------------

    missing_report = (
        missing_value_check(
            df
        )
    )

    # --------------------------------------------------------
    # Duplicates
    # --------------------------------------------------------

    duplicate_count = (
        duplicate_check(
            df
        )
    )

    # --------------------------------------------------------
    # Target
    # --------------------------------------------------------

    target_report = (
        target_quality_check(
            df
        )
    )

    # --------------------------------------------------------
    # Numerical
    # --------------------------------------------------------

    numerical_report = (
        numerical_quality_check(
            df
        )
    )

    # --------------------------------------------------------
    # Categorical
    # --------------------------------------------------------

    categorical_report = (
        categorical_quality_check(
            df
        )
    )

    # --------------------------------------------------------
    # Family Income
    # --------------------------------------------------------

    inspect_family_income(
        df
    )

    # --------------------------------------------------------
    # Text quality
    # --------------------------------------------------------

    text_quality_check(
        df
    )

    # --------------------------------------------------------
    # Identifier check
    # --------------------------------------------------------

    identifier_check(
        df
    )

    # --------------------------------------------------------
    # Final summary
    # --------------------------------------------------------

    print_final_summary(
        df=df,
        missing_report=missing_report,
        duplicate_count=duplicate_count,
        target_report=target_report,
        numerical_report=numerical_report,
        categorical_report=categorical_report,
    )

    return df


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    run_quality_check()