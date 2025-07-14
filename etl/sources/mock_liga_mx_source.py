# etl/sources/mock_liga_mx_source.py
def get_all_teams():
    return [
        {
            "name": "Club América",
            "coach": "André Jardine",
            "stadium": "Estadio Azteca",
            "ranking": 1,
            "games_played": 17,
            "wins": 12,
            "draws": 3,
            "losses": 2,
            "goals_scored": 34,
            "goals_against": 18,
            "top_scorer": {
                "name": "Henry Martín",
                "goals": 11
            },
            "next_match": {
                "opponent": "Cruz Azul",
                "date": "2025-07-14",
                "location": "Estadio Azteca"
            }
        },
        {
            "name": "Cruz Azul",
            "coach": "Martín Anselmi",
            "stadium": "Estadio Azul",
            "ranking": 2,
            "games_played": 17,
            "wins": 11,
            "draws": 4,
            "losses": 2,
            "goals_scored": 30,
            "goals_against": 19,
            "top_scorer": {
                "name": "Uriel Antuna",
                "goals": 9
            },
            "next_match": {
                "opponent": "Club América",
                "date": "2025-07-14",
                "location": "Estadio Azteca"
            }
        },
        {
            "name": "Tigres UANL",
            "coach": "Guido Pizarro",
            "stadium": "Estadio Universitario",
            "ranking": 4,
            "games_played": 17,
            "wins": 11,
            "draws": 4,
            "losses": 2,
            "goals_scored": 30,
            "goals_against": 19,
            "top_scorer": {
                "name": "Juan Brunetta",
                "goals": 5
            },
            "next_match": {
                "opponent": "Juárez",
                "date": "2025-07-18",
                "location": "Estadio Juárez"
            }
        }
        # Add more if needed
    ]
