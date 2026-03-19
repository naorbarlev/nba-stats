from pathlib import Path

def get_or_create_full_path(path):
    """Checks if a directory exists at the given path, and creates it if it doesn't exist."""
    full_path = Path(path)
    full_path.parent.mkdir(parents=True, exist_ok=True)
    return full_path
