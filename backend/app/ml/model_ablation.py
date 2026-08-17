"""
======================================================================
AI STUDENT ANALYTICS DASHBOARD
FEATURE ABLATION EXPERIMENT
======================================================================

Purpose:
    Compare different leakage-safe feature groups for CGPA regression.

Experiments:

    A - Demographic + Academic
    B - Demographic + Academic + Study/Behavior
    C - All current leakage-safe features

Metrics:
    MAE
    RMSE
    R²

Important:
    - No known leakage features are included.
    - Target is never used as an input feature.
    - Preprocessing is fitted separately inside each experiment.
    - No model is saved.
    - Original dataset is never modified.
======================================================================
"""

from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
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

REPORT_DIR = (
    BASE_DIR
    / "ml_reports"
)

REPORT_PATH = (
    REPORT_DIR
    / "feature_ablation_results.csv"
)


# ======================================================================
# TARGET
# ======================================================================

TARGET = "What is your current CGPA?"


# ======================================================================
# KNOWN LEAKAGE FEATURES
# ======================================================================

LEAKAGE_FEATURES = [

    "Program",

    "Current Semester",

    "Did you ever fall in probation?",

    "Did you ever got suspension?",

    "Average attendance on class (Percentage )",

    "Do you attend in teacher consultancy for any kind of academical problems?",
]


# ======================================================================
# FEATURE GROUPS
# ======================================================================

DEMOGRAPHIC_FEATURES = [

    "Age (Years)",

    "Gender",

    "What is your relationship status?",

    "With whom you are living with?",

    "Do you have any health issues?",

    "Do you have any physical disabilities?",
]


ACADEMIC_FEATURES = [

    "University Admission year",

    "H.S.C passing year",

    "Do you have meritorious scholarship ?",

    "Status of your English language proficiency",
]


STUDY_BEHAVIOR_FEATURES = [

    "How many hour do you study daily? (Hours )",

    "How many times do you seat for study in a day?",

    "How many hour do you spent daily in social media? (Hours)",

    "How many hour do you spent daily on your skill development? (Hours )",

]


ACCESS_FEATURES = [

    "Do you use University transportation?",

    "Do you use smart phone?",

    "Do you have personal Computer?",

    "What is your preferable learning mode?",

    "Are you engaged with any co-curriculum activities?",

]


FINANCIAL_FEATURES = [

    "What is your monthly Family Income",
]


SKILLS_COLUMN = (
    "What are the skills do you have ?"
)

INTEREST_COLUMN = (
    "What is you interested area?"
)


# ======================================================================
# SKILL DOMAINS
# ======================================================================

SKILL_DOMAINS = {

    "skill_programming": [
        "programming",
        "python",
        "java",
        "javascript",
        "php",
        "coding",
        "software development",
        "web development",
        "frontend",
        "backend",
        "full stack",
    ],

    "skill_ai_ml": [
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "data science",
        "ai",
        "ml",
    ],

    "skill_design": [
        "graphic",
        "graphics",
        "design",
        "photoshop",
        "logo",
        "ui",
        "ux",
        "animation",
        "photography",
        "video editing",
        "poster",
    ],

    "skill_cybersecurity": [
        "cyber",
        "security",
        "hacking",
        "kali",
        "forensic",
        "networking",
    ],

    "skill_marketing": [
        "marketing",
        "digital marketing",
        "seo",
        "content",
        "freelancing",
        "entrepreneur",
    ],

    "skill_technical": [
        "iot",
        "hardware",
        "network",
        "isp",
        "system",
        "wordpress",
        "mis",
    ],

    "skill_other": [
        "teaching",
        "mentoring",
        "sports",
        "volunteering",
        "problem solving",
        "communication",
    ],
}


# ======================================================================
# INTEREST DOMAINS
# ======================================================================

INTEREST_DOMAINS = {

    "interest_ai_ml": [
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "ai",
        "data science",
    ],

    "interest_programming": [
        "programming",
        "software",
        "web",
        "web development",
        "web developer",
        "full stack",
        "app",
    ],

    "interest_cybersecurity": [
        "cyber",
        "cybersecurity",
        "security",
        "hacking",
        "kali",
        "forensic",
    ],

    "interest_design": [
        "graphics",
        "graphic design",
        "ui",
        "ux",
        "design",
    ],

    "interest_business": [
        "marketing",
        "digital marketing",
        "entrepreneur",
        "freelancing",
        "bcs",
    ],

    "interest_technical": [
        "iot",
        "hardware",
        "networking",
        "physics",
        "mathematics",
        "blockchain",
    ],
}


# ======================================================================
# UTILITY
# ======================================================================

def header(title):

    print()
    print("=" * 75)
    print(title)
    print("=" * 75)


# ======================================================================
# LOAD DATASET
# ======================================================================

def load_dataset():

    header("LOADING CLEANED DATASET")

    if not DATASET_PATH.exists():

        raise FileNotFoundError(
            f"""
Cleaned dataset not found:

{DATASET_PATH}

Run target_cleaning.py first.
"""
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
        f"Dataset: {DATASET_PATH}"
    )

    print(
        f"Rows    : {len(df)}"
    )

    print(
        f"Columns : {len(df.columns)}"
    )

    return df


# ======================================================================
# TARGET CLEANING / VALIDATION
# ======================================================================

def validate_target(df):

    df = df.copy()

    df[TARGET] = pd.to_numeric(
        df[TARGET],
        errors="coerce"
    )

    invalid = (
        (df[TARGET] < 0)
        |
        (df[TARGET] > 4)
    )

    df = df.loc[
        ~df[TARGET].isna()
        & ~invalid
    ].copy()

    if len(df) == 0:

        raise ValueError(
            "No valid target rows remain."
        )

    return df


# ======================================================================
# NORMALIZE TEXT
# ======================================================================

def normalize_text(df):

    df = df.copy()

    for column in df.select_dtypes(
        include=["object", "string"]
    ).columns:

        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )

    return df


# ======================================================================
# NUMERICAL CLEANING
# ======================================================================

def clean_numerical_features(df):

    df = df.copy()

    numerical_columns = [

        "University Admission year",

        "Age (Years)",

        "H.S.C passing year",

        "How many hour do you study daily? (Hours )",

        "How many times do you seat for study in a day?",

        "How many hour do you spent daily in social media? (Hours)",

        "How many hour do you spent daily on your skill development? (Hours )",

        "What is your monthly Family Income",
    ]

    for column in numerical_columns:

        if column not in df.columns:
            continue

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # --------------------------------------------------------------
    # Valid ranges
    # --------------------------------------------------------------

    rules = {

        "University Admission year": (
            1990,
            2035
        ),

        "Age (Years)": (
            15,
            80
        ),

        "H.S.C passing year": (
            1990,
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

        "How many hour do you spent daily on your skill development? (Hours )": (
            0,
            24
        ),

        "What is your monthly Family Income": (
            0,
            np.inf
        ),
    }

    for column, (minimum, maximum) in rules.items():

        if column not in df.columns:
            continue

        if np.isinf(maximum):

            invalid_mask = (
                df[column] < minimum
            )

        else:

            invalid_mask = (
                (df[column] < minimum)
                |
                (df[column] > maximum)
            )

        df.loc[
            invalid_mask,
            column
        ] = np.nan

    return df


# ======================================================================
# CATEGORICAL CLEANING
# ======================================================================

def clean_categorical_features(df):

    df = df.copy()

    categorical_columns = (

        DEMOGRAPHIC_FEATURES
        + ACADEMIC_FEATURES
        + STUDY_BEHAVIOR_FEATURES
        + ACCESS_FEATURES
        + FINANCIAL_FEATURES
    )

    for column in categorical_columns:

        if column not in df.columns:
            continue

        # Only clean string/object columns.
        if (
            df[column].dtype == "object"
            or
            pd.api.types.is_string_dtype(
                df[column]
            )
        ):

            df[column] = (
                df[column]
                .astype("string")
                .str.strip()
            )

    return df


# ======================================================================
# MULTI-RESPONSE PARSER
# ======================================================================

def parse_multi_response(value):

    if pd.isna(value):

        return []

    text = (
        str(value)
        .strip()
        .lower()
    )

    if not text:

        return []

    # Handle common delimiters.
    for separator in [
        ";",
        "|",
        "/",
        "\\",
        "\n",
    ]:

        text = text.replace(
            separator,
            ","
        )

    values = []

    for item in text.split(","):

        item = item.strip()

        if item:

            values.append(item)

    return values


# ======================================================================
# DOMAIN FEATURE CREATION
# ======================================================================

def create_domain_features(
    df,
    source_column,
    domains,
):

    result = pd.DataFrame(
        index=df.index
    )

    for feature_name, keywords in domains.items():

        def detect(value):

            values = parse_multi_response(
                value
            )

            for item in values:

                for keyword in keywords:

                    if keyword.lower() in item:

                        return 1

            return 0

        result[feature_name] = (
            df[source_column]
            .apply(detect)
        )

    return result


# ======================================================================
# CREATE ENGINEERED FEATURES
# ======================================================================

def engineer_features(df):

    df = df.copy()

    # --------------------------------------------------------------
    # Skills
    # --------------------------------------------------------------

    if SKILLS_COLUMN in df.columns:

        skills = create_domain_features(
            df,
            SKILLS_COLUMN,
            SKILL_DOMAINS,
        )

        df = pd.concat(
            [
                df,
                skills
            ],
            axis=1
        )

        df["skill_count"] = (
            skills.sum(axis=1)
        )

    # --------------------------------------------------------------
    # Interests
    # --------------------------------------------------------------

    if INTEREST_COLUMN in df.columns:

        interests = create_domain_features(
            df,
            INTEREST_COLUMN,
            INTEREST_DOMAINS,
        )

        df = pd.concat(
            [
                df,
                interests
            ],
            axis=1
        )

        df["interest_count"] = (
            interests.sum(axis=1)
        )

    return df


# ======================================================================
# FEATURE GROUP DEFINITIONS
# ======================================================================

def feature_groups():

    engineered_skill_features = (
        list(SKILL_DOMAINS.keys())
        + ["skill_count"]
    )

    engineered_interest_features = (
        list(INTEREST_DOMAINS.keys())
        + ["interest_count"]
    )

    groups = {

        "A_Demographic_Academic":
            (
                DEMOGRAPHIC_FEATURES
                + ACADEMIC_FEATURES
            ),

        "B_Demographic_Academic_Behavior":
            (
                DEMOGRAPHIC_FEATURES
                + ACADEMIC_FEATURES
                + STUDY_BEHAVIOR_FEATURES
            ),

        "C_All_Leakage_Safe":
            (
                DEMOGRAPHIC_FEATURES
                + ACADEMIC_FEATURES
                + STUDY_BEHAVIOR_FEATURES
                + ACCESS_FEATURES
                + FINANCIAL_FEATURES
                + engineered_skill_features
                + engineered_interest_features
            ),
    }

    return groups


# ======================================================================
# VALIDATE FEATURE GROUP
# ======================================================================

def validate_feature_group(
    df,
    feature_list
):

    available = [
        feature
        for feature in feature_list
        if feature in df.columns
    ]

    missing = [
        feature
        for feature in feature_list
        if feature not in df.columns
    ]

    if missing:

        print()
        print(
            "⚠ Missing features:"
        )

        for feature in missing:

            print(
                f"   - {feature}"
            )

    return available


# ======================================================================
# BUILD PREPROCESSOR
# ======================================================================

def build_preprocessor(
    X_train
):

    numerical_columns = [
        column
        for column in X_train.columns
        if pd.api.types.is_numeric_dtype(
            X_train[column]
        )
    ]

    categorical_columns = [
        column
        for column in X_train.columns
        if column not in numerical_columns
    ]

    numerical_pipeline = Pipeline(
        steps=[

            (
                "imputer",
                SimpleImputer(
                    strategy="median"
                )
            ),

            (
                "scaler",
                StandardScaler()
            ),

        ]
    )

    categorical_pipeline = Pipeline(
        steps=[

            (
                "imputer",
                SimpleImputer(
                    strategy="most_frequent"
                )
            ),

            (
                "encoder",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=False
                )
            ),

        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[

            (
                "numerical",
                numerical_pipeline,
                numerical_columns
            ),

            (
                "categorical",
                categorical_pipeline,
                categorical_columns
            ),

        ],

        remainder="drop"
    )

    return preprocessor


# ======================================================================
# EVALUATE ONE EXPERIMENT
# ======================================================================

def evaluate_experiment(
    name,
    X,
    y
):

    print()
    print("=" * 75)
    print(
        f"EXPERIMENT: {name}"
    )
    print("=" * 75)

    print(
        f"Raw feature count: {X.shape[1]}"
    )

    # --------------------------------------------------------------
    # Same fixed split for every experiment
    # --------------------------------------------------------------

    X_train_raw, X_test_raw, y_train, y_test = (
        train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=42
        )
    )

    print(
        f"Training samples: {len(X_train_raw)}"
    )

    print(
        f"Testing samples : {len(X_test_raw)}"
    )

    # --------------------------------------------------------------
    # Preprocessing fitted only on training data
    # --------------------------------------------------------------

    preprocessor = build_preprocessor(
        X_train_raw
    )

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

    # --------------------------------------------------------------
    # Model
    # --------------------------------------------------------------

    model = RandomForestRegressor(

        n_estimators=500,

        max_depth=8,

        min_samples_leaf=6,

        min_samples_split=2,

        max_features=0.4,

        random_state=42,

        n_jobs=-1
    )

    model.fit(
        X_train,
        y_train
    )

    predictions = model.predict(
        X_test
    )

    # --------------------------------------------------------------
    # Metrics
    # --------------------------------------------------------------

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_test,
            predictions
        )
    )

    r2 = r2_score(
        y_test,
        predictions
    )

    # --------------------------------------------------------------
    # Print
    # --------------------------------------------------------------

    print()
    print(
        f"Processed features : "
        f"{X_train.shape[1]}"
    )

    print(
        f"MAE                : "
        f"{mae:.4f}"
    )

    print(
        f"RMSE               : "
        f"{rmse:.4f}"
    )

    print(
        f"R²                 : "
        f"{r2:.4f}"
    )

    print(
        f"Expected GPA Error : "
        f"±{mae:.2f} GPA"
    )

    return {

        "experiment": name,

        "raw_features":
            int(X.shape[1]),

        "processed_features":
            int(X_train.shape[1]),

        "train_samples":
            int(len(X_train)),

        "test_samples":
            int(len(X_test)),

        "mae":
            float(mae),

        "rmse":
            float(rmse),

        "r2":
            float(r2),

    }


# ======================================================================
# MAIN
# ======================================================================

def main():

    header(
        "AI STUDENT ANALYTICS DASHBOARD"
    )

    print(
        "FEATURE ABLATION EXPERIMENT"
    )

    # --------------------------------------------------------------
    # Load
    # --------------------------------------------------------------

    df = load_dataset()

    # --------------------------------------------------------------
    # Normalize
    # --------------------------------------------------------------

    df = normalize_text(
        df
    )

    # --------------------------------------------------------------
    # Target
    # --------------------------------------------------------------

    df = validate_target(
        df
    )

    # --------------------------------------------------------------
    # Numerical
    # --------------------------------------------------------------

    df = clean_numerical_features(
        df
    )

    # --------------------------------------------------------------
    # Categorical
    # --------------------------------------------------------------

    df = clean_categorical_features(
        df
    )

    # --------------------------------------------------------------
    # Feature engineering
    # --------------------------------------------------------------

    df = engineer_features(
        df
    )

    # --------------------------------------------------------------
    # Feature groups
    # --------------------------------------------------------------

    groups = feature_groups()

    # --------------------------------------------------------------
    # Run experiments
    # --------------------------------------------------------------

    results = []

    for name, requested_features in groups.items():

        available_features = (
            validate_feature_group(
                df,
                requested_features
            )
        )

        # Remove any leakage feature defensively
        available_features = [

            feature

            for feature in available_features

            if feature not in LEAKAGE_FEATURES

            and feature != TARGET

        ]

        if not available_features:

            print(
                f"\n❌ No usable features for {name}"
            )

            continue

        X = df[
            available_features
        ].copy()

        y = df[
            TARGET
        ].copy()

        result = evaluate_experiment(
            name,
            X,
            y
        )

        results.append(
            result
        )

    # --------------------------------------------------------------
    # Results table
    # --------------------------------------------------------------

    header(
        "FEATURE ABLATION RESULTS"
    )

    results_df = pd.DataFrame(
        results
    )

    if results_df.empty:

        raise RuntimeError(
            "No ablation experiments were completed."
        )

    results_df = results_df.sort_values(
        by="mae",
        ascending=True
    ).reset_index(
        drop=True
    )

    results_df.insert(
        0,
        "rank",
        np.arange(
            1,
            len(results_df) + 1
        )
    )

    print()

    print(
        results_df.to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}"
        )
    )

    # --------------------------------------------------------------
    # Best experiment
    # --------------------------------------------------------------

    best = results_df.iloc[
        0
    ]

    print()
    print("=" * 75)
    print("BEST FEATURE SET")
    print("=" * 75)

    print()

    print(
        f"Experiment        : "
        f"{best['experiment']}"
    )

    print(
        f"Raw features      : "
        f"{best['raw_features']}"
    )

    print(
        f"Processed features: "
        f"{best['processed_features']}"
    )

    print(
        f"MAE               : "
        f"{best['mae']:.4f}"
    )

    print(
        f"RMSE              : "
        f"{best['rmse']:.4f}"
    )

    print(
        f"R²                : "
        f"{best['r2']:.4f}"
    )

    print(
        f"Expected error    : "
        f"±{best['mae']:.2f} GPA"
    )

    # --------------------------------------------------------------
    # Save
    # --------------------------------------------------------------

    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    results_df.to_csv(
        REPORT_PATH,
        index=False,
        encoding="utf-8-sig"
    )

    print()
    print(
        f"✓ Results saved:"
    )

    print(
        REPORT_PATH
    )

    # --------------------------------------------------------------
    # Final
    # --------------------------------------------------------------

    print()
    print("=" * 75)
    print("ABLATION EXPERIMENT COMPLETE")
    print("=" * 75)

    print()
    print(
        "IMPORTANT:"
    )

    print(
        "This experiment does NOT replace the production model yet."
    )

    print(
        "Use the results to select the final feature set."
    )


# ======================================================================
# ENTRY POINT
# ======================================================================

if __name__ == "__main__":

    main()