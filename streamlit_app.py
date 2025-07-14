import streamlit as st
import json
import os

st.set_page_config(page_title="⚽ FutStats", layout="wide")
st.title("⚽ FutStats")

# Load Liga MX teams
with open("data/liga_mx_teams.json", encoding="utf-8") as f:
    teams = json.load(f)

# Search bar
search_query = st.text_input("Search for a team or player", "")

# Filter teams by search query
filtered_teams = [
    team for team in teams
    if search_query.lower() in team["name"].lower()
]

st.subheader("Liga MX Teams")

# Display filtered teams in rows of 6
for i in range(0, len(filtered_teams), 6):
    cols = st.columns(6)
    for j, team in enumerate(filtered_teams[i:i+6]):
        with cols[j]:
            st.image(team["icon"], width=60)
            if st.button(team["name"], key=team["slug"]):
                st.session_state.selected_team = team["slug"]

# Show team details
if "selected_team" in st.session_state:
    team_slug = st.session_state.selected_team
    detail_path = f"data/teams/liga_mx/{team_slug}_detail.json"
    if os.path.exists(detail_path):
        with open(detail_path, encoding="utf-8") as f:
            detail = json.load(f)
        st.header(detail["name"])
        st.write(detail["description"])
    else:
        st.error("Team data not found.")
