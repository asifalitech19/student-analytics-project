import pandas as pd

# Dataset load
df = pd.read_csv("dataset/dataset.csv")

print("=" * 50)
print("Dataset Shape")
print(df.shape)

print("=" * 50)
print("Columns")
print(df.columns)

print("=" * 50)
print("First 5 Rows")
print(df.head())

print("=" * 50)
print("Missing Values")
print(df.isnull().sum())

print("=" * 50)
print("Data Types")
print(df.dtypes)

print("=" * 50)
print("Statistics")
print(df.describe(include="all"))
