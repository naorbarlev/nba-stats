import streamlit as st
import pandas as pd
import queries

# -----------------------------
# HELPERS
# -----------------------------
def get_player_image(player_id):
    return f"https://cdn.nba.com/headshots/nba/latest/1040x760/{player_id}.png"

def get_team_logo(team_id):
    return f"https://cdn.nba.com/logos/nba/{team_id}/primary/L/logo.svg"

def get_top_players(stats_df, game_id, home_team_id, away_team_id):
    game_df = stats_df[stats_df["game_id"] == game_id]

    home_df = game_df[game_df["team_id"] == home_team_id]
    away_df = game_df[game_df["team_id"] == away_team_id]

    top_home = home_df.loc[home_df["points"].idxmax()]
    top_away = away_df.loc[away_df["points"].idxmax()]

    return top_home, top_away


def render_player(player, team_name):

    col_img, col_stats = st.columns([1, 1])

    with col_img:
        st.image(get_player_image(player["player_id"]), use_container_width=True)

    with col_stats:
        st.markdown(f"### {player['player_name']}")
        st.write(f"🏀 Points: {player['points']}")
        st.write(f"🔄 Offensive Rebounds: {player['offensive_rebounds']}")
        st.write(f"🔄 Defensive Rebounds: {player['defensive_rebounds']}")
        st.write(f"🎯 Assists: {player['assists']}")
        st.write(f"🛡️ Steals: {player['steals']}")
        st.write(f"⛔ Blocks: {player['blocks']}")
        st.write(f"⛔ Turnovers: {player['turnovers']}")
        st.write(f"🕒 Minutes Played: {int(player['minutes_played'])}")
        st.write(f"🎯 FG %: {player['field_goal_percentage'] * 100:.1f}%")
        st.write(f"🏹 3P %: {player['three_point_percentage'] * 100:.1f}%")
        st.write(f"🏀 FT %: {player['free_throw_percentage'] * 100:.1f}%")
        st.write(f"➕ Plus/Minus: {int(player['plus_minus_points'])}")


# -----------------------------
# UI
# -----------------------------
st.set_page_config(layout="wide")
st.title("🏀 NBA Game Leaders")

games_df = queries.get_games()
stats_df = queries.load_player_stats()

games_df["label"] = (
    games_df["home_team_name"]
    + " vs "
    + games_df["away_team_name"]
    + " | "
    + games_df["home_score"].astype(str)
    + "-"
    + games_df["away_score"].astype(str)
    + " | "
    + games_df["full_date"].str.slice(0, 10)
)

selected_label = st.selectbox("Select Game", games_df["label"])

selected_row = games_df[games_df["label"] == selected_label].iloc[0]

# Match header
col1, col2, col3 = st.columns([2, 1, 2])

# HOME TEAM
with col1:
    logo_col, name_col = st.columns([1, 3])
    
    with logo_col:
        st.image(get_team_logo(selected_row["home_team_id"]), width=60)
    
    with name_col:
        st.markdown(f"### {selected_row['home_team_name']}")

# SCORE
with col2:
    st.markdown(
        f"<h2 style='text-align:center;'>{selected_row['home_score']} - {selected_row['away_score']}</h2>",
        unsafe_allow_html=True
    )

# AWAY TEAM
with col3:
    name_col, logo_col = st.columns([3, 1])
    
    with name_col:
        st.markdown(f"### {selected_row['away_team_name']}")
    
    with logo_col:
        st.image(get_team_logo(selected_row["away_team_id"]), width=60)

game_id = selected_row["game_id"]
home_team_id = selected_row["home_team_id"]
away_team_id = selected_row["away_team_id"]

# Get top players
top_home, top_away = get_top_players(
    stats_df, game_id, home_team_id, away_team_id
)

# Layout
col1, col2 = st.columns(2)

with col1:
    render_player(top_home, selected_row["home_team_name"])

with col2:
    render_player(top_away, selected_row["away_team_name"])