import pandas as pd

df = pd.read_csv("dataset/dataset.csv")

print("=" * 50)
print("TARGET COLUMN")

print(df["6. Current CGPA"].unique())

print("=" * 50)

print(df["6. Current CGPA"].value_counts())