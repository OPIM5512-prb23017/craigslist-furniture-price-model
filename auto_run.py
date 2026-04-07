import os
from datetime import datetime

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.inspection import permutation_importance, PartialDependenceDisplay

RESULTS_DIR = "results"

os.makedirs(f"{RESULTS_DIR}/metrics_history", exist_ok=True)
os.makedirs(f"{RESULTS_DIR}/importance", exist_ok=True)
os.makedirs(f"{RESULTS_DIR}/pdp", exist_ok=True)
os.makedirs(f"{RESULTS_DIR}/predictions", exist_ok=True)

df = pd.read_csv(f"{RESULTS_DIR}/furniture_master.csv")
df["price"] = df["price_raw"].replace(r"[\$,]", "", regex=True).astype(float)
df = df.dropna(subset=["price"]).fillna("unknown")

df["title_len"] = df["title"].astype(str).str.len()
df["location_len"] = df["location_raw"].astype(str).str.len()

X = df[["title_len", "location_len"]]
y = df["price"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=None)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
run_id = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

pd.DataFrame({
    "run_id": [run_id],
    "MAE": [mae],
    "RMSE": [rmse]
}).to_csv(f"{RESULTS_DIR}/metrics_history/{run_id}.csv", index=False)

pd.DataFrame({
    "actual": y_test.values,
    "predicted": y_pred
}).to_csv(f"{RESULTS_DIR}/predictions/{run_id}-preds.csv", index=False)

perm = permutation_importance(model, X_test, y_test, n_repeats=5, random_state=42)
imp_df = pd.DataFrame({
    "feature": X.columns,
    "importance": perm.importances_mean
}).sort_values("importance", ascending=False)

imp_df.to_csv(f"{RESULTS_DIR}/importance/{run_id}-importance.csv", index=False)

plt.figure(figsize=(6, 4))
plt.barh(imp_df["feature"], imp_df["importance"])
plt.gca().invert_yaxis()
plt.title("Feature Importance")
plt.tight_layout()
plt.savefig(f"{RESULTS_DIR}/importance/{run_id}-importance.png")
plt.close()

fig, ax = plt.subplots(figsize=(8, 4))
PartialDependenceDisplay.from_estimator(model, X_test, [0, 1], ax=ax)
plt.tight_layout()
plt.savefig(f"{RESULTS_DIR}/pdp/{run_id}-pdp.png")
plt.close()

print(f"Completed run {run_id}")
