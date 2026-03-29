from sqlalchemy import create_engine, text
from utils import SQLITE_URL

engine = create_engine(SQLITE_URL)

with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS fact_games (
            game_id INTEGER PRIMARY KEY,
            date_id INTEGER,
            home_team_id INTEGER,
            away_team_id INTEGER,
            home_score INTEGER,
            away_score INTEGER
        );
    """))
    
    conn.execute(text("""
        CREATE TABLE fact_players_stats (
            player_id INTEGER,
            game_id INTEGER,
            team_id INTEGER,
            field_goals_made INTEGER,
            field_goals_attempted INTEGER,
            three_pointers_made INTEGER,
            three_pointers_attempted INTEGER,
            free_throws_made INTEGER,
            free_throws_attempted INTEGER,
            rebounds_offensive INTEGER,
            rebounds_defensive INTEGER,
            rebounds_total INTEGER,
            assists INTEGER,
            steals INTEGER,
            blocks INTEGER,
            turnovers INTEGER,
            fouls_personal INTEGER,
            points INTEGER,
            plus_minus_points REAL,
            minutes_seconds INTEGER,
            minutes_float INTEGER,
            PRIMARY KEY (game_id, player_id)
        );
    """))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS dim_date (
            date_id TEXT PRIMARY KEY,
            year INTEGER,
            month INTEGER,
            day INTEGER,
            month_name TEXT,
            day_name TEXT
        );
    """))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS dim_players (
            id INTEGER PRIMARY KEY,
            full_name TEXT,
            first_name TEXT,
            last_name TEXT,
            position TEXT,
            team_id INTEGER
            height INTEGER,
            weight INTEGER,
            is_active BOOLEAN
        );
    """))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS dim_teams (
            id INTEGER PRIMARY KEY,
            full_name TEXT,
            abbreviation TEXT,
            nickname TEXT,
            city TEXT,
            state TEXT,
            year_founded INTEGER
        );
    """))