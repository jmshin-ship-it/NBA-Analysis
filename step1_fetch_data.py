# ============================================================
# NBA Player Performance & Team Success Analysis
# STEP 1: Fetch Data & Load into SQLite Database
# ============================================================

import pandas as pd
import sqlite3
import time
from nba_api.stats.endpoints import leaguedashteamstats, leaguedashplayerstats

# ── Config ──────────────────────────────────────────────────
SEASON = "2024-25"       # Change to current season if needed
DB_PATH = "/Users/jeffreyshin/nba_analysis.db"
# ────────────────────────────────────────────────────────────


def fetch_team_stats(season: str) -> pd.DataFrame:
    """Fetch per-team stats for a given season."""
    print(f"Fetching team stats for {season}...")
    endpoint = leaguedashteamstats.LeagueDashTeamStats(
        season=season,
        per_mode_detailed="PerGame",
        measure_type_detailed_defense="Base",
    )
    df = endpoint.get_data_frames()[0]

    # Keep only the columns we care about
    cols = [
        "TEAM_ID", "TEAM_NAME",
        "GP", "W", "L", "W_PCT",
        "PTS", "AST", "REB", "TOV",
        "FG_PCT", "FG3_PCT", "FT_PCT",
        "PLUS_MINUS",
    ]
    return df[cols].copy()


def fetch_player_stats(season: str) -> pd.DataFrame:
    """Fetch per-player stats for a given season."""
    print(f"Fetching player stats for {season}...")
    time.sleep(1)   # be polite to the NBA API
    endpoint = leaguedashplayerstats.LeagueDashPlayerStats(
        season=season,
        per_mode_detailed="PerGame",
        measure_type_detailed_defense="Base",
    )
    df = endpoint.get_data_frames()[0]

    cols = [
        "PLAYER_ID", "PLAYER_NAME", "TEAM_ID", "TEAM_ABBREVIATION",
        "GP", "PTS", "AST", "REB", "STL", "BLK", "TOV",
        "FG_PCT", "FG3_PCT", "FT_PCT",
        "PLUS_MINUS",
    ]
    return df[cols].copy()


def save_to_sqlite(team_df: pd.DataFrame, player_df: pd.DataFrame, db_path: str):
    """Save DataFrames to SQLite tables."""
    print(f"Saving to {db_path}...")
    conn = sqlite3.connect(db_path)

    team_df.to_sql("teams", conn, if_exists="replace", index=False)
    player_df.to_sql("players", conn, if_exists="replace", index=False)

    # ── Useful views ─────────────────────────────────────────
    conn.execute("DROP VIEW IF EXISTS top_scorers")
    conn.execute("""
        CREATE VIEW top_scorers AS
        SELECT PLAYER_NAME, TEAM_ABBREVIATION, PTS, AST, REB, PLUS_MINUS
        FROM players
        ORDER BY PTS DESC
        LIMIT 20
    """)

    conn.execute("DROP VIEW IF EXISTS team_win_stats")
    conn.execute("""
        CREATE VIEW team_win_stats AS
        SELECT TEAM_NAME, W, L, W_PCT,
               PTS, AST, REB, TOV,
               FG_PCT, FG3_PCT, PLUS_MINUS
        FROM teams
        ORDER BY W DESC
    """)

    conn.commit()
    conn.close()
    print("Done! Tables created: 'teams', 'players'")
    print("Views created:  'top_scorers', 'team_win_stats'")


def preview(db_path: str):
    """Quick sanity-check — print first few rows of each table."""
    conn = sqlite3.connect(db_path)
    print("\n── Team Stats (first 5 rows) ──────────────────────")
    print(pd.read_sql("SELECT * FROM team_win_stats LIMIT 5", conn).to_string(index=False))

    print("\n── Top Scorers (first 5 rows) ─────────────────────")
    print(pd.read_sql("SELECT * FROM top_scorers LIMIT 5", conn).to_string(index=False))
    conn.close()


# ── Main ─────────────────────────────────────────────────────
if __name__ == "__main__":
    team_df   = fetch_team_stats(SEASON)
    player_df = fetch_player_stats(SEASON)
    save_to_sqlite(team_df, player_df, DB_PATH)
    preview(DB_PATH)
    print(f"\nAll done! Open '{DB_PATH}' with DB Browser or continue to step2_analysis.py")