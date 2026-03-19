from nba_api.stats.static import teams as Teams
import json
from utils import get_or_create_full_path


def pull_teams() -> list[dict]:
    """Pulls all teams from the NBA API and returns them as a list of dictionaries."""
    return Teams.get_teams()


def main():
    teams = pull_teams()
    file_path = get_or_create_full_path("data/raw/teams.json")
    with open(file_path.as_posix(), "w") as f:
        json.dump(teams, f, indent=4)


if __name__ == "__main__":
    main()