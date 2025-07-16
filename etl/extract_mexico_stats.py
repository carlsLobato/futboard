import pandas as pd
import os
import json
from datetime import datetime
import pytz

# Rutas
CSV_PATH = '../data/MEX.csv'
TEAM_INFO_PATH = '../data/liga_mx_teams.json'
OUTPUT_DIR = '../data/teams/liga_mx'
os.makedirs(OUTPUT_DIR, exist_ok=True)

#Calcular estadísticas
def compute_stats(matches, team_name):
    wins, draws, losses = 0, 0, 0
    goals_for, goals_against = 0, 0
    for _, row in matches.iterrows():
        home = row['Home'] == team_name
        gf = row['HG'] if home else row['AG']
        ga = row['AG'] if home else row['HG']

        goals_for += gf
        goals_against += ga

        if gf > ga:
            wins += 1
        elif gf == ga:
            draws += 1
        else:
            losses += 1

    total_games = len(matches)
    return {
        "games_played": total_games,
        "wins": wins,
        "draws": draws,
        "losses": losses,
        "goals_for": goals_for,
        "goals_against": goals_against,
        "goal_difference": goals_for - goals_against,
        "win_rate": round((wins / total_games) * 100, 2) if total_games > 0 else 0
    }

# Slugify básico
def slugify(name):
    return name.lower().replace('á', 'a').replace('é', 'e').replace('í', 'i')\
        .replace('ó', 'o').replace('ú', 'u').replace('ü', 'u')\
        .replace('ñ', 'n').replace(' ', '_').replace('club_', '')\
        .replace('atl._', '').replace('_fc', '').replace('_chivas', '')

# Cargar info oficial de equipos
with open(TEAM_INFO_PATH, 'r', encoding='utf-8') as f:
    team_info = json.load(f)

# Crear diccionario: slugify(name) -> (name_oficial, slug_oficial)
slug_to_official = {
    slugify(team["name"]): (team["name"], team["slug"])
    for team in team_info
}

# Cargar CSV
df = pd.read_csv(CSV_PATH)
df.columns = [col.strip() for col in df.columns]

# Columnas relevantes
columns_needed = ['Home', 'Away', 'Date', 'Time', 'HG', 'AG', 'Res']
df = df[columns_needed]
df = df.dropna(subset=['Home', 'Away'])

# Parseo de fechas: combinar Date y Time
df['Datetime'] = df['Date'].astype(str) + ' ' + df['Time'].astype(str)

# Intentar parsear datetime
df['Datetime'] = pd.to_datetime(df['Datetime'], format='%d/%m/%Y %H:%M', errors='coerce')

# Mostrar errores de parseo
failed = df[df['Datetime'].isna()]
if not failed.empty:
    print("❌ Falló el parseo en las siguientes filas:")
    print(failed[['Date', 'Time']])
else:
    print("✅ Todas las fechas se parsearon correctamente.")

# Eliminar filas con datetime inválido
df = df.dropna(subset=['Datetime'])

# Convertir a zona horaria local
df['Datetime'] = df['Datetime'].dt.tz_localize('UTC').dt.tz_convert('America/Mexico_City')

# Diagnóstico de fechas
print("🗓️ Rango de fechas:", df['Datetime'].min(), "→", df['Datetime'].max())

# Obtener equipos únicos
teams = pd.concat([df['Home'], df['Away']]).unique()

# Tiempo actual con tz
now = pd.Timestamp.now(tz='America/Mexico_City')

for team in teams:
    matches = df[(df['Home'] == team) | (df['Away'] == team)].sort_values(by='Datetime')
    slug = slugify(team)

    # Usar nombre y slug oficiales si están en el JSON
    if slug in slug_to_official:
        team_name, team_slug = slug_to_official[slug]
    else:
        print(f"⚠️ No encontrado en JSON: {team} → usando nombre y slug locales")
        team_name, team_slug = team, slug

    # Último partido jugado
    # Último partido
    past_matches = matches[matches['Datetime'] < pd.Timestamp.now(tz='America/Mexico_City')]
    last_match = past_matches.iloc[-1] if not past_matches.empty else None

    if last_match is not None:
        is_home = last_match['Home'] == team
        goals_for = last_match['HG'] if is_home else last_match['AG']
        goals_against = last_match['AG'] if is_home else last_match['HG']

        if goals_for > goals_against:
            result = 'W'
        elif goals_for < goals_against:
            result = 'L'
        else:
            result = 'T'

        last_match_data = {
            'vs': last_match['Away'] if is_home else last_match['Home'],
            'date': last_match['Datetime'].strftime('%Y-%m-%d'),
            'time': last_match['Datetime'].strftime('%H:%M'),
            'home': is_home,
            'score': f"{last_match['HG']} - {last_match['AG']}",
            'result': result
        }
    else:
        last_match_data = None

    # Subsets por condición de local/visitante
    home_matches = past_matches[past_matches['Home'] == team]
    away_matches = past_matches[past_matches['Away'] == team]

    # Record general, local y visitante
    record = {
        "total": compute_stats(past_matches, team),
        "home": compute_stats(home_matches, team),
        "away": compute_stats(away_matches, team)
    }

    # Últimos 5 resultados
    form = []
    for _, row in past_matches.tail(5).iterrows():
        home = row['Home'] == team
        gf = row['HG'] if home else row['AG']
        ga = row['AG'] if home else row['HG']
        if gf > ga:
            form.append("W")
        elif gf == ga:
            form.append("D")
        else:
            form.append("L")

    # Agregar historial de últimos 12 meses
    cutoff_date = pd.Timestamp.now(tz='America/Mexico_City') - pd.Timedelta(days=365)
    last_year_matches = past_matches[past_matches['Datetime'] >= cutoff_date]

    match_history = []
    for _, row in last_year_matches.iterrows():
        is_home = row['Home'] == team
        goals_for = row['HG'] if is_home else row['AG']
        goals_against = row['AG'] if is_home else row['HG']
        result = (
            'W' if goals_for > goals_against else
            'L' if goals_for < goals_against else
            'T'
        )
        match_history.append({
            "date": row['Datetime'].strftime('%Y-%m-%d'),
            "goals_for": goals_for,
            "goals_against": goals_against,
            "result": result
        })

    # Objeto final
    team_data = {
        "name": team_name,
        "last_match": last_match_data,
        "record": record,
        "form": form,
        "match_history": match_history
    }

    output_path = os.path.join(OUTPUT_DIR, f"{team_slug}_detail.json")

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(team_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Guardado: {output_path}")
