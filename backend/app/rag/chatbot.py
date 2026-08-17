"""
======================================================================
AI STUDENT ANALYTICS DASHBOARD
FINAL LOCAL AI CHATBOT
======================================================================

Data source:
    IUBAT_CGPA_Training_Cleaned.csv

LLM:
    Ollama
    llama3.2:1b

Design:
    Python/Pandas handles exact dataset statistics.
    Ollama handles natural-language interpretation.

Important:
    - No cloud API
    - No OpenAI API
    - No fabricated numerical statistics
    - Uses the finalized cleaned dataset
======================================================================
"""

import json
import os
from pathlib import Path
from typing import Optional

import pandas as pd
import requests


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
# OLLAMA CONFIGURATION
# ======================================================================

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://127.0.0.1:11434/api/generate"
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2:1b"
)


# ======================================================================
# FINAL DATASET COLUMNS
# ======================================================================

TARGET = (
    "What is your current CGPA?"
)

AGE = (
    "Age (Years)"
)

GENDER = (
    "Gender"
)

RELATIONSHIP = (
    "What is your relationship status?"
)

LIVING = (
    "With whom you are living with?"
)

HEALTH = (
    "Do you have any health issues?"
)

PHYSICAL_DISABILITY = (
    "Do you have any physical disabilities?"
)

ADMISSION_YEAR = (
    "University Admission year"
)

HSC_YEAR = (
    "H.S.C passing year"
)

SCHOLARSHIP = (
    "Do you have meritorious scholarship ?"
)

ENGLISH = (
    "Status of your English language proficiency"
)

STUDY_HOURS = (
    "How many hour do you study daily? (Hours )"
)

STUDY_SESSIONS = (
    "How many times do you seat for study in a day?"
)

SOCIAL_MEDIA = (
    "How many hour do you spent daily in social media? (Hours)"
)

SKILL_HOURS = (
    "How many hour do you spent daily on your skill development? (Hours )"
)


# ======================================================================
# DATASET LOADING
# ======================================================================

def get_dataset() -> pd.DataFrame:
    """
    Load the finalized cleaned training dataset directly.
    """

    if not DATASET_PATH.exists():

        raise FileNotFoundError(
            f"Cleaned dataset not found:\n{DATASET_PATH}"
        )

    df = pd.read_csv(
        DATASET_PATH
    )

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    # Normalize text columns
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


# ======================================================================
# VALIDATE FINAL DATASET
# ======================================================================

def validate_dataset_columns(
    df: pd.DataFrame
):
    """
    Make sure the chatbot is using the final dataset schema.
    """

    required_columns = [

        TARGET,
        AGE,
        GENDER,
        RELATIONSHIP,
        LIVING,
        HEALTH,
        PHYSICAL_DISABILITY,
        ADMISSION_YEAR,
        HSC_YEAR,
        SCHOLARSHIP,
        ENGLISH,
        STUDY_HOURS,
        STUDY_SESSIONS,
        SOCIAL_MEDIA,
        SKILL_HOURS,
    ]

    missing = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing:

        raise ValueError(
            "Final dataset is missing required columns:\n"
            + "\n".join(
                f"- {column}"
                for column in missing
            )
        )


# ======================================================================
# SAFE NUMERIC CONVERSION
# ======================================================================

def numeric_series(
    df: pd.DataFrame,
    column: str
):

    return pd.to_numeric(
        df[column],
        errors="coerce"
    ).dropna()


# ======================================================================
# EXACT DATASET STATISTICS
# ======================================================================

def calculate_exact_statistics(
    df: pd.DataFrame
):
    """
    Calculate exact statistics using Pandas.

    The LLM never calculates these values.
    """

    validate_dataset_columns(
        df
    )

    stats = {}

    # ------------------------------------------------------------------
    # Dataset
    # ------------------------------------------------------------------

    stats["total_students"] = int(
        len(df)
    )

    stats["total_columns"] = int(
        len(df.columns)
    )

    # ------------------------------------------------------------------
    # CGPA
    # ------------------------------------------------------------------

    cgpa = numeric_series(
        df,
        TARGET
    )

    if len(cgpa) > 0:

        stats["cgpa"] = {

            "count":
                int(len(cgpa)),

            "minimum":
                round(
                    float(cgpa.min()),
                    2
                ),

            "maximum":
                round(
                    float(cgpa.max()),
                    2
                ),

            "average":
                round(
                    float(cgpa.mean()),
                    2
                ),

            "median":
                round(
                    float(cgpa.median()),
                    2
                ),

        }

        # CGPA ranges
        stats["cgpa_ranges"] = {

            "Below 2.50":
                int(
                    (cgpa < 2.50).sum()
                ),

            "2.50 - 2.99":
                int(
                    (
                        (cgpa >= 2.50)
                        &
                        (cgpa < 3.00)
                    ).sum()
                ),

            "3.00 - 3.39":
                int(
                    (
                        (cgpa >= 3.00)
                        &
                        (cgpa < 3.40)
                    ).sum()
                ),

            "3.40 - 3.79":
                int(
                    (
                        (cgpa >= 3.40)
                        &
                        (cgpa < 3.80)
                    ).sum()
                ),

            "3.80 - 4.00":
                int(
                    (
                        (cgpa >= 3.80)
                        &
                        (cgpa <= 4.00)
                    ).sum()
                ),
        }

    # ------------------------------------------------------------------
    # Age
    # ------------------------------------------------------------------

    age = numeric_series(
        df,
        AGE
    )

    if len(age) > 0:

        stats["age"] = {

            "average":
                round(
                    float(age.mean()),
                    2
                ),

            "minimum":
                round(
                    float(age.min()),
                    2
                ),

            "maximum":
                round(
                    float(age.max()),
                    2
                ),
        }

    # ------------------------------------------------------------------
    # Study hours
    # ------------------------------------------------------------------

    study_hours = numeric_series(
        df,
        STUDY_HOURS
    )

    if len(study_hours) > 0:

        stats["study_hours"] = {

            "average":
                round(
                    float(study_hours.mean()),
                    2
                ),

            "minimum":
                round(
                    float(study_hours.min()),
                    2
                ),

            "maximum":
                round(
                    float(study_hours.max()),
                    2
                ),
        }

    # ------------------------------------------------------------------
    # Study sessions
    # ------------------------------------------------------------------

    sessions = numeric_series(
        df,
        STUDY_SESSIONS
    )

    if len(sessions) > 0:

        stats["study_sessions"] = {

            "average":
                round(
                    float(sessions.mean()),
                    2
                ),

            "minimum":
                round(
                    float(sessions.min()),
                    2
                ),

            "maximum":
                round(
                    float(sessions.max()),
                    2
                ),
        }

    # ------------------------------------------------------------------
    # Social media
    # ------------------------------------------------------------------

    social = numeric_series(
        df,
        SOCIAL_MEDIA
    )

    if len(social) > 0:

        stats["social_media_hours"] = {

            "average":
                round(
                    float(social.mean()),
                    2
                ),

            "minimum":
                round(
                    float(social.min()),
                    2
                ),

            "maximum":
                round(
                    float(social.max()),
                    2
                ),
        }

    # ------------------------------------------------------------------
    # Skill development
    # ------------------------------------------------------------------

    skill_hours = numeric_series(
        df,
        SKILL_HOURS
    )

    if len(skill_hours) > 0:

        stats["skill_development_hours"] = {

            "average":
                round(
                    float(skill_hours.mean()),
                    2
                ),

            "minimum":
                round(
                    float(skill_hours.min()),
                    2
                ),

            "maximum":
                round(
                    float(skill_hours.max()),
                    2
                ),
        }

    # ------------------------------------------------------------------
    # Admission year
    # ------------------------------------------------------------------

    admission_year = numeric_series(
        df,
        ADMISSION_YEAR
    )

    if len(admission_year) > 0:

        stats["admission_year"] = {

            "minimum":
                int(admission_year.min()),

            "maximum":
                int(admission_year.max()),
        }

    # ------------------------------------------------------------------
    # HSC year
    # ------------------------------------------------------------------

    hsc_year = numeric_series(
        df,
        HSC_YEAR
    )

    if len(hsc_year) > 0:

        stats["hsc_year"] = {

            "minimum":
                int(hsc_year.min()),

            "maximum":
                int(hsc_year.max()),
        }

    # ------------------------------------------------------------------
    # Gender distribution
    # ------------------------------------------------------------------

    stats["gender_distribution"] = (
        df[GENDER]
        .fillna("Unknown")
        .astype(str)
        .value_counts()
        .to_dict()
    )

    stats["gender_distribution"] = {
        str(key): int(value)
        for key, value
        in stats["gender_distribution"].items()
    }

    # ------------------------------------------------------------------
    # Scholarship distribution
    # ------------------------------------------------------------------

    stats["scholarship_distribution"] = (
        df[SCHOLARSHIP]
        .fillna("Unknown")
        .astype(str)
        .value_counts()
        .to_dict()
    )

    stats["scholarship_distribution"] = {
        str(key): int(value)
        for key, value
        in stats["scholarship_distribution"].items()
    }

    # ------------------------------------------------------------------
    # English
    # ------------------------------------------------------------------

    stats["english_distribution"] = (
        df[ENGLISH]
        .fillna("Unknown")
        .astype(str)
        .value_counts()
        .to_dict()
    )

    stats["english_distribution"] = {
        str(key): int(value)
        for key, value
        in stats["english_distribution"].items()
    }

    # ------------------------------------------------------------------
    # Relationship
    # ------------------------------------------------------------------

    stats["relationship_distribution"] = (
        df[RELATIONSHIP]
        .fillna("Unknown")
        .astype(str)
        .value_counts()
        .head(10)
        .to_dict()
    )

    stats["relationship_distribution"] = {
        str(key): int(value)
        for key, value
        in stats[
            "relationship_distribution"
        ].items()
    }

    # ------------------------------------------------------------------
    # Living arrangement
    # ------------------------------------------------------------------

    stats["living_distribution"] = (
        df[LIVING]
        .fillna("Unknown")
        .astype(str)
        .value_counts()
        .head(10)
        .to_dict()
    )

    stats["living_distribution"] = {
        str(key): int(value)
        for key, value
        in stats[
            "living_distribution"
        ].items()
    }

    # ------------------------------------------------------------------
    # Health
    # ------------------------------------------------------------------

    stats["health_distribution"] = (
        df[HEALTH]
        .fillna("Unknown")
        .astype(str)
        .value_counts()
        .to_dict()
    )

    stats["health_distribution"] = {
        str(key): int(value)
        for key, value
        in stats[
            "health_distribution"
        ].items()
    }

    # ------------------------------------------------------------------
    # Physical disability
    # ------------------------------------------------------------------

    stats["physical_disability_distribution"] = (
        df[PHYSICAL_DISABILITY]
        .fillna("Unknown")
        .astype(str)
        .value_counts()
        .to_dict()
    )

    stats["physical_disability_distribution"] = {
        str(key): int(value)
        for key, value
        in stats[
            "physical_disability_distribution"
        ].items()
    }

    return stats


# ======================================================================
# DATASET CONTEXT FOR OLLAMA
# ======================================================================

def build_dataset_context(
    statistics
):
    """
    Convert exact Python statistics into compact
    context for the local model.
    """

    return json.dumps(
        statistics,
        indent=2,
        ensure_ascii=False
    )


# ======================================================================
# QUESTION DETECTION
# ======================================================================

def detect_statistical_question(
    question: str
):
    """
    Detect common questions that should be answered
    exactly by Python rather than the LLM.
    """

    q = (
        question
        .lower()
        .strip()
    )

    # --------------------------------------------------------------
    # Total students
    # --------------------------------------------------------------

    if any(
        phrase in q
        for phrase in [
            "how many students",
            "number of students",
            "total students",
            "student count",
            "how many student",
        ]
    ):

        return "total_students"

    # --------------------------------------------------------------
    # Average CGPA
    # --------------------------------------------------------------

    if any(
        phrase in q
        for phrase in [
            "average cgpa",
            "mean cgpa",
            "avg cgpa",
            "overall cgpa",
        ]
    ):

        return "average_cgpa"

    # --------------------------------------------------------------
    # CGPA min/max
    # --------------------------------------------------------------

    if (
        "highest cgpa" in q
        or "maximum cgpa" in q
        or "max cgpa" in q
    ):

        return "maximum_cgpa"

    if (
        "lowest cgpa" in q
        or "minimum cgpa" in q
        or "min cgpa" in q
    ):

        return "minimum_cgpa"

    # --------------------------------------------------------------
    # Age
    # --------------------------------------------------------------

    if (
        "average age" in q
        or "mean age" in q
    ):

        return "average_age"

    # --------------------------------------------------------------
    # Study hours
    # --------------------------------------------------------------

    if (
        "average study hours" in q
        or "average study hour" in q
        or "mean study hours" in q
        or "how many hours do students study" in q
    ):

        return "average_study_hours"

    # --------------------------------------------------------------
    # Study sessions
    # --------------------------------------------------------------

    if (
        "study sessions" in q
        or "study session" in q
    ):

        return "average_study_sessions"

    # --------------------------------------------------------------
    # Social media
    # --------------------------------------------------------------

    if (
        "average social media" in q
        or "social media hours" in q
    ):

        return "average_social_media"

    # --------------------------------------------------------------
    # Skill development
    # --------------------------------------------------------------

    if (
        "skill development" in q
        or "skill development hours" in q
    ):

        return "average_skill_hours"

    # --------------------------------------------------------------
    # Gender
    # --------------------------------------------------------------

    if any(
        phrase in q
        for phrase in [
            "gender distribution",
            "gender breakdown",
            "students by gender",
            "gender of students",
        ]
    ):

        return "gender_distribution"

    # --------------------------------------------------------------
    # Scholarship
    # --------------------------------------------------------------

    if any(
        phrase in q
        for phrase in [
            "scholarship distribution",
            "scholarship breakdown",
            "scholarship status",
            "students with scholarship",
            "scholarship students",
        ]
    ):

        return "scholarship_distribution"

    # --------------------------------------------------------------
    # English
    # --------------------------------------------------------------

    if (
        "english proficiency" in q
        or "english level" in q
        or "english distribution" in q
    ):

        return "english_distribution"

    # --------------------------------------------------------------
    # Relationship
    # --------------------------------------------------------------

    if (
        "relationship status" in q
        or "relationship distribution" in q
    ):

        return "relationship_distribution"

    # --------------------------------------------------------------
    # Living
    # --------------------------------------------------------------

    if (
        "living arrangement" in q
        or "where students live" in q
    ):

        return "living_distribution"

    # --------------------------------------------------------------
    # CGPA ranges
    # --------------------------------------------------------------

    if (
        "cgpa distribution" in q
        or "cgpa ranges" in q
        or "cgpa range" in q
        or "students by cgpa" in q
    ):

        return "cgpa_ranges"

    return None


# ======================================================================
# EXACT RESPONSE
# ======================================================================

def exact_statistical_response(
    question,
    statistics
):
    """
    Generate exact responses using only Python statistics.
    """

    question_type = (
        detect_statistical_question(
            question
        )
    )

    if question_type == "total_students":

        return (
            f"The dataset contains "
            f"**{statistics['total_students']:,} "
            f"students**."
        )

    if question_type == "average_cgpa":

        value = statistics[
            "cgpa"
        ]["average"]

        return (
            f"The average CGPA is "
            f"**{value:.2f}**."
        )

    if question_type == "maximum_cgpa":

        value = statistics[
            "cgpa"
        ]["maximum"]

        return (
            f"The highest recorded CGPA is "
            f"**{value:.2f}**."
        )

    if question_type == "minimum_cgpa":

        value = statistics[
            "cgpa"
        ]["minimum"]

        return (
            f"The lowest recorded CGPA is "
            f"**{value:.2f}**."
        )

    if question_type == "average_age":

        value = statistics[
            "age"
        ]["average"]

        return (
            f"The average student age is "
            f"**{value:.2f} years**."
        )

    if question_type == "average_study_hours":

        value = statistics[
            "study_hours"
        ]["average"]

        return (
            f"Students study an average of "
            f"**{value:.2f} hours per day**."
        )

    if question_type == "average_study_sessions":

        value = statistics[
            "study_sessions"
        ]["average"]

        return (
            f"Students have an average of "
            f"**{value:.2f} study sessions per day**."
        )

    if question_type == "average_social_media":

        value = statistics[
            "social_media_hours"
        ]["average"]

        return (
            f"Students spend an average of "
            f"**{value:.2f} hours per day "
            f"on social media**."
        )

    if question_type == "average_skill_hours":

        value = statistics[
            "skill_development_hours"
        ]["average"]

        return (
            f"Students spend an average of "
            f"**{value:.2f} hours per day "
            f"on skill development**."
        )

    if question_type == "gender_distribution":

        distribution = statistics[
            "gender_distribution"
        ]

        lines = [
            "**Gender Distribution**"
        ]

        for label, count in (
            distribution.items()
        ):

            lines.append(
                f"- {label}: **{count:,} students**"
            )

        return "\n".join(
            lines
        )

    if question_type == "scholarship_distribution":

        distribution = statistics[
            "scholarship_distribution"
        ]

        lines = [
            "**Scholarship Distribution**"
        ]

        for label, count in (
            distribution.items()
        ):

            lines.append(
                f"- {label}: **{count:,} students**"
            )

        return "\n".join(
            lines
        )

    if question_type == "english_distribution":

        distribution = statistics[
            "english_distribution"
        ]

        lines = [
            "**English Proficiency Distribution**"
        ]

        for label, count in (
            distribution.items()
        ):

            lines.append(
                f"- {label}: **{count:,} students**"
            )

        return "\n".join(
            lines
        )

    if question_type == "relationship_distribution":

        distribution = statistics[
            "relationship_distribution"
        ]

        lines = [
            "**Relationship Status Distribution**"
        ]

        for label, count in (
            distribution.items()
        ):

            lines.append(
                f"- {label}: **{count:,} students**"
            )

        return "\n".join(
            lines
        )

    if question_type == "living_distribution":

        distribution = statistics[
            "living_distribution"
        ]

        lines = [
            "**Living Arrangement Distribution**"
        ]

        for label, count in (
            distribution.items()
        ):

            lines.append(
                f"- {label}: **{count:,} students**"
            )

        return "\n".join(
            lines
        )

    if question_type == "cgpa_ranges":

        distribution = statistics[
            "cgpa_ranges"
        ]

        lines = [
            "**CGPA Distribution**"
        ]

        for label, count in (
            distribution.items()
        ):

            lines.append(
                f"- {label}: **{count:,} students**"
            )

        return "\n".join(
            lines
        )

    return None


# ======================================================================
# OLLAMA GENERATION
# ======================================================================

def generate_ai_response(
    question: str,
    conversation: Optional[list] = None
):
    """
    Generate a response using local Ollama.

    Exact statistical questions are answered directly
    by Python first.
    """

    try:

        # ----------------------------------------------------------
        # Load dataset
        # ----------------------------------------------------------

        df = get_dataset()

        validate_dataset_columns(
            df
        )

        # ----------------------------------------------------------
        # Exact statistics
        # ----------------------------------------------------------

        statistics = (
            calculate_exact_statistics(
                df
            )
        )

        # ----------------------------------------------------------
        # Exact-answer shortcut
        # ----------------------------------------------------------

        exact_answer = (
            exact_statistical_response(
                question,
                statistics
            )
        )

        if exact_answer:

            return exact_answer

        # ----------------------------------------------------------
        # Dataset context
        # ----------------------------------------------------------

        dataset_context = (
            build_dataset_context(
                statistics
            )
        )

        # ----------------------------------------------------------
        # Conversation context
        # ----------------------------------------------------------

        conversation_text = ""

        if conversation:

            for message in (
                conversation[-8:]
            ):

                if not isinstance(
                    message,
                    dict
                ):
                    continue

                role = str(
                    message.get(
                        "role",
                        "user"
                    )
                )

                content = str(
                    message.get(
                        "content",
                        ""
                    )
                ).strip()

                if not content:
                    continue

                conversation_text += (
                    f"{role.upper()}: "
                    f"{content}\n"
                )

        # ----------------------------------------------------------
        # Prompt
        # ----------------------------------------------------------

        prompt = f"""
You are the local AI assistant for a university
Student Analytics Dashboard.

You are running completely locally through Ollama.

Model:
{OLLAMA_MODEL}

Your job is to help the user understand the student dataset.

RULES:

1. Use only the supplied dataset context.
2. Never invent a statistic.
3. Never fabricate a number.
4. If the requested exact value is not present in
   the context, clearly say that the exact value
   is not available.
5. You may explain relationships qualitatively,
   but do not claim causation from descriptive data.
6. Keep answers concise and organized.
7. Use bullets when they improve readability.
8. Do not provide medical diagnoses.
9. Do not mention internal implementation details
   unless the user asks.
10. The target dataset is the finalized IUBAT
    student CGPA dataset.

DATASET CONTEXT:

{dataset_context}

CONVERSATION HISTORY:

{conversation_text}

USER QUESTION:

{question}

Answer clearly and professionally.
"""

        # ----------------------------------------------------------
        # Ollama request
        # ----------------------------------------------------------

        response = requests.post(

            OLLAMA_URL,

            json={

                "model":
                    OLLAMA_MODEL,

                "prompt":
                    prompt,

                "stream":
                    False,

                "options": {

                    "temperature":
                        0.1,

                    "top_p":
                        0.9,

                },

            },

            timeout=120,
        )

        response.raise_for_status()

        payload = response.json()

        answer = str(
            payload.get(
                "response",
                ""
            )
        ).strip()

        if not answer:

            return (
                "The local AI model returned "
                "an empty response."
            )

        return answer

    # ------------------------------------------------------------------
    # Connection
    # ------------------------------------------------------------------

    except requests.exceptions.ConnectionError:

        return (
            "I could not connect to the local Ollama server. "
            "Please make sure Ollama is running."
        )

    # ------------------------------------------------------------------
    # Timeout
    # ------------------------------------------------------------------

    except requests.exceptions.Timeout:

        return (
            "The local AI model took too long to respond. "
            "Please try again."
        )

    # ------------------------------------------------------------------
    # HTTP
    # ------------------------------------------------------------------

    except requests.exceptions.HTTPError as error:

        print(
            f"[OLLAMA HTTP ERROR] {error}"
        )

        return (
            "The local Ollama server returned an error. "
            "Please check the installed model and Ollama status."
        )

    # ------------------------------------------------------------------
    # Dataset / code
    # ------------------------------------------------------------------

    except FileNotFoundError as error:

        print(
            f"[DATASET ERROR] {error}"
        )

        return (
            "The cleaned student dataset could not be found."
        )

    except Exception as error:

        print(
            f"[CHATBOT ERROR] {error}"
        )

        # During development, print the real error.
        # The API can still return a user-friendly response.
        return (
            "The chatbot could not process the question "
            "right now."
        )


# ======================================================================
# MAIN CHAT FUNCTION
# ======================================================================

def chat_with_ai(
    question: str,
    conversation: Optional[list] = None
):
    """
    Main function used by FastAPI.
    """

    if (
        not question
        or not question.strip()
    ):

        return {
            "success":
                False,

            "response":
                "Please enter a question.",
        }

    answer = generate_ai_response(
        question=question.strip(),
        conversation=conversation,
    )

    return {
        "success":
            True,

        "response":
            answer,
    }


# ======================================================================
# LOCAL TEST
# ======================================================================

if __name__ == "__main__":

    print()
    print("=" * 70)
    print(
        "LOCAL OLLAMA CHATBOT TEST"
    )
    print("=" * 70)

    print()
    print(
        f"Dataset: {DATASET_PATH}"
    )

    print(
        f"Ollama : {OLLAMA_URL}"
    )

    print(
        f"Model  : {OLLAMA_MODEL}"
    )

    print()
    print(
        "Testing exact dataset question..."
    )

    result = chat_with_ai(
        "What is the average CGPA in the dataset?"
    )

    print()
    print(
        result
    )

    print()
    print(
        "Testing general dataset question..."
    )

    result = chat_with_ai(
        "What kind of information is available "
        "about the students in this dataset?"
    )

    print()
    print(
        result
    )

    print()
    print("=" * 70)
    print(
        "CHATBOT TEST COMPLETE"
    )
    print("=" * 70)