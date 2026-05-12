import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

DB_PATH = "/Users/jeffreyshin/nba_analysis.db"
sns.set_theme(style="darkgrid")

# Load team data
conn = sqlite3.connect(DB_PATH)
teams = pd.read_sql("SELECT * FROM team_win_stats", conn)
conn.close()

# Features and target
features = ["PTS", "AST", "REB", "TOV", "FG_PCT", "FG3_PCT", "PLUS_MINUS"]
X = teams[features]
y = teams["W"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print("=" * 40)
print("MODEL RESULTS")
print("=" * 40)
print(f"R² Score:  {r2:.3f}  (1.0 = perfect)")
print(f"RMSE:      {rmse:.1f} wins")
print()

# Feature importance
print("FEATURE IMPORTANCE (coefficient)")
print("-" * 40)
coef_df = pd.DataFrame({
    "Feature": features,
    "Coefficient": model.coef_
}).sort_values("Coefficient", ascending=False)
print(coef_df.to_string(index=False))
print()

# Predict all teams
teams["PREDICTED_W"] = model.predict(X).round(1)
teams["DIFF"] = (teams["PREDICTED_W"] - teams["W"]).round(1)
print("ACTUAL vs PREDICTED WINS")
print("-" * 40)
print(teams[["TEAM_NAME", "W", "PREDICTED_W", "DIFF"]].sort_values("W", ascending=False).to_string(index=False))

# Chart 1 - Actual vs Predicted
fig, ax = plt.subplots(figsize=(9, 6))
ax.scatter(y_test, y_pred, color="steelblue", s=100, edgecolor="white")
ax.plot([y.min(), y.max()], [y.min(), y.max()], "r--", linewidth=1.5, label="Perfect Prediction")
ax.set_xlabel("Actual Wins")
ax.set_ylabel("Predicted Wins")
ax.set_title(f"Actual vs Predicted Wins (R² = {r2:.3f})", fontsize=14)
ax.legend()
plt.tight_layout()
plt.savefig("/Users/jeffreyshin/chart6_actual_vs_predicted.png")
print("\nSaved chart6_actual_vs_predicted.png")

# Chart 2 - Feature coefficients
fig, ax = plt.subplots(figsize=(9, 6))
colors = ["steelblue" if c > 0 else "tomato" for c in coef_df["Coefficient"]]
ax.barh(coef_df["Feature"], coef_df["Coefficient"], color=colors)
ax.axvline(0, color="black", linewidth=0.8)
ax.set_xlabel("Coefficient (impact on wins)")
ax.set_title("Which Stats Drive Wins? — Linear Regression Coefficients", fontsize=13)
plt.tight_layout()
plt.savefig("/Users/jeffreyshin/chart7_feature_importance.png")
print("Saved chart7_feature_importance.png")

plt.show()
print("\nDone! Check chart6 and chart7 in your home folder.")
