from sqlalchemy import Engine, create_engine
import json
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import re
from utils import PLAYERS_STATS_PATH

def minutes_to_seconds(series: pd.Series) -> pd.Series:
    def parse(x):
        try:
            if pd.isna(x):
                return 0
            m, s = str(x).strip().split(":")
            return int(m) * 60 + int(s)
        except:
            return 0  # handles DNP, '', bad values, etc.

    return series.apply(parse).astype("int32")

def minutes_to_float(series: pd.Series) -> pd.Series:
    def parse(x):
        try:
            if pd.isna(x):
                return 0.0
            m, s = str(x).strip().split(":")
            return int(m) + int(s) / 60
        except:
            return 0.0  # handles DNP, '', bad values

    return series.apply(parse).astype("float32")


def to_snake_case(name: str) -> str:
    # Add underscore before capital letters (except first), then lowercase
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
    return s2.lower()


def clean_players_stats(engine: Engine, yesterday: datetime):
    """
    Reads the raw games data from the JSON file, processes it to identify home and away teams, and then merges the data to create a clean DataFrame. Finally, it writes the cleaned data to a staging table in the database.
    """
    try:
        with open(f"{PLAYERS_STATS_PATH}/{yesterday.year}/{yesterday.month}/{yesterday.day}_player_stats.json") as f:
                data = json.load(f)
    except FileNotFoundError:
        print("No player stats data available for the specified date.")
        return []


    df_game_stats = pd.DataFrame(data)

    df_stats = df_game_stats['statistics'].apply(pd.Series)
    df_game_stats = pd.concat([df_game_stats, df_stats], axis=1)
    
    df_game_stats.columns = [to_snake_case(col) for col in df_game_stats.columns]

    df_game_stats["minutes_seconds"] = minutes_to_seconds(df_game_stats["minutes"])
    df_game_stats["minutes_float"] = minutes_to_float(df_game_stats["minutes"])

    df_game_stats = df_game_stats.astype({col: "int32" for col in df_game_stats.select_dtypes(include="int64").columns})
    df_game_stats['game_id'] = pd.to_numeric(df_game_stats['game_id']).astype(np.int32)

    df_game_stats = df_game_stats.drop(columns=["minutes"])
    df_game_stats = df_game_stats.rename(columns={"person_id": "player_id"})
        
    df_game_stats = df_game_stats.drop(columns=['free_throws_percentage', 'three_pointers_percentage', "field_goals_percentage", 'statistics', 'jersey_num', 'comment', 'position', 'player_slug', 'name_i', 'family_name', 'first_name'])

    df_game_stats.to_sql("fact_players_stats", con=engine, if_exists="append", index=False)

