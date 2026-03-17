from nba_api.stats.endpoints import leaguegamefinder
import json
from datetime import datetime, timedelta

now = datetime.now()
yesterday = now - timedelta(days=1)


def pull_games() -> list[dict]:
    """Pulls all games from the NBA API and returns them as a list of dictionaries."""
    games = leaguegamefinder.LeagueGameFinder(
    date_from_nullable=yesterday.strftime("%m/%d/%Y"))

    headers = games.get_dict().get("resultSets")[0].get("headers")
    rows = games.get_dict().get("resultSets")[0].get("rowSet")
    games_list = []
    for row in rows:
        games_list.append(dict(zip(headers, row)))
    return games_list


def main():
    games = pull_games()
    with open(f"data/raw/games/{yesterday.strftime('%m-%d-%Y')}_games.json", "w") as f:
        json.dump(games, f, indent=4)

if __name__ == "__main__":
    main()