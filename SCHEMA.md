
# ⭐ Dimensions (DI = DIM)

## `dim_player`

**Grain:** 1 row = 1 player

```sql
CREATE TABLE dim_player (
    player_id INTEGER PRIMARY KEY,
    player_name TEXT,
    first_name TEXT,
    last_name TEXT,
    position TEXT,
    height TEXT,
    weight TEXT,
    team_id INTEGER,
    is_active INTEGER
);
```

💡 Notes:

* `player_id` = `PERSON_ID`
* Keep it **simple first**, you can enrich later

---

## `dim_team`

**Grain:** 1 row = 1 team

```sql
CREATE TABLE dim_team (
    team_id INTEGER PRIMARY KEY,
    team_name TEXT,
    team_abbreviation TEXT,
    team_city TEXT
);
```

---

## `dim_date`

**Grain:** 1 row = 1 date

```sql
CREATE TABLE dim_date (
    date_id INTEGER PRIMARY KEY,   -- YYYYMMDD
    full_date DATE,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    day_of_week INTEGER,
    is_weekend INTEGER
);
```

💡 Example:

```
20240315 → 2024-03-15
```

---

# ⭐ Fact Tables

## `fact_games`

**Grain:** 1 row = 1 game

```sql
CREATE TABLE fact_games (
    game_id TEXT PRIMARY KEY,
    date_id INTEGER,
    home_team_id INTEGER,
    away_team_id INTEGER,
    home_score INTEGER,
    away_score INTEGER,
    season TEXT,

    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (home_team_id) REFERENCES dim_team(team_id),
    FOREIGN KEY (away_team_id) REFERENCES dim_team(team_id)
);
```

---

## `fact_player_stats`

**Grain:** 1 row = 1 player in 1 game

```sql
CREATE TABLE fact_player_stats (
    game_id TEXT,
    player_id INTEGER,
    team_id INTEGER,

    minutes TEXT,
    points INTEGER,
    rebounds INTEGER,
    assists INTEGER,
    steals INTEGER,
    blocks INTEGER,
    turnovers INTEGER,

    fg_made INTEGER,
    fg_attempted INTEGER,
    fg_pct REAL,

    three_pt_made INTEGER,
    three_pt_attempted INTEGER,
    three_pt_pct REAL,

    ft_made INTEGER,
    ft_attempted INTEGER,
    ft_pct REAL,

    plus_minus INTEGER,

    PRIMARY KEY (game_id, player_id),

    FOREIGN KEY (game_id) REFERENCES fact_games(game_id),
    FOREIGN KEY (player_id) REFERENCES dim_player(player_id),
    FOREIGN KEY (team_id) REFERENCES dim_team(team_id)
);
```

---

# 🔗 Relationships (Important)

```text
dim_player  ─────┐
                 ├── fact_player_stats ─── fact_games ─── dim_date
dim_team    ─────┘            │
                              └── dim_team (home/away)
```

---

# ✅ Summary

| Table             | Grain             |
| ----------------- | ----------------- |
| dim_player        | 1 player          |
| dim_team          | 1 team            |
| dim_date          | 1 date            |
| fact_games        | 1 game            |
| fact_player_stats | 1 player per game |


