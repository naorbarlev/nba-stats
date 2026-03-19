from nba_api.stats.endpoints import playergamelogs
import json
from datetime import datetime, timedelta
from nba_api.stats.endpoints import boxscoretraditionalv3
import time

now = datetime.now()
yesterday = now - timedelta(days=2)


def pull_players_stats() -> list[dict]:

    with open(f"data/raw/games/{yesterday.strftime('%m-%d-%Y')}_games.json", "r") as f:
        games = json.load(f)
    
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
    with open(f"data/raw/players_stats/{yesterday.strftime('%m-%d-%Y')}_player_stats.json", "w") as f:
        json.dump(players_stats, f, indent=4)

if __name__ == "__main__":
    main()