import requests
import pandas as pd

# Step 1: Fetch data from the endpoint
url = "https://www.thesportsdb.com/api/v1/json/123/search_all_teams.php?l=Mexican_Primera_League"
response = requests.get(url)

# Step 2: Parse JSON
data = response.json()

# Step 3: Normalize the 'teams' list into a DataFrame
teams = data.get("teams", [])
df = pd.json_normalize(teams)


# Step 4: save to csv
df.to_csv("liga_mx_teams.csv", index=False)
