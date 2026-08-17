"""
AI Student Analytics Dashboard
================================

DATA LEAKAGE AUDIT

Purpose
-------
Identify features that may cause target leakage when predicting
Current CGPA.

Target:
    What is your current CGPA?

This script DOES NOT:
    - delete columns
    - modify the dataset
    - train a model
    - encode features
    - impute missing values

It only performs an audit and produces recommendations.

Prediction principle
--------------------
A feature is acceptable only if that information would realistically
be available at the time we want to predict the student's CGPA.

Important:
------------
This is a rule-based first-pass audit.

Final feature selection will be decided after reviewing:
    1. Leakage risk
    2. Prediction-time availability
    3. Data quality
    4. Cardinality
    5. Statistical relationship with target
"""

from pathlib import Path

import pandas as pd
import numpy as np


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
# LOAD DATASET
# ============================================================

def load_dataset():

    print()
    print("=" * 80)
    print("LOADING DATASET FOR LEAKAGE AUDIT")
    print("=" * 80)

    print()
    print("Dataset:")
    print(DATASET_PATH)

    if not DATASET_PATH.exists():

        raise FileNotFoundError(
            f"\nDataset not found:\n{DATASET_PATH}"
        )

    try:

        df = pd.read_excel(
            DATASET_PATH
        )

    except Exception as error:

        raise RuntimeError(
            f"\nUnable to read dataset:\n{error}"
        )

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    print()
    print(
        f"Rows    : {len(df)}"
    )

    print(
        f"Columns : {len(df.columns)}"
    )

    return df


# ============================================================
# COLUMN RISK DEFINITIONS
# ============================================================

# ------------------------------------------------------------
# HIGH RISK
# ------------------------------------------------------------
#
# These variables can potentially represent academic outcomes
# that happen because of, or after, poor academic performance.
#
# They require strong justification before inclusion.
# ------------------------------------------------------------

HIGH_RISK_COLUMNS = {

    "Did you ever fall in probation?":
        "Probation can be a consequence of poor academic performance.",

    "Did you ever got suspension?":
        "Suspension may occur after academic or disciplinary outcomes.",

}


# ============================================================
# POTENTIAL TEMPORAL RISK
# ============================================================

TEMPORAL_RISK_COLUMNS = {

    "Current Semester":
        "May reflect academic progression and therefore may contain information related to current CGPA.",

    "Average attendance on class (Percentage )":
        "Potentially valid, but timing must be confirmed: attendance should be available before prediction.",

    "Do you attend in teacher consultancy for any kind of academical problems?":
        "Potentially valid, but the timing of consultancy relative to CGPA must be confirmed.",

}


# ============================================================
# SAFE CANDIDATE FEATURES
# ============================================================

SAFE_CANDIDATE_COLUMNS = {

    "Gender":
        "Demographic information normally available before prediction.",

    "Age (Years)":
        "Basic demographic information.",

    "University Admission year":
        "Admission information available before or during enrollment.",

    "H.S.C passing year":
        "Pre-university academic history.",

    "Program":
        "Academic program information, although constant in this dataset.",

    "Do you have meritorious scholarship ?":
        "Scholarship status can be available before prediction.",

    "Do you use University transportation?":
        "Student contextual information.",

    "How many hour do you study daily? (Hours )":
        "Study behavior reported by the student.",

    "How many times do you seat for study in a day?":
        "Study behavior reported by the student.",

    "What is your preferable learning mode?":
        "Learning preference.",

    "Do you use smart phone?":
        "Technology usage information.",

    "Do you have personal Computer?":
        "Technology/access information.",

    "How many hour do you spent daily in social media? (Hours)":
        "Reported behavioral information.",

    "Status of your English language proficiency":
        "Self-reported proficiency.",

    "What are the skills do you have ?":
        "Self-reported skills.",

    "How many hour do you spent daily on your skill development? (Hours )":
        "Self-reported development behavior.",

    "What is you interested area?":
        "Self-reported interests.",

    "What is your relationship status?":
        "Demographic/social information.",

    "Are you engaged with any co-curriculum activities?":
        "Student activity information.",

    "With whom you are living with?":
        "Living arrangement.",

    "Do you have any health issues?":
        "Self-reported health information.",

    "Do you have any physical disabilities?":
        "Self-reported demographic/contextual information.",

    "What is your monthly Family Income":
        "Family financial context.",

}


# ============================================================
# TARGET CHECK
# ============================================================

def validate_target(df):

    print()
    print("=" * 80)
    print("TARGET VALIDATION")
    print("=" * 80)

    if TARGET_COLUMN not in df.columns:

        raise ValueError(
            f"Target column not found:\n{TARGET_COLUMN}"
        )

    target = pd.to_numeric(
        df[TARGET_COLUMN],
        errors="coerce"
    )

    print()
    print(
        f"Target column: {TARGET_COLUMN}"
    )

    print(
        f"Missing target : {target.isna().sum()}"
    )

    invalid_mask = (
        target.notna()
        & (
            (target < 0)
            | (target > 4)
        )
    )

    print(
        f"Invalid target : {invalid_mask.sum()}"
    )

    valid_target = target[
        target.notna()
        & (~invalid_mask)
    ]

    if len(valid_target) > 0:

        print()
        print("Valid target statistics:")

        print(
            f"Minimum : {valid_target.min():.3f}"
        )

        print(
            f"Maximum : {valid_target.max():.3f}"
        )

        print(
            f"Mean    : {valid_target.mean():.3f}"
        )

        print(
            f"Median  : {valid_target.median():.3f}"
        )


# ============================================================
# CARDINALITY AUDIT
# ============================================================

def audit_cardinality(df):

    print()
    print("=" * 80)
    print("CARDINALITY AUDIT")
    print("=" * 80)

    results = []

    for column in df.columns:

        if column == TARGET_COLUMN:
            continue

        unique_count = (
            df[column]
            .nunique(
                dropna=True
            )
        )

        unique_ratio = (
            unique_count
            / len(df)
        )

        dtype = str(
            df[column].dtype
        )

        results.append(
            {
                "column": column,
                "dtype": dtype,
                "unique_values": unique_count,
                "unique_ratio": round(
                    unique_ratio,
                    4
                ),
            }
        )

    report = pd.DataFrame(
        results
    )

    report = report.sort_values(
        by="unique_values",
        ascending=False
    )

    print()

    print(
        report.to_string(
            index=False
        )
    )

    print()
    print(
        "High-cardinality columns require "
        "special feature engineering."
    )

    return report


# ============================================================
# CONSTANT COLUMN AUDIT
# ============================================================

def audit_constant_columns(df):

    print()
    print("=" * 80)
    print("CONSTANT COLUMN AUDIT")
    print("=" * 80)

    constant_columns = []

    for column in df.columns:

        if column == TARGET_COLUMN:
            continue

        unique_count = (
            df[column]
            .nunique(
                dropna=False
            )
        )

        if unique_count <= 1:

            constant_columns.append(
                column
            )

    if constant_columns:

        print()
        print(
            "Constant columns:"
        )

        for column in constant_columns:

            print(
                f"  - {column}"
            )

        print()
        print(
            "These columns provide no predictive variation."
        )

    else:

        print()
        print(
            "No constant feature columns found."
        )

    return constant_columns


# ============================================================
# CORRELATION AUDIT
# ============================================================

def audit_numeric_relationships(df):

    print()
    print("=" * 80)
    print("NUMERICAL RELATIONSHIP AUDIT")
    print("=" * 80)

    numeric_df = (
        df.select_dtypes(
            include=np.number
        )
        .copy()
    )

    if TARGET_COLUMN not in numeric_df.columns:

        print(
            "Target is not numerical."
        )

        return None

    correlations = (
        numeric_df
        .corr(
            numeric_only=True
        )[TARGET_COLUMN]
        .drop(
            TARGET_COLUMN,
            errors="ignore"
        )
        .sort_values(
            key=lambda x: abs(x),
            ascending=False
        )
    )

    print()

    for column, value in correlations.items():

        print(
            f"{column:65} "
            f"{value:+.4f}"
        )

    print()
    print(
        "NOTE:"
    )

    print(
        "Correlation does NOT prove causation "
        "and does NOT automatically mean leakage."
    )

    print(
        "It is only a diagnostic signal."
    )

    return correlations


# ============================================================
# RULE-BASED LEAKAGE AUDIT
# ============================================================

def run_rule_based_audit(df):

    print()
    print("=" * 80)
    print("RULE-BASED DATA LEAKAGE AUDIT")
    print("=" * 80)

    results = []

    for column in df.columns:

        if column == TARGET_COLUMN:
            continue

        # ----------------------------------------------------
        # Constant
        # ----------------------------------------------------

        if (
            df[column]
            .nunique(
                dropna=False
            )
            <= 1
        ):

            results.append(
                {
                    "column": column,
                    "risk": "REMOVE",
                    "reason":
                        "Constant feature; provides no predictive information.",
                }
            )

            continue

        # ----------------------------------------------------
        # High Risk
        # ----------------------------------------------------

        if column in HIGH_RISK_COLUMNS:

            results.append(
                {
                    "column": column,
                    "risk": "HIGH RISK",
                    "reason":
                        HIGH_RISK_COLUMNS[column],
                }
            )

            continue

        # ----------------------------------------------------
        # Temporal Risk
        # ----------------------------------------------------

        if column in TEMPORAL_RISK_COLUMNS:

            results.append(
                {
                    "column": column,
                    "risk": "REVIEW",
                    "reason":
                        TEMPORAL_RISK_COLUMNS[column],
                }
            )

            continue

        # ----------------------------------------------------
        # Safe Candidate
        # ----------------------------------------------------

        if column in SAFE_CANDIDATE_COLUMNS:

            results.append(
                {
                    "column": column,
                    "risk": "CANDIDATE",
                    "reason":
                        SAFE_CANDIDATE_COLUMNS[column],
                }
            )

            continue

        # ----------------------------------------------------
        # Unknown feature
        # ----------------------------------------------------

        results.append(
            {
                "column": column,
                "risk": "REVIEW",
                "reason":
                    "No automatic decision. Requires manual review.",
            }
        )

    report = pd.DataFrame(
        results
    )

    # --------------------------------------------------------
    # Sort by risk priority
    # --------------------------------------------------------

    priority = {
        "HIGH RISK": 1,
        "REMOVE": 2,
        "REVIEW": 3,
        "CANDIDATE": 4,
    }

    report["_priority"] = (
        report["risk"]
        .map(priority)
        .fillna(99)
    )

    report = report.sort_values(
        by="_priority"
    ).drop(
        columns="_priority"
    )

    print()

    print(
        report.to_string(
            index=False
        )
    )

    return report


# ============================================================
# FINAL RECOMMENDATION
# ============================================================

def print_final_recommendation(
    report,
    constant_columns
):

    print()
    print("=" * 80)
    print("FINAL LEAKAGE AUDIT RECOMMENDATION")
    print("=" * 80)

    high_risk = report[
        report["risk"] == "HIGH RISK"
    ]

    review = report[
        report["risk"] == "REVIEW"
    ]

    candidates = report[
        report["risk"] == "CANDIDATE"
    ]

    removable = report[
        report["risk"] == "REMOVE"
    ]

    print()

    print(
        f"Potentially removable : "
        f"{len(removable)}"
    )

    print(
        f"High-risk features    : "
        f"{len(high_risk)}"
    )

    print(
        f"Review features       : "
        f"{len(review)}"
    )

    print(
        f"Candidate features    : "
        f"{len(candidates)}"
    )

    # --------------------------------------------------------
    # Remove
    # --------------------------------------------------------

    if len(removable) > 0:

        print()
        print(
            "REMOVE FROM MODEL:"
        )

        for column in removable[
            "column"
        ]:

            print(
                f"  ❌ {column}"
            )

    # --------------------------------------------------------
    # High risk
    # --------------------------------------------------------

    if len(high_risk) > 0:

        print()
        print(
            "HIGH-RISK FEATURES:"
        )

        for _, row in high_risk.iterrows():

            print(
                f"  🚨 {row['column']}"
            )

            print(
                f"     {row['reason']}"
            )

    # --------------------------------------------------------
    # Review
    # --------------------------------------------------------

    if len(review) > 0:

        print()
        print(
            "FEATURES REQUIRING REVIEW:"
        )

        for _, row in review.iterrows():

            print(
                f"  ⚠ {row['column']}"
            )

            print(
                f"     {row['reason']}"
            )

    # --------------------------------------------------------
    # Candidate
    # --------------------------------------------------------

    if len(candidates) > 0:

        print()
        print(
            "INITIAL CANDIDATE FEATURES:"
        )

        for column in candidates[
            "column"
        ]:

            print(
                f"  ✓ {column}"
            )

    # --------------------------------------------------------
    # Final warning
    # --------------------------------------------------------

    print()
    print("=" * 80)

    print(
        "IMPORTANT:"
    )

    print(
        "This audit does NOT automatically delete "
        "or modify any feature."
    )

    print(
        "The final feature set must be locked "
        "before model training."
    )

    print(
        "Do NOT use the current CGPA itself as an input feature."
    )

    print("=" * 80)


# ============================================================
# SAVE AUDIT REPORT
# ============================================================

def save_audit_report(report):

    output_path = (
        BASE_DIR
        / "ml_reports"
        / "data_leakage_audit.csv"
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    report.to_csv(
        output_path,
        index=False
    )

    print()
    print(
        f"Audit report saved to:"
    )

    print(
        output_path
    )


# ============================================================
# COMPLETE AUDIT PIPELINE
# ============================================================

def run_audit():

    print()
    print("=" * 80)
    print("AI STUDENT ANALYTICS DASHBOARD")
    print("CGPA DATA LEAKAGE AUDIT")
    print("=" * 80)

    # --------------------------------------------------------
    # Load
    # --------------------------------------------------------

    df = load_dataset()

    # --------------------------------------------------------
    # Target
    # --------------------------------------------------------

    validate_target(
        df
    )

    # --------------------------------------------------------
    # Cardinality
    # --------------------------------------------------------

    cardinality_report = (
        audit_cardinality(
            df
        )
    )

    # --------------------------------------------------------
    # Constant columns
    # --------------------------------------------------------

    constant_columns = (
        audit_constant_columns(
            df
        )
    )

    # --------------------------------------------------------
    # Numerical relationships
    # --------------------------------------------------------

    audit_numeric_relationships(
        df
    )

    # --------------------------------------------------------
    # Leakage rules
    # --------------------------------------------------------

    leakage_report = (
        run_rule_based_audit(
            df
        )
    )

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    save_audit_report(
        leakage_report
    )

    # --------------------------------------------------------
    # Final recommendation
    # --------------------------------------------------------

    print_final_recommendation(
        leakage_report,
        constant_columns
    )

    print()
    print(
        "=" * 80
    )

    print(
        "LEAKAGE AUDIT COMPLETE"
    )

    print(
        "=" * 80
    )

    return {
        "data": df,
        "cardinality": cardinality_report,
        "leakage": leakage_report,
    }


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    run_audit()