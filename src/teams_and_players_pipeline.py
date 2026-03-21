from sqlalchemy import create_engine

from extract.pull_teams import pull_teams_and_save
from extract.pull_games import pull_games_and_save
from extract.pull_players import pull_players_and_save
from extract.pull_player_stats import pull_players_stats_and_save

from transform.clean_games import clean_games
from transform.clean_players import clean_players
from transform.clean_teams import clean_teams
from transform.clean_players_stats import clean_players_stats

engine = create_engine("sqlite:///db/nba_wh.db")

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