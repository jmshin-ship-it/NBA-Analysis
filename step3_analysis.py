import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

DB_PATH = "/Users/jeffreyshin/nba_analysis.db"
sns.set_theme(style="darkgrid")
plt.rcParams["figure.dpi"] = 130

conn    = sqlite3.connect(DB_PATH)
teams   = pd.read_sql("SELECT * FROM team_win_stats", conn)
players = pd.read_sql("SELECT * FROM players", conn)
conn.close()

stat_cols = ["W", "PTS", "AST", "REB", "TOV", "FG_PCT", "FG3_PCT", "PLUS_MINUS"]
corr = teams[stat_cols].corr()
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, square=True, linewidths=0.5, ax=ax)
ax.set_title("Correlation Heatmap", fontsize=14)
plt.tight_layout()
plt.savefig("/Users/jeffreyshin/chart1.png")
print("Saved chart1")

fig, ax = plt.subplots(figsize=(9, 6))
sns.scatterplot(data=teams, x="PLUS_MINUS", y="W_PCT", s=100, color="steelblue", ax=ax)
for _, row in teams.iterrows():
    ax.annotate(row["TEAM_NAME"].split()[-1], (row["PLUS_MINUS"], row["W_PCT"]), fontsize=7)
m, b = np.polyfit(teams["PLUS_MINUS"], teams["W_PCT"], 1)
x_line = np.linspace(teams["PLUS_MINUS"].min(), teams["PLUS_MINUS"].max(), 100)
ax.plot(x_line, m * x_line + b, color="tomato", linestyle="--")
ax.set_title("Plus/Minus vs Win Pct", fontsize=14)
plt.tight_layout()
plt.savefig("/Users/jeffreyshin/chart2.png")
print("Saved chart2")

top10 = teams.nlargest(10, "W")
bottom10 = teams.nsmallest(10, "W")
compare_stats = ["PTS", "AST", "TOV", "FG_PCT", "FG3_PCT"]
compare_labels = ["Points/G", "Assists/G", "Turnovers/G", "FG%", "3P%"]
top_means = [top10[s].mean() for s in compare_stats]
bottom_means = [bottom10[s].mean() for s in compare_stats]
x = np.arange(len(compare_stats))
fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - 0.175, top_means, 0.35, label="Top 10", color="steelblue")
bars2 = ax.bar(x + 0.175, bottom_means, 0.35, label="Bottom 10", color="tomato")
ax.set_xticks(x)
ax.set_xticklabels(compare_labels)
ax.set_title("Top 10 vs Bottom 10 Teams", fontsize=14)
ax.legend()
plt.tight_layout()
plt.savefig("/Users/jeffreyshin/chart3.png")
print("Saved chart3")

qualified = players[players["GP"] >= 40].copy()
top_pm = qualified.nlargest(15, "PLUS_MINUS")
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(top_pm["PLAYER_NAME"] + " (" + top_pm["TEAM_ABBREVIATION"] + ")", top_pm["PLUS_MINUS"], color="steelblue")
ax.set_title("Top 15 Players by Plus/Minus", fontsize=14)
ax.invert_yaxis()
plt.tight_layout()
plt.savefig("/Users/jeffreyshin/chart4.png")
print("Saved chart4")

efficient = qualified[qualified["PTS"] >= 12].copy()
fig, ax = plt.subplots(figsize=(10, 7))
scatter = ax.scatter(efficient["TOV"], efficient["PTS"], s=efficient["GP"] * 3, c=efficient["PLUS_MINUS"], cmap="RdYlGn", alpha=0.75)
plt.colorbar(scatter, ax=ax, label="Plus/Minus")
ax.set_xlabel("Turnovers per Game")
ax.set_ylabel("Points per Game")
ax.set_title("Scoring Efficiency", fontsize=13)
plt.tight_layout()
plt.savefig("/Users/jeffreyshin/chart5.png")
print("Saved chart5")

print("All done! Charts saved to your home folder.")
