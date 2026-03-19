from nba_api.stats.static import players as Players
from nba_api.stats.endpoints import commonplayerinfo
import json
import time
import requests
from urllib3 import HTTPSConnectionPool

def pull_players() -> list[dict]:
    """Pulls all players from the NBA API and returns them as a list of dictionaries."""
    return Players.get_players()


def main():
    playersExapnded = []
    players = pull_players()
    for player in players:
        try:
            if player.get("is_active") == False:
                continue
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
            playersExapnded.append(player)
            time.sleep(0.5)
        
        except requests.exceptions.ReadTimeout:
            print(f"Read timeout occurred for player: {player.get('full_name')}. Retrying after 60 seconds...")
            time.sleep(60)
        except requests.RequestException as e:
            print(f"Error occurred for player: {player.get('full_name')}, Error: {e}")

    with open("data/raw/players.json", "w") as f:
        json.dump(playersExapnded, f, indent=4)


if __name__ == "__main__":
    main()