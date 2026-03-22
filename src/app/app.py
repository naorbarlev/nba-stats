import streamlit as st
import pandas as pd
import queries

# -----------------------------
# HELPERS
# -----------------------------
def get_player_image(player_id):
    return f"https://cdn.nba.com/headshots/nba/latest/1040x760/{player_id}.png"


def get_top_players(stats_df, game_id, home_team_id, away_team_id):
    game_df = stats_df[stats_df["game_id"] == game_id]

    home_df = game_df[game_df["team_id"] == home_team_id]
    away_df = game_df[game_df["team_id"] == away_team_id]

    top_home = home_df.loc[home_df["points"].idxmax()]
    top_away = away_df.loc[away_df["points"].idxmax()]

    return top_home, top_away


def render_player(player, team_name):
    st.subheader(team_name)

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


# -----------------------------
# UI
# -----------------------------
st.set_page_config(layout="wide")
st.title("🏀 NBA Game Leaders")

games_df = queries.get_games()
stats_df = queries.load_player_stats()

# Create label for drostreamlit run app/app.pyown
games_df["label"] = (
    games_df["home_team_name"]
    + " vs "
    + games_df["away_team_name"]
)

selected_label = st.selectbox("Select Game", games_df["label"])

selected_row = games_df[games_df["label"] == selected_label].iloc[0]

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