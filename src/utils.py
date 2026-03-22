from pathlib import Path
from datetime import datetime, timedelta
import json

# Load config from project root
CONFIG_PATH = Path(__file__).resolve().parents[1] / "config.json"

def load_config():
    """Load configuration from config.json"""
    with open(CONFIG_PATH) as f:
        return json.load(f)

CONFIG = load_config()

# Database configuration
DB_PATH = CONFIG["database"]["path"]
SQLITE_URL = f"sqlite:///{DB_PATH}"

# Path configuration
RAW_DATA_PATH = CONFIG["paths"]["raw_data"]
GAMES_PATH = CONFIG["paths"]["games"]
PLAYERS_STATS_PATH = CONFIG["paths"]["players_stats"]
PLAYERS_PATH = CONFIG["paths"]["players"]
TEAMS_PATH = CONFIG["paths"]["teams"]


def get_or_create_full_path(path):
    """Checks if a directory exists at the given path, and creates it if it doesn't exist."""
    full_path = Path(path)
    full_path.parent.mkdir(parents=True, exist_ok=True)
    return full_path


def get_yesterday_date() -> datetime:
    """Returns yesterday's date as a datetime object."""
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    return yesterday
