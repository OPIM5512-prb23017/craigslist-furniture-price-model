# llm extraction logic
import pandas as pd
import os

os.makedirs("results", exist_ok=True)

df = pd.read_csv("results/regex_features.csv")

df["color"] = None
df["condition"] = None

df.to_csv("results/llm_features.csv", index=False)

print("llm_features.csv created")
