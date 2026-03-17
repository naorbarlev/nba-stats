from nba_api.stats.endpoints import playergamelogs
import json
from datetime import datetime, timedelta

now = datetime.now()
yesterday = now - timedelta(days=1)


def pull_players_stats() -> list[dict]:
    """Pulls all player stats from the NBA API and returns them as a list of dictionaries."""
    player_game_logs_res = playergamelogs.PlayerGameLogs(
    date_from_nullable=yesterday.strftime("%m/%d/%Y")
    )
    with open(f"data/raw/player_stats/{yesterday.strftime('%m-%d-%Y')}_player_stats.json", "w") as f:
        json.dump(player_game_logs_res.get_dict(), f, indent=4)
        return
    headers = player_game_logs_res.get_dict().get("data_sets").get("PlayerGameLogs")[0]
    print(headers)
    rows = player_game_logs_res.get_dict().get("resultSets")[0].get("rowSet")
    games_list = []
    for row in rows:
        games_list.append(dict(zip(headers, row)))
    return games_list


def main():
    players_stats = pull_players_stats()
    with open(f"data/raw/player_stats/{yesterday.strftime('%m-%d-%Y')}_player_stats.json", "w") as f:
        json.dump(players_stats, f, indent=4)

if __name__ == "__main__":
    main()