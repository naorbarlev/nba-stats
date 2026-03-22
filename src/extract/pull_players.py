from nba_api.stats.static import players as Players
from nba_api.stats.endpoints import commonplayerinfo
import json
import time
import requests
from utils import get_or_create_full_path, PLAYERS_PATH


def pull_players() -> list[dict]:
    """Pulls all players from the NBA API and returns them as a list of dictionaries."""
    return Players.get_players()

def pull_players_and_save():
    expanded_players = []
    players = pull_players()
    retries = 0
    for player in players:

        # We only want to pull data for active players, and we want to avoid getting stuck on a player that causes repeated API errors, so we will skip players that are not active and we will retry a player up to 2 times before skipping them.
        if player.get("is_active") == False: 
            continue
        if retries >= 2:
            print("Maximum retries reached. continuing with the next player.")
            continue
        try:
            common_player_info_res = commonplayerinfo.CommonPlayerInfo(player_id=player.get("id"), timeout=180).get_dict()
            if not common_player_info_res.get("resultSets"):
                continue
            headers = common_player_info_res.get("resultSets")[0]["headers"]
            row = common_player_info_res["resultSets"][0]["rowSet"][0]

            common_player_info_dict = dict(zip(headers, row))
            player["position"] = common_player_info_dict.get("POSITION")
            player["height"] = common_player_info_dict.get("HEIGHT")
            player["weight"] = common_player_info_dict.get("WEIGHT")
            player["team_id"] = common_player_info_dict.get("TEAM_ID")
            player["birthdate"] = common_player_info_dict.get("BIRTHDATE")
            expanded_players.append(player)
            retries = 0
            time.sleep(1.5)
        
        except requests.exceptions.ReadTimeout:
            print(f"Read timeout occurred for player: {player.get('full_name')}. Retrying after 60 seconds...")
            time.sleep(60)
            retries += 1
        except requests.exceptions.ConnectionError:
            print(f"Connection error occurred for player: {player.get('full_name')}. Retrying after 60 seconds...")
            time.sleep(60)
            retries += 1
        except requests.RequestException as e:
            print(f"Error occurred for player: {player.get('full_name')}, Error: {e}")
            retries += 1

    file_path = get_or_create_full_path(PLAYERS_PATH)
    with open(file_path.as_posix(), "r") as f:
        previously_expanded_players = json.load(f)
    
    if len(previously_expanded_players) > len(expanded_players):
            print("Using previously saved expanded players data due to API issues.")
            return

    with open(file_path.as_posix(), "w") as f:
        json.dump(expanded_players, f, indent=4)