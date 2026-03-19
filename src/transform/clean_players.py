from sqlalchemy import Engine, create_engine
import json
import pandas as pd

engine = create_engine("sqlite:///data/staging/staging.db")

def clean_players(engine: Engine):
    with open("data/raw/players.json") as f:
        data = json.load(f)
    
    df = pd.DataFrame(data)
    df.to_sql(
        "stg_players",
        engine,
        if_exists="replace",
        index=False
    )


if __name__ == "__main__":
    clean_players(engine)