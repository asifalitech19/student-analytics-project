"""
AI Student Analytics Dashboard
================================

LEAKAGE-SAFE FEATURE ENGINEERING

Dataset:
    IUBAT Student Academic Performance Dataset

Purpose:
    - Clean model-ready features
    - Remove known leakage features
    - Handle invalid numerical observations
    - Convert Family Income to numerical
    - Convert multi-response Skills into binary indicators
    - Convert multi-response Interested Area into binary indicators
    - Normalize binary categorical fields
    - Preserve the original dataset
    - Prepare X and y for the preprocessing stage

IMPORTANT:
    This file does NOT train a model.

Pipeline:

    Raw Dataset
        ↓
    Target Cleaning
        ↓
    Leakage Protection
        ↓
    Feature Cleaning
        ↓
    Multi-Label Feature Engineering
        ↓
    Numerical Feature Preparation
        ↓
    Categorical Feature Preparation
        ↓
    Model Dataset
"""

from pathlib import Path
import re

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

TARGET = "What is your current CGPA?"


# ============================================================
# KNOWN LEAKAGE / TIMING-RISK FEATURES
# ============================================================

LEAKAGE_FEATURES = [

    # Explicitly removed by leakage audit
    "Program",

    # Academic progression / outcome-related
    "Current Semester",

    # Potential post-outcome information
    "Did you ever fall in probation?",
    "Did you ever got suspension?",

    # Timing uncertain
    "Average attendance on class (Percentage )",

    "Do you attend in teacher consultancy for any kind of academical problems?",
]


# ============================================================
# CORE NUMERICAL FEATURES
# ============================================================

NUMERICAL_FEATURES = [

    "University Admission year",

    "Age (Years)",

    "H.S.C passing year",

    "How many hour do you study daily? (Hours )",

    "How many times do you seat for study in a day?",

    "How many hour do you spent daily in social media? (Hours)",

    "What is your monthly Family Income",
]


# ============================================================
# CATEGORICAL FEATURES
# ============================================================

CATEGORICAL_FEATURES = [

    "Gender",

    "Do you have meritorious scholarship ?",

    "Do you use University transportation?",

    "What is your preferable learning mode?",

    "Do you use smart phone?",

    "Do you have personal Computer?",

    "Status of your English language proficiency",

    "What is your relationship status?",

    "Are you engaged with any co-curriculum activities?",

    "With whom you are living with?",

    "Do you have any health issues?",

    "Do you have any physical disabilities?",
]


# ============================================================
# MULTI-RESPONSE FEATURES
# ============================================================

MULTI_RESPONSE_COLUMNS = {

    "What are the skills do you have ?":
        "skill",

    "What is you interested area?":
        "interest",
}


# ============================================================
# EXPECTED NUMERICAL RANGES
# ============================================================

NUMERICAL_RANGES = {

    "Age (Years)": (
        15,
        80,
    ),

    "H.S.C passing year": (
        1950,
        2035,
    ),

    "University Admission year": (
        1950,
        2035,
    ),

    "How many hour do you study daily? (Hours )": (
        0,
        24,
    ),

    "How many times do you seat for study in a day?": (
        0,
        30,
    ),

    "How many hour do you spent daily in social media? (Hours)": (
        0,
        24,
    ),

    "What is your monthly Family Income": (
        0,
        np.inf,
    ),
}


# ============================================================
# LOAD DATASET
# ============================================================

def load_dataset():

    print()
    print("=" * 80)
    print("LOADING RAW DATASET")
    print("=" * 80)

    print()
    print(
        f"Dataset: {DATASET_PATH}"
    )

    if not DATASET_PATH.exists():

        raise FileNotFoundError(
            f"\nDataset not found:\n{DATASET_PATH}"
        )

    df = pd.read_excel(
        DATASET_PATH
    )

    # Normalize column names
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    print(
        f"Rows    : {df.shape[0]}"
    )

    print(
        f"Columns : {df.shape[1]}"
    )

    return df


# ============================================================
# TARGET CLEANING
# ============================================================

def clean_target(df):

    print()
    print("=" * 80)
    print("TARGET CLEANING")
    print("=" * 80)

    if TARGET not in df.columns:

        raise ValueError(
            f"Target column not found:\n{TARGET}"
        )

    result = df.copy()

    # Convert target to numeric
    result[TARGET] = pd.to_numeric(
        result[TARGET],
        errors="coerce",
    )

    missing_target = (
        result[TARGET].isna()
    )

    invalid_target = (
        result[TARGET].notna()
        & (
            (result[TARGET] < 0)
            | (result[TARGET] > 4)
        )
    )

    missing_count = (
        missing_target.sum()
    )

    invalid_count = (
        invalid_target.sum()
    )

    rows_before = len(result)

    # Target is unavailable for prediction/training
    result = result.loc[
        ~missing_target
        & ~invalid_target
    ].copy()

    rows_removed = (
        rows_before
        - len(result)
    )

    print()
    print(
        f"Missing CGPA       : "
        f"{missing_count}"
    )

    print(
        f"Invalid CGPA       : "
        f"{invalid_count}"
    )

    print(
        f"Rows removed       : "
        f"{rows_removed}"
    )

    print(
        f"Rows remaining     : "
        f"{len(result)}"
    )

    # Safety validation
    if result[TARGET].isna().any():

        raise RuntimeError(
            "Target still contains missing values."
        )

    if (
        (result[TARGET] < 0)
        | (result[TARGET] > 4)
    ).any():

        raise RuntimeError(
            "Target still contains invalid CGPA values."
        )

    print()
    print(
        "✓ Target cleaning completed."
    )

    return result


# ============================================================
# LEAKAGE PROTECTION
# ============================================================

def remove_leakage_features(df):

    print()
    print("=" * 80)
    print("LEAKAGE PROTECTION")
    print("=" * 80)

    result = df.copy()

    removed = []
    missing = []

    for column in LEAKAGE_FEATURES:

        if column in result.columns:

            result = result.drop(
                columns=[column]
            )

            removed.append(
                column
            )

        else:

            missing.append(
                column
            )

    print()

    for column in removed:

        print(
            f"✓ Removed: {column}"
        )

    for column in missing:

        print(
            f"⚠ Not present: {column}"
        )

    # --------------------------------------------------------
    # Target must NEVER be an input feature
    # --------------------------------------------------------

    if TARGET in result.columns:

        print()
        print(
            "✓ Target retained separately "
            "for y and excluded from X."
        )

    return result


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text_columns(df):

    print()
    print("=" * 80)
    print("TEXT NORMALIZATION")
    print("=" * 80)

    result = df.copy()

    for column in result.select_dtypes(
        include=["object", "string"]
    ).columns:

        result[column] = (
            result[column]
            .astype("string")
            .str.strip()
        )

    print()
    print(
        "✓ Leading/trailing whitespace removed."
    )

    return result


# ============================================================
# NUMERICAL CLEANING
# ============================================================

def clean_numerical_features(df):

    print()
    print("=" * 80)
    print("NUMERICAL FEATURE CLEANING")
    print("=" * 80)

    result = df.copy()

    for column in NUMERICAL_FEATURES:

        if column not in result.columns:

            print()
            print(
                f"⚠ Numerical column missing: "
                f"{column}"
            )

            continue

        # Convert to numeric
        result[column] = pd.to_numeric(
            result[column],
            errors="coerce",
        )

        if column in NUMERICAL_RANGES:

            minimum, maximum = (
                NUMERICAL_RANGES[column]
            )

            invalid_mask = (
                result[column].notna()
                & (
                    (result[column] < minimum)
                    | (result[column] > maximum)
                )
            )

            invalid_count = (
                invalid_mask.sum()
            )

            if invalid_count > 0:

                print()
                print(
                    f"⚠ {column}"
                )

                print(
                    f"  Invalid values: "
                    f"{invalid_count}"
                )

                print(
                    "  Converted invalid "
                    "values to NaN."
                )

                # DO NOT delete student records.
                # Invalid feature values become
                # missing values and will later
                # be imputed inside the ML pipeline.
                result.loc[
                    invalid_mask,
                    column
                ] = np.nan

            else:

                print(
                    f"✓ {column}"
                )

        else:

            print(
                f"✓ {column}"
            )

    print()
    print(
        "✓ Numerical cleaning completed."
    )

    return result


# ============================================================
# BINARY NORMALIZATION
# ============================================================

def normalize_binary_column(series):

    if series is None:
        return series

    result = (
        series
        .astype("string")
        .str.strip()
        .str.lower()
    )

    mapping = {

        "yes": "Yes",
        "y": "Yes",
        "true": "Yes",
        "1": "Yes",

        "no": "No",
        "n": "No",
        "false": "No",
        "0": "No",

    }

    result = result.map(
        lambda value:
        mapping.get(
            value,
            value
        )
        if pd.notna(value)
        else pd.NA
    )

    return result


# ============================================================
# CATEGORICAL CLEANING
# ============================================================

def clean_categorical_features(df):

    print()
    print("=" * 80)
    print("CATEGORICAL FEATURE CLEANING")
    print("=" * 80)

    result = df.copy()

    binary_columns = [

        "Do you have meritorious scholarship ?",

        "Do you use University transportation?",

        "Do you use smart phone?",

        "Do you have personal Computer?",

        "Are you engaged with any co-curriculum activities?",

        "Do you have any health issues?",

        "Do you have any physical disabilities?",

    ]

    for column in binary_columns:

        if column not in result.columns:
            continue

        result[column] = (
            normalize_binary_column(
                result[column]
            )
        )

        print(
            f"✓ Normalized: {column}"
        )

    # General categorical cleanup
    for column in CATEGORICAL_FEATURES:

        if column not in result.columns:
            continue

        result[column] = (
            result[column]
            .astype("string")
            .str.strip()
        )

    print()
    print(
        "✓ Categorical cleaning completed."
    )

    return result


# ============================================================
# MULTI-LABEL VALUE NORMALIZATION
# ============================================================

def normalize_multi_value(value):

    if pd.isna(value):
        return []

    text = str(value).strip()

    if not text:
        return []

    # Split comma-separated responses
    parts = text.split(",")

    cleaned = []

    for part in parts:

        item = (
            part
            .strip()
            .lower()
        )

        # Normalize repeated whitespace
        item = re.sub(
            r"\s+",
            " ",
            item
        )

        if item:

            cleaned.append(
                item
            )

    return sorted(
        set(cleaned)
    )


# ============================================================
# MULTI-LABEL FEATURE ENGINEERING
# ============================================================

def create_multi_label_features(
    df,
    source_column,
    prefix,
):

    result = df.copy()

    if source_column not in result.columns:

        print()
        print(
            f"⚠ Column not found: "
            f"{source_column}"
        )

        return result

    print()
    print(
        f"Processing multi-response feature:"
    )

    print(
        f"  Source : {source_column}"
    )

    print(
        f"  Prefix : {prefix}"
    )

    parsed_values = (
        result[source_column]
        .apply(
            normalize_multi_value
        )
    )

    all_categories = sorted(
        {
            item
            for values in parsed_values
            for item in values
        }
    )

    print(
        f"  Categories discovered: "
        f"{len(all_categories)}"
    )

    for category in all_categories:

        # Safe column name
        safe_name = re.sub(
            r"[^a-z0-9]+",
            "_",
            category
        ).strip("_")

        feature_name = (
            f"{prefix}_{safe_name}"
        )

        result[feature_name] = (
            parsed_values
            .apply(
                lambda values:
                int(
                    category
                    in values
                )
            )
        )

    # Remove original multi-response
    # text columns from model inputs.
    result = result.drop(
        columns=[source_column]
    )

    print(
        f"✓ Created {len(all_categories)} "
        f"{prefix} indicator features."
    )

    return result


# ============================================================
# BUILD MODEL DATASET
# ============================================================

def build_model_dataset(df):

    print()
    print("=" * 80)
    print("BUILDING MODEL DATASET")
    print("=" * 80)

    result = df.copy()

    # --------------------------------------------------------
    # Remove multi-response text fields
    # by converting them into indicators
    # --------------------------------------------------------

    for source_column, prefix in (
        MULTI_RESPONSE_COLUMNS.items()
    ):

        result = create_multi_label_features(
            result,
            source_column,
            prefix,
        )

    # --------------------------------------------------------
    # Separate target
    # --------------------------------------------------------

    y = result[TARGET].copy()

    X = result.drop(
        columns=[TARGET]
    ).copy()

    # --------------------------------------------------------
    # Identify final columns
    # --------------------------------------------------------

    numerical_features = [
        column
        for column in X.columns
        if pd.api.types.is_numeric_dtype(
            X[column]
        )
    ]

    categorical_features = [
        column
        for column in X.columns
        if column not in numerical_features
    ]

    # --------------------------------------------------------
    # Safety check
    # --------------------------------------------------------

    leakage_remaining = [
        column
        for column in LEAKAGE_FEATURES
        if column in X.columns
    ]

    if leakage_remaining:

        raise RuntimeError(
            "Leakage features still present:\n"
            + "\n".join(
                leakage_remaining
            )
        )

    if TARGET in X.columns:

        raise RuntimeError(
            "Target column leaked into X."
        )

    print()
    print(
        f"X shape              : "
        f"{X.shape}"
    )

    print(
        f"y shape              : "
        f"{y.shape}"
    )

    print(
        f"Numerical features   : "
        f"{len(numerical_features)}"
    )

    print(
        f"Categorical features : "
        f"{len(categorical_features)}"
    )

    print()
    print(
        "Numerical features:"
    )

    for feature in numerical_features:

        print(
            f"  ✓ {feature}"
        )

    print()
    print(
        "Categorical features:"
    )

    for feature in categorical_features:

        print(
            f"  ✓ {feature}"
        )

    return (
        X,
        y,
        numerical_features,
        categorical_features,
    )


# ============================================================
# FEATURE ENGINEERING SUMMARY
# ============================================================

def print_summary(
    original_df,
    cleaned_df,
    X,
    y,
):

    print()
    print("=" * 80)
    print("FEATURE ENGINEERING SUMMARY")
    print("=" * 80)

    print()

    print(
        f"Original rows       : "
        f"{len(original_df)}"
    )

    print(
        f"Training-ready rows : "
        f"{len(cleaned_df)}"
    )

    print(
        f"Original columns    : "
        f"{len(original_df.columns)}"
    )

    print(
        f"Model input columns : "
        f"{X.shape[1]}"
    )

    print(
        f"Target              : "
        f"{TARGET}"
    )

    print()

    print(
        "Leakage protection:"
    )

    for feature in LEAKAGE_FEATURES:

        print(
            f"  ✓ {feature}"
        )

    print()
    print(
        "✓ Target excluded from X."
    )

    print(
        "✓ Known leakage features excluded."
    )

    print(
        "✓ Invalid feature values converted "
        "to NaN rather than deleting students."
    )

    print(
        "✓ Family Income treated as numerical."
    )

    print(
        "✓ Skills converted to multi-label "
        "indicator features."
    )

    print(
        "✓ Interested Area converted to "
        "multi-label indicator features."
    )

    print()
    print(
        "✓ Feature engineering completed."
    )

    print(
        "✓ No model training performed."
    )

    print(
        "✓ Original dataset was NOT modified."
    )


# ============================================================
# COMPLETE FEATURE ENGINEERING PIPELINE
# ============================================================

def feature_engineering():

    print()
    print("=" * 80)
    print("AI STUDENT ANALYTICS DASHBOARD")
    print("LEAKAGE-SAFE FEATURE ENGINEERING")
    print("=" * 80)

    # --------------------------------------------------------
    # 1. Load
    # --------------------------------------------------------

    original_df = load_dataset()

    # --------------------------------------------------------
    # 2. Normalize text
    # --------------------------------------------------------

    df = normalize_text_columns(
        original_df
    )

    # --------------------------------------------------------
    # 3. Clean target
    # --------------------------------------------------------

    df = clean_target(
        df
    )

    # --------------------------------------------------------
    # 4. Leakage protection
    # --------------------------------------------------------

    df = remove_leakage_features(
        df
    )

    # --------------------------------------------------------
    # 5. Numerical cleaning
    # --------------------------------------------------------

    df = clean_numerical_features(
        df
    )

    # --------------------------------------------------------
    # 6. Categorical cleaning
    # --------------------------------------------------------

    df = clean_categorical_features(
        df
    )

    # --------------------------------------------------------
    # 7. Build model dataset
    # --------------------------------------------------------

    (
        X,
        y,
        numerical_features,
        categorical_features,
    ) = build_model_dataset(
        df
    )

    # --------------------------------------------------------
    # 8. Summary
    # --------------------------------------------------------

    print_summary(
        original_df=original_df,
        cleaned_df=df,
        X=X,
        y=y,
    )

    return (
        X,
        y,
        numerical_features,
        categorical_features,
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    (
        X,
        y,
        numerical_features,
        categorical_features,
    ) = feature_engineering()
    