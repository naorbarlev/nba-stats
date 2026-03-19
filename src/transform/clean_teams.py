from sqlalchemy import Engine, create_engine
import json
import numpy as np
import pandas as pd

engine = create_engine("sqlite:///db/nba_wh.db")


def clean_teams(engine: Engine):
    try:
        with open("data/raw/teams.json") as f:
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


if __name__ == "__main__":
    clean_teams(engine)