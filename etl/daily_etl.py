# etl/daily_etl.py
import os
import json

teams = [
    {"name": "América", "slug": "america"},
    {"name": "Atlas", "slug": "atlas"},
    {"name": "Atlético San Luis", "slug": "atletico_san_luis"},
    {"name": "Cruz Azul", "slug": "cruz_azul"},
    {"name": "FC Juárez", "slug": "juarez"},
    {"name": "Guadalajara", "slug": "guadalajara"},
    {"name": "León", "slug": "leon"},
    {"name": "Mazatlán", "slug": "mazatlan"},
    {"name": "Monterrey", "slug": "monterrey"},
    {"name": "Necaxa", "slug": "necaxa"},
    {"name": "Pachuca", "slug": "pachuca"},
    {"name": "Puebla", "slug": "puebla"},
    {"name": "Pumas UNAM", "slug": "pumas_unam"},
    {"name": "Querétaro", "slug": "queretaro"},
    {"name": "Santos Laguna", "slug": "santos_laguna"},
    {"name": "Tigres UANL", "slug": "tigres_uanl"},
    {"name": "Toluca", "slug": "toluca"},
    {"name": "Tijuana", "slug": "tijuana"}
]

os.makedirs("../data/teams/liga_mx", exist_ok=True)

summary = []
for team in teams:
    slug = team["slug"]
    icon = f"assets/icons/{slug}.png"
    summary.append({
        "name": team["name"],
        "slug": slug,
        "icon": icon
    })

    detail = {
        "name": team["name"],
        "slug": slug,
        "icon": icon,
        "description": f"{team['name']} is a Liga MX team.",
        "schedules": [],
        "players": [],
        "stats": {}
    }

    with open(f"../data/teams/liga_mx/{slug}_detail.json", "w", encoding="utf-8") as f:
        json.dump(detail, f, indent=2, ensure_ascii=False)

with open("../data/liga_mx_teams.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)

print("✅ ETL complete: teams and detail files written.")
