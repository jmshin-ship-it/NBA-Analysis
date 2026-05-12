# 🏀 NBA Player Performance & Team Success Analysis

A data analysis project exploring which NBA player and team stats most strongly correlate with winning, using real NBA API data, SQL, Python, and machine learning.

## 📊 Key Findings
- **Plus/Minus** has a 0.98 correlation with wins — the strongest predictor
- **Turnovers** hurt teams the most (-0.68 correlation with wins)
- **FG%** is the biggest positive driver of wins in the regression model
- OKC Thunder dominated the 2024-25 season with 4 players in the top 15 Plus/Minus list
- Linear regression model achieved **R² = 0.916** predicting team wins

## 📁 Project Structure
| File | Description |
|---|---|
| `step1_fetch_data.py` | Fetches NBA API data, saves to SQLite database |
| `step2_queries.sql` | SQL queries for team and player analysis |
| `step3_analysis.py` | Generates 5 data visualizations |
| `step4_regression.py` | Linear regression model to predict team wins |
| `nba_analysis.db` | SQLite database with team and player stats |

## 📈 Charts
- **Chart 1** — Correlation heatmap of team stats vs wins
- **Chart 2** — Point differential vs win percentage (all 30 teams)
- **Chart 3** — Top 10 vs Bottom 10 teams stat comparison
- **Chart 4** — Top 15 players by Plus/Minus
- **Chart 5** — Scoring efficiency bubble chart (PTS vs TOV)
- **Chart 6** — Actual vs Predicted wins (regression model)
- **Chart 7** — Feature importance from linear regression

## 🛠️ Tools & Libraries
- Python, SQL, SQLite
- nba_api, pandas, matplotlib, seaborn, scikit-learn

## 🚀 How to Run
```bash
# Install dependencies
pip install nba_api pandas matplotlib seaborn scikit-learn

# Fetch data and create database
python step1_fetch_data.py

# Generate visualizations
python step3_analysis.py

# Run regression model
python step4_regression.py
```

## 📅 Data
2024-25 NBA Regular Season via the official NBA Stats API
