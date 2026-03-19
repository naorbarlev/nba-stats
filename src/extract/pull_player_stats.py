from nba_api.stats.endpoints import playergamelogs
import json
from datetime import datetime, timedelta
from nba_api.stats.endpoints import boxscoretraditionalv3
import time
from utils import get_or_create_full_path

now = datetime.now()
yesterday = now - timedelta(days=1)


def pull_players_stats() -> list[dict]:
    try:   
        with open(f"data/raw/games/{yesterday.year}/{yesterday.month}/{yesterday.day}_games.json", "r") as f:
            games = json.load(f)
    except FileNotFoundError:
        print("No games data available for the specified date. Cannot pull player stats.")
        return []
    
    game_ids = [game.get("GAME_ID") for game in games]
    game_ids = list(set(game_ids))

    player_stats_list = []
    for game_id in game_ids:
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

        
        time.sleep(1.5)  
    return player_stats_list


def main():
    players_stats = pull_players_stats()
    file_path = get_or_create_full_path(f"data/raw/players_stats/{yesterday.year}/{yesterday.month}/{yesterday.day}_player_stats.json")
    with open(file_path.as_posix(), "w") as f:
        json.dump(players_stats, f, indent=4)

if __name__ == "__main__":
    main()