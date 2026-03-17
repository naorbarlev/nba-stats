from nba_api.stats.static import teams as Teams
import json


def pull_teams() -> list[dict]:
    """Pulls all teams from the NBA API and returns them as a list of dictionaries."""
    return Teams.get_teams()


def main():
    teams = pull_teams()
    with open("data/raw/teams.json", "w") as f:
        json.dump(teams, f, indent=4)


if __name__ == "__main__":
    main()