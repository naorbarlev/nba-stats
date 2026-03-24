from sqlalchemy import create_engine

from extract.pull_teams import pull_teams_and_save
from extract.pull_players import pull_players_and_save

from transform.clean_raw_data import clean_teams, clean_players

from utils import SQLITE_URL


engine = create_engine(SQLITE_URL)

def run_pipeline():
    print("Starting the NBA data pipeline...")
    print("Pulling players data...")
    pull_players_and_save()
    print("Pulling teams data...")
    pull_teams_and_save()

    print("Starting data transformation...")
    print("Cleaning players data...")
    clean_players(engine)
    print("Cleaning teams data...")
    clean_teams(engine)   
    print("Data transformation completed successfully!")



run_pipeline()