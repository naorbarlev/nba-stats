from nba_api.stats.static import teams as Teams
import json
from utils import get_or_create_full_path, TEAMS_PATH


def pull_teams() -> list[dict]:
    """Pulls all teams from the NBA API and returns them as a list of dictionaries."""
    try:
        return Teams.get_teams()
    except Exception as e:
        print(f"Error occurred while pulling teams: {e}")
        return []


def pull_teams_and_save():
    teams = pull_teams()
    file_path = get_or_create_full_path(TEAMS_PATH)

    # open the previously saved teams data to compare it with the newly pulled data. If the newly pulled data has fewer teams than the previously saved data, we will keep the previously saved data to avoid losing data due to API issues.
    with open(file_path.as_posix(), "r") as f:
        previously_teams = json.load(f)
    
    if len(previously_teams) > len(teams):
        print("Using previously saved teams data due to API issues.")
        return
    
    with open(file_path.as_posix(), "w") as f:
        json.dump(teams, f, indent=4)
