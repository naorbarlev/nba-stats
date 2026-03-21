
import json
from datetime import datetime
from nba_api.stats.endpoints import boxscoretraditionalv3
import time
import requests
from utils import get_or_create_full_path


def pull_players_stats(yesterday: datetime) -> list[dict]:
    try:   
        with open(f"data/raw/games/{yesterday.year}/{yesterday.month}/{yesterday.day}_games.json", "r") as f:
            games = json.load(f)
    except FileNotFoundError:
        print("No games data available for the specified date. Cannot pull player stats.")
        return []
    
    game_ids = [game.get("GAME_ID") for game in games]
    game_ids = list(set(game_ids)) # because each game appears twice in the games data (once for each team), we need to deduplicate the game ids

    player_stats_list = []
    for game_id in game_ids:
        try:
            box_score_res = boxscoretraditionalv3.BoxScoreTraditionalV3(
                game_id=game_id
            ).get_dict()
            if not box_score_res.get("boxScoreTraditional"):
                continue

            home_players_stats = box_score_res.get("boxScoreTraditional").get("homeTeam", {}).get("players", [])
            for hp in home_players_stats:
                hp["GAME_ID"] = game_id
                hp["TEAM_ID"] = box_score_res.get("boxScoreTraditional").get("homeTeam", {}).get("teamId")
                player_stats_list.append(hp)
            
            away_players_stats = box_score_res.get("boxScoreTraditional").get("awayTeam", {}).get("players", [])
            for ap in away_players_stats:
                ap["GAME_ID"] = game_id
                ap["TEAM_ID"] = box_score_res.get("boxScoreTraditional").get("awayTeam", {}).get("teamId")
                player_stats_list.append(ap)
        
        except requests.exceptions.ReadTimeout:
            print(f"Read timeout occurred for game: {game_id}. Retrying after 60 seconds...")
            time.sleep(60)
        except requests.exceptions.ConnectionError:
            print(f"Connection error occurred for game: {game_id}. Retrying after 60 seconds...")
            time.sleep(60)
        except requests.RequestException as e:
            print(f"Error occurred for game: {game_id}, Error: {e}")

        
        time.sleep(1.5) # to avoid hitting the API rate limit
    return player_stats_list


def pull_players_stats_and_save(yesterday: datetime):
    players_stats = pull_players_stats(yesterday)
    file_path = get_or_create_full_path(f"data/raw/players_stats/{yesterday.year}/{yesterday.month}/{yesterday.day}_player_stats.json")
    with open(file_path.as_posix(), "w") as f:
        json.dump(players_stats, f, indent=4)
