# regex extraction logic
import pandas as pd
import re
import os

os.makedirs("results", exist_ok=True)

df = pd.read_csv("results/raw_furniture_listings.csv")

def clean_price(x):
    if pd.isna(x):
        return None
    return int(re.sub(r"[^\d]", "", str(x))) if re.sub(r"[^\d]", "", str(x)) else None

df["price"] = df["price_raw"].apply(clean_price)

df.to_csv("results/regex_features.csv", index=False)

print("regex_features.csv created")
