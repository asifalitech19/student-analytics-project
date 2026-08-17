"""
======================================================================
AI STUDENT ANALYTICS DASHBOARD
FINAL CGPA PREDICTION SERVICE
FEATURE SET B+ | RF + GB ENSEMBLE
======================================================================

Final raw prediction features:
    17

Prediction response:
    predicted_cgpa only

Post-processing:
    raw model prediction - 0.17

No UI exposure of:
    - model name
    - confidence
    - expected error
    - feature set

======================================================================
"""

from pathlib import Path
import json

import joblib
import numpy as np
import pandas as pd

from app.ml.preprocessing import prepare_data
from app.ml.ensemble import WeightedRegressionEnsemble


# ======================================================================
# PATHS
# ======================================================================

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_DIR = (
    BASE_DIR /
    "saved_models"
)

DATASET_PATH = (
    BASE_DIR /
    "dataset" /
    "IUBAT_CGPA_Training_Cleaned.csv"
)

MODEL_PATH = (
    MODEL_DIR /
    "cgpa_regression_model.pkl"
)

METADATA_PATH = (
    MODEL_DIR /
    "cgpa_model_metadata.json"
)


# ======================================================================
# FINAL 17-FEATURE SCHEMA
# ======================================================================

NUMERICAL_FEATURES = [

    "Age (Years)",

    "University Admission year",

    "H.S.C passing year",

    "How many hour do you study daily? (Hours )",

    "How many times do you seat for study in a day?",

    "How many hour do you spent daily in social media? (Hours)",

    "How many hour do you spent daily on your skill development? (Hours )",

    # --------------------------------------------------------------
    # B+ ACADEMIC CONTEXT
    # --------------------------------------------------------------

    "Current Semester",

    "Average attendance on class (Percentage )",

    "How many Credit did you have completed?",
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


FEATURE_COLUMNS = (
    NUMERICAL_FEATURES
    + CATEGORICAL_FEATURES
)


# ======================================================================
# VALID CGPA RANGE
# ======================================================================

MIN_PREDICTED_CGPA = 1.42
MAX_PREDICTED_CGPA = 4.00


# ======================================================================
# FINAL POST-PROCESSING ADJUSTMENT
# ======================================================================

PREDICTION_ADJUSTMENT = 0.17


# ======================================================================
# CACHED COMPONENTS
# ======================================================================

_model = None
_preprocessor = None
_metadata = None


# ======================================================================
# LOAD MODEL + PREPROCESSOR
# ======================================================================

def load_prediction_components():

    global _model
    global _preprocessor
    global _metadata

    # --------------------------------------------------------------
    # LOAD MODEL
    # --------------------------------------------------------------

    if _model is None:

        if not MODEL_PATH.exists():

            raise FileNotFoundError(
                f"""
Trained model not found:

{MODEL_PATH}

Run:

python -m app.ml.model_training
"""
            )

        _model = joblib.load(
            MODEL_PATH
        )

    # --------------------------------------------------------------
    # LOAD EXACT TRAINING PREPROCESSOR
    # --------------------------------------------------------------

    if _preprocessor is None:

        (
            _,
            _,
            _,
            _,
            _preprocessor,
            _,
            _,
        ) = prepare_data()

    # --------------------------------------------------------------
    # LOAD METADATA
    # --------------------------------------------------------------

    if _metadata is None:

        if METADATA_PATH.exists():

            try:

                with open(
                    METADATA_PATH,
                    "r",
                    encoding="utf-8",
                ) as file:

                    _metadata = json.load(
                        file
                    )

            except Exception as error:

                print(
                    f"[METADATA WARNING] {error}"
                )

                _metadata = {}

        else:

            _metadata = {}

    return (
        _model,
        _preprocessor,
        _metadata,
    )


# ======================================================================
# GET PREDICTION OPTIONS
# ======================================================================

def get_prediction_options():

    if not DATASET_PATH.exists():

        raise FileNotFoundError(
            f"Dataset not found:\n{DATASET_PATH}"
        )

    df = pd.read_csv(
        DATASET_PATH
    )

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    categorical_options = {}

    # --------------------------------------------------------------
    # CATEGORICAL OPTIONS
    # --------------------------------------------------------------

    for column in CATEGORICAL_FEATURES:

        if column not in df.columns:

            categorical_options[column] = []

            continue

        values = (
            df[column]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            .tolist()
        )

        categorical_options[column] = sorted(
            values
        )

    # --------------------------------------------------------------
    # NUMERICAL RANGES
    # --------------------------------------------------------------

    numerical_ranges = {}

    for column in NUMERICAL_FEATURES:

        if column not in df.columns:

            numerical_ranges[column] = {
                "min": None,
                "max": None,
            }

            continue

        values = pd.to_numeric(
            df[column],
            errors="coerce"
        ).dropna()

        if len(values) == 0:

            numerical_ranges[column] = {
                "min": None,
                "max": None,
            }

        else:

            numerical_ranges[column] = {
                "min": float(
                    values.min()
                ),

                "max": float(
                    values.max()
                ),
            }

    return {
        "categorical":
            categorical_options,

        "numerical_ranges":
            numerical_ranges,
    }


# ======================================================================
# PREPARE RAW INPUT
# ======================================================================

def prepare_prediction_input(
    age,
    gender,
    relationship_status,
    living_arrangement,
    health_issues,
    physical_disability,
    admission_year,
    hsc_year,
    scholarship,
    english_proficiency,
    study_hours,
    study_sessions,
    social_media_hours,
    skill_development_hours,
    current_semester,
    attendance,
    completed_credits,
):

    data = {

        # ----------------------------------------------------------
        # NUMERICAL FEATURES
        # ----------------------------------------------------------

        "Age (Years)":
            age,

        "University Admission year":
            admission_year,

        "H.S.C passing year":
            hsc_year,

        "How many hour do you study daily? (Hours )":
            study_hours,

        "How many times do you seat for study in a day?":
            study_sessions,

        "How many hour do you spent daily in social media? (Hours)":
            social_media_hours,

        "How many hour do you spent daily on your skill development? (Hours )":
            skill_development_hours,

        # ----------------------------------------------------------
        # B+ FEATURES
        # ----------------------------------------------------------

        "Current Semester":
            current_semester,

        "Average attendance on class (Percentage )":
            attendance,

        "How many Credit did you have completed?":
            completed_credits,

        # ----------------------------------------------------------
        # CATEGORICAL FEATURES
        # ----------------------------------------------------------

        "Gender":
            gender,

        "What is your relationship status?":
            relationship_status,

        "With whom you are living with?":
            living_arrangement,

        "Do you have any health issues?":
            health_issues,

        "Do you have any physical disabilities?":
            physical_disability,

        "Do you have meritorious scholarship ?":
            scholarship,

        "Status of your English language proficiency":
            english_proficiency,
    }

    df = pd.DataFrame(
        [data]
    )

    # Exact feature order used during training
    df = df[
        FEATURE_COLUMNS
    ]

    return df


# ======================================================================
# VALIDATE INPUT
# ======================================================================

def validate_prediction_input(
    df
):

    # --------------------------------------------------------------
    # AGE
    # --------------------------------------------------------------

    age = float(
        df[
            "Age (Years)"
        ].iloc[0]
    )

    if not 15 <= age <= 80:

        raise ValueError(
            "Age must be between 15 and 80."
        )

    # --------------------------------------------------------------
    # ADMISSION YEAR
    # --------------------------------------------------------------

    admission_year = float(
        df[
            "University Admission year"
        ].iloc[0]
    )

    if not 1990 <= admission_year <= 2035:

        raise ValueError(
            "University Admission year must be "
            "between 1990 and 2035."
        )

    # --------------------------------------------------------------
    # HSC YEAR
    # --------------------------------------------------------------

    hsc_year = float(
        df[
            "H.S.C passing year"
        ].iloc[0]
    )

    if not 1990 <= hsc_year <= 2035:

        raise ValueError(
            "H.S.C passing year must be "
            "between 1990 and 2035."
        )

    # --------------------------------------------------------------
    # STUDY HOURS
    # --------------------------------------------------------------

    study_hours = float(
        df[
            "How many hour do you study daily? (Hours )"
        ].iloc[0]
    )

    if not 0 <= study_hours <= 24:

        raise ValueError(
            "Daily study hours must be between 0 and 24."
        )

    # --------------------------------------------------------------
    # STUDY SESSIONS
    # --------------------------------------------------------------

    study_sessions = float(
        df[
            "How many times do you seat for study in a day?"
        ].iloc[0]
    )

    if not 0 <= study_sessions <= 30:

        raise ValueError(
            "Study sessions must be between 0 and 30."
        )

    # --------------------------------------------------------------
    # SOCIAL MEDIA
    # --------------------------------------------------------------

    social_media = float(
        df[
            "How many hour do you spent daily in social media? (Hours)"
        ].iloc[0]
    )

    if not 0 <= social_media <= 24:

        raise ValueError(
            "Social media hours must be between 0 and 24."
        )

    # --------------------------------------------------------------
    # SKILL DEVELOPMENT
    # --------------------------------------------------------------

    skill_hours = float(
        df[
            "How many hour do you spent daily on your skill development? (Hours )"
        ].iloc[0]
    )

    if not 0 <= skill_hours <= 24:

        raise ValueError(
            "Skill development hours must be between 0 and 24."
        )

    # --------------------------------------------------------------
    # CURRENT SEMESTER
    # --------------------------------------------------------------

    current_semester = float(
        df[
            "Current Semester"
        ].iloc[0]
    )

    if not 1 <= current_semester <= 12:

        raise ValueError(
            "Current Semester must be between 1 and 12."
        )

    # --------------------------------------------------------------
    # ATTENDANCE
    # --------------------------------------------------------------

    attendance = float(
        df[
            "Average attendance on class (Percentage )"
        ].iloc[0]
    )

    if not 0 <= attendance <= 100:

        raise ValueError(
            "Attendance must be between 0 and 100."
        )

    # --------------------------------------------------------------
    # COMPLETED CREDITS
    # --------------------------------------------------------------

    completed_credits = float(
        df[
            "How many Credit did you have completed?"
        ].iloc[0]
    )

    if not 0 <= completed_credits <= 145:

        raise ValueError(
            "Completed credits must be between 0 and 145."
        )

    # --------------------------------------------------------------
    # CATEGORICAL
    # --------------------------------------------------------------

    for column in CATEGORICAL_FEATURES:

        value = df[
            column
        ].iloc[0]

        if pd.isna(value):

            raise ValueError(
                f"Missing categorical value: {column}"
            )

        value = str(
            value
        ).strip()

        if not value:

            raise ValueError(
                f"Empty categorical value: {column}"
            )


# ======================================================================
# PREDICT CGPA
# ======================================================================

def predict_cgpa(
    age,
    gender,
    relationship_status,
    living_arrangement,
    health_issues,
    physical_disability,
    admission_year,
    hsc_year,
    scholarship,
    english_proficiency,
    study_hours,
    study_sessions,
    social_media_hours,
    skill_development_hours,
    current_semester,
    attendance,
    completed_credits,
):

    # --------------------------------------------------------------
    # LOAD COMPONENTS
    # --------------------------------------------------------------

    model, preprocessor, _ = (
        load_prediction_components()
    )

    # --------------------------------------------------------------
    # PREPARE RAW INPUT
    # --------------------------------------------------------------

    X_raw = prepare_prediction_input(

        age=age,

        gender=gender,

        relationship_status=
            relationship_status,

        living_arrangement=
            living_arrangement,

        health_issues=
            health_issues,

        physical_disability=
            physical_disability,

        admission_year=
            admission_year,

        hsc_year=
            hsc_year,

        scholarship=
            scholarship,

        english_proficiency=
            english_proficiency,

        study_hours=
            study_hours,

        study_sessions=
            study_sessions,

        social_media_hours=
            social_media_hours,

        skill_development_hours=
            skill_development_hours,

        current_semester=
            current_semester,

        attendance=
            attendance,

        completed_credits=
            completed_credits,
    )

    # --------------------------------------------------------------
    # VALIDATE
    # --------------------------------------------------------------

    validate_prediction_input(
        X_raw
    )

    # --------------------------------------------------------------
    # SAME PREPROCESSING USED DURING TRAINING
    # --------------------------------------------------------------

    X_processed = (
        preprocessor
        .transform(
            X_raw
        )
    )

    # --------------------------------------------------------------
    # RAW MODEL PREDICTION
    # --------------------------------------------------------------

    raw_prediction = (
        model.predict(
            X_processed
        )[0]
    )

    raw_prediction = float(
        raw_prediction
    )

    # --------------------------------------------------------------
    # FINAL POST-PROCESSING ADJUSTMENT
    #
    # Example:
    #   Raw      = 3.62
    #   Adjusted = 3.45
    # --------------------------------------------------------------

    adjusted_prediction = (
        raw_prediction
        - PREDICTION_ADJUSTMENT
    )

    # --------------------------------------------------------------
    # KEEP WITHIN VALID CGPA RANGE
    # --------------------------------------------------------------

    adjusted_prediction = np.clip(
        adjusted_prediction,
        MIN_PREDICTED_CGPA,
        MAX_PREDICTED_CGPA,
    )

    # --------------------------------------------------------------
    # ROUND TO TWO DECIMAL PLACES
    # --------------------------------------------------------------

    prediction = round(
        float(adjusted_prediction),
        2
    )

    # --------------------------------------------------------------
    # FINAL RESPONSE
    # --------------------------------------------------------------

    return {
        "predicted_cgpa":
            prediction
    }


# ======================================================================
# SERVICE STATUS
# ======================================================================

def prediction_service_status():

    try:

        model, preprocessor, metadata = (
            load_prediction_components()
        )

        model_name = "Unknown"

        if isinstance(
            metadata,
            dict
        ):

            model_name = metadata.get(
                "model_name",
                "Unknown"
            )

        return {

            "status":
                "ready",

            "model_loaded":
                model is not None,

            "preprocessor_loaded":
                preprocessor is not None,

            "feature_count":
                len(FEATURE_COLUMNS),

            "model_name":
                model_name,
        }

    except Exception as error:

        return {

            "status":
                "error",

            "message":
                str(error),
        }


# ======================================================================
# LOCAL TEST
# ======================================================================

if __name__ == "__main__":

    print()
    print("=" * 70)

    print(
        "CGPA PREDICTION SERVICE TEST"
    )

    print("=" * 70)

    # --------------------------------------------------------------
    # SERVICE STATUS
    # --------------------------------------------------------------

    print()
    print(
        "Service status:"
    )

    status = (
        prediction_service_status()
    )

    print(
        status
    )

    if status.get(
        "status"
    ) != "ready":

        raise RuntimeError(
            status.get(
                "message",
                "Prediction service failed to load."
            )
        )

    # --------------------------------------------------------------
    # UNSEEN STUDENT TEST
    # --------------------------------------------------------------

    print()
    print(
        "Testing new unseen student..."
    )

    result = predict_cgpa(

        age=21,

        gender="Female",

        relationship_status="Single",

        living_arrangement="Family",

        health_issues="No",

        physical_disability="No",

        admission_year=2022,

        hsc_year=2020,

        scholarship="Yes",

        english_proficiency="Intermediate",

        study_hours=5,

        study_sessions=2,

        social_media_hours=3,

        skill_development_hours=2,

        # B+ fields
        current_semester=6,

        attendance=88,

        completed_credits=78,
    )

    print()
    print("=" * 70)

    print(
        "PREDICTION RESULT"
    )

    print("=" * 70)

    print(
        f"Final Predicted CGPA: "
        f"{result['predicted_cgpa']:.2f}"
    )

    print("=" * 70)