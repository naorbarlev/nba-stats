# 🏀 NBA Data Engineering Pipeline

A comprehensive ETL (Extract, Transform, Load) pipeline for NBA data that collects, processes, and visualizes basketball statistics using modern data engineering practices.

## 🏗️ Architecture

### ETL Pipeline Components:

1. **Extract**: Pull data from NBA API endpoints
2. **Transform**: Clean, validate, and structure data
3. **Load**: Insert processed data into SQLite database
4. **Visualize**: Interactive dashboard for data exploration

## 📊 Data Model

### Fact Tables
- `fact_games`: Game results and scores
- `fact_players_stats`: Detailed player performance metrics

### Dimension Tables
- `dim_players`: Player information and attributes
- `dim_teams`: Team details and metadata
- `dim_date`: Date dimension for time-based analysis

## 🚀 Installation

### Prerequisites

- Python 3.8+
- pip package manager
- Git

### Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd pyhton-mid-project
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up database schema:**
   ```bash
   python src/schema.py
   ```

## 📖 Usage

### Running the Complete Pipeline

1. **Load reference data (teams & players):**
   ```bash
   python src/teams_and_players_pipeline.py
   ```

2. **Load daily games and stats:**
   ```bash
   python src/games_and_stats_pipeline.py
   ```

### Individual Pipeline Steps

```bash
# Extract data
python src/extract/pull_games.py
python src/extract/pull_player_stats.py
python src/extract/pull_players.py
python src/extract/pull_teams.py

# Run the dashboard
python src/app/app.py
```

### Flask Dashboard

The interactive dashboard allows you to:
- Browse all NBA games with scores
- View top performers for each game
- Explore detailed player statistics
- Compare team performances

```bash
python src/app/app.py
```

## ⚙️ Configuration

All configuration is managed through `config.json`:

```json
{
  "database": {
    "type": "sqlite",
    "path": "db/nba_wh.db"
  },
  "paths": {
    "raw_data": "data/raw",
    "games": "data/raw/games",
    "players_stats": "data/raw/players_stats",
    "players": "data/raw/players.json",
    "teams": "data/raw/teams.json"
  }
}
```

## 📁 Project Structure

```
├── config.json              # Configuration file
├── requirements.txt         # Python dependencies
├── data/
│   └── raw/                # Raw data storage
│       ├── games/          # Game data by date
│       ├── players_stats/  # Player stats by date
│       ├── players.json    # Player reference data
│       └── teams.json      # Team reference data
├── db/
│   └── nba_wh.db          # SQLite database
└── src/
    ├── app/                # Streamlit dashboard
    │   ├── app.py         # Main dashboard app
    │   ├── queries.py     # Database queries
    │   └── db.py          # Database connection
    ├── extract/           # Data extraction modules
    │   ├── pull_games.py
    │   ├── pull_player_stats.py
    │   ├── pull_players.py
    │   └── pull_teams.py
    ├── transform/         # Data transformation modules
    │   ├── clean_raw_data.py
    │   ├── create_dim_date.py
    │   └── __init__.py
    ├── schema.py          # Database schema setup
    ├── teams_and_players_pipeline.py
    ├── games_and_stats_pipeline.py
    └── utils.py           # Utility functions
```

## 🔗 API Sources

- **NBA API**: Official NBA statistics API
  - Games data: `nba_api.stats.endpoints.LeagueGameFinder`
  - Player stats: `nba_api.stats.endpoints.BoxScoreTraditionalV3`
  - Player info: `nba_api.stats.endpoints.CommonPlayerInfo`
  - Teams data: `nba_api.stats.static.teams`

## 🗄️ Database Schema

### Fact Tables

#### `fact_games`
```sql
CREATE TABLE fact_games (
    game_id INTEGER PRIMARY KEY,
    date_id INTEGER,
    home_team_id INTEGER,
    away_team_id INTEGER,
    home_score INTEGER,
    away_score INTEGER
);
```

#### `fact_players_stats`
```sql
CREATE TABLE fact_players_stats (
    player_id INTEGER,
    game_id INTEGER,
    team_id INTEGER,
    field_goals_made INTEGER,
    field_goals_attempted INTEGER,
    three_pointers_made INTEGER,
    three_pointers_attempted INTEGER,
    free_throws_made INTEGER,
    free_throws_attempted INTEGER,
    rebounds_offensive INTEGER,
    rebounds_defensive INTEGER,
    rebounds_total INTEGER,
    assists INTEGER,
    steals INTEGER,
    blocks INTEGER,
    turnovers INTEGER,
    fouls_personal INTEGER,
    points INTEGER,
    plus_minus_points REAL,
    minutes_seconds INTEGER,
    minutes_float INTEGER,
    PRIMARY KEY (game_id, player_id)
);
```

### Dimension Tables

#### `dim_players`
```sql
CREATE TABLE dim_players (
    id INTEGER PRIMARY KEY,
    full_name TEXT,
    first_name TEXT,
    last_name TEXT,
    position TEXT,
    team_id INTEGER,
    height INTEGER,
    weight INTEGER,
    is_active BOOLEAN
);
```

#### `dim_teams`
```sql
CREATE TABLE dim_teams (
    id INTEGER PRIMARY KEY,
    full_name TEXT,
    abbreviation TEXT,
    nickname TEXT,
    city TEXT,
    state TEXT,
    year_founded INTEGER
);
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- NBA API for providing comprehensive basketball data
- Streamlit for the amazing dashboard framework
- The data engineering community for inspiration and best practices

---

**Note**: This project is for educational purposes. Please respect NBA API usage policies and terms of service.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- NBA API for providing comprehensive basketball data
- Streamlit for the amazing dashboard framework
- The data engineering community for inspiration and best practices

---

**Note**: This project is for educational purposes. Please respect NBA API usage policies and terms of service.