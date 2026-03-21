from sqlalchemy import create_engine
from extract.pull_games import pull_games_and_save
from extract.pull_player_stats import pull_players_stats_and_save
from transform.clean_games import clean_games
from transform.clean_players_stats import clean_players_stats

from utils import get_yesterday_date

yesterday = get_yesterday_date()
engine = create_engine("sqlite:///db/nba_wh.db")

def run_pipeline():
    print("Starting the NBA data pipeline...")
    print("Pulling games data...")
    pull_games_and_save(yesterday)
    print("Pulling player stats data...")
    pull_players_stats_and_save(yesterday)

    print("Starting data transformation...")
    print("Cleaning games data...")
    clean_games(engine, yesterday=yesterday)
    print("Cleaning player stats data...")
    clean_players_stats(engine, yesterday=yesterday)
    print("Data transformation completed successfully!")



run_pipeline()