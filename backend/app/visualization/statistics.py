from app.ml.data_loader import load_dataset


# ==========================================================
# Dashboard Statistics
# ==========================================================

def dashboard_statistics():
    """
    Returns summary statistics for Dashboard KPI Cards.
    """

    df = load_dataset()

    return {
        "total_students": len(df),
        "total_columns": len(df.columns),
        "total_universities": df["3. University"].nunique(),
        "total_departments": df["4. Department"].nunique(),
        "total_genders": df["2. Gender"].nunique(),
        "average_anxiety": round(df["Anxiety Value"].mean(), 2),
        "average_stress": round(df["Stress Value"].mean(), 2),
        "average_depression": round(df["Depression Value"].mean(), 2),
    }


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    stats = dashboard_statistics()

    print("=" * 60)
    print("DASHBOARD STATISTICS")
    print("=" * 60)

    for key, value in stats.items():
        print(f"{key:25}: {value}")

    print("\n" + "=" * 60)
    print("UNIVERSITIES")
    print("=" * 60)

    df = load_dataset()

    universities = sorted(df["3. University"].dropna().unique())

    print(f"Total Universities: {len(universities)}\n")

    for i, university in enumerate(universities, start=1):
        print(f"{i}. {university}")