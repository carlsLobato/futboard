import streamlit as st
import json
import os
import base64
import pandas as pd
import plotly.express as px

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
search_query = st.text_input("Search for a team", "")

# Filter teams by search query
filtered_teams = [
    team for team in teams
    if search_query.lower() in team["name"].lower()
]

with st.expander("Liga MX", icon="🛡️"):

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
                'T': '⚪️ Empate',
                'L': '🔴 Derrota'
            }.get(last.get("result"), "❓ Resultado desconocido")

            st.markdown(f"- Marcador: {last['score']} {result_emoji}")

        form = detail.get("form", [])
        if form:
            st.subheader("📈 Últimos 5 partidos")
            emoji_map = {"W": "🟩", "D": "🟨", "L": "🟥"}
            form_display = " ".join([emoji_map.get(r, r) for r in form])
            st.markdown(f"{form_display}  \n`{' '.join(form)}`")

        #Historial
        record = detail.get("record", {})
        total = record.get("total", {})

        st.subheader("📊 Estadísticas Generales (desde Apertura 2012)")
        st.markdown(f"- Partidos jugados: **{total.get('games_played', 0)}**")
        st.markdown(f"- Victorias: 🟩 **{total.get('wins', 0)}**")
        st.markdown(f"- Empates: 🟨 **{total.get('draws', 0)}**")
        st.markdown(f"- Derrotas: 🟥 **{total.get('losses', 0)}**")
        # Datos base
        labels = ['Victorias', 'Empates', 'Derrotas']
        values = [
            total.get('wins', 0),
            total.get('draws', 0),
            total.get('losses', 0)
        ]

        # Crear gráfico de pastel
        fig = px.pie(
            names=labels,
            values=values,
            title="Distribución de resultados",
            color=labels,
            color_discrete_map={
                'Victorias': 'green',
                'Empates': 'gold',
                'Derrotas': 'red'
            },
            hole=0.3  # Donut style (opcional)
        )

        # Mostrar en Streamlit
        st.plotly_chart(fig, use_container_width=True)


        st.markdown(f"- Goles a favor: **{total.get('goals_for', 0)}**")
        st.markdown(f"- Goles en contra: **{total.get('goals_against', 0)}**")
        st.markdown(f"- Diferencia de goles: **{total.get('goal_difference', 0)}**")
        st.markdown(f"- % Victorias: **{total.get('win_rate', 0)}%**")

        #Últimos 12 meses
        history = detail.get("match_history", [])
        if history:
            hist_df = pd.DataFrame(history)
            hist_df['date'] = pd.to_datetime(hist_df['date'])

            fig = px.line(
                hist_df,
                x='date',
                y=['goals_for', 'goals_against'],
                labels={
                    'value': 'Goles',
                    'variable': 'Tipo',
                    'date': 'Fecha'
                },
                title="📈 Goles por partido (últimos 12 meses)",
                markers=True
            )
            fig.update_traces(mode='lines+markers')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay historial de partidos en los últimos 12 meses.")

        #Resultados de local vs visitante
        home = record.get("home", {})
        away = record.get("away", {})

        import pandas as pd
        import plotly.express as px

        home = record.get("home", {})
        away = record.get("away", {})

        # Crear DataFrame para comparativa
        stats_data = {
            "Condición": ["Local", "Visitante"],
            "PJ": [home.get("games_played", 0), away.get("games_played", 0)],
            "W": [home.get("wins", 0), away.get("wins", 0)],
            "D": [home.get("draws", 0), away.get("draws", 0)],
            "L": [home.get("losses", 0), away.get("losses", 0)],
            "GF": [home.get("goals_for", 0), away.get("goals_for", 0)],
            "GA": [home.get("goals_against", 0), away.get("goals_against", 0)],
            "%W": [home.get("win_rate", 0), away.get("win_rate", 0)],
        }

        df_stats = pd.DataFrame(stats_data)

        fig_results = px.bar(
            df_stats.melt(id_vars="Condición", value_vars=["W", "D", "L"], var_name="Resultado", value_name="Cantidad"),
            x="Condición",
            y="Cantidad",
            color="Resultado",
            barmode="group",
            title="🏟️ Resultados como Local vs Visitante",
            color_discrete_map={"W": "green", "D": "gray", "L": "red"}
        )
        st.plotly_chart(fig_results, use_container_width=True)

        fig_goals = px.bar(
            df_stats.melt(id_vars="Condición", value_vars=["GF", "GA"], var_name="Tipo", value_name="Goles"),
            x="Condición",
            y="Goles",
            color="Tipo",
            barmode="group",
            title="⚽ Goles a Favor y en Contra",
            color_discrete_map={"GF": "blue", "GA": "orange"}
        )
        st.plotly_chart(fig_goals, use_container_width=True)

        fig_winrate = px.bar(
            df_stats,
            x="Condición",
            y="%W",
            color="Condición",
            title="✅ Porcentaje de Victorias",
            text="%W",
            labels={"%W": "Porcentaje de Victorias"},
            color_discrete_sequence=["green", "blue"]
        )
        fig_winrate.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_winrate.update_layout(yaxis=dict(range=[0, 100]))
        st.plotly_chart(fig_winrate, use_container_width=True)