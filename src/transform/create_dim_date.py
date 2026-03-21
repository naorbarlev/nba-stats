import pandas as pd
from sqlalchemy import Engine


def build_dim_date(engine: Engine, start_date="2000-01-01", end_date="2030-12-31"):
    dates = pd.date_range(start=start_date, end=end_date)

    df = pd.DataFrame({
        "full_date": dates
    })

    df["date_id"] = df["full_date"].dt.strftime("%Y%m%d").astype(int)
    df["year"] = df["full_date"].dt.year
    df["month"] = df["full_date"].dt.month
    df["day"] = df["full_date"].dt.day

    df["month_name"] = df["full_date"].dt.month_name()
    df["day_name"] = df["full_date"].dt.day_name()

    df.to_sql(
    "dim_date",
    engine,
    if_exists="replace",  # only once
    index=False
)

