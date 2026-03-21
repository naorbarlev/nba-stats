from sqlalchemy import Engine, create_engine
import json
import pandas as pd
import re
import numpy as np

WEIGHT_CONVERSION_FACTOR = 0.45359237

engine = create_engine("sqlite:///db/nba_wh.db")

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
    

def clean_players(engine: Engine):
    with open("data/raw/players.json") as f:
        data = json.load(f)
    
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
