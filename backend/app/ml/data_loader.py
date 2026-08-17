import pandas as pd
from app.core.config import DATASET_PATH


def load_dataset():
    """
    Load the student dataset.
    """

    try:
        df = pd.read_csv(DATASET_PATH)

        print("=" * 60)
        print("Dataset Loaded Successfully")
        print(f"Rows    : {df.shape[0]}")
        print(f"Columns : {df.shape[1]}")
        print("=" * 60)

        return df

    except Exception as e:
        print(f"Error Loading Dataset : {e}")
        return None


if __name__ == "__main__":

    df = load_dataset()

    if df is not None:
        print(df.head())