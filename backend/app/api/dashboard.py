from pathlib import Path

import pandas as pd
from fastapi import APIRouter, HTTPException


router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"],
)


# ============================================================
# PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATASET_PATH = (
    BASE_DIR
    / "dataset"
    / "IUBAT_CGPA_Training_Cleaned.csv"
)


# ============================================================
# LOAD DATASET
# ============================================================

def load_dashboard_dataset():

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

    return df


# ============================================================
# NORMALIZE
# ============================================================

def normalize_dataframe(df):

    df = df.copy()

    for column in df.columns:

        if (
            df[column].dtype == "object"
            or pd.api.types.is_string_dtype(
                df[column]
            )
        ):

            df[column] = (
                df[column]
                .astype("string")
                .str.strip()
            )

    return df


# ============================================================
# MAIN ANALYTICS ENDPOINT
# ============================================================

@router.get("/analytics")
def analytics():

    try:

        df = load_dashboard_dataset()

        df = normalize_dataframe(
            df
        )

        target = (
            "What is your current CGPA?"
        )

        scholarship = (
            "Do you have meritorious scholarship ?"
        )

        study_hours = (
            "How many hour do you study daily? (Hours )"
        )

        social_media = (
            "How many hour do you spent daily in social media? (Hours)"
        )

        skill_hours = (
            "How many hour do you spent daily on your skill development? (Hours )"
        )

        admission_year = (
            "University Admission year"
        )

        hsc_year = (
            "H.S.C passing year"
        )

        age = (
            "Age (Years)"
        )

        gender = (
            "Gender"
        )

        english = (
            "Status of your English language proficiency"
        )

        relationship = (
            "What is your relationship status?"
        )

        living = (
            "With whom you are living with?"
        )

        # --------------------------------------------------------
        # Numeric conversion
        # --------------------------------------------------------

        numeric_columns = [
            target,
            study_hours,
            social_media,
            skill_hours,
            admission_year,
            hsc_year,
            age,
        ]

        for column in numeric_columns:

            if column in df.columns:

                df[column] = pd.to_numeric(
                    df[column],
                    errors="coerce"
                )

        # --------------------------------------------------------
        # KPI
        # --------------------------------------------------------

        total_students = len(df)

        average_cgpa = float(
            df[target].mean()
        )

        average_age = float(
            df[age].mean()
        )

        average_study_hours = float(
            df[study_hours].mean()
        )

        average_social_media = float(
            df[social_media].mean()
        )

        scholarship_counts = (
            df[scholarship]
            .fillna("Unknown")
            .value_counts()
        )

        scholarship_yes = sum(
            count
            for value, count
            in scholarship_counts.items()
            if str(value).strip().lower()
            in ["yes", "true", "1"]
        )

        scholarship_rate = (
            scholarship_yes
            /
            total_students
            *
            100
            if total_students
            else 0
        )

        # --------------------------------------------------------
        # CGPA distribution
        # --------------------------------------------------------

        def cgpa_band(value):

            if value < 2.50:
                return "Below 2.50"

            if value < 3.00:
                return "2.50 - 2.99"

            if value < 3.40:
                return "3.00 - 3.39"

            if value < 3.80:
                return "3.40 - 3.79"

            return "3.80 - 4.00"

        cgpa_df = (
            df[
                [target]
            ]
            .dropna()
            .copy()
        )

        cgpa_df["CGPA Range"] = (
            cgpa_df[target]
            .apply(cgpa_band)
        )

        cgpa_distribution = (
            cgpa_df[
                "CGPA Range"
            ]
            .value_counts()
            .reindex(
                [
                    "Below 2.50",
                    "2.50 - 2.99",
                    "3.00 - 3.39",
                    "3.40 - 3.79",
                    "3.80 - 4.00",
                ],
                fill_value=0,
            )
            .reset_index()
        )

        cgpa_distribution.columns = [
            "range",
            "count",
        ]

        # --------------------------------------------------------
        # Gender distribution
        # --------------------------------------------------------

        gender_distribution = (
            df[gender]
            .fillna("Unknown")
            .value_counts()
            .reset_index()
        )

        gender_distribution.columns = [
            "gender",
            "count",
        ]

        # --------------------------------------------------------
        # Scholarship analysis
        # --------------------------------------------------------

        scholarship_analysis = (
            df.groupby(
                scholarship,
                dropna=False
            )[target]
            .agg(
                students="count",
                average_cgpa="mean",
            )
            .reset_index()
        )

        scholarship_analysis[
            scholarship
        ] = (
            scholarship_analysis[
                scholarship
            ]
            .fillna("Unknown")
            .astype(str)
        )

        scholarship_analysis = (
            scholarship_analysis
            .rename(
                columns={
                    scholarship:
                        "status"
                }
            )
        )

        # --------------------------------------------------------
        # Study hours analysis
        # --------------------------------------------------------

        study_df = df[
            [
                study_hours,
                target,
            ]
        ].dropna().copy()

        study_df["study_band"] = pd.cut(
            study_df[study_hours],
            bins=[
                -0.01,
                2,
                4,
                6,
                8,
                24,
            ],
            labels=[
                "0-2 hrs",
                "2-4 hrs",
                "4-6 hrs",
                "6-8 hrs",
                "8+ hrs",
            ],
        )

        study_analysis = (
            study_df.groupby(
                "study_band",
                observed=False
            )[target]
            .agg(
                students="count",
                average_cgpa="mean",
            )
            .reset_index()
        )

        study_analysis[
            "study_band"
        ] = (
            study_analysis[
                "study_band"
            ]
            .astype(str)
        )

        # --------------------------------------------------------
        # English proficiency
        # --------------------------------------------------------

        english_distribution = (
            df[english]
            .fillna("Unknown")
            .value_counts()
            .reset_index()
        )

        english_distribution.columns = [
            "level",
            "count",
        ]

        # --------------------------------------------------------
        # Relationship
        # --------------------------------------------------------

        relationship_distribution = (
            df[relationship]
            .fillna("Unknown")
            .value_counts()
            .head(8)
            .reset_index()
        )

        relationship_distribution.columns = [
            "status",
            "count",
        ]

        # --------------------------------------------------------
        # Living arrangement
        # --------------------------------------------------------

        living_distribution = (
            df[living]
            .fillna("Unknown")
            .value_counts()
            .head(8)
            .reset_index()
        )

        living_distribution.columns = [
            "arrangement",
            "count",
        ]

        # --------------------------------------------------------
        # Insights
        # --------------------------------------------------------

        top_gender = (
            gender_distribution.iloc[0].to_dict()
            if len(gender_distribution)
            else None
        )

        top_english = (
            english_distribution.iloc[0].to_dict()
            if len(english_distribution)
            else None
        )

        top_scholarship = (
            scholarship_analysis
            .sort_values(
                "students",
                ascending=False
            )
            .iloc[0]
            .to_dict()
            if len(scholarship_analysis)
            else None
        )

        best_scholarship_group = (
            scholarship_analysis
            .sort_values(
                "average_cgpa",
                ascending=False
            )
            .iloc[0]
            .to_dict()
            if len(scholarship_analysis)
            else None
        )

        return {

            "success": True,

            "kpis": {
                "total_students":
                    total_students,

                "average_cgpa":
                    round(
                        average_cgpa,
                        2
                    ),

                "average_age":
                    round(
                        average_age,
                        2
                    ),

                "average_study_hours":
                    round(
                        average_study_hours,
                        2
                    ),

                "average_social_media_hours":
                    round(
                        average_social_media,
                        2
                    ),

                "scholarship_rate":
                    round(
                        scholarship_rate,
                        2
                    ),
            },

            "charts": {

                "cgpa_distribution":
                    cgpa_distribution.to_dict(
                        orient="records"
                    ),

                "gender_distribution":
                    gender_distribution.to_dict(
                        orient="records"
                    ),

                "scholarship_analysis":
                    scholarship_analysis.to_dict(
                        orient="records"
                    ),

                "study_analysis":
                    study_analysis.to_dict(
                        orient="records"
                    ),

                "english_distribution":
                    english_distribution.to_dict(
                        orient="records"
                    ),

                "relationship_distribution":
                    relationship_distribution.to_dict(
                        orient="records"
                    ),

                "living_distribution":
                    living_distribution.to_dict(
                        orient="records"
                    ),
            },

            "insights": {

                "top_gender":
                    top_gender,

                "top_english":
                    top_english,

                "top_scholarship":
                    top_scholarship,

                "best_scholarship_group":
                    best_scholarship_group,
            },

        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                "Dashboard analytics failed: "
                f"{str(error)}"
            )
        )