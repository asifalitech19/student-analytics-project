# """
# AI Student Analytics Dashboard
# ================================

# IUBAT CGPA Dataset
# Data Validation Pipeline

# Purpose:
#     Validate the cleaned academic dataset BEFORE machine
#     learning model development.

# Checks:
#     1. Dataset loading
#     2. Dataset structure
#     3. Duplicate records
#     4. Missing values
#     5. Data types
#     6. Target / CGPA validation
#     7. Numerical features
#     8. Categorical features
#     9. Possible identifier columns
#     10. Constant columns

# IMPORTANT:
#     This module does NOT:
#         - train a model
#         - delete columns
#         - delete rows
#         - modify data
#         - perform preprocessing

# It only audits the dataset.
# """

# from pathlib import Path

# import numpy as np
# import pandas as pd


# # ============================================================
# # PATH CONFIGURATION
# # ============================================================

# # Current file:
# #
# # backend/
# # └── app/
# #     └── ml/
# #         └── data_validation.py
# #
# # Therefore parents[2] = backend/

# BASE_DIR = Path(__file__).resolve().parents[2]


# DATASET_DIR = (
#     BASE_DIR / "dataset"
# )


# # ============================================================
# # DATASET FILE
# # ============================================================

# # Your current dataset is Excel.

# DATASET_PATH = (
#     DATASET_DIR
#     / "IUBAT_CGPA_Cleaned.xlsx"
# )


# # ============================================================
# # TARGET COLUMN
# # ============================================================

# TARGET_COLUMN = "What is your current CGPA?"


# # ============================================================
# # LOAD DATASET
# # ============================================================

# def load_dataset() -> pd.DataFrame:
#     """
#     Load the IUBAT dataset.

#     Supports:
#         .xlsx
#         .xls
#         .csv

#     The current project uses .xlsx.
#     """

#     print()
#     print("=" * 75)
#     print("LOADING DATASET")
#     print("=" * 75)

#     print()
#     print("Dataset location:")
#     print(DATASET_PATH)

#     # --------------------------------------------------------
#     # Check dataset file
#     # --------------------------------------------------------

#     if not DATASET_PATH.exists():

#         raise FileNotFoundError(
#             "\nDataset not found.\n\n"
#             f"Expected:\n{DATASET_PATH}\n\n"
#             "Please make sure the dataset exists inside:\n"
#             f"{DATASET_DIR}"
#         )

#     # --------------------------------------------------------
#     # Read according to file extension
#     # --------------------------------------------------------

#     try:

#         extension = (
#             DATASET_PATH
#             .suffix
#             .lower()
#         )

#         if extension == ".xlsx":

#             df = pd.read_excel(
#                 DATASET_PATH
#             )

#         elif extension == ".xls":

#             df = pd.read_excel(
#                 DATASET_PATH
#             )

#         elif extension == ".csv":

#             df = pd.read_csv(
#                 DATASET_PATH
#             )

#         else:

#             raise ValueError(
#                 f"Unsupported dataset format: "
#                 f"{extension}"
#             )

#     except Exception as error:

#         raise RuntimeError(
#             "\nUnable to read dataset.\n"
#             f"Error: {error}"
#         )

#     # --------------------------------------------------------
#     # Remove accidental whitespace from column names
#     #
#     # IMPORTANT:
#     # We are NOT modifying the dataset file.
#     # This only creates cleaned column labels in memory.
#     # --------------------------------------------------------

#     df.columns = (
#         df.columns
#         .astype(str)
#         .str.strip()
#     )

#     print()
#     print("Dataset loaded successfully.")

#     print(
#         f"Rows    : {df.shape[0]}"
#     )

#     print(
#         f"Columns : {df.shape[1]}"
#     )

#     return df


# # ============================================================
# # BASIC STRUCTURE VALIDATION
# # ============================================================

# def validate_basic_structure(
#     df: pd.DataFrame
# ):
#     """
#     Validate the basic structure of the dataset.
#     """

#     print()
#     print("=" * 75)
#     print("1. BASIC DATASET VALIDATION")
#     print("=" * 75)

#     rows = len(df)
#     columns = len(df.columns)

#     print(
#         f"Total rows    : {rows}"
#     )

#     print(
#         f"Total columns : {columns}"
#     )

#     # --------------------------------------------------------
#     # Empty dataset
#     # --------------------------------------------------------

#     if rows == 0:

#         raise ValueError(
#             "Dataset contains zero rows."
#         )

#     if columns == 0:

#         raise ValueError(
#             "Dataset contains zero columns."
#         )

#     # --------------------------------------------------------
#     # Target column
#     # --------------------------------------------------------

#     print()
#     print(
#         "Expected target:"
#     )

#     print(
#         TARGET_COLUMN
#     )

#     if TARGET_COLUMN in df.columns:

#         print(
#             "Target status : FOUND"
#         )

#     else:

#         print(
#             "Target status : NOT FOUND"
#         )

#         print()
#         print(
#             "Actual columns in dataset:"
#         )

#         for index, column in enumerate(
#             df.columns,
#             start=1
#         ):

#             print(
#                 f"{index:02d}. {column}"
#             )

#         raise ValueError(
#             "\nExpected CGPA target column "
#             "was not found."
#         )

#     # --------------------------------------------------------
#     # All columns
#     # --------------------------------------------------------

#     print()
#     print(
#         "All dataset columns:"
#     )

#     for index, column in enumerate(
#         df.columns,
#         start=1
#     ):

#         print(
#             f"{index:02d}. {column}"
#         )


# # ============================================================
# # DUPLICATE CHECK
# # ============================================================

# def check_duplicates(
#     df: pd.DataFrame
# ):
#     """
#     Check for exact duplicate rows.
#     """

#     print()
#     print("=" * 75)
#     print("2. DUPLICATE ROW CHECK")
#     print("=" * 75)

#     duplicate_count = int(
#         df.duplicated().sum()
#     )

#     print(
#         f"Duplicate rows : "
#         f"{duplicate_count}"
#     )

#     if duplicate_count == 0:

#         print(
#             "STATUS         : PASS"
#         )

#         print(
#             "No exact duplicate rows found."
#         )

#     else:

#         percentage = (
#             duplicate_count
#             / len(df)
#             * 100
#         )

#         print(
#             "STATUS         : REVIEW REQUIRED"
#         )

#         print(
#             f"Duplicate percentage : "
#             f"{percentage:.2f}%"
#         )

#         print()
#         print(
#             "No rows will be deleted automatically."
#         )

#     return duplicate_count


# # ============================================================
# # MISSING VALUE ANALYSIS
# # ============================================================

# def check_missing_values(
#     df: pd.DataFrame
# ):
#     """
#     Check missing values in every column.
#     """

#     print()
#     print("=" * 75)
#     print("3. MISSING VALUE ANALYSIS")
#     print("=" * 75)

#     missing_count = df.isna().sum()

#     missing_percentage = (
#         missing_count
#         / len(df)
#         * 100
#     )

#     report = pd.DataFrame(
#         {
#             "column": df.columns,
#             "missing_count": (
#                 missing_count.values
#             ),
#             "missing_percentage": (
#                 missing_percentage.values
#             ),
#         }
#     )

#     report = report[
#         report["missing_count"] > 0
#     ]

#     report = report.sort_values(
#         by="missing_count",
#         ascending=False
#     )

#     if report.empty:

#         print(
#             "STATUS : PASS"
#         )

#         print(
#             "No missing values found."
#         )

#     else:

#         print(
#             "STATUS : REVIEW REQUIRED"
#         )

#         print()

#         print(
#             report.to_string(
#                 index=False
#             )
#         )

#     return report


# # ============================================================
# # DATA TYPE ANALYSIS
# # ============================================================

# def check_data_types(
#     df: pd.DataFrame
# ):
#     """
#     Display all column data types.
#     """

#     print()
#     print("=" * 75)
#     print("4. DATA TYPE ANALYSIS")
#     print("=" * 75)

#     report = pd.DataFrame(
#         {
#             "column": df.columns,
#             "dtype": [
#                 str(dtype)
#                 for dtype in df.dtypes
#             ],
#         }
#     )

#     print(
#         report.to_string(
#             index=False
#         )
#     )

#     return report


# # ============================================================
# # TARGET / CGPA VALIDATION
# # ============================================================

# def check_target(
#     df: pd.DataFrame
# ):
#     """
#     Validate the CGPA target.

#     Expected academic CGPA range:

#         0.00 <= CGPA <= 4.00

#     No values are changed.
#     """

#     print()
#     print("=" * 75)
#     print("5. TARGET / CGPA VALIDATION")
#     print("=" * 75)

#     print()
#     print(
#         f"Target column:"
#     )

#     print(
#         TARGET_COLUMN
#     )

#     # --------------------------------------------------------
#     # Convert only for validation
#     # --------------------------------------------------------

#     target = pd.to_numeric(
#         df[TARGET_COLUMN],
#         errors="coerce"
#     )

#     # --------------------------------------------------------
#     # Missing target
#     # --------------------------------------------------------

#     missing_count = int(
#         target.isna().sum()
#     )

#     # --------------------------------------------------------
#     # Invalid target
#     # --------------------------------------------------------

#     invalid_mask = (
#         target.notna()
#         & (
#             (target < 0)
#             | (target > 4)
#         )
#     )

#     invalid_count = int(
#         invalid_mask.sum()
#     )

#     # --------------------------------------------------------
#     # Valid target
#     # --------------------------------------------------------

#     valid_mask = (
#         target.notna()
#         & (~invalid_mask)
#     )

#     valid_count = int(
#         valid_mask.sum()
#     )

#     # --------------------------------------------------------
#     # Counts
#     # --------------------------------------------------------

#     print()
#     print(
#         f"Total records : "
#         f"{len(df)}"
#     )

#     print(
#         f"Missing CGPA  : "
#         f"{missing_count}"
#     )

#     print(
#         f"Invalid CGPA  : "
#         f"{invalid_count}"
#     )

#     print(
#         f"Valid CGPA    : "
#         f"{valid_count}"
#     )

#     # --------------------------------------------------------
#     # Statistics
#     # --------------------------------------------------------

#     if valid_count > 0:

#         valid_target = (
#             target[valid_mask]
#         )

#         print()
#         print(
#             "CGPA STATISTICS"
#         )

#         print(
#             "-" * 45
#         )

#         print(
#             f"Minimum : "
#             f"{valid_target.min():.3f}"
#         )

#         print(
#             f"Maximum : "
#             f"{valid_target.max():.3f}"
#         )

#         print(
#             f"Mean    : "
#             f"{valid_target.mean():.3f}"
#         )

#         print(
#             f"Median  : "
#             f"{valid_target.median():.3f}"
#         )

#         print(
#             f"Std Dev : "
#             f"{valid_target.std():.3f}"
#         )

#     # --------------------------------------------------------
#     # Invalid values
#     # --------------------------------------------------------

#     if invalid_count > 0:

#         print()
#         print(
#             "INVALID CGPA VALUES"
#         )

#         print(
#             "-" * 45
#         )

#         invalid_values = (
#             target[invalid_mask]
#             .value_counts()
#             .sort_index()
#         )

#         print(
#             invalid_values.to_string()
#         )

#         print()
#         print(
#             "STATUS : REVIEW REQUIRED"
#         )

#     else:

#         print()
#         print(
#             "STATUS : PASS"
#         )

#         print(
#             "All non-missing CGPA values "
#             "are within the 0-4 range."
#         )

#     return {
#         "missing": missing_count,
#         "invalid": invalid_count,
#         "valid": valid_count,
#     }


# # ============================================================
# # NUMERICAL FEATURE ANALYSIS
# # ============================================================

# def check_numeric_columns(
#     df: pd.DataFrame
# ):
#     """
#     Analyze numerical columns.
#     """

#     print()
#     print("=" * 75)
#     print("6. NUMERICAL FEATURE ANALYSIS")
#     print("=" * 75)

#     numeric_columns = (
#         df.select_dtypes(
#             include=np.number
#         )
#         .columns
#         .tolist()
#     )

#     print(
#         f"Numerical columns : "
#         f"{len(numeric_columns)}"
#     )

#     if not numeric_columns:

#         print(
#             "No numerical columns detected."
#         )

#         return None

#     rows = []

#     for column in numeric_columns:

#         series = pd.to_numeric(
#             df[column],
#             errors="coerce"
#         )

#         rows.append(
#             {
#                 "column": column,
#                 "min": series.min(),
#                 "max": series.max(),
#                 "mean": series.mean(),
#                 "median": series.median(),
#                 "missing": int(
#                     series.isna().sum()
#                 ),
#             }
#         )

#     report = pd.DataFrame(
#         rows
#     )

#     print()

#     print(
#         report.to_string(
#             index=False
#         )
#     )

#     return report


# # ============================================================
# # CATEGORICAL FEATURE ANALYSIS
# # ============================================================

# def check_categorical_columns(
#     df: pd.DataFrame
# ):
#     """
#     Analyze categorical columns.
#     """

#     print()
#     print("=" * 75)
#     print("7. CATEGORICAL FEATURE ANALYSIS")
#     print("=" * 75)

#     categorical_columns = (
#         df.select_dtypes(
#             include=[
#                 "object",
#                 "string",
#                 "category",
#             ]
#         )
#         .columns
#         .tolist()
#     )

#     print(
#         f"Categorical columns : "
#         f"{len(categorical_columns)}"
#     )

#     if not categorical_columns:

#         print(
#             "No categorical columns detected."
#         )

#         return

#     for column in categorical_columns:

#         print()
#         print(
#             "-" * 75
#         )

#         print(
#             f"COLUMN: {column}"
#         )

#         print(
#             "-" * 75
#         )

#         values = (
#             df[column]
#             .dropna()
#             .astype(str)
#             .str.strip()
#         )

#         unique_values = sorted(
#             values.unique()
#         )

#         print(
#             f"Unique values : "
#             f"{len(unique_values)}"
#         )

#         # Display first 30 categories
#         # to prevent huge terminal output.

#         limit = 30

#         for value in unique_values[
#             :limit
#         ]:

#             count = int(
#                 (values == value).sum()
#             )

#             print(
#                 f"  {value!r} : {count}"
#             )

#         if len(unique_values) > limit:

#             print()
#             print(
#                 f"... and "
#                 f"{len(unique_values) - limit} "
#                 "more values."
#             )


# # ============================================================
# # POSSIBLE IDENTIFIER CHECK
# # ============================================================

# def check_identifier_columns(
#     df: pd.DataFrame
# ):
#     """
#     Detect columns where every row
#     contains a unique value.

#     These may represent:
#         - Student ID
#         - Record ID
#         - Application ID
#         - Timestamp
#         - Other identifiers

#     They are NOT automatically removed.
#     """

#     print()
#     print("=" * 75)
#     print("8. POSSIBLE IDENTIFIER COLUMN CHECK")
#     print("=" * 75)

#     possible_ids = []

#     for column in df.columns:

#         unique_count = df[
#             column
#         ].nunique(
#             dropna=False
#         )

#         if unique_count == len(df):

#             possible_ids.append(
#                 column
#             )

#     if possible_ids:

#         print(
#             "Potential identifier columns:"
#         )

#         for column in possible_ids:

#             print(
#                 f"  - {column}"
#             )

#         print()
#         print(
#             "STATUS : REVIEW REQUIRED"
#         )

#         print(
#             "These columns will be examined "
#             "during leakage auditing."
#         )

#     else:

#         print(
#             "No fully unique columns detected."
#         )

#     return possible_ids


# # ============================================================
# # CONSTANT COLUMN CHECK
# # ============================================================

# def check_constant_columns(
#     df: pd.DataFrame
# ):
#     """
#     Detect columns containing only one unique value.
#     """

#     print()
#     print("=" * 75)
#     print("9. CONSTANT COLUMN CHECK")
#     print("=" * 75)

#     constant_columns = []

#     for column in df.columns:

#         unique_count = df[
#             column
#         ].nunique(
#             dropna=False
#         )

#         if unique_count <= 1:

#             constant_columns.append(
#                 column
#             )

#     if constant_columns:

#         print(
#             "Constant columns detected:"
#         )

#         for column in constant_columns:

#             print(
#                 f"  - {column}"
#             )

#         print()
#         print(
#             "STATUS : REVIEW REQUIRED"
#         )

#     else:

#         print(
#             "No constant columns detected."
#         )

#     return constant_columns


# # ============================================================
# # FINAL SUMMARY
# # ============================================================

# def print_final_summary(
#     df: pd.DataFrame,
#     duplicate_count: int,
#     target_report: dict,
#     possible_ids: list,
#     constant_columns: list,
# ):
#     """
#     Print final validation summary.
#     """

#     print()
#     print()
#     print("=" * 75)
#     print("FINAL DATA VALIDATION SUMMARY")
#     print("=" * 75)

#     print(
#         f"Rows                : "
#         f"{len(df)}"
#     )

#     print(
#         f"Columns             : "
#         f"{len(df.columns)}"
#     )

#     print(
#         f"Duplicate rows      : "
#         f"{duplicate_count}"
#     )

#     print(
#         f"Missing CGPA        : "
#         f"{target_report['missing']}"
#     )

#     print(
#         f"Invalid CGPA        : "
#         f"{target_report['invalid']}"
#     )

#     print(
#         f"Valid CGPA          : "
#         f"{target_report['valid']}"
#     )

#     print(
#         f"Possible ID columns : "
#         f"{len(possible_ids)}"
#     )

#     print(
#         f"Constant columns    : "
#         f"{len(constant_columns)}"
#     )

#     # --------------------------------------------------------
#     # Target status
#     # --------------------------------------------------------

#     if (
#         target_report["missing"] == 0
#         and target_report["invalid"] == 0
#     ):

#         print()
#         print(
#             "TARGET STATUS : PASS"
#         )

#     else:

#         print()
#         print(
#             "TARGET STATUS : REVIEW REQUIRED"
#         )

#     print()
#     print("=" * 75)
#     print("DATA VALIDATION COMPLETE")
#     print("=" * 75)

#     print()
#     print(
#         "IMPORTANT:"
#     )

#     print(
#         "No rows were automatically deleted."
#     )

#     print(
#         "No columns were automatically deleted."
#     )

#     print(
#         "No values were automatically modified."
#     )

#     print()
#     print(
#         "NEXT STEP:"
#     )

#     print(
#         "Run the leakage audit before "
#         "building the ML model."
#     )

#     print("=" * 75)


# # ============================================================
# # COMPLETE VALIDATION PIPELINE
# # ============================================================

# def run_validation():
#     """
#     Execute the complete validation pipeline.
#     """

#     print()
#     print("=" * 75)
#     print("AI STUDENT ANALYTICS DASHBOARD")
#     print("IUBAT CGPA DATA VALIDATION PIPELINE")
#     print("=" * 75)

#     # --------------------------------------------------------
#     # 1. Load dataset
#     # --------------------------------------------------------

#     df = load_dataset()

#     # --------------------------------------------------------
#     # 2. Basic validation
#     # --------------------------------------------------------

#     validate_basic_structure(
#         df
#     )

#     # --------------------------------------------------------
#     # 3. Duplicate check
#     # --------------------------------------------------------

#     duplicate_count = (
#         check_duplicates(
#             df
#         )
#     )

#     # --------------------------------------------------------
#     # 4. Missing values
#     # --------------------------------------------------------

#     check_missing_values(
#         df
#     )

#     # --------------------------------------------------------
#     # 5. Data types
#     # --------------------------------------------------------

#     check_data_types(
#         df
#     )

#     # --------------------------------------------------------
#     # 6. Target validation
#     # --------------------------------------------------------

#     target_report = check_target(
#         df
#     )

#     # --------------------------------------------------------
#     # 7. Numerical features
#     # --------------------------------------------------------

#     check_numeric_columns(
#         df
#     )

#     # --------------------------------------------------------
#     # 8. Categorical features
#     # --------------------------------------------------------

#     check_categorical_columns(
#         df
#     )

#     # --------------------------------------------------------
#     # 9. Identifier columns
#     # --------------------------------------------------------

#     possible_ids = (
#         check_identifier_columns(
#             df
#         )
#     )

#     # --------------------------------------------------------
#     # 10. Constant columns
#     # --------------------------------------------------------

#     constant_columns = (
#         check_constant_columns(
#             df
#         )
#     )

#     # --------------------------------------------------------
#     # Final summary
#     # --------------------------------------------------------

#     print_final_summary(
#         df=df,
#         duplicate_count=duplicate_count,
#         target_report=target_report,
#         possible_ids=possible_ids,
#         constant_columns=constant_columns,
#     )

#     return df


# # ============================================================
# # MAIN
# # ============================================================

# if __name__ == "__main__":

#     run_validation()



































































































"""
======================================================================
AI STUDENT ANALYTICS DASHBOARD
INDEPENDENT CGPA MODEL VALIDATION
======================================================================

Purpose:
    Validate the already-trained CGPA regression model.

This script:
    1. Loads the existing trained model
    2. Recreates the same preprocessing split
    3. Uses ONLY the independent test set
    4. Calculates MAE, RMSE and R²
    5. Calculates expected GPA error
    6. Compares against a simple mean baseline
    7. Performs error analysis
    8. Saves validation results
    9. Does NOT retrain the model
    10. Does NOT modify the original dataset

======================================================================
"""

import json
import os
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)


# ======================================================================
# PATH CONFIGURATION
# ======================================================================

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_DIR = BASE_DIR / "saved_models"

MODEL_PATH = MODEL_DIR / "cgpa_regression_model.pkl"
METADATA_PATH = MODEL_DIR / "cgpa_model_metadata.json"

VALIDATION_DIR = MODEL_DIR / "validation"

VALIDATION_RESULTS_PATH = (
    VALIDATION_DIR / "validation_results.json"
)

PREDICTIONS_PATH = (
    VALIDATION_DIR / "validation_predictions.csv"
)


# ======================================================================
# PRINT HELPERS
# ======================================================================

def print_header(title):
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


def print_section(title):
    print()
    print("-" * 70)
    print(title)
    print("-" * 70)


# ======================================================================
# LOAD TRAINED MODEL
# ======================================================================

def load_model():

    print_header("LOADING TRAINED MODEL")

    if not MODEL_PATH.exists():

        raise FileNotFoundError(
            f"""
Trained model was not found.

Expected location:
{MODEL_PATH}

Run model_training.py first.
"""
        )

    model = joblib.load(MODEL_PATH)

    print(f"Model path : {MODEL_PATH}")
    print(f"Model type : {type(model).__name__}")

    print("✓ Trained model loaded successfully.")

    return model


# ======================================================================
# LOAD METADATA
# ======================================================================

def load_metadata():

    print_section("LOADING MODEL METADATA")

    if not METADATA_PATH.exists():

        print(
            "⚠ Model metadata file was not found."
        )

        return {}

    try:

        with open(
            METADATA_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            metadata = json.load(file)

        print(
            f"✓ Metadata loaded from:\n{METADATA_PATH}"
        )

        return metadata

    except Exception as error:

        print(
            f"⚠ Could not read metadata: {error}"
        )

        return {}


# ======================================================================
# LOAD PREPROCESSING PIPELINE
# ======================================================================

def load_preprocessed_data():

    """
    IMPORTANT:

    We call prepare_data() only to recreate the exact same
    deterministic train/test split.

    No model is trained here.

    The preprocessing itself must fit transformations only
    on the training partition.
    """

    print_header("RECREATING VALIDATION DATA")

    from app.ml.preprocessing import prepare_data

    result = prepare_data()

    if not isinstance(result, tuple):

        raise ValueError(
            "prepare_data() did not return a tuple."
        )

    print(
        f"Objects returned: {len(result)}"
    )

    # --------------------------------------------------------------
    # Expected output from current preprocessing.py
    # --------------------------------------------------------------

    if len(result) < 4:

        raise ValueError(
            """
prepare_data() returned fewer than 4 objects.

Expected at least:

[0] X_train
[1] X_test
[2] y_train
[3] y_test
"""
        )

    X_train = result[0]
    X_test = result[1]
    y_train = result[2]
    y_test = result[3]

    preprocessor = None

    if len(result) >= 5:

        preprocessor = result[4]

    print_section("VALIDATION DATA")

    print(
        f"X_train shape : {getattr(X_train, 'shape', None)}"
    )

    print(
        f"X_test shape  : {getattr(X_test, 'shape', None)}"
    )

    print(
        f"y_train shape : {getattr(y_train, 'shape', None)}"
    )

    print(
        f"y_test shape  : {getattr(y_test, 'shape', None)}"
    )

    print()
    print("✓ Independent test set recreated.")
    print("✓ Test set will NOT be used for training.")

    return (
        X_train,
        X_test,
        y_train,
        y_test,
        preprocessor,
    )


# ======================================================================
# DATA VALIDATION
# ======================================================================

def validate_data(X_train, X_test, y_train, y_test):

    print_header("VALIDATING TEST DATA")

    # --------------------------------------------------------------
    # Empty checks
    # --------------------------------------------------------------

    if len(X_test) == 0:

        raise ValueError(
            "Test dataset is empty."
        )

    if len(y_test) == 0:

        raise ValueError(
            "Test target is empty."
        )

    # --------------------------------------------------------------
    # Shape checks
    # --------------------------------------------------------------

    if len(X_test) != len(y_test):

        raise ValueError(
            f"""
X_test and y_test have different lengths.

X_test: {len(X_test)}
y_test: {len(y_test)}
"""
        )

    # --------------------------------------------------------------
    # Numeric conversion
    # --------------------------------------------------------------

    y_test_array = np.asarray(
        y_test,
        dtype=float
    )

    # --------------------------------------------------------------
    # Missing target check
    # --------------------------------------------------------------

    missing_targets = np.isnan(
        y_test_array
    ).sum()

    if missing_targets > 0:

        raise ValueError(
            f"Test target contains {missing_targets} missing values."
        )

    # --------------------------------------------------------------
    # CGPA range
    # --------------------------------------------------------------

    invalid_range = (
        (y_test_array < 0)
        | (y_test_array > 4)
    ).sum()

    print(
        f"Test samples       : {len(y_test)}"
    )

    print(
        f"Input features      : {X_test.shape[1]}"
    )

    print(
        f"Missing targets     : {missing_targets}"
    )

    print(
        f"Out-of-range target : {invalid_range}"
    )

    if invalid_range > 0:

        raise ValueError(
            "Test set contains CGPA values outside 0-4."
        )

    print()
    print("✓ Test data validation passed.")

    return y_test_array


# ======================================================================
# MODEL PREDICTION
# ======================================================================

def generate_predictions(model, X_test):

    print_header("GENERATING INDEPENDENT PREDICTIONS")

    print(
        "Training model: NO"
    )

    print(
        "Test data used for fitting: NO"
    )

    print()

    predictions = model.predict(X_test)

    predictions = np.asarray(
        predictions,
        dtype=float
    )

    print(
        f"Predictions generated : {len(predictions)}"
    )

    # --------------------------------------------------------------
    # Check prediction range
    # --------------------------------------------------------------

    print(
        f"Prediction minimum    : {predictions.min():.4f}"
    )

    print(
        f"Prediction maximum    : {predictions.max():.4f}"
    )

    # --------------------------------------------------------------
    # CGPA predictions should normally be 0-4
    # --------------------------------------------------------------

    outside_range = (
        (predictions < 0)
        | (predictions > 4)
    ).sum()

    print(
        f"Predictions outside 0-4 : {outside_range}"
    )

    # --------------------------------------------------------------
    # We do not silently modify predictions.
    # --------------------------------------------------------------

    if outside_range > 0:

        print(
            "⚠ Some predictions are outside the expected CGPA range."
        )

    else:

        print(
            "✓ All predictions are within 0-4."
        )

    return predictions


# ======================================================================
# REGRESSION METRICS
# ======================================================================

def calculate_metrics(
    y_true,
    predictions
):

    print_header("MODEL PERFORMANCE")

    mae = mean_absolute_error(
        y_true,
        predictions
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_true,
            predictions
        )
    )

    r2 = r2_score(
        y_true,
        predictions
    )

    print(
        f"MAE  : {mae:.4f}"
    )

    print(
        f"RMSE : {rmse:.4f}"
    )

    print(
        f"R²   : {r2:.4f}"
    )

    print()

    print(
        f"Expected GPA Error: ±{mae:.2f} GPA"
    )

    return {
        "mae": float(mae),
        "rmse": float(rmse),
        "r2": float(r2),
    }


# ======================================================================
# BASELINE MODEL
# ======================================================================

def calculate_baseline(
    y_train,
    y_test
):

    print_header("BASELINE COMPARISON")

    """
    Baseline:

    Predict the average CGPA of the training data
    for every student in the test set.

    This is important because the Random Forest must
    perform better than a trivial mean predictor.
    """

    y_train_array = np.asarray(
        y_train,
        dtype=float
    )

    y_test_array = np.asarray(
        y_test,
        dtype=float
    )

    training_mean = float(
        np.mean(y_train_array)
    )

    baseline_predictions = np.full(
        shape=len(y_test_array),
        fill_value=training_mean,
        dtype=float
    )

    baseline_mae = mean_absolute_error(
        y_test_array,
        baseline_predictions
    )

    baseline_rmse = np.sqrt(
        mean_squared_error(
            y_test_array,
            baseline_predictions
        )
    )

    baseline_r2 = r2_score(
        y_test_array,
        baseline_predictions
    )

    print(
        f"Training mean CGPA : {training_mean:.4f}"
    )

    print(
        f"Baseline MAE       : {baseline_mae:.4f}"
    )

    print(
        f"Baseline RMSE      : {baseline_rmse:.4f}"
    )

    print(
        f"Baseline R²        : {baseline_r2:.4f}"
    )

    return {
        "mean_cgpa": training_mean,
        "mae": float(baseline_mae),
        "rmse": float(baseline_rmse),
        "r2": float(baseline_r2),
    }


# ======================================================================
# MODEL VS BASELINE
# ======================================================================

def compare_with_baseline(
    model_metrics,
    baseline_metrics
):

    print_header("MODEL VS BASELINE")

    model_mae = model_metrics["mae"]
    baseline_mae = baseline_metrics["mae"]

    improvement = (
        baseline_mae - model_mae
    )

    improvement_percentage = (
        improvement / baseline_mae * 100
    )

    print(
        f"Baseline MAE : {baseline_mae:.4f}"
    )

    print(
        f"Model MAE    : {model_mae:.4f}"
    )

    print(
        f"Improvement  : {improvement:.4f}"
    )

    print(
        f"Improvement %: {improvement_percentage:.2f}%"
    )

    if model_mae < baseline_mae:

        print()
        print(
            "✓ Model performs better than the mean baseline."
        )

        baseline_status = "PASS"

    else:

        print()
        print(
            "❌ Model does NOT outperform the mean baseline."
        )

        baseline_status = "FAIL"

    return {
        "improvement": float(improvement),
        "improvement_percentage": float(
            improvement_percentage
        ),
        "status": baseline_status,
    }


# ======================================================================
# ERROR ANALYSIS
# ======================================================================

def error_analysis(
    y_true,
    predictions
):

    print_header("PREDICTION ERROR ANALYSIS")

    errors = (
        predictions - y_true
    )

    absolute_errors = np.abs(
        errors
    )

    print(
        f"Mean error          : {errors.mean():.4f}"
    )

    print(
        f"Median absolute err : {np.median(absolute_errors):.4f}"
    )

    print(
        f"Maximum absolute err: {absolute_errors.max():.4f}"
    )

    print(
        f"Minimum absolute err: {absolute_errors.min():.4f}"
    )

    # --------------------------------------------------------------
    # Error percentages
    # --------------------------------------------------------------

    within_025 = (
        absolute_errors <= 0.25
    ).mean() * 100

    within_050 = (
        absolute_errors <= 0.50
    ).mean() * 100

    within_075 = (
        absolute_errors <= 0.75
    ).mean() * 100

    within_100 = (
        absolute_errors <= 1.00
    ).mean() * 100

    print()
    print("ERROR TOLERANCE")

    print(
        f"Within ±0.25 GPA : {within_025:.2f}%"
    )

    print(
        f"Within ±0.50 GPA : {within_050:.2f}%"
    )

    print(
        f"Within ±0.75 GPA : {within_075:.2f}%"
    )

    print(
        f"Within ±1.00 GPA : {within_100:.2f}%"
    )

    # --------------------------------------------------------------
    # Error buckets
    # --------------------------------------------------------------

    print()
    print("ERROR DISTRIBUTION")

    buckets = {
        "<= 0.25": (
            absolute_errors <= 0.25
        ).sum(),

        "0.25 - 0.50": (
            (absolute_errors > 0.25)
            & (absolute_errors <= 0.50)
        ).sum(),

        "0.50 - 0.75": (
            (absolute_errors > 0.50)
            & (absolute_errors <= 0.75)
        ).sum(),

        "0.75 - 1.00": (
            (absolute_errors > 0.75)
            & (absolute_errors <= 1.00)
        ).sum(),

        "> 1.00": (
            absolute_errors > 1.00
        ).sum(),
    }

    for bucket, count in buckets.items():

        percentage = (
            count / len(y_true) * 100
        )

        print(
            f"{bucket:15} : "
            f"{count:4} "
            f"({percentage:.2f}%)"
        )

    return {
        "mean_error": float(errors.mean()),
        "median_absolute_error": float(
            np.median(absolute_errors)
        ),
        "maximum_absolute_error": float(
            absolute_errors.max()
        ),
        "within_025_percent": float(
            within_025
        ),
        "within_050_percent": float(
            within_050
        ),
        "within_075_percent": float(
            within_075
        ),
        "within_100_percent": float(
            within_100
        ),
        "error_buckets": {
            key: int(value)
            for key, value in buckets.items()
        },
    }


# ======================================================================
# CGPA RANGE ANALYSIS
# ======================================================================

def cgpa_range_analysis(
    y_true,
    predictions
):

    print_header("CGPA RANGE ERROR ANALYSIS")

    data = pd.DataFrame(
        {
            "actual": y_true,
            "predicted": predictions,
        }
    )

    data["absolute_error"] = (
        data["actual"]
        - data["predicted"]
    ).abs()

    # --------------------------------------------------------------
    # CGPA ranges
    # --------------------------------------------------------------

    bins = [
        -0.001,
        2.50,
        3.00,
        3.40,
        3.80,
        4.001,
    ]

    labels = [
        "Below 2.50",
        "2.50 - 2.99",
        "3.00 - 3.39",
        "3.40 - 3.79",
        "3.80 - 4.00",
    ]

    data["cgpa_range"] = pd.cut(
        data["actual"],
        bins=bins,
        labels=labels,
        include_lowest=True,
        right=False,
    )

    grouped = (
        data
        .groupby(
            "cgpa_range",
            observed=False
        )
        .agg(
            samples=("actual", "count"),
            mae=("absolute_error", "mean"),
            actual_mean=("actual", "mean"),
            predicted_mean=("predicted", "mean"),
        )
        .reset_index()
    )

    print(
        grouped.to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}"
        )
    )

    return grouped


# ======================================================================
# CREATE PREDICTION FILE
# ======================================================================

def save_predictions(
    y_true,
    predictions
):

    VALIDATION_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    errors = predictions - y_true

    result = pd.DataFrame(
        {
            "actual_cgpa": y_true,
            "predicted_cgpa": predictions,
            "error": errors,
            "absolute_error": np.abs(errors),
        }
    )

    result.to_csv(
        PREDICTIONS_PATH,
        index=False
    )

    print_section("VALIDATION PREDICTIONS SAVED")

    print(
        PREDICTIONS_PATH
    )

    print(
        "✓ Prediction-level validation file saved."
    )

    return result


# ======================================================================
# SAVE VALIDATION RESULTS
# ======================================================================

def save_results(
    model,
    metadata,
    model_metrics,
    baseline_metrics,
    comparison,
    error_results,
    sample_count,
):

    VALIDATION_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------------
    # Overall validation status
    # --------------------------------------------------------------

    if comparison["status"] == "PASS":

        validation_status = (
            "MODEL OUTPERFORMS BASELINE"
        )

    else:

        validation_status = (
            "MODEL REQUIRES REVIEW"
        )

    results = {

        "validation_status":
            validation_status,

        "model":
            type(model).__name__,

        "test_samples":
            int(sample_count),

        "model_metrics":
            model_metrics,

        "baseline_metrics":
            baseline_metrics,

        "baseline_comparison":
            comparison,

        "error_analysis":
            error_results,

        "training_metadata":
            metadata,
    }

    with open(
        VALIDATION_RESULTS_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=4
        )

    print_section("VALIDATION RESULTS SAVED")

    print(
        VALIDATION_RESULTS_PATH
    )

    return results


# ======================================================================
# FINAL DECISION
# ======================================================================

def final_decision(
    model_metrics,
    comparison,
    error_results,
):

    print_header(
        "FINAL INDEPENDENT VALIDATION DECISION"
    )

    print(
        f"Model MAE : "
        f"{model_metrics['mae']:.4f}"
    )

    print(
        f"Model RMSE: "
        f"{model_metrics['rmse']:.4f}"
    )

    print(
        f"Model R²  : "
        f"{model_metrics['r2']:.4f}"
    )

    print(
        f"Expected Error: "
        f"±{model_metrics['mae']:.2f} GPA"
    )

    print()

    if comparison["status"] == "FAIL":

        print(
            "❌ DECISION: MODEL REQUIRES IMPROVEMENT"
        )

        print()
        print(
            "Reason:"
        )

        print(
            "The model does not outperform the "
            "simple training-mean baseline."
        )

        print()
        print(
            "Do NOT deploy this model yet."
        )

        return "REVIEW"

    # --------------------------------------------------------------
    # Model beats baseline
    # --------------------------------------------------------------

    if model_metrics["r2"] <= 0:

        print(
            "⚠ DECISION: MODEL REQUIRES REVIEW"
        )

        print(
            "Model beats baseline MAE, "
            "but R² is not positive."
        )

        return "REVIEW"

    # --------------------------------------------------------------
    # Positive R² and better baseline
    # --------------------------------------------------------------

    print(
        "✓ DECISION: MODEL PASSES BASIC VALIDATION"
    )

    print()
    print(
        "The model performs better than the "
        "simple mean baseline."
    )

    print()
    print(
        "Next:"
    )

    print(
        "→ Feature importance"
    )

    print(
        "→ Prediction service"
    )

    print(
        "→ FastAPI integration"
    )

    print(
        "→ React dashboard integration"
    )

    return "PASS"


# ======================================================================
# MAIN VALIDATION PIPELINE
# ======================================================================

def main():

    print()
    print("=" * 70)
    print(
        "AI STUDENT ANALYTICS DASHBOARD"
    )
    print(
        "INDEPENDENT CGPA MODEL VALIDATION"
    )
    print("=" * 70)

    # --------------------------------------------------------------
    # Create validation directory
    # --------------------------------------------------------------

    VALIDATION_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------------
    # Load model
    # --------------------------------------------------------------

    model = load_model()

    # --------------------------------------------------------------
    # Load metadata
    # --------------------------------------------------------------

    metadata = load_metadata()

    # --------------------------------------------------------------
    # Recreate test data
    # --------------------------------------------------------------

    (
        X_train,
        X_test,
        y_train,
        y_test,
        preprocessor,
    ) = load_preprocessed_data()

    # --------------------------------------------------------------
    # Validate test data
    # --------------------------------------------------------------

    y_test_array = validate_data(
        X_train,
        X_test,
        y_train,
        y_test,
    )

    # --------------------------------------------------------------
    # Generate predictions
    # --------------------------------------------------------------

    predictions = generate_predictions(
        model,
        X_test
    )

    # --------------------------------------------------------------
    # Calculate model metrics
    # --------------------------------------------------------------

    model_metrics = calculate_metrics(
        y_test_array,
        predictions
    )

    # --------------------------------------------------------------
    # Baseline
    # --------------------------------------------------------------

    baseline_metrics = calculate_baseline(
        y_train,
        y_test_array
    )

    # --------------------------------------------------------------
    # Compare model vs baseline
    # --------------------------------------------------------------

    comparison = compare_with_baseline(
        model_metrics,
        baseline_metrics
    )

    # --------------------------------------------------------------
    # Error analysis
    # --------------------------------------------------------------

    error_results = error_analysis(
        y_test_array,
        predictions
    )

    # --------------------------------------------------------------
    # CGPA range analysis
    # --------------------------------------------------------------

    range_results = cgpa_range_analysis(
        y_test_array,
        predictions
    )

    # --------------------------------------------------------------
    # Save predictions
    # --------------------------------------------------------------

    save_predictions(
        y_test_array,
        predictions
    )

    # --------------------------------------------------------------
    # Save results
    # --------------------------------------------------------------

    results = save_results(
        model=model,
        metadata=metadata,
        model_metrics=model_metrics,
        baseline_metrics=baseline_metrics,
        comparison=comparison,
        error_results=error_results,
        sample_count=len(y_test_array),
    )

    # --------------------------------------------------------------
    # Add range analysis to JSON
    # --------------------------------------------------------------

    results["cgpa_range_analysis"] = (
        range_results
        .replace(
            {np.nan: None}
        )
        .to_dict(
            orient="records"
        )
    )

    with open(
        VALIDATION_RESULTS_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=4,
            default=str
        )

    # --------------------------------------------------------------
    # Final decision
    # --------------------------------------------------------------

    status = final_decision(
        model_metrics,
        comparison,
        error_results,
    )

    # --------------------------------------------------------------
    # Final summary
    # --------------------------------------------------------------

    print()
    print("=" * 70)
    print("VALIDATION COMPLETE")
    print("=" * 70)

    print(
        f"Status          : {status}"
    )

    print(
        f"Model           : {type(model).__name__}"
    )

    print(
        f"MAE             : "
        f"{model_metrics['mae']:.4f}"
    )

    print(
        f"RMSE            : "
        f"{model_metrics['rmse']:.4f}"
    )

    print(
        f"R²              : "
        f"{model_metrics['r2']:.4f}"
    )

    print(
        f"Expected Error  : "
        f"±{model_metrics['mae']:.2f} GPA"
    )

    print()
    print(
        "Validation results:"
    )

    print(
        VALIDATION_RESULTS_PATH
    )

    print()
    print(
        "Prediction details:"
    )

    print(
        PREDICTIONS_PATH
    )

    print("=" * 70)


# ======================================================================
# ENTRY POINT
# ======================================================================

if __name__ == "__main__":

    main()
    