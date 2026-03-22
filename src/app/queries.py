from turtle import st

import pandas as pd
import sys
import streamlit as st
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.db import get_engine

engine = get_engine()


@st.cache_data
def get_games():
    query = """
    SELECT 
        f.game_id,
        f.date_id,

        ht.full_name AS home_team_name,
        at.full_name AS away_team_name,

        f.home_team_id,
        f.away_team_id,

        f.home_score,
        f.away_score

    FROM fact_games f

    JOIN dim_teams ht 
        ON f.home_team_id = ht.id

    JOIN dim_teams at 
        ON f.away_team_id = at.id

    ORDER BY f.date_id DESC;
    """
    return pd.read_sql(query, engine)


@st.cache_data
def load_player_stats():
    engine = get_engine()
    query = """
    SELECT 
        f.game_id,
        f.home_team_id,
        f.away_team_id,
        fps.player_id,
        fps.team_id,
        fps.points,
        fps.rebounds_offensive AS offensive_rebounds,
        fps.rebounds_defensive AS defensive_rebounds,
        fps.assists,
        fps.steals,
        fps.blocks,
        dp.full_name AS player_name
    FROM fact_games f
    JOIN fact_players_stats fps 
        ON f.game_id = fps.game_id
    JOIN dim_players dp 
        ON fps.player_id = dp.id
    """
    return pd.read_sql(query, engine)