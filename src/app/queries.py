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

        f.home_score AS home_score,
        f.away_score AS away_score,

        d.full_date AS full_date

    FROM fact_games f

    JOIN dim_teams ht 
        ON f.home_team_id = ht.id

    JOIN dim_teams at 
        ON f.away_team_id = at.id
    
    JOIN dim_date d
        ON f.date_id = d.date_id

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
        fps.turnovers,
        fps.minutes_seconds / 60.0 AS minutes_played,
        fps.plus_minus_points,
        CASE WHEN fps.field_goals_attempted > 0 
             THEN fps.field_goals_made * 1.0 / fps.field_goals_attempted 
             ELSE NULL END AS field_goal_percentage,
        CASE WHEN fps.three_pointers_attempted > 0 
             THEN fps.three_pointers_made * 1.0 / fps.three_pointers_attempted 
             ELSE NULL END AS three_point_percentage,
        CASE WHEN fps.free_throws_attempted > 0 
             THEN fps.free_throws_made * 1.0 / fps.free_throws_attempted 
             ELSE NULL END AS free_throw_percentage,
        dp.full_name AS player_name
    FROM fact_games f
    JOIN fact_players_stats fps 
        ON f.game_id = fps.game_id
    JOIN dim_players dp 
        ON fps.player_id = dp.id
    """
    return pd.read_sql(query, engine)