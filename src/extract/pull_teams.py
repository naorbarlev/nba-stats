from nba_api.stats.static import teams as Teams
import json
from utils import get_or_create_full_path, TEAMS_PATH


def pull_teams() -> list[dict]:
    """Pulls all teams from the NBA API and returns them as a list of dictionaries."""
    return Teams.get_teams()

def pull_teams_and_save():
    teams = pull_teams()
    file_path = get_or_create_full_path(TEAMS_PATH)
    with open(file_path.as_posix(), "w") as f:
        json.dump(teams, f, indent=4)
