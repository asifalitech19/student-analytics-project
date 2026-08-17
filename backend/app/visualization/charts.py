import pandas as pd

from app.ml.data_loader import load_dataset


# ==========================================================
# Generic Distribution Function
# ==========================================================

def get_distribution(column_name, label_name):
    """
    Returns frequency distribution for a dataset column.
    """

    df = load_dataset()

    data = (
        df[column_name]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
        .value_counts()
        .reset_index()
    )

    data.columns = [label_name, "Count"]

    return data.to_dict(orient="records")


# ==========================================================
# Gender Distribution
# ==========================================================

def gender_distribution():
    return get_distribution(
        "2. Gender",
        "Gender"
    )


# ==========================================================
# Age Distribution
# ==========================================================

def age_distribution():
    return get_distribution(
        "1. Age",
        "Age"
    )


# ==========================================================
# University Distribution
# ==========================================================

def university_distribution():
    return get_distribution(
        "3. University",
        "University"
    )


# ==========================================================
# Department Distribution
# ==========================================================

def department_distribution():
    return get_distribution(
        "4. Department",
        "Department"
    )


# ==========================================================
# Academic Year Distribution
# ==========================================================

# def academic_year_distribution():
    return get_distribution(
        "5. Academic Year",
        "Academic Year"
    )
# ==========================================================
# Academic Year Distribution
# ==========================================================

def academic_year_distribution():
    """
    Returns academic year distribution in a fixed order
    for dashboard visualization.
    """

    df = load_dataset()

    column = "5. Academic Year"

    academic_year = (
        df[column]
        .fillna("Other")
        .astype(str)
        .str.strip()
    )

    # Fixed order for dashboard presentation
    order = [
        "First Year or Equivalent",
        "Second Year or Equivalent",
        "Third Year or Equivalent",
        "Fourth Year or Equivalent",
        "Other",
    ]

    counts = academic_year.value_counts()

    result = []

    for category in order:
        result.append({
            "Academic Year": category,
            "Count": int(counts.get(category, 0))
        })

    return result

# ==========================================================
# Scholarship Distribution
# ==========================================================

def scholarship_distribution():
    return get_distribution(
        "7. Did you receive a waiver or scholarship at your university?",
        "Scholarship"
    )


# ==========================================================
# CGPA Distribution
# ==========================================================

# def cgpa_distribution():
    """
    Converts CGPA values into meaningful academic performance bands.
    """

    df = load_dataset()

    column = "6. Current CGPA"

    # Convert values to numeric.
    # Invalid values such as "Other" become NaN.
    cgpa = pd.to_numeric(
        df[column],
        errors="coerce"
    )

    # ------------------------------------------------------
    # CGPA Categorization
    # ------------------------------------------------------

    def categorize(value):

        if pd.isna(value):
            return "Other / Not Available"

        elif value < 2.0:
            return "Below 2.0"

        elif value < 2.5:
            return "2.0 - 2.49"

        elif value < 3.0:
            return "2.5 - 2.99"

        elif value < 3.5:
            return "3.0 - 3.49"

        elif value < 4.0:
            return "3.5 - 3.99"

        elif value == 4.0:
            return "4.0"

        else:
            return "Other / Not Available"

    categories = cgpa.apply(categorize)

    # ------------------------------------------------------
    # Fixed order for professional dashboard presentation
    # ------------------------------------------------------

    order = [
        "Below 2.0",
        "2.0 - 2.49",
        "2.5 - 2.99",
        "3.0 - 3.49",
        "3.5 - 3.99",
        "4.0",
        "Other / Not Available",
    ]

    counts = categories.value_counts()

    result = []

    for category in order:

        result.append(
            {
                "CGPA": category,
                "Count": int(
                    counts.get(category, 0)
                )
            }
        )

    return result

# ==========================================================
# CGPA Distribution
# ==========================================================

def cgpa_distribution():
    """
    Returns the existing CGPA categories from the dataset
    in a fixed academic-performance order.
    """

    df = load_dataset()

    column = "6. Current CGPA"

    # Clean CGPA values
    cgpa = (
        df[column]
        .fillna("Other")
        .astype(str)
        .str.strip()
    )

    # Fixed order for professional dashboard presentation
    order = [
        "Below 2.50",
        "2.50 - 2.99",
        "3.00 - 3.39",
        "3.40 - 3.79",
        "3.80 - 4.00",
        "Other",
    ]

    counts = cgpa.value_counts()

    result = []

    for category in order:
        result.append({
            "CGPA": category,
            "Count": int(counts.get(category, 0))
        })

    return result
# ==========================================================
# Anxiety Label Distribution
# ==========================================================

def anxiety_label_distribution():
    return get_distribution(
        "Anxiety Label",
        "Anxiety"
    )


# ==========================================================
# Stress Label Distribution
# ==========================================================

def stress_label_distribution():
    return get_distribution(
        "Stress Label",
        "Stress"
    )


# ==========================================================
# Depression Label Distribution
# ==========================================================

def depression_label_distribution():
    return get_distribution(
        "Depression Label",
        "Depression"
    )


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    print("\n" + "=" * 60)
    print("GENDER DISTRIBUTION")
    print("=" * 60)

    print(gender_distribution())


    print("\n" + "=" * 60)
    print("AGE DISTRIBUTION")
    print("=" * 60)

    print(age_distribution())


    print("\n" + "=" * 60)
    print("UNIVERSITY DISTRIBUTION")
    print("=" * 60)

    print(university_distribution())


    print("\n" + "=" * 60)
    print("DEPARTMENT DISTRIBUTION")
    print("=" * 60)

    print(department_distribution())


    print("\n" + "=" * 60)
    print("ACADEMIC YEAR DISTRIBUTION")
    print("=" * 60)

    print(academic_year_distribution())


    print("\n" + "=" * 60)
    print("SCHOLARSHIP DISTRIBUTION")
    print("=" * 60)

    print(scholarship_distribution())


    print("\n" + "=" * 60)
    print("CGPA DISTRIBUTION")
    print("=" * 60)

    print(cgpa_distribution())


    print("\n" + "=" * 60)
    print("ANXIETY DISTRIBUTION")
    print("=" * 60)

    print(anxiety_label_distribution())


    print("\n" + "=" * 60)
    print("STRESS DISTRIBUTION")
    print("=" * 60)

    print(stress_label_distribution())


    print("\n" + "=" * 60)
    print("DEPRESSION DISTRIBUTION")
    print("=" * 60)

    print(depression_label_distribution())


    