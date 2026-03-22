from sqlalchemy import create_engine
from utils import SQLITE_URL

def get_engine():
    return create_engine(SQLITE_URL)