from nba_api.stats.endpoints import leaguegamefinder
import json
from datetime import datetime, timedelta
from utils import get_or_create_full_path
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
    file_path = get_or_create_full_path(f"data/raw/games/{yesterday.year}/{yesterday.month}/{yesterday.day}_games.json")
    with open(file_path.as_posix(), "w") as f:
        json.dump(games, f, indent=4)

if __name__ == "__main__":
    main()