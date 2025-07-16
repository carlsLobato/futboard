import streamlit as st
import json
import os
import base64

st.set_page_config(page_title="⚽ Futboard", layout="wide")
st.title("⚽ Futboard")
st.markdown(
    """
    <style>
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.55);  /* Adjust the opacity as needed */
        z-index: -1;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Inject custom CSS for background
def set_background(image_file):
    with open(image_file, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background("assets/bg.png")  # ✅ adjust the path if needed

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

        # Stats
        stats = detail.get("stats", {})
        st.subheader("📊 Estadísticas")
        st.markdown(f"- Partidos programados: **{stats.get('games_scheduled', 0)}**")
        st.markdown(f"- Partidos jugados: **{stats.get('games_played', 0)}**")

        # Último partido
        last = detail.get("last_match")
        if last:
            st.subheader("⏪ Último partido")
            st.markdown(f"- Rival: **{last['vs']}**")
            st.markdown(f"- Fecha: **{last['date']}**, **{last['time']}**")
            st.markdown(f"- {'Local' if last['home'] else 'Visitante'}")

            # Mostrar resultado con emoji
            result_emoji = {
                'W': '🟢 Victoria',
                'T': '🟡 Empate',
                'L': '🔴 Derrota'
            }.get(last.get("result"), "❓ Resultado desconocido")

            st.markdown(f"- Marcador: {last['score']} {result_emoji}")

        # Próximo partido
        next_match = detail.get("next_match")
        if next_match:
            st.subheader("⏭️ Próximo partido")
            st.markdown(f"- Rival: **{next_match['vs']}**")
            st.markdown(f"- Fecha: **{next_match['date']}**")
            st.markdown(f"- Local: {'✅' if next_match['home'] else '🚫'}")
        else:
            st.markdown("❌ Sin partidos futuros registrados.")
    else:
        st.error("⚠️ No se encontró información del equipo.")

