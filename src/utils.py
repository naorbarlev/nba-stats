from pathlib import Path
from datetime import datetime, timedelta

def get_or_create_full_path(path):
    """Checks if a directory exists at the given path, and creates it if it doesn't exist."""
    full_path = Path(path)
    full_path.parent.mkdir(parents=True, exist_ok=True)
    return full_path


def get_yesterday_date() -> datetime:
    """Returns yesterday's date as a string in the format YYYY-MM-DD."""
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    return yesterday
