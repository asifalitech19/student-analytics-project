"""
======================================================================
AI STUDENT ANALYTICS DASHBOARD
FINAL LEAKAGE-SAFE CGPA REGRESSION PREPROCESSING
FEATURE SET B+ | ACADEMIC CONTEXT
======================================================================

Final feature set:

Demographic
    - Age
    - Gender
    - Relationship Status
    - Living Arrangement
    - Health Issues
    - Physical Disability

Academic
    - University Admission Year
    - H.S.C Passing Year
    - Scholarship
    - English Proficiency
    - Current Semester
    - Completed Credits

Behavior
    - Daily Study Hours
    - Study Sessions per Day
    - Social Media Hours
    - Skill Development Hours
    - Average Attendance

Target:
    What is your current CGPA?

Important:
    - Target is always excluded
    - Current Semester, Attendance and Completed Credits are included
      ONLY as prediction-time-available academic context
    - No Program
    - No Probation
    - No Suspension
    - No Teacher Consultancy
    - No Skills text
    - No Interests text
    - No technology/access variables
"""

from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


# ======================================================================
# PATHS
# ======================================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATASET_PATH = (
    BASE_DIR
    / "dataset"
    / "IUBAT_CGPA_Training_Cleaned.csv"
)


# ======================================================================
# TARGET
# ======================================================================

TARGET = "What is your current CGPA?"


# ======================================================================
# FINAL FEATURE SET B+ | ACADEMIC CONTEXT
# ======================================================================

NUMERICAL_FEATURES = [

    "Age (Years)",

    "University Admission year",

    "H.S.C passing year",

    "Current Semester",

    "Average attendance on class (Percentage )",

    "How many Credit did you have completed?",

    "How many hour do you study daily? (Hours )",

    "How many times do you seat for study in a day?",

    "How many hour do you spent daily in social media? (Hours)",

    "How many hour do you spent daily on your skill development? (Hours )",
]


CATEGORICAL_FEATURES = [

    "Gender",

    "What is your relationship status?",

    "With whom you are living with?",

    "Do you have any health issues?",

    "Do you have any physical disabilities?",

    "Do you have meritorious scholarship ?",

    "Status of your English language proficiency",
]


# ======================================================================
# EXCLUDED / LEAKAGE FEATURES
# ======================================================================

EXCLUDED_FEATURES = [

    "Program",

    "Did you ever fall in probation?",

    "Did you ever got suspension?",

    "Do you attend in teacher consultancy for any kind of academical problems?",

    "Do you use University transportation?",

    "Do you use smart phone?",

    "Do you have personal Computer?",

    "What is your preferable learning mode?",

    "Are you engaged with any co-curriculum activities?",

    "What is your monthly Family Income",

    "What are the skills do you have ?",

    "What is you interested area?",
]


# ======================================================================
# TEXT NORMALIZATION
# ======================================================================

def normalize_text(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

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


# ======================================================================
# LOAD DATASET
# ======================================================================

def load_dataset() -> pd.DataFrame:

    print("=" * 70)
    print("LOADING FINAL CLEANED DATASET")
    print("=" * 70)

    print(
        f"Dataset: {DATASET_PATH}"
    )

    if not DATASET_PATH.exists():

        raise FileNotFoundError(
            f"\nDataset not found:\n{DATASET_PATH}"
        )

    df = pd.read_csv(
        DATASET_PATH
    )

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    print(
        f"Rows    : {len(df)}"
    )

    print(
        f"Columns : {len(df.columns)}"
    )

    return df


# ======================================================================
# REQUIRED COLUMN VALIDATION
# ======================================================================

def validate_columns(df: pd.DataFrame):

    print()
    print("=" * 70)
    print("FINAL FEATURE SET VALIDATION")
    print("=" * 70)

    required_columns = (
        NUMERICAL_FEATURES
        + CATEGORICAL_FEATURES
        + [TARGET]
    )

    missing = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing:

        print(
            "\n❌ Missing required columns:"
        )

        for column in missing:
            print(
                f"   - {column}"
            )

        raise ValueError(
            "Final feature set validation failed."
        )

    print(
        f"✓ Required columns found: "
        f"{len(required_columns)}"
    )


# ======================================================================
# TARGET VALIDATION
# ======================================================================

def validate_target(df: pd.DataFrame):

    print()
    print("=" * 70)
    print("TARGET VALIDATION")
    print("=" * 70)

    df = df.copy()

    df[TARGET] = pd.to_numeric(
        df[TARGET],
        errors="coerce"
    )

    missing = df[TARGET].isna().sum()

    invalid = (
        (df[TARGET] < 0)
        | (df[TARGET] > 4)
    ).sum()

    if missing > 0:

        raise ValueError(
            f"Missing target values found: {missing}"
        )

    if invalid > 0:

        raise ValueError(
            f"Invalid target values found: {invalid}"
        )

    if (df[TARGET] == 0).any():

        raise ValueError(
            "CGPA = 0 detected in cleaned training dataset."
        )

    print(
        f"Rows               : {len(df)}"
    )

    print(
        f"Missing target     : {missing}"
    )

    print(
        f"Invalid target     : {invalid}"
    )

    print(
        f"Minimum CGPA       : {df[TARGET].min():.3f}"
    )

    print(
        f"Maximum CGPA       : {df[TARGET].max():.3f}"
    )

    print(
        f"Mean CGPA          : {df[TARGET].mean():.3f}"
    )

    print(
        "✓ Target validation passed."
    )

    return df


# ======================================================================
# NUMERICAL CLEANING
# ======================================================================

def clean_numerical_features(
    df: pd.DataFrame
) -> pd.DataFrame:

    print()
    print("=" * 70)
    print("NUMERICAL FEATURE CLEANING")
    print("=" * 70)

    df = df.copy()

    for column in NUMERICAL_FEATURES:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    rules = {

        "Age (Years)": (
            15,
            80
        ),

        "University Admission year": (
            1990,
            2035
        ),

        "H.S.C passing year": (
            1990,
            2035
        ),

        "Current Semester": (
            1,
            12
        ),

        "Average attendance on class (Percentage )": (
            0,
            100
        ),

        "How many Credit did you have completed?": (
            0,
            160
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

        "How many hour do you spent daily on your skill development? (Hours )": (
            0,
            24
        ),
    }

    for column, (
        minimum,
        maximum
    ) in rules.items():

        invalid_mask = (
            (df[column] < minimum)
            |
            (df[column] > maximum)
        )

        invalid_count = (
            invalid_mask.sum()
        )

        if invalid_count > 0:

            print(
                f"⚠ {column}"
            )

            print(
                f"  Invalid values: "
                f"{invalid_count}"
            )

            print(
                "  Converted to NaN for "
                "training-time imputation."
            )

            df.loc[
                invalid_mask,
                column
            ] = np.nan

        else:

            print(
                f"✓ {column}"
            )

    return df


# ======================================================================
# CATEGORICAL CLEANING
# ======================================================================

def clean_categorical_features(
    df: pd.DataFrame
) -> pd.DataFrame:

    print()
    print("=" * 70)
    print("CATEGORICAL FEATURE CLEANING")
    print("=" * 70)

    df = df.copy()

    for column in CATEGORICAL_FEATURES:

        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )

        df[column] = df[column].replace(
            {
                "": pd.NA,
                "nan": pd.NA,
                "None": pd.NA,
                "N/A": pd.NA,
                "NA": pd.NA,
            }
        )

        print(
            f"✓ {column}"
        )

    return df


# ======================================================================
# BUILD X / y
# ======================================================================

def build_model_data(df):

    print()
    print("=" * 70)
    print("BUILDING FINAL MODEL DATA")
    print("=" * 70)

    X = df[
        NUMERICAL_FEATURES
        + CATEGORICAL_FEATURES
    ].copy()

    y = df[
        TARGET
    ].astype(float).copy()

    # ------------------------------------------------------------------
    # Target leakage check
    # ------------------------------------------------------------------

    if TARGET in X.columns:

        raise RuntimeError(
            "TARGET LEAKAGE DETECTED."
        )

    # ------------------------------------------------------------------
    # Excluded feature check
    # ------------------------------------------------------------------

    forbidden_found = [
        column
        for column in EXCLUDED_FEATURES
        if column in X.columns
    ]

    if forbidden_found:

        raise RuntimeError(
            "Excluded features detected:\n"
            + "\n".join(
                forbidden_found
            )
        )

    print(
        f"X shape : {X.shape}"
    )

    print(
        f"y shape : {y.shape}"
    )

    print(
        f"Input features : {X.shape[1]}"
    )

    print(
        "✓ Target excluded."
    )

    print(
        "✓ Leakage/post-outcome features excluded."
    )

    print(
        "✓ Feature Set B+ locked (17 raw features)."
    )

    return X, y


# ======================================================================
# TRAIN / TEST SPLIT
# ======================================================================

def split_data(
    X,
    y
):

    print()
    print("=" * 70)
    print("TRAIN / TEST SPLIT")
    print("=" * 70)

    X_train_raw, X_test_raw, y_train, y_test = (
        train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=42,
        )
    )

    print(
        f"Training samples : "
        f"{len(X_train_raw)}"
    )

    print(
        f"Testing samples  : "
        f"{len(X_test_raw)}"
    )

    return (
        X_train_raw,
        X_test_raw,
        y_train,
        y_test,
    )


# ======================================================================
# PREPROCESSOR
# ======================================================================

def build_preprocessor(
    X_train_raw
):

    print()
    print("=" * 70)
    print("BUILDING PREPROCESSING PIPELINE")
    print("=" * 70)

    numerical_columns = [
        column
        for column in X_train_raw.columns
        if column in NUMERICAL_FEATURES
    ]

    categorical_columns = [
        column
        for column in X_train_raw.columns
        if column in CATEGORICAL_FEATURES
    ]

    numerical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="median"
                ),
            ),
            (
                "scaler",
                StandardScaler(),
            ),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="most_frequent"
                ),
            ),
            (
                "encoder",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=False,
                ),
            ),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "numerical",
                numerical_pipeline,
                numerical_columns,
            ),
            (
                "categorical",
                categorical_pipeline,
                categorical_columns,
            ),
        ],
        remainder="drop",
        verbose_feature_names_out=True,
    )

    print(
        f"Numerical features   : "
        f"{len(numerical_columns)}"
    )

    print(
        f"Categorical features : "
        f"{len(categorical_columns)}"
    )

    return preprocessor


# ======================================================================
# COMPLETE PREPARATION
# ======================================================================

def prepare_data():

    # ------------------------------------------------------------------
    # Load
    # ------------------------------------------------------------------

    df = load_dataset()

    # ------------------------------------------------------------------
    # Normalize
    # ------------------------------------------------------------------

    df = normalize_text(
        df
    )

    # ------------------------------------------------------------------
    # Validate columns
    # ------------------------------------------------------------------

    validate_columns(
        df
    )

    # ------------------------------------------------------------------
    # Validate target
    # ------------------------------------------------------------------

    df = validate_target(
        df
    )

    # ------------------------------------------------------------------
    # Clean numerical
    # ------------------------------------------------------------------

    df = clean_numerical_features(
        df
    )

    # ------------------------------------------------------------------
    # Clean categorical
    # ------------------------------------------------------------------

    df = clean_categorical_features(
        df
    )

    # ------------------------------------------------------------------
    # Build X/y
    # ------------------------------------------------------------------

    X, y = build_model_data(
        df
    )

    # ------------------------------------------------------------------
    # Split
    # ------------------------------------------------------------------

    (
        X_train_raw,
        X_test_raw,
        y_train,
        y_test,
    ) = split_data(
        X,
        y
    )

    # ------------------------------------------------------------------
    # Build preprocessor
    # ------------------------------------------------------------------

    preprocessor = build_preprocessor(
        X_train_raw
    )

    # ------------------------------------------------------------------
    # FIT ONLY ON TRAIN DATA
    # ------------------------------------------------------------------

    print()
    print("=" * 70)
    print("FITTING PREPROCESSOR")
    print("=" * 70)

    X_train = (
        preprocessor
        .fit_transform(
            X_train_raw
        )
    )

    X_test = (
        preprocessor
        .transform(
            X_test_raw
        )
    )

    # ------------------------------------------------------------------
    # Safety checks
    # ------------------------------------------------------------------

    if not np.isfinite(
        X_train
    ).all():

        raise ValueError(
            "X_train contains NaN or infinite values."
        )

    if not np.isfinite(
        X_test
    ).all():

        raise ValueError(
            "X_test contains NaN or infinite values."
        )

    # ------------------------------------------------------------------
    # Final summary
    # ------------------------------------------------------------------

    print()
    print("=" * 70)
    print("FINAL PREPROCESSING RESULT")
    print("=" * 70)

    print(
        f"Raw features       : "
        f"{X_train_raw.shape[1]}"
    )

    print(
        f"Processed features : "
        f"{X_train.shape[1]}"
    )

    print(
        f"X_train shape      : "
        f"{X_train.shape}"
    )

    print(
        f"X_test shape       : "
        f"{X_test.shape}"
    )

    print(
        f"y_train shape      : "
        f"{y_train.shape}"
    )

    print(
        f"y_test shape       : "
        f"{y_test.shape}"
    )

    print()
    print(
        "✓ Feature Set B+ confirmed."
    )

    print(
        "✓ Target leakage protection passed."
    )

    print(
        "✓ Numerical imputation fitted on training data."
    )

    print(
        "✓ Categorical imputation fitted on training data."
    )

    print(
        "✓ OneHotEncoder fitted on training data."
    )

    print(
        "✓ StandardScaler fitted on training data."
    )

    print(
        "✓ READY FOR FINAL MODEL TRAINING."
    )

    # ------------------------------------------------------------------
    # EXACT RETURN STRUCTURE
    # ------------------------------------------------------------------

    return (
        X_train,
        X_test,
        y_train.to_numpy(),
        y_test.to_numpy(),
        preprocessor,
        X_train_raw,
        X_test_raw,
    )


# ======================================================================
# SCRIPT ENTRY
# ======================================================================

if __name__ == "__main__":

    print()
    print("=" * 70)
    print(
        "AI STUDENT ANALYTICS DASHBOARD"
    )
    print(
        "FINAL FEATURE SET B+ | ACADEMIC CONTEXT PREPROCESSING"
    )
    print("=" * 70)

    (
        X_train,
        X_test,
        y_train,
        y_test,
        preprocessor,
        X_train_raw,
        X_test_raw,
    ) = prepare_data()

    print()
    print("=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)

    print(
        f"Training rows : {len(y_train)}"
    )

    print(
        f"Testing rows  : {len(y_test)}"
    )

    print(
        f"Features      : {X_train.shape[1]}"
    )

    print(
        f"CGPA min      : {y_train.min():.2f}"
    )

    print(
        f"CGPA max      : {y_train.max():.2f}"
    )

    print(
        f"CGPA mean     : {y_train.mean():.2f}"
    )

    print()
    print(
        "✓ FINAL PREPROCESSING COMPLETE"
    )