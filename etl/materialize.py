# combine all data into final dataset
import pandas as pd
import os

os.makedirs("results", exist_ok=True)

df = pd.read_csv("results/llm_features.csv")

df = df.dropna(subset=["price"])

df.to_csv("results/furniture_master.csv", index=False)

print("furniture_master.csv created")
