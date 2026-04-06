# model training logic
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import os

os.makedirs("results/predictions", exist_ok=True)
os.makedirs("results/metrics_history", exist_ok=True)

df = pd.read_csv("results/furniture_master.csv")

df = df.dropna()

if len(df) < 5:
    print("Not enough data")
    exit()

X = pd.get_dummies(df.drop(columns=["price"]))
y = df["price"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestRegressor()
model.fit(X_train, y_train)

preds = model.predict(X_test)

pd.DataFrame({"actual": y_test, "pred": preds}).to_csv("results/predictions/preds.csv", index=False)

print("model trained and predictions saved")
