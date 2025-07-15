import requests
import json
import os
import re

API_KEY = "123"  # Replace with your actual API key if needed
LEAGUE_TEAMS_URL = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}/search_all_teams.php?l=Mexican_Primera_League"

DATA_DIR = "data/teams/liga_mx"
os.makedirs(DATA_DIR, exist_ok=True)


def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def fetch_liga_mx_teams():
    print("🔄 Fetching Liga MX teams...")
    response = requests.get(LEAGUE_TEAMS_URL)

    if response.status_code != 200:
        print(f"❌ Error fetching league data: {response.status_code}")
        return

    data = response.json()
    teams = data.get("teams", [])
    if not teams:
        print("⚠️ No teams found for Liga MX.")
        return

    teams_json = []

    for team in teams:
        team_name = team.get("strTeam")
        if not team_name:
            continue

        slug = slugify(team_name)
        icon_path = f"assets/icons/{slug}.png"  # Assumes PNGs with slugified names

        # Add summary
        summary = {
            "id": team.get("idTeam"),
            "name": team_name,
            "slug": slug,
            "icon": icon_path
        }
        teams_json.append(summary)

        # Save full team data
        detail_path = os.path.join(DATA_DIR, f"{slug}_detail.json")
        with open(detail_path, "w", encoding="utf-8") as f:
            json.dump(team, f, indent=2, ensure_ascii=False)

    # Save all team summaries
    with open("data/liga_mx_teams.json", "w", encoding="utf-8") as f:
        json.dump(teams_json, f, indent=2, ensure_ascii=False)

    print(f"✅ {len(teams_json)} Liga MX teams saved.")


if __name__ == "__main__":
    fetch_liga_mx_teams()
