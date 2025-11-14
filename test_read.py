import pandas as pd

df = pd.read_csv("data/gigasvaer_sales.csv", sep=";")

print("Antall rader i datasettet:", len(df))
print(df.head())
