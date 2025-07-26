import requests
from bs4 import BeautifulSoup

BASE_URL = "https://int.soccerway.com"
START_URL = f"{BASE_URL}/national/mexico/primera-division/"

headers = {"User-Agent": "Mozilla/5.0"}

def get_current_season_url():
    res = requests.get(START_URL, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    links = soup.select("div#page_competition_1_block_competition_seasonlist_1 a")

    for link in links:
        if "apertura" in link['href'].lower():
            return BASE_URL + link['href']
    return None

def get_game_week_matches(season_url):
    res = requests.get(season_url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    # Go to Fixtures tab
    fixtures_tab = soup.find("a", string="Fixtures & Results")
    if not fixtures_tab:
        print("❌ Could not find Fixtures tab.")
        return []

    fixtures_url = BASE_URL + fixtures_tab['href']
    res = requests.get(fixtures_url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    matches = []
    for row in soup.select("table.matches tbody tr"):
        cols = row.find_all("td")
        if not cols or len(cols) < 5:
            continue

        date = cols[0].get_text(strip=True)
        time = cols[1].get_text(strip=True)
        home_team = cols[2].get_text(strip=True)
        away_team = cols[4].get_text(strip=True)
        score = cols[3].get_text(strip=True)

        matches.append({
            "date": date,
            "time": time,
            "home_team": home_team,
            "away_team": away_team,
            "score": score
        })

    return matches

# Example usage:
season_url = get_current_season_url()
if season_url:
    print(f"📅 Found season: {season_url}")
    game_week_matches = get_game_week_matches(season_url)

    for match in game_week_matches:
        print(f"{match['date']} {match['time']} — {match['home_team']} vs {match['away_team']} [{match['score']}]")
else:
    print("⚠️ Could not find current season.")
