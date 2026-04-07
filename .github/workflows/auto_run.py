import pandas as pd
import numpy as np
import os
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.inspection import permutation_importance
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("results/furniture_master.csv")

# Clean
df["price"] = df["price_raw"].replace(r'[\$,]', '', regex=True).astype(float)

df["title_len"] = df["title"].astype(str).apply(len)
df["location_len"] = df["location_raw"].astype(str).apply(len)

X = df[["title_len", "location_len"]]
y = df["price"]

# Train
X_train, X_test, y_train, y_test = train_test_split(X, y)

model = RandomForestRegressor()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

# Metrics
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mae = mean_absolute_error(y_test, y_pred)

run_id = datetime.now().strftime("%Y%m%d%H%M%S")

os.makedirs("results/metrics_history", exist_ok=True)
os.makedirs("results/importance", exist_ok=True)
os.makedirs("results/pdp", exist_ok=True)

# Save metrics
pd.DataFrame({
    "run_id": [run_id],
    "RMSE": [rmse],
    "MAE": [mae]
}).to_csv(f"results/metrics_history/{run_id}.csv", index=False)

# Importance
perm = permutation_importance(model, X_test, y_test)

imp_df = pd.DataFrame({
    "feature": X.columns,
    "importance": perm.importances_mean
}).sort_values("importance", ascending=False)

imp_df.to_csv(f"results/importance/{run_id}.csv", index=False)

plt.figure()
plt.barh(imp_df["feature"], imp_df["importance"])
plt.gca().invert_yaxis()
plt.savefig(f"results/importance/{run_id}.png")

print("Run complete")
