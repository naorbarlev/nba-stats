from sqlalchemy import Engine
import json
import pandas as pd
from datetime import datetime
import numpy as np
from utils import GAMES_PATH, PLAYERS_STATS_PATH, TEAMS_PATH, PLAYERS_PATH
import re


WEIGHT_CONVERSION_FACTOR = 0.45359237


def to_snake_case(name: str) -> str:
    # Add underscore before capital letters (except first), then lowercase
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
    return s2.lower()


def convert_height_str_to_cm(height_str):
    """
    Converts height string in "feet-inches\"" format to centimeters.
    """
    match = re.match(r"(\d+)-(\d+)\"?", height_str)
    if match:
        feet = int(match.group(1))
        inches = int(match.group(2))
        total_inches = (feet * 12) + inches
        centimeters = total_inches * 2.54
        return int(centimeters)
    else:
        return None
    

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


def clean_games(engine: Engine, yesterday: datetime):
    """
    Reads the raw games data from the JSON file, processes it to identify home and away teams, and then merges the data to create a clean DataFrame. Finally, it writes the cleaned data to a staging table in the database.
    """
    try:
        with open(f"{GAMES_PATH}/{yesterday.year}/{yesterday.month}/{yesterday.day}_games.json") as f:
                data = json.load(f)
    except FileNotFoundError:
        print(f"No games data available for the specified date. {GAMES_PATH}/{yesterday.year}/{yesterday.month}/{yesterday.day}_games.json")
        return

    df_games = pd.DataFrame(data)
    df_games.columns = [col.lower() for col in df_games.columns]
    df_games["is_home"] = df_games["matchup"].str.contains("vs")

    home_df = df_games[df_games["is_home"]]
    away_df = df_games[~df_games["is_home"]]

    # raw data has home and away teams in separate rows, we need to merge them to get a complete picture of each game
    merged_games = home_df.merge(
        away_df,
        on="game_id",
        suffixes=("_home", "_away")
    )

    merged_games["date_id"] = merged_games["game_date_home"].str.replace("-", "")
    merged_games = merged_games[["team_id_home", "game_id", "date_id", "team_id_away", "pts_away", "pts_home"]]
    merged_games = merged_games.rename(columns={
        'team_id_home': 'home_team_id',
        'team_id_away': 'away_team_id',
        'pts_away': 'away_score',
        'pts_home': 'home_score',
    })

    # cast to int for better storage and performance
    merged_games['game_id'] = pd.to_numeric(merged_games['game_id']).astype(np.int32)
    merged_games['date_id'] = pd.to_numeric(merged_games['date_id']).astype(np.int32)
    merged_games['home_team_id'] = merged_games['home_team_id'].astype(np.int32)
    merged_games['away_team_id'] = merged_games['away_team_id'].astype(np.int32)
    merged_games['away_score'] = merged_games['away_score'].astype(np.int32)
    merged_games['home_score'] = merged_games['home_score'].astype(np.int32)

    merged_games.to_sql("fact_games", con=engine, if_exists="append", index=False)


def clean_teams(engine: Engine):
    try:
        with open(TEAMS_PATH) as f:
                data = json.load(f)
    except FileNotFoundError:
        print("No teams data available.")
        return

    teams_df = pd.DataFrame(data)

    # cast to int for better storage and performance
    teams_df['id'] = teams_df['id'].astype(np.int32)
    teams_df['year_founded'] = teams_df['year_founded'].astype(np.int32)

    teams_df.to_sql(
        "dim_teams",
        engine,
        if_exists="replace",
        index=False
    )


def clean_players(engine: Engine):
    try:
        with open(PLAYERS_PATH) as f:
                data = json.load(f)
    except FileNotFoundError:
        print("No players data available.")
        return
    
    plyaers_df = pd.DataFrame(data)

    # convert height from feet-inches to cm
    plyaers_df["height"] = plyaers_df["height"].apply(convert_height_str_to_cm)

    # convert weight from pounds to kg
    plyaers_df['weight'] = pd.to_numeric(plyaers_df['weight'])
    plyaers_df['weight'] = plyaers_df['weight'] * WEIGHT_CONVERSION_FACTOR

    plyaers_df['weight'] = plyaers_df['weight'].fillna(0)
    plyaers_df['height'] = plyaers_df['height'].fillna(0)

    # cast to int for better storage and performance
    plyaers_df['weight'] = plyaers_df['weight'].astype(np.int32)
    plyaers_df['height'] = plyaers_df['height'].astype(np.int32)

    plyaers_df.to_sql(
        "dim_players",
        engine,
        if_exists="replace",
        index=False
    )