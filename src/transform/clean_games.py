from sqlalchemy import Engine, create_engine
import json
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

engine = create_engine("sqlite:///data/staging/staging.db")
now = datetime.now()
yesterday = now - timedelta(days=1)

def clean_games(engine: Engine):
    try:
        with open(f"data/raw/games/{yesterday.strftime('%m-%d-%Y')}_games.json") as f:
                data = json.load(f)
    except FileNotFoundError:
        print("No games data available for the specified date.")
        return

    df_games = pd.DataFrame(data)
    df_games.columns = [col.lower() for col in df_games.columns]
    df_games["is_home"] = df_games["matchup"].str.contains("vs")

    home_df = df_games[df_games["is_home"]]
    away_df = df_games[~df_games["is_home"]]

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

    merged_games['game_id'] = pd.to_numeric(merged_games['game_id']).astype(np.int32)
    merged_games['date_id'] = pd.to_numeric(merged_games['date_id']).astype(np.int32)
    merged_games['home_team_id'] = merged_games['home_team_id'].astype(np.int32)
    merged_games['away_team_id'] = merged_games['away_team_id'].astype(np.int32)
    merged_games['away_score'] = merged_games['away_score'].astype(np.int32)
    merged_games['home_score'] = merged_games['home_score'].astype(np.int32)

    merged_games.to_sql("staging_games", con=engine, if_exists="append", index=False)


if __name__ == "__main__":
    clean_games(engine)