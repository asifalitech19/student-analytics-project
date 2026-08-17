"""
======================================================================
AI STUDENT ANALYTICS DASHBOARD
MODEL EXPLAINABILITY & FEATURE IMPORTANCE
======================================================================

Purpose:
    Explain the currently trained CGPA regression model.

This script:
    1. Loads the saved Random Forest model
    2. Recreates the current preprocessing pipeline
    3. Extracts processed feature names
    4. Reads Random Forest feature importance
    5. Ranks features
    6. Groups engineered features back to their source domains
    7. Performs permutation importance on the independent test set
    8. Saves feature-importance reports

IMPORTANT:
    - Does NOT retrain the model
    - Does NOT modify the dataset
    - Does NOT modify the saved model
    - Does NOT introduce leakage
======================================================================
"""

from pathlib import Path
import json

import joblib
import numpy as np
import pandas as pd

from sklearn.inspection import permutation_importance


# ======================================================================
# PATHS
# ======================================================================

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_DIR = BASE_DIR / "saved_models"

MODEL_PATH = (
    MODEL_DIR
    / "cgpa_regression_model.pkl"
)

METADATA_PATH = (
    MODEL_DIR
    / "cgpa_model_metadata.json"
)

REPORT_DIR = (
    BASE_DIR
    / "ml_reports"
)

RF_IMPORTANCE_PATH = (
    REPORT_DIR
    / "random_forest_feature_importance.csv"
)

PERMUTATION_IMPORTANCE_PATH = (
    REPORT_DIR
    / "permutation_feature_importance.csv"
)

GROUPED_IMPORTANCE_PATH = (
    REPORT_DIR
    / "grouped_feature_importance.csv"
)


# ======================================================================
# PRINT HELPERS
# ======================================================================

def header(title):

    print()
    print("=" * 75)
    print(title)
    print("=" * 75)


# ======================================================================
# LOAD MODEL
# ======================================================================

def load_model():

    header("LOADING TRAINED MODEL")

    if not MODEL_PATH.exists():

        raise FileNotFoundError(
            f"""
Trained model not found.

Expected:
{MODEL_PATH}

Run:
python -m app.ml.model_training

first.
"""
        )

    model = joblib.load(
        MODEL_PATH
    )

    print(
        f"Model: {type(model).__name__}"
    )

    print(
        f"Path : {MODEL_PATH}"
    )

    print(
        "✓ Model loaded."
    )

    return model


# ======================================================================
# LOAD METADATA
# ======================================================================

def load_metadata():

    if not METADATA_PATH.exists():

        return {}

    try:

        with open(
            METADATA_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception:

        return {}


# ======================================================================
# LOAD CURRENT PREPROCESSED DATA
# ======================================================================

def load_preprocessed_data():

    header(
        "RECREATING CURRENT PREPROCESSING OUTPUT"
    )

    from app.ml.preprocessing import prepare_data

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
    print(
        f"X_train: {X_train.shape}"
    )

    print(
        f"X_test : {X_test.shape}"
    )

    print(
        f"y_train: {y_train.shape}"
    )

    print(
        f"y_test : {y_test.shape}"
    )

    print(
        "✓ Current preprocessing recreated."
    )

    return (
        X_train,
        X_test,
        y_train,
        y_test,
        preprocessor,
        X_train_raw,
        X_test_raw,
    )


# ======================================================================
# GET FEATURE NAMES
# ======================================================================

def get_feature_names(
    preprocessor
):

    header(
        "EXTRACTING PROCESSED FEATURE NAMES"
    )

    try:

        feature_names = (
            preprocessor
            .get_feature_names_out()
        )

    except Exception as error:

        raise RuntimeError(
            f"""
Could not extract processed feature names.

Error:
{error}
"""
        )

    feature_names = np.asarray(
        feature_names,
        dtype=str
    )

    print(
        f"Processed feature count: "
        f"{len(feature_names)}"
    )

    print()
    print(
        "Sample processed features:"
    )

    for feature in feature_names[:25]:

        print(
            f"  - {feature}"
        )

    if len(feature_names) > 25:

        print(
            f"  ... and "
            f"{len(feature_names) - 25} more."
        )

    return feature_names


# ======================================================================
# RANDOM FOREST FEATURE IMPORTANCE
# ======================================================================

def calculate_random_forest_importance(
    model,
    feature_names
):

    header(
        "RANDOM FOREST FEATURE IMPORTANCE"
    )

    if not hasattr(
        model,
        "feature_importances_"
    ):

        raise TypeError(
            "The loaded model does not expose "
            "feature_importances_."
        )

    importances = np.asarray(
        model.feature_importances_,
        dtype=float
    )

    if len(importances) != len(feature_names):

        raise ValueError(
            f"""
Feature count mismatch.

Model importances : {len(importances)}
Feature names     : {len(feature_names)}
"""
        )

    report = pd.DataFrame(
        {
            "feature": feature_names,
            "importance": importances,
        }
    )

    report = report.sort_values(
        by="importance",
        ascending=False
    ).reset_index(
        drop=True
    )

    report["rank"] = (
        np.arange(
            1,
            len(report) + 1
        )
    )

    # Percentage share
    total = report["importance"].sum()

    if total > 0:

        report["importance_percent"] = (
            report["importance"]
            / total
            * 100
        )

    else:

        report["importance_percent"] = 0.0

    return report


# ======================================================================
# PERMUTATION IMPORTANCE
# ======================================================================

def calculate_permutation_importance(
    model,
    X_test,
    y_test,
    feature_names
):

    header(
        "PERMUTATION IMPORTANCE"
    )

    print(
        "Calculating permutation importance "
        "on the independent test set..."
    )

    result = permutation_importance(

        model,

        X_test,

        y_test,

        scoring="neg_mean_absolute_error",

        n_repeats=20,

        random_state=42,

        n_jobs=-1,
    )

    mean_importance = np.asarray(
        result.importances_mean,
        dtype=float
    )

    std_importance = np.asarray(
        result.importances_std,
        dtype=float
    )

    if len(mean_importance) != len(
        feature_names
    ):

        raise ValueError(
            f"""
Permutation importance feature mismatch.

Importance values : {len(mean_importance)}
Feature names     : {len(feature_names)}
"""
        )

    report = pd.DataFrame(
        {
            "feature": feature_names,
            "permutation_importance":
                mean_importance,
            "permutation_std":
                std_importance,
        }
    )

    report = report.sort_values(
        by="permutation_importance",
        ascending=False
    ).reset_index(
        drop=True
    )

    report["rank"] = (
        np.arange(
            1,
            len(report) + 1
        )
    )

    return report


# ======================================================================
# CLEAN FEATURE NAME
# ======================================================================

def clean_feature_name(
    feature
):

    value = str(
        feature
    )

    # Remove transformer prefix
    prefixes = [
        "numerical__",
        "categorical__",
    ]

    for prefix in prefixes:

        if value.startswith(prefix):

            value = value[
                len(prefix):
            ]

    # OneHotEncoder category separator
    # remains meaningful, so don't remove it.

    return value


# ======================================================================
# GROUP ENGINEERED FEATURES
# ======================================================================

def classify_feature_group(
    feature
):

    feature = clean_feature_name(
        feature
    )

    lower = feature.lower()

    # --------------------------------------------------------------
    # Skill groups
    # --------------------------------------------------------------

    if lower.startswith("skill_"):

        return "Skills"

    # --------------------------------------------------------------
    # Interest groups
    # --------------------------------------------------------------

    if lower.startswith("interest_"):

        return "Interests"

    # --------------------------------------------------------------
    # Family income
    # --------------------------------------------------------------

    if (
        "family income"
        in lower
    ):

        return "Family Income"

    # --------------------------------------------------------------
    # Study behavior
    # --------------------------------------------------------------

    if (
        "study daily"
        in lower
        or
        "seat for study"
        in lower
        or
        "skill development"
        in lower
        or
        "social media"
        in lower
    ):

        return "Study & Digital Behavior"

    # --------------------------------------------------------------
    # Demographic
    # --------------------------------------------------------------

    if (
        "age"
        in lower
        or
        "gender"
        in lower
        or
        "relationship"
        in lower
        or
        "living"
        in lower
    ):

        return "Demographics"

    # --------------------------------------------------------------
    # Academic background
    # --------------------------------------------------------------

    if (
        "admission year"
        in lower
        or
        "h.s.c"
        in lower
        or
        "hsc"
        in lower
    ):

        return "Academic Background"

    # --------------------------------------------------------------
    # Technology
    # --------------------------------------------------------------

    if (
        "smart phone"
        in lower
        or
        "personal computer"
        in lower
        or
        "transportation"
        in lower
    ):

        return "Technology & Access"

    # --------------------------------------------------------------
    # Scholarship
    # --------------------------------------------------------------

    if (
        "scholarship"
        in lower
    ):

        return "Scholarship"

    # --------------------------------------------------------------
    # Health
    # --------------------------------------------------------------

    if (
        "health"
        in lower
        or
        "physical"
        in lower
    ):

        return "Health"

    # --------------------------------------------------------------
    # Language
    # --------------------------------------------------------------

    if (
        "english"
        in lower
    ):

        return "Language Proficiency"

    # --------------------------------------------------------------
    # Learning mode
    # --------------------------------------------------------------

    if (
        "learning mode"
        in lower
    ):

        return "Learning Preference"

    # --------------------------------------------------------------
    # Fallback
    # --------------------------------------------------------------

    return "Other"


# ======================================================================
# GROUPED FEATURE IMPORTANCE
# ======================================================================

def build_grouped_importance(
    report
):

    header(
        "GROUPED FEATURE IMPORTANCE"
    )

    grouped = report.copy()

    grouped["group"] = (
        grouped["feature"]
        .apply(
            classify_feature_group
        )
    )

    grouped_result = (
        grouped
        .groupby(
            "group",
            as_index=False
        )
        .agg(
            total_importance=(
                "importance",
                "sum"
            ),
            feature_count=(
                "feature",
                "count"
            )
        )
        .sort_values(
            by="total_importance",
            ascending=False
        )
        .reset_index(drop=True)
    )

    total = (
        grouped_result[
            "total_importance"
        ].sum()
    )

    if total > 0:

        grouped_result[
            "importance_percent"
        ] = (
            grouped_result[
                "total_importance"
            ]
            / total
            * 100
        )

    else:

        grouped_result[
            "importance_percent"
        ] = 0.0

    grouped_result["rank"] = (
        np.arange(
            1,
            len(grouped_result) + 1
        )
    )

    return grouped_result


# ======================================================================
# PRINT TOP FEATURES
# ======================================================================

def print_top_features(
    report,
    title,
    importance_column,
    top_n=20
):

    print()
    print("=" * 75)
    print(title)
    print("=" * 75)

    top = report.head(
        top_n
    )

    for _, row in top.iterrows():

        feature = clean_feature_name(
            row["feature"]
        )

        value = row[
            importance_column
        ]

        print(
            f"{int(row['rank']):02d}. "
            f"{feature:<65} "
            f"{value:.6f}"
        )


# ======================================================================
# SAVE REPORTS
# ======================================================================

def save_reports(
    rf_report,
    permutation_report,
    grouped_report
):

    header(
        "SAVING EXPLAINABILITY REPORTS"
    )

    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    rf_report.to_csv(
        RF_IMPORTANCE_PATH,
        index=False,
        encoding="utf-8-sig"
    )

    permutation_report.to_csv(
        PERMUTATION_IMPORTANCE_PATH,
        index=False,
        encoding="utf-8-sig"
    )

    grouped_report.to_csv(
        GROUPED_IMPORTANCE_PATH,
        index=False,
        encoding="utf-8-sig"
    )

    print(
        f"✓ Random Forest importance:\n"
        f"  {RF_IMPORTANCE_PATH}"
    )

    print(
        f"✓ Permutation importance:\n"
        f"  {PERMUTATION_IMPORTANCE_PATH}"
    )

    print(
        f"✓ Grouped importance:\n"
        f"  {GROUPED_IMPORTANCE_PATH}"
    )


# ======================================================================
# MAIN
# ======================================================================

def main():

    header(
        "AI STUDENT ANALYTICS DASHBOARD"
    )

    print(
        "MODEL EXPLAINABILITY ANALYSIS"
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
    # Recreate preprocessing
    # --------------------------------------------------------------

    (
        X_train,
        X_test,
        y_train,
        y_test,
        preprocessor,
        X_train_raw,
        X_test_raw,
    ) = load_preprocessed_data()

    # --------------------------------------------------------------
    # Extract names
    # --------------------------------------------------------------

    feature_names = get_feature_names(
        preprocessor
    )

    # --------------------------------------------------------------
    # Random Forest importance
    # --------------------------------------------------------------

    rf_report = (
        calculate_random_forest_importance(
            model,
            feature_names
        )
    )

    # --------------------------------------------------------------
    # Print top RF features
    # --------------------------------------------------------------

    print_top_features(
        rf_report,
        "TOP RANDOM FOREST FEATURES",
        "importance",
        top_n=25
    )

    # --------------------------------------------------------------
    # Permutation importance
    # --------------------------------------------------------------

    permutation_report = (
        calculate_permutation_importance(
            model,
            X_test,
            y_test,
            feature_names
        )
    )

    # --------------------------------------------------------------
    # Print top permutation features
    # --------------------------------------------------------------

    print_top_features(
        permutation_report,
        "TOP PERMUTATION FEATURES",
        "permutation_importance",
        top_n=25
    )

    # --------------------------------------------------------------
    # Grouped importance
    # --------------------------------------------------------------

    grouped_report = (
        build_grouped_importance(
            rf_report
        )
    )

    print()
    print("=" * 75)
    print("TOP FEATURE GROUPS")
    print("=" * 75)

    for _, row in (
        grouped_report.head(
            15
        ).iterrows()
    ):

        print(
            f"{int(row['rank']):02d}. "
            f"{row['group']:<35} "
            f"{row['importance_percent']:.2f}%"
        )

    # --------------------------------------------------------------
    # Save
    # --------------------------------------------------------------

    save_reports(
        rf_report,
        permutation_report,
        grouped_report
    )

    # --------------------------------------------------------------
    # Metadata summary
    # --------------------------------------------------------------

    print()
    print("=" * 75)
    print("MODEL INFORMATION")
    print("=" * 75)

    print(
        f"Model : "
        f"{type(model).__name__}"
    )

    if metadata:

        print(
            f"Test MAE : "
            f"{metadata.get('test_mae', 'N/A')}"
        )

        print(
            f"Test RMSE: "
            f"{metadata.get('test_rmse', 'N/A')}"
        )

        print(
            f"Test R²  : "
            f"{metadata.get('test_r2', 'N/A')}"
        )

    # --------------------------------------------------------------
    # Final
    # --------------------------------------------------------------

    print()
    print("=" * 75)
    print("EXPLAINABILITY ANALYSIS COMPLETE")
    print("=" * 75)

    print()
    print(
        "Next step:"
    )

    print(
        "Review the TOP RANDOM FOREST FEATURES, "
        "TOP PERMUTATION FEATURES and TOP FEATURE GROUPS."
    )

    print(
        "These results will guide the next feature/model "
        "improvement round."
    )


# ======================================================================
# ENTRY POINT
# ======================================================================

if __name__ == "__main__":

    main()